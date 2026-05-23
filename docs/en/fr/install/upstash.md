---
summary: "Héberger OpenClaw sur Upstash Box avec support keep-alive et accès par tunnel SSH"
read_when:
  - Déployer OpenClaw sur Upstash Box
  - Vous voulez un environnement Linux géré pour OpenClaw avec accès au tableau de bord via tunnel SSH
title: "Upstash Box"
---

Exécutez une passerelle OpenClaw persistante sur Upstash Box, un environnement Linux géré
avec support du cycle de vie keep-alive.

Utilisez un tunnel SSH pour accéder au tableau de bord. N'exposez pas le port de la passerelle directement
à l'internet public.

## Prérequis

- Compte Upstash
- Box Upstash avec keep-alive
- Client SSH sur votre machine locale

## Créer une Box

Créez une Box avec keep-alive dans la console Upstash. Notez l'ID de la Box, par exemple
`right-flamingo-14486`, et votre clé API Box.

Upstash maintient sa procédure pas à pas actuelle pour OpenClaw Box à
[Configuration OpenClaw](https://upstash.com/docs/box/guides/openclaw-setup).

## Se connecter avec un tunnel SSH

Transférez le port du tableau de bord OpenClaw vers votre machine locale. Utilisez votre clé API Box
comme mot de passe SSH lorsque vous y êtes invité :

```bash
ssh -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -L 18789:127.0.0.1:18789 <box-id>@us-east-1.box.upstash.com
```

Les options keepalive réduisent les interruptions de tunnel inactif pendant l'intégration.

## Installer OpenClaw

À l'intérieur de la Box :

```bash
sudo npm install -g openclaw
```

## Exécuter l'intégration

```bash
openclaw onboard --install-daemon
```

Suivez les invites. Copiez l'URL du tableau de bord et le jeton lorsque l'intégration est terminée.

## Démarrer la passerelle

Configurez la passerelle pour le réseau Box et démarrez-la en arrière-plan :

```bash
openclaw config set gateway.bind lan
nohup openclaw gateway > gateway.log 2>&1 &
```

Avec le tunnel SSH actif, ouvrez l'URL du tableau de bord localement :

```text
http://127.0.0.1:18789/#token=<your-token>
```

## Redémarrage automatique

Définissez cette commande comme script d'initialisation de la Box pour que la passerelle redémarre au démarrage de la Box :

```bash
nohup openclaw gateway > gateway.log 2>&1 &
```

## Dépannage

Si SSH se fige pendant l'intégration, reconnectez-vous avec une configuration SSH propre et
des keepalives :

```bash
ssh -F /dev/null -o ControlMaster=no -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -L 18789:127.0.0.1:18789 <box-id>@us-east-1.box.upstash.com
```

Cela contourne les paramètres obsolètes de `~/.ssh/config` locaux et maintient le tunnel actif
pendant les périodes d'inactivité réseau.

## Connexes

- [Accès à distance](/fr/gateway/remote)
- [Sécurité de la passerelle](/fr/gateway/security)
- [Mise à jour d'OpenClaw](/fr/install/updating)
