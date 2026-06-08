---
title: "Compréhension des médias et génération de médias - Note de Maturité de Configuration des Médias"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de Maturité de Configuration des Médias

## Résumé

OpenClaw dispose d'une couche d'orchestration mature pour la compréhension et la génération de médias : la config `tools.media` est typée et validée par schéma, la découverte des capacités des fournisseurs est basée sur un manifeste, la compréhension des images/audio/vidéo utilise une résolution de modèle ordonnée partagée, la génération d'images asynchrone a un statut de tâche limité à la session, et les médias générés sont intégrés dans le pipeline de réponse via la gestion des médias de confiance et la livraison message-outil. Le plus grand risque restant n'est pas la mécanique locale, mais la clarté de l'itinéraire face aux opérateurs : les problèmes archivés et les fils Discord montrent une confusion récurrente ou des régressions autour des modèles de vision actifs contournant la compréhension des médias, l'authentification des images Codex/OpenAI, les échecs de livraison de complétion, et le modèle de médias choisi n'étant pas assez visible.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration des capacités médias : config `tools.media` image/audio/vidéo, entrées de modèles médias partagées et par capacité, résolution des entrées fournisseur/CLI, sélection des capacités basée sur l'authentification, ordre de secours, règles de portée, concurrence, comportement de saut du modèle actif, routage des images déchargées, disponibilité de la fabrique d'outils de génération d'images, statut/liste/garde contre les doublons des tâches de génération d'images, et livraison des médias générés dans le pipeline de réponse

## Fonctionnalités

- Configuration des capacités médias : config `tools.media` image/audio/vidéo, entrées de modèles médias partagées et par capacité, résolution des entrées fournisseur/CLI, sélection des capacités basée sur l'authentification, ordre de secours, règles de portée, concurrence, comportement de saut du modèle actif, routage des images déchargées, disponibilité de la fabrique d'outils de génération d'images, statut/liste/garde contre les doublons des tâches de génération d'images, et livraison des médias générés dans le pipeline de réponse

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - Les scénarios QA couvrent la livraison des pièces jointes de compréhension d'image, la disponibilité native de `image_generate` et la création d'artefacts, et l'aller-retour des images générées via le chemin de vision.
  - Les couches intégration/unité exercent la config/schéma `tools.media`, la résolution de modèles partagés et par capacité, le comportement de saut/secours du modèle actif, les entrées fournisseur CLI, les règles de portée, la concurrence, le statut des tâches de génération d'images, les gardes contre les doublons, et la gestion des réponses médias de confiance.
  - Des tests de balayage de fournisseur de génération d'images en direct existent pour les fournisseurs avec authentification configurée.
- Signaux négatifs :
  - La couverture de bout en bout la plus forte est concentrée sur la génération d'images et les flux de pièces jointes d'images ; le secours, la portée et la concurrence du fournisseur audio/vidéo `tools.media` sont couverts principalement en dessous du niveau complet du canal/runtime.
  - Le comportement de déchargement d'images du modèle actif a une couverture unitaire explicite et des scénarios QA à proximité, mais les régressions archivées montrent que ce chemin est assez subtil pour que la couverture d'intégration WebChat/canal plus large soit toujours justifiée.
- Lacunes d'intégration :
  - Ajouter des scénarios runtime multi-canaux qui affirment la portée/concurrence `tools.media` et l'ordre de secours du fournisseur depuis les médias entrants jusqu'à la réponse finale.
  - Ajouter un scénario de statut/config visible par l'opérateur qui prouve le rapport du fournisseur/modèle de compréhension des médias choisi pour les chemins de vision active ignorée et de médias déchargés.

## Score de Qualité

- Score : `Beta (77%)`
- Rapports Gitcrawl :
  - `gitcrawl search openclaw/openclaw --query "media understanding" --json` a retourné des signaux de routage actif et de robustesse incluant #87168 (la compréhension des médias `image` peut contourner l'itinéraire d'image Codex configuré), #87185 (router la compréhension des médias Codex uniquement via Codex limité), #62924 (exposer le modèle réellement choisi), #81525 (validation de la capacité du modèle de vision déclaré), #77760 (le bundle peut manquer `sharp`), #74644 (fournisseurs STT sans authentification/locaux), et #72031 (mode d'authentification AWS SDK Bedrock).
  - `gitcrawl search openclaw/openclaw --query "image_generate" --json` a retourné des signaux d'orchestration/authentification de génération actifs incluant #86034 (la génération réussit mais la livraison de complétion ressemble à un échec), #86279 (conserver le succès de la génération de médias en cas d'échec de livraison), #85797 (chemin d'image OAuth Codex OpenAI), #75683 (les sorties générées sont accessibles depuis l'espace de travail sandbox), #86075 (rupture de génération d'images de sous-agent), #83857 (xAI infer vs incompatibilité REPL), et #84627 (comportement SSRF/réseau privé).
  - `gitcrawl search openclaw/openclaw --query "tools.media" --json` a retourné les problèmes/PR associés sur la livraison d'assistant de médias générés (#74041), le routage de réveil de complétion (#74402), la confiance des médias locaux (#47523), les octets max de sandbox codés en dur (#40880), et les échecs de prétraitement d'images (#73424).
  - Des recherches plus spécifiques (`"tools.media image audio provider fallback concurrency scope"`, `"image_generate background task status message tool fallback generated media"`, et `"image understanding active model supports vision skip offload media://inbound"`) n'ont retourné aucun résultat gitcrawl, donc les requêtes de fonctionnalités larges ci-dessus sont la preuve d'archive utile.
- Rapports Discrawl :
  - `/Users/kevinlin/.local/bin/discrawl search "media understanding" --limit 5` a d'abord heurté le verrou sandbox et a été réexécuté avec escalade. Le résultat pertinent principal résumé #82524/#85501 : une régression de téléchargement d'image WebChat a déplacé les sessions actives texte uniquement avec `agents.defaults.imageModel` loin des `MediaPaths` / compréhension des médias en attente vers les remplacements d'images en ligne, cassant les fournisseurs qui s'attendaient à la forme de requête de compréhension des médias ; #85501 a restauré le routage des médias déchargés et a déplacé la résolution imageModel sans fournisseur vers la compréhension des médias.
  - La même requête a également surfacé des notes de test de version avec un signal permanent "Media understanding timeout: no provider request captured" et un rapport utilisateur selon lequel le secours de l'alias du plugin `media-understanding-core` manquait dans la source v5.12-beta.1.
  - `/Users/kevinlin/.local/bin/discrawl search "image_generate" --limit 5` a d'abord heurté le verrou sandbox et a été réexécuté avec escalade. Les résultats pertinents principaux incluaient la rupture du sous-agent MiniMax Token Plan autour de `image_generate`, la confusion d'authentification de génération d'images OpenAI où le chat fonctionnait mais l'outil obtenait `HTTP 401 Unauthorized`, un utilisateur local uniquement confus par les erreurs d'authentification OpenRouter, et les notes du responsable sur le comportement de timeout/par défaut de la génération d'images.
  - `/Users/kevinlin/.local/bin/discrawl search "tools.media" --limit 5` a d'abord heurté le verrou sandbox et a été réexécuté avec escalade. Les résultats pertinents principaux incluaient la complexité du pipeline médias/tts envoyé par agent touchant Codex et les gestionnaires embedded-subscribe, une question du responsable sur l'échec du réveil de complétion `media-generate-background-shared`, et des notes selon lesquelles la complétion des médias asynchrones devrait rester médiatisée par agent.
  - Des recherches discrawl plus spécifiques (`"tools.media image audio provider fallback concurrency scope"`, `"image_generate background task status message tool fallback generated media"`, et `"image understanding active model supports vision skip offload media://inbound"`) ont été réexécutées après l'échec du verrou sandbox et n'ont produit aucun résultat imprimé.
- Bonnes qualités :
  - Le modèle de config est explicite et typé : `tools.media.models`, configs `image`/`audio`/`vidéo` par capacité, timeout, prompt, max octets/caractères, politique de pièces jointes, portée, langue, et concurrence sont des champs de première classe.
  - La résolution du fournisseur est en couches et prévisible : les entrées par capacité remplacent les entrées partagées, les entrées partagées sont filtrées par capacités, `agents.defaults.imageModel` peut définir les primaires/secours de compréhension d'images, le secours du modèle actif est vérifié par capacité, et la découverte du fournisseur basée sur l'authentification/par défaut existe.
  - Le chemin de saut du modèle actif évite la compréhension d'image dupliquée lorsque le modèle de réponse actif supporte déjà la vision, tandis que les images déchargées sont analysées, assainies et fusionnées dans l'ordre des images de prompt.
  - La génération asynchrone a un texte de statut/liste/garde contre les doublons visible par l'opérateur et un registre de tâches limité à la session, ce qui aide à prévenir les appels `image_generate` répétés pendant qu'une tâche s'exécute.
  - Le pipeline de réponse a une posture de sécurité forte pour les médias locaux générés : les chemins `MEDIA:` locaux ne sont acceptés que des outils de confiance core ou des noms d'outils exécutés localement exacts, la provenance MCP et les collisions de variantes de casse sont bloquées, et les médias orphelins sont vidés avant la fin du cycle de vie.
- Mauvaises qualités :
  - La limite entre la vision du modèle actif en ligne, la compréhension des médias déchargés, et le `agents.defaults.imageModel` explicite reste facile à casser et difficile à raisonner pour les opérateurs.
  - Le rapport du modèle/fournisseur n'est toujours pas suffisamment visible dans le corps entrant visible par l'utilisateur, basé sur les demandes archivées d'exposer le modèle de compréhension des médias réellement choisi.
  - Les étiquettes d'authentification et de runtime restent confuses pour la génération d'images, en particulier OAuth Codex/OpenAI par rapport aux chemins de clé API directe et à l'héritage des outils de sous-agent/arrière-plan.
  - Les échecs de livraison de complétion peuvent toujours être perçus comme des échecs de génération, même si le code récent essaie de séparer le succès de la génération de l'échec de la livraison.
- Exclu de la qualité :
  - La profondeur de couverture unitaire, intégration, e2e, en direct et QA ne sont pas utilisées comme entrées de notation de Qualité.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la Configuration des capacités médias.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une page de docs concise ou une surface de statut qui explique quand les médias d'image entrants sont gérés par la vision du modèle actif par rapport à `tools.media.image` par rapport à `agents.defaults.imageModel`.
- Afficher le fournisseur/modèle de compréhension des médias choisi dans le statut visible par l'opérateur ou le contexte entrant pour réduire le rapport de modèle deviné.
- Continuer à fermer les problèmes d'authentification/routage basés sur l'archive autour de la génération d'images Codex/OpenAI, des fournisseurs de médias locaux/sans authentification, et des modes d'authentification spécifiques au fournisseur.
- Élargir la preuve runtime pour le comportement de portée/concurrence/secours audio/vidéo `tools.media` sur les chemins de canal réels.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md:11` décrit les médias OpenClaw comme des images/vidéos/musiques générées, la compréhension des médias entrants et la synthèse vocale ; les lignes 43-45 lient la compréhension des médias aux images/audio/vidéos entrants avec des fournisseurs compatibles avec la vision et des plugins dédiés ; les lignes 81-85 clarifient que les modèles de réponse multimodaux actifs peuvent également comprendre les médias entrants.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md:97` documente le suivi asynchrone des tâches de génération de médias et le comportement de réveil à la fin, y compris la livraison message-outil et le repli direct idempotent pour les médias manquants.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:11` documente la génération d'images de chat comme création asynchrone de tâches en arrière-plan ; les lignes 20-24 décrivent la disponibilité des outils en fonction de la configuration du fournisseur/authentification ; les lignes 211-224 définissent l'ordre de sélection et le comportement de repli ; les lignes 247-249 documentent l'inspection du fournisseur à l'exécution via `action:"list"`.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:183` documente les instantanés de propriété des capacités des plugins, y compris les contrats de compréhension des médias et de génération d'images ; les lignes 699-704 définissent les métadonnées de compréhension des médias pour les modèles par défaut, la priorité de repli d'authentification automatique et le support natif des documents.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness.md:229` documente la sémantique du préfixe `agents.defaults.imageModel` pour la compréhension des images, y compris le routage limité du serveur d'application Codex ; les lignes 543-553 documentent l'ordre dynamique des délais d'expiration des outils pour `image_generate` et la compréhension des médias `image`.

## Source

- `/Users/kevinlin/code/openclaw/src/config/types.tools.ts:82` définit `MediaUnderstandingConfig` avec les contrôles `enabled`, `scope`, limites, invite, délai d'expiration, langue, pièces jointes, liste de modèles et écho de transcription ; les lignes 141-145 définissent les `tools.media.models` partagés et la concurrence `tools.media.concurrency`.
- `/Users/kevinlin/code/openclaw/src/config/zod-schema.core.ts:964` valide `tools.media` avec un schéma strict par capacité et la ligne 982 valide la concurrence d'entier positif.
- `/Users/kevinlin/code/openclaw/src/media-understanding/resolve.ts:80` résout les entrées par capacité avant les entrées partagées et filtre les entrées partagées par les capacités du fournisseur ; les lignes 119-125 appliquent la concurrence configurée avec une valeur par défaut ; les lignes 127-145 utilisent le repli du modèle actif uniquement lorsqu'il est activé et qu'aucun modèle n'est configuré.
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.ts:648` résout les entrées primaires/replis `agents.defaults.imageModel` en entrées fournisseur/modèle ; les lignes 713-753 définissent l'ordre des entrées automatiques via imageModel, modèle actif, fournisseurs soutenus par authentification, audio local et CLI Antigravity ; les lignes 1018-1061 ignorent la compréhension des images lorsque le modèle actif principal supporte nativement la vision ; les lignes 1065-1091 reviennent aux entrées explicites/automatiques ou enregistrent les décisions ignorées.
- `/Users/kevinlin/code/openclaw/src/media-understanding/apply.ts:522` normalise les pièces jointes entrantes, construit le registre/cache du fournisseur, exécute les capacités image/audio/vidéo sous concurrence configurée, enregistre les décisions, formate les sorties corps/transcription et revient à l'extraction de fichiers.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.media-factory-plan.ts:102` expose les usines d'outils image/PDF lorsqu'un répertoire d'agent existe et que soit le modèle actif a la vision, soit une configuration image/PDF explicite existe, soit une capacité de compréhension des médias soutenus par authentification existe ; les lignes 167-258 appliquent la politique d'outils globale et par exécution avant d'activer les usines de génération/PDF.
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-tool.actions.ts:65` implémente `image_generate action:"list"` et les lignes 86-132 implémentent les actions de statut/garde contre les doublons.
- `/Users/kevinlin/code/openclaw/src/agents/media-generation-task-status-shared.ts:302` liste les tâches de médias actives limitées à la session ; les lignes 387-461 formatent le statut, la garde contre les doublons et le contexte d'invite de tâche active.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run/images.ts:55` analyse défensivement les références de vérification de réclamation `media://inbound` ; les lignes 116-162 préservent l'ordre des images en ligne/déchargées ; les lignes 553-560 ignorent le chargement d'images pour les modèles sans entrée d'image ; les lignes 623-644 assainissent et retournent les images d'invite.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-subscribe.tools.ts:275` restreint les noms d'outils de médias locaux de confiance ; les lignes 340-407 rejettent la provenance externe/MCP et les collisions de noms bruts pour les médias locaux tout en autorisant les URL distantes.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/media/image-understanding-attachment.md:12` vérifie qu'une image jointe atteint le modèle d'agent et est décrite ; les lignes 72-92 affirment que le fournisseur simulé a vu au moins une entrée d'image pour l'invite du scénario.
- `/Users/kevinlin/code/openclaw/qa/scenarios/media/native-image-generation.md:12` vérifie que `image_generate` apparaît lorsqu'il est configuré et retourne un artefact de médias enregistré ; les lignes 44-51 affirment l'inventaire des outils et les lignes 72-88 affirment l'appel d'outil planifié et le chemin généré.
- `/Users/kevinlin/code/openclaw/qa/scenarios/media/image-generation-roundtrip.md:12` vérifie que les médias générés sont réattachés au tour suivant et décrits via le chemin de vision ; les lignes 93-99 affirment à la fois l'appel `image_generate` et l'entrée d'image ultérieure.
- `/Users/kevinlin/code/openclaw/test/image-generation.runtime.live.test.ts:196` exécute un balayage de fournisseur en direct pour les variantes de génération d'images configurées avec authentification utilisable et rapporte les cas de fournisseur tentés/ignorés/échoués.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/suite-runtime-agent-media.test.ts:106` vérifie que la configuration de génération d'images QA préserve les plugins de transport requis et attend la disponibilité de la passerelle/transport.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/media-understanding/resolve.test.ts:11` couvre la résolution des entrées de modèles partagées/par capacité et le comportement de repli du modèle actif.
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.vision-skip.test.ts:266` vérifie que `agents.defaults.imageModel` l'emporte sur le modèle actif pour la résolution d'image automatique ; les lignes 286-369 vérifient les références de modèle primaire/repli sans fournisseur et le comportement de repli primaire échoué ; les lignes 374-427 vérifient le repli du modèle actif MiniMax vers l'image par défaut du fournisseur.
- `/Users/kevinlin/code/openclaw/src/media-understanding/apply.test.ts:420` couvre la transcription audio limitée en chat direct ; les lignes 464-488 couvrent les règles de portée spécifiques au canal ; les lignes 988-1027 couvrent la compréhension d'image CLI et l'exécution du repli Antigravity.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.media-factory-plan.test.ts:174` couvre l'ignorance des usines indisponibles ; les lignes 250-273 couvrent l'activation par configuration de modèle explicite ; les lignes 345-400 couvrent la politique d'autorisation/refus ; les lignes 460-496 couvrent la disponibilité de l'usine de fournisseur soutenus par authentification.
- `/Users/kevinlin/code/openclaw/src/agents/image-generation-task-status.test.ts:53` couvre la détection de tâches de génération d'images soutenus par session active ; les lignes 216-227 couvrent la garde contre les doublons de succès récent ; les lignes 500-504 couvrent le contexte d'invite de tâche active.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-subscribe.handlers.tools.media.test.ts:208` couvre la mise en file d'attente des médias locaux de confiance lorsque la sortie détaillée est désactivée ; les lignes 246-295 couvrent le rejet des médias locaux non fiables/MCP tout en autorisant les URL distantes ; les lignes 461-490 couvrent l'évitement des doublons de médias locaux dans la sortie détaillée simple.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-subscribe.handlers.lifecycle.test.ts:424` couvre le vidage des médias d'outils orphelins comme réponse de bloc médias uniquement avant la fin du cycle de vie.

## Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "tools.media image audio provider fallback concurrency scope" --json
```

Résultats :

- Aucun résultat.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "image_generate background task status message tool fallback generated media" --json
```

Résultats :

- Aucun résultat.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "image understanding active model supports vision skip offload media://inbound" --json
```

Résultats :

- Aucun résultat.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "media understanding" --json
```

Résultats :

- Problèmes/PR actifs retournés pour la qualité de routage/authentification/empaquetage/visibilité de la compréhension des médias, y compris #87168, #87185, #62924, #81525, #77760, #74644 et #72031.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "image_generate" --json
```

Résultats :

- Problèmes/PR actifs retournés pour la livraison de génération asynchrone, l'authentification, l'accessibilité du bac à sable, le comportement des sous-agents, l'enregistrement des fournisseurs et la gestion du réseau privé, y compris #86034, #86279, #85797, #75683, #86075, #86493, #83857 et #84627.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "tools.media" --json
```

Résultats :

- Problèmes/PR retournés pour la livraison de médias générés, la confiance des médias, le délai d'expiration/configuration, le prétraitement et le routage de la compréhension des médias, y compris #74041, #86279, #87219, #40880, #82870, #74402, #47523, #73424, #73817 et #75683.

## Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "tools.media image audio provider fallback concurrency scope" --limit 5
```

Résultats :

- L'exécution initiale du bac à sable a échoué avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
- Réexécution de la commande exacte avec escalade ; aucun résultat imprimé.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "image_generate background task status message tool fallback generated media" --limit 5
```

Résultats :

- L'exécution initiale du bac à sable a échoué avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
- Réexécution de la commande exacte avec escalade ; aucun résultat imprimé.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "image understanding active model supports vision skip offload media://inbound" --limit 5
```

Résultats :

- L'exécution initiale du bac à sable a échoué avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
- Réexécution de la commande exacte avec escalade ; aucun résultat imprimé.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "media understanding" --limit 5
```

Résultats :

- L'exécution initiale du bac à sable a échoué avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
- Réexécution de la commande exacte avec escalade. Le résultat le plus pertinent a résumé #82524/#85501 et décrit une régression de téléchargement WebChat où `agents.defaults.imageModel` a déplacé les téléchargements d'images en texte uniquement loin de la compréhension des médias intermédiaires vers le routage de remplacement de modèle en ligne ; #85501 a restauré `routeImageOffloadsAsMediaPaths` et a déplacé la résolution imageModel sans fournisseur dans la compréhension des médias.
- D'autres résultats pertinents ont mentionné les tests de version avec un signal permanent « Media understanding timeout: no provider request captured » et le repli d'alias de plugin manquant pour `media-understanding-core`.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "image_generate" --limit 5
```

Résultats :

- L'exécution initiale du bac à sable a échoué avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
- Réexécution de la commande exacte avec escalade. Les résultats les plus pertinents incluaient la rupture de génération d'images du sous-agent du plan de jetons MiniMax #86075, la confusion d'authentification de génération d'images OpenAI où le modèle de chat fonctionnait mais `image_generate` recevait `HTTP 401 Unauthorized`, un utilisateur local uniquement frappant une erreur d'authentification OpenRouter, et des notes de mainteneur selon lesquelles les délais d'expiration par défaut de génération d'images non-OpenAI avaient été trop bas.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "tools.media" --limit 5
```

Résultats :

- L'exécution initiale du bac à sable a échoué avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
- Réexécution de la commande exacte avec escalade. Les résultats les plus pertinents incluaient la complexité du pipeline TTS/médias envoyés par agent à travers les gestionnaires Codex et embedded-subscribe, une question de mainteneur sur l'échec du réveil à la fin de `media-generate-background-shared`, et des notes de mainteneur selon lesquelles les complétions de médias asynchrones doivent rester médiées par agent.
