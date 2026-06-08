---
title: "Long-tail hosted providers - Hosted Speech, Transcription, and Audio Providers Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Long-tail hosted providers - Hosted Speech, Transcription, and Audio Providers Maturity Note

## Résumé

Les fournisseurs de parole hébergée, de transcription et d'audio sont en Beta pour la couverture et en Alpha pour la qualité. ElevenLabs, Deepgram, Azure Speech, Gradium, Inworld, Volcengine, Vydra, MiniMax, Mistral, SenseAudio et xAI disposent de documentations significatives, de manifestes et de chemins en direct sélectionnés, mais le format audio, le protocole en temps réel, la téléphonie et les variations de région/compte maintiennent le score de qualité opérationnelle plus bas.

## Portée de la catégorie

Cette note couvre la synthèse vocale, la reconnaissance vocale, la transcription en temps réel, l'audio téléphonique, la sortie de notes vocales et les chemins de compréhension médias des fournisseurs d'audio hébergés.

Hors de portée : l'évaluation audio OpenAI propriétaire lorsqu'elle est évaluée séparément, le traitement audio local et la livraison audio spécifique aux canaux.

## Fonctionnalités

- Fournisseurs de synthèse vocale : Couvre les fournisseurs de synthèse vocale dans la synthèse vocale, la reconnaissance vocale, la transcription en temps réel, l'audio téléphonique et le comportement des fournisseurs de parole, transcription et audio hébergés associés.
- Fournisseurs de reconnaissance vocale : Couvre les fournisseurs de reconnaissance vocale dans la synthèse vocale, la reconnaissance vocale, la transcription en temps réel, l'audio téléphonique et le comportement des fournisseurs de parole, transcription et audio hébergés associés.
- Fournisseurs de transcription en temps réel : Couvre les fournisseurs de transcription en temps réel dans la synthèse vocale, la reconnaissance vocale, la transcription en temps réel, l'audio téléphonique et le comportement des fournisseurs de parole, transcription et audio hébergés associés.
- Diagnostics de format audio : Couvre les diagnostics de format audio dans la synthèse vocale, la reconnaissance vocale, la transcription en temps réel, l'audio téléphonique et le comportement des fournisseurs de parole, transcription et audio hébergés associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs :
  - Le répertoire des fournisseurs liste Azure Speech, Deepgram, ElevenLabs, Mistral, SenseAudio et les chemins audio/transcription xAI.
  - Les contrats de manifeste incluent les fournisseurs de parole et les fournisseurs de transcription en temps réel.
  - Les tests en direct ElevenLabs couvrent TTS, STT et STT en temps réel.
  - Les tests en direct Deepgram couvrent la transcription d'audio d'exemple et STT en temps réel.
  - Azure Speech, Inworld, Gradium, MiniMax, Volcengine, Vydra, Mistral et xAI disposent de preuves en direct ou source pour les chemins audio hébergés.
  - Les tests unitaires couvrent de nombreux contrats de parole/audio spécifiques aux fournisseurs.
- Signaux négatifs :
  - La preuve en direct est plus forte pour ElevenLabs, Deepgram, Azure Speech, Inworld, Gradium, MiniMax, Volcengine et Vydra que pour chaque fournisseur listé.
  - Le comportement audio varie selon les formats, les taux d'échantillonnage, les contraintes téléphoniques, les protocoles de streaming et les régions des fournisseurs.
  - Les recherches d'archive exactes pour la phrase audio-provider n'ont retourné aucun résultat direct.

## Score de qualité

- Score : `Alpha (66%)`
- Bonnes qualités :
  - Les contrats de fournisseur séparent les fournisseurs de parole, les fournisseurs de transcription en temps réel, les fournisseurs de compréhension médias et les métadonnées de fournisseur de génération.
  - Les implémentations de fournisseur exposent les formats de sortie concrets, les extensions de fichier, la compatibilité des notes vocales, l'audio téléphonique et le texte de transcription.
  - Plusieurs fournisseurs réutilisent les contrats partagés pour STT en temps réel et les entrées audio synthétisées.
- Mauvaises qualités :
  - Les intégrations audio ont une variance externe élevée dans la disponibilité du catalogue vocal, la région, le cycle de vie du flux, le support des codecs et les exigences de taux d'échantillonnage.
  - Certains fournisseurs nécessitent plusieurs identifiants pour synthétiser une entrée de test en temps réel ou sonder un chemin dépendant.
  - Le signal de support soutenu par archive est mince pour la phrase exacte du fournisseur audio hébergé.
- Exclus de la qualité :
  - Les preuves unitaires, d'intégration et en direct ont été utilisées uniquement pour le score de couverture.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/long-tail-hosted-providers.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les fournisseurs de synthèse vocale, les fournisseurs de reconnaissance vocale, les fournisseurs de transcription en temps réel, les diagnostics de format audio.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un tableau de couverture du mode/fournisseur audio couvrant TTS, STT, STT en temps réel, notes vocales, téléphonie, taux d'échantillonnage et format de sortie par fournisseur.
- Ajouter un test de fumée récurrent à faible coût pour un mode audio par fournisseur audio hébergé.
- Ajouter des diagnostics plus clairs orientés utilisateur pour les défaillances de format et de région.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/index.md:32` : le répertoire des fournisseurs lie Azure Speech.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:40` : le répertoire des fournisseurs lie ElevenLabs.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:65` : le répertoire des fournisseurs lie SenseAudio.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:87` : la liste des fournisseurs de transcription inclut Deepgram, ElevenLabs, Mistral, OpenAI, SenseAudio et xAI.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:630` : les contrats incluent `speechProviders` et `realtimeTranscriptionProviders`.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:658` : la référence de contrat définit `speechProviders`.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:659` : la référence de contrat définit `realtimeTranscriptionProviders`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/elevenlabs/openclaw.plugin.json:2` : le manifeste du fournisseur ElevenLabs existe.
- `/Users/kevinlin/code/openclaw/extensions/deepgram/openclaw.plugin.json:2` : le manifeste du fournisseur Deepgram existe.
- `/Users/kevinlin/code/openclaw/extensions/azure-speech/openclaw.plugin.json:2` : le manifeste du fournisseur Azure Speech existe.
- `/Users/kevinlin/code/openclaw/extensions/senseaudio/openclaw.plugin.json:2` : le manifeste du fournisseur SenseAudio existe.
- `/Users/kevinlin/code/openclaw/extensions/inworld/openclaw.plugin.json:2` : le manifeste du fournisseur Inworld existe.
- `/Users/kevinlin/code/openclaw/extensions/gradium/openclaw.plugin.json:2` : le manifeste du fournisseur Gradium existe.
- `/Users/kevinlin/code/openclaw/extensions/volcengine/openclaw.plugin.json:2` : le manifeste du fournisseur Volcengine existe.
- `/Users/kevinlin/code/openclaw/extensions/vydra/openclaw.plugin.json:2` : le manifeste du fournisseur Vydra existe.
- `/Users/kevinlin/code/openclaw/extensions/mistral/openclaw.plugin.json:2` : le manifeste du fournisseur Mistral inclut les métadonnées du fournisseur liées à l'audio.
- `/Users/kevinlin/code/openclaw/extensions/xai/openclaw.plugin.json:2` : le manifeste du fournisseur xAI inclut les chemins de parole/transcription.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/elevenlabs/elevenlabs.live.test.ts:27` : le test en direct ElevenLabs synthétise la parole via le fournisseur enregistré.
- `/Users/kevinlin/code/openclaw/extensions/elevenlabs/elevenlabs.live.test.ts:45` : le test en direct ElevenLabs transcrit la parole synthétisée via le fournisseur de médias.
- `/Users/kevinlin/code/openclaw/extensions/elevenlabs/elevenlabs.live.test.ts:67` : le test en direct ElevenLabs diffuse STT en temps réel via le fournisseur de transcription enregistré.
- `/Users/kevinlin/code/openclaw/extensions/deepgram/audio.live.test.ts:36` : le test en direct Deepgram transcrit l'audio d'exemple.
- `/Users/kevinlin/code/openclaw/extensions/deepgram/audio.live.test.ts:51` : le test en direct Deepgram diffuse STT en temps réel.
- `/Users/kevinlin/code/openclaw/extensions/azure-speech/azure-speech.live.test.ts:26` : le test en direct Azure Speech liste les voix via le fournisseur enregistré.
- `/Users/kevinlin/code/openclaw/extensions/azure-speech/azure-speech.live.test.ts:42` : le test en direct Azure Speech synthétise MP3, note vocale Ogg/Opus et audio téléphonique.
- `/Users/kevinlin/code/openclaw/extensions/inworld/inworld.live.test.ts:20` : le test en direct Inworld liste les voix.
- `/Users/kevinlin/code/openclaw/extensions/inworld/inworld.live.test.ts:33` : le test en direct Inworld synthétise MP3, note vocale Ogg/Opus et PCM téléphonique.
- `/Users/kevinlin/code/openclaw/extensions/gradium/gradium.live.test.ts:22` : le test en direct Gradium synthétise la parole via le fournisseur enregistré.
- `/Users/kevinlin/code/openclaw/extensions/minimax/minimax.live.test.ts:53` : le test en direct MiniMax synthétise TTS.
- `/Users/kevinlin/code/openclaw/extensions/vydra/vydra.live.test.ts:59` : le test en direct Vydra couvre la parole.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/elevenlabs/speech-provider.test.ts` : couverture unitaire du comportement du fournisseur de parole ElevenLabs.
- `/Users/kevinlin/code/openclaw/extensions/deepgram/audio.test.ts` : couverture unitaire de la transcription audio Deepgram.
- `/Users/kevinlin/code/openclaw/extensions/azure-speech/speech-provider.test.ts` : couverture unitaire du comportement du fournisseur de parole Azure Speech.
- `/Users/kevinlin/code/openclaw/extensions/senseaudio/media-understanding-provider.test.ts` : couverture unitaire du comportement du fournisseur de compréhension médias SenseAudio.
- `/Users/kevinlin/code/openclaw/extensions/inworld/speech-provider.test.ts` : couverture unitaire du comportement du fournisseur de parole Inworld.
- `/Users/kevinlin/code/openclaw/extensions/gradium/speech-provider.test.ts` : couverture unitaire du comportement du fournisseur de parole Gradium.
- `/Users/kevinlin/code/openclaw/extensions/volcengine/tts.test.ts` : couverture unitaire du comportement TTS Volcengine.
- `/Users/kevinlin/code/openclaw/extensions/vydra/speech-provider.test.ts` : couverture unitaire du comportement du fournisseur de parole Vydra.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "ElevenLabs Deepgram Azure Speech provider"` a retourné `[]`.
- `gitcrawl --json search prs -R openclaw/openclaw "ElevenLabs Deepgram Azure Speech provider"` a retourné `[]`.
- `gitcrawl --json search prs -R openclaw/openclaw "provider fallback error timeout auth missing model"` a retourné des modifications de fournisseur/runtime adjacentes incluant #81834, qui a ajouté le support du fournisseur TTS SenseAudio.

### Requêtes Discrawl

- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "ElevenLabs Deepgram Azure Speech provider" --limit 5` a retourné `null`.
- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "Qwen ZAI Moonshot MiniMax provider" --limit 5` a retourné un rapport de problème de voix/STT avec des clés de registre de fournisseur incluant Deepgram et MiniMax, plus une défaillance de paramètre de modèle STT.
- Ce faible taux de résultat d'archive directe est traité comme un signal d'archive faible plutôt que comme une preuve d'absence de problèmes.
