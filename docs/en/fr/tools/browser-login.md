---
summary: "Connexions manuelles pour l'automatisation de navigateur + publication sur X/Twitter"
read_when:
  - Vous devez vous connecter à des sites pour l'automatisation de navigateur
  - Vous souhaitez publier des mises à jour sur X/Twitter
title: "Connexion au navigateur"
---

# Connexion au navigateur + publication sur X/Twitter

## Connexion manuelle (recommandée)

Lorsqu'un site nécessite une connexion, **connectez-vous manuellement** dans le profil de navigateur **hôte** (le navigateur openclaw).

**Ne donnez pas** vos identifiants au modèle. Les connexions automatisées déclenchent souvent des défenses anti-bot et peuvent verrouiller le compte.

Retour à la documentation principale du navigateur : [Browser](/tools/browser).

## Quel profil Chrome est utilisé ?

OpenClaw contrôle un **profil Chrome dédié** (nommé `openclaw`, interface teintée d'orange). Il est séparé de votre profil de navigateur quotidien.

Deux façons faciles d'y accéder :

1. **Demandez à l'agent d'ouvrir le navigateur** puis connectez-vous vous-même.
2. **Ouvrez-le via CLI** :

```bash
openclaw browser start
openclaw browser open https://x.com
```

Si vous avez plusieurs profils, passez `--browser-profile <name>` (la valeur par défaut est `openclaw`).

## X/Twitter : flux recommandé

- **Lire/rechercher/fils** : utilisez le navigateur **hôte** (connexion manuelle).
- **Publier des mises à jour** : utilisez le navigateur **hôte** (connexion manuelle).

## Isolation + accès au navigateur hôte

Les sessions de navigateur isolées sont **plus susceptibles** de déclencher la détection de bot. Pour X/Twitter (et autres sites stricts), préférez le navigateur **hôte**.

Si l'agent est isolé, l'outil de navigateur utilise par défaut le bac à sable. Pour autoriser le contrôle hôte :

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

Ou désactivez l'isolation pour l'agent qui publie les mises à jour.
