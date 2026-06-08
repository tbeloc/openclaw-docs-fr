---
title: "Voice et conversation en temps réel - Note de maturité Native App Talk"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice et conversation en temps réel - Note de maturité Native App Talk

## Résumé

Native Talk existe sur macOS, iOS, Android et analyse partagée OpenClawKit. La couverture est Alpha car chaque plateforme dispose de sources significatives et de tests, mais la preuve de parité en temps réel inter-appareils et la parité sont inégales. La qualité est Alpha car le comportement côté opérateur diffère encore selon la plateforme, avec la parité macOS de la parole en temps réel et les limitations de réveil/micro manuel Android visibles dans la documentation et les preuves d'archive.

## Portée de la catégorie

Inclus dans cette catégorie :

- Mode Talk natif macOS : mode Talk natif macOS, reconnaissance vocale, lecture TTS et transfert push-to-talk
- Mode Talk iOS : mode Talk iOS, sessions WebRTC, sessions de relais en temps réel et préférences de réveil
- Mode Talk Android : mode Talk Android, mode reconnaissance vocale, relais en temps réel, capture micro et récepteur E2E de débogage
- Configuration Talk partagée : configuration Talk partagée et analyse de commandes

## Fonctionnalités

- Mode Talk natif macOS : mode Talk natif macOS, reconnaissance vocale, lecture TTS et transfert push-to-talk
- Mode Talk iOS : mode Talk iOS, sessions WebRTC, sessions de relais en temps réel et préférences de réveil
- Mode Talk Android : mode Talk Android, mode reconnaissance vocale, relais en temps réel, capture micro et récepteur E2E de débogage
- Configuration Talk partagée : configuration Talk partagée et analyse de commandes

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`

La source native et la preuve au niveau unitaire de la plateforme sont larges, et Android dispose d'un récepteur/script E2E de débogage. La couverture reste Alpha car le comportement natif en temps réel n'est pas aussi uniformément documenté ou testé en direct que le comportement du relais navigateur/Gateway.

## Score de qualité

- Score : `Alpha (64%)`

La qualité est améliorée par les portes de permission, la gestion du silence, la lecture de secours, l'analyse de configuration partagée et les gestionnaires de session spécifiques à la plateforme. Elle reste Alpha car la documentation et l'archive montrent des lacunes de parité entre les plates-formes, le réveil Android désactivé/manuel, l'historique de secours spécifique au fournisseur et le travail ouvert macOS de parole en temps réel.

Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : la documentation archivée, la source, le test, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le mode Talk natif macOS, le mode Talk iOS, le mode Talk Android, la configuration Talk partagée.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La parité macOS OpenAI de la parole en temps réel reste ouverte.
- Le réveil vocal Android est documenté comme désactivé/micro manuel.
- Le comportement du fournisseur natif n'est pas encore aussi cohésif que les chemins de relais navigateur/Gateway.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:9` documente les formes de runtime Talk STT/TTS natives macOS/iOS/Android.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:126` documente le comportement Talk natif macOS et Android, les permissions, le secours, `talk.speak`, MLX, la validation du niveau de latence et les formats PCM Android.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/voicewake.md:39` documente le comportement de la touche de raccourci push-to-talk macOS et le transfert vers les commandes Gateway.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/TalkModeRuntime.swift:9` implémente le runtime du mode Talk macOS, la reconnaissance vocale, la gestion du silence et la lecture.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/VoicePushToTalk.swift:39` implémente la touche de raccourci push-to-talk et le transfert de superposition.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice/TalkModeManager.swift:31` implémente l'état Talk iOS et la sélection du fournisseur.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice/RealtimeTalkRelaySession.swift:154` démarre les sessions de relais Talk en temps réel iOS via Gateway `talk.session.create`.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice/TalkRealtimeWebRTCSession.swift:78` démarre les sessions Talk WebRTC iOS.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/voice/TalkModeManager.kt:90` implémente l'état du mode Talk Android, le chemin de reconnaissance vocale et l'état de la session en temps réel.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/voice/MicCaptureManager.kt:270` gère les événements Talk, les événements de chat, la lecture de réponse de l'assistant et les sessions de transcription.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawKit/TalkCommands.swift:3` définit les noms de commandes Talk partagées.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/apps/android/app/src/debug/java/ai/openclaw/app/VoiceE2eReceiver.kt`
- `/Users/kevinlin/code/openclaw/apps/android/scripts/voice-e2e.sh`
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/VoiceTests/RealtimeTalkRelaySessionTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/TalkModeRuntimeSpeechTests.swift`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/TalkAudioPlayerTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/TalkModeGatewayConfigTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoicePushToTalkTests.swift`
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/VoiceTests/TalkModeIncrementalSpeechBufferTests.swift`
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/VoiceTests/TalkSpeechLocaleTests.swift`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/TalkAudioPlayerTest.kt`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/TalkDirectiveParserTest.kt`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/MicCaptureManagerTest.kt`

### Requêtes Gitcrawl

- `gitcrawl search issues "talk realtime voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #71195 pour la parité macOS OpenAI de la parole en temps réel, #85275 pour l'inadéquation de la sortie parlée et les problèmes connexes de fournisseur/configuration.
- `gitcrawl search issues "macOS Talk voice wake push to talk" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #87140 pour le backend STT enfichable pour macOS Push-to-Talk.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "talk realtime voice" --limit 5` a retourné les notes de version du 2026-05-27 indiquant que les exécutions Talk et voice peuvent être inspectées, dirigées, annulées et suivies.
- `/Users/kevinlin/.local/bin/discrawl search "Android realtime voice e2e relay path" --limit 5` n'a retourné aucun résultat direct.
- `/Users/kevinlin/.local/bin/discrawl search "talk.speak voice directive" --limit 5` a retourné la preuve #65661 fixed-on-main pour le comportement de secours vocal configuré macOS.
