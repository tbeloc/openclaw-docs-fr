---
summary: "Configuration de Baseten pour Inkling et les API de modèles hébergés"
title: "Baseten"
read_when:
  - You want to run Thinking Machines Lab's Inkling in OpenClaw
  - You want one OpenAI-compatible API for Baseten's hosted models
---

[Les API de modèles Baseten](https://docs.baseten.co/inference/model-apis/overview) fournissent un accès hébergé et compatible avec OpenAI aux modèles de pointe. Le plugin externe officiel utilise la découverte authentifiée, donc OpenClaw suit l'ensemble complet des modèles activés pour votre compte Baseten. Son repli hors ligne contient chaque API de modèle disponible lors de la création de cette version d'OpenClaw.

| Propriété       | Valeur                                                   |
| --------------- | -------------------------------------------------------- |
| ID du fournisseur | `baseten`                                                |
| Plugin          | paquet externe officiel (`@openclaw/baseten-provider`) |
| Variable d'env d'authentification | `BASETEN_API_KEY`                                        |
| Drapeau d'intégration | `--auth-choice baseten-api-key`                          |
| Drapeau CLI direct | `--baseten-api-key <key>`                                |
| API             | Compatible OpenAI (`openai-completions`)                |
| URL de base      | `https://inference.baseten.co/v1`                       |
| Modèle par défaut | `baseten/thinkingmachines/inkling`                       |

## Installer le plugin

```bash
openclaw plugins install @openclaw/baseten-provider
openclaw gateway restart
```

## Démarrage rapide

<Steps>
  <Step title="Créer un compte Baseten et une clé API">
    Le plan Basic de Baseten n'a pas de frais mensuels de plateforme ; les appels à l'API de modèle sont facturés à l'usage. Créez une clé dans les [paramètres de clé API Baseten](https://app.baseten.co/settings/api_keys) et consultez les tarifs actuels sur la [page de tarification](https://www.baseten.co/pricing).
  </Step>
  <Step title="Exécuter l'intégration">
    <CodeGroup>

```bash Intégration
openclaw onboard --auth-choice baseten-api-key
```

```bash Drapeau direct
openclaw onboard --non-interactive \
  --auth-choice baseten-api-key \
  --baseten-api-key "$BASETEN_API_KEY"
```

```bash Env uniquement
export BASETEN_API_KEY=...
```

    </CodeGroup>

  </Step>
  <Step title="Vérifier le catalogue en direct">
    ```bash
    openclaw models list --provider baseten
    ```

    Avec une authentification utilisable, le plugin demande `GET /v1/models` et liste chaque modèle retourné pour le compte. Sans authentification, il reste hors ligne et utilise le repli fourni.

  </Step>
</Steps>

## Inkling

[Inkling de Thinking Machines Lab](https://thinkingmachines.ai/news/introducing-inkling/) est le modèle par défaut. Dans OpenClaw, il supporte l'entrée de texte et d'images, l'appel d'outils, les schémas d'outils structurés, l'effort de raisonnement configurable, une fenêtre de contexte de 1,048M jetons et jusqu'à 32k jetons de sortie :

```json5
{
  agents: {
    defaults: {
      model: { primary: "baseten/thinkingmachines/inkling" },
    },
  },
}
```

Utilisez `/model baseten/thinkingmachines/inkling` pour basculer un chat existant.

## Catalogue de repli fourni

Le catalogue en direct authentifié est autoritaire. Ces lignes gardent la configuration et la sélection de modèle utiles avant que la découverte réussisse :

| Référence du modèle                                | Entrée      | Contexte | Sortie max |
| -------------------------------------------------- | ----------- | -------: | ---------: |
| `baseten/deepseek-ai/DeepSeek-V4-Pro`              | texte       |    262k |       262k |
| `baseten/zai-org/GLM-4.7`                          | texte       |    200k |       200k |
| `baseten/zai-org/GLM-5`                            | texte       |    202k |       202k |
| `baseten/zai-org/GLM-5.1`                          | texte       |    202k |       202k |
| `baseten/zai-org/GLM-5.2`                          | texte       |    202k |       202k |
| `baseten/thinkingmachines/inkling`                 | texte, image |  1.048M |        32k |
| `baseten/moonshotai/Kimi-K2.5`                     | texte, image |    262k |       262k |
| `baseten/moonshotai/Kimi-K2.6`                     | texte, image |    262k |       262k |
| `baseten/moonshotai/Kimi-K2.7-Code`                | texte, image |    262k |       262k |
| `baseten/nvidia/Nemotron-120B-A12B`                | texte       |    202k |       202k |
| `baseten/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B` | texte       |    202k |       202k |
| `baseten/openai/gpt-oss-120b`                      | texte       |    128k |       128k |

Tous les modèles fournis supportent l'appel d'outils et le raisonnement. OpenClaw mappe ses niveaux de réflexion aux modèles avec `reasoning_effort` natif. Les modèles GLM, Kimi et Nemotron opt-in de Baseten désactivent par défaut la réflexion ; la plupart exposent un contrôle binaire activé/désactivé, tandis que GLM 5.2 expose désactivé, élevé et maximum. OpenClaw envoie ces choix via le contrôle `chat_template_args.enable_thinking` de Baseten et, pour GLM 5.2, le paramètre `reasoning_effort` validé au niveau supérieur.

<Note>
Baseten peut ajouter, supprimer ou modifier les API de modèles indépendamment des versions d'OpenClaw. Le plugin actualise les identifiants de modèles, les limites de contexte, les limites de sortie et les tarifs d'entrée, d'entrée en cache et de sortie à partir de l'API authentifiée tout en conservant la politique de transport spécifique au modèle d'OpenClaw.
</Note>

## Configuration manuelle

La plupart des configurations n'ont besoin que de la clé API. Pour épingler le fournisseur explicitement :

```json5
{
  env: { BASETEN_API_KEY: "..." },
  agents: {
    defaults: {
      model: { primary: "baseten/thinkingmachines/inkling" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      baseten: {
        baseUrl: "https://inference.baseten.co/v1",
        apiKey: "${BASETEN_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "thinkingmachines/inkling",
            name: "Inkling",
            reasoning: true,
            input: ["text", "image"],
            contextWindow: 1048000,
            maxTokens: 32000,
            compat: {
              supportsStore: false,
              supportsDeveloperRole: false,
              supportsUsageInStreaming: true,
              supportsStrictMode: true,
              supportsTools: true,
              supportsReasoningEffort: true,
              supportedReasoningEfforts: ["none", "minimal", "low", "medium", "high", "xhigh"],
              reasoningEffortMap: {
                off: "none",
                none: "none",
                adaptive: "xhigh",
                max: "xhigh",
              },
              maxTokensField: "max_tokens",
            },
          },
        ],
      },
    },
  },
}
```

<Note>
Si la passerelle s'exécute en tant que démon (launchd, systemd, Docker), assurez-vous que `BASETEN_API_KEY` est disponible pour ce processus. Une clé exportée uniquement dans un shell interactif n'est pas visible pour un service géré déjà en cours d'exécution.
</Note>

## Connexes

<CardGroup cols={2}>
  <Card title="Fournisseurs de modèles" href="/fr/concepts/model-providers" icon="layers">
    Choisir des fournisseurs, des références de modèles et un comportement de basculement.
  </Card>
  <Card title="Modes de réflexion" href="/fr/tools/thinking" icon="brain">
    Sélectionner les niveaux d'effort de raisonnement d'OpenClaw.
  </Card>
  <Card title="CLI Modèles" href="/fr/cli/models" icon="terminal">
    Lister, inspecter et sélectionner les modèles découverts.
  </Card>
  <Card title="FAQ Modèles" href="/fr/help/faq-models" icon="circle-question">
    Profils d'authentification et dépannage de la sélection de modèles.
  </Card>
</CardGroup>
