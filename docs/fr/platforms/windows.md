---
summary: "Support Windows (WSL2) + statut de l'application compagnon"
read_when:
  - Installing OpenClaw on Windows
  - Looking for Windows companion app status
title: "Windows (WSL2)"
---

# Windows (WSL2)

OpenClaw sur Windows est recommandé **via WSL2** (Ubuntu recommandé). La
CLI + Gateway s'exécutent à l'intérieur de Linux, ce qui maintient le runtime cohérent et rend
les outils beaucoup plus compatibles (Node/Bun/pnpm, binaires Linux, skills). Windows natif
peut être plus délicat. WSL2 vous offre l'expérience Linux complète — une seule commande
pour installer : `wsl --install`.

Les applications compagnon Windows natives sont prévues.

## Installation (WSL2)

- [Getting Started](/start/getting-started) (à utiliser à l'intérieur de WSL)
- [Install & updates](/install/updating)
- Guide officiel WSL2 (Microsoft) : [https://learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/windows/wsl/install)

## Statut Windows natif

Les flux CLI Windows natifs s'améliorent, mais WSL2 reste le chemin recommandé.

Ce qui fonctionne bien sur Windows natif aujourd'hui :

- installateur de site web via `install.ps1`
- utilisation CLI locale telle que `openclaw --version`, `openclaw doctor`, et `openclaw plugins list --json`
- smoke test local-agent/provider intégré tel que :

```powershell
openclaw agent --local --agent main --thinking low -m "Reply with exactly WINDOWS-HATCH-OK."
```

Limitations actuelles :

- `openclaw onboard --non-interactive` s'attend toujours à une gateway locale accessible sauf si vous passez `--skip-health`
- `openclaw onboard --non-interactive --install-daemon` et `openclaw gateway install` essaient d'abord les Tâches planifiées Windows
- si la création de Tâche planifiée est refusée, OpenClaw revient à un élément de dossier Startup par utilisateur et démarre la gateway immédiatement
- si `schtasks` lui-même se bloque ou cesse de répondre, OpenClaw abandonne maintenant ce chemin rapidement et revient au lieu de rester bloqué indéfiniment
- Les Tâches planifiées sont toujours préférées quand elles sont disponibles car elles fournissent un meilleur statut de superviseur

Si vous voulez la CLI native uniquement, sans installation de service gateway, utilisez l'une de ces commandes :

```powershell
openclaw onboard --non-interactive --skip-health
openclaw gateway run
```

Si vous voulez un démarrage géré sur Windows natif :

```powershell
openclaw gateway install
openclaw gateway status --json
```

Si la création de Tâche planifiée est bloquée, le mode service de secours démarre toujours automatiquement après la connexion via le dossier Startup de l'utilisateur actuel.

## Gateway

- [Gateway runbook](/gateway)
- [Configuration](/gateway/configuration)

## Installation du service Gateway (CLI)

À l'intérieur de WSL2 :

```
openclaw onboard --install-daemon
```

Ou :

```
openclaw gateway install
```

Ou :

```
openclaw configure
```

Sélectionnez **Gateway service** quand vous y êtes invité.

Réparation/migration :

```
openclaw doctor
```

## Démarrage automatique de la Gateway avant la connexion Windows

Pour les configurations sans interface, assurez-vous que la chaîne de démarrage complète s'exécute même quand personne ne se connecte à Windows.

### 1) Maintenir les services utilisateur en cours d'exécution sans connexion

À l'intérieur de WSL :

```bash
sudo loginctl enable-linger "$(whoami)"
```

### 2) Installer le service utilisateur OpenClaw gateway

À l'intérieur de WSL :

```bash
openclaw gateway install
```

### 3) Démarrer WSL automatiquement au démarrage de Windows

Dans PowerShell en tant qu'Administrateur :

```powershell
schtasks /create /tn "WSL Boot" /tr "wsl.exe -d Ubuntu --exec /bin/true" /sc onstart /ru SYSTEM
```

Remplacez `Ubuntu` par le nom de votre distribution depuis :

```powershell
wsl --list --verbose
```

### Vérifier la chaîne de démarrage

Après un redémarrage (avant la connexion Windows), vérifiez depuis WSL :

```bash
systemctl --user is-enabled openclaw-gateway
systemctl --user status openclaw-gateway --no-pager
```

## Avancé : exposer les services WSL sur le LAN (portproxy)

WSL a son propre réseau virtuel. Si une autre machine doit accéder à un service
s'exécutant **à l'intérieur de WSL** (SSH, un serveur TTS local, ou la Gateway), vous devez
transférer un port Windows vers l'IP WSL actuelle. L'IP WSL change après les redémarrages,
donc vous devrez peut-être actualiser la règle de transfert.

Exemple (PowerShell **en tant qu'Administrateur**) :

```powershell
$Distro = "Ubuntu-24.04"
$ListenPort = 2222
$TargetPort = 22

$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]
if (-not $WslIp) { throw "WSL IP not found." }

netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort `
  connectaddress=$WslIp connectport=$TargetPort
```

Autoriser le port via le Pare-feu Windows (une seule fois) :

```powershell
New-NetFirewallRule -DisplayName "WSL SSH $ListenPort" -Direction Inbound `
  -Protocol TCP -LocalPort $ListenPort -Action Allow
```

Actualiser le portproxy après les redémarrages de WSL :

```powershell
netsh interface portproxy delete v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 | Out-Null
netsh interface portproxy add v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 `
  connectaddress=$WslIp connectport=$TargetPort | Out-Null
```

Notes :

- SSH depuis une autre machine cible l'**IP de l'hôte Windows** (exemple : `ssh user@windows-host -p 2222`).
- Les nœuds distants doivent pointer vers une URL Gateway **accessible** (pas `127.0.0.1`); utilisez
  `openclaw status --all` pour confirmer.
- Utilisez `listenaddress=0.0.0.0` pour l'accès LAN; `127.0.0.1` le garde local uniquement.
- Si vous voulez que ce soit automatique, enregistrez une Tâche planifiée pour exécuter l'étape
  d'actualisation à la connexion.

## Installation WSL2 étape par étape

### 1) Installer WSL2 + Ubuntu

Ouvrez PowerShell (Admin) :

```powershell
wsl --install
# Ou choisissez une distribution explicitement :
wsl --list --online
wsl --install -d Ubuntu-24.04
```

Redémarrez si Windows le demande.

### 2) Activer systemd (requis pour l'installation de la gateway)

Dans votre terminal WSL :

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

Puis depuis PowerShell :

```powershell
wsl --shutdown
```

Rouvrez Ubuntu, puis vérifiez :

```bash
systemctl --user status
```

### 3) Installer OpenClaw (à l'intérieur de WSL)

Suivez le flux Getting Started Linux à l'intérieur de WSL :

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # installe automatiquement les dépendances UI à la première exécution
pnpm build
openclaw onboard
```

Guide complet : [Getting Started](/start/getting-started)

## Application compagnon Windows

Nous n'avons pas encore d'application compagnon Windows. Les contributions sont bienvenues si vous voulez
contribuer pour que cela se produise.
