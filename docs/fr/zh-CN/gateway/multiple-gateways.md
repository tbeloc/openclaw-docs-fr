---
read_when:
  - 在同一台机器上运行多个 Gateway 网关
  - 你需要每个 Gateway 网关有隔离的配置/状态/端口
summary: 在同一主机上运行多个 OpenClaw Gateway 网关（隔离、端口和配置文件）
title: 多 Gateway 网关
x-i18n:
  generated_at: "2026-02-03T07:48:13Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 09b5035d4e5fb97c8d4596f7e23dea67224dad3b6d9e2c37ecb99840f28bd77d
  source_path: gateway/multiple-gateways.md
  workflow: 15
---

# Plusieurs passerelles Gateway (même hôte)

La plupart des configurations devraient utiliser une seule passerelle Gateway, car une passerelle Gateway peut gérer plusieurs connexions de messages et agents. Si vous avez besoin d'une meilleure isolation ou redondance (par exemple, robot de secours), exécutez plusieurs passerelles Gateway avec des fichiers de configuration/ports isolés.

## Liste de contrôle d'isolation (obligatoire)

- `OPENCLAW_CONFIG_PATH` — fichier de configuration pour chaque instance
- `OPENCLAW_STATE_DIR` — sessions, identifiants, cache pour chaque instance
- `agents.defaults.workspace` — répertoire racine de l'espace de travail pour chaque instance
- `gateway.port` (ou `--port`) — unique pour chaque instance
- Les ports dérivés (navigateur/canvas) ne doivent pas se chevaucher

Si ces éléments sont partagés, vous rencontrerez des conditions de course de configuration et des conflits de ports.

## Recommandé : Profils de configuration (`--profile`)

Les profils de configuration limitent automatiquement `OPENCLAW_STATE_DIR` + `OPENCLAW_CONFIG_PATH` et ajoutent un suffixe aux noms de services.

```bash
# main
openclaw --profile main setup
openclaw --profile main gateway --port 18789

# rescue
openclaw --profile rescue setup
openclaw --profile rescue gateway --port 19001
```

Services par profil :

```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

## Guide du robot de secours

Exécutez une deuxième passerelle Gateway sur le même hôte avec des éléments indépendants :

- Fichiers de configuration/configuration
- Répertoire d'état
- Espace de travail
- Port de base (plus les ports dérivés)

Cela isole le robot de secours du robot principal, ce qui vous permet de déboguer ou d'appliquer des modifications de configuration si le robot principal tombe en panne.

Espacement des ports : laissez au moins 20 ports entre les ports de base, de sorte que les ports dérivés du navigateur/canvas/CDP ne se chevauchent jamais.

### Comment installer (robot de secours)

```bash
# Robot principal (existant ou nouveau, sans paramètre --profile)
# S'exécute sur le port 18789 + ports CDC/Canvas/... Chrome
openclaw onboard
openclaw gateway install

# Robot de secours (profil isolé + port)
openclaw --profile rescue onboard
# Remarque :
# - Le nom de l'espace de travail aura automatiquement le suffixe -rescue
# - Le port doit être au moins 18789 + 20 ports,
#   de préférence choisir un port de base complètement différent, comme 19789,
# - Le reste de l'intégration est identique à la normale

# Installer les services (s'ils n'ont pas été installés automatiquement lors de l'intégration)
openclaw --profile rescue gateway install
```

## Mappage des ports (dérivés)

Port de base = `gateway.port` (ou `OPENCLAW_GATEWAY_PORT` / `--port`).

- Port du service de contrôle du navigateur = base + 2 (loopback uniquement)
- `canvasHost.port = base + 4`
- Les ports CDP du profil du navigateur sont automatiquement alloués de `browser.controlPort + 9 .. + 108`

Si vous remplacez ces éléments dans la configuration ou les variables d'environnement, vous devez vous assurer que chaque instance est unique.

## Remarques sur le navigateur/CDP (pièges courants)

- **Ne pas** fixer `browser.cdpUrl` à la même valeur sur plusieurs instances.
- Chaque instance a besoin de son propre port de contrôle du navigateur et de sa propre plage CDP (dérivée de son port Gateway).
- Si vous avez besoin de ports CDP explicites, définissez `browser.profiles.<name>.cdpPort` pour chaque instance.
- Chrome distant : utilisez `browser.profiles.<name>.cdpUrl` (par profil, par instance).

## Exemple de variables d'environnement manuelles

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/main.json \
OPENCLAW_STATE_DIR=~/.openclaw-main \
openclaw gateway --port 18789

OPENCLAW_CONFIG_PATH=~/.openclaw/rescue.json \
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw gateway --port 19001
```

## Vérification rapide

```bash
openclaw --profile main status
openclaw --profile rescue status
openclaw --profile rescue browser status
```
