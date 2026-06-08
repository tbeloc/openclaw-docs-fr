---
title: "Android app - Voice Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Android app - Voice Maturity Note

## Résumé

Android voice a dépassé le stade de placeholder : l'application expose la dictée manuelle au micro et l'interface utilisateur Talk Mode, la synthèse Gateway `talk.speak` avec secours local, le câblage du relais en temps réel, le changement de type de microphone du service de premier plan, les scripts e2e vocaux et la couverture unitaire ciblée. La couverture est Alpha car l'artefact e2e le plus solide est un chemin de script de débogage plutôt qu'un flux d'installation utilisateur répété. La qualité est Alpha car l'archive enregistre le churn vocal, une boucle de thrashing micro antérieure et des demandes non résolues concernant le changement d'agent/session et la voix TTS par agent.

## Portée de la catégorie

Inclus dans cette catégorie :

- Onglet Voice : Onglet Voice, capture manuelle au micro, boucle Talk Mode listen/think/speak, configuration Gateway Talk, talk.speak, mode relais en temps réel, type de service de capture vocale et récepteur/script e2e vocal

## Fonctionnalités

- Onglet Voice : Onglet Voice, capture manuelle au micro, boucle Talk Mode listen/think/speak, configuration Gateway Talk, talk.speak, mode relais en temps réel, type de service de capture vocale et récepteur/script e2e vocal

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (66%)`
- Signaux positifs : La documentation décrit les modes de capture manuelle au micro et Talk, les exigences de microphone du service de premier plan Android 14+, Gateway `talk.speak`, le secours TTS local, les conditions de relais Gateway en temps réel et Voice Wake désactivé dans l'UX/runtime. Le script e2e vocal de débogage peut exécuter les chemins vocaux normaux et en temps réel via une application de débogage installée.
- Signaux négatifs : La preuve vocale dépend de la configuration du récepteur/script de débogage et des transcriptions synthétiques ; aucune latence audio sur appareil réel récurrente, permission de microphone, défaillance du reconnaisseur vocal, secours du fournisseur et scénario de premier plan/arrière-plan n'a été trouvé.
- Lacunes d'intégration : Besoin d'une fiche d'évaluation vocale d'application signée qui accorde la permission de microphone, exécute la capture manuelle au micro et Talk Mode, exerce le secours `talk.speak`, vérifie le relais en temps réel lorsqu'il est configuré, met l'application en arrière-plan/la réouvre et enregistre les classifications de défaillance.

## Score de qualité

- Score : `Alpha (60%)`
- Rapports Gitcrawl : `Android Talk Mode` a trouvé le problème #56613 demandant le changement d'agent Voice/Talk tab et la voix TTS par agent, plus PR #80082 ajustant l'utilisation du service de premier plan Android pour Talk Mode. La recherche `Android app` expose également le contexte plus large de reconstruction/publication d'application.
- Rapports Discrawl : La recherche a trouvé un commentaire PR fusionné pour #66179 exposant Talk Mode dans l'interface utilisateur et la permission de microphone de premier plan ; un commentaire fermant #47883 après remplacement d'une boucle de thrashing micro par le nouveau chemin manuelle au micro ; et un message d'assistance notant le comportement vocal partiel Android antérieur et le churn voice-wake/talk-mode.
- Bonnes qualités : La source actuelle sépare la capture manuelle au micro de Talk Mode, vérifie la permission de microphone, gère la disponibilité du reconnaisseur vocal, suit l'état d'écoute/parole, met en pause la capture pendant TTS et bascule de Gateway `talk.speak` lorsqu'il est admissible.
- Mauvaises qualités : Le comportement vocal est limité par la disponibilité du reconnaisseur vocal Android, le focus audio, la politique du service de premier plan, la configuration du fournisseur et le routage de session. Les demandes des utilisateurs pour le changement d'agent/session de l'onglet Talk restent ouvertes.
- Exclu de la qualité : La couverture des tests et la preuve du flux runtime n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (66%)`
- Instructions de surface : évaluées par rapport à `references/completeness/android-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'onglet Voice.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des fiches d'évaluation audio et de défaillance du fournisseur sur appareil réel pour la capture manuelle au micro et Talk Mode.
- Ajouter la sélection de session/agent de l'onglet Voice si Android est censé correspondre aux contrôles de session Chat.
- Maintenir la documentation alignée avec l'état réel de Voice Wake ; la documentation actuelle indique correctement que Voice Wake Android reste désactivé.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` documente la capture manuelle au Mic, Talk Mode continu, comportement du microphone du service de premier plan, Gateway `talk.speak`, secours TTS local, conditions de relais en temps réel et Voice Wake désactivé.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` répertorie la fonctionnalité complète de l'onglet Voice dans la liste de contrôle de reconstruction et documente le script `voice-e2e.sh`.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md` est la référence de comportement Talk partagée.

### Source

- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/VoiceScreen.kt` expose la dictée manuelle et l'interface utilisateur Talk, les invites de permission, le basculement du haut-parleur, l'état et le rendu de la transcription.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/voice/MicCaptureManager.kt` implémente la transcription manuelle au micro, la mise en file d'attente, l'envoi Gateway, la pause/reprise TTS et le délai d'expiration de l'exécution en attente.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/voice/TalkModeManager.kt` implémente l'écoute Talk Mode, le cycle de vie du reconnaisseur vocal, la finalisation du chat, le relais en temps réel, la lecture audio et les contrôles d'interruption.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/voice/TalkSpeakClient.kt` appelle Gateway `talk.speak` et classe le secours local.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/NodeForegroundService.kt` promeut Talk Mode à `dataSync|microphone`.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/debug/java/ai/openclaw/app/VoiceE2eReceiver.kt` supporte l'orchestration e2e vocale de débogage.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/apps/android/scripts/voice-e2e.sh` installe l'application de débogage, accorde `RECORD_AUDIO`, utilise `adb reverse`, pilote les modes vocaux normaux et en temps réel via `VoiceE2eReceiver`, capture des captures d'écran et enregistre le logcat filtré.
- Aucun scénario vocal de construction Play signée répété n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/MicCaptureManagerTest.kt`, `TalkModeManagerTest.kt`, `TalkSpeakClientTest.kt`, `TalkAudioPlayerTest.kt`, `TalkDirectiveParserTest.kt`, `TalkModeConfigParsingTest.kt`, `VoiceWakeCommandExtractorTest.kt`, `VoiceWakeManagerTest.kt` et `ChatEventTextTest.kt` couvrent les aides vocales principales.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/NodeForegroundServiceTest.kt` couvre le comportement du type de service de premier plan.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Android Talk Mode" --json`

Résultats :

- Problème #56613 `[Feature]: Talk/Voice tab - agent/session switching + per-agent TTS voice`.
- PR #80082 `fix(android): avoid dataSync FGS for persistent node`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android Talk Mode Voice tab"`

Résultats :

- 2026-04-25 Commentaire du miroir GitHub sur #66179 indiquant que l'interface utilisateur Android Talk Mode et la permission de microphone de premier plan ont été fusionnées.
- 2026-04-25 Commentaire du miroir GitHub sur #47883 indiquant que la boucle de thrashing micro antérieure a été remplacée par l'onglet Voice manuel soutenu par `MicCaptureManager`.
- 2026-03-28 Problème du miroir GitHub #56613 demandant le changement d'agent Voice/Talk tab et la voix TTS par agent.
