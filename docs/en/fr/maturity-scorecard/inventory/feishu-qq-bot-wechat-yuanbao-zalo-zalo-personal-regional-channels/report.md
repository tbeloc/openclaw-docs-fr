---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux Rapport de maturité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux Rapport de maturité

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Expérimental (43%)`
- Qualité : `Expérimental (47%)`
- Complétude : `Expérimental (43%)`
- Fonctionnalités LTS : `0/4`

## Résumé

Ce rapport promeut les preuves de maturité archivées `feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels` de `/Users/kevinlin/tmp/maturity/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels` dans le contrat d'inventaire actuel process-version-3.

Les scores de catégorie Couverture et Qualité proviennent des lignes de score archivées soutenues par des preuves. La Complétude est initialisée à partir de la même largeur de preuve archivée et du registre des lacunes connues, puis jointe au rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                          | LTS | Couverture           | Qualité              | Complétude           | Fonctionnalités à évaluer                                                                                                                                                             |
| --------------------------------------------------------------------------------- | --- | -------------------- | -------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration et opérations des canaux](shared-regional-channel-catalog-install-status.md) | ❌  | `Expérimental (42%)` | `Expérimental (44%)` | `Expérimental (42%)` | Index des canaux de documentation, Entrées du catalogue de canaux externes officiels, Catalogue principal canal-plugin, Assistant de configuration des canaux, Plugin manquant, Préoccupations d'ingress/accès/refactorisation entre canaux |
| [Accès et identité](access-and-identity.md)                                     | ❌  | `Expérimental (42%)` | `Expérimental (44%)` | `Expérimental (42%)` | Accès et identité                                                                                                                                                              |
| [Routage et livraison des conversations](conversation-routing-and-delivery.md)         | ❌  | `Expérimental (42%)` | `Expérimental (44%)` | `Expérimental (42%)` | Routage et livraison des conversations                                                                                                                                                |
| [Médias et contenu enrichi](media-and-rich-content.md)                               | ❌  | `Expérimental (47%)` | `Alpha (55%)`        | `Expérimental (47%)` | Médias et contenu enrichi                                                                                                                                                           |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, live, ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et du flux runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement l'ensemble
  de capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `qualité > 80 et couverture > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité plus élevé.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations des canaux

Ancres de recherche : feishu, qq bot, wechat, yuanbao, zalo, zalo personal, regional channels feishu, qq bot, wechat, yuanbao, zalo, zalo personal, regional channels matrice des fonctionnalités : catalogue de canaux régionaux partagés, installation et statut, feishu, qq bot, wechat, yuanbao, zalo, zalo personal, regional channels matrice des fonctionnalités : catalogue de canaux régionaux partagés, installation et statut.

Note de catégorie : [Configuration et opérations des canaux](shared-regional-channel-catalog-install-status.md)

Décisions de notation :

- Couverture : `Expérimental (42%)`
- Qualité : `Expérimental (44%)`
- Complétude : `Expérimental (42%)`
- LTS : ❌

Fonctionnalités :

- Index des canaux de documentation : Index des canaux de documentation, pages de référence des plugins, redirections et liste de support d'appairage pour les canaux régionaux
- Entrées du catalogue de canaux externes officiels : Entrées du catalogue de canaux externes officiels pour WeCom, Yuanbao, Weixin et canaux externes adjacents
- Catalogue principal canal-plugin : Catalogue principal canal-plugin, normalisation des alias, résolution du plan d'installation, drapeaux de source de confiance, indices de réparation et sortie de statut/liste
- Assistant de configuration des canaux : Assistant de configuration des canaux et blurbs i18n pour les canaux régionaux
- Plugin manquant : Plugin manquant, plugin obsolète, mise à niveau brute du gestionnaire de paquets et chemins de docteur/réparation
- Préoccupations d'ingress/accès/refactorisation entre canaux : Préoccupations d'ingress/accès/refactorisation entre canaux pour les plugins régionaux

Documentation principale :

- `docs/channels/index.md`
- `docs/channels/pairing.md`
- `docs/plugins/reference/feishu.md`
- `docs/plugins/architecture-internals.md`

### 2. Accès et identité

Ancres de recherche : feishu, qq bot, wechat, yuanbao, zalo, zalo personal, regional channels accès et identité, accès et identité.

Note de catégorie : [Accès et identité](access-and-identity.md)

Décisions de notation :

- Couverture : `Expérimental (42%)`
- Qualité : `Expérimental (44%)`
- Complétude : `Expérimental (42%)`
- LTS : ❌

Fonctionnalités :

- Accès et identité : Portée des preuves pour Accès et identité.

Documentation principale :

### 3. Routage et livraison des conversations

Ancres de recherche : feishu, qq bot, wechat, yuanbao, zalo, zalo personal, regional channels routage et livraison des conversations, routage et livraison des conversations.

Note de catégorie : [Routage et livraison des conversations](conversation-routing-and-delivery.md)

Décisions de notation :

- Couverture : `Expérimental (42%)`
- Qualité : `Expérimental (44%)`
- Complétude : `Expérimental (42%)`
- LTS : ❌

Fonctionnalités :

- Routage et livraison des conversations : Portée des preuves pour Routage et livraison des conversations.

Documentation principale :

### 4. Médias et contenu enrichi

Ancres de recherche : feishu, qq bot, wechat, yuanbao, zalo, zalo personal, regional channels médias et contenu enrichi, médias et contenu enrichi.

Note de catégorie : [Médias et contenu enrichi](media-and-rich-content.md)

Décisions de notation :

- Couverture : `Expérimental (47%)`
- Qualité : `Alpha (55%)`
- Complétude : `Expérimental (47%)`
- LTS : ❌

Fonctionnalités :

- Médias et contenu enrichi : Portée des preuves pour Médias et contenu enrichi.

Documentation principale :

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels`.
