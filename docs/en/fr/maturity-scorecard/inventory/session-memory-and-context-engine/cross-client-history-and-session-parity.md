---
title: "Session, memory, and context engine - Cross-client History and Session Parity Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Cross-client History and Session Parity Maturity Note

## Résumé

La parité de session inter-clients est une promesse centrale du produit : WebChat, TUI, Android,
HTTP compatible OpenAI et les clients de canal doivent voir un historique et un état de session
compatibles via les sessions détenues par Gateway. La source a une projection forte, un historique
et un code client, mais les rapports d'archive montrent des lacunes persistantes après réinitialisation,
redémarrage, importations CLI natives, persistance Telegram, actualisation TUI et affichage de point de contrôle WebChat.

## Portée de la catégorie

Cette catégorie couvre `chat.history`, `chat.send`, projection d'affichage WebChat,
actions de session TUI, sélection de chat/session Android, mappage d'historique compatible OpenAI,
fenêtres d'historique de canal et visibilité de l'historique lors de réinitialisation/redémarrage.

## Fonctionnalités

- Cross-client History : Couvre l'historique inter-clients sur `chat.history`, `chat.send`, projection d'affichage WebChat, actions de session TUI, sélection de chat/session Android, mappage d'historique compatible OpenAI, fenêtres d'historique de canal et visibilité de l'historique lors de réinitialisation/redémarrage.
- Session Parity : Couvre la parité de session sur `chat.history`, `chat.send`, projection d'affichage WebChat, actions de session TUI, sélection de chat/session Android, mappage d'historique compatible OpenAI, fenêtres d'historique de canal et visibilité de l'historique lors de réinitialisation/redémarrage.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : tests Gateway `chat.history`, tests d'historique HTTP, tests d'historique TUI, tests du contrôleur de chat Android, mappage d'historique compatible OpenAI et tests de fenêtre d'historique de canal couvrent les surfaces client principales.
- Signaux négatifs : la parité en direct sur tous les clients et les amonts de canal n'est pas représentée par un scénario unique et complet.
- Lacunes d'intégration : ajouter un smoke de parité qui envoie des messages depuis WebChat, TUI, Android et un canal dans la même session et vérifie un historique cohérent, un ID de session, une sélection de modèle et un comportement de réinitialisation.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : la requête session/historique a retourné de nombreux rapports ouverts pour les archives cachées WebChat, les manques d'actualisation TUI, la non-persistance des DM Telegram, les abandons de réponse Slack, la rotation de redémarrage WebChat et la perte de contexte CLI native.
- Rapports Discrawl : les mentions de support Android `chat.history` parité ; les discussions d'archive session/historique identifient les magasins de transcription CLI natif versus OpenClaw non appariés.
- Bonnes qualités : Gateway est l'autorité d'historique unique et le code client demande l'historique via des RPC typés.
- Mauvaises qualités : les ruptures de parité sont visibles par l'utilisateur et se présentent souvent comme un historique manquant plutôt que des erreurs explicites récupérables.
- Exclu de la qualité : profondeur des tests unitaires, intégration, e2e, en direct et flux d'exécution.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs : les docs archivées, source, test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Cross-client History, Session Parity.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La parité d'importation CLI native est inégale entre les fournisseurs.
- L'affichage de réinitialisation/redémarrage/point de contrôle peut toujours diverger entre les clients WebChat, TUI et canal.

## Preuves

### Docs

- `docs/web/webchat.md:25` dit que WebChat utilise `chat.history`, `chat.send` et `chat.inject` ; `docs/web/webchat.md:52` dit que JSONL est la transcription durable.
- `docs/platforms/android.md:166` documente le chat Android plus l'historique ; `docs/platforms/android.md:170` dit que l'historique utilise `chat.history`.
- `docs/channels/channel-routing.md:143` dit que WebChat s'attache à l'agent sélectionné et utilise par défaut sa session principale.

### Source

- `src/gateway/chat-display-projection.ts:1201` projette les messages d'affichage de chat et `src/gateway/chat-display-projection.ts:850` assainit les messages d'historique.
- `src/tui/gateway-chat.ts:210` charge l'historique via `chat.history` ; `src/tui/gateway-chat.ts:230` liste les sessions.
- `apps/android/app/src/main/java/ai/openclaw/app/chat/ChatController.kt:333` demande `chat.history` ; `apps/android/app/src/main/java/ai/openclaw/app/chat/ChatController.kt:367` demande `sessions.list`.
- `src/channels/turn/history-window.ts:40` crée des fenêtres d'historique de canal.

### Tests d'intégration

- `src/gateway/server.chat.gateway-server-chat-b.test.ts:163` vérifie que `chat.history` n'attend pas la découverte du catalogue de modèles.
- `src/gateway/server.chat.gateway-server-chat-b.test.ts:741` remplit les sessions Claude CLI à partir des fichiers de projet.
- `src/gateway/sessions-history-http.test.ts:575` diffuse les mises à jour d'historique de session sur SSE.
- `src/gateway/openai-http.test.ts:130` valide le routage des messages d'historique/courant compatible OpenAI.

### Tests unitaires

- `src/tui/gateway-chat.test.ts:572` réessaie le `chat.history` indisponible au démarrage.
- `apps/android/app/src/test/java/ai/openclaw/app/chat/ChatControllerSessionPolicyTest.kt:36` empêche le chargement d'historique obsolète après le changement de session.
- `src/channels/turn/history-window.test.ts:6` enregistre, formate, expose et efface l'historique du canal.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "chat.history WebChat Android session history" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- Retourné `[]`.

Requête :

`gitcrawl search issues "openclaw sessions transcripts chat.history" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- Retourné 13 rapports ouverts, incluant les archives cachées WebChat, la non-actualisation TUI après réinitialisation de canal, la non-persistance de session Telegram, l'inadéquation de transcription/livraison Slack, la rotation de redémarrage WebChat et les courses de perte de contexte CLI native.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "chat.history WebChat Android session history"`

Résultats :

- Retourné les conseils de support Android selon lesquels le chat nécessite une connexion d'opérateur et utilise `chat.history` ; également retourné un support plus ancien où une session bloquée par limite de contexte nécessitait d'effacer l'état de session.

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "openclaw sessions transcripts chat.history"`

Résultats :

- Retourné des discussions sur le nettoyage des transcriptions orphelines, les artefacts cachés de transcription uniquement et la confusion du magasin d'historique OpenClaw versus CLI natif.
