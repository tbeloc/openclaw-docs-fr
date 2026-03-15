---
summary: "Référence CLI pour `openclaw models` (status/list/set/scan, alias, fallbacks, auth)"
read_when:
  - You want to change default models or view provider auth status
  - You want to scan available models/providers and debug auth profiles
title: "models"
---

# `openclaw models`

Découverte de modèles, analyse et configuration (modèle par défaut, fallbacks, profils d'authentification).

Liens connexes :

- Fournisseurs + modèles : [Models](/providers/models)
- Configuration de l'authentification du fournisseur : [Getting started](/start/getting-started)

## Commandes courantes

```bash
openclaw models status
openclaw models list
openclaw models set <model-or-alias>
openclaw models scan
```

`openclaw models status` affiche le modèle par défaut/fallbacks résolus ainsi qu'un aperçu de l'authentification.
Lorsque des snapshots d'utilisation du fournisseur sont disponibles, la section d'état OAuth/token inclut
les en-têtes d'utilisation du fournisseur.
Ajoutez `--probe` pour exécuter des sondes d'authentification en direct sur chaque profil de fournisseur configuré.
Les sondes sont des requêtes réelles (peuvent consommer des tokens et déclencher des limites de débit).
Utilisez `--agent <id>` pour inspecter l'état du modèle/authentification d'un agent configuré. Si omis,
la commande utilise `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR` s'il est défini, sinon l'agent
par défaut configuré.

Notes :

- `models set <model-or-alias>` accepte `provider/model` ou un alias.
- Les références de modèle sont analysées en divisant sur le **premier** `/`. Si l'ID du modèle inclut `/` (style OpenRouter), incluez le préfixe du fournisseur (exemple : `openrouter/moonshotai/kimi-k2`).
- Si vous omettez le fournisseur, OpenClaw traite l'entrée comme un alias ou un modèle pour le **fournisseur par défaut** (fonctionne uniquement s'il n'y a pas de `/` dans l'ID du modèle).
- `models status` peut afficher `marker(<value>)` dans la sortie d'authentification pour les espaces réservés non-secrets (par exemple `OPENAI_API_KEY`, `secretref-managed`, `minimax-oauth`, `qwen-oauth`, `ollama-local`) au lieu de les masquer comme des secrets.

### `models status`

Options :

- `--json`
- `--plain`
- `--check` (exit 1=expired/missing, 2=expiring)
- `--probe` (sonde en direct des profils d'authentification configurés)
- `--probe-provider <name>` (sonde un fournisseur)
- `--probe-profile <id>` (répéter ou IDs de profil séparés par des virgules)
- `--probe-timeout <ms>`
- `--probe-concurrency <n>`
- `--probe-max-tokens <n>`
- `--agent <id>` (ID d'agent configuré ; remplace `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR`)

## Alias + fallbacks

```bash
openclaw models aliases list
openclaw models fallbacks list
```

## Profils d'authentification

```bash
openclaw models auth add
openclaw models auth login --provider <id>
openclaw models auth setup-token
openclaw models auth paste-token
```

`models auth login` exécute le flux d'authentification d'un plugin de fournisseur (OAuth/clé API). Utilisez
`openclaw plugins list` pour voir quels fournisseurs sont installés.

Notes :

- `setup-token` demande une valeur de setup-token (générez-la avec `claude setup-token` sur n'importe quelle machine).
- `paste-token` accepte une chaîne de token générée ailleurs ou à partir d'une automatisation.
- Note de politique Anthropic : le support de setup-token est une compatibilité technique. Anthropic a bloqué certains usages d'abonnement en dehors de Claude Code par le passé, donc vérifiez les conditions actuelles avant de l'utiliser largement.
