---
title: "Voice and realtime talk - Realtime Talk Sessions Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice and realtime talk - Realtime Talk Sessions Maturity Note

## Résumé

Les sessions de relais de passerelle fournissent le chemin détenu par le backend pour Talk en temps réel et la transcription. La couverture est au niveau bêta car la source expose une API de session complète avec documentation, limites, suivi d'état, couverture de fumée en direct et tests de relais. La qualité atteint le seuil bêta car le runtime inclut des limites explicites et un nettoyage, tandis que les problèmes d'archive affichent toujours le contexte par session et les lacunes d'injection de parole asynchrone.

## Portée de la catégorie

Inclus dans cette catégorie :

- Agent consult handoff : Comportement de transfert de consultation entre les sessions Talk actives et les exécutions d'agent.
- Active Talk agent-run status : Statut de l'exécution d'agent Talk actif, annulation, direction et contrôles de suivi
- Talkback runtime behavior : Comportement du runtime Talkback et coordination de la parole de l'assistant
- Forced consult scheduling : Planification forcée de consultation et propagation d'événements de contrôle
- Browser Talk start/stop UI : Interface utilisateur de démarrage/arrêt de Talk du navigateur et affichage du statut
- Browser WebRTC sessions : Sessions WebRTC du navigateur pour les fournisseurs OpenAI Realtime et Google Live.
- Browser relay mode : Mode relais du navigateur pour les fournisseurs de temps réel backend uniquement.
- Browser tool-call forwarding : Transfert d'appels d'outils du navigateur, événements de transcription et lecture audio
- Realtime session controls : Création de session en temps réel, ajout audio, annulation de tour, direction, soumission de résultat d'outil et contrôles de fermeture.
- Gateway relay sessions : Sessions de relais de passerelle pour les flux de voix et de transcription en temps réel.
- Audio-frame limits : Limites de trame audio, TTL de session, plafonds par connexion/globaux, événements de transcription et nettoyage de relais

## Fonctionnalités

- Agent consult handoff : Comportement de transfert de consultation entre les sessions Talk actives et les exécutions d'agent.
- Active Talk agent-run status : Statut de l'exécution d'agent Talk actif, annulation, direction et contrôles de suivi
- Talkback runtime behavior : Comportement du runtime Talkback et coordination de la parole de l'assistant
- Forced consult scheduling : Planification forcée de consultation et propagation d'événements de contrôle
- Browser Talk start/stop UI : Interface utilisateur de démarrage/arrêt de Talk du navigateur et affichage du statut
- Browser WebRTC sessions : Sessions WebRTC du navigateur pour les fournisseurs OpenAI Realtime et Google Live.
- Browser relay mode : Mode relais du navigateur pour les fournisseurs de temps réel backend uniquement.
- Browser tool-call forwarding : Transfert d'appels d'outils du navigateur, événements de transcription et lecture audio
- Realtime session controls : Création de session en temps réel, ajout audio, annulation de tour, direction, soumission de résultat d'outil et contrôles de fermeture.
- Gateway relay sessions : Sessions de relais de passerelle pour les flux de voix et de transcription en temps réel.
- Audio-frame limits : Limites de trame audio, TTL de session, plafonds par connexion/globaux, événements de transcription et nettoyage de relais

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`

Le runtime de relais a une couverture large des méthodes Gateway, des protections au niveau source, des tests spécifiques au relais et un script de fumée en direct qui exerce les API d'adaptateur de navigateur et de session. La couverture n'est pas stable car le comportement de relais backend s'étend sur plusieurs fournisseurs et transports audio en direct.

## Score de qualité

- Score : `Bêta (70%)`

La qualité est soutenue par les TTL, les plafonds de trame audio, les limites de session par connexion/globales, l'état de transcription/santé, le nettoyage, la planification forcée de consultation et la propagation d'erreur explicite. La qualité est limitée par les demandes ouvertes pour les instructions/contexte de temps réel par session et l'injection de parole non bloquante.

Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux runtime réel.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Agent consult handoff, Active Talk agent-run status, Talkback runtime behavior, Forced consult scheduling, Browser Talk start/stop UI, Browser WebRTC sessions, Browser relay mode, Browser tool-call forwarding, Realtime session controls, Gateway relay sessions, Audio-frame limits.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les instructions et le contexte de temps réel par session sont toujours une demande ouverte.
- L'injection de parole de relais de temps réel non bloquante reste ouverte.
- Le comportement de relais dépend de la fiabilité du pont spécifique au fournisseur.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:12` décrit `talk.session.create` pour les sessions de relais de passerelle et l'opt-in Android.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:117` documente le comportement du relais de passerelle et de la transcription en temps réel.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:101` décrit les fournisseurs backend via le relais de passerelle et le PCM du microphone du navigateur via `talk.session.appendAudio`.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-session.ts:130` implémente les chemins `talk.session.create` en temps réel et de transcription.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-session.ts:408` implémente `talk.session.appendAudio`.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-session.ts:553` implémente les méthodes d'annulation et de contrôle.
- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.ts:46` définit les limites de TTL, trame audio, par connexion et session globale.
- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.ts:298` crée des sessions de relais en temps réel, des ponts de fournisseur, des événements de transcription, la direction, la planification forcée de consultation et le nettoyage.
- `/Users/kevinlin/code/openclaw/src/talk/session-runtime.ts:16` définit l'interface de session de pont utilisée par les fournisseurs de relais.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/talk-transcription-relay.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.test.ts`
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/talk/session-runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/talk-session-controller.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/session-log-runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/forced-consult-coordinator.test.ts`

### Requêtes Gitcrawl

- `gitcrawl search issues "talk.session gateway relay" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #84664 pour les instructions/contexte de temps réel par session, #84639 pour l'injection de parole de relais de temps réel non bloquante et #86425 pour le support de trame caméra.
- `gitcrawl search issues "talk realtime voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné des problèmes de relais/fournisseur plus larges incluant #84639 et #84664.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "gateway relay talk" --limit 5` a retourné des commentaires d'archive GitHub pour #71849 décrivant la latence et la fragilité de la consultation vocale en temps réel, plus #60093 et #71262 corrigés sur main pour le fournisseur de voix en temps réel partagé et les chemins de consultation.
- `/Users/kevinlin/.local/bin/discrawl search "gateway relay talk" --limit 5` a également retourné un commentaire d'examen de PR #71272 concernant les instructions par défaut référençant un outil indisponible sous `toolPolicy: none`.
