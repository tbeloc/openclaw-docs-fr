---
summary: "Générer de la musique avec des fournisseurs partagés, y compris les plugins basés sur des workflows"
read_when:
  - Generating music or audio via the agent
  - Configuring music generation providers and models
  - Understanding the music_generate tool parameters
title: "Music Generation"
---

# Génération de musique

L'outil `music_generate` permet à l'agent de créer de la musique ou de l'audio via la
capacité de génération de musique partagée avec des fournisseurs configurés tels que Google,
MiniMax et ComfyUI configuré par workflow.

Pour les sessions d'agent soutenues par des fournisseurs partagés, OpenClaw démarre la génération de musique en tant que
tâche de fond, la suit dans le registre des tâches, puis réveille l'agent à nouveau lorsque
la piste est prête afin que l'agent puisse publier l'audio terminé dans le
canal d'origine.

<Note>
L'outil partagé intégré n'apparaît que lorsqu'au moins un fournisseur de génération de musique est disponible. Si vous ne voyez pas `music_generate` dans les outils de votre agent, configurez `agents.defaults.musicGenerationModel` ou configurez une clé API de fournisseur.
</Note>

## Démarrage rapide

### Génération soutenue par un fournisseur partagé

1. Définissez une clé API pour au moins un fournisseur, par exemple `GEMINI_API_KEY` ou
   `MINIMAX_API_KEY`.
2. Définissez éventuellement votre modèle préféré :

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: {
        primary: "google/lyria-3-clip-preview",
      },
    },
  },
}
```

3. Demandez à l'agent : _"Generate an upbeat synthpop track about a night drive
   through a neon city."_

L'agent appelle `music_generate` automatiquement. Aucune liste d'autorisation d'outil nécessaire.

Pour les contextes synchrones directs sans exécution d'agent soutenue par une session, l'outil intégré
revient toujours à la génération en ligne et retourne le chemin du média final dans
le résultat de l'outil.

Exemples de prompts :

```text
Generate a cinematic piano track with soft strings and no vocals.
```

```text
Generate an energetic chiptune loop about launching a rocket at sunrise.
```

### Génération Comfy pilotée par workflow

Le plugin `comfy` fourni se connecte à l'outil `music_generate` partagé via
le registre des fournisseurs de génération de musique.

1. Configurez `models.providers.comfy.music` avec un JSON de workflow et
   des nœuds de prompt/sortie.
2. Si vous utilisez Comfy Cloud, définissez `COMFY_API_KEY` ou `COMFY_CLOUD_API_KEY`.
3. Demandez à l'agent de la musique ou appelez l'outil directement.

Exemple :

```text
/tool music_generate prompt="Warm ambient synth loop with soft tape texture"
```

## Support des fournisseurs partagés intégrés

| Fournisseur | Modèle par défaut      | Entrées de référence | Contrôles supportés                                       | Clé API                                |
| ----------- | ---------------------- | -------------------- | --------------------------------------------------------- | -------------------------------------- |
| ComfyUI     | `workflow`             | Jusqu'à 1 image      | Musique ou audio défini par workflow                      | `COMFY_API_KEY`, `COMFY_CLOUD_API_KEY` |
| Google      | `lyria-3-clip-preview` | Jusqu'à 10 images    | `lyrics`, `instrumental`, `format`                        | `GEMINI_API_KEY`, `GOOGLE_API_KEY`     |
| MiniMax     | `music-2.5+`           | Aucun                | `lyrics`, `instrumental`, `durationSeconds`, `format=mp3` | `MINIMAX_API_KEY`                      |

Utilisez `action: "list"` pour inspecter les fournisseurs et modèles partagés disponibles à
l'exécution :

```text
/tool music_generate action=list
```

Utilisez `action: "status"` pour inspecter la tâche de musique active soutenue par la session :

```text
/tool music_generate action=status
```

Exemple de génération directe :

```text
/tool music_generate prompt="Dreamy lo-fi hip hop with vinyl texture and gentle rain" instrumental=true
```

## Paramètres de l'outil intégré

| Paramètre         | Type     | Description                                                                                       |
| ----------------- | -------- | ------------------------------------------------------------------------------------------------- |
| `prompt`          | string   | Prompt de génération de musique (requis pour `action: "generate"`)                                |
| `action`          | string   | `"generate"` (par défaut), `"status"` pour la tâche de session actuelle, ou `"list"` pour inspecter les fournisseurs |
| `model`           | string   | Remplacement du fournisseur/modèle, par ex. `google/lyria-3-pro-preview` ou `comfy/workflow`     |
| `lyrics`          | string   | Paroles optionnelles lorsque le fournisseur supporte l'entrée de paroles explicites              |
| `instrumental`    | boolean  | Demander une sortie instrumentale uniquement lorsque le fournisseur la supporte                  |
| `image`           | string   | Chemin ou URL d'une seule image de référence                                                     |
| `images`          | string[] | Plusieurs images de référence (jusqu'à 10)                                                       |
| `durationSeconds` | number   | Durée cible en secondes lorsque le fournisseur supporte les indices de durée                     |
| `format`          | string   | Indice de format de sortie (`mp3` ou `wav`) lorsque le fournisseur le supporte                   |
| `filename`        | string   | Indice de nom de fichier de sortie                                                               |

Tous les fournisseurs ne supportent pas tous les paramètres. OpenClaw valide toujours les limites strictes
telles que les comptages d'entrée avant la soumission, mais les indices optionnels non supportés sont
ignorés avec un avertissement lorsque le fournisseur ou le modèle sélectionné ne peut pas les honorer.

## Comportement asynchrone pour le chemin soutenu par un fournisseur partagé

- Exécutions d'agent soutenues par une session : `music_generate` crée une tâche de fond, retourne une réponse de tâche/démarrage immédiatement, et publie la piste terminée plus tard dans un message d'agent de suivi.
- Prévention des doublons : tant que cette tâche de fond est toujours `queued` ou `running`, les appels ultérieurs de `music_generate` dans la même session retournent le statut de la tâche au lieu de démarrer une autre génération.
- Recherche de statut : utilisez `action: "status"` pour inspecter la tâche de musique active soutenue par la session sans en démarrer une nouvelle.
- Suivi des tâches : utilisez `openclaw tasks list` ou `openclaw tasks show <taskId>` pour inspecter le statut en attente, en cours d'exécution et terminal pour la génération.
- Réveil à la fin : OpenClaw injecte un événement de fin interne dans la même session afin que le modèle puisse écrire lui-même le suivi orienté utilisateur.
- Indice de prompt : les tours ultérieurs de l'utilisateur/manuel dans la même session reçoivent un petit indice d'exécution lorsqu'une tâche de musique est déjà en cours afin que le modèle n'appelle pas aveuglément `music_generate` à nouveau.
- Secours sans session : les contextes directs/locaux sans véritable session d'agent s'exécutent toujours en ligne et retournent le résultat audio final dans le même tour.

## Configuration

### Sélection du modèle

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: {
        primary: "google/lyria-3-clip-preview",
        fallbacks: ["minimax/music-2.5+"],
      },
    },
  },
}
```

### Ordre de sélection des fournisseurs

Lors de la génération de musique, OpenClaw essaie les fournisseurs dans cet ordre :

1. Paramètre `model` de l'appel d'outil, si l'agent en spécifie un
2. `musicGenerationModel.primary` de la configuration
3. `musicGenerationModel.fallbacks` dans l'ordre
4. Détection automatique utilisant uniquement les valeurs par défaut des fournisseurs basées sur l'authentification :
   - fournisseur par défaut actuel en premier
   - fournisseurs de génération de musique enregistrés restants dans l'ordre des ID de fournisseur

Si un fournisseur échoue, le candidat suivant est essayé automatiquement. Si tous échouent, l'erreur
inclut les détails de chaque tentative.

## Notes sur les fournisseurs

- Google utilise la génération par lot Lyria 3. Le flux fourni actuel supporte
  le prompt, le texte des paroles optionnel et les images de référence optionnelles.
- MiniMax utilise le point de terminaison par lot `music_generation`. Le flux fourni actuel
  supporte le prompt, les paroles optionnelles, le mode instrumental, la direction de durée et
  la sortie mp3.
- Le support de ComfyUI est piloté par workflow et dépend du graphique configuré plus
  le mappage des nœuds pour les champs de prompt/sortie.

## Choisir le bon chemin

- Utilisez le chemin soutenu par un fournisseur partagé lorsque vous voulez la sélection de modèle, le basculement de fournisseur et le flux de tâche/statut asynchrone intégré.
- Utilisez un chemin de plugin tel que ComfyUI lorsque vous avez besoin d'un graphique de workflow personnalisé ou d'un fournisseur qui ne fait pas partie de la capacité de musique partagée intégrée.
- Si vous déboguez un comportement spécifique à ComfyUI, consultez [ComfyUI](/fr/providers/comfy). Si vous déboguez un comportement de fournisseur partagé, commencez par [Google (Gemini)](/fr/providers/google) ou [MiniMax](/fr/providers/minimax).

## Tests en direct

Couverture en direct optionnelle pour les fournisseurs partagés intégrés :

```bash
OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/music-generation-providers.live.test.ts
```

Couverture en direct optionnelle pour le chemin de musique ComfyUI fourni :

```bash
OPENCLAW_LIVE_TEST=1 COMFY_LIVE_TEST=1 pnpm test:live -- extensions/comfy/comfy.live.test.ts
```

Le fichier Comfy en direct couvre également les workflows d'image et de vidéo comfy lorsque ces
sections sont configurées.

## Connexes

- [Background Tasks](/fr/automation/tasks) - suivi des tâches pour les exécutions `music_generate` détachées
- [Configuration Reference](/fr/gateway/configuration-reference#agent-defaults) - configuration `musicGenerationModel`
- [ComfyUI](/fr/providers/comfy)
- [Google (Gemini)](/fr/providers/google)
- [MiniMax](/fr/providers/minimax)
- [Models](/fr/concepts/models) - configuration du modèle et basculement
- [Tools Overview](/fr/tools)
