---
summary: "Comment les entrées de présence OpenClaw sont produites, fusionnées et affichées"
read_when:
  - Debugging the Instances tab
  - Investigating duplicate or stale instance rows
  - Changing gateway WS connect or system-event beacons
title: "Presence"
---

# Presence

La "presence" OpenClaw est une vue légère et au mieux effort de :

- la **Gateway** elle-même, et
- les **clients connectés à la Gateway** (app mac, WebChat, CLI, etc.)

La presence est utilisée principalement pour afficher l'onglet **Instances** de l'app macOS et pour
fournir une visibilité rapide aux opérateurs.

## Champs de presence (ce qui s'affiche)

Les entrées de presence sont des objets structurés avec des champs comme :

- `instanceId` (optionnel mais fortement recommandé) : identité client stable (généralement `connect.client.instanceId`)
- `host` : nom d'hôte convivial
- `ip` : adresse IP au mieux effort
- `version` : chaîne de version du client
- `deviceFamily` / `modelIdentifier` : indices matériels
- `mode` : `ui`, `webchat`, `cli`, `backend`, `probe`, `test`, `node`, ...
- `lastInputSeconds` : "secondes depuis la dernière entrée utilisateur" (si connue)
- `reason` : `self`, `connect`, `node-connected`, `periodic`, ...
- `ts` : timestamp de la dernière mise à jour (ms depuis epoch)

## Producteurs (d'où vient la presence)

Les entrées de presence sont produites par plusieurs sources et **fusionnées**.

### 1) Entrée self de la Gateway

La Gateway amorce toujours une entrée "self" au démarrage afin que les UIs affichent l'hôte gateway
même avant que des clients ne se connectent.

### 2) Connexion WebSocket

Chaque client WS commence par une requête `connect`. Lors de la poignée de main réussie, la
Gateway upsert une entrée de presence pour cette connexion.

#### Pourquoi les commandes CLI ponctuelles ne s'affichent pas

Le CLI se connecte souvent pour des commandes ponctuelles courtes. Pour éviter de spammer la
liste Instances, `client.mode === "cli"` n'est **pas** transformé en entrée de presence.

### 3) Balises `system-event`

Les clients peuvent envoyer des balises périodiques plus riches via la méthode `system-event`. L'app mac
l'utilise pour signaler le nom d'hôte, l'IP et `lastInputSeconds`.

### 4) Connexions de nœud (role: node)

Quand un nœud se connecte sur la WebSocket Gateway avec `role: node`, la Gateway
upsert une entrée de presence pour ce nœud (même flux que les autres clients WS).

## Règles de fusion + déduplication (pourquoi `instanceId` est important)

Les entrées de presence sont stockées dans une seule carte en mémoire :

- Les entrées sont indexées par une **clé de presence**.
- La meilleure clé est un `instanceId` stable (de `connect.client.instanceId`) qui survit aux redémarrages.
- Les clés sont insensibles à la casse.

Si un client se reconnecte sans un `instanceId` stable, il peut s'afficher comme une
ligne **dupliquée**.

## TTL et taille limitée

La presence est intentionnellement éphémère :

- **TTL :** les entrées plus anciennes que 5 minutes sont supprimées
- **Entrées max :** 200 (les plus anciennes supprimées en premier)

Cela garde la liste fraîche et évite une croissance mémoire illimitée.

## Caveat distant/tunnel (IPs loopback)

Quand un client se connecte via un tunnel SSH / redirection de port local, la Gateway peut
voir l'adresse distante comme `127.0.0.1`. Pour éviter de remplacer une bonne IP signalée par le client,
les adresses distantes loopback sont ignorées.

## Consommateurs

### Onglet Instances macOS

L'app mac affiche la sortie de `system-presence` et applique un petit indicateur de statut
(Active/Idle/Stale) basé sur l'âge de la dernière mise à jour.

## Conseils de débogage

- Pour voir la liste brute, appelez `system-presence` contre la Gateway.
- Si vous voyez des doublons :
  - confirmez que les clients envoient un `client.instanceId` stable dans la poignée de main
  - confirmez que les balises périodiques utilisent le même `instanceId`
  - vérifiez si l'entrée dérivée de la connexion manque `instanceId` (les doublons sont attendus)
