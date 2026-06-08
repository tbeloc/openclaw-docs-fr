---
title: "Rapport de maturité Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (62%)`
- Fonctionnalités LTS : `0/4`

## Résumé

Ce rapport promeut les preuves archivées `mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat` de `/Users/kevinlin/tmp/maturity/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat` dans le contrat d'inventaire actuel de la version 3 du processus.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                  | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer         |
| -------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | --------------------------------- |
| [Configuration et opérations des canaux](channel-setup-and-operations.md)  | ❌  | `Alpha (62%)` | `Alpha (58%)` | `Alpha (62%)` | Configuration et opérations des canaux |
| [Accès et identité](access-and-identity.md)                               | ❌  | `Alpha (62%)` | `Alpha (58%)` | `Alpha (62%)` | Accès et identité                 |
| [Routage et livraison des conversations](conversation-routing-and-delivery.md) | ❌  | `Alpha (62%)` | `Alpha (58%)` | `Alpha (62%)` | Routage et livraison des conversations |
| [Médias et contenu enrichi](media-and-rich-content.md)                    | ❌  | `Alpha (62%)` | `Alpha (58%)` | `Alpha (62%)` | Médias et contenu enrichi         |

## Rubrique de notation

- Couverture :
  évaluation du label de maturité pour l'intégration, e2e, live ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation du label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et du flux runtime réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation du label de maturité pour la façon dont la catégorie livre l'ensemble
  des capacités spécifiques à la surface prévues. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `qualité > 80 et couverture > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations des canaux

Ancres de recherche : mattermost, line, irc, nextcloud talk, nostr, twitch, tlon, synology chat configuration et opérations des canaux, configuration et opérations des canaux.

Note de catégorie : [Configuration et opérations des canaux](channel-setup-and-operations.md)

Décisions de notation :

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Configuration et opérations des canaux : Étendue des preuves pour la configuration et les opérations des canaux.

Documentation principale :

### 2. Accès et identité

Ancres de recherche : mattermost, line, irc, nextcloud talk, nostr, twitch, tlon, synology chat accès et identité, accès et identité.

Note de catégorie : [Accès et identité](access-and-identity.md)

Décisions de notation :

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Accès et identité : Étendue des preuves pour l'accès et l'identité.

Documentation principale :

### 3. Routage et livraison des conversations

Ancres de recherche : mattermost, line, irc, nextcloud talk, nostr, twitch, tlon, synology chat routage et livraison des conversations, routage et livraison des conversations.

Note de catégorie : [Routage et livraison des conversations](conversation-routing-and-delivery.md)

Décisions de notation :

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Routage et livraison des conversations : Étendue des preuves pour le routage et la livraison des conversations.

Documentation principale :

### 4. Médias et contenu enrichi

Ancres de recherche : mattermost, line, irc, nextcloud talk, nostr, twitch, tlon, synology chat médias et contenu enrichi, médias et contenu enrichi.

Note de catégorie : [Médias et contenu enrichi](media-and-rich-content.md)

Décisions de notation :

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Médias et contenu enrichi : Étendue des preuves pour les médias et le contenu enrichi.

Documentation principale :

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat`.
