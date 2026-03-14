---
read_when:
  - 修改媒体管道或附件
summary: 发送、Gateway 网关和智能体回复的图像和媒体处理规则
title: 图像和媒体支持
x-i18n:
  generated_at: "2026-02-03T07:50:42Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 971aed398ea01078efbad7a8a4bca17f2a975222a2c4db557565e4334c9450e0
  source_path: nodes/images.md
  workflow: 15
---

# Support des images et des médias — 2025-12-05

Le canal WhatsApp s'exécute via **Baileys Web**. Cette documentation enregistre les règles actuelles de traitement des médias pour les envois, les passerelles et les réponses des agents.

## Objectifs

- Envoyer des médias avec une légende optionnelle via `openclaw message send --media`.
- Permettre aux réponses automatiques de la boîte de réception web d'inclure des médias à côté du texte.
- Maintenir les limites pour chaque type raisonnables et prévisibles.

## Interface CLI

- `openclaw message send --media <path-or-url> [--message <caption>]`
  - `--media` est optionnel ; la légende peut être vide pour un envoi de média pur.
  - `--dry-run` affiche la charge utile analysée ; `--json` génère `{ channel, to, messageId, mediaUrl, caption }`.

## Comportement du canal WhatsApp Web

- Entrée : chemin de fichier local **ou** URL HTTP(S).
- Flux : charger dans un Buffer, détecter le type de média et construire la charge utile correcte :
  - **Images :** redimensionner et récompresser en JPEG (côté max 2048px), cible `agents.defaults.mediaMaxMb` (par défaut 5 MB), limite 6 MB.
  - **Audio/Voix/Vidéo :** passage direct jusqu'à 16 MB ; l'audio est envoyé comme message vocal (`ptt: true`).
  - **Documents :** tout autre contenu, jusqu'à 100 MB, nom de fichier conservé si disponible.
- Lecture GIF style WhatsApp : envoyer MP4 avec `gifPlayback: true` (CLI : `--gif-playback`) pour que les clients mobiles le lisent en boucle en ligne.
- Détection MIME : priorité aux octets magiques, puis en-têtes, puis extension de fichier.
- Légende provenant de `--message` ou `reply.text` ; légende vide autorisée.
- Journalisation : mode non verbeux affiche `↩️`/`✅` ; mode verbeux inclut la taille et le chemin source/URL.

## Pipeline de réponse automatique

- `getReplyFromConfig` retourne `{ text?, mediaUrl?, mediaUrls? }`.
- Lorsque des médias sont présents, l'expéditeur web utilise le même pipeline que `openclaw message send` pour analyser les chemins locaux ou les URL.
- Si plusieurs entrées de médias sont fournies, elles sont envoyées séquentiellement.

## Médias entrants vers commandes (Pi)

- Lorsqu'un message web entrant contient des médias, OpenClaw télécharge dans un fichier temporaire et expose les variables de modèle :
  - `{{MediaUrl}}` pseudo-URL du média entrant.
  - `{{MediaPath}}` chemin temporaire local écrit avant l'exécution de la commande.
- Lorsque le bac à sable Docker par session est activé, les médias entrants sont copiés dans l'espace de travail du bac à sable, et `MediaPath`/`MediaUrl` sont réécrits en chemins relatifs comme `media/inbound/<filename>`.
- La compréhension des médias (si activée via `tools.media.*` ou configuration partagée `tools.media.models`) s'exécute avant le modèle, pouvant insérer des blocs `[Image]`, `[Audio]` et `[Video]` dans `Body`.
  - L'audio définit `{{Transcript}}` et utilise la transcription pour l'analyse des commandes, donc les commandes slash fonctionnent toujours.
  - Les descriptions vidéo et image conservent tout texte de légende pour l'analyse des commandes.
- Par défaut, seule la première pièce jointe image/audio/vidéo correspondante est traitée ; définir `tools.media.<cap>.attachments` pour traiter plusieurs pièces jointes.

## Limites et erreurs

**Limites d'envoi sortant (envoi WhatsApp Web)**

- Images : limite d'environ 6 MB après récompression.
- Audio/Voix/Vidéo : limite de 16 MB ; Documents : limite de 100 MB.
- Médias trop volumineux ou illisibles → erreur explicite dans les journaux, réponse ignorée.

**Limites de compréhension des médias (transcription/description)**

- Images par défaut : 10 MB (`tools.media.image.maxBytes`).
- Audio par défaut : 20 MB (`tools.media.audio.maxBytes`).
- Vidéo par défaut : 50 MB (`tools.media.video.maxBytes`).
- Les médias trop volumineux ignorent la compréhension, mais la réponse utilise toujours le corps original.

## Notes de test

- Couvrir les cas d'envoi + flux de réponse pour images/audio/documents.
- Vérifier la récompression des images (limites de taille) et le drapeau de message vocal pour l'audio.
- S'assurer que les réponses multi-médias sont envoyées en tant que fan-out séquentiel.
