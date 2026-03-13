---
read_when:
  - Lors de l'ajout ou de la modification de champs de configuration
summary: Toutes les options de configuration pour ~/.openclaw/openclaw.json avec des exemples
title: Configuration
x-i18n:
  generated_at: "2026-02-01T21:29:41Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b5e51290bbc755acb259ad455878625aa894c115e5c0ac6a1a3397e10fff8b4b
  source_path: gateway/configuration.md
  workflow: 15
---

# Configuration 🔧

OpenClaw lit une configuration **JSON5** optionnelle depuis `~/.openclaw/openclaw.json` (commentaires et virgules finales supportés).

Si le fichier n'existe pas, OpenClaw utilise des valeurs par défaut sécurisées (agent Pi intégré + sessions par expéditeur + espace de travail `~/.openclaw/workspace`). La configuration est généralement nécessaire uniquement pour :

- Limiter qui peut déclencher le bot (`channels.whatsapp.allowFrom`, `channels.telegram.allowFrom`, etc.)
- Contrôler la liste blanche des groupes + comportement des mentions (`channels.whatsapp.groups`, `channels.telegram.groups`, `channels.discord.guilds`, `agents.list[].groupChat`)
- Personnaliser les préfixes de message (`messages`)
- Définir les espaces de travail des agents (`agents.defaults.workspace` ou `agents.list[].workspace`)
- Ajuster les valeurs par défaut des agents intégrés (`agents.defaults`) et le comportement des sessions (`session`)
- Définir l'identité par agent (`agents.list[].identity`)

> **Nouveau à la configuration ?** Consultez le guide [Exemples de configuration](/gateway/configuration-examples) pour des exemples complets avec explications détaillées !

## Validation stricte de la configuration

OpenClaw n'accepte que les configurations qui correspondent exactement au schéma.
Les clés inconnues, les erreurs de type ou les valeurs invalides entraînent le **refus de démarrage** de la passerelle pour assurer la sécurité.

En cas d'échec de validation :

- La passerelle ne démarre pas.
- Seules les commandes de diagnostic sont autorisées (par exemple : `openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`, `openclaw service`, `openclaw help`).
- Exécutez `openclaw doctor` pour voir les problèmes spécifiques.
- Exécutez `openclaw doctor --fix` (ou `--yes`) pour appliquer les migrations/corrections.

Doctor n'écrira aucune modification à moins que vous n'ayez explicitement choisi `--fix`/`--yes`.

## Schéma + Conseils UI

La passerelle expose une représentation JSON Schema de la configuration via `config.schema` pour les éditeurs UI.
L'interface utilisateur de la console rend les formulaires en fonction de ce schéma et fournit un éditeur **JSON brut** comme secours.

Les plugins de canal et les extensions peuvent enregistrer des schémas + conseils UI pour leur configuration, de sorte que les paramètres de canal
restent pilotés par schéma dans les applications sans formulaires codés en dur.

Les conseils (étiquettes, groupes, champs sensibles) sont fournis avec le schéma, permettant aux clients de rendre de meilleurs formulaires sans connaissances de configuration codées en dur.

## Appliquer + Redémarrer (RPC)

Utilisez `config.apply` pour valider + écrire la configuration complète et redémarrer la passerelle en une seule étape.
Il écrit un fichier sentinelle de redémarrage et effectue un ping de la dernière session active après la récupération de la passerelle.

Avertissement : `config.apply` remplace **l'intégralité de la configuration**. Si vous souhaitez modifier uniquement certaines clés,
utilisez `config.patch` ou `openclaw config set`. Veuillez sauvegarder `~/.openclaw/openclaw.json`.

Paramètres :

- `raw` (chaîne) — Charge utile JSON5 pour la configuration complète
- `baseHash` (optionnel) — Hachage de configuration depuis `config.get` (obligatoire si la configuration existe)
- `sessionKey` (optionnel) — Clé de la dernière session active pour le ping de réveil
- `note` (optionnel) — Note à inclure dans la sentinelle de redémarrage
- `restartDelayMs` (optionnel) — Délai avant redémarrage (par défaut 2000)

Exemple (via `gateway call`) :

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.apply --params '{
  "raw": "{\\n  agents: { defaults: { workspace: \\"~/.openclaw/workspace\\" } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

## Mise à jour partielle (RPC)

Utilisez `config.patch` pour fusionner des mises à jour partielles dans la configuration existante sans écraser
les clés non liées. Il utilise la sémantique JSON merge patch :

- Les objets sont fusionnés récursivement
- `null` supprime les clés
- Les tableaux sont remplacés
  Comme `config.apply`, il valide, écrit la configuration, stocke la sentinelle de redémarrage et planifie
  le redémarrage de la passerelle (réveil optionnel quand `sessionKey` est fourni).

Paramètres :

- `raw` (chaîne) — Charge utile JSON5 contenant uniquement les clés à modifier
- `baseHash` (obligatoire) — Hachage de configuration depuis `config.get`
- `sessionKey` (optionnel) — Clé de la dernière session active pour le ping de réveil
- `note` (optionnel) — Note à inclure dans la sentinelle de redémarrage
- `restartDelayMs` (optionnel) — Délai avant redémarrage (par défaut 2000)

Exemple :

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.patch --params '{
  "raw": "{\\n  channels: { telegram: { groups: { \\"*\\": { requireMention: false } } } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

## Configuration minimale (point de départ recommandé)

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Construire l'image par défaut pour la première fois :

```bash
scripts/sandbox-setup.sh
```

## Mode auto-chat (recommandé pour le contrôle des groupes)

Empêcher le bot de répondre aux mentions WhatsApp @dans les groupes (répondre uniquement aux déclencheurs de texte spécifiques) :

```json5
{
  agents: {
    defaults: { workspace: "~/.openclaw/workspace" },
    list: [
      {
        id: "main",
        groupChat: { mentionPatterns: ["@openclaw", "reisponde"] },
      },
    ],
  },
  channels: {
    whatsapp: {
      // La liste blanche s'applique uniquement aux messages privés ; inclure votre propre numéro active le mode auto-chat.
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Inclusion de configuration (`$include`)

Utilisez la directive `$include` pour diviser la configuration en plusieurs fichiers. Utile pour :

- Organiser les grandes configurations (par exemple, définir les agents par client)
- Partager les paramètres communs entre les environnements
- Garder la configuration sensible séparée

### Utilisation de base

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },

  // Inclure un seul fichier (remplace la valeur de cette clé)
  agents: { $include: "./agents.json5" },

  // Inclure plusieurs fichiers (fusionnés en profondeur dans l'ordre)
  broadcast: {
    $include: ["./clients/mueller.json5", "./clients/schmidt.json5"],
  },
}
```

```json5
// ~/.openclaw/agents.json5
{
  defaults: { sandbox: { mode: "all", scope: "session" } },
  list: [{ id: "main", workspace: "~/.openclaw/workspace" }],
}
```

### Comportement de fusion

- **Fichier unique** : Remplace l'objet contenant `$include`
- **Tableau de fichiers** : Fusionnés en profondeur dans l'ordre (les fichiers ultérieurs remplacent les antérieurs)
- **Avec clés frères** : Les clés frères sont fusionnées après l'inclusion (remplacent les valeurs incluses)
- **Clés frères + tableau/valeur primitive** : Non supporté (le contenu inclus doit être un objet)

```json5
// Les clés frères remplacent le contenu inclus
{
  $include: "./base.json5", // { a: 1, b: 2 }
  b: 99, // Résultat : { a: 1, b: 99 }
}
```

### Inclusions imbriquées

Les fichiers inclus peuvent eux-mêmes contenir des directives `$include` (jusqu'à 10 niveaux de profondeur) :

```json5
// clients/mueller.json5
{
  agents: { $include: "./mueller/agents.json5" },
  broadcast: { $include: "./mueller/broadcast.json5" },
}
```

### Résolution des chemins

- **Chemins relatifs** : Résolus par rapport au fichier d'inclusion
- **Chemins absolus** : Utilisés directement
- **Répertoire parent** : Les références `../` fonctionnent comme prévu

```json5
{ "$include": "./sub/config.json5" }      // Chemin relatif
{ "$include": "/etc/openclaw/base.json5" } // Chemin absolu
{ "$include": "../shared/common.json5" }   // Répertoire parent
```

### Gestion des erreurs

- **Fichier manquant** : Erreur claire avec chemin résolu
- **Erreur d'analyse** : Indique quel fichier inclus a échoué
- **Inclusion circulaire** : Détectée et signalée

### Exemple : Configuration multi-clients pour cabinet juridique

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789, auth: { token: "secret" } },

  // Valeurs par défaut des agents communs
  agents: {
    defaults: {
      sandbox: { mode: "all", scope: "session" },
    },
    // Fusionner les listes d'agents de tous les clients
    list: { $include: ["./clients/mueller/agents.json5", "./clients/schmidt/agents.json5"] },
  },

  // Fusionner les configurations de diffusion
  broadcast: {
    $include: ["./clients/mueller/broadcast.json5", "./clients/schmidt/broadcast.json5"],
  },

  channels: { whatsapp: { groupPolicy: "allowlist" } },
}
```

```json5
// ~/.openclaw/clients/mueller/agents.json5
[
  { id: "mueller-transcribe", workspace: "~/clients/mueller/transcribe" },
  { id: "mueller-docs", workspace: "~/clients/mueller/docs" },
]
```

```json5
// ~/.openclaw/clients/mueller/broadcast.json5
{
  "120363403215116621@g.us": ["mueller-transcribe", "mueller-docs"],
}
```

## Options courantes

### Variables d'environnement + `.env`

OpenClaw lit les variables d'environnement du processus parent (shell, launchd/systemd, CI, etc.).

De plus, il charge :

- `.env` dans le répertoire de travail actuel (s'il existe)
- `~/.openclaw/.env` (c'est-à-dire `$OPENCLAW_STATE_DIR/.env`) comme `.env` de secours global

Aucun des deux fichiers `.env` ne remplace les variables d'environnement existantes.

Vous pouvez également fournir des variables d'environnement en ligne dans la configuration. Celles-ci ne s'appliquent que si la clé manque dans l'environnement du processus (même règle de non-remplacement) :

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

Voir [/environment](/help/environment) pour les détails de priorité et de source.

### `env.shellEnv` (optionnel)

Fonctionnalité de commodité optionnelle : si activée et que les clés attendues ne sont pas définies, OpenClaw exécutera votre shell de connexion et importera uniquement les clés attendues manquantes (sans remplacement).
Cela source effectivement vos fichiers de configuration de shell.

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Variables d'environnement équivalentes :

- `OPENCLAW_LOAD_SHELL_ENV=1`
- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

### Substitution de variables d'environnement dans la configuration

Vous pouvez référencer les variables d'environnement directement dans n'importe quelle valeur de chaîne de configuration en utilisant la syntaxe `${VAR_NAME}`. Les variables sont remplacées lors du chargement de la configuration, avant la validation.

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
  gateway: {
    auth: {
      token: "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

**Règles :**

- Correspond uniquement aux noms de variables d'environnement en majuscules : `[A-Z_][A-Z0-9_]*`
- Les variables d'environnement manquantes ou vides lèvent une erreur lors du chargement de la configuration
- Utilisez `$${VAR}` pour échapper et produire un littéral `${VAR}`
- Fonctionne avec `$include` (les fichiers inclus sont également remplacés)

**Substitution en ligne :**

```json5
{
  models: {
    providers: {
      custom: {
        baseUrl: "${CUSTOM_API_BASE}/v1", // → "https://api.example.com
