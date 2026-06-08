---
title: "Outils de recherche web - Note de maturité des fournisseurs de recherche"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche web - Note de maturité des fournisseurs de recherche

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche web` / `Fournisseurs de recherche structurée groupés` dans l'inventaire de scorecard actuel de la version-3 du processus.

## Portée de la catégorie

Inclus dans cette catégorie :

- Fournisseurs soutenus par API : Couvre l'acheminement des fournisseurs soutenus par API, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Fournisseurs sans clé et auto-hébergés : Couvre l'acheminement des fournisseurs sans clé et auto-hébergés, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Comparaison des fournisseurs et détection automatique : Couvre l'acheminement de la comparaison des fournisseurs et de la détection automatique, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Filtres et extraction spécifiques aux fournisseurs : Couvre l'acheminement des filtres et de l'extraction spécifiques aux fournisseurs, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Normalisation des résultats : Couvre l'acheminement de la normalisation des résultats, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Recherche web native OpenAI : Couvre l'acheminement de la recherche web native OpenAI, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Recherche web native Codex : Couvre l'acheminement de la recherche web native Codex, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Ancrage Gemini : Couvre l'acheminement de l'ancrage Gemini, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Ancrage web Grok : Couvre l'acheminement de l'ancrage web Grok, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Recherche web Kimi : Couvre l'acheminement de la recherche web Kimi, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Citations natives du fournisseur : Couvre l'acheminement des citations natives du fournisseur, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Acheminement du modèle et du filtre : Couvre l'acheminement du modèle et du filtre, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- webSearchProviders : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour webSearchProviders dans les contrats de plugin de fournisseur web.
- registerWebSearchProvider : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour registerWebSearchProvider dans les contrats de plugin de fournisseur web.
- webFetchProviders : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour webFetchProviders dans les contrats de plugin de fournisseur web.
- registerWebFetchProvider : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour registerWebFetchProvider dans les contrats de plugin de fournisseur web.
- Chargement d'artefacts publics : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour le chargement d'artefacts publics dans les contrats de plugin de fournisseur web.
- Résolution à l'exécution : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour la résolution à l'exécution dans les contrats de plugin de fournisseur web.
- Tests de contrat : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour les tests de contrat dans les contrats de plugin de fournisseur web.

## Fonctionnalités

- Fournisseurs soutenus par API : Couvre l'acheminement des fournisseurs soutenus par API, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Fournisseurs sans clé et auto-hébergés : Couvre l'acheminement des fournisseurs sans clé et auto-hébergés, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Comparaison des fournisseurs et détection automatique : Couvre l'acheminement de la comparaison des fournisseurs et de la détection automatique, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Filtres et extraction spécifiques aux fournisseurs : Couvre l'acheminement des filtres et de l'extraction spécifiques aux fournisseurs, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Normalisation des résultats : Couvre l'acheminement de la normalisation des résultats, la mise en forme des requêtes, la diffusion en continu et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Recherche web native OpenAI : Couvre l'acheminement de la recherche web native OpenAI, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Recherche web native Codex : Couvre l'acheminement de la recherche web native Codex, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Ancrage Gemini : Couvre l'acheminement de l'ancrage Gemini, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Ancrage web Grok : Couvre l'acheminement de l'ancrage web Grok, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Recherche web Kimi : Couvre l'acheminement de la recherche web Kimi, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Citations natives du fournisseur : Couvre l'acheminement des citations natives du fournisseur, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Acheminement du modèle et du filtre : Couvre l'acheminement du modèle et du filtre, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- webSearchProviders : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour webSearchProviders dans les contrats de plugin de fournisseur web.
- registerWebSearchProvider : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour registerWebSearchProvider dans les contrats de plugin de fournisseur web.
- webFetchProviders : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour webFetchProviders dans les contrats de plugin de fournisseur web.
- registerWebFetchProvider : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour registerWebFetchProvider dans les contrats de plugin de fournisseur web.
- Chargement d'artefacts publics : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour le chargement d'artefacts publics dans les contrats de plugin de fournisseur web.
- Résolution à l'exécution : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour la résolution à l'exécution dans les contrats de plugin de fournisseur web.
- Tests de contrat : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour les tests de contrat dans les contrats de plugin de fournisseur web.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`

La couverture est Bêta car la documentation des fournisseurs et les sources existent pour Brave, Tavily, Exa, Firecrawl, Perplexity, DuckDuckGo et SearXNG, avec la gestion des authentifiants, la normalisation des résultats, les requêtes protégées, la mise en cache et les erreurs des fournisseurs représentées. Le score reste en dessous de Stable car la preuve est inégale entre les fournisseurs, plusieurs fournisseurs sont sans clé ou expérimentaux, et les preuves archivées montrent un travail continu spécifique aux fournisseurs en matière d'authentification, de secours et de qualité des résultats.

## Score de qualité

- Score : `Bêta (74%)`

La qualité est Bêta car la forme du fournisseur structuré est réutilisable, mais la qualité de mise en œuvre varie selon l'API en amont. La famille de fournisseurs mélange les API officielles, les points de terminaison auto-hébergés, le scraping sans clé, l'extraction de secours, les API de recherche de type modèle et la sémantique d'erreur spécifique au fournisseur, donc l'exécution doit normaliser de nombreux modes de défaillance divergents.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les fournisseurs soutenus par API, les fournisseurs sans clé et auto-hébergés, la comparaison des fournisseurs et la détection automatique, les filtres et l'extraction spécifiques aux fournisseurs, la normalisation des résultats, la recherche web native OpenAI, la recherche web native Codex, l'ancrage Gemini, l'ancrage web Grok, la recherche web Kimi, les citations natives du fournisseur, l'acheminement du modèle et du filtre, webSearchProviders, registerWebSearchProvider, webFetchProviders, registerWebFetchProvider, le chargement d'artefacts publics, la résolution à l'exécution, les tests de contrat.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version-3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/web.md:57` énumère les cartes de fournisseur pour les fournisseurs web_search groupés.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:100` compare les fournisseurs, les identifiants, le type de source, la fraîcheur et le coût.
- `/Users/kevinlin/code/openclaw/docs/tools/brave-search.md:9` documente Brave Search.
- `/Users/kevinlin/code/openclaw/docs/tools/tavily.md:11` documente la recherche et l'extraction Tavily.
- `/Users/kevinlin/code/openclaw/docs/tools/exa-search.md:10` documente Exa Search.
- `/Users/kevinlin/code/openclaw/docs/tools/firecrawl.md:11` documente Firecrawl Search et Fetch.
- `/Users/kevinlin/code/openclaw/docs/tools/perplexity-search.md:9` documente Perplexity Search.
- `/Users/kevinlin/code/openclaw/docs/tools/duckduckgo-search.md:10` documente DuckDuckGo Search comme expérimental et sans clé.
- `/Users/kevinlin/code/openclaw/docs/tools/searxng-search.md:10` documente SearXNG Search.

### Source

- `/Users/kevinlin/code/openclaw/extensions/brave/src/brave-web-search-provider.runtime.ts:88` résout les identifiants Brave et env.
- `/Users/kevinlin/code/openclaw/extensions/brave/src/brave-web-search-provider.runtime.ts:336` exécute la recherche Brave avec validation, mise en cache, diagnostics et gestion des erreurs.
- `/Users/kevinlin/code/openclaw/extensions/tavily/src/tavily-client.ts:68` émet des requêtes Tavily protégées.
- `/Users/kevinlin/code/openclaw/extensions/exa/src/exa-web-search-provider.runtime.ts:363` émet des requêtes de recherche Exa protégées.
- `/Users/kevinlin/code/openclaw/extensions/firecrawl/src/firecrawl-client.ts:335` implémente la recherche Firecrawl.
- `/Users/kevinlin/code/openclaw/extensions/perplexity/src/perplexity-web-search-provider.runtime.ts:200` implémente le chemin natif de l'API Perplexity Search.
- `/Users/kevinlin/code/openclaw/extensions/duckduckgo/src/ddg-client.ts:115` implémente la recherche DuckDuckGo, la mise en cache et l'utilisation de points de terminaison protégés.
- `/Users/kevinlin/code/openclaw/extensions/searxng/src/searxng-client.ts:105` valide l'URL de base SearXNG et le mode de point de terminaison.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/tavily-search.md:4` définit un scénario d'exécution de recherche Tavily.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/tavily-extract.md:4` définit un scénario d'exécution d'extraction Tavily.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/kitchen-sink-plugin/assertions.mjs:423` vérifie les identifiants de fournisseur web-search du plugin dans un chemin de plugin E2E.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/brave/src/brave-web-search-provider.test.ts:154` couvre le comportement de clé manquante Brave et les cas ultérieurs couvrent l'URL de base, le JSON mal formé, les erreurs limitées, l'isolation du cache et les diagnostics.
- `/Users/kevinlin/code/openclaw/extensions/tavily/src/tavily-tools.test.ts:74` couvre le comportement de l'outil Tavily, et `/Users/kevinlin/code/openclaw/extensions/tavily/src/tavily-client.test.ts:44` couvre les erreurs du client.
- `/Users/kevinlin/code/openclaw/extensions/exa/src/exa-web-search-provider.test.ts:24` couvre le comportement du fournisseur Exa et la gestion des erreurs.
- `/Users/kevinlin/code/openclaw/extensions/firecrawl/src/firecrawl-tools.test.ts:80` couvre les outils de recherche et de récupération Firecrawl.
- `/Users/kevinlin/code/openclaw/extensions/perplexity/src/perplexity-web-search-provider.test.ts:33` couvre le comportement du fournisseur Perplexity.
- `/Users/kevinlin/code/openclaw/extensions/duckduckgo/src/ddg-search-provider.test.ts:34` couvre le comportement du fournisseur DuckDuckGo.
- `/Users/kevinlin/code/openclaw/extensions/searxng/src/searxng-search-provider.test.ts:30` et `/Users/kevinlin/code/openclaw/extensions/searxng/src/searxng-client.test.ts:47` couvrent le comportement du fournisseur et du client SearXNG.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a signalé la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29,810` threads, `11,181` threads ouverts et `18,594` clusters.

- `gitcrawl --json search issues -R openclaw/openclaw "Perplexity"` a retourné #84872, #85800, #6792, #80843, #17925, #75562, #72527, #49949 et #87347.
- `gitcrawl --json search prs -R openclaw/openclaw "Perplexity"` a retourné #86338 taille du contexte de recherche, #85828 remplacement de modèle, #86622 correction d'authentification Tavily, #62126 intégration de recherche native, #85158 fournisseur parallèle et travail de fournisseur connexe.
- `gitcrawl --json search prs -R openclaw/openclaw "provider-web-search"` a retourné #85158 Parallel, #86440 SerpApi, #40311 Brave Goggles, #52207 fraîcheur SearXNG et Tavily, #86622 authentification Tavily et #63571 fallback.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a signalé l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1,487,061` messages, `25,819` canaux et zéro backlog d'intégration.

- `discrawl search --mode hybrid --limit 12 "Tavily Firecrawl Perplexity Brave SearXNG DuckDuckGo web_search"` a trouvé une discussion sur le choix du fournisseur, des listes publiques de fournisseurs disponibles, une sortie CLI du fournisseur Perplexity et des preuves d'échec utilisateur Perplexity 401.
- `discrawl search --mode hybrid --limit 12 "web_fetch web_search config provider api key"` a trouvé des conseils de configuration pour les clés API Brave et des notes indiquant que web_fetch ne récupère que les URL connues.
