---
read_when:
  - 你想在 OpenClaw 中使用 Anthropic 模型
  - 你想使用 setup-token 而不是 API 密钥
summary: 在 OpenClaw 中通过 API 密钥或 setup-token 使用 Anthropic Claude
title: Anthropic
x-i18n:
  generated_at: "2026-02-03T10:08:33Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a78ccd855810a93e71d7138af4d3fc7d66e877349815c4a3207cf2214b0150b3
  source_path: providers/anthropic.md
  workflow: 15
---

# Anthropic (Claude)

Anthropic construit la famille de modèles **Claude** et fournit l'accès via une API.
Dans OpenClaw, vous pouvez vous authentifier à l'aide d'une clé API ou d'un **setup-token**.

## Option A : Clé API Anthropic

**Pour :** Accès API standard et facturation à l'usage.
Créez votre clé API dans la console Anthropic.

### Configuration CLI

```bash
openclaw onboard
# Sélectionnez : Anthropic API key

# Ou non-interactif
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
```

### Extrait de configuration

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

## Cache de prompts (API Anthropic)

OpenClaw prend en charge la fonctionnalité de cache de prompts d'Anthropic. Ceci est **API uniquement** ; l'authentification par abonnement ne supporte pas les paramètres de cache.

### Configuration

Utilisez le paramètre `cacheRetention` dans la configuration du modèle :

| Valeur  | Durée du cache | Description                          |
| ------- | -------------- | ------------------------------------ |
| `none`  | Pas de cache   | Désactiver le cache de prompts       |
| `short` | 5 minutes      | Valeur par défaut pour l'auth API    |
| `long`  | 1 heure        | Cache étendu (nécessite flag beta)   |

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-5": {
          params: { cacheRetention: "long" },
        },
      },
    },
  },
}
```

### Valeurs par défaut

Lors de l'authentification avec une clé API Anthropic, OpenClaw applique automatiquement `cacheRetention: "short"` (cache de 5 minutes) pour tous les modèles Anthropic. Vous pouvez remplacer ce paramètre en définissant explicitement `cacheRetention` dans votre configuration.

### Paramètres hérités

Pour la compatibilité rétroactive, le paramètre hérité `cacheControlTtl` est toujours supporté :

- `"5m"` correspond à `short`
- `"1h"` correspond à `long`

Nous recommandons de migrer vers le nouveau paramètre `cacheRetention`.

OpenClaw inclut le flag beta `extended-cache-ttl-2025-04-11` dans les requêtes API Anthropic ;
si vous remplacez les en-têtes du fournisseur, veuillez le conserver (voir [/gateway/configuration](/gateway/configuration)).

## Option B : Claude setup-token

**Pour :** Utiliser votre abonnement Claude.

### Où obtenir le setup-token

Le setup-token est créé par **Claude Code CLI**, pas par la console Anthropic. Vous pouvez l'exécuter sur **n'importe quelle machine** :

```bash
claude setup-token
```

Collez le token dans OpenClaw (assistant : **Anthropic token (paste setup-token)**), ou exécutez-le sur l'hôte Gateway :

```bash
openclaw models auth setup-token --provider anthropic
```

Si vous avez généré le token sur une machine différente, collez-le :

```bash
openclaw models auth paste-token --provider anthropic
```

### Configuration CLI

```bash
# Collez le setup-token pendant l'intégration
openclaw onboard --auth-choice setup-token
```

### Extrait de configuration

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

## Remarques

- Générez le setup-token avec `claude setup-token` et collez-le, ou exécutez `openclaw models auth setup-token` sur l'hôte Gateway.
- Si vous voyez "OAuth token refresh failed …" sur votre abonnement Claude, réauthentifiez-vous avec le setup-token. Voir [/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription](/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription).
- Les détails d'authentification + les règles de réutilisation sont dans [/concepts/oauth](/concepts/oauth).

## Dépannage

**Erreur 401 / Token soudainement invalide**

- L'authentification par abonnement Claude peut avoir expiré ou être révoquée. Réexécutez `claude setup-token`
  et collez-le sur l'**hôte Gateway**.
- Si la connexion Claude CLI est sur une machine différente, utilisez
  `openclaw models auth paste-token --provider anthropic` sur l'hôte Gateway.

**No API key found for provider "anthropic"**

- L'authentification est **par agent**. Les nouveaux agents n'héritent pas de la clé de l'agent principal.
- Réexécutez l'intégration pour cet agent, ou collez le setup-token / la clé API sur l'hôte Gateway,
  puis vérifiez avec `openclaw models status`.

**No credentials found for profile `anthropic:default`**

- Exécutez `openclaw models status` pour voir quel profil d'authentification est actif.
- Réexécutez l'intégration, ou collez le setup-token / la clé API pour ce profil.

**No available auth profile (all in cooldown/unavailable)**

- Vérifiez `auth.unusableProfiles` dans `openclaw models status --json`.
- Ajoutez un autre profil Anthropic ou attendez la fin de la période de refroidissement.

Plus d'informations : [/gateway/troubleshooting](/gateway/troubleshooting) et [/help/faq](/help/faq).
