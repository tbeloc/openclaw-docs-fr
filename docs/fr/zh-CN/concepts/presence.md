---
read_when:
  - 调试实例标签页
  - 排查重复或过期的实例行
  - 更改 Gateway 网关 WS 连接或系统事件信标
summary: OpenClaw 在线状态条目如何生成、合并和显示
title: 在线状态
x-i18n:
  generated_at: "2026-02-03T07:46:37Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c752c76a880878fed673d656db88beb5dbdeefff2491985127ad791521f97d00
  source_path: concepts/presence.md
  workflow: 15
---

# Présence en ligne

La "présence en ligne" OpenClaw est une vue légère et au mieux de l'effort de :

- **La passerelle Gateway elle-même**, et
- **Les clients connectés à la passerelle Gateway** (application mac, WebChat, CLI, etc.)

La présence en ligne est principalement utilisée pour afficher l'onglet **Instances** de l'application macOS et fournir une visibilité rapide aux opérateurs.

## Champs de présence en ligne (ce qui s'affiche)

Une entrée de présence en ligne est un objet structuré avec les champs suivants :

- `instanceId` (optionnel mais fortement recommandé) : identité client stable (généralement `connect.client.instanceId`)
- `host` : nom d'hôte convivial
- `ip` : adresse IP au mieux de l'effort
- `version` : chaîne de version du client
- `deviceFamily` / `modelIdentifier` : indices matériels
- `mode` : `ui`, `webchat`, `cli`, `backend`, `probe`, `test`, `node`, ...
- `lastInputSeconds` : "secondes depuis la dernière entrée utilisateur" (si connu)
- `reason` : `self`, `connect`, `node-connected`, `periodic`, ...
- `ts` : horodatage de la dernière mise à jour (millisecondes depuis l'époque)

## Producteurs (sources de présence en ligne)

Les entrées de présence en ligne sont générées par plusieurs sources et **fusionnées**.

### 1) Entrée de la passerelle Gateway elle-même

La passerelle Gateway injecte toujours une entrée "self" au démarrage, de sorte que l'interface utilisateur peut afficher l'hôte Gateway même avant que tout client ne se connecte.

### 2) Connexions WebSocket

Chaque client WS commence par une requête `connect`. Après une poignée de main réussie, la passerelle Gateway insère une entrée de présence en ligne mise à jour pour cette connexion.

#### Pourquoi les commandes CLI ponctuelles ne s'affichent pas

Le CLI se connecte souvent pour des commandes ponctuelles éphémères. Pour éviter que la liste des instances ne soit inondée, `client.mode === "cli"` **ne sera pas** converti en entrée de présence en ligne.

### 3) Balises `system-event`

Les clients peuvent envoyer des balises périodiques plus riches via la méthode `system-event`. L'application mac utilise cette méthode pour signaler le nom d'hôte, l'IP et `lastInputSeconds`.

### 4) Connexions de nœuds (role: node)

Lorsqu'un nœud se connecte via WebSocket Gateway avec `role: node`, la passerelle Gateway insère une entrée de présence en ligne mise à jour pour ce nœud (même processus que les autres clients WS).

## Règles de fusion + déduplication (pourquoi `instanceId` est important)

Les entrées de présence en ligne sont stockées dans une seule carte en mémoire :

- Les entrées sont indexées par **clé de présence en ligne**.
- La meilleure clé est l'`instanceId` stable (de `connect.client.instanceId`), qui persiste après les redémarrages.
- La clé n'est pas sensible à la casse.

Si un client se reconnecte sans `instanceId` stable, il peut s'afficher comme une ligne **dupliquée**.

## TTL et taille bornée

La présence en ligne est intentionnellement conçue pour être éphémère :

- **TTL :** Les entrées de plus de 5 minutes sont supprimées
- **Nombre maximum d'entrées :** 200 (les plus anciennes sont supprimées en premier)

Cela maintient la liste fraîche et évite une croissance mémoire illimitée.

## Considérations distantes/tunnel (IP de bouclage)

Lorsqu'un client se connecte via un tunnel SSH/redirection de port local, la passerelle Gateway peut voir l'adresse distante comme `127.0.0.1`. Pour éviter de remplacer une IP valide signalée par le client, les adresses de bouclage distantes sont ignorées.

## Consommateurs

### Onglet Instances macOS

L'application macOS affiche la sortie de `system-presence` et applique un petit indicateur d'état (actif/inactif/expiré) en fonction de l'heure de la dernière mise à jour.

## Conseils de débogage

- Pour voir la liste brute, appelez `system-presence` sur la passerelle Gateway.
- Si vous voyez des doublons :
  - Confirmez que le client envoie un `client.instanceId` stable lors de la poignée de main
  - Confirmez que les balises périodiques utilisent le même `instanceId`
  - Vérifiez si les entrées dérivées de la connexion manquent `instanceId` (dans ce cas, les doublons sont attendus)
