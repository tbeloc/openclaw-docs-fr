---
summary: "Exécuter OpenClaw via inferrs (serveur local compatible OpenAI)"
read_when:
  - Vous souhaitez exécuter OpenClaw contre un serveur inferrs local
  - Vous servez Gemma ou un autre modèle via inferrs
  - Vous avez besoin des drapeaux de compatibilité OpenClaw exacts pour inferrs
title: "inferrs"
---

# inferrs

[inferrs](https://github.com/ericcurtin/inferrs) peut servir des modèles locaux derrière une API `/v1` compatible OpenAI. OpenClaw fonctionne avec `inferrs` via le chemin générique `openai-completions`.

`inferrs` est actuellement mieux traité comme un backend auto-hébergé personnalisé compatible OpenAI, et non comme un plugin de fournisseur OpenClaw dédié.

## Démarrage rapide

1. Démarrez `inferrs` avec un modèle.

Exemple :

```bash
inferrs serve gg-hf-gg/gemma-4-E2B-it \
  --host 127.0.0.1 \
  --port 8080 \
  --device metal
```

2. Vérifiez que le serveur est accessible.

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/v1/models
```

3. Ajoutez une entrée de fournisseur OpenClaw explicite et pointez votre modèle par défaut vers celle-ci.

## Exemple de configuration complète

Cet exemple utilise Gemma 4 sur un serveur `inferrs` local.

```json5
{
  agents: {
    defaults: {
      model: { primary: "inferrs/gg-hf-gg/gemma-4-E2B-it" },
      models: {
        "inferrs/gg-hf-gg/gemma-4-E2B-it": {
          alias: "Gemma 4 (inferrs)",
        },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      inferrs: {
        baseUrl: "http://127.0.0.1:8080/v1",
        apiKey: "inferrs-local",
        api: "openai-completions",
        models: [
          {
            id: "gg-hf-gg/gemma-4-E2B-it",
            name: "Gemma 4 E2B (inferrs)",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 4096,
            compat: {
              requiresStringContent: true,
            },
          },
        ],
      },
    },
  },
}
```

## Pourquoi `requiresStringContent` est important

Certaines routes Chat Completions `inferrs` acceptent uniquement le contenu `messages[].content` sous forme de chaîne, et non des tableaux de parties de contenu structurées.

Si les exécutions OpenClaw échouent avec une erreur comme :

```text
messages[1].content: invalid type: sequence, expected a string
```

définissez :

```json5
compat: {
  requiresStringContent: true
}
```

OpenClaw aplatira les parties de contenu en texte pur en chaînes simples avant d'envoyer la demande.

## Caveat Gemma et tool-schema

Certaines combinaisons actuelles `inferrs` + Gemma acceptent de petites demandes directes `/v1/chat/completions` mais échouent toujours sur les tours complets du runtime d'agent OpenClaw.

Si cela se produit, essayez d'abord ceci :

```json5
compat: {
  requiresStringContent: true,
  supportsTools: false
}
```

Cela désactive la surface du schéma d'outils d'OpenClaw pour le modèle et peut réduire la pression d'invite sur les backends locaux plus stricts.

Si les minuscules demandes directes fonctionnent toujours mais que les tours d'agent OpenClaw normaux continuent de planter à l'intérieur de `inferrs`, le problème restant est généralement le comportement du modèle/serveur en amont plutôt que la couche de transport d'OpenClaw.

## Test de fumée manuel

Une fois configuré, testez les deux couches :

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"gg-hf-gg/gemma-4-E2B-it","messages":[{"role":"user","content":"What is 2 + 2?"}],"stream":false}'

openclaw infer model run \
  --model inferrs/gg-hf-gg/gemma-4-E2B-it \
  --prompt "What is 2 + 2? Reply with one short sentence." \
  --json
```

Si la première commande fonctionne mais que la seconde échoue, utilisez les notes de dépannage ci-dessous.

## Dépannage

- `curl /v1/models` échoue : `inferrs` n'est pas en cours d'exécution, n'est pas accessible, ou n'est pas lié à l'hôte/port attendu.
- `messages[].content ... expected a string` : définissez `compat.requiresStringContent: true`.
- Les appels directs minuscules `/v1/chat/completions` réussissent, mais `openclaw infer model run` échoue : essayez `compat.supportsTools: false`.
- OpenClaw n'obtient plus d'erreurs de schéma, mais `inferrs` plante toujours sur les tours d'agent plus importants : traitez-le comme une limitation en amont `inferrs` ou du modèle et réduisez la pression d'invite ou changez de backend/modèle local.

## Comportement de style proxy

`inferrs` est traité comme un backend proxy-style compatible OpenAI `/v1`, et non comme un point de terminaison OpenAI natif.

- la mise en forme des demandes spécifiques à OpenAI natif ne s'applique pas ici
- pas de `service_tier`, pas de `store` Responses, pas d'indices de cache d'invite, et pas de mise en forme de charge utile compatible avec le raisonnement OpenAI
- les en-têtes d'attribution OpenClaw cachés (`originator`, `version`, `User-Agent`) ne sont pas injectés sur les URL de base `inferrs` personnalisées

## Voir aussi

- [Modèles locaux](/fr/gateway/local-models)
- [Dépannage de la passerelle](/fr/gateway/troubleshooting#local-openai-compatible-backend-passes-direct-probes-but-agent-runs-fail)
- [Fournisseurs de modèles](/fr/concepts/model-providers)
