```markdown
---
summary: "VPS hosting hub for OpenClaw (Oracle/Fly/Hetzner/GCP/exe.dev)"
read_when:
  - You want to run the Gateway in the cloud
  - You need a quick map of VPS/hosting guides
title: "VPS Hosting"
---

# Hébergement VPS

Ce hub relie les guides d'hébergement VPS/cloud pris en charge et explique le fonctionnement des déploiements cloud à haut niveau.

## Choisir un fournisseur

- **Railway** (configuration en un clic + navigateur) : [Railway](/install/railway)
- **Northflank** (configuration en un clic + navigateur) : [Northflank](/install/northflank)
- **Oracle Cloud (Always Free)** : [Oracle](/platforms/oracle) — 0 $/mois (Always Free, ARM ; la capacité/inscription peut être capricieuse)
- **Fly.io** : [Fly.io](/install/fly)
- **Hetzner (Docker)** : [Hetzner](/install/hetzner)
- **GCP (Compute Engine)** : [GCP](/install/gcp)
- **exe.dev** (VM + proxy HTTPS) : [exe.dev](/install/exe-dev)
- **AWS (EC2/Lightsail/free tier)** : fonctionne bien aussi. Guide vidéo :
  [https://x.com/techfrenAJ/status/2014934471095812547](https://x.com/techfrenAJ/status/2014934471095812547)

## Fonctionnement des configurations cloud

- La **Gateway s'exécute sur le VPS** et possède l'état + l'espace de travail.
- Vous vous connectez depuis votre ordinateur portable/téléphone via l'**interface de contrôle** ou **Tailscale/SSH**.
- Traitez le VPS comme la source de vérité et **sauvegardez** l'état + l'espace de travail.
- Sécurité par défaut : gardez la Gateway sur la boucle locale et accédez-y via un tunnel SSH ou Tailscale Serve.
  Si vous liez à `lan`/`tailnet`, exigez `gateway.auth.token` ou `gateway.auth.password`.

Accès à distance : [Gateway remote](/gateway/remote)  
Hub des plateformes : [Platforms](/platforms)

## Agent d'entreprise partagé sur un VPS

C'est une configuration valide lorsque les utilisateurs se trouvent dans une même limite de confiance (par exemple une équipe d'entreprise), et l'agent est réservé aux activités professionnelles.

- Gardez-le sur un runtime dédié (VPS/VM/conteneur + utilisateur/comptes OS dédiés).
- Ne connectez pas ce runtime à des comptes Apple/Google personnels ou à des profils de navigateur/gestionnaire de mots de passe personnels.
- Si les utilisateurs sont adversaires les uns envers les autres, divisez par gateway/host/utilisateur OS.

Détails du modèle de sécurité : [Security](/gateway/security)

## Utilisation de nœuds avec un VPS

Vous pouvez garder la Gateway dans le cloud et associer des **nœuds** sur vos appareils locaux
(Mac/iOS/Android/headless). Les nœuds fournissent des capacités d'écran/caméra/canevas locales et `system.run`
tandis que la Gateway reste dans le cloud.

Documentation : [Nodes](/nodes), [Nodes CLI](/cli/nodes)

## Optimisation du démarrage pour les petites VM et les hôtes ARM

Si les commandes CLI semblent lentes sur les VM basse puissance (ou les hôtes ARM), activez le cache de compilation du module Node :

```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

- `NODE_COMPILE_CACHE` améliore les temps de démarrage des commandes répétées.
- `OPENCLAW_NO_RESPAWN=1` évite les frais de démarrage supplémentaires d'un chemin d'auto-respawn.
- La première exécution de commande réchauffe le cache ; les exécutions suivantes sont plus rapides.
- Pour les spécificités de Raspberry Pi, voir [Raspberry Pi](/platforms/raspberry-pi).

### Liste de contrôle d'optimisation systemd (optionnel)

Pour les hôtes VM utilisant `systemd`, considérez :

- Ajouter l'env de service pour un chemin de démarrage stable :
  - `OPENCLAW_NO_RESPAWN=1`
  - `NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache`
- Gardez le comportement de redémarrage explicite :
  - `Restart=always`
  - `RestartSec=2`
  - `TimeoutStartSec=90`
- Préférez les disques sauvegardés par SSD pour les chemins d'état/cache afin de réduire les pénalités de démarrage à froid d'E/S aléatoires.

Exemple :

```bash
sudo systemctl edit openclaw
```

```ini
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
TimeoutStartSec=90
```

Comment les politiques `Restart=` aident à la récupération automatisée :
[systemd can automate service recovery](https://www.redhat.com/en/blog/systemd-automate-recovery).
```
