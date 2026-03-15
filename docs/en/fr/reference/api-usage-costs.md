---
summary: "Auditez ce qui peut dépenser de l'argent, quelles clés sont utilisées et comment afficher l'utilisation"
read_when:
  - You want to understand which features may call paid APIs
  - You need to audit keys, costs, and usage visibility
  - You're explaining /status or /usage cost reporting
title: "Utilisation et coûts des API"
---

# Utilisation et coûts des API

Ce document énumère les **fonctionnalités qui peuvent invoquer des clés API** et où leurs coûts s'affichent. Il se concentre sur les fonctionnalités OpenClaw qui peuvent générer une utilisation de fournisseur ou des appels API payants.

## Où les coûts s'affichent (chat + CLI)

**Snapshot de coût par session**

- `/status` affiche le modèle de session actuel, l'utilisation du contexte et les tokens de la dernière réponse.
- Si le modèle utilise l'**authentification par clé API**, `/status` affiche également le **coût estimé** pour la dernière réponse.

**Pied de page de coût par message**

- `/usage full` ajoute un pied de page d'utilisation à chaque réponse, incluant le **coût estimé** (clé API uniquement).
- `/usage tokens` affiche uniquement les tokens ; les flux OAuth masquent le coût en dollars.

**Fenêtres d'utilisation CLI (quotas de fournisseur)**

- `openclaw status --usage` et `openclaw channels list` affichent les **fenêtres d'utilisation** du fournisseur
  (snapshots de quota, pas des coûts par message).

Consultez [Utilisation et coûts des tokens](/fr/reference/token-use) pour plus de détails et d'exemples.

## Comment les clés sont découvertes

OpenClaw peut récupérer les identifiants à partir de :

- **Profils d'authentification** (par agent, stockés dans `auth-profiles.json`).
- **Variables d'environnement** (par ex. `OPENAI_API_KEY`, `BRAVE_API_KEY`, `FIRECRAWL_API_KEY`).
- **Configuration** (`models.providers.*.apiKey`, `tools.web.search.*`, `tools.web.fetch.firecrawl.*`,
  `memorySearch.*`, `talk.apiKey`).
- **Skills** (`skills.entries.<name>.apiKey`) qui peuvent exporter des clés vers l'environnement du processus skill.

## Fonctionnalités qui peuvent dépenser des clés

### 1) Réponses du modèle principal (chat + outils)

Chaque réponse ou appel d'outil utilise le **fournisseur de modèle actuel** (OpenAI, Anthropic, etc). C'est la
source principale d'utilisation et de coûts.

Consultez [Modèles](/fr/providers/models) pour la configuration des tarifs et [Utilisation et coûts des tokens](/fr/reference/token-use) pour l'affichage.

### 2) Compréhension des médias (audio/image/vidéo)

Les médias entrants peuvent être résumés/transcrits avant l'exécution de la réponse. Cela utilise les API du modèle/fournisseur.

- Audio : OpenAI / Groq / Deepgram (maintenant **activé automatiquement** quand les clés existent).
- Image : OpenAI / Anthropic / Google.
- Vidéo : Google.

Consultez [Compréhension des médias](/fr/nodes/media-understanding).

### 3) Embeddings de mémoire + recherche sémantique

La recherche sémantique en mémoire utilise les **API d'embedding** quand configurées pour des fournisseurs distants :

- `memorySearch.provider = "openai"` → Embeddings OpenAI
- `memorySearch.provider = "gemini"` → Embeddings Gemini
- `memorySearch.provider = "voyage"` → Embeddings Voyage
- `memorySearch.provider = "mistral"` → Embeddings Mistral
- `memorySearch.provider = "ollama"` → Embeddings Ollama (local/auto-hébergé ; généralement pas de facturation API hébergée)
- Fallback optionnel vers un fournisseur distant si les embeddings locaux échouent

Vous pouvez le garder local avec `memorySearch.provider = "local"` (pas d'utilisation d'API).

Consultez [Mémoire](/fr/concepts/memory).

### 4) Outil de recherche web

`web_search` utilise des clés API et peut entraîner des frais d'utilisation selon votre fournisseur :

- **Brave Search API** : `BRAVE_API_KEY` ou `tools.web.search.apiKey`
- **Gemini (Google Search)** : `GEMINI_API_KEY` ou `tools.web.search.gemini.apiKey`
- **Grok (xAI)** : `XAI_API_KEY` ou `tools.web.search.grok.apiKey`
- **Kimi (Moonshot)** : `KIMI_API_KEY`, `MOONSHOT_API_KEY`, ou `tools.web.search.kimi.apiKey`
- **Perplexity Search API** : `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`, ou `tools.web.search.perplexity.apiKey`

**Crédit gratuit Brave Search :** Chaque plan Brave inclut \$5/mois en crédit
gratuit renouvelable. Le plan Search coûte \$5 pour 1 000 requêtes, donc le crédit couvre
1 000 requêtes/mois sans frais. Définissez votre limite d'utilisation dans le tableau de bord Brave
pour éviter les frais inattendus.

Consultez [Outils web](/fr/tools/web).

### 5) Outil de récupération web (Firecrawl)

`web_fetch` peut appeler **Firecrawl** quand une clé API est présente :

- `FIRECRAWL_API_KEY` ou `tools.web.fetch.firecrawl.apiKey`

Si Firecrawl n'est pas configuré, l'outil revient à une récupération directe + lisibilité (pas d'API payante).

Consultez [Outils web](/fr/tools/web).

### 6) Snapshots d'utilisation du fournisseur (statut/santé)

Certaines commandes de statut appellent les **points de terminaison d'utilisation du fournisseur** pour afficher les fenêtres de quota ou la santé de l'authentification.
Ce sont généralement des appels à faible volume mais qui frappent toujours les API du fournisseur :

- `openclaw status --usage`
- `openclaw models status --json`

Consultez [CLI Modèles](/fr/cli/models).

### 7) Résumé de sauvegarde de compaction

La sauvegarde de compaction peut résumer l'historique de session en utilisant le **modèle actuel**, ce qui
invoque les API du fournisseur quand elle s'exécute.

Consultez [Gestion de session + compaction](/fr/reference/session-management-compaction).

### 8) Scan / sonde de modèle

`openclaw models scan` peut sonder les modèles OpenRouter et utilise `OPENROUTER_API_KEY` quand
le sondage est activé.

Consultez [CLI Modèles](/fr/cli/models).

### 9) Talk (parole)

Le mode Talk peut invoquer **ElevenLabs** quand configuré :

- `ELEVENLABS_API_KEY` ou `talk.apiKey`

Consultez [Mode Talk](/fr/nodes/talk).

### 10) Skills (API tierces)

Les skills peuvent stocker `apiKey` dans `skills.entries.<name>.apiKey`. Si une skill utilise cette clé pour des
API externes, elle peut entraîner des coûts selon le fournisseur de la skill.

Consultez [Skills](/fr/tools/skills).
