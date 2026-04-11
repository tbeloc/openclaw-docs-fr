---
title: "Codex Harness"
summary: "Exécutez les tours d'agent intégrés OpenClaw via le harnais bundlé Codex app-server"
read_when:
  - You want to use the bundled Codex app-server harness
  - You need Codex model refs and config examples
  - You want to disable PI fallback for Codex-only deployments
---

# Codex Harness

Le plugin `codex` bundlé permet à OpenClaw d'exécuter les tours d'agent intégrés via
le Codex app-server au lieu du harnais PI intégré.

Utilisez ceci quand vous voulez que Codex possède la session d'agent de bas niveau : découverte de modèle,
reprise de thread natif, compaction natif, et exécution app-server.
OpenClaw conserve toujours les canaux de chat, les fichiers de session, la sélection de modèle, les outils,
les approbations, la livraison de médias, et le miroir de transcription visible.

Le harnais est désactivé par défaut. Il est sélectionné uniquement quand le plugin `codex` est
activé et que le modèle résolu est un modèle `codex/*`, ou quand vous forcez explicitement
`embeddedHarness.runtime: "codex"` ou `OPENCLAW_AGENT_RUNTIME=codex`.
Si vous ne configurez jamais `codex/*`, les exécutions PI, OpenAI, Anthropic, Gemini, locales,
et de fournisseur personnalisé existantes conservent leur comportement actuel.

## Choisir le bon préfixe de modèle

OpenClaw a des routes séparées pour l'accès OpenAI et Codex :

| Référence de modèle    | Chemin d'exécution                                | Utiliser quand                                                                |
| ---------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------- |
| `openai/gpt-5.4`       | Fournisseur OpenAI via plomberie OpenClaw/PI     | Vous voulez un accès direct à l'API OpenAI Platform avec `OPENAI_API_KEY`.    |
| `openai-codex/gpt-5.4` | Fournisseur OpenAI Codex OAuth via PI            | Vous voulez ChatGPT/Codex OAuth sans le harnais app-server Codex.            |
| `codex/gpt-5.4`        | Fournisseur Codex bundlé plus harnais Codex      | Vous voulez l'exécution native Codex app-server pour le tour d'agent intégré. |

Le harnais Codex ne revendique que les références de modèle `codex/*`. Les références `openai/*`,
`openai-codex/*`, Anthropic, Gemini, xAI, locales, et de fournisseur personnalisé existantes conservent
leurs chemins normaux.

## Exigences

- OpenClaw avec le plugin `codex` bundlé disponible.
- Codex app-server `0.118.0` ou plus récent.
- Authentification Codex disponible pour le processus app-server.

Le plugin bloque les poignées de main app-server plus anciennes ou sans version. Cela maintient
OpenClaw sur la surface de protocole contre laquelle il a été testé.

Pour les tests de fumée en direct et Docker, l'authentification provient généralement de `OPENAI_API_KEY`, plus
les fichiers Codex CLI optionnels tels que `~/.codex/auth.json` et
`~/.codex/config.toml`. Utilisez le même matériel d'authentification que votre app-server Codex local.

## Configuration minimale

Utilisez `codex/gpt-5.4`, activez le plugin bundlé, et forcez le harnais `codex` :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
  agents: {
    defaults: {
      model: "codex/gpt-5.4",
      embeddedHarness: {
        runtime: "codex",
        fallback: "none",
      },
    },
  },
}
```

Si votre config utilise `plugins.allow`, incluez `codex` là aussi :

```json5
{
  plugins: {
    allow: ["codex"],
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

Définir `agents.defaults.model` ou un modèle d'agent sur `codex/<model>` active également
automatiquement le plugin `codex` bundlé. L'entrée de plugin explicite est toujours
utile dans les configs partagées car elle rend l'intention de déploiement évidente.

## Ajouter Codex sans remplacer d'autres modèles

Gardez `runtime: "auto"` quand vous voulez Codex pour les modèles `codex/*` et PI pour
tout le reste :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
  agents: {
    defaults: {
      model: {
        primary: "codex/gpt-5.4",
        fallbacks: ["openai/gpt-5.4", "anthropic/claude-opus-4-6"],
      },
      models: {
        "codex/gpt-5.4": { alias: "codex" },
        "codex/gpt-5.4-mini": { alias: "codex-mini" },
        "openai/gpt-5.4": { alias: "gpt" },
        "anthropic/claude-opus-4-6": { alias: "opus" },
      },
      embeddedHarness: {
        runtime: "auto",
        fallback: "pi",
      },
    },
  },
}
```

Avec cette forme :

- `/model codex` ou `/model codex/gpt-5.4` utilise le harnais app-server Codex.
- `/model gpt` ou `/model openai/gpt-5.4` utilise le chemin du fournisseur OpenAI.
- `/model opus` utilise le chemin du fournisseur Anthropic.
- Si un modèle non-Codex est sélectionné, PI reste le harnais de compatibilité.

## Déploiements Codex uniquement

Désactivez le fallback PI quand vous avez besoin de prouver que chaque tour d'agent intégré utilise
le harnais Codex :

```json5
{
  agents: {
    defaults: {
      model: "codex/gpt-5.4",
      embeddedHarness: {
        runtime: "codex",
        fallback: "none",
      },
    },
  },
}
```

Remplacement d'environnement :

```bash
OPENCLAW_AGENT_RUNTIME=codex \
OPENCLAW_AGENT_HARNESS_FALLBACK=none \
openclaw gateway run
```

Avec le fallback désactivé, OpenClaw échoue rapidement si le plugin Codex est désactivé,
le modèle demandé n'est pas une référence `codex/*`, l'app-server est trop ancien, ou l'
app-server ne peut pas démarrer.

## Codex par agent

Vous pouvez rendre un agent Codex uniquement tandis que l'agent par défaut conserve la
sélection automatique normale :

```json5
{
  agents: {
    defaults: {
      embeddedHarness: {
        runtime: "auto",
        fallback: "pi",
      },
    },
    list: [
      {
        id: "main",
        default: true,
        model: "anthropic/claude-opus-4-6",
      },
      {
        id: "codex",
        name: "Codex",
        model: "codex/gpt-5.4",
        embeddedHarness: {
          runtime: "codex",
          fallback: "none",
        },
      },
    ],
  },
}
```

Utilisez les commandes de session normales pour basculer les agents et les modèles. `/new` crée une nouvelle
session OpenClaw et le harnais Codex crée ou reprend son thread app-server sidecar selon les besoins. `/reset` efface
la liaison de session OpenClaw pour ce thread.

## Découverte de modèle

Par défaut, le plugin Codex demande à l'app-server les modèles disponibles. Si
la découverte échoue ou expire, il utilise le catalogue de fallback bundlé :

- `codex/gpt-5.4`
- `codex/gpt-5.4-mini`
- `codex/gpt-5.2`

Vous pouvez affiner la découverte sous `plugins.entries.codex.config.discovery` :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          discovery: {
            enabled: true,
            timeoutMs: 2500,
          },
        },
      },
    },
  },
}
```

Désactivez la découverte quand vous voulez que le démarrage évite de sonder Codex et s'en tienne au
catalogue de fallback :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          discovery: {
            enabled: false,
          },
        },
      },
    },
  },
}
```

## Connexion app-server et politique

Par défaut, le plugin démarre Codex localement avec :

```bash
codex app-server --listen stdio://
```

Vous pouvez conserver ce défaut et seulement affiner la politique native Codex :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            approvalPolicy: "on-request",
            sandbox: "workspace-write",
            serviceTier: "priority",
          },
        },
      },
    },
  },
}
```

Pour un app-server déjà en cours d'exécution, utilisez le transport WebSocket :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            transport: "websocket",
            url: "ws://127.0.0.1:39175",
            authToken: "${CODEX_APP_SERVER_TOKEN}",
            requestTimeoutMs: 60000,
          },
        },
      },
    },
  },
}
```

Champs `appServer` supportés :

| Champ               | Défaut                                   | Signification                                                              |
| ------------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| `transport`         | `"stdio"`                                | `"stdio"` démarre Codex; `"websocket"` se connecte à `url`.                |
| `command`           | `"codex"`                                | Exécutable pour le transport stdio.                                        |
| `args`              | `["app-server", "--listen", "stdio://"]` | Arguments pour le transport stdio.                                         |
| `url`               | non défini                               | URL app-server WebSocket.                                                  |
| `authToken`         | non défini                               | Jeton Bearer pour le transport WebSocket.                                  |
| `headers`           | `{}`                                     | En-têtes WebSocket supplémentaires.                                        |
| `requestTimeoutMs`  | `60000`                                  | Délai d'expiration pour les appels du plan de contrôle app-server.         |
| `approvalPolicy`    | `"never"`                                | Politique d'approbation Codex native envoyée au démarrage/reprise/tour.    |
| `sandbox`           | `"workspace-write"`                      | Mode sandbox Codex natif envoyé au démarrage/reprise.                     |
| `approvalsReviewer` | `"user"`                                 | Utilisez `"guardian_subagent"` pour laisser Codex guardian examiner les approbations natives. |
| `serviceTier`       | non défini                               | Niveau de service Codex optionnel, par exemple `"priority"`.               |

Les variables d'environnement plus anciennes fonctionnent toujours comme fallbacks pour les tests locaux quand
le champ de config correspondant n'est pas défini :

- `OPENCLAW_CODEX_APP_SERVER_BIN`
- `OPENCLAW_CODEX_APP_SERVER_ARGS`
- `OPENCLAW_CODEX_APP_SERVER_APPROVAL_POLICY`
- `OPENCLAW_CODEX_APP_SERVER_SANDBOX`
- `OPENCLAW_CODEX_APP_SERVER_GUARDIAN=1`

La config est préférée pour les déploiements reproductibles.

## Recettes courantes

Codex local avec transport stdio par défaut :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

Validation du harnais Codex uniquement, avec fallback PI désactivé :

```json5
{
  embeddedHarness: {
    fallback: "none",
  },
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

Approbations Codex examinées par Guardian :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            approvalPolicy: "on-request",
            approvalsReviewer: "guardian_subagent",
            sandbox: "workspace-write",
          },
        },
      },
    },
  },
}
```

App-server distant avec en-têtes explicites :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            transport: "websocket",
            url: "ws://gateway-host:39175",
            headers: {
              "X-OpenClaw-Agent": "main",
            },
          },
        },
      },
    },
  },
}
```

La commutation de modèle reste contrôlée par OpenClaw. Quand une session OpenClaw est attachée
à un thread Codex existant, le prochain tour envoie le modèle `codex/*` actuellement sélectionné,
le fournisseur, la politique d'approbation, le sandbox, et le niveau de service à
l'app-server à nouveau. Basculer de `codex/gpt-5.4` à `codex/gpt-5.2` conserve la
liaison de thread mais demande à Codex de continuer avec le modèle nouvellement sélectionné.

## Commande Codex

Le plugin fourni enregistre `/codex` comme commande slash autorisée. C'est une
commande générique qui fonctionne sur n'importe quel canal supportant les commandes
texte OpenClaw.

Formes courantes :

- `/codex status` affiche la connectivité en direct du serveur d'application, les modèles, le compte, les limites de débit, les serveurs MCP et les compétences.
- `/codex models` liste les modèles du serveur d'application Codex en direct.
- `/codex threads [filter]` liste les threads Codex récents.
- `/codex resume <thread-id>` attache la session OpenClaw actuelle à un thread Codex existant.
- `/codex compact` demande au serveur d'application Codex de compacter le thread attaché.
- `/codex review` démarre l'examen natif Codex pour le thread attaché.
- `/codex account` affiche le statut du compte et des limites de débit.
- `/codex mcp` liste le statut du serveur MCP du serveur d'application Codex.
- `/codex skills` liste les compétences du serveur d'application Codex.

`/codex resume` écrit le même fichier de liaison sidecar que celui utilisé par le
harnais pour les tours normaux. Au message suivant, OpenClaw reprend ce thread Codex,
transmet le modèle `codex/*` OpenClaw actuellement sélectionné au serveur d'application,
et maintient l'historique étendu activé.

La surface de commande nécessite Codex app-server `0.118.0` ou plus récent. Les
méthodes de contrôle individuelles sont signalées comme `non supportées par ce serveur
d'application Codex` si un serveur d'application futur ou personnalisé n'expose pas
cette méthode JSON-RPC.

## Outils, médias et compaction

Le harnais Codex ne modifie que l'exécuteur d'agent intégré de bas niveau.

OpenClaw construit toujours la liste des outils et reçoit les résultats dynamiques
des outils du harnais. Le texte, les images, les vidéos, la musique, la synthèse vocale,
les approbations et la sortie des outils de messagerie continuent à passer par le
chemin de livraison normal d'OpenClaw.

Lorsque le modèle sélectionné utilise le harnais Codex, la compaction native des
threads est déléguée au serveur d'application Codex. OpenClaw conserve un miroir de
transcription pour l'historique des canaux, la recherche, `/new`, `/reset` et les
changements futurs de modèle ou de harnais. Le miroir inclut l'invite utilisateur,
le texte final de l'assistant, et les enregistrements légers de raisonnement ou de
plan Codex lorsque le serveur d'application les émet.

La génération de médias ne nécessite pas PI. La génération d'images, vidéos, musique,
PDF, synthèse vocale et la compréhension des médias continuent à utiliser les
paramètres de fournisseur/modèle correspondants tels que `agents.defaults.imageGenerationModel`,
`videoGenerationModel`, `pdfModel` et `messages.tts`.

## Dépannage

**Codex n'apparaît pas dans `/model` :** activez `plugins.entries.codex.enabled`,
définissez une référence de modèle `codex/*`, ou vérifiez si `plugins.allow` exclut `codex`.

**OpenClaw revient à PI :** définissez `embeddedHarness.fallback: "none"` ou
`OPENCLAW_AGENT_HARNESS_FALLBACK=none` lors des tests.

**Le serveur d'application est rejeté :** mettez à jour Codex pour que la négociation
du serveur d'application signale la version `0.118.0` ou plus récente.

**La découverte de modèles est lente :** réduisez `plugins.entries.codex.config.discovery.timeoutMs`
ou désactivez la découverte.

**Le transport WebSocket échoue immédiatement :** vérifiez `appServer.url`, `authToken`,
et que le serveur d'application distant utilise la même version du protocole du serveur
d'application Codex.

**Un modèle non-Codex utilise PI :** c'est attendu. Le harnais Codex ne revendique que
les références de modèle `codex/*`.

## Connexes

- [Agent Harness Plugins](/fr/plugins/sdk-agent-harness)
- [Model Providers](/fr/concepts/model-providers)
- [Configuration Reference](/fr/gateway/configuration-reference)
- [Testing](/fr/help/testing#live-codex-app-server-harness-smoke)
