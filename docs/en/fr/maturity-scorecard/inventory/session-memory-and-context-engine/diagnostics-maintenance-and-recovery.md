---
title: "Session, memory, and context engine - Diagnostics, Maintenance, and Recovery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Diagnostics, Maintenance, and Recovery Maturity Note

## Résumé

Les diagnostics et la récupération pour les sessions sont substantiels : le suivi de l'état de la session,
la classification de l'attention, la récupération des sessions bloquées, la récupération de la session principale
interrompue, la récupération des sous-agents orphelins, la récupération de la file d'attente de livraison, les bundles de diagnostics,
et les avertissements de maintenance existent tous. Le risque est que la récupération soit toujours
au mieux un effort et répartie sur plusieurs sous-systèmes, donc les opérateurs ont besoin de résultats clairs
et de valeurs par défaut sûres quand une session est bloquée ou l'historique est suspect.

## Portée de la catégorie

Cette catégorie couvre les diagnostics des sessions bloquées, la récupération au redémarrage, la reprise des
sous-agents orphelins, les avertissements de maintenance de session, les files d'attente de livraison, les bundles
de diagnostics, les snapshots de stabilité, les surfaces de réparation de transcription, et la visibilité
des diagnostics de mémoire/session.

## Fonctionnalités

- Rapports de diagnostic de session : Couvre les diagnostics des sessions bloquées, les bundles de diagnostics, les snapshots de stabilité, et la visibilité de l'opérateur sur la santé de la transcription et de la session.
- Avertissements de maintenance de session : Couvre les avertissements de maintenance au redémarrage, les files d'attente de livraison, les signaux de nettoyage de mémoire/session, et l'état de maintenance visible par l'opérateur.
- Récupération de session et de transcription : Couvre la récupération au redémarrage, la reprise des sous-agents orphelins, la réparation de transcription, et la restauration sûre de l'état de la session après les défaillances.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : la source et les tests couvrent les cartes d'état de session, la récupération des sessions bloquées, la récupération du redémarrage de la session principale, la récupération de la file d'attente de livraison, les méthodes Gateway de diagnostics, les bundles de support, et les avertissements de maintenance.
- Signaux négatifs : les flux d'opérateur en direct pour diagnostiquer une session bloquée et confirmer la récupération sur les canaux sont moins complets que les tests d'aide/runtime.
- Lacunes d'intégration : ajouter un scénario qui force une exécution active obsolète, exécute les diagnostics, effectue la récupération, vérifie l'état de la voie de session, et confirme aucune perte de transcription/historique.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : la requête de diagnostic de session bloquée exacte n'a retourné aucun résultat, mais les problèmes de nettoyage de session et d'archive de transcription connexes restent des risques de qualité actifs pour la maintenance.
- Rapports Discrawl : la requête de diagnostic de session bloquée exacte n'a retourné aucune ligne ; la requête de maintenance de session a retourné des discussions d'archive sur la réinitialisation des archives et les préoccupations d'examen du nettoyage de la rétention.
- Bonnes qualités : les actions de récupération enregistrent les résultats explicites et évitent souvent les actions destructrices sauf si configurées ; les bundles de diagnostics ont des conseils de confidentialité.
- Mauvaises qualités : les surfaces de récupération/maintenance sont distribuées, et un mauvais chemin de nettoyage/récupération peut sembler réussi tout en cachant l'historique.
- Exclu de la qualité : la profondeur des tests unitaires, d'intégration, e2e, en direct et de flux runtime.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les rapports de diagnostic de session, les avertissements de maintenance de session, la récupération de session et de transcription.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les opérateurs ont besoin d'un arbre de décision plus clair pour la session bloquée, l'historique manquant, le verrou de transcription, et les problèmes de nettoyage.
- La preuve de récupération devrait montrer l'état avant/après de la voie de session, de la transcription, et de la livraison.

## Preuves

### Docs

- `docs/gateway/diagnostics.md:10` décrit les bundles de diagnostics ; `docs/gateway/diagnostics.md:75` énumère le contenu du bundle ; `docs/gateway/diagnostics.md:112` documente l'enregistreur de stabilité.
- `docs/reference/session-management-compaction.md:77` documente les contrôles de maintenance et le nettoyage ; `docs/reference/session-management-compaction.md:97` documente le comportement du verrou d'écriture de transcription.
- `docs/diagnostics/flags.md:128` décrit les enregistrements de chronologie des diagnostics.

### Source

- `src/logging/diagnostic-session-state.ts:35` stocke l'état de diagnostic de session ; `src/logging/diagnostic-session-attention.ts:27` classe l'attention de session.
- `src/logging/diagnostic-stuck-session-recovery.runtime.ts:84` récupère les sessions de diagnostic bloquées.
- `src/agents/subagent-orphan-recovery.ts:183` analyse et reprend les sessions de sous-agent orphelins.
- `src/agents/main-session-restart-recovery.ts:539` récupère les sessions principales interrompues.
- `src/infra/session-delivery-queue-recovery.ts` et `src/infra/session-maintenance-warning.ts` soutiennent la sécurité de livraison/maintenance.

### Tests d'intégration

- `src/logging/diagnostic-stuck-session-recovery.runtime.test.ts:161` réclame les exécutions intégrées actives obsolètes.
- `src/agents/main-session-restart-recovery.test.ts:390` reprend les sessions marquées avec une queue de transcription de résultat d'outil.
- `src/infra/session-delivery-queue.recovery.test.ts` couvre la persistance de retry/backoff pour la récupération de livraison.

### Tests unitaires

- `src/infra/session-maintenance-warning.test.ts` couvre les avertissements de maintenance de session active.
- `src/gateway/server-methods/diagnostics.test.ts:27` retourne les snapshots de stabilité filtrés.
- `src/logging/diagnostic-memory.test.ts` couvre les aides de diagnostics de mémoire.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "stuck session session recovery transcript repair memory diagnostic" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- Retourné `[]`.

Requête :

`gitcrawl search issues "sessions cleanup session maintenance transcript archive" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- Retourné l'ouverture `#77941` pour le support de nettoyage des sessions natives et `#60745` pour les sessions éphémères.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "stuck session session recovery transcript repair memory diagnostic"`

Résultats :

- Aucune ligne correspondante retournée.

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "sessions cleanup session maintenance transcript archive"`

Résultats :

- Retourné les explications d'archive de réinitialisation automatique de session et les commentaires d'examen sur le comportement de nettoyage de rétention d'archive de compaction.
