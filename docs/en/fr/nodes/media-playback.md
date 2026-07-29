---
summary: "Lecture audio et vidéo en ligne dans l'interface de contrôle et les applications natives"
read_when:
  - Playing or troubleshooting audio and video attachments in chat
  - Comparing media format support across OpenClaw clients
  - Debugging playback metadata, transcoding, or codec availability
title: "Lecture de médias"
---

Les clients de chat OpenClaw lisent les pièces jointes audio et vidéo de l'assistant en ligne. La passerelle conserve ces pièces jointes derrière un accès limité à la session, sert des plages d'octets consultables et peut préparer un rendu de lecture portable pour les formats reconnus qui ne sont pas sûrs sur tous les clients.

Cette page couvre la lecture dans les clients OpenClaw. La livraison par canal, la compréhension des médias entrants et les conversations vocales en direct utilisent des chemins distincts ; voir [Support des images et des médias](/fr/nodes/images), [Compréhension des médias](/fr/nodes/media-understanding) et [Mode conversation](/fr/nodes/talk).

## Support des clients

| Client          | Chemin de lecture                                   | Notes de l'opérateur                                                                                                                                                                                                                                                                          |
| --------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Interface de contrôle      | Cartes audio à thème et contrôles vidéo natifs | Les cartes audio fournissent lecture/pause, recherche, temps écoulé et total, téléchargement, un badge de note vocale et des contrôles clavier. L'espace bascule la lecture ; Gauche/Droite recherche par cinq secondes. Le démarrage d'une carte audio met en pause la précédente. Le téléchargement vidéo est disponible à partir du sélecteur de pièces jointes de chat. |
| iOS et macOS   | `AVAudioPlayer` pour l'audio et `AVPlayer` pour la vidéo  | Les médias en ligne se coordonnent avec Talk et Listen pour que deux chemins de parole ne se jouent pas l'un sur l'autre. Pour une passerelle TLS épinglée, l'application effectue un téléchargement authentifié limité avant la lecture vidéo au lieu de contourner l'épinglage de certificat.                                              |
| Android         | Media3 ExoPlayer                                    | L'application diffuse la vidéo via le client HTTP de la passerelle authentifiée, demande la mise au point audio Android et coordonne la lecture des pièces jointes avec Talk/TTS. Les lignes de médias de transcription en cache restent visibles hors ligne, mais la lecture nécessite une connexion pour obtenir un nouveau ticket de média.              |
| Compagnon Linux | Interface de contrôle dans le WebView du compagnon             | La disponibilité des codecs provient de GStreamer. Les packages publiés incluent ou déclarent les plugins de codec attendus ; voir [Codecs médias Linux](/fr/platforms/linux#media-codecs).                                                                                                                                      |

## Formats portables

La passerelle classe ces formats comme l'ensemble natif portable partagé par le navigateur, les lecteurs Apple et Android Media3 :

| Type  | Entrée native portable                                                                   | Entrée de transcodage reconnue                                         | Cible de lecture                                          |
| ----- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------- |
| Audio | MP3 ; AAC en M4A/MP4 ; PCM WAV                                                            | AAC, AIFF, AMR/AMR-WB, CAF, FLAC, Ogg/Opus/Vorbis, WebM audio, WMA | AAC en M4A (`audio/mp4`)                                 |
| Vidéo | H.264 MP4 avec un profil portable et format de pixel 4:2:0 ; audio AAC ou MP3 si présent | AVI, FLV, Matroska/MKV, QuickTime/MOV, WebM, ASF, WMV              | H.264/AAC MP4 avec format de pixel 4:2:0, au maximum 1920×1080 |

Le compagnon Linux peut également lire les formats fournis par ses plugins GStreamer installés. Les mises à jour du navigateur et du système d'exploitation peuvent ajouter des formats natifs, mais le tableau ci-dessus est le contrat inter-clients qu'OpenClaw cible.

## Rendus de lecture paresseux

Les deux routes d'octets de la passerelle acceptent `?playback=1` : la route de pièce jointe gérée sous `/api/chat/media/outgoing/.../full` et la route de média assistant de l'interface de contrôle. Les métadonnées de pièce jointe peuvent signaler `playback: "native"` ou `playback: "transcode"` pour qu'un client puisse choisir délibérément le rendu.

La conversion de lecture est paresseuse :

1. Une source native passe inchangée.
2. Une source non portable reconnue démarre un travail `ffmpeg` limité. La route retourne HTTP `202` avec `{ "status": "preparing" }` pendant que le rendu est préparé.
3. Une demande ultérieure reçoit le rendu M4A ou MP4 en cache.
4. Si l'inspection ou la conversion n'est pas disponible, échoue ou dépasse une limite, la route revient aux octets d'origine. Le client peut alors afficher son fallback de média non lisible et garder l'action de téléchargement disponible.

Le transcodage accepte les sources jusqu'à 20 minutes et ne relève jamais le plafond d'octets audio ou vidéo normal. Les rendus de lecture en cache sont élagués par la maintenance normale du magasin de médias.

## Pièces jointes gérées et accès

L'audio et la vidéo produits par l'agent sont stockés en tant qu'artefacts de médias gérés. Les images conservent leur famille d'artefacts d'image gérée distincte. Les clients natifs résolvent l'artefact via `artifacts.download`, qui retourne des octets base64 en ligne lorsque l'artefact est sauvegardé en octets ou une URL courte durée avec ticket lorsqu'il est géré par la passerelle.

Les routes d'octets avec ticket supportent :

- Les demandes `Range` avec HTTP `206 Partial Content` pour la recherche
- `ETag` et `If-Range` pour un comportement de reprise sûr
- Les demandes `HEAD` avec les mêmes métadonnées de contenu et aucun corps de réponse

Ne copiez pas une URL avec ticket dans une configuration durable. Les clients réacquièrent un ticket auprès de la passerelle authentifiée lorsque nécessaire.

## Métadonnées et limites

Les pièces jointes de chat peuvent inclure `sizeBytes`, `durationMs`, `width` et `height`. OpenClaw utilise également `ffprobe`, lorsqu'il est disponible, pour remplir la durée audio et la durée/dimensions vidéo pour les faits médias et la sonde de disponibilité `?meta=1` de l'interface de contrôle. Le sondage est au mieux : une sonde manquante ou échouée laisse les champs absents au lieu de rejeter la pièce jointe.

Les pièces jointes d'assistant gérées par la passerelle utilisent ces plafonds par fichier :

| Type  | Taille maximale |
| ----- | -----------: |
| Image |       12 MiB |
| Audio |       16 MiB |
| Vidéo |       16 MiB |

Ce sont des plafonds de lecture/stockage, pas les limites de compréhension des médias distinctes. Pour les limites de transcription et de description, voir [Support des images et des médias](/fr/nodes/images#limits-and-errors).

## Dépannage

### La durée ou les dimensions sont manquantes

Vérifiez que `ffprobe` est installé sur l'hôte de la passerelle et visible sur son `PATH` :

```bash
ffprobe -version
```

La lecture d'un fichier déjà portable peut toujours fonctionner sans métadonnées.

### Un format reconnu se télécharge au lieu de se lire

Vérifiez les deux outils de médias sur l'hôte de la passerelle :

```bash
ffmpeg -version
ffprobe -version
```

`ffprobe` classe les codecs et la durée ; `ffmpeg` crée le rendu portable. Si l'une ou l'autre étape ne peut pas gérer en toute sécurité la source, OpenClaw sert le fichier d'origine et le client conserve son chemin de fallback/téléchargement.

### La lecture reste en état de préparation

La première demande de rendu est asynchrone. Attendez brièvement et réessayez. Les sources très volumineuses, plus longues que 20 minutes, non probables ou non supportées restent sur le fallback d'octets d'origine au lieu de bloquer la passerelle.

### Linux signale une erreur de codec

Utilisez les instructions de package et de construction à partir de la source dans [Codecs médias Linux](/fr/platforms/linux#media-codecs). Le `.deb` dépend des packages de plugins GStreamer requis ; l'AppImage porte le framework de médias et les codecs installés par la version de compilation.

### Android affiche une ligne de média hors ligne

C'est attendu. Android met en cache les métadonnées de transcription, pas les octets de pièce jointe ou sa capacité de téléchargement courte durée. Reconnectez-vous, puis lisez à nouveau pour que l'application puisse demander un nouveau ticket.

## Connexes

- [Support des images et des médias](/fr/nodes/images)
- [Audio et notes vocales](/fr/nodes/audio)
- [Aperçu des médias](/fr/tools/media-overview)
- [Synthèse vocale](/fr/tools/tts)
- [Application Linux](/fr/platforms/linux)
