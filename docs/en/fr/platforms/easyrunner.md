---
summary: "Exécutez la passerelle OpenClaw sur EasyRunner avec Podman et Caddy"
read_when:
  - Déploiement d'OpenClaw sur EasyRunner
  - Exécution de la passerelle derrière le proxy Caddy d'EasyRunner
  - Choix des volumes persistants et de l'authentification pour une passerelle hébergée
title: "EasyRunner"
---

EasyRunner peut héberger la passerelle OpenClaw en tant qu'application conteneurisée derrière son proxy Caddy. Ce guide suppose un hôte EasyRunner qui exécute des applications Compose compatibles avec Podman et expose HTTPS via Caddy.

## Avant de commencer

- Un serveur EasyRunner avec un domaine routé vers celui-ci.
- Une image de conteneur OpenClaw construite ou publiée.
- Un volume de configuration persistant pour `/home/node/.openclaw`.
- Un volume d'espace de travail persistant pour `/workspace`.
- Un jeton de passerelle ou un mot de passe fort.

Gardez l'authentification des appareils activée si possible. Si votre déploiement de proxy inverse ne peut pas transporter correctement l'identité de l'appareil, corrigez d'abord les paramètres de proxy de confiance ; utilisez les contournements d'authentification dangereux uniquement pour un réseau entièrement privé contrôlé par l'opérateur.

## Application Compose

Créez une application EasyRunner avec un fichier Compose structuré comme ceci :

```yaml
services:
  openclaw:
    image: ghcr.io/openclaw/openclaw:latest
    restart: unless-stopped
    environment:
      OPENCLAW_GATEWAY_TOKEN: ${OPENCLAW_GATEWAY_TOKEN}
      OPENCLAW_HOME: /home/node
      OPENCLAW_STATE_DIR: /home/node/.openclaw
      OPENCLAW_CONFIG_PATH: /home/node/.openclaw/openclaw.json
      OPENCLAW_WORKSPACE_DIR: /workspace
    volumes:
      - openclaw-config:/home/node/.openclaw
      - openclaw-workspace:/workspace
    labels:
      caddy: openclaw.example.com
      caddy.reverse_proxy: "{{upstreams 1455}}"
    command: ["openclaw", "gateway", "--bind", "lan", "--port", "1455"]

volumes:
  openclaw-config:
  openclaw-workspace:
```

Remplacez `openclaw.example.com` par le nom d'hôte de votre passerelle. Stockez `OPENCLAW_GATEWAY_TOKEN` dans le gestionnaire de secrets/environnement d'EasyRunner au lieu de le valider dans la définition de l'application.

## Configurer OpenClaw

À l'intérieur du volume de configuration persistant, gardez la passerelle accessible uniquement via le proxy et exigez une authentification :

```json5
{
  gateway: {
    bind: "lan",
    port: 1455,
    auth: {
      token: "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

Si Caddy termine TLS pour la passerelle, configurez les paramètres de proxy de confiance pour le chemin exact du proxy plutôt que de désactiver les vérifications d'authentification globalement. Voir [Authentification par proxy de confiance](/fr/gateway/trusted-proxy-auth).

## Vérifier

Depuis votre station de travail :

```bash
openclaw gateway probe --url https://openclaw.example.com --token <token>
openclaw gateway status --url https://openclaw.example.com --token <token>
```

Depuis l'hôte EasyRunner, vérifiez les journaux de l'application pour une passerelle à l'écoute et aucun échec d'authentification SecretRef, plugin ou canal au démarrage.

## Mises à jour et sauvegardes

- Tirez ou construisez la nouvelle image OpenClaw, puis redéployez l'application EasyRunner.
- Sauvegardez le volume `openclaw-config` avant les mises à jour.
- Sauvegardez `openclaw-workspace` si les agents y écrivent des données de projet durables.
- Exécutez `openclaw doctor` après les mises à jour majeures pour détecter les migrations de configuration et les avertissements de service.

## Dépannage

- `gateway probe` ne peut pas se connecter : confirmez que le nom d'hôte Caddy pointe vers l'application et que le conteneur écoute sur `0.0.0.0:1455`.
- L'authentification échoue : faites pivoter le jeton dans les secrets EasyRunner et la commande client local ensemble.
- Les fichiers sont la propriété de root après la restauration : réparez les volumes montés pour que l'utilisateur du conteneur puisse écrire `/home/node/.openclaw` et `/workspace`.
- Les plugins de navigateur ou de canal échouent : vérifiez si les binaires externes requis, la sortie réseau et les identifiants montés sont disponibles à l'intérieur du conteneur.
