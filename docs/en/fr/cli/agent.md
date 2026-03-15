---
summary: "Référence CLI pour `openclaw agent` (envoyer un tour d'agent via la Gateway)"
read_when:
  - You want to run one agent turn from scripts (optionally deliver reply)
title: "agent"
---

# `openclaw agent`

Exécuter un tour d'agent via la Gateway (utilisez `--local` pour l'intégration).
Utilisez `--agent <id>` pour cibler directement un agent configuré.

Connexes :

- Outil d'envoi d'agent : [Agent send](/fr/tools/agent-send)

## Exemples

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

## Notes

- Lorsque cette commande déclenche la régénération de `models.json`, les identifiants de fournisseur gérés par SecretRef sont conservés en tant que marqueurs non-secrets (par exemple, les noms de variables d'environnement, `secretref-env:ENV_VAR_NAME`, ou `secretref-managed`), et non en tant que texte brut de secrets résolus.
- Les écritures de marqueurs sont source-autoritaires : OpenClaw persiste les marqueurs à partir de l'instantané de configuration source actif, et non à partir des valeurs de secrets résolus au moment de l'exécution.
