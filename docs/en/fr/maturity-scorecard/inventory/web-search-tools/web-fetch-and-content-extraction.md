---
title: "Outils de recherche web - Note de maturité Web Fetch et Content Extraction"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche web - Note de maturité Web Fetch et Content Extraction

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche web` / `Web Fetch et Content Extraction` dans l'inventaire de scorecard actuel process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité des outils de recherche web représentée par ces fonctionnalités de taxonomie :

- Web Fetch et Content Extraction : Portée des preuves pour Web Fetch et Content Extraction.

## Fonctionnalités

- URL fetch : Couvre l'invocation de l'outil URL fetch, l'exécution hôte, la politique sandbox et la gestion des artefacts pour Web Fetch et Content Extraction.
- HTML extraction : Couvre l'invocation de l'outil HTML extraction, l'exécution hôte, la politique sandbox et la gestion des artefacts pour Web Fetch et Content Extraction.
- PDF/text extraction : Couvre l'invocation de l'outil PDF/text extraction, l'exécution hôte, la politique sandbox et la gestion des artefacts pour Web Fetch et Content Extraction.
- Safe truncation : Couvre l'invocation de l'outil Safe truncation, l'exécution hôte, la politique sandbox et la gestion des artefacts pour Web Fetch et Content Extraction.
- Content citation handoff : Couvre l'invocation de l'outil Content citation handoff, l'exécution hôte, la politique sandbox et la gestion des artefacts pour Web Fetch et Content Extraction.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`

La couverture est Stable car web_fetch dispose de docs dédiées, de source runtime, de chemins de fallback de fournisseur, de scénarios runtime, de limites sandbox, de vérifications axées sur SSRF, de comportement d'extraction et de couverture d'archive. Le score est limité par les demandes de fonctionnalités actives concernant l'opt-in de réseau privé, la fidélité du corps d'extraction, la surfacing de progression et le comportement de fallback de fournisseur tiers.

## Score de qualité

- Score : `Stable (80%)`

La qualité est Stable car web_fetch a un contrat étroit et compréhensible : récupérer une URL fournie, appliquer la politique de sécurité réseau, extraire le contenu lisible, envelopper le contenu non fiable et utiliser optionnellement le fallback de fournisseur. Le score de qualité se situe à l'extrémité inférieure de Stable car la fidélité d'extraction, le fallback de fournisseur et la politique de réseau privé changent encore.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : les docs archivées, la source, le test, Gitcrawl et les preuves Discrawl couvrent la portée de taxonomie pour URL fetch, HTML extraction, PDF/text extraction, Safe truncation, Content citation handoff.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:11` décrit web_fetch comme un simple HTTP GET plus l'extraction de lisibilité sans exécution JavaScript.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:19` documente l'activation par défaut.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:40` documente le comportement de fetch, extract, fallback, cache et redirect.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:60` documente la configuration de la politique timeout, redirect, response-size, readability, proxy et SSRF.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:88` documente la configuration du fallback Firecrawl.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:135` documente le comportement runtime et sandbox.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:243` documente que la sélection du fournisseur web_fetch est séparée de web_search.

### Source

- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.ts:107` résout les IDs de fournisseur web_fetch.
- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.ts:163` résout les définitions de fournisseur et le choix de sandbox.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ts:136` limite les options de réponse max et redirect.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ts:313` normalise les payloads de fallback de fournisseur.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ts:399` construit les clés de cache et les opt-ins SSRF.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ts:418` valide les URLs et utilise le fetch gardé.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ts:498` extrait le contenu et applique le fallback de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/firecrawl/src/firecrawl-client.ts:518` implémente le scrape Firecrawl.
- `/Users/kevinlin/code/openclaw/extensions/tavily/src/tavily-client.ts:207` implémente l'extract Tavily.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-fetch.md:4` définit le scénario runtime web_fetch.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/tavily-extract.md:4` définit la couverture d'extract Tavily.
- `/Users/kevinlin/code/openclaw/src/gateway/server-startup-web-fetch-bind.test.ts:78` vérifie le démarrage avec la configuration web_fetch sans credential.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.test.ts:108` couvre la gestion de SecretRef.
- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.test.ts:168` couvre les credentials env et fallback.
- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.test.ts:275` couvre les limites de sandbox du fournisseur bundled.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.provider-fallback.test.ts:40` couvre le comportement de fallback de fournisseur.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.cf-markdown.test.ts:51` couvre le comportement markdown/extraction.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ssrf.test.ts:103` couvre le comportement SSRF depuis le chemin de l'outil.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch-visibility.test.ts:5` couvre le comportement de visibilité et de transcript.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a rapporté la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29,810` threads, `11,181` threads ouverts et `18,594` clusters.

- `gitcrawl --json search issues -R openclaw/openclaw "web_fetch"` a retourné #39604 opt-in réseau privé, #82685 extraction corps complet, #45049, #76260 parité SSRF, #41993 IPv6 special-use, #48486 sanitizer de visibilité, #87505 timeout et #77826 runtime supprimant les outils web de plugin.
- `gitcrawl --json search prs -R openclaw/openclaw "web_fetch"` a retourné #67421 politique SSRF par agent, #86965 progression, #39630 allowPrivateNetwork, #75218 fournisseur Tavily fetch, #87758 durcissement d'injection, #55485 politique SSRF, #77859 métadonnées runtime et #85993 expansion de capacité navigateur.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a rapporté l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1,487,061` messages, `25,819` channels et zéro backlog d'embedding.

- `discrawl search --mode hybrid --limit 12 "web_fetch ssrf private internal redirect injection"` a trouvé des conseils de sécurité expliquant que web_fetch fait un simple HTTP GET, n'exécute pas JavaScript, bloque les hôtes privés/internes, revérifie les redirects et traite le contenu récupéré comme non fiable.
- `discrawl search --mode hybrid --limit 12 "web_fetch web_search config provider api key"` a trouvé des conseils visibles par l'utilisateur que web_fetch peut récupérer les URLs fournies sans clé de recherche, mais ne peut pas découvrir les URLs.
