---
summary: "Exécutions directes de CLI `openclaw agent` (avec livraison optionnelle)"
read_when:
  - Adding or modifying the agent CLI entrypoint
title: "Agent Send"
---

# `openclaw agent` (exécutions directes d'agent)

`openclaw agent` exécute un seul tour d'agent sans nécessiter un message de chat entrant.
Par défaut, il passe **par la Gateway** ; ajoutez `--local` pour forcer le runtime intégré
sur la machine actuelle.

## Comportement

- Requis : `--message <text>`
- Sélection de session :
  - `--to <dest>` dérive la clé de session (les cibles de groupe/canal préservent l'isolation ; les chats directs s'effondrent en `main`), **ou**
  - `--session-id <id>` réutilise une session existante par id, **ou**
  - `--agent <id>` cible un agent configuré directement (utilise la clé de session `main` de cet agent)
- Exécute le même runtime d'agent intégré que les réponses entrantes normales.
- Les drapeaux de réflexion/verbosité persistent dans le magasin de session.
- Sortie :
  - par défaut : imprime le texte de réponse (plus les lignes `MEDIA:<url>`)
  - `--json` : imprime la charge utile structurée + métadonnées
- Livraison optionnelle vers un canal avec `--deliver` + `--channel` (les formats cibles correspondent à `openclaw message --target`).
- Utilisez `--reply-channel`/`--reply-to`/`--reply-account` pour remplacer la livraison sans modifier la session.

Si la Gateway est inaccessible, le CLI **bascule** vers l'exécution locale intégrée.

## Exemples

```bash
openclaw agent --to +15555550123 --message "status update"
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --to +15555550123 --message "Summon reply" --deliver
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

## Drapeaux

- `--local` : exécuter localement (nécessite les clés API du fournisseur de modèle dans votre shell)
- `--deliver` : envoyer la réponse au canal choisi
- `--channel` : canal de livraison (`whatsapp|telegram|discord|googlechat|slack|signal|imessage`, par défaut : `whatsapp`)
- `--reply-to` : remplacement de la cible de livraison
- `--reply-channel` : remplacement du canal de livraison
- `--reply-account` : remplacement de l'id de compte de livraison
- `--thinking <off|minimal|low|medium|high|xhigh>` : persister le niveau de réflexion (modèles GPT-5.2 + Codex uniquement)
- `--verbose <on|full|off>` : persister le niveau de verbosité
- `--timeout <seconds>` : remplacer le délai d'expiration de l'agent
- `--json` : sortie JSON structurée
