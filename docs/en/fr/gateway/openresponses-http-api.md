---
summary: "Exposer un point de terminaison HTTP /v1/responses compatible avec OpenResponses à partir de la Gateway"
read_when:
  - Intégration de clients qui utilisent l'API OpenResponses
  - Vous souhaitez des entrées basées sur des éléments, des appels d'outils clients ou des événements SSE
title: "API OpenResponses"
---

# API OpenResponses (HTTP)

La Gateway d'OpenClaw peut servir un point de terminaison `POST /v1/responses` compatible avec OpenResponses.

Ce point de terminaison est **désactivé par défaut**. Activez-le d'abord dans la configuration.

- `POST /v1/responses`
- Même port que la Gateway (WS + HTTP multiplex) : `http://<gateway-host>:<port>/v1/responses`

En arrière-plan, les requêtes sont exécutées comme une exécution normale d'agent Gateway (même chemin de code que
`openclaw agent`), donc le routage/les permissions/la configuration correspondent à votre Gateway.

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

Aucun en-tête personnalisé requis : encodez l'ID d'agent dans le champ OpenResponses `model` :

- `model: "openclaw:<agentId>"` (exemple : `"openclaw:main"`, `"openclaw:beta"`)
- `model: "agent:<agentId>"` (alias)

Ou ciblez un agent OpenClaw spécifique par en-tête :

- `x-openclaw-agent-id: <agentId>` (par défaut : `main`)

Avancé :

- `x-openclaw-session-key: <sessionKey>` pour contrôler complètement le routage de session.

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

Par défaut, le point de terminaison est **sans état par requête** (une nouvelle clé de session est générée à chaque appel).

Si la requête inclut une chaîne OpenResponses `user`, la Gateway dérive une clé de session stable
à partir de celle-ci, de sorte que les appels répétés peuvent partager une session d'agent.

## Forme de requête (supportée)

La requête suit l'API OpenResponses avec entrée basée sur des éléments. Support actuel :

- `input` : chaîne ou tableau d'objets d'élément.
- `instructions` : fusionnées dans l'invite système.
- `tools` : définitions d'outils clients (outils de fonction).
- `tool_choice` : filtrer ou exiger des outils clients.
- `stream` : active le streaming SSE.
- `max_output_tokens` : limite de sortie au mieux (dépend du fournisseur).
- `user` : routage de session stable.

Acceptés mais **actuellement ignorés** :

- `max_tool_calls`
- `reasoning`
- `metadata`
- `store`
- `previous_response_id`
- `truncation`

## Éléments (entrée)

### `message`

Rôles : `system`, `developer`, `user`, `assistant`.

- `system` et `developer` sont ajoutés à l'invite système.
- L'élément `user` ou `function_call_output` le plus récent devient le « message actuel ».
- Les messages utilisateur/assistant antérieurs sont inclus comme historique pour le contexte.

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

Acceptés pour la compatibilité de schéma mais ignorés lors de la construction de l'invite.

## Outils (outils de fonction côté client)

Fournissez des outils avec `tools: [{ type: "function", function: { name, description?, parameters? } }]`.

Si l'agent décide d'appeler un outil, la réponse retourne un élément de sortie `function_call`.
Vous envoyez ensuite une requête de suivi avec `function_call_output` pour continuer le tour.

## Images (`input_image`)

Supporte les sources base64 ou URL :

```json
{
  "type": "input_image",
  "source": { "type": "url", "url": "https://example.com/image.png" }
}
```

Types MIME autorisés (actuels) : `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `image/heic`, `image/heif`.
Taille max (actuelle) : 10 Mo.

## Fichiers (`input_file`)

Supporte les sources base64 ou URL :

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

Types MIME autorisés (actuels) : `text/plain`, `text/markdown`, `text/html`, `text/csv`,
`application/json`, `application/pdf`.

Taille max (actuelle) : 5 Mo.

Comportement actuel :

- Le contenu du fichier est décodé et ajouté à l'**invite système**, pas au message utilisateur,
  il reste donc éphémère (non persisté dans l'historique de session).
- Les PDF sont analysés pour le texte. Si peu de texte est trouvé, les premières pages sont rastérisées
  en images et transmises au modèle.

L'analyse PDF utilise la version héritée `pdfjs-dist` compatible Node (pas de worker). La version moderne
PDF.js s'attend à des workers/globals DOM du navigateur, elle n'est donc pas utilisée dans la Gateway.

Récupération d'URL par défaut :

- `files.allowUrl` : `true`
- `images.allowUrl` : `true`
- `maxUrlParts` : `8` (total des parties `input_file` + `input_image` basées sur URL par requête)
- Les requêtes sont gardées (résolution DNS, blocage d'IP privée, limites de redirection, délais d'expiration).
- Les listes blanches de noms d'hôte optionnelles sont supportées par type d'entrée (`files.urlAllowlist`, `images.urlAllowlist`).
  - Hôte exact : `"cdn.example.com"`
  - Sous-domaines avec caractères génériques : `"*.assets.example.com"` (ne correspond pas à l'apex)

## Limites de fichier + image (config)

Les valeurs par défaut peuvent être ajustées sous `gateway.http.endpoints.responses` :

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          maxUrlParts: 8,
          files: {
            allowUrl: true,
            urlAllowlist: ["cdn.example.com", "*.assets.example.com"],
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
            urlAllowlist: ["images.example.com"],
            allowedMimes: [
              "image/jpeg",
              "image/png",
              "image/gif",
              "image/webp",
              "image/heic",
              "image/heif",
            ],
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

Valeurs par défaut si omises :

- `maxBodyBytes` : 20 Mo
- `maxUrlParts` : 8
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
- Les sources `input_image` HEIC/HEIF sont acceptées et normalisées en JPEG avant la livraison au fournisseur.

Note de sécurité :

- Les listes blanches d'URL sont appliquées avant la récupération et sur les sauts de redirection.
- L'ajout d'un nom d'hôte à la liste blanche ne contourne pas le blocage d'IP privée/interne.
- Pour les gateways exposées à internet, appliquez des contrôles de sortie réseau en plus des gardes au niveau de l'application.
  Voir [Sécurité](/gateway/security).

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

Les erreurs utilisent un objet JSON comme :

```json
{ "error": { "message": "...", "type": "invalid_request_error" } }
```

Cas courants :

- `401` authentification manquante/invalide
- `400` corps de requête invalide
- `405` mauvaise méthode

## Exemples

Sans streaming :

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

Avec streaming :

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
