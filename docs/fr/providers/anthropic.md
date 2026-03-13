---
summary: "Utilisez Anthropic Claude via des clés API ou setup-token dans OpenClaw"
read_when:
  - You want to use Anthropic models in OpenClaw
  - You want setup-token instead of API keys
title: "Anthropic"
---

# Anthropic (Claude)

Anthropic développe la famille de modèles **Claude** et fournit un accès via une API.
Dans OpenClaw, vous pouvez vous authentifier avec une clé API ou un **setup-token**.

## Option A : clé API Anthropic

**Idéal pour :** l'accès API standard et la facturation à l'usage.
Créez votre clé API dans la console Anthropic.

### Configuration CLI

```bash
openclaw onboard
# choose: Anthropic API key

# or non-interactive
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
```

### Extrait de configuration

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Paramètres par défaut de la réflexion (Claude 4.6)

- Les modèles Anthropic Claude 4.6 utilisent par défaut la réflexion `adaptive` dans OpenClaw quand aucun niveau de réflexion explicite n'est défini.
- Vous pouvez remplacer par message (`/think:<level>`) ou dans les paramètres du modèle :
  `agents.defaults.models["anthropic/<model>"].params.thinking`.
- Documentation Anthropic associée :
  - [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
  - [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)

## Mode rapide (API Anthropic)

Le bouton bascule `/fast` partagé d'OpenClaw supporte également le trafic direct de clé API Anthropic.

- `/fast on` correspond à `service_tier: "auto"`
- `/fast off` correspond à `service_tier: "standard_only"`
- Configuration par défaut :

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-sonnet-4-5": {
          params: { fastMode: true },
        },
      },
    },
  },
}
```

Limites importantes :

- Ceci est **clé API uniquement**. L'authentification Anthropic setup-token / OAuth n'honore pas l'injection de niveau fast-mode d'OpenClaw.
- OpenClaw n'injecte les niveaux de service Anthropic que pour les requêtes directes `api.anthropic.com`. Si vous routez `anthropic/*` via un proxy ou une passerelle, `/fast` laisse `service_tier` inchangé.
- Anthropic rapporte le niveau effectif dans la réponse sous `usage.service_tier`. Sur les comptes sans capacité Priority Tier, `service_tier: "auto"` peut toujours se résoudre en `standard`.

## Mise en cache des invites (API Anthropic)

OpenClaw supporte la fonctionnalité de mise en cache des invites d'Anthropic. Ceci est **API uniquement** ; l'authentification par abonnement n'honore pas les paramètres de cache.

### Configuration

Utilisez le paramètre `cacheRetention` dans votre configuration de modèle :

| Valeur  | Durée du cache | Description                              |
| ------- | -------------- | ---------------------------------------- |
| `none`  | Pas de cache   | Désactiver la mise en cache des invites  |
| `short` | 5 minutes      | Par défaut pour l'authentification par clé API |
| `long`  | 1 heure        | Cache étendu (nécessite le drapeau beta) |

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" },
        },
      },
    },
  },
}
```

### Valeurs par défaut

Lors de l'utilisation de l'authentification par clé API Anthropic, OpenClaw applique automatiquement `cacheRetention: "short"` (cache de 5 minutes) pour tous les modèles Anthropic. Vous pouvez remplacer cela en définissant explicitement `cacheRetention` dans votre configuration.

### Remplacements de cacheRetention par agent

Utilisez les paramètres au niveau du modèle comme base de référence, puis remplacez les agents spécifiques via `agents.list[].params`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" }, // baseline for most agents
        },
      },
    },
    list: [
      { id: "research", default: true },
      { id: "alerts", params: { cacheRetention: "none" } }, // override for this agent only
    ],
  },
}
```

Ordre de fusion de la configuration pour les paramètres liés au cache :

1. `agents.defaults.models["provider/model"].params`
2. `agents.list[].params` (correspondant à `id`, remplace par clé)

Cela permet à un agent de conserver un cache de longue durée tandis qu'un autre agent sur le même modèle désactive la mise en cache pour éviter les coûts d'écriture sur le trafic par rafales/faible réutilisation.

### Notes sur Bedrock Claude

- Les modèles Anthropic Claude sur Bedrock (`amazon-bedrock/*anthropic.claude*`) acceptent le pass-through `cacheRetention` quand configuré.
- Les modèles Bedrock non-Anthropic sont forcés à `cacheRetention: "none"` à l'exécution.
- Les valeurs par défaut intelligentes de clé API Anthropic ensemencent également `cacheRetention: "short"` pour les références de modèle Claude-on-Bedrock quand aucune valeur explicite n'est définie.

### Paramètre hérité

Le paramètre `cacheControlTtl` plus ancien est toujours supporté pour la compatibilité rétroactive :

- `"5m"` correspond à `short`
- `"1h"` correspond à `long`

Nous recommandons de migrer vers le nouveau paramètre `cacheRetention`.

OpenClaw inclut le drapeau beta `extended-cache-ttl-2025-04-11` pour les requêtes API Anthropic ;
conservez-le si vous remplacez les en-têtes du fournisseur (voir [/gateway/configuration](/gateway/configuration)).

## Fenêtre de contexte 1M (bêta Anthropic)

La fenêtre de contexte 1M d'Anthropic est protégée par bêta. Dans OpenClaw, activez-la par modèle
avec `params.context1m: true` pour les modèles Opus/Sonnet supportés.

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { context1m: true },
        },
      },
    },
  },
}
```

OpenClaw mappe cela à `anthropic-beta: context-1m-2025-08-07` sur les requêtes Anthropic.

Ceci ne s'active que quand `params.context1m` est explicitement défini à `true` pour ce modèle.

Exigence : Anthropic doit autoriser l'utilisation de contexte long sur cette credential
(généralement facturation par clé API, ou un compte d'abonnement avec Extra Usage
activé). Sinon Anthropic retourne :
`HTTP 429: rate_limit_error: Extra usage is required for long context requests`.

Remarque : Anthropic rejette actuellement les requêtes bêta `context-1m-*` lors de l'utilisation
de tokens OAuth/abonnement (`sk-ant-oat-*`). OpenClaw ignore automatiquement l'en-tête bêta context1m pour l'authentification OAuth et conserve les bêtas OAuth requises.

## Option B : setup-token Claude

**Idéal pour :** utiliser votre abonnement Claude.

### Où obtenir un setup-token

Les setup-tokens sont créés par la **Claude Code CLI**, pas par la console Anthropic. Vous pouvez l'exécuter sur **n'importe quelle machine** :

```bash
claude setup-token
```

Collez le token dans OpenClaw (assistant : **Anthropic token (paste setup-token)**), ou exécutez-le sur l'hôte de la passerelle :

```bash
openclaw models auth setup-token --provider anthropic
```

Si vous avez généré le token sur une machine différente, collez-le :

```bash
openclaw models auth paste-token --provider anthropic
```

### Configuration CLI (setup-token)

```bash
# Collez un setup-token pendant l'intégration
openclaw onboard --auth-choice setup-token
```

### Extrait de configuration (setup-token)

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Remarques

- Générez le setup-token avec `claude setup-token` et collez-le, ou exécutez `openclaw models auth setup-token` sur l'hôte de la passerelle.
- Si vous voyez "OAuth token refresh failed …" sur un abonnement Claude, réauthentifiez-vous avec un setup-token. Voir [/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription](/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription).
- Les détails d'authentification + les règles de réutilisation sont dans [/concepts/oauth](/concepts/oauth).

## Dépannage

**Erreurs 401 / token soudainement invalide**

- L'authentification par abonnement Claude peut expirer ou être révoquée. Réexécutez `claude setup-token`
  et collez-le dans l'**hôte de la passerelle**.
- Si la connexion Claude CLI se trouve sur une machine différente, utilisez
  `openclaw models auth paste-token --provider anthropic` sur l'hôte de la passerelle.

**Aucune clé API trouvée pour le fournisseur "anthropic"**

- L'authentification est **par agent**. Les nouveaux agents n'héritent pas des clés de l'agent principal.
- Réexécutez l'intégration pour cet agent, ou collez un setup-token / clé API sur l'hôte de la passerelle,
  puis vérifiez avec `openclaw models status`.

**Aucune credential trouvée pour le profil `anthropic:default`**

- Exécutez `openclaw models status` pour voir quel profil d'authentification est actif.
- Réexécutez l'intégration, ou collez un setup-token / clé API pour ce profil.

**Aucun profil d'authentification disponible (tous en refroidissement/indisponibles)**

- Vérifiez `openclaw models status --json` pour `auth.unusableProfiles`.
- Ajoutez un autre profil Anthropic ou attendez le refroidissement.

Plus : [/gateway/troubleshooting](/gateway/troubleshooting) et [/help/faq](/help/faq).
