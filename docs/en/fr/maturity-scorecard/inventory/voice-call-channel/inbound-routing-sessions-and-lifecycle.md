---
title: "Canal Voice Call - Note de Maturité du Routage et de la Livraison des Conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Canal Voice Call - Note de Maturité du Routage et de la Livraison des Conversations

## Résumé

Cette note migre les preuves de maturité archivées pour le `canal Voice Call` / `Routage entrant, Sessions et Cycle de vie` dans l'inventaire actuel du scorecard process-version-3.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Conversation Routing and Delivery`
- Fusionnée à partir de : `Call Routing and Sessions`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Canal Voice Call : Routage entrant, Sessions et Cycle de vie

## Fonctionnalités

- Canal Voice Call : Routage entrant, Sessions et Cycle de vie

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (52%)`

Les listes blanches entrantes, le routage par numéro, les clés de session par téléphone/par appel, le comportement de lecture initial, la grâce de déconnexion du flux, la récolte des appels obsolètes, le comportement de restauration et les flux de cycle de vie du gestionnaire sont implémentés et documentés. La couverture reste faible Alpha car les preuves sont principalement simulées, et les problèmes ouverts montrent que le comportement de session/cycle de vie a toujours des défauts non résolus adjacents à la production.

## Score de Qualité

- Score : `Alpha (58%)`

La qualité est basée sur la conception du cycle de vie, les avertissements documentés concernant l'ID de l'appelant, la configuration du routage, le comportement de récupération et les problèmes d'archive actifs. L'existence des tests et l'étendue des tests n'ont pas été comptabilisées dans ce score de Qualité.

La conception est raisonnablement défensive : les listes blanches existent, l'ID de l'appelant à faible assurance est documenté, la portée de la session est explicite, et les chemins obsolètes/restauration sont implémentés. La qualité reste Alpha car les preuves d'archive actives incluent des appels actifs obsolètes, des problèmes de routage multi-agent/clé de session et des lacunes de notification de transcription entrante.

## Score de Complétude

- Score : `Alpha (52%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le Canal Voice Call.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Le comportement de clé de session/routage a des preuves de problème de suivi ouvert.
- La gestion des appels actifs obsolètes a un bug ouvert.
- La notification de transcription entrante et la réponse automatique entrante Telnyx ne sont pas résolues dans l'archive des problèmes.

## Preuves

### Docs

- `docs/plugins/voice-call.md:206-212` documente la portée de session par défaut par téléphone et la portée de session par appel.
- `docs/plugins/voice-call.md:545-568` documente les appels entrants, les listes blanches, l'avertissement d'ID de l'appelant à faible assurance, les réponses automatiques, le modèle de réponse, l'invite système et l'ajustement du délai d'expiration.
- `docs/plugins/voice-call.md:569-618` documente le routage par numéro.
- `docs/plugins/voice-call.md:638-647` documente le comportement de démarrage de la conversation, la lecture initiale/état en direct, le comportement de nouvelle tentative, le démarrage du streaming Twilio, l'effacement du barrage-in et la propriété du tour d'ouverture en temps réel.
- `docs/plugins/voice-call.md:649-655` documente la grâce de déconnexion du flux Twilio.
- `docs/plugins/voice-call.md:657-681` documente le comportement du récolte d'appels obsolètes.

### Source

- `extensions/voice-call/src/config.ts:568-616` calcule les clés de route par numéro et les fusions de configuration efficaces.
- `extensions/voice-call/src/config.ts:719-734` dérive les clés de session pour les portées de session par téléphone et par appel.
- `extensions/voice-call/src/webhook.ts:327-504` initialise les rappels du fournisseur de streaming multimédia et gère la connexion/déconnexion du flux avec grâce.
- `extensions/voice-call/src/webhook.ts:511-580` démarre le serveur, les chemins de mise à niveau WebSocket et le récolte d'appels obsolètes.
- `extensions/voice-call/src/providers/twilio.ts:333-397`, `extensions/voice-call/src/providers/telnyx.ts:128-225` et `extensions/voice-call/src/providers/plivo.ts:132-299` normalisent les événements entrants/cycle de vie du fournisseur.

### Tests d'intégration

- `extensions/voice-call/src/runtime.test.ts:380-465` couvre le câblage de consultation en temps réel avec métadonnées de transcription/clé de session et spawned-by.
- `extensions/voice-call/src/runtime.test.ts:467-516` couvre les clés de session par appel pour les consultations en temps réel.
- `extensions/voice-call/src/webhook.test.ts:1562-1650` couvre la grâce de déconnexion du flux et le déclenchement de la disponibilité de la transcription des messages initiaux.
- `extensions/voice-call/src/webhook.test.ts:1652-1750` couvre la suppression du barrage-in pendant les messages initiaux.

### Tests unitaires

- `extensions/voice-call/src/manager.inbound-allowlist.test.ts:4-180` couvre le rejet pour les appelants manquants, anonymes, suffixe, doublon et nouvelle tentative, et accepte les correspondances exactes de la liste blanche.
- `extensions/voice-call/src/manager.closed-loop.test.ts:35-245` couvre les tours en boucle fermée sans audio en direct, rejet de chevauchement, jetons de parole obsolètes, tours répétés et métadonnées de latence.
- `extensions/voice-call/src/manager.notify.test.ts:137-370` couvre le mappage d'ID d'appel du fournisseur, les modes de message initial, l'attente de streaming/secours, l'écoute Telnyx, la journalisation des défaillances, la nouvelle tentative et les messages initiaux une seule fois/concurrents.
- `extensions/voice-call/src/manager.restore.test.ts:34-276` couvre la vérification de restauration pour les états terminal/actif/inconnu/délai d'expiration/pas de fournisseur/échec de vérification et la durée maximale restante.
- `extensions/voice-call/src/config.test.ts:281-397` couvre la portée de session et le routage par numéro.

### Requêtes Gitcrawl

- `gitcrawl search issues "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #79121 pour les conversations Twilio actives terminées par le récolte obsolète, #77753 pour Google Meet et routage voice_call dirigeant chaque appel vers un agent configuré unique dans les déploiements multi-agent, #83967 pour le suivi de clé de session et #77957 pour les appels entrants terminés persistant la transcription mais ne notifiant pas l'utilisateur.
- `gitcrawl search issues "voice-call streaming transcription" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #79121, #79118 et #79521 pour le récolte obsolète, la réponse automatique entrante Telnyx et la latence post-tour avant la réponse parlée.
- `gitcrawl search prs "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #77763 pour le routage des appels vocaux vers l'agent appelant, #75592 pour le contexte de l'appelant en temps réel, #83942 pour les objectifs sortants privés et #84161 pour la persistance de la transcription de l'assistant sur les événements de parole d'appel.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call stale reaper session key inbound"` : a retourné `null`, donc aucun résultat d'archive Discord n'a été trouvé pour ces termes exacts.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "google meet twilio voice-call"` : a retourné des notes en direct où une session `google_meet` obsolète pointait vers un ID voice-call mort, tandis qu'un `voice_call.initiate_call` frais produisait de l'audio sortant audible.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call realtime twilio"` : a retourné des notes de mainteneur sur les appels frais, les défauts de streaming/temps réel et le comportement de redémarrage autour de la configuration appliquée.

### Snapshot source archivé

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
