---
title: "macOS companion app - Voice and Talk Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# macOS companion app - Voice and Talk Maturity Note

## Résumé

L'application macOS dispose de surfaces vocales véritablement natives : détecteur de mot de réveil, hotkey push-to-talk, overlay, boucle Talk Mode, planification de secours STT/TTS, transfert vocal vers la session/canal sélectionné, et mises à jour de l'état talk-mode de la passerelle. La couverture est Beta à la limite inférieure car les chemins d'exécution natifs couvrent le réveil, PTT, le transfert et Talk Mode avec preuve unitaire de support, mais aucun scénario de latence/mode de défaillance/audio en direct n'a été trouvé. La qualité est Alpha car la surface évolue rapidement et les preuves d'archive montrent un historique de plantages, une rotation de routage et des demandes de fonctionnalités ouvertes.

## Portée de la catégorie

Inclus dans cette catégorie :

- Exécution Voice Wake : exécution Voice Wake, détection de déclenchement, autorisations, overlay, carillons et transfert
- Push-to-talk : cycle de capture/écoute/réflexion/parole Push-to-talk et Talk Mode
- Plan de lecture du fournisseur Talk : plan de lecture du fournisseur Talk et état talk de la passerelle

## Fonctionnalités

- Exécution Voice Wake : exécution Voice Wake, détection de déclenchement, autorisations, overlay, carillons et transfert
- Push-to-talk : cycle de capture/écoute/réflexion/parole Push-to-talk et Talk Mode
- Plan de lecture du fournisseur Talk : plan de lecture du fournisseur Talk et état talk de la passerelle

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`
- Signaux positifs : La documentation couvre le mot de réveil, le push-to-talk, le comportement d'exécution, les invariants d'overlay, les paramètres et le transfert. La source implémente l'exécution de la reconnaissance vocale, la coordination d'overlay, le transfert de session sélectionnée, l'exécution Talk, le secours du fournisseur et les mises à jour de l'état de la passerelle. Les tests couvrent l'analyse/gating du mot de réveil, la synchronisation des paramètres globaux, le contrôleur/vue d'overlay, le push-to-talk, l'analyse de la configuration Talk, les plans de lecture et les valeurs par défaut des demandes vocales.
- Signaux négatifs : Les tests ne sont pas des scénarios de latence/mode de défaillance d'audio en direct. Aucune preuve de smoke test de version n'a été trouvée pour les autorisations de microphone, le déclenchement de réveil, l'audio de réponse Talk Mode, l'interruption et le transfert en mode distant ensemble.
- Lacunes d'intégration : Besoin d'un scénario vocal d'application signée reproductible avec autorisations mic/speech, mot de réveil, push-to-talk, Talk Mode, secours de défaillance du fournisseur, transfert en mode distant et latence/classification de défaillance enregistrées.

## Score de qualité

- Score : `Alpha (63%)`
- Rapports Gitcrawl : Les résultats incluent le problème #46844 pour le délai d'inactivité Talk Mode après Voice Wake, le problème #87140 pour le backend STT Push-to-Talk enfichable macOS, le problème #63531 pour le MVP du fournisseur Talk MLX et le problème #70266 pour le support d'avatar d'overlay Talk.
- Rapports Discrawl : L'archive inclut #41603 remplacé par l'architecture de routage voicewake actuelle, #34912/#34903 historique de plantages autour de Voice Wake/Talk overlay, et explication communautaire que macOS est le client Talk Mode complet tandis qu'Android/iOS ont des surfaces vocales plus faibles/limitées en distribution.
- Bonnes qualités : L'exécution évite de capturer l'audio au lancement, gère l'entrée par défaut manquante, suit les délais d'attente, contrôle les autorisations, met en pause le réveil pendant le push-to-talk/Talk, et achemine la livraison de transcription via le contexte de session actif.
- Mauvaises qualités : La surface dépend des autorisations de parole/mic du système d'exploitation, des appareils audio, de l'état d'overlay, des identifiants du fournisseur, des hotkeys natifs et de la livraison de canal. L'historique d'archive montre des plantages et des demandes UX/fournisseur/routage actives.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'exécution Voice Wake, Push-to-talk, le plan de lecture du fournisseur Talk.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin de fiches de latence, mode de défaillance et configuration avant promotion au-delà de la limite Beta/Alpha.
- Besoin de preuve en direct pour le rejet/reprise d'overlay, les conflits PTT et l'interruption Talk sur les appareils audio réels.
- Besoin d'une orientation d'opérateur plus claire pour les défaillances de secours du fournisseur et de transfert vocal en mode distant.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/voicewake.md` documente le mode mot de réveil, push-to-talk, le comportement d'exécution, les invariants d'overlay, les paramètres, le transfert et la vérification rapide.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/voice-overlay.md` documente le comportement d'overlay.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md` documente le comportement Talk partagé.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` répertorie les fonctionnalités de l'application liées à voice wake et Talk.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/VoiceWakeRuntime.swift` implémente la reconnaissance du mot de réveil, le gating de déclenchement, le cycle de vie du moteur audio, les mises à jour d'overlay, les délais d'attente et le comportement de redémarrage.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/VoiceWakeForwarder.swift` achemine les transcriptions vers la session/canal sélectionné et préfixe le contexte machine.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/TalkModeRuntime.swift` implémente la capture Talk, la reconnaissance, le plan de lecture du fournisseur, la gestion du silence et le secours.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/TalkModeController.swift` coordonne l'overlay, la pause, la désactivation PTT, les mises à jour du talk-mode de la passerelle et la reprise.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/VoicePushToTalk*.swift` implémente les chemins de capture/hotkey push-to-talk.

### Tests d'intégration

- Aucun scénario d'intégration d'exécution audio/Talk en direct n'a été trouvé.
- Des tests vocaux/temps réel adjacents existent sous `/Users/kevinlin/code/openclaw/extensions/*/src/*voice*.test.ts`, mais ceux-ci ne prouvent pas la boucle d'application native macOS.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/VoiceWakeRuntimeTests.swift` couvre la correspondance de déclenchement, l'élagage, le gating d'écart et les formes multilingues/insensibles à la largeur.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/VoiceWakeForwarderTests.swift`, `VoiceWakeGlobalSettingsSyncTests.swift`, `VoiceWakeOverlayControllerTests.swift`, `VoiceWakeOverlayTests.swift` et `VoiceWakeTesterTests.swift` couvrent les aides vocales natives.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/VoicePushToTalkTests.swift` et `VoicePushToTalkHotkeyTests.swift` couvrent le comportement PTT.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/TalkModeRuntimeSpeechTests.swift`, `TalkModeConfigParsingTests.swift` et `TalkModeGatewayConfigTests.swift` couvrent la logique d'analyse/lecture Talk.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS voice wake talk mode" --json`

Résultats :

- Problème #46844 `Talk Mode Idle Timeout / Auto-Deactivation After Voice Wake`.
- Problème #87140 `Pluggable STT backend for macOS Push-to-Talk`.

Contexte de requête macOS supplémentaire :

- Problème #63531 `Add MLX Talk provider MVP for local macOS TTS`.
- Problème #70266 `Use assistant avatar in macOS Talk Mode overlay`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS voice wake"`

Résultats :

- 2026-04-26 Miroir GitHub : #41603 PR de routage voicewake remplacée par l'architecture de routage actuelle.
- 2026-04-20 Miroir GitHub : #34912/#34903 rapports de plantage autour de Voice Wake / Push-to-Talk / Talk Mode overlay ont été fermés en raison de l'inactivité.
- 2026-04-18 Message de support distingue macOS comme le client Talk Mode complet et note la parité vocale Android/iOS plus faible.
