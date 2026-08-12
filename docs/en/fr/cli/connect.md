---
summary: "Connectez une machine à une passerelle OpenClaw avec une seule commande collée"
read_when:
  - Pairing a new headless node with a Gateway
  - Installing a node host from a join URL or setup code
title: "Connect"
---

# `openclaw connect`

Connectez la machine actuelle à une passerelle OpenClaw en tant que nœud sans interface. La
commande utilise une credential d'amorçage de courte durée, enregistre le point de terminaison de la passerelle
dans l'état du nœud-hôte existant, et exécute le même runtime que
[`openclaw node run`](/fr/cli/node).

## Créer une commande de jointure

Sur l'hôte de la passerelle, utilisez les credentials d'administrateur pour générer une URL de jointure à usage unique :

```bash
openclaw devices join-code
```

La commande affiche l'URL et une commande collable :

```bash
npx openclaw connect https://gateway.example/j/<shortcode>
```

Le code court a 128 bits d'entropie, expire avec la credential d'installation après
environ 10 minutes, et ne peut être récupéré qu'une seule fois. Générez un autre code s'il
expire ou a déjà été utilisé.

## Se connecter au premier plan

Collez la commande affichée sur la machine que vous souhaitez connecter :

```bash
npx openclaw connect https://gateway.example/j/<shortcode>
```

Définissez le nom de l'appareil lors de l'inscription si utile :

```bash
npx openclaw connect https://gateway.example/j/<shortcode> --display-name "Build Node"
```

Le nœud reste au premier plan jusqu'à ce que vous l'arrêtiez.

## Installer en tant que service

Passez `--service` pour utiliser la credential d'amorçage et installer le nœud-hôte en tant que
service utilisateur de la plateforme :

```bash
npx openclaw connect https://gateway.example/j/<shortcode> --service
```

OpenClaw complète la première connexion authentifiée avant d'installer le
service. Le token d'amorçage de courte durée n'est jamais stocké dans la commande de service
ou la configuration du nœud-hôte ; les démarrages ultérieurs utilisent le token d'appareil appairé durable.
Utilisez [`openclaw node status`](/fr/cli/node#service-background) pour inspecter le
service installé.

## Cibles acceptées

`openclaw connect <target>` accepte :

- une URL de jointure `https://<gateway>/j/<shortcode>` ;
- une URL `oc-pair://<setup-code>` ;
- un code d'installation base64url nu.

Les URL de jointure doivent utiliser HTTPS. HTTP simple est accepté uniquement pour les URL de passerelle de boucle locale
telles que `http://127.0.0.1/j/<shortcode>`. Les codes d'installation directs peuvent porter l'
empreinte du certificat TLS de la passerelle, ce qui permet au nœud-hôte d'épingler un certificat
de passerelle auto-signé après décodage de la charge utile.

La charge utile détermine l'hôte enregistré, le port, le mode TLS, le chemin du contexte WebSocket,
et les points de terminaison de secours ordonnés. Aucune clé `openclaw.json` supplémentaire n'est créée.

## Comportement de révocation

Un code de jointure et un appareil appairé ont des cycles de vie distincts :

- Brûler ou expirer un code de jointure empêche une autre inscription avec ce code.
- Cela ne déconnecte pas ou ne supprime pas un nœud qui l'a déjà utilisé.
- Pour révoquer une machine inscrite, supprimez son appareil appairé avec
  [`openclaw devices remove <deviceId>`](/fr/cli/devices#openclaw-devices-remove-deviceid).

## Dépannage

Si l'URL de jointure signale qu'elle est manquante ou expirée, générez-en une nouvelle avec
`openclaw devices join-code`. Un code utilisé retourne intentionnellement le même résultat
qu'un code inconnu.

Si une URL de jointure HTTPS utilise un certificat que la machine locale ne fait pas confiance, utilisez
la forme directe `oc-pair://` ou le code d'installation nu qui inclut l'épingle TLS.

Voir [Node](/fr/cli/node) pour la gestion des services, les flags de connexion explicites, l'état du nœud,
et le comportement d'approbation d'exécution.
