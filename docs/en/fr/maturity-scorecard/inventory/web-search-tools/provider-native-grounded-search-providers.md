---
title: "Outils de recherche Web - Note de maturité de la recherche ancrée native du fournisseur"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche Web - Note de maturité de la recherche ancrée native du fournisseur

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche Web` / `Fournisseurs de recherche ancrée native du fournisseur` dans l'inventaire de scorecard de la version actuelle du processus-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité des outils de recherche Web représentée par ces fonctionnalités de taxonomie :

- Fournisseurs de recherche ancrée native du fournisseur : Portée des preuves pour les fournisseurs de recherche ancrée native du fournisseur.

## Fonctionnalités

- web_search natif OpenAI : Couvre le routage web_search natif OpenAI, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- web_search natif Codex : Couvre le routage web_search natif Codex, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Ancrage Gemini : Couvre le routage d'ancrage Gemini, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Ancrage Web Grok : Couvre le routage d'ancrage Web Grok, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Recherche Web Kimi : Couvre le routage de recherche Web Kimi, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Citations natives du fournisseur : Couvre le routage des citations natives du fournisseur, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Routage du modèle et du filtre : Couvre le routage du modèle et du filtre, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`

La couverture est Beta car la documentation, la source et les vérifications ciblées existent pour la recherche native OpenAI/Codex, l'ancrage Gemini, la recherche Grok X, Kimi, MiniMax et Ollama. Le score est limité par la variance de l'API spécifique au fournisseur, la dépendance aux identifiants en direct, les demandes de fonctionnalités natives du fournisseur toujours ouvertes et les PR actives pour les métadonnées, la plage horaire, le contournement SSRF et le comportement spécifique au fournisseur.

## Score de qualité

- Score : `Beta (72%)`

La qualité est Beta car la recherche ancrée native dépend de la sémantique du fournisseur de modèle au lieu d'un contrat web_search uniforme. Les implémentations doivent traduire les filtres, les citations, les métadonnées, les identifiants, le secours local/cloud, l'authentification OAuth ou par clé API et les capacités du fournisseur non prises en charge dans un résultat d'outil OpenClaw commun.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : la documentation archivée, la source, le test, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la recherche Web native OpenAI, la recherche Web native Codex, l'ancrage Gemini, l'ancrage Web Grok, la recherche Web Kimi, les citations natives du fournisseur et le routage du modèle et du filtre.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version-3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/tools/web.md:117` documente la recherche Web native OpenAI.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:123` documente la recherche Web native Codex.
- `/Users/kevinlin/code/openclaw/docs/tools/gemini-search.md:10` documente la recherche ancrée Gemini.
- `/Users/kevinlin/code/openclaw/docs/tools/grok-search.md:9` documente la recherche Web et X Grok.
- `/Users/kevinlin/code/openclaw/docs/tools/kimi-search.md:9` documente la recherche Web Kimi.
- `/Users/kevinlin/code/openclaw/docs/tools/minimax-search.md:10` documente la recherche MiniMax.
- `/Users/kevinlin/code/openclaw/docs/tools/ollama-search.md:11` documente la recherche Web Ollama.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openai/native-web-search.ts:16` détermine l'éligibilité de la recherche native OpenAI.
- `/Users/kevinlin/code/openclaw/extensions/openai/native-web-search.ts:57` injecte l'outil web_search natif OpenAI et le comportement de raisonnement minimal.
- `/Users/kevinlin/code/openclaw/src/agents/codex-native-web-search-core.ts:79` active la recherche Web native Codex.
- `/Users/kevinlin/code/openclaw/extensions/google/src/gemini-web-search-provider.runtime.ts:179` implémente les demandes d'ancrage Gemini gardées et la gestion de la redirection des citations.
- `/Users/kevinlin/code/openclaw/extensions/xai/src/web-search-provider.runtime.ts:211` implémente le secours OAuth/profil/API Grok.
- `/Users/kevinlin/code/openclaw/extensions/moonshot/src/kimi-web-search-provider.runtime.ts:214` implémente la gestion des appels d'outil de recherche Web Kimi.
- `/Users/kevinlin/code/openclaw/extensions/minimax/src/minimax-web-search-provider.runtime.ts:120` implémente la recherche gardée MiniMax.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/web-search-provider.ts:129` implémente les tentatives de secours local/cloud Ollama.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/models/openai-native-web-search-live.md:4` définit le scénario en direct de recherche Web native OpenAI.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/openai-web-search-minimal/scenario.sh:57` démarre la passerelle et affirme l'injection web_search native OpenAI.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/openai-web-search-minimal/assertions.mjs:96` valide le comportement de la charge utile de recherche Web native.
- `/Users/kevinlin/code/openclaw/extensions/google/google.live.test.ts:121` exerce la recherche Web Gemini.
- `/Users/kevinlin/code/openclaw/extensions/minimax/minimax.live.test.ts:38` exerce la recherche MiniMax.
- `/Users/kevinlin/code/openclaw/extensions/moonshot/moonshot.live.test.ts:22` exerce la recherche Kimi.
- `/Users/kevinlin/code/openclaw/extensions/ollama/ollama.live.test.ts:300` exerce le secours de recherche Web Ollama.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/codex-native-web-search.test.ts:26` couvre l'activation de la recherche Web native Codex et la mise en forme de la charge utile.
- `/Users/kevinlin/code/openclaw/test/scripts/openai-web-search-minimal-assertions.test.ts:15` couvre les assistants d'assertion de recherche Web native OpenAI.
- `/Users/kevinlin/code/openclaw/extensions/google/web-search-provider.test.ts:87` couvre le comportement de la recherche Gemini.
- `/Users/kevinlin/code/openclaw/extensions/xai/web-search.test.ts:175` couvre le comportement de la recherche Grok et X.
- `/Users/kevinlin/code/openclaw/extensions/moonshot/src/kimi-web-search-provider.test.ts:55` couvre le comportement du fournisseur Kimi.
- `/Users/kevinlin/code/openclaw/extensions/minimax/src/minimax-web-search-provider.test.ts:44` couvre le comportement du fournisseur MiniMax.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/web-search-provider.test.ts:152` couvre le comportement du fournisseur Ollama.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a signalé la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29 810` threads, `11 181` threads ouverts et `18 594` clusters.

- `gitcrawl --json search issues -R openclaw/openclaw "Gemini web search"` a retourné #17925 demande native Anthropic, #79876, #49949 travail natif Gemini/OpenAI, #78573 Copilot, #72527, #85937, #79670, #51593 et #85030.
- `gitcrawl --json search prs -R openclaw/openclaw "Gemini web search"` a retourné #85317 contournement SSRF Gemini, #85195 correction d'horodatage Gemini, #86828 snapshots de démarrage, #55485 politique SSRF, #76146 SecretRefs et #77859 métadonnées d'exécution.
- `gitcrawl --json search prs -R openclaw/openclaw "provider-web-search"` a retourné #78574 recherche Web native Copilot, #62126 intégration native Codex, #85148 préservation des métadonnées Codex, #85317 correction Gemini et #85195 correction d'horodatage Gemini.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a signalé l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1 487 061` messages, `25 819` canaux et zéro arriéré d'intégration.

- `discrawl search --mode hybrid --limit 12 "Gemini Grok Kimi MiniMax Ollama web_search"` a trouvé une discussion publique listant ces fournisseurs dans le sélecteur de configuration et la sortie d'état du fournisseur Perplexity/Gemini/Ollama.
- `discrawl search --mode hybrid --limit 12 "Tavily Firecrawl Perplexity Brave SearXNG DuckDuckGo web_search"` a également surfacé les conseils X/Grok selon lesquels le secours web_search prend en charge plusieurs fournisseurs, tandis que les données X spécifiques à xAI nécessitent x_search.
