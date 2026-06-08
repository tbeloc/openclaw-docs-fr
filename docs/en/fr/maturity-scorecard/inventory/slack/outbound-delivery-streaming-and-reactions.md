---
title: "Slack - Message Delivery and Media Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Message Delivery and Media Maturity Note

## Summary

La livraison sortante Slack a une portée d'implémentation substantielle : envois de texte, Block Kit, chunking, réponses en thread, streaming de brouillon/progression, streaming/statut natif, réactions ack/typing, reçus de livraison, assistants de retry et contrôles d'identité. La couverture est Stable car la voie en direct vérifie le comportement des réponses visibles et du threading, tandis que la qualité reste Beta en raison des régressions actives de livraison/streaming et de la confusion de progression visible dans l'historique d'archive.

## Category Scope

Inclus dans cette catégorie :

- Outbound Delivery : Couvre la livraison sortante sur `message.send` livraison texte/bloc, réponses en thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Streaming : Couvre le streaming sur `message.send` livraison texte/bloc, réponses en thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Reactions : Couvre les réactions sur `message.send` livraison texte/bloc, réponses en thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Media : Couvre les médias sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Attachments : Couvre les pièces jointes sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Files : Couvre les fichiers sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Vision : Couvre la vision sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.

## Features

- Outbound Delivery : Couvre la livraison sortante sur `message.send` livraison texte/bloc, réponses en thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Streaming : Couvre le streaming sur `message.send` livraison texte/bloc, réponses en thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Reactions : Couvre les réactions sur `message.send` livraison texte/bloc, réponses en thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Media : Couvre les médias sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Attachments : Couvre les pièces jointes sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Files : Couvre les fichiers sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Vision : Couvre la vision sur fichiers entrants Slack, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.

## Archive Freshness

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Coverage Score

- Score : `Stable (82%)`
- Signaux positifs : Les sources et tests couvrent les chemins d'envoi/mise à jour/téléchargement Slack, le threading, la diffusion de réponse, les modes de streaming, le fallback d'aperçu, l'idempotence des réactions, la sélection de lecture/écriture de jeton utilisateur et le comportement de réponse en direct au niveau supérieur/thread.
- Signaux négatifs : La couverture en direct ne couvre pas encore tous les modes de streaming, les cartes de tâches de progression natives, le cycle de vie d'ajout/suppression de réaction, la personnalisation d'identité, la conversion longue markdown/rich-text ou la récupération de livraison au moment de la reconnexion.
- Lacunes d'intégration : Ajouter des scénarios en direct pour les cartes de tâches de progression/natives, le nettoyage de réaction/typing, les réponses longues chunked, les reçus de livraison via les hooks et le comportement de retry sous les erreurs transitoires Slack.

## Quality Score

- Score : `Beta (74%)`
- Rapports Gitcrawl : `#78103`, `#78536`, `#82258`, `#87748`, `#85612`, `#84271`, `#78046`, `#80749`, `#72896`, `#66614` et `#57708` montrent le travail continu de livraison, streaming, corrélation de hook et formatage Slack.
- Rapports Discrawl : Les discussions de version et de support mentionnent les améliorations de réponse interactive/thread/DM Slack, le churn de progression-aperçu, la suppression de progression verbose/outil Slack non-DM et les corrections de corrélation de livraison de canal.
- Bonnes qualités : Les chemins de livraison ont une gestion explicite des reçus, des wrappers de retry, un fallback du streaming échoué à la livraison normale, l'enregistrement de participation au thread et des valeurs par défaut conservatrices comme les unfurls désactivés.
- Mauvaises qualités : La sémantique du streaming/progression change encore fréquemment, la livraison peut sembler réussie tandis que le post-traitement échoue et le formatage riche spécifique à Slack est encore partiellement en attente.
- Exclu de la qualité : Nombre de tests unitaires, portée de la voie en direct et profondeur d'intégration.

## Completeness Score

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les docs archivées, les sources, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Outbound Delivery, Streaming, Reactions, Media, Attachments, Files, Vision.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même portée de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Ajouter une couverture en direct pour les cartes de tâches natives Slack et le fallback d'aperçu de brouillon en cas d'échec.
- Ajouter une preuve de corrélation de livraison de Slack `chat.postMessage` via les hooks `message_sent`.
- Ajouter un plan de conversion de formatage/rich-text Slack pour les réponses markdown longues et structurées.

## Evidence

### Docs

- `docs/channels/slack.md` documente les réactions ack, le fallback de réaction typing, le streaming de texte, le streaming natif, les cartes de tâches de progression, le fallback de médias/erreur, le chunking de texte, les unfurls et les contrôles de réponse en thread.
- `docs/concepts/qa-e2e-automation.md` documente les artefacts de sortie de la voie en direct Slack et les rapports de messages observés.

### Source

- `extensions/slack/src/send.ts` implémente les envois texte/bloc/fichier Slack, `thread_ts`, `reply_broadcast`, le comportement d'ouverture DM, l'achèvement du téléchargement et l'enregistrement de participation au thread.
- `extensions/slack/src/streaming.ts`, `extensions/slack/src/draft-stream.ts`, `extensions/slack/src/progress-blocks.ts` et `extensions/slack/src/monitor/message-handler/dispatch.ts` implémentent le comportement de brouillon/stream/progression.
- `extensions/slack/src/actions.ts` et `extensions/slack/src/actions.reactions.test.ts` couvrent les opérations de réaction.
- `extensions/slack/src/client.ts` centralise le comportement de retry/proxy/write-client Slack WebClient.

### Integration tests

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` vérifie l'écho canary, la forme de réponse au niveau supérieur, la reprise de redémarrage, le suivi en thread et l'isolation de thread dans un espace de travail Slack en direct.
- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.test.ts` affirme la couverture de scénario et la gestion des messages observés.

### Unit tests

- `extensions/slack/src/send.blocks.test.ts`, `send.identity-fallback.test.ts`, `send.unfurl.test.ts`, `send.upload.test.ts`, `outbound-delivery.test.ts` et `outbound-payload.test.ts` couvrent les détails de la charge utile d'envoi.
- `extensions/slack/src/streaming.test.ts`, `stream-mode.test.ts`, `draft-stream.test.ts`, `progress-blocks.test.ts` et `monitor/message-handler/dispatch.streaming.test.ts` couvrent les modes de streaming et le fallback d'aperçu.
- `extensions/slack/src/actions.reactions.test.ts`, `action-runtime.test.ts` et `client.test.ts` couvrent les réactions, la livraison d'action et le comportement de WebClient.

### Gitcrawl queries

Requête :

- `gitcrawl search openclaw/openclaw --query "slack streaming delivery" --json`
- `gitcrawl search openclaw/openclaw --query "Slack" --json`

Résultats :

- Retourné les problèmes et PRs de livraison/streaming incluant `#87748`, `#78103`, `#78536`, `#82258`, `#66614`, `#57708`, `#85612`, `#80632`, `#84297`, `#72896`, `#80749` et `#78046`.

### Discrawl queries

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack streaming progress delivery"`

Résultats :

- Retourné les notes de version/support sur le comportement de progression-aperçu Slack, les améliorations de réponse interactive/thread/DM Slack, la suppression de la livraison verbose/outil Slack non-DM et la direction de livraison de progression/finale de canal implémentée.
