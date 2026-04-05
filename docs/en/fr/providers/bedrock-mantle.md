---
summary: "Utilisez les modèles Amazon Bedrock Mantle (compatibles OpenAI) avec OpenClaw"
read_when:
  - You want to use Bedrock Mantle hosted OSS models with OpenClaw
  - You need the Mantle OpenAI-compatible endpoint for GPT-OSS, Qwen, Kimi, or GLM
title: "Amazon Bedrock Mantle"
---

# Amazon Bedrock Mantle

OpenClaw inclut un fournisseur **Amazon Bedrock Mantle** intégré qui se connecte
au point de terminaison compatible OpenAI de Mantle. Mantle héberge des modèles
open-source et tiers (GPT-OSS, Qwen, Kimi, GLM, et similaires) via une surface
standard `/v1/chat/completions` soutenue par l'infrastructure Bedrock.

## Ce qu'OpenClaw supporte

- Fournisseur : `amazon-bedrock-mantle`
- API : `openai-completions` (compatible OpenAI)
- Authentification : jeton bearer via `AWS_BEARER_TOKEN_BEDROCK`
- Région : `AWS_REGION` ou `AWS_DEFAULT_REGION` (par défaut : `us-east-1`)

## Découverte automatique des modèles

Lorsque `AWS_BEARER_TOKEN_BEDROCK` est défini, OpenClaw découvre automatiquement
les modèles Mantle disponibles en interrogeant le point de terminaison `/v1/models`
de la région. Les résultats de la découverte sont mis en cache pendant 1 heure.

Régions supportées : `us-east-1`, `us-east-2`, `us-west-2`, `ap-northeast-1`,
`ap-south-1`, `ap-southeast-3`, `eu-central-1`, `eu-west-1`, `eu-west-2`,
`eu-south-1`, `eu-north-1`, `sa-east-1`.

## Intégration

1. Définissez le jeton bearer sur l'**hôte de passerelle** :

```bash
export AWS_BEARER_TOKEN_BEDROCK="..."
# Optionnel (par défaut us-east-1) :
export AWS_REGION="us-west-2"
```

2. Vérifiez que les modèles sont découverts :

```bash
openclaw models list
```

Les modèles découverts apparaissent sous le fournisseur `amazon-bedrock-mantle`.
Aucune configuration supplémentaire n'est requise sauf si vous souhaitez
remplacer les valeurs par défaut.

## Configuration manuelle

Si vous préférez une configuration explicite plutôt que la découverte automatique :

```json5
{
  models: {
    providers: {
      "amazon-bedrock-mantle": {
        baseUrl: "https://bedrock-mantle.us-east-1.api.aws/v1",
        api: "openai-completions",
        auth: "api-key",
        apiKey: "env:AWS_BEARER_TOKEN_BEDROCK",
        models: [
          {
            id: "gpt-oss-120b",
            name: "GPT-OSS 120B",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 32000,
            maxTokens: 4096,
          },
        ],
      },
    },
  },
}
```

## Remarques

- Mantle nécessite actuellement un jeton bearer. Les identifiants IAM simples
  (rôles d'instance, SSO, clés d'accès) ne suffisent pas sans jeton.
- Le jeton bearer est le même `AWS_BEARER_TOKEN_BEDROCK` utilisé par le
  fournisseur standard [Amazon Bedrock](/fr/providers/bedrock).
- Le support du raisonnement est déduit des ID de modèles contenant des motifs
  comme `thinking`, `reasoner`, ou `gpt-oss-120b`.
- Si le point de terminaison Mantle est indisponible ou ne retourne aucun modèle,
  le fournisseur est silencieusement ignoré.
