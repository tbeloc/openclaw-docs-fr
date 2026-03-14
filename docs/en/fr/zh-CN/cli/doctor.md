---
read_when:
  - Vous rencontrez des problèmes de connexion/authentification et avez besoin d'une correction guidée
  - Vous souhaitez effectuer une vérification d'intégrité après une mise à jour
summary: "Référence CLI pour `openclaw doctor` (vérification de santé + correction guidée)"
title: doctor
x-i18n:
  generated_at: "2026-02-03T10:04:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 92310aa3f3d111e91a74ce1150359d5d8a8d70a856666d9419e16c60d78209f2
  source_path: cli/doctor.md
  workflow: 15
---

# `openclaw doctor`

Vérification de santé + correction rapide pour la passerelle et les canaux.

Contenu connexe :

- Dépannage : [Dépannage](/gateway/troubleshooting)
- Audit de sécurité : [Sécurité](/gateway/security)

## Exemples

```bash
openclaw doctor
openclaw doctor --repair
openclaw doctor --deep
```

Remarques :

- Les invites interactives (comme la correction du trousseau/OAuth) s'exécutent uniquement si stdin est un TTY et que `--non-interactive` n'est **pas** défini. Les exécutions sans interface (cron, Telegram, sans terminal) ignoreront les invites.
- `--fix` (alias de `--repair`) écrit une sauvegarde dans `~/.openclaw/openclaw.json.bak` et supprime les clés de configuration inconnues, tout en listant chaque élément supprimé.

## macOS : remplacement des variables d'environnement `launchctl`

Si vous avez précédemment exécuté `launchctl setenv OPENCLAW_GATEWAY_TOKEN ...` (ou `...PASSWORD`), cette valeur remplacera votre fichier de configuration et pourrait entraîner des erreurs "Non autorisé" persistantes.

```bash
launchctl getenv OPENCLAW_GATEWAY_TOKEN
launchctl getenv OPENCLAW_GATEWAY_PASSWORD

launchctl unsetenv OPENCLAW_GATEWAY_TOKEN
launchctl unsetenv OPENCLAW_GATEWAY_PASSWORD
```
