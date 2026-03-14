---
read_when:
  - 你需要为浏览器自动化登录网站
  - 你想在 X/Twitter 上发布更新
summary: 用于浏览器自动化 + X/Twitter 发帖的手动登录
title: 浏览器登录
x-i18n:
  generated_at: "2026-02-03T07:55:03Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8ceea2d5258836e3db10f858ee122b5832a40f83a72ba18de140671091eef5a8
  source_path: tools/browser-login.md
  workflow: 15
---

# Connexion au navigateur + Publication sur X/Twitter

## Connexion manuelle (recommandée)

Lorsqu'un site Web nécessite une connexion, **connectez-vous manuellement** dans le profil de navigateur **hôte** (navigateur openclaw).

**Ne fournissez pas** vos identifiants au modèle. La connexion automatique déclenche généralement les défenses anti-bot et peut verrouiller le compte.

Retour à la documentation du navigateur principal : [Navigateur](/tools/browser).

## Quel profil Chrome utiliser ?

OpenClaw contrôle un **profil Chrome dédié** (nommé `openclaw`, interface de couleur orange). C'est séparé de votre profil de navigateur quotidien.

Deux façons simples d'y accéder :

1. **Laissez l'agent ouvrir le navigateur**, puis connectez-vous vous-même.
2. **Ouvrir via CLI** :

```bash
openclaw browser start
openclaw browser open https://x.com
```

Si vous avez plusieurs profils, passez `--browser-profile <name>` (par défaut `openclaw`).

## X/Twitter : flux recommandé

- **Lecture/Recherche/Tendances :** Utilisez les **bird** CLI Skills (pas de navigateur, stable).
  - Dépôt : https://github.com/steipete/bird
- **Publication de mises à jour :** Utilisez le navigateur **hôte** (connexion manuelle).

## Isolation du bac à sable + accès au navigateur hôte

Les sessions de navigateur isolées en bac à sable **déclenchent plus facilement** la détection de bot. Pour X/Twitter (et autres sites stricts), privilégiez le navigateur **hôte**.

Si l'agent est en bac à sable, l'outil de navigateur utilise par défaut le bac à sable. Pour autoriser le contrôle hôte :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

Ensuite, ciblez le navigateur hôte :

```bash
openclaw browser open https://x.com --browser-profile openclaw --target host
```

Ou désactivez l'isolation du bac à sable pour l'agent qui publie les mises à jour.
