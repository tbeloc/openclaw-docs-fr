---
summary: "Manuel d'exploitation pour le service Gateway, cycle de vie et opérations"
read_when:
  - Running or debugging the gateway process
title: "Manuel d'exploitation Gateway"
---

# Manuel d'exploitation Gateway

Utilisez cette page pour le démarrage initial et les opérations quotidiennes du service Gateway.

<CardGroup cols={2}>
  <Card title="Dépannage approfondi" icon="siren" href="/fr/gateway/troubleshooting">
    Diagnostics basés sur les symptômes avec des échelles de commandes exactes et des signatures de journaux.
  </Card>
  <Card title="Configuration" icon="sliders" href="/fr/gateway/configuration">
    Guide de configuration orienté tâches + référence de configuration complète.
  </Card>
  <Card title="Gestion des secrets" icon="key-round" href="/fr/gateway/secrets">
    Contrat SecretRef, comportement des snapshots d'exécution et opérations de migration/rechargement.
  </Card>
  <Card title="Contrat du plan des secrets" icon="shield-check" href="/fr/gateway/secrets-plan-contract">
    Règles exactes de cible/chemin `secrets apply` et comportement auth-profile en mode ref uniquement.
  </Card>
</CardGroup>

## Démarrage local en 5 minutes

<Steps>
  <Step title="Démarrer la Gateway">

```bash
openclaw gateway --port 18789
# debug/trace mirrored to stdio
openclaw gateway --port 18789 --verbose
# force-kill listener on selected port, then start
openclaw gateway --force
```

  </Step>

  <Step title="Vérifier la santé du service">

```bash
openclaw gateway status
openclaw status
openclaw logs --follow
```

Ligne de base saine : `Runtime: running` et `RPC probe: ok`.

  </Step>

  <Step title="Valider la disponibilité des canaux">

```bash
openclaw channels status --probe
```

  </Step>
</Steps>

<Note>
Le rechargement de la configuration Gateway surveille le chemin du fichier de configuration actif (résolu à partir des valeurs par défaut du profil/état, ou `OPENCLAW_CONFIG_PATH` lorsqu'il est défini).
Le mode par défaut est `gateway.reload.mode="hybrid"`.
</Note>

## Modèle d'exécution

- Un processus toujours actif pour le routage, le plan de contrôle et les connexions de canaux.
- Port multiplexé unique pour :
  - Contrôle WebSocket/RPC
  - APIs HTTP (compatibles OpenAI, Responses, invocation d'outils)
  - Interface utilisateur de contrôle et hooks
- Mode de liaison par défaut : `loopback`.
- L'authentification est requise par défaut (`gateway.auth.token` / `gateway.auth.password`, ou `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`).

### Précédence du port et de la liaison

| Paramètre      | Ordre de résolution                                           |
| -------------- | ------------------------------------------------------------- |
| Port Gateway   | `--port` → `OPENCLAW_GATEWAY_PORT` → `gateway.port` → `18789` |
| Mode de liaison| CLI/override → `gateway.bind` → `loopback`                    |

### Modes de rechargement à chaud

| `gateway.reload.mode` | Comportement                                   |
| --------------------- | ---------------------------------------------- |
| `off`                 | Pas de rechargement de configuration            |
| `hot`                 | Appliquer uniquement les changements sûrs      |
| `restart`             | Redémarrer sur les changements nécessitant un redémarrage |
| `hybrid` (par défaut) | Application à chaud si sûr, redémarrage si nécessaire |

## Ensemble de commandes d'opérateur

```bash
openclaw gateway status
openclaw gateway status --deep
openclaw gateway status --json
openclaw gateway install
openclaw gateway restart
openclaw gateway stop
openclaw secrets reload
openclaw logs --follow
openclaw doctor
```

## Accès distant

Préféré : Tailscale/VPN.
Secours : Tunnel SSH.

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

Connectez ensuite les clients à `ws://127.0.0.1:18789` localement.

<Warning>
Si l'authentification de la gateway est configurée, les clients doivent toujours envoyer l'authentification (`token`/`password`) même sur les tunnels SSH.
</Warning>

Voir : [Gateway distante](/fr/gateway/remote), [Authentification](/fr/gateway/authentication), [Tailscale](/fr/gateway/tailscale).

## Supervision et cycle de vie du service

Utilisez des exécutions supervisées pour une fiabilité de type production.

<Tabs>
  <Tab title="macOS (launchd)">

```bash
openclaw gateway install
openclaw gateway status
openclaw gateway restart
openclaw gateway stop
```

Les étiquettes LaunchAgent sont `ai.openclaw.gateway` (par défaut) ou `ai.openclaw.<profile>` (profil nommé). `openclaw doctor` audite et répare la dérive de la configuration du service.

  </Tab>

  <Tab title="Linux (utilisateur systemd)">

```bash
openclaw gateway install
systemctl --user enable --now openclaw-gateway[-<profile>].service
openclaw gateway status
```

Pour la persistance après la déconnexion, activez la persistance :

```bash
sudo loginctl enable-linger <user>
```

  </Tab>

  <Tab title="Linux (service système)">

Utilisez une unité système pour les hôtes multi-utilisateurs/toujours actifs.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now openclaw-gateway[-<profile>].service
```

  </Tab>
</Tabs>

## Plusieurs gateways sur un seul hôte

La plupart des configurations doivent exécuter **une seule** Gateway.
Utilisez plusieurs uniquement pour l'isolation stricte/la redondance (par exemple un profil de secours).

Liste de contrôle par instance :

- `gateway.port` unique
- `OPENCLAW_CONFIG_PATH` unique
- `OPENCLAW_STATE_DIR` unique
- `agents.defaults.workspace` unique

Exemple :

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002
```

Voir : [Plusieurs gateways](/fr/gateway/multiple-gateways).

### Chemin rapide du profil de développement

```bash
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
openclaw --dev status
```

Les valeurs par défaut incluent l'état/configuration isolés et le port gateway de base `19001`.

## Référence rapide du protocole (vue opérateur)

- La première trame client doit être `connect`.
- La gateway retourne un snapshot `hello-ok` (`presence`, `health`, `stateVersion`, `uptimeMs`, limites/politique).
- Requêtes : `req(method, params)` → `res(ok/payload|error)`.
- Événements courants : `connect.challenge`, `agent`, `chat`, `presence`, `tick`, `health`, `heartbeat`, `shutdown`.

Les exécutions d'agent sont en deux étapes :

1. Accusé de réception accepté immédiat (`status:"accepted"`)
2. Réponse d'achèvement final (`status:"ok"|"error"`), avec événements `agent` en streaming entre les deux.

Voir la documentation complète du protocole : [Protocole Gateway](/fr/gateway/protocol).

## Vérifications opérationnelles

### Vivacité

- Ouvrir WS et envoyer `connect`.
- Attendre une réponse `hello-ok` avec snapshot.

### Disponibilité

```bash
openclaw gateway status
openclaw channels status --probe
openclaw health
```

### Récupération des lacunes

Les événements ne sont pas relus. En cas de lacunes de séquence, actualisez l'état (`health`, `system-presence`) avant de continuer.

## Signatures d'échec courant

| Signature                                                      | Problème probable                        |
| -------------------------------------------------------------- | ---------------------------------------- |
| `refusing to bind gateway ... without auth`                    | Liaison non-loopback sans token/password |
| `another gateway instance is already listening` / `EADDRINUSE` | Conflit de port                          |
| `Gateway start blocked: set gateway.mode=local`                | Configuration définie en mode distant    |
| `unauthorized` during connect                                  | Incompatibilité d'authentification entre client et gateway |

Pour les échelles de diagnostic complètes, utilisez [Dépannage Gateway](/fr/gateway/troubleshooting).

## Garanties de sécurité

- Les clients du protocole Gateway échouent rapidement lorsque la Gateway n'est pas disponible (pas de secours de canal direct implicite).
- Les premières trames non-connect invalides sont rejetées et fermées.
- L'arrêt gracieux émet un événement `shutdown` avant la fermeture du socket.

---

Connexes :

- [Dépannage](/fr/gateway/troubleshooting)
- [Processus en arrière-plan](/fr/gateway/background-process)
- [Configuration](/fr/gateway/configuration)
- [Santé](/fr/gateway/health)
- [Doctor](/fr/gateway/doctor)
- [Authentification](/fr/gateway/authentication)
