---
read_when:
  - Planifier des tâches de fond ou réveiller
  - Configurer des automatisations qui doivent s'exécuter avec ou en parallèle du heartbeat
  - Choisir entre cron et heartbeat
summary: Tâches planifiées et réveils du planificateur Gateway
title: Tâches planifiées
x-i18n:
  generated_at: "2026-02-01T19:37:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d43268b0029f1b13d0825ddcc9c06a354987ea17ce02f3b5428a9c68bf936676
  source_path: automation/cron-jobs.md
  workflow: 14
---

# Tâches planifiées (Planificateur Gateway)

> **Tâches planifiées ou heartbeat ?** Consultez [Comparaison cron vs heartbeat](/automation/cron-vs-heartbeat) pour savoir quand utiliser chaque approche.

Les tâches planifiées sont le planificateur intégré de Gateway. Elles persistent les tâches, réveillent les agents au moment opportun, et peuvent optionnellement renvoyer la sortie au chat.

Si vous voulez _"exécuter chaque matin"_ ou _"rappeler l'agent dans 20 minutes"_, les tâches planifiées sont le mécanisme approprié.

## Aperçu rapide

- Les tâches planifiées s'exécutent **à l'intérieur de Gateway** (et non dans le modèle).
- Les tâches sont persistées dans `~/.openclaw/cron/`, donc les redémarrages ne perdent pas les planifications.
- Deux modes d'exécution :
  - **Session principale** : met en file d'attente un événement système, puis s'exécute au prochain heartbeat.
  - **Isolé** : exécute un tour d'agent dédié dans `cron:<jobId>`, peut livrer un résumé (announce par défaut) ou ne rien livrer.
- Le réveil est une fonctionnalité de première classe : les tâches peuvent demander "réveiller maintenant" ou "au prochain heartbeat".

## Démarrage rapide (opérationnel)

Créez un rappel unique, vérifiez son existence, puis exécutez-le immédiatement :

```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

openclaw cron list
openclaw cron run <job-id> --force
openclaw cron runs --id <job-id>
```

Planifiez une tâche isolée périodique avec livraison :

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

## Équivalent d'appel d'outil (Outil de tâches planifiées Gateway)

Pour les structures JSON canoniques et les exemples, consultez [Schéma JSON pour les appels d'outil](/automation/cron-jobs#json-schema-for-tool-calls).

## Où sont stockées les tâches planifiées

Les tâches planifiées sont persistées par défaut dans `~/.openclaw/cron/jobs.json` sur l'hôte Gateway. Gateway charge le fichier en mémoire et le réécrit lors des modifications, donc l'édition manuelle n'est sûre que lorsque Gateway est arrêté. Préférez utiliser `openclaw cron add/edit` ou l'API d'appel d'outil de tâches planifiées pour les modifications.

## Aperçu convivial pour les débutants

Pensez aux tâches planifiées comme : **quand** exécuter + **quoi faire**.

1. **Choisissez un calendrier de planification**
   - Rappel unique → `schedule.kind = "at"` (CLI : `--at`)
   - Tâche répétée → `schedule.kind = "every"` ou `schedule.kind = "cron"`
   - Si votre horodatage ISO omet le fuseau horaire, il sera traité comme **UTC**.

2. **Choisissez où exécuter**
   - `sessionTarget: "main"` → Exécute avec le contexte de session principale au prochain heartbeat.
   - `sessionTarget: "isolated"` → Exécute un tour d'agent dédié dans `cron:<jobId>`.

3. **Choisissez la charge utile**
   - Session principale → `payload.kind = "systemEvent"`
   - Session isolée → `payload.kind = "agentTurn"`

Optionnel : les tâches uniques (`schedule.kind = "at"`) sont supprimées par défaut après une exécution réussie. Définissez `deleteAfterRun: false` pour les conserver (désactivées après succès).

## Concepts

### Tâche

Une tâche planifiée est un enregistrement stocké contenant :

- Un **calendrier de planification** (quand exécuter),
- Une **charge utile** (quoi faire),
- Une **livraison** optionnelle (où envoyer la sortie).
- Un **lien d'agent** optionnel (`agentId`) : exécute la tâche sous un agent spécifié ; s'il est absent ou inconnu, Gateway revient à l'agent par défaut.

Les tâches sont identifiées par un `jobId` stable (utilisé dans CLI/API Gateway).
Dans les appels d'outil d'agent, `jobId` est le champ canonique ; l'ancien `id` reste compatible.
Les tâches uniques sont supprimées par défaut après une exécution réussie ; définissez `deleteAfterRun: false` pour les conserver.

### Calendrier de planification

Les tâches planifiées supportent trois types de planification :

- `at` : horodatage unique (chaîne ISO 8601).
- `every` : intervalle fixe (millisecondes).
- `cron` : expression cron à 5 champs, fuseau horaire IANA optionnel.

Les expressions cron utilisent `croner`. Si le fuseau horaire est omis, le fuseau horaire local de l'hôte Gateway est utilisé.

### Exécution en session principale vs isolée

#### Tâches de session principale (événements système)

Les tâches de session principale mettent en file d'attente un événement système et peuvent optionnellement réveiller le runner heartbeat. Elles doivent utiliser `payload.kind = "systemEvent"`.

- `wakeMode: "next-heartbeat"` (par défaut) : l'événement attend le prochain heartbeat planifié.
- `wakeMode: "now"` : l'événement déclenche un heartbeat immédiat.

C'est le meilleur choix quand vous avez besoin d'une invite heartbeat normale + contexte de session principale. Voir [Heartbeat](/gateway/heartbeat).

#### Tâches isolées (session cron dédiée)

Les tâches isolées exécutent un tour d'agent dédié dans la session `cron:<jobId>`.

Comportements clés :

- L'invite est préfixée par `[cron:<jobId> <nom-tâche>]` pour la traçabilité.
- Chaque exécution démarre un **nouvel ID de session** (n'hérite pas de la conversation précédente).
- Si `delivery` n'est pas spécifié, les tâches isolées livrent par défaut un résumé en mode "announce".
- `delivery.mode` peut être `announce` (livrer le résumé) ou `none` (exécution interne).

Pour les tâches bruyantes, fréquentes ou "tâches de fond", utilisez les tâches isolées pour éviter de polluer votre historique de chat principal.

### Structure de charge utile (contenu à exécuter)

Deux types de charge utile sont supportés :

- `systemEvent` : session principale uniquement, routée via l'invite heartbeat.
- `agentTurn` : session isolée uniquement, exécute un tour d'agent dédié.

Champs `agentTurn` courants :

- `message` : invite textuelle obligatoire.
- `model` / `thinking` : surcharges optionnelles (voir ci-dessous).
- `timeoutSeconds` : surcharge de délai d'attente optionnelle.

### Surcharges de modèle et de réflexion

Les tâches isolées (`agentTurn`) peuvent surcharger le modèle et le niveau de réflexion :

- `model` : chaîne fournisseur/modèle (par ex. `anthropic/claude-sonnet-4-20250514`) ou alias (par ex. `opus`)
- `thinking` : niveau de réflexion (`off`, `minimal`, `low`, `medium`, `high`, `xhigh` ; GPT-5.2 + modèles Codex uniquement)

Remarque : vous pouvez également définir `model` sur les tâches de session principale, mais cela change le modèle de session principale partagée. Nous recommandons d'utiliser les surcharges de modèle uniquement pour les tâches isolées pour éviter les changements de contexte accidentels.

Ordre de résolution des priorités :

1. Surcharges de charge utile de tâche (priorité la plus élevée)
2. Valeurs par défaut spécifiques au hook (par ex. `hooks.gmail.model`)
3. Valeurs par défaut de configuration d'agent

### Livraison (canal + cible)

Les tâches isolées peuvent livrer la sortie via la configuration `delivery` de niveau supérieur :

- `delivery.mode` : `announce` (livrer le résumé) ou `none`
- `delivery.channel` : `whatsapp` / `telegram` / `discord` / `slack` / `mattermost` (plugin) / `signal` / `imessage` / `last`
- `delivery.to` : cible de réception spécifique au canal
- `delivery.bestEffort` : évite l'échec de la tâche en cas d'échec de livraison

Lorsque la livraison announce est activée, ce tour supprime l'envoi d'outil de message ; utilisez `delivery.channel`/`delivery.to` pour spécifier la cible.

Si `delivery.channel` ou `delivery.to` est omis, la tâche planifiée revient au "dernier routage" de la session principale (où l'agent a répondu en dernier).

Rappel de format de cible :

- Les cibles Slack/Discord/Mattermost (plugin) doivent utiliser des préfixes explicites (par ex. `channel:<id>`, `user:<id>`) pour éviter l'ambiguïté.
- Les sujets Telegram doivent utiliser le format `:topic:` (voir ci-dessous).

#### Cibles de livraison Telegram (sujets/fils de forum)

Telegram supporte les sujets de forum via `message_thread_id`. Pour la livraison de tâches planifiées, vous pouvez encoder le sujet/fil dans le champ `to` :

- `-1001234567890` (ID de chat uniquement)
- `-1001234567890:topic:123` (recommandé : marqueur de sujet explicite)
- `-1001234567890:123` (raccourci : suffixe numérique)

Les cibles avec préfixe comme `telegram:...` / `telegram:group:...` sont également acceptées :

- `telegram:group:-1001234567890:topic:123`

## Schéma JSON pour les appels d'outil

Utilisez ces structures lors d'appels directs aux outils Gateway `cron.*` (appels d'outil d'agent ou RPC). Les drapeaux CLI acceptent les formats de temps lisibles par l'homme comme `20m`, mais les appels d'outil doivent utiliser les chaînes ISO 8601 pour `schedule.at` et les millisecondes pour `schedule.everyMs`.

### Paramètres cron.add

Tâche de session principale unique (événement système) :

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

Tâche isolée périodique avec livraison :

```json
{
  "name": "Morning brief",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "America/Los_Angeles" },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize overnight updates."
  },
  "delivery": {
    "mode": "announce",
    "channel": "slack",
    "to": "channel:C1234567890",
    "bestEffort": true
  }
}
```

Explications :

- `schedule.kind` : `at` (`at`), `every` (`everyMs`) ou `cron` (`expr`, `tz` optionnel).
- `schedule.at` accepte ISO 8601 (fuseau horaire optionnel ; omis = UTC).
- `everyMs` en millisecondes.
- `sessionTarget` doit être `"main"` ou `"isolated"` et doit correspondre à `payload.kind`.
- Champs optionnels : `agentId`, `description`, `enabled`, `deleteAfterRun`, `delivery`.
- `wakeMode` par défaut à `"next-heartbeat"` s'il est omis.

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

Explications :

- `jobId` est le champ canonique ; `id` reste compatible.
- Utilisez `agentId: null` dans le patch pour effacer la liaison d'agent.

### Paramètres cron.run et cron.remove

```json
{ "jobId": "job-123", "mode": "force" }
```

```json
{ "jobId": "job-123" }
```

## Stockage et historique

- Stockage des tâches : `~/.openclaw/cron/jobs.json` (JSON géré par Gateway).
- Historique des exécutions : `~/.openclaw/cron/runs/<jobId>.jsonl` (JSONL, nettoyage automatique).
- Chemin de stockage de remplacement : `cron.store` dans la configuration.

## Configuration

```json5
{
  cron: {
    enabled: true, // true par défaut
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentR
