---
summary: "Exécuter plusieurs passerelles OpenClaw sur un seul hôte (isolation, ports et profils)"
read_when:
  - Running more than one Gateway on the same machine
  - You need isolated config/state/ports per Gateway
title: "Plusieurs passerelles"
---

# Plusieurs passerelles (même hôte)

La plupart des configurations doivent utiliser une seule passerelle car une seule passerelle peut gérer plusieurs connexions de messagerie et agents. Si vous avez besoin d'une isolation plus forte ou d'une redondance (par exemple, un bot de secours), exécutez des passerelles séparées avec des profils/ports isolés.

## Liste de contrôle d'isolation (obligatoire)

- `OPENCLAW_CONFIG_PATH` — fichier de configuration par instance
- `OPENCLAW_STATE_DIR` — sessions, identifiants, caches par instance
- `agents.defaults.workspace` — racine de l'espace de travail par instance
- `gateway.port` (ou `--port`) — unique par instance
- Les ports dérivés (navigateur/canvas) ne doivent pas se chevaucher

Si ces éléments sont partagés, vous rencontrerez des conflits de configuration et de ports.

## Recommandé : profils (`--profile`)

Les profils délimitent automatiquement `OPENCLAW_STATE_DIR` + `OPENCLAW_CONFIG_PATH` et suffixent les noms de services.

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

## Guide du bot de secours

Exécutez une deuxième passerelle sur le même hôte avec ses propres :

- profil/configuration
- répertoire d'état
- espace de travail
- port de base (plus ports dérivés)

Cela maintient le bot de secours isolé du bot principal afin qu'il puisse déboguer ou appliquer des modifications de configuration si le bot principal est arrêté.

Espacement des ports : laissez au moins 20 ports entre les ports de base afin que les ports dérivés du navigateur/canvas/CDP ne se heurtent jamais.

### Comment installer (bot de secours)

```bash
# Bot principal (existant ou nouveau, sans paramètre --profile)
# S'exécute sur le port 18789 + ports Chrome CDC/Canvas/...
openclaw onboard
openclaw gateway install

# Bot de secours (profil isolé + ports)
openclaw --profile rescue onboard
# Notes :
# - le nom de l'espace de travail sera suffixé avec -rescue par défaut
# - Le port doit être au moins 18789 + 20 ports,
#   il est préférable de choisir un port de base complètement différent, comme 19789,
# - le reste de l'intégration est le même que la normale

# Pour installer le service (si cela ne s'est pas produit automatiquement lors de l'intégration)
openclaw --profile rescue gateway install
```

## Mappage des ports (dérivés)

Port de base = `gateway.port` (ou `OPENCLAW_GATEWAY_PORT` / `--port`).

- port du service de contrôle du navigateur = base + 2 (loopback uniquement)
- l'hôte canvas est servi sur le serveur HTTP de la passerelle (même port que `gateway.port`)
- Les ports CDP du profil du navigateur s'allouent automatiquement à partir de `browser.controlPort + 9 .. + 108`

Si vous remplacez l'un de ces éléments dans la configuration ou l'environnement, vous devez les garder uniques par instance.

## Notes sur le navigateur/CDP (piège courant)

- Ne **pas** épingler `browser.cdpUrl` aux mêmes valeurs sur plusieurs instances.
- Chaque instance a besoin de son propre port de contrôle du navigateur et de sa propre plage CDP (dérivée de son port de passerelle).
- Si vous avez besoin de ports CDP explicites, définissez `browser.profiles.<name>.cdpPort` par instance.
- Chrome distant : utilisez `browser.profiles.<name>.cdpUrl` (par profil, par instance).

## Exemple d'environnement manuel

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/main.json \
OPENCLAW_STATE_DIR=~/.openclaw-main \
openclaw gateway --port 18789

OPENCLAW_CONFIG_PATH=~/.openclaw/rescue.json \
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw gateway --port 19001
```

## Vérifications rapides

```bash
openclaw --profile main status
openclaw --profile rescue status
openclaw --profile rescue browser status
```
