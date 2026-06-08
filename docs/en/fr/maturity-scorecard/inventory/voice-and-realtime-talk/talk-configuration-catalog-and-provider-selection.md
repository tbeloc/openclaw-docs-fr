---
title: "Voice et conversation en temps réel - Note de Maturité des Fournisseurs de Talk"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice et conversation en temps réel - Note de Maturité des Fournisseurs de Talk

## Résumé

La surface de configuration Talk dispose de documentation réelle, d'un catalogue Gateway, d'un code de registre/résolveur de fournisseur, de vérifications de portée de secret et d'analyseurs natifs partagés. La couverture est au niveau bêta. La qualité est au niveau bêta mais reste limitée par les bogues de configuration vocale spécifiques aux fournisseurs et la sémantique inégale des fournisseurs dans l'archive.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Pont de backend OpenAI Realtime voice : Pont de backend OpenAI Realtime voice et chemin de credential WebRTC du navigateur
- Pont de backend Google Gemini Live : Pont de backend Google Gemini Live et chemin token/WebSocket du navigateur
- Contrats SDK de fournisseur de voix en temps réel : Contrats SDK de fournisseur de voix en temps réel, métadonnées d'activation, registre de fournisseur et résolveur
- Diagnostics de fournisseur : Diagnostics de fournisseur, comportement de reconnexion, déclarations d'outils et cycle de vie de session de pont
- Catalogue Talk : Découverte du catalogue Talk pour les fournisseurs de transport, cerveau, parole, voix en temps réel et transcription.
- Configuration du fournisseur Talk : Sélection du fournisseur Talk, paramètres de temps réel spécifiques au fournisseur et règles d'exposition de secret.
- Analyse de configuration native partagée : Analyse de configuration native partagée pour macOS, iOS et Android

## Fonctionnalités

- Pont de backend OpenAI Realtime voice : Pont de backend OpenAI Realtime voice et chemin de credential WebRTC du navigateur
- Pont de backend Google Gemini Live : Pont de backend Google Gemini Live et chemin token/WebSocket du navigateur
- Contrats SDK de fournisseur de voix en temps réel : Contrats SDK de fournisseur de voix en temps réel, métadonnées d'activation, registre de fournisseur et résolveur
- Diagnostics de fournisseur : Diagnostics de fournisseur, comportement de reconnexion, déclarations d'outils et cycle de vie de session de pont
- Catalogue Talk : Découverte du catalogue Talk pour les fournisseurs de transport, cerveau, parole, voix en temps réel et transcription.
- Configuration du fournisseur Talk : Sélection du fournisseur Talk, paramètres de temps réel spécifiques au fournisseur et règles d'exposition de secret.
- Analyse de configuration native partagée : Analyse de configuration native partagée pour macOS, iOS et Android

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Bêta (78%)`

Le composant est couvert dans la documentation, la source Gateway, l'analyse native partagée, les tests du résolveur de fournisseur et les tests de méthode serveur. La couverture n'est pas stable car le comportement de configuration spécifique au fournisseur et la parité entre fournisseurs restent des sujets actifs de l'archive.

## Score de Qualité

- Score : `Bêta (74%)`

La qualité est déterminée par la forme de configuration explicite, la découverte du catalogue, la gestion des secrets consciente de la portée, la normalisation des fournisseurs et la réutilisation des analyseurs natifs/partagés. Le risque de qualité persiste autour des paramètres vocaux spécifiques au fournisseur, de la prolifération des fournisseurs et des différences d'exécution entre les clients navigateur, relais Gateway et clients natifs.

Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel.

## Score de Complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : la documentation archivée, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le pont de backend OpenAI Realtime voice, le pont de backend Google Gemini Live, les contrats SDK de fournisseur de voix en temps réel, les diagnostics de fournisseur, le catalogue Talk, la configuration du fournisseur Talk, l'analyse de configuration native partagée.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- `talk.provider` et `talk.realtime.provider` sont documentés, mais le comportement vocal spécifique au fournisseur a régressé auparavant.
- Le catalogue a de nombreux axes, ce qui augmente la complexité de configuration de l'opérateur.
- Les nouvelles demandes de fournisseur, y compris ElevenLabs realtime, Azure Foundry, xAI et MLX local, restent actives ou proposées.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:64` documente `talk.provider`, les cartes de fournisseur, le fournisseur en temps réel, le modèle, la voix, le transport, le cerveau et la configuration de consultation.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:112` documente `talk.catalog`, la découverte de fournisseur, les fournisseurs de transcription, les formats de sortie et la locale.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:185` documente la configuration du mode Talk, l'authentification, les secrets éphémères, les options de mode et l'utilisation de smoke en direct.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.ts:87` résout la configuration Talk TTS active.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.ts:161` construit le catalogue Talk sur les modes, transports, cerveaux, fournisseurs de parole, fournisseurs de voix en temps réel et fournisseurs de transcription.
- `/Users/kevinlin/code/openclaw/src/talk/provider-resolver.ts:23` résout les fournisseurs de voix en temps réel configurés et lève les erreurs de fournisseur manquant.
- `/Users/kevinlin/code/openclaw/src/talk/provider-registry.ts:19` répertorie et canonicalise les enregistrements de fournisseur de voix en temps réel.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawKit/TalkConfigParsing.swift:20` analyse la configuration du fournisseur sélectionné et les charges utiles Talk résolues pour les applications natives.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server.talk-config.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/protocol/talk-config.contract.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-talk-nodes.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/talk/provider-resolver.test.ts`
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/VoiceTests/TalkConfigParsingTests.swift`
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawTests/TalkModeConfigParsingTests.swift`
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/voice/TalkModeManagerTest.kt`

### Requêtes Gitcrawl

- `gitcrawl search issues "talk provider voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné les threads de configuration de fournisseur et voix incluant #71195, #86180, #86434, #63531, #84639, #80010, #86425, #76952, #85275 et #87140.
- `gitcrawl search issues "talk realtime voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné les problèmes ouverts de temps réel/fournisseur/configuration incluant #71195, #86434, #76952, #84639, #86425, #84664, #85275, #83822, #87325 et #87140.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "talk provider voice" --limit 5` a retourné les notes de version du 2026-05-27 disant que Talk et voice sont plus faciles à contrôler, inspecter, diriger, annuler et suivre à partir de l'interface Web et de la voix Discord.
- `/Users/kevinlin/.local/bin/discrawl search "talk.speak voice directive" --limit 5` a retourné un commentaire d'archive GitHub pour #65661 notant que le correctif de sélection de voix ElevenLabs du mode Talk macOS lit maintenant `talk.config` résolu et réessaie le `talk.speak` Gateway avant le secours système.
