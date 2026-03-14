---
summary: "Référence CLI pour `openclaw onboard` (assistant d'intégration interactif)"
read_when:
  - You want guided setup for gateway, workspace, auth, channels, and skills
title: "onboard"
---

# `openclaw onboard`

Assistant d'intégration interactif (configuration de Gateway locale ou distante).

## Guides connexes

- Hub d'intégration CLI : [Onboarding Wizard (CLI)](/start/wizard)
- Aperçu de l'intégration : [Onboarding Overview](/start/onboarding-overview)
- Référence d'intégration CLI : [CLI Onboarding Reference](/start/wizard-cli-reference)
- Automatisation CLI : [CLI Automation](/start/wizard-cli-automation)
- Intégration macOS : [Onboarding (macOS App)](/start/onboarding)

## Exemples

```bash
openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --mode remote --remote-url wss://gateway-host:18789
```

Pour les cibles de réseau privé en texte brut `ws://` (réseaux de confiance uniquement), définissez
`OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` dans l'environnement du processus d'intégration.

Fournisseur personnalisé non interactif :

```bash
openclaw onboard --non-interactive \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --secret-input-mode plaintext \
  --custom-compatibility openai
```

`--custom-api-key` est optionnel en mode non interactif. S'il est omis, l'intégration vérifie `CUSTOM_API_KEY`.

Ollama non interactif :

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://ollama-host:11434" \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk
```

`--custom-base-url` par défaut à `http://127.0.0.1:11434`. `--custom-model-id` est optionnel ; s'il est omis, l'intégration utilise les valeurs par défaut suggérées par Ollama. Les ID de modèles cloud tels que `kimi-k2.5:cloud` fonctionnent également ici.

Stocker les clés de fournisseur en tant que références au lieu de texte brut :

```bash
openclaw onboard --non-interactive \
  --auth-choice openai-api-key \
  --secret-input-mode ref \
  --accept-risk
```

Avec `--secret-input-mode ref`, l'intégration écrit des références soutenues par env au lieu de valeurs de clés en texte brut.
Pour les fournisseurs soutenus par un profil d'authentification, cela écrit des entrées `keyRef` ; pour les fournisseurs personnalisés, cela écrit `models.providers.<id>.apiKey` en tant que référence env (par exemple `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`).

Contrat du mode `ref` non interactif :

- Définissez la variable env du fournisseur dans l'environnement du processus d'intégration (par exemple `OPENAI_API_KEY`).
- Ne passez pas les drapeaux de clé en ligne (par exemple `--openai-api-key`) sauf si cette variable env est également définie.
- Si un drapeau de clé en ligne est passé sans la variable env requise, l'intégration échoue rapidement avec des conseils.

Options de jeton Gateway en mode non interactif :

- `--gateway-auth token --gateway-token <token>` stocke un jeton en texte brut.
- `--gateway-auth token --gateway-token-ref-env <name>` stocke `gateway.auth.token` en tant que SecretRef env.
- `--gateway-token` et `--gateway-token-ref-env` s'excluent mutuellement.
- `--gateway-token-ref-env` nécessite une variable env non vide dans l'environnement du processus d'intégration.
- Avec `--install-daemon`, lorsque l'authentification par jeton nécessite un jeton, les jetons de gateway gérés par SecretRef sont validés mais non persistés en tant que texte brut résolu dans les métadonnées d'environnement du service superviseur.
- Avec `--install-daemon`, si le mode jeton nécessite un jeton et que la SecretRef de jeton configurée n'est pas résolue, l'intégration échoue fermée avec des conseils de correction.
- Avec `--install-daemon`, si à la fois `gateway.auth.token` et `gateway.auth.password` sont configurés et que `gateway.auth.mode` n'est pas défini, l'intégration bloque l'installation jusqu'à ce que le mode soit défini explicitement.

Exemple :

```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN \
  --accept-risk
```

Santé de la gateway locale non interactive :

- À moins que vous ne passiez `--skip-health`, l'intégration attend une gateway locale accessible avant de se terminer avec succès.
- `--install-daemon` démarre d'abord le chemin d'installation de la gateway gérée. Sans cela, vous devez déjà avoir une gateway locale en cours d'exécution, par exemple `openclaw gateway run`.
- Si vous ne voulez que des écritures de config/workspace/bootstrap en automatisation, utilisez `--skip-health`.
- Sur Windows natif, `--install-daemon` essaie d'abord les Tâches planifiées et revient à un élément de dossier de démarrage par utilisateur si la création de tâche est refusée.

Comportement d'intégration interactif avec mode référence :

- Choisissez **Use secret reference** lorsque vous y êtes invité.
- Puis choisissez l'une des options suivantes :
  - Variable d'environnement
  - Fournisseur de secret configuré (`file` ou `exec`)
- L'intégration effectue une validation de préflight rapide avant d'enregistrer la référence.
  - Si la validation échoue, l'intégration affiche l'erreur et vous permet de réessayer.

Choix de points de terminaison Z.AI non interactifs :

Remarque : `--auth-choice zai-api-key` détecte maintenant automatiquement le meilleur point de terminaison Z.AI pour votre clé (préfère l'API générale avec `zai/glm-5`).
Si vous voulez spécifiquement les points de terminaison du Plan de codage GLM, choisissez `zai-coding-global` ou `zai-coding-cn`.

```bash
# Sélection de point de terminaison sans invite
openclaw onboard --non-interactive \
  --auth-choice zai-coding-global \
  --zai-api-key "$ZAI_API_KEY"

# Autres choix de points de terminaison Z.AI :
# --auth-choice zai-coding-cn
# --auth-choice zai-global
# --auth-choice zai-cn
```

Exemple Mistral non interactif :

```bash
openclaw onboard --non-interactive \
  --auth-choice mistral-api-key \
  --mistral-api-key "$MISTRAL_API_KEY"
```

Notes sur le flux :

- `quickstart` : invites minimales, génère automatiquement un jeton de gateway.
- `manual` : invites complètes pour port/bind/auth (alias de `advanced`).
- Comportement de portée DM d'intégration locale : [CLI Onboarding Reference](/start/wizard-cli-reference#outputs-and-internals).
- Premier chat le plus rapide : `openclaw dashboard` (Control UI, pas de configuration de canal).
- Fournisseur personnalisé : connectez n'importe quel point de terminaison compatible OpenAI ou Anthropic,
  y compris les fournisseurs hébergés non listés. Utilisez Unknown pour la détection automatique.

## Commandes de suivi courantes

```bash
openclaw configure
openclaw agents add <name>
```

<Note>
`--json` n'implique pas le mode non interactif. Utilisez `--non-interactive` pour les scripts.
</Note>
