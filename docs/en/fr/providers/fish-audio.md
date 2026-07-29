---
summary: "Utilisez Fish Audio S2.1 hébergé ou S2 Pro local sur Apple silicon"
read_when:
  - You want Fish Audio text-to-speech in OpenClaw
  - You want expressive or cloned voices with Fish Audio
  - You want local Fish S2 Pro speech in macOS Talk mode
title: "Fish Audio"
---

OpenClaw supporte Fish Audio de deux façons distinctes :

- **S2.1 hébergé** s'exécute via le fournisseur de synthèse vocale `fish-audio` sur la Gateway et fonctionne sur tous les canaux, les notes vocales, Talk et la téléphonie.
- **S2 Pro local** s'exécute dans l'application macOS native via le fournisseur `mlx` Talk existant. Il reste sur le Mac et ne nécessite pas de clé API Fish.

<Warning>
Les poids S2 Pro téléchargeables utilisent la licence de recherche Fish Audio. L'utilisation personnelle,
la recherche et l'évaluation non commerciale sont autorisées ; l'utilisation commerciale nécessite une
licence Fish Audio distincte. L'utilisation de l'API hébergée suit les conditions de service de Fish Audio.
</Warning>

## S2.1 hébergé

Définissez une clé API à partir de la page [Fish Audio API Keys](https://fish.audio/app/api-keys) :

```bash
export FISH_API_KEY="..."
```

Ensuite, configurez le fournisseur :

```json5
{
  tts: {
    auto: "tagged",
    provider: "fish-audio",
    providers: {
      "fish-audio": {
        apiKey: "${FISH_API_KEY}",
        model: "s2.1-pro",
        // ID de modèle de voix Fish Audio sauvegardé ou public optionnel :
        speakerVoiceId: "802e3bc2b27e49c2995d23ef70e6ac89",
        latency: "balanced",
      },
    },
  },
}
```

`speakerVoiceId` est optionnel. Sans lui, Fish Audio utilise sa voix par défaut.
`FISH_AUDIO_API_KEY` est également accepté pour la compatibilité avec les plugins communautaires existants,
mais `FISH_API_KEY` est la variable d'environnement canonique du SDK Fish.

### Modèles hébergés

| Modèle          | Utilisation                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------- |
| `s2.1-pro`      | Par défaut. Service S2.1 de production avec les garanties de service hébergé attachées à votre plan.           |
| `s2.1-pro-free` | Accès promotionnel S2.1 jusqu'au 31 août 2026 ; aucune garantie TTFA ou DPA. Sélectionnez-le explicitement. |
| `s2-pro`        | Génération S2 précédente.                                                                                      |
| `s1`            | Génération précédente avec contrôles d'émotion entre parenthèses.                                              |

Le fournisseur demande MP3 pour l'audio ordinaire, Opus à 48 kHz pour les notes vocales natives,
et PCM brut à 8 kHz pour la téléphonie. Pour la voix Discord, OpenClaw consomme
la réponse HTTP fragmentée de Fish Audio au fur et à mesure de son arrivée au lieu d'attendre
l'intégralité du clip.

### Synthèse expressive

S2 et S2.1 acceptent les balises en langage naturel en ligne. Mettez-les dans le texte parlé :

```text
[whisper] Keep this between us. [pause] [excited] We shipped it!
```

Les balises courantes incluent `[whisper]`, `[laughing]`, `[excited]`, `[sad]`, `[pause]`,
et les instructions libres telles que `[professional broadcast tone]`.

### Sélection et clonage de voix

Utilisez `/tts status` pour inspecter le fournisseur actif et `/tts audio <text>` pour un
clip unique. Les identifiants de voix Fish peuvent provenir de vos propres voix entraînées ou de la
bibliothèque publique de voix Fish. OpenClaw liste d'abord vos voix, puis une page limitée
de voix publiques populaires.

Le fournisseur de synthèse vocale consomme les identifiants de voix existants ; il ne télécharge pas
d'enregistrements ni ne crée de modèles de voix. La création de voix est une action distincte
sensible au consentement dans l'application ou l'API Fish Audio.

## S2 Pro local sur macOS

L'application macOS native intègre un assistant MLX TTS isolé. Sur Apple silicon, pointez
le fournisseur `mlx` Talk existant vers la conversion Fish 8 bits :

```json5
{
  talk: {
    provider: "mlx",
    providers: {
      mlx: {
        modelId: "mlx-community/fish-audio-s2-pro-8bit",
      },
    },
  },
}
```

La première énonciation télécharge environ 6,8 Go de données de modèle et de codec. OpenClaw
garde un modèle MLX sélectionné résident pour les énunciations répétées, puis le décharge
après cinq minutes d'inactivité, l'arrêt de l'application ou la pression mémoire.

### Voix de référence locale

Lorsque la Gateway et l'application macOS partagent le même système de fichiers, configurez un
enregistrement de référence propre de 10 à 30 secondes et sa transcription exacte :

```json5
{
  talk: {
    provider: "mlx",
    providers: {
      mlx: {
        modelId: "mlx-community/fish-audio-s2-pro-8bit",
        referenceAudioPath: "/Users/example/Voices/reference.wav",
        referenceText: "The exact words spoken in the reference recording.",
      },
    },
  },
}
```

`referenceAudioPath` est résolu sur le Mac exécutant l'application native, pas sur une
Gateway distante. Le fichier reste local : l'application ne le transmet qu'à son assistant MLX
isolé. La sortie Fish locale est diffusée en continu en tant que PCM dans la lecture Talk afin que
la synthèse vocale puisse commencer avant qu'une longue génération ne se termine.

<Note>
MLX local s'applique actuellement uniquement à Talk macOS natif. Les autres canaux et
clients utilisent le fournisseur de synthèse vocale hébergé sélectionné par la Gateway. iOS et Android conservent
leurs chemins Talk natifs/système et Gateway existants.
</Note>

## Dépannage

- **`Fish Audio API key missing`** : définissez `FISH_API_KEY` ou `tts.providers.fish-audio.apiKey`.
- **HTTP 401** : vérifiez la clé API sur Fish Audio.
- **HTTP 402** : le modèle hébergé sélectionné nécessite des crédits disponibles ou un accès au plan.
- **Le modèle local revient à la voix système** : confirmez Apple silicon, l'espace disque libre et l'identifiant exact du modèle Hugging Face.
- **Le clone local ne correspond pas** : utilisez l'audio monolocuteur propre et assurez-vous que `referenceText` correspond exactement.

Consultez l'[API TTS Fish Audio](https://docs.fish.audio/features/text-to-speech)
et la [licence de recherche Fish Audio](https://huggingface.co/fishaudio/s2-pro/blob/main/LICENSE.md).
