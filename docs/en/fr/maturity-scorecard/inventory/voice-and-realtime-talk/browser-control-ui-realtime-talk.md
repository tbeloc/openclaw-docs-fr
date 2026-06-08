---
title: "Voice and realtime talk - Browser Control UI Realtime Talk Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice and realtime talk - Browser Control UI Realtime Talk Maturity Note

## Résumé

Control UI Talk couvre OpenAI WebRTC, Google Live browser WebSocket, et les adaptateurs de relais Gateway. La couverture est au niveau bêta car la documentation, le code source de l'interface utilisateur, le code source de Gateway, et les chemins de smoke tests en direct existent. La qualité reste Alpha car les preuves d'archive incluent des défaillances de modèle/facturation, une inadéquation de la sortie vocale, et une confusion des utilisateurs due à plusieurs chemins de transport.

## Portée de la catégorie

- Interface utilisateur de démarrage/arrêt de Browser Talk et affichage du statut.
- Sessions OpenAI WebRTC et Google Live browser.
- Adaptateur de relais Gateway browser pour les fournisseurs backend uniquement.
- Transfert d'appels d'outils browser, événements de transcription, et lecture audio.

## Fonctionnalités

- Interface utilisateur de démarrage/arrêt de Browser Talk : Interface utilisateur de démarrage/arrêt de Browser Talk et affichage du statut
- Sessions Browser WebRTC : Sessions Browser WebRTC pour les fournisseurs OpenAI Realtime et Google Live.
- Mode relais Browser : Mode relais Browser pour les fournisseurs realtime backend uniquement.
- Transfert d'appels d'outils Browser : Transfert d'appels d'outils Browser, événements de transcription, et lecture audio

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`

Le composant browser dispose de documentation, trois implémentations de transport, des API de session Gateway, du câblage d'état de l'interface utilisateur, des tests spécifiques au transport, et un script de smoke test en direct. La couverture est limitée par les identifiants de fournisseur et le comportement des médias browser qui ne peuvent être prouvés qu'en direct.

## Score de qualité

- Score : `Alpha (68%)`

La qualité a des points forts : identifiants browser contraints, relais de secours explicite, et une interface d'événement partagée. Elle reste Alpha car l'archive montre des défaillances visibles par l'utilisateur actif pour l'accès au modèle OpenAI, l'inadéquation de la sortie vocale de l'assistant, le suivi des images de caméra, et la complexité de Control UI Talk.

Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution réel.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour Browser Talk start/stop UI, Browser WebRTC sessions, Browser relay mode, Browser tool-call forwarding.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- OpenAI WebRTC peut échouer avec `model_not_found` ou des problèmes de facturation/configuration.
- La sortie vocale peut diverger du texte Control UI lorsque le comportement du miroir de livraison diffère.
- Les choix de transport browser sont difficiles à expliquer et à exploiter.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:101` documente Chat/Talk, OpenAI WebRTC, les jetons browser Google à usage unique contraint, le relais Gateway, `talk.session.appendAudio`, la consultation, et la direction.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:185` documente la configuration du mode Talk, l'authentification, les secrets éphémères, les options, la ligne de statut, et le smoke test en direct.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:12` décrit les sessions browser `talk.client.create` pour les transports WebRTC et WebSocket du fournisseur, plus `talk.session.create` pour le relais Gateway.

### Code source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-client.ts:30` implémente `talk.client.create` pour les sessions realtime browser détenues par le client.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-client.ts:160` implémente le transfert browser `talk.client.toolCall` pour `openclaw_agent_consult`.
- `/Users/kevinlin/code/openclaw/ui/src/ui/app.ts:1087` câble les options de lancement Talk et l'état d'exécution dans Control UI.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk-webrtc.ts` implémente le chemin client OpenAI WebRTC.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk-google-live.ts:73` implémente le chemin client Google Live browser WebSocket.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk-gateway-relay.ts:44` implémente l'adaptateur browser de relais Gateway.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-webrtc.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-google-live.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-gateway-relay.test.ts`
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/app.talk.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk-conversation.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-consult.test.ts`

### Requêtes Gitcrawl

- `gitcrawl search issues "Control UI Talk realtime" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #83822 pour OpenAI WebRTC `model_not_found`, #85275 pour l'inadéquation de la sortie vocale, #86425 pour le support des images de caméra, #77966 pour la vérification audio Google Meet, et #73019 pour la voix realtime xAI.
- `gitcrawl search issues "talk realtime voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné des suites supplémentaires de Control UI et Talk provider.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "Control UI Talk" --limit 5` a retourné des notes de version indiquant que Google Live browser Talk utilise des identifiants éphémères contraints lorsqu'ils sont disponibles et le relais Gateway lorsque le fournisseur est backend uniquement.
- `/Users/kevinlin/.local/bin/discrawl search "Control UI Talk" --limit 5` a également retourné une discussion du 2026-04-30 soulignant l'étendue des fonctionnalités Control UI/Talk sur le transport realtime browser générique, Google Live, et le relais Gateway.
