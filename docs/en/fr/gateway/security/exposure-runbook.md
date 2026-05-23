---
summary: "Liste de contrôle de pré-vol et de restauration avant d'exposer une passerelle OpenClaw au-delà de la boucle locale"
title: "Runbook d'exposition de la passerelle"
sidebarTitle: "Runbook d'exposition"
read_when:
  - Exposer la passerelle sur LAN, tailnet, Tailscale Serve, Funnel, ou un proxy inverse
  - Examiner un déploiement avant d'autoriser les utilisateurs de messagerie réels
  - Restaurer une configuration d'accès à distance ou de messagerie directe risquée
---

<Warning>
Exposez la passerelle uniquement après avoir pu expliquer qui peut y accéder, comment ils sont
authentifiés, quels agents ils peuvent déclencher, et quels outils ces agents peuvent
utiliser. En cas de doute, revenez à l'accès en boucle locale uniquement et relancez l'audit.
</Warning>

Ce runbook transforme les conseils de sécurité plus larges [Security](/fr/gateway/security) en
liste de contrôle d'opérateur pour l'accès à distance et l'exposition de la messagerie.

## Choisir le modèle d'exposition

Préférez le modèle le plus restrictif qui satisfait le flux de travail.

| Modèle                     | Recommandé quand                                | Contrôles requis                                                                                    |
| -------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Boucle locale + tunnel SSH | Utilisation personnelle, accès administrateur, débogage | Gardez `gateway.bind: "loopback"` et tunnel `127.0.0.1:18789`                                      |
| Boucle locale + Tailscale Serve | Accès personnel à tailnet pour Control UI/WebSocket | Gardez la passerelle en boucle locale uniquement ; fiez-vous aux en-têtes d'identité Tailscale uniquement pour les surfaces supportées |
| Liaison Tailnet/LAN        | Réseau privé dédié avec appareils connus       | Auth de passerelle, liste blanche de pare-feu, pas de redirection de port public                   |
| Proxy inverse de confiance | SSO/OIDC organisationnel devant la passerelle   | Auth `trusted-proxy`, `trustedProxies` strict, règles de remplacement/suppression d'en-têtes, utilisateurs autorisés explicites |
| Internet public            | Déploiements rares et à haut risque             | Proxy conscient de l'identité, TLS, limites de débit, listes blanches strictes, sessions non-main en sandbox |

Évitez la redirection de port public directe vers la passerelle. Si vous avez besoin d'un accès public,
placez un proxy conscient de l'identité devant et rendez le proxy le seul chemin réseau
vers la passerelle.

## Inventaire de pré-vol

Enregistrez ces éléments avant de modifier la liaison, le proxy, Tailscale, ou la politique de canal :

- Hôte de passerelle, utilisateur du système d'exploitation, et répertoire d'état.
- URL de passerelle et mode de liaison.
- Mode d'authentification, source de jeton/mot de passe, ou source d'identité de proxy de confiance.
- Tous les canaux activés et s'ils acceptent les DM, les groupes, ou les webhooks.
- Agents accessibles à partir d'expéditeurs non locaux.
- Profil d'outil, mode sandbox, et politique d'outil élevé pour chaque agent accessible.
- Credentials externes disponibles pour ces agents.
- Emplacement de sauvegarde pour `~/.openclaw/openclaw.json` et les credentials.

Si plus d'une personne peut envoyer un message au bot, traitez ceci comme une autorité d'outil déléguée partagée,
non comme une isolation d'hôte par utilisateur.

## Vérifications de base

Exécutez ces vérifications avant d'ouvrir l'accès :

```bash
openclaw doctor
openclaw security audit
openclaw security audit --deep
openclaw health
```

Résolvez d'abord les résultats critiques. Les avertissements peuvent être acceptables uniquement s'ils sont
intentionnels et documentés pour le déploiement.

Pour la validation CLI à distance, transmettez les credentials explicitement :

```bash
openclaw gateway probe --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

Ne supposez pas que les credentials de configuration locale s'appliquent à une URL distante explicite.

## Ligne de base minimale sûre

Utilisez cette structure comme point de départ pour les déploiements exposés :

```json5
{
  gateway: {
    bind: "loopback",
    auth: {
      mode: "token",
      token: "replace-with-a-long-random-token",
    },
  },
  session: {
    dmScope: "per-channel-peer",
  },
  agents: {
    defaults: {
      sandbox: { mode: "non-main" },
    },
  },
  tools: {
    profile: "messaging",
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
}
```

Ensuite, élargissez un contrôle à la fois. Par exemple, ajoutez une liste blanche de canal spécifique
avant d'activer les outils capables d'écriture, ou activez un proxy inverse avant d'accepter
le trafic Control UI distant.

La ligne de base stricte `exec.security: "deny"` bloque tous les appels exec, y compris
les diagnostics bénins. Si les diagnostics ou les commandes à faible risque sont requis, assouplissez ceci
uniquement après avoir choisi les expéditeurs spécifiques, les agents, les commandes, et le mode d'approbation
qui correspondent à votre modèle de menace.

## Exposition DM et groupe

Les canaux de messagerie sont des surfaces d'entrée non fiables. Avant d'autoriser les DM ou les groupes :

- Préférez `dmPolicy: "pairing"` ou des listes `allowFrom` strictes.
- Évitez `dmPolicy: "open"` sauf si chaque expéditeur est de confiance.
- Ne combinez pas les listes blanches `"*"` avec un accès aux outils large.
- Exigez des mentions dans les groupes sauf si la salle est étroitement contrôlée.
- Utilisez `session.dmScope: "per-channel-peer"` quand plusieurs personnes peuvent envoyer un DM au bot.
- Routez les canaux partagés vers les agents avec des outils minimaux et aucune credential personnelle.

L'appairage approuve l'expéditeur pour déclencher le bot. Cela ne fait pas de cet expéditeur une
limite de sécurité d'hôte séparée.

## Vérifications de proxy inverse

Pour les proxies conscients de l'identité :

- Le proxy doit authentifier les utilisateurs avant de transférer vers la passerelle.
- L'accès direct au port de la passerelle doit être bloqué par le pare-feu ou la politique réseau.
- `gateway.trustedProxies` doit contenir uniquement les adresses IP source du proxy.
- Le proxy doit supprimer ou réécrire les en-têtes d'identité et de redirection fournis par le client.
- `gateway.auth.trustedProxy.allowUsers` doit lister les utilisateurs attendus quand le proxy sert plus d'une audience.
- Le mode proxy loopback sur le même hôte doit utiliser `allowLoopback` uniquement quand les processus locaux sont de confiance et le proxy possède les en-têtes d'identité.

Exécutez `openclaw security audit --deep` après les modifications de proxy. Les résultats de trusted-proxy
sont intentionnellement à haut signal car le proxy devient la limite d'authentification.

## Examen des outils et du sandbox

Avant d'exposer un agent aux expéditeurs distants :

- Confirmez quelles sessions s'exécutent sur l'hôte par rapport au sandbox.
- Refusez ou exigez l'approbation pour l'exec d'hôte.
- Gardez les outils élevés désactivés sauf si un expéditeur spécifique et de confiance en a besoin.
- Évitez les outils de navigateur, canvas, node, cron, gateway, et session-spawn pour les surfaces de messagerie ouvertes ou semi-ouvertes.
- Gardez les montages de liaison étroits et évitez les chemins de credential, home, Docker socket, et système.
- Utilisez des passerelles, des utilisateurs du système d'exploitation, ou des hôtes séparés pour les limites de confiance matériellement différentes.

Si les utilisateurs distants ne sont pas entièrement de confiance, l'isolation doit provenir de déploiements séparés,
non seulement de prompts ou d'étiquettes de session.

## Validation post-modification

Après chaque modification d'exposition :

1. Relancez `openclaw security audit --deep`.
2. Testez une connexion autorisée réussie.
3. Testez qu'un expéditeur non autorisé ou une session de navigateur est refusée.
4. Confirmez que les logs masquent les secrets.
5. Confirmez que le routage DM/groupe atteint uniquement l'agent prévu.
6. Confirmez que les outils à haut impact demandent l'approbation ou sont refusés.
7. Documentez les avertissements résiduels acceptés.

Ne procédez pas à la modification d'exposition suivante jusqu'à ce que la modification actuelle soit comprise.

## Plan de restauration

Si la passerelle peut être surexposée :

```json5
{
  gateway: {
    bind: "loopback",
  },
  channels: {
    whatsapp: { dmPolicy: "disabled" },
    telegram: { dmPolicy: "disabled" },
    discord: { dmPolicy: "disabled" },
    slack: { dmPolicy: "disabled" },
  },
  tools: {
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
}
```

Ensuite :

1. Arrêtez la redirection publique, Tailscale Funnel, ou les routes de proxy inverse.
2. Faites tourner les tokens/mots de passe de passerelle et les credentials d'intégration affectés.
3. Supprimez `"*"` et les expéditeurs inattendus des listes blanches.
4. Examinez les logs d'audit récents, l'historique d'exécution, les appels d'outils, et les modifications de configuration.
5. Relancez `openclaw security audit --deep`.
6. Réactivez l'accès avec le modèle le plus restrictif qui satisfait le flux de travail.

## Liste de contrôle d'examen

- La passerelle reste en boucle locale uniquement sauf s'il y a une raison documentée.
- L'accès non-loopback a auth, pare-feu, et aucune route directe publique.
- Les déploiements de trusted-proxy ont des IPs de proxy strictes et des contrôles d'en-têtes.
- Les DM utilisent l'appairage ou les listes blanches, pas l'accès ouvert par défaut.
- Les groupes exigent des mentions ou des listes blanches explicites.
- Les canaux partagés n'atteignent pas les credentials personnelles.
- Les sessions non-main s'exécutent en mode sandbox.
- L'exec d'hôte et les outils élevés sont refusés ou contrôlés par approbation.
- Les logs masquent les secrets.
- Les résultats d'audit critiques sont résolus.
- Les étapes de restauration sont testées et documentées.
