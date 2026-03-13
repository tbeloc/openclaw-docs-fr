---
read_when:
  - Implémenter l'approbation d'appairage de nœuds sans interface utilisateur macOS
  - Ajouter un flux CLI pour approuver les nœuds distants
  - Étendre le protocole Gateway pour supporter la gestion des nœuds
summary: Appairage détenu par Gateway (option B), pour iOS et autres nœuds distants
title: Appairage détenu par Gateway
x-i18n:
  generated_at: "2026-02-03T07:48:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1f5154292a75ea2c1470324babc99c6c46a5e4e16afb394ed323d28f6168f459
  source_path: gateway/pairing.md
  workflow: 15
---

# Appairage détenu par Gateway (Option B)

Dans l'appairage détenu par Gateway, **Gateway** est la seule source d'autorité pour décider quels nœuds peuvent rejoindre. L'interface utilisateur (application macOS, clients futurs) n'est qu'un frontend pour approuver ou rejeter les demandes en attente.

**Important :** Les nœuds WS utilisent l'**appairage d'appareil** (rôle `node`) pendant `connect`. `node.pair.*` est un stockage d'appairage indépendant qui **ne limite pas** la poignée de main WS. Seuls les clients qui appellent explicitement `node.pair.*` utilisent ce flux.

## Concepts

- **Demande en attente** : Un nœud demande à rejoindre ; nécessite approbation.
- **Nœud apparié** : Un nœud approuvé avec un jeton d'authentification émis.
- **Couche transport** : Le point de terminaison WS de Gateway transfère les demandes mais ne décide pas de l'adhésion. (Le support du pont TCP hérité est déprécié/supprimé.)

## Fonctionnement de l'appairage

1. Un nœud se connecte à Gateway WS et demande l'appairage.
2. Gateway stocke une **demande en attente** et émet `node.pair.requested`.
3. Vous approuvez ou rejetez la demande (CLI ou interface utilisateur).
4. Après approbation, Gateway émet un **nouveau jeton** (les jetons sont renouvelés lors du réappairage).
5. Le nœud se reconnecte avec ce jeton, maintenant à l'état "apparié".

Les demandes en attente expirent automatiquement après **5 minutes**.

## Flux CLI (support du mode sans tête)

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"
```

`nodes status` affiche les nœuds appairés/connectés et leurs capacités.

## Interface API (Protocole Gateway)

Événements :

- `node.pair.requested` — Émis lors de la création d'une nouvelle demande en attente.
- `node.pair.resolved` — Émis quand une demande est approuvée/rejetée/expirée.

Méthodes :

- `node.pair.request` — Crée ou réutilise une demande en attente.
- `node.pair.list` — Liste les nœuds en attente + appairés.
- `node.pair.approve` — Approuve une demande en attente (émet un jeton).
- `node.pair.reject` — Rejette une demande en attente.
- `node.pair.verify` — Vérifie `{ nodeId, token }`.

Remarques :

- `node.pair.request` est idempotent par nœud : les appels répétés retournent la même demande en attente.
- L'approbation **génère toujours** un nouveau jeton ; `node.pair.request` ne retourne jamais de jeton.
- Les demandes peuvent inclure `silent: true` comme indication pour un flux d'approbation automatique.

## Approbation automatique (Application macOS)

L'application macOS peut choisir de tenter une **approbation silencieuse** quand :

- La demande est marquée `silent`, et
- L'application peut authentifier une connexion SSH au host Gateway avec le même utilisateur.

Si l'approbation silencieuse échoue, elle revient à l'invite normale "approuver/rejeter".

## Stockage (Local, Privé)

L'état d'appairage est stocké dans le répertoire d'état de Gateway (par défaut `~/.openclaw`) :

- `~/.openclaw/nodes/paired.json`
- `~/.openclaw/nodes/pending.json`

Si vous avez remplacé `OPENCLAW_STATE_DIR`, le dossier `nodes/` se déplace avec lui.

Considérations de sécurité :

- Les jetons sont confidentiels ; traitez `paired.json` comme un fichier sensible.
- La rotation des jetons nécessite une réapprobation (ou la suppression de l'entrée du nœud).

## Comportement de la couche transport

- La couche transport est **sans état** ; elle ne stocke pas l'adhésion.
- Si Gateway est hors ligne ou l'appairage désactivé, les nœuds ne peuvent pas s'appairer.
- Si Gateway est en mode distant, l'appairage cible toujours le stockage du Gateway distant.
