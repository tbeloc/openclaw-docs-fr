# Gestion des sessions et compaction (Analyse approfondie)

Ce document explique comment OpenClaw gère les sessions de bout en bout :

- **Routage des sessions** (comment les messages entrants sont mappés à une `sessionKey`)
- **Magasin de sessions** (`sessions.json`) et ce qu'il suit
- **Persistance des transcriptions** (`*.jsonl`) et sa structure
- **Hygiène des transcriptions** (corrections spécifiques aux fournisseurs avant les exécutions)
- **Limites de contexte** (fenêtre de contexte vs jetons suivis)
- **Compaction** (compaction manuelle + automatique) et où accrocher le travail de pré-compaction
- **Maintenance silencieuse** (par exemple, écritures en mémoire qui ne doivent pas produire de sortie visible par l'utilisateur)

Si vous voulez d'abord un aperçu de plus haut niveau, commencez par :

- [/concepts/session](/concepts/session)
- [/concepts/compaction](/concepts/compaction)
- [/concepts/session-pruning](/concepts/session-pruning)
- [/reference/transcript-hygiene](/reference/transcript-hygiene)

---

## Source de vérité : la passerelle

OpenClaw est conçu autour d'un seul **processus Gateway** qui possède l'état de la session.

- Les interfaces utilisateur (application macOS, interface de contrôle web, TUI) doivent interroger la Gateway pour les listes de sessions et les comptages de jetons.
- En mode distant, les fichiers de session se trouvent sur l'hôte distant ; « vérifier vos fichiers Mac locaux » ne reflètera pas ce que la Gateway utilise.

---

## Deux couches de persistance

OpenClaw persiste les sessions en deux couches :

1. **Magasin de sessions (`sessions.json`)**
   - Carte clé/valeur : `sessionKey -> SessionEntry`
   - Petit, mutable, sûr à éditer (ou supprimer des entrées)
   - Suit les métadonnées de session (ID de session actuel, dernière activité, bascules, compteurs de jetons, etc.)

2. **Transcription (`<sessionId>.jsonl`)**
   - Transcription en ajout seul avec structure arborescente (les entrées ont `id` + `parentId`)
   - Stocke la conversation réelle + appels d'outils + résumés de compaction
   - Utilisé pour reconstruire le contexte du modèle pour les tours futurs

---

## Emplacements sur disque

Par agent, sur l'hôte Gateway :

- Magasin : `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Transcriptions : `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
  - Sessions de sujet Telegram : `.../<sessionId>-topic-<threadId>.jsonl`

OpenClaw résout ces chemins via `src/config/sessions.ts`.

---

## Maintenance du magasin et contrôles disque

La persistance des sessions a des contrôles de maintenance automatique (`session.maintenance`) pour `sessions.json` et les artefacts de transcription :

- `mode` : `warn` (par défaut) ou `enforce`
- `pruneAfter` : seuil d'âge des entrées obsolètes (par défaut `30d`)
- `maxEntries` : limite les entrées dans `sessions.json` (par défaut `500`)
- `rotateBytes` : rotation de `sessions.json` quand surdimensionné (par défaut `10mb`)
- `resetArchiveRetention` : rétention pour les archives de transcription `*.reset.<timestamp>` (par défaut : identique à `pruneAfter` ; `false` désactive le nettoyage)
- `maxDiskBytes` : budget optionnel pour le répertoire des sessions
- `highWaterBytes` : cible optionnelle après nettoyage (par défaut `80%` de `maxDiskBytes`)

Ordre d'application pour le nettoyage du budget disque (`mode: "enforce"`) :

1. Supprimez d'abord les artefacts de transcription archivés ou orphelins les plus anciens.
2. Si toujours au-dessus de la cible, évincer les entrées de session les plus anciennes et leurs fichiers de transcription.
3. Continuez jusqu'à ce que l'utilisation soit à ou en dessous de `highWaterBytes`.

En `mode: "warn"`, OpenClaw signale les évictions potentielles mais ne modifie pas le magasin/les fichiers.

Exécutez la maintenance à la demande :

```bash
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --enforce
```

---

## Sessions cron et journaux d'exécution

Les exécutions cron isolées créent également des entrées de session/transcriptions, et elles ont des contrôles de rétention dédiés :

- `cron.sessionRetention` (par défaut `24h`) nettoie les anciennes sessions d'exécution cron isolées du magasin de sessions (`false` désactive).
- `cron.runLog.maxBytes` + `cron.runLog.keepLines` nettoient les fichiers `~/.openclaw/cron/runs/<jobId>.jsonl` (par défaut : `2_000_000` octets et `2000` lignes).

---

## Clés de session (`sessionKey`)

Une `sessionKey` identifie _quel compartiment de conversation_ vous êtes (routage + isolation).

Modèles courants :

- Chat principal/direct (par agent) : `agent:<agentId>:<mainKey>` (par défaut `main`)
- Groupe : `agent:<agentId>:<channel>:group:<id>`
- Salle/canal (Discord/Slack) : `agent:<agentId>:<channel>:channel:<id>` ou `...:room:<id>`
- Cron : `cron:<job.id>`
- Webhook : `hook:<uuid>` (sauf si remplacé)

Les règles canoniques sont documentées à [/concepts/session](/concepts/session).

---

## IDs de session (`sessionId`)

Chaque `sessionKey` pointe vers un `sessionId` actuel (le fichier de transcription qui continue la conversation).

Règles empiriques :

- **Réinitialisation** (`/new`, `/reset`) crée un nouveau `sessionId` pour cette `sessionKey`.
- **Réinitialisation quotidienne** (par défaut 4:00 AM heure locale sur l'hôte gateway) crée un nouveau `sessionId` au prochain message après la limite de réinitialisation.
- **Expiration d'inactivité** (`session.reset.idleMinutes` ou ancien `session.idleMinutes`) crée un nouveau `sessionId` quand un message arrive après la fenêtre d'inactivité. Quand quotidien + inactivité sont tous deux configurés, celui qui expire en premier gagne.
- **Garde de bifurcation de parent de fil** (`session.parentForkMaxTokens`, par défaut `100000`) ignore la bifurcation de transcription parent quand la session parent est déjà trop grande ; le nouveau fil commence à zéro. Définissez `0` pour désactiver.

Détail d'implémentation : la décision se produit dans `initSessionState()` dans `src/auto-reply/reply/session.ts`.

---

## Schéma du magasin de sessions (`sessions.json`)

Le type de valeur du magasin est `SessionEntry` dans `src/config/sessions.ts`.

Champs clés (non exhaustif) :

- `sessionId` : ID de transcription actuel (le nom de fichier en est dérivé sauf si `sessionFile` est défini)
- `updatedAt` : horodatage de la dernière activité
- `sessionFile` : remplacement de chemin de transcription explicite optionnel
- `chatType` : `direct | group | room` (aide les interfaces utilisateur et la politique d'envoi)
- `provider`, `subject`, `room`, `space`, `displayName` : métadonnées pour l'étiquetage de groupe/canal
- Bascules :
  - `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`
  - `sendPolicy` (remplacement par session)
- Sélection du modèle :
  - `providerOverride`, `modelOverride`, `authProfileOverride`
- Compteurs de jetons (meilleur effort / dépendant du fournisseur) :
  - `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`
- `compactionCount` : nombre de fois où la compaction automatique s'est terminée pour cette clé de session
- `memoryFlushAt` : horodatage du dernier vidage de mémoire pré-compaction
- `memoryFlushCompactionCount` : nombre de compactions quand le dernier vidage s'est exécuté

Le magasin est sûr à éditer, mais la Gateway est l'autorité : elle peut réécrire ou réhydrater les entrées au fur et à mesure que les sessions s'exécutent.

---

## Structure de transcription (`*.jsonl`)

Les transcriptions sont gérées par `SessionManager` de `@mariozechner/pi-coding-agent`.

Le fichier est JSONL :

- Première ligne : en-tête de session (`type: "session"`, inclut `id`, `cwd`, `timestamp`, `parentSession` optionnel)
- Puis : entrées de session avec `id` + `parentId` (arborescence)

Types d'entrées notables :

- `message` : messages utilisateur/assistant/toolResult
- `custom_message` : messages injectés par extension qui _entrent_ dans le contexte du modèle (peuvent être cachés à l'interface utilisateur)
- `custom` : état d'extension qui n'_entre pas_ dans le contexte du modèle
- `compaction` : résumé de compaction persisté avec `firstKeptEntryId` et `tokensBefore`
- `branch_summary` : résumé persisté lors de la navigation dans une branche d'arborescence

OpenClaw intentionnellement ne « corrige pas » les transcriptions ; la Gateway utilise `SessionManager` pour les lire/écrire.

---

## Fenêtres de contexte vs jetons suivis

Deux concepts différents importent :

1. **Fenêtre de contexte du modèle** : limite stricte par modèle (jetons visibles au modèle)
2. **Compteurs du magasin de sessions** : statistiques roulantes écrites dans `sessions.json` (utilisées pour /status et les tableaux de bord)

Si vous accordez les limites :

- La fenêtre de contexte provient du catalogue de modèles (et peut être remplacée via la configuration).
- `contextTokens` dans le magasin est une valeur d'estimation/rapport d'exécution ; ne la traitez pas comme une garantie stricte.

Pour plus, voir [/token-use](/reference/token-use).

---

## Compaction : ce qu'elle est

La compaction résume la conversation plus ancienne en une entrée `compaction` persistée dans la transcription et garde les messages récents intacts.

Après compaction, les tours futurs voient :

- Le résumé de compaction
- Messages après `firstKeptEntryId`

La compaction est **persistante** (contrairement à l'élagage de session). Voir [/concepts/session-pruning](/concepts/session-pruning).

---

## Quand la compaction automatique se produit (exécution Pi)

Dans l'agent Pi intégré, la compaction automatique se déclenche dans deux cas :

1. **Récupération de débordement** : le modèle retourne une erreur de débordement de contexte → compacter → réessayer.
2. **Maintenance du seuil** : après un tour réussi, quand :

`contextTokens > contextWindow - reserveTokens`

Où :

- `contextWindow` est la fenêtre de contexte du modèle
- `reserveTokens` est l'espace de manœuvre réservé pour les invites + la sortie du modèle suivant

Ce sont les sémantiques d'exécution Pi (OpenClaw consomme les événements, mais Pi décide quand compacter).

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

OpenClaw applique également un plancher de sécurité pour les exécutions intégrées :

- Si `compaction.reserveTokens < reserveTokensFloor`, OpenClaw l'augmente.
- Le plancher par défaut est `20000` jetons.
- Définissez `agents.defaults.compaction.reserveTokensFloor: 0` pour désactiver le plancher.
- S'il est déjà plus élevé, OpenClaw le laisse tel quel.

Pourquoi : laisser suffisamment d'espace de manœuvre pour la « maintenance » multi-tour (comme les écritures en mémoire) avant que la compaction ne devienne inévitable.

Implémentation : `ensurePiCompactionReserveTokens()` dans `src/agents/pi-settings.ts`
(appelé depuis `src/agents/pi-embedded-runner.ts`).

---

## Surfaces visibles par l'utilisateur

Vous pouvez observer la compaction et l'état de la session via :

- `/status` (dans n'importe quelle session de chat)
- `openclaw status` (CLI)
- `openclaw sessions` / `sessions --json`
- Mode verbeux : `🧹 Auto-compaction complete` + nombre de compactions

---

## Maintenance silencieuse (`NO_REPLY`)

OpenClaw prend en charge les tours « silencieux » pour les tâches de fond où l'utilisateur ne doit pas voir la sortie intermédiaire.

Convention :

- L'assistant commence sa sortie par `NO_REPLY` pour indiquer « ne pas livrer de réponse à l'utilisateur ».
- OpenClaw supprime/masque cela dans la couche de livraison.

À partir de `2026.1.10`, OpenClaw supprime également le **streaming de brouillon/saisie** quand un bloc partiel commence par `NO_REPLY`, donc les opérations silencieuses ne fuient pas de sortie partielle à mi-tour.

---

## « Vidage de mémoire » pré-compaction (implémenté)

Objectif : avant que la compaction automatique ne se produise, exécuter un tour agentic silencieux qui écrit l'état durable sur disque (par exemple `memory/YYYY-MM-DD.md` dans l'espace de travail de l'agent) afin que la compaction ne puisse pas effacer le contexte critique.

OpenClaw utilise l'approche **vidage de seuil pré-compaction** :

1. Surveiller l'utilisation du contexte de session.
2. Quand elle franchit un « seuil logiciel » (en dessous du seuil de compaction de Pi), exécuter une directive silencieuse « écrire la mémoire maintenant » à l'agent.
3. Utiliser `NO_REPLY` pour que l'utilisateur ne voie rien.

Configuration (`agents.defaults.compaction.memoryFlush`) :

- `enabled` (par défaut : `true`)
- `softThresholdTokens` (par défaut : `4000`)
- `prompt` (message utilisateur pour le tour de vidage)
- `systemPrompt` (invite système supplémentaire ajoutée pour le tour de vidage)

Notes :

- L'invite/invite système par défaut incluent un indice `NO_REPLY` pour supprimer la livraison.
- Le vidage s'exécute une fois par cycle de compaction (suivi dans `sessions.json`).
- Le vidage s'exécute uniquement pour les sessions Pi intégrées (les backends CLI le sautent).
- Le vidage est ignoré quand l'espace de travail de session est en lecture seule (`workspaceAccess: "ro"` ou `"none"`).
- Voir [Memory](/concepts/memory) pour la disposition des fichiers d'espace de travail et les modèles d'écriture.

Pi expose également un crochet `session_before_compact` dans l'API d'extension, mais la logique de vidage d'OpenClaw se trouve côté Gateway aujourd'hui.

## Liste de contrôle de dépannage

- Clé de session incorrecte ? Commencez par [/concepts/session](/concepts/session) et confirmez la `sessionKey` dans `/status`.
- Décalage entre le magasin et la transcription ? Confirmez l'hôte Gateway et le chemin du magasin à partir de `openclaw status`.
- Spam de compaction ? Vérifiez :
  - fenêtre de contexte du modèle (trop petite)
  - paramètres de compaction (`reserveTokens` trop élevé pour la fenêtre du modèle peut causer une compaction plus précoce)
  - surcharge de résultats d'outils : activez/ajustez l'élagage de session
- Tours silencieux qui fuient ? Confirmez que la réponse commence par `NO_REPLY` (jeton exact) et que vous utilisez une version qui inclut le correctif de suppression du streaming.
