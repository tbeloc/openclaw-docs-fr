---
summary: "Invoquer un seul outil directement via le point de terminaison HTTP de la passerelle"
read_when:
  - Calling tools without running a full agent turn
  - Building automations that need tool policy enforcement
title: "API Tools Invoke"
---

# Tools Invoke (HTTP)

La passerelle OpenClaw expose un point de terminaison HTTP simple pour invoquer un seul outil directement. Il est toujours activé, mais contrôlé par l'authentification de la passerelle et la politique des outils.

- `POST /tools/invoke`
- Même port que la passerelle (WS + HTTP multiplex) : `http://<gateway-host>:<port>/tools/invoke`

La taille maximale par défaut de la charge utile est de 2 Mo.

## Authentification

Utilise la configuration d'authentification de la passerelle. Envoyez un jeton porteur :

- `Authorization: Bearer <token>`

Remarques :

- Quand `gateway.auth.mode="token"`, utilisez `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
- Quand `gateway.auth.mode="password"`, utilisez `gateway.auth.password` (ou `OPENCLAW_GATEWAY_PASSWORD`).
- Si `gateway.auth.rateLimit` est configuré et que trop d'échecs d'authentification se produisent, le point de terminaison retourne `429` avec `Retry-After`.

## Corps de la requête

```json
{
  "tool": "sessions_list",
  "action": "json",
  "args": {},
  "sessionKey": "main",
  "dryRun": false
}
```

Champs :

- `tool` (chaîne, obligatoire) : nom de l'outil à invoquer.
- `action` (chaîne, optionnel) : mappé dans les arguments si le schéma de l'outil supporte `action` et que la charge utile des arguments l'a omis.
- `args` (objet, optionnel) : arguments spécifiques à l'outil.
- `sessionKey` (chaîne, optionnel) : clé de session cible. Si omis ou `"main"`, la passerelle utilise la clé de session principale configurée (respecte `session.mainKey` et l'agent par défaut, ou `global` dans la portée globale).
- `dryRun` (booléen, optionnel) : réservé pour un usage futur ; actuellement ignoré.

## Comportement de la politique et du routage

La disponibilité des outils est filtrée à travers la même chaîne de politique utilisée par les agents de la passerelle :

- `tools.profile` / `tools.byProvider.profile`
- `tools.allow` / `tools.byProvider.allow`
- `agents.<id>.tools.allow` / `agents.<id>.tools.byProvider.allow`
- politiques de groupe (si la clé de session correspond à un groupe ou un canal)
- politique de sous-agent (lors de l'invocation avec une clé de session de sous-agent)

Si un outil n'est pas autorisé par la politique, le point de terminaison retourne **404**.

HTTP de la passerelle applique également une liste de refus stricte par défaut (même si la politique de session autorise l'outil) :

- `sessions_spawn`
- `sessions_send`
- `gateway`
- `whatsapp_login`

Vous pouvez personnaliser cette liste de refus via `gateway.tools` :

```json5
{
  gateway: {
    tools: {
      // Outils supplémentaires à bloquer sur HTTP /tools/invoke
      deny: ["browser"],
      // Supprimer les outils de la liste de refus par défaut
      allow: ["gateway"],
    },
  },
}
```

Pour aider les politiques de groupe à résoudre le contexte, vous pouvez optionnellement définir :

- `x-openclaw-message-channel: <channel>` (exemple : `slack`, `telegram`)
- `x-openclaw-account-id: <accountId>` (quand plusieurs comptes existent)

## Réponses

- `200` → `{ ok: true, result }`
- `400` → `{ ok: false, error: { type, message } }` (requête invalide ou erreur d'entrée d'outil)
- `401` → non autorisé
- `429` → limité en débit d'authentification (`Retry-After` défini)
- `404` → outil non disponible (non trouvé ou non autorisé)
- `405` → méthode non autorisée
- `500` → `{ ok: false, error: { type, message } }` (erreur d'exécution d'outil inattendue ; message assaini)

## Exemple

```bash
curl -sS http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "tool": "sessions_list",
    "action": "json",
    "args": {}
  }'
```
