---
summary: "Configuration Meta (authentification + sélection du modèle muse-spark-1.1)"
title: "Meta"
read_when:
  - You want to use Meta with OpenClaw
  - You need the MODEL_API_KEY env var or CLI auth choice
---

L'**API Meta** utilise l'**API Responses** compatible OpenAI (`POST /v1/responses`)
pour le modèle de raisonnement `muse-spark-1.1`. Le fournisseur est fourni en tant que plugin OpenClaw intégré.

| Property          | Value                              |
| ----------------- | ---------------------------------- |
| Provider id       | `meta`                             |
| Plugin            | bundled provider                   |
| Auth env var      | `MODEL_API_KEY`                    |
| Onboarding flag   | `--auth-choice meta-api-key`       |
| Direct CLI flag   | `--meta-api-key <key>`             |
| API               | Responses API (`openai-responses`) |
| Base URL          | `https://api.ai.meta.com/v1`       |
| Default model     | `meta/muse-spark-1.1`              |
| Default reasoning | `high` (`reasoning.effort`)        |

## Démarrage rapide

<Steps>
  <Step title="Définir la clé API">
    <CodeGroup>

```bash Onboarding
openclaw onboard --auth-choice meta-api-key
```

```bash Direct flag
openclaw onboard --non-interactive --accept-risk \
  --auth-choice meta-api-key \
  --meta-api-key "$MODEL_API_KEY"
```

```bash Env only
export MODEL_API_KEY=<key>
```

    </CodeGroup>

  </Step>
  <Step title="Vérifier que les modèles sont disponibles">
    ```bash
    openclaw models list --provider meta
    ```

    Liste l'entrée du catalogue statique `muse-spark-1.1`. Si `MODEL_API_KEY` n'est pas résolu,
    `openclaw models status --json` signale les identifiants manquants sous
    `auth.unusableProfiles`.

  </Step>
</Steps>

## Configuration non-interactive

```bash
openclaw onboard --non-interactive --accept-risk \
  --mode local \
  --auth-choice meta-api-key \
  --meta-api-key "$MODEL_API_KEY"
```

## Catalogue intégré

| Model ref             | Name           | Reasoning | Context window | Max output |
| --------------------- | -------------- | --------- | -------------- | ---------- |
| `meta/muse-spark-1.1` | Muse Spark 1.1 | yes       | 1,048,576      | 128,000    |

Capacités :

- Entrée texte + image
- Appels d'outils et streaming
- Effort de raisonnement : `minimal`, `low`, `medium`, `high`, `xhigh` (par défaut : `high`)
- Relecture de raisonnement chiffré sans état (`store: false`, `include: ["reasoning.encrypted_content"]`)

<Warning>
`muse-spark-1.1` n'accepte pas `reasoning.effort: "none"`. OpenClaw mappe
`--thinking off` à `minimal` pour ce fournisseur.
</Warning>

<Note>
Jusqu'au déploiement de `muse-spark-1.1`, les tests de fumée et les vérifications manuelles peuvent utiliser
l'ID de modèle déployé `muse-spark` : `--model meta/muse-spark`.
</Note>

## Configuration manuelle

```json5
{
  env: { MODEL_API_KEY: "<key>" },
  agents: {
    defaults: {
      model: { primary: "meta/muse-spark-1.1" },
      models: {
        "meta/muse-spark-1.1": { alias: "Muse Spark 1.1" },
      },
    },
  },
}
```

<Note>
Si la Gateway s'exécute en tant que daemon (launchd, systemd, Docker), assurez-vous
que `MODEL_API_KEY` est disponible pour ce processus — par exemple dans
`~/.openclaw/.env` ou via `env.shellEnv`. Une clé exportée uniquement dans un
shell interactif ne sera pas utile à un service géré sauf si l'env est importé
séparément.
</Note>

## Test de fumée

```bash
export MODEL_API_KEY=<key>
export OPENCLAW_LIVE_TEST=1
export META_LIVE_TEST=1
pnpm test extensions/meta/meta.live.test.ts
```

Les tests en direct utilisent `muse-spark` déployé contre `POST /v1/responses`.

## Voir aussi

<CardGroup cols={2}>
  <Card title="Model providers" href="/fr/concepts/model-providers" icon="layers">
    Choosing providers, model refs, and failover behavior.
  </Card>
  <Card title="Thinking modes" href="/fr/tools/thinking" icon="brain">
    Reasoning effort levels for muse-spark-1.1.
  </Card>
  <Card title="Configuration reference" href="/fr/gateway/config-agents#agent-defaults" icon="gear">
    Agent defaults and model configuration.
  </Card>
</CardGroup>
