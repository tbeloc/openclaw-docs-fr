---
title: "Session, memory, and context engine - Memory Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Memory Maturity Note

## Résumé

La surface mémoire d'OpenClaw combine le comportement mémoire orienté utilisateur avec la couche de stockage et de récupération backend qui le rend possible. Elle inclut le `MEMORY.md` canonique, les fichiers datés `memory/*.md`, les outils de recherche mémoire, le rappel pré-réponse Active Memory, les hooks session-memory, les sections de prompt mémoire, les capacités mémoire des plugins, les magasins soutenus par SQLite, l'accélération optionnelle sqlite-vec, les fournisseurs d'embedding distants et locaux, la config de collection QMD, et l'indexation des transcriptions de session.

La catégorie combinée est notée au niveau backend plus conservateur. La documentation est solide, mais les rapports actifs montrent toujours des index obsolètes, l'empoisonnement session-memory, la pollution par rêve, le comportement de timeout Active Memory, l'inadéquation fournisseur/modèle, la contention QMD/SQLite, et la complexité de configuration.

## Portée de la catégorie

Cette catégorie couvre les fichiers mémoire racine, la mémoire active, l'exposition des outils de recherche/obtention/stockage mémoire, les sections de prompt mémoire, les plans de vidage mémoire, le comportement des hooks session-memory, l'enregistrement de capacité des plugins mémoire visibles aux agents, la config backend mémoire, le schéma SQLite, l'accélération vectorielle, la sélection du fournisseur d'embedding, la récupération d'embedding distante, l'analyse des processus/requêtes QMD, l'indexation des transcriptions de session pour la recherche, les chemins supplémentaires, et les limites de sécurité backend.

## Fonctionnalités

- Memory Backend Storage: Couvre Memory Backend Storage sur la config backend mémoire, le schéma SQLite, l'accélération vectorielle, la sélection du fournisseur d'embedding, la récupération d'embedding distante, l'analyse des processus/requêtes QMD, l'indexation des transcriptions de session pour la recherche, les chemins supplémentaires, et les limites de sécurité backend.
- Embedding Search: Couvre Embedding Search sur la config backend mémoire, le schéma SQLite, l'accélération vectorielle, la sélection du fournisseur d'embedding, la récupération d'embedding distante, l'analyse des processus/requêtes QMD, l'indexation des transcriptions de session pour la recherche, les chemins supplémentaires, et les limites de sécurité backend.
- Memory Files: Couvre Memory Files sur les fichiers mémoire racine, la mémoire active, l'exposition des outils de recherche/obtention/stockage mémoire, les sections de prompt mémoire, les plans de vidage mémoire, le comportement des hooks session-memory, et l'enregistrement de capacité des plugins mémoire visibles aux agents.
- Memory search and store tools: Couvre l'exposition des outils de recherche/obtention/stockage mémoire, les sections de prompt mémoire, les plans de vidage mémoire, le comportement des hooks session-memory, et l'enregistrement de capacité des plugins mémoire visibles aux agents.
- Active Memory: Couvre Active Memory sur les fichiers mémoire racine, la mémoire active, l'exposition des outils de recherche/obtention/stockage mémoire, les sections de prompt mémoire, les plans de vidage mémoire, le comportement des hooks session-memory, et l'enregistrement de capacité des plugins mémoire visibles aux agents.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Alpha (66%)`
- Signaux positifs: la documentation explique les concepts mémoire, Active Memory, la config backend, la recherche hybride, l'accélération sqlite-vec, la config backend QMD, et la recherche mémoire de session expérimentale. La source expose la résolution canonique des fichiers mémoire, le chargement mémoire à l'exécution, la construction de prompts, les plans de vidage, le comportement des hooks session-memory, la résolution de config backend, la gestion du schéma SQLite, les fournisseurs d'embedding locaux/distants, la détection des processus QMD, et l'indexation des fichiers de session.
- Signaux négatifs: le rappel Active Memory end-to-end sur les plugins mémoire sélectionnés et les sessions pilotées par canal est moins prouvé que le comportement unitaire fichier/exécution, tandis que la fiabilité du fournisseur en direct, la disponibilité du processus QMD, et les flux d'indexation multi-backend sont difficiles à prouver avec des tests unitaires locaux.
- Lacunes d'intégration: ajouter un scénario qui stocke une mémoire, l'indexe, la rappelle avec Active Memory, effectue un vidage pré-compaction, et confirme le résultat sur les sessions directes et pilotées par canal; ajouter une matrice smoke backend qui exécute le fallback par mot-clé intégré, la recherche vectorielle sqlite-vec, la recherche lexicale QMD, la préparation vectorielle QMD, et un fournisseur d'embedding distant avec injection de défaillance.

## Score de qualité

- Score: `Alpha (58%)`
- Rapports Gitcrawl: de nombreux problèmes ouverts restent pour les index mémoire obsolètes, la fiabilité d'embedding en direct, la contention de verrou SQLite QMD, l'inadéquation docs/exécution, la pollution par rêve, la classification de timeout Active Memory, l'indexation session-memory, et le couplage de capacité des outils mémoire.
- Rapports Discrawl: les discussions d'archive recommandent la mémoire canonique basée sur fichiers plus la récupération QMD, expliquent Active Memory comme une couche pré-réponse, soulignent le couplage de capacité LanceDB, et montrent le dépannage autour de l'inadéquation fournisseur/modèle, des index vides, des répertoires mémoire manquants, et les compromis QMD versus recherche intégrée.
- Bonnes qualités: le modèle mental basé sur fichiers est compréhensible, l'état du plugin mémoire a une API de capacité consolidée, la config backend est explicite, les valeurs par défaut sont conservatrices pour l'utilisation interactive CPU uniquement, et HTTP distant a une limite de politique SSRF.
- Mauvaises qualités: l'exécution mémoire, l'indexation, Active Memory, le rêve, la mémoire de session, la configuration embedding/fournisseur, et la performance/fiabilité backend interagissent de manière à pouvoir polluer, bloquer, ou varier substantiellement selon l'environnement.
- Exclu de la qualité: profondeur des tests unitaires, intégration, e2e, en direct, et flux d'exécution.

## Score de complétude

- Score: `Alpha (66%)`
- Instructions de surface: évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs: les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour Memory Backend Storage, Embedding Search, Memory Files, Memory search and store tools, Active Memory.
- Signaux négatifs: la note archivée a précédé la notation de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Active Memory est toujours une couche mince mais sensible aux politiques, en particulier en dehors des chats persistants directs.
- Les noms d'outils et les capacités des plugins se stabilisent toujours pour les plugins mémoire non-core.
- Les opérateurs ont besoin de diagnostics plus clairs pour les index vides, les index sales, l'inadéquation des fournisseurs, et la contention de verrou QMD.
- La recherche de transcription de session est toujours marquée comme expérimentale dans la documentation et la configuration.

## Preuves

### Documentation

- `docs/concepts/memory.md`, `docs/concepts/active-memory.md`, `docs/concepts/memory-search.md`, et `docs/cli/memory.md` documentent le modèle mémoire visible par l'utilisateur.
- `docs/reference/memory-config.md:35` dit que Active Memory utilise la config propriétaire du plugin; `docs/reference/memory-config.md:410` documente la recherche mémoire de session expérimentale.
- `docs/reference/memory-config.md:47` documente la sélection du fournisseur; `docs/reference/memory-config.md:286` documente la recherche hybride; `docs/reference/memory-config.md:427` documente l'accélération sqlite-vec; `docs/reference/memory-config.md:447` documente la config backend QMD.
- `docs/concepts/memory-qmd.md` documente l'utilisation et les compromis QMD.
- `docs/channels/discord.md:285` explique comment la mémoire se comporte dans les canaux de guilde Discord.

### Source

- `src/memory/root-memory-files.ts:4` définit `MEMORY.md`; `src/memory/root-memory-files.ts:33` résout le fichier mémoire racine canonique.
- `src/plugins/memory-state.ts:230` construit les sections de prompt mémoire; `src/plugins/memory-state.ts:271` résout les plans de vidage mémoire.
- `src/plugins/memory-runtime.ts:56` obtient le gestionnaire de recherche mémoire active.
- `src/hooks/bundled/session-memory/handler.ts:130` sauvegarde le contexte de session en mémoire sur `/new` ou `/reset`.
- `packages/memory-host-sdk/src/host/backend-config.ts:385` résout la config backend mémoire; `packages/memory-host-sdk/src/host/backend-config.ts:422` construit les chemins QMD et les collections par défaut.
- `packages/memory-host-sdk/src/host/memory-schema.ts:4` assure le schéma SQLite.
- `packages/memory-host-sdk/src/host/embeddings.ts:48` crée les fournisseurs d'embedding locaux; `packages/memory-host-sdk/src/host/embeddings-remote-fetch.ts:31` récupère les vecteurs d'embedding distants.
- `packages/memory-host-sdk/src/host/qmd-process.ts:49` vérifie la disponibilité du binaire QMD; `packages/memory-host-sdk/src/host/session-files.ts:300` liste les fichiers de session pour l'indexation.

### Tests d'intégration

- `src/hooks/bundled/session-memory/handler.test.ts:255` vérifie la création de fichier mémoire à partir du contenu de session.
- `src/plugin-sdk/memory-host-search.test.ts` couvre l'accès au gestionnaire de recherche mémoire active soutenus par SDK.
- `src/agents/memory-search.test.ts:237` couvre la configuration de synchronisation session-memory utilisée par l'indexation à l'exécution.
- `packages/memory-host-sdk/src/host/remote-http.test.ts` couvre le comportement HTTP distant.
- `packages/memory-host-sdk/src/host/qmd-process.test.ts:139` couvre la détection de disponibilité QMD et la gestion des défaillances de commande.
- `packages/memory-host-sdk/src/host/session-files.test.ts:47` vérifie le comportement de listage des transcriptions de session pour l'indexation mémoire.

### Tests unitaires

- `src/plugins/memory-state.test.ts:80` vérifie les valeurs par défaut vides et `src/plugins/memory-state.test.ts:121` vérifie la précédence d'enregistrement de capacité.
- `src/plugins/memory-runtime.test.ts:193` charge uniquement le plugin d'emplacement mémoire configuré.
- `src/memory/root-memory-files.test.ts` couvre le comportement des fichiers mémoire racine.
- `packages/memory-host-sdk/src/host/backend-config.test.ts` couvre la résolution de config backend.
- `packages/memory-host-sdk/src/host/embedding-chunk-limits.test.ts:69` couvre les limites d'entrée du fournisseur.
- `packages/memory-host-sdk/src/host/sqlite-vec.test.ts` couvre le comportement de chargement sqlite-vec.

### Requêtes Gitcrawl

Requête:

`gitcrawl search issues "memory qmd embeddings sqlite-vec memorySearch" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats:

- A retourné le rapport ouvert `#71784 Bug: memory search live embedding fails ~20-40% with fetch failed / other side closed`.

Requête:

`gitcrawl search issues "memory_search MEMORY.md active-memory" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats:

- A retourné les rapports ouverts incluant `#40088` observateur de fichier obsolète, `#66339` contention de verrou SQLite QMD, `#77831` pollution par rêve, `#53550` lacunes de recherche mémoire de session, `#74586` classification de timeout Active Memory, et `#49524` blocages de session en direct.
- A également retourné la contention de verrou SQLite QMD, l'inadéquation docs/exécution, et les rapports d'index obsolète du observateur de fichier pertinents pour la qualité backend.

### Requêtes Discrawl

Requête:

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "memory qmd embeddings sqlite-vec memorySearch"`

Résultats:

- A retourné le dépannage Discord pour l'inadéquation fournisseur/modèle d'embedding, l'index vide et le répertoire mémoire manquant, et la discussion comparant la recherche hybride SQLite memory-core avec le comportement du backend QMD.

Requête:

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "memory_search MEMORY.md active-memory"`

Résultats:

- A retourné les discussions sur le découplage d'Active Memory des noms d'outils codés en dur, l'implémentation mémoire pré-réponse, le vidage automatique de mémoire avant compaction, et les recommandations de mémoire basées sur fichiers.
