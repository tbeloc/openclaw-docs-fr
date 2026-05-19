---
summary: "Configuration, auth, discovery, and app-server reference for the Codex harness"
title: "Codex harness reference"
read_when:
  - You need every Codex harness config field
  - You are changing app-server transport, auth, discovery, or timeout behavior
  - You are debugging Codex harness startup, model discovery, or environment isolation
---

Cette référence couvre la configuration détaillée du plugin `codex` fourni. Pour les décisions de configuration et de routage, commencez par [Codex harness](/fr/plugins/codex-harness).

## Surface de configuration du plugin

Tous les paramètres du harnais Codex se trouvent sous `plugins.entries.codex.config`.

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
          appServer: {
            mode: "guardian",
          },
        },
      },
    },
  },
}
```

Champs de niveau supérieur pris en charge :

| Champ                      | Défaut                   | Signification                                                                                                                                   |
| -------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `discovery`                | activé                  | Paramètres de découverte de modèle pour `model/list` du serveur d'application Codex.                                                                               |
| `appServer`                | serveur d'application stdio géré | Paramètres de transport, commande, authentification, approbation, sandbox et délai d'expiration.                                                                        |
| `codexDynamicToolsLoading` | `"searchable"`           | Utilisez `"direct"` pour placer les outils dynamiques OpenClaw directement dans le contexte d'outil Codex initial.                                                  |
| `codexDynamicToolsExclude` | `[]`                     | Noms d'outils dynamiques OpenClaw supplémentaires à omettre des tours du serveur d'application Codex.                                                               |
| `codexPlugins`             | désactivé                 | Support natif des plugins/applications Codex pour les plugins organisés installés à partir de la source migrés. Voir [Native Codex plugins](/fr/plugins/codex-native-plugins). |
| `computerUse`              | désactivé                 | Configuration de Codex Computer Use. Voir [Codex Computer Use](/fr/plugins/codex-computer-use).                                                          |

## Transport du serveur d'application

Par défaut, OpenClaw démarre le binaire Codex géré fourni avec le plugin fourni :

```bash
codex app-server --listen stdio://
```

Cela maintient la version du serveur d'application liée au plugin `codex` fourni plutôt qu'à la CLI Codex installée localement. Définissez `appServer.command` uniquement lorsque vous souhaitez intentionnellement exécuter un exécutable différent.

Pour un serveur d'application déjà en cours d'exécution, utilisez le transport WebSocket :

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
            authToken: "${CODEX_APP_SERVER_TOKEN}",
            requestTimeoutMs: 60000,
          },
        },
      },
    },
  },
}
```

Champs `appServer` pris en charge :

| Champ                         | Défaut                                                | Signification                                                                                                                                                                                                   |
| ----------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `transport`                   | `"stdio"`                                              | `"stdio"` démarre Codex ; `"websocket"` se connecte à `url`.                                                                                                                                                  |
| `command`                     | binaire Codex géré                                   | Exécutable pour le transport stdio. Laissez non défini pour utiliser le binaire géré.                                                                                                                                    |
| `args`                        | `["app-server", "--listen", "stdio://"]`               | Arguments pour le transport stdio.                                                                                                                                                            |
| `url`                         | non défini                                                  | URL du serveur d'application WebSocket.                                                                                                                                                                                 |
| `authToken`                   | non défini                                                  | Jeton Bearer pour le transport WebSocket.                                                                                                                                                                     |
| `headers`                     | `{}`                                                   | En-têtes WebSocket supplémentaires.                                                                                                                                                                                                  |
| `clearEnv`                    | `[]`                                                   | Noms de variables d'environnement supplémentaires supprimés du processus du serveur d'application stdio généré après qu'OpenClaw ait construit son environnement hérité.                                                                       |
| `requestTimeoutMs`            | `60000`                                                | Délai d'expiration pour les appels du plan de contrôle du serveur d'application.                                                                                                                                                               |
| `turnCompletionIdleTimeoutMs` | `60000`                                                | Fenêtre silencieuse après que Codex accepte un tour ou après une demande du serveur d'application limitée au tour tandis qu'OpenClaw attend `turn/completed`.                                                                              |
| `mode`                        | `"yolo"` sauf si les exigences locales de Codex interdisent YOLO | Préréglage pour l'exécution examinée par YOLO ou gardien.                                                                                                                                                           |
| `approvalPolicy`              | `"never"` ou une politique d'approbation gardien autorisée       | Politique d'approbation Codex native envoyée au démarrage du thread, à la reprise et au tour.                                                                                                                                      |
| `sandbox`                     | `"danger-full-access"` ou un sandbox gardien autorisé  | Mode sandbox Codex natif envoyé au démarrage et à la reprise du thread. Les sandboxes OpenClaw actifs réduisent les tours `danger-full-access` à Codex `workspace-write` ; l'indicateur réseau du tour suit l'accès sortant du sandbox OpenClaw. |
| `approvalsReviewer`           | `"user"` ou un examinateur gardien autorisé               | Utilisez `"auto_review"` pour laisser Codex examiner les invites d'approbation natives lorsque cela est autorisé.                                                                                                                                                  |
| `defaultWorkspaceDir`         | répertoire du processus actuel                              | Espace de travail utilisé par `/codex bind` lorsque `--cwd` est omis.                                                                                                                                                  |
| `serviceTier`                 | non défini                                                  | Niveau de service du serveur d'application Codex optionnel. `"priority"` active le routage en mode rapide, `"flex"` demande un traitement flex, et `null` efface le remplacement. L'ancien `"fast"` est accepté comme `"priority"`.           |

Le plugin bloque les poignées de main du serveur d'application plus anciennes ou sans version. Le serveur d'application Codex doit signaler la version stable `0.125.0` ou plus récente.

## Modes d'approbation et de sandbox

Les sessions du serveur d'application stdio local utilisent par défaut le mode YOLO :
`approvalPolicy: "never"`, `approvalsReviewer: "user"`, et
`sandbox: "danger-full-access"`. Cette posture d'opérateur local de confiance permet aux tours OpenClaw sans surveillance et aux battements de cœur de progresser sans invites d'approbation natives auxquelles personne n'est là pour répondre.

Si le fichier d'exigences du système local de Codex interdit l'approbation YOLO implicite, l'examinateur ou les valeurs de sandbox, OpenClaw traite la valeur par défaut implicite comme gardien à la place et sélectionne les autorisations gardien autorisées. Les entrées `[[remote_sandbox_config]]` correspondant au nom d'hôte dans le même fichier d'exigences sont honorées pour la décision de défaut du sandbox.

Définissez `appServer.mode: "guardian"` pour les approbations examinées par le gardien Codex :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            mode: "guardian",
            serviceTier: "priority",
          },
        },
      },
    },
  },
}
```

Le préréglage `guardian` se développe en `approvalPolicy: "on-request"`,
`approvalsReviewer: "auto_review"`, et `sandbox: "workspace-write"` lorsque ces
valeurs sont autorisées. Les champs de politique individuels remplacent `mode`. La valeur d'examinateur `guardian_subagent` plus ancienne est toujours acceptée comme alias de compatibilité,
mais les nouvelles configurations doivent utiliser `auto_review`.

Lorsqu'un sandbox OpenClaw est actif, le processus du serveur d'application Codex local s'exécute toujours sur l'hôte Gateway. OpenClaw maintient donc le sandbox du système de fichiers propre à Codex pour les tours en mode code natif. Les tours `danger-full-access` sont réduites à Codex `workspace-write`, et le `networkAccess` du tour `workspace-write` est dérivé du paramètre d'accès sortant du sandbox OpenClaw : Docker `network: "none"` reste hors ligne, tandis que `network: "bridge"` ou un réseau Docker personnalisé permet l'accès sortant.

## Authentification et isolation de l'environnement

L'authentification est sélectionnée dans cet ordre :

1. Un profil d'authentification OpenClaw Codex explicite pour l'agent.
2. Le compte existant du serveur d'application dans le répertoire Codex de cet agent.
3. Pour les lancements locaux du serveur d'application stdio uniquement, `CODEX_API_KEY`, puis
   `OPENAI_API_KEY`, quand aucun compte de serveur d'application n'est présent et que l'authentification OpenAI est
   toujours requise.

Quand OpenClaw voit un profil d'authentification Codex de style abonnement ChatGPT, il supprime
`CODEX_API_KEY` et `OPENAI_API_KEY` du processus enfant Codex généré. Cela
garde les clés API au niveau de la passerelle disponibles pour les embeddings ou les modèles OpenAI directs
sans faire facturer accidentellement les tours du serveur d'application Codex natif via l'API.

Les profils de clé API Codex explicites et le recours aux clés d'environnement stdio local utilisent la connexion au serveur d'application
au lieu de l'environnement du processus enfant hérité. Les connexions du serveur d'application WebSocket
ne reçoivent pas le recours aux clés API d'environnement de la passerelle ; utilisez un profil d'authentification explicite ou le
compte propre du serveur d'application distant.

Les lancements du serveur d'application stdio héritent de l'environnement du processus OpenClaw par défaut.
OpenClaw possède le pont de compte du serveur d'application Codex et définit `CODEX_HOME` sur un
répertoire par agent sous l'état OpenClaw de cet agent. Cela garde la configuration Codex, les
comptes, le cache/les données des plugins et l'état des threads limités à l'agent OpenClaw
au lieu de fuir depuis le répertoire personnel `~/.codex` de l'opérateur.

OpenClaw ne réécrit pas `HOME` pour les lancements normaux du serveur d'application local. Les
sous-processus exécutés par Codex tels que `openclaw`, `gh`, `git`, les CLI cloud et les commandes shell voient
le répertoire personnel du processus normal et peuvent trouver la configuration et les jetons du répertoire personnel de l'utilisateur. Codex peut également
découvrir `$HOME/.agents/skills` et `$HOME/.agents/plugins/marketplace.json` ;
cette découverte `.agents` est intentionnellement partagée avec le répertoire personnel de l'opérateur et est
séparée de l'état isolé `~/.codex`.

Les plugins OpenClaw et les snapshots de compétences OpenClaw circulent toujours via le
registre de plugins propre d'OpenClaw et le chargeur de compétences. Les actifs Codex personnels `~/.codex` ne le font pas. Si
vous avez des compétences ou des plugins CLI Codex utiles provenant d'un répertoire Codex qui devraient devenir
partie d'un agent OpenClaw, inventoriez-les explicitement :

```bash
openclaw migrate codex --dry-run
openclaw migrate apply codex --yes
```

Si un déploiement nécessite une isolation d'environnement supplémentaire, ajoutez ces variables à
`appServer.clearEnv` :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            clearEnv: ["CODEX_API_KEY", "OPENAI_API_KEY"],
          },
        },
      },
    },
  },
}
```

`appServer.clearEnv` affecte uniquement le processus enfant du serveur d'application Codex généré.
OpenClaw supprime `CODEX_HOME` et `HOME` de cette liste lors de la normalisation du lancement local : `CODEX_HOME`
reste par agent, et `HOME` reste hérité pour que les sous-processus puissent utiliser l'état normal du répertoire personnel de l'utilisateur.

## Outils dynamiques

Les outils dynamiques Codex sont par défaut chargés en mode `searchable`. OpenClaw n'expose pas
les outils dynamiques qui dupliquent les opérations natives du workspace Codex :

- `read`
- `write`
- `edit`
- `apply_patch`
- `exec`
- `process`
- `update_plan`

La plupart des outils d'intégration OpenClaw restants, tels que la messagerie, les médias, cron,
le navigateur, les nœuds, la passerelle, `heartbeat_respond` et `web_search`, sont disponibles
via la recherche d'outils Codex sous l'espace de noms `openclaw`. Cela garde le contexte initial
du modèle plus petit. `sessions_yield` et les réponses source de message-tool-only
restent directs car ce sont des contrats de contrôle de tour. `sessions_spawn` reste
searchable pour que le `spawn_agent` natif de Codex reste la surface de sous-agent Codex primaire, tandis que la
délégation OpenClaw ou ACP explicite est toujours disponible via
l'espace de noms d'outil dynamique `openclaw`.

Définissez `codexDynamicToolsLoading: "direct"` uniquement lors de la connexion à un serveur d'application Codex personnalisé
qui ne peut pas rechercher des outils dynamiques différés ou lors du débogage de la charge utile complète des outils.

## Délais d'expiration

Les appels d'outils dynamiques appartenant à OpenClaw sont limités indépendamment de
`appServer.requestTimeoutMs`. Chaque demande Codex `item/tool/call` utilise le premier
délai d'expiration disponible dans cet ordre :

- Un argument `timeoutMs` par appel positif.
- Pour `image_generate`, `agents.defaults.imageGenerationModel.timeoutMs`.
- Pour l'outil `image` de compréhension des médias, `tools.media.image.timeoutSeconds`
  converti en millisecondes, ou le défaut de 60 secondes pour les médias.
- Le défaut de 30 secondes pour les outils dynamiques.

Les budgets des outils dynamiques sont plafonnés à 600000 ms. En cas de dépassement du délai, OpenClaw interrompt le
signal de l'outil où cela est supporté et retourne une réponse d'outil dynamique échouée à Codex
pour que le tour puisse continuer au lieu de laisser la session en `processing`.

Après que Codex accepte un tour, et après qu'OpenClaw répond à une demande du serveur d'application limitée au tour, le
harnais s'attend à ce que Codex fasse des progrès sur le tour actuel et finisse finalement le tour natif avec `turn/completed`. Si le serveur d'application reste silencieux pendant `appServer.turnCompletionIdleTimeoutMs`, OpenClaw
interrompt au mieux le tour Codex, enregistre un diagnostic de délai d'expiration et libère la
voie de session OpenClaw pour que les messages de chat de suivi ne soient pas mis en file d'attente derrière un tour natif obsolète.

La plupart des notifications non terminales pour le même tour désarment ce court chien de garde
car Codex a prouvé que le tour est toujours actif. Les complétions brutes `custom_tool_call_output`
gardent le court chien de garde post-outil armé car ce sont la remise de résultat d'outil limitée au tour. Les éléments `agentMessage` complétés et les éléments bruts d'assistant pré-outil `rawResponseItem/completed` arment la libération de sortie d'assistant : si
Codex reste ensuite silencieux sans `turn/completed`, OpenClaw interrompt au mieux le tour natif et libère la voie de session. Le progrès brut d'assistant post-outil continue d'attendre `turn/completed` ou le chien de garde terminal. Les diagnostics de délai d'expiration incluent la dernière méthode de notification du serveur d'application et, pour les éléments de réponse d'assistant bruts, le type d'élément, le rôle, l'id et un aperçu de texte d'assistant limité.

## Découverte de modèles

Par défaut, le plugin Codex demande au serveur d'application les modèles disponibles. La disponibilité des modèles est
possédée par le serveur d'application Codex, donc la liste peut changer quand OpenClaw
met à niveau la version `@openai/codex` fournie ou quand un déploiement pointe
`appServer.command` vers un binaire Codex différent. La disponibilité peut également
être limitée au compte. Utilisez `/codex models` sur une passerelle en cours d'exécution pour voir le catalogue en direct
pour ce harnais et ce compte.

Si la découverte échoue ou expire, OpenClaw utilise un catalogue de secours fourni pour :

- GPT-5.5
- GPT-5.4 mini
- GPT-5.2

Le harnais fourni actuel est `@openai/codex` `0.130.0`. Une sonde `model/list`
contre ce serveur d'application fourni a retourné :

| ID du modèle          | Par défaut | Caché | Modalités d'entrée | Efforts de raisonnement  |
| --------------------- | ---------- | ----- | ------------------ | ------------------------ |
| `gpt-5.5`             | Oui        | Non   | texte, image       | bas, moyen, haut, xhaut  |
| `gpt-5.4`             | Non        | Non   | texte, image       | bas, moyen, haut, xhaut  |
| `gpt-5.4-mini`        | Non        | Non   | texte, image       | bas, moyen, haut, xhaut  |
| `gpt-5.3-codex`       | Non        | Non   | texte, image       | bas, moyen, haut, xhaut  |
| `gpt-5.3-codex-spark` | Non        | Non   | texte              | bas, moyen, haut, xhaut  |
| `gpt-5.2`             | Non        | Non   | texte, image       | bas, moyen, haut, xhaut  |

Les modèles cachés peuvent être retournés par le catalogue du serveur d'application pour des flux internes ou
spécialisés, mais ce ne sont pas des choix normaux du sélecteur de modèles.

Affinez la découverte sous `plugins.entries.codex.config.discovery` :

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

Désactivez la découverte quand vous voulez que le démarrage évite de sonder Codex et utilise uniquement le
catalogue de secours :

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

## Fichiers d'amorçage du workspace

Codex gère `AGENTS.md` lui-même via la découverte native de documentation de projet. OpenClaw
n'écrit pas de fichiers de documentation de projet Codex synthétiques ni ne dépend des noms de fichiers de secours Codex
pour les fichiers de persona, car les secours Codex ne s'appliquent que quand
`AGENTS.md` est manquant.

Pour la parité du workspace OpenClaw, le harnais Codex résout les autres fichiers
d'amorçage, y compris `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`,
`HEARTBEAT.md`, `BOOTSTRAP.md` et `MEMORY.md` quand présents, et les transmet
comme contexte de référence d'entrée de tour OpenClaw. Cela garde le contexte de persona et de profil du workspace
visible au tour Codex natif sans le promouvoir au-dessus des instructions système/développeur possédées par Codex ou
dupliquer `AGENTS.md`.

## Remplacements d'environnement

Les remplacements d'environnement restent disponibles pour les tests locaux :

- `OPENCLAW_CODEX_APP_SERVER_BIN`
- `OPENCLAW_CODEX_APP_SERVER_ARGS`
- `OPENCLAW_CODEX_APP_SERVER_MODE=yolo|guardian`
- `OPENCLAW_CODEX_APP_SERVER_APPROVAL_POLICY`
- `OPENCLAW_CODEX_APP_SERVER_SANDBOX`

`OPENCLAW_CODEX_APP_SERVER_BIN` contourne le binaire géré quand
`appServer.command` n'est pas défini.

`OPENCLAW_CODEX_APP_SERVER_GUARDIAN=1` a été supprimé. Utilisez
`plugins.entries.codex.config.appServer.mode: "guardian"` à la place, ou
`OPENCLAW_CODEX_APP_SERVER_MODE=guardian` pour les tests locaux ponctuels. La configuration est
préférée pour les déploiements reproductibles car elle garde le comportement du plugin dans le
même fichier examiné que le reste de la configuration du harnais Codex.

## Connexes

- [Harnais Codex](/fr/plugins/codex-harness)
- [Runtime du harnais Codex](/fr/plugins/codex-harness-runtime)
- [Plugins Codex natifs](/fr/plugins/codex-native-plugins)
- [Codex Computer Use](/fr/plugins/codex-computer-use)
- [Fournisseur OpenAI](/fr/providers/openai)
- [Référence de configuration](/fr/gateway/configuration-reference)
