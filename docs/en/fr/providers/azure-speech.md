---
summary: "Azure AI Speech text-to-speech pour les réponses OpenClaw"
read_when:
  - You want Azure Speech synthesis for outbound replies
  - You need native Ogg Opus voice-note output from Azure Speech
title: "Azure Speech"
---

Azure Speech est un fournisseur de synthèse vocale Azure AI Speech text-to-speech. Dans OpenClaw, il synthétise l'audio des réponses sortantes en MP3 par défaut, en Ogg/Opus natif pour les notes vocales, et en audio mulaw 8 kHz pour les canaux de téléphonie tels que Voice Call.

OpenClaw utilise directement l'API REST Azure Speech avec SSML et envoie le format de sortie propriétaire du fournisseur via `X-Microsoft-OutputFormat`.

| Détail                  | Valeur                                                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| Site web                | [Azure AI Speech](https://azure.microsoft.com/products/ai-services/ai-speech)                                  |
| Documentation           | [Speech REST text-to-speech](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech) |
| Authentification        | `AZURE_SPEECH_KEY` plus `AZURE_SPEECH_REGION`                                                                  |
| Voix par défaut         | `en-US-JennyNeural`                                                                                            |
| Sortie fichier par défaut | `audio-24khz-48kbitrate-mono-mp3`                                                                              |
| Fichier note vocale par défaut | `ogg-24khz-16bit-mono-opus`                                                                                    |

## Commencer

<Steps>
  <Step title="Créer une ressource Azure Speech">
    Dans le portail Azure, créez une ressource Speech. Copiez **KEY 1** depuis
    Resource Management > Keys and Endpoint, et copiez l'emplacement de la ressource
    tel que `eastus`.

    ```
    AZURE_SPEECH_KEY=<speech-resource-key>
    AZURE_SPEECH_REGION=eastus
    ```

  </Step>
  <Step title="Sélectionner Azure Speech dans messages.tts">
    ```json5
    {
      messages: {
        tts: {
          auto: "always",
          provider: "azure-speech",
          providers: {
            "azure-speech": {
              voice: "en-US-JennyNeural",
              lang: "en-US",
            },
          },
        },
      },
    }
    ```
  </Step>
  <Step title="Envoyer un message">
    Envoyez une réponse via n'importe quel canal connecté. OpenClaw synthétise l'audio
    avec Azure Speech et livre le MP3 pour l'audio standard, ou Ogg/Opus quand
    le canal attend une note vocale.
  </Step>
</Steps>

## Options de configuration

| Option                  | Chemin                                                      | Description                                                                                           |
| ----------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `apiKey`                | `messages.tts.providers.azure-speech.apiKey`                | Clé de ressource Azure Speech. Revient à `AZURE_SPEECH_KEY`, `AZURE_SPEECH_API_KEY`, ou `SPEECH_KEY`. |
| `region`                | `messages.tts.providers.azure-speech.region`                | Région de ressource Azure Speech. Revient à `AZURE_SPEECH_REGION` ou `SPEECH_REGION`.                 |
| `endpoint`              | `messages.tts.providers.azure-speech.endpoint`              | Remplacement optionnel du point de terminaison/URL de base Azure Speech.                                                     |
| `baseUrl`               | `messages.tts.providers.azure-speech.baseUrl`               | Remplacement optionnel de l'URL de base Azure Speech.                                                              |
| `voice`                 | `messages.tts.providers.azure-speech.voice`                 | ShortName de voix Azure (par défaut `en-US-JennyNeural`).                                                  |
| `lang`                  | `messages.tts.providers.azure-speech.lang`                  | Code de langue SSML (par défaut `en-US`).                                                                 |
| `outputFormat`          | `messages.tts.providers.azure-speech.outputFormat`          | Format de sortie fichier audio (par défaut `audio-24khz-48kbitrate-mono-mp3`).                                 |
| `voiceNoteOutputFormat` | `messages.tts.providers.azure-speech.voiceNoteOutputFormat` | Format de sortie note vocale (par défaut `ogg-24khz-16bit-mono-opus`).                                       |

## Notes

<AccordionGroup>
  <Accordion title="Authentification">
    Azure Speech utilise une clé de ressource Speech, pas une clé Azure OpenAI. La clé
    est envoyée en tant que `Ocp-Apim-Subscription-Key` ; OpenClaw dérive
    `https://<region>.tts.speech.microsoft.com` de `region` sauf si vous
    fournissez `endpoint` ou `baseUrl`.
  </Accordion>
  <Accordion title="Noms de voix">
    Utilisez la valeur `ShortName` de voix Azure Speech, par exemple
    `en-US-JennyNeural`. Le fournisseur fourni peut lister les voix via la
    même ressource Speech et filtre les voix marquées comme dépréciées ou retirées.
  </Accordion>
  <Accordion title="Sorties audio">
    Azure accepte les formats de sortie tels que `audio-24khz-48kbitrate-mono-mp3`,
    `ogg-24khz-16bit-mono-opus`, et `riff-24khz-16bit-mono-pcm`. OpenClaw
    demande Ogg/Opus pour les cibles `voice-note` afin que les canaux puissent envoyer des
    bulles vocales natives sans conversion MP3 supplémentaire.
  </Accordion>
  <Accordion title="Alias">
    `azure` est accepté comme alias de fournisseur pour les PRs existantes et la configuration utilisateur,
    mais la nouvelle configuration doit utiliser `azure-speech` pour éviter la confusion avec les fournisseurs de modèles Azure
    OpenAI.
  </Accordion>
</AccordionGroup>

## Connexes

<CardGroup cols={2}>
  <Card title="Text-to-speech" href="/fr/tools/tts" icon="waveform-lines">
    Aperçu TTS, fournisseurs, et configuration `messages.tts`.
  </Card>
  <Card title="Configuration" href="/fr/gateway/configuration" icon="gear">
    Référence de configuration complète incluant les paramètres `messages.tts`.
  </Card>
  <Card title="Fournisseurs" href="/fr/providers" icon="grid">
    Tous les fournisseurs OpenClaw fournis.
  </Card>
  <Card title="Dépannage" href="/fr/help/troubleshooting" icon="wrench">
    Problèmes courants et étapes de débogage.
  </Card>
</CardGroup>
