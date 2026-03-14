---
summary: "Plugins OpenClaw/extensions : découverte, configuration et sécurité"
read_when:
  - Adding or modifying plugins/extensions
  - Documenting plugin install or load rules
title: "Plugins"
---

# Plugins (Extensions)

## Démarrage rapide (nouveau dans les plugins ?)

Un plugin est juste un **petit module de code** qui étend OpenClaw avec des fonctionnalités supplémentaires (commandes, outils et Gateway RPC).

La plupart du temps, vous utiliserez des plugins quand vous voulez une fonctionnalité qui n'est pas encore intégrée dans le cœur d'OpenClaw (ou que vous voulez garder les fonctionnalités optionnelles en dehors de votre installation principale).

Chemin rapide :

1. Voir ce qui est déjà chargé :

```bash
openclaw plugins list
```

2. Installer un plugin officiel (exemple : Voice Call) :

```bash
openclaw plugins install @openclaw/voice-call
```

Les spécifications Npm sont **registry-only** (nom du package + **version exacte** optionnelle ou **dist-tag**). Les spécifications Git/URL/fichier et les plages semver sont rejetées.

Les spécifications nues et `@latest` restent sur la piste stable. Si npm résout l'une ou l'autre en une préversion, OpenClaw s'arrête et vous demande d'accepter explicitement avec une balise de préversion telle que `@beta`/`@rc` ou une version de préversion exacte.

3. Redémarrez la Gateway, puis configurez sous `plugins.entries.<id>.config`.

Voir [Voice Call](/plugins/voice-call) pour un exemple concret de plugin.
Vous cherchez des listes tierces ? Voir [Plugins communautaires](/plugins/community).

## Architecture

Le système de plugins d'OpenClaw a quatre couches :

1. **Manifeste + découverte**
   OpenClaw trouve les plugins candidats à partir de chemins configurés, de racines d'espace de travail, de racines d'extensions globales et d'extensions groupées. La découverte lit d'abord `openclaw.plugin.json` plus les métadonnées du package.
2. **Activation + validation**
   Le cœur décide si un plugin découvert est activé, désactivé, bloqué ou sélectionné pour un emplacement exclusif comme la mémoire.
3. **Chargement à l'exécution**
   Les plugins activés sont chargés en processus via jiti et enregistrent les capacités dans un registre central.
4. **Consommation de surface**
   Le reste d'OpenClaw lit le registre pour exposer les outils, les canaux, la configuration du fournisseur, les hooks, les routes HTTP, les commandes CLI et les services.

La limite de conception importante :

- la découverte + la validation de la configuration doivent fonctionner à partir des **métadonnées du manifeste/schéma** sans exécuter le code du plugin
- le comportement à l'exécution provient du chemin `register(api)` du module du plugin

Cette séparation permet à OpenClaw de valider la configuration, d'expliquer les plugins manquants/désactivés et de construire des indices UI/schéma avant que le runtime complet soit actif.

## Modèle d'exécution

Les plugins s'exécutent **en processus** avec la Gateway. Ils ne sont pas isolés. Un plugin chargé a la même limite de confiance au niveau du processus que le code principal.

Implications :

- un plugin peut enregistrer des outils, des gestionnaires réseau, des hooks et des services
- un bug de plugin peut planter ou déstabiliser la gateway
- un plugin malveillant équivaut à une exécution de code arbitraire à l'intérieur du processus OpenClaw

Utilisez des listes blanches et des chemins d'installation/chargement explicites pour les plugins non groupés. Traitez les plugins d'espace de travail comme du code au moment du développement, pas comme des valeurs par défaut de production.

Note de confiance importante :

- `plugins.allow` fait confiance aux **ids de plugin**, pas à la provenance de la source.
- Un plugin d'espace de travail avec le même id qu'un plugin groupé masque intentionnellement la copie groupée quand ce plugin d'espace de travail est activé/autorisé.
- C'est normal et utile pour le développement local, les tests de correctifs et les correctifs d'urgence.

## Plugins disponibles (officiels)

- Microsoft Teams est plugin-only à partir de 2026.1.15 ; installez `@openclaw/msteams` si vous utilisez Teams.
- Memory (Core) — plugin de recherche de mémoire groupé (activé par défaut via `plugins.slots.memory`)
- Memory (LanceDB) — plugin de mémoire à long terme groupé (rappel/capture automatique ; définissez `plugins.slots.memory = "memory-lancedb"`)
- [Voice Call](/plugins/voice-call) — `@openclaw/voice-call`
- [Zalo Personal](/plugins/zalouser) — `@openclaw/zalouser`
- [Matrix](/channels/matrix) — `@openclaw/matrix`
- [Nostr](/channels/nostr) — `@openclaw/nostr`
- [Zalo](/channels/zalo) — `@openclaw/zalo`
- [Microsoft Teams](/channels/msteams) — `@openclaw/msteams`
- Google Antigravity OAuth (authentification du fournisseur) — groupé comme `google-antigravity-auth` (désactivé par défaut)
- Gemini CLI OAuth (authentification du fournisseur) — groupé comme `google-gemini-cli-auth` (désactivé par défaut)
- Qwen OAuth (authentification du fournisseur) — groupé comme `qwen-portal-auth` (désactivé par défaut)
- Copilot Proxy (authentification du fournisseur) — pont local VS Code Copilot Proxy ; distinct de la connexion d'appareil `github-copilot` intégrée (groupé, désactivé par défaut)

Les plugins OpenClaw sont des **modules TypeScript** chargés à l'exécution via jiti. **La validation de la configuration n'exécute pas le code du plugin** ; elle utilise le manifeste du plugin et JSON Schema à la place. Voir [Manifeste du plugin](/plugins/manifest).

Les plugins peuvent enregistrer :

- Méthodes Gateway RPC
- Routes HTTP Gateway
- Outils d'agent
- Commandes CLI
- Services en arrière-plan
- Moteurs de contexte
- Validation de configuration optionnelle
- **Skills** (en listant les répertoires `skills` dans le manifeste du plugin)
- **Commandes de réponse automatique** (exécution sans invoquer l'agent IA)

Les plugins s'exécutent **en processus** avec la Gateway, traitez-les donc comme du code de confiance.
Guide de création d'outils : [Outils d'agent de plugin](/plugins/agent-tools).

## Pipeline de chargement

Au démarrage, OpenClaw fait à peu près ceci :

1. découvrir les racines de plugins candidats
2. lire `openclaw.plugin.json` et les métadonnées du package
3. rejeter les candidats non sûrs
4. normaliser la configuration du plugin (`plugins.enabled`, `allow`, `deny`, `entries`, `slots`, `load.paths`)
5. décider de l'activation pour chaque candidat
6. charger les modules activés via jiti
7. appeler `register(api)` et collecter les enregistrements dans le registre du plugin
8. exposer le registre aux surfaces de commandes/runtime

Les portes de sécurité se produisent **avant** l'exécution à l'exécution. Les candidats sont bloqués quand l'entrée s'échappe de la racine du plugin, le chemin est accessible en écriture au monde, ou la propriété du chemin semble suspecte pour les plugins non groupés.

### Comportement basé sur le manifeste

Le manifeste est la source de vérité du plan de contrôle. OpenClaw l'utilise pour :

- identifier le plugin
- découvrir les canaux/skills/schéma de configuration déclarés
- valider `plugins.entries.<id>.config`
- augmenter les étiquettes/espaces réservés de l'interface utilisateur de contrôle
- afficher les métadonnées d'installation/catalogue

Le module à l'exécution est la partie plan de données. Il enregistre le comportement réel comme les hooks, les outils, les commandes ou les flux de fournisseur.

### Ce que le chargeur met en cache

OpenClaw maintient des caches courts en processus pour :

- résultats de découverte
- données du registre de manifeste
- registres de plugins chargés

Ces caches réduisent le surcoût de démarrage en rafales et les frais généraux de commandes répétées. Ils sont sûrs à considérer comme des caches de performance à courte durée de vie, pas de persistance.

## Assistants à l'exécution

Les plugins peuvent accéder aux assistants principaux sélectionnés via `api.runtime`. Pour la TTS de téléphonie :

```ts
const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
```

Notes :

- Utilise la configuration `messages.tts` principale (OpenAI ou ElevenLabs).
- Retourne un tampon audio PCM + taux d'échantillonnage. Les plugins doivent rééchantillonner/encoder pour les fournisseurs.
- Edge TTS n'est pas supporté pour la téléphonie.

Pour STT/transcription, les plugins peuvent appeler :

```ts
const { text } = await api.runtime.stt.transcribeAudioFile({
  filePath: "/tmp/inbound-audio.ogg",
  cfg: api.config,
  // Optionnel quand MIME ne peut pas être déduit de manière fiable :
  mime: "audio/ogg",
});
```

Notes :

- Utilise la configuration audio de compréhension des médias principale (`tools.media.audio`) et l'ordre de secours du fournisseur.
- Retourne `{ text: undefined }` quand aucune sortie de transcription n'est produite (par exemple entrée ignorée/non supportée).

## Routes HTTP Gateway

Les plugins peuvent exposer des points de terminaison HTTP avec `api.registerHttpRoute(...)`.

```ts
api.registerHttpRoute({
  path: "/acme/webhook",
  auth: "plugin",
  match: "exact",
  handler: async (_req, res) => {
    res.statusCode = 200;
    res.end("ok");
    return true;
  },
});
```

Champs de route :

- `path` : chemin de route sous le serveur HTTP de la gateway.
- `auth` : requis. Utilisez `"gateway"` pour exiger l'authentification normale de la gateway, ou `"plugin"` pour l'authentification gérée par le plugin/vérification du webhook.
- `match` : optionnel. `"exact"` (par défaut) ou `"prefix"`.
- `replaceExisting` : optionnel. Permet au même plugin de remplacer son propre enregistrement de route existant.
- `handler` : retournez `true` quand la route a traité la demande.

Notes :

- `api.registerHttpHandler(...)` est obsolète. Utilisez `api.registerHttpRoute(...)`.
- Les routes de plugin doivent déclarer `auth` explicitement.
- Les conflits exacts `path + match` sont rejetés sauf si `replaceExisting: true`, et un plugin ne peut pas remplacer la route d'un autre plugin.
- Les routes qui se chevauchent avec différents niveaux `auth` sont rejetées. Gardez les chaînes de secours `exact`/`prefix` au même niveau d'authentification uniquement.

## Chemins d'importation du SDK du plugin

Utilisez les sous-chemins du SDK au lieu de l'importation monolithique `openclaw/plugin-sdk` lors de la création de plugins :

- `openclaw/plugin-sdk/core` pour les API de plugin génériques, les types d'authentification du fournisseur et les assistants partagés.
- `openclaw/plugin-sdk/compat` pour le code de plugin groupé/interne qui a besoin d'assistants de runtime partagés plus larges que `core`.
- `openclaw/plugin-sdk/telegram` pour les plugins de canal Telegram.
- `openclaw/plugin-sdk/discord` pour les plugins de canal Discord.
- `openclaw/plugin-sdk/slack` pour les plugins de canal Slack.
- `openclaw/plugin-sdk/signal` pour les plugins de canal Signal.
- `openclaw/plugin-sdk/imessage` pour les plugins de canal iMessage.
- `openclaw/plugin-sdk/whatsapp` pour les plugins de canal WhatsApp.
- `openclaw/plugin-sdk/line` pour les plugins de canal LINE.
- `openclaw/plugin-sdk/msteams` pour la surface du plugin Microsoft Teams groupé.
- Les sous-chemins spécifiques à l'extension groupée sont également disponibles :
  `openclaw/plugin-sdk/acpx`, `openclaw/plugin-sdk/bluebubbles`,
  `openclaw/plugin-sdk/copilot-proxy`, `openclaw/plugin-sdk/device-pair`,
  `openclaw/plugin-sdk/diagnostics-otel`, `openclaw/plugin-sdk/diffs`,
  `openclaw/plugin-sdk/feishu`,
  `openclaw/plugin-sdk/google-gemini-cli-auth`, `openclaw/plugin-sdk/googlechat`,
  `openclaw/plugin-sdk/irc`, `openclaw/plugin-sdk/llm-task`,
  `openclaw/plugin-sdk/lobster`, `openclaw/plugin-sdk/matrix`,
  `openclaw/plugin-sdk/mattermost`, `openclaw/plugin-sdk/memory-core`,
  `openclaw/plugin-sdk/memory-lancedb`,
  `openclaw/plugin-sdk/minimax-portal-auth`,
  `openclaw/plugin-sdk/nextcloud-talk`, `openclaw/plugin-sdk/nostr`,
  `openclaw/plugin-sdk/open-prose`, `openclaw/plugin-sdk/phone-control`,
  `openclaw/plugin-sdk/qwen-portal-auth`, `openclaw/plugin-sdk/synology-chat`,
  `openclaw/plugin-sdk/talk-voice`, `openclaw/plugin-sdk/test-utils`,
  `openclaw/plugin-sdk/thread-ownership`, `openclaw/plugin-sdk/tlon`,
  `openclaw/plugin-sdk/twitch`, `openclaw/plugin-sdk/voice-call`,
  `openclaw/plugin-sdk/zalo`, et `openclaw/plugin-sdk/zalouser`.

Note de compatibilité :

- `openclaw/plugin-sdk` reste supporté pour les plugins externes existants.
- Les plugins groupés nouveaux et migrés doivent utiliser les sous-chemins spécifiques au canal ou à l'extension ; utilisez `core` pour les surfaces génériques et `compat` uniquement quand des assistants partagés plus larges sont requis.

## Inspection de canal en lecture seule

Si votre plugin enregistre un canal, préférez implémenter `plugin.config.inspectAccount(cfg, accountId)` aux côtés de `resolveAccount(...)`.

Pourquoi :

- `resolveAccount(...)`
