---
title: "Outils de génération d'images/vidéos/musique - Note de maturité du routage et de la découverte des médias"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Note de maturité du routage et de la découverte des médias

## Résumé

La configuration et la découverte sont bien représentées dans la documentation et le code source. Les images, vidéos et musique ont chacune des clés d'agent par défaut explicites, une analyse des références fournisseur/modèle, des secours ordonnés, une découverte automatique basée sur l'authentification, un listage de catalogue et des portes de disponibilité des outils.

La couverture est Stable car l'implémentation dispose d'assistants d'exécution partagés, de catalogues de fournisseurs, de documentation et de tests de contrat pour le chemin de découverte. La qualité est Beta car les abstractions de référence de modèle et de découverte de fournisseur sont cohérentes, mais les preuves d'archives Discord montrent que la découverte d'outils médias différés confond toujours les agents et les opérateurs.

## Portée de la catégorie

Inclus dans cette catégorie :

- configuration du modèle média par défaut : Couvre la configuration du modèle média par défaut sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.
- références de modèle par appel et secours : Couvre les références de modèle par appel et les secours sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.
- découverte d'outils basée sur l'authentification : Couvre la découverte d'outils basée sur l'authentification sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.
- inspection du fournisseur action=list : Couvre l'inspection du fournisseur action=list sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.

## Fonctionnalités

- configuration du modèle média par défaut : Couvre la configuration du modèle média par défaut sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.
- références de modèle par appel et secours : Couvre les références de modèle par appel et les secours sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.
- découverte d'outils basée sur l'authentification : Couvre la découverte d'outils basée sur l'authentification sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.
- inspection du fournisseur action=list : Couvre l'inspection du fournisseur action=list sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, les références fournisseur/modèle et le comportement de routage de modèle et de découverte d'outils associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La documentation couvre les trois clés de modèle par défaut, les références fournisseur/modèle, l'ordre de sélection du fournisseur, les secours, la détection automatique et les actions de liste ; le code source centralise la résolution des candidats et la disponibilité de la fabrique d'outils.
- Signaux négatifs : La couverture de découverte est meilleure pour les fournisseurs enregistrés que pour les explications d'échec face aux opérateurs lorsqu'aucun fournisseur n'est disponible ou qu'un outil différé est masqué du schéma d'outils actif.
- Lacunes d'intégration : Ajouter un scénario qui commence sans outil média visible, déclenche la découverte du fournisseur via la recherche d'outils différés et confirme que l'agent expose la bonne capacité d'image, vidéo ou musique.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : Les recherches larges de médias ont révélé des problèmes autour des métadonnées du fournisseur, de la disponibilité de la génération d'images Codex OAuth, du comportement vidéo/musique OpenRouter et de la réutilisation d'outils médias différés.
- Rapports Discrawl : La recherche Discord a trouvé une discussion du responsable sur les outils médias différés où le modèle a vu des aperçus de source mais pas les noms d'outils individuels `music_generate`, `video_generate` et `image_generate`.
- Bonnes qualités : Le résolveur de référence de modèle partagé et le catalogue de fournisseurs réduisent le comportement de sélection de fournisseur dupliqué sur les images, vidéos et musique.
- Mauvaises qualités : La même flexibilité rend difficile le diagnostic des mauvaises configurations, des outils différés masqués et des incompatibilités d'authentification du fournisseur du côté de l'opérateur.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : les preuves archivées de documentation, code source, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration du modèle média par défaut, les références de modèle par appel et les secours, la découverte d'outils basée sur l'authentification, l'inspection du fournisseur action=list.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La découverte d'outils médias différés n'est pas suffisamment explicite lorsqu'un schéma d'outils direct est absent.
- La découverte automatique du fournisseur dépend de signaux d'authentification et d'instantanés de fournisseur qui peuvent être opaques pour les utilisateurs.
- Les lignes du catalogue de fournisseurs sont utiles pour les experts mais n'expliquent pas toujours pourquoi une demande spécifique ignorera un fournisseur.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md:390` documente les valeurs par défaut `imageGenerationModel` et `videoGenerationModel` dans les exemples de configuration d'agent.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md:426` documente `imageGenerationModel`, la détection automatique et les valeurs d'authentification typiques.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md:431` documente `musicGenerationModel`.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md:436` documente `videoGenerationModel`.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:193` documente la configuration du fournisseur principal/secours d'image et les références de modèle.
- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md:290` documente l'ordre de sélection du modèle vidéo et la configuration.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:223` documente la sélection du modèle musique, les secours et la détection automatique.

### Code source

- `/Users/kevinlin/code/openclaw/src/media-generation/model-ref.ts:8` analyse les références fournisseur/modèle.
- `/Users/kevinlin/code/openclaw/src/media-generation/runtime-shared.ts:100` résout les fournisseurs par défaut actuels et les profils d'authentification.
- `/Users/kevinlin/code/openclaw/src/media-generation/runtime-shared.ts:138` construit les références de secours automatique basées sur l'authentification.
- `/Users/kevinlin/code/openclaw/src/media-generation/runtime-shared.ts:182` résout les candidats de modèle ordonnés à partir des remplacements, des valeurs par défaut principales, des secours et de la détection automatique.
- `/Users/kevinlin/code/openclaw/src/media-generation/catalog.ts:36` synthétise les entrées de catalogue média statiques.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.media-factory-plan.ts:167` planifie les outils médias optionnels en fonction de la politique, de la configuration, des instantanés et de la disponibilité des capacités.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-tool-actions-shared.ts:41` retourne les résultats de la liste des fournisseurs avec l'état configuré, l'authentification, les modes, les capacités et les lignes du catalogue.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts:54` vérifie que les fournisseurs vidéo et musique fournis ont des déclarations de capacité.
- `/Users/kevinlin/code/openclaw/scripts/test-live-media.ts:31` définit les suites de fournisseurs médias en direct pour les images, la musique et la vidéo.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.image-generation.test.ts:1` exerce le support d'enregistrement d'outils d'image partagés.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.video-generation.test.ts:1` exerce le support d'enregistrement d'outils vidéo partagés.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "imageGenerationModel videoGenerationModel musicGenerationModel provider discovery image_generate video_generate music_generate" --json`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte, ce qui suggère que le contrat de clé de configuration explicite n'est pas une plainte archivée courante.

Requête : `gitcrawl search openclaw/openclaw --query "image generation" --json`

Résultats :

- A retourné #78852 sur la réutilisation de la disponibilité d'outils médias lors de la préparation d'outils, #78330 sur l'exposition des fournisseurs de génération d'images sur RPC de passerelle et #76690 sur l'échec de la génération d'images Codex OAuth car l'outil n'était pas disponible.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "video_generate"`

Résultats :

- A trouvé une discussion du responsable sur les outils médias différés où les aperçus de source existaient mais les noms d'outils médias individuels n'étaient pas suffisamment découvrables pour `music_generate`, `video_generate` et `image_generate`.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "image_generate"`

Résultats :

- A trouvé des rapports d'utilisateurs et de responsables sur l'authentification d'image OpenRouter, l'incompatibilité de source de credentials Codex/OpenAI et le routage des points de terminaison d'outils médias.
