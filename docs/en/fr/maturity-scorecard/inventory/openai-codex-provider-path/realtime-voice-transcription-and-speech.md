---
title: "Chemin du fournisseur OpenAI / Codex - Note de maturité de la voix et de l'audio en temps réel"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenAI / Codex - Note de maturité de la voix et de l'audio en temps réel

## Résumé

La couverture de la parole et du temps réel d'OpenAI est significative mais pas encore stable. La documentation couvre la synthèse vocale, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, la facturation, le secours OAuth, les ponts de déploiement Azure, le WebRTC du navigateur, le WebSocket du serveur, et les outils de test en direct. La source dispose de plugins de fournisseur dédiés et de code de relais de passerelle. La couverture est bêta car une grande partie de la preuve est un test en direct optionnel ou spécifique au canal. La qualité est alpha car le temps réel a un chemin de facturation/quota distinct de la plateforme OpenAI, les champs de voix/session ont des contraintes spécifiques au fournisseur, et l'interruption/l'ajustement d'écho est complexe.

## Portée de la catégorie

Inclus dans cette catégorie :

- Transcription vocale en temps réel : couvre la transcription vocale en temps réel sur la synthèse vocale OpenAI, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, le Talk/WebRTC du navigateur, les ponts WebSocket du serveur, la création de secret client soutenue par OAuth, les déploiements Azure en temps réel, et le comportement de contrôle vocal.
- Parole : couvre la parole sur la synthèse vocale OpenAI, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, le Talk/WebRTC du navigateur, les ponts WebSocket du serveur, la création de secret client soutenue par OAuth, les déploiements Azure en temps réel, et le comportement de contrôle vocal.

## Fonctionnalités

- Transcription vocale en temps réel : couvre la transcription vocale en temps réel sur la synthèse vocale OpenAI, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, le Talk/WebRTC du navigateur, les ponts WebSocket du serveur, la création de secret client soutenue par OAuth, les déploiements Azure en temps réel, et le comportement de contrôle vocal.
- Parole : couvre la parole sur la synthèse vocale OpenAI, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, le Talk/WebRTC du navigateur, les ponts WebSocket du serveur, la création de secret client soutenue par OAuth, les déploiements Azure en temps réel, et le comportement de contrôle vocal.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (72%)`
- Signaux positifs : des plugins de fournisseur OpenAI dédiés existent pour la parole, la transcription en temps réel et la voix en temps réel ; les tests de relais de passerelle couvrent l'audio du navigateur, les transcriptions et les résultats des outils ; le script de test en direct vérifie le pont du serveur OpenAI et l'échange SDP WebRTC.
- Signaux négatifs : l'IC standard ne peut pas couvrir le comportement réel de la facturation/quota et du transport audio du temps réel OpenAI sans identifiants.
- Lacunes d'intégration : la voix en temps réel a besoin d'une preuve de version plus forte pour la facturation de la plateforme, la création de secret client OAuth, la forme de déploiement Azure, et les interfaces vocales spécifiques au canal.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : #76952 demande une documentation plus claire pour les voix du Talk en temps réel, les rôles d'agent vocal et les options de pont mobile/téléphone.
- Rapports Discrawl : les requêtes d'archive spécifiques au temps réel n'ont retourné aucune ligne directe, mais la source et la documentation OpenAI montrent une gestion explicite pour les risques de quota insuffisant et de fractionnement de facturation.
- Bonnes qualités : la source gère explicitement l'authentification par clé API par rapport à OAuth Codex, la création de secret client, les formes de session spécifiques à Azure, la troncature d'interruption, les reconnexions et les événements de transcription.
- Mauvaises qualités : le temps réel est opérationnellement sensible à la facturation, au quota, à l'écho, à la durée de session, à l'immuabilité de la voix et au comportement audio du canal.
- Exclu de la qualité : la présence de tests en temps réel et de test en direct a été utilisée uniquement pour la couverture.

## Score de complétude

- Score : `Bêta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la transcription vocale en temps réel, la parole.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La facturation et le quota en temps réel doivent être affichés avant le premier tour audio si possible.
- Les paramètres de voix et d'interruption ont besoin de diagnostics d'opérateur plus clairs lorsque l'écho/le bruit tronque la sortie.
- Les chemins Talk/WebRTC du navigateur, WebSocket du serveur et Voice Call ont besoin d'une histoire de preuve de version partagée.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente la synthèse vocale, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, le fractionnement de facturation de la plateforme, les secrets client soutenus par OAuth, les paramètres Azure en temps réel et la commande de test en direct.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md` documente les paramètres de voix en temps réel OpenAI pour la voix Discord, le contrôle du nom de réveil, la consultation d'agent, l'interruption, la gestion de l'écho/du bruit et l'interprétation des journaux.
- `/Users/kevinlin/code/openclaw/docs/plugins/voice-call.md` documente la configuration du fournisseur Voice Call en temps réel/streaming.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openai/speech-provider.ts` implémente la configuration du fournisseur TTS OpenAI, les voix, les formats de réponse, l'analyse des directives et la résolution de la configuration de talk.
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-transcription-provider.ts` implémente les sessions WebSocket de transcription en temps réel OpenAI, le secours du secret client OAuth, les paramètres VAD et la gestion des événements de transcription.
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-voice-provider.ts` implémente le pont WebSocket de voix en temps réel, la création de session du navigateur, la sélection d'authentification par clé API/OAuth Codex, le mode de déploiement Azure, les contrôles d'interruption, les reconnexions et la continuation des résultats des outils.
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-provider-shared.ts` crée des secrets client en temps réel et de transcription via les API HTTP OpenAI.
- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.ts` relie l'audio du navigateur, les transcriptions, les outils de consultation d'agent OpenClaw, les consultations forcées, l'interruption et la durée de vie de la session de relais.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.test.ts` exerce l'audio du navigateur, les transcriptions, les appels d'outils, l'enregistrement d'exécution d'agent, l'annulation et le comportement de la session de relais.
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts` vérifie le pont WebSocket du serveur OpenAI et l'échange SDP WebRTC du navigateur lorsque les identifiants en direct sont fournis.
- `/Users/kevinlin/code/openclaw/src/talk/provider-resolver.test.ts` couvre la résolution du fournisseur configuré et les remplacements de modèle/voix pour les fournisseurs de voix en temps réel.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-voice-provider.test.ts` couvre la configuration du fournisseur de voix en temps réel OpenAI et la gestion des événements.
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-transcription-provider.test.ts` couvre le comportement du fournisseur de transcription en temps réel.
- `/Users/kevinlin/code/openclaw/extensions/openai/speech-provider.test.ts` et `extensions/openai/tts.test.ts` couvrent la configuration TTS et le comportement de la requête de parole OpenAI.
- `/Users/kevinlin/code/openclaw/src/talk/agent-run-control.test.ts` couvre les appels d'outils de contrôle sémantique en temps réel.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "realtime voice OpenAI Platform credits quota"`

Résultats :

- A retourné #76952, une demande de documentation/fonctionnalité pour les voix du Talk en temps réel, le rôle d'agent vocal et les options de pont mobile/téléphone.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "barge-in realtime provider audio truncation Discord voice"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "OpenAI realtime gpt-realtime quota insufficient_quota barge-in voice WebRTC"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies.

Requête : `discrawl search --limit 10 "realtime voice OpenAI Platform credits quota"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies.
