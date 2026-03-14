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
**Nouveau dans la configuration ?** Commencez par `openclaw onboard` pour une configuration interactive, ou consultez le guide [Configuration Examples](/gateway/configuration-examples) pour des configurations complètes prêtes à copier-coller.
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
    L'interface de contrôle affiche un formulaire basé sur le schéma de configuration, avec un éditeur **Raw JSON** comme solution de secours.
  </Tab>
  <Tab title="Édition directe">
    Éditez `~/.openclaw/openclaw.json` directement. La Gateway surveille le fichier et applique les modifications automatiquement (voir [rechargement à chaud](#config-hot-reload)).
  </Tab>
</Tabs>

## Validation stricte

<Warning>
OpenClaw n'accepte que les configurations qui correspondent exactement au schéma. Les clés inconnues, les types mal formés ou les valeurs invalides font que la Gateway **refuse de démarrer**. La seule exception au niveau racine est `$schema` (chaîne), pour que les éditeurs puissent joindre des métadonnées JSON Schema.
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
          allowFrom: ["tg:123"], // uniquement pour allowlist/open
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

    - `agents.defaults.models` définit le catalogue de modèles et agit comme liste blanche pour `/model`.
    - Les références de modèles utilisent le format `provider/model` (par exemple `anthropic/claude-opus-4-6`).
    - `agents.defaults.imageMaxDimensionPx` contrôle la réduction d'échelle des images de transcription/outil (par défaut `1200`) ; les valeurs plus basses réduisent généralement l'utilisation des jetons de vision sur les exécutions chargées de captures d'écran.
    - Consultez [Models CLI](/concepts/models) pour changer de modèle dans le chat et [Model Failover](/concepts/model-failover) pour la rotation d'authentification et le comportement de secours.
    - Pour les fournisseurs personnalisés/auto-hébergés, consultez [Custom providers](/gateway/configuration-reference#custom-providers-and-base-urls) dans la référence.

  </Accordion>

  <Accordion title="Contrôler qui peut envoyer des messages au bot">
    L'accès DM est contrôlé par canal via `dmPolicy` :

    - `"pairing"` (par défaut) : les expéditeurs inconnus reçoivent un code d'appairage unique à approuver
    - `"allowlist"` : uniquement les expéditeurs dans `allowFrom` (ou le magasin d'appairage)
    - `"open"` : autoriser tous les DM entrants (nécessite `allowFrom: ["*"]`)
    - `"disabled"` : ignorer tous les DM

    Pour les groupes, utilisez `groupPolicy` + `groupAllowFrom` ou des listes blanches spécifiques au canal.

    Consultez la [référence complète](/gateway/configuration-reference#dm-and-group-access) pour les détails par canal.

  </Accordion>

  <Accordion title="Configurer la limitation de mention dans les chats de groupe">
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

  <Accordion title="Configurer les sessions et réinitialisations">
    Les sessions contrôlent la continuité et l'isolation des conversations :

    ```json5
    {
      session: {
        dmScope: "per-channel-peer",  // recommandé pour multi-utilisateur
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
    - `threadBindings` : valeurs par défaut globales pour le routage de session lié aux threads (Discord supporte `/focus`, `/unfocus`, `/agents`, `/session idle` et `/session max-age`).
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

  <Accordion title="Activer le push basé sur relais pour les builds iOS officiels">
    Le push basé sur relais est configuré dans `openclaw.json`.

    Définissez ceci dans la configuration de la gateway :

    ```json5
    {
      gateway: {
        push: {
          apns: {
            relay: {
              baseUrl: "https://relay.example.com",
              // Optionnel. Par défaut : 10000
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

    - Permet à la gateway d'envoyer `push.test`, les nudges de réveil et les réveils de reconnexion via le relais externe.
    - Utilise une subvention d'envoi à portée d'enregistrement transmise par l'application iOS appairée. La gateway n'a pas besoin d'un jeton de relais à l'échelle du déploiement.
    - Lie chaque enregistrement basé sur relais à l'identité de la gateway avec laquelle l'application iOS s'est appairée, de sorte qu'une autre gateway ne puisse pas réutiliser l'enregistrement stocké.
    - Garde les builds iOS locaux/manuels sur APNs directs. Les envois basés sur relais s'appliquent uniquement aux builds officiels distribués qui se sont enregistrés via le relais.
    - Doit correspondre à l'URL de base du relais intégrée dans le build iOS officiel/TestFlight, de sorte que le trafic d'enregistrement et d'envoi atteigne le même déploiement de relais.

    Flux de bout en bout :

    1. Installez un build iOS officiel/TestFlight compilé avec la même URL de base de relais.
    2. Configurez `gateway.push.apns.relay.baseUrl` sur la gateway.
    3. Appairez l'application iOS à la gateway et laissez les sessions de nœud et d'opérateur se connecter.
    4. L'application iOS récupère l'identité de la gateway, s'enregistre auprès du relais en utilisant App Attest plus le reçu de l'application, puis publie la charge utile `push.apns.register` basée sur relais à la gateway appairée.
    5. La gateway stocke le handle de relais et la subvention d'envoi, puis les utilise pour `push.test`, les nudges de réveil et les réveils de reconnexion.

    Notes opérationnelles :

    - Si vous basculez l'application iOS vers une gateway différente, reconnectez l'application pour qu'elle puisse publier un nouvel enregistrement de relais lié à cette gateway.
    - Si vous livrez un nouveau build iOS qui pointe vers un déploiement de relais différent, l'application actualise son enregistrement de relais en cache au lieu de réutiliser l'ancienne origine du relais.

    Note de compatibilité :

    - `OPENCLAW_APNS_RELAY_BASE_URL` et `OPENCLAW_APNS_RELAY_TIMEOUT_MS` fonctionnent toujours comme remplacements env temporaires.
    - `OPENCLAW_APNS_RELAY_ALLOW_HTTP=true` reste une échappatoire de développement en boucle locale ; ne persistez pas les URL de relais HTTP dans la configuration.

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
    - Consultez [Cron jobs](/automation/c
