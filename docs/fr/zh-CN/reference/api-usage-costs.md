---
read_when:
  - Vous voulez savoir quelles fonctionnalités peuvent appeler des API payantes
  - Vous devez examiner les clés, les frais et la visibilité de l'utilisation
  - Vous expliquez les rapports de frais de /status ou /usage
summary: Examinez quelles fonctionnalités génèrent des frais, quelles clés ont été utilisées et comment afficher l'utilisation
title: Utilisation et frais de l'API
x-i18n:
  generated_at: "2026-02-01T21:37:08Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 807d0d88801e919a8246517820644db1e6271d165fa376b2e637f05a9121d8b1
  source_path: reference/api-usage-costs.md
  workflow: 15
---

# Utilisation et frais de l'API

Ce document énumère les **fonctionnalités qui peuvent appeler des clés API** et où afficher leurs frais. Il met l'accent sur les fonctionnalités d'OpenClaw qui peuvent générer une utilisation du fournisseur ou des appels API payants.

## Où afficher les frais (Chat + CLI)

**Snapshot des frais par session**

- `/status` affiche le modèle de session actuel, l'utilisation du contexte et le nombre de tokens de la dernière réponse.
- Si le modèle utilise **l'authentification par clé API**, `/status` affiche également les **frais estimés** de la dernière réponse.

**Pied de page des frais par message**

- `/usage full` ajoute un pied de page d'utilisation après chaque réponse, incluant les **frais estimés** (clés API uniquement).
- `/usage tokens` affiche uniquement le nombre de tokens ; les flux OAuth masquent les frais en dollars.

**Fenêtre d'utilisation CLI (quota du fournisseur)**

- `openclaw status --usage` et `openclaw channels list` affichent la **fenêtre d'utilisation** du fournisseur (snapshot de quota, non les frais par message).

Pour plus de détails et d'exemples, consultez [Utilisation et frais des tokens](/reference/token-use).

## Comment les clés sont découvertes

OpenClaw peut obtenir des identifiants à partir des sources suivantes :

- **Profils d'authentification** (configurés par agent, stockés dans `auth-profiles.json`).
- **Variables d'environnement** (par exemple `OPENAI_API_KEY`, `BRAVE_API_KEY`, `FIRECRAWL_API_KEY`).
- **Fichiers de configuration** (`models.providers.*.apiKey`, `tools.web.search.*`, `tools.web.fetch.firecrawl.*`, `memorySearch.*`, `talk.apiKey`).
- **Skills** (`skills.entries.<name>.apiKey`), qui peuvent exporter des clés vers les variables d'environnement du processus Skills.

## Fonctionnalités susceptibles de consommer des clés

### 1) Réponses du modèle principal (Chat + Outils)

Chaque réponse ou appel d'outil utilise le **fournisseur de modèle actuel** (OpenAI, Anthropic, etc.). C'est la principale source d'utilisation et de frais.

Pour la configuration des tarifs, consultez [Modèles](/providers/models) ; pour l'affichage, consultez [Utilisation et frais des tokens](/reference/token-use).

### 2) Compréhension des médias (audio/image/vidéo)

Les médias entrants peuvent être résumés/transcrits avant la génération de réponse. Cela utilise l'API du modèle/fournisseur.

- Audio : OpenAI / Groq / Deepgram (**activé automatiquement** quand la clé existe).
- Image : OpenAI / Anthropic / Google.
- Vidéo : Google.

Consultez [Compréhension des médias](/nodes/media-understanding).

### 3) Intégration de mémoire + Recherche sémantique

La recherche de mémoire sémantique utilise l'**API d'intégration** quand elle est configurée pour un fournisseur distant :

- `memorySearch.provider = "openai"` → Intégration OpenAI
- `memorySearch.provider = "gemini"` → Intégration Gemini
- Basculement optionnel vers OpenAI en cas d'échec de l'intégration locale

Vous pouvez utiliser `memorySearch.provider = "local"` pour rester en local (pas d'utilisation d'API).

Consultez [Mémoire](/concepts/memory).

### 4) Outil de recherche web (Brave / Perplexity via OpenRouter)

`web_search` utilise une clé API et peut générer des frais d'utilisation :

- **API Brave Search** : `BRAVE_API_KEY` ou `tools.web.search.apiKey`
- **Perplexity** (via OpenRouter) : `PERPLEXITY_API_KEY` ou `OPENROUTER_API_KEY`

**Plan gratuit Brave (quota généreux) :**

- **2 000 requêtes par mois**
- **1 requête par seconde**
- **Carte de crédit requise** pour la vérification (pas de frais sauf mise à niveau)

Consultez [Outils web](/tools/web).

### 5) Outil de scraping web (Firecrawl)

`web_fetch` peut appeler **Firecrawl** quand une clé API existe :

- `FIRECRAWL_API_KEY` ou `tools.web.fetch.firecrawl.apiKey`

Si Firecrawl n'est pas configuré, l'outil bascule vers le scraping direct + extraction de lisibilité (pas d'API payante).

Consultez [Outils web](/tools/web).

### 6) Snapshot d'utilisation du fournisseur (vérification de statut/santé)

Certaines commandes de statut appellent les **points de terminaison d'utilisation du fournisseur** pour afficher les fenêtres de quota ou l'état de santé de l'authentification. Ce sont généralement des appels peu fréquents, mais ils accèdent toujours à l'API du fournisseur :

- `openclaw status --usage`
- `openclaw models status --json`

Consultez [CLI Modèles](/cli/models).

### 7) Résumé de protection par compression

La fonctionnalité de protection par compression peut utiliser le **modèle actuel** pour résumer l'historique de session, appelant l'API du fournisseur à l'exécution.

Consultez [Gestion de session + Compression](/reference/session-management-compaction).

### 8) Scan/Sondage de modèles

`openclaw models scan` peut sonder les modèles OpenRouter, utilisant `OPENROUTER_API_KEY` quand le sondage est activé.

Consultez [CLI Modèles](/cli/models).

### 9) Conversation vocale (Talk)

Le mode conversation vocale peut appeler **ElevenLabs** une fois configuré :

- `ELEVENLABS_API_KEY` ou `talk.apiKey`

Consultez [Mode conversation vocale](/nodes/talk).

### 10) Skills (API tierces)

Les Skills peuvent stocker une `apiKey` dans `skills.entries.<name>.apiKey`. Si un Skill utilise cette clé pour appeler une API externe, des frais sont générés selon le fournisseur du Skill.

Consultez [Skills](/tools/skills).
