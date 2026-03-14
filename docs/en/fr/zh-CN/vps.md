---
read_when:
  - 你想在云端运行 Gateway 网关
  - 你需要 VPS/托管指南的快速索引
summary: OpenClaw 的 VPS 托管中心（Oracle/Fly/Hetzner/GCP/exe.dev）
title: VPS 托管
x-i18n:
  generated_at: "2026-02-03T10:12:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 7749b479b333aa5541e7ad8b0ff84e9f8f6bd10d7188285121975cb893acc037
  source_path: vps.md
  workflow: 15
---

# Hébergement VPS

Ce centre relie vers les guides VPS/hébergement pris en charge et explique à haut niveau le fonctionnement du déploiement cloud.

## Choisir un fournisseur

- **Railway** (un clic + configuration navigateur) : [Railway](/install/railway)
- **Northflank** (un clic + configuration navigateur) : [Northflank](/install/northflank)
- **Oracle Cloud (gratuit à perpétuité)** : [Oracle](/platforms/oracle) — 0 $/mois (gratuit à perpétuité, ARM ; la capacité/l'inscription peut être un peu instable)
- **Fly.io** : [Fly.io](/install/fly)
- **Hetzner (Docker)** : [Hetzner](/install/hetzner)
- **GCP (Compute Engine)** : [GCP](/install/gcp)
- **exe.dev** (VM + proxy HTTPS) : [exe.dev](/install/exe-dev)
- **AWS (EC2/Lightsail/forfait gratuit)** : fonctionne également bien. Guide vidéo :
  https://x.com/techfrenAJ/status/2014934471095812547

## Comment fonctionne la configuration cloud

- **Gateway s'exécute sur le VPS** et possède l'état + les espaces de travail.
- Vous vous connectez depuis votre ordinateur portable/téléphone via l'**interface de contrôle** ou **Tailscale/SSH**.
- Considérez le VPS comme une source de données et **sauvegardez** l'état + les espaces de travail.
- Sécurité par défaut : gardez Gateway sur la boucle locale, accédez via tunnel SSH ou Tailscale Serve.
  Si vous vous liez à `lan`/`tailnet`, vous avez besoin de `gateway.auth.token` ou `gateway.auth.password`.

Accès à distance : [Accès à distance Gateway](/gateway/remote)
Centre des plateformes : [Plateformes](/platforms)

## Utiliser des nœuds sur un VPS

Vous pouvez garder Gateway dans le cloud et appairer des **nœuds** sur des appareils locaux (Mac/iOS/Android/sans tête). Les nœuds fournissent l'écran/caméra/canvas locaux et la fonctionnalité `system.run`, tandis que Gateway reste dans le cloud.

Documentation : [Nœuds](/nodes), [CLI Nœuds](/cli/nodes)
