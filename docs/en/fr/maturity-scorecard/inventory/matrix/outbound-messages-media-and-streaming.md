---
title: "Matrix - Media and Rich Content Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Media and Rich Content Maturity Note

## Résumé

La livraison sortante Matrix dispose d'un large support de fonctionnalités : segmentation de texte, téléchargement de médias,
charges utiles de médias chiffrées, sondages, saisie, accusés de réception, modifications, mentions,
réactions, métadonnées de charge utile, aperçus de brouillon, mode silencieux, diffusion en continu par blocs et
livraison de secours. La couverture est Beta car la documentation, le code source, les tests unitaires et l'assurance qualité Matrix
couvrent de nombreux chemins. La qualité est Alpha car gitcrawl a des rapports ouverts pour
la gestion des images, les défaillances de la file d'attente d'envoi, la livraison du raisonnement et le rendu des mentions.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Media and Rich Content`
- Fusionnée à partir de : `Messaging and Room Tools`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Découverte d'actions de canal : Découverte d'actions de canal, portes d'actions à portée de compte et schémas d'outils
- Envoi/lecture/modification/suppression de messages : Envoi/lecture/modification/suppression de messages, vote sur sondages, ajout/suppression/liste de réactions, épingles et outils de salle associés.
- Chargement de médias de profil : Chargement de médias de profil à partir d'une URL ou d'un chemin local.
- Texte Matrix sortant : Texte Matrix sortant, médias, médias chiffrés, sondage, saisie, accusé de réception et comportement de livraison.
- Métadonnées de présentation des messages : Métadonnées de présentation des messages, métadonnées de mention Matrix et comportement de livraison segmenté.
- Gestion des défaillances de médias entrants : Gestion des défaillances de téléchargement de médias entrants lorsqu'elles affectent les réponses sortantes.

## Fonctionnalités

- Media and Rich Content : Portée des preuves pour Media and Rich Content.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - La documentation couvre les aperçus de diffusion en continu, les règles de notification en mode silencieux, les métadonnées d'approbation,
    les réactions, le contexte historique et la configuration du comportement de réponse.
  - Le code source implémente la segmentation de texte, le téléchargement de médias, les médias chiffrés, les sondages,
    les accusés de réception/saisie, les marqueurs en direct, les modifications, les réactions et la
    résolution des cibles.
  - Les tests unitaires couvrent le texte/médias sortants, la diffusion de médias, la présentation des messages,
    les médias chiffrés, les mentions, les envois segmentés, les modifications, les sondages, le flux de brouillon et les secours en cas de défaillance de médias.
  - L'assurance qualité Matrix couvre les aperçus de diffusion en continu, la progression des outils, la diffusion en continu par blocs, la compréhension d'images,
    la génération d'images et chaque type de message média Matrix avec des réponses déclenchées par des légendes.
- Signaux négatifs :
  - Les rapports d'archive ouverts montrent que le comportement sortant/média reste un risque majeur
    visible par l'utilisateur.
  - La couverture est large mais fragmentée entre les tests d'adaptateur sortant, les tests d'envoi,
    les tests de gestionnaire de moniteur et les scénarios d'assurance qualité.
- Lacunes d'intégration :
  - Ajouter une seule voie de médias en direct critique pour la version qui couvre le téléchargement, le téléchargement,
    les médias chiffrés, les mentions de légende et la livraison finale.
  - Ajouter une voie de livraison de raisonnement en direct pour Matrix lorsque le raisonnement est activé.
  - Lier les diagnostics de la file d'attente d'envoi Matrix aux artefacts d'assurance qualité sortante échoués.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans
le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par
eux-mêmes.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "matrix outbound media streaming mention rendering"` n'a retourné aucun résultat.
  - La requête large `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné le problème ouvert #85620 pour les tours non résolus d'images entrantes et les défaillances de récupération de la file d'attente d'envoi, le problème ouvert #81892 pour le raisonnement non livré, le problème ouvert #80432 pour le rendu des mentions sortantes sans pilules Matrix ou métadonnées de mention, et la demande de tirage ouverte #83156 pour les étiquettes de mention de nom d'affichage entre crochets.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix outbound media streaming"` a retourné une discussion de version/journal de mars 2026 mentionnant la diffusion en continu de brouillon Matrix plus l'historique de la salle comme fonctionnalité visible par l'utilisateur.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions de version mentionnant le comportement des mentions Matrix.
- Bonnes qualités :
  - Le code d'envoi sépare la conversion de charge utile, la résolution de cible, le téléchargement de médias,
    la construction de contenu, les segments, les modifications, les réactions et les accusés de réception.
  - La diffusion en continu de brouillon a un throttling explicite, des limites d'événement unique, des sauts sans opération,
    un comportement d'arrêt/finalisation et des marqueurs de secours.
  - Le rendu des mentions crée intentionnellement des ancres `m.mentions` et Matrix.to
    pour les mentions d'utilisateur et de salle qualifiées tout en évitant les mentions actives dans
    les contextes non sécurisés.
  - Le téléchargement de médias chiffrés inclut la gestion des charges utiles de miniature et de fichier.
- Mauvaises qualités :
  - Les médias et la diffusion en continu ont des problèmes visibles par l'utilisateur ouverts et des rapports opérationnels.
  - Le rendu des mentions Matrix est subtil et a des corrections actives récentes.
  - Les défaillances de la file d'attente d'envoi/récupération peuvent se propager en tours non résolus et en rechargements de passerelle.
  - La livraison du raisonnement a un rapport Matrix ouvert direct.
- Exclu de la qualité :
  - Je n'ai pas augmenté ou diminué la qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct ou
    d'exécution réelle.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou
d'exécution réelle comme entrée de notation.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Media and Rich Content.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Fermer ou retester #85620, #81892 et #80432 avant de relever la qualité au-dessus d'Alpha.
- Ajouter une couverture d'assurance qualité directe pour la livraison de charge utile de raisonnement sur Matrix.
- Enregistrer les artefacts de défaillance pour les défaillances de récupération de la file d'attente d'envoi Matrix et les tours de médias non résolus.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:183` documente
  les modes d'aperçu en streaming, les règles de notification silencieuse et les métadonnées d'approbation.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:568` documente les
  réactions Matrix.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:589` documente
  l'historique du contexte et la visibilité du contexte.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:831` documente le
  comportement des réponses, les paramètres de réaction et la configuration des outils.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.ts:160`
  prépare et divise le texte Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.ts:211`
  envoie du texte et des médias avec des salons résolus, des relations, du téléchargement de médias, du contenu,
  des suivis et des accusés de réception.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.ts:366`
  envoie des événements de sondage Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.ts:450`
  gère les envois de messages uniques, les limites de texte et les marqueurs en direct.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.ts:542`
  édite les messages Matrix avec diffing de mentions et marqueurs en direct.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send/media.ts:61`
  construit le contenu et les métadonnées des médias.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send/media.ts:203`
  télécharge les médias chiffrés.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/draft-stream.ts:49`
  implémente le flux de brouillon Matrix et la limite d'aperçu d'événement unique.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/outbound.ts:96`
  adapte les charges utiles sortantes partagées au texte Matrix, aux médias, aux sondages et aux
  métadonnées de présentation.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:2875`
  capture les avis d'aperçu silencieux avant la réponse Matrix finalisée.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:2957`
  capture les messages texte d'aperçu partiel avant la réponse finalisée.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:3091`
  capture la progression des outils Matrix dans l'aperçu silencieux avant la finalisation.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4074`
  préserve les événements de bloc finalisés séparés lorsque le streaming de bloc est activé.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4181`
  envoie une véritable pièce jointe d'image Matrix pour les invites de compréhension d'image.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4277`
  attend une véritable pièce jointe d'image Matrix après la génération d'image.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4366`
  couvre tous les types de messages de médias Matrix avec des réponses déclenchées par légende.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/outbound.test.ts:65`
  couvre la configuration résolue pour les envois de texte.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/outbound.test.ts:93`
  couvre la configuration résolue pour les envois de médias.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/outbound.test.ts:381`
  couvre l'envoi de toutes les URL de médias via `sendPayload`.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/outbound.test.ts:468`
  protège contre les URL de médias silencieusement supprimées.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.test.ts:225`
  couvre le téléchargement de médias avec des charges utiles d'URL.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.test.ts:249`
  couvre les médias chiffrés avec des charges utiles de fichiers.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.test.ts:486`
  couvre les ancres de mention Matrix et `m.mentions`.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send.test.ts:596`
  couvre les métadonnées de relation de fil.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/draft-stream.test.ts:212`
  couvre les aperçus de texte normaux.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/draft-stream.test.ts:507`
  couvre le repli lorsque le texte d'aperçu dépasse un événement Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/media.test.ts:54`
  couvre le téléchargement de médias chiffrés.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.media-failure.test.ts:157`
  couvre les marqueurs de repli pour les téléchargements d'images échoués.

### Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "matrix outbound media streaming mention rendering"`
  n'a retourné aucun résultat.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné #85620,
  #81892, #80432, #83156 et d'autres résultats adjacents à la sortie Matrix.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix outbound media streaming"`
  a retourné une discussion de version sur le streaming de brouillon Matrix et l'historique des salons.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"`
  a retourné des discussions de version mentionnant le comportement des mentions Matrix.
