---
summary: "Générer et modifier des images à l'aide de fournisseurs configurés (OpenAI, Google Gemini, fal, MiniMax)"
read_when:
  - Generating images via the agent
  - Configuring image generation providers and models
  - Understanding the image_generate tool parameters
title: "Génération d'images"
---

# Génération d'images

L'outil `image_generate` permet à l'agent de créer et modifier des images à l'aide de vos fournisseurs configurés. Les images générées sont livrées automatiquement en tant que pièces jointes multimédias dans la réponse de l'agent.

<Note>
L'outil n'apparaît que lorsqu'au moins un fournisseur de génération d'images est disponible. Si vous ne voyez pas `image_generate` dans les outils de votre agent, configurez `agents.defaults.imageGenerationModel` ou configurez une clé API de fournisseur.
</Note>

## Démarrage rapide

1. Définissez une clé API pour au moins un fournisseur (par exemple `OPENAI_API_KEY` ou `GEMINI_API_KEY`).
2. Définissez éventuellement votre modèle préféré :

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: "openai/gpt-image-1",
    },
  },
}
```

3. Demandez à l'agent : _« Générez une image d'une mascotte homard amical. »_

L'agent appelle `image_generate` automatiquement. Aucune autorisation d'outil nécessaire — elle est activée par défaut lorsqu'un fournisseur est disponible.

## Fournisseurs pris en charge

| Fournisseur | Modèle par défaut | Support de l'édition | Clé API |
|---|---|---|---|
| OpenAI | `gpt-image-1` | Non | `OPENAI_API_KEY` |
| Google | `gemini-3.1-flash-image-preview` | Oui | `GEMINI_API_KEY` ou `GOOGLE_API_KEY` |
| fal | `fal-ai/flux/dev` | Oui | `FAL_KEY` |
| MiniMax | `image-01` | Oui (référence de sujet) | `MINIMAX_API_KEY` |

Utilisez `action: "list"` pour inspecter les fournisseurs et modèles disponibles à l'exécution :

```
/tool image_generate action=list
```

## Paramètres de l'outil

| Paramètre | Type | Description |
|---|---|---|
| `prompt` | string | Invite de génération d'image (obligatoire pour `action: "generate"`) |
| `action` | string | `"generate"` (par défaut) ou `"list"` pour inspecter les fournisseurs |
| `model` | string | Remplacement du fournisseur/modèle, par exemple `openai/gpt-image-1` |
| `image` | string | Chemin ou URL d'une seule image de référence pour le mode édition |
| `images` | string[] | Plusieurs images de référence pour le mode édition (jusqu'à 5) |
| `size` | string | Indice de taille : `1024x1024`, `1536x1024`, `1024x1536`, `1024x1792`, `1792x1024` |
| `aspectRatio` | string | Rapport d'aspect : `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |
| `resolution` | string | Indice de résolution : `1K`, `2K` ou `4K` |
| `count` | number | Nombre d'images à générer (1–4) |
| `filename` | string | Indice de nom de fichier de sortie |

Tous les fournisseurs ne prennent pas en charge tous les paramètres. L'outil transmet ce que chaque fournisseur prend en charge et ignore le reste.

## Configuration

### Sélection du modèle

```json5
{
  agents: {
    defaults: {
      // Forme chaîne : modèle principal uniquement
      imageGenerationModel: "google/gemini-3-pro-image-preview",

      // Forme objet : principal + secours ordonnés
      imageGenerationModel: {
        primary: "openai/gpt-image-1",
        fallbacks: ["google/gemini-3.1-flash-image-preview", "fal/fal-ai/flux/dev"],
      },
    },
  },
}
```

### Ordre de sélection du fournisseur

Lors de la génération d'une image, OpenClaw essaie les fournisseurs dans cet ordre :

1. **Paramètre `model`** de l'appel d'outil (si l'agent en spécifie un)
2. **`imageGenerationModel.primary`** de la configuration
3. **`imageGenerationModel.fallbacks`** dans l'ordre
4. **Détection automatique** — interroge tous les fournisseurs enregistrés pour les valeurs par défaut, en privilégiant : le fournisseur principal configuré, puis OpenAI, puis Google, puis les autres

Si un fournisseur échoue (erreur d'authentification, limite de débit, etc.), le candidat suivant est essayé automatiquement. Si tous échouent, l'erreur inclut les détails de chaque tentative.

### Édition d'images

Google, fal et MiniMax prennent en charge l'édition d'images de référence. Transmettez un chemin ou une URL d'image de référence :

```
"Générez une version aquarelle de cette photo" + image: "/path/to/photo.jpg"
```

Google prend en charge jusqu'à 5 images de référence via le paramètre `images`. fal et MiniMax en prennent en charge 1.

## Capacités des fournisseurs

| Capacité | OpenAI | Google | fal | MiniMax |
|---|---|---|---|---|
| Générer | Oui (jusqu'à 4) | Oui (jusqu'à 4) | Oui (jusqu'à 4) | Oui (jusqu'à 9) |
| Édition/référence | Non | Oui (jusqu'à 5 images) | Oui (1 image) | Oui (1 image, référence de sujet) |
| Contrôle de taille | Oui | Oui | Oui | Non |
| Rapport d'aspect | Non | Oui | Oui (génération uniquement) | Oui |
| Résolution (1K/2K/4K) | Non | Oui | Oui | Non |

## Connexes

- [Aperçu des outils](/fr/tools) — tous les outils d'agent disponibles
- [Référence de configuration](/fr/gateway/configuration-reference#agent-defaults) — configuration `imageGenerationModel`
- [Modèles](/fr/concepts/models) — configuration des modèles et basculement
