---
permalink: /security/formal-verification/
summary: Vérification de sécurité par machine pour les chemins à risque maximal d'OpenClaw.
title: Vérification formelle (modèle de sécurité)
x-i18n:
  generated_at: "2026-02-03T07:54:04Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8dff6ea41a37fb6b870424e4e788015c3f8a6099075eece5dbf909883c045106
  source_path: security/formal-verification.md
  workflow: 15
---

# Vérification formelle (modèle de sécurité)

Cette page suit le **modèle de sécurité formelle** d'OpenClaw (actuellement TLA+/TLC ; d'autres seront ajoutés selon les besoins).

> Remarque : certains anciens liens peuvent faire référence à des noms de projets antérieurs.

**Objectif (étoile polaire) :** Fournir un argument vérifié par machine démontrant qu'OpenClaw exécute ses
politiques de sécurité prévues sous des hypothèses explicites (autorisation, isolation de session, contrôle d'accès aux outils et
sécurité en cas de configuration erronée).

**État actuel :** Une suite de **tests de régression de sécurité** exécutable et pilotée par les attaquants :

- Chaque affirmation a une vérification de modèle s'exécutant sur un espace d'états fini.
- De nombreuses affirmations ont un **modèle négatif** appairé générant des traces de contre-exemple pour des catégories de bugs réalistes.

**Ce que ce n'est pas :** Une preuve qu'« OpenClaw est sûr sous tous les aspects » ou que l'implémentation TypeScript complète est correcte.

## Où se trouvent les modèles

Les modèles sont maintenus dans un référentiel séparé : [vignesh07/openclaw-formal-models](https://github.com/vignesh07/openclaw-formal-models).

## Remarques importantes

- Ce sont des **modèles**, pas l'implémentation TypeScript complète. Des écarts entre le modèle et le code peuvent exister.
- Les résultats sont limités par l'espace d'états exploré par TLC ; « vert » ne signifie pas que c'est sûr au-delà des hypothèses et limites modélisées.
- Certaines affirmations dépendent d'hypothèses environnementales explicites (par exemple, déploiement correct, entrées de configuration correctes).

## Reproduire les résultats

Actuellement, les résultats sont reproduits en clonant localement le référentiel de modèles et en exécutant TLC (voir ci-dessous). Les itérations futures pourraient fournir :

- Des exécutions de modèles CI avec des artefacts publics (traces de contre-exemple, journaux d'exécution)
- Des flux de travail « Exécuter ce modèle » hébergés pour des vérifications petites et bornées

Pour commencer :

```bash
git clone https://github.com/vignesh07/openclaw-formal-models
cd openclaw-formal-models

# Nécessite Java 11+ (TLC s'exécute sur la JVM).
# Le référentiel inclut une version fixe de `tla2tools.jar` (outils TLA+) et fournit `bin/tlc` + cibles Make.

make <target>
```

### Exposition de la passerelle et configuration erronée de la passerelle ouverte

**Affirmation :** La liaison en dehors de loopback sans authentification peut permettre une compromission à distance / augmenter l'exposition ; les jetons/mots de passe peuvent bloquer les attaquants non authentifiés (selon les hypothèses du modèle).

- Exécutions vertes :
  - `make gateway-exposure-v2`
  - `make gateway-exposure-v2-protected`
- Rouges (attendues) :
  - `make gateway-exposure-v2-negative`

Voir aussi : `docs/gateway-exposure-matrix.md` dans le référentiel de modèles.

### Pipeline nodes.run (capacité à risque maximal)

**Affirmation :** `nodes.run` nécessite (a) une liste d'autorisation de commandes de nœud plus la commande déclarée et (b) une approbation en temps réel au moment de la configuration ; les approbations sont tokenisées pour prévenir la relecture (dans le modèle).

- Exécutions vertes :
  - `make nodes-pipeline`
  - `make approvals-token`
- Rouges (attendues) :
  - `make nodes-pipeline-negative`
  - `make approvals-token-negative`

### Stockage d'appairage (contrôle d'accès aux messages privés)

**Affirmation :** Les demandes d'appairage respectent la TTL et la limite de demandes en attente.

- Exécutions vertes :
  - `make pairing`
  - `make pairing-cap`
- Rouges (attendues) :
  - `make pairing-negative`
  - `make pairing-cap-negative`

### Contrôle d'entrée (mention + contournement de commande de contrôle)

**Affirmation :** Dans les contextes de groupe nécessitant une mention, les « commandes de contrôle » non autorisées ne peuvent pas contourner le contrôle de mention.

- Vert :
  - `make ingress-gating`
- Rouges (attendues) :
  - `make ingress-gating-negative`

### Isolation du routage/clé de session

**Affirmation :** Les messages privés de différents pairs ne s'effondrent pas dans la même session, sauf s'ils sont explicitement liés/configurés.

- Vert :
  - `make routing-isolation`
- Rouges (attendues) :
  - `make routing-isolation-negative`

## v1++ : modèles bornés supplémentaires (concurrence, nouvelles tentatives, exactitude du suivi)

Ce sont des modèles de suivi, augmentant la fidélité autour des modes de défaillance du monde réel (mises à jour non atomiques, nouvelles tentatives et fan-out de messages).

### Concurrence du stockage d'appairage / idempotence

**Affirmation :** Le stockage d'appairage doit appliquer `MaxPending` et l'idempotence même dans les cas entrelacés (c'est-à-dire que « vérifier puis écrire » doit être atomique/verrouillé ; l'actualisation ne doit pas créer de doublons).

Cela signifie :

- Sous les demandes concurrentes, vous ne pouvez pas dépasser le `MaxPending` du canal.
- Les demandes/actualisations en double pour le même `(channel, sender)` ne doivent pas créer de lignes en attente actives en double.

- Exécutions vertes :
  - `make pairing-race`(vérification de limite atomique/verrouillée)
  - `make pairing-idempotency`
  - `make pairing-refresh`
  - `make pairing-refresh-race`
- Rouges (attendues) :
  - `make pairing-race-negative`(course de limite begin/commit non atomique)
  - `make pairing-idempotency-negative`
  - `make pairing-refresh-negative`
  - `make pairing-refresh-race-negative`

### Association de suivi d'entrée / idempotence

**Affirmation :** L'ingestion doit maintenir l'association de suivi lors du fan-out et rester idempotente sous les nouvelles tentatives du fournisseur.

Cela signifie :

- Quand un événement externe devient plusieurs messages internes, chaque partie conserve le même suivi/ID d'événement.
- Les nouvelles tentatives ne causent pas de traitement en double.
- Si l'ID d'événement du fournisseur est manquant, la déduplification revient à une clé sûre (par exemple, ID de suivi) pour éviter de rejeter des événements différents.

- Vert :
  - `make ingress-trace`
  - `make ingress-trace2`
  - `make ingress-idempotency`
  - `make ingress-dedupe-fallback`
- Rouges (attendues) :
  - `make ingress-trace-negative`
  - `make ingress-trace2-negative`
  - `make ingress-idempotency-negative`
  - `make ingress-dedupe-fallback-negative`

### Priorité dmScope de routage + identityLinks

**Affirmation :** Le routage doit maintenir par défaut l'isolation de session des messages privés, en ne s'effondrant que lorsqu'explicitement configuré (priorité de canal + liens d'identité).

Cela signifie :

- Les remplacements dmScope spécifiques au canal doivent avoir priorité sur les valeurs par défaut globales.
- Les identityLinks ne doivent s'effondrer que dans les groupes explicitement liés, pas entre les pairs non liés.

- Vert :
  - `make routing-precedence`
  - `make routing-identitylinks`
- Rouges (attendues) :
  - `make routing-precedence-negative`
  - `make routing-identitylinks-negative`
