---
summary: "Hub réseau : surfaces de passerelle, appairage, découverte et sécurité"
read_when:
  - You need the network architecture + security overview
  - You are debugging local vs tailnet access or pairing
  - You want the canonical list of networking docs
title: "Network"
---

# Hub réseau

Ce hub relie la documentation principale sur la façon dont OpenClaw se connecte, s'appaire et sécurise les appareils sur localhost, LAN et tailnet.

## Modèle principal

- [Architecture de passerelle](/concepts/architecture)
- [Protocole de passerelle](/gateway/protocol)
- [Guide opérationnel de passerelle](/gateway)
- [Surfaces web + modes de liaison](/web)

## Appairage + identité

- [Aperçu de l'appairage (DM + nœuds)](/channels/pairing)
- [Appairage de nœud détenu par la passerelle](/gateway/pairing)
- [CLI Devices (appairage + rotation de jeton)](/cli/devices)
- [CLI Pairing (approbations DM)](/cli/pairing)

Confiance locale :

- Les connexions locales (loopback ou l'adresse tailnet de l'hôte de la passerelle lui-même) peuvent être approuvées automatiquement pour l'appairage afin de maintenir une UX fluide sur le même hôte.
- Les clients tailnet/LAN non locaux nécessitent toujours une approbation d'appairage explicite.

## Découverte + transports

- [Découverte & transports](/gateway/discovery)
- [Bonjour / mDNS](/gateway/bonjour)
- [Accès à distance (SSH)](/gateway/remote)
- [Tailscale](/gateway/tailscale)

## Nœuds + transports

- [Aperçu des nœuds](/nodes)
- [Protocole Bridge (nœuds hérités)](/gateway/bridge-protocol)
- [Guide opérationnel des nœuds : iOS](/platforms/ios)
- [Guide opérationnel des nœuds : Android](/platforms/android)

## Sécurité

- [Aperçu de la sécurité](/gateway/security)
- [Référence de configuration de passerelle](/gateway/configuration)
- [Dépannage](/gateway/troubleshooting)
- [Doctor](/gateway/doctor)
