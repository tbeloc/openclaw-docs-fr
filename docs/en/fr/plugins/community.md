---
summary: "Plugins communautaires : barre de qualité, exigences d'hébergement et processus de soumission de PR"
read_when:
  - Vous souhaitez publier un plugin OpenClaw tiers
  - Vous souhaitez proposer un plugin pour la liste de documentation
title: "Plugins communautaires"
---

# Plugins communautaires

Cette page répertorie les **plugins maintenus par la communauté** de haute qualité pour OpenClaw.

Nous acceptons les PR qui ajoutent des plugins communautaires ici lorsqu'ils respectent la barre de qualité.

## Requis pour la liste

- Le package du plugin est publié sur npmjs (installable via `openclaw plugins install <npm-spec>`).
- Le code source est hébergé sur GitHub (référentiel public).
- Le référentiel inclut la documentation de configuration/utilisation et un suivi des problèmes.
- Le plugin a un signal de maintenance clair (mainteneur actif, mises à jour récentes ou gestion réactive des problèmes).

## Comment soumettre

Ouvrez une PR qui ajoute votre plugin à cette page avec :

- Nom du plugin
- Nom du package npm
- URL du référentiel GitHub
- Description d'une ligne
- Commande d'installation

## Barre d'examen

Nous préférons les plugins qui sont utiles, documentés et sûrs à utiliser.
Les wrappers peu élaborés, la propriété peu claire ou les packages non maintenus peuvent être refusés.

## Format candidat

Utilisez ce format lors de l'ajout d'entrées :

- **Nom du plugin** — description courte
  npm: `@scope/package`
  repo: `https://github.com/org/repo`
  install: `openclaw plugins install @scope/package`

## Plugins listés

- **WeChat** — Connectez OpenClaw aux comptes personnels WeChat via WeChatPadPro (protocole iPad). Supporte l'échange de texte, d'image et de fichier avec des conversations déclenchées par des mots-clés.
  npm: `@icesword760/openclaw-wechat`
  repo: `https://github.com/icesword0760/openclaw-wechat`
  install: `openclaw plugins install @icesword760/openclaw-wechat`
