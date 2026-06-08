---
title: "Compréhension des médias et génération de médias - Note de maturité de l'outil de génération vidéo et du routage des fournisseurs"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de l'outil de génération vidéo et du routage des fournisseurs

## Résumé

La génération vidéo est une surface d'outil large mais en évolution rapide. Elle prend en charge la conversion texte-vidéo, image-vidéo, vidéo-vidéo, les indices de rôle de référence, la normalisation des capacités spécifiques au fournisseur, les tâches en arrière-plan et le secours d'URL du fournisseur. La qualité est à la limite bêta/alpha car le support du mode fournisseur et le comportement de livraison varient considérablement.

## Portée de la catégorie

Cette catégorie couvre `video_generate`, la résolution de mode, les capacités du fournisseur, les entrées d'image/vidéo/audio de référence, la validation des options du fournisseur, la persistance de la vidéo générée, les sorties URL uniquement, le cycle de vie des tâches en arrière-plan, les actions de statut/liste et l'enregistrement du fournisseur SDK. Elle ne note pas la compréhension vidéo.

## Fonctionnalités

- Invocation de l'outil de génération vidéo : Couvre l'invocation de l'outil de génération vidéo sur `video_generate`, la résolution de mode, les capacités du fournisseur, les entrées d'image/vidéo/audio de référence et le comportement connexe de l'outil de génération vidéo et du routage des fournisseurs.
- Sélection du mode et des capacités du fournisseur : Couvre la sélection du mode et des capacités du fournisseur sur `video_generate`, la résolution de mode, les capacités du fournisseur, les entrées d'image/vidéo/audio de référence et le comportement connexe de l'outil de génération vidéo et du routage des fournisseurs.
- Entrées d'image, vidéo et audio de référence : Couvre les entrées d'image, vidéo et audio de référence sur `video_generate`, la résolution de mode, les capacités du fournisseur, les entrées d'image/vidéo/audio de référence et le comportement connexe de l'outil de génération vidéo et du routage des fournisseurs.
- Validation des options du fournisseur : Couvre la validation des options du fournisseur sur `video_generate`, la résolution de mode, les capacités du fournisseur, les entrées d'image/vidéo/audio de référence et le comportement connexe de l'outil de génération vidéo et du routage des fournisseurs.
- Cycle de vie et statut de la tâche vidéo : Couvre le cycle de vie et le statut de la tâche vidéo sur `video_generate`, la résolution de mode, les capacités du fournisseur, les entrées d'image/vidéo/audio de référence et le comportement connexe de l'outil de génération vidéo et du routage des fournisseurs.
- Persistance et livraison de la vidéo générée : Couvre la persistance et la livraison de la vidéo générée sur `video_generate`, la résolution de mode, les capacités du fournisseur, les entrées d'image/vidéo/audio de référence et le comportement connexe de l'outil de génération vidéo et du routage des fournisseurs.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`
- Signaux positifs : La documentation publique énumère de nombreux fournisseurs, modes, limites d'entrée, indices de rôle, cycle de vie des tâches asynchrones, actions de statut/liste, inspection des tâches CLI et matrices de capacités du fournisseur. La source dispose d'un runtime dédié, d'une normalisation des capacités, d'un outil, d'un statut, d'une tâche en arrière-plan et d'exportations SDK.
- Signaux négatifs : Le support du mode spécifique au fournisseur est complexe et inégal ; les voies en direct ignorent intentionnellement certaines combinaisons mode/fournisseur.
- Lacunes d'intégration : La preuve de bout en bout récurrente pour chaque combinaison fournisseur/mode/client n'est pas présente, en particulier pour les contraintes vidéo-vidéo et URL distante uniquement.

## Score de qualité

- Score : `Bêta (70%)`
- Rapports Gitcrawl : #79535 signale l'échec silencieux de la génération vidéo OpenRouter ; #45655 signale les modèles de sortie vidéo Poe acceptés mais échouant à l'exécution ; #86034/#86279 montrent l'échec de la livraison de fin après la génération de médias réussie ; #87741 ajoute un secours lorsque la remise de médias générés se verrouille.
- Rapports Discrawl : La requête de livraison de génération de médias montre plusieurs rapports Discord/Molty où la génération ou la fin s'est réveillée correctement mais la livraison visible des pièces jointes a échoué. La requête discrawl spécifique à la vidéo n'a retourné aucun résultat ciblé supplémentaire.
- Bonnes qualités : La résolution de mode est explicite, les capacités du fournisseur sont lisibles par machine, les remplacements non pris en charge sont signalés, la persistance locale surdimensionnée peut revenir aux URL du fournisseur et les appels de tâches actives en double retournent le statut.
- Mauvaises qualités : La dérive des capacités du fournisseur est élevée, le support du modèle diffère selon le mode d'entrée et les contraintes d'URL/chemin, et le succès de l'utilisateur dépend toujours de la livraison asynchrone via l'outil de message.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'invocation de l'outil de génération vidéo, la sélection du mode et des capacités du fournisseur, les entrées d'image, vidéo et audio de référence, la validation des options du fournisseur, le cycle de vie et le statut de la tâche vidéo, la persistance et la livraison de la vidéo générée.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Vidéo-vidéo reste contraint par le fournisseur et le chemin d'entrée.
- La dérive des capacités du fournisseur hébergé crée un risque de non-concordance fréquent entre la documentation, la configuration et le comportement d'exécution.
- Les bogues de livraison peuvent faire que le succès du fournisseur ressemble à un échec de génération pour les utilisateurs.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md` documente `video_generate`, le comportement asynchrone, le cycle de vie des tâches, les fournisseurs, les modes, les indices de rôle, les capacités, les paramètres de l'outil, la normalisation et la sémantique de secours.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` résume la génération vidéo et le comportement des médias asynchrones.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/tools/video-generate-tool.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/video-generate-tool.actions.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/video-generate-background.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/runtime.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/capabilities.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/capability-overlays.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/duration-support.ts`
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/video-generation.ts`
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/video-generation-core.ts`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.video-generation.test.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/live-test-helpers.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/tools/video-generate-tool.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/video-generate-tool.status.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/video-generate-background.test.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/provider-registry.test.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/capabilities.test.ts`
- `/Users/kevinlin/code/openclaw/src/video-generation/capability-overlays.test.ts`

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "video generation OpenRouter silently fails" --json
```

Résultats :

- A retourné #79535 signalant l'échec silencieux de la génération vidéo OpenRouter et la génération musicale non expédiée à ce moment-là.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "video generation" --json
```

Résultats :

- A retourné #79535, #64607 affichage des médias en ligne, #45655 échec d'exécution du modèle de sortie image/vidéo Poe, #86279 échec de livraison après succès de génération et PRs adjacentes au mode/capacité du fournisseur.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "video generation OpenRouter silently fails" --limit 5
```

Résultats :

- N'a retourné aucun résultat Discord ciblé.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "media generation completion delivery" --limit 5
```

Résultats :

- A retourné plusieurs rapports de canal où la fin de génération de médias asynchrones a réussi mais la livraison visible des pièces jointes a échoué, y compris des exemples MP3/musique ; le même cycle de vie de livraison de génération de médias partagés s'applique à la vidéo.
