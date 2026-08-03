---
summary: "Installez le plugin WeCom officiel et trouvez sa documentation de configuration versionnée"
read_when:
  - Vous souhaitez connecter OpenClaw à WeCom
  - Vous avez besoin du plugin WeCom supporté et de sa documentation de configuration
title: "WeCom"
---

OpenClaw expose WeCom via le package externe
`@wecom/wecom-openclaw-plugin` maintenu par l'équipe Tencent WeCom.
Le plugin est listé dans le catalogue officiel des canaux OpenClaw mais n'est pas inclus
dans l'installation principale.

## Installation

```bash
openclaw channels add --channel wecom
openclaw gateway restart
openclaw channels status --channel wecom
```

Le catalogue OpenClaw installe une version exacte de
`@wecom/wecom-openclaw-plugin`.

## Configuration

Les identifiants WeCom, les modes de connexion, les routes de rappel et le comportement du contrôle d'accès
appartiennent au plugin externe et peuvent changer indépendamment d'
OpenClaw. Suivez la
[documentation du package](https://www.npmjs.com/package/@wecom/wecom-openclaw-plugin)
pour la version installée avant de configurer le canal.

Lors de la mise à niveau du plugin indépendamment, continuez à utiliser la documentation pour la
version installée.
