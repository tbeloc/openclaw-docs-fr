---
read_when:
  - Vous devez comprendre l'architecture réseau et l'aperçu de la sécurité
  - Vous déboguez des problèmes d'accès local, d'accès tailnet ou d'appairage
  - Vous souhaitez obtenir une liste faisant autorité de la documentation réseau
summary: Centre réseau : interfaces Gateway, appairage, découverte de périphériques et sécurité
title: Réseau
x-i18n:
  generated_at: "2026-02-03T10:07:45Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0fe4e7dbc8ddea312c8f3093af9b6bc71d9ae4007df76ae24b85889871933bc8
  source_path: network.md
  workflow: 15
---

# Centre réseau

Ce centre rassemble la documentation centrale sur la façon dont OpenClaw se connecte, s'appaire et sécurise les périphériques entre localhost, le réseau local et tailnet.

## Modèle fondamental

- [Architecture Gateway](/concepts/architecture)
- [Protocole Gateway](/gateway/protocol)
- [Manuel opérationnel Gateway](/gateway)
- [Interface Web + modes de liaison](/web)

## Appairage + Identité

- [Aperçu de l'appairage (messages privés + nœuds)](/channels/pairing)
- [Appairage de nœuds possédés par Gateway](/gateway/pairing)
- [CLI Devices (appairage + rotation de token)](/cli/devices)
- [CLI Pairing (approbation des messages privés)](/cli/pairing)

Confiance locale :

- Les connexions locales (loopback ou adresse tailnet du host Gateway lui-même) peuvent approuver automatiquement l'appairage pour maintenir une expérience utilisateur fluide sur le même host.
- Les clients tailnet/réseau local non locaux nécessitent toujours une approbation d'appairage explicite.

## Découverte de périphériques + protocoles de transport

- [Découverte de périphériques et protocoles de transport](/gateway/discovery)
- [Bonjour / mDNS](/gateway/bonjour)
- [Accès à distance (SSH)](/gateway/remote)
- [Tailscale](/gateway/tailscale)

## Nœuds + protocoles de transport

- [Aperçu des nœuds](/nodes)
- [Protocole de pont (nœuds hérités)](/gateway/bridge-protocol)
- [Manuel opérationnel des nœuds : iOS](/platforms/ios)
- [Manuel opérationnel des nœuds : Android](/platforms/android)

## Sécurité

- [Aperçu de la sécurité](/gateway/security)
- [Référence de configuration Gateway](/gateway/configuration)
- [Dépannage](/gateway/troubleshooting)
- [Doctor](/gateway/doctor)
