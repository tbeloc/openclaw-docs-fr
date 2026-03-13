---
read_when:
  - Vous souhaitez modifier le modèle par défaut ou consulter l'état d'authentification du fournisseur
  - Vous souhaitez analyser les modèles/fournisseurs disponibles et déboguer la configuration d'authentification
summary: "Référence CLI pour `openclaw models` (status/list/set/scan, alias, fallback, authentification)"
title: models
x-i18n:
  generated_at: "2026-02-01T20:21:16Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 923b6ffc7de382ba25bc6e699f0515607e74877b39f2136ccdba2d99e1b1e9c3
  source_path: cli/models.md
  workflow: 14
---

# `openclaw models`

Découverte, analyse et configuration des modèles (modèle par défaut, fallback, configuration d'authentification).

Contenu connexe :

- Fournisseurs + modèles : [Modèles](/providers/models)
- Configuration d'authentification des fournisseurs : [Démarrage rapide](/start/getting-started)

## Commandes courantes

```bash
openclaw models status
openclaw models list
openclaw models set <model-or-alias>
openclaw models scan
```

`openclaw models status` affiche la configuration du modèle par défaut/fallback résolue ainsi qu'un aperçu de l'authentification.
Lorsque des snapshots d'utilisation des fournisseurs sont disponibles, la section d'état OAuth/token inclut les informations d'en-tête d'utilisation du fournisseur.
Ajoutez `--probe` pour exécuter des sondes d'authentification en temps réel sur chaque configuration de fournisseur configurée.
Les sondes envoient des requêtes réelles (qui peuvent consommer des tokens et déclencher des limites de débit).
Utilisez `--agent <id>` pour vérifier l'état du modèle/authentification d'un agent configuré. Lorsqu'il est omis,
la commande utilise `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR` (s'ils sont définis), sinon elle utilise
l'agent par défaut configuré.

Remarques :

- `models set <model-or-alias>` accepte `provider/model` ou un alias.
- Les références de modèle sont résolues en divisant au **premier** `/`. Si l'ID du modèle contient `/` (style OpenRouter), vous devez inclure le préfixe du fournisseur (exemple : `openrouter/moonshotai/kimi-k2`).
- Si le fournisseur est omis, OpenClaw traite l'entrée comme un alias ou un modèle du **fournisseur par défaut** (valide uniquement si l'ID du modèle ne contient pas `/`).

### `models status`

Options :

- `--json`
- `--plain`
- `--check` (code de sortie 1=expiré/manquant, 2=expiration imminente)
- `--probe` (sonde en temps réel des configurations d'authentification configurées)
- `--probe-provider <name>` (sonde un fournisseur unique)
- `--probe-profile <id>` (répétable ou IDs de profil séparés par des virgules)
- `--probe-timeout <ms>`
- `--probe-concurrency <n>`
- `--probe-max-tokens <n>`
- `--agent <id>` (ID d'agent configuré ; remplace `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR`)

## Alias + Fallback

```bash
openclaw models aliases list
openclaw models fallbacks list
```

## Configuration d'authentification

```bash
openclaw models auth add
openclaw models auth login --provider <id>
openclaw models auth setup-token
openclaw models auth paste-token
```

`models auth login` exécute le flux d'authentification du plugin du fournisseur (OAuth/clé API). Utilisez
`openclaw plugins list` pour voir les fournisseurs installés.

Remarques :

- `setup-token` vous invite à entrer la valeur du setup-token (généré avec `claude setup-token` sur n'importe quelle machine).
- `paste-token` accepte une chaîne de token générée ailleurs ou via l'automatisation.
