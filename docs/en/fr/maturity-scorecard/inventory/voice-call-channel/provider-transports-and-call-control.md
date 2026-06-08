---
title: "Canal Voice Call - Note de maturité des médias et du contenu enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Canal Voice Call - Note de maturité des médias et du contenu enrichi

## Résumé

Cette note migre les preuves de maturité archivées pour le `canal Voice Call` / `Transports de fournisseur et contrôle d'appel` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Médias et contenu enrichi`
- Fusionnée à partir de : `Fournisseurs de téléphonie et médias`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Canal Voice Call : Transports de fournisseur et contrôle d'appel
- Canal Voice Call : Téléphonie TTS, lecture, DTMF et audio

## Fonctionnalités

- Canal Voice Call : Transports de fournisseur et contrôle d'appel
- Canal Voice Call : Téléphonie TTS, lecture, DTMF et audio

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (48%)`

Twilio, Telnyx, Plivo et les fournisseurs fictifs disposent de code adaptateur réel pour les appels sortants, les événements entrants, le statut, le DTMF, les opérations TTS/écoute et l'analyse des webhooks spécifiques au fournisseur. La couverture reste expérimentale car les preuves sont principalement du code et des chemins de fournisseur simulés ; il n'existe actuellement aucune matrice de scénario de transporteur en direct prouvant le même comportement sur tous les fournisseurs.

## Score de qualité

- Score : `Alpha (58%)`

La qualité est basée sur la forme d'abstraction du fournisseur, le comportement de normalisation, les limitations documentées et l'état actuel de l'archive. L'existence des tests et l'étendue des tests n'ont pas été comptabilisées dans ce score de qualité.

Les adaptateurs normalisent les événements spécifiques au transporteur dans un contrat de gestionnaire d'appels unique et échouent rapidement en cas d'identifiants manquants. La qualité est limitée par une parité plus faible en dehors de Twilio, des preuves de réponse automatique Telnyx ouvertes et des travaux d'expansion de fournisseur/temps réel actifs.

## Score de complétude

- Score : `Expérimental (48%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le canal Voice Call, le canal Voice Call.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Telnyx et Plivo ne sont pas prouvés à la même profondeur en direct que Twilio.
- La réponse automatique entrante de Telnyx a un problème ouvert.
- Aucune matrice de scénario en direct par transporteur n'a été trouvée pour le comportement sortant, entrant, DTMF, TTS, streaming et démontage.

## Preuves

### Docs

- `docs/plugins/voice-call.md:11-17` répertorie les fournisseurs Twilio, Telnyx, Plivo et fictifs et indique le support des notifications sortantes, des conversations multi-tours, de la voix en temps réel, de la transcription en streaming et des appels entrants.
- `docs/plugins/voice-call.md:101-168` documente la configuration du fournisseur, des numéros de/vers, des identifiants du fournisseur, du routage des numéros, de la diffusion, de la sécurité, des appels sortants, du streaming, du temps réel et de la portée de la session.
- `docs/plugins/voice-call.md:170-204` documente les notes d'exposition/sécurité du fournisseur et les limites de connexion en streaming.
- `docs/plugins/plugin-inventory.md:173` répertorie le plugin voice-call comme le plugin d'appel téléphonique Twilio/Telnyx/Plivo.

### Source

- `extensions/voice-call/src/providers/twilio.ts:333-397` normalise les webhooks de parole, DTMF, statut et fin de Twilio en événements d'appel.
- `extensions/voice-call/src/providers/twilio.ts:417-518` construit TwiML pour les réponses stockées, les conversations, les flux et les jetons par appel.
- `extensions/voice-call/src/providers/telnyx.ts:62-225` valide la configuration de Telnyx, vérifie les webhooks et analyse les événements du cycle de vie des appels, de transcription, de DTMF et de statut.
- `extensions/voice-call/src/providers/telnyx.ts:264-385` implémente les champs d'initiation, de réponse, de raccrochage, de TTS, d'écoute, de statut et de streaming de Telnyx.
- `extensions/voice-call/src/providers/plivo.ts:54-213` valide la configuration de Plivo, vérifie les webhooks, analyse les flux XML/spéciaux et normalise les webhooks.
- `extensions/voice-call/src/providers/plivo.ts:301-483` implémente le comportement sortant, TTS/écoute et statut de Plivo.

### Tests d'intégration

- `extensions/voice-call/src/runtime.test.ts:305-351` vérifie le comportement de fermeture d'échec du runtime du fournisseur pour les fournisseurs externes avec des webhooks locaux uniquement.
- `extensions/voice-call/src/webhook.test.ts:703-800` exerce la gestion de la relecture et les effets secondaires de la relecture de Plivo.
- `extensions/voice-call/src/webhook.test.ts:1033-1096` vérifie que le TwiML du fournisseur est servi avant les chemins de raccourci en temps réel.

### Tests unitaires

- `extensions/voice-call/src/providers/twilio.test.ts:110-260` couvre TwiML sortant, URL de conversation, TwiML en streaming et gestion de la file d'attente entrante.
- `extensions/voice-call/src/providers/twilio.test.ts:263-595` couvre le nettoyage, la déduplication, les jetons de tour, le secours TTS, la nouvelle tentative, le DTMF, la désinscription de flux, le délai d'expiration de la synthèse et l'audio supprimé.
- `extensions/voice-call/src/providers/telnyx.test.ts:121-456` couvre la vérification des webhooks de Telnyx, l'analyse, la déduplication, la direction, la transcription, le contrôle de réponse et les champs de streaming multimédia.
- `extensions/voice-call/src/providers/plivo.test.ts:18-85` couvre le rappel de réponse, la gestion des clés vérifiées et l'épinglage de la base de rappel.

### Requêtes Gitcrawl

- `gitcrawl search issues "voice-call twilio telnyx plivo" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #79118, où les appels entrants de Telnyx répondent et saluent mais ne répondent pas automatiquement sur le chemin `call.speech`.
- `gitcrawl search issues "voice-call realtime twilio media stream" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #85847, #80841, #85848, #79121 et #59245 pour la latence en temps réel, le changement de mode dynamique/AMD de Twilio, l'écrêtage audio, le moissonneur obsolète et les appels de tâches sortantes.
- `gitcrawl search prs "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné des RP adjacentes au fournisseur ouvertes, notamment le routage des appels vers l'agent appelant (#77763), les objectifs sortants privés (#83942), la correspondance de proxy (#86527), la persistance des transcriptions (#84161) et les dépendances du plugin de canal de voix groupées (#82105).

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call twilio telnyx plivo"` : a retourné des conseils de configuration/fournisseur et une note d'examen selon laquelle le mode temps réel devrait échouer rapidement sur les chemins de fournisseur non-Twilio plutôt que de ne rien faire silencieusement.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call realtime twilio"` : a retourné une note de contributeur selon laquelle Twilio dispose d'un support complet de Media Streams/WebSocket en temps réel tandis que le streaming bidirectionnel de Telnyx était toujours un travail de contribution.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "google meet twilio voice-call"` : a retourné des notes en direct de voix-appel/Google Meet de Twilio montrant que l'audio sortant frais fonctionnait, mais l'état de session obsolète et la propagation du mode restaient des préoccupations de débogage.

### Snapshot source archivé

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
