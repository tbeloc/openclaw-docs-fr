---
read_when:
  - Vous devez savoir quelles variables d'environnement sont chargées et dans quel ordre
  - Vous déboguez une clé API manquante dans la passerelle Gateway
  - Vous écrivez de la documentation pour l'authentification des fournisseurs ou les environnements de déploiement
summary: D'où OpenClaw charge les variables d'environnement et l'ordre de priorité
title: Variables d'environnement
x-i18n:
  generated_at: "2026-02-03T07:47:11Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b49ae50e5d306612f89f93a86236188a4f2ec23f667e2388b043832be3ac1546
  source_path: help/environment.md
  workflow: 15
---

# Variables d'environnement

OpenClaw extrait les variables d'environnement de plusieurs sources. La règle est **de ne jamais écraser les valeurs existantes**.

## Ordre de priorité (du plus élevé au plus bas)

1. **Environnement du processus** (ce que le processus de passerelle Gateway a déjà du shell/daemon parent).
2. **`.env` dans le répertoire de travail actuel** (dotenv par défaut ; ne pas écraser).
3. **`.env` global** situé à `~/.openclaw/.env` (c'est-à-dire `$OPENCLAW_STATE_DIR/.env` ; ne pas écraser).
4. **Bloc `env` de configuration** situé à `~/.openclaw/openclaw.json` (appliqué uniquement s'il manque).
5. **Importation optionnelle du shell de connexion** (`env.shellEnv.enabled` ou `OPENCLAW_LOAD_SHELL_ENV=1`), appliquée uniquement aux noms de clés attendues manquantes.

Si le fichier de configuration est complètement absent, l'étape 4 sera ignorée ; si l'importation du shell est activée, elle s'exécutera quand même.

## Bloc `env` de configuration

Deux façons équivalentes de définir des variables d'environnement en ligne (les deux ne remplacent pas) :

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

## Importation de l'environnement du shell

`env.shellEnv` exécute votre shell de connexion et importe uniquement les noms de clés attendues **manquantes** :

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Équivalents de variables d'environnement :

- `OPENCLAW_LOAD_SHELL_ENV=1`
- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

## Substitution de variables d'environnement dans la configuration

Vous pouvez référencer les variables d'environnement directement dans les valeurs de chaîne de configuration en utilisant la syntaxe `${VAR_NAME}` :

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
}
```

Pour plus de détails, consultez [Configuration : Substitution de variables d'environnement](/gateway/configuration#env-var-substitution-in-config).

## Contenu connexe

- [Configuration de la passerelle Gateway](/gateway/configuration)
- [FAQ : Variables d'environnement et chargement de .env](/help/faq#env-vars-and-env-loading)
- [Aperçu des modèles](/concepts/models)
