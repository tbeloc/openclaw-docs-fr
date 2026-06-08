---
title: "Voice and realtime talk - Talk Observability Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice and realtime talk - Talk Observability Maturity Note

## Résumé

Talk observability dispose d'une infrastructure runtime concrète : journaux d'événements, enregistrements de diagnostics, santé de session, suivi de la suppression d'écho, sortie live smoke, et diagnostics orientés Prometheus. La couverture est au niveau bêta. La qualité atteint le bêta car l'implémentation évite de bloquer les chemins runtime et capture la santé du fournisseur/session, mais la ligne de scorecard d'origine appelle toujours à la notation de la latence, du mode de défaillance et de la configuration avant la promotion bêta.

## Portée de la catégorie

Inclus dans cette catégorie :

- Journalisation des événements Talk : journalisation des événements Talk et mappage des événements de diagnostics
- Santé du journal de session : santé du journal de session, enregistrements de transcription, événements de pont et synchronisation de la suppression d'écho/sortie
- Sortie live smoke : sortie live smoke et inspection des événements du fournisseur
- Compteurs de diagnostics Prometheus : compteurs de diagnostics Prometheus pour les événements Talk
- Visibilité de l'opérateur sur la configuration : visibilité de l'opérateur sur la configuration, la latence et les modes de défaillance

## Fonctionnalités

- Journalisation des événements Talk : journalisation des événements Talk et mappage des événements de diagnostics
- Santé du journal de session : santé du journal de session, enregistrements de transcription, événements de pont et synchronisation de la suppression d'écho/sortie
- Sortie live smoke : sortie live smoke et inspection des événements du fournisseur
- Compteurs de diagnostics Prometheus : compteurs de diagnostics Prometheus pour les événements Talk
- Visibilité de l'opérateur sur la configuration : visibilité de l'opérateur sur la configuration, la latence et les modes de défaillance

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`

Les diagnostics, journaux, santé de session, événements de pont du fournisseur, compteurs Prometheus et sortie live smoke couvrent la plupart des comportements runtime observables par l'opérateur. La couverture n'est pas stable car la latence et la vérification de la configuration ne sont pas organisées dans un scorecard opérateur dédié.

## Score de qualité

- Score : `Bêta (70%)`

La qualité est soutenue par la journalisation non-bloquante, les événements delta de haut volume supprimés, les métadonnées de diagnostics structurées, les résumés de santé de session, l'état de suppression d'écho et les vérifications d'événements live smoke. La qualité est maintenue au plancher bêta car la visibilité de la configuration, de la latence et du mode de défaillance orientée opérateur sont toujours appelées comme entrées de maturité manquantes.

Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, live et de flux runtime réel.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : les docs archivées, source, test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la journalisation des événements Talk, la santé du journal de session, la sortie live smoke, les compteurs de diagnostics Prometheus, la visibilité de l'opérateur sur la configuration.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun scorecard de latence Talk dédié n'a été trouvé.
- Les chemins de configuration et de mode de défaillance sont documentés par morceaux plutôt qu'une liste de contrôle opérateur unique.
- La recherche d'archive pour les diagnostics de latence spécifiques à Talk n'a retourné aucun résultat direct pertinent.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:136` documente le comportement du journal d'événements dans l'interface utilisateur de contrôle.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:185` documente le statut du mode Talk et l'invocation live smoke.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/voice-overlay.md:43` documente une liste de contrôle de débogage avec journalisation et état de superposition.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:126` documente les notes natives, le repli et les détails de validation qui affectent le diagnostic de l'opérateur.

### Source

- `/Users/kevinlin/code/openclaw/src/talk/session-log-runtime.ts:29` suit la santé des événements de transcription et de pont.
- `/Users/kevinlin/code/openclaw/src/talk/session-log-runtime.ts:105` enregistre la synchronisation de la suppression d'écho et de la suppression de sortie.
- `/Users/kevinlin/code/openclaw/src/talk/diagnostics.ts:10` mappe les événements Talk dans les métadonnées d'événements de diagnostics.
- `/Users/kevinlin/code/openclaw/src/talk/logging.ts:13` supprime les événements delta de haut volume et enregistre les métadonnées d'événements non-bloquantes.
- `/Users/kevinlin/code/openclaw/extensions/diagnostics-prometheus/src/service.ts` expose les métriques de diagnostics Talk.
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts:148` couvre le pont backend OpenAI, WebRTC navigateur, Google Live et les chemins de relais Gateway.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/diagnostics-prometheus/src/service.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/talk/session-log-runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/diagnostics.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/logging.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/output-activity-tracker.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/turn-context-tracker.test.ts`

### Requêtes Gitcrawl

- `gitcrawl search issues "talk diagnostics latency session log" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` n'a retourné aucune correspondance directe.
- `gitcrawl search issues "talk realtime voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné des problèmes de configuration et de fournisseur pertinents à la visibilité des défaillances, incluant #83822, #84639 et #84664.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "talk diagnostics latency" --limit 5` n'a retourné aucun résultat direct pertinent à Talk.
- `/Users/kevinlin/.local/bin/discrawl search "talk realtime voice" --limit 5` a retourné les notes de version du 2026-05-27 indiquant que les exécutions Talk en temps réel peuvent être inspectées, dirigées, annulées et suivies.
- `/Users/kevinlin/.local/bin/discrawl search "OpenAI Realtime Talk Google Live" --limit 5` a retourné les notes de version du 2026-05-03 indiquant que les erreurs en temps réel s'affichent dans Talk.
