---
read_when:
  - Clients intégrant l'API OpenResponses
  - Vous devez baser sur l'entrée de l'item, les appels d'outils clients ou les événements SSE
summary: Exposer un point de terminaison HTTP /v1/responses compatible OpenResponses à partir de la passerelle Gateway
title: API OpenResponses
x-i18n:
  generated_at: "2026-02-03T07:48:43Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0597714837f8b210c38eeef53561894220c1473e54c56a5c69984847685d518c
  source_path: gateway/openresponses-http-api.md
  workflow: 15
---

# API OpenResponses (HTTP)

La passerelle Gateway d'OpenClaw peut fournir un point de terminaison `POST /v1/responses` compatible OpenResponses.

Ce point de terminaison est **désactivé par défaut**. Veuillez d'abord l'activer dans la configuration.

- `POST /v1/responses`
- Même port que la passerelle Gateway (multiplexage WS + HTTP) : `http://<gateway-host>:<port>/v1/responses`

En interne, les requêtes s'exécutent comme des exécutions normales d'agent Gateway (même chemin de code que `openclaw agent`), donc le routage/les permissions/la configuration correspondent à votre passerelle Gateway.

## Authentification

Utilisez la configuration d'authentification de la passerelle Gateway. Envoyez un jeton bearer :

- `Authorization: Bearer <token>`

Détails :

- Quand `gateway.auth.mode="token"`, utilisez `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
- Quand `gateway.auth.mode="password"`, utilisez `gateway.auth.password` (ou `OPENCLAW_GATEWAY_PASSWORD`).

## Sélection de l'agent

Pas besoin d'en-tête personnalisé : encodez l'ID de l'agent dans le champ OpenResponses `model` :

- `model: "openclaw:<agentId>"` (exemples : `"openclaw:main"`, `"openclaw:beta"`)
- `model: "agent:<agentId>"` (alias)

Ou spécifiez un agent OpenClaw spécifique via un en-tête :

- `x-openclaw-agent-id: <agentId>` (par défaut : `main`)

Avancé :

- `x-openclaw-session-key: <sessionKey>` pour un contrôle complet du routage de session.

## Activation du point de terminaison

Définissez `gateway.http.endpoints.responses.enabled` à `true` :

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: true },
      },
    },
  },
}
```

## Désactivation du point de terminaison

Définissez `gateway.http.endpoints.responses.enabled` à `false` :

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: false },
      },
    },
  },
}
```

## Comportement de session

Par défaut, le point de terminaison est **sans état pour chaque requête** (une nouvelle clé de session est générée à chaque appel).

Si la requête contient une chaîne OpenResponses `user`, la passerelle Gateway en dérive une clé de session stable, de sorte que les appels répétés peuvent partager une session d'agent.

## Structure de requête (supportée)

Les requêtes suivent l'API OpenResponses, en utilisant une entrée basée sur les items. Actuellement supporté :

- `input` : chaîne ou tableau d'objets item.
- `instructions` : fusionné dans l'invite système.
- `tools` : définitions d'outils clients (outils de fonction).
- `tool_choice` : filtrer ou exiger des outils clients.
- `stream` : activer le streaming SSE.
- `max_output_tokens` : limite de sortie au mieux (dépend du fournisseur).
- `user` : routage de session stable.

Accepté mais **actuellement ignoré** :

- `max_tool_calls`
- `reasoning`
- `metadata`
- `store`
- `previous_response_id`
- `truncation`

## Item (entrée)

### `message`

Rôles : `system`, `developer`, `user`, `assistant`.

- `system` et `developer` sont ajoutés à l'invite système.
- Le dernier item `user` ou `function_call_output` devient le « message actuel ».
- Les messages user/assistant antérieurs sont inclus comme historique de contexte.

### `function_call_output` (outils basés sur les tours)

Renvoyez les résultats d'outils au modèle :

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72F\"}"
}
```

### `reasoning` et `item_reference`

Acceptés pour la compatibilité de schéma, mais ignorés lors de la construction de l'invite.

## Outils (outils de fonction clients)

Fournissez des outils en utilisant `tools: [{ type: "function", function: { name, description?, parameters? } }]`.

Si l'agent décide d'appeler un outil, la réponse retourne un item de sortie `function_call`. Vous envoyez ensuite une requête ultérieure avec `function_call_output` pour continuer le tour.

## Images (`input_image`)

Support des sources base64 ou URL :

```json
{
  "type": "input_image",
  "source": { "type": "url", "url": "https://example.com/image.png" }
}
```

Types MIME autorisés (actuellement) : `image/jpeg`, `image/png`, `image/gif`, `image/webp`.
Taille maximale (actuellement) : 10 Mo.

## Fichiers (`input_file`)

Support des sources base64 ou URL :

```json
{
  "type": "input_file",
  "source": {
    "type": "base64",
    "media_type": "text/plain",
    "data": "SGVsbG8gV29ybGQh",
    "filename": "hello.txt"
  }
}
```

Types MIME autorisés (actuellement) : `text/plain`, `text/markdown`, `text/html`, `text/csv`, `application/json`, `application/pdf`.

Taille maximale (actuellement) : 5 Mo.

Comportement actuel :

- Le contenu du fichier est décodé et ajouté à l'**invite système**, et non au message utilisateur, il reste donc temporaire (non persistant dans l'historique de session).
- Les PDF sont analysés pour extraire le texte. Si peu de texte est trouvé, les premières pages sont rastérisées en images et transmises au modèle.

L'analyse PDF utilise la version legacy `pdfjs-dist` compatible Node (sans worker). La version moderne de PDF.js s'attend à des variables globales de worker/DOM du navigateur, elle n'est donc pas utilisée dans la passerelle Gateway.

Récupération d'URL par défaut :

- `files.allowUrl` : `true`
- `images.allowUrl` : `true`
- Les requêtes sont protégées (résolution DNS, blocage des IP privées, limite de redirections, délai d'expiration).

## Limites fichiers + images (configuration)

Les valeurs par défaut peuvent être ajustées sous `gateway.http.endpoints.responses` :

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          files: {
            allowUrl: true,
            allowedMimes: [
              "text/plain",
              "text/markdown",
              "text/html",
              "text/csv",
              "application/json",
              "application/pdf",
            ],
            maxBytes: 5242880,
            maxChars: 200000,
            maxRedirects: 3,
            timeoutMs: 10000,
            pdf: {
              maxPages: 4,
              maxPixels: 4000000,
              minTextChars: 200,
            },
          },
          images: {
            allowUrl: true,
            allowedMimes: ["image/jpeg", "image/png", "image/gif", "image/webp"],
            maxBytes: 10485760,
            maxRedirects: 3,
            timeoutMs: 10000,
          },
        },
      },
    },
  },
}
```

Valeurs par défaut en cas d'omission :

- `maxBodyBytes` : 20 Mo
- `files.maxBytes` : 5 Mo
- `files.maxChars` : 200 k
- `files.maxRedirects` : 3
- `files.timeoutMs` : 10 s
- `files.pdf.maxPages` : 4
- `files.pdf.maxPixels` : 4 000 000
- `files.pdf.minTextChars` : 200
- `images.maxBytes` : 10 Mo
- `images.maxRedirects` : 3
- `images.timeoutMs` : 10 s

## Streaming (SSE)

Définissez `stream: true` pour recevoir des Server-Sent Events (SSE) :

- `Content-Type: text/event-stream`
- Chaque ligne d'événement est `event: <type>` et `data: <json>`
- Le flux se termine par `data: [DONE]`

Types d'événements actuellement émis :

- `response.created`
- `response.in_progress`
- `response.output_item.added`
- `response.content_part.added`
- `response.output_text.delta`
- `response.output_text.done`
- `response.content_part.done`
- `response.output_item.done`
- `response.completed`
- `response.failed` (en cas d'erreur)

## Utilisation

`usage` est rempli quand le fournisseur sous-jacent rapporte les comptages de jetons.

## Erreurs

Les erreurs utilisent l'objet JSON suivant :

```json
{ "error": { "message": "...", "type": "invalid_request_error" } }
```

Cas courants :

- `401` authentification manquante/invalide
- `400` corps de requête invalide
- `405` mauvaise méthode

## Exemples

Non-streaming :

```bash
curl -sS http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "input": "hi"
  }'
```

Streaming :

```bash
curl -N http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "input": "hi"
  }'
```
