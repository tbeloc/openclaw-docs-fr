---
read_when:
  - Vous souhaitez installer et exécuter une Gateway fonctionnelle de la manière la plus rapide possible
summary: Installez OpenClaw, complétez l'assistant de configuration de Gateway et appairez votre premier canal.
title: Démarrage rapide
x-i18n:
  generated_at: "2026-02-04T17:53:21Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3c5da65996f89913cd115279ae21dcab794eadd14595951b676d8f7864fbbe2d
  source_path: start/quickstart.md
  workflow: 15
---

<Note>
OpenClaw nécessite Node 22 ou une version plus récente.
</Note>

## Installation

<Tabs>
  <Tab title="npm">
    ```bash
    npm install -g openclaw@latest
    ```
  </Tab>
  <Tab title="pnpm">
    ```bash
    pnpm add -g openclaw@latest
    ```
  </Tab>
</Tabs>

## Assistant de configuration et exécution de Gateway

<Steps>
  <Step title="Assistant de configuration et installation du service">
    ```bash
    openclaw onboard --install-daemon
    ```
  </Step>
  <Step title="Appairer WhatsApp">
    ```bash
    openclaw channels login
    ```
  </Step>
  <Step title="Démarrer Gateway">
    ```bash
    openclaw gateway --port 18789
    ```
  </Step>
</Steps>

Après avoir complété l'assistant de configuration, Gateway s'exécutera via le service utilisateur. Vous pouvez également le démarrer manuellement avec `openclaw gateway`.

<Info>
Par la suite, il est très simple de basculer entre l'installation npm et l'installation git. Après avoir installé l'autre méthode, exécutez
`openclaw doctor` pour mettre à jour le point d'entrée du service Gateway.
</Info>

## Installation à partir des sources (développement)

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # Les dépendances de l'interface utilisateur seront installées automatiquement lors de la première exécution
pnpm build
openclaw onboard --install-daemon
```

Si vous n'avez pas installé globalement, vous pouvez exécuter l'assistant de configuration dans le répertoire du dépôt avec `pnpm openclaw ...`.

## Démarrage rapide multi-instances (optionnel)

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

## Envoyer un message de test

Nécessite une Gateway en cours d'exécution.

```bash
openclaw message send --target +15555550123 --message "Hello from OpenClaw"
```
