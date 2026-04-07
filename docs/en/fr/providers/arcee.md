---
title: "Arcee AI"
summary: "Configuration d'Arcee AI (authentification + sélection du modèle)"
read_when:
  - You want to use Arcee AI with OpenClaw
  - You need the API key env var or CLI auth choice
---

# Arcee AI

[Arcee AI](https://arcee.ai) fournit un accès à la famille de modèles Trinity mixture-of-experts via une API compatible OpenAI. Tous les modèles Trinity sont sous licence Apache 2.0.

Les modèles Arcee AI peuvent être accessibles directement via la plateforme Arcee ou via [OpenRouter](/fr/providers/openrouter).

- Fournisseur : `arcee`
- Authentification : `ARCEEAI_API_KEY` (direct) ou `OPENROUTER_API_KEY` (via OpenRouter)
- API : Compatible OpenAI
- URL de base : `https://api.arcee.ai/api/v1` (direct) ou `https://openrouter.ai/api/v1` (OpenRouter)

## Démarrage rapide

1. Obtenez une clé API depuis [Arcee AI](https://chat.arcee.ai/) ou [OpenRouter](https://openrouter.ai/keys).

2. Définissez la clé API (recommandé : stockez-la pour la Gateway) :

```bash
# Direct (plateforme Arcee)
openclaw onboard --auth-choice arceeai-api-key

# Via OpenRouter
openclaw onboard --auth-choice arceeai-openrouter
```

3. Définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "arcee/trinity-large-thinking" },
    },
  },
}
```

## Exemple non-interactif

```bash
# Direct (plateforme Arcee)
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice arceeai-api-key \
  --arceeai-api-key "$ARCEEAI_API_KEY"

# Via OpenRouter
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice arceeai-openrouter \
  --openrouter-api-key "$OPENROUTER_API_KEY"
```

## Note sur l'environnement

Si la Gateway s'exécute en tant que daemon (launchd/systemd), assurez-vous que `ARCEEAI_API_KEY`
(ou `OPENROUTER_API_KEY`) est disponible pour ce processus (par exemple, dans
`~/.openclaw/.env` ou via `env.shellEnv`).

## Catalogue intégré

OpenClaw est actuellement fourni avec ce catalogue Arcee groupé :

| Référence du modèle            | Nom                    | Entrée | Contexte | Coût (entrée/sortie par 1M) | Notes                                     |
| ------------------------------ | ---------------------- | ------ | -------- | --------------------------- | ----------------------------------------- |
| `arcee/trinity-large-thinking` | Trinity Large Thinking | texte | 256K     | $0.25 / $0.90               | Modèle par défaut ; raisonnement activé   |
| `arcee/trinity-large-preview`  | Trinity Large Preview  | texte | 128K     | $0.25 / $1.00               | Usage général ; 400B params, 13B actifs   |
| `arcee/trinity-mini`           | Trinity Mini 26B       | texte | 128K     | $0.045 / $0.15              | Rapide et économique ; function calling   |

Les mêmes références de modèle fonctionnent pour les configurations directes et OpenRouter (par exemple `arcee/trinity-large-thinking`).

Le préréglage d'intégration définit `arcee/trinity-large-thinking` comme modèle par défaut.

## Fonctionnalités supportées

- Streaming
- Utilisation d'outils / function calling
- Sortie structurée (mode JSON et schéma JSON)
- Pensée étendue (Trinity Large Thinking)
