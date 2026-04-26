---
summary: "Synthèse vocale en streaming Inworld pour les réponses OpenClaw"
read_when:
  - You want Inworld speech synthesis for outbound replies
  - You need PCM telephony or OGG_OPUS voice-note output from Inworld
title: "Inworld"
---

Inworld est un fournisseur de synthèse vocale en streaming (TTS). Dans OpenClaw, il
synthétise l'audio des réponses sortantes (MP3 par défaut, OGG_OPUS pour les notes vocales)
et l'audio PCM pour les canaux de téléphonie tels que Voice Call.

OpenClaw envoie des requêtes au point de terminaison TTS en streaming d'Inworld, concatène
les chunks audio base64 retournés dans un seul buffer, et transmet le résultat au
pipeline standard de traitement de l'audio de réponse.

| Détail        | Valeur                                                      |
| ------------- | ----------------------------------------------------------- |
| Site web      | [inworld.ai](https://inworld.ai)                            |
| Documentation | [docs.inworld.ai/tts/tts](https://docs.inworld.ai/tts/tts)  |
| Authentification | `INWORLD_API_KEY` (HTTP Basic, credential Base64 du tableau de bord) |
| Voix par défaut | `Sarah`                                                     |
| Modèle par défaut | `inworld-tts-1.5-max`                                       |

## Démarrage rapide

<Steps>
  <Step title="Définissez votre clé API">
    Copiez les identifiants de votre tableau de bord Inworld (Workspace > API Keys)
    et définissez-les comme variable d'environnement. La valeur est envoyée verbatim comme
    identifiant HTTP Basic, donc ne l'encodez pas à nouveau en Base64 ni ne la convertissez
    en token bearer.

    ```
    INWORLD_API_KEY=<base64-credential-from-dashboard>
    ```

  </Step>
  <Step title="Sélectionnez Inworld dans messages.tts">
    ```json5
    {
      messages: {
        tts: {
          auto: "always",
          provider: "inworld",
          providers: {
            inworld: {
              voiceId: "Sarah",
              modelId: "inworld-tts-1.5-max",
            },
          },
        },
      },
    }
    ```
  </Step>
  <Step title="Envoyez un message">
    Envoyez une réponse via n'importe quel canal connecté. OpenClaw synthétise l'audio
    avec Inworld et le livre en MP3 (ou OGG_OPUS lorsque le canal
    attend une note vocale).
  </Step>
</Steps>

## Options de configuration

| Option        | Chemin                                       | Description                                                       |
| ------------- | -------------------------------------------- | ----------------------------------------------------------------- |
| `apiKey`      | `messages.tts.providers.inworld.apiKey`      | Credential Base64 du tableau de bord. Revient à `INWORLD_API_KEY`. |
| `baseUrl`     | `messages.tts.providers.inworld.baseUrl`     | Remplacez l'URL de base de l'API Inworld (par défaut `https://api.inworld.ai`). |
| `voiceId`     | `messages.tts.providers.inworld.voiceId`     | Identifiant de voix (par défaut `Sarah`).                         |
| `modelId`     | `messages.tts.providers.inworld.modelId`     | ID du modèle TTS (par défaut `inworld-tts-1.5-max`).              |
| `temperature` | `messages.tts.providers.inworld.temperature` | Température d'échantillonnage `0..2` (optionnel).                 |

## Notes

<AccordionGroup>
  <Accordion title="Authentification">
    Inworld utilise l'authentification HTTP Basic avec une seule chaîne de credential encodée en Base64.
    Copiez-la verbatim depuis le tableau de bord Inworld. Le fournisseur l'envoie comme
    `Authorization: Basic <apiKey>` sans encodage supplémentaire, donc
    ne l'encodez pas vous-même en Base64 et ne passez pas un token de style bearer.
    Voir [Notes d'authentification TTS](/fr/tools/tts#inworld-primary) pour le même avertissement.
  </Accordion>
  <Accordion title="Modèles">
    IDs de modèles supportés : `inworld-tts-1.5-max` (par défaut),
    `inworld-tts-1.5-mini`, `inworld-tts-1-max`, `inworld-tts-1`.
  </Accordion>
  <Accordion title="Sorties audio">
    Les réponses utilisent MP3 par défaut. Lorsque la cible du canal est `voice-note`,
    OpenClaw demande à Inworld `OGG_OPUS` pour que l'audio soit lu comme une bulle
    vocale native. La synthèse de téléphonie utilise du `PCM` brut à 22050 Hz pour alimenter
    le pont de téléphonie.
  </Accordion>
  <Accordion title="Points de terminaison personnalisés">
    Remplacez l'hôte API avec `messages.tts.providers.inworld.baseUrl`.
    Les barres obliques finales sont supprimées avant l'envoi des requêtes.
  </Accordion>
</AccordionGroup>

## Connexes

<CardGroup cols={2}>
  <Card title="Synthèse vocale" href="/fr/tools/tts" icon="waveform-lines">
    Aperçu TTS, fournisseurs et configuration `messages.tts`.
  </Card>
  <Card title="Configuration" href="/fr/gateway/configuration" icon="gear">
    Référence de configuration complète incluant les paramètres `messages.tts`.
  </Card>
  <Card title="Fournisseurs" href="/fr/providers" icon="grid">
    Tous les fournisseurs OpenClaw intégrés.
  </Card>
  <Card title="Dépannage" href="/fr/help/troubleshooting" icon="wrench">
    Problèmes courants et étapes de débogage.
  </Card>
</CardGroup>
