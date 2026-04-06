---
summary: "Page d'accueil unifiée pour les capacités de génération, de compréhension et de synthèse vocale de médias"
read_when:
  - Looking for an overview of media capabilities
  - Deciding which media provider to configure
  - Understanding how async media generation works
title: "Aperçu des médias"
---

# Génération et compréhension de médias

OpenClaw génère des images, des vidéos et de la musique, comprend les médias entrants (images, audio, vidéo) et lit les réponses à haute voix avec la synthèse vocale. Toutes les capacités médias sont basées sur des outils : l'agent décide quand les utiliser en fonction de la conversation, et chaque outil n'apparaît que si au moins un fournisseur de support est configuré.

## Capacités en un coup d'œil

| Capacité             | Outil            | Fournisseurs                                                                                 | Ce qu'il fait                                          |
| -------------------- | ---------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Génération d'images  | `image_generate` | ComfyUI, fal, Google, MiniMax, OpenAI, Vydra                                                 | Crée ou édite des images à partir de textes ou références |
| Génération vidéo     | `video_generate` | Alibaba, BytePlus, ComfyUI, fal, Google, MiniMax, OpenAI, Qwen, Runway, Together, Vydra, xAI | Crée des vidéos à partir de texte, d'images ou de vidéos existantes |
| Génération musicale  | `music_generate` | ComfyUI, Google, MiniMax                                                                     | Crée de la musique ou des pistes audio à partir de textes |
| Synthèse vocale (TTS) | `tts`            | ElevenLabs, Microsoft, MiniMax, OpenAI                                                       | Convertit les réponses sortantes en audio parlé        |
| Compréhension médias | (automatique)    | Tout fournisseur de modèle capable de vision/audio, plus les alternatives CLI                | Résume les images, l'audio et la vidéo entrants        |

## Matrice de capacités des fournisseurs

Ce tableau montre quels fournisseurs supportent quelles capacités médias sur la plateforme.

| Fournisseur | Image | Vidéo | Musique | TTS | STT / Transcription | Compréhension médias |
| ----------- | ----- | ----- | ------- | --- | ------------------- | -------------------- |
| Alibaba     |       | Oui   |         |     |                     |                      |
| BytePlus    |       | Oui   |         |     |                     |                      |
| ComfyUI     | Oui   | Oui   | Oui     |     |                     |                      |
| Deepgram    |       |       |         |     | Oui                 |                      |
| ElevenLabs  |       |       |         | Oui |                     |                      |
| fal         | Oui   | Oui   |         |     |                     |                      |
| Google      | Oui   | Oui   | Oui     |     |                     | Oui                  |
| Microsoft   |       |       |         | Oui |                     |                      |
| MiniMax     | Oui   | Oui   | Oui     | Oui |                     |                      |
| OpenAI      | Oui   | Oui   |         | Oui | Oui                 | Oui                  |
| Qwen        |       | Oui   |         |     |                     |                      |
| Runway      |       | Oui   |         |     |                     |                      |
| Together    |       | Oui   |         |     |                     |                      |
| Vydra       | Oui   | Oui   |         |     |                     |                      |
| xAI         |       | Oui   |         |     |                     |                      |

<Note>
La compréhension des médias utilise tout modèle capable de vision ou d'audio enregistré dans votre configuration de fournisseur. Le tableau ci-dessus met en évidence les fournisseurs avec un support dédié à la compréhension des médias ; la plupart des fournisseurs de modèles de langage avec des modèles multimodaux (Anthropic, Google, OpenAI, etc.) peuvent également comprendre les médias entrants lorsqu'ils sont configurés comme modèle de réponse actif.
</Note>

## Fonctionnement de la génération asynchrone

La génération vidéo et musicale s'exécutent en tant que tâches de fond car le traitement par le fournisseur prend généralement 30 secondes à plusieurs minutes. Lorsque l'agent appelle `video_generate` ou `music_generate`, OpenClaw soumet la demande au fournisseur, retourne immédiatement un ID de tâche et suit le travail dans le registre des tâches. L'agent continue à répondre à d'autres messages pendant que le travail s'exécute. Lorsque le fournisseur termine, OpenClaw réveille l'agent pour qu'il puisse publier les médias terminés dans le canal d'origine. La génération d'images et la TTS sont synchrones et se complètent en ligne avec la réponse.

## Liens rapides

- [Génération d'images](/fr/tools/image-generation) -- génération et édition d'images
- [Génération vidéo](/fr/tools/video-generation) -- texte vers vidéo, image vers vidéo et vidéo vers vidéo
- [Génération musicale](/fr/tools/music-generation) -- création de musique et de pistes audio
- [Synthèse vocale](/fr/tools/tts) -- conversion des réponses en audio parlé
- [Compréhension des médias](/fr/nodes/media-understanding) -- compréhension des images, de l'audio et de la vidéo entrants
