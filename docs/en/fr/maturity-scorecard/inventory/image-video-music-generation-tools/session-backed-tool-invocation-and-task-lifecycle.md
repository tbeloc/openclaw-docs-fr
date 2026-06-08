---
title: "Outils de génération d'images/vidéos/musique - Note de maturité du cycle de vie des tâches et de la livraison"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Note de maturité du cycle de vie des tâches et de la livraison

## Résumé

Le chemin d'invocation soutenu par session est implémenté comme un cycle de vie partagé des tâches médias.
Les outils médias peuvent démarrer la génération en arrière-plan, enregistrer les métadonnées des tâches, envoyer des signaux de maintien, supporter les vérifications de statut sans duplication, réveiller la conversation à la fin ou en cas d'échec, et utiliser un secours direct lorsque les médias générés n'ont pas été livrés via l'outil de message.

La couverture est Stable car la documentation, le code source et les tests couvrent le cycle de vie à travers la création, l'achèvement, l'échec et la livraison de secours des tâches. La qualité est Alpha car les rapports d'archive récents montrent que le succès de la génération de médias peut ressembler à un échec lorsque le chemin de livraison d'achèvement se brise ou lorsque les outils médias différés ne sont pas suffisamment visibles pour l'agent.

## Portée de la catégorie

Inclus dans cette catégorie :

- création de tâche en arrière-plan : Couvre la création de tâche en arrière-plan sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- statut/liste/affichage/annulation de tâche : Couvre le statut/liste/affichage/annulation de tâche sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- gardes contre les doublons : Couvre les gardes contre les doublons sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- maintien de la progression : Couvre le maintien de la progression sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- réveil à l'achèvement/échec : Couvre le réveil à l'achèvement/échec sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- secours en ligne sans session : Couvre le secours en ligne sans session sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- persistance des médias locaux : Couvre la persistance des médias locaux sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- inférence MIME/nom de fichier : Couvre l'inférence MIME/nom de fichier sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- secours URL hébergée : Couvre le secours URL hébergée sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- remise de l'outil de message : Couvre la remise de l'outil de message sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- secours idempotent en cas de médias manquants : Couvre le secours idempotent en cas de médias manquants sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- preuve de pièce jointe de canal : Couvre la preuve de pièce jointe de canal sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.

## Fonctionnalités

- création de tâche en arrière-plan : Couvre la création de tâche en arrière-plan sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- statut/liste/affichage/annulation de tâche : Couvre le statut/liste/affichage/annulation de tâche sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- gardes contre les doublons : Couvre les gardes contre les doublons sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- maintien de la progression : Couvre le maintien de la progression sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- réveil à l'achèvement/échec : Couvre le réveil à l'achèvement/échec sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- secours en ligne sans session : Couvre le secours en ligne sans session sur `image_generate`, `video_generate` et `music_generate` exposition d'outils, planification des tâches en arrière-plan et comportement du cycle de vie des tâches asynchrones associé.
- persistance des médias locaux : Couvre la persistance des médias locaux sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- inférence MIME/nom de fichier : Couvre l'inférence MIME/nom de fichier sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- secours URL hébergée : Couvre le secours URL hébergée sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- remise de l'outil de message : Couvre la remise de l'outil de message sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- secours idempotent en cas de médias manquants : Couvre le secours idempotent en cas de médias manquants sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.
- preuve de pièce jointe de canal : Couvre la preuve de pièce jointe de canal sur les objets artefacts image/audio/vidéo générés, inférence MIME et nom de fichier, chemins médias locaux, URL médias hébergées et comportement de livraison des médias générés associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : Le code source du cycle de vie partagé et les tests couvrent le démarrage des tâches, le statut des tâches actives, la livraison du réveil, la livraison d'échec et le secours direct des médias générés.
- Signaux négatifs : La couverture est concentrée dans le cycle de vie partagé et les assistants de livraison ; la preuve d'exécution spécifique au canal et les flux de travail utilisateur complets de bout en bout restent plus minces.
- Lacunes d'intégration : Ajouter un scénario de génération de médias au niveau du canal qui vérifie le registre des tâches, le réveil d'achèvement, la preuve de pièce jointe de l'outil de message et la non-duplication du secours dans un seul flux.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : Les recherches ont retourné #86279 sur le maintien du succès de la génération de médias malgré l'échec de la livraison, #86034 où la génération a réussi mais la livraison d'achèvement ressemblait à un échec, et #77265 où `agent --deliver` a retourné une URL de médias sans livrer les médias Telegram.
- Rapports Discrawl : La recherche Discord a trouvé des rapports d'achèvement de médias générés où la remise des médias s'est routée en arrière mais la livraison du canal était instable ou s'est repliée sur un nom de fichier/chemin généré.
- Bonnes qualités : Le cycle de vie est partagé entre l'image, la vidéo et la musique, avec des clés d'idempotence et une détection de médias manquants pour réduire les livraisons dupliquées ou perdues.
- Mauvaises qualités : L'opération visible par l'utilisateur dépend toujours du réveil multi-étapes, de la preuve de l'outil de message et de l'état de livraison du canal, donc un succès du fournisseur peut être obscurci par le comportement de livraison.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : les docs archivées, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la création de tâche en arrière-plan, le statut/liste/affichage/annulation de tâche, les gardes contre les doublons, le maintien de la progression, le réveil à l'achèvement/échec, le secours en ligne sans session, la persistance des médias locaux, l'inférence MIME/nom de fichier, le secours URL hébergée, la remise de l'outil de message, le secours idempotent en cas de médias manquants, la preuve de pièce jointe de canal.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Un fournisseur peut se terminer avec succès tandis que la livraison visible par l'utilisateur échoue toujours ou semble échouée.
- Les affordances des outils médias différés peuvent empêcher l'outil d'être invoqué en premier lieu.
- Le cycle de vie a plusieurs chemins de récupération, ce qui améliore la résilience mais augmente la complexité diagnostique de l'opérateur.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md:88` explique la génération de médias asynchrone par rapport à synchrone et la livraison de secours.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:11` décrit la génération d'images comme une tâche de fond asynchrone avec livraison à la fin.
- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md:57` documente le flux de génération vidéo asynchrone, l'ID de tâche, l'activation, l'outil de message, la livraison de secours et le stockage.
- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md:86` documente le cycle de vie et l'état de la tâche.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:15` documente la tâche de fond, le registre, l'activation, la livraison par outil de message et la livraison de secours.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:185` documente le comportement asynchrone, la prévention des doublons, l'état et la livraison de secours sans session.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.media-factory-plan.ts:167` contrôle les outils d'image, vidéo et musique optionnels.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.ts:103` crée des exécutions de tâches et enregistre les métadonnées de tâche de médias.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.ts:176` envoie des maintiens de progression.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.ts:200` complète ou échoue les exécutions de tâches.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.ts:254` construit les instructions de fin requises par l'outil de message.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.ts:350` planifie la fin de fond et la livraison d'activation.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-tool-actions-shared.ts:118` retourne l'état de la tâche active et les résultats de la garde contre les doublons.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.ts:770` envoie directement les médias générés lorsque l'agent d'annonce ne les livre pas.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/media/native-image-generation.md:4` définit un scénario de génération d'images natif avec inventaire d'outils et critères de succès de médias sauvegardés.
- `/Users/kevinlin/code/openclaw/qa/scenarios/media/image-generation-roundtrip.md:4` vérifie que les médias générés peuvent être réattachés et décrits.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.test.ts:14` maintient une tâche de médias générés active jusqu'à la fin de la livraison d'activation.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.test.ts:78` échoue la tâche lorsque la livraison de fin ne peut pas être confirmée.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.test.ts:129` couvre le comportement d'échec d'activation.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2247` évite la livraison de secours lorsque la preuve de l'outil de message inclut les médias générés.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2289` couvre les messages directs de fin de musique nécessitant l'outil de message.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2393` couvre les messages directs de fin d'image nécessitant l'outil de message.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2826` couvre la livraison directe après l'échec d'activation active.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "image_generate video_generate music_generate background task completion delivery" --json`

Résultats :

- Retourné #86279 sur le maintien du succès de la génération de médias lorsque la livraison de fin échoue.

Requête : `gitcrawl search openclaw/openclaw --query "generated media delivery message tool completion" --json`

Résultats :

- Retourné #86279, #87741 sur la livraison de secours après le verrouillage de la transmission de médias générés, #74041 sur l'acheminement des médias générés via la livraison d'assistant, et #86034 sur le succès de la génération ressemblant à l'échec de la livraison de fin.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "generated media completion delivery"`

Résultats :

- Trouvé une discussion de mainteneur sur les verrouillages de transmission de médias générés, la livraison de médias instable, la livraison de secours vers la sortie de nom de fichier/chemin et les correctifs de livraison de médias générés en doublon.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "music_generate"`

Résultats :

- Trouvé une discussion de mainteneur sur les outils de médias différés, y compris `music_generate`, ayant besoin d'une meilleure découvrabilité.
