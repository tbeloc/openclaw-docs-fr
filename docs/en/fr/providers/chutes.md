---
title: "Chutes"
summary: "Configuration de Chutes (OAuth ou clé API, découverte de modèles, alias)"
read_when:
  - You want to use Chutes with OpenClaw
  - You need the OAuth or API key setup path
  - You want the default model, aliases, or discovery behavior
---

# Chutes

[Chutes](https://chutes.ai) expose les catalogues de modèles open-source via une
API compatible OpenAI. OpenClaw supporte à la fois OAuth dans le navigateur et
l'authentification par clé API directe pour le fournisseur `chutes` fourni.

- Fournisseur : `chutes`
- API : Compatible OpenAI
- URL de base : `https://llm.chutes.ai/v1`
- Authentification :
  - OAuth via `openclaw onboard --auth-choice chutes`
  - Clé API via `openclaw onboard --auth-choice chutes-api-key`
  - Variables d'environnement à l'exécution : `CHUTES_API_KEY`, `CHUTES_OAUTH_TOKEN`

## Démarrage rapide

### OAuth

```bash
openclaw onboard --auth-choice chutes
```

OpenClaw lance le flux du navigateur localement, ou affiche une URL + flux de
redirection-collage sur les hôtes distants/sans interface. Les jetons OAuth
s'actualisent automatiquement via les profils d'authentification OpenClaw.

Remplacements OAuth optionnels :

- `CHUTES_CLIENT_ID`
- `CHUTES_CLIENT_SECRET`
- `CHUTES_OAUTH_REDIRECT_URI`
- `CHUTES_OAUTH_SCOPES`

### Clé API

```bash
openclaw onboard --auth-choice chutes-api-key
```

Obtenez votre clé sur
[chutes.ai/settings/api-keys](https://chutes.ai/settings/api-keys).

Les deux chemins d'authentification enregistrent le catalogue Chutes fourni et
définissent le modèle par défaut sur `chutes/zai-org/GLM-4.7-TEE`.

## Comportement de découverte

Lorsque l'authentification Chutes est disponible, OpenClaw interroge le
catalogue Chutes avec cette credential et utilise les modèles découverts. Si la
découverte échoue, OpenClaw revient à un catalogue statique fourni pour que
l'intégration et le démarrage fonctionnent toujours.

## Alias par défaut

OpenClaw enregistre également trois alias de commodité pour le catalogue Chutes
fourni :

- `chutes-fast` -> `chutes/zai-org/GLM-4.7-FP8`
- `chutes-pro` -> `chutes/deepseek-ai/DeepSeek-V3.2-TEE`
- `chutes-vision` -> `chutes/chutesai/Mistral-Small-3.2-24B-Instruct-2506`

## Catalogue de démarrage intégré

Le catalogue de secours fourni inclut les références Chutes actuelles telles que :

- `chutes/zai-org/GLM-4.7-TEE`
- `chutes/zai-org/GLM-5-TEE`
- `chutes/deepseek-ai/DeepSeek-V3.2-TEE`
- `chutes/deepseek-ai/DeepSeek-R1-0528-TEE`
- `chutes/moonshotai/Kimi-K2.5-TEE`
- `chutes/chutesai/Mistral-Small-3.2-24B-Instruct-2506`
- `chutes/Qwen/Qwen3-Coder-Next-TEE`
- `chutes/openai/gpt-oss-120b-TEE`

## Exemple de configuration

```json5
{
  agents: {
    defaults: {
      model: { primary: "chutes/zai-org/GLM-4.7-TEE" },
      models: {
        "chutes/zai-org/GLM-4.7-TEE": { alias: "Chutes GLM 4.7" },
        "chutes/deepseek-ai/DeepSeek-V3.2-TEE": { alias: "Chutes DeepSeek V3.2" },
      },
    },
  },
}
```

## Notes

- Aide OAuth et exigences de l'application de redirection : [Documentation OAuth Chutes](https://chutes.ai/docs/sign-in-with-chutes/overview)
- La découverte par clé API et OAuth utilisent toutes deux le même identifiant de fournisseur `chutes`.
- Les modèles Chutes sont enregistrés sous la forme `chutes/<model-id>`.
