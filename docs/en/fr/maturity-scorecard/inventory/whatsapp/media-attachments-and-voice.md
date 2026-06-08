---
title: "WhatsApp - Note de maturité des médias et du contenu enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Note de maturité des médias et du contenu enrichi

## Résumé

Les pièces jointes multimédias WhatsApp et la voix sont en Bêta pour la couverture et stables pour la qualité. Les contrats source sont solides pour les téléchargements entrants, les médias cités, les charges utiles image/audio/vidéo/document sortantes, la conversion de notes vocales, les limites de médias, la gestion des noms de fichiers et la sécurité de la racine locale. La couverture reste en Bêta car la preuve en direct actuelle ne couvre pas la matrice complète des médias.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Media and Rich Content`
- Fusionnée à partir de : `Media Attachments`
- Report du score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Téléchargement de médias entrants : téléchargement de médias entrants et construction d'espaces réservés, extraction de médias cités et remise de fichiers.
- Image sortante : construction de charges utiles image, audio, vidéo, document et note vocale sortantes.

## Fonctionnalités

- Téléchargement de médias entrants : téléchargement de médias entrants et construction d'espaces réservés, extraction de médias cités et remise de fichiers.
- Image sortante : construction de charges utiles image, audio, vidéo, document et note vocale sortantes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`
- Signaux positifs : la documentation décrit les médias entrants, les médias cités, les médias sortants, les limites de taille, les légendes, les solutions de secours et le dépannage ; la source a des contrats explicites pour les médias entrants et sortants ainsi que des tests unitaires/d'exécution sur les types de charges utiles courants.
- Signaux négatifs : Gitcrawl et Discrawl n'ont retourné aucun résultat spécifique aux médias actuels, et la preuve la plus solide est basée sur le contrat source/test plutôt que sur les exécutions WhatsApp multimédias en direct actuelles.
- Lacunes d'intégration : aucune matrice en direct localisée ne prouve ensemble les images/documents/audio entrants, les médias cités, les images/audio/vidéo/documents sortants, la conversion de notes vocales et le secours de surcharge.

## Score de qualité

- Score : `Stable (80%)`
- Rapports Gitcrawl : `whatsapp media voice note document image` n'a retourné aucun résultat.
- Rapports Discrawl : `whatsapp media voice note document image` a retourné `null`.
- Bonnes qualités : les limites des médias sont explicites, les tailles de téléchargement entrant sont plafonnées, le chargement de fichiers locaux est enraciné, le texte est assaini, la conversion vocale est isolée derrière les contrats multimédias, les noms de fichiers sont normalisés, et les défaillances multimédias sortantes réessayables sont gérées séparément.
- Mauvaises qualités : l'acceptation du fournisseur en direct dépend toujours de Baileys/WhatsApp, les notes vocales dépendent des outils multimédias de l'hôte, et la documentation de l'opérateur n'énumère pas une matrice de compatibilité multimédias en direct actuelle.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas augmenté ni diminué ce score de qualité.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le téléchargement de médias entrants et l'image sortante.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve en direct récurrente pour les images, audio, voix, vidéo, documents entrants et sortants, les médias cités et le secours de surcharge.
- Documenter la matrice de compatibilité multimédias pratique, y compris les attentes ffmpeg de l'hôte pour la conversion de notes vocales.
- Améliorer les diagnostics de l'opérateur pour les médias acceptés par le fournisseur par rapport aux médias rejetés par WhatsApp/Baileys.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:330` documente la construction d'enveloppe entrante, les médias cités, les espaces réservés multimédias, l'historique de groupe et les accusés de lecture.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:421` documente le comportement des médias sortants, la segmentation du texte, les limites de taille et le comportement de secours.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:455` documente les citations de réponse, les réactions et les réactions de statut/ack.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:669` documente le dépannage de l'acceptation du fournisseur.

### Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/media.ts:51` télécharge les médias entrants avec des limites d'octets max et un secours MIME.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/media.ts:103` télécharge les médias cités.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/extract.ts:270` construit des espaces réservés multimédias pour le contexte entrant.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-media-contract.ts:65` assainit le texte pour les médias sortants.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-media-contract.ts:84` résout les URL multimédias et les charges utiles multimédias locales.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-media-contract.ts:114` construit les charges utiles image, audio, vidéo, document et voix Opus.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-media-contract.ts:209` gère le transcodage ffmpeg pour les charges utiles vocales.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-media-contract.ts:269` gère le comportement des médias sortants réessayables.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-media.runtime.ts:3` charge les médias sortants à partir d'URL et de racines locales.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/monitor-inbox.captures-media-path-image-messages.test-support.ts:1` prend en charge la capture de messages image avec chemin multimédia.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/deliver-reply.test.ts:514` couvre les réponses multimédias dans le pipeline de livraison.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.web-auto-reply.compresses-common-formats-jpeg-cap.test.ts:1` couvre le comportement de compression pour les formats courants.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:1192` exécute le pilote QA WhatsApp en direct et le flux d'artefacts.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/media.test.ts:97` couvre la récupération de médias, l'optimisation, SSRF/racines locales et les limites.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/media.node.test.ts:1` couvre le comportement des médias entrants Node.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound.media.test.ts:1` couvre le comportement des médias entrants.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/document-filename.test.ts:1` couvre la normalisation des noms de fichiers de documents.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/send-api.test.ts:58` couvre les médias, les mentions, l'audio PTT, les sondages/réactions, les infolettres, les remoteJid cités et le routage LID.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp media voice note document image" --json`

Résultats :

- N'a retourné aucun résultat.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp media voice note document image" --limit 5`

Résultats :

- A retourné `null`.
