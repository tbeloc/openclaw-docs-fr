---
summary: "Utilisez directement Ollama Cloud avec OpenClaw"
read_when:
  - You want to use hosted Ollama models without a local Ollama server
  - You need the ollama-cloud provider id, key, or endpoint
title: "Ollama Cloud"
---

Ollama Cloud est l'API de modèle hébergée d'Ollama. Elle permet à OpenClaw d'appeler directement les modèles hébergés par Ollama, sans installer un serveur Ollama local ni connecter une application Ollama locale au mode cloud. Utilisez l'identifiant de fournisseur `ollama-cloud` et les références de modèle comme `ollama-cloud/kimi-k2.6`.

Cette page concerne le routage cloud uniquement. Le fournisseur utilise le style natif `/api/chat` d'Ollama, et non la route compatible OpenAI `/v1`. OpenClaw l'enregistre comme un identifiant de fournisseur distinct afin que les identifiants cloud uniquement, la découverte de catalogue en direct et la sélection de modèle ne se mélangent pas avec un hôte `ollama` local.

Utilisez cette page lorsque vous souhaitez un routage cloud uniquement. Pour Ollama local, le routage hybride cloud-plus-local, les embeddings et les détails d'hôte personnalisés, consultez [Ollama](/fr/providers/ollama).

## Configuration

Créez une clé API Ollama Cloud sur [ollama.com/settings/keys](https://ollama.com/settings/keys), puis exécutez :

```bash
openclaw onboard --auth-choice ollama-cloud
```

Ou définissez :

```bash
export OLLAMA_API_KEY="<your-ollama-cloud-api-key>" # pragma: allowlist secret
```

## Valeurs par défaut

- Fournisseur : `ollama-cloud`
- URL de base : `https://ollama.com`
- Variable d'environnement : `OLLAMA_API_KEY`
- Style API : Ollama natif `/api/chat`
- Modèle d'exemple : `ollama-cloud/kimi-k2.6`

## Quand choisir Ollama Cloud

- Vous souhaitez des modèles Ollama hébergés sans exécuter `ollama serve` localement.
- Vous souhaitez la même forme d'API de chat Ollama natif qu'OpenClaw utilise pour Ollama local, mais pointée vers `https://ollama.com`.
- Vous souhaitez un chemin cloud simple pour les modèles qui sont déjà dans le catalogue hébergé d'Ollama.
- Vous n'avez pas besoin de pulls de modèles locaux, de contrôle GPU local ou d'inférence LAN uniquement.

Utilisez [Ollama](/fr/providers/ollama) à la place lorsque vous souhaitez un routage local uniquement ou cloud-plus-local via un hôte Ollama connecté. Utilisez un fournisseur compatible OpenAI à la place lorsque vous avez besoin de la sémantique `/v1/chat/completions` ou de fonctionnalités spécifiques au fournisseur de style OpenAI.

## Modèles

OpenClaw découvre les modèles Ollama Cloud à partir du catalogue hébergé en direct. Les identifiants hébergés couramment disponibles incluent :

- `ollama-cloud/gpt-oss:20b`
- `ollama-cloud/kimi-k2.6`
- `ollama-cloud/deepseek-v4-flash`
- `ollama-cloud/minimax-m2.7`
- `ollama-cloud/glm-5`

Utilisez un identifiant de modèle de votre catalogue hébergé actuel :

```bash
openclaw models list --provider ollama-cloud
openclaw models set ollama-cloud/kimi-k2.6
```

Les identifiants de modèle sont des identifiants de catalogue cloud, pas des noms de pulls locaux. Si un nom de modèle fonctionne sur un hôte Ollama local mais est absent du catalogue hébergé, utilisez le fournisseur `ollama` avec cet hôte local à la place.

## Test en direct

Pour les tests de fumée de clé API Ollama Cloud, pointez le test en direct d'Ollama vers le point de terminaison hébergé et choisissez un modèle de votre catalogue actuel :

```bash
export OLLAMA_API_KEY="<your-ollama-cloud-api-key>" # pragma: allowlist secret

OPENCLAW_LIVE_TEST=1 \
OPENCLAW_LIVE_OLLAMA=1 \
OPENCLAW_LIVE_OLLAMA_BASE_URL=https://ollama.com \
OPENCLAW_LIVE_OLLAMA_MODEL=kimi-k2.6 \
OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=1 \
pnpm test:live -- extensions/ollama/ollama.live.test.ts
```

L'exécution de fumée cloud teste le texte, le flux natif et la recherche web. Elle ignore les embeddings par défaut pour `https://ollama.com` car les clés API Ollama Cloud peuvent ne pas autoriser `/api/embed`.

## Dépannage

- Erreurs `Set OLLAMA_API_KEY` : fournissez une véritable clé API cloud. Le marqueur `ollama-local` local est uniquement pour les hôtes Ollama locaux ou privés.
- Erreurs de modèle inconnu : exécutez `openclaw models list --provider ollama-cloud` et copiez exactement l'identifiant de modèle hébergé.
- Problèmes d'appel d'outil ou JSON brut sur les hôtes Ollama personnalisés : vérifiez que vous n'utilisez pas accidentellement une URL `/v1` compatible OpenAI. Les routes Ollama doivent utiliser l'URL de base native sans suffixe `/v1`.

## Connexes

- [Ollama](/fr/providers/ollama)
- [Fournisseurs de modèles](/fr/concepts/model-providers)
- [Tous les fournisseurs](/fr/providers/index)
