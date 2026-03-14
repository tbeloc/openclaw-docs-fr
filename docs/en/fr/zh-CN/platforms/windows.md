---
read_when:
  - 在 Windows 上安装 OpenClaw
  - 查找 Windows 配套应用状态
summary: Windows（WSL2）支持 + 配套应用状态
title: Windows (WSL2)
x-i18n:
  generated_at: "2026-02-03T07:53:19Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c93d2263b4e5b60cb6fbe9adcb1a0ca95b70cd6feb6e63cfc4459cb18b229da0
  source_path: platforms/windows.md
  workflow: 15
---

# Windows (WSL2)

OpenClaw sur Windows est recommandé **via WSL2** (Ubuntu recommandé). Le CLI + Gateway s'exécutent à l'intérieur de Linux, ce qui maintient la cohérence du runtime et améliore considérablement la compatibilité des outils (Node/Bun/pnpm, binaires Linux, Skills). Windows natif peut être plus délicat. WSL2 vous offre une expérience Linux complète — une seule commande pour installer : `wsl --install`.

Une application compagnon Windows native est en cours de planification.

## Installation (WSL2)

- [Guide de démarrage](/start/getting-started) (à utiliser dans WSL)
- [Installation et mise à jour](/install/updating)
- Guide officiel WSL2 (Microsoft) : https://learn.microsoft.com/windows/wsl/install

## Gateway

- [Manuel d'exploitation de Gateway](/gateway)
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

Sélectionnez **Gateway service** lorsque vous y êtes invité.

Réparation/migration :

```
openclaw doctor
```

## Avancé : Exposer les services WSL via LAN (portproxy)

WSL dispose de son propre réseau virtuel. Si une autre machine doit accéder à des services s'exécutant **à l'intérieur de WSL** (SSH, serveur TTS local ou Gateway), vous devez transférer les ports Windows vers l'adresse IP WSL actuelle. L'adresse IP WSL change après un redémarrage, vous devrez donc peut-être actualiser les règles de transfert.

Exemple (exécutez PowerShell **en tant qu'administrateur**) :

```powershell
$Distro = "Ubuntu-24.04"
$ListenPort = 2222
$TargetPort = 22

$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]
if (-not $WslIp) { throw "WSL IP not found." }

netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort `
  connectaddress=$WslIp connectport=$TargetPort
```

Autorisez le port via le pare-feu Windows (une seule fois) :

```powershell
New-NetFirewallRule -DisplayName "WSL SSH $ListenPort" -Direction Inbound `
  -Protocol TCP -LocalPort $ListenPort -Action Allow
```

Actualisez portproxy après un redémarrage de WSL :

```powershell
netsh interface portproxy delete v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 | Out-Null
netsh interface portproxy add v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 `
  connectaddress=$WslIp connectport=$TargetPort | Out-Null
```

Points importants :

- La cible SSH depuis une autre machine est **l'adresse IP de l'hôte Windows** (exemple : `ssh user@windows-host -p 2222`).
- Les nœuds distants doivent pointer vers une URL Gateway **accessible** (pas `127.0.0.1`) ; utilisez `openclaw status --all` pour confirmer.
- Utilisez `listenaddress=0.0.0.0` pour l'accès LAN ; `127.0.0.1` maintient uniquement l'accès local.
- Si vous souhaitez automatiser, enregistrez une tâche planifiée pour exécuter l'étape d'actualisation à la connexion.

## Installation étape par étape WSL2

### 1) Installer WSL2 + Ubuntu

Ouvrez PowerShell (administrateur) :

```powershell
wsl --install
# Or pick a distro explicitly:
wsl --list --online
wsl --install -d Ubuntu-24.04
```

Redémarrez si Windows vous le demande.

### 2) Activer systemd (requis pour l'installation de Gateway)

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

À l'intérieur de WSL, suivez le processus du guide de démarrage Linux :

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
openclaw onboard
```

Guide complet : [Guide de démarrage](/start/getting-started)

## Application compagnon Windows

Nous n'avons pas encore d'application compagnon Windows. Si vous souhaitez la voir implémentée, les contributions sont bienvenues.
