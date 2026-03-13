---
read_when:
  - Vous souhaitez lire ou modifier la configuration de manière non-interactive
summary: "Référence CLI pour `openclaw config` (obtenir/définir/annuler les valeurs de configuration)"
title: config
x-i18n:
  generated_at: "2026-02-03T10:04:13Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d60a35f5330f22bc99a0df090590586109d329ddd2ca294aeed191a22560c1c2
  source_path: cli/config.md
  workflow: 15
---

# `openclaw config`

Commande auxiliaire de configuration : obtenir/définir/annuler des valeurs par chemin. L'exécution sans sous-commande ouvrira
l'assistant de configuration (identique à `openclaw configure`).

## Exemples

```bash
openclaw config get browser.executablePath
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
openclaw config unset tools.web.search.apiKey
```

## Chemins

Les chemins utilisent la notation pointée ou entre crochets :

```bash
openclaw config get agents.defaults.workspace
openclaw config get agents.list[0].id
```

Utilisez l'index de la liste des agents pour localiser un agent spécifique :

```bash
openclaw config get agents.list
openclaw config set agents.list[1].tools.exec.node "node-id-or-name"
```

## Valeurs

Les valeurs sont analysées en JSON5 autant que possible ; sinon, elles sont traitées comme des chaînes.
Utilisez `--json` pour forcer l'analyse JSON5.

```bash
openclaw config set agents.defaults.heartbeat.every "0m"
openclaw config set gateway.port 19001 --json
openclaw config set channels.whatsapp.groups '["*"]' --json
```

Veuillez redémarrer la passerelle Gateway après modification.
