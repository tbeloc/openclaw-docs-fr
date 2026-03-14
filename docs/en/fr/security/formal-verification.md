---
title: Vérification formelle (Modèles de sécurité)
summary: Modèles de sécurité vérifiés par machine pour les chemins à plus haut risque d'OpenClaw.
read_when:
  - Reviewing formal security model guarantees or limits
  - Reproducing or updating TLA+/TLC security model checks
permalink: /security/formal-verification/
---

# Vérification formelle (Modèles de sécurité)

Cette page suit les **modèles de sécurité formels** d'OpenClaw (TLA+/TLC aujourd'hui ; plus selon les besoins).

> Note: certains anciens liens peuvent faire référence au nom du projet précédent.

**Objectif (étoile polaire) :** fournir un argument vérifié par machine selon lequel OpenClaw applique sa politique de sécurité prévue (autorisation, isolation de session, gating d'outils et sécurité de configuration erronée), sous des hypothèses explicites.

**Ce que c'est (aujourd'hui) :** une **suite de régression de sécurité** exécutable et pilotée par les attaquants :

- Chaque affirmation a une vérification de modèle exécutable sur un espace d'états fini.
- De nombreuses affirmations ont un **modèle négatif** associé qui produit une trace de contre-exemple pour une classe de bug réaliste.

**Ce que ce n'est pas (encore) :** une preuve qu'« OpenClaw est sécurisé sous tous les aspects » ou que l'implémentation TypeScript complète est correcte.

## Où vivent les modèles

Les modèles sont maintenus dans un dépôt séparé : [vignesh07/openclaw-formal-models](https://github.com/vignesh07/openclaw-formal-models).

## Avertissements importants

- Ce sont des **modèles**, pas l'implémentation TypeScript complète. Une dérive entre le modèle et le code est possible.
- Les résultats sont limités par l'espace d'états exploré par TLC ; « vert » n'implique pas la sécurité au-delà des hypothèses et limites modélisées.
- Certaines affirmations reposent sur des hypothèses environnementales explicites (par exemple, déploiement correct, entrées de configuration correctes).

## Reproduire les résultats

Aujourd'hui, les résultats sont reproduits en clonant le dépôt de modèles localement et en exécutant TLC (voir ci-dessous). Une itération future pourrait offrir :

- Modèles exécutés en CI avec artefacts publics (traces de contre-exemple, journaux d'exécution)
- un flux de travail « exécuter ce modèle » hébergé pour les vérifications petites et bornées

Pour commencer :

```bash
git clone https://github.com/vignesh07/openclaw-formal-models
cd openclaw-formal-models

# Java 11+ requis (TLC s'exécute sur la JVM).
# Le dépôt fournit un `tla2tools.jar` épinglé (outils TLA+) et fournit `bin/tlc` + cibles Make.

make <target>
```

### Exposition de la passerelle et configuration erronée de la passerelle ouverte

**Affirmation :** la liaison au-delà de loopback sans authentification peut rendre la compromission à distance possible / augmente l'exposition ; token/password bloque les attaquants non authentifiés (selon les hypothèses du modèle).

- Exécutions vertes :
  - `make gateway-exposure-v2`
  - `make gateway-exposure-v2-protected`
- Rouge (attendu) :
  - `make gateway-exposure-v2-negative`

Voir aussi : `docs/gateway-exposure-matrix.md` dans le dépôt de modèles.

### Pipeline nodes.run (capacité à plus haut risque)

**Affirmation :** `nodes.run` nécessite (a) une liste blanche de commandes de nœud plus des commandes déclarées et (b) une approbation en direct lorsqu'elle est configurée ; les approbations sont tokenisées pour prévenir la relecture (dans le modèle).

- Exécutions vertes :
  - `make nodes-pipeline`
  - `make approvals-token`
- Rouge (attendu) :
  - `make nodes-pipeline-negative`
  - `make approvals-token-negative`

### Magasin d'appairage (gating DM)

**Affirmation :** les demandes d'appairage respectent le TTL et les limites de demandes en attente.

- Exécutions vertes :
  - `make pairing`
  - `make pairing-cap`
- Rouge (attendu) :
  - `make pairing-negative`
  - `make pairing-cap-negative`

### Gating d'entrée (mentions + contournement de commande de contrôle)

**Affirmation :** dans les contextes de groupe nécessitant une mention, une « commande de contrôle » non autorisée ne peut pas contourner le gating de mention.

- Vert :
  - `make ingress-gating`
- Rouge (attendu) :
  - `make ingress-gating-negative`

### Isolation du routage/clé de session

**Affirmation :** les DM de pairs distincts ne s'effondrent pas dans la même session sauf s'ils sont explicitement liés/configurés.

- Vert :
  - `make routing-isolation`
- Rouge (attendu) :
  - `make routing-isolation-negative`

## v1++ : modèles bornés supplémentaires (concurrence, tentatives, correction de trace)

Ce sont des modèles de suivi qui resserrent la fidélité autour des modes de défaillance du monde réel (mises à jour non atomiques, tentatives et fan-out de messages).

### Concurrence/idempotence du magasin d'appairage

**Affirmation :** un magasin d'appairage doit appliquer `MaxPending` et l'idempotence même sous les entrelacages (c'est-à-dire que « vérifier-puis-écrire » doit être atomique / verrouillé ; l'actualisation ne doit pas créer de doublons).

Ce que cela signifie :

- Sous des demandes concurrentes, vous ne pouvez pas dépasser `MaxPending` pour un canal.
- Les demandes/actualisations répétées pour le même `(channel, sender)` ne doivent pas créer de lignes en attente en direct en double.

- Exécutions vertes :
  - `make pairing-race` (vérification de cap atomique/verrouillée)
  - `make pairing-idempotency`
  - `make pairing-refresh`
  - `make pairing-refresh-race`
- Rouge (attendu) :
  - `make pairing-race-negative` (course de cap begin/commit non atomique)
  - `make pairing-idempotency-negative`
  - `make pairing-refresh-negative`
  - `make pairing-refresh-race-negative`

### Corrélation/idempotence de trace d'entrée

**Affirmation :** l'ingestion doit préserver la corrélation de trace sur le fan-out et être idempotente sous les tentatives du fournisseur.

Ce que cela signifie :

- Lorsqu'un événement externe devient plusieurs messages internes, chaque partie conserve la même identité de trace/événement.
- Les tentatives ne résultent pas en double traitement.
- Si les ID d'événement du fournisseur sont manquants, la déduplication revient à une clé sûre (par exemple, ID de trace) pour éviter de perdre des événements distincts.

- Vert :
  - `make ingress-trace`
  - `make ingress-trace2`
  - `make ingress-idempotency`
  - `make ingress-dedupe-fallback`
- Rouge (attendu) :
  - `make ingress-trace-negative`
  - `make ingress-trace2-negative`
  - `make ingress-idempotency-negative`
  - `make ingress-dedupe-fallback-negative`

### Précédence dmScope de routage + identityLinks

**Affirmation :** le routage doit maintenir les sessions DM isolées par défaut, et ne fusionner les sessions que lorsqu'elles sont explicitement configurées (précédence de canal + liens d'identité).

Ce que cela signifie :

- Les remplacements dmScope spécifiques au canal doivent l'emporter sur les valeurs par défaut globales.
- identityLinks doit fusionner uniquement dans les groupes explicitement liés, pas entre les pairs non liés.

- Vert :
  - `make routing-precedence`
  - `make routing-identitylinks`
- Rouge (attendu) :
  - `make routing-precedence-negative`
  - `make routing-identitylinks-negative`
