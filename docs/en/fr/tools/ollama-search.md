---
summary: "Recherche Web Ollama via votre hôte Ollama configuré"
read_when:
  - Vous voulez utiliser Ollama pour web_search
  - Vous voulez un fournisseur web_search sans clé
  - Vous avez besoin de conseils de configuration pour Ollama Web Search
title: "Ollama Web Search"
---

# Ollama Web Search

OpenClaw supporte **Ollama Web Search** en tant que fournisseur `web_search` intégré.
Il utilise l'API de recherche Web expérimentale d'Ollama et retourne des résultats structurés
avec des titres, des URL et des extraits.

Contrairement au fournisseur de modèle Ollama, cette configuration n'a pas besoin de clé API. Elle
nécessite :

- un hôte Ollama accessible depuis OpenClaw
- `ollama signin`

## Configuration

<Steps>
  <Step title="Démarrer Ollama">
    Assurez-vous qu'Ollama est installé et en cours d'exécution.
  </Step>
  <Step title="Se connecter">
    Exécutez :

    ```bash
    ollama signin
    ```

  </Step>
  <Step title="Choisir Ollama Web Search">
    Exécutez :

    ```bash
    openclaw configure --section web
    ```

    Puis sélectionnez **Ollama Web Search** comme fournisseur.

  </Step>
</Steps>

Si vous utilisez déjà Ollama pour les modèles, Ollama Web Search réutilise le même
hôte configuré.

## Config

```json5
{
  tools: {
    web: {
      search: {
        provider: "ollama",
      },
    },
  },
}
```

Remplacement optionnel de l'hôte Ollama :

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434",
      },
    },
  },
}
```

Si aucune URL de base Ollama explicite n'est définie, OpenClaw utilise `http://127.0.0.1:11434`.

## Notes

- Aucun champ de clé API n'est requis pour ce fournisseur.
- OpenClaw avertit lors de la configuration si Ollama est inaccessible ou non connecté, mais
  cela ne bloque pas la sélection.
- La détection automatique à l'exécution peut revenir à Ollama Web Search quand aucun fournisseur
  accrédité de priorité plus élevée n'est configuré.
- Le fournisseur utilise le point de terminaison expérimental `/api/experimental/web_search`
  d'Ollama.

## Liens connexes

- [Aperçu de Web Search](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [Ollama](/fr/providers/ollama) -- Configuration du modèle Ollama et modes cloud/local
