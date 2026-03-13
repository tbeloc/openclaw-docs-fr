---
summary: "Référence CLI pour `openclaw doctor` (vérifications de santé + réparations guidées)"
read_when:
  - Vous avez des problèmes de connectivité/authentification et souhaitez des corrections guidées
  - Vous avez effectué une mise à jour et souhaitez une vérification de cohérence
title: "doctor"
---

# `openclaw doctor`

Vérifications de santé + corrections rapides pour la passerelle et les canaux.

Connexes :

- Dépannage : [Dépannage](/gateway/troubleshooting)
- Audit de sécurité : [Sécurité](/gateway/security)

## Exemples

```bash
openclaw doctor
openclaw doctor --repair
openclaw doctor --deep
```

Notes :

- Les invites interactives (comme les corrections de trousseau/OAuth) s'exécutent uniquement lorsque stdin est un TTY et que `--non-interactive` n'est **pas** défini. Les exécutions sans terminal (cron, Telegram, pas de terminal) ignoreront les invites.
- `--fix` (alias pour `--repair`) écrit une sauvegarde dans `~/.openclaw/openclaw.json.bak` et supprime les clés de configuration inconnues, en listant chaque suppression.
- Les vérifications d'intégrité d'état détectent désormais les fichiers de transcription orphelins dans le répertoire des sessions et peuvent les archiver sous la forme `.deleted.<timestamp>` pour récupérer de l'espace en toute sécurité.
- Doctor analyse également `~/.openclaw/cron/jobs.json` (ou `cron.store`) pour les formes de tâches cron héritées et peut les réécrire sur place avant que le planificateur ne doive les normaliser automatiquement à l'exécution.
- Doctor inclut une vérification de disponibilité de la recherche en mémoire et peut recommander `openclaw configure --section model` lorsque les identifiants d'intégration sont manquants.
- Si le mode sandbox est activé mais que Docker n'est pas disponible, doctor signale un avertissement à fort signal avec correction (`installer Docker` ou `openclaw config set agents.defaults.sandbox.mode off`).

## macOS : remplacements d'env `launchctl`

Si vous avez précédemment exécuté `launchctl setenv OPENCLAW_GATEWAY_TOKEN ...` (ou `...PASSWORD`), cette valeur remplace votre fichier de configuration et peut causer des erreurs persistantes « non autorisé ».

```bash
launchctl getenv OPENCLAW_GATEWAY_TOKEN
launchctl getenv OPENCLAW_GATEWAY_PASSWORD

launchctl unsetenv OPENCLAW_GATEWAY_TOKEN
launchctl unsetenv OPENCLAW_GATEWAY_PASSWORD
```
