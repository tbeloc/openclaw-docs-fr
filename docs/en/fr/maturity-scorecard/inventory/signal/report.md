---
title: "Rapport de Maturité du Signal"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité du Signal

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Alpha (66%)`
- Qualité : `Alpha (65%)`
- Complétude : `Alpha (66%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées du `signal` de `/Users/kevinlin/tmp/maturity/signal` dans le contrat d'inventaire actuel de la version-3 du processus.

Les scores de couverture et de qualité de la catégorie proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                 | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                         |
| ------------------------------------------------------------------------ | --- | ------------- | ------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration et Opérations des Canaux](setup-install-account-provisioning.md)    | ❌  | `Alpha (55%)` | `Alpha (58%)` | `Alpha (55%)` | Configuration de lien QR, Enregistrement SMS, Configuration de l'installateur et du binaire, Provisionnement de compte conteneur, Sondes d'état, Diagnostics de configuration, Garde-fous de sécurité des comptes                     |
| [Accès et Identité](dm-pairing-access-control.md)                      | ❌  | `Beta (70%)`  | `Alpha (66%)` | `Beta (70%)`  | Appairage DM, Listes blanches DM, Normalisation de l'identité de l'expéditeur, Listes blanches de groupe, Portes de mention, Historique de groupe en attente                                                             |
| [Routage et Livraison des Conversations](group-routing-mention-history.md)    | ❌  | `Beta (70%)`  | `Alpha (66%)` | `Beta (70%)`  | Routage et Livraison des Conversations                                                                                                                                            |
| [Médias et Contenu Enrichi](outbound-delivery-media-receipts.md)            | ❌  | `Beta (70%)`  | `Alpha (68%)` | `Beta (70%)`  | Cibles de livraison de texte, Livraison et limites des médias, Indicateurs de saisie et de lecture, Sortie stylisée/fragmentée, Découverte d'actions de réaction, Ajouter/supprimer des réactions, Ciblage de réaction de groupe |
| [Contrôles Natifs et Approbations](approval-routing-reaction-resolution.md) | ❌  | `Alpha (65%)` | `Alpha (68%)` | `Alpha (65%)` | Routage d'approbation natif, Réponses d'approbation de réaction, Ciblage des approbateurs                                                                                                     |

## Barème de notation

- Couverture :
  notation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  notation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifique à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `qualité > 80 et couverture > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité
  plus élevée.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et Opérations des Canaux

Ancres de recherche : Configuration de lien QR, Enregistrement SMS, Configuration de l'installateur et du binaire, Provisionnement de compte conteneur, dmPolicy, allowFrom, groupPolicy, requireMention, Sondes d'état, Diagnostics de configuration, Garde-fous de sécurité des comptes, historyLimit.

Note de catégorie : [Configuration et Opérations des Canaux](setup-install-account-provisioning.md)

Décisions de notation :

- Couverture : `Alpha (55%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (55%)`
- LTS : ❌

Fonctionnalités :

- Configuration de lien QR : Définit la configuration de lien QR, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la Configuration, l'Installation et le Provisionnement de Compte.
- Enregistrement SMS : Définit l'enregistrement SMS, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la Configuration, l'Installation et le Provisionnement de Compte.
- Configuration de l'installateur et du binaire : Définit la configuration de l'installateur et du binaire, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la Configuration, l'Installation et le Provisionnement de Compte.
- Provisionnement de compte conteneur : Définit le provisionnement de compte conteneur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la Configuration, l'Installation et le Provisionnement de Compte.
- Sondes d'état : Définit les sondes d'état, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les Diagnostics, l'État de la Configuration et les Garde-fous de l'Opérateur.
- Diagnostics de configuration : Définit les diagnostics de configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les Diagnostics, l'État de la Configuration et les Garde-fous de l'Opérateur.
- Garde-fous de sécurité des comptes : Définit les garde-fous de sécurité des comptes, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les Diagnostics, l'État de la Configuration et les Garde-fous de l'Opérateur.

Documentation principale :

- `docs/channels/signal.md`
- `docs/plugins/reference/signal.md`

### 2. Accès et Identité

Ancres de recherche : Appairage DM, Listes blanches DM, Normalisation de l'identité de l'expéditeur, dmPolicy, allowFrom, groupPolicy, requireMention, historyLimit, Listes blanches de groupe, Portes de mention, Historique de groupe en attente.

Note de catégorie : [Accès et Identité](dm-pairing-access-control.md)

Décisions de notation :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Appairage DM : Définit l'appairage DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour l'Appairage DM et le Contrôle d'Accès.
- Listes blanches DM : Définit les listes blanches DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour l'Appairage DM et le Contrôle d'Accès.
- Normalisation de l'identité de l'expéditeur : Définit la normalisation de l'identité de l'expéditeur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour l'Appairage DM et le Contrôle d'Accès.
- Listes blanches de groupe : Définit les listes blanches de groupe, l'autorisation, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.
- Portes de mention : Définit les portes de mention, l'autorisation, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.
- Historique de groupe en attente : Définit l'historique de groupe en attente, l'autorisation, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.

Documentation principale :

- `docs/channels/signal.md`

### 3. Routage et Livraison des Conversations

Ancres de recherche : routage et livraison des conversations signal, routage et livraison des conversations.

Note de catégorie : [Routage et Livraison des Conversations](group-routing-mention-history.md)

Décisions de notation :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Routage et Livraison des Conversations : Portée des preuves pour le Routage et la Livraison des Conversations.

Documentation principale :

- `docs/channels/signal.md`

### 4. Médias et Contenu Enrichi

Ancres de recherche : Cibles de livraison de texte, Livraison et limites des médias, Indicateurs de saisie et de lecture, Sortie stylisée/fragmentée, dmPolicy, allowFrom, groupPolicy, requireMention, Découverte d'actions de réaction, Ajouter/supprimer des réactions, Ciblage de réaction de groupe, historyLimit.

Note de catégorie : [Médias et Contenu Enrichi](outbound-delivery-media-receipts.md)

Décisions de notation :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Cibles de livraison de texte : Couvre le routage des cibles de livraison de texte, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Livraison et limites des médias : Couvre le routage de la livraison et des limites des médias, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Indicateurs de saisie et de lecture : Couvre le routage des indicateurs de saisie et de lecture, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Sortie stylisée/fragmentée : Couvre le routage de la sortie stylisée/fragmentée, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Découverte d'actions de réaction : Couvre le routage de la découverte d'actions de réaction, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.
- Ajouter/supprimer des réactions : Couvre le routage de l'ajout/suppression de réactions, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.
- Ciblage de réaction de groupe : Couvre le routage du ciblage de réaction de groupe, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.

Documentation principale :

- `docs/channels/signal.md`

### 5. Contrôles Natifs et Approbations

Ancres de recherche : Routage d'approbation natif, Réponses d'approbation de réaction, Ciblage des approbateurs, dmPolicy, allowFrom, groupPolicy, requireMention, historyLimit.

Note de catégorie : [Contrôles Natifs et Approbations](approval-routing-reaction-resolution.md)

Décisions de notation :

- Couverture : `Alpha (65%)`
- Qualité : `Alpha (68%)`
- Complétude : `Alpha (65%)`
- LTS : ❌

Fonctionnalités :

- Routage d'approbation natif : Définit le routage d'approbation natif, l'autorisation, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage d'Approbation et la Résolution de Réaction.
- Réponses d'approbation de réaction : Définit les réponses d'approbation de réaction, l'autorisation, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage d'Approbation et la Résolution de Réaction.
- Ciblage des approbateurs : Définit le ciblage des approbateurs, l'autorisation, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage d'Approbation et la Résolution de Réaction.

Documentation principale :

- `docs/channels/signal.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme la ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/signal/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/signal`.
