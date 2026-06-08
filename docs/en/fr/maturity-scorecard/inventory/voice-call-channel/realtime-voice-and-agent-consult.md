---
title: "Canal Voice Call - Note de maturité Voice et Calls en temps réel"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Canal Voice Call - Note de maturité Voice et Calls en temps réel

## Résumé

Cette note migre les preuves de maturité archivées pour le `canal Voice Call` / `Voice en temps réel et Agent Consult` dans l'inventaire de scorecard actuel de la version-3 du processus.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Realtime Voice and Calls`
- Fusionnée à partir de : `Realtime and Streaming Conversation`, `Telephony Providers and Media`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Canal Voice Call : Voice en temps réel et Agent Consult
- Canal Voice Call : Transcription en streaming et Auto-réponse
- Canal Voice Call : Transports de fournisseur et contrôle d'appel
- Canal Voice Call : Telephony TTS, Playback, DTMF et Audio
- Canal Voice Call : CLI, Gateway RPC et Agent Tool

## Fonctionnalités

- Canal Voice Call : Voice en temps réel et Agent Consult
- Canal Voice Call : Transcription en streaming et Auto-réponse

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (44%)`

La voice en temps réel dispose de preuves d'implémentation significatives pour les flux médias Twilio, les fournisseurs en temps réel OpenAI/Google, les jetons de flux, le pontage WebSocket, le contexte d'agent, le contexte rapide, les outils de consult, la gestion native des appels d'outils et le barge-in. Elle reste Experimental car les preuves d'archive d'appels en direct sont dominées par les défauts ouverts et le travail de contribution plutôt que par la preuve de scénario stable.

## Score de qualité

- Score : `Alpha (55%)`

La qualité est basée sur la structure d'exécution en temps réel, la conception des jetons/ponts, les contrôles de politique d'outils, les limites de support des fournisseurs et l'état actif des problèmes/PR. L'existence des tests et l'étendue des tests n'ont pas été comptabilisées dans ce score de qualité.

Le composant dispose de pièces architecturales solides, notamment les jetons par appel, le cycle de vie du pont, le rythme audio/la contre-pression, la politique de consult, le contexte rapide et la déduplication des consults forcés/natifs. Il n'est pas plus élevé car l'archive active montre des salutations doubles, des coupures audio, une latence au premier tour, des lacunes de liaison d'outils en temps réel, le durcissement du chemin de flux et des lacunes de parité des fournisseurs.

## Score de complétude

- Score : `Experimental (44%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Voice Call Channel, Voice Call Channel.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version-3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les preuves en temps réel en direct sont toujours dominées par les défauts ouverts et les PR de suivi.
- La parité en temps réel bidirectionnelle de Telnyx n'est pas établie par les preuves actuelles.
- La liaison d'outils et la latence de consult sont des préoccupations actives pour les appels téléphoniques en direct.

## Preuves

### Docs

- `docs/plugins/voice-call.md:214-236` documente la voice en temps réel, l'exclusion mutuelle streaming/temps réel, le support Twilio Media Streams, la configuration optionnelle du fournisseur en temps réel, les fournisseurs Google/OpenAI, les outils de consult, la politique de consult, le contexte d'agent, le contexte rapide et le comportement lorsque la configuration du fournisseur en temps réel est manquante.
- `docs/plugins/voice-call.md:238-254` documente la politique d'outils en temps réel et la politique de consult.
- `docs/plugins/voice-call.md:256-365` documente le contexte de voice d'agent et les exemples de fournisseur en temps réel Google/OpenAI.
- `docs/plugins/voice-call.md:638-647` indique que le temps réel possède le tour d'ouverture et que le barge-in efface les entrées en attente.

### Source

- `extensions/voice-call/src/config.ts:653-717` normalise la configuration du fournisseur en temps réel, le chemin de flux, les paramètres de consult et le contexte d'agent.
- `extensions/voice-call/src/config.ts:793-883` valide les paramètres en temps réel et empêche les combinaisons incompatibles temps réel/streaming.
- `extensions/voice-call/src/runtime.ts:380-465` câble les outils de consult en temps réel, la politique de lecture sécurisée uniquement, les métadonnées de clé de transcript/session et les métadonnées générées par.
- `extensions/voice-call/src/webhook/realtime-handler.ts:288-510` implémente les jetons de flux, la génération TwiML, la gestion de la mise à niveau, l'analyse des trames, les ponts actifs et le comportement issue-stream-token.
- `extensions/voice-call/src/webhook/realtime-handler.ts:620-900` implémente le rythme audio/la contre-pression, les sessions de pont, les récepteurs, les transcripts au gestionnaire, les appels d'outils, le barge-in, les erreurs et la gestion de la fermeture.
- `extensions/voice-call/src/webhook/realtime-handler.ts:1029-1325` implémente le comportement de consult forcé, l'enregistrement/fin d'appel, la déduplication de consult natif/forcé et les réponses de travail.

### Tests d'intégration

- `extensions/voice-call/src/runtime.test.ts:380-465` couvre le câblage des outils de consult en temps réel, la politique d'outils de lecture sécurisée uniquement, les métadonnées de clé de transcript/session et les métadonnées générées par.
- `extensions/voice-call/src/runtime.test.ts:467-516` couvre les clés de session par appel pour les consults en temps réel.
- `extensions/voice-call/src/runtime.test.ts:518-587` couvre les réponses de contexte de mémoire rapide avant le consult d'agent intégré.
- `extensions/voice-call/src/webhook.test.ts:972-1031` couvre les webhooks Twilio en temps réel relus ne frappant pas l'état du flux.
- `extensions/voice-call/src/webhook.test.ts:1033-1096` vérifie que le TwiML du fournisseur initial est servi avant le comportement de raccourci en temps réel.
- `extensions/voice-call/src/webhook.test.ts:1098-1200` couvre le rejet et l'acceptation de la liste blanche en temps réel.

### Tests unitaires

- `extensions/voice-call/src/config.test.ts:32-279` couvre l'exclusion mutuelle en temps réel et les restrictions de fournisseur.
- `extensions/voice-call/src/config.test.ts:399-545` couvre le chemin de flux en temps réel personnalisé et les paramètres en temps réel.
- `extensions/voice-call/src/providers/twilio.test.ts:110-260` couvre le TwiML en streaming et le comportement de l'URL de conversation utilisés par la configuration du flux en temps réel.

### Requêtes Gitcrawl

- `gitcrawl search issues "voice-call realtime twilio media stream" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #85847 pour la latence au premier tour du timing WebSocket du fournisseur en temps réel, #85848 pour la coupure audio en temps réel OpenAI, #79121 pour le reaper obsolète pendant les conversations Twilio, #80841 pour le changement de mode AMD/dynamique et #59245 pour les appels de tâches sortantes.
- `gitcrawl search issues "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #85846 pour la salutation double en temps réel OpenAI, #79918 pour les mises à niveau du chemin de flux frère, #79055 pour le préchargement du contexte avant réponse, #80840 pour les outils en temps réel annoncés sans liaison de gestionnaire et #78190 pour la voice en temps réel par agent.
- `gitcrawl search prs "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #86285, #86502 et #85932 pour les correctifs de salutation double ; #75592 pour le contexte d'appelant en temps réel ; #79919 pour le durcissement du chemin de flux ; et #79572 pour les correctifs de paramètre FunctionDeclaration en temps réel.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call realtime twilio"` : a retourné une discussion selon laquelle Twilio dispose du support Media Streams/WebSocket en temps réel, le streaming bidirectionnel Telnyx était toujours un travail de contribution, des notes de configuration en direct où le temps réel était désactivé et des commentaires sur les problèmes/PR concernant les consults lents/fragiles et les flux sortants en temps réel.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call twilio telnyx plivo"` : a retourné des preuves d'examen selon lesquelles le mode en temps réel avait besoin d'une gestion rapide des défaillances sur les chemins de fournisseur où il ne ferait rien silencieusement.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "google meet twilio voice-call"` : a retourné des notes de version/responsable selon lesquelles les chemins de voice en temps réel sont devenus plus débogables tandis que l'état Google Meet/Twilio voice-call avait toujours besoin de soins.

### Snapshot de source archivée

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
