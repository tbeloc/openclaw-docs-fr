---
summary: "Hooks: automation pilotée par événements pour les commandes et les événements du cycle de vie"
read_when:
  - You want event-driven automation for /new, /reset, /stop, and agent lifecycle events
  - You want to build, install, or debug hooks
title: "Hooks"
---

# Hooks

Les hooks fournissent un système extensible piloté par événements pour automatiser les actions en réponse aux commandes et événements des agents. Les hooks sont automatiquement découverts à partir de répertoires et peuvent être gérés via des commandes CLI, de la même manière que les compétences fonctionnent dans OpenClaw.

## Orientation

Les hooks sont de petits scripts qui s'exécutent quand quelque chose se produit. Il y a deux types :

- **Hooks** (cette page) : s'exécutent à l'intérieur de la Gateway quand des événements d'agent se déclenchent, comme `/new`, `/reset`, `/stop`, ou des événements du cycle de vie.
- **Webhooks** : webhooks HTTP externes qui permettent à d'autres systèmes de déclencher du travail dans OpenClaw. Voir [Webhook Hooks](/automation/webhook) ou utiliser `openclaw webhooks` pour les commandes d'aide Gmail.

Les hooks peuvent également être regroupés à l'intérieur de plugins ; voir [Plugins](/tools/plugin#plugin-hooks).

Utilisations courantes :

- Enregistrer un snapshot de mémoire quand vous réinitialisez une session
- Maintenir une piste d'audit des commandes pour le dépannage ou la conformité
- Déclencher une automation de suivi quand une session démarre ou se termine
- Écrire des fichiers dans l'espace de travail de l'agent ou appeler des API externes quand des événements se déclenchent

Si vous pouvez écrire une petite fonction TypeScript, vous pouvez écrire un hook. Les hooks sont découverts automatiquement, et vous les activez ou les désactivez via la CLI.

## Aperçu

Le système de hooks vous permet de :

- Enregistrer le contexte de session en mémoire quand `/new` est émis
- Enregistrer toutes les commandes pour l'audit
- Déclencher des automations personnalisées sur les événements du cycle de vie de l'agent
- Étendre le comportement d'OpenClaw sans modifier le code principal

## Démarrage

### Hooks Intégrés

OpenClaw est livré avec quatre hooks intégrés qui sont automatiquement découverts :

- **💾 session-memory** : Enregistre le contexte de session dans votre espace de travail d'agent (par défaut `~/.openclaw/workspace/memory/`) quand vous émettez `/new`
- **📎 bootstrap-extra-files** : Injecte des fichiers de bootstrap d'espace de travail supplémentaires à partir de motifs glob/chemin configurés pendant `agent:bootstrap`
- **📝 command-logger** : Enregistre tous les événements de commande dans `~/.openclaw/logs/commands.log`
- **🚀 boot-md** : Exécute `BOOT.md` quand la gateway démarre (nécessite que les hooks internes soient activés)

Lister les hooks disponibles :

```bash
openclaw hooks list
```

Activer un hook :

```bash
openclaw hooks enable session-memory
```

Vérifier le statut du hook :

```bash
openclaw hooks check
```

Obtenir des informations détaillées :

```bash
openclaw hooks info session-memory
```

### Intégration

Pendant l'intégration (`openclaw onboard`), vous serez invité à activer les hooks recommandés. L'assistant découvre automatiquement les hooks éligibles et les présente pour sélection.

## Découverte des Hooks

Les hooks sont automatiquement découverts à partir de trois répertoires (dans l'ordre de précédence) :

1. **Hooks d'espace de travail** : `<workspace>/hooks/` (par agent, plus haute précédence)
2. **Hooks gérés** : `~/.openclaw/hooks/` (installés par l'utilisateur, partagés entre les espaces de travail)
3. **Hooks intégrés** : `<openclaw>/dist/hooks/bundled/` (livrés avec OpenClaw)

Les répertoires de hooks gérés peuvent être soit un **hook unique** soit un **pack de hooks** (répertoire de package).

Chaque hook est un répertoire contenant :

```
my-hook/
├── HOOK.md          # Métadonnées + documentation
└── handler.ts       # Implémentation du gestionnaire
```

## Packs de Hooks (npm/archives)

Les packs de hooks sont des packages npm standard qui exportent un ou plusieurs hooks via `openclaw.hooks` dans
`package.json`. Installez-les avec :

```bash
openclaw hooks install <path-or-spec>
```

Les spécifications npm sont réservées au registre (nom du package + version exacte optionnelle ou dist-tag).
Les spécifications Git/URL/fichier et les plages semver sont rejetées.

Les spécifications nues et `@latest` restent sur la piste stable. Si npm résout l'une ou l'autre
à une préversion, OpenClaw s'arrête et vous demande d'opter explicitement avec une
balise de préversion telle que `@beta`/`@rc` ou une version de préversion exacte.

Exemple `package.json` :

```json
{
  "name": "@acme/my-hooks",
  "version": "0.1.0",
  "openclaw": {
    "hooks": ["./hooks/my-hook", "./hooks/other-hook"]
  }
}
```

Chaque entrée pointe vers un répertoire de hook contenant `HOOK.md` et `handler.ts` (ou `index.ts`).
Les packs de hooks peuvent expédier des dépendances ; elles seront installées sous `~/.openclaw/hooks/<id>`.
Chaque entrée `openclaw.hooks` doit rester à l'intérieur du répertoire du package après la résolution du symlink ;
les entrées qui s'échappent sont rejetées.

Note de sécurité : `openclaw hooks install` installe les dépendances avec `npm install --ignore-scripts`
(pas de scripts de cycle de vie). Gardez les arbres de dépendances des packs de hooks « pur JS/TS » et évitez les packages qui dépendent
des builds `postinstall`.

## Structure des Hooks

### Format HOOK.md

Le fichier `HOOK.md` contient des métadonnées en préambule YAML plus la documentation Markdown :

```markdown
---
name: my-hook
description: "Description courte de ce que fait ce hook"
homepage: https://docs.openclaw.ai/automation/hooks#my-hook
metadata:
  { "openclaw": { "emoji": "🔗", "events": ["command:new"], "requires": { "bins": ["node"] } } }
---

# My Hook

La documentation détaillée va ici...

## Ce qu'il fait

- Écoute les commandes `/new`
- Effectue une action
- Enregistre le résultat

## Exigences

- Node.js doit être installé

## Configuration

Aucune configuration nécessaire.
```

### Champs de Métadonnées

L'objet `metadata.openclaw` supporte :

- **`emoji`** : Emoji d'affichage pour la CLI (par exemple, `"💾"`)
- **`events`** : Tableau des événements à écouter (par exemple, `["command:new", "command:reset"]`)
- **`export`** : Export nommé à utiliser (par défaut `"default"`)
- **`homepage`** : URL de documentation
- **`requires`** : Exigences optionnelles
  - **`bins`** : Binaires requis sur PATH (par exemple, `["git", "node"]`)
  - **`anyBins`** : Au moins un de ces binaires doit être présent
  - **`env`** : Variables d'environnement requises
  - **`config`** : Chemins de configuration requis (par exemple, `["workspace.dir"]`)
  - **`os`** : Plates-formes requises (par exemple, `["darwin", "linux"]`)
- **`always`** : Contourner les vérifications d'éligibilité (booléen)
- **`install`** : Méthodes d'installation (pour les hooks intégrés : `[{"id":"bundled","kind":"bundled"}]`)

### Implémentation du Gestionnaire

Le fichier `handler.ts` exporte une fonction `HookHandler` :

```typescript
const myHandler = async (event) => {
  // Déclencher uniquement sur la commande 'new'
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log(`[my-hook] Commande New déclenchée`);
  console.log(`  Session: ${event.sessionKey}`);
  console.log(`  Timestamp: ${event.timestamp.toISOString()}`);

  // Votre logique personnalisée ici

  // Optionnellement envoyer un message à l'utilisateur
  event.messages.push("✨ Mon hook a été exécuté!");
};

export default myHandler;
```

#### Contexte d'Événement

Chaque événement inclut :

```typescript
{
  type: 'command' | 'session' | 'agent' | 'gateway' | 'message',
  action: string,              // par exemple, 'new', 'reset', 'stop', 'received', 'sent'
  sessionKey: string,          // Identifiant de session
  timestamp: Date,             // Quand l'événement s'est produit
  messages: string[],          // Poussez les messages ici pour envoyer à l'utilisateur
  context: {
    // Événements de commande :
    sessionEntry?: SessionEntry,
    sessionId?: string,
    sessionFile?: string,
    commandSource?: string,    // par exemple, 'whatsapp', 'telegram'
    senderId?: string,
    workspaceDir?: string,
    bootstrapFiles?: WorkspaceBootstrapFile[],
    cfg?: OpenClawConfig,
    // Événements de message (voir la section Message Events pour les détails complets) :
    from?: string,             // message:received
    to?: string,               // message:sent
    content?: string,
    channelId?: string,
    success?: boolean,         // message:sent
  }
}
```

## Types d'Événements

### Événements de Commande

Déclenchés quand des commandes d'agent sont émises :

- **`command`** : Tous les événements de commande (écouteur général)
- **`command:new`** : Quand la commande `/new` est émise
- **`command:reset`** : Quand la commande `/reset` est émise
- **`command:stop`** : Quand la commande `/stop` est émise

### Événements de Session

- **`session:compact:before`** : Juste avant que la compaction résume l'historique
- **`session:compact:after`** : Après que la compaction se termine avec les métadonnées de résumé

Les payloads de hook internes émettent ceux-ci comme `type: "session"` avec `action: "compact:before"` / `action: "compact:after"` ; les écouteurs s'abonnent avec les clés combinées ci-dessus.
L'enregistrement du gestionnaire spécifique utilise le format de clé littéral `${type}:${action}`. Pour ces événements, enregistrez `session:compact:before` et `session:compact:after`.

### Événements d'Agent

- **`agent:bootstrap`** : Avant que les fichiers de bootstrap d'espace de travail soient injectés (les hooks peuvent muter `context.bootstrapFiles`)

### Événements de Gateway

Déclenchés quand la gateway démarre :

- **`gateway:startup`** : Après le démarrage des canaux et le chargement des hooks

### Événements de Message

Déclenchés quand des messages sont reçus ou envoyés :

- **`message`** : Tous les événements de message (écouteur général)
- **`message:received`** : Quand un message entrant est reçu de n'importe quel canal. Se déclenche tôt dans le traitement avant la compréhension des médias. Le contenu peut contenir des espaces réservés bruts comme `<media:audio>` pour les pièces jointes multimédias qui n'ont pas encore été traitées.
- **`message:transcribed`** : Quand un message a été entièrement traité, y compris la transcription audio et la compréhension des liens. À ce stade, `transcript` contient le texte de transcription complet pour les messages audio. Utilisez ce hook quand vous avez besoin d'accès au contenu audio transcrit.
- **`message:preprocessed`** : Se déclenche pour chaque message après que toute la compréhension des médias + liens soit terminée, donnant aux hooks l'accès au corps entièrement enrichi (transcriptions, descriptions d'images, résumés de liens) avant que l'agent ne le voie.
- **`message:sent`** : Quand un message sortant est envoyé avec succès

#### Contexte d'Événement de Message

Les événements de message incluent un contexte riche sur le message :

```typescript
// contexte message:received
{
  from: string,           // Identifiant de l'expéditeur (numéro de téléphone, ID utilisateur, etc.)
  content: string,        // Contenu du message
  timestamp?: number,     // Timestamp Unix quand reçu
  channelId: string,      // Canal (par exemple, "whatsapp", "telegram", "discord")
  accountId?: string,     // ID de compte du fournisseur pour les configurations multi-comptes
  conversationId?: string, // ID de chat/conversation
  messageId?: string,     // ID de message du fournisseur
  metadata?: {            // Données supplémentaires spécifiques au fournisseur
    to?: string,
    provider?: string,
    surface?: string,
    threadId?: string,
    senderId?: string,
    senderName?: string,
    senderUsername?: string,
    senderE164?: string,
  }
}

// contexte message:sent
{
  to: string,             // Identifiant du destinataire
  content: string,        // Contenu du message qui a été envoyé
  success: boolean,       // Si l'envoi a réussi
  error?: string,         // Message d'erreur si l'envoi a échoué
  channelId: string,      // Canal (par exemple, "whatsapp", "telegram", "discord")
  accountId?: string,     // ID de compte du fournisseur
  conversationId?: string, // ID de chat/conversation
  messageId?: string,     // ID de message retourné par le fournisseur
  isGroup?: boolean,      // Si ce message sortant appartient à un contexte de groupe/canal
  groupId?: string,       // Identifiant de groupe/canal pour la corrélation avec message:received
}

// contexte message:transcribed
{
  body?: string,          // Corps brut entrant avant enrichissement
  bodyForAgent?: string,  // Corps enrichi visible à l'agent
  transcript: string,     //
