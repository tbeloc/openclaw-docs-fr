---
title: "Moteur de mémoire intégré"
summary: "Le backend de mémoire par défaut basé sur SQLite avec recherche par mots-clés, vecteurs et hybride"
read_when:
  - You want to understand the default memory backend
  - You want to configure embedding providers or hybrid search
---

# Moteur de mémoire intégré

Le moteur intégré est le backend de mémoire par défaut. Il stocke votre index de mémoire dans une base de données SQLite par agent et ne nécessite aucune dépendance supplémentaire pour commencer.

## Ce qu'il fournit

- **Recherche par mots-clés** via l'indexation full-text FTS5 (notation BM25).
- **Recherche vectorielle** via des embeddings de n'importe quel fournisseur supporté.
- **Recherche hybride** qui combine les deux pour les meilleurs résultats.
- **Support CJK** via tokenisation trigramme pour le chinois, le japonais et le coréen.
- **Accélération sqlite-vec** pour les requêtes vectorielles en base de données (optionnel).

## Premiers pas

Si vous avez une clé API pour OpenAI, Gemini, Voyage ou Mistral, le moteur intégré la détecte automatiquement et active la recherche vectorielle. Aucune configuration nécessaire.

Pour définir un fournisseur explicitement :

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai",
      },
    },
  },
}
```

Sans fournisseur d'embedding, seule la recherche par mots-clés est disponible.

## Fournisseurs d'embedding supportés

| Fournisseur | ID        | Détection automatique | Notes                               |
| ----------- | --------- | --------------------- | ----------------------------------- |
| OpenAI      | `openai`  | Oui                   | Par défaut : `text-embedding-3-small`   |
| Gemini      | `gemini`  | Oui                   | Supporte multimodal (image + audio) |
| Voyage      | `voyage`  | Oui                   |                                     |
| Mistral     | `mistral` | Oui                   |                                     |
| Ollama      | `ollama`  | Non                   | Local, à définir explicitement               |
| Local       | `local`   | Oui (premier)         | Modèle GGUF, ~0,6 GB de téléchargement        |

La détection automatique choisit le premier fournisseur dont la clé API peut être résolue, dans l'ordre indiqué. Définissez `memorySearch.provider` pour remplacer.

## Comment fonctionne l'indexation

OpenClaw indexe `MEMORY.md` et `memory/*.md` en chunks (~400 tokens avec chevauchement de 80 tokens) et les stocke dans une base de données SQLite par agent.

- **Emplacement de l'index :** `~/.openclaw/memory/<agentId>.sqlite`
- **Surveillance des fichiers :** les modifications des fichiers de mémoire déclenchent une réindexation débounce (1,5s).
- **Réindexation automatique :** lorsque le fournisseur d'embedding, le modèle ou la configuration du chunking change, l'index entier est reconstruit automatiquement.
- **Réindexation à la demande :** `openclaw memory index --force`

<Info>
Vous pouvez également indexer des fichiers Markdown en dehors de l'espace de travail avec
`memorySearch.extraPaths`. Voir la
[référence de configuration](/fr/reference/memory-config#additional-memory-paths).
</Info>

## Quand l'utiliser

Le moteur intégré est le bon choix pour la plupart des utilisateurs :

- Fonctionne immédiatement sans dépendances supplémentaires.
- Gère bien la recherche par mots-clés et vectorielle.
- Supporte tous les fournisseurs d'embedding.
- La recherche hybride combine le meilleur des deux approches de récupération.

Envisagez de passer à [QMD](/fr/concepts/memory-qmd) si vous avez besoin de reranking, d'expansion de requête ou si vous voulez indexer des répertoires en dehors de l'espace de travail.

Envisagez [Honcho](/fr/concepts/memory-honcho) si vous voulez une mémoire multi-sessions avec modélisation automatique des utilisateurs.

## Dépannage

**Recherche de mémoire désactivée ?** Vérifiez `openclaw memory status`. Si aucun fournisseur n'est détecté, définissez-en un explicitement ou ajoutez une clé API.

**Résultats obsolètes ?** Exécutez `openclaw memory index --force` pour reconstruire. Le watcher peut manquer les modifications dans de rares cas limites.

**sqlite-vec ne se charge pas ?** OpenClaw revient automatiquement à la similarité cosinus en processus. Vérifiez les logs pour l'erreur de chargement spécifique.

## Configuration

Pour la configuration du fournisseur d'embedding, le réglage de la recherche hybride (poids, MMR, décroissance temporelle), l'indexation par batch, la mémoire multimodale, sqlite-vec, les chemins supplémentaires et tous les autres paramètres de configuration, voir la
[référence de configuration de la mémoire](/fr/reference/memory-config).
