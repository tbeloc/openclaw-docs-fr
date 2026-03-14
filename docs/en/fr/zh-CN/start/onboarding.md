---
read_when:
  - 设计 macOS 新手引导助手
  - 实现认证或身份设置
summary: OpenClaw 的首次运行新手引导流程（macOS 应用）
title: 新手引导
x-i18n:
  generated_at: "2026-02-03T07:54:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ae883b2deb1f9032be7c47a04d67e1741dffbdcc4445de1e0bbaa976e606bc10
  source_path: start/onboarding.md
  workflow: 15
---

# Onboarding (Application macOS)

Ce document décrit le processus d'onboarding au premier lancement **actuel**. L'objectif est une expérience fluide du « jour 0 » : sélectionner l'emplacement d'exécution de la Gateway, se connecter, exécuter l'assistant, puis laisser l'agent se guider lui-même.

## Ordre des pages (actuel)

1. Bienvenue + Avertissement de sécurité
2. **Sélection de la Gateway** (Local / Distant / Configurer plus tard)
3. **Authentification (Anthropic OAuth)** — Local uniquement
4. **Assistant de configuration** (Piloté par Gateway)
5. **Permissions** (Invites TCC)
6. **CLI** (Optionnel)
7. **Chat d'onboarding** (Session dédiée)
8. Prêt

## 1) Bienvenue + Avertissement de sécurité

Lisez l'avertissement de sécurité affiché et décidez en conséquence.

## 2) Local vs Distant

Où la **Gateway** s'exécute-t-elle ?

- **Local (ce Mac) :** L'onboarding peut exécuter le flux OAuth localement et écrire les identifiants.
- **Distant (via SSH/Tailnet) :** L'onboarding **ne** exécutera pas OAuth localement ; les identifiants doivent exister sur l'hôte Gateway.
- **Configurer plus tard :** Ignorer la configuration et laisser l'application non configurée.

Remarques sur l'authentification de la Gateway :

- L'assistant génère maintenant un **token** même pour loopback, donc le client WS local doit s'authentifier.
- Si vous désactivez l'authentification, tout processus local peut se connecter ; utilisez uniquement sur des machines entièrement fiables.
- Pour l'accès multi-machines ou les liaisons non-loopback, utilisez des **tokens**.

## 3) Authentification locale uniquement (Anthropic OAuth)

L'application macOS supporte Anthropic OAuth (Claude Pro/Max). Processus :

- Ouvrir le navigateur pour OAuth (PKCE)
- Demander à l'utilisateur de coller la valeur `code#state`
- Écrire les identifiants dans `~/.openclaw/credentials/oauth.json`

Les autres fournisseurs (OpenAI, API personnalisée) sont actuellement configurés via des variables d'environnement ou des fichiers de configuration.

## 4) Assistant de configuration (Piloté par Gateway)

L'application peut exécuter le même assistant de configuration que la CLI. Cela maintient l'onboarding synchronisé avec le comportement côté Gateway, évitant la duplication de logique dans SwiftUI.

## 5) Permissions

L'onboarding demande les permissions TCC requises suivantes :

- Notifications
- Accessibilité
- Enregistrement d'écran
- Microphone / Reconnaissance vocale
- Automatisation (AppleScript)

## 6) CLI (Optionnel)

L'application peut installer globalement le CLI `openclaw` via npm/pnpm pour les flux de terminal et les tâches launchd prêts à l'emploi.

## 7) Chat d'onboarding (Session dédiée)

Une fois la configuration terminée, l'application ouvre une session de chat d'onboarding dédiée, permettant à l'agent de se présenter et de guider les étapes suivantes. Cela sépare les conseils au premier lancement de vos conversations normales.

## Rituel de guidage de l'agent

Lors de la première exécution de l'agent, OpenClaw initialise un espace de travail (par défaut `~/.openclaw/workspace`) :

- Initialiser `AGENTS.md`, `BOOTSTRAP.md`, `IDENTITY.md`, `USER.md`
- Exécuter un court rituel de questions-réponses (une question à la fois)
- Écrire l'identité + préférences dans `IDENTITY.md`, `USER.md`, `SOUL.md`
- Une fois terminé, supprimer `BOOTSTRAP.md` pour qu'il ne s'exécute qu'une fois

## Optionnel : Hook Gmail (Manuel)

La configuration Gmail Pub/Sub est actuellement une étape manuelle. Utilisez :

```bash
openclaw webhooks gmail setup --account you@gmail.com
```

Consultez [/automation/gmail-pubsub](/automation/gmail-pubsub) pour plus de détails.

## Notes sur le mode distant

Lorsque la Gateway s'exécute sur une autre machine, les identifiants et fichiers d'espace de travail sont stockés sur **cet hôte**. Si vous avez besoin d'utiliser OAuth en mode distant, créez sur l'hôte Gateway :

- `~/.openclaw/credentials/oauth.json`
- `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
