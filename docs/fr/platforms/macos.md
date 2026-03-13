---
summary: "Application compagnon macOS OpenClaw (barre de menu + courtier de passerelle)"
read_when:
  - Implementing macOS app features
  - Changing gateway lifecycle or node bridging on macOS
title: "Application macOS"
---

# Compagnon macOS OpenClaw (barre de menu + courtier de passerelle)

L'application macOS est le **compagnon de barre de menu** pour OpenClaw. Elle possède les permissions,
gère/s'attache à la Gateway localement (launchd ou manuel), et expose les capacités macOS
à l'agent en tant que nœud.

## Ce qu'elle fait

- Affiche les notifications natives et le statut dans la barre de menu.
- Possède les invites TCC (Notifications, Accessibilité, Enregistrement d'écran, Microphone,
  Reconnaissance vocale, Automation/AppleScript).
- Exécute ou se connecte à la Gateway (locale ou distante).
- Expose les outils macOS uniquement (Canvas, Caméra, Enregistrement d'écran, `system.run`).
- Démarre le service d'hôte de nœud local en mode **distant** (launchd), et l'arrête en mode **local**.
- Héberge optionnellement **PeekabooBridge** pour l'automatisation de l'interface utilisateur.
- Installe l'interface de ligne de commande globale (`openclaw`) via npm/pnpm sur demande (bun non recommandé pour le runtime Gateway).

## Mode local vs distant

- **Local** (par défaut) : l'application s'attache à une Gateway locale en cours d'exécution si présente ;
  sinon elle active le service launchd via `openclaw gateway install`.
- **Distant** : l'application se connecte à une Gateway via SSH/Tailscale et ne démarre jamais
  un processus local.
  L'application démarre le **service d'hôte de nœud** local afin que la Gateway distante puisse atteindre ce Mac.
  L'application ne génère pas la Gateway en tant que processus enfant.

## Contrôle Launchd

L'application gère un LaunchAgent par utilisateur étiqueté `ai.openclaw.gateway`
(ou `ai.openclaw.<profile>` lors de l'utilisation de `--profile`/`OPENCLAW_PROFILE` ; l'ancien `com.openclaw.*` se décharge toujours).

```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

Remplacez l'étiquette par `ai.openclaw.<profile>` lors de l'exécution d'un profil nommé.

Si le LaunchAgent n'est pas installé, activez-le depuis l'application ou exécutez
`openclaw gateway install`.

## Capacités des nœuds (mac)

L'application macOS se présente comme un nœud. Commandes courantes :

- Canvas : `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`, `canvas.a2ui.*`
- Caméra : `camera.snap`, `camera.clip`
- Écran : `screen.record`
- Système : `system.run`, `system.notify`

Le nœud rapporte une carte `permissions` afin que les agents puissent décider ce qui est autorisé.

Service de nœud + IPC d'application :

- Lorsque le service d'hôte de nœud sans interface est en cours d'exécution (mode distant), il se connecte à la Gateway WS en tant que nœud.
- `system.run` s'exécute dans l'application macOS (contexte UI/TCC) via un socket Unix local ; les invites + la sortie restent dans l'application.

Diagramme (SCI) :

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + TCC + system.run)
```

## Approbations d'exécution (system.run)

`system.run` est contrôlé par les **approbations d'exécution** dans l'application macOS (Paramètres → Approbations d'exécution).
La sécurité + demande + liste d'autorisation sont stockées localement sur le Mac dans :

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

Notes :

- Les entrées `allowlist` sont des motifs glob pour les chemins binaires résolus.
- Le texte de commande shell brut qui contient une syntaxe de contrôle ou d'expansion shell (`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) est traité comme un manque de liste d'autorisation et nécessite une approbation explicite (ou l'ajout du binaire shell à la liste d'autorisation).
- Choisir « Toujours autoriser » dans l'invite ajoute cette commande à la liste d'autorisation.
- Les remplacements d'environnement `system.run` sont filtrés (supprime `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`) puis fusionnés avec l'environnement de l'application.
- Pour les wrappers shell (`bash|sh|zsh ... -c/-lc`), les remplacements d'environnement limités à la requête sont réduits à une petite liste d'autorisation explicite (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`).
- Pour les décisions « toujours autoriser » en mode liste d'autorisation, les wrappers de dispatch connus (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) conservent les chemins exécutables internes au lieu des chemins wrapper. Si le dépliage n'est pas sûr, aucune entrée de liste d'autorisation n'est conservée automatiquement.

## Liens profonds

L'application enregistre le schéma d'URL `openclaw://` pour les actions locales.

### `openclaw://agent`

Déclenche une requête `agent` Gateway.

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
- Sans `key`, l'application applique une limite de longueur de message courte pour l'invite de confirmation et ignore `deliver` / `to` / `channel`.
- Avec une `key` valide, l'exécution est sans surveillance (destinée aux automations personnelles).

## Flux d'intégration (typique)

1. Installez et lancez **OpenClaw.app**.
2. Complétez la liste de contrôle des permissions (invites TCC).
3. Assurez-vous que le mode **Local** est actif et que la Gateway est en cours d'exécution.
4. Installez l'interface de ligne de commande si vous souhaitez un accès au terminal.

## Placement du répertoire d'état (macOS)

Évitez de placer votre répertoire d'état OpenClaw dans iCloud ou d'autres dossiers synchronisés par le cloud.
Les chemins sauvegardés par synchronisation peuvent ajouter de la latence et occasionnellement causer des blocages de fichiers/courses de synchronisation pour
les sessions et les identifiants.

Préférez un chemin d'état local non synchronisé tel que :

```bash
OPENCLAW_STATE_DIR=~/.openclaw
```

Si `openclaw doctor` détecte l'état sous :

- `~/Library/Mobile Documents/com~apple~CloudDocs/...`
- `~/Library/CloudStorage/...`

il avertira et recommandera de revenir à un chemin local.

## Flux de travail de construction et de développement (natif)

- `cd apps/macos && swift build`
- `swift run OpenClaw` (ou Xcode)
- Empaqueter l'application : `scripts/package-mac-app.sh`

## Déboguer la connectivité de la passerelle (CLI macOS)

Utilisez l'interface de ligne de commande de débogage pour exercer la même logique de poignée de main et de découverte WebSocket Gateway
que l'application macOS utilise, sans lancer l'application.

```bash
cd apps/macos
swift run openclaw-mac connect --json
swift run openclaw-mac discover --timeout 3000 --json
```

Options de connexion :

- `--url <ws://host:port>` : remplacer la configuration
- `--mode <local|remote>` : résoudre à partir de la configuration (par défaut : configuration ou local)
- `--probe` : forcer une sonde de santé fraîche
- `--timeout <ms>` : délai d'expiration de la requête (par défaut : `15000`)
- `--json` : sortie structurée pour la comparaison

Options de découverte :

- `--include-local` : inclure les passerelles qui seraient filtrées comme « locales »
- `--timeout <ms>` : fenêtre de découverte globale (par défaut : `2000`)
- `--json` : sortie structurée pour la comparaison

Conseil : comparez avec `openclaw gateway discover --json` pour voir si le
pipeline de découverte de l'application macOS (NWBrowser + secours DNS‑SD tailnet) diffère de
la découverte basée sur `dns-sd` de l'interface de ligne de commande Node.

## Tuyauterie de connexion distante (tunnels SSH)

Lorsque l'application macOS s'exécute en mode **Distant**, elle ouvre un tunnel SSH afin que les composants UI locaux
puissent communiquer avec une Gateway distante comme s'il s'agissait de localhost.

### Tunnel de contrôle (port WebSocket Gateway)

- **Objectif :** vérifications de santé, statut, Web Chat, configuration et autres appels du plan de contrôle.
- **Port local :** le port Gateway (par défaut `18789`), toujours stable.
- **Port distant :** le même port Gateway sur l'hôte distant.
- **Comportement :** pas de port local aléatoire ; l'application réutilise un tunnel sain existant
  ou le redémarre si nécessaire.
- **Forme SSH :** `ssh -N -L <local>:127.0.0.1:<remote>` avec BatchMode +
  ExitOnForwardFailure + options de maintien en vie.
- **Rapport IP :** le tunnel SSH utilise la boucle locale, donc la passerelle verra l'IP du nœud comme `127.0.0.1`. Utilisez le transport **Direct (ws/wss)** si vous souhaitez que l'IP client réelle apparaisse (voir [accès distant macOS](/platforms/mac/remote)).

Pour les étapes de configuration, voir [accès distant macOS](/platforms/mac/remote). Pour les détails du protocole, voir [protocole Gateway](/gateway/protocol).

## Documents connexes

- [Runbook Gateway](/gateway)
- [Gateway (macOS)](/platforms/mac/bundled-gateway)
- [Permissions macOS](/platforms/mac/permissions)
- [Canvas](/platforms/mac/canvas)
