---
title: "Voice et conversation en temps réel - Note de maturité de la transcription et de la parole"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice et conversation en temps réel - Note de maturité de la transcription et de la parole

## Résumé

La transcription vocale, les directives vocales JSON et `talk.speak` forment le chemin vocal non-duplex complet qui prend en charge Talk natif et la sortie audio de secours. La couverture est au niveau bêta car la documentation, les méthodes Gateway, la source de relais de transcription, les ponts de transcription des fournisseurs, les analyseurs natifs et les tests existent. La qualité reste Alpha car la configuration de transcription Talk dédiée n'est pas complètement séparée et la gestion des paramètres du fournisseur vocal a régressé auparavant.

## Portée de la catégorie

Inclus dans cette catégorie :

- Directives vocales : Directives vocales et suppression de directives avant la lecture TTS.
- Lecture de parole Talk : Comportement de `talk.speak` Gateway et comportement TTS de secours.
- Sessions de relais de transcription : Sessions de relais de transcription Gateway, événements de transcription et comportement de nettoyage.
- Fournisseurs de transcription en temps réel : Sélection du fournisseur de transcription en temps réel, diagnostics et comportement de pont spécifique au fournisseur.
- Analyse native de directives : Analyse native de directives et comportement de locale de parole Talk

## Fonctionnalités

- Directives vocales : Directives vocales et suppression de directives avant la lecture TTS.
- Lecture de parole Talk : Comportement de `talk.speak` Gateway et comportement TTS de secours.
- Sessions de relais de transcription : Sessions de relais de transcription Gateway, événements de transcription et comportement de nettoyage.
- Fournisseurs de transcription en temps réel : Sélection du fournisseur de transcription en temps réel, diagnostics et comportement de pont spécifique au fournisseur.
- Analyse native de directives : Analyse native de directives et comportement de locale de parole Talk

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (72%)`

La documentation et la source couvrent les directives, `talk.speak`, les sessions de transcription et les ponts de transcription des fournisseurs. La couverture n'est pas stable car la transcription Talk partage toujours la lignée de configuration avec les paramètres du fournisseur Voice Call.

## Score de qualité

- Score : `Alpha (68%)`

La qualité est améliorée par les directives vocales structurées, la suppression de directives avant TTS, l'abstraction du fournisseur et le comportement de secours. Elle reste Alpha car la configuration de transcription Talk est toujours partiellement empruntée, et l'archive montre des défaillances antérieures de sélection vocale dans Talk natif.

Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel.

## Score de complétude

- Score : `Bêta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : la documentation archivée, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les directives vocales, la lecture de parole Talk, les sessions de relais de transcription, les fournisseurs de transcription en temps réel, l'analyse native de directives.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La configuration de transcription Talk dédiée n'est pas complètement séparée de la configuration du fournisseur de streaming Voice Call.
- Les paramètres vocaux spécifiques au fournisseur ont régressé auparavant.
- Les requêtes d'archive `talk.speak` avaient des résultats directs clairsemés, ce qui rend l'historique de l'opérateur plus difficile à évaluer.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:40` documente les directives vocales JSON, les clés prises en charge et la suppression de directives avant TTS.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:117` documente la découverte du fournisseur de transcription en temps réel et la note actuelle selon laquelle la transcription emprunte le fournisseur de streaming Voice Call jusqu'à ce qu'une configuration Talk dédiée existe.
- `/Users/kevinlin/code/openclaw/docs/providers/openai.md:708` documente les paramètres OpenAI liés à la voix en temps réel et à la transcription.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:335` documente le comportement du fournisseur de voix en temps réel Google.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.ts:87` construit la configuration TTS Talk utilisée par `talk.speak`.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-session.ts:130` crée des sessions de relais en temps réel et de transcription.
- `/Users/kevinlin/code/openclaw/src/gateway/talk-transcription-relay.ts` implémente le relais de transcription Gateway.
- `/Users/kevinlin/code/openclaw/src/realtime-transcription/websocket-session.ts:103` gère le comportement de connexion WebSocket de transcription en temps réel et d'envoi audio.
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-transcription-provider.ts:182` résout l'authentification OpenAI et la gestion des sessions de transcription.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/TalkDirectiveParserTest.kt` couvre le comportement d'analyse native de directives.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/talk-transcription-relay.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-transcription-provider.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/realtime-transcription/websocket-session.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/deepgram/realtime-transcription-provider.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/elevenlabs/realtime-transcription-provider.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/mistral/realtime-transcription-provider.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/xai/realtime-transcription-provider.test.ts`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/TalkSpeakClientTest.kt`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/TalkDirectiveParserTest.kt`

### Requêtes Gitcrawl

- `gitcrawl search issues "talk.speak voice directive" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` n'a retourné aucune correspondance directe.
- `gitcrawl search issues "talk provider voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #86180 pour le comportement du paramètre de voix ElevenLabs TTS et les problèmes de fournisseur/voix connexes.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "talk.speak voice directive" --limit 5` a retourné la preuve #65661 fixed-on-main que macOS Talk Mode lit maintenant `talk.config` résolu et réessaie Gateway `talk.speak` avant le secours système.
- `/Users/kevinlin/.local/bin/discrawl search "OpenAI Realtime Talk Google Live" --limit 5` a retourné les notes de version indiquant que les erreurs en temps réel apparaissent dans Talk et que l'audio local survit à la livraison Telegram.
