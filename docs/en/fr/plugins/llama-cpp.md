---
summary: "Installez le fournisseur officiel llama.cpp pour les embeddings de mémoire GGUF locaux"
read_when:
  - Vous voulez des embeddings de recherche de mémoire à partir d'un modèle GGUF local
  - Vous configurez memorySearch.provider = "local"
  - Vous avez besoin du plugin OpenClaw qui possède le runtime node-llama-cpp
title: "Fournisseur llama.cpp"
sidebarTitle: "Fournisseur llama.cpp"
---

`llama-cpp` est le plugin fournisseur externe officiel pour les embeddings GGUF locaux.
Il possède la dépendance runtime `node-llama-cpp` utilisée par
`memorySearch.provider: "local"`.

Installez-le avant d'utiliser les embeddings de mémoire locaux :

```bash
openclaw plugins install @openclaw/llama-cpp-provider
```

Le package npm principal `openclaw` n'inclut pas `node-llama-cpp`. Garder la
dépendance native dans ce plugin empêche les mises à jour npm normales d'OpenClaw de
supprimer un runtime installé manuellement dans le répertoire du package OpenClaw.

## Configuration

Définissez le fournisseur de recherche de mémoire sur `local` :

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "local",
        local: {
          modelPath: "hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf",
        },
      },
    },
  },
}
```

Le modèle par défaut est `embeddinggemma-300m-qat-Q8_0.gguf`. Vous pouvez également pointer
`local.modelPath` vers un fichier `.gguf` local.

## Runtime natif

Utilisez Node 24 pour le chemin d'installation natif le plus fluide. Les checkouts de source utilisant pnpm
peuvent avoir besoin d'approuver et de reconstruire la dépendance native :

```bash
pnpm approve-builds
pnpm rebuild node-llama-cpp
```

Pour des embeddings locaux avec moins de friction, utilisez un fournisseur de service local tel que
Ollama ou LM Studio à la place.
