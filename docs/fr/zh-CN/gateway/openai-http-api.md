---
read_when:
  - 集成需要 OpenAI Chat Completions 的工具
summary: Exposer un point de terminaison HTTP /v1/chat/completions compatible avec OpenAI à partir de la passerelle Gateway
title: OpenAI Chat Completions
x-i18n:
  generated_at: "2026-02-03T07:48:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6f935777f489bff925a3bf18b1e4b7493f83ae7b1e581890092e5779af59b732
  source_path: gateway/openai-http-api.md
  workflow: 15
---

# OpenAI Chat Completions (HTTP)

La passerelle Gateway d'OpenClaw peut fournir un petit point de terminaison Chat Completions compatible avec OpenAI.

Ce point de terminaison est **désactivé par défaut**. Veuillez d'abord l'activer dans la configuration.

- `POST /v1/chat/completions`
- Même port que la passerelle Gateway (multiplexage WS + HTTP) : `http://<gateway-host>:<port>/v1/chat/completions`

Dans l'implémentation sous-jacente, les requêtes s'exécutent comme des exécutions d'agent Gateway ordinaires (même chemin de code que `openclaw agent`), donc le routage/les permissions/la configuration sont cohérents avec votre passerelle Gateway.

## Authentification

Utilisez la configuration d'authentification de la passerelle Gateway. Envoyez un jeton bearer :

- `Authorization: Bearer <token>`

Remarques :

- Quand `gateway.auth.mode="token"`, utilisez `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
- Quand `gateway.auth.mode="password"`, utilisez `gateway.auth.password` (ou `OPENCLAW_GATEWAY_PASSWORD`).

## Sélection de l'agent

Aucun en-tête personnalisé requis : encodez l'ID de l'agent dans le champ OpenAI `model` :

- `model: "openclaw:<agentId>"` (par exemple : `"openclaw:main"`, `"openclaw:beta"`)
- `model: "agent:<agentId>"` (alias)

Ou spécifiez un agent OpenClaw spécifique via un en-tête :

- `x-openclaw-agent-id: <agentId>` (par défaut : `main`)

Options avancées :

- `x-openclaw-session-key: <sessionKey>` pour un contrôle complet du routage des sessions.

## Activation du point de terminaison

Définissez `gateway.http.endpoints.chatCompletions.enabled` sur `true` :

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

Définissez `gateway.http.endpoints.chatCompletions.enabled` sur `false` :

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

## Comportement des sessions

Par défaut, le point de terminaison est **sans état par requête** (chaque appel génère une nouvelle clé de session).

Si la requête contient une chaîne OpenAI `user`, la passerelle Gateway en dérive une clé de session stable, de sorte que les appels répétés peuvent partager une session d'agent.

## Streaming (SSE)

Définissez `stream: true` pour recevoir des Server-Sent Events (SSE) :

- `Content-Type: text/event-stream`
- Chaque ligne d'événement est `data: <json>`
- Le flux se termine par `data: [DONE]`

## Exemples

Non-streaming :

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

Streaming :

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
