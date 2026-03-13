---
read_when:
  - Ajouter ou modifier des plugins/extensions
  - Documenter les règles d'installation ou de chargement des plugins
summary: Plugins/extensions OpenClaw : découverte, configuration et sécurité
title: Plugins
x-i18n:
  generated_at: "2026-02-03T07:55:25Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b36ca6b90ca03eaae25c00f9b12f2717fcd17ac540ba616ee03b398b234c2308
  source_path: tools/plugin.md
  workflow: 15
---

# Plugins (Extensions)

## Démarrage rapide (Nouveau aux plugins ?)

Les plugins sont simplement de **petits modules de code** qui étendent OpenClaw avec des fonctionnalités supplémentaires (commandes, outils et RPC Gateway).

La plupart du temps, vous utiliserez des plugins lorsque vous souhaitez une fonctionnalité qui n'est pas encore intégrée au cœur d'OpenClaw (ou que vous souhaitez exclure une fonctionnalité optionnelle de l'installation principale).

Chemin rapide :

1. Voir ce qui est chargé :

```bash
openclaw plugins list
```

2. Installer un plugin officiel (par exemple : Voice Call) :

```bash
openclaw plugins install @openclaw/voice-call
```

3. Redémarrer la Gateway, puis configurer sous `plugins.entries.<id>.config`.

Voir [Voice Call](/plugins/voice-call) pour un exemple de plugin spécifique.

## Plugins disponibles (Officiels)

- À partir du 15.01.2026, Microsoft Teams n'est disponible que comme plugin ; si vous utilisez Teams, installez `@openclaw/msteams`.
- Memory (Core) — Plugin de recherche mémoire fourni (activé par défaut via `plugins.slots.memory`)
- Memory (LanceDB) — Plugin de mémoire à long terme fourni (rappel/capture automatiques ; définissez `plugins.slots.memory = "memory-lancedb"`)
- [Voice Call](/plugins/voice-call) — `@openclaw/voice-call`
- [Zalo Personal](/plugins/zalouser) — `@openclaw/zalouser`
- [Matrix](/channels/matrix) — `@openclaw/matrix`
- [Nostr](/channels/nostr) — `@openclaw/nostr`
- [Zalo](/channels/zalo) — `@openclaw/zalo`
- [Microsoft Teams](/channels/msteams) — `@openclaw/msteams`
- Google Antigravity OAuth (authentification du fournisseur) — Fourni en tant que `google-antigravity-auth` (désactivé par défaut)
- Gemini CLI OAuth (authentification du fournisseur) — Fourni en tant que `google-gemini-cli-auth` (désactivé par défaut)
- Qwen OAuth (authentification du fournisseur) — Fourni en tant que `qwen-portal-auth` (désactivé par défaut)
- Copilot Proxy (authentification du fournisseur) — Pont local VS Code Copilot Proxy ; différent de la connexion d'appareil `github-copilot` intégrée (fourni, désactivé par défaut)

Les plugins OpenClaw sont des **modules TypeScript** chargés au runtime via jiti. **La validation de configuration n'exécute pas le code du plugin** ; elle utilise le manifeste du plugin et JSON Schema. Voir [Manifeste du plugin](/plugins/manifest).

Les plugins peuvent enregistrer :

- Des méthodes RPC Gateway
- Des gestionnaires HTTP Gateway
- Des outils d'agent
- Des commandes CLI
- Des services en arrière-plan
- Une validation de configuration optionnelle
- **Skills** (en listant le répertoire `skills` dans le manifeste du plugin)
- **Commandes de réponse automatique** (exécutées sans invoquer l'agent IA)

Les plugins s'exécutent **dans le même processus** que la Gateway, traitez-les donc comme du code de confiance.
Guide d'écriture d'outils : [Outils d'agent de plugin](/plugins/agent-tools).

## Utilitaires d'exécution

Les plugins peuvent accéder aux utilitaires principaux sélectionnés via `api.runtime`. Pour la TTS téléphonique :

```ts
const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
```

Remarques :

- Utilise la configuration `messages.tts` du cœur (OpenAI ou ElevenLabs).
- Retourne un buffer audio PCM + taux d'échantillonnage. Le plugin doit rééchantillonner/encoder pour le fournisseur.
- Edge TTS n'est pas supporté pour la téléphonie.

## Découverte et priorité

OpenClaw scanne dans cet ordre :

1. Chemins de configuration

- `plugins.load.paths` (fichier ou répertoire)

2. Extensions d'espace de travail

- `<workspace>/.openclaw/extensions/*.ts`
- `<workspace>/.openclaw/extensions/*/index.ts`

3. Extensions globales

- `~/.openclaw/extensions/*.ts`
- `~/.openclaw/extensions/*/index.ts`

4. Extensions fournies (publiées avec OpenClaw, **désactivées par défaut**)

- `<openclaw>/extensions/*`

Les plugins fournis doivent être explicitement activés via `plugins.entries.<id>.enabled` ou `openclaw plugins enable <id>`. Les plugins installés sont activés par défaut, mais peuvent être désactivés de la même manière.

Chaque plugin doit contenir un fichier `openclaw.plugin.json` dans son répertoire racine. Si le chemin pointe vers un fichier, le répertoire racine du plugin est le répertoire du fichier, qui doit contenir le manifeste.

Si plusieurs plugins se résolvent au même id, le premier match dans l'ordre ci-dessus gagne, les copies de priorité inférieure sont ignorées.

### Collections de paquets

Un répertoire de plugins peut contenir un `package.json` avec `openclaw.extensions` :

```json
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"]
  }
}
```

Chaque entrée devient un plugin. Si le paquet liste plusieurs extensions, l'id du plugin devient `name/<fileBase>`.

Si votre plugin importe des dépendances npm, installez-les dans ce répertoire pour que `node_modules` soit disponible (`npm install` / `pnpm install`).

### Métadonnées du répertoire des canaux

Les plugins de canal peuvent diffuser des métadonnées d'onboarding via `openclaw.channel`, et des invites d'installation via `openclaw.install`. Cela garde le répertoire principal sans données.

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

OpenClaw peut également fusionner des **catalogues de canaux externes** (par exemple, exports de registre MPM). Placez un fichier JSON dans l'un de ces emplacements :

- `~/.openclaw/mpm/plugins.json`
- `~/.openclaw/mpm/catalog.json`
- `~/.openclaw/plugins/catalog.json`

Ou pointez `OPENCLAW_PLUGIN_CATALOG_PATHS` (ou `OPENCLAW_MPM_CATALOG_PATHS`) vers un ou plusieurs fichiers JSON (séparés par virgule/point-virgule/`PATH`). Chaque fichier doit contenir `{ "entries": [ { "name": "@scope/pkg", "openclaw": { "channel": {...}, "install": {...} } } ] }`.

## ID de plugin

ID de plugin par défaut :

- Collections de paquets : `name` du `package.json`
- Fichiers autonomes : nom de base du fichier (`~/.../voice-call.ts` → `voice-call`)

Si le plugin exporte un `id`, OpenClaw l'utilisera, mais émettra un avertissement s'il ne correspond pas à l'id configuré.

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

- `enabled` : commutateur principal (par défaut : true)
- `allow` : liste blanche (optionnel)
- `deny` : liste noire (optionnel ; deny a priorité)
- `load.paths` : fichiers/répertoires de plugins supplémentaires
- `entries.<id>` : commutateur par plugin + configuration

Les changements de configuration **nécessitent un redémarrage de la Gateway**.

Règles de validation (strictes) :

- Les id de plugin inconnus dans `entries`, `allow`, `deny` ou `slots` sont une **erreur**.
- Les clés `channels.<id>` inconnues sont une **erreur**, sauf si le manifeste du plugin déclare l'id du canal.
- La configuration du plugin est validée avec JSON Schema intégré dans `openclaw.plugin.json` (`configSchema`).
- Si un plugin est désactivé, sa configuration est conservée et une **avertissement** est émis.

## Emplacements de plugin (Catégories exclusives)

Certaines catégories de plugins sont **exclusives** (une seule active à la fois). Utilisez `plugins.slots` pour sélectionner quel plugin possède l'emplacement :

```json5
{
  plugins: {
    slots: {
      memory: "memory-core", // or "none" to disable memory plugins
    },
  },
}
```

Si plusieurs plugins déclarent `kind: "memory"`, seul celui sélectionné est chargé. Les autres sont désactivés avec des informations de diagnostic.

## Interface de contrôle (schema + labels)

L'interface de contrôle utilise `config.schema` (JSON Schema + `uiHints`) pour rendre de meilleurs formulaires.

OpenClaw améliore `uiHints` au runtime en fonction des plugins découverts :

- Ajoute des labels par plugin pour `plugins.entries.<id>` / `.enabled` / `.config`
- Fusionne les hints de champs de configuration optionnels fournis par le plugin à :
  `plugins.entries.<id>.config.<field>`

Si vous souhaitez que les champs de configuration du plugin affichent de bons labels/placeholders (et marquent les clés comme sensibles), fournissez `uiHints` et JSON Schema dans le manifeste du plugin.

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
    "apiKey": { "label": "API Key", "sensitive": true },
    "region": { "label": "Region", "placeholder": "us-east-1" }
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
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

`plugins update` ne fonctionne que pour les installations npm suivies sous `plugins.installs`.

Les plugins peuvent également enregistrer leurs propres commandes de niveau supérieur (par exemple : `openclaw voicecall`).

## API de plugin (Aperçu)

Les plugins exportent l'un des éléments suivants :

- Fonction : `(api) => { ... }`
- Objet : `{ id, name, configSchema, register(api) { ... } }`

## Hooks de plugin

Les plugins peuvent être accompagnés de hooks et les enregistrer au runtime. Cela permet aux plugins de regrouper l'automatisation pilotée par événements sans nécessiter une installation de paquet de hook séparé.

### Exemple

```
import { registerPluginHooksFromDir } from "openclaw/plugin-sdk";

export default function register(api) {
  registerPluginHooksFromDir(api, "./hooks");
}
```

Remarques :

- Le répertoire des hooks suit la structure normale des hooks (`HOOK.md` + `handler.ts`).
- Les règles de qualification des hooks s'appliquent toujours (exigences d'OS/binaire/environnement/configuration).
- Les hooks gérés par les plugins s'affichent comme `plugin:<id>` dans `openclaw hooks list`.
- Vous ne pouvez pas activer/désactiver les hooks gérés par les plugins via `openclaw hooks` ; activez/désactivez plutôt le plugin.

## Plugins de fournisseur (Authentification de modèle)

Les plugins peuvent enregistrer des **flux d'authentification de fournisseur de modèle** pour que les utilisateurs puissent exécuter OAuth ou la configuration de clé API dans OpenClaw (sans scripts externes).

Enregistrez les fournisseurs via `api.registerProvider(...)`. Chaque fournisseur expose une ou plusieurs méthodes d'authentification (OAuth, clé API, code d'appareil, etc.). Ces méthodes pilotent :

- `openclaw models auth login --provider <id> [--method <id>]`

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
