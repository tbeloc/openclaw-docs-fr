---
summary: "Tâches cron + réveils pour le planificateur Gateway"
read_when:
  - Scheduling background jobs or wakeups
  - Wiring automation that should run with or alongside heartbeats
  - Deciding between heartbeat and cron for scheduled tasks
title: "Cron Jobs"
---

# Tâches cron (planificateur Gateway)

> **Cron vs Heartbeat ?** Consultez [Cron vs Heartbeat](/automation/cron-vs-heartbeat) pour des conseils sur quand utiliser chacun.

Cron est le planificateur intégré du Gateway. Il persiste les tâches, réveille l'agent
au bon moment et peut optionnellement livrer la sortie à un chat.

Si vous voulez _« exécuter ceci chaque matin »_ ou _« poke l'agent dans 20 minutes »_,
cron est le mécanisme.

Dépannage : [/automation/troubleshooting](/automation/troubleshooting)

## TL;DR

- Cron s'exécute **à l'intérieur du Gateway** (pas à l'intérieur du modèle).
- Les tâches persistent sous `~/.openclaw/cron/` donc les redémarrages ne perdent pas les planifications.
- Deux styles d'exécution :
  - **Session principale** : enqueue un événement système, puis exécuter au prochain heartbeat.
  - **Isolée** : exécuter un tour d'agent dédié dans `cron:<jobId>`, avec livraison (annonce par défaut ou aucune).
- Les réveils sont de première classe : une tâche peut demander « réveiller maintenant » vs « prochain heartbeat ».
- La publication webhook est par tâche via `delivery.mode = "webhook"` + `delivery.to = "<url>"`.
- Le fallback hérité reste pour les tâches stockées avec `notify: true` quand `cron.webhook` est défini, migrez ces tâches vers le mode de livraison webhook.
- Pour les mises à niveau, `openclaw doctor --fix` peut normaliser les champs du magasin cron hérité avant que le planificateur ne les touche.

## Démarrage rapide (actionnable)

Créez un rappel unique, vérifiez qu'il existe et exécutez-le immédiatement :

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

Planifiez une tâche isolée récurrente avec livraison :

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

Pour les formes JSON canoniques et les exemples, consultez [Schéma JSON pour les appels d'outils](/automation/cron-jobs#json-schema-for-tool-calls).

## Où les tâches cron sont stockées

Les tâches cron sont persistées sur l'hôte Gateway à `~/.openclaw/cron/jobs.json` par défaut.
Le Gateway charge le fichier en mémoire et le réécrit lors des modifications, donc les éditions manuelles
ne sont sûres que lorsque le Gateway est arrêté. Préférez `openclaw cron add/edit` ou l'API d'appel d'outil cron pour les modifications.

## Aperçu convivial pour les débutants

Pensez à une tâche cron comme : **quand** l'exécuter + **quoi** faire.

1. **Choisissez un calendrier**
   - Rappel unique → `schedule.kind = "at"` (CLI : `--at`)
   - Tâche répétée → `schedule.kind = "every"` ou `schedule.kind = "cron"`
   - Si votre timestamp ISO omet un fuseau horaire, il est traité comme **UTC**.

2. **Choisissez où il s'exécute**
   - `sessionTarget: "main"` → exécuter pendant le prochain heartbeat avec le contexte principal.
   - `sessionTarget: "isolated"` → exécuter un tour d'agent dédié dans `cron:<jobId>`.

3. **Choisissez la charge utile**
   - Session principale → `payload.kind = "systemEvent"`
   - Session isolée → `payload.kind = "agentTurn"`

Optionnel : les tâches uniques (`schedule.kind = "at"`) se suppriment après succès par défaut. Définissez
`deleteAfterRun: false` pour les conserver (elles se désactiveront après succès).

## Concepts

### Tâches

Une tâche cron est un enregistrement stocké avec :

- un **calendrier** (quand il doit s'exécuter),
- une **charge utile** (ce qu'il doit faire),
- un **mode de livraison** optionnel (`announce`, `webhook`, ou `none`).
- une **liaison d'agent** optionnelle (`agentId`) : exécuter la tâche sous un agent spécifique ; si
  manquant ou inconnu, le gateway revient à l'agent par défaut.

Les tâches sont identifiées par un `jobId` stable (utilisé par les API CLI/Gateway).
Dans les appels d'outils d'agent, `jobId` est canonique ; `id` hérité est accepté pour la compatibilité.
Les tâches uniques se suppriment automatiquement après succès par défaut ; définissez `deleteAfterRun: false` pour les conserver.

### Calendriers

Cron supporte trois types de calendrier :

- `at` : timestamp unique via `schedule.at` (ISO 8601).
- `every` : intervalle fixe (ms).
- `cron` : expression cron à 5 champs (ou 6 champs avec secondes) avec fuseau horaire IANA optionnel.

Les expressions cron utilisent `croner`. Si un fuseau horaire est omis, le
fuseau horaire local de l'hôte Gateway est utilisé.

Pour réduire les pics de charge en haut de l'heure sur plusieurs gateways, OpenClaw applique une
fenêtre de décalage déterministe par tâche de jusqu'à 5 minutes pour les expressions récurrentes
en haut de l'heure (par exemple `0 * * * *`, `0 */2 * * *`). Les expressions à heure fixe
comme `0 7 * * *` restent exactes.

Pour tout calendrier cron, vous pouvez définir une fenêtre de décalage explicite avec `schedule.staggerMs`
(`0` garde le timing exact). Raccourcis CLI :

- `--stagger 30s` (ou `1m`, `5m`) pour définir une fenêtre de décalage explicite.
- `--exact` pour forcer `staggerMs = 0`.

### Exécution principale vs isolée

#### Tâches de session principale (événements système)

Les tâches principales enqueue un événement système et réveillent optionnellement le runner heartbeat.
Elles doivent utiliser `payload.kind = "systemEvent"`.

- `wakeMode: "now"` (par défaut) : l'événement déclenche une exécution heartbeat immédiate.
- `wakeMode: "next-heartbeat"` : l'événement attend le prochain heartbeat planifié.

C'est le meilleur choix quand vous voulez l'invite heartbeat normale + contexte de session principale.
Voir [Heartbeat](/gateway/heartbeat).

#### Tâches isolées (sessions cron dédiées)

Les tâches isolées exécutent un tour d'agent dédié dans la session `cron:<jobId>`.

Comportements clés :

- L'invite est préfixée avec `[cron:<jobId> <job name>]` pour la traçabilité.
- Chaque exécution démarre un **nouvel id de session** (pas de carry-over de conversation antérieure).
- Comportement par défaut : si `delivery` est omis, les tâches isolées annoncent un résumé (`delivery.mode = "announce"`).
- `delivery.mode` choisit ce qui se passe :
  - `announce` : livrer un résumé au canal cible et poster un bref résumé à la session principale.
  - `webhook` : POST la charge utile d'événement terminé à `delivery.to` quand l'événement terminé inclut un résumé.
  - `none` : interne uniquement (pas de livraison, pas de résumé de session principale).
- `wakeMode` contrôle quand le résumé de session principale est posté :
  - `now` : heartbeat immédiat.
  - `next-heartbeat` : attend le prochain heartbeat planifié.

Utilisez les tâches isolées pour les chores bruyantes, fréquentes ou « de fond » qui ne devraient pas spammer
votre historique de chat principal.

### Formes de charge utile (ce qui s'exécute)

Deux types de charge utile sont supportés :

- `systemEvent` : session principale uniquement, routée via l'invite heartbeat.
- `agentTurn` : session isolée uniquement, exécute un tour d'agent dédié.

Champs `agentTurn` courants :

- `message` : invite de texte requise.
- `model` / `thinking` : remplacements optionnels (voir ci-dessous).
- `timeoutSeconds` : remplacement de timeout optionnel.
- `lightContext` : mode bootstrap léger optionnel pour les tâches qui n'ont pas besoin d'injection de fichier bootstrap workspace.

Configuration de livraison :

- `delivery.mode` : `none` | `announce` | `webhook`.
- `delivery.channel` : `last` ou un canal spécifique.
- `delivery.to` : cible spécifique au canal (announce) ou URL webhook (mode webhook).
- `delivery.bestEffort` : éviter d'échouer la tâche si la livraison announce échoue.

La livraison announce supprime les envois d'outils de messagerie pour l'exécution ; utilisez `delivery.channel`/`delivery.to`
pour cibler le chat à la place. Quand `delivery.mode = "none"`, aucun résumé n'est posté à la session principale.

Si `delivery` est omis pour les tâches isolées, OpenClaw utilise par défaut `announce`.

#### Flux de livraison announce

Quand `delivery.mode = "announce"`, cron livre directement via les adaptateurs de canal sortant.
L'agent principal n'est pas lancé pour composer ou transférer le message.

Détails du comportement :

- Contenu : la livraison utilise les charges utiles sortantes de l'exécution isolée (texte/média) avec chunking normal et
  formatage de canal.
- Les réponses heartbeat uniquement (`HEARTBEAT_OK` sans contenu réel) ne sont pas livrées.
- Si l'exécution isolée a déjà envoyé un message à la même cible via l'outil de message, la livraison est
  ignorée pour éviter les doublons.
- Les cibles de livraison manquantes ou invalides échouent la tâche sauf si `delivery.bestEffort = true`.
- Un bref résumé est posté à la session principale uniquement quand `delivery.mode = "announce"`.
- Le résumé de session principale respecte `wakeMode` : `now` déclenche un heartbeat immédiat et
  `next-heartbeat` attend le prochain heartbeat planifié.

#### Flux de livraison webhook

Quand `delivery.mode = "webhook"`, cron poste la charge utile d'événement terminé à `delivery.to` quand l'événement terminé inclut un résumé.

Détails du comportement :

- Le point de terminaison doit être une URL HTTP(S) valide.
- Aucune livraison de canal n'est tentée en mode webhook.
- Aucun résumé de session principale n'est posté en mode webhook.
- Si `cron.webhookToken` est défini, l'en-tête auth est `Authorization: Bearer <cron.webhookToken>`.
- Fallback déprécié : les tâches héritées stockées avec `notify: true` postent toujours à `cron.webhook` (si configuré), avec un avertissement pour que vous puissiez migrer vers `delivery.mode = "webhook"`.

### Remplacements de modèle et de réflexion

Les tâches isolées (`agentTurn`) peuvent remplacer le modèle et le niveau de réflexion :

- `model` : chaîne Provider/model (par ex. `anthropic/claude-sonnet-4-20250514`) ou alias (par ex. `opus`)
- `thinking` : niveau de réflexion (`off`, `minimal`, `low`, `medium`, `high`, `xhigh` ; modèles GPT-5.2 + Codex uniquement)

Remarque : vous pouvez également définir `model` sur les tâches de session principale, mais cela change le modèle de session principale partagée. Nous recommandons les remplacements de modèle uniquement pour les tâches isolées pour éviter
les changements de contexte inattendus.

Priorité de résolution :

1. Remplacement de charge utile de tâche (le plus élevé)
2. Valeurs par défaut spécifiques au hook (par ex. `hooks.gmail.model`)
3. Défaut de configuration d'agent

### Contexte bootstrap léger

Les tâches isolées (`agentTurn`) peuvent définir `lightContext: true` pour s'exécuter avec un contexte bootstrap léger.

- Utilisez ceci pour les chores planifiées qui n'ont pas besoin d'injection de fichier bootstrap workspace.
- En pratique, le runtime intégré s'exécute avec `bootstrapContextMode: "lightweight"`, ce qui garde le contexte bootstrap cron vide intentionnellement.
- Équivalents CLI : `openclaw cron add --light-context ...` et `openclaw cron edit --light-context`.

### Livraison (canal + cible)

Les tâches isolées peuvent livrer la sortie à un canal via la configuration `delivery` de haut niveau :

- `delivery.mode` : `announce` (livraison de canal), `webhook` (HTTP POST), ou `none`.
- `delivery.channel` : `whatsapp` / `telegram` / `discord` / `slack` / `mattermost` (plugin) / `signal` / `imessage` / `last`.
- `delivery.to` : cible de destinataire spécifique au canal.

La livraison `announce` n'est valide que pour les tâches isolées (`sessionTarget: "isolated"`).
La livraison `webhook` est valide pour les tâches principales et isolées.

Si `delivery.channel` ou `delivery.to` est omis, cron peut revenir à la
« dernière route »
