```markdown
---
read_when:
  - 不运行完整智能体回合直接调用工具
  - 构建需要工具策略强制执行的自动化
summary: Appelez directement des outils individuels via le point de terminaison HTTP de la passerelle Gateway
title: API d'invocation d'outils
x-i18n:
  generated_at: "2026-02-03T07:48:58Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 17ccfbe0b0d9bb61cc46fb21f5c09b106ba6e8e4c2c14135a11ca8d5b77b8a88
  source_path: gateway/tools-invoke-http-api.md
  workflow: 15
---

# Invocation d'outils (HTTP)

La passerelle Gateway d'OpenClaw expose un simple point de terminaison HTTP pour invoquer directement des outils individuels. Il est toujours activé, mais soumis à l'authentification de la passerelle Gateway et aux restrictions de politique d'outils.

- `POST /tools/invoke`
- Même port que la passerelle Gateway (multiplexage WS + HTTP) : `http://<gateway-host>:<port>/tools/invoke`

La taille maximale de charge utile par défaut est de 2 Mo.

## Authentification

Utilisez la configuration d'authentification de la passerelle Gateway. Envoyez un jeton bearer :

- `Authorization: Bearer <token>`

Instructions :

- Quand `gateway.auth.mode="token"`, utilisez `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
- Quand `gateway.auth.mode="password"`, utilisez `gateway.auth.password` (ou `OPENCLAW_GATEWAY_PASSWORD`).

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

- `tool` (string, requis) : Nom de l'outil à invoquer.
- `action` (string, optionnel) : Mappé aux args si le schéma de l'outil supporte `action` et que la charge utile args l'omet.
- `args` (object, optionnel) : Paramètres spécifiques à l'outil.
- `sessionKey` (string, optionnel) : Clé de session cible. Si omis ou `"main"`, la passerelle Gateway utilise la clé de session principale configurée (en suivant `session.mainKey` et l'agent par défaut, ou en utilisant `global` au niveau global).
- `dryRun` (boolean, optionnel) : Réservé pour une utilisation future ; actuellement ignoré.

## Comportement de politique + routage

La disponibilité des outils est filtrée par la même chaîne de politique utilisée par l'agent de la passerelle Gateway :

- `tools.profile` / `tools.byProvider.profile`
- `tools.allow` / `tools.byProvider.allow`
- `agents.<id>.tools.allow` / `agents.<id>.tools.byProvider.allow`
- Politiques de groupe (si la clé de session mappe à un groupe ou un canal)
- Politiques de sous-agent (lors de l'invocation avec une clé de session de sous-agent)

Si l'outil n'est pas autorisé par la politique, le point de terminaison retourne **404**.

Pour aider à la résolution du contexte de politique de groupe, vous pouvez optionnellement définir :

- `x-openclaw-message-channel: <channel>` (exemple : `slack`, `telegram`)
- `x-openclaw-account-id: <accountId>` (quand plusieurs comptes existent)

## Réponse

- `200` → `{ ok: true, result }`
- `400` → `{ ok: false, error: { type, message } }` (requête invalide ou erreur d'outil)
- `401` → Non autorisé
- `404` → Outil non disponible (non trouvé ou non dans la liste d'autorisation)
- `405` → Méthode non autorisée

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
```
