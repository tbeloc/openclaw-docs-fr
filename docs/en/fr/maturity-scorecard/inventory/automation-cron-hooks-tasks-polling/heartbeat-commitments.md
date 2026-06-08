---
title: "Automation: cron, hooks, tasks, polling - Heartbeat Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Heartbeat Maturity Note

## Résumé

Heartbeat et les engagements déduits forment le côté approximatif du sondage/suivi de l'automatisation. L'implémentation inclut la planification, les portes d'heures actives, les refroidissements de réveil, le filtrage des événements, le report de session occupée, le routage de livraison, la gestion des outils de réponse et l'extraction/exécution des engagements. C'est une implémentation riche en fonctionnalités, mais les preuves d'archive montrent que le comportement autour des heures actives, des réveils de groupe, des premiers messages post-heartbeat et des attentes d'inactivité basées sur l'activité confond toujours les utilisateurs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Planification du heartbeat : Couvre la planification du heartbeat sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Heures actives : Couvre les heures actives sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Gestion du réveil et du refroidissement : Couvre la gestion du réveil et du refroidissement sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Tâches heartbeat due-only : Couvre les tâches heartbeat due-only sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Vérifications d'engagement : Couvre les vérifications d'engagement sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.

## Fonctionnalités

- Planification du heartbeat : Couvre la planification du heartbeat sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Heures actives : Couvre les heures actives sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Gestion du réveil et du refroidissement : Couvre la gestion du réveil et du refroidissement sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Tâches heartbeat due-only : Couvre les tâches heartbeat due-only sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.
- Vérifications d'engagement : Couvre les vérifications d'engagement sur les exécutions périodiques du heartbeat, le comportement des heures actives et de la planification variable, la gestion du réveil/refroidissement, les invites de heartbeat et le mode tâche due-only, et le comportement connexe du heartbeat et des engagements.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La planification du heartbeat, les heures actives, les refroidissements, le filtrage des événements, les gardes de session occupée, le routage de livraison, les remplacements de modèle, les engagements, les rappels fantômes et la planification e2e des heures actives ont des tests ciblés.
- Signaux négatifs : Le comportement en direct complet dépend des canaux actifs, des sessions longues et du timing des messages utilisateur après le heartbeat ; ceux-ci sont difficiles à prouver avec des fixtures unitaires uniquement.
- Lacunes d'intégration : Un scénario en direct devrait couvrir les heures actives du heartbeat, le saut de tâche due-only, l'événement de réveil cron, le réveil d'achèvement exec, le report occupé du sous-agent, la vérification d'engagement et la livraison du canal de groupe.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : Le problème #14051 demande un délai d'inactivité du heartbeat basé sur l'activité ; la PR #58683 ajoute des intervalles variables en fonction de l'heure de la journée ; le problème #40611 signale que les retries de dérive du heartbeat bloquent Telegram ; le problème #85614 signale que le premier message utilisateur après le sondage du heartbeat est mal identifié comme continuation du heartbeat ; la PR #78718 corrige les défauts de secours au niveau de l'agent.
- Rapports Discrawl : Le fil de discussion cron Dreaming montre que les opérateurs peuvent être surpris que les tâches gérées ciblant main s'exécutent via heartbeat et peuvent être ignorées par `activeHours` ; le problème de réveil de groupe #47578 a été fermé après que le main actuel ait corrigé les réveils d'achèvement exec/ACP.
- Bonnes qualités : Heartbeat a des raisons de saut explicites, une logique d'heures actives, des gardes de refroidissement/inondation, la préservation de la cible de livraison, le support des outils de réponse et la politique d'exécution spécifique aux engagements.
- Mauvaises qualités : Heartbeat participe à de nombreux flux adjacents - cron, achèvements exec, engagements, dreaming, groupes et achèvements de tâches - et les utilisateurs lisent mal pourquoi les exécutions sont ignorées ou routées via heartbeat.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve d'exécution ; ce sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la planification du heartbeat, les heures actives, la gestion du réveil et du refroidissement, les tâches heartbeat due-only, les vérifications d'engagement.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La documentation devrait rendre la relation « main-session cron utilise la voie heartbeat » plus visible.
- Le délai d'inactivité basé sur l'activité reste une demande de produit ouverte.
- La limite du premier message après heartbeat devrait rester un point focal de régression car elle peut corrompre l'interaction utilisateur normale.

## Preuves

### Docs

- `docs/automation/index.md` compare cron et heartbeat, explique heartbeat comme une sensibilisation périodique approximative et note que les enregistrements de tâches ne sont pas créés pour les tours de heartbeat.
- `docs/gateway/heartbeat.md` documente la configuration du heartbeat, les heures actives, le comportement de réveil, les raisons de saut et le dépannage.
- `docs/concepts/commitments.md` documente les engagements déduits et la livraison du heartbeat des vérifications dues.

### Source

- `src/infra/heartbeat-runner.ts`, `src/infra/heartbeat-schedule.ts`, `src/infra/heartbeat-active-hours.ts`, `src/infra/heartbeat-cooldown.ts`, `src/infra/heartbeat-events-filter.ts`, `src/infra/heartbeat-wake.ts` et `src/infra/heartbeat-visibility.ts` implémentent la planification du heartbeat et la gestion des événements.
- `src/commitments/runtime.ts`, `src/commitments/extraction.ts`, `src/commitments/store.ts` et `src/commitments/model-selection.runtime.ts` implémentent les engagements déduits.
- `src/auto-reply/heartbeat.ts`, `src/auto-reply/heartbeat-filter.ts` et `src/agents/heartbeat-system-prompt.ts` connectent heartbeat à l'invite d'agent et au comportement de réponse.

### Tests d'intégration

- `src/infra/heartbeat-runner.active-hours-schedule.e2e.test.ts` teste la planification consciente des heures actives.
- `src/commitments/commitments-full-chain.integration.test.ts` et `src/commitments/commitments-heartbeat-policy.e2e.test.ts` couvrent les flux engagement-vers-heartbeat.
- `src/infra/heartbeat-runner.ghost-reminder.test.ts` couvre le routage des événements cron/exec via heartbeat.

### Tests unitaires

- `src/infra/heartbeat-schedule.test.ts`, `src/infra/heartbeat-active-hours.test.ts`, `src/infra/heartbeat-cooldown.test.ts`, `src/infra/heartbeat-events-filter.test.ts`, `src/infra/heartbeat-runner.skips-busy-session-lane.test.ts`, `src/infra/heartbeat-runner.subagent-session-guard.test.ts` et `src/infra/heartbeat-runner.model-override.test.ts` couvrent la mécanique du heartbeat.
- `src/commitments/extraction.test.ts`, `src/commitments/store.test.ts` et `src/commitments/runtime.test.ts` couvrent les engagements.
- `src/auto-reply/heartbeat.test.ts` et `src/auto-reply/heartbeat-filter.test.ts` couvrent le comportement du heartbeat auto-reply.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "heartbeat commitments skipWhenBusy activeHours no-tasks-due" --json --limit 5`

Résultats :

- Aucun résultat pour la requête exacte.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "heartbeat activeHours" --json --limit 5`

Résultats :

- Le problème #14051 demande un heartbeat basé sur l'activité avec délai d'inactivité.
- La PR #58683 ajoute la planification en fonction de l'heure de la journée pour les intervalles variables.
- Le problème #40611 signale que le retry de dérive du heartbeat bloque Telegram lors de conversations actives.
- Le problème #85614 signale que le premier message utilisateur après le sondage du heartbeat est mal identifié comme continuation du heartbeat.
- La PR #78718 corrige les défauts de secours du heartbeat au niveau de l'agent.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "heartbeat activeHours"`

Résultats :

- L'examen automatisé du problème #14051 maintient le délai d'inactivité du heartbeat basé sur l'activité ouvert.
- La fermeture du problème #47578 indique que le main actuel implémente le chemin de réveil exec/ACP de session de groupe avec des réveils de heartbeat ciblés préservant les clés de session.
- Le fil de discussion du problème dreaming explique qu'un cron dreaming géré ciblant `main` s'exécute via heartbeat et peut être ignoré par les fenêtres silencieuses des heures actives.
