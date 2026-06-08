---
title: "Voice and realtime talk - Voice Wake and Routing Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice and realtime talk - Voice Wake and Routing Maturity Note

## Résumé

Voice Wake et push-to-talk sont adjacents à Talk car ils déclenchent et acheminent la capture vocale vers les applications locales et les commandes Gateway. La couverture est au niveau bêta dans la documentation, la configuration Gateway, la source runtime native et les tests de plateforme. La qualité reste Alpha car les preuves d'archive incluent des défaillances de réveil, des rapports de crash obsolètes, des pinwheels de superposition et un comportement de délai d'inactivité en attente.

## Portée de la catégorie

Inclus dans cette catégorie :

- Paramètres de mot de réveil : paramètres de mot de réveil et préférences d'acheminement appartenant à Gateway.
- Acheminement du réveil : méthodes d'acheminement par défaut, vers l'application la plus récemment utilisée, vers l'application locale et vers un nœud spécifique.
- Runtime Voice Wake macOS : runtime Voice Wake macOS, touche de raccourci push-to-talk, adoption de superposition, comportement de pause/reprise et transfert.
- Préférences de réveil mobile : préférences de réveil iOS et Android et extraction de commandes.

## Fonctionnalités

- Paramètres de mot de réveil : paramètres de mot de réveil et préférences d'acheminement appartenant à Gateway.
- Acheminement du réveil : méthodes d'acheminement par défaut, vers l'application la plus récemment utilisée, vers l'application locale et vers un nœud spécifique.
- Runtime Voice Wake macOS : runtime Voice Wake macOS, touche de raccourci push-to-talk, adoption de superposition, comportement de pause/reprise et transfert.
- Préférences de réveil mobile : préférences de réveil iOS et Android et extraction de commandes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`

Le composant dispose de documentation dédiée, de méthodes Gateway, d'un runtime macOS natif, de gestionnaires de préférences iOS/Android et d'un large ensemble de tests de plateforme. La couverture n'est pas stable car la fiabilité du réveil nécessite des permissions OS réelles, de l'audio, du focus et un comportement de superposition.

## Score de qualité

- Score : `Alpha (66%)`

La qualité s'est améliorée grâce à l'état appartenant à Gateway, l'acheminement explicite, le renforcement du cycle de vie de la superposition et le comportement de pause/reprise du push-to-talk. Elle reste Alpha car la fiabilité du réveil dans le monde réel et le comportement de la superposition ont échoué à plusieurs reprises dans les preuves d'archive.

Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux runtime réel.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les paramètres de mot de réveil, l'acheminement du réveil, le runtime Voice Wake macOS et les préférences de réveil mobile.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le délai d'inactivité de Voice Wake et la désactivation automatique sont toujours suivis.
- Voice Wake macOS a des preuves de défaillance ouvertes et obsolètes.
- Le cycle de vie de la superposition et le comportement des permissions restent sensibles à l'opérateur.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/nodes/voicewake.md:9` documente les mots de réveil appartenant à Gateway, les bascules natives et le comportement du microphone désactivé/manuel Android.
- `/Users/kevinlin/code/openclaw/docs/nodes/voicewake.md:28` documente `voicewake.get`, `voicewake.set`, les méthodes d'acheminement et les événements de diffusion.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/voicewake.md:12` documente les modes de mot de réveil et push-to-talk, le délai de pause, l'arrêt dur, la superposition et le comportement de redémarrage.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/voice-overlay.md:14` documente l'adoption de superposition, les jetons par capture, l'envoi unifié et la journalisation.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/voicewake.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/voicewake-routing.ts`
- `/Users/kevinlin/code/openclaw/src/infra/voicewake.ts`
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/VoiceWakeRuntime.swift:10` implémente l'écouteur de réveil en arrière-plan.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/VoicePushToTalk.swift:146` gère le début du push-to-talk, les permissions, l'adoption de superposition et la pause du runtime de réveil.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice/VoiceWakeManager.swift`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/voice/VoiceWakeManager.kt`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-talk-nodes.test.ts`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoiceWakeRuntimeTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoicePushToTalkTests.swift`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoiceWakeForwarderTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoiceWakeGlobalSettingsSyncTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoiceWakeHelpersTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoiceWakeOverlayControllerTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/VoiceWakeOverlayTests.swift`
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/VoiceTests/VoiceWakeGatewaySyncTests.swift`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/VoiceWakeManagerTest.kt`

### Requêtes Gitcrawl

- `gitcrawl search issues "voice wake" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #46844 pour le délai d'inactivité du mode Talk/désactivation automatique, #87140 pour le backend STT Push-to-Talk macOS, #43480 pour un pinwheel VoiceWakeOverlay et les éléments de réveil associés.
- `gitcrawl search issues "macOS Talk voice wake push to talk" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #87140.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "voice wake push to talk" --limit 5` a retourné #34912 preuves de crash obsolètes/fermées pour Voice Wake/Push-to-Talk/Talk Mode, #64986 preuves ouvertes pour la défaillance de Voice Wake du compagnon macOS malgré les permissions et les notes de planification de version pour séparer le push-to-talk et le voice wake macOS du travail vocal plus large.
