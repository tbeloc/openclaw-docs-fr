---
title: "Rapport de Maturité WhatsApp"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité WhatsApp

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (76%)`
- Qualité : `Beta (76%)`
- Complétude : `Beta (76%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `whatsapp` de `/Users/kevinlin/tmp/maturity/whatsapp` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                              | LTS | Couverture   | Qualité        | Complétude   | Fonctionnalités à évaluer                                                                                                                                                                                  |
| --------------------------------------------------------------------- | --- | ------------ | -------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration et Opérations des Canaux](operator-install-and-configuration.md) | ❌  | `Beta (74%)` | `Beta (72%)`   | `Beta (74%)` | Métadonnées officielles du plugin @openclaw/whatsapp, installation du plugin openclaw whatsapp, schéma de configuration du canal, cycle de vie du socket Baileys, dépannage de l'opérateur                                              |
| [Accès et Identité](pairing-login-and-session-auth.md)              | ❌  | `Beta (76%)` | `Beta (72%)`   | `Beta (76%)` | Connexion par code QR, persistance d'authentification multi-fichiers Baileys, défi d'appairage DM, résolution de compte multi-compte/compte par défaut, dmPolicy de message direct, extraction d'identité de l'expéditeur, contrôles de confidentialité pour les hooks de plugin |
| [Routage et Livraison des Conversations](group-routing-and-activation.md)  | ❌  | `Beta (76%)` | `Beta (72%)`   | `Beta (76%)` | Listes blanches de groupes, clés de session de groupe, envois de texte sortants, reçus acceptés par le fournisseur                                                                                                                 |
| [Médias et Contenu Enrichi](media-attachments-and-voice.md)              | ❌  | `Beta (76%)` | `Stable (80%)` | `Beta (76%)` | Téléchargement de médias entrants, image sortante                                                                                                                                                                |
| [Contrôles Natifs et Approbations](native-approvals-and-reactions.md)    | ❌  | `Beta (78%)` | `Stable (84%)` | `Beta (78%)` | Exécution native, résolution de la cible de l'approbateur                                                                                                                                               |

## Rubrique de notation

- Couverture :
  notation de l'étiquette de maturité pour l'intégration, e2e, en direct, ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et du flux runtime réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  notation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité
  plus élevée.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et Opérations des Canaux

Ancres de recherche : installation et configuration de l'opérateur whatsapp, installation et configuration de l'opérateur, reconnexion et docteur de la santé du runtime whatsapp, reconnexion et docteur de la santé du runtime.

Note de catégorie : [Configuration et Opérations des Canaux](operator-install-and-configuration.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Métadonnées officielles du plugin @openclaw/whatsapp : Métadonnées officielles du plugin @openclaw/whatsapp, points d'entrée de package et découverte de configuration.
- Installation du plugin openclaw whatsapp : Installation du plugin openclaw whatsapp et conseils de configuration en premier.
- Schéma de configuration du canal : Schéma de configuration du canal, hooks de plugin, finalisation de la configuration, compte par défaut et gestion des secrets.
- Cycle de vie du socket Baileys : Cycle de vie du socket Baileys, état du contrôleur de connexion, décisions de reconnexion et statut de réparation.
- Dépannage de l'opérateur : Dépannage de l'opérateur pour les boucles de reconnexion, les sockets obsolètes, runtime Bun/Node

Docs principaux :

- `docs/channels/whatsapp.md`
- `docs/gateway/config-channels.md`
- `docs/plugins/reference/whatsapp.md`
- `docs/concepts/qa-e2e-automation.md`
- `docs/gateway/doctor.md`

### 2. Accès et Identité

Ancres de recherche : authentification de connexion et de session d'appairage whatsapp, authentification de connexion et de session d'appairage, accès dm entrant et confidentialité whatsapp, accès dm entrant et confidentialité.

Note de catégorie : [Accès et Identité](pairing-login-and-session-auth.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Connexion par code QR : Connexion par code QR et flux de code QR de connexion d'agent
- Persistance d'authentification multi-fichiers Baileys : Persistance d'authentification multi-fichiers Baileys, écritures de credentials en file d'attente, restauration de sauvegarde et récupération de connexion.
- Défi d'appairage DM : Défi d'appairage DM et persistance du magasin d'autorisation où il croise WhatsApp
- Résolution de compte multi-compte/compte par défaut : Résolution de compte multi-compte/compte par défaut et récupération Baileys 515/401
- dmPolicy de message direct : dmPolicy de message direct, allowFrom, défi d'appairage, magasin d'appairage
- Extraction d'identité de l'expéditeur : Extraction d'identité de l'expéditeur, reçus de lecture, protections de chat personnel et correspondance de contact.
- Contrôles de confidentialité pour les hooks de plugin : Contrôles de confidentialité pour les hooks de plugin et contexte non approuvé

Docs principaux :

- `docs/channels/whatsapp.md`
- `docs/gateway/config-channels.md`
- `docs/concepts/qa-e2e-automation.md`
- `docs/channels/pairing.md`

### 3. Routage et Livraison des Conversations

Ancres de recherche : routage et activation de groupe whatsapp, routage et activation de groupe, livraison et ciblage sortants whatsapp, livraison et ciblage sortants.

Note de catégorie : [Routage et Livraison des Conversations](group-routing-and-activation.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Listes blanches de groupes : Listes blanches de groupes, groupPolicy, JID de groupe exact, requireMention, propriétaire
- Clés de session de groupe : Clés de session de groupe, diffusion en éventail, mentions sortantes et invite de groupe
- Envois de texte sortants : Envois de texte sortants, livraison d'outil de message, DM/groupe/infolettre explicite
- Reçus acceptés par le fournisseur : Reçus acceptés par le fournisseur et identifiants de livraison durables

Docs principaux :

- `docs/channels/whatsapp.md`
- `docs/channels/group-messages.md`

### 4. Médias et Contenu Enrichi

Ancres de recherche : pièces jointes médias et voix whatsapp, pièces jointes médias et voix.

Note de catégorie : [Médias et Contenu Enrichi](media-attachments-and-voice.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Stable (80%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Téléchargement de médias entrants : Téléchargement de médias entrants et construction d'espace réservé, extraction de médias cités et remise de fichier.
- Image sortante : Image, audio, vidéo, document et construction de charge utile de note vocale sortants.

Docs principaux :

- `docs/channels/whatsapp.md`

### 5. Contrôles Natifs et Approbations

Ancres de recherche : approbations et réactions natives whatsapp, approbations et réactions natives.

Note de catégorie : [Contrôles Natifs et Approbations](native-approvals-and-reactions.md)

Décisions de notation :

- Couverture : `Beta (78%)`
- Qualité : `Stable (84%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Exécution native : Exécution native et livraison d'approbation de plugin via WhatsApp
- Résolution de la cible de l'approbateur : Résolution de la cible de l'approbateur, admissibilité de la cible DM/groupe, suppression de route et livraison d'approbation.

Docs principaux :

- `docs/channels/whatsapp.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, les docs et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/whatsapp/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/whatsapp`.
