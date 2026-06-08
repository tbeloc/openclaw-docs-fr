---
title: "Matrix - Native Controls and Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Native Controls and Approvals Maturity Note

## Summary

La prise en charge des actions Matrix est large et raisonnablement structurée. Le plugin expose
les actions de canal pour les messages, les sondages, les réactions, les épingles, les mises à jour de profil, les
informations de membre, les informations de salle, les permissions et les actions de vérification, avec
gating au niveau du compte et schémas d'outils. La couverture est Beta car la source et les tests couvrent les
familles d'actions mais la preuve de scénario en direct n'est pas également approfondie pour chaque action.
La qualité est Beta car la source est robuste mais la surface d'action est large
et certains champs d'informations de salle/membre restent intentionnellement partiels.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Native Controls and Approvals`
- Fusionnée à partir de : `Messaging and Room Tools`, `Approvals`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Découverte d'actions de canal : Découverte d'actions de canal, portes d'actions au niveau du compte et schémas d'outils
- Envoi/lecture/édition/suppression de messages : Envoi/lecture/édition/suppression de messages, vote sur sondage, ajout/suppression/liste de réactions, épingles et outils de salle associés.
- Chargement de médias de profil : Chargement de médias de profil à partir d'une URL ou d'un chemin local.
- Texte Matrix sortant : Texte Matrix sortant, médias, médias chiffrés, sondage, saisie, reçu de lecture et comportement de livraison.
- Métadonnées de présentation de message : Métadonnées de présentation de message, métadonnées de mention Matrix et comportement de livraison fragmenté.
- Gestion des défaillances de médias entrants : Gestion des défaillances de téléchargement de médias entrants lorsqu'elles affectent les réponses sortantes.
- Exécution native Matrix : Exécution native Matrix et capacité d'approbation du plugin
- Résolution de cible d'origine à partir du tour Matrix : Résolution de cible d'origine à partir de la source du tour Matrix, secours de session et routage d'approbation.
- Résolution de cible DM approbateur : Résolution de cible DM approbateur, suppression de secours de transfert et livraison d'approbation native.
- Métadonnées d'approbation Matrix : Métadonnées d'approbation Matrix, indices de réaction, persistance d'ancrage de réaction et état de décision.
- Résolution de cible d'origine à partir du tour Matrix : Résolution de cible d'origine à partir de la source du tour Matrix, secours de session et routage d'approbation
- Résolution de cible DM approbateur : Résolution de cible DM approbateur, suppression de secours de transfert et livraison d'approbation native
- Métadonnées d'approbation Matrix : Métadonnées d'approbation Matrix, indices de réaction, persistance d'ancrage de réaction et état de décision

## Fonctionnalités

- Découverte d'actions de canal : Découverte d'actions de canal, portes d'actions au niveau du compte et schémas d'outils
- Envoi/lecture/édition/suppression de messages : Envoi/lecture/édition/suppression de messages, vote sur sondage, ajout/suppression/liste de réactions, épingles et outils de salle associés.
- Chargement de médias de profil : Chargement de médias de profil à partir d'une URL ou d'un chemin local.
- Texte Matrix sortant : Texte Matrix sortant, médias, médias chiffrés, sondage, saisie, reçu de lecture et comportement de livraison.
- Métadonnées de présentation de message : Métadonnées de présentation de message, métadonnées de mention Matrix et comportement de livraison fragmenté.
- Gestion des défaillances de médias entrants : Gestion des défaillances de téléchargement de médias entrants lorsqu'elles affectent les réponses sortantes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs :
  - Les docs couvrent la gestion des profils, les réactions, la résolution de cible, l'historique
    contexte, référence de configuration et paramètres d'outils/actions.
  - La source a un adaptateur d'action de canal et un dispatcher d'outil direct avec
    portes au niveau du compte et analyse spécifique à l'action.
  - Les tests unitaires couvrent la découverte d'actions, le schéma de profil, le gating d'actions, la propagation de compte,
    votes sur sondage, réactions, actions de message, épingles, appareils, résumé,
    mises à jour de profil et informations de salle/membre.
  - L'assurance qualité Matrix inclut les médias, les réactions, l'édition, la salle, les DM et les scénarios E2EE
    qui exercent un comportement adjacent à l'action.
- Signaux négatifs :
  - La preuve en direct n'est pas également forte pour chaque action exposée via l'
    adaptateur.
  - Certaines actions dépendent des API d'état du serveur Matrix qui peuvent être clairsemées ou
    sensibles aux permissions.
- Lacunes d'intégration :
  - Ajouter un profil QA Matrix axé sur les actions pour les mises à jour de profil, les épingles, les informations de
    membre, les informations de salle, les votes sur sondage et la liste des réactions.
  - Ajouter une preuve en direct pour les remplacements d'actions au niveau du compte.
  - Ajouter des docs reliant chaque action exposée à son nom de commande/outil et ses modes de défaillance.

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

- Score : `Beta (72%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "Matrix actions polls reactions profile pins"` n'a retourné aucun résultat.
  - La requête large `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné des problèmes Matrix plus larges, mais aucun incident spécifique à l'action à haut signal direct parmi les meilleurs résultats.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix actions polls reactions profile pins"` n'a retourné aucun résultat.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions de version mentionnant la validation de canal Matrix et le comportement de mention.
- Bonnes qualités :
  - L'exposition d'action est contrôlée par la configuration du compte et le contexte du propriétaire de l'expéditeur pour
    les mises à jour de profil.
  - La gestion directe des actions normalise les alias snake_case et les
    options au niveau du compte.
  - Le code de vote sur sondage valide le type d'événement de sondage, les identifiants d'option, les index et
    les limites de sélection avant d'envoyer une réponse.
  - Les mises à jour de profil utilisent les chargeurs de médias d'exécution et persistent via les chemins d'aide partagés.
- Mauvaises qualités :
  - La surface d'action est large et expose de nombreux modes de défaillance via un
    dispatcher unique.
  - Les informations de membre et de salle retournent intentionnellement des données partielles pour l'adhésion,
    les niveaux de pouvoir et les alias alternatifs.
  - La preuve d'archive est large plutôt que spécifique à l'action, donc le signal de support est
    limité par l'examen de la source et les tests.
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

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la découverte d'actions de canal, l'envoi/lecture/édition/suppression de messages, le chargement de médias de profil, le texte Matrix sortant, les métadonnées de présentation de message, la gestion des défaillances de médias entrants.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un tableau de contrat d'action qui liste chaque action, porte de configuration, paramètres
  et dépendance d'événement/API Matrix.
- Ajouter l'assurance qualité en direct pour les épingles et les informations de membre/salle, pas seulement la couverture unitaire de bas niveau.
- Décider si les informations partielles de membre/salle doivent être documentées comme une limitation explicite.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:491` documente la gestion des profils Matrix.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:568` documente les réactions.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:589` documente le contexte historique.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:812` documente la résolution des cibles.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:831` documente la configuration des actions et des outils.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/actions.ts:20` énumère les noms d'actions de canal gérées par le plugin Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/actions.ts:64` construit les actions exposées à partir des portes d'action, de l'état de chiffrement et du contexte du propriétaire.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/actions.ts:119` implémente l'adaptateur d'action de message de canal Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/tool-actions.ts:47` regroupe les actions d'outils Matrix directs.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/tool-actions.ts:150` distribue les actions directes Matrix avec une configuration délimitée par compte.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/polls.ts:24` résout les identifiants et les étiquettes des réponses de sondage sélectionnées.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/polls.ts:73` envoie les réponses de vote de sondage Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/profile.ts:6` met à jour le nom et l'avatar du profil Matrix en utilisant le chargement de médias à l'exécution.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/room.ts:5` lit les informations des membres et les informations de la salle.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/devices.ts:5` énumère les appareils Matrix et supprime les appareils de passerelle obsolètes.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:581` attend l'écho de réaction d'approbation Matrix avant d'attendre une décision.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4181` envoie une véritable pièce jointe d'image Matrix pour les invites de compréhension d'image.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4366` couvre chaque type de message de média Matrix avec des réponses déclenchées par légende.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4816` rejoint automatiquement une salle de groupe Matrix nouvellement invitée avant de répondre.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/actions.test.ts:55` couvre l'exposition des actions de sondage.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/actions.test.ts:75` couvre la découverte des actions de profil personnel.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/actions.test.ts:122` couvre les actions contrôlées désactivées par la configuration du compte.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/actions.test.ts:193` couvre le compte Matrix sélectionné lors de la découverte des actions.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/tool-actions.test.ts:74` couvre les paramètres de vote de sondage en snake_case.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/tool-actions.test.ts:141` couvre les ajouts de réaction délimités par compte.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/tool-actions.test.ts:277` couvre les racines de médias pour les mises à jour de profil.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/tool-actions.test.ts:316` couvre les actions d'informations sur les membres et les salles.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/tool-actions.test.ts:404` couvre les remplacements d'actions délimités par compte.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/reactions.test.ts:43` couvre les actions de réaction Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/pins.test.ts:39` couvre les actions d'épingles.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/profile.test.ts:41` couvre les actions de profil.

### Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "Matrix actions polls reactions profile pins"` n'a retourné aucun résultat.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné des résultats opérationnels Matrix larges mais aucun incident spécifique aux actions dans l'ensemble retourné.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix actions polls reactions profile pins"` n'a retourné aucun résultat.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions générales sur les versions et validations Matrix.
