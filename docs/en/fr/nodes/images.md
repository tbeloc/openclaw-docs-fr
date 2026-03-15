---
summary: "Règles de gestion des images et médias pour les réponses d'envoi, de passerelle et d'agent"
read_when:
  - Modifying media pipeline or attachments
title: "Support des images et médias"
---

# Support des images et médias — 2025-12-05

Le canal WhatsApp s'exécute via **Baileys Web**. Ce document capture les règles actuelles de gestion des médias pour les réponses d'envoi, de passerelle et d'agent.

## Objectifs

- Envoyer des médias avec des légendes optionnelles via `openclaw message send --media`.
- Permettre aux réponses automatiques de la boîte de réception web d'inclure des médias aux côtés du texte.
- Maintenir des limites par type sensées et prévisibles.

## Surface CLI

- `openclaw message send --media <path-or-url> [--message <caption>]`
  - `--media` optionnel ; la légende peut être vide pour les envois de médias uniquement.
  - `--dry-run` affiche la charge utile résolue ; `--json` émet `{ channel, to, messageId, mediaUrl, caption }`.

## Comportement du canal WhatsApp Web

- Entrée : chemin de fichier local **ou** URL HTTP(S).
- Flux : charger dans un Buffer, détecter le type de média et construire la charge utile correcte :
  - **Images :** redimensionner et recompresser en JPEG (côté max 2048px) ciblant `agents.defaults.mediaMaxMb` (par défaut 5 MB), plafonné à 6 MB.
  - **Audio/Voix/Vidéo :** passage direct jusqu'à 16 MB ; l'audio est envoyé comme une note vocale (`ptt: true`).
  - **Documents :** tout le reste, jusqu'à 100 MB, avec le nom de fichier préservé si disponible.
- Lecture de style GIF WhatsApp : envoyer un MP4 avec `gifPlayback: true` (CLI : `--gif-playback`) pour que les clients mobiles boucle en ligne.
- Détection MIME préfère les octets magiques, puis les en-têtes, puis l'extension de fichier.
- La légende provient de `--message` ou `reply.text` ; une légende vide est autorisée.
- Journalisation : non-verbose affiche `↩️`/`✅` ; verbose inclut la taille et le chemin/URL source.

## Pipeline de réponse automatique

- `getReplyFromConfig` retourne `{ text?, mediaUrl?, mediaUrls? }`.
- Quand un média est présent, l'expéditeur web résout les chemins locaux ou les URL en utilisant le même pipeline que `openclaw message send`.
- Les entrées de médias multiples sont envoyées séquentiellement si fournies.

## Médias entrants vers les commandes (Pi)

- Quand les messages web entrants incluent des médias, OpenClaw télécharge vers un fichier temporaire et expose les variables de modèle :
  - `{{MediaUrl}}` pseudo-URL pour le média entrant.
  - `{{MediaPath}}` chemin temporaire local écrit avant d'exécuter la commande.
- Quand un bac à sable Docker par session est activé, les médias entrants sont copiés dans l'espace de travail du bac à sable et `MediaPath`/`MediaUrl` sont réécrits en un chemin relatif comme `media/inbound/<filename>`.
- La compréhension des médias (si configurée via `tools.media.*` ou `tools.media.models` partagé) s'exécute avant le modèle et peut insérer des blocs `[Image]`, `[Audio]` et `[Video]` dans `Body`.
  - L'audio définit `{{Transcript}}` et utilise la transcription pour l'analyse des commandes afin que les commandes slash fonctionnent toujours.
  - Les descriptions vidéo et image préservent tout texte de légende pour l'analyse des commandes.
- Par défaut, seule la première pièce jointe image/audio/vidéo correspondante est traitée ; définissez `tools.media.<cap>.attachments` pour traiter plusieurs pièces jointes.

## Limites et erreurs

**Plafonds d'envoi sortant (envoi web WhatsApp)**

- Images : plafond ~6 MB après recompression.
- Audio/voix/vidéo : plafond 16 MB ; documents : plafond 100 MB.
- Médias surdimensionnés ou illisibles → erreur claire dans les journaux et la réponse est ignorée.

**Plafonds de compréhension des médias (transcription/description)**

- Image par défaut : 10 MB (`tools.media.image.maxBytes`).
- Audio par défaut : 20 MB (`tools.media.audio.maxBytes`).
- Vidéo par défaut : 50 MB (`tools.media.video.maxBytes`).
- Les médias surdimensionnés ignorent la compréhension, mais les réponses continuent avec le corps original.

## Notes pour les tests

- Couvrir les flux d'envoi + réponse pour les cas image/audio/document.
- Valider la recompression pour les images (limite de taille) et le drapeau de note vocale pour l'audio.
- Assurer que les réponses multi-médias se déploient comme des envois séquentiels.
