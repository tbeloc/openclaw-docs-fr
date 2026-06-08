---
title: "Matrix Maturity Report"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité Matrix

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans
`scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Beta (72%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (72%)`
- Fonctionnalités LTS : `0/6`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `matrix` depuis `/Users/kevinlin/tmp/maturity/matrix` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrix

| Catégorie                                                                           | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                              |
| ---------------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Configuration des canaux et opérations](setup-config-and-account-selection.md)    | ❌  | `Beta (74%)`  | `Beta (74%)`  | `Beta (74%)`  | Identité du plugin Matrix, Assistant de configuration, Découverte de compte, Avertissements Matrix doctor, Sonde/statut Matrix                                                                         |
| [Accès et identité](dm-room-routing-and-access-policy.md)                          | ❌  | `Beta (72%)`  | `Alpha (66%)` | `Beta (72%)`  | Politique DM, Classification des salons directs, Sélection de route entrante entre les DM liés à l'expéditeur, Portes de mention, Routage des réponses de fil Matrix, Gestionnaires de routage de fil Matrix persistants, Crochets de génération ACP/sous-agent |
| [Routage et livraison des conversations](threads-acp-and-subagent-bindings.md)     | ❌  | `Beta (72%)`  | `Alpha (66%)` | `Beta (72%)`  | Routage et livraison des conversations                                                                                                                                                                 |
| [Médias et contenu enrichi](outbound-messages-media-and-streaming.md)              | ❌  | `Beta (74%)`  | `Alpha (68%)` | `Beta (74%)`  | Médias et contenu enrichi                                                                                                                                                                              |
| [Contrôles natifs et approbations](actions-profile-polls-reactions-and-room-tools.md) | ❌  | `Alpha (64%)` | `Alpha (68%)` | `Alpha (64%)` | Découverte d'actions de canal, Envoi/lecture/édition/suppression de messages, Chargement des médias de profil, Texte Matrix sortant, Métadonnées de présentation des messages, Gestion des défaillances de médias entrants |
| [Chiffrement et vérification](e2ee-verification-backup-and-migration.md)           | ❌  | `Beta (76%)`  | `Alpha (68%)` | `Beta (76%)`  | Configuration du chiffrement, Téléchargement/téléversement de médias chiffrés, État hérité                                                                                                            |

## Barème de notation

- Couverture :
  notation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; ils ne
  n'augmentent ni ne diminuent la qualité.
- Complétude :
  notation de l'étiquette de maturité pour la complétude avec laquelle la catégorie fournit l'ensemble de
  capacités spécifiques à la surface prévues. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'
  étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration des canaux et opérations

Ancres de recherche : configuration et sélection de compte matrix, configuration et sélection de compte, diagnostics et réparation opérationnelle matrix doctor, diagnostics et réparation opérationnelle.

Note de catégorie : [Configuration des canaux et opérations](setup-config-and-account-selection.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Identité du plugin Matrix : Identité du plugin Matrix, métadonnées d'installation, entrées runtime/configuration et configuration de compte.
- Assistant de configuration : Assistant de configuration, adaptateur de configuration, validation, bootstrap post-écriture et configuration de compte.
- Découverte de compte : Découverte de compte, règles de compte par défaut, comptes soutenus par env et métadonnées de compte stockées.
- Avertissements Matrix doctor : Avertissements Matrix doctor, normalisation de la configuration et nettoyage de la configuration de plugin obsolète.
- Sonde/statut Matrix : Sonde/statut Matrix, recherche de répertoire en direct, diagnostics CLI et statut runtime QA.

Documentation principale :

- `docs/channels/matrix.md`
- `docs/channels/matrix-migration.md`

### 2. Accès et identité

Ancres de recherche : routage des salons dm matrix et politique d'accès, routage des salons dm et politique d'accès, fils matrix, acp et liaisons de sous-agent, fils, acp et liaisons de sous-agent.

Note de catégorie : [Accès et identité](dm-room-routing-and-access-policy.md)

Décisions de notation :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Politique DM : Politique DM, appairage, allowFrom, groupAllowFrom, listes blanches de salons et vérifications d'accès en direct.
- Classification des salons directs : Classification des salons directs et décisions de routage adjacentes à la réparation
- Sélection de route entrante entre les DM liés à l'expéditeur : Sélection de route entrante entre les DM liés à l'expéditeur, liaisons de salons et routes délimitées par compte.
- Portes de mention : Portes de mention, vérifications d'accès aux commandes slash, suppression de boucles de bot et admission de contexte.
- Routage des réponses de fil Matrix : Routage des réponses de fil Matrix, extraction de racine/contexte de fil et placement de session conscient du fil.
- Gestionnaires de routage de fil Matrix persistants : Gestionnaires de liaison de fil Matrix persistants, liaison de session enfant et suivi d'activité.
- Crochets de génération ACP/sous-agent : Crochets de génération ACP/sous-agent et cibles de livraison Matrix pour les sessions enfants

Documentation principale :

- `docs/channels/matrix.md`
- `docs/channels/groups.md`
- `docs/channels/bot-loop-protection.md`

### 3. Routage et livraison des conversations

Ancres de recherche : routage et livraison des conversations matrix, routage et livraison des conversations.

Note de catégorie : [Routage et livraison des conversations](threads-acp-and-subagent-bindings.md)

Décisions de notation :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Routage et livraison des conversations : Portée des preuves pour le routage et la livraison des conversations.

Documentation principale :

- `docs/channels/matrix.md`

### 4. Médias et contenu enrichi

Ancres de recherche : médias et contenu enrichi matrix, médias et contenu enrichi.

Note de catégorie : [Médias et contenu enrichi](outbound-messages-media-and-streaming.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Médias et contenu enrichi : Portée des preuves pour les médias et le contenu enrichi.

Documentation principale :

- `docs/channels/matrix.md`

### 5. Contrôles natifs et approbations

Ancres de recherche : actions matrix, profil, sondages, réactions et outils de salon, actions, profil, sondages, réactions et outils de salon, messages sortants matrix, médias et streaming, messages sortants, médias et streaming.

Note de catégorie : [Contrôles natifs et approbations](actions-profile-polls-reactions-and-room-tools.md)

Décisions de notation :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (68%)`
- Complétude : `Alpha (64%)`
- LTS : ❌

Fonctionnalités :

- Découverte d'actions de canal : Découverte d'actions de canal, portes d'actions délimitées par compte et schémas d'outils
- Envoi/lecture/édition/suppression de messages : Envoi/lecture/édition/suppression de messages, vote aux sondages, ajout/suppression/liste de réactions, épingles et outils de salon connexes.
- Chargement des médias de profil : Chargement des médias de profil à partir d'une URL ou d'un chemin local.
- Texte Matrix sortant : Texte Matrix sortant, médias, médias chiffrés, sondage, saisie, reçu de lecture et comportement de livraison.
- Métadonnées de présentation des messages : Métadonnées de présentation des messages, métadonnées de mention Matrix et comportement de livraison fragmenté.
- Gestion des défaillances de médias entrants : Gestion des défaillances de téléchargement de médias entrants lorsqu'elles affectent les réponses sortantes.

Documentation principale :

- `docs/channels/matrix.md`

### 6. Chiffrement et vérification

Ancres de recherche : e2ee matrix, vérification, sauvegarde et migration, e2ee, vérification, sauvegarde et migration.

Note de catégorie : [Chiffrement et vérification](e2ee-verification-backup-and-migration.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Configuration du chiffrement : Configuration du chiffrement, disponibilité de la cryptographie, stockage de clé de récupération et stockage de secrets.
- Téléchargement/téléversement de médias chiffrés : Téléchargement/téléversement de médias chiffrés et avis de vérification au démarrage
- État hérité : État hérité et migration de cryptographie, instantanés de migration et réparation au démarrage de la passerelle.

Documentation principale :

- `docs/channels/matrix.md`
- `docs/channels/matrix-migration.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/matrix/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/matrix`.
