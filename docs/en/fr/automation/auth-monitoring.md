---
summary: "Surveiller l'expiration OAuth pour les fournisseurs de modèles"
read_when:
  - Configuration de la surveillance ou des alertes d'expiration d'authentification
  - Automatisation des vérifications d'actualisation OAuth Claude Code / Codex
title: "Surveillance de l'authentification"
---

# Surveillance de l'authentification

OpenClaw expose la santé de l'expiration OAuth via `openclaw models status`. Utilisez cela pour
l'automatisation et les alertes ; les scripts sont des extras optionnels pour les workflows téléphoniques.

## Préféré : vérification CLI (portable)

```bash
openclaw models status --check
```

Codes de sortie :

- `0` : OK
- `1` : identifiants expirés ou manquants
- `2` : expiration imminente (dans les 24h)

Cela fonctionne dans cron/systemd et ne nécessite aucun script supplémentaire.

## Scripts optionnels (workflows ops / téléphone)

Ceux-ci se trouvent sous `scripts/` et sont **optionnels**. Ils supposent un accès SSH à l'hôte
passerelle et sont optimisés pour systemd + Termux.

- `scripts/claude-auth-status.sh` utilise maintenant `openclaw models status --json` comme source
  de vérité (avec repli sur les lectures directes de fichiers si la CLI n'est pas disponible),
  donc gardez `openclaw` sur `PATH` pour les minuteurs.
- `scripts/auth-monitor.sh` : cible du minuteur cron/systemd ; envoie des alertes (ntfy ou téléphone).
- `scripts/systemd/openclaw-auth-monitor.{service,timer}` : minuteur utilisateur systemd.
- `scripts/claude-auth-status.sh` : vérificateur d'authentification Claude Code + OpenClaw (complet/json/simple).
- `scripts/mobile-reauth.sh` : flux de réauthentification guidé via SSH.
- `scripts/termux-quick-auth.sh` : statut du widget en un clic + ouverture de l'URL d'authentification.
- `scripts/termux-auth-widget.sh` : flux complet du widget guidé.
- `scripts/termux-sync-widget.sh` : synchronisation des identifiants Claude Code → OpenClaw.

Si vous n'avez pas besoin d'automatisation téléphonique ou de minuteurs systemd, ignorez ces scripts.
