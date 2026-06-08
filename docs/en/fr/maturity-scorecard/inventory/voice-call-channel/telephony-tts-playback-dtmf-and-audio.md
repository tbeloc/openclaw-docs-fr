---
title: "Canal Voice Call - Note de maturité Telephony TTS, Playback, DTMF et Audio"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Canal Voice Call - Note de maturité Telephony TTS, Playback, DTMF et Audio

## Résumé

Cette note migre les preuves de maturité archivées pour le `canal Voice Call` / `Telephony TTS, Playback, DTMF et Audio` dans l'inventaire de la fiche d'évaluation actuelle process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité du canal Voice Call représentée par ces fonctionnalités de taxonomie :

- Canal Voice Call : Telephony Tts, Playback, Dtmf, and Audio

## Fonctionnalités

- Canal Voice Call : Telephony Tts, Playback, Dtmf, and Audio

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (49%)`

Telephony TTS, playback, DTMF et audio disposent de preuves d'implémentation pour la fusion de configuration TTS de base, la synthèse téléphonique, la conversion PCM en mu-law, la lecture de médias Twilio, le comportement de secours, la gestion DTMF, la mise en file d'attente TTS, l'effacement du barge-in et les délais d'expiration de lecture. Il reste Expérimental car la preuve de qualité audio en direct est instable et il n'existe pas de matrice de lecture en direct large.

## Score de qualité

- Score : `Alpha (57%)`

La qualité est basée sur la conception du pipeline audio, la sémantique de secours, les contraintes spécifiques au fournisseur et l'état de l'archive active. L'existence des tests et l'étendue des tests n'ont pas été comptabilisées dans ce score de qualité.

Le code est prudent quant à ne pas mélanger les flux de médias actifs Twilio avec le secours Twilio Say, en effaçant l'audio mis en file d'attente lors du barge-in, en expirant la synthèse/lecture de flux et en enregistrant les décisions de secours. Il n'est pas plus élevé car les problèmes ouverts mentionnent la musique d'attente après les appels échoués/sans flux, l'écrêtage mu-law OpenAI realtime et les problèmes d'alias de configuration du fournisseur TTS.

## Score de complétude

- Score : `Expérimental (49%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le canal Voice Call.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune matrice de qualité audio en direct n'a été trouvée entre les fournisseurs TTS et les opérateurs.
- Les preuves de problèmes actifs couvrent la musique d'attente, les salutations en double et l'écrêtage mu-law.
- La dérive d'alias de configuration du fournisseur TTS a une activité PR récente, donc le comportement au niveau du fournisseur ne doit pas être supposé stable.

## Preuves

### Docs

- `docs/plugins/voice-call.md:447-479` documente TTS pour les appels, le comportement de fusion profonde TTS de base, Microsoft speech étant ignoré pour les appels vocaux, les limites de secours de flux de médias Twilio, la journalisation de la chaîne de secours et l'effacement de la file d'attente lors du barge-in.
- `docs/plugins/voice-call.md:480-543` documente les exemples TTS.
- `docs/plugins/voice-call.md:638-647` documente l'état initial de lecture/en direct et le comportement d'effacement du barge-in.
- `docs/plugins/voice-call.md:750-763` documente les actions de l'outil `voice_call` qui incluent la parole et les opérations du cycle de vie des appels.

### Source

- `extensions/voice-call/src/telephony-tts.ts:50-115` fusionne la configuration du fournisseur TTS téléphonique, analyse les directives, appelle le TTS téléphonique d'exécution, enregistre le secours et convertit l'audio PCM en mu-law 8 kHz.
- `extensions/voice-call/src/telephony-audio.ts:1` exporte les assistants partagés de conversion/rééchantillonnage de voix en temps réel pour l'audio téléphonique.
- `extensions/voice-call/src/providers/twilio.ts:611-660` implémente le comportement du mode TTS Twilio et empêche le secours Say lorsqu'un flux actif est requis.
- `extensions/voice-call/src/providers/twilio.ts:662-675` construit TwiML DTMF.
- `extensions/voice-call/src/providers/twilio.ts:677-798` diffuse TTS via les médias Twilio avec mise en file d'attente, chunks de 20 ms, délai d'expiration et gestion des défaillances pour les chunks/marques manquants.
- `extensions/voice-call/src/providers/twilio.ts:803-855` implémente le comportement d'écoute/statut.
- `extensions/voice-call/src/media-stream.ts:484-660` implémente la contre-pression du tampon d'envoi, le comportement d'envoi/marque/effacement audio.
- `extensions/voice-call/src/media-stream.ts:670-830` implémente la TTS mise en file d'attente et l'observabilité Talk.

### Tests d'intégration

- `extensions/voice-call/src/media-stream.test.ts:96-183` couvre la sérialisation de la file d'attente TTS, l'annulation et le comportement de démontage.
- `extensions/voice-call/src/webhook.test.ts:1652-1750` couvre la suppression du barge-in lors du message initial.
- `extensions/voice-call/src/webhook.test.ts:1562-1650` couvre la grâce de déconnexion de flux et le déclenchement de la disponibilité de transcription de la parole initiale.

### Tests unitaires

- `extensions/voice-call/src/providers/twilio.test.ts:382-595` couvre le secours TTS, la nouvelle tentative, DTMF, la désinscription de flux, le délai d'expiration de synthèse et l'audio supprimé.
- `extensions/voice-call/src/providers/twilio.test.ts:110-260` couvre la configuration TwiML/flux qui pilote le comportement de lecture.
- `extensions/voice-call/src/config.test.ts:399-545` couvre les remplacements TTS.

### Requêtes Gitcrawl

- `gitcrawl search issues "voice-call tts barge-in dtmf" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : n'a retourné aucun résultat pour ces termes exacts.
- `gitcrawl search issues "voice-call realtime twilio media stream" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #85848 pour l'écrêtage/rupture audio OpenAI realtime à l'intérieur des mots lors des appels sortants et #79121 pour la récolte de conversation Twilio obsolète.
- `gitcrawl search issues "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #81122 pour voice-call Twilio bloqué dans la musique d'attente après un appel échoué/sans flux et #85846 pour une salutation en double.
- `gitcrawl search prs "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #86285/#86502/#85932 pour les correctifs de salutation en double et #86413/#86366 pour les correctifs d'alias de voix/modèle ElevenLabs liés à la configuration TTS.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call tts dtmf barge"` : a retourné `null`, donc aucun résultat d'archive Discord n'a été trouvé pour ces termes exacts.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "google meet twilio voice-call"` : a retourné des notes de mainteneur selon lesquelles l'audio sortant Twilio frais fonctionnait, tandis que l'état Google Meet/voice-call obsolète et la propagation DTMF/mode nécessitaient un débogage.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call twilio telnyx plivo"` : a retourné des conseils de configuration selon lesquels `messages.tts` de base peut être utilisé pour les appels, TTS au niveau du plugin peut le remplacer, et Microsoft/Edge speech ne doit pas être compté comme support téléphonique.

### Snapshot de source archivée

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
