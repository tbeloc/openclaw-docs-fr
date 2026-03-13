---
read_when:
  - 你需要调试会话 ID、记录 JSONL 或 sessions.json 字段
  - 你正在更改自动压缩行为或添加"压缩前"内务处理
  - 你想实现记忆刷新或静默系统回合
summary: 深入了解：会话存储 + 记录、生命周期和（自动）压缩内部机制
title: 会话管理深入了解
x-i18n:
  generated_at: "2026-02-03T07:54:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bf3715770ba634363933f6038117b6a91af11c62f5191aaaf97e6bce099bc120
  source_path: reference/session-management-compaction.md
  workflow: 15
---

# Gestion des sessions et compaction (Approfondissement)

Ce document explique comment OpenClaw gère les sessions de bout en bout :

- **Routage des sessions** (comment les messages entrants sont mappés à `sessionKey`)
- **Stockage des sessions** (`sessions.json`) et ce qu'il suit
- **Persistance des journaux** (`*.jsonl`) et sa structure
- **Nettoyage des journaux** (corrections spécifiques au fournisseur avant exécution)
- **Limites de contexte** (fenêtre de contexte vs nombre de tokens suivis)
- **Compaction** (compaction manuelle + automatique) et où accrocher le travail pré-compaction
- **Maintenance silencieuse** (par exemple, les écritures de mémoire qui ne doivent pas produire de sortie visible par l'utilisateur)

Si vous souhaitez d'abord un aperçu de plus haut niveau, commencez par :

- [/concepts/session](/concepts/session)
- [/concepts/compaction](/concepts/compaction)
- [/concepts/session-pruning](/concepts/session-pruning)
- [/reference/transcript-hygiene](/reference/transcript-hygiene)

---

## Source de vérité : Passerelle Gateway

OpenClaw est conçu autour d'un seul **processus Gateway** qui possède l'état de la session.

- L'interface utilisateur (application macOS, interface de contrôle web, TUI) doit interroger la Gateway pour les listes de sessions et les comptages de tokens.
- En mode distant, les fichiers de session se trouvent sur l'hôte distant ; « vérifier vos fichiers Mac locaux » ne reflètera pas ce que la Gateway utilise.

---

## Deux couches de persistance

OpenClaw persiste les sessions dans deux couches :

1. **Stockage des sessions (`sessions.json`)**
   - Mappage clé/valeur : `sessionKey -> SessionEntry`
   - Petit, mutable, peut être édité ou supprimé en toute sécurité (ou supprimer des entrées)
   - Suit les métadonnées de session (ID de session actuel, dernière activité, commutateurs, compteurs de tokens, etc.)

2. **Journaux (`<sessionId>.jsonl`)**
   - Journal d'ajout uniquement avec structure arborescente (les entrées ont `id` + `parentId`)
   - Stocke la conversation réelle + appels d'outils + résumés de compaction
   - Utilisé pour reconstruire le contexte du modèle pour les tours suivants

---

## Emplacements sur le disque

Sur l'hôte Gateway, pour chaque agent :

- Stockage : `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Journaux : `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
  - Sessions de sujet Telegram : `.../<sessionId>-topic-<threadId>.jsonl`

OpenClaw analyse ces emplacements via `src/config/sessions.ts`.

---

## Clé de session (`sessionKey`)

`sessionKey` identifie *quel bucket de conversation* vous êtes dans (routage + isolation).

Modèles courants :

- Chat principal/direct (par agent) : `agent:<agentId>:<mainKey>` (par défaut `main`)
- Groupes : `agent:<agentId>:<channel>:group:<id>`
- Salons/canaux (Discord/Slack) : `agent:<agentId>:<channel>:channel:<id>` ou `...:room:<id>`
- Tâches planifiées : `cron:<job.id>`
- Webhook : `hook:<uuid>` (sauf s'il est remplacé)

Les règles canoniques sont documentées dans [/concepts/session](/concepts/session).

---

## ID de session (`sessionId`)

Chaque `sessionKey` pointe vers un `sessionId` actuel (le fichier journal pour continuer la conversation).

Règle générale :

- **Réinitialisation** (`/new`, `/reset`) crée un nouveau `sessionId` pour ce `sessionKey`.
- **Réinitialisation quotidienne** (par défaut 4h00 du matin heure locale de l'hôte Gateway) crée un nouveau `sessionId` au prochain message après la limite de réinitialisation.
- **Expiration d'inactivité** (`session.reset.idleMinutes` ou ancien `session.idleMinutes`) crée un nouveau `sessionId` quand un message arrive après la fenêtre d'inactivité. Quand à la fois quotidien et inactivité sont configurés, le premier à expirer gagne.

Détails d'implémentation : la décision se produit dans `initSessionState()` dans `src/auto-reply/reply/session.ts`.

---

## Schéma de stockage des sessions (`sessions.json`)

Le type de valeur stockée est `SessionEntry` dans `src/config/sessions.ts`.

Champs clés (incomplet) :

- `sessionId` : ID de journal actuel (le nom de fichier en est dérivé, sauf si `sessionFile` est défini)
- `updatedAt` : horodatage de la dernière activité
- `sessionFile` : remplacement de chemin de journal explicite optionnel
- `chatType` : `direct | group | room` (aide l'interface utilisateur et les stratégies d'envoi)
- `provider`, `subject`, `room`, `space`, `displayName` : métadonnées pour les étiquettes de groupe/canal
- Commutateurs :
  - `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`
  - `sendPolicy` (remplacement par session)
- Sélection du modèle :
  - `providerOverride`, `modelOverride`, `authProfileOverride`
- Compteurs de tokens (meilleur effort/dépendant du fournisseur) :
  - `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`
- `compactionCount` : nombre de fois que la compaction automatique a été complétée pour cette clé de session
- `memoryFlushAt` : horodatage du dernier vidage de mémoire pré-compaction
- `memoryFlushCompactionCount` : comptage de compaction au moment de la dernière exécution de vidage

Le stockage peut être édité en toute sécurité, mais la Gateway est l'autorité : elle peut réécrire ou réhydrater les entrées pendant l'exécution de la session.

---

## Structure du journal (`*.jsonl`)

Les journaux sont gérés par `SessionManager` de `@mariozechner/pi-coding-agent`.

Le fichier est au format JSONL :

- Première ligne : en-tête de session (`type: "session"`, incluant `id`, `cwd`, `timestamp`, `parentSession` optionnel)
- Puis : entrées de session avec `id` + `parentId` (structure arborescente)

Types d'entrées notables :

- `message` : messages utilisateur/assistant/résultat d'outil
- `custom_message` : message injecté par extension, *entre* dans le contexte du modèle (peut être caché de l'interface utilisateur)
- `custom` : état d'extension qui *n'entre pas* dans le contexte du modèle
- `compaction` : résumé de compaction persisté, avec `firstKeptEntryId` et `tokensBefore`
- `branch_summary` : résumé persisté lors de la navigation dans les branches d'arbre

OpenClaw **ne "corrige" intentionnellement pas** les journaux ; la Gateway utilise `SessionManager` pour les lire/écrire.

---

## Fenêtre de contexte vs tokens suivis

Deux concepts distincts sont importants :

1. **Fenêtre de contexte du modèle** : limite matérielle par modèle (tokens visibles par le modèle)
2. **Compteurs de session stockés** : statistiques roulantes écrites dans `sessions.json` (pour /status et le tableau de bord)

Si vous ajustez les limites :

- La fenêtre de contexte provient du répertoire des modèles (peut être remplacée par configuration).
- `contextTokens` dans le stockage est une valeur estimée/rapportée à l'exécution ; ne la traitez pas comme une garantie stricte.

Pour plus d'informations, voir [/token-use](/reference/token-use).

---

## Compaction : qu'est-ce que c'est

La compaction résume les conversations plus anciennes en une entrée `compaction` persistée dans le journal, et garde les messages récents intacts.

Après compaction, les tours futurs verront :

- Le résumé de compaction
- Les messages après `firstKeptEntryId`

La compaction est **persistée** (contrairement à l'élagage de session). Voir [/concepts/session-pruning](/concepts/session-pruning).

---

## Quand la compaction automatique se produit (Runtime Pi)

Dans les agents Pi intégrés, la compaction automatique se déclenche dans deux cas :

1. **Récupération de débordement** : le modèle retourne une erreur de débordement de contexte → compaction → nouvelle tentative.
2. **Maintenance de seuil** : après un tour réussi, quand :

`contextTokens > contextWindow - reserveTokens`

Où :

- `contextWindow` est la fenêtre de contexte du modèle
- `reserveTokens` est l'espace réservé pour l'invite + la sortie du modèle suivant

Ce sont les sémantiques du runtime Pi (OpenClaw consomme les événements, mais Pi décide quand compacter).

---

## Paramètres de compaction (`reserveTokens`, `keepRecentTokens`)

Les paramètres de compaction de Pi se trouvent dans les paramètres Pi :

```json5
{
  compaction: {
    enabled: true,
    reserveTokens: 16384,
    keepRecentTokens: 20000,
  },
}
```

OpenClaw applique également des limites de sécurité inférieure pour l'exécution intégrée :

- Si `compaction.reserveTokens < reserveTokensFloor`, OpenClaw l'augmente.
- Le plancher par défaut est `20000` tokens.
- Définissez `agents.defaults.compaction.reserveTokensFloor: 0` pour désactiver le plancher.
- S'il est déjà plus élevé, OpenClaw ne le change pas.

Raison : laisser suffisamment d'espace pour plusieurs tours de « maintenance » (comme les écritures de mémoire) avant que la compaction ne devienne inévitable.

Implémentation : `ensurePiCompactionReserveTokens()` dans `src/agents/pi-settings.ts` (appelé depuis `src/agents/pi-embedded-runner.ts`).

---

## Interface visible par l'utilisateur

Vous pouvez observer la compaction et l'état de la session via :

- `/status` (dans n'importe quelle session de chat)
- `openclaw status` (CLI)
- `openclaw sessions` / `sessions --json`
- Mode détaillé : `🧹 Auto-compaction complete` + comptage de compaction

---

## Maintenance silencieuse (`NO_REPLY`)

OpenClaw prend en charge les tours « silencieux » pour les tâches en arrière-plan où l'utilisateur ne devrait pas voir la sortie intermédiaire.

Convention :

- L'assistant commence sa sortie par `NO_REPLY`, ce qui signifie « ne pas envoyer de réponse à l'utilisateur ».
- OpenClaw supprime/inhibe ce contenu à la couche de livraison.

À partir de `2026.1.10`, quand des chunks partiels commencent par `NO_REPLY`, OpenClaw supprime également **la sortie de flux de brouillon/dactylographie**, donc les opérations silencieuses ne fuient pas de sortie partielle au milieu d'un tour.

---

## « Vidage de mémoire » pré-compaction (Implémenté)

Objectif : avant que la compaction automatique ne se produise, exécuter un tour d'agent silencieux qui écrit l'état persistant sur le disque (par exemple `memory/YYYY-MM-DD.md` dans l'espace de travail de l'agent), de sorte que la compaction n'efface pas le contexte critique.

OpenClaw utilise une approche de **vidage de seuil pré-compaction** :

1. Surveiller l'utilisation du contexte de session.
2. Quand il dépasse un « seuil logiciel » (en dessous du seuil de compaction de Pi), exécuter une instruction silencieuse « écrire la mémoire maintenant » vers l'agent.
3. Utiliser `NO_REPLY` pour que l'utilisateur ne voie rien.

Configuration (`agents.defaults.compaction.memoryFlush`) :

- `enabled` (par défaut : `true`)
- `softThresholdTokens` (par défaut : `4000`)
- `prompt` (message utilisateur pour le tour de vidage)
- `systemPrompt` (invite système supplémentaire à ajouter pour le tour de vidage)

Notes :

- L'invite/invite système par défaut contient l'invite `NO_REPLY` pour supprimer la livraison.
- Le vidage s'exécute une fois par cycle de compaction (suivi dans `sessions.json`).
- Le vidage s'exécute uniquement pour les sessions Pi intégrées (le backend CLI le saute).
- Quand l'espace de travail de session est en lecture seule (`workspaceAccess: "ro"` ou `"none"`), le vidage est ignoré.
- Voir [Mémoire](/concepts/memory) pour la disposition des fichiers d'espace de travail et les modes d'écriture.

Pi expose également un crochet `session_before_compact` dans l'API d'extension, mais la logique de vidage d'OpenClaw se trouve actuellement du côté Gateway.

---

## Liste de contrôle de dépannage

- Clé de session incorrecte ? Commencez par [/concepts/session](/concepts/session) et confirmez `sessionKey` dans `/status`.
- Stockage vs journal ne correspondent pas ? Confirmez l'hôte Gateway et le chemin de stockage depuis `openclaw status`.
- Compaction trop fréquente ? Vérifiez :
  - Fenêtre de contexte du modèle (trop petite)
  - Paramètres de compaction (`reserve
