---
summary: "Hub réseau : surfaces de passerelle, appairage, découverte et sécurité"
read_when:
  - You need the network architecture + security overview
  - You are debugging local vs tailnet access or pairing
  - You want the canonical list of networking docs
title: "Network"
---

# Hub réseau

Ce hub relie les documents essentiels expliquant comment OpenClaw se connecte, appaire et sécurise les appareils sur localhost, LAN et tailnet.

## Modèle fondamental

- [Architecture de passerelle](/fr/concepts/architecture)
- [Protocole de passerelle](/fr/gateway/protocol)
- [Guide opérationnel de passerelle](/fr/gateway)
- [Surfaces web + modes de liaison](/fr/web)

## Appairage + identité

- [Aperçu de l'appairage (DM + nœuds)](/fr/channels/pairing)
- [Appairage de nœud détenu par la passerelle](/fr/gateway/pairing)
- [CLI Devices (appairage + rotation de jetons)](/fr/cli/devices)
- [CLI Pairing (approbations DM)](/fr/cli/pairing)

Confiance locale :

- Les connexions locales (loopback ou l'adresse tailnet propre de l'hôte de passerelle) peuvent être auto-approuvées pour l'appairage afin de maintenir une UX fluide sur le même hôte.
- Les clients tailnet/LAN non locaux nécessitent toujours une approbation d'appairage explicite.

## Découverte + transports

- [Découverte & transports](/fr/gateway/discovery)
- [Bonjour / mDNS](/fr/gateway/bonjour)
- [Accès à distance (SSH)](/fr/gateway/remote)
- [Tailscale](/fr/gateway/tailscale)

## Nœuds + transports

- [Aperçu des nœuds](/fr/nodes)
- [Protocole Bridge (nœuds hérités)](/fr/gateway/bridge-protocol)
- [Guide opérationnel des nœuds : iOS](/fr/platforms/ios)
- [Guide opérationnel des nœuds : Android](/fr/platforms/android)

## Sécurité

- [Aperçu de la sécurité](/fr/gateway/security)
- [Référence de configuration de passerelle](/fr/gateway/configuration)
- [Dépannage](/fr/gateway/troubleshooting)
- [Doctor](/fr/gateway/doctor)
