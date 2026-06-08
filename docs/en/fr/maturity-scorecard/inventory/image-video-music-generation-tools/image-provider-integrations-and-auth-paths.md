---
title: "Outils de génération d'images/vidéos/musique - Fournisseurs d'images et note de maturité d'authentification"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Fournisseurs d'images et note de maturité d'authentification

## Résumé

L'étendue de l'intégration des fournisseurs d'images est solide : OpenAI, OpenAI Codex, OpenRouter, xAI, fal, LiteLLM, DeepInfra, Google, MiniMax et d'autres plugins groupés exposent la génération d'images via le contrat de fournisseur partagé. L'authentification du fournisseur dispose également de chemins de résolution de profil/env partagés et de chemins d'enregistrement de fournisseur.

La couverture est Beta car plusieurs fournisseurs sont enregistrés, documentés et balayés en direct, mais le comportement spécifique au fournisseur et les combinaisons d'authentification restent larges. La qualité est Alpha car les rapports d'archives GitHub et Discord actifs incluent des défaillances d'outils d'images OAuth Codex, des défaillances d'authentification manquante OpenRouter, le blocage de réseau privé/SSRF xAI et les défaillances de routage de plan de jetons MiniMax.

## Portée de la catégorie

Cette catégorie couvre les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OpenAI/Codex OAuth, OpenRouter, xAI, fal, LiteLLM, DeepInfra, Google, MiniMax, résolution de profil/env d'authentification, compatibilité des demandes de fournisseur et mise en forme des réponses de fournisseur.

## Fonctionnalités

- OpenAI/Codex OAuth : Couvre OpenAI/Codex OAuth sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OpenAI/Codex OAuth, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification connexes.
- OpenAI avec clé API : Couvre OpenAI avec clé API sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OpenAI/Codex OAuth, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification connexes.
- Authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI : Couvre l'authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OpenAI/Codex OAuth, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification connexes.
- Diagnostics d'erreur du fournisseur : Couvre les diagnostics d'erreur du fournisseur sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OpenAI/Codex OAuth, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification connexes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation du fournisseur énumère le support d'images, la source enregistre plusieurs fournisseurs groupés, la découverte d'authentification partagée alimente la sélection du fournisseur et les tests en direct balayent les fournisseurs d'images configurés.
- Signaux négatifs : La couverture n'est pas également profonde pour le chemin d'authentification de chaque fournisseur, la capacité d'édition, la règle de réseau privé et la forme de réponse spécifique au point de terminaison.
- Lacunes d'intégration : Ajouter une matrice d'authentification d'image par fournisseur qui vérifie OpenAI Codex OAuth, API-key OpenAI, OpenRouter, xAI, fal et LiteLLM avec une assertion de génération et une assertion de capacité d'édition où supportées.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : Les recherches d'images ont retourné #76690 sur la génération d'images OAuth Codex échouant car l'outil n'a pas été trouvé, #84627 sur `image_generate` xAI étant bloqué par le comportement SSRF/réseau privé, #86493 et #86605 autour de l'enregistrement du fournisseur StepFun et #83030 sur le support ReCraft OpenRouter.
- Rapports Discrawl : La recherche Discord a trouvé des rapports de jetons d'accès d'image invalides, authentification OpenRouter manquante et incompatibilité de source de credentials du worker d'image.
- Bonnes qualités : L'enregistrement du fournisseur est explicite et l'exécution partagée enregistre les tentatives du fournisseur et les remplacements ignorés.
- Mauvaises qualités : L'authentification du fournisseur et le comportement du point de terminaison restent la plus grande source de défaillances d'images visibles par l'utilisateur, en particulier lorsque les workers utilisent un chemin de credentials différent du modèle interactif.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour OpenAI/Codex OAuth, API-key OpenAI, authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI, diagnostics d'erreur du fournisseur.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le comportement OpenAI/Codex OAuth n'est pas systématiquement transparent pour l'utilisateur.
- Les défaillances OpenRouter et xAI peuvent ressembler à des défaillances génériques de génération d'images plutôt qu'à des défaillances d'authentification ou de politique réseau spécifiques au fournisseur.
- La dérive de capacité spécifique au fournisseur peut faire qu'un modèle configuré semble disponible avant d'échouer au moment de la demande.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:76` énumère les routes de fournisseur d'images et les fournisseurs supportés.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:122` documente les capacités du fournisseur.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:327` documente les modèles d'images OpenRouter.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:360` documente la génération d'images xAI et les contrôles natifs non supportés.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md:55` résume la couverture de capacité du fournisseur de médias.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openai/index.ts:47` enregistre le fournisseur OpenAI, le fournisseur Codex, la génération d'images, la parole/médias et la génération vidéo.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts:194` enregistre la compréhension des médias OpenRouter, l'image, la musique, la vidéo, le catalogue vidéo et la parole.
- `/Users/kevinlin/code/openclaw/extensions/fal/index.ts:13` enregistre le fournisseur fal, l'image, la musique et la génération vidéo.
- `/Users/kevinlin/code/openclaw/extensions/xai/index.ts:234` enregistre la recherche web xAI, la compréhension des médias, la vidéo, l'image, la parole et la STT.
- `/Users/kevinlin/code/openclaw/extensions/litellm/index.ts:95` enregistre le catalogue LiteLLM et la génération d'images.
- `/Users/kevinlin/code/openclaw/src/media-generation/runtime-shared.ts:100` résout le profil d'authentification et l'état du fournisseur soutenu par l'environnement.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/image-generation.runtime.live.test.ts:196` balaye en direct les fournisseurs d'images configurés et valide la sortie MIME et buffer.
- `/Users/kevinlin/code/openclaw/scripts/test-live-media.ts:31` inclut les listes de fournisseurs de suite d'images en direct.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts:54` applique les déclarations de capacité du fournisseur groupé.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.image-generation.test.ts:1` exerce l'enregistrement d'outils d'image via le support de test partagé.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "image generation provider openai openrouter xai litellm fal" --json`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl search openclaw/openclaw --query "image generation" --json`

Résultats :

- A retourné #76690, #84627, #86493, #86605, #83030, #83857 et d'autres rapports liés au fournisseur d'images ou à l'authentification.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "image_generate"`

Résultats :

- A trouvé un jeton d'accès invalide, authentification OpenRouter manquante, rapports d'incompatibilité de source de credentials Codex/OpenAI et routage de génération d'images de plan de jetons MiniMax.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "image generation provider openai openrouter xai litellm fal"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase de liste de fournisseurs exacte.
