---
read_when:
  - 你想添加/删除渠道账户（WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost（插件）/Signal/iMessage）
  - 你想检查渠道状态或跟踪渠道日志
summary: "`openclaw channels` 的 CLI 参考（账户、状态、登录/登出、日志）"
title: channels
x-i18n:
  generated_at: "2026-02-03T07:44:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 16ab1642f247bfa96e8e08dfeb1eedfccb148f40d91099f5423f971df2b54e20
  source_path: cli/channels.md
  workflow: 15
---

# `openclaw channels`

Gérez les comptes de canaux de chat et leur état d'exécution sur la passerelle Gateway.

Documentation connexe :

- Guide des canaux : [Canaux](/channels/index)
- Configuration de la passerelle Gateway : [Configuration](/gateway/configuration)

## Commandes courantes

```bash
openclaw channels list
openclaw channels status
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels logs --channel all
```

## Ajouter/Supprimer des comptes

```bash
openclaw channels add --channel telegram --token <bot-token>
openclaw channels remove --channel telegram --delete
```

Conseil : `openclaw channels add --help` affiche les drapeaux pour chaque canal (token, app token, chemin signal-cli, etc.).

## Connexion/Déconnexion (interactif)

```bash
openclaw channels login --channel whatsapp
openclaw channels logout --channel whatsapp
```

## Dépannage

- Exécutez `openclaw status --deep` pour une sonde complète.
- Utilisez `openclaw doctor` pour obtenir une correction guidée.
- La sortie de `openclaw channels list` affiche `Claude: HTTP 403 ... user:profile` → L'instantané d'utilisation nécessite la portée de permission `user:profile`. Utilisez `--no-usage`, ou fournissez une clé de session claude.ai (`CLAUDE_WEB_SESSION_KEY` / `CLAUDE_WEB_COOKIE`), ou réautorisez via Claude Code CLI.

## Détection des capacités

Obtenez les conseils de capacités du fournisseur (intentions/portées disponibles) et le support des fonctionnalités statiques :

```bash
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
```

Remarques :

- `--channel` est facultatif ; l'omettre liste tous les canaux (y compris les extensions).
- `--target` accepte `channel:<id>` ou l'ID de canal numérique brut, applicable uniquement à Discord.
- La détection est spécifique au fournisseur : intentions Discord + permissions de canal optionnelles ; portées bot + utilisateur Slack ; drapeaux bot Telegram + webhook ; version du daemon Signal ; jeton d'application MS Teams + rôles/portées Graph (annotés aux emplacements connus). Les canaux sans capacité de détection rapportent `Probe: unavailable`.

## Résoudre les noms en ID

Utilisez le répertoire du fournisseur pour résoudre les noms de canaux/utilisateurs en ID :

```bash
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels resolve --channel discord "My Server/#support" "@someone"
openclaw channels resolve --channel matrix "Project Room"
```

Remarques :

- Utilisez `--kind user|group|auto` pour forcer le type de cible.
- Lorsque plusieurs entrées partagent le même nom, la résolution privilégie les correspondances actives.
