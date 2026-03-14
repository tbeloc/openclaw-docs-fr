---
read_when:
  - 添加或修改模型 CLI（models list/set/scan/aliases/fallbacks）
  - 更改模型回退行为或选择用户体验
  - 更新模型扫描探测（工具/图像）
summary: CLI des modèles : liste, définition, alias, repli, analyse, état
title: CLI des modèles
x-i18n:
  generated_at: "2026-02-03T10:05:42Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e8b54bb370b4f63a9b917594fb0f6ff48192e168196d30c713b8bbe72b78fef6
  source_path: concepts/models.md
  workflow: 15
---

# CLI des modèles

Consultez [/concepts/model-failover](/concepts/model-failover) pour en savoir plus sur la rotation des profils d'authentification, les délais d'attente et leur interaction avec le repli.
Aperçu rapide des fournisseurs + exemples : [/concepts/model-providers](/concepts/model-providers).

## Fonctionnement de la sélection de modèle

OpenClaw sélectionne les modèles dans l'ordre suivant :

1. Le modèle **principal** (`agents.defaults.model.primary` ou `agents.defaults.model`).
2. Les **replis** dans `agents.defaults.model.fallbacks` (dans l'ordre).
3. Le **basculement d'authentification du fournisseur** se produit au sein du fournisseur avant de passer au modèle suivant.

Éléments connexes :

- `agents.defaults.models` est une liste blanche/répertoire des modèles qu'OpenClaw peut utiliser (plus les alias).
- `agents.defaults.imageModel` n'est utilisé **que si** le modèle principal ne peut pas accepter les images.
- Les valeurs par défaut de chaque agent peuvent remplacer `agents.defaults.model` via `agents.list[].model` avec liaison (voir [/concepts/multi-agent](/concepts/multi-agent)).

## Recommandations rapides de modèles (règles empiriques)

- **GLM** : légèrement meilleur pour la programmation/appels d'outils.
- **MiniMax** : meilleur pour l'écriture et l'ambiance.

## Assistant d'installation (recommandé)

Si vous ne souhaitez pas modifier manuellement la configuration, exécutez l'assistant d'intégration :

```bash
openclaw onboard
```

Il peut configurer les modèles + l'authentification pour les fournisseurs courants, y compris l'**abonnement OpenAI Code (Codex)** (OAuth) et **Anthropic** (recommandé d'utiliser une clé API ; `claude setup-token` est également supporté).

## Clés de configuration (aperçu)

- `agents.defaults.model.primary` et `agents.defaults.model.fallbacks`
- `agents.defaults.imageModel.primary` et `agents.defaults.imageModel.fallbacks`
- `agents.defaults.models` (liste blanche + alias + paramètres du fournisseur)
- `models.providers` (fournisseurs personnalisés écrits dans `models.json`)

Les références de modèle sont normalisées en minuscules. Les alias de fournisseur comme `z.ai/*` sont normalisés en `zai/*`.

Des exemples de configuration de fournisseur (y compris OpenCode Zen) se trouvent dans [/gateway/configuration](/gateway/configuration#opencode-zen-multi-model-proxy).

## « Model is not allowed » (et pourquoi les réponses s'arrêtent)

Si `agents.defaults.models` est défini, il devient une **liste blanche** pour `/model` et les remplacements de session. Lorsqu'un utilisateur sélectionne un modèle qui ne figure pas dans cette liste blanche, OpenClaw retourne :

```
Model "provider/model" is not allowed. Use /model to list available models.
```

Cela se produit **avant** la génération normale de réponse, le message peut donc sembler « sans réponse ». Les solutions sont :

- Ajouter le modèle à `agents.defaults.models`, ou
- Effacer la liste blanche (supprimer `agents.defaults.models`), ou
- Sélectionner un modèle dans `/model list`.

Exemple de configuration de liste blanche :

```json5
{
  agent: {
    model: { primary: "anthropic/claude-sonnet-4-5" },
    models: {
      "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
      "anthropic/claude-opus-4-5": { alias: "Opus" },
    },
  },
}
```

## Changer de modèle dans le chat (`/model`)

Vous pouvez changer le modèle de la session actuelle sans redémarrer :

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model status
```

Remarques :

- `/model` (et `/model list`) est un sélecteur numéroté compact (familles de modèles + fournisseurs disponibles).
- `/model <#>` sélectionne dans ce sélecteur.
- `/model status` est une vue détaillée (candidats d'authentification, ainsi que les points de terminaison `baseUrl` du fournisseur + les modèles `api` lors de la configuration).
- Les références de modèle sont analysées en divisant au **premier** `/`. Utilisez `provider/model` lors de la saisie de `/model <ref>`.
- Si l'ID du modèle lui-même contient `/` (style OpenRouter), vous devez inclure le préfixe du fournisseur (par exemple : `/model openrouter/moonshotai/kimi-k2`).
- Si le fournisseur est omis, OpenClaw traite l'entrée comme un alias ou un modèle du **fournisseur par défaut** (valide uniquement si l'ID du modèle ne contient pas `/`).

Comportement complet des commandes/configuration : [Commandes slash](/tools/slash-commands).

## Commandes CLI

```bash
openclaw models list
openclaw models status
openclaw models set <provider/model>
openclaw models set-image <provider/model>

openclaw models aliases list
openclaw models aliases add <alias> <provider/model>
openclaw models aliases remove <alias>

openclaw models fallbacks list
openclaw models fallbacks add <provider/model>
openclaw models fallbacks remove <provider/model>
openclaw models fallbacks clear

openclaw models image-fallbacks list
openclaw models image-fallbacks add <provider/model>
openclaw models image-fallbacks remove <provider/model>
openclaw models image-fallbacks clear
```

`openclaw models` (sans sous-commande) est un raccourci pour `models status`.

### `models list`

Affiche les modèles configurés par défaut. Drapeaux utiles :

- `--all` : répertoire complet
- `--local` : fournisseurs locaux uniquement
- `--provider <name>` : filtrer par fournisseur
- `--plain` : un modèle par ligne
- `--json` : sortie lisible par machine

### `models status`

Affiche le modèle principal résolu, les replis, le modèle d'image, ainsi qu'un aperçu de l'authentification des fournisseurs configurés. Il affiche également l'état d'expiration OAuth des profils trouvés dans le magasin d'authentification (par défaut, avertissement dans les 24 heures). `--plain` imprime uniquement le modèle principal résolu.
L'état OAuth est toujours affiché (et inclus dans la sortie `--json`). Si un fournisseur configuré n'a pas d'identifiants, `models status` imprime une section **Missing auth**.
JSON inclut `auth.oauth` (fenêtre d'avertissement + profils) et `auth.providers` (authentification valide pour chaque fournisseur).
Utilisez `--check` pour l'automatisation (quitter avec `1` si manquant/expiré, `2` si sur le point d'expirer).

L'authentification Anthropic préférée est le jeton de configuration Claude Code CLI (exécutez n'importe où ; collez sur l'hôte Gateway si nécessaire) :

```bash
claude setup-token
openclaw models status
```

## Analyse (modèles gratuits OpenRouter)

`openclaw models scan` vérifie le **répertoire des modèles gratuits** d'OpenRouter et sonde optionnellement le support des outils et des images pour les modèles.

Drapeaux clés :

- `--no-probe` : ignorer la sonde en direct (métadonnées uniquement)
- `--min-params <b>` : nombre minimum de paramètres (milliards)
- `--max-age-days <days>` : ignorer les modèles plus anciens
- `--provider <name>` : filtrer par préfixe de fournisseur
- `--max-candidates <n>` : taille de la liste de repli
- `--set-default` : définir `agents.defaults.model.primary` sur le premier choix
- `--set-image` : définir `agents.defaults.imageModel.primary` sur le premier choix d'image

La sonde nécessite une clé API OpenRouter (à partir du profil d'authentification ou `OPENROUTER_API_KEY`). Sans clé, utilisez `--no-probe` pour lister uniquement les candidats.

Les résultats de l'analyse sont classés dans l'ordre suivant :

1. Support des images
2. Latence des outils
3. Taille du contexte
4. Nombre de paramètres

Entrées

- Liste OpenRouter `/models` (filtrée `:free`)
- Clé API OpenRouter requise à partir du profil d'authentification ou `OPENROUTER_API_KEY` (voir [/environment](/help/environment))
- Filtres optionnels : `--max-age-days`, `--min-params`, `--provider`, `--max-candidates`
- Contrôle de sonde : `--timeout`, `--concurrency`

Lors de l'exécution dans un TTY, vous pouvez sélectionner les replis de manière interactive. En mode non interactif, passez `--yes` pour accepter les valeurs par défaut.

## Registre des modèles (`models.json`)

Les fournisseurs personnalisés dans `models.providers` sont écrits dans `models.json` sous le répertoire de l'agent (par défaut `~/.openclaw/agents/<agentId>/models.json`). Ce fichier est fusionné par défaut, sauf si `models.mode` est défini sur `replace`.
