---
summary: "Comment acheminer le trafic HTTP et WebSocket du runtime OpenClaw via un proxy de filtrage géré par l'opérateur"
title: "Proxy réseau"
read_when:
  - You want defense-in-depth against SSRF and DNS rebinding attacks
  - Configuring an external forward proxy for OpenClaw runtime traffic
---

# Proxy réseau

OpenClaw peut acheminer le trafic HTTP et WebSocket du runtime via un proxy direct géré par l'opérateur. Il s'agit d'une défense optionnelle en profondeur pour les déploiements qui souhaitent un contrôle d'accès centralisé, une meilleure protection SSRF et une meilleure auditabilité du réseau.

OpenClaw ne fournit pas, ne télécharge pas, ne démarre pas, ne configure pas et ne certifie pas de proxy. Vous exécutez la technologie de proxy qui convient à votre environnement, et OpenClaw achemine les clients HTTP et WebSocket locaux normaux via celui-ci.

## Pourquoi utiliser un proxy ?

Un proxy donne aux opérateurs un point de contrôle réseau unique pour le trafic HTTP et WebSocket sortant. Cela peut être utile même en dehors du renforcement SSRF :

- Politique centralisée : maintenir une politique d'accès unique au lieu de compter sur chaque site d'appel HTTP d'application pour appliquer correctement les règles réseau.
- Vérifications au moment de la connexion : évaluer la destination après la résolution DNS et immédiatement avant que le proxy n'ouvre la connexion en amont.
- Défense contre le rebinding DNS : réduire l'écart entre une vérification DNS au niveau de l'application et la connexion sortante réelle.
- Couverture JavaScript plus large : acheminer les clients `fetch`, `node:http`, `node:https`, WebSocket, axios, got, node-fetch et similaires ordinaires via le même chemin.
- Auditabilité : enregistrer les destinations autorisées et refusées à la limite d'accès.
- Contrôle opérationnel : appliquer les règles de destination, la segmentation réseau, les limites de débit ou les listes blanches d'accès sans reconstruire OpenClaw.

OpenClaw conserve toujours les gardes SSRF au niveau de l'application telles que `fetchWithSsrFGuard`. L'acheminement via proxy est une barrière de sécurité supplémentaire au niveau du processus pour l'accès HTTP et WebSocket normal, et non un remplacement pour les récupérations gardées ou un bac à sable réseau au niveau du système d'exploitation.

## Comment OpenClaw achemine le trafic

Lorsque `proxy.enabled=true` et qu'une URL de proxy est configurée, les processus runtime protégés tels que `openclaw gateway run`, `openclaw node run` et `openclaw agent --local` acheminent l'accès HTTP et WebSocket normal via le proxy configuré :

```text
Processus OpenClaw
  fetch                  -> proxy de filtrage géré par l'opérateur -> internet public
  node:http et https     -> proxy de filtrage géré par l'opérateur -> internet public
  Clients WebSocket      -> proxy de filtrage géré par l'opérateur -> internet public
```

Le contrat public est le comportement d'acheminement, et non les hooks Node internes utilisés pour l'implémenter. Les clients WebSocket du plan de contrôle OpenClaw Gateway utilisent un chemin direct étroit pour le trafic RPC Gateway loopback local lorsque l'URL Gateway utilise une adresse loopback littérale telle que `127.0.0.1` ou `[::1]`. Ce chemin du plan de contrôle doit pouvoir atteindre les Gateways loopback même lorsque le proxy de l'opérateur bloque les destinations loopback. Les requêtes HTTP et WebSocket normales du runtime utilisent toujours le proxy configuré.

L'URL du proxy elle-même doit utiliser `http://`. Les destinations HTTPS sont toujours supportées via le proxy avec HTTP `CONNECT` ; cela signifie seulement qu'OpenClaw s'attend à un écouteur de proxy direct HTTP simple tel que `http://127.0.0.1:3128`.

Pendant que le proxy est actif, OpenClaw efface `no_proxy`, `NO_PROXY` et `GLOBAL_AGENT_NO_PROXY`. Ces listes de contournement sont basées sur la destination, donc laisser `localhost` ou `127.0.0.1` là-dedans permettrait aux cibles SSRF à haut risque de contourner le proxy de filtrage.

À l'arrêt, OpenClaw restaure l'environnement proxy précédent et réinitialise l'état d'acheminement du processus en cache.

## Configuration

```yaml
proxy:
  enabled: true
  proxyUrl: http://127.0.0.1:3128
```

Vous pouvez également fournir l'URL via l'environnement, tout en gardant `proxy.enabled=true` dans la configuration :

```bash
OPENCLAW_PROXY_URL=http://127.0.0.1:3128 openclaw gateway run
```

`proxy.proxyUrl` a la priorité sur `OPENCLAW_PROXY_URL`.

Si `enabled=true` mais qu'aucune URL de proxy valide n'est configurée, les commandes protégées échouent au démarrage au lieu de revenir à l'accès réseau direct.

Pour les services de passerelle gérés démarrés avec `openclaw gateway start`, préférez stocker l'URL dans la configuration :

```bash
openclaw config set proxy.enabled true
openclaw config set proxy.proxyUrl http://127.0.0.1:3128
openclaw gateway install --force
openclaw gateway start
```

Le recours à l'environnement est préférable pour les exécutions au premier plan. Si vous l'utilisez avec un service installé, mettez `OPENCLAW_PROXY_URL` dans l'environnement durable du service, tel que `$OPENCLAW_STATE_DIR/.env` ou `~/.openclaw/.env`, puis réinstallez le service afin que launchd, systemd ou Scheduled Tasks démarre la passerelle avec cette valeur.

Pour les commandes `openclaw --container ...`, OpenClaw transfère `OPENCLAW_PROXY_URL` dans l'interface CLI enfant ciblée par le conteneur lorsqu'elle est définie. L'URL doit être accessible de l'intérieur du conteneur ; `127.0.0.1` fait référence au conteneur lui-même, et non à l'hôte. OpenClaw rejette les URL de proxy loopback pour les commandes ciblées par conteneur à moins que vous ne remplaciez explicitement cette vérification de sécurité.

## Exigences du proxy

La politique du proxy est la limite de sécurité. OpenClaw ne peut pas vérifier que le proxy bloque les bonnes cibles.

Configurez le proxy pour :

- Se lier uniquement à loopback ou à une interface privée de confiance.
- Restreindre l'accès afin que seul le processus OpenClaw, l'hôte, le conteneur ou le compte de service puisse l'utiliser.
- Résoudre les destinations lui-même et bloquer les adresses IP de destination après la résolution DNS.
- Appliquer la politique au moment de la connexion pour les requêtes HTTP simples et les tunnels HTTPS `CONNECT`.
- Rejeter les contournements basés sur la destination pour les plages loopback, privées, link-local, métadonnées, multidiffusion, réservées ou de documentation.
- Éviter les listes blanches de noms d'hôte à moins que vous ne fassiez entièrement confiance au chemin de résolution DNS.
- Enregistrer la destination, la décision, l'état et la raison sans enregistrer les corps de requête, les en-têtes d'autorisation, les cookies ou d'autres secrets.
- Maintenir la politique du proxy sous contrôle de version et examiner les modifications comme une configuration sensible à la sécurité.

## Destinations bloquées recommandées

Utilisez cette liste de refus comme point de départ pour tout proxy direct, pare-feu ou politique d'accès.

La logique de classification au niveau de l'application OpenClaw se trouve dans `src/infra/net/ssrf.ts` et `src/shared/net/ip.ts`. Les hooks de parité pertinents sont `BLOCKED_HOSTNAMES`, `BLOCKED_IPV4_SPECIAL_USE_RANGES`, `BLOCKED_IPV6_SPECIAL_USE_RANGES`, `RFC2544_BENCHMARK_PREFIX` et la gestion des sentinelles IPv4 intégrées pour NAT64, 6to4, Teredo, ISATAP et les formes mappées IPv4. Ces fichiers sont des références utiles lors de la maintenance d'une politique de proxy externe, mais OpenClaw n'exporte pas ou n'applique pas automatiquement ces règles dans votre proxy.

| Plage ou hôte                                                                        | Raison du blocage                                    |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| `127.0.0.0/8`, `localhost`, `localhost.localdomain`                                  | Loopback IPv4                                        |
| `::1/128`                                                                            | Loopback IPv6                                        |
| `0.0.0.0/8`, `::/128`                                                                | Adresses non spécifiées et de ce réseau              |
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`                                      | Réseaux privés RFC1918                               |
| `169.254.0.0/16`, `fe80::/10`                                                        | Adresses link-local et chemins de métadonnées cloud courants |
| `169.254.169.254`, `metadata.google.internal`                                        | Services de métadonnées cloud                        |
| `100.64.0.0/10`                                                                      | Espace d'adresses partagées NAT de classe opérateur  |
| `198.18.0.0/15`, `2001:2::/48`                                                       | Plages d'évaluation                                  |
| `192.0.0.0/24`, `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32` | Plages d'usage spécial et de documentation          |
| `224.0.0.0/4`, `ff00::/8`                                                            | Multidiffusion                                       |
| `240.0.0.0/4`                                                                        | IPv4 réservé                                         |
| `fc00::/7`, `fec0::/10`                                                              | Plages locales/privées IPv6                          |
| `100::/64`, `2001:20::/28`                                                           | Plages IPv6 de rejet et ORCHIDv2                     |
| `64:ff9b::/96`, `64:ff9b:1::/48`                                                     | Préfixes NAT64 avec IPv4 intégré                     |
| `2002::/16`, `2001::/32`                                                             | 6to4 et Teredo avec IPv4 intégré                     |
| `::/96`, `::ffff:0:0/96`                                                             | IPv6 compatible IPv4 et mappé IPv4                   |

Si votre fournisseur cloud ou plateforme réseau documente des hôtes de métadonnées ou des plages réservées supplémentaires, ajoutez-les également.

## Validation

Validez le proxy à partir du même hôte, conteneur ou compte de service qui exécute OpenClaw :

```bash
curl -x http://127.0.0.1:3128 https://example.com/
curl -x http://127.0.0.1:3128 http://127.0.0.1/
curl -x http://127.0.0.1:3128 http://169.254.169.254/
```

La requête publique devrait réussir. Les requêtes loopback et métadonnées devraient échouer au proxy.

Ensuite, activez l'acheminement du proxy OpenClaw :

```bash
openclaw config set proxy.enabled true
openclaw config set proxy.proxyUrl http://127.0.0.1:3128
openclaw gateway run
```

ou définissez :

```yaml
proxy:
  enabled: true
  proxyUrl: http://127.0.0.1:3128
```

## Limites

- Le proxy améliore la couverture pour les clients HTTP et WebSocket JavaScript locaux au processus, mais il ne remplace pas `fetchWithSsrFGuard` au niveau de l'application.
- Les sockets `net`, `tls` et `http2` bruts, les modules natifs et les processus enfants peuvent contourner l'acheminement du proxy au niveau Node à moins qu'ils n'héritent et ne respectent les variables d'environnement du proxy.
- Les interfaces utilisateur Web locales et les serveurs de modèles locaux doivent être mis en liste blanche dans la politique de proxy de l'opérateur si nécessaire ; OpenClaw n'expose pas de contournement général du réseau local pour eux.
- Le contournement du proxy du plan de contrôle Gateway est intentionnellement limité aux URL d'adresses IP loopback littérales. Utilisez `ws://127.0.0.1:18789` ou `ws://[::1]:18789` pour les connexions directes du plan de contrôle Gateway locales ; les noms d'hôte `localhost` s'acheminent comme le trafic ordinaire basé sur le nom d'hôte.
- OpenClaw n'inspecte pas, ne teste pas et ne certifie pas votre politique de proxy.
- Traitez les modifications de politique de proxy comme des modifications opérationnelles sensibles à la sécurité.
