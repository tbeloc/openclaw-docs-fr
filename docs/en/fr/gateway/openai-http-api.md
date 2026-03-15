---
summary: "Exposer un point de terminaison HTTP /v1/chat/completions compatible avec OpenAI à partir de la Gateway"
read_when:
  - Integrating tools that expect OpenAI Chat Completions
title: "OpenAI Chat Completions"
---

# OpenAI Chat Completions (HTTP)

La Gateway d'OpenClaw peut servir un petit point de terminaison Chat Completions compatible avec OpenAI.

Ce point de terminaison est **désactivé par défaut**. Activez-le d'abord dans la configuration.

- `POST /v1/chat/completions`
- Même port que la Gateway (WS + HTTP multiplex) : `http://<gateway-host>:<port>/v1/chat/completions`

En arrière-plan, les requêtes sont exécutées comme une exécution normale d'agent Gateway (même chemin de code que `openclaw agent`), donc le routage/les permissions/la configuration correspondent à votre Gateway.

## Authentification

Utilise la configuration d'authentification de la Gateway. Envoyez un jeton bearer :

- `Authorization: Bearer <token>`

Notes :

- Quand `gateway.auth.mode="token"`, utilisez `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
- Quand `gateway.auth.mode="password"`, utilisez `gateway.auth.password` (ou `OPENCLAW_GATEWAY_PASSWORD`).
- Si `gateway.auth.rateLimit` est configuré et que trop d'échecs d'authentification se produisent, le point de terminaison retourne `429` avec `Retry-After`.

## Limite de sécurité (important)

Traitez ce point de terminaison comme une surface d'**accès complet opérateur** pour l'instance de la gateway.

- L'authentification bearer HTTP ici n'est pas un modèle de portée étroite par utilisateur.
- Un jeton/mot de passe Gateway valide pour ce point de terminaison doit être traité comme une credential propriétaire/opérateur.
- Les requêtes s'exécutent via le même chemin d'agent du plan de contrôle que les actions d'opérateur de confiance.
- Il n'y a pas de limite d'outil séparé non-propriétaire/par-utilisateur sur ce point de terminaison ; une fois qu'un appelant passe l'authentification Gateway ici, OpenClaw traite cet appelant comme un opérateur de confiance pour cette gateway.
- Si la politique d'agent cible autorise les outils sensibles, ce point de terminaison peut les utiliser.
- Gardez ce point de terminaison sur loopback/tailnet/ingress privé uniquement ; ne l'exposez pas directement à l'internet public.

Voir [Sécurité](/gateway/security) et [Accès distant](/gateway/remote).

## Choisir un agent

Aucun en-tête personnalisé requis : encodez l'id d'agent dans le champ OpenAI `model` :

- `model: "openclaw:<agentId>"` (exemple : `"openclaw:main"`, `"openclaw:beta"`)
- `model: "agent:<agentId>"` (alias)

Ou ciblez un agent OpenClaw spécifique par en-tête :

- `x-openclaw-agent-id: <agentId>` (par défaut : `main`)

Avancé :

- `x-openclaw-session-key: <sessionKey>` pour contrôler complètement le routage de session.

## Activation du point de terminaison

Définissez `gateway.http.endpoints.chatCompletions.enabled` à `true` :

```json5
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: true },
      },
    },
  },
}
```

## Désactivation du point de terminaison

Définissez `gateway.http.endpoints.chatCompletions.enabled` à `false` :

```json5
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: false },
      },
    },
  },
}
```

## Comportement de session

Par défaut, le point de terminaison est **sans état par requête** (une nouvelle clé de session est générée à chaque appel).

Si la requête inclut une chaîne OpenAI `user`, la Gateway en dérive une clé de session stable, de sorte que les appels répétés peuvent partager une session d'agent.

## Streaming (SSE)

Définissez `stream: true` pour recevoir des Server-Sent Events (SSE) :

- `Content-Type: text/event-stream`
- Chaque ligne d'événement est `data: <json>`
- Le flux se termine par `data: [DONE]`

## Exemples

Sans streaming :

```bash
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "messages": [{"role":"user","content":"hi"}]
  }'
```

Avec streaming :

```bash
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "messages": [{"role":"user","content":"hi"}]
  }'
```
