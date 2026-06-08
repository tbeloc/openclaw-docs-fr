---
title: "iOS app - Voice Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Voice Maturity Note

## Résumé

iOS dispose d'une pile vocale réelle mais hautement expérimentale : mode Talk, commandes de nœud push-to-talk, reconnaissance vocale, synchronisation de la configuration Talk de la passerelle, mots-clés de déclenchement de réveil vocal, sessions de relais Gateway en temps réel, lecture TTS locale et suppression du microphone entre Talk, réveil et capture de clip caméra. La couverture reste Expérimentale car aucune fiche de score vocale au niveau de l'appareil n'a été trouvée pour les permissions de microphone, la mise en arrière-plan, l'audio de relais, le barge-in et le basculement de fournisseur. La qualité est Expérimentale car le code traite de nombreuses préoccupations de robustesse, mais la documentation et les archives encadrent toujours la voix comme étant au premier plan et sensible aux limites audio d'iOS.

## Portée de la catégorie

Inclus dans cette catégorie :

- Réveil vocal : réveil vocal, synchronisation des mots-clés de déclenchement, mode Talk, commandes push-to-talk, relais Gateway en temps réel, permissions de parole et de microphone, coordination de session audio, suspension en arrière-plan et paramètres vocaux

## Fonctionnalités

- Réveil vocal : réveil vocal, synchronisation des mots-clés de déclenchement, mode Talk, commandes push-to-talk, relais Gateway en temps réel, permissions de parole et de microphone, coordination de session audio, suspension en arrière-plan et paramètres vocaux

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (38%)`
- Signaux positifs : la documentation décrit la disponibilité de Talk et du réveil vocal ; la source implémente les chemins natifs et de relais ; les tests unitaires couvrent l'analyse de la configuration, les préférences de réveil vocal, l'analyse de synchronisation de la passerelle et certains comportements d'état de relais en temps réel.
- Signaux négatifs : aucun artefact e2e vocal iOS sur appareil réel n'a été trouvé pour les invites de permission de microphone, l'autorisation Speech, les trames audio de relais en temps réel, le basculement TTS, les transitions au premier plan/arrière-plan et la livraison du déclenchement du mot de réveil.
- Lacunes d'intégration : besoin d'une fiche de score vocale d'appareil couvrant le démarrage/arrêt de Talk, PTT une fois/démarrage/arrêt/annulation, la distribution de commande de réveil vocal, la connexion de relais en temps réel, l'échec du fournisseur et la suspension/reprise en arrière-plan.

## Score de qualité

- Score : `Expérimental (43%)`
- Rapports Gitcrawl : `iOS voice wake talk` a retourné la PR #81402 pour le travail SQLite d'état d'exécution qui mentionne l'état voicewake, mais aucun résultat direct de bug vocal iOS. Les résultats plus larges de `iOS app` incluaient le problème #47584 pour l'intégration Siri App Intent et la PR #40877 pour les avertissements de thread principal CLLocationManager/SFSpeechRecognizer.
- Rapports Discrawl : `iOS voice wake talk microphone` a trouvé des conseils de support indiquant que le mode Talk est disponible sur les nœuds iOS et utilise le microphone plus TTS. Une note de support d'application iOS de février indique que la voix bidirectionnelle et les mains libres sont prises en charge via le mode Talk plus Voice Wake, mais restent au premier plan car la suspension audio/socket en arrière-plan est une limitation réelle.
- Bonnes qualités : Talk et wake coordonnent la propriété du microphone, Talk supprime le réveil vocal pendant le push-to-talk, les trames de relais en temps réel sont limitées, le rapport de réveil vocal du simulateur est non pris en charge, et la configuration Talk de la passerelle est synchronisée.
- Mauvaises qualités : le succès vocal dépend du comportement au premier plan/session audio d'iOS, de la configuration du fournisseur, de la disponibilité de Speech et des invites de permission utilisateur ; la documentation décrit la fonctionnalité comme étant au mieux effort en dehors de l'utilisation active au premier plan.
- Exclu de la qualité : les tests unitaires pour la configuration et l'état de relais n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Expérimental (38%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le réveil vocal.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des fiches de score Talk/réveil vocal sur appareil réel avec des preuves de latence, arrière-plan, focus audio et échec du fournisseur.
- Documenter le comportement exact pour le maintien actif en arrière-plan de Talk, la suppression du réveil et la contention du microphone.
- Clarifier Siri/App Intent comme travail futur plutôt que support actuel.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente le réveil vocal, le mode Talk, les commandes PTT et le comportement d'arrière-plan au mieux effort.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` indique que Talk et Voice Wake fonctionnent mais restent au premier plan et approximatifs.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md` documente le comportement adjacent du nœud Talk.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice/TalkModeManager.swift` implémente l'état du mode Talk, la configuration de la passerelle, PTT, TTS, la capture vocale et la suspension en arrière-plan.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice/VoiceWakeManager.swift` implémente les mots-clés de déclenchement, la reconnaissance vocale, la gestion des permissions de microphone et la suppression.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice/RealtimeTalkRelaySession.swift` crée des sessions de relais Gateway et diffuse les trames audio PCM.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Settings/VoiceWakeWordsSettingsView.swift` expose les paramètres des mots-clés de déclenchement.

### Tests d'intégration

- Aucun artefact e2e vocal/Talk iOS sur appareil réel automatisé n'a été trouvé.
- Des tests de relais Talk côté passerelle existent en dehors de la surface de l'application iOS, mais ils ne prouvent pas le chemin microphone/audio de l'application iOS.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/TalkModeConfigParsingTests.swift`, `TalkModeIncrementalSpeechBufferTests.swift`, `TalkSpeechLocaleTests.swift` et `RealtimeTalkRelaySessionTests.swift` couvrent la logique Talk locale.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/VoiceWakeManagerStateTests.swift`, `VoiceWakeManagerExtractCommandTests.swift`, `VoiceWakeGatewaySyncTests.swift` et `VoiceWakePreferencesTests.swift` couvrent les paramètres et l'analyse du réveil.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iOS voice wake talk" --json`

Résultats :

- PR #81402 `refactor: move runtime state to SQLite`, avec l'état voicewake mentionné dans l'inventaire d'état.

Contexte de requête supplémentaire :

- `gitcrawl search openclaw/openclaw --query "iOS app" --json` a trouvé le problème #47584 pour le support Siri App Intent et la PR #40877 pour les corrections d'avertissement de thread principal SFSpeechRecognizer.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS voice wake talk microphone"`

Résultats :

- La note de support de janvier répertorie le mode Talk comme disponible sur le nœud iOS avec microphone et TTS, plus la détection du réveil vocal.
- La note de support d'application iOS de février indique que la voix bidirectionnelle est prise en charge via le mode Talk plus Voice Wake, mais reste au premier plan car la suspension audio/socket en arrière-plan d'iOS reste une limitation.
