---
title: "Outils de recherche Web - Note de maturité des contrats de plugin Web Provider"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche Web - Note de maturité des contrats de plugin Web Provider

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche Web` / `Registre des fournisseurs, contrats SDK et résolution d'exécution` dans l'inventaire de scorecard actuel du processus-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité des outils de recherche Web représentée par ces fonctionnalités de taxonomie :

- Registre des fournisseurs, contrats SDK et résolution d'exécution : Portée des preuves pour le registre des fournisseurs, les contrats SDK et la résolution d'exécution.

## Fonctionnalités

- webSearchProviders : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur de webSearchProviders pour les contrats de plugin Web Provider.
- registerWebSearchProvider : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur de registerWebSearchProvider pour les contrats de plugin Web Provider.
- webFetchProviders : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur de webFetchProviders pour les contrats de plugin Web Provider.
- registerWebFetchProvider : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur de registerWebFetchProvider pour les contrats de plugin Web Provider.
- chargement d'artefacts publics : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur du chargement d'artefacts publics pour les contrats de plugin Web Provider.
- résolution d'exécution : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur de la résolution d'exécution pour les contrats de plugin Web Provider.
- tests de contrat : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur des tests de contrat pour les contrats de plugin Web Provider.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`

La couverture est stable car les exports SDK publics, le contrat de propriété du manifeste, l'unicité du registre, la résolution du fournisseur d'exécution, l'artefact public de secours et le chemin d'outil d'agent lié tardivement sont couverts dans la documentation, la source, les suites de contrats et les vérifications d'exécution. Le score est limité par les preuves d'archive actives autour du routage de fournisseur personnalisé, des snapshots de démarrage, du comportement du cache d'artefacts publics et des incompatibilités de disponibilité des fournisseurs.

## Score de qualité

- Score : `Beta (78%)`

La qualité est Beta car la conception sépare clairement la propriété du manifeste, les artefacts publics, la découverte en mode configuration et les registres d'exécution, mais le chemin reste hautement stateful. La résolution du fournisseur traverse les exports de paquets, les manifestes de plugin, la réparation de configuration, les snapshots d'exécution et le contexte d'outil d'agent, ce qui crée des points fragiles lorsque les plugins sont manquants, obsolètes ou chargés via un chemin d'exécution différent.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour webSearchProviders, registerWebSearchProvider, webFetchProviders, registerWebFetchProvider, chargement d'artefacts publics, résolution d'exécution, tests de contrat.
- Signaux négatifs : la note archivée a précédé la notation de complétude du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-subpaths.md:157` documente le sous-chemin de contrat de configuration de recherche Web.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-subpaths.md:158` documente les assistants de contrat de recherche Web tels que les assistants de configuration et d'authentification scoped.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-subpaths.md:159` documente les assistants d'enregistrement et d'exécution de recherche Web.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-overview.md:107` documente `api.registerWebSearchProvider(...)`.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:667` documente `contracts.webSearchProviders`.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:12` documente la recherche Web gérée en utilisant le fournisseur configuré.

### Source

- `/Users/kevinlin/code/openclaw/package.json:1252` exporte `plugin-sdk/provider-web-search-config-contract`.
- `/Users/kevinlin/code/openclaw/package.json:1256` exporte `plugin-sdk/provider-web-search-contract`.
- `/Users/kevinlin/code/openclaw/package.json:1260` exporte `plugin-sdk/provider-web-search`.
- `/Users/kevinlin/code/openclaw/src/plugins/types.ts:2702` expose `registerWebSearchProvider`.
- `/Users/kevinlin/code/openclaw/src/plugins/registry.ts:1376` applique l'enregistrement unique du fournisseur de recherche Web.
- `/Users/kevinlin/code/openclaw/src/plugins/web-search-providers.runtime.ts:48` résout les fournisseurs de recherche Web du plugin.
- `/Users/kevinlin/code/openclaw/src/plugins/web-provider-public-artifacts.ts:105` résout les fournisseurs de recherche Web groupés à partir d'artefacts publics.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.ts:263` résout la définition d'outil gérée.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search.ts:89` lie tardivement le contexte d'exécution avant l'exécution.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/package.json:1654` définit la voie de plugin Docker kitchen-sink.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/kitchen-sink-plugin/assertions.mjs:423` valide les identifiants de fournisseur de recherche Web kitchen-sink.
- `/Users/kevinlin/code/openclaw/extensions/google/google.live.test.ts:121` exerce la recherche Web Gemini dans un chemin de fournisseur en direct.
- `/Users/kevinlin/code/openclaw/extensions/minimax/minimax.live.test.ts:38` exerce la recherche Web MiniMax dans un chemin de fournisseur en direct.
- `/Users/kevinlin/code/openclaw/extensions/moonshot/moonshot.live.test.ts:22` exerce la recherche Web Kimi dans un chemin de fournisseur en direct.
- `/Users/kevinlin/code/openclaw/extensions/ollama/ollama.live.test.ts:300` exerce le secours de recherche Web Ollama dans un chemin de fournisseur en direct.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/contracts/providers.contract.test.ts:17` exécute les suites de contrats de fournisseur de recherche Web sur les identifiants de fournisseur groupés.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/test-helpers/web-search-provider-contract.ts:41` charge les fournisseurs d'artefacts publics dans le chemin de contrat.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/test-helpers/provider-contract-suites.ts:130` affirme le contrat de fournisseur de recherche Web de base.
- `/Users/kevinlin/code/openclaw/src/plugins/web-search-providers.runtime.test.ts:462` couvre le chargement du fournisseur déclaré par manifeste en mode configuration.
- `/Users/kevinlin/code/openclaw/src/plugins/web-provider-public-artifacts.test.ts:47` vérifie les artefacts publics pour les fournisseurs Web groupés.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.test.ts:753` couvre le chargement du fournisseur d'exécution scoped.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.test.ts:950` couvre le comportement d'exécution de préférence-fournisseur-exécution.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a signalé la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29 810` threads, `11 181` threads ouverts et `18 594` clusters.

- `gitcrawl --json search prs -R openclaw/openclaw "provider-web-search"` a retourné des éléments de registre actif et de fournisseur-exécution incluant #77736 routage de fournisseur personnalisé, #86828 snapshots de démarrage, #76146 chemin CLI SecretRef, #63571 support de secours, #85158 fournisseur parallèle et #86440 fournisseur SerpApi.
- `gitcrawl --json search issues -R openclaw/openclaw "no provider available web_search"` a retourné #87347 aucun fournisseur disponible malgré Brave chargé, plus #80843 chaîne de secours et #85030 injection d'outil de sous-agent.
- `gitcrawl --json search prs -R openclaw/openclaw "web provider public artifacts"` a retourné principalement des PRs de métadonnées adjacentes et de chargement d'exécution, ce qui suggère que les régressions d'artefacts publics se manifestent par des requêtes de fournisseur/exécution plus larges plutôt que par des titres de problèmes directs.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a signalé l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1 487 061` messages, `25 819` canaux et zéro backlog d'intégration.

- `discrawl search --mode hybrid --limit 12 "provider-web-search resolvePluginWebSearchProviders public artifacts"` n'a retourné aucun hit hybride direct, donc les preuves Discord actuelles sont rares pour les noms d'assistants internes.
- Les passages d'archive focalisés antérieurs ont trouvé des conseils de fournisseur personnalisé autour de `api.registerWebSearchProvider(...)` et des commentaires d'examen concernant l'incompatibilité de registre d'exécution, la staleness du cache et le secours d'artefacts publics.
- `discrawl search --mode hybrid --limit 12 "web_fetch web_search config provider api key"` a trouvé des commentaires d'examen impliquant la configuration du fournisseur et le comportement de fusion de configuration hérité.
