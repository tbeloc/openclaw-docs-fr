---
read_when:
  - Implémenter les fonctionnalités des applications macOS
  - Modifier le cycle de vie de la Gateway ou le pontage de nœuds sur macOS
summary: Application compagnon OpenClaw macOS (barre de menu + proxy Gateway)
title: Application macOS
x-i18n:
  generated_at: "2026-02-03T07:53:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a5b1c02e5905e4cbc6c0688149cdb50a5bf7653e641947143e169ad948d1f057
  source_path: platforms/macos.md
  workflow: 15
---

# Application compagnon OpenClaw macOS (barre de menu + proxy Gateway)

L'application macOS est l'**application compagnon de la barre de menu** d'OpenClaw. Elle dispose des permissions pour gérer/attacher localement une Gateway (launchd ou manuelle) et expose les fonctionnalités macOS aux agents en tant que nœud.

## Fonctionnalités

- Affiche les notifications natives et l'état dans la barre de menu.
- Dispose des invites TCC (notifications, accessibilité, enregistrement d'écran, microphone, reconnaissance vocale, automatisation/AppleScript).
- Exécute ou se connecte à une Gateway (locale ou distante).
- Expose les outils spécifiques à macOS (Canvas, caméra, enregistrement d'écran, `system.run`).
- Lance le service hôte de nœud local (launchd) en mode **distant**, l'arrête en mode **local**.
- Héberge optionnellement **PeekabooBridge** pour l'automatisation de l'interface utilisateur.
- Installe globalement la CLI (`openclaw`) via npm/pnpm à la demande (l'utilisation de bun comme runtime Gateway n'est pas recommandée).

## Mode local vs distant

- **Local** (par défaut) : Si une Gateway locale en cours d'exécution existe, l'application s'y attache ; sinon, elle active le service launchd via `openclaw gateway install`.
- **Distant** : L'application se connecte à une Gateway via SSH/Tailscale, ne lance jamais de processus local.
  L'application lance le **service hôte de nœud** local afin que la Gateway distante puisse accéder à ce Mac.
  L'application ne génère pas la Gateway en tant que sous-processus.

## Contrôle Launchd

L'application gère un LaunchAgent par utilisateur étiqueté `bot.molt.gateway` (ou `bot.molt.<profile>` lors de l'utilisation de `--profile`/`OPENCLAW_PROFILE` ; les anciens `com.openclaw.*` seront toujours déchargés).

```bash
launchctl kickstart -k gui/$UID/bot.molt.gateway
launchctl bootout gui/$UID/bot.molt.gateway
```

Lors de l'exécution d'un profil nommé, remplacez l'étiquette par `bot.molt.<profile>`.

Si le LaunchAgent n'est pas installé, activez-le depuis l'application ou exécutez `openclaw gateway install`.

## Capacités des nœuds (mac)

L'application macOS se présente elle-même comme un nœud. Commandes courantes :

- Canvas : `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`, `canvas.a2ui.*`
- Caméra : `camera.snap`, `camera.clip`
- Écran : `screen.record`
- Système : `system.run`, `system.notify`

Le nœud rapporte une carte `permissions` afin que les agents puissent décider ce qui est autorisé.

Service de nœud + IPC d'application :

- Lorsque le service hôte de nœud sans interface graphique s'exécute (mode distant), il se connecte en tant que nœud à la Gateway WS.
- `system.run` s'exécute dans l'application macOS (contexte UI/TCC) via une socket Unix locale ; les invites + la sortie restent dans l'application.

Diagramme (SCI) :

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + TCC + system.run)
```

## Approbation Exec (system.run)

`system.run` est contrôlé par l'**approbation Exec** dans l'application macOS (Paramètres → Approbations Exec). Sécurité + invite + liste d'autorisation stockée localement sur le Mac :

```
~/.openclaw/exec-approvals.json
```

Exemple :

```json
{
  "version": 1,
  "defaults": {
    "security": "deny",
    "ask": "on-miss"
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [{ "pattern": "/opt/homebrew/bin/rg" }]
    }
  }
}
```

Remarques :

- Les entrées `allowlist` sont des motifs glob des chemins binaires résolus.
- La sélection de « Toujours autoriser » dans l'invite ajoute la commande à la liste d'autorisation.
- Les remplacements d'environnement `system.run` sont filtrés (suppression de `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`), puis fusionnés avec l'environnement de l'application.

## Liens profonds

L'application enregistre le schéma d'URL `openclaw://` pour les opérations locales.

### `openclaw://agent`

Déclenche une demande `agent` de la Gateway.

```bash
open 'openclaw://agent?message=Hello%20from%20deep%20link'
```

Paramètres de requête :

- `message` (obligatoire)
- `sessionKey` (optionnel)
- `thinking` (optionnel)
- `deliver` / `to` / `channel` (optionnel)
- `timeoutSeconds` (optionnel)
- `key` (clé de mode sans surveillance optionnelle)

Sécurité :

- Sans `key`, l'application demande une confirmation.
- Avec une `key` valide, l'exécution est sans surveillance (pour l'automatisation personnelle).

## Flux d'intégration (typique)

1. Installez et lancez **OpenClaw.app**.
2. Complétez la liste de contrôle des permissions (invites TCC).
3. Assurez-vous que le mode **local** est actif et que la Gateway s'exécute.
4. Si vous souhaitez un accès au terminal, installez la CLI.

## Flux de travail de construction et de développement (natif)

- `cd apps/macos && swift build`
- `swift run OpenClaw` (ou Xcode)
- Empaquetez l'application : `scripts/package-mac-app.sh`

## Débogage de la connexion Gateway (CLI macOS)

Utilisez la CLI de débogage pour exécuter la même logique de poignée de main WebSocket Gateway et de découverte que celle utilisée par l'application macOS, sans lancer l'application.

```bash
cd apps/macos
swift run openclaw-mac connect --json
swift run openclaw-mac discover --timeout 3000 --json
```

Options de connexion :

- `--url <ws://host:port>` : Remplace la configuration
- `--mode <local|remote>` : Analysé à partir de la configuration (par défaut : configuration ou local)
- `--probe` : Force une nouvelle sonde de santé
- `--timeout <ms>` : Délai d'expiration de la demande (par défaut : `15000`)
- `--json` : Sortie structurée pour comparaison

Options de découverte :

- `--include-local` : Inclut les Gateway qui seraient filtrées comme « locales »
- `--timeout <ms>` : Fenêtre de découverte globale (par défaut : `2000`)
- `--json` : Sortie structurée pour comparaison

Conseil : Comparez avec `openclaw gateway discover --json` pour voir si le pipeline de découverte de l'application macOS (NWBrowser + repli DNS-SD tailnet) diffère de la découverte basée sur `dns-sd` de la CLI Node.

## Pipeline de connexion distante (tunnel SSH)

Lorsque l'application macOS s'exécute en mode **distant**, elle ouvre un tunnel SSH afin que les composants UI locaux puissent communiquer avec la Gateway distante comme s'il s'agissait de localhost.

### Tunnel de contrôle (port WebSocket Gateway)

- **Objectif :** Vérification de santé, état, Web Chat, configuration et autres appels du plan de contrôle.
- **Port local :** Port Gateway (par défaut `18789`), toujours stable.
- **Port distant :** Même port Gateway sur l'hôte distant.
- **Comportement :** Pas de port local aléatoire ; l'application réutilise le tunnel de santé existant ou le redémarre si nécessaire.
- **Forme SSH :** `ssh -N -L <local>:127.0.0.1:<remote>`, avec options BatchMode + ExitOnForwardFailure + keepalive.
- **Rapport IP :** Le tunnel SSH utilise la boucle locale, donc la Gateway verra l'IP du nœud comme `127.0.0.1`. Si vous souhaitez afficher l'IP client réelle, utilisez le transport **Direct (ws/wss)** (voir [Accès distant macOS](/platforms/mac/remote)).

Pour les étapes de configuration, consultez [Accès distant macOS](/platforms/mac/remote). Pour les détails du protocole, consultez [Protocole Gateway](/gateway/protocol).

## Documentation connexe

- [Manuel d'exploitation Gateway](/gateway)
- [Gateway (macOS)](/platforms/mac/bundled-gateway)
- [Permissions macOS](/platforms/mac/permissions)
- [Canvas](/platforms/mac/canvas)
