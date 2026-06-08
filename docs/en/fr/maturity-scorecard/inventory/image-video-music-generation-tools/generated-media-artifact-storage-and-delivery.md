---
title: "Outils de génération d'images/vidéos/musique - Note de maturité de la livraison de médias générés"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Note de maturité de la livraison de médias générés

## Résumé

La livraison de médias générés possède une véritable architecture partagée : les actifs d'images, d'audio et de vidéo générés contiennent des buffers, des chemins, des URL, des métadonnées MIME, des noms de fichiers et des lignes de pièces jointes de messages ; la livraison d'achèvement est acheminée via un transfert message-outil-requis ; le repli direct envoie les médias manquants avec une clé d'idempotence.

La couverture est Beta car la source et les tests couvrent l'extraction et les replis de livraison d'actifs, mais la preuve de stockage et de livraison d'artefacts au niveau du canal est inégale. La qualité est Alpha car les archives GitHub et Discord récentes montrent des verrous de transfert de médias, des échecs de livraison après le succès du fournisseur, des préoccupations concernant les replis en double et des preuves manquantes de livraison message-outil.

## Portée de la catégorie

Cette catégorie couvre les objets d'artefacts d'images/audio/vidéo générés, l'inférence MIME et de nom de fichier, les chemins de médias locaux, les URL de médias hébergés, les lignes de pièces jointes générées, le transfert d'achèvement message-outil-requis, la livraison de repli direct, l'idempotence, la détection de médias manquants et le comportement de réveil du demandeur actif.

## Fonctionnalités

- persistance des médias locaux : Couvre la persistance des médias locaux sur les objets d'artefacts d'images/audio/vidéo générés, l'inférence MIME et de nom de fichier, les chemins de médias locaux, les URL de médias hébergés et le comportement de livraison de médias générés associé.
- inférence MIME/nom de fichier : Couvre l'inférence MIME/nom de fichier sur les objets d'artefacts d'images/audio/vidéo générés, l'inférence MIME et de nom de fichier, les chemins de médias locaux, les URL de médias hébergés et le comportement de livraison de médias générés associé.
- repli d'URL hébergée : Couvre le repli d'URL hébergée sur les objets d'artefacts d'images/audio/vidéo générés, l'inférence MIME et de nom de fichier, les chemins de médias locaux, les URL de médias hébergés et le comportement de livraison de médias générés associé.
- transfert message-outil : Couvre le transfert message-outil sur les objets d'artefacts d'images/audio/vidéo générés, l'inférence MIME et de nom de fichier, les chemins de médias locaux, les URL de médias hébergés et le comportement de livraison de médias générés associé.
- repli idempotent de médias manquants : Couvre le repli idempotent de médias manquants sur les objets d'artefacts d'images/audio/vidéo générés, l'inférence MIME et de nom de fichier, les chemins de médias locaux, les URL de médias hébergés et le comportement de livraison de médias générés associé.
- preuve de pièce jointe de canal : Couvre la preuve de pièce jointe de canal sur les objets d'artefacts d'images/audio/vidéo générés, l'inférence MIME et de nom de fichier, les chemins de médias locaux, les URL de médias hébergés et le comportement de livraison de médias générés associé.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La source couvre l'extraction d'URL de médias, le rendu des pièces jointes, la mise en forme des actifs d'images/audio, les instructions de transfert de tâches, la livraison de repli et plusieurs cas de livraison de médias manquants.
- Signaux négatifs : La plupart des preuves de livraison sont couvertes par des tests d'aide/unité partagés ; moins de vérifications au niveau du scénario prouvent le rendu réel des pièces jointes de canal après l'achèvement du fournisseur.
- Lacunes d'intégration : Ajouter une preuve de médias générés spécifique au canal pour les images, vidéos et musique qui enregistre les preuves de charge utile de message final et vérifie l'absence de livraison de repli en double.

## Score de qualité

- Score : `Alpha (65%)`
- Rapports Gitcrawl : Les recherches de livraison ont retourné #86279 sur la préservation du succès de la génération en cas d'échec de la livraison, #87741 sur le repli après les verrous de transfert de médias générés, #86034 sur le succès de la génération ressemblant à un échec, #74041 sur l'acheminement des médias générés via la livraison d'assistant et #77265 sur les charges utiles d'URL de médias sans livraison de médias Telegram.
- Rapports Discrawl : La recherche Discord a trouvé des discussions sur la livraison de médias générés concernant les transferts instables, le repli vers la sortie de nom de fichier/chemin générée et les correctifs de livraison de médias en double.
- Bonnes qualités : Le chemin de repli est explicite, idempotent et vérifie les médias générés manquants au lieu de dupliquer aveuglément les pièces jointes.
- Mauvaises qualités : La livraison dépend du réveil de la tâche, de la preuve message-outil, du comportement d'envoi de canal et de l'analyse des pièces jointes générées, elle reste donc l'un des chemins opérationnels les plus risqués.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : les docs archivées, la source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la persistance des médias locaux, l'inférence MIME/nom de fichier, le repli d'URL hébergée, le transfert message-outil, le repli idempotent de médias manquants, la preuve de pièce jointe de canal.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, ce score est donc initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La sortie du fournisseur réussie peut toujours échouer à atteindre l'utilisateur en tant que pièce jointe de canal.
- Le système dispose d'une logique de récupération, mais l'état du transfert est difficile à inspecter après coup.
- Certains bugs de livraison spécifiques au canal sont en dehors du runtime du fournisseur partagé mais affectent toujours la maturité perçue par l'utilisateur de la génération de médias.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md:88` décrit la génération asynchrone et la livraison de repli.
- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md:57` documente le stockage de médias géré et le repli d'URL.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:15` documente le registre de tâches, le réveil, la livraison message-outil, le repli et l'avertissement de route privée.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md:11` documente la génération d'images asynchrone et la livraison d'achèvement message-outil.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/generated-attachments.ts:5` définit les objets de pièces jointes générées.
- `/Users/kevinlin/code/openclaw/src/agents/generated-attachments.ts:15` extrait les URL de médias.
- `/Users/kevinlin/code/openclaw/src/agents/generated-attachments.ts:40` rend les lignes de pièces jointes générées.
- `/Users/kevinlin/code/openclaw/src/image-generation/image-assets.ts:112` construit les actifs d'images générés à partir de données base64.
- `/Users/kevinlin/code/openclaw/src/music-generation/provider-assets.ts:50` extrait les candidats de fichiers musicaux générés.
- `/Users/kevinlin/code/openclaw/src/music-generation/provider-assets.ts:78` télécharge les actifs musicaux générés.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.ts:254` construit les instructions de réponse message-outil-requis.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.ts:770` envoie les médias générés de repli direct avec une clé d'idempotence.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.ts:1089` limite le repli direct aux chemins inactifs ou de réveil échoué avec médias manquants.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/media/native-image-generation.md:4` nécessite que les médias d'images générés soient sauvegardés ou livrés.
- `/Users/kevinlin/code/openclaw/qa/scenarios/media/image-generation-roundtrip.md:4` vérifie que les médias générés peuvent être réattachés et décrits.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2247` évite le repli direct lorsque les médias générés ont déjà été livrés par l'outil de message.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2497` livre directement les médias générés lorsque l'agent d'annonce répond uniquement par du texte.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2590` livre directement les médias générés dans les achèvements de groupe manquant la livraison message-outil.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2714` livre directement uniquement les médias manquants après une livraison partielle.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2774` maintient le chemin du demandeur actif à l'abri du repli inutile.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2826` couvre la livraison directe après l'échec du réveil actif.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-generate-background-shared.test.ts:78` échoue la tâche lorsque la livraison d'achèvement ne peut pas être confirmée.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "generated media delivery message tool completion" --json`

Résultats :

- A retourné #86279, #87741, #74041, #86034, #87466 et #87141 sur la livraison de médias générés, le repli et la robustesse des charges utiles.

Requête : `gitcrawl search openclaw/openclaw --query "media generation succeeds completion delivery fails" --json`

Résultats :

- A retourné #86034 sur la génération de médias suivie d'un échec de livraison d'achèvement.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "generated media completion delivery"`

Résultats :

- A trouvé une discussion du responsable sur les verrous de transfert de médias, le repli après une livraison de médias instable, la sortie de nom de fichier/chemin de repli et les correctifs de livraison de médias en double.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "image_generate"`

Résultats :

- A trouvé des rapports d'opérateurs où les échecs de génération et de livraison étaient difficiles à distinguer des problèmes d'authentification du fournisseur ou de credentials de worker.
