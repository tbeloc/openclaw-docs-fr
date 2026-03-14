---
read_when:
  - 你想要简要了解 Gateway 网关的网络模型
summary: Gateway 网关、节点和 canvas 主机如何连接。
title: 网络模型
x-i18n:
  generated_at: "2026-02-04T17:53:21Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e3508b884757ef19f425c82e891e2b07e7fd7d985413d569e55ae9b175c91f0f
  source_path: gateway/network-model.md
  workflow: 15
---

La plupart des opérations sont effectuées via la passerelle Gateway (`openclaw gateway`), qui est un processus unique de longue durée responsable de la gestion des connexions de canal et du plan de contrôle WebSocket.

## Règles fondamentales

- Il est recommandé d'exécuter une passerelle Gateway par hôte. C'est le seul processus autorisé à posséder une session WhatsApp Web. Pour les scénarios de bot de sauvetage ou d'isolation stricte, plusieurs passerelles Gateway peuvent être exécutées avec des fichiers de configuration et des ports isolés. Voir [Passerelles Gateway multiples](/gateway/multiple-gateways).
- Privilégiez l'adresse de bouclage : le WS de la passerelle Gateway est par défaut `ws://127.0.0.1:18789`. Même pour les connexions de bouclage, l'assistant génère par défaut un jeton de passerelle. Pour accéder via tailnet, exécutez `openclaw gateway --bind tailnet --token ...`, car les liaisons non-bouclage doivent utiliser un jeton.
- Les nœuds se connectent au WS de la passerelle Gateway selon les besoins via le réseau local, tailnet ou SSH. Le pont TCP hérité est obsolète.
- L'hôte Canvas est un serveur de fichiers HTTP s'exécutant sur `canvasHost.port` (par défaut `18793`), fournissant le chemin `/__openclaw__/canvas/` pour utilisation par WebView des nœuds. Voir [Configuration de la passerelle Gateway](/gateway/configuration) (`canvasHost`).
- L'utilisation à distance se fait généralement via un tunnel SSH ou un VPN Tailscale. Voir [Accès à distance](/gateway/remote) et [Découverte d'appareils](/gateway/discovery).
