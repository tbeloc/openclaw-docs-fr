---
summary: "Cron jobs + wakeups for the Gateway scheduler"
read_when:
  - Scheduling background jobs or wakeups
  - Wiring automation that should run with or alongside heartbeats
  - Deciding between heartbeat and cron for scheduled tasks
title: "Cron Jobs"
---

# Cron jobs (Gateway scheduler)

> **Cron vs Heartbeat?** Voir [Cron vs Heartbeat](/automation/cron-vs-heartbeat) pour des conseils sur quand utiliser chacun.

Cron est le planificateur intégré de la Gateway. Il persiste les jobs, réveille l'agent
au bon moment, et peut optionnellement renvoyer la sortie vers un chat.

Si vous voulez _"exécuter ceci chaque matin"_ ou _"vérifier l'agent dans 20 minutes"_,
cron est le mécanisme.

Dépannage: [/automation/troubleshooting](/automation/troubleshooting)

## TL;DR

- Cron s'exécute **à l'intérieur de la Gateway** (pas à l'intérieur du modèle).
- Les jobs persistent sous `~/.openclaw/cron/` donc les redémarrages ne perdent pas les planifications.
- Deux styles d'exécution :
  - **Session principale** : enqueue un événement système, puis exécuter au prochain heartbeat.
  - **Isolé** : exécuter un tour d'agent dédié dans `cron:<jobId>` ou une session personnalisée, avec livraison (annonce par défaut ou aucune).
  - **Session actuelle** : lier à la session où le cron est créé (`sessionTarget: "current"`).
  - **Session personnalisée** : exécuter dans une session nommée persistante (`sessionTarget: "session:custom-id"`).
- Les réveils sont de première classe : un job peut demander "réveiller maintenant" vs "prochain heartbeat".
- La publication webhook est par job via `delivery.mode = "webhook"` + `delivery.to = "<url>"`.
- Le fallback hérité reste pour les jobs stockés avec `notify: true` quand `cron.webhook` est défini, migrez ces jobs vers le mode de livraison webhook.
- Pour les mises à niveau, `openclaw doctor --fix` peut normaliser les champs du magasin cron hérité avant que le planificateur ne les touche.

## Démarrage rapide (actionnable)

Créez un rappel unique, vérifiez qu'il existe, et exécutez-le immédiatement :

```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

openclaw cron list
openclaw cron run <job-id>
openclaw cron runs --id <job-id>
```

Planifiez un job isolé récurrent avec livraison :

```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

## Équivalents d'appels d'outils (outil cron Gateway)

Pour les formes JSON canoniques et les exemples, voir [JSON schema for tool calls](/automation/cron-jobs#json-schema-for-tool-calls).

## Où les cron jobs sont stockés

Les cron jobs sont persistés sur l'hôte Gateway à `~/.openclaw/cron/jobs.json` par défaut.
La Gateway charge le fichier en mémoire et le réécrit lors des modifications, donc les éditions manuelles
ne sont sûres que lorsque la Gateway est arrêtée. Préférez `openclaw cron add/edit` ou l'API d'appel d'outil cron pour les modifications.

## Aperçu convivial pour les débutants

Pensez à un cron job comme : **quand** exécuter + **quoi** faire.

1. **Choisissez une planification**
   - Rappel unique → `schedule.kind = "at"` (CLI : `--at`)
   - Job répétitif → `schedule.kind = "every"` ou `schedule.kind = "cron"`
   - Si votre timestamp ISO omet un fuseau horaire, il est traité comme **UTC**.

2. **Choisissez où il s'exécute**
   - `sessionTarget: "main"` → exécuter pendant le prochain heartbeat avec le contexte principal.
   - `sessionTarget: "isolated"` → exécuter un tour d'agent dédié dans `cron:<jobId>`.
   - `sessionTarget: "current"` → lier à la session actuelle (résolu au moment de la création en `session:<sessionKey>`).
   - `sessionTarget: "session:custom-id"` → exécuter dans une session nommée persistante qui maintient le contexte entre les exécutions.

   Comportement par défaut (inchangé) :
   - Les charges utiles `systemEvent` par défaut à `main`
   - Les charges utiles `agentTurn` par défaut à `isolated`

   Pour utiliser la liaison de session actuelle, définissez explicitement `sessionTarget: "current"`.

3. **Choisissez la charge utile**
   - Session principale → `payload.kind = "systemEvent"`
   - Session isolée → `payload.kind = "agentTurn"`

Optionnel : les jobs uniques (`schedule.kind = "at"`) se suppriment après succès par défaut. Définissez
`deleteAfterRun: false` pour les conserver (ils se désactiveront après succès).

## Concepts

### Tâches

Une tâche cron est un enregistrement stocké avec :

- un **calendrier** (quand elle doit s'exécuter),
- une **charge utile** (ce qu'elle doit faire),
- un **mode de livraison** optionnel (`announce`, `webhook`, ou `none`).
- une **liaison d'agent** optionnelle (`agentId`) : exécuter la tâche sous un agent spécifique ; si elle est manquante ou inconnue, la passerelle revient à l'agent par défaut.

Les tâches sont identifiées par un `jobId` stable (utilisé par les API CLI/Gateway).
Dans les appels d'outils d'agent, `jobId` est canonique ; l'ancien `id` est accepté pour la compatibilité.
Les tâches ponctuelles se suppriment automatiquement après succès par défaut ; définissez `deleteAfterRun: false` pour les conserver.

### Calendriers

Cron supporte trois types de calendriers :

- `at` : timestamp ponctuel via `schedule.at` (ISO 8601).
- `every` : intervalle fixe (ms).
- `cron` : expression cron à 5 champs (ou 6 champs avec secondes) avec fuseau horaire IANA optionnel.

Les expressions cron utilisent `croner`. Si un fuseau horaire est omis, le fuseau horaire local de l'hôte Gateway est utilisé.

Pour réduire les pics de charge en haut de l'heure sur plusieurs passerelles, OpenClaw applique une fenêtre de décalage déterministe par tâche pouvant aller jusqu'à 5 minutes pour les expressions récurrentes en haut de l'heure (par exemple `0 * * * *`, `0 */2 * * *`). Les expressions à heure fixe comme `0 7 * * *` restent exactes.

Pour tout calendrier cron, vous pouvez définir une fenêtre de décalage explicite avec `schedule.staggerMs` (`0` conserve le timing exact). Raccourcis CLI :

- `--stagger 30s` (ou `1m`, `5m`) pour définir une fenêtre de décalage explicite.
- `--exact` pour forcer `staggerMs = 0`.

### Exécution principale vs isolée

#### Tâches de session principale (événements système)

Les tâches principales mettent en file d'attente un événement système et réveillent optionnellement le runner de battement cardiaque.
Elles doivent utiliser `payload.kind = "systemEvent"`.

- `wakeMode: "now"` (par défaut) : l'événement déclenche une exécution immédiate du battement cardiaque.
- `wakeMode: "next-heartbeat"` : l'événement attend le prochain battement cardiaque programmé.

C'est le meilleur choix quand vous voulez l'invite de battement cardiaque normale + contexte de session principale.
Voir [Heartbeat](/gateway/heartbeat).

#### Tâches isolées (sessions cron dédiées)

Les tâches isolées exécutent un tour d'agent dédié dans la session `cron:<jobId>` ou une session personnalisée.

Comportements clés :

- L'invite est préfixée avec `[cron:<jobId> <job name>]` pour la traçabilité.
- Chaque exécution démarre un **nouvel identifiant de session** (pas de report de conversation antérieure), sauf si vous utilisez une session personnalisée.
- Les sessions personnalisées (`session:xxx`) conservent le contexte entre les exécutions, permettant des flux de travail comme les points quotidiens qui s'appuient sur les résumés précédents.
- Comportement par défaut : si `delivery` est omis, les tâches isolées annoncent un résumé (`delivery.mode = "announce"`).
- `delivery.mode` choisit ce qui se passe :
  - `announce` : livrer un résumé au canal cible et publier un bref résumé dans la session principale.
  - `webhook` : POST la charge utile d'événement terminée à `delivery.to` quand l'événement terminé inclut un résumé.
  - `none` : interne uniquement (pas de livraison, pas de résumé de session principale).
- `wakeMode` contrôle quand le résumé de session principale est publié :
  - `now` : battement cardiaque immédiat.
  - `next-heartbeat` : attend le prochain battement cardiaque programmé.

Utilisez les tâches isolées pour les tâches bruyantes, fréquentes ou « tâches de fond » qui ne devraient pas spammer votre historique de chat principal.

### Formes de charge utile (ce qui s'exécute)

Deux types de charge utile sont supportés :

- `systemEvent` : session principale uniquement, acheminé via l'invite de battement cardiaque.
- `agentTurn` : session isolée uniquement, exécute un tour d'agent dédié.

Champs `agentTurn` courants :

- `message` : invite de texte requise.
- `model` / `thinking` : remplacements optionnels (voir ci-dessous).
- `timeoutSeconds` : remplacement de délai d'attente optionnel.
- `lightContext` : mode d'amorçage léger optionnel pour les tâches qui n'ont pas besoin d'injection de fichier de contexte d'amorçage d'espace de travail.

Configuration de livraison :

- `delivery.mode` : `none` | `announce` | `webhook`.
- `delivery.channel` : `last` ou un canal spécifique.
- `delivery.to` : cible spécifique au canal (announce) ou URL webhook (mode webhook).
- `delivery.bestEffort` : éviter d'échouer la tâche si la livraison d'annonce échoue.

La livraison d'annonce supprime les envois d'outils de messagerie pour l'exécution ; utilisez `delivery.channel`/`delivery.to` pour cibler le chat à la place. Quand `delivery.mode = "none"`, aucun résumé n'est publié dans la session principale.

Si `delivery` est omis pour les tâches isolées, OpenClaw utilise par défaut `announce`.

#### Flux de livraison d'annonce

Quand `delivery.mode = "announce"`, cron livre directement via les adaptateurs de canal sortant.
L'agent principal n'est pas lancé pour composer ou transférer le message.

Détails du comportement :

- Contenu : la livraison utilise les charges utiles sortantes de l'exécution isolée (texte/média) avec chunking normal et formatage de canal.
- Les réponses uniquement pour battement cardiaque (`HEARTBEAT_OK` sans contenu réel) ne sont pas livrées.
- Si l'exécution isolée a déjà envoyé un message à la même cible via l'outil de message, la livraison est ignorée pour éviter les doublons.
- Les cibles de livraison manquantes ou invalides échouent la tâche sauf si `delivery.bestEffort = true`.
- Un bref résumé est publié dans la session principale uniquement quand `delivery.mode = "announce"`.
- Le résumé de session principale respecte `wakeMode` : `now` déclenche un battement cardiaque immédiat et `next-heartbeat` attend le prochain battement cardiaque programmé.

#### Flux de livraison webhook

Quand `delivery.mode = "webhook"`, cron poste la charge utile d'événement terminée à `delivery.to` quand l'événement terminé inclut un résumé.

Détails du comportement :

- Le point de terminaison doit être une URL HTTP(S) valide.
- Aucune livraison de canal n'est tentée en mode webhook.
- Aucun résumé de session principale n'est publié en mode webhook.
- Si `cron.webhookToken` est défini, l'en-tête d'authentification est `Authorization: Bearer <cron.webhookToken>`.
- Secours déprécié : les tâches héritées stockées avec `notify: true` postent toujours à `cron.webhook` (si configuré), avec un avertissement pour que vous puissiez migrer vers `delivery.mode = "webhook"`.

### Remplacements de modèle et de réflexion

Les tâches isolées (`agentTurn`) peuvent remplacer le modèle et le niveau de réflexion :

- `model` : chaîne Fournisseur/modèle (par exemple, `anthropic/claude-sonnet-4-20250514`) ou alias (par exemple, `opus`)
- `thinking` : niveau de réflexion (`off`, `minimal`, `low`, `medium`, `high`, `xhigh` ; modèles GPT-5.2 + Codex uniquement)

Remarque : vous pouvez également définir `model` sur les tâches de session principale, mais cela change le modèle de session principale partagée. Nous recommandons les remplacements de modèle uniquement pour les tâches isolées pour éviter les changements de contexte inattendus.

Priorité de résolution :

1. Remplacement de charge utile de tâche (le plus élevé)
2. Valeurs par défaut spécifiques au hook (par exemple, `hooks.gmail.model`)
3. Valeur par défaut de configuration d'agent

### Contexte d'amorçage léger

Les tâches isolées (`agentTurn`) peuvent définir `lightContext: true` pour s'exécuter avec un contexte d'amorçage léger.

- Utilisez ceci pour les tâches programmées qui n'ont pas besoin d'injection de fichier de contexte d'amorçage d'espace de travail.
- En pratique, le runtime intégré s'exécute avec `bootstrapContextMode: "lightweight"`, ce qui garde le contexte d'amorçage cron vide intentionnellement.
- Équivalents CLI : `openclaw cron add --light-context ...` et `openclaw cron edit --light-context`.

### Livraison (canal + cible)

Les tâches isolées peuvent livrer la sortie à un canal via la configuration `delivery` de niveau supérieur :

- `delivery.mode` : `announce` (livraison de canal), `webhook` (HTTP POST), ou `none`.
- `delivery.channel` : `whatsapp` / `telegram` / `discord` / `slack` / `mattermost` (plugin) / `signal` / `imessage` / `last`.
- `delivery.to` : cible de destinataire spécifique au canal.

La livraison `announce` n'est valide que pour les tâches isolées (`sessionTarget: "isolated"`).
La livraison `webhook` est valide pour les tâches principales et isolées.

Si `delivery.channel` ou `delivery.to` est omis, cron peut revenir à la « dernière route » de la session principale (le dernier endroit où l'agent a répondu).

Rappels de format de cible :

- Les cibles Slack/Discord/Mattermost (plugin) doivent utiliser des préfixes explicites (par exemple `channel:<id>`, `user:<id>`) pour éviter l'ambiguïté.
  Les IDs Mattermost nus de 26 caractères sont résolus **en priorité utilisateur** (DM si l'utilisateur existe, canal sinon) — utilisez `user:<id>` ou `channel:<id>` pour un routage déterministe.
- Les sujets Telegram doivent utiliser la forme `:topic:` (voir ci-dessous).

#### Cibles de livraison Telegram (sujets / fils de discussion de forum)

Telegram supporte les sujets de forum via `message_thread_id`. Pour la livraison cron, vous pouvez encoder le sujet/fil dans le champ `to` :

- `-1001234567890` (ID de chat uniquement)
- `-1001234567890:topic:123` (préféré : marqueur de sujet explicite)
- `-1001234567890:123` (raccourci : suffixe numérique)

Les cibles préfixées comme `telegram:...` / `telegram:group:...` sont également acceptées :

- `telegram:group:-1001234567890:topic:123`

## Schéma JSON pour les appels d'outils

Utilisez ces formes lors de l'appel direct des outils Gateway `cron.*` (appels d'outils d'agent ou RPC).
Les drapeaux CLI acceptent les durées humaines comme `20m`, mais les appels d'outils doivent utiliser une chaîne ISO 8601 pour `schedule.at` et des millisecondes pour `schedule.everyMs`.

### Paramètres cron.add

Tâche ponctuelle, session principale (événement système) :

```json
{
  "name": "Reminder",
  "schedule": { "kind": "at", "at": "2026-02-01T16:00:00Z" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": { "kind": "systemEvent", "text": "Reminder text" },
  "deleteAfterRun": true
}
```

Tâche récurrente, isolée avec livraison :

```json
{
  "name": "Morning brief",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "America/Los_Angeles" },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize overnight updates.",
    "lightContext": true
  },
  "delivery": {
    "mode": "announce",
    "channel": "slack",
    "to": "channel:C1234567890",
    "bestEffort": true
  }
}
```

Tâche récurrente liée à la session actuelle (auto-résolue à la création) :

```json
{
  "name": "Daily standup",
  "schedule": { "kind": "cron", "expr": "0 9 * * *" },
  "sessionTarget": "current",
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize yesterday's progress."
  }
}
```

Tâche récurrente dans une session persistante personnalisée :

```json
{
  "name": "Project monitor",
  "schedule": { "kind": "every", "everyMs": 300000 },
  "sessionTarget": "session:project-alpha-monitor",
  "payload": {
    "kind": "agentTurn",
    "message": "Check project status and update the running log."
  }
}
```

Remarques :

- `schedule.kind` : `at` (`at`), `every` (`everyMs`), ou `cron` (`expr`, `tz` optionnel).
- `schedule.at` accepte ISO 8601 (fuseau horaire optionnel ; traité comme UTC quand omis).
- `everyMs` est en millisecondes.
- `sessionTarget` : `"main"`, `"isolated"`, `"current"`, ou `"session:<custom-id>"`.
- `"current"` est résolu à `"session:<sessionKey>"` au moment de la création.
- Les sessions personnalisées (`session:xxx`) maintiennent un contexte persistant entre les exécutions.
- Champs optionnels : `agentId`, `description`, `enabled`, `deleteAfterRun` (par défaut true pour `at`), `delivery`.
- `wakeMode` par défaut à `"now"` quand omis.

### Paramètres cron.update

```json
{
  "jobId": "job-123",
  "patch": {
    "enabled": false,
    "schedule": { "kind": "every", "everyMs": 3600000 }
  }
}
```

Remarques :

- `jobId` est canonique ; `id` est accepté pour la compatibilité.
- Utilisez `agentId: null` dans le patch pour effacer une liaison d'agent.

### Paramètres cron.run et cron.remove

```json
{ "jobId": "job-123", "mode": "force" }
```

```json
{ "jobId": "job-123" }
```

## Stockage et historique

- Magasin de tâches : `~/.openclaw/cron/jobs.json` (JSON géré par Gateway).
- Historique d'exécution : `~/.openclaw/cron/runs/<jobId>.jsonl` (JSONL, auto-élagué par taille et nombre de lignes).
- Les sessions d'exécution cron isolées dans `sessions.json` sont élaguées par `cron.sessionRetention` (par défaut `24h` ; définissez `false` pour désactiver).
- Chemin de magasin de remplacement : `cron.store` dans la configuration.

## Politique de retry

Quand un job échoue, OpenClaw classe les erreurs comme **transitoires** (réessayables) ou **permanentes** (désactiver immédiatement).

### Erreurs transitoires (réessayées)

- Limite de débit (429, trop de requêtes, ressource épuisée)
- Surcharge du fournisseur (par exemple Anthropic `529 overloaded_error`, résumés de secours de surcharge)
- Erreurs réseau (timeout, ECONNRESET, fetch échoué, socket)
- Erreurs serveur (5xx)
- Erreurs liées à Cloudflare

### Erreurs permanentes (pas de retry)

- Échecs d'authentification (clé API invalide, non autorisé)
- Erreurs de configuration ou de validation
- Autres erreurs non-transitoires

### Comportement par défaut (sans config)

**Jobs ponctuels (`schedule.kind: "at"`):**

- En cas d'erreur transitoire : réessayer jusqu'à 3 fois avec backoff exponentiel (30s → 1m → 5m).
- En cas d'erreur permanente : désactiver immédiatement.
- En cas de succès ou de saut : désactiver (ou supprimer si `deleteAfterRun: true`).

**Jobs récurrents (`cron` / `every`):**

- En cas d'erreur : appliquer un backoff exponentiel (30s → 1m → 5m → 15m → 60m) avant la prochaine exécution programmée.
- Le job reste activé ; le backoff se réinitialise après la prochaine exécution réussie.

Configurez `cron.retry` pour remplacer ces valeurs par défaut (voir [Configuration](/automation/cron-jobs#configuration)).

## Configuration

```json5
{
  cron: {
    enabled: true, // default true
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1, // default 1
    // Optional: override retry policy for one-shot jobs
    retry: {
      maxAttempts: 3,
      backoffMs: [60000, 120000, 300000],
      retryOn: ["rate_limit", "overloaded", "network", "server_error"],
    },
    webhook: "https://example.invalid/legacy", // deprecated fallback for stored notify:true jobs
    webhookToken: "replace-with-dedicated-webhook-token", // optional bearer token for webhook mode
    sessionRetention: "24h", // duration string or false
    runLog: {
      maxBytes: "2mb", // default 2_000_000 bytes
      keepLines: 2000, // default 2000
    },
  },
}
```

Comportement de l'élagage du journal d'exécution :

- `cron.runLog.maxBytes` : taille maximale du fichier journal d'exécution avant élagage.
- `cron.runLog.keepLines` : lors de l'élagage, conserver uniquement les N dernières lignes.
- Les deux s'appliquent aux fichiers `cron/runs/<jobId>.jsonl`.

Comportement du webhook :

- Préféré : définir `delivery.mode: "webhook"` avec `delivery.to: "https://..."` par job.
- Les URL de webhook doivent être des URL `http://` ou `https://` valides.
- Lors de la publication, la charge utile est le JSON de l'événement cron terminé.
- Si `cron.webhookToken` est défini, l'en-tête d'authentification est `Authorization: Bearer <cron.webhookToken>`.
- Si `cron.webhookToken` n'est pas défini, aucun en-tête `Authorization` n'est envoyé.
- Secours déprécié : les jobs hérités stockés avec `notify: true` utilisent toujours `cron.webhook` s'il est présent.

Désactiver cron entièrement :

- `cron.enabled: false` (config)
- `OPENCLAW_SKIP_CRON=1` (env)

## Maintenance

Cron dispose de deux chemins de maintenance intégrés : la rétention de session d'exécution isolée et l'élagage du journal d'exécution.

### Valeurs par défaut

- `cron.sessionRetention` : `24h` (définir `false` pour désactiver l'élagage de session d'exécution)
- `cron.runLog.maxBytes` : `2_000_000` bytes
- `cron.runLog.keepLines` : `2000`

### Fonctionnement

- Les exécutions isolées créent des entrées de session (`...:cron:<jobId>:run:<uuid>`) et des fichiers de transcription.
- Le reaper supprime les entrées de session d'exécution expirées plus anciennes que `cron.sessionRetention`.
- Pour les sessions d'exécution supprimées qui ne sont plus référencées par le magasin de sessions, OpenClaw archive les fichiers de transcription et purge les anciennes archives supprimées sur la même fenêtre de rétention.
- Après chaque ajout d'exécution, `cron/runs/<jobId>.jsonl` est vérifié en taille :
  - si la taille du fichier dépasse `runLog.maxBytes`, il est réduit aux `runLog.keepLines` lignes les plus récentes.

### Avertissement de performance pour les planificateurs à haut volume

Les configurations cron haute fréquence peuvent générer des empreintes de session d'exécution et de journal d'exécution importantes. La maintenance est intégrée, mais des limites lâches peuvent toujours créer du travail d'E/S et de nettoyage évitable.

À surveiller :

- fenêtres `cron.sessionRetention` longues avec de nombreuses exécutions isolées
- `cron.runLog.keepLines` élevé combiné avec `runLog.maxBytes` important
- de nombreux jobs récurrents bruyants écrivant dans le même `cron/runs/<jobId>.jsonl`

À faire :

- garder `cron.sessionRetention` aussi court que vos besoins de débogage/audit le permettent
- garder les journaux d'exécution limités avec `runLog.maxBytes` et `runLog.keepLines` modérés
- déplacer les jobs de fond bruyants en mode isolé avec des règles de livraison qui évitent les bavardages inutiles
- examiner la croissance périodiquement avec `openclaw cron runs` et ajuster la rétention avant que les journaux ne deviennent volumineux

### Exemples de personnalisation

Conserver les sessions d'exécution pendant une semaine et autoriser des journaux d'exécution plus volumineux :

```json5
{
  cron: {
    sessionRetention: "7d",
    runLog: {
      maxBytes: "10mb",
      keepLines: 5000,
    },
  },
}
```

Désactiver l'élagage de session d'exécution isolée mais conserver l'élagage du journal d'exécution :

```json5
{
  cron: {
    sessionRetention: false,
    runLog: {
      maxBytes: "5mb",
      keepLines: 3000,
    },
  },
}
```

Optimiser pour une utilisation cron à haut volume (exemple) :

```json5
{
  cron: {
    sessionRetention: "12h",
    runLog: {
      maxBytes: "3mb",
      keepLines: 1500,
    },
  },
}
```

## Démarrage rapide CLI

Rappel ponctuel (ISO UTC, suppression automatique après succès) :

```bash
openclaw cron add \
  --name "Send reminder" \
  --at "2026-01-12T18:00:00Z" \
  --session main \
  --system-event "Reminder: submit expense report." \
  --wake now \
  --delete-after-run
```

Rappel ponctuel (session principale, réveil immédiat) :

```bash
openclaw cron add \
  --name "Calendar check" \
  --at "20m" \
  --session main \
  --system-event "Next heartbeat: check calendar." \
  --wake now
```

Job isolé récurrent (annoncer sur WhatsApp) :

```bash
openclaw cron add \
  --name "Morning status" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize inbox + calendar for today." \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

Job cron récurrent avec décalage explicite de 30 secondes :

```bash
openclaw cron add \
  --name "Minute watcher" \
  --cron "0 * * * * *" \
  --tz "UTC" \
  --stagger 30s \
  --session isolated \
  --message "Run minute watcher checks." \
  --announce
```

Job isolé récurrent (livrer à un sujet Telegram) :

```bash
openclaw cron add \
  --name "Nightly summary (topic)" \
  --cron "0 22 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize today; send to the nightly topic." \
  --announce \
  --channel telegram \
  --to "-1001234567890:topic:123"
```

Job isolé avec modèle et remplacement de réflexion :

```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 1" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Weekly deep analysis of project progress." \
  --model "opus" \
  --thinking high \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

Sélection d'agent (configurations multi-agents) :

```bash
# Pin a job to agent "ops" (falls back to default if that agent is missing)
openclaw cron add --name "Ops sweep" --cron "0 6 * * *" --session isolated --message "Check ops queue" --agent ops

# Switch or clear the agent on an existing job
openclaw cron edit <jobId> --agent ops
openclaw cron edit <jobId> --clear-agent
```

Exécution manuelle (force est la valeur par défaut, utiliser `--due` pour exécuter uniquement si dû) :

```bash
openclaw cron run <jobId>
openclaw cron run <jobId> --due
```

`cron.run` reconnaît maintenant une fois que l'exécution manuelle est mise en file d'attente, pas après la fin du job. Les réponses de file d'attente réussies ressemblent à `{ ok: true, enqueued: true, runId }`. Si le job s'exécute déjà ou si `--due` ne trouve rien de dû, la réponse reste `{ ok: true, ran: false, reason }`. Utilisez `openclaw cron runs --id <jobId>` ou la méthode de passerelle `cron.runs` pour inspecter l'entrée terminée éventuelle.

Modifier un job existant (champs de patch) :

```bash
openclaw cron edit <jobId> \
  --message "Updated prompt" \
  --model "opus" \
  --thinking low
```

Forcer un job cron existant à s'exécuter exactement selon le calendrier (pas de décalage) :

```bash
openclaw cron edit <jobId> --exact
```

Historique d'exécution :

```bash
openclaw cron runs --id <jobId> --limit 50
```

Événement système immédiat sans créer de job :

```bash
openclaw system event --mode now --text "Next heartbeat: check battery."
```

## Surface de l'API Gateway

- `cron.list`, `cron.status`, `cron.add`, `cron.update`, `cron.remove`
- `cron.run` (force ou due), `cron.runs`
  Pour les événements système immédiats sans job, utilisez [`openclaw system event`](/cli/system).

## Dépannage

### "Rien ne s'exécute"

- Vérifier que cron est activé : `cron.enabled` et `OPENCLAW_SKIP_CRON`.
- Vérifier que la Gateway s'exécute en continu (cron s'exécute à l'intérieur du processus Gateway).
- Pour les calendriers `cron` : confirmer le fuseau horaire (`--tz`) par rapport au fuseau horaire de l'hôte.

### Un job récurrent continue de retarder après des échecs

- OpenClaw applique un backoff de retry exponentiel pour les jobs récurrents après des erreurs consécutives :
  30s, 1m, 5m, 15m, puis 60m entre les tentatives.
- Le backoff se réinitialise automatiquement après la prochaine exécution réussie.
- Les jobs ponctuels (`at`) réessaient les erreurs transitoires (limite de débit, surcharge, réseau, erreur_serveur) jusqu'à 3 fois avec backoff ; les erreurs permanentes désactivent immédiatement. Voir [Politique de retry](/automation/cron-jobs#retry-policy).

### Telegram livre au mauvais endroit

- Pour les sujets de forum, utilisez `-100…:topic:<id>` pour que ce soit explicite et sans ambiguïté.
- Si vous voyez des préfixes `telegram:...` dans les journaux ou les cibles "dernière route" stockées, c'est normal ;
  la livraison cron les accepte et analyse toujours correctement les ID de sujet.

### Retries d'annonce de sous-agent

- Quand une exécution de sous-agent se termine, la gateway annonce le résultat à la session du demandeur.
- Si le flux d'annonce retourne `false` (par exemple, la session du demandeur est occupée), la gateway réessaye jusqu'à 3 fois avec suivi via `announceRetryCount`.
- Les annonces plus anciennes que 5 minutes après `endedAt` sont forcément expirées pour éviter que les entrées obsolètes ne boucles indéfiniment.
- Si vous voyez des livraisons d'annonce répétées dans les journaux, vérifiez le registre de sous-agent pour les entrées avec des valeurs `announceRetryCount` élevées.
