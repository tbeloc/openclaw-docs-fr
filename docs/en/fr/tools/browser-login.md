---
summary: "Connexions manuelles pour l'automatisation du navigateur + publication sur X/Twitter"
read_when:
  - Vous devez vous connecter à des sites pour l'automatisation du navigateur
  - Vous souhaitez publier des mises à jour sur X/Twitter
title: "Connexion au navigateur"
---

# Connexion au navigateur + publication sur X/Twitter

## Connexion manuelle (recommandée)

Lorsqu'un site nécessite une connexion, **connectez-vous manuellement** dans le profil de navigateur **hôte** (le navigateur openclaw).

Ne **donnez pas** vos identifiants au modèle. Les connexions automatisées déclenchent souvent des défenses anti-bot et peuvent verrouiller le compte.

Retour à la documentation principale du navigateur : [Browser](/tools/browser).

## Quel profil Chrome est utilisé ?

OpenClaw contrôle un **profil Chrome dédié** (nommé `openclaw`, interface teintée d'orange). Il est séparé de votre profil de navigateur quotidien.

Pour les appels d'outil de navigateur d'agent :

- Choix par défaut : l'agent doit utiliser son navigateur `openclaw` isolé.
- Utilisez `profile="user"` uniquement lorsque les sessions connectées existantes sont importantes et que l'utilisateur est à l'ordinateur pour cliquer/approuver une invite d'attachement.
- Utilisez `profile="chrome-relay"` uniquement pour le flux d'attachement de l'extension Chrome / bouton de barre d'outils.
- Si vous avez plusieurs profils de navigateur utilisateur, spécifiez le profil explicitement au lieu de deviner.

Deux façons faciles d'y accéder :

1. **Demandez à l'agent d'ouvrir le navigateur** puis connectez-vous vous-même.
2. **Ouvrez-le via CLI** :

```bash
openclaw browser start
openclaw browser open https://x.com
```

Si vous avez plusieurs profils, passez `--browser-profile <name>` (la valeur par défaut est `openclaw`).

## X/Twitter : flux recommandé

- **Lecture/recherche/fils** : utilisez le navigateur **hôte** (connexion manuelle).
- **Publication de mises à jour** : utilisez le navigateur **hôte** (connexion manuelle).

## Sandboxing + accès au navigateur hôte

Les sessions de navigateur en sandbox sont **plus susceptibles** de déclencher la détection de bot. Pour X/Twitter (et autres sites stricts), préférez le navigateur **hôte**.

Si l'agent est en sandbox, l'outil de navigateur utilise par défaut le sandbox. Pour autoriser le contrôle hôte :

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

Ou désactivez le sandboxing pour l'agent qui publie les mises à jour.
