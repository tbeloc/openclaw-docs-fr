---
title: "Outils de recherche Web - Note de Maturité de la Fiabilité du Fournisseur et des Diagnostics"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche Web - Note de Maturité de la Fiabilité du Fournisseur et des Diagnostics

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche Web` / `Gestion des erreurs, quotas, mise en cache et diagnostics` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité des outils de recherche Web représentée par ces fonctionnalités de taxonomie :

- Gestion des erreurs, quotas, mise en cache et diagnostics : Portée des preuves pour la gestion des erreurs, quotas, mise en cache et diagnostics.

## Fonctionnalités

- Erreurs de quota : Couvre l'état des erreurs de quota, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Contrôles de cache : Couvre l'état des contrôles de cache, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Diagnostics du fournisseur : Couvre l'état des diagnostics du fournisseur, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Retry et fallback : Couvre l'état du retry et fallback, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Réparation par l'opérateur : Couvre l'état de la réparation par l'opérateur, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`

La couverture est Beta car les clés manquantes, les erreurs d'API du fournisseur, les réponses malformées, les clés de cache, les diagnostics limités, la gestion des délais d'expiration et le fallback du fournisseur ont des vérifications source et ciblées sur les chemins majeurs. Le score reste Beta car le comportement des quotas/limites de débit est incohérent selon le fournisseur, les chaînes de fallback sont toujours en cours de travail, et les preuves d'archive montrent les défaillances actuelles de délai d'expiration, d'authentification et d'absence de fournisseur.

## Score de qualité

- Score : `Beta (70%)`

La qualité est Beta car chaque fournisseur signale différentes défaillances d'authentification, de quota, de fraîcheur, de limite de débit et de forme de charge utile. OpenClaw enveloppe beaucoup de ces éléments dans les erreurs et diagnostics du fournisseur, mais la famille manque toujours d'un modèle d'échec uniforme face à l'opérateur pour l'épuisement des quotas, la sélection du fallback et la santé dégradée du fournisseur.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les erreurs de quota, les contrôles de cache, les diagnostics du fournisseur, le retry et fallback, la réparation par l'opérateur.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/reference/api-usage-costs.md:129` documente le coût du fournisseur web_search et le comportement du crédit Brave.
- `/Users/kevinlin/code/openclaw/docs/reference/api-usage-costs.md:155` documente le comportement du coût du fallback web_fetch Firecrawl/local.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:100` documente les exigences d'authentification et les différences de coût du fournisseur.
- `/Users/kevinlin/code/openclaw/docs/tools/brave-search.md:122` documente le dépannage de Brave.
- `/Users/kevinlin/code/openclaw/docs/tools/perplexity-search.md:198` documente le dépannage de Perplexity.
- `/Users/kevinlin/code/openclaw/docs/tools/tavily.md:127` documente le dépannage de Tavily.
- `/Users/kevinlin/code/openclaw/docs/tools/firecrawl.md:139` documente le dépannage de Firecrawl et les notes de sécurité.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search-provider-common.ts:53` définit les valeurs par défaut communes de comptage, cache et fraîcheur.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search-provider-common.ts:71` résout les valeurs d'authentification SecretRef et env.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search-provider-common.ts:127` enveloppe les erreurs d'API du fournisseur.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search-provider-common.ts:188` construit les aides de fraîcheur, date et cache.
- `/Users/kevinlin/code/openclaw/extensions/brave/src/brave-web-search-provider.runtime.ts:152` émet les charges utiles de clé manquante.
- `/Users/kevinlin/code/openclaw/extensions/brave/src/brave-web-search-provider.runtime.ts:336` gère les diagnostics d'exécution de Brave et le comportement du cache.
- `/Users/kevinlin/code/openclaw/extensions/perplexity/src/perplexity-web-search-provider.runtime.ts:312` gère les filtres non supportés, les clés manquantes et les erreurs du fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/tavily/src/tavily-client.ts:100` gère les réponses de recherche Tavily.
- `/Users/kevinlin/code/openclaw/extensions/firecrawl/src/firecrawl-client.ts:181` enveloppe les erreurs POST gardées de Firecrawl.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.ts:424` exécute le comportement de fallback du fournisseur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-search.md:43` couvre les attentes de runtime de succès et d'échec.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-fetch.md:43` couvre les attentes de runtime de succès et d'échec de fetch.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/openai-web-search-minimal/assertions.mjs:132` vérifie le comportement de rejet du raisonnement minimal natif d'OpenAI.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/brave/src/brave-web-search-provider.test.ts:309` couvre le JSON malformé et les cas ultérieurs couvrent les erreurs limitées, l'isolation du cache, la validation et les diagnostics.
- `/Users/kevinlin/code/openclaw/extensions/tavily/src/tavily-client.test.ts:44` couvre le comportement de défaillance de l'API Tavily.
- `/Users/kevinlin/code/openclaw/extensions/exa/src/exa-web-search-provider.test.ts:147` couvre les cas limites d'erreur et de réponse d'Exa.
- `/Users/kevinlin/code/openclaw/extensions/firecrawl/src/firecrawl-tools.test.ts:652` couvre le comportement de défaillance de Firecrawl.
- `/Users/kevinlin/code/openclaw/extensions/perplexity/src/perplexity-web-search-provider.test.ts:93` couvre les chemins non supportés et d'erreur de Perplexity.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.test.ts:614` couvre le comportement de fallback du runtime.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.provider-fallback.test.ts:104` couvre les réponses de fallback du fournisseur.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a signalé la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29 810` threads, `11 181` threads ouverts et `18 594` clusters.

- `gitcrawl --json search issues -R openclaw/openclaw "web_search"` a retourné #79384 maxResults codé en dur, #80843 chaîne de fallback, #87505 régression de délai d'expiration, #13615 limitation de débit, #87347 aucun fournisseur disponible et #79670 validation de limite de quota.
- `gitcrawl --json search issues -R openclaw/openclaw "Perplexity"` a retourné #84872, #85800, #80843, #87347 et d'autres demandes de défaillance ou de fonctionnalité spécifiques au fournisseur.
- `gitcrawl --json search prs -R openclaw/openclaw "web_search"` a retourné #86338 taille de contexte Perplexity, #86622 authentification Tavily, #63571 support de fallback, #77859 métadonnées de runtime, #76146 SecretRefs et #86965 surfacing de progression.
- `gitcrawl --json search issues -R openclaw/openclaw "SSRF web_fetch"` a retourné #87505 régression de délai d'expiration dans le chemin de fetch gardé.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a signalé l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1 487 061` messages, `25 819` canaux et zéro backlog d'embedding.

- `discrawl search --mode hybrid --limit 12 "Tavily Firecrawl Perplexity Brave SearXNG DuckDuckGo web_search"` a trouvé la sortie CLI du fournisseur Perplexity et un cas d'erreur de fournisseur 401.
- `discrawl search --mode hybrid --limit 12 "web_search no provider available Brave loaded web_fetch"` a trouvé des avertissements sans fournisseur et de liste blanche quand web_search n'est pas configuré.
- `discrawl search --mode hybrid --limit 12 "web_fetch web_search config provider api key"` a trouvé des discussions de configuration et d'examen impliquant les clés du fournisseur et les modes de défaillance.
