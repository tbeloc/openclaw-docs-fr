---
read_when:
  - Configurer la surveillance ou les alertes d'expiration d'authentification
  - Vérifier automatiquement l'actualisation OAuth de Claude Code / Codex
summary: Surveiller l'état d'expiration OAuth du fournisseur de modèles
title: Surveillance de l'authentification
x-i18n:
  generated_at: "2026-02-03T10:03:53Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: eef179af9545ed7ab881f3ccbef998869437fb50cdb4088de8da7223b614fa2b
  source_path: automation/auth-monitoring.md
  workflow: 15
---

# Surveillance de l'authentification

OpenClaw fournit l'état de santé d'expiration OAuth via `openclaw models status`. Utilisez cette commande pour l'automatisation et les alertes ; les scripts sont des fonctionnalités supplémentaires optionnelles fournies pour les flux de travail mobiles.

## Approche recommandée : Vérification CLI (portable)

```bash
openclaw models status --check
```

Codes de sortie :

- `0` : Normal
- `1` : Identifiants expirés ou manquants
- `2` : Expiration imminente (dans les 24 heures)

Cette approche fonctionne avec cron/systemd sans scripts supplémentaires.

## Scripts optionnels (DevOps / flux de travail mobiles)

Ces scripts se trouvent dans le répertoire `scripts/` et sont **optionnels**. Ils supposent que vous avez accès SSH à l'hôte Gateway et ont été optimisés pour systemd + Termux.

- `scripts/claude-auth-status.sh` utilise maintenant `openclaw models status --json` comme source de données (avec repli sur la lecture directe des fichiers si la CLI n'est pas disponible), assurez-vous donc que `openclaw` se trouve dans le `PATH` du minuteur.
- `scripts/auth-monitor.sh` : cible du minuteur cron/systemd ; envoie des alertes (ntfy ou mobile).
- `scripts/systemd/openclaw-auth-monitor.{service,timer}` : minuteur utilisateur systemd.
- `scripts/claude-auth-status.sh` : vérificateur d'authentification Claude Code + OpenClaw (modes complet/json/concis).
- `scripts/mobile-reauth.sh` : flux de réauthentification guidé par SSH.
- `scripts/termux-quick-auth.sh` : widget de visualisation d'état en un clic + ouverture d'URL d'authentification.
- `scripts/termux-auth-widget.sh` : flux de widget guidé complet.
- `scripts/termux-sync-widget.sh` : synchronisation des identifiants Claude Code → OpenClaw.

Si vous n'avez pas besoin d'automatisation mobile ou de minuteurs systemd, vous pouvez ignorer ces scripts.
