---
title: "Chemin du fournisseur OpenAI / Codex - Note de maturité des entrées d'image et multimodales"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenAI / Codex - Note de maturité des entrées d'image et multimodales

## Résumé

La couverture des entrées d'image et multimodales d'OpenAI est solide. La documentation décrit `image_generate`, les routes de clé API OpenAI et OAuth Codex, la gestion des arrière-plans transparents, les limites d'édition/référence, le comportement de secours, les déploiements d'images Azure et la politique des points de terminaison privés. La source dispose d'un fournisseur d'images OpenAI dédié qui choisit entre l'API Images directe et le backend Codex Responses et applique les limites de sortie/taille/sécurité. La qualité reste Beta car il existe un problème d'archive ouvert où l'outil générique de compréhension des médias `image` peut contourner l'itinéraire d'image Codex configuré via les remplacements de modèle et la sélection automatique directe d'OpenAI.

## Portée de la catégorie

Inclus dans cette catégorie :

- Édition de génération d'images : couvre l'édition de génération d'images sur la génération et l'édition d'images OpenAI, le backend d'images OAuth Codex, le routage des arrière-plans transparents, les points de terminaison d'images OpenAI Azure/privés, et le comportement connexe de génération et d'entrée multimodale d'images.
- Entrée multimodale : couvre l'entrée multimodale sur la génération et l'édition d'images OpenAI, le backend d'images OAuth Codex, le routage des arrière-plans transparents, les points de terminaison d'images OpenAI Azure/privés, et le comportement connexe de génération et d'entrée multimodale d'images.

## Fonctionnalités

- Édition de génération d'images : couvre l'édition de génération d'images sur la génération et l'édition d'images OpenAI, le backend d'images OAuth Codex, le routage des arrière-plans transparents, les points de terminaison d'images OpenAI Azure/privés, et le comportement connexe de génération et d'entrée multimodale d'images.
- Entrée multimodale : couvre l'entrée multimodale sur la génération et l'édition d'images OpenAI, le backend d'images OAuth Codex, le routage des arrière-plans transparents, les points de terminaison d'images OpenAI Azure/privés, et le comportement connexe de génération et d'entrée multimodale d'images.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : la documentation et la source couvrent les itinéraires d'image majeurs ; les tests unitaires couvrent le comportement du fournisseur et le flux de tâches ; Docker E2E couvre l'authentification des images OpenAI ; l'outillage multimédia en direct peut exécuter des tests d'images spécifiques au fournisseur.
- Signaux négatifs : l'itinéraire d'image OAuth Codex et les variantes de points de terminaison Azure/privés ne sont pas tous représentés par des tests d'intégration toujours actifs.
- Lacunes d'intégration : la preuve de version actuelle devrait inclure le comportement direct d'OpenAI, OAuth Codex, arrière-plan transparent, édition/référence d'image, et le comportement configuré du point de terminaison privé/Azure.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : #87168 enregistre que l'outil de compréhension des médias `image` peut contourner l'itinéraire d'image Codex configuré via les remplacements de modèle et la sélection automatique directe d'OpenAI.
- Rapports Discrawl : les requêtes spécifiques aux images n'ont retourné aucune ligne directe. Ceci a été traité comme neutre après la réussite de la fraîcheur.
- Bonnes qualités : le fournisseur distingue explicitement la configuration de clé API directe de l'utilisation du profil OAuth Codex, applique les limites de taille/événement, normalise les demandes d'arrière-plan transparent, et bloque les points de terminaison privés par défaut.
- Mauvaises qualités : plusieurs surfaces compatibles avec les images partagent des références de modèle similaires, ce qui rend la propriété de l'itinéraire facile à contourner accidentellement.
- Exclu de la qualité : la couverture des tests unitaires, Docker et en direct des images a été utilisée uniquement pour la couverture.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'édition de génération d'images et l'entrée multimodale.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'itinéraire d'image OAuth Codex devrait être plus difficile à contourner lorsqu'une installation s'attend à une génération d'images soutenue par abonnement.
- L'outil générique de compréhension des médias `image` et l'itinéraire `image_generate` ont besoin d'une séparation plus claire visible par l'opérateur.
- Le comportement des points de terminaison Azure/personnalisés a besoin de plus de preuves de version publique.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente la génération d'images OpenAI, le backend d'images OAuth Codex, le reroutage du modèle d'arrière-plan transparent, le comportement du point de terminaison de génération d'images Azure, et l'opt-in du point de terminaison privé.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md` documente `image_generate`, l'ordre de sélection du fournisseur, les fournisseurs pris en charge, les paramètres d'édition/référence, les indices de sortie, la gestion des arrière-plans, le comportement de secours, et le comportement de réveil des tâches.
- `/Users/kevinlin/code/openclaw/docs/nodes/images.md` documente les capacités des nœuds d'image.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openai/image-generation-provider.ts` implémente l'API Images OpenAI directe, le backend d'images Codex Responses, la normalisation de sortie/taille, le reroutage d'arrière-plan transparent, le routage du déploiement Azure, les vérifications de points de terminaison privés, l'analyse des événements SSE, et les limites de résultats.
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.ts` résout les candidats de génération d'images, les délais d'expiration, la normalisation des remplacements, le secours du fournisseur, et la signalisation des défaillances.
- `/Users/kevinlin/code/openclaw/src/image-generation/openai-compatible-image-provider.ts` implémente la construction de demandes de génération/édition d'images réutilisables compatibles avec OpenAI et le comportement HTTP conscient de SSRF.
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-tool.ts` expose l'outil `image_generate`, l'enregistrement des tâches, l'intégration du magasin multimédia, et le comportement de réveil de session.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run/images.ts` détecte et fusionne les pièces jointes d'image, les références d'image d'invite, et les médias déchargés dans les tours d'agent.
- `/Users/kevinlin/code/openclaw/extensions/openai/openai-codex-provider.ts` restaure la capacité d'entrée d'image pour les lignes de modèle Codex modernes connues.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/openai-image-auth-docker.sh` exécute un E2E Docker d'authentification de génération d'images OpenAI simulé.
- `/Users/kevinlin/code/openclaw/scripts/test-live-media.ts` inclut la suite multimédia en direct d'image et le filtrage du fournisseur pour la génération d'images OpenAI.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-codex-harness.live.test.ts` inclut les sondes d'image et de chat-image du harnais Codex optionnel.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/openai/image-generation-provider.test.ts` couvre le comportement du fournisseur d'images OpenAI.
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.test.ts` couvre la sélection du fournisseur, le secours, le délai d'expiration, et le comportement des résultats d'image.
- `/Users/kevinlin/code/openclaw/src/image-generation/openai-compatible-image-provider.test.ts` couvre la construction de demandes de génération/édition d'images compatibles avec OpenAI, l'authentification, le délai d'expiration, et l'analyse des réponses.
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-tool.test.ts` couvre le comportement de génération d'images côté outil.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run/images.test.ts` couvre la gestion des pièces jointes/références d'image.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "image media-understanding tool bypass configured Codex image route"`

Résultats :

- A retourné #87168, "l'outil de compréhension des médias `image` peut contourner l'itinéraire d'image Codex configuré via les remplacements de modèle et la sélection automatique directe d'OpenAI".

Requête : `gitcrawl --json search issues -R openclaw/openclaw "gpt-image transparent background OpenAI Codex OAuth image"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après les vérifications de fraîcheur réussies.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "openai image generation codex oauth gpt-image transparent background"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après les vérifications de fraîcheur réussies.

Requête : `discrawl search --limit 10 "gpt-image transparent background OpenAI Codex OAuth image"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après les vérifications de fraîcheur réussies.
