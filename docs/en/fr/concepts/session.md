---
summary: "Règles de gestion de session, clés et persistance pour les chats"
read_when:
  - Modifying session handling or storage
title: "Gestion des sessions"
---

# Gestion des sessions

OpenClaw traite **une session de chat direct par agent** comme primaire. Les chats directs se réduisent à `agent:<agentId>:<mainKey>` (par défaut `main`), tandis que les chats de groupe/canal obtiennent leurs propres clés. `session.mainKey` est respecté.

Utilisez `session.dmScope` pour contrôler comment les **messages directs** sont regroupés :

- `main` (par défaut) : tous les DM partagent la session principale pour la continuité.
- `per-peer` : isoler par ID d'expéditeur sur les canaux.
- `per-channel-peer` : isoler par canal + expéditeur (recommandé pour les boîtes de réception multi-utilisateurs).
- `per-account-channel-peer` : isoler par compte + canal + expéditeur (recommandé pour les boîtes de réception multi-comptes).
  Utilisez `session.identityLinks` pour mapper les ID de pairs préfixés par le fournisseur à une identité canonique afin que la même personne partage une session DM sur les canaux lors de l'utilisation de `per-peer`, `per-channel-peer` ou `per-account-channel-peer`.

## Mode DM sécurisé (recommandé pour les configurations multi-utilisateurs)

> **Avertissement de sécurité :** Si votre agent peut recevoir des DM de **plusieurs personnes**, vous devriez fortement envisager d'activer le mode DM sécurisé. Sans cela, tous les utilisateurs partagent le même contexte de conversation, ce qui peut divulguer des informations privées entre les utilisateurs.

**Exemple du problème avec les paramètres par défaut :**

- Alice (`<SENDER_A>`) envoie un message à votre agent sur un sujet privé (par exemple, un rendez-vous médical)
- Bob (`<SENDER_B>`) envoie un message à votre agent en demandant « De quoi parlions-nous ? »
- Parce que les deux DM partagent la même session, le modèle peut répondre à Bob en utilisant le contexte antérieur d'Alice.

**La solution :** Définissez `dmScope` pour isoler les sessions par utilisateur :

```json5
// ~/.openclaw/openclaw.json
{
  session: {
    // Mode DM sécurisé : isoler le contexte DM par canal + expéditeur.
    dmScope: "per-channel-peer",
  },
}
```

**Quand activer ceci :**

- Vous avez des approbations d'appairage pour plus d'un expéditeur
- Vous utilisez une liste blanche DM avec plusieurs entrées
- Vous définissez `dmPolicy: "open"`
- Plusieurs numéros de téléphone ou comptes peuvent envoyer des messages à votre agent

Notes :

- La valeur par défaut est `dmScope: "main"` pour la continuité (tous les DM partagent la session principale). C'est correct pour les configurations à un seul utilisateur.
- L'intégration CLI locale écrit `session.dmScope: "per-channel-peer"` par défaut lorsqu'il n'est pas défini (les valeurs explicites existantes sont conservées).
- Pour les boîtes de réception multi-comptes sur le même canal, préférez `per-account-channel-peer`.
- Si la même personne vous contacte sur plusieurs canaux, utilisez `session.identityLinks` pour réduire ses sessions DM en une seule identité canonique.
- Vous pouvez vérifier vos paramètres DM avec `openclaw security audit` (voir [security](/cli/security)).

## La passerelle est la source de vérité

Tout l'état de la session est **détenu par la passerelle** (le « maître » OpenClaw). Les clients UI (application macOS, WebChat, etc.) doivent interroger la passerelle pour les listes de sessions et les comptages de jetons au lieu de lire les fichiers locaux.

- En **mode distant**, le magasin de sessions qui vous intéresse se trouve sur l'hôte de passerelle distant, pas sur votre Mac.
- Les comptages de jetons affichés dans les interfaces utilisateur proviennent des champs du magasin de la passerelle (`inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`). Les clients n'analysent pas les transcriptions JSONL pour « corriger » les totaux.

## Où l'état réside

- Sur l'**hôte de passerelle** :
  - Fichier de magasin : `~/.openclaw/agents/<agentId>/sessions/sessions.json` (par agent).
- Transcriptions : `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl` (les sessions de sujet Telegram utilisent `.../<SessionId>-topic-<threadId>.jsonl`).
- Le magasin est une carte `sessionKey -> { sessionId, updatedAt, ... }`. Supprimer des entrées est sûr ; elles sont recréées à la demande.
- Les entrées de groupe peuvent inclure `displayName`, `channel`, `subject`, `room` et `space` pour étiqueter les sessions dans les interfaces utilisateur.
- Les entrées de session incluent les métadonnées `origin` (étiquette + indices de routage) afin que les interfaces utilisateur puissent expliquer d'où provient une session.
- OpenClaw ne lit **pas** les dossiers de session Pi/Tau hérités.

## Maintenance

OpenClaw applique la maintenance du magasin de sessions pour maintenir `sessions.json` et les artefacts de transcription limités dans le temps.

### Valeurs par défaut

- `session.maintenance.mode`: `warn`
- `session.maintenance.pruneAfter`: `30d`
- `session.maintenance.maxEntries`: `500`
- `session.maintenance.rotateBytes`: `10mb`
- `session.maintenance.resetArchiveRetention`: par défaut à `pruneAfter` (`30d`)
- `session.maintenance.maxDiskBytes`: non défini (désactivé)
- `session.maintenance.highWaterBytes`: par défaut à `80%` de `maxDiskBytes` lorsque la budgétisation est activée

### Comment ça marche

La maintenance s'exécute lors des écritures du magasin de sessions, et vous pouvez la déclencher à la demande avec `openclaw sessions cleanup`.

- `mode: "warn"`: rapporte ce qui serait supprimé mais ne modifie pas les entrées/transcriptions.
- `mode: "enforce"`: applique le nettoyage dans cet ordre :
  1. élaguer les entrées obsolètes plus anciennes que `pruneAfter`
  2. plafonner le nombre d'entrées à `maxEntries` (les plus anciennes en premier)
  3. archiver les fichiers de transcription pour les entrées supprimées qui ne sont plus référencées
  4. purger les anciennes archives `*.deleted.<timestamp>` et `*.reset.<timestamp>` selon la politique de rétention
  5. faire pivoter `sessions.json` lorsqu'il dépasse `rotateBytes`
  6. si `maxDiskBytes` est défini, appliquer le budget disque vers `highWaterBytes` (les artefacts les plus anciens en premier, puis les sessions les plus anciennes)

### Mise en garde de performance pour les grands magasins

Les grands magasins de sessions sont courants dans les configurations à haut volume. Le travail de maintenance est un travail sur le chemin d'écriture, donc les très grands magasins peuvent augmenter la latence d'écriture.

Ce qui augmente le coût le plus :

- des valeurs très élevées de `session.maintenance.maxEntries`
- des fenêtres `pruneAfter` longues qui conservent les entrées obsolètes
- de nombreux artefacts de transcription/archive dans `~/.openclaw/agents/<agentId>/sessions/`
- l'activation des budgets disque (`maxDiskBytes`) sans limites raisonnables d'élagage/plafonnement

Que faire :

- utiliser `mode: "enforce"` en production afin que la croissance soit automatiquement limitée
- définir à la fois les limites de temps et de nombre (`pruneAfter` + `maxEntries`), pas seulement l'une
- définir `maxDiskBytes` + `highWaterBytes` pour les limites supérieures strictes dans les grands déploiements
- garder `highWaterBytes` significativement en dessous de `maxDiskBytes` (la valeur par défaut est 80%)
- exécuter `openclaw sessions cleanup --dry-run --json` après les modifications de configuration pour vérifier l'impact projeté avant d'appliquer
- pour les sessions actives fréquentes, passer `--active-key` lors de l'exécution du nettoyage manuel

### Exemples de personnalisation

Utiliser une politique d'application conservatrice :

```json5
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "45d",
      maxEntries: 800,
      rotateBytes: "20mb",
      resetArchiveRetention: "14d",
    },
  },
}
```

Activer un budget disque strict pour le répertoire des sessions :

```json5
{
  session: {
    maintenance: {
      mode: "enforce",
      maxDiskBytes: "1gb",
      highWaterBytes: "800mb",
    },
  },
}
```

Affiner pour les installations plus grandes (exemple) :

```json5
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "14d",
      maxEntries: 2000,
      rotateBytes: "25mb",
      maxDiskBytes: "2gb",
      highWaterBytes: "1.6gb",
    },
  },
}
```

Aperçu ou forcer la maintenance à partir de la CLI :

```bash
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --enforce
```

## Élagage des sessions

OpenClaw supprime les **anciens résultats d'outils** du contexte en mémoire juste avant les appels LLM par défaut.
Cela ne réécrit **pas** l'historique JSONL. Voir [/concepts/session-pruning](/concepts/session-pruning).

## Vidage de mémoire avant compaction

Lorsqu'une session approche de la compaction automatique, OpenClaw peut exécuter un **vidage de mémoire silencieux**
qui rappelle au modèle d'écrire des notes durables sur le disque. Cela ne s'exécute que lorsque
l'espace de travail est accessible en écriture. Voir [Memory](/concepts/memory) et
[Compaction](/concepts/compaction).

## Mappage des transports → clés de session

- Les chats directs suivent `session.dmScope` (par défaut `main`).
  - `main`: `agent:<agentId>:<mainKey>` (continuité sur les appareils/canaux).
    - Plusieurs numéros de téléphone et canaux peuvent mapper à la même clé principale d'agent ; ils agissent comme des transports dans une conversation.
  - `per-peer`: `agent:<agentId>:direct:<peerId>`.
  - `per-channel-peer`: `agent:<agentId>:<channel>:direct:<peerId>`.
  - `per-account-channel-peer`: `agent:<agentId>:<channel>:<accountId>:direct:<peerId>` (accountId par défaut à `default`).
  - Si `session.identityLinks` correspond à un ID de pair préfixé par le fournisseur (par exemple `telegram:123`), la clé canonique remplace `<peerId>` afin que la même personne partage une session sur les canaux.
- Les chats de groupe isolent l'état : `agent:<agentId>:<channel>:group:<id>` (les salons/canaux utilisent `agent:<agentId>:<channel>:channel:<id>`).
  - Les sujets du forum Telegram ajoutent `:topic:<threadId>` à l'ID du groupe pour l'isolation.
  - Les clés héritées `group:<id>` sont toujours reconnues pour la migration.
- Les contextes entrants peuvent toujours utiliser `group:<id>` ; le canal est déduit de `Provider` et normalisé à la forme canonique `agent:<agentId>:<channel>:group:<id>`.
- Autres sources :
  - Tâches Cron : `cron:<job.id>` (isolé) ou `session:<custom-id>` personnalisé (persistant)
  - Webhooks : `hook:<uuid>` (sauf s'il est explicitement défini par le webhook)
  - Exécutions de nœud : `node-<nodeId>`

## Cycle de vie

- Politique de réinitialisation : les sessions sont réutilisées jusqu'à leur expiration, et l'expiration est évaluée au prochain message entrant.
- Réinitialisation quotidienne : par défaut **4:00 AM heure locale sur l'hôte de passerelle**. Une session est obsolète une fois que sa dernière mise à jour est antérieure à l'heure de réinitialisation quotidienne la plus récente.
- Réinitialisation d'inactivité (optionnel) : `idleMinutes` ajoute une fenêtre d'inactivité glissante. Lorsque les réinitialisations quotidiennes et d'inactivité sont configurées, **celle qui expire en premier** force une nouvelle session.
- Inactivité héritée uniquement : si vous définissez `session.idleMinutes` sans aucune configuration `session.reset`/`resetByType`, OpenClaw reste en mode inactivité uniquement pour la compatibilité rétroactive.
- Remplacements par type (optionnel) : `resetByType` vous permet de remplacer la politique pour les sessions `direct`, `group` et `thread` (thread = threads Slack/Discord, sujets Telegram, threads Matrix lorsqu'ils sont fournis par le connecteur).
- Remplacements par canal (optionnel) : `resetByChannel` remplace la politique de réinitialisation pour un canal (s'applique à tous les types de session pour ce canal et a priorité sur `reset`/`resetByType`).
- Déclencheurs de réinitialisation : `/new` ou `/reset` exacts (plus tous les extras dans `resetTriggers`) démarrent un nouvel ID de session et transmettent le reste du message. `/new <model>` accepte un alias de modèle, `provider/model` ou un nom de fournisseur (correspondance floue) pour définir le nouveau modèle de session. Si `/new` ou `/reset` est envoyé seul, OpenClaw exécute un court tour de salutation « hello » pour confirmer la réinitialisation.
- Réinitialisation manuelle : supprimer des clés spécifiques du magasin ou supprimer la transcription JSONL ; le message suivant les recrée.
- Les tâches cron isolées créent toujours un nouvel `sessionId` par exécution (pas de réutilisation d'inactivité).

## Politique d'envoi (optionnel)

Bloquer la livraison pour des types de session spécifiques sans lister les ID individuels.

```json5
{
  session: {
    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } },
        { action: "deny", match: { keyPrefix: "cron:" } },
        // Correspond à la clé de session brute (y compris le préfixe `agent:<id>:`).
        { action: "deny", match: { rawKeyPrefix: "agent:main:discord:" } },
      ],
      default: "allow",
    },
  },
}
```

Remplacement à l'exécution (propriétaire uniquement) :

- `/send on` → autoriser pour cette session
- `/send off` → refuser pour cette session
- `/send inherit` → effacer le remplacement et utiliser les règles de configuration
  Envoyez-les en tant que messages autonomes afin qu'ils s'enregistrent.

## Configuration (renommage optionnel)

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
      direct: { mode: "idle", idleMinutes: 240 },
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

## Inspection

- `openclaw status` — affiche le chemin du magasin et les sessions récentes.
- `openclaw sessions --json` — exporte chaque entrée (filtrer avec `--active <minutes>`).
- `openclaw gateway call sessions.list --params '{}'` — récupère les sessions depuis la passerelle en cours d'exécution (utilisez `--url`/`--token` pour l'accès à une passerelle distante).
- Envoyez `/status` comme message autonome dans le chat pour voir si l'agent est accessible, combien de contexte de session est utilisé, les bascules de réflexion/rapide/verbeux actuelles, et quand vos identifiants WhatsApp Web ont été actualisés pour la dernière fois (aide à détecter les besoins de reliaison).
- Envoyez `/context list` ou `/context detail` pour voir ce qui se trouve dans l'invite système et les fichiers d'espace de travail injectés (et les plus grands contributeurs de contexte).
- Envoyez `/stop` (ou des phrases d'abandon autonomes comme `stop`, `stop action`, `stop run`, `stop openclaw`) pour abandonner l'exécution actuelle, effacer les suites en file d'attente pour cette session, et arrêter toute exécution de sous-agent générée à partir de celle-ci (la réponse inclut le nombre arrêté).
- Envoyez `/compact` (instructions optionnelles) comme message autonome pour résumer le contexte plus ancien et libérer de l'espace de fenêtre. Voir [/concepts/compaction](/concepts/compaction).
- Les transcriptions JSONL peuvent être ouvertes directement pour examiner les tours complets.

## Conseils

- Gardez la clé primaire dédiée au trafic 1:1 ; laissez les groupes conserver leurs propres clés.
- Lors de l'automatisation du nettoyage, supprimez les clés individuelles au lieu de tout le magasin pour préserver le contexte ailleurs.

## Métadonnées d'origine de session

Chaque entrée de session enregistre d'où elle provient (au mieux) dans `origin` :

- `label` : étiquette humaine (résolue à partir de l'étiquette de conversation + sujet du groupe/canal)
- `provider` : identifiant de canal normalisé (y compris les extensions)
- `from`/`to` : identifiants de routage bruts de l'enveloppe entrante
- `accountId` : identifiant de compte du fournisseur (en cas de multi-compte)
- `threadId` : identifiant de fil/sujet lorsque le canal le supporte
  Les champs d'origine sont remplis pour les messages directs, les canaux et les groupes. Si un
  connecteur met à jour uniquement le routage de livraison (par exemple, pour garder une session principale DM
  fraîche), il doit toujours fournir le contexte entrant afin que la session conserve ses
  métadonnées explicatives. Les extensions peuvent le faire en envoyant `ConversationLabel`,
  `GroupSubject`, `GroupChannel`, `GroupSpace`, et `SenderName` dans le contexte entrant et en appelant
  `recordSessionMetaFromInbound` (ou en passant le même contexte à `updateLastRoute`).
