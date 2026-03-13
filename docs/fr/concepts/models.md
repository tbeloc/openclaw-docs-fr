---
summary: "CLI Modèles : list, set, aliases, fallbacks, scan, status"
read_when:
  - Adding or modifying models CLI (models list/set/scan/aliases/fallbacks)
  - Changing model fallback behavior or selection UX
  - Updating model scan probes (tools/images)
title: "CLI Modèles"
---

# CLI Modèles

Voir [/concepts/model-failover](/concepts/model-failover) pour la rotation des profils d'authentification,
les délais d'attente et leur interaction avec les fallbacks.
Aperçu rapide des fournisseurs + exemples : [/concepts/model-providers](/concepts/model-providers).

## Fonctionnement de la sélection de modèle

OpenClaw sélectionne les modèles dans cet ordre :

1. **Modèle primaire** (`agents.defaults.model.primary` ou `agents.defaults.model`).
2. **Fallbacks** dans `agents.defaults.model.fallbacks` (dans l'ordre).
3. **Basculement d'authentification du fournisseur** qui se produit à l'intérieur d'un fournisseur avant de passer au
   modèle suivant.

Éléments connexes :

- `agents.defaults.models` est la liste d'autorisation/catalogue des modèles qu'OpenClaw peut utiliser (plus les alias).
- `agents.defaults.imageModel` est utilisé **uniquement quand** le modèle primaire ne peut pas accepter d'images.
- Les valeurs par défaut par agent peuvent remplacer `agents.defaults.model` via `agents.list[].model` plus les liaisons (voir [/concepts/multi-agent](/concepts/multi-agent)).

## Politique rapide des modèles

- Définissez votre modèle primaire sur le modèle de dernière génération le plus puissant disponible pour vous.
- Utilisez les fallbacks pour les tâches sensibles au coût/latence et les discussions de faible enjeu.
- Pour les agents activés par des outils ou les entrées non fiables, évitez les niveaux de modèle plus anciens/plus faibles.

## Assistant de configuration (recommandé)

Si vous ne voulez pas éditer manuellement la configuration, exécutez l'assistant d'intégration :

```bash
openclaw onboard
```

Il peut configurer le modèle + l'authentification pour les fournisseurs courants, y compris **OpenAI Code (abonnement Codex)**
(OAuth) et **Anthropic** (clé API ou `claude setup-token`).

## Clés de configuration (aperçu)

- `agents.defaults.model.primary` et `agents.defaults.model.fallbacks`
- `agents.defaults.imageModel.primary` et `agents.defaults.imageModel.fallbacks`
- `agents.defaults.models` (liste d'autorisation + alias + paramètres du fournisseur)
- `models.providers` (fournisseurs personnalisés écrits dans `models.json`)

Les références de modèle sont normalisées en minuscules. Les alias de fournisseur comme `z.ai/*` se normalisent
en `zai/*`.

Les exemples de configuration du fournisseur (y compris OpenCode) se trouvent dans
[/gateway/configuration](/gateway/configuration#opencode).

## « Le modèle n'est pas autorisé » (et pourquoi les réponses s'arrêtent)

Si `agents.defaults.models` est défini, il devient la **liste d'autorisation** pour `/model` et pour
les remplacements de session. Quand un utilisateur sélectionne un modèle qui n'est pas dans cette liste d'autorisation,
OpenClaw retourne :

```
Model "provider/model" is not allowed. Use /model to list available models.
```

Cela se produit **avant** qu'une réponse normale soit générée, donc le message peut sembler
comme s'il « n'avait pas répondu ». La solution est soit :

- Ajouter le modèle à `agents.defaults.models`, ou
- Effacer la liste d'autorisation (supprimer `agents.defaults.models`), ou
- Choisir un modèle dans `/model list`.

Exemple de configuration de liste d'autorisation :

```json5
{
  agent: {
    model: { primary: "anthropic/claude-sonnet-4-5" },
    models: {
      "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
      "anthropic/claude-opus-4-6": { alias: "Opus" },
    },
  },
}
```

## Changer de modèle dans le chat (`/model`)

Vous pouvez changer de modèle pour la session actuelle sans redémarrer :

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model status
```

Remarques :

- `/model` (et `/model list`) est un sélecteur compact et numéroté (famille de modèles + fournisseurs disponibles).
- Sur Discord, `/model` et `/models` ouvrent un sélecteur interactif avec des listes déroulantes de fournisseur et de modèle plus une étape Soumettre.
- `/model <#>` sélectionne à partir de ce sélecteur.
- `/model status` est la vue détaillée (candidats d'authentification et, si configuré, point de terminaison du fournisseur `baseUrl` + mode `api`).
- Les références de modèle sont analysées en divisant sur le **premier** `/`. Utilisez `provider/model` lors de la saisie de `/model <ref>`.
- Si l'ID du modèle lui-même contient `/` (style OpenRouter), vous devez inclure le préfixe du fournisseur (exemple : `/model openrouter/moonshotai/kimi-k2`).
- Si vous omettez le fournisseur, OpenClaw traite l'entrée comme un alias ou un modèle pour le **fournisseur par défaut** (ne fonctionne que s'il n'y a pas de `/` dans l'ID du modèle).

Comportement/configuration complète de la commande : [Commandes slash](/tools/slash-commands).

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

- `--all` : catalogue complet
- `--local` : fournisseurs locaux uniquement
- `--provider <name>` : filtrer par fournisseur
- `--plain` : un modèle par ligne
- `--json` : sortie lisible par machine

### `models status`

Affiche le modèle primaire résolu, les fallbacks, le modèle d'image et un aperçu d'authentification
des fournisseurs configurés. Il affiche également l'état d'expiration OAuth pour les profils trouvés
dans le magasin d'authentification (avertit dans les 24 heures par défaut). `--plain` imprime uniquement le
modèle primaire résolu.
L'état OAuth est toujours affiché (et inclus dans la sortie `--json`). Si un fournisseur configuré
n'a pas d'identifiants, `models status` imprime une section **Authentification manquante**.
JSON inclut `auth.oauth` (fenêtre d'avertissement + profils) et `auth.providers`
(authentification effective par fournisseur).
Utilisez `--check` pour l'automatisation (sortie `1` quand manquant/expiré, `2` quand expire).

Le choix d'authentification dépend du fournisseur/compte. Pour les hôtes de passerelle toujours actifs, les clés API sont généralement les plus prévisibles ; les flux de jetons d'abonnement sont également pris en charge.

Exemple (jeton de configuration Anthropic) :

```bash
claude setup-token
openclaw models status
```

## Analyse (modèles gratuits OpenRouter)

`openclaw models scan` inspecte le **catalogue de modèles gratuits** d'OpenRouter et peut
éventuellement sonder les modèles pour le support des outils et des images.

Drapeaux clés :

- `--no-probe` : ignorer les sondes en direct (métadonnées uniquement)
- `--min-params <b>` : taille minimale des paramètres (milliards)
- `--max-age-days <days>` : ignorer les modèles plus anciens
- `--provider <name>` : filtre de préfixe de fournisseur
- `--max-candidates <n>` : taille de la liste de fallback
- `--set-default` : définir `agents.defaults.model.primary` sur la première sélection
- `--set-image` : définir `agents.defaults.imageModel.primary` sur la première sélection d'image

Le sondage nécessite une clé API OpenRouter (à partir des profils d'authentification ou
`OPENROUTER_API_KEY`). Sans clé, utilisez `--no-probe` pour lister uniquement les candidats.

Les résultats de l'analyse sont classés par :

1. Support des images
2. Latence des outils
3. Taille du contexte
4. Nombre de paramètres

Entrée

- Liste OpenRouter `/models` (filtre `:free`)
- Nécessite une clé API OpenRouter à partir des profils d'authentification ou `OPENROUTER_API_KEY` (voir [/environment](/help/environment))
- Filtres optionnels : `--max-age-days`, `--min-params`, `--provider`, `--max-candidates`
- Contrôles de sondage : `--timeout`, `--concurrency`

Lorsqu'il est exécuté dans un TTY, vous pouvez sélectionner les fallbacks de manière interactive. En mode non interactif,
passez `--yes` pour accepter les valeurs par défaut.

## Registre des modèles (`models.json`)

Les fournisseurs personnalisés dans `models.providers` sont écrits dans `models.json` sous le
répertoire de l'agent (par défaut `~/.openclaw/agents/<agentId>/agent/models.json`). Ce fichier
est fusionné par défaut sauf si `models.mode` est défini sur `replace`.

Précédence du mode de fusion pour les ID de fournisseur correspondants :

- Non-vide `baseUrl` déjà présent dans l'agent `models.json` gagne.
- Non-vide `apiKey` dans l'agent `models.json` gagne uniquement quand ce fournisseur n'est pas géré par SecretRef dans le contexte de configuration/profil d'authentification actuel.
- Les valeurs `apiKey` du fournisseur gérées par SecretRef sont actualisées à partir des marqueurs source (`ENV_VAR_NAME` pour les références env, `secretref-managed` pour les références fichier/exec) au lieu de persister les secrets résolus.
- Les valeurs d'en-tête du fournisseur gérées par SecretRef sont actualisées à partir des marqueurs source (`secretref-env:ENV_VAR_NAME` pour les références env, `secretref-managed` pour les références fichier/exec).
- `apiKey`/`baseUrl` vides ou manquants de l'agent reviennent à `models.providers` de configuration.
- Les autres champs du fournisseur sont actualisés à partir de la configuration et des données du catalogue normalisé.

La persistance des marqueurs est source-autoritaire : OpenClaw écrit les marqueurs à partir de l'instantané de configuration source actif (pré-résolution), pas à partir des valeurs de secret d'exécution résolues.
Cela s'applique chaque fois qu'OpenClaw régénère `models.json`, y compris les chemins pilotés par commande comme `openclaw agent`.
