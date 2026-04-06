---
summary: "Utilisez la génération d'images, vidéos et paroles Vydra dans OpenClaw"
read_when:
  - You want Vydra media generation in OpenClaw
  - You need Vydra API key setup guidance
title: "Vydra"
---

# Vydra

Le plugin Vydra fourni ajoute :

- la génération d'images via `vydra/grok-imagine`
- la génération de vidéos via `vydra/veo3` et `vydra/kling`
- la synthèse vocale via la route TTS soutenue par ElevenLabs de Vydra

OpenClaw utilise la même `VYDRA_API_KEY` pour les trois capacités.

## URL de base importante

Utilisez `https://www.vydra.ai/api/v1`.

L'hôte apex de Vydra (`https://vydra.ai/api/v1`) redirige actuellement vers `www`. Certains clients HTTP suppriment `Authorization` lors de cette redirection inter-hôtes, ce qui transforme une clé API valide en un échec d'authentification trompeur. Le plugin fourni utilise directement l'URL de base `www` pour éviter cela.

## Configuration

Intégration interactive :

```bash
openclaw onboard --auth-choice vydra-api-key
```

Ou définissez la variable d'environnement directement :

```bash
export VYDRA_API_KEY="vydra_live_..."
```

## Génération d'images

Modèle d'image par défaut :

- `vydra/grok-imagine`

Définissez-le comme fournisseur d'images par défaut :

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "vydra/grok-imagine",
      },
    },
  },
}
```

Le support fourni actuellement est texte vers image uniquement. Les routes d'édition hébergées de Vydra s'attendent à des URL d'images distantes, et OpenClaw n'ajoute pas encore de pont de téléchargement spécifique à Vydra dans le plugin fourni.

Voir [Génération d'images](/fr/tools/image-generation) pour le comportement des outils partagés.

## Génération de vidéos

Modèles vidéo enregistrés :

- `vydra/veo3` pour la génération texte vers vidéo
- `vydra/kling` pour la génération image vers vidéo

Définissez Vydra comme fournisseur vidéo par défaut :

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "vydra/veo3",
      },
    },
  },
}
```

Remarques :

- `vydra/veo3` est fourni en tant que texte vers vidéo uniquement.
- `vydra/kling` nécessite actuellement une référence d'URL d'image distante. Les téléchargements de fichiers locaux sont rejetés d'emblée.
- Le plugin fourni reste conservateur et ne transmet pas les paramètres de style non documentés tels que le rapport d'aspect, la résolution, le filigrane ou l'audio généré.

Voir [Génération de vidéos](/fr/tools/video-generation) pour le comportement des outils partagés.

## Synthèse vocale

Définissez Vydra comme fournisseur de parole :

```json5
{
  messages: {
    tts: {
      provider: "vydra",
      providers: {
        vydra: {
          apiKey: "${VYDRA_API_KEY}",
          voiceId: "21m00Tcm4TlvDq8ikWAM",
        },
      },
    },
  },
}
```

Valeurs par défaut :

- model: `elevenlabs/tts`
- voice id: `21m00Tcm4TlvDq8ikWAM`

Le plugin fourni expose actuellement une voix par défaut connue et fiable et retourne des fichiers audio MP3.

## Connexes

- [Répertoire des fournisseurs](/fr/providers/index)
- [Génération d'images](/fr/tools/image-generation)
- [Génération de vidéos](/fr/tools/video-generation)
