---
summary: "Configurez le plugin de mémoire LanceDB fourni, y compris les embeddings locaux compatibles avec Ollama"
read_when:
  - You are configuring the bundled memory-lancedb plugin
  - You want LanceDB-backed long-term memory with auto-recall or auto-capture
  - You are using local OpenAI-compatible embeddings such as Ollama
title: "Memory LanceDB"
sidebarTitle: "Memory LanceDB"
---

`memory-lancedb` est un plugin de mémoire fourni qui stocke la mémoire à long terme dans
LanceDB et utilise des embeddings pour la récupération. Il peut automatiquement récupérer les souvenirs pertinents
avant un tour de modèle et capturer les faits importants après une réponse.

Utilisez-le lorsque vous voulez une base de données vectorielle locale pour la mémoire, avez besoin d'un
point de terminaison d'embedding compatible avec OpenAI, ou voulez conserver une base de données de mémoire en dehors
du magasin de mémoire intégré par défaut.

<Note>
`memory-lancedb` est un plugin de mémoire actif. Activez-le en sélectionnant l'emplacement de mémoire avec `plugins.slots.memory = "memory-lancedb"`. Les plugins complémentaires tels que
`memory-wiki` peuvent s'exécuter à côté, mais un seul plugin possède l'emplacement de mémoire actif.
</Note>

## Démarrage rapide

```json5
{
  plugins: {
    slots: {
      memory: "memory-lancedb",
    },
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          embedding: {
            apiKey: "${OPENAI_API_KEY}",
            model: "text-embedding-3-small",
          },
          autoRecall: true,
          autoCapture: false,
        },
      },
    },
  },
}
```

Redémarrez la Gateway après avoir modifié la configuration du plugin :

```bash
openclaw gateway restart
```

Ensuite, vérifiez que le plugin est chargé :

```bash
openclaw plugins list
```

## Embeddings Ollama

`memory-lancedb` appelle les embeddings via une API d'embeddings compatible avec OpenAI.
Pour les embeddings Ollama, utilisez le point de terminaison de compatibilité Ollama `/v1` ici. Ceci
est uniquement pour les embeddings ; le fournisseur de chat/modèle Ollama utilise l'URL API Ollama native
documentée dans [Ollama](/fr/providers/ollama).

```json5
{
  plugins: {
    slots: {
      memory: "memory-lancedb",
    },
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          embedding: {
            apiKey: "ollama",
            baseUrl: "http://127.0.0.1:11434/v1",
            model: "mxbai-embed-large",
            dimensions: 1024,
          },
          recallMaxChars: 400,
          autoRecall: true,
          autoCapture: false,
        },
      },
    },
  },
}
```

Définissez `dimensions` pour les modèles d'embedding non standard. OpenClaw connaît les
dimensions pour `text-embedding-3-small` et `text-embedding-3-large` ; les modèles personnalisés
ont besoin de la valeur dans la configuration pour que LanceDB puisse créer la colonne vectorielle.

Pour les petits modèles d'embedding locaux, réduisez `recallMaxChars` si vous voyez des erreurs de longueur de contexte
du serveur local.

## Fournisseurs compatibles avec OpenAI

Certains fournisseurs d'embedding compatibles avec OpenAI rejettent le paramètre `encoding_format`,
tandis que d'autres l'ignorent et retournent toujours des vecteurs `number[]`.
`memory-lancedb` omet donc `encoding_format` sur les demandes d'embedding et
accepte soit des réponses de tableau flottant, soit des réponses float32 codées en base64.

Définissez `embedding.dimensions` pour les fournisseurs dont les dimensions du modèle ne sont pas intégrées.
Par exemple, ZhiPu `embedding-3` utilise `2048` dimensions :

```json5
{
  plugins: {
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          embedding: {
            apiKey: "${ZHIPU_API_KEY}",
            baseUrl: "https://open.bigmodel.cn/api/paas/v4",
            model: "embedding-3",
            dimensions: 2048,
          },
        },
      },
    },
  },
}
```

## Limites de récupération et de capture

`memory-lancedb` a deux limites de texte distinctes :

| Paramètre         | Par défaut | Plage     | S'applique à                                          |
| ----------------- | ---------- | --------- | ----------------------------------------------------- |
| `recallMaxChars`  | `1000`     | 100-10000 | texte envoyé à l'API d'embedding pour la récupération |
| `captureMaxChars` | `500`      | 100-10000 | longueur du message assistant éligible pour la capture |

`recallMaxChars` contrôle la récupération automatique, l'outil `memory_recall`, le
chemin de requête `memory_forget`, et `openclaw ltm search`. La récupération automatique préfère le
dernier message utilisateur du tour et revient au prompt complet uniquement lorsqu'aucun
message utilisateur n'est disponible. Cela garde les métadonnées de canal et les grands blocs de prompt
en dehors de la demande d'embedding.

`captureMaxChars` contrôle si une réponse est assez courte pour être considérée
pour la capture automatique. Il ne limite pas les embeddings de requête de récupération.

## Commandes

Lorsque `memory-lancedb` est le plugin de mémoire actif, il enregistre l'espace de noms CLI `ltm` :

```bash
openclaw ltm list
openclaw ltm search "project preferences"
openclaw ltm stats
```

Les agents obtiennent également les outils de mémoire LanceDB du plugin de mémoire actif :

- `memory_recall` pour la récupération soutenue par LanceDB
- `memory_store` pour sauvegarder les faits importants, les préférences, les décisions et les entités
- `memory_forget` pour supprimer les souvenirs correspondants

## Stockage

Par défaut, les données LanceDB se trouvent sous `~/.openclaw/memory/lancedb`. Remplacez le
chemin avec `dbPath` :

```json5
{
  plugins: {
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          dbPath: "~/.openclaw/memory/lancedb",
          embedding: {
            apiKey: "${OPENAI_API_KEY}",
            model: "text-embedding-3-small",
          },
        },
      },
    },
  },
}
```

`storageOptions` accepte les paires clé/valeur de chaîne pour les backends de stockage LanceDB et
supporte l'expansion `${ENV_VAR}` :

```json5
{
  plugins: {
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          dbPath: "s3://memory-bucket/openclaw",
          storageOptions: {
            access_key: "${AWS_ACCESS_KEY_ID}",
            secret_key: "${AWS_SECRET_ACCESS_KEY}",
            endpoint: "${AWS_ENDPOINT_URL}",
          },
          embedding: {
            apiKey: "${OPENAI_API_KEY}",
            model: "text-embedding-3-small",
          },
        },
      },
    },
  },
}
```

## Dépendances d'exécution

`memory-lancedb` dépend du package natif `@lancedb/lancedb`. Les installations OpenClaw empaquetées
essaient d'abord la dépendance d'exécution fournie et peuvent réparer la dépendance d'exécution du plugin
sous l'état OpenClaw lorsque l'import fourni n'est pas disponible.

Si une installation plus ancienne enregistre une erreur `dist/package.json` manquant ou `@lancedb/lancedb`
manquant lors du chargement du plugin, mettez à jour OpenClaw et redémarrez la Gateway.

Si le plugin enregistre que LanceDB n'est pas disponible sur `darwin-x64`, utilisez le backend de mémoire par défaut
sur cette machine, déplacez la Gateway vers une plateforme supportée, ou
désactivez `memory-lancedb`.

## Dépannage

### La longueur d'entrée dépasse la longueur du contexte

Cela signifie généralement que le modèle d'embedding a rejeté la requête de récupération :

```text
memory-lancedb: recall failed: Error: 400 the input length exceeds the context length
```

Définissez un `recallMaxChars` plus bas, puis redémarrez la Gateway :

```json5
{
  plugins: {
    entries: {
      "memory-lancedb": {
        config: {
          recallMaxChars: 400,
        },
      },
    },
  },
}
```

Pour Ollama, vérifiez également que le serveur d'embedding est accessible depuis l'hôte Gateway :

```bash
curl http://127.0.0.1:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"mxbai-embed-large","input":"hello"}'
```

### Modèle d'embedding non supporté

Sans `dimensions`, seules les dimensions d'embedding OpenAI intégrées sont connues.
Pour les modèles d'embedding locaux ou personnalisés, définissez `embedding.dimensions` à la taille vectorielle
rapportée par ce modèle.

### Le plugin se charge mais aucun souvenir n'apparaît

Vérifiez que `plugins.slots.memory` pointe vers `memory-lancedb`, puis exécutez :

```bash
openclaw ltm stats
openclaw ltm search "recent preference"
```

Si `autoCapture` est désactivé, le plugin récupérera les souvenirs existants mais ne
stockera pas automatiquement les nouveaux. Utilisez l'outil `memory_store` ou activez
`autoCapture` si vous voulez la capture automatique.

## Connexes

- [Aperçu de la mémoire](/fr/concepts/memory)
- [Mémoire active](/fr/concepts/active-memory)
- [Recherche de mémoire](/fr/concepts/memory-search)
- [Memory Wiki](/fr/plugins/memory-wiki)
- [Ollama](/fr/providers/ollama)
