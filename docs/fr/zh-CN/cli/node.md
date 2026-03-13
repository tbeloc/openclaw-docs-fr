---
read_when:
  - 运行无头节点主机
  - 为 system.run 配对非 macOS 节点
summary: "`openclaw node` 的 CLI 参考（无头节点主机）"
title: node
x-i18n:
  generated_at: "2026-02-03T07:45:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a8b1a57712663e2285c9ecd306fe57d067eb3e6820d7d8aec650b41b022d995a
  source_path: cli/node.md
  workflow: 15
---

# `openclaw node`

Exécutez un **hôte de nœud sans interface**, connecté à la passerelle WebSocket et exposez
`system.run` / `system.which` sur cette machine.

## Pourquoi utiliser un hôte de nœud ?

Utilisez un hôte de nœud lorsque vous souhaitez que les agents **exécutent des commandes sur d'autres machines du réseau** sans avoir besoin d'installer l'application macOS complète à cet endroit.

Cas d'usage courants :

- Exécuter des commandes sur des machines Linux/Windows distantes (serveurs de compilation, machines de laboratoire, NAS).
- Maintenir l'**isolation du bac à sable** sur la passerelle, mais déléguer les exécutions approuvées à d'autres hôtes.
- Fournir une cible d'exécution légère et sans interface pour l'automatisation ou les nœuds CI.

L'exécution est toujours protégée par l'**approbation d'exécution** et les listes blanches par agent sur l'hôte de nœud, vous pouvez donc garder l'accès aux commandes bien délimité.

## Proxy de navigateur (zéro configuration)

Si `browser.enabled` sur le nœud n'est pas désactivé, l'hôte de nœud diffuse automatiquement un proxy de navigateur. Cela permet aux agents d'utiliser l'automatisation de navigateur sur ce nœud sans configuration supplémentaire.

Pour désactiver sur le nœud :

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
- `--node-id <id>` : Remplacer l'id du nœud (effacer le jeton d'appairage)
- `--display-name <name>` : Remplacer le nom d'affichage du nœud

## Service (arrière-plan)

Installez l'hôte de nœud sans interface en tant que service utilisateur.

```bash
openclaw node install --host <gateway-host> --port 18789
```

Options :

- `--host <host>` : Hôte WebSocket de la passerelle (par défaut : `127.0.0.1`)
- `--port <port>` : Port WebSocket de la passerelle (par défaut : `18789`)
- `--tls` : Utiliser TLS pour la connexion à la passerelle
- `--tls-fingerprint <sha256>` : Empreinte digitale du certificat TLS attendue (sha256)
- `--node-id <id>` : Remplacer l'id du nœud (effacer le jeton d'appairage)
- `--display-name <name>` : Remplacer le nom d'affichage du nœud
- `--runtime <runtime>` : Runtime du service (`node` ou `bun`)
- `--force` : Réinstaller/remplacer si déjà installé

Gérer le service :

```bash
openclaw node status
openclaw node stop
openclaw node restart
openclaw node uninstall
```

Utilisez `openclaw node run` pour exécuter l'hôte de nœud au premier plan (sans service).

Les commandes de service acceptent `--json` pour une sortie lisible par machine.

## Appairage

La première connexion crée une demande d'appairage de nœud en attente sur la passerelle.
Approuvez-la via :

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

L'hôte de nœud stocke son id de nœud, son jeton, son nom d'affichage et les informations de connexion à la passerelle dans
`~/.openclaw/node.json`.

## Approbation d'exécution

`system.run` est soumis aux limites d'approbation d'exécution locale :

- `~/.openclaw/exec-approvals.json`
- [Approbation d'exécution](/tools/exec-approvals)
- `openclaw approvals --node <id|name|ip>` (éditer depuis la passerelle)
