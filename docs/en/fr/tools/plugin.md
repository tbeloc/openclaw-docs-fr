---
summary: "Plugins/extensions OpenClaw : découverte, configuration et sécurité"
read_when:
  - Adding or modifying plugins/extensions
  - Documenting plugin install or load rules
title: "Plugins"
---

# Plugins (Extensions)

## Démarrage rapide (nouveau dans les plugins ?)

Un plugin est simplement un **petit module de code** qui étend OpenClaw avec des fonctionnalités supplémentaires (commandes, outils et Gateway RPC).

La plupart du temps, vous utiliserez des plugins quand vous voulez une fonctionnalité qui n'est pas encore intégrée dans le cœur d'OpenClaw (ou quand vous voulez garder les fonctionnalités optionnelles en dehors de votre installation principale).

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

Les spécifications nues et `@latest` restent sur la piste stable. Si npm résout l'une ou l'autre vers une préversion, OpenClaw s'arrête et vous demande d'accepter explicitement avec une balise de préversion telle que `@beta`/`@rc` ou une version de préversion exacte.

3. Redémarrez la Gateway, puis configurez sous `plugins.entries.<id>.config`.

Voir [Voice Call](/fr/plugins/voice-call) pour un exemple concret de plugin.
Vous cherchez des listes tierces ? Voir [Plugins communautaires](/fr/plugins/community).

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
- Memory (Core) — plugin de recherche mémoire groupé (activé par défaut via `plugins.slots.memory`)
- Memory (LanceDB) — plugin de mémoire à long terme groupé (rappel/capture automatique ; définissez `plugins.slots.memory = "memory-lancedb"`)
- [Voice Call](/fr/plugins/voice-call) — `@openclaw/voice-call`
- [Zalo Personal](/fr/plugins/zalouser) — `@openclaw/zalouser`
- [Matrix](/fr/channels/matrix) — `@openclaw/matrix`
- [Nostr](/fr/channels/nostr) — `@openclaw/nostr`
- [Zalo](/fr/channels/zalo) — `@openclaw/zalo`
- [Microsoft Teams](/fr/channels/msteams) — `@openclaw/msteams`
- Google Antigravity OAuth (authentification du fournisseur) — groupé en tant que `google-antigravity-auth` (désactivé par défaut)
- Gemini CLI OAuth (authentification du fournisseur) — groupé en tant que `google-gemini-cli-auth` (désactivé par défaut)
- Qwen OAuth (authentification du fournisseur) — groupé en tant que `qwen-portal-auth` (désactivé par défaut)
- Copilot Proxy (authentification du fournisseur) — pont local VS Code Copilot Proxy ; distinct de la connexion d'appareil `github-copilot` intégrée (groupé, désactivé par défaut)

Les plugins OpenClaw sont des **modules TypeScript** chargés à l'exécution via jiti. **La validation de la configuration n'exécute pas le code du plugin** ; elle utilise à la place le manifeste du plugin et JSON Schema. Voir [Manifeste du plugin](/fr/plugins/manifest).

Les plugins peuvent enregistrer :

- Méthodes Gateway RPC
- Routes HTTP Gateway
- Outils d'agent
- Commandes CLI
- Services en arrière-plan
- Moteurs de contexte
- Validation de configuration optionnelle
- **Skills** (en listant les répertoires `skills` dans le manifeste du plugin)
- **Commandes de réponse automatique** (exécuter sans invoquer l'agent IA)

Les plugins s'exécutent **en processus** avec la Gateway, traitez-les donc comme du code de confiance.
Guide de création d'outils : [Outils d'agent de plugin](/fr/plugins/agent-tools).

## Pipeline de chargement

Au démarrage, OpenClaw fait à peu près ceci :

1. découvrir les racines de plugins candidats
2. lire `openclaw.plugin.json` et les métadonnées du package
3. rejeter les candidats non sûrs
4. normaliser la configuration du plugin (`plugins.enabled`, `allow`, `deny`, `entries`, `slots`, `load.paths`)
5. décider de l'activation pour chaque candidat
6. charger les modules activés via jiti
7. appeler `register(api)` et collecter les enregistrements dans le registre des plugins
8. exposer le registre aux surfaces de commandes/runtime

Les portes de sécurité se produisent **avant** l'exécution à l'exécution. Les candidats sont bloqués quand l'entrée s'échappe de la racine du plugin, le chemin est accessible en écriture au monde, ou la propriété du chemin semble suspecte pour les plugins non groupés.

### Comportement basé sur le manifeste

Le manifeste est la source de vérité du plan de contrôle. OpenClaw l'utilise pour :

- identifier le plugin
- découvrir les canaux/skills/schéma de configuration déclarés
- valider `plugins.entries.<id>.config`
- augmenter les étiquettes/placeholders de l'interface utilisateur de contrôle
- afficher les métadonnées d'installation/catalogue

Le module runtime est la partie du plan de données. Il enregistre le comportement réel tel que les hooks, les outils, les commandes ou les flux de fournisseur.

### Ce que le chargeur met en cache

OpenClaw maintient des caches courts en processus pour :

- les résultats de découverte
- les données du registre de manifeste
- les registres de plugins chargés

Ces caches réduisent les pics de démarrage et les frais généraux de commandes répétées. Ils sont sûrs à considérer comme des caches de performance de courte durée, pas de persistance.

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
- Retourne un buffer audio PCM + taux d'échantillonnage. Les plugins doivent rééchantillonner/encoder pour les fournisseurs.
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

- Utilise la configuration audio de compréhension médias principale (`tools.media.audio`) et l'ordre de secours du fournisseur.
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
- `auth` : requis. Utilisez `"gateway"` pour exiger l'authentification gateway normale, ou `"plugin"` pour l'authentification/vérification de webhook gérée par le plugin.
- `match` : optionnel. `"exact"` (par défaut) ou `"prefix"`.
- `replaceExisting` : optionnel. Permet au même plugin de remplacer son propre enregistrement de route existant.
- `handler` : retournez `true` quand la route a traité la demande.

Notes :

- `api.registerHttpHandler(...)` est obsolète. Utilisez `api.registerHttpRoute(...)`.
- Les routes de plugin doivent déclarer `auth` explicitement.
- Les conflits exacts `path + match` sont rejetés sauf si `replaceExisting: true`, et un plugin ne peut pas remplacer la route d'un autre plugin.
- Les routes qui se chevauchent avec différents niveaux `auth` sont rejetées. Gardez les chaînes de secours `exact`/`prefix` au même niveau d'authentification uniquement.

## Chemins d'importation du SDK de plugin

Utilisez les sous-chemins du SDK au lieu de l'importation monolithique `openclaw/plugin-sdk` lors de la création de plugins :

- `openclaw/plugin-sdk/core` pour les APIs de plugin génériques, les types d'authentification de fournisseur et les assistants partagés.
- `openclaw/plugin-sdk/compat` pour le code de plugin groupé/interne qui a besoin d'assistants runtime partagés plus larges que `core`.
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
- Les plugins groupés nouveaux et migrés doivent utiliser les sous-chemins spécifiques au canal ou à l'extension ; utilisez `core` pour les surfaces génériques et `compat` uniquement quand des assistants runtime partagés plus larges sont requis.

## Inspection de canal en lecture seule

Si votre plugin enregistre un canal, préférez implémenter
`plugin.config.inspectAccount(cfg, accountId)` aux côtés de `resolveAccount(...)`.

Pourquoi :

- `resolveAccount(...)` est le chemin d'exécution. Il est autorisé à supposer que les identifiants
  sont entièrement matérialisés et peut échouer rapidement quand les secrets requis manquent.
- Les chemins de commande en lecture seule tels que `openclaw status`, `openclaw status --all`,
  `openclaw channels status`, `openclaw channels resolve`, et les flux de réparation doctor/config
  ne devraient pas avoir besoin de matérialiser les identifiants d'exécution juste pour
  décrire la configuration.

Comportement recommandé pour `inspectAccount(...)` :

- Retourner uniquement l'état descriptif du compte.
- Préserver `enabled` et `configured`.
- Inclure les champs de source/statut des identifiants quand pertinent, tels que :
  - `tokenSource`, `tokenStatus`
  - `botTokenSource`, `botTokenStatus`
  - `appTokenSource`, `appTokenStatus`
  - `signingSecretSource`, `signingSecretStatus`
- Vous n'avez pas besoin de retourner les valeurs brutes des tokens juste pour signaler la
  disponibilité en lecture seule. Retourner `tokenStatus: "available"` (et le champ source correspondant)
  est suffisant pour les commandes de type statut.
- Utilisez `configured_unavailable` quand un identifiant est configuré via SecretRef mais
  indisponible dans le chemin de commande actuel.

Cela permet aux commandes en lecture seule de signaler « configuré mais indisponible dans ce chemin
de commande » au lieu de planter ou de mal signaler le compte comme non configuré.

Note de performance :

- La découverte de plugins et les métadonnées de manifeste utilisent des caches courts en processus pour réduire
  le travail de démarrage/rechargement par rafales.
- Définissez `OPENCLAW_DISABLE_PLUGIN_DISCOVERY_CACHE=1` ou
  `OPENCLAW_DISABLE_PLUGIN_MANIFEST_CACHE=1` pour désactiver ces caches.
- Ajustez les fenêtres de cache avec `OPENCLAW_PLUGIN_DISCOVERY_CACHE_MS` et
  `OPENCLAW_PLUGIN_MANIFEST_CACHE_MS`.

## Découverte et précédence

OpenClaw analyse, dans l'ordre :

1. Chemins de configuration

- `plugins.load.paths` (fichier ou répertoire)

2. Extensions d'espace de travail

- `<workspace>/.openclaw/extensions/*.ts`
- `<workspace>/.openclaw/extensions/*/index.ts`

3. Extensions globales

- `~/.openclaw/extensions/*.ts`
- `~/.openclaw/extensions/*/index.ts`

4. Extensions intégrées (livrées avec OpenClaw, principalement désactivées par défaut)

- `<openclaw>/extensions/*`

La plupart des plugins intégrés doivent être activés explicitement via
`plugins.entries.<id>.enabled` ou `openclaw plugins enable <id>`.

Exceptions de plugin intégré activé par défaut :

- `device-pair`
- `phone-control`
- `talk-voice`
- plugin d'emplacement de mémoire actif (emplacement par défaut : `memory-core`)

Les plugins installés sont activés par défaut, mais peuvent être désactivés de la même manière.

Les plugins d'espace de travail sont **désactivés par défaut** sauf si vous les activez explicitement
ou les ajoutez à une liste blanche. C'est intentionnel : un dépôt extrait ne devrait pas devenir
silencieusement du code de passerelle de production.

Notes de durcissement :

- Si `plugins.allow` est vide et que des plugins non intégrés sont découvrables, OpenClaw enregistre un avertissement
  au démarrage avec les ids et sources des plugins.
- Les chemins candidats sont vérifiés pour la sécurité avant l'admission de découverte. OpenClaw bloque les candidats quand :
  - l'entrée d'extension se résout en dehors de la racine du plugin (y compris les échappements de lien symbolique/traversée de chemin),
  - la racine du plugin/chemin source est accessible en écriture par tous,
  - la propriété du chemin est suspecte pour les plugins non intégrés (le propriétaire POSIX n'est ni l'uid actuel ni root).
- Les plugins non intégrés chargés sans provenance d'installation/chemin de chargement émettent un avertissement
  pour que vous puissiez épingler la confiance (`plugins.allow`) ou installer le suivi (`plugins.installs`).

Chaque plugin doit inclure un fichier `openclaw.plugin.json` dans sa racine. Si un chemin
pointe vers un fichier, la racine du plugin est le répertoire du fichier et doit contenir le
manifeste.

Si plusieurs plugins se résolvent au même id, le premier match dans l'ordre ci-dessus
gagne et les copies de précédence inférieure sont ignorées.

Cela signifie :

- les plugins d'espace de travail masquent intentionnellement les plugins intégrés avec le même id
- `plugins.allow: ["foo"]` autorise le plugin `foo` actif par id, même quand
  la copie active provient de l'espace de travail au lieu de la racine d'extension intégrée
- si vous avez besoin d'un contrôle de provenance plus strict, utilisez des chemins d'installation/chargement explicites et
  inspectez la source du plugin résolue avant de l'activer

### Règles d'activation

L'activation est résolue après la découverte :

- `plugins.enabled: false` désactive tous les plugins
- `plugins.deny` gagne toujours
- `plugins.entries.<id>.enabled: false` désactive ce plugin
- les plugins d'origine d'espace de travail sont désactivés par défaut
- les listes blanches restreignent l'ensemble actif quand `plugins.allow` est non vide
- les listes blanches sont **basées sur l'id**, pas sur la source
- les plugins intégrés sont désactivés par défaut sauf si :
  - l'id intégré est dans l'ensemble activé par défaut intégré, ou
  - vous l'activez explicitement, ou
  - la configuration du canal active implicitement le plugin de canal intégré
- les emplacements exclusifs peuvent forcer l'activation du plugin sélectionné pour cet emplacement

Dans le core actuel, les ids intégrés activés par défaut incluent les aides locales/fournisseur telles que
`ollama`, `sglang`, `vllm`, plus `device-pair`, `phone-control`, et
`talk-voice`.

### Packs de paquets

Un répertoire de plugin peut inclure un `package.json` avec `openclaw.extensions` :

```json
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"]
  }
}
```

Chaque entrée devient un plugin. Si le pack liste plusieurs extensions, l'id du plugin
devient `name/<fileBase>`.

Si votre plugin importe des dépendances npm, installez-les dans ce répertoire pour que
`node_modules` soit disponible (`npm install` / `pnpm install`).

Garde-fou de sécurité : chaque entrée `openclaw.extensions` doit rester à l'intérieur du répertoire du plugin
après résolution des liens symboliques. Les entrées qui s'échappent du répertoire du paquet sont
rejetées.

Note de sécurité : `openclaw plugins install` installe les dépendances du plugin avec
`npm install --ignore-scripts` (pas de scripts de cycle de vie). Gardez les arbres de dépendances du plugin « pur JS/TS »
et évitez les paquets qui nécessitent des constructions `postinstall`.

### Métadonnées du catalogue de canaux

Les plugins de canal peuvent annoncer les métadonnées d'intégration via `openclaw.channel` et
les indices d'installation via `openclaw.install`. Cela garde les données du catalogue core-free.

Exemple :

```json
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "extensions": ["./index.ts"],
    "channel": {
      "id": "nextcloud-talk",
      "label": "Nextcloud Talk",
      "selectionLabel": "Nextcloud Talk (self-hosted)",
      "docsPath": "/channels/nextcloud-talk",
      "docsLabel": "nextcloud-talk",
      "blurb": "Self-hosted chat via Nextcloud Talk webhook bots.",
      "order": 65,
      "aliases": ["nc-talk", "nc"]
    },
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "extensions/nextcloud-talk",
      "defaultChoice": "npm"
    }
  }
}
```

OpenClaw peut également fusionner des **catalogues de canaux externes** (par exemple, une exportation de registre MPM).
Déposez un fichier JSON à l'un de :

- `~/.openclaw/mpm/plugins.json`
- `~/.openclaw/mpm/catalog.json`
- `~/.openclaw/plugins/catalog.json`

Ou pointez `OPENCLAW_PLUGIN_CATALOG_PATHS` (ou `OPENCLAW_MPM_CATALOG_PATHS`) vers
un ou plusieurs fichiers JSON (délimités par virgule/point-virgule/`PATH`). Chaque fichier devrait
contenir `{ "entries": [ { "name": "@scope/pkg", "openclaw": { "channel": {...}, "install": {...} } } ] }`.

## IDs de plugin

IDs de plugin par défaut :

- Packs de paquets : `package.json` `name`
- Fichier autonome : nom de base du fichier (`~/.../voice-call.ts` → `voice-call`)

Si un plugin exporte `id`, OpenClaw l'utilise mais avertit quand il ne correspond pas à
l'id configuré.

## Modèle de registre

Les plugins chargés ne mutent pas directement les globals core aléatoires. Ils s'enregistrent dans un
registre de plugin central.

Le registre suit :

- enregistrements de plugin (identité, source, origine, statut, diagnostics)
- outils
- hooks hérités et hooks typés
- canaux
- fournisseurs
- gestionnaires RPC de passerelle
- routes HTTP
- enregistreurs CLI
- services en arrière-plan
- commandes possédées par le plugin

Les fonctionnalités core lisent ensuite à partir de ce registre au lieu de parler directement aux modules de plugin.
Cela garde le chargement unidirectionnel :

- module de plugin -> enregistrement de registre
- runtime core -> consommation de registre

Cette séparation est importante pour la maintenabilité. Cela signifie que la plupart des surfaces core n'ont besoin que
d'un seul point d'intégration : « lire le registre », pas « cas spécial pour chaque module de plugin ».

## Configuration

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-extension"] },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } },
    },
  },
}
```

Champs :

- `enabled` : commutateur maître (par défaut : true)
- `allow` : liste blanche (optionnel)
- `deny` : liste noire (optionnel ; deny gagne)
- `load.paths` : fichiers/répertoires de plugin supplémentaires
- `slots` : sélecteurs d'emplacement exclusif tels que `memory` et `contextEngine`
- `entries.<id>` : bascules par plugin + configuration

Les changements de configuration **nécessitent un redémarrage de la passerelle**.

Règles de validation (strictes) :

- Les ids de plugin inconnus dans `entries`, `allow`, `deny`, ou `slots` sont des **erreurs**.
- Les clés `channels.<id>` inconnues sont des **erreurs** sauf si un manifeste de plugin déclare
  l'id du canal.
- La configuration du plugin est validée en utilisant le schéma JSON intégré dans
  `openclaw.plugin.json` (`configSchema`).
- Si un plugin est désactivé, sa configuration est préservée et un **avertissement** est émis.

### Désactivé vs manquant vs invalide

Ces états sont intentionnellement différents :

- **désactivé** : le plugin existe, mais les règles d'activation l'ont désactivé
- **manquant** : la configuration référence un id de plugin que la découverte n'a pas trouvé
- **invalide** : le plugin existe, mais sa configuration ne correspond pas au schéma déclaré

OpenClaw préserve la configuration des plugins désactivés pour que les réactiver ne soit pas
destructeur.

## Emplacements de plugin (catégories exclusives)

Certaines catégories de plugin sont **exclusives** (un seul actif à la fois). Utilisez
`plugins.slots` pour sélectionner quel plugin possède l'emplacement :

```json5
{
  plugins: {
    slots: {
      memory: "memory-core", // ou "none" pour désactiver les plugins de mémoire
      contextEngine: "legacy", // ou un id de plugin tel que "lossless-claw"
    },
  },
}
```

Emplacements exclusifs supportés :

- `memory` : plugin de mémoire actif (`"none"` désactive les plugins de mémoire)
- `contextEngine` : plugin de moteur de contexte actif (`"legacy"` est la valeur par défaut intégrée)

Si plusieurs plugins déclarent `kind: "memory"` ou `kind: "context-engine"`, seul
le plugin sélectionné se charge pour cet emplacement. Les autres sont désactivés avec des diagnostics.

### Plugins de moteur de contexte

Les plugins de moteur de contexte possèdent l'orchestration du contexte de session pour l'ingestion, l'assemblage,
et la compaction. Enregistrez-les à partir de votre plugin avec
`api.registerContextEngine(id, factory)`, puis sélectionnez le moteur actif avec
`plugins.slots.contextEngine`.

Utilisez ceci quand votre plugin doit remplacer ou étendre le pipeline de contexte par défaut
plutôt que juste ajouter la recherche de mémoire ou des hooks.

## Interface utilisateur de contrôle (schéma + étiquettes)

L'interface utilisateur de contrôle utilise `config.schema` (schéma JSON + `uiHints`) pour rendre de meilleures formes.

OpenClaw augmente `uiHints` à l'exécution en fonction des plugins découverts :

- Ajoute des étiquettes par plugin pour `plugins.entries.<id>` / `.enabled` / `.config`
- Fusionne les indices de champ de configuration fournis par le plugin optionnel sous :
  `plugins.entries.<id>.config.<field>`

Si vous voulez que vos champs de configuration de plugin affichent de bonnes étiquettes/espaces réservés (et marquent les secrets comme sensibles),
fournissez `uiHints` aux côtés de votre schéma JSON dans le manifeste du plugin.

Exemple :

```json
{
  "id": "my-plugin",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" },
      "region": { "type": "string" }
    }
  },
  "uiHints": {
    "apiKey": { "label": "Clé API", "sensitive": true },
    "region": { "label": "Région", "placeholder": "us-east-1" }
  }
}
```

## CLI

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins install <path>                 # copy a local file/dir into ~/.openclaw/extensions/<id>
openclaw plugins install ./extensions/voice-call # relative path ok
openclaw plugins install ./plugin.tgz           # install from a local tarball
openclaw plugins install ./plugin.zip           # install from a local zip
openclaw plugins install -l ./extensions/voice-call # link (no copy) for dev
openclaw plugins install @openclaw/voice-call # install from npm
openclaw plugins install @openclaw/voice-call --pin # store exact resolved name@version
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

`plugins update` fonctionne uniquement pour les installations npm suivies sous `plugins.installs`.
Si les métadonnées d'intégrité stockées changent entre les mises à jour, OpenClaw avertit et demande une confirmation (utilisez le global `--yes` pour contourner les invites).

Les plugins peuvent également enregistrer leurs propres commandes de haut niveau (exemple : `openclaw voicecall`).

## API des plugins (aperçu)

Les plugins exportent soit :

- Une fonction : `(api) => { ... }`
- Un objet : `{ id, name, configSchema, register(api) { ... } }`

`register(api)` est l'endroit où les plugins attachent le comportement. Les enregistrements courants incluent :

- `registerTool`
- `registerHook`
- `on(...)` pour les hooks de cycle de vie typés
- `registerChannel`
- `registerProvider`
- `registerHttpRoute`
- `registerCommand`
- `registerCli`
- `registerContextEngine`
- `registerService`

Les plugins de moteur de contexte peuvent également enregistrer un gestionnaire de contexte détenu par le runtime :

```ts
export default function (api) {
  api.registerContextEngine("lossless-claw", () => ({
    info: { id: "lossless-claw", name: "Lossless Claw", ownsCompaction: true },
    async ingest() {
      return { ingested: true };
    },
    async assemble({ messages }) {
      return { messages, estimatedTokens: 0 };
    },
    async compact() {
      return { ok: true, compacted: false };
    },
  }));
}
```

Ensuite, activez-le dans la configuration :

```json5
{
  plugins: {
    slots: {
      contextEngine: "lossless-claw",
    },
  },
}
```

## Hooks des plugins

Les plugins peuvent enregistrer des hooks au runtime. Cela permet à un plugin de regrouper l'automatisation pilotée par les événements sans une installation de pack de hook séparé.

### Exemple

```ts
export default function register(api) {
  api.registerHook(
    "command:new",
    async () => {
      // Hook logic here.
    },
    {
      name: "my-plugin.command-new",
      description: "Runs when /new is invoked",
    },
  );
}
```

Notes :

- Enregistrez les hooks explicitement via `api.registerHook(...)`.
- Les règles d'éligibilité des hooks s'appliquent toujours (exigences OS/bins/env/config).
- Les hooks gérés par les plugins apparaissent dans `openclaw hooks list` avec `plugin:<id>`.
- Vous ne pouvez pas activer/désactiver les hooks gérés par les plugins via `openclaw hooks` ; activez/désactivez plutôt le plugin.

### Hooks du cycle de vie de l'agent (`api.on`)

Pour les hooks de cycle de vie du runtime typés, utilisez `api.on(...)` :

```ts
export default function register(api) {
  api.on(
    "before_prompt_build",
    (event, ctx) => {
      return {
        prependSystemContext: "Follow company style guide.",
      };
    },
    { priority: 10 },
  );
}
```

Hooks importants pour la construction du prompt :

- `before_model_resolve` : s'exécute avant le chargement de la session (`messages` ne sont pas disponibles). Utilisez ceci pour remplacer de manière déterministe `modelOverride` ou `providerOverride`.
- `before_prompt_build` : s'exécute après le chargement de la session (`messages` sont disponibles). Utilisez ceci pour façonner l'entrée du prompt.
- `before_agent_start` : hook de compatibilité hérité. Préférez les deux hooks explicites ci-dessus.

Politique de hook appliquée par le noyau :

- Les opérateurs peuvent désactiver les hooks de mutation de prompt par plugin via `plugins.entries.<id>.hooks.allowPromptInjection: false`.
- Lorsqu'elle est désactivée, OpenClaw bloque `before_prompt_build` et ignore les champs mutant le prompt retournés par le hook hérité `before_agent_start` tout en préservant les `modelOverride` et `providerOverride` hérités.

Champs de résultat `before_prompt_build` :

- `prependContext` : ajoute du texte au début du prompt utilisateur pour cette exécution. Idéal pour le contenu spécifique au tour ou dynamique.
- `systemPrompt` : remplacement complet du prompt système.
- `prependSystemContext` : ajoute du texte au début du prompt système actuel.
- `appendSystemContext` : ajoute du texte à la fin du prompt système actuel.

Ordre de construction du prompt dans le runtime intégré :

1. Appliquez `prependContext` au prompt utilisateur.
2. Appliquez le remplacement `systemPrompt` lorsqu'il est fourni.
3. Appliquez `prependSystemContext + prompt système actuel + appendSystemContext`.

Notes de fusion et de précédence :

- Les gestionnaires de hooks s'exécutent par priorité (plus élevée en premier).
- Pour les champs de contexte fusionnés, les valeurs sont concaténées dans l'ordre d'exécution.
- Les valeurs `before_prompt_build` sont appliquées avant les valeurs de secours héritées `before_agent_start`.

Conseils de migration :

- Déplacez les conseils statiques de `prependContext` vers `prependSystemContext` (ou `appendSystemContext`) afin que les fournisseurs puissent mettre en cache le contenu du préfixe système stable.
- Conservez `prependContext` pour le contexte dynamique par tour qui doit rester lié au message utilisateur.

## Plugins de fournisseur (authentification de modèle)

Les plugins peuvent enregistrer des **fournisseurs de modèles** pour que les utilisateurs puissent exécuter la configuration OAuth ou de clé API dans OpenClaw, afficher la configuration du fournisseur dans l'intégration/les sélecteurs de modèles, et contribuer à la découverte implicite du fournisseur.

Les plugins de fournisseur sont la couture d'extension modulaire pour la configuration du fournisseur de modèles. Ce ne sont plus seulement des « assistants OAuth ».

### Cycle de vie du plugin de fournisseur

Un plugin de fournisseur peut participer à cinq phases distinctes :

1. **Authentification**
   `auth[].run(ctx)` effectue OAuth, la capture de clé API, le code d'appareil ou la configuration personnalisée et retourne les profils d'authentification plus les correctifs de configuration optionnels.
2. **Configuration non interactive**
   `auth[].runNonInteractive(ctx)` gère `openclaw onboard --non-interactive` sans invites. Utilisez ceci lorsque le fournisseur a besoin d'une configuration sans interface au-delà des chemins de clé API simples intégrés.
3. **Intégration de l'assistant**
   `wizard.onboarding` ajoute une entrée à `openclaw onboard`.
   `wizard.modelPicker` ajoute une entrée de configuration au sélecteur de modèles.
4. **Découverte implicite**
   `discovery.run(ctx)` peut contribuer à la configuration du fournisseur automatiquement lors de la résolution/énumération des modèles.
5. **Suivi après sélection**
   `onModelSelected(ctx)` s'exécute après qu'un modèle est choisi. Utilisez ceci pour les travaux spécifiques au fournisseur tels que le téléchargement d'un modèle local.

Cette division est recommandée car ces phases ont des exigences de cycle de vie différentes :

- l'authentification est interactive et écrit les identifiants/configuration
- la configuration non interactive est pilotée par des drapeaux/env et ne doit pas inviter
- les métadonnées de l'assistant sont statiques et orientées vers l'interface utilisateur
- la découverte doit être sûre, rapide et tolérante aux défaillances
- les crochets post-sélection sont des effets secondaires liés au modèle choisi

### Contrat d'authentification du fournisseur

`auth[].run(ctx)` retourne :

- `profiles` : profils d'authentification à écrire
- `configPatch` : modifications optionnelles de `openclaw.json`
- `defaultModel` : référence optionnelle `provider/model`
- `notes` : notes optionnelles destinées à l'utilisateur

Le noyau fait alors :

1. écrit les profils d'authentification retournés
2. applique le câblage de configuration du profil d'authentification
3. fusionne le correctif de configuration
4. applique optionnellement le modèle par défaut
5. exécute le crochet `onModelSelected` du fournisseur le cas échéant

Cela signifie qu'un plugin de fournisseur possède la logique de configuration spécifique au fournisseur, tandis que le noyau possède le chemin générique de persistance et de fusion de configuration.

### Contrat non interactif du fournisseur

`auth[].runNonInteractive(ctx)` est optionnel. Implémentez-le lorsque le fournisseur a besoin d'une configuration sans interface qui ne peut pas être exprimée par les flux de clé API génériques intégrés.

Le contexte non interactif inclut :

- la configuration actuelle et de base
- les options CLI d'intégration analysées
- les assistants de journalisation/erreur d'exécution
- les répertoires d'agent/espace de travail
- `resolveApiKey(...)` pour lire les clés du fournisseur à partir des drapeaux, env ou des profils d'authentification existants tout en respectant `--secret-input-mode`
- `toApiKeyCredential(...)` pour convertir une clé résolue en identifiant de profil d'authentification avec le stockage en texte brut ou en référence secrète approprié

Utilisez cette surface pour les fournisseurs tels que :

- les runtimes compatibles OpenAI auto-hébergés qui ont besoin de `--custom-base-url` + `--custom-model-id`
- la vérification non interactive spécifique au fournisseur ou la synthèse de configuration

Ne pas inviter depuis `runNonInteractive`. Rejetez plutôt les entrées manquantes avec des erreurs exploitables.

### Métadonnées de l'assistant du fournisseur

`wizard.onboarding` contrôle comment le fournisseur apparaît dans l'intégration groupée :

- `choiceId` : valeur du choix d'authentification
- `choiceLabel` : étiquette de l'option
- `choiceHint` : indice court
- `groupId` : id du compartiment de groupe
- `groupLabel` : étiquette du groupe
- `groupHint` : indice du groupe
- `methodId` : méthode d'authentification à exécuter

`wizard.modelPicker` contrôle comment un fournisseur apparaît comme une entrée « configurer maintenant » dans la sélection de modèles :

- `label`
- `hint`
- `methodId`

Lorsqu'un fournisseur a plusieurs méthodes d'authentification, l'assistant peut soit pointer vers une méthode explicite, soit laisser OpenClaw synthétiser les choix par méthode.

OpenClaw valide les métadonnées de l'assistant du fournisseur lors de l'enregistrement du plugin :

- les ids de méthode d'authentification en double ou vides sont rejetés
- les métadonnées de l'assistant sont ignorées lorsque le fournisseur n'a pas de méthodes d'authentification
- les liaisons `methodId` invalides sont rétrogradées en avertissements et reviennent aux méthodes d'authentification restantes du fournisseur

### Contrat de découverte du fournisseur

`discovery.run(ctx)` retourne l'un des éléments suivants :

- `{ provider }`
- `{ providers }`
- `null`

Utilisez `{ provider }` pour le cas courant où le plugin possède un id de fournisseur. Utilisez `{ providers }` lorsqu'un plugin découvre plusieurs entrées de fournisseur.

Le contexte de découverte inclut :

- la configuration actuelle
- les répertoires d'agent/espace de travail
- l'env du processus
- un assistant pour résoudre la clé API du fournisseur et une valeur de clé API sûre pour la découverte

La découverte doit être :

- rapide
- au mieux
- sûre à ignorer en cas d'échec
- prudente quant aux effets secondaires

Elle ne doit pas dépendre d'invites ou de configuration longue.

### Ordre de découverte

La découverte du fournisseur s'exécute en phases ordonnées :

- `simple`
- `profile`
- `paired`
- `late`

Utilisez :

- `simple` pour la découverte bon marché basée sur l'environnement uniquement
- `profile` lorsque la découverte dépend des profils d'authentification
- `paired` pour les fournisseurs qui doivent se coordonner avec une autre étape de découverte
- `late` pour le sondage coûteux ou du réseau local

La plupart des fournisseurs auto-hébergés doivent utiliser `late`.

### Bonnes limites de plugin de fournisseur

Bon ajustement pour les plugins de fournisseur :

- fournisseurs locaux/auto-hébergés avec des flux de configuration personnalisés
- OAuth spécifique au fournisseur/connexion par code d'appareil
- découverte implicite des serveurs de modèles locaux
- effets secondaires après sélection tels que les extraits de modèles

Ajustement moins convaincant :

- fournisseurs triviaux de clé API uniquement qui ne diffèrent que par la variable env, l'URL de base et un modèle par défaut

Ceux-ci peuvent toujours devenir des plugins, mais le principal avantage de modularité provient de l'extraction des fournisseurs riches en comportement en premier.

Enregistrez un fournisseur via `api.registerProvider(...)`. Chaque fournisseur expose une ou plusieurs méthodes d'authentification (OAuth, clé API, code d'appareil, etc.). Ces méthodes peuvent alimenter :

- `openclaw models auth login --provider <id> [--method <id>]`
- `openclaw onboard`
- les entrées de configuration du fournisseur personnalisé du sélecteur de modèles
- la découverte implicite du fournisseur lors de la résolution/énumération des modèles

Exemple :

```ts
api.registerProvider({
  id: "acme",
  label: "AcmeAI",
  auth: [
    {
      id: "oauth",
      label: "OAuth",
      kind: "oauth",
      run: async (ctx) => {
        // Run OAuth flow and return auth profiles.
        return {
          profiles: [
            {
              profileId: "acme:default",
              credential: {
                type: "oauth",
                provider: "acme",
                access: "...",
                refresh: "...",
                expires: Date.now() + 3600 * 1000,
              },
            },
          ],
          defaultModel: "acme/opus-1",
        };
      },
    },
  ],
  wizard: {
    onboarding: {
      choiceId: "acme",
      choiceLabel: "AcmeAI",
      groupId: "acme",
      groupLabel: "AcmeAI",
      methodId: "oauth",
    },
    modelPicker: {
      label: "AcmeAI (custom)",
      hint: "Connect a self-hosted AcmeAI endpoint",
      methodId: "oauth",
    },
  },
  discovery: {
    order: "late",
    run: async () => ({
      provider: {
        baseUrl: "https://acme.example/v1",
        api: "openai-completions",
        apiKey: "${ACME_API_KEY}",
        models: [],
      },
    }),
  },
});
```

Notes :

- `run` reçoit un `ProviderAuthContext` avec les assistants `prompter`, `runtime`, `openUrl` et `oauth.createVpsAwareHandlers`.
- `runNonInteractive` reçoit un `ProviderAuthMethodNonInteractiveContext` avec les assistants `opts`, `resolveApiKey` et `toApiKeyCredential` pour l'intégration sans interface.
- Retournez `configPatch` lorsque vous devez ajouter des modèles par défaut ou une configuration de fournisseur.
- Retournez `defaultModel` pour que `--set-default` puisse mettre à jour les valeurs par défaut de l'agent.
- `wizard.onboarding` ajoute un choix de fournisseur à `openclaw onboard`.
- `wizard.modelPicker` ajoute une entrée « configurer ce fournisseur » au sélecteur de modèles.
- `discovery.run` retourne soit `{ provider }` pour l'id de fournisseur du plugin, soit `{ providers }` pour la découverte multi-fournisseur.
- `discovery.order` contrôle quand le fournisseur s'exécute par rapport aux phases de découverte intégrées : `simple`, `profile`, `paired` ou `late`.
- `onModelSelected` est le crochet post-sélection pour les travaux de suivi spécifiques au fournisseur tels que l'extraction d'un modèle local.

### Enregistrer un canal de messagerie

Les plugins peuvent enregistrer des **plugins de canal** qui se comportent comme des canaux intégrés (WhatsApp, Telegram, etc.). La configuration du canal se trouve sous `channels.<id>` et est validée par le code de votre plugin de canal.

```ts
const myChannel = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "demo channel plugin.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async () => ({ ok: true }),
  },
};

export default function (api) {
  api.registerChannel({ plugin: myChannel });
}
```

Notes :

- Mettez la configuration sous `channels.<id>` (pas `plugins.entries`).
- `meta.label` est utilisé pour les étiquettes dans les listes CLI/UI.
- `meta.aliases` ajoute des ids alternatifs pour la normalisation et les entrées CLI.
- `meta.preferOver` répertorie les ids de canal à ignorer lors de l'activation automatique lorsque les deux sont configurés.
- `meta.detailLabel` et `meta.systemImage` permettent aux interfaces utilisateur d'afficher des étiquettes/icônes de canal plus riches.

### Crochets d'intégration du canal

Les plugins de canal peuvent définir des crochets d'intégration optionnels sur `plugin.onboarding` :

- `configure(ctx)` est le flux de configuration de base.
- `configureInteractive(ctx)` peut posséder entièrement la configuration interactive pour les états configurés et non configurés.
- `configureWhenConfigured(ctx)` peut remplacer le comportement uniquement pour les canaux déjà configurés.

Précédence des crochets dans l'assistant :

1. `configureInteractive` (si présent)
2. `configureWhenConfigured` (uniquement lorsque l'état du canal est déjà configuré)
3. revenir à `configure`

Détails du contexte :

- `configureInteractive` et `configureWhenConfigured` reçoivent :
  - `configured` (`true` ou `false`)
  - `label` (nom du canal destiné à l'utilisateur utilisé par les invites)
  - plus les champs partagés config/runtime/prompter/options
- Retourner `"skip"` laisse la sélection et le suivi des comptes inchangés.
- Retourner `{ cfg, accountId? }` applique les mises à jour de configuration et enregistre la sélection du compte.

### Écrire un nouveau canal de messagerie (étape par étape)

Utilisez ceci lorsque vous voulez une **nouvelle surface de chat** (un « canal de messagerie »), pas un fournisseur de modèles.
La documentation du fournisseur de modèles se trouve sous `/providers/*`.

1. Choisissez un id + une forme de configuration

- Toute la configuration du canal se trouve sous `channels.<id>`.
- Préférez `channels.<id>.accounts.<accountId>` pour les configurations multi-comptes.

2. Définissez les métadonnées du canal

- `meta.label`, `meta.selectionLabel`, `meta.docsPath`, `meta.blurb` contrôlent les listes CLI/UI.
- `meta.docsPath` doit pointer vers une page de documentation comme `/channels/<id>`.
- `meta.preferOver` permet à un plugin de remplacer un autre canal (l'activation automatique le préfère).
- `meta.detailLabel` et `meta.systemImage` sont utilisés par les interfaces utilisateur pour le texte de détail/les icônes.

3. Implémentez les adaptateurs requis

- `config.listAccountIds` + `config.resolveAccount`
- `capabilities` (types de chat, médias, threads, etc.)
- `outbound.deliveryMode` + `outbound.sendText` (pour l'envoi basique)

4. Ajoutez des adaptateurs optionnels selon les besoins

- `setup` (assistant), `security` (politique DM), `status` (santé/diagnostics)
- `gateway` (démarrer/arrêter/connexion), `mentions`, `threading`, `streaming`
- `actions` (actions de message), `commands` (comportement de commande native)

5. Enregistrez le canal dans votre plugin

- `api.registerChannel({ plugin })`

Exemple de configuration minimale :

```json5
{
  channels: {
    acmechat: {
      accounts: {
        default: { token: "ACME_TOKEN", enabled: true },
      },
    },
  },
}
```

Plugin de canal minimal (sortie uniquement) :

```ts
const plugin = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "AcmeChat messaging channel.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async ({ text }) => {
      // deliver `text` to your channel here
      return { ok: true };
    },
  },
};

export default function (api) {
  api.registerChannel({ plugin });
}
```

Chargez le plugin (répertoire des extensions ou `plugins.load.paths`), redémarrez la passerelle, puis configurez `channels.<id>` dans votre configuration.

### Outils d'agent

Voir le guide dédié : [Plugin agent tools](/fr/plugins/agent-tools).

### Enregistrer une méthode RPC de passerelle

```ts
export default function (api) {
  api.registerGatewayMethod("myplugin.status", ({ respond }) => {
    respond(true, { ok: true });
  });
}
```

### Enregistrer les commandes CLI

```ts
export default function (api) {
  api.registerCli(
    ({ program }) => {
      program.command("mycmd").action(() => {
        console.log("Hello");
      });
    },
    { commands: ["mycmd"] },
  );
}
```

### Enregistrer les commandes de réponse automatique

Les plugins peuvent enregistrer des commandes de barre oblique personnalisées qui s'exécutent **sans invoquer l'agent IA**. Ceci est utile pour les commandes de basculement, les vérifications d'état ou les actions rapides qui n'ont pas besoin de traitement LLM.

```ts
export default function (api) {
  api.registerCommand({
    name: "mystatus",
    description: "Show plugin status",
    handler: (ctx) => ({
      text: `Plugin is running! Channel: ${ctx.channel}`,
    }),
  });
}
```

Contexte du gestionnaire de commande :

- `senderId` : L'ID de l'expéditeur (le cas échéant)
- `channel` : Le canal où la commande a été envoyée
- `isAuthorizedSender` : Si l'expéditeur est un utilisateur autorisé
- `args` : Arguments passés après la commande (si `acceptsArgs: true`)
- `commandBody` : Le texte de commande complet
- `config` : La configuration OpenClaw actuelle

Options de commande :

- `name` : Nom de la commande (sans la barre oblique initiale)
- `nativeNames` : Alias de commande native optionnels pour les surfaces de barre oblique/menu. Utilisez `default` pour tous les fournisseurs natifs, ou des clés spécifiques au fournisseur comme `discord`
- `description` : Texte d'aide affiché dans les listes de commandes
- `acceptsArgs` : Si la commande accepte des arguments (par défaut : false). Si false et que des arguments sont fournis, la commande ne correspondra pas et le message passera à d'autres gestionnaires
- `requireAuth` : Si l'expéditeur autorisé est requis (par défaut : true)
- `handler` : Fonction qui retourne `{ text: string }` (peut être asynchrone)

Exemple avec autorisation et arguments :

```ts
api.registerCommand({
  name: "setmode",
  description: "Set plugin mode",
  acceptsArgs: true,
  requireAuth: true,
  handler: async (ctx) => {
    const mode = ctx.args?.trim() || "default";
    await saveMode(mode);
    return { text: `Mode set to: ${mode}` };
  },
});
```

Notes :

- Les commandes de plugin sont traitées **avant** les commandes intégrées et l'agent IA
- Les commandes sont enregistrées globalement et fonctionnent sur tous les canaux
- Les noms de commande ne sont pas sensibles à la casse (`/MyStatus` correspond à `/mystatus`)
- Les noms de commande doivent commencer par une lettre et contenir uniquement des lettres, des chiffres, des tirets et des traits de soulignement
- Les noms de commande réservés (comme `help`, `status`, `reset`, etc.) ne peuvent pas être remplacés par les plugins
- L'enregistrement de commandes en double entre les plugins échouera avec une erreur de diagnostic

### Enregistrer les services d'arrière-plan

```ts
export default function (api) {
  api.registerService({
    id: "my-service",
    start: () => api.logger.info("ready"),
    stop: () => api.logger.info("bye"),
  });
}
```

## Conventions de nommage

- Méthodes Gateway : `pluginId.action` (exemple : `voicecall.status`)
- Outils : `snake_case` (exemple : `voice_call`)
- Commandes CLI : kebab ou camel, mais évitez les conflits avec les commandes principales

## Compétences

Les plugins peuvent livrer une compétence dans le dépôt (`skills/<name>/SKILL.md`).
Activez-la avec `plugins.entries.<id>.enabled` (ou d'autres portes de configuration) et assurez-vous
qu'elle est présente dans vos emplacements de compétences workspace/gérées.

## Distribution (npm)

Empaquetage recommandé :

- Package principal : `openclaw` (ce dépôt)
- Plugins : packages npm séparés sous `@openclaw/*` (exemple : `@openclaw/voice-call`)

Contrat de publication :

- Le `package.json` du plugin doit inclure `openclaw.extensions` avec un ou plusieurs fichiers d'entrée.
- Les fichiers d'entrée peuvent être `.js` ou `.ts` (jiti charge TS à l'exécution).
- `openclaw plugins install <npm-spec>` utilise `npm pack`, extrait dans `~/.openclaw/extensions/<id>/`, et l'active dans la configuration.
- Stabilité de la clé de configuration : les packages scoped sont normalisés à l'id **non-scoped** pour `plugins.entries.*`.

## Exemple de plugin : Voice Call

Ce dépôt inclut un plugin voice-call (Twilio ou fallback log) :

- Source : `extensions/voice-call`
- Compétence : `skills/voice-call`
- CLI : `openclaw voicecall start|status`
- Outil : `voice_call`
- RPC : `voicecall.start`, `voicecall.status`
- Configuration (twilio) : `provider: "twilio"` + `twilio.accountSid/authToken/from` (optionnel `statusCallbackUrl`, `twimlUrl`)
- Configuration (dev) : `provider: "log"` (pas de réseau)

Consultez [Voice Call](/fr/plugins/voice-call) et `extensions/voice-call/README.md` pour la configuration et l'utilisation.

## Notes de sécurité

Les plugins s'exécutent dans le processus avec la Gateway. Traitez-les comme du code de confiance :

- Installez uniquement les plugins en lesquels vous avez confiance.
- Préférez les listes blanches `plugins.allow`.
- Rappelez-vous que `plugins.allow` est basé sur l'id, donc un plugin workspace activé peut
  intentionnellement masquer un plugin bundlé avec le même id.
- Redémarrez la Gateway après les modifications.

## Test des plugins

Les plugins peuvent (et doivent) livrer des tests :

- Les plugins dans le dépôt peuvent conserver les tests Vitest sous `src/**` (exemple : `src/plugins/voice-call.plugin.test.ts`).
- Les plugins publiés séparément doivent exécuter leur propre CI (lint/build/test) et valider que `openclaw.extensions` pointe vers le point d'entrée construit (`dist/index.js`).
