---
read_when:
  - Modification de la gestion ou du stockage des sessions
summary: Règles de gestion des sessions de chat, clés et persistance
title: Gestion des sessions
x-i18n:
  generated_at: "2026-02-03T07:47:44Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 147c8d1a4b6b4864cb16ad942feba80181b6b0e29afa765e7958f8c2483746b5
  source_path: concepts/session.md
  workflow: 15
---

# Gestion des sessions

OpenClaw traite **une session de chat direct par agent** comme la session principale. Les chats directs se réduisent à `agent:<agentId>:<mainKey>` (par défaut `main`), tandis que les chats de groupe/canal obtiennent leurs propres clés. `session.mainKey` est respectée.

Utilisez `session.dmScope` pour contrôler **comment les messages privés** sont regroupés :

- `main` (par défaut) : tous les messages privés partagent la session principale pour maintenir la continuité.
- `per-peer` : isolés par ID d'expéditeur entre les canaux.
- `per-channel-peer` : isolés par canal + expéditeur (recommandé pour les boîtes de réception multi-utilisateurs).
- `per-account-channel-peer` : isolés par compte + canal + expéditeur (recommandé pour les boîtes de réception multi-comptes).
  Utilisez `session.identityLinks` pour mapper les ID de pairs avec préfixe de fournisseur à une identité canonique, de sorte que la même personne puisse partager une session de message privé entre les canaux lors de l'utilisation de `per-peer`, `per-channel-peer` ou `per-account-channel-peer`.

## Gateway est la source unique de vérité

Tous les états de session sont **possédés par Gateway** (l'OpenClaw "principal"). Les clients UI (application macOS, WebChat, etc.) doivent interroger Gateway pour les listes de sessions et les comptages de jetons, plutôt que de lire les fichiers locaux.

- En **mode distant**, le stockage de session qui vous intéresse se trouve sur l'hôte Gateway distant, pas sur votre Mac.
- Les comptages de jetons affichés dans l'UI proviennent des champs de stockage de Gateway (`inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`). Le client ne parse pas les enregistrements de conversation JSONL pour "corriger" les totaux.

## Emplacements de stockage d'état

- Sur l'**hôte Gateway** :
  - Fichiers de stockage : `~/.openclaw/agents/<agentId>/sessions/sessions.json` (par agent).
- Enregistrements de conversation : `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl` (les sessions de sujet Telegram utilisent `.../<SessionId>-topic-<threadId>.jsonl`).
- Le stockage est une carte `sessionKey -> { sessionId, updatedAt, ... }`. Il est sûr de supprimer des entrées ; elles seront recréées à la demande.
- Les entrées de groupe peuvent contenir `displayName`, `channel`, `subject`, `room` et `space` pour étiqueter les sessions dans l'UI.
- Les entrées de session contiennent des métadonnées `origin` (étiquette + conseils de routage) afin que l'UI puisse interpréter la source de la session.
- OpenClaw **ne** lit **pas** les anciens dossiers de sessions Pi/Tau.

## Élagage de session

Par défaut, OpenClaw élague les **anciens résultats d'outils** du contexte en mémoire avant un appel LLM.
Cela **ne** réécrit **pas** l'historique JSONL. Voir [/concepts/session-pruning](/concepts/session-pruning).

## Rafraîchissement de la mémoire avant compression

Lorsqu'une session approche de la compression automatique, OpenClaw peut exécuter un tour de **rafraîchissement de mémoire silencieux**, rappelant au modèle d'écrire des notes persistantes sur le disque. Cela ne s'exécute que si l'espace de travail est accessible en écriture. Voir [Mémoire](/concepts/memory) et [Compression](/concepts/compaction).

## Mappage des transports aux clés de session

- Les chats directs suivent `session.dmScope` (par défaut `main`).
  - `main` : `agent:<agentId>:<mainKey>` (continuité entre appareils/canaux).
    - Plusieurs numéros de téléphone et canaux peuvent mapper à la même clé principale d'agent ; ils agissent comme des canaux de transport entrant dans la même conversation.
  - `per-peer` : `agent:<agentId>:dm:<peerId>`.
  - `per-channel-peer` : `agent:<agentId>:<channel>:dm:<peerId>`.
  - `per-account-channel-peer` : `agent:<agentId>:<channel>:<accountId>:dm:<peerId>` (accountId par défaut `default`).
  - Si `session.identityLinks` correspond à un ID de pair avec préfixe de fournisseur (par ex. `telegram:123`), la clé canonique remplace `<peerId>`, de sorte que la même personne puisse partager une session entre les canaux.
- Les chats de groupe isolent l'état : `agent:<agentId>:<channel>:group:<id>` (les salons/canaux utilisent `agent:<agentId>:<channel>:channel:<id>`).
  - Les sujets de forum Telegram ajoutent `:topic:<threadId>` après l'ID de groupe pour l'isolation.
  - Les anciennes clés `group:<id>` sont toujours reconnues pour la migration.
- Le contexte entrant peut toujours utiliser `group:<id>` ; le canal est déduit du `Provider` et normalisé à la forme canonique `agent:<agentId>:<channel>:group:<id>`.
- Autres sources :
  - Tâches programmées : `cron:<job.id>`
  - Webhooks : `hook:<uuid>` (sauf si défini explicitement par le hook)
  - Exécutions de nœud : `node-<nodeId>`

## Cycle de vie

- Politique de réinitialisation : les sessions sont réutilisées jusqu'à expiration, l'expiration étant évaluée au prochain message entrant.
- Réinitialisation quotidienne : par défaut **4:00 du matin heure locale de l'hôte Gateway**. Une session expire lorsque sa dernière mise à jour est antérieure à l'heure de réinitialisation quotidienne la plus récente.
- Réinitialisation d'inactivité (optionnel) : `idleMinutes` ajoute une fenêtre d'inactivité glissante. Lorsque la réinitialisation quotidienne et d'inactivité sont configurées ensemble, **celui qui expire en premier** force une nouvelle session.
- Mode inactivité uniquement hérité : si vous définissez `session.idleMinutes` sans aucune configuration `session.reset`/`resetByType`, OpenClaw maintient le mode inactivité uniquement pour la compatibilité rétroactive.
- Surcharges par type (optionnel) : `resetByType` vous permet de surcharger la politique pour les sessions `dm`, `group` et `thread` (thread = threads Slack/Discord, sujets Telegram, threads Matrix fournis par le connecteur).
- Surcharges par canal (optionnel) : `resetByChannel` surcharge la politique de réinitialisation d'un canal (s'applique à tous les types de sessions de ce canal, prioritaire sur `reset`/`resetByType`).
- Déclencheurs de réinitialisation : `/new` ou `/reset` exacts (plus tout élément supplémentaire dans `resetTriggers`) lancent un nouvel ID de session et transmettent le reste du message. `/new <model>` accepte un alias de modèle, `provider/model` ou un nom de fournisseur (correspondance floue) pour définir le modèle de nouvelle session. Si vous envoyez `/new` ou `/reset` seul, OpenClaw exécute un tour court de "salutation" pour confirmer la réinitialisation.
- Réinitialisation manuelle : supprimez une clé spécifique du stockage ou supprimez l'enregistrement de conversation JSONL ; le message suivant les recréera.
- Les tâches programmées isolées génèrent toujours un nouvel `sessionId` à chaque exécution (pas de réutilisation d'inactivité).

## Politique d'envoi (optionnel)

Bloquez la livraison de types de sessions spécifiques sans lister les ID individuels.

```json5
{
  session: {
    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } },
        { action: "deny", match: { keyPrefix: "cron:" } },
      ],
      default: "allow",
    },
  },
}
```

Surcharges à l'exécution (propriétaire uniquement) :

- `/send on` → autoriser pour cette session
- `/send off` → refuser pour cette session
- `/send inherit` → effacer la surcharge et utiliser les règles de configuration
  Envoyez-les comme des messages indépendants pour qu'ils prennent effet.

## Configuration (exemple de renommage optionnel)

```json5
// ~/.openclaw/openclaw.json
{
  session: {
    scope: "per-sender", // keep group keys separate
    dmScope: "main", // DM continuity (set per-channel-peer/per-account-channel-peer for shared inboxes)
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      // Defaults: mode=daily, atHour=4 (gateway host local time).
      // If you also set idleMinutes, whichever expires first wins.
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      dm: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetByChannel: {
      discord: { mode: "idle", idleMinutes: 10080 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    mainKey: "main",
  },
}
```

## Inspections

- `openclaw status` — affiche le chemin de stockage et les sessions récentes.
- `openclaw sessions --json` — exporte chaque entrée (utilisez `--active <minutes>` pour filtrer).
- `openclaw gateway call sessions.list --params '{}'` — récupère les sessions depuis Gateway en cours d'exécution (utilisez `--url`/`--token` pour l'accès Gateway distant).
- Envoyez un message `/status` seul dans le chat pour voir si l'agent est accessible, combien de contexte la session utilise, les commutateurs de mode de réflexion/détail actuels, et quand vos identifiants WhatsApp Web ont été actualisés pour la dernière fois (utile pour découvrir les besoins de reliaison).
- Envoyez `/context list` ou `/context detail` pour voir le contenu de l'invite système et les fichiers d'espace de travail injectés (ainsi que les plus grands contributeurs de contexte).
- Envoyez un message `/stop` seul pour interrompre l'exécution actuelle, effacer les suites en attente pour cette session, et arrêter toute exécution de sous-agents générée à partir de celle-ci (la réponse contient le nombre arrêté).
- Envoyez un message `/compact` seul (avec instruction optionnelle) pour résumer l'ancien contexte et libérer de l'espace de fenêtre. Voir [/concepts/compaction](/concepts/compaction).
- Vous pouvez ouvrir directement les enregistrements de conversation JSONL pour voir les tours complets.

## Conseils

- Réservez la clé principale à la communication 1:1 ; laissez les groupes conserver leurs propres clés.
- Lors du nettoyage automatique, supprimez les clés individuelles plutôt que l'ensemble du stockage pour préserver le contexte ailleurs.

## Métadonnées d'origine de session

Chaque entrée de session enregistre sa source (au mieux) dans `origin` :

- `label` : étiquette lisible par l'homme (analysée à partir de l'étiquette de conversation + sujet de groupe/canal)
- `provider` : ID de canal normalisé (y compris les extensions)
- `from`/`to` : ID de routage d'enveloppe entrant d'origine
- `accountId` : ID de compte du fournisseur (en cas de multi-comptes)
- `threadId` : ID de thread/sujet lorsque supporté par le canal
  Les champs d'origine sont remplis pour les messages privés, les canaux et les groupes. Si un connecteur met à jour uniquement le routage de livraison (par ex., en gardant la session principale de message privé fraîche), il doit toujours fournir le contexte entrant afin que la session conserve ses métadonnées d'interprète. Les extensions peuvent le faire en envoyant `ConversationLabel`, `GroupSubject`, `GroupChannel`, `GroupSpace` et `SenderName` dans le contexte entrant et en appelant `recordSessionMetaFromInbound` (ou en transmettant le même contexte à `updateLastRoute`).
