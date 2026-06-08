---
title: "Session, memory, and context engine - Transcript Persistence Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Transcript Persistence Maturity Note

## Résumé

La persistance des transcriptions a une architecture et une implémentation solides : la passerelle possède l'état de la session, `sessions.json` mappe les clés aux fichiers de transcription actifs, et les transcriptions JSONL sont en ajout seul, verrouillées, expurgées, indexées, archivées et budgétisées. Le risque réside dans la durabilité opérationnelle lors de réinitialisations, nettoyages, débordements de contexte et sauvegarde/restauration : les preuves d'archive montrent plusieurs rapports ouverts où l'historique valide peut être masqué, orphelin ou croître sans limites.

## Portée de la catégorie

Cette catégorie couvre les fichiers de session JSONL, l'ajout et l'expurgation de transcriptions, les verrous d'écriture de session, le comportement de rotation/archivage des transcriptions, le nettoyage du budget disque, les magasins de transcriptions des fournisseurs et la durabilité du redémarrage/réparation.

## Fonctionnalités

- Transcript Persistence: Couvre la persistance des transcriptions sur les fichiers de session JSONL, l'ajout et l'expurgation de transcriptions, les verrous d'écriture de session, le comportement de rotation/archivage des transcriptions, le nettoyage du budget disque, les magasins de transcriptions des fournisseurs et la durabilité du redémarrage/réparation.
- Durability: Couvre la durabilité sur les fichiers de session JSONL, l'ajout et l'expurgation de transcriptions, les verrous d'écriture de session, le comportement de rotation/archivage des transcriptions, le nettoyage du budget disque, les magasins de transcriptions des fournisseurs et la durabilité du redémarrage/réparation.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Beta (78%)`
- Signaux positifs: la source couvre les en-têtes de transcription, les files d'attente d'ajout, les verrous de fichier, l'expurgation, l'idempotence, la maintenance et le nettoyage du budget disque ; les tests d'historique de la passerelle exercent les lectures de transcription bornées et l'historique HTTP/SSE.
- Signaux négatifs: les flux de travail de sauvegarde/restauration et de durabilité complète sont moins directement prouvés que le comportement d'ajout/lecture du chemin critique.
- Lacunes d'intégration: ajouter un scénario de redémarrage et restauration qui s'étend sur l'ajout, la réinitialisation, l'archivage, le nettoyage en mode simulation, le nettoyage en mode application, la lecture d'historique et la récupération explicite à partir d'une transcription précédente.

## Score de qualité

- Score: `Alpha (58%)`
- Rapports Gitcrawl: plusieurs problèmes ouverts décrivent un mappage de transcription inexistant, une croissance de transcription non bornée, un support de sauvegarde/restauration, des en-têtes JSONL manquants, un archivage de l'historique par le docteur en tant qu'orphelins, et WebChat masquant les sessions archivées.
- Rapports Discrawl: les résultats d'archive Discord discutent du nettoyage des transcriptions orphelines, de la préservation de l'historique des points de contrôle de compaction, des artefacts de transcription seule fuyant dans l'historique, et de la confusion entre les magasins d'historique CLI natifs et les transcriptions OpenClaw.
- Bonnes qualités: la source a des files d'attente d'ajout disciplinées, des verrous d'écriture, l'expurgation, la dénomination d'archive et des primitives de nettoyage du budget disque.
- Mauvaises qualités: la durabilité des données côté utilisateur a toujours des risques actifs de perte/masquage autour de la réinitialisation, du nettoyage, de la détection d'orphelins et de la restauration entre magasins.
- Exclu de la qualité: la profondeur des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution.

## Score de complétude

- Score: `Beta (78%)`
- Instructions de surface: évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs: les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la persistance des transcriptions et la durabilité.
- Signaux négatifs: la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les opérateurs n'ont pas encore d'histoire de restauration complète pour tous les chemins de réinitialisation/archivage/orphelin.
- La durabilité de l'historique dépend de plusieurs fichiers en interaction et de politiques de nettoyage, ce qui rend les recommandations de réparation non sécurisées coûteuses.

## Preuves

### Docs

- `docs/reference/session-management-compaction.md:40` définit deux couches de persistance: `sessions.json` et transcription JSONL.
- `docs/reference/session-management-compaction.md:57` dit que les lecteurs d'historique actif doivent utiliser des lectures de queue bornées ou l'index de transcription.
- `docs/reference/session-management-compaction.md:77` documente la maintenance du magasin, les archives de réinitialisation, les budgets disque et les commandes de nettoyage.
- `docs/reference/transcript-hygiene.md:10` documente la réparation spécifique au fournisseur et le comportement de sauvegarde avant les réécritures durables.

### Source

- `src/config/sessions/transcript.ts:105` résout les fichiers de transcription ; `src/config/sessions/transcript.ts:199` ajoute les messages de l'assistant.
- `src/config/sessions/transcript-append.ts:203` sérialise les files d'attente d'ajout par transcription ; `src/config/sessions/transcript-append.ts:284` acquiert les verrous d'écriture ; `src/config/sessions/transcript-append.ts:346` expurge avant l'ajout.
- `src/config/sessions/store.ts:360` sauvegarde les magasins de session ; `src/config/sessions/store.ts:675` archive les transcriptions de session supprimées.
- `src/config/sessions/disk-budget.ts:535` applique les budgets disque du répertoire des sessions.

### Tests d'intégration

- `src/gateway/sessions-history-http.test.ts:296` retourne l'historique de session sur REST direct ; `src/gateway/sessions-history-http.test.ts:456` diffuse l'historique borné sur SSE.
- `src/gateway/server.sessions.store-rpc.test.ts:421` vérifie que la réinitialisation crée un nouvel identifiant de session et archive l'ancienne transcription.
- `src/gateway/server.sessions.compaction.test.ts:24` couvre le comportement de branche de point de contrôle/restauration sur les transcriptions compactées.

### Tests unitaires

- `src/config/sessions/transcript-append-redact.test.ts:45` vérifie que les secrets sont masqués avant les écritures disque ; `src/config/sessions/transcript-append-redact.test.ts:432` vérifie la déduplication du miroir de livraison.
- `src/config/sessions/disk-budget.test.ts` et `src/config/sessions/store.pruning.test.ts` couvrent les assistants de maintenance et de nettoyage.
- `packages/agent-core/src/harness/session/jsonl-repo.ts:38` implémente le comportement du référentiel de session JSONL.

### Requêtes Gitcrawl

Requête:

`gitcrawl search issues "transcript jsonl session file disk budget" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats:

- A retourné les problèmes ouverts `#75151 Context overflow reset can map sessionFile to nonexistent transcript` et `#85025 Defaults cause unbounded transcript growth + nightly session death`.

Requête:

`gitcrawl search issues "openclaw sessions transcripts chat.history" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats:

- A retourné 13 rapports ouverts, y compris `#86382` préservation de sauvegarde/JSONL, `#84209` `sessionKey` persistant dans les en-têtes, `#73471` archivage de l'historique des transcriptions par le docteur en tant qu'orphelins, `#77819` WebChat masquant les sessions archivées, et `#45003` demande de script de restauration.

### Requêtes Discrawl

Requête:

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "transcript jsonl session file disk budget"`

Résultats:

- N'a retourné aucune ligne correspondante.

Requête:

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "openclaw sessions transcripts chat.history"`

Résultats:

- A retourné des discussions PR/review et support sur le nettoyage des JSONL orphelins, la préservation de l'historique de chat sur les points de contrôle de compaction, le masquage des artefacts de transcription seule et l'historique CLI natif n'apparaissant pas dans WebChat.
