---
summary: "Appairage détenu par la passerelle (Option B) pour iOS et autres nœuds distants"
read_when:
  - Implementing node pairing approvals without macOS UI
  - Adding CLI flows for approving remote nodes
  - Extending gateway protocol with node management
title: "Appairage détenu par la passerelle"
---

# Appairage détenu par la passerelle (Option B)

Dans l'appairage détenu par la passerelle, la **Passerelle** est la source de vérité pour déterminer quels nœuds sont autorisés à rejoindre. Les interfaces utilisateur (application macOS, futurs clients) ne sont que des frontends qui approuvent ou rejettent les demandes en attente.

**Important :** Les nœuds WS utilisent l'**appairage d'appareil** (rôle `node`) lors de `connect`.
`node.pair.*` est un magasin d'appairage séparé et ne **gère pas** la poignée de main WS.
Seuls les clients qui appellent explicitement `node.pair.*` utilisent ce flux.

## Concepts

- **Demande en attente** : un nœud a demandé à rejoindre ; nécessite une approbation.
- **Nœud apparié** : nœud approuvé avec un jeton d'authentification émis.
- **Transport** : le point de terminaison WS de la Passerelle transfère les demandes mais ne décide pas de l'adhésion. (Le support du pont TCP hérité est obsolète/supprimé.)

## Fonctionnement de l'appairage

1. Un nœud se connecte à la Passerelle WS et demande l'appairage.
2. La Passerelle stocke une **demande en attente** et émet `node.pair.requested`.
3. Vous approuvez ou rejetez la demande (CLI ou interface utilisateur).
4. En cas d'approbation, la Passerelle émet un **nouveau jeton** (les jetons sont renouvelés lors du réappairage).
5. Le nœud se reconnecte en utilisant le jeton et est maintenant « apparié ».

Les demandes en attente expirent automatiquement après **5 minutes**.

## Flux CLI (convivial pour les environnements sans interface)

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"
```

`nodes status` affiche les nœuds appairés/connectés et leurs capacités.

## Surface API (protocole de passerelle)

Événements :

- `node.pair.requested` — émis lorsqu'une nouvelle demande en attente est créée.
- `node.pair.resolved` — émis lorsqu'une demande est approuvée/rejetée/expirée.

Méthodes :

- `node.pair.request` — créer ou réutiliser une demande en attente.
- `node.pair.list` — lister les nœuds en attente + appairés.
- `node.pair.approve` — approuver une demande en attente (émet un jeton).
- `node.pair.reject` — rejeter une demande en attente.
- `node.pair.verify` — vérifier `{ nodeId, token }`.

Remarques :

- `node.pair.request` est idempotent par nœud : les appels répétés retournent la même
  demande en attente.
- L'approbation **génère toujours** un jeton nouveau ; aucun jeton n'est jamais retourné par
  `node.pair.request`.
- Les demandes peuvent inclure `silent: true` comme indice pour les flux d'approbation automatique.

## Approbation automatique (application macOS)

L'application macOS peut éventuellement tenter une **approbation silencieuse** lorsque :

- la demande est marquée `silent`, et
- l'application peut vérifier une connexion SSH à l'hôte de la passerelle en utilisant le même utilisateur.

Si l'approbation silencieuse échoue, elle revient à l'invite normale « Approuver/Rejeter ».

## Stockage (local, privé)

L'état d'appairage est stocké dans le répertoire d'état de la Passerelle (par défaut `~/.openclaw`) :

- `~/.openclaw/nodes/paired.json`
- `~/.openclaw/nodes/pending.json`

Si vous remplacez `OPENCLAW_STATE_DIR`, le dossier `nodes/` se déplace avec lui.

Notes de sécurité :

- Les jetons sont des secrets ; traitez `paired.json` comme sensible.
- La rotation d'un jeton nécessite une réapprobation (ou la suppression de l'entrée du nœud).

## Comportement du transport

- Le transport est **sans état** ; il ne stocke pas l'adhésion.
- Si la Passerelle est hors ligne ou si l'appairage est désactivé, les nœuds ne peuvent pas s'appairer.
- Si la Passerelle est en mode distant, l'appairage se fait toujours par rapport au magasin de la Passerelle distante.
