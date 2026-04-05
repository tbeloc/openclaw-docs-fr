---
summary: "Générer des vidéos à l'aide de fournisseurs configurés tels que Qwen"
read_when:
  - Generating videos via the agent
  - Configuring video generation providers and models
  - Understanding the video_generate tool parameters
title: "Génération de vidéos"
---

# Génération de vidéos

L'outil `video_generate` permet à l'agent de créer des vidéos à l'aide de vos fournisseurs configurés. Les vidéos générées sont livrées automatiquement en tant que pièces jointes multimédias dans la réponse de l'agent.

<Note>
L'outil n'apparaît que lorsqu'au moins un fournisseur de génération de vidéos est disponible. Si vous ne voyez pas `video_generate` dans les outils de votre agent, configurez `agents.defaults.videoGenerationModel` ou configurez une clé API de fournisseur.
</Note>

## Démarrage rapide

1. Définissez une clé API pour au moins un fournisseur (par exemple `QWEN_API_KEY`).
2. Définissez éventuellement votre modèle préféré :

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: "qwen/wan2.6-t2v",
    },
  },
}
```

3. Demandez à l'agent : _« Générez une vidéo cinématographique de 5 secondes d'un homard amical surfant au coucher du soleil. »_

L'agent appelle `video_generate` automatiquement. Aucune liste d'autorisation d'outils nécessaire — elle est activée par défaut lorsqu'un fournisseur est disponible.

## Fournisseurs pris en charge

| Fournisseur | Modèle par défaut | Entrées de référence | Clé API                                                    |
| ----------- | ----------------- | -------------------- | ---------------------------------------------------------- |
| Qwen        | `wan2.6-t2v`      | Oui, URLs distantes  | `QWEN_API_KEY`, `MODELSTUDIO_API_KEY`, `DASHSCOPE_API_KEY` |

Utilisez `action: "list"` pour inspecter les fournisseurs et modèles disponibles à l'exécution :

```
/tool video_generate action=list
```

## Paramètres de l'outil

| Paramètre         | Type     | Description                                                                           |
| ----------------- | -------- | ------------------------------------------------------------------------------------- |
| `prompt`          | string   | Invite de génération de vidéo (obligatoire pour `action: "generate"`)                 |
| `action`          | string   | `"generate"` (par défaut) ou `"list"` pour inspecter les fournisseurs                 |
| `model`           | string   | Remplacement du fournisseur/modèle, par ex. `qwen/wan2.6-t2v`                        |
| `image`           | string   | Chemin ou URL d'une seule image de référence                                         |
| `images`          | string[] | Plusieurs images de référence (jusqu'à 5)                                             |
| `video`           | string   | Chemin ou URL d'une seule vidéo de référence                                         |
| `videos`          | string[] | Plusieurs vidéos de référence (jusqu'à 4)                                             |
| `size`            | string   | Indice de taille lorsque le fournisseur le supporte                                   |
| `aspectRatio`     | string   | Rapport d'aspect : `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |
| `resolution`      | string   | Indice de résolution : `480P`, `720P`, ou `1080P`                                     |
| `durationSeconds` | number   | Durée cible en secondes                                                               |
| `audio`           | boolean  | Activer l'audio généré lorsque le fournisseur le supporte                             |
| `watermark`       | boolean  | Basculer le filigrane du fournisseur lorsqu'il est pris en charge                     |
| `filename`        | string   | Indice de nom de fichier de sortie                                                    |

Tous les fournisseurs ne supportent pas tous les paramètres. L'outil valide les limites de capacité du fournisseur avant de soumettre la demande.

## Configuration

### Sélection du modèle

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "qwen/wan2.6-t2v",
        fallbacks: ["qwen/wan2.6-r2v-flash"],
      },
    },
  },
}
```

### Ordre de sélection du fournisseur

Lors de la génération d'une vidéo, OpenClaw essaie les fournisseurs dans cet ordre :

1. **Paramètre `model`** de l'appel d'outil (si l'agent en spécifie un)
2. **`videoGenerationModel.primary`** de la configuration
3. **`videoGenerationModel.fallbacks`** dans l'ordre
4. **Détection automatique** — utilise uniquement les valeurs par défaut du fournisseur soutenues par l'authentification :
   - fournisseur par défaut actuel en premier
   - fournisseurs de génération de vidéos enregistrés restants dans l'ordre des ID de fournisseur

Si un fournisseur échoue, le candidat suivant est essayé automatiquement. Si tous échouent, l'erreur inclut les détails de chaque tentative.

## Entrées de référence Qwen

Le fournisseur Qwen fourni supporte le texte vers vidéo ainsi que les modes de référence image/vidéo, mais le point de terminaison vidéo DashScope en amont nécessite actuellement des **URLs http(s) distantes** pour les entrées de référence. Les chemins de fichiers locaux et les tampons téléchargés sont rejetés d'avance au lieu d'être ignorés silencieusement.

## Connexes

- [Aperçu des outils](/fr/tools) — tous les outils d'agent disponibles
- [Qwen](/fr/providers/qwen) — configuration spécifique à Qwen et limites
- [Référence de configuration](/fr/gateway/configuration-reference#agent-defaults) — configuration `videoGenerationModel`
- [Modèles](/fr/concepts/models) — configuration des modèles et basculement
