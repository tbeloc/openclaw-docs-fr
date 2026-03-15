---
title: "Mise en cache des invites"
summary: "Boutons de mise en cache des invites, ordre de fusion, comportement du fournisseur et modèles de réglage"
read_when:
  - You want to reduce prompt token costs with cache retention
  - You need per-agent cache behavior in multi-agent setups
  - You are tuning heartbeat and cache-ttl pruning together
---

# Mise en cache des invites

La mise en cache des invites signifie que le fournisseur de modèles peut réutiliser les préfixes d'invites inchangés (généralement les instructions système/développeur et autres contextes stables) entre les tours au lieu de les retraiter à chaque fois. La première demande correspondante écrit les jetons de cache (`cacheWrite`), et les demandes correspondantes ultérieures peuvent les relire (`cacheRead`).

Pourquoi c'est important : coût des jetons réduit, réponses plus rapides et performances plus prévisibles pour les sessions longues. Sans mise en cache, les invites répétées paient le coût complet de l'invite à chaque tour même si la plupart des entrées n'ont pas changé.

Cette page couvre tous les boutons liés au cache qui affectent la réutilisation des invites et le coût des jetons.

Pour les détails de tarification d'Anthropic, consultez :
[https://docs.anthropic.com/docs/build-with-claude/prompt-caching](https://docs.anthropic.com/docs/build-with-claude/prompt-caching)

## Boutons principaux

### `cacheRetention` (modèle et par agent)

Définir la rétention du cache sur les paramètres du modèle :

```yaml
agents:
  defaults:
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "short" # none | short | long
```

Remplacement par agent :

```yaml
agents:
  list:
    - id: "alerts"
      params:
        cacheRetention: "none"
```

Ordre de fusion de la configuration :

1. `agents.defaults.models["provider/model"].params`
2. `agents.list[].params` (correspondant à l'id de l'agent ; remplace par clé)

### `cacheControlTtl` hérité

Les valeurs héritées sont toujours acceptées et mappées :

- `5m` -> `short`
- `1h` -> `long`

Préférez `cacheRetention` pour la nouvelle configuration.

### `contextPruning.mode: "cache-ttl"`

Élague l'ancien contexte des résultats d'outils après les fenêtres TTL du cache afin que les demandes post-inactivité ne remettent pas en cache l'historique surdimensionné.

```yaml
agents:
  defaults:
    contextPruning:
      mode: "cache-ttl"
      ttl: "1h"
```

Voir [Élagage de session](/fr/concepts/session-pruning) pour le comportement complet.

### Battement de cœur pour maintenir la chaleur

Le battement de cœur peut maintenir les fenêtres de cache chaudes et réduire les écritures de cache répétées après les lacunes d'inactivité.

```yaml
agents:
  defaults:
    heartbeat:
      every: "55m"
```

Le battement de cœur par agent est pris en charge à `agents.list[].heartbeat`.

## Comportement du fournisseur

### Anthropic (API directe)

- `cacheRetention` est pris en charge.
- Avec les profils d'authentification par clé API Anthropic, OpenClaw amorce `cacheRetention: "short"` pour les références de modèles Anthropic lorsqu'elles ne sont pas définies.

### Amazon Bedrock

- Les références de modèles Anthropic Claude (`amazon-bedrock/*anthropic.claude*`) prennent en charge le passage explicite de `cacheRetention`.
- Les modèles Bedrock non-Anthropic sont forcés à `cacheRetention: "none"` au moment de l'exécution.

### Modèles Anthropic OpenRouter

Pour les références de modèles `openrouter/anthropic/*`, OpenClaw injecte `cache_control` Anthropic sur les blocs d'invites système/développeur pour améliorer la réutilisation du cache d'invites.

### Autres fournisseurs

Si le fournisseur ne prend pas en charge ce mode de cache, `cacheRetention` n'a aucun effet.

## Modèles de réglage

### Trafic mixte (défaut recommandé)

Conservez une ligne de base longue durée sur votre agent principal, désactivez la mise en cache sur les agents notificateurs en rafales :

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
  list:
    - id: "research"
      default: true
      heartbeat:
        every: "55m"
    - id: "alerts"
      params:
        cacheRetention: "none"
```

### Ligne de base axée sur les coûts

- Définir la ligne de base `cacheRetention: "short"`.
- Activer `contextPruning.mode: "cache-ttl"`.
- Gardez le battement de cœur en dessous de votre TTL uniquement pour les agents qui bénéficient de caches chauds.

## Diagnostics du cache

OpenClaw expose des diagnostics de trace de cache dédiés pour les exécutions d'agents intégrés.

### Configuration `diagnostics.cacheTrace`

```yaml
diagnostics:
  cacheTrace:
    enabled: true
    filePath: "~/.openclaw/logs/cache-trace.jsonl" # optional
    includeMessages: false # default true
    includePrompt: false # default true
    includeSystem: false # default true
```

Valeurs par défaut :

- `filePath`: `$OPENCLAW_STATE_DIR/logs/cache-trace.jsonl`
- `includeMessages`: `true`
- `includePrompt`: `true`
- `includeSystem`: `true`

### Bascules d'environnement (débogage ponctuel)

- `OPENCLAW_CACHE_TRACE=1` active le traçage du cache.
- `OPENCLAW_CACHE_TRACE_FILE=/path/to/cache-trace.jsonl` remplace le chemin de sortie.
- `OPENCLAW_CACHE_TRACE_MESSAGES=0|1` bascule la capture complète de la charge utile du message.
- `OPENCLAW_CACHE_TRACE_PROMPT=0|1` bascule la capture du texte d'invite.
- `OPENCLAW_CACHE_TRACE_SYSTEM=0|1` bascule la capture de l'invite système.

### Quoi inspecter

- Les événements de trace de cache sont JSONL et incluent des instantanés par étapes comme `session:loaded`, `prompt:before`, `stream:context` et `session:after`.
- L'impact des jetons de cache par tour est visible dans les surfaces d'utilisation normales via `cacheRead` et `cacheWrite` (par exemple `/usage full` et les résumés d'utilisation de session).

## Dépannage rapide

- `cacheWrite` élevé sur la plupart des tours : vérifiez les entrées d'invite système volatiles et vérifiez que le modèle/fournisseur prend en charge vos paramètres de cache.
- Aucun effet de `cacheRetention` : confirmez que la clé du modèle correspond à `agents.defaults.models["provider/model"]`.
- Demandes Bedrock Nova/Mistral avec paramètres de cache : forçage au moment de l'exécution attendu à `none`.

Documents connexes :

- [Anthropic](/fr/providers/anthropic)
- [Utilisation et coûts des jetons](/fr/reference/token-use)
- [Élagage de session](/fr/concepts/session-pruning)
- [Référence de configuration de la passerelle](/fr/gateway/configuration-reference)
