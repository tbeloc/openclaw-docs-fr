---
title: "Canal Voice Call - Note de maturité Transcription en continu et Réponse automatique"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Canal Voice Call - Note de maturité Transcription en continu et Réponse automatique

## Résumé

Cette note migre les preuves de maturité archivées pour `Canal Voice Call` / `Transcription en continu et Réponse automatique` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité du canal Voice Call représentée par ces fonctionnalités de taxonomie :

- Canal Voice Call : Transcription en continu et Réponse automatique

## Fonctionnalités

- Canal Voice Call : Transcription en continu et Réponse automatique

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (47%)`

La transcription en continu dispose de documentation, de configuration, de code runtime de flux médias, de plomberie STT générique pour les fournisseurs, de mise en mémoire tampon des médias précoces, de gestion de la disponibilité de la transcription, d'événements Talk et d'intégration de réponse automatique. Elle reste Expérimentale car les preuves ne montrent pas une couverture stable des appels téléphoniques en direct sur les fournisseurs STT, et les preuves archivées incluent des notes d'opérateur où l'état de configuration/redémarrage a affecté la validation du flux médias Twilio en direct.

## Score de qualité

- Score : `Alpha (55%)`

La qualité est basée sur la conception du cycle de vie du flux médias, la configuration générique pour les fournisseurs, le comportement en cas d'échec et l'état archivé. L'existence des tests et l'étendue des tests n'ont pas été comptabilisées dans ce score de qualité.

La conception gère la disponibilité de la connexion au fournisseur, les médias précoces, les limites de file d'attente, les événements de rappel et la fermeture en cas d'échec. La qualité reste Alpha car la disponibilité du fournisseur, l'application de redémarrage de la passerelle, la disponibilité STT et la latence de réponse automatique restent opérationnellement fragiles.

## Score de complétude

- Score : `Expérimental (47%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le canal Voice Call.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune matrice de fournisseur STT en direct actuelle n'a été trouvée pour Deepgram, ElevenLabs, Mistral, OpenAI et xAI dans les appels téléphoniques réels.
- L'état d'application de redémarrage/configuration de la passerelle peut rendre la validation du flux médias en direct trompeuse.
- La latence de réponse automatique et le comportement du chemin de parole Telnyx ont des preuves de problèmes ouverts.

## Preuves

### Documentation

- `docs/plugins/voice-call.md:367-377` documente la transcription en continu avec Deepgram, ElevenLabs, Mistral, OpenAI et xAI ; l'audio entrant en file d'attente pendant que le fournisseur se connecte ; et le comportement de salutation après la disponibilité de la transcription.
- `docs/plugins/voice-call.md:379-445` documente les exemples de fournisseur en continu.
- `docs/plugins/voice-call.md:620-636` documente le contrat JSON de sortie parlée et l'extraction défensive.
- `docs/plugins/voice-call.md:638-647` documente le comportement au démarrage, l'état de lecture initial, le comportement de nouvelle tentative, le démarrage du flux Twilio et l'effacement de l'interruption.

### Source

- `extensions/voice-call/src/config.ts:653-717` normalise la configuration du fournisseur en continu et les paramètres du chemin du flux médias.
- `extensions/voice-call/src/webhook.ts:327-504` initialise les rappels du fournisseur de flux médias en continu et connecte les événements de flux aux métadonnées d'appel.
- `extensions/voice-call/src/media-stream.ts:136-285` implémente l'état MediaStreamHandler, la gestion de la mise à niveau WebSocket, les charges utiles maximales, les limites de connexion en attente, la gestion des messages médias Twilio et le transfert STT.
- `extensions/voice-call/src/media-stream.ts:327-455` crée des sessions de transcription, émet des événements Talk, connecte les fournisseurs de transcription et ferme en cas d'échec de disponibilité.
- `extensions/voice-call/src/media-stream.ts:484-660` implémente les limites/délais d'attente, la contre-pression du tampon d'envoi, l'envoi audio, la gestion des marques et le comportement d'effacement.
- `extensions/voice-call/src/media-stream.ts:670-830` implémente la TTS en file d'attente et l'observabilité Talk.

### Tests d'intégration

- `extensions/voice-call/src/webhook.test.ts:211-256` vérifie la sélection automatique du premier fournisseur de transcription en temps réel et la présence de MediaStreamHandler.
- `extensions/voice-call/src/webhook.test.ts:258-316` enregistre les événements Talk du flux médias sur les métadonnées d'appel.
- `extensions/voice-call/src/webhook.test.ts:1562-1650` vérifie la grâce de déconnexion du flux et le déclenchement de la disponibilité de la transcription pour les messages initiaux.
- `extensions/voice-call/src/media-stream.test.ts:706-771` reporte la disponibilité de la transcription jusqu'à la connexion STT.
- `extensions/voice-call/src/media-stream.test.ts:773-855` transfère les médias Twilio précoces avant la disponibilité.
- `extensions/voice-call/src/media-stream.test.ts:857-916` ferme en cas d'échec de disponibilité STT.

### Tests unitaires

- `extensions/voice-call/src/config.test.ts:399-545` couvre les valeurs par défaut en continu, le comportement du chemin personnalisé et les interactions de configuration TTS/temps réel associées.
- `extensions/voice-call/src/media-stream.test.ts:185-215` couvre l'enveloppe JSON malformée et le comportement de démarrage des événements Talk.
- `extensions/voice-call/src/media-stream.test.ts:918-925` protège les cadres de pré-démarrage surdimensionnés.

### Requêtes Gitcrawl

- `gitcrawl search issues "voice-call streaming transcription" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #79121 pour le moissonneur Twilio obsolète, #79118 pour la parole entrante Telnyx ne répondant pas automatiquement, #79521 pour la compaction post-tour retardant la réponse vocale et #73019 pour la proposition de fournisseur de voix en temps réel xAI.
- `gitcrawl search issues "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #77957 pour les appels entrants persistant la transcription sans notification utilisateur et #85848 pour l'écrêtage audio mu-law Twilio.
- `gitcrawl search prs "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #84161 pour la persistance de la transcription de l'assistant sur les événements de parole d'appel et #75018/#73032 pour le travail du fournisseur de parole en temps réel.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call streaming transcription"` : a retourné des notes de responsable/archive sur la STT en continu générique pour les fournisseurs, le support de transcription en continu ElevenLabs/xAI, une configuration Twilio en direct où la transcription en continu était activée mais nécessitait un redémarrage de la passerelle pour s'appliquer, et des conseils de configuration distinguant la gestion régulière des webhooks/TTS de la STT du flux médias.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call twilio telnyx plivo"` : a retourné des conseils selon lesquels la transcription en continu est particulièrement pertinente pour le mode conversation et pas toujours requise pour les tests de notification simples.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "google meet twilio voice-call"` : a retourné des notes en direct où la configuration en continu était définie mais la passerelle en cours d'exécution ne l'avait pas encore appliquée en raison de l'état de redémarrage différé.

### Snapshot source archivé

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
