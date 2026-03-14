---
read_when:
  - Vous souhaitez utiliser GitHub Copilot comme fournisseur de modèle
  - Vous devez comprendre le flux `openclaw models auth login-github-copilot`
summary: Connexion à GitHub Copilot depuis OpenClaw à l'aide du flux d'appareil
title: GitHub Copilot
x-i18n:
  generated_at: "2026-02-01T21:34:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 503e0496d92c921e2f7111b1b4ba16374f5b781643bfbc6cb69cea97d9395c25
  source_path: providers/github-copilot.md
  workflow: 15
---

# GitHub Copilot

## Qu'est-ce que GitHub Copilot ?

GitHub Copilot est l'assistant de programmation IA de GitHub. Il fournit l'accès aux modèles Copilot pour votre compte GitHub et votre plan d'abonnement. OpenClaw peut utiliser Copilot comme fournisseur de modèle de deux manières différentes.

## Deux façons d'utiliser Copilot dans OpenClaw

### 1) Fournisseur GitHub Copilot intégré (`github-copilot`)

Utilisez le flux de connexion d'appareil natif pour obtenir un jeton GitHub, puis échangez-le contre un jeton API Copilot au moment de l'exécution d'OpenClaw. C'est la façon **par défaut** et la plus simple, car elle ne nécessite pas VS Code.

### 2) Extension Copilot Proxy (`copilot-proxy`)

Utilisez l'extension VS Code **Copilot Proxy** comme pont local. OpenClaw communique avec le point de terminaison `/v1` du proxy et utilise la liste des modèles que vous y avez configurée. Choisissez cette méthode si vous exécutez déjà Copilot Proxy dans VS Code ou si vous devez router via celui-ci. Vous devez activer l'extension et maintenir l'extension VS Code en cours d'exécution.

Utilisez GitHub Copilot comme fournisseur de modèle (`github-copilot`). La commande de connexion exécute le flux d'appareil GitHub, enregistre le fichier de configuration d'authentification et met à jour votre configuration pour utiliser ce fichier.

## Configuration CLI

```bash
openclaw models auth login-github-copilot
```

Vous serez invité à visiter une URL et à entrer un code à usage unique. Gardez le terminal ouvert jusqu'à ce que le flux soit terminé.

### Paramètres optionnels

```bash
openclaw models auth login-github-copilot --profile-id github-copilot:work
openclaw models auth login-github-copilot --yes
```

## Définir le modèle par défaut

```bash
openclaw models set github-copilot/gpt-4o
```

### Extrait de configuration

```json5
{
  agents: { defaults: { model: { primary: "github-copilot/gpt-4o" } } },
}
```

## Remarques

- Nécessite un TTY interactif ; exécutez directement dans le terminal.
- La disponibilité des modèles Copilot dépend de votre plan d'abonnement ; si un modèle est rejeté, essayez un autre ID (par exemple `github-copilot/gpt-4.1`).
- La connexion stocke le jeton GitHub dans le fichier de configuration d'authentification et l'échange contre un jeton API Copilot au moment de l'exécution d'OpenClaw.
