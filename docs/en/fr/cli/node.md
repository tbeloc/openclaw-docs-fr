---
summary: "Référence CLI pour `openclaw node` (hôte de nœud sans interface)"
read_when:
  - Running the headless node host
  - Pairing a non-macOS node for system.run
title: "node"
---

# `openclaw node`

Exécutez un **hôte de nœud sans interface** qui se connecte à la passerelle WebSocket et expose
`system.run` / `system.which` sur cette machine.

## Pourquoi utiliser un hôte de nœud ?

Utilisez un hôte de nœud lorsque vous souhaitez que les agents **exécutent des commandes sur d'autres machines** de votre
réseau sans installer une application compagnon macOS complète.

Cas d'usage courants :

- Exécuter des commandes sur des boîtes Linux/Windows distantes (serveurs de compilation, machines de laboratoire, NAS).
- Garder l'exécution **isolée** sur la passerelle, mais déléguer les exécutions approuvées à d'autres hôtes.
- Fournir une cible d'exécution légère et sans interface pour l'automatisation ou les nœuds CI.

L'exécution est toujours protégée par les **approbations d'exécution** et les listes d'autorisation par agent sur l'
hôte de nœud, vous pouvez donc garder l'accès aux commandes limité et explicite.

## Proxy de navigateur (zéro configuration)

Les hôtes de nœud annoncent automatiquement un proxy de navigateur si `browser.enabled` n'est pas
désactivé sur le nœud. Cela permet à l'agent d'utiliser l'automatisation de navigateur sur ce nœud
sans configuration supplémentaire.

Désactivez-le sur le nœud si nécessaire :

```json5
{
  nodeHost: {
    browserProxy: {
      enabled: false,
    },
  },
}
```

## Exécution (premier plan)

```bash
openclaw node run --host <gateway-host> --port 18789
```

Options :

- `--host <host>` : Hôte WebSocket de la passerelle (par défaut : `127.0.0.1`)
- `--port <port>` : Port WebSocket de la passerelle (par défaut : `18789`)
- `--tls` : Utiliser TLS pour la connexion à la passerelle
- `--tls-fingerprint <sha256>` : Empreinte digitale du certificat TLS attendue (sha256)
- `--node-id <id>` : Remplacer l'ID du nœud (efface le jeton d'appairage)
- `--display-name <name>` : Remplacer le nom d'affichage du nœud

## Authentification de la passerelle pour l'hôte de nœud

`openclaw node run` et `openclaw node install` résolvent l'authentification de la passerelle à partir de la configuration/env (pas de drapeaux `--token`/`--password` sur les commandes de nœud) :

- `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD` sont vérifiés en premier.
- Ensuite, secours de configuration locale : `gateway.auth.token` / `gateway.auth.password`.
- En mode local, l'hôte de nœud n'hérite intentionnellement pas de `gateway.remote.token` / `gateway.remote.password`.
- Si `gateway.auth.token` / `gateway.auth.password` est explicitement configuré via SecretRef et non résolu, la résolution d'authentification du nœud échoue fermée (pas de secours distant masquant).
- En `gateway.mode=remote`, les champs de client distant (`gateway.remote.token` / `gateway.remote.password`) sont également éligibles selon les règles de précédence distante.
- Les variables d'env héritées `CLAWDBOT_GATEWAY_*` sont ignorées pour la résolution d'authentification de l'hôte de nœud.

## Service (arrière-plan)

Installez un hôte de nœud sans interface en tant que service utilisateur.

```bash
openclaw node install --host <gateway-host> --port 18789
```

Options :

- `--host <host>` : Hôte WebSocket de la passerelle (par défaut : `127.0.0.1`)
- `--port <port>` : Port WebSocket de la passerelle (par défaut : `18789`)
- `--tls` : Utiliser TLS pour la connexion à la passerelle
- `--tls-fingerprint <sha256>` : Empreinte digitale du certificat TLS attendue (sha256)
- `--node-id <id>` : Remplacer l'ID du nœud (efface le jeton d'appairage)
- `--display-name <name>` : Remplacer le nom d'affichage du nœud
- `--runtime <runtime>` : Runtime du service (`node` ou `bun`)
- `--force` : Réinstaller/remplacer s'il est déjà installé

Gérez le service :

```bash
openclaw node status
openclaw node stop
openclaw node restart
openclaw node uninstall
```

Utilisez `openclaw node run` pour un hôte de nœud au premier plan (pas de service).

Les commandes de service acceptent `--json` pour une sortie lisible par machine.

## Appairage

La première connexion crée une demande d'appairage de périphérique en attente (`role: node`) sur la passerelle.
Approuvez-la via :

```bash
openclaw devices list
openclaw devices approve <requestId>
```

L'hôte de nœud stocke son ID de nœud, son jeton, son nom d'affichage et ses informations de connexion à la passerelle dans
`~/.openclaw/node.json`.

## Approbations d'exécution

`system.run` est contrôlé par les approbations d'exécution locales :

- `~/.openclaw/exec-approvals.json`
- [Approbations d'exécution](/tools/exec-approvals)
- `openclaw approvals --node <id|name|ip>` (modifier à partir de la passerelle)
