---
summary: "Aperçu de la configuration : tâches courantes, configuration rapide et liens vers la référence complète"
read_when:
  - Setting up OpenClaw for the first time
  - Looking for common configuration patterns
  - Navigating to specific config sections
title: "Configuration"
---

# Configuration

OpenClaw lit une configuration <Tooltip tip="JSON5 supports comments and trailing commas">**JSON5**</Tooltip> optionnelle depuis `~/.openclaw/openclaw.json`.

Si le fichier est absent, OpenClaw utilise des valeurs par défaut sûres. Les raisons courantes d'ajouter une configuration :

- Connecter des canaux et contrôler qui peut envoyer des messages au bot
- Définir les modèles, outils, sandboxing ou automatisation (cron, hooks)
- Ajuster les sessions, médias, réseau ou interface utilisateur

Consultez la [référence complète](/gateway/configuration-reference) pour tous les champs disponibles.

<Tip>
**Nouveau dans la configuration ?** Commencez par `openclaw onboard` pour une configuration interactive, ou consultez le guide [Exemples de configuration](/gateway/configuration-examples) pour des configurations complètes prêtes à copier-coller.
</Tip>

## Configuration minimale

```json5
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

## Édition de la configuration

<Tabs>
  <Tab title="Assistant interactif">
    ```bash
    openclaw onboard       # assistant de configuration complet
    openclaw configure     # assistant de configuration
    ```
  </Tab>
  <Tab title="CLI (commandes uniques)">
    ```bash
    openclaw config get agents.defaults.workspace
    openclaw config set agents.defaults.heartbeat.every "2h"
    openclaw config unset tools.web.search.apiKey
    ```
  </Tab>
  <Tab title="Interface de contrôle">
    Ouvrez [http://127.0.0.1:18789](http://127.0.0.1:18789) et utilisez l'onglet **Config**.
    L'interface de contrôle affiche un formulaire généré à partir du schéma de configuration, avec un éditeur **JSON brut** comme solution de secours.
  </Tab>
  <Tab title="Édition directe">
    Éditez `~/.openclaw/openclaw.json` directement. La Gateway surveille le fichier et applique les modifications automatiquement (voir [rechargement à chaud](#config-hot-reload)).
  </Tab>
</Tabs>

## Validation stricte

<Warning>
OpenClaw n'accepte que les configurations qui correspondent exactement au schéma. Les clés inconnues, les types mal formés ou les valeurs invalides causent le **refus de démarrage** de la Gateway. La seule exception au niveau racine est `$schema` (chaîne), pour que les éditeurs puissent joindre des métadonnées de schéma JSON.
</Warning>

Quand la validation échoue :

- La Gateway ne démarre pas
- Seules les commandes de diagnostic fonctionnent (`openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`)
- Exécutez `openclaw doctor` pour voir les problèmes exacts
- Exécutez `openclaw doctor --fix` (ou `--yes`) pour appliquer les réparations

## Tâches courantes

<AccordionGroup>
  <Accordion title="Configurer un canal (WhatsApp, Telegram, Discord, etc.)">
    Chaque canal a sa propre section de configuration sous `channels.<provider>`. Consultez la page dédiée au canal pour les étapes de configuration :

    - [WhatsApp](/channels/whatsapp) — `channels.whatsapp`
    - [Telegram](/channels/telegram) — `channels.telegram`
    - [Discord](/channels/discord) — `channels.discord`
    - [Slack](/channels/slack) — `channels.slack`
    - [Signal](/channels/signal) — `channels.signal`
    - [iMessage](/channels/imessage) — `channels.imessage`
    - [Google Chat](/channels/googlechat) — `channels.googlechat`
    - [Mattermost](/channels/mattermost) — `channels.mattermost`
    - [MS Teams](/channels/msteams) — `channels.msteams`

    Tous les canaux partagent le même modèle de politique DM :

    ```json5
    {
      channels: {
        telegram: {
          enabled: true,
          botToken: "123:abc",
          dmPolicy: "pairing",   // pairing | allowlist | open | disabled
          allowFrom: ["tg:123"], // only for allowlist/open
        },
      },
    }
    ```

  </Accordion>

  <Accordion title="Choisir et configurer les modèles">
    Définissez le modèle principal et les alternatives optionnelles :

    ```json5
    {
      agents: {
        defaults: {
          model: {
            primary: "anthropic/claude-sonnet-4-5",
            fallbacks: ["openai/gpt-5.2"],
          },
          models: {
            "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
            "openai/gpt-5.2": { alias: "GPT" },
          },
        },
      },
    }
    ```

    - `agents.defaults.models` définit le catalogue des modèles et agit comme liste blanche pour `/model`.
    - Les références de modèles utilisent le format `provider/model` (par exemple `anthropic/claude-opus-4-6`).
    - `agents.defaults.imageMaxDimensionPx` contrôle la réduction d'échelle des images de transcription/outil (par défaut `1200`) ; les valeurs plus basses réduisent généralement l'utilisation des jetons de vision lors des exécutions chargées de captures d'écran.
    - Consultez [Models CLI](/concepts/models) pour changer de modèle dans le chat et [Model Failover](/concepts/model-failover) pour la rotation d'authentification et le comportement de secours.
    - Pour les fournisseurs personnalisés/auto-hébergés, consultez [Custom providers](/gateway/configuration-reference#custom-providers-and-base-urls) dans la référence.

  </Accordion>

  <Accordion title="Contrôler qui peut envoyer des messages au bot">
    L'accès DM est contrôlé par canal via `dmPolicy` :

    - `"pairing"` (par défaut) : les expéditeurs inconnus reçoivent un code d'appairage unique à approuver
    - `"allowlist"` : uniquement les expéditeurs dans `allowFrom` (ou le magasin d'appairage autorisé)
    - `"open"` : autoriser tous les DM entrants (nécessite `allowFrom: ["*"]`)
    - `"disabled"` : ignorer tous les DM

    Pour les groupes, utilisez `groupPolicy` + `groupAllowFrom` ou des listes blanches spécifiques au canal.

    Consultez la [référence complète](/gateway/configuration-reference#dm-and-group-access) pour les détails par canal.

  </Accordion>

  <Accordion title="Configurer la mention gating pour les chats de groupe">
    Les messages de groupe nécessitent par défaut une **mention**. Configurez les modèles par agent :

    ```json5
    {
      agents: {
        list: [
          {
            id: "main",
            groupChat: {
              mentionPatterns: ["@openclaw", "openclaw"],
            },
          },
        ],
      },
      channels: {
        whatsapp: {
          groups: { "*": { requireMention: true } },
        },
      },
    }
    ```

    - **Mentions de métadonnées** : mentions natives @-mentions (WhatsApp tap-to-mention, Telegram @bot, etc.)
    - **Modèles de texte** : modèles regex dans `mentionPatterns`
    - Consultez la [référence complète](/gateway/configuration-reference#group-chat-mention-gating) pour les remplacements par canal et le mode auto-chat.

  </Accordion>

  <Accordion title="Configurer les sessions et les réinitialisations">
    Les sessions contrôlent la continuité et l'isolation des conversations :

    ```json5
    {
      session: {
        dmScope: "per-channel-peer",  // recommended for multi-user
        threadBindings: {
          enabled: true,
          idleHours: 24,
          maxAgeHours: 0,
        },
        reset: {
          mode: "daily",
          atHour: 4,
          idleMinutes: 120,
        },
      },
    }
    ```

    - `dmScope` : `main` (partagé) | `per-peer` | `per-channel-peer` | `per-account-channel-peer`
    - `threadBindings` : valeurs par défaut globales pour le routage des sessions liées aux threads (Discord supporte `/focus`, `/unfocus`, `/agents`, `/session idle` et `/session max-age`).
    - Consultez [Session Management](/concepts/session) pour la portée, les liens d'identité et la politique d'envoi.
    - Consultez la [référence complète](/gateway/configuration-reference#session) pour tous les champs.

  </Accordion>

  <Accordion title="Activer le sandboxing">
    Exécutez les sessions d'agent dans des conteneurs Docker isolés :

    ```json5
    {
      agents: {
        defaults: {
          sandbox: {
            mode: "non-main",  // off | non-main | all
            scope: "agent",    // session | agent | shared
          },
        },
      },
    }
    ```

    Construisez d'abord l'image : `scripts/sandbox-setup.sh`

    Consultez [Sandboxing](/gateway/sandboxing) pour le guide complet et la [référence complète](/gateway/configuration-reference#sandbox) pour toutes les options.

  </Accordion>

  <Accordion title="Activer le push soutenu par relais pour les builds iOS officiels">
    Le push soutenu par relais est configuré dans `openclaw.json`.

    Définissez ceci dans la configuration de la passerelle :

    ```json5
    {
      gateway: {
        push: {
          apns: {
            relay: {
              baseUrl: "https://relay.example.com",
              // Optional. Default: 10000
              timeoutMs: 10000,
            },
          },
        },
      },
    }
    ```

    Équivalent CLI :

    ```bash
    openclaw config set gateway.push.apns.relay.baseUrl https://relay.example.com
    ```

    Ce que cela fait :

    - Permet à la passerelle d'envoyer `push.test`, les nudges de réveil et les réveils de reconnexion via le relais externe.
    - Utilise une subvention d'envoi scoped à l'enregistrement transmise par l'application iOS appairée. La passerelle n'a pas besoin d'un jeton de relais à l'échelle du déploiement.
    - Lie chaque enregistrement soutenu par relais à l'identité de la passerelle avec laquelle l'application iOS s'est appairée, de sorte qu'une autre passerelle ne peut pas réutiliser l'enregistrement stocké.
    - Garde les builds iOS locaux/manuels sur APNs directs. Les envois soutenus par relais s'appliquent uniquement aux builds distribués officiels qui se sont enregistrés via le relais.
    - Doit correspondre à l'URL de base du relais intégrée dans le build iOS officiel/TestFlight, de sorte que le trafic d'enregistrement et d'envoi atteigne le même déploiement de relais.

    Flux de bout en bout :

    1. Installez un build iOS officiel/TestFlight qui a été compilé avec la même URL de base de relais.
    2. Configurez `gateway.push.apns.relay.baseUrl` sur la passerelle.
    3. Appairez l'application iOS à la passerelle et laissez les sessions de nœud et d'opérateur se connecter.
    4. L'application iOS récupère l'identité de la passerelle, s'enregistre auprès du relais en utilisant App Attest plus le reçu de l'application, puis publie la charge utile `push.apns.register` soutenue par relais à la passerelle appairée.
    5. La passerelle stocke le handle de relais et la subvention d'envoi, puis les utilise pour `push.test`, les nudges de réveil et les réveils de reconnexion.

    Notes opérationnelles :

    - Si vous basculez l'application iOS vers une passerelle différente, reconnectez l'application pour qu'elle puisse publier un nouvel enregistrement de relais lié à cette passerelle.
    - Si vous livrez un nouveau build iOS qui pointe vers un déploiement de relais différent, l'application actualise son enregistrement de relais en cache au lieu de réutiliser l'ancienne origine du relais.

    Note de compatibilité :

    - `OPENCLAW_APNS_RELAY_BASE_URL` et `OPENCLAW_APNS_RELAY_TIMEOUT_MS` fonctionnent toujours comme remplacements d'env temporaires.
    - `OPENCLAW_APNS_RELAY_ALLOW_HTTP=true` reste une trappe d'échappement de développement en boucle locale uniquement ; ne persistez pas les URL de relais HTTP dans la configuration.

    Consultez [iOS App](/platforms/ios#relay-backed-push-for-official-builds) pour le flux de bout en bout et [Authentication and trust flow](/platforms/ios#authentication-and-trust-flow) pour le modèle de sécurité du relais.

  </Accordion>

  <Accordion title="Configurer le heartbeat (vérifications périodiques)">
    ```json5
    {
      agents: {
        defaults: {
          heartbeat: {
            every: "30m",
            target: "last",
          },
        },
      },
    }
    ```

    - `every` : chaîne de durée (`30m`, `2h`). Définissez `0m` pour désactiver.
    - `target` : `last` | `whatsapp` | `telegram` | `discord` | `none`
    - `directPolicy` : `allow` (par défaut) ou `block` pour les cibles de heartbeat de style DM
    - Consultez [Heartbeat](/gateway/heartbeat) pour le guide complet.

  </Accordion>

  <Accordion title="Configurer les tâches cron">
    ```json5
    {
      cron: {
        enabled: true,
        maxConcurrentRuns: 2,
        sessionRetention: "24h",
        runLog: {
          maxBytes: "2mb",
          keepLines: 2000,
        },
      },
    }
    ```

    - `sessionRetention` : nettoyer les sessions d'exécution isolées complétées de `sessions.json` (par défaut `24h` ; définissez `false` pour désactiver).
    - `runLog` : nettoyer `cron/runs/<jobId>.jsonl` par taille et lignes conservées.
    - Consultez [Cron jobs](/automation/cron-jobs) pour l'aperçu des fonctionnalités et les exemples CLI.

  </Accordion>

  <Accordion title="Configurer les webhooks (hooks)">
    Activez les points de terminaison webhook HTTP sur la passerelle :

    ```json5
    {
      hooks: {
        enabled: true,
        token: "shared-secret",
        path: "/hooks",
        defaultSessionKey: "hook:ingress",
        allowRequestSessionKey: false,
        allowedSessionKeyPrefixes: ["hook:"],
        mappings: [
          {
            match: { path: "gmail" },
            action: "agent",
            agentId: "main",
            deliver: true,
          },
        ],
      },
    }
    ```

    Note de sécurité :
    - Traitez tout le contenu de la charge utile hook/webhook comme une entrée non fiable.
    - Gardez les drapeaux de contournement de contenu non sécurisé désactivés (`hooks.gmail.allowUnsafeExternalContent`, `hooks.mappings[].allowUnsafeExternalContent`) sauf pour le débogage étroitement scoped.
    - Pour les agents pilotés par hook, préférez les niveaux de modèle modernes et forts avec une politique d'outil stricte (par exemple, messagerie uniquement plus sandboxing si possible).

    Consultez la [référence complète](/gateway/configuration-reference#hooks) pour toutes les options de mappage et l'intégration Gmail.

  </Accordion>

  <Accordion title="Configurer le routage multi-agent">
    Exécutez plusieurs agents isolés avec des espaces de travail et des sessions séparés :

    ```json5
    {
      agents: {
        list: [
          { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
          { id: "work", workspace: "~/.openclaw/workspace-work" },
        ],
      },
      bindings: [
        { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
        { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
      ],
    }
    ```

    Consultez [Multi-Agent](/concepts/multi-agent) et la [référence complète](/gateway/configuration-reference#multi-agent-routing) pour les règles de liaison et les profils d'accès par agent.

  </Accordion>

  <Accordion title="Diviser la configuration en plusieurs fichiers ($include)">
    Utilisez `$include` pour organiser les grandes configurations :

    ```json5
    // ~/.openclaw/openclaw.json
    {
      gateway: { port: 18789 },
      agents: { $include: "./agents.json5" },
      broadcast: {
        $include: ["./clients/a.json5", "./clients/b.json5"],
      },
    }
    ```

    - **Fichier unique** : remplace l'objet contenant
    - **Tableau de fichiers** : fusionné en profondeur dans l'ordre (le dernier gagne)
    - **Clés sœurs** : fusionnées après les inclusions (remplacent les valeurs incluses)
    - **Inclusions imbriquées** : supportées jusqu'à 10 niveaux de profondeur
    - **Chemins relatifs** : résolus par rapport au fichier d'inclusion
    - **Gestion des erreurs** : erreurs claires pour les fichiers manquants, les erreurs d'analyse et les inclusions circulaires

  </Accordion>
</AccordionGroup>

## Rechargement à chaud de la configuration

La Gateway surveille `~/.openclaw/openclaw.json` et applique les modifications automatiquement — aucun redémarrage manuel n'est nécessaire pour la plupart des paramètres.

### Modes de rechargement

| Mode                   | Comportement                                                                                |
| ---------------------- | --------------------------------------------------------------------------------------- |
| **`hybrid`** (défaut) | Applique instantanément les modifications sûres. Redémarre automatiquement pour les modifications critiques.           |
| **`hot`**              | Applique uniquement les modifications sûres. Enregistre un avertissement quand un redémarrage est nécessaire — vous le gérez. |
| **`restart`**          | Redémarre la Gateway à chaque modification de configuration, sûre ou non.                                 |
| **`off`**              | Désactive la surveillance des fichiers. Les modifications prennent effet au prochain redémarrage manuel.                 |

```json5
{
  gateway: {
    reload: { mode: "hybrid", debounceMs: 300 },
  },
}
```

### Ce qui s'applique à chaud vs ce qui nécessite un redémarrage

La plupart des champs s'appliquent à chaud sans interruption. En mode `hybrid`, les modifications nécessitant un redémarrage sont gérées automatiquement.

| Catégorie            | Champs                                                               | Redémarrage nécessaire ? |
| ------------------- | -------------------------------------------------------------------- | --------------- |
| Canaux            | `channels.*`, `web` (WhatsApp) — tous les canaux intégrés et d'extension | Non              |
| Agent & modèles      | `agent`, `agents`, `models`, `routing`                               | Non              |
| Automatisation          | `hooks`, `cron`, `agent.heartbeat`                                   | Non              |
| Sessions & messages | `session`, `messages`                                                | Non              |
| Outils & médias       | `tools`, `browser`, `skills`, `audio`, `talk`                        | Non              |
| Interface & divers           | `ui`, `logging`, `identity`, `bindings`                              | Non              |
| Serveur Gateway      | `gateway.*` (port, bind, auth, tailscale, TLS, HTTP)                 | **Oui**         |
| Infrastructure      | `discovery`, `canvasHost`, `plugins`                                 | **Oui**         |

<Note>
`gateway.reload` et `gateway.remote` sont des exceptions — les modifier ne **déclenche pas** de redémarrage.
</Note>

## RPC de configuration (mises à jour programmatiques)

<Note>
Les RPC d'écriture du plan de contrôle (`config.apply`, `config.patch`, `update.run`) sont limités à **3 requêtes par 60 secondes** par `deviceId+clientIp`. En cas de limitation, le RPC retourne `UNAVAILABLE` avec `retryAfterMs`.
</Note>

<AccordionGroup>
  <Accordion title="config.apply (remplacement complet)">
    Valide + écrit la configuration complète et redémarre la Gateway en une seule étape.

    <Warning>
    `config.apply` remplace la **configuration entière**. Utilisez `config.patch` pour les mises à jour partielles, ou `openclaw config set` pour les clés uniques.
    </Warning>

    Paramètres :

    - `raw` (string) — charge utile JSON5 pour la configuration entière
    - `baseHash` (optionnel) — hash de configuration de `config.get` (requis quand la configuration existe)
    - `sessionKey` (optionnel) — clé de session pour le ping de réveil post-redémarrage
    - `note` (optionnel) — note pour la sentinelle de redémarrage
    - `restartDelayMs` (optionnel) — délai avant redémarrage (défaut 2000)

    Les demandes de redémarrage sont fusionnées pendant qu'une est déjà en attente/en vol, et un délai d'attente de 30 secondes s'applique entre les cycles de redémarrage.

    ```bash
    openclaw gateway call config.get --params '{}'  # capture payload.hash
    openclaw gateway call config.apply --params '{
      "raw": "{ agents: { defaults: { workspace: \"~/.openclaw/workspace\" } } }",
      "baseHash": "<hash>",
      "sessionKey": "agent:main:whatsapp:direct:+15555550123"
    }'
    ```

  </Accordion>

  <Accordion title="config.patch (mise à jour partielle)">
    Fusionne une mise à jour partielle dans la configuration existante (sémantique du correctif de fusion JSON) :

    - Les objets fusionnent récursivement
    - `null` supprime une clé
    - Les tableaux remplacent

    Paramètres :

    - `raw` (string) — JSON5 avec uniquement les clés à modifier
    - `baseHash` (requis) — hash de configuration de `config.get`
    - `sessionKey`, `note`, `restartDelayMs` — identiques à `config.apply`

    Le comportement de redémarrage correspond à `config.apply` : redémarrages en attente fusionnés plus un délai d'attente de 30 secondes entre les cycles de redémarrage.

    ```bash
    openclaw gateway call config.patch --params '{
      "raw": "{ channels: { telegram: { groups: { \"*\": { requireMention: false } } } } }",
      "baseHash": "<hash>"
    }'
    ```

  </Accordion>
</AccordionGroup>

## Variables d'environnement

OpenClaw lit les variables d'environnement du processus parent plus :

- `.env` du répertoire de travail actuel (s'il existe)
- `~/.openclaw/.env` (secours global)

Aucun fichier ne remplace les variables d'environnement existantes. Vous pouvez également définir des variables d'environnement en ligne dans la configuration :

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

<Accordion title="Importation d'env shell (optionnel)">
  Si activé et que les clés attendues ne sont pas définies, OpenClaw exécute votre shell de connexion et importe uniquement les clés manquantes :

```json5
{
  env: {
    shellEnv: { enabled: true, timeoutMs: 15000 },
  },
}
```

Équivalent de variable d'environnement : `OPENCLAW_LOAD_SHELL_ENV=1`
</Accordion>

<Accordion title="Substitution de variables d'environnement dans les valeurs de configuration">
  Référencez les variables d'environnement dans n'importe quelle valeur de chaîne de configuration avec `${VAR_NAME}` :

```json5
{
  gateway: { auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" } },
  models: { providers: { custom: { apiKey: "${CUSTOM_API_KEY}" } } },
}
```

Règles :

- Seuls les noms en majuscules correspondent : `[A-Z_][A-Z0-9_]*`
- Les variables manquantes/vides lèvent une erreur au moment du chargement
- Échappez avec `$${VAR}` pour une sortie littérale
- Fonctionne à l'intérieur des fichiers `$include`
- Substitution en ligne : `"${BASE}/v1"` → `"https://api.example.com/v1"`

</Accordion>

<Accordion title="Références secrètes (env, file, exec)">
  Pour les champs qui supportent les objets SecretRef, vous pouvez utiliser :

```json5
{
  models: {
    providers: {
      openai: { apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" } },
    },
  },
  skills: {
    entries: {
      "nano-banana-pro": {
        apiKey: {
          source: "file",
          provider: "filemain",
          id: "/skills/entries/nano-banana-pro/apiKey",
        },
      },
    },
  },
  channels: {
    googlechat: {
      serviceAccountRef: {
        source: "exec",
        provider: "vault",
        id: "channels/googlechat/serviceAccount",
      },
    },
  },
}
```

Les détails de SecretRef (y compris `secrets.providers` pour `env`/`file`/`exec`) sont dans [Gestion des secrets](/gateway/secrets).
Les chemins d'accès aux identifiants supportés sont listés dans [Surface des identifiants SecretRef](/reference/secretref-credential-surface).
</Accordion>

Voir [Environnement](/help/environment) pour la précédence complète et les sources.

## Référence complète

Pour la référence complète champ par champ, voir **[Référence de configuration](/gateway/configuration-reference)**.

---

_Connexes : [Exemples de configuration](/gateway/configuration-examples) · [Référence de configuration](/gateway/configuration-reference) · [Doctor](/gateway/doctor)_
