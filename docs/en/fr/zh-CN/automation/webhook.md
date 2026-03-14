---
read_when:
  - Ajouter ou modifier un point de terminaison webhook
  - Intégrer des systèmes externes à OpenClaw
summary: Point d'entrée Webhook pour déclencher et isoler l'exécution des agents
title: Webhooks
x-i18n:
  generated_at: "2026-02-03T07:43:23Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f26b88864567be82366b1f66a4772ef2813c7846110c62fce6caf7313568265e
  source_path: automation/webhook.md
  workflow: 15
---

# Webhooks

La passerelle Gateway peut exposer un petit point de terminaison HTTP webhook pour les déclenchements externes.

## Activation

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
  },
}
```

Remarques :

- Lorsque `hooks.enabled=true`, `hooks.token` est obligatoire.
- `hooks.path` est par défaut `/hooks`.

## Authentification

Chaque requête doit inclure le jeton hook. Il est recommandé d'utiliser l'en-tête :

- `Authorization: Bearer <token>` (recommandé)
- `x-openclaw-token: <token>`
- `?token=<token>` (déprécié ; enregistrera un avertissement et sera supprimé dans une future version majeure)

## Points de terminaison

### `POST /hooks/wake`

Corps de la requête :

```json
{ "text": "System line", "mode": "now" }
```

- `text` **obligatoire** (chaîne) : description de l'événement (par exemple « Nouvel e-mail reçu »).
- `mode` optionnel (`now` | `next-heartbeat`) : déclencher immédiatement un battement de cœur (par défaut `now`) ou attendre le prochain contrôle périodique.

Effet :

- Ajoute un événement système à la file d'attente de la session **principale**
- Si `mode=now`, déclenche immédiatement un battement de cœur

### `POST /hooks/agent`

Corps de la requête :

```json
{
  "message": "Run this",
  "name": "Email",
  "sessionKey": "hook:email:msg-123",
  "wakeMode": "now",
  "deliver": true,
  "channel": "last",
  "to": "+15551234567",
  "model": "openai/gpt-5.2-mini",
  "thinking": "low",
  "timeoutSeconds": 120
}
```

- `message` **obligatoire** (chaîne) : invite ou message à traiter par l'agent.
- `name` optionnel (chaîne) : nom lisible du hook (par exemple « GitHub »), utilisé comme préfixe du résumé de session.
- `sessionKey` optionnel (chaîne) : clé pour identifier la session de l'agent. Par défaut, un `hook:<uuid>` aléatoire. Utiliser une clé cohérente permet les conversations multi-tours dans le contexte du hook.
- `wakeMode` optionnel (`now` | `next-heartbeat`) : déclencher immédiatement un battement de cœur (par défaut `now`) ou attendre le prochain contrôle périodique.
- `deliver` optionnel (booléen) : si `true`, la réponse de l'agent sera envoyée au canal de messages. Par défaut `true`. Seules les réponses confirmées par battement de cœur seront automatiquement ignorées.
- `channel` optionnel (chaîne) : canal de messages pour la livraison. Valeurs possibles : `last`, `whatsapp`, `telegram`, `discord`, `slack`, `mattermost` (plugin), `signal`, `imessage`, `msteams`. Par défaut `last`.
- `to` optionnel (chaîne) : identifiant du destinataire pour le canal (par exemple numéro de téléphone pour WhatsApp/Signal, ID de chat pour Telegram, ID de canal pour Discord/Slack/Mattermost (plugin), ID de session pour MS Teams). Par défaut, le dernier destinataire de la session principale.
- `model` optionnel (chaîne) : remplacement du modèle (par exemple `anthropic/claude-3-5-sonnet` ou alias). S'il y a des restrictions, doit être dans la liste des modèles autorisés.
- `thinking` optionnel (chaîne) : remplacement du niveau de réflexion (par exemple `low`, `medium`, `high`).
- `timeoutSeconds` optionnel (nombre) : durée maximale d'exécution de l'agent en secondes.

Effet :

- Exécute un tour d'agent **isolé** (clé de session indépendante)
- Publie toujours un résumé dans la session **principale**
- Si `wakeMode=now`, déclenche immédiatement un battement de cœur

### `POST /hooks/<name>` (mappages)

Les noms de hook personnalisés sont résolus via `hooks.mappings` (voir configuration). Les mappages peuvent convertir un corps de requête arbitraire en opérations `wake` ou `agent`, avec support optionnel de modèles ou transformations de code.

Options de mappage (résumé) :

- `hooks.presets: ["gmail"]` active le mappage Gmail intégré.
- `hooks.mappings` vous permet de définir `match`, `action` et des modèles dans la configuration.
- `hooks.transformsDir` + `transform.module` charge des modules JS/TS pour la logique personnalisée.
- Utiliser `match.source` pour maintenir un point de terminaison générique (routage basé sur le corps de la requête).
- Les transformations TS nécessitent un chargeur TS (par exemple `bun` ou `tsx`) ou des `.js` précompilés au runtime.
- Définir `deliver: true` + `channel`/`to` sur un mappage pour router les réponses vers l'interface de chat (`channel` par défaut `last`, repli sur WhatsApp).
- `allowUnsafeExternalContent: true` désactive l'enveloppe de sécurité du contenu externe pour ce hook (dangereux ; réservé aux sources internes de confiance).
- `openclaw webhooks gmail setup` écrit la configuration `hooks.gmail` pour `openclaw webhooks gmail run`. Pour le flux complet d'écoute Gmail, consultez [Gmail Pub/Sub](/automation/gmail-pubsub).

## Réponses

- `200` pour `/hooks/wake`
- `202` pour `/hooks/agent` (exécution asynchrone lancée)
- `401` authentification échouée
- `400` corps de requête invalide
- `413` corps de requête trop volumineux

## Exemples

```bash
curl -X POST http://127.0.0.1:18789/hooks/wake \
  -H 'Authorization: Bearer SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"text":"New email received","mode":"now"}'
```

```bash
curl -X POST http://127.0.0.1:18789/hooks/agent \
  -H 'x-openclaw-token: SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Summarize inbox","name":"Email","wakeMode":"next-heartbeat"}'
```

### Utiliser un modèle différent

Ajoutez `model` au corps de la requête d'agent (ou au mappage) pour remplacer le modèle pour cette exécution :

```bash
curl -X POST http://127.0.0.1:18789/hooks/agent \
  -H 'x-openclaw-token: SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Summarize inbox","name":"Email","model":"openai/gpt-5.2-mini"}'
```

Si vous avez activé la restriction `agents.defaults.models`, assurez-vous que le modèle remplacé y est inclus.

```bash
curl -X POST http://127.0.0.1:18789/hooks/gmail \
  -H 'Authorization: Bearer SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"source":"gmail","messages":[{"from":"Ada","subject":"Hello","snippet":"Hi"}]}'
```

## Sécurité

- Gardez le point de terminaison webhook derrière une boucle locale, un tailnet ou un proxy inverse de confiance.
- Utilisez un jeton hook dédié ; ne réutilisez pas le jeton d'authentification de la passerelle Gateway.
- Évitez d'inclure les corps de requête bruts sensibles dans les journaux webhook.
- Les corps de requête Hook sont par défaut traités comme non fiables et enveloppés avec une limite de sécurité. Si vous devez désactiver cela pour un hook spécifique, définissez `allowUnsafeExternalContent: true` dans le mappage de ce hook (dangereux).
