---
title: "Outils de génération d'images/vidéos/musique - Note de maturité de la génération d'images"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Note de maturité de la génération d'images

## Résumé

Le runtime d'image est la partie la plus solide de cette surface. Il gère
la génération de texte en image, l'édition d'images de référence, les entrées multi-images, le format de sortie,
les indices d'arrière-plan, la normalisation de la taille et du rapport d'aspect, la validation des résultats du fournisseur, l'analyse base64/URL de données, la détection MIME et les métadonnées de tentative du fournisseur.

La couverture est Stable car la documentation, le code source du runtime, la mise en forme des ressources, les analyses en direct et
les scénarios d'assurance qualité couvrent les principaux chemins de génération et d'édition d'images. La qualité est Beta
car le runtime principal est cohérent, mais les identifiants d'édition itérative,
les métadonnées spécifiques au fournisseur et la compatibilité auth/fournisseur restent des risques opérationnels actifs.

## Portée de la catégorie

Inclus dans cette catégorie :

- texte-en-image : Couvre la génération de texte en image dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- édition d'images de référence : Couvre l'édition d'images de référence dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- indices de sortie : Couvre les indices de sortie dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- action=status : Couvre action=status dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- métadonnées de tentative du fournisseur : Couvre les métadonnées de tentative du fournisseur dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- OAuth OpenAI/Codex : Couvre OAuth OpenAI/Codex dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.
- Clé API OpenAI : Couvre la clé API OpenAI dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.
- Authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI : Couvre l'authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.
- diagnostics d'erreur du fournisseur : Couvre les diagnostics d'erreur du fournisseur dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.

## Fonctionnalités

- texte-en-image : Couvre la génération de texte en image dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- édition d'images de référence : Couvre l'édition d'images de référence dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- indices de sortie : Couvre les indices de sortie dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- action=status : Couvre action=status dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- métadonnées de tentative du fournisseur : Couvre les métadonnées de tentative du fournisseur dans le comportement du runtime de génération et d'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des demandes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images et comportement de génération et d'édition d'images associé.
- OAuth OpenAI/Codex : Couvre OAuth OpenAI/Codex dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.
- Clé API OpenAI : Couvre la clé API OpenAI dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.
- Authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI : Couvre l'authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.
- diagnostics d'erreur du fournisseur : Couvre les diagnostics d'erreur du fournisseur dans les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI et les fournisseurs d'images et comportements d'authentification associés.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : La documentation des images couvre les paramètres et le comportement du fournisseur ; la source implémente la validation, la normalisation, l'analyse et les métadonnées de tentative ; les tests d'assurance qualité et en direct couvrent l'utilisation de génération et d'aller-retour.
- Signaux négatifs : La couverture du runtime est plus forte pour les sorties standard réussies que pour la dérive des réponses spécifiques au fournisseur, les chaînes d'édition itérative et la persistance des métadonnées.
- Lacunes d'intégration : Ajouter un scénario de chaîne d'édition en direct qui préserve les identifiants d'image du fournisseur et valide une édition de suivi par rapport à l'image générée précédemment.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : La recherche d'images a retourné #85466 demandant les métadonnées d'utilisation du fournisseur de génération d'images et #79360 demandant les ID de génération d'images Responses pour les éditions itératives.
- Rapports Discrawl : La recherche Discord a trouvé des rapports d'opérateurs où la génération d'images a échoué car l'authentification du worker différait de la gestion des identifiants Codex/OpenAI ou l'authentification OpenRouter était manquante.
- Bonnes qualités : Le runtime valide que les fournisseurs retournent des images, capture les remplacements ignorés, normalise les ressources de sortie et signale les tentatives du fournisseur.
- Mauvaises qualités : La génération d'images repose toujours sur les formes de réponse spécifiques au fournisseur et le comportement d'authentification, et le runtime ne rend pas encore la provenance d'édition itérative de première classe entre les fournisseurs.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : la documentation archivée, la source, le test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la génération de texte en image, l'édition d'images de référence, les indices de sortie, action=status, les métadonnées de tentative du fournisseur, OAuth OpenAI/Codex, la clé API OpenAI, l'authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI, les diagnostics d'erreur du fournisseur.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les ID d'édition itérative et les métadonnées d'utilisation du fournisseur ne sont pas entièrement exposés.
- Les différences d'authentification et de point de terminaison du fournisseur peuvent dominer le succès visible par l'utilisateur même lorsque la mise en forme des demandes du runtime est correcte.
- L'analyse des réponses prend en charge les formes compatibles OpenAI courantes mais reste exposée à la dérive de schéma en amont.

# Génération d'images

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:11` décrit le comportement de génération/édition d'images et l'achèvement asynchrone.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:132` documente les paramètres de l'outil d'image.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:179` documente la suppression des paramètres non supportés et la normalisation.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:253` documente le support de l'édition d'images et les limites d'entrée.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:270` documente les détails de génération d'images OpenAI pour le modèle, l'arrière-plan, l'invite, le nombre, la taille, la qualité, le format et les références.
- `/Users/kevinlin/code/openclaw/cli/infer.md:184` documente l'utilisation CLI de génération et édition d'images.

### Source

- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.ts:45` liste les fournisseurs de génération d'images à l'exécution.
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.ts:52` construit les candidats du fournisseur d'images à partir du remplacement du modèle et de la configuration.
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.ts:94` applique la normalisation du délai d'attente et du remplacement avant l'invocation du fournisseur.
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.ts:128` valide les résultats d'image et enregistre les métadonnées de normalisation.
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.ts:146` enregistre les tentatives du fournisseur et lève les défaillances agrégées.
- `/Users/kevinlin/code/openclaw/src/image-generation/image-assets.ts:34` déduit le MIME d'image et l'extension de fichier.
- `/Users/kevinlin/code/openclaw/src/image-generation/image-assets.ts:81` analyse les URL de données d'image.
- `/Users/kevinlin/code/openclaw/src/image-generation/image-assets.ts:148` analyse les réponses d'image compatibles OpenAI.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/image-generation.runtime.live.test.ts:196` résout l'authentification, enregistre les plugins, appelle les fournisseurs de génération d'images en direct et vérifie les MIME et tampons retournés.
- `/Users/kevinlin/code/openclaw/qa/scenarios/media/native-image-generation.md:34` vérifie l'inventaire des outils, l'utilisation prévue des outils et le chemin du média enregistré.
- `/Users/kevinlin/code/openclaw/qa/scenarios/media/image-generation-roundtrip.md:36` vérifie la réattache d'image générée et la description.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.image-generation.test.ts:1` exécute les tests d'enregistrement d'outil de génération d'images partagés.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.test.ts:14` couvre le comportement du cycle de vie des médias générés utilisé par la génération d'images.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "image generation" --json`

Résultats :

- Retourné #85466 sur la capture des métadonnées d'utilisation du fournisseur de génération d'images, #79360 sur l'exposition des ID de génération d'images Responses pour les éditions itératives, #76690 sur la disponibilité de l'outil d'image OAuth Codex, #83857 sur le comportement de génération d'images xAI et #84627 sur le blocage SSRF/réseau privé xAI.

Requête : `gitcrawl search openclaw/openclaw --query "image generation edit reference images transparent background gpt-image" --json`

Résultats :

- Aucun résultat direct pour la phrase exacte, ce qui suggère que le contrat de paramètre d'édition documenté est moins représenté dans les titres de problèmes archivés que le comportement du fournisseur/authentification.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "image_generate"`

Résultats :

- Trouvé des rapports Discord pour les défaillances de jeton d'accès invalide, l'authentification manquante d'OpenRouter, l'inadéquation de la source d'identifiants Codex/OpenAI et le routage du point de terminaison de génération d'images.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "image generation edit reference images transparent background gpt-image"`

Résultats :

- Aucun résultat direct pour la phrase exacte.
