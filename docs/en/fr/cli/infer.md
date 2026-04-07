---
summary: "CLI inférence pour les workflows de modèles, images, audio, TTS, vidéo, web et embeddings soutenus par des fournisseurs"
read_when:
  - Adding or modifying `openclaw infer` commands
  - Designing stable headless capability automation
title: "CLI d'inférence"
---

# CLI d'inférence

`openclaw infer` est la surface headless canonique pour les workflows d'inférence soutenus par des fournisseurs.

Elle expose intentionnellement les familles de capacités, et non les noms RPC bruts de la passerelle ni les identifiants bruts des outils d'agent.

## Transformer infer en compétence

Copiez et collez ceci dans un agent :

```text
Read https://docs.openclaw.ai/cli/infer, then create a skill that routes my common workflows to `openclaw infer`.
Focus on model runs, image generation, video generation, audio transcription, TTS, web search, and embeddings.
```

Une bonne compétence basée sur infer devrait :

- mapper les intentions utilisateur courantes à la bonne sous-commande infer
- inclure quelques exemples infer canoniques pour les workflows qu'elle couvre
- préférer `openclaw infer ...` dans les exemples et suggestions
- éviter de redocumenter toute la surface infer dans le corps de la compétence

Couverture typique axée sur infer :

- `openclaw infer model run`
- `openclaw infer image generate`
- `openclaw infer audio transcribe`
- `openclaw infer tts convert`
- `openclaw infer web search`
- `openclaw infer embedding create`

## Pourquoi utiliser infer

`openclaw infer` fournit une CLI cohérente pour les tâches d'inférence soutenues par des fournisseurs dans OpenClaw.

Avantages :

- Utilisez les fournisseurs et modèles déjà configurés dans OpenClaw au lieu de câbler des wrappers ponctuels pour chaque backend.
- Gardez les workflows de modèle, image, transcription audio, TTS, vidéo, web et embedding sous un seul arbre de commandes.
- Utilisez une forme de sortie `--json` stable pour les scripts, l'automatisation et les workflows pilotés par agent.
- Préférez une surface OpenClaw propriétaire de première partie quand la tâche est fondamentalement « exécuter l'inférence ».
- Utilisez le chemin local normal sans nécessiter la passerelle pour la plupart des commandes infer.

## Arbre de commandes

```text
 openclaw infer
  list
  inspect

  model
    run
    list
    inspect
    providers
    auth login
    auth logout
    auth status

  image
    generate
    edit
    describe
    describe-many
    providers

  audio
    transcribe
    providers

  tts
    convert
    voices
    providers
    status
    enable
    disable
    set-provider

  video
    generate
    describe
    providers

  web
    search
    fetch
    providers

  embedding
    create
    providers
```

## Tâches courantes

Ce tableau mappe les tâches d'inférence courantes à la commande infer correspondante.

| Tâche                          | Commande                                                                | Notes                                                |
| ------------------------------ | ---------------------------------------------------------------------- | ---------------------------------------------------- |
| Exécuter une invite de texte/modèle | `openclaw infer model run --prompt "..." --json`                       | Utilise le chemin local normal par défaut                |
| Générer une image       | `openclaw infer image generate --prompt "..." --json`                  | Utilisez `image edit` en partant d'un fichier existant |
| Décrire un fichier image  | `openclaw infer image describe --file ./image.png --json`              | `--model` doit être `<provider/model>`                 |
| Transcrire l'audio        | `openclaw infer audio transcribe --file ./memo.m4a --json`             | `--model` doit être `<provider/model>`                 |
| Synthétiser la parole       | `openclaw infer tts convert --text "..." --output ./speech.mp3 --json` | `tts status` est orienté passerelle                     |
| Générer une vidéo        | `openclaw infer video generate --prompt "..." --json`                  |                                                      |
| Décrire un fichier vidéo   | `openclaw infer video describe --file ./clip.mp4 --json`               | `--model` doit être `<provider/model>`                 |
| Rechercher sur le web          | `openclaw infer web search --query "..." --json`                       |                                                      |
| Récupérer une page web        | `openclaw infer web fetch --url https://example.com --json`            |                                                      |
| Créer des embeddings       | `openclaw infer embedding create --text "..." --json`                  |                                                      |

## Comportement

- `openclaw infer ...` est la surface CLI principale pour ces workflows.
- Utilisez `--json` quand la sortie sera consommée par une autre commande ou un script.
- Utilisez `--provider` ou `--model provider/model` quand un backend spécifique est requis.
- Pour `image describe`, `audio transcribe` et `video describe`, `--model` doit utiliser la forme `<provider/model>`.
- Les commandes d'exécution sans état par défaut sont locales.
- Les commandes d'état gérées par la passerelle par défaut sont la passerelle.
- Le chemin local normal ne nécessite pas que la passerelle soit en cours d'exécution.

## Modèle

Utilisez `model` pour l'inférence de texte soutenue par des fournisseurs et l'inspection de modèle/fournisseur.

```bash
openclaw infer model run --prompt "Reply with exactly: smoke-ok" --json
openclaw infer model run --prompt "Summarize this changelog entry" --provider openai --json
openclaw infer model providers --json
openclaw infer model inspect --name gpt-5.4 --json
```

Notes :

- `model run` réutilise le runtime d'agent afin que les remplacements de fournisseur/modèle se comportent comme l'exécution d'agent normal.
- `model auth login`, `model auth logout` et `model auth status` gèrent l'état d'authentification du fournisseur enregistré.

## Image

Utilisez `image` pour la génération, l'édition et la description.

```bash
openclaw infer image generate --prompt "friendly lobster illustration" --json
openclaw infer image generate --prompt "cinematic product photo of headphones" --json
openclaw infer image describe --file ./photo.jpg --json
openclaw infer image describe --file ./ui-screenshot.png --model openai/gpt-4.1-mini --json
```

Notes :

- Utilisez `image edit` en partant de fichiers d'entrée existants.
- Pour `image describe`, `--model` doit être `<provider/model>`.

## Audio

Utilisez `audio` pour la transcription de fichiers.

```bash
openclaw infer audio transcribe --file ./memo.m4a --json
openclaw infer audio transcribe --file ./team-sync.m4a --language en --prompt "Focus on names and action items" --json
openclaw infer audio transcribe --file ./memo.m4a --model openai/whisper-1 --json
```

Notes :

- `audio transcribe` est pour la transcription de fichiers, pas la gestion de session en temps réel.
- `--model` doit être `<provider/model>`.

## TTS

Utilisez `tts` pour la synthèse vocale et l'état du fournisseur TTS.

```bash
openclaw infer tts convert --text "hello from openclaw" --output ./hello.mp3 --json
openclaw infer tts convert --text "Your build is complete" --output ./build-complete.mp3 --json
openclaw infer tts providers --json
openclaw infer tts status --json
```

Notes :

- `tts status` par défaut à la passerelle car il reflète l'état TTS géré par la passerelle.
- Utilisez `tts providers`, `tts voices` et `tts set-provider` pour inspecter et configurer le comportement TTS.

## Vidéo

Utilisez `video` pour la génération et la description.

```bash
openclaw infer video generate --prompt "cinematic sunset over the ocean" --json
openclaw infer video generate --prompt "slow drone shot over a forest lake" --json
openclaw infer video describe --file ./clip.mp4 --json
openclaw infer video describe --file ./clip.mp4 --model openai/gpt-4.1-mini --json
```

Notes :

- `--model` doit être `<provider/model>` pour `video describe`.

## Web

Utilisez `web` pour les workflows de recherche et de récupération.

```bash
openclaw infer web search --query "OpenClaw docs" --json
openclaw infer web search --query "OpenClaw infer web providers" --json
openclaw infer web fetch --url https://docs.openclaw.ai/cli/infer --json
openclaw infer web providers --json
```

Notes :

- Utilisez `web providers` pour inspecter les fournisseurs disponibles, configurés et sélectionnés.

## Embedding

Utilisez `embedding` pour la création de vecteurs et l'inspection du fournisseur d'embedding.

```bash
openclaw infer embedding create --text "friendly lobster" --json
openclaw infer embedding create --text "customer support ticket: delayed shipment" --model openai/text-embedding-3-large --json
openclaw infer embedding providers --json
```

## Sortie JSON

Les commandes infer normalisent la sortie JSON sous une enveloppe partagée :

```json
{
  "ok": true,
  "capability": "image.generate",
  "transport": "local",
  "provider": "openai",
  "model": "gpt-image-1",
  "attempts": [],
  "outputs": []
}
```

Les champs de niveau supérieur sont stables :

- `ok`
- `capability`
- `transport`
- `provider`
- `model`
- `attempts`
- `outputs`
- `error`

## Pièges courants

```bash
# Mauvais
openclaw infer media image generate --prompt "friendly lobster"

# Bon
openclaw infer image generate --prompt "friendly lobster"
```

```bash
# Mauvais
openclaw infer audio transcribe --file ./memo.m4a --model whisper-1 --json

# Bon
openclaw infer audio transcribe --file ./memo.m4a --model openai/whisper-1 --json
```

## Notes

- `openclaw capability ...` est un alias pour `openclaw infer ...`.
