---
read_when:
  - Ajouter ou modifier des points d'entrée CLI d'agent
summary: Exécuter directement `openclaw agent` CLI (avec livraison optionnelle)
title: Agent Send
x-i18n:
  generated_at: "2026-02-03T07:54:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a84d6a304333eebe155da2bf24cf5fc0482022a0a48ab34aa1465cd6e667022d
  source_path: tools/agent-send.md
  workflow: 15
---

# `openclaw agent`（exécution directe d'agent）

`openclaw agent` exécute un seul tour d'agent sans message de chat entrant.
Par défaut, il **s'exécute via la passerelle Gateway** ; ajoutez `--local` pour forcer l'exécution avec le runtime intégré sur la machine actuelle.

## Comportement

- Requis : `--message <text>`
- Sélection de session :
  - `--to <dest>` dérive une clé de session (les cibles de groupe/canal restent isolées ; les chats directs se réduisent à `main`), **ou**
  - `--session-id <id>` réutilise une session existante par ID, **ou**
  - `--agent <id>` cible directement un agent configuré (utilise la clé de session `main` de cet agent)
- Exécute le même runtime d'agent intégré que les réponses entrantes normales.
- Les drapeaux de réflexion/détail persistent dans le stockage de session.
- Sortie :
  - Par défaut : imprime le texte de réponse (plus les lignes `MEDIA:<url>`)
  - `--json` : imprime la charge utile structurée + métadonnées
- Livrez optionnellement la réponse au canal avec `--deliver` + `--channel` (le format cible correspond à `openclaw message --target`).
- Utilisez `--reply-channel`/`--reply-to`/`--reply-account` pour remplacer la livraison sans modifier la session.

Si la passerelle Gateway est inaccessible, la CLI **bascule** vers l'exécution locale intégrée.

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

- `--local` : exécution locale (nécessite des clés API de fournisseur de modèle dans votre shell)
- `--deliver` : envoie la réponse au canal sélectionné
- `--channel` : canal de livraison (`whatsapp|telegram|discord|googlechat|slack|signal|imessage`, par défaut : `whatsapp`)
- `--reply-to` : remplacement de la cible de livraison
- `--reply-channel` : remplacement du canal de livraison
- `--reply-account` : remplacement de l'ID de compte de livraison
- `--thinking <off|minimal|low|medium|high|xhigh>` : niveau de réflexion persistant (GPT-5.2 + modèles Codex uniquement)
- `--verbose <on|full|off>` : niveau de détail persistant
- `--timeout <seconds>` : remplace le délai d'expiration de l'agent
- `--json` : sortie JSON structurée
