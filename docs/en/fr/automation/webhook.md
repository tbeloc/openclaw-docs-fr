---
summary: "Webhook ingress for wake and isolated agent runs"
read_when:
  - Adding or changing webhook endpoints
  - Wiring external systems into OpenClaw
title: "Webhooks"
---

# Webhooks

Gateway peut exposer un petit point de terminaison webhook HTTP pour les déclencheurs externes.

## Activer

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    // Optionnel : restreindre le routage explicite `agentId` à cette liste d'autorisation.
    // Omettez ou incluez "*" pour autoriser n'importe quel agent.
    // Définissez [] pour refuser tout routage explicite `agentId`.
    allowedAgentIds: ["hooks", "main"],
  },
}
```

Notes :

- `hooks.token` est requis quand `hooks.enabled=true`.
- `hooks.path` par défaut à `/hooks`.

## Authentification

Chaque requête doit inclure le jeton du hook. Préférez les en-têtes :

- `Authorization: Bearer <token>` (recommandé)
- `x-openclaw-token: <token>`
- Les jetons de chaîne de requête sont rejetés (`?token=...` retourne `400`).

## Points de terminaison

### `POST /hooks/wake`

Charge utile :

```json
{ "text": "System line", "mode": "now" }
```

- `text` **requis** (chaîne) : La description de l'événement (par exemple, « Nouvel e-mail reçu »).
- `mode` optionnel (`now` | `next-heartbeat`) : S'il faut déclencher un battement de cœur immédiat (par défaut `now`) ou attendre le prochain contrôle périodique.

Effet :

- Met en file d'attente un événement système pour la session **main**
- Si `mode=now`, déclenche un battement de cœur immédiat

### `POST /hooks/agent`

Charge utile :

```json
{
  "message": "Run this",
  "name": "Email",
  "agentId": "hooks",
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

- `message` **requis** (chaîne) : L'invite ou le message que l'agent doit traiter.
- `name` optionnel (chaîne) : Nom lisible pour le hook (par exemple, « GitHub »), utilisé comme préfixe dans les résumés de session.
- `agentId` optionnel (chaîne) : Acheminez ce hook vers un agent spécifique. Les ID inconnus reviennent à l'agent par défaut. Lorsqu'il est défini, le hook s'exécute en utilisant l'espace de travail et la configuration de l'agent résolu.
- `sessionKey` optionnel (chaîne) : La clé utilisée pour identifier la session de l'agent. Par défaut, ce champ est rejeté sauf si `hooks.allowRequestSessionKey=true`.
- `wakeMode` optionnel (`now` | `next-heartbeat`) : S'il faut déclencher un battement de cœur immédiat (par défaut `now`) ou attendre le prochain contrôle périodique.
- `deliver` optionnel (booléen) : Si `true`, la réponse de l'agent sera envoyée au canal de messagerie. Par défaut `true`. Les réponses qui sont uniquement des accusés de réception de battement de cœur sont automatiquement ignorées.
- `channel` optionnel (chaîne) : Le canal de messagerie pour la livraison. L'un de : `last`, `whatsapp`, `telegram`, `discord`, `slack`, `mattermost` (plugin), `signal`, `imessage`, `msteams`. Par défaut `last`.
- `to` optionnel (chaîne) : L'identifiant du destinataire pour le canal (par exemple, numéro de téléphone pour WhatsApp/Signal, ID de chat pour Telegram, ID de canal pour Discord/Slack/Mattermost (plugin), ID de conversation pour MS Teams). Par défaut le dernier destinataire de la session main.
- `model` optionnel (chaîne) : Remplacement du modèle (par exemple, `anthropic/claude-3-5-sonnet` ou un alias). Doit être dans la liste des modèles autorisés si restreint.
- `thinking` optionnel (chaîne) : Remplacement du niveau de réflexion (par exemple, `low`, `medium`, `high`).
- `timeoutSeconds` optionnel (nombre) : Durée maximale pour l'exécution de l'agent en secondes.

Effet :

- Exécute un tour d'agent **isolé** (clé de session propre)
- Affiche toujours un résumé dans la session **main**
- Si `wakeMode=now`, déclenche un battement de cœur immédiat

## Politique de clé de session (changement majeur)

Les remplacements de `sessionKey` de la charge utile `/hooks/agent` sont désactivés par défaut.

- Recommandé : définissez une `hooks.defaultSessionKey` fixe et gardez les remplacements de requête désactivés.
- Optionnel : autorisez les remplacements de requête uniquement si nécessaire, et restreignez les préfixes.

Configuration recommandée :

```json5
{
  hooks: {
    enabled: true,
    token: "${OPENCLAW_HOOKS_TOKEN}",
    defaultSessionKey: "hook:ingress",
    allowRequestSessionKey: false,
    allowedSessionKeyPrefixes: ["hook:"],
  },
}
```

Configuration de compatibilité (comportement hérité) :

```json5
{
  hooks: {
    enabled: true,
    token: "${OPENCLAW_HOOKS_TOKEN}",
    allowRequestSessionKey: true,
    allowedSessionKeyPrefixes: ["hook:"], // fortement recommandé
  },
}
```

### `POST /hooks/<name>` (mappé)

Les noms de hooks personnalisés sont résolus via `hooks.mappings` (voir configuration). Un mappage peut
transformer des charges utiles arbitraires en actions `wake` ou `agent`, avec des modèles optionnels ou
des transformations de code.

Options de mappage (résumé) :

- `hooks.presets: ["gmail"]` active le mappage Gmail intégré.
- `hooks.mappings` vous permet de définir `match`, `action` et des modèles dans la configuration.
- `hooks.transformsDir` + `transform.module` charge un module JS/TS pour la logique personnalisée.
  - `hooks.transformsDir` (s'il est défini) doit rester dans la racine des transformations sous votre répertoire de configuration OpenClaw (généralement `~/.openclaw/hooks/transforms`).
  - `transform.module` doit se résoudre dans le répertoire des transformations effectif (les chemins de traversée/échappement sont rejetés).
- Utilisez `match.source` pour conserver un point de terminaison d'ingestion générique (routage basé sur la charge utile).
- Les transformations TS nécessitent un chargeur TS (par exemple `bun` ou `tsx`) ou un `.js` précompilé au moment de l'exécution.
- Définissez `deliver: true` + `channel`/`to` sur les mappages pour acheminer les réponses vers une surface de chat
  (`channel` par défaut à `last` et revient à WhatsApp).
- `agentId` achemine le hook vers un agent spécifique ; les ID inconnus reviennent à l'agent par défaut.
- `hooks.allowedAgentIds` restreint le routage explicite `agentId`. Omettez-le (ou incluez `*`) pour autoriser n'importe quel agent. Définissez `[]` pour refuser le routage explicite `agentId`.
- `hooks.defaultSessionKey` définit la session par défaut pour les exécutions d'agent hook quand aucune clé explicite n'est fournie.
- `hooks.allowRequestSessionKey` contrôle si les charges utiles `/hooks/agent` peuvent définir `sessionKey` (par défaut : `false`).
- `hooks.allowedSessionKeyPrefixes` restreint optionnellement les valeurs `sessionKey` explicites des charges utiles de requête et des mappages.
- `allowUnsafeExternalContent: true` désactive le wrapper de sécurité du contenu externe pour ce hook
  (dangereux ; uniquement pour les sources internes de confiance).
- `openclaw webhooks gmail setup` écrit la configuration `hooks.gmail` pour `openclaw webhooks gmail run`.
  Voir [Gmail Pub/Sub](/automation/gmail-pubsub) pour le flux Gmail watch complet.

## Réponses

- `200` pour `/hooks/wake`
- `200` pour `/hooks/agent` (exécution asynchrone acceptée)
- `401` en cas d'échec d'authentification
- `429` après des échecs d'authentification répétés du même client (vérifiez `Retry-After`)
- `400` pour une charge utile invalide
- `413` pour les charges utiles surdimensionnées

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

Ajoutez `model` à la charge utile de l'agent (ou au mappage) pour remplacer le modèle pour cette exécution :

```bash
curl -X POST http://127.0.0.1:18789/hooks/agent \
  -H 'x-openclaw-token: SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Summarize inbox","name":"Email","model":"openai/gpt-5.2-mini"}'
```

Si vous appliquez `agents.defaults.models`, assurez-vous que le modèle de remplacement y est inclus.

```bash
curl -X POST http://127.0.0.1:18789/hooks/gmail \
  -H 'Authorization: Bearer SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"source":"gmail","messages":[{"from":"Ada","subject":"Hello","snippet":"Hi"}]}'
```

## Sécurité

- Gardez les points de terminaison des hooks derrière une boucle locale, un tailnet ou un proxy inverse de confiance.
- Utilisez un jeton de hook dédié ; ne réutilisez pas les jetons d'authentification de la passerelle.
- Les échecs d'authentification répétés sont limités en débit par adresse client pour ralentir les tentatives de force brute.
- Si vous utilisez le routage multi-agent, définissez `hooks.allowedAgentIds` pour limiter la sélection explicite `agentId`.
- Gardez `hooks.allowRequestSessionKey=false` sauf si vous avez besoin de sessions sélectionnées par l'appelant.
- Si vous activez la `sessionKey` de requête, restreignez `hooks.allowedSessionKeyPrefixes` (par exemple, `["hook:"]`).
- Évitez d'inclure les charges utiles brutes sensibles dans les journaux des webhooks.
- Les charges utiles des hooks sont traitées comme non fiables et enveloppées avec des limites de sécurité par défaut.
  Si vous devez désactiver cela pour un hook spécifique, définissez `allowUnsafeExternalContent: true`
  dans le mappage de ce hook (dangereux).
