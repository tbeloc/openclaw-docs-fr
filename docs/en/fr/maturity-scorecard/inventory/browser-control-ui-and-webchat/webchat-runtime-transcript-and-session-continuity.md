---
title: "Gateway Web App - WebChat Runtime and Session Continuity Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - WebChat Runtime and Session Continuity Maturity Note

## Résumé

WebChat est profondément intégré au runtime Gateway via `chat.history`, `chat.send`, `chat.abort`, `chat.inject`, la résolution de session, les événements `chat` en direct, la projection d'affichage des transcriptions, les suppléments médias et la réconciliation optimiste côté client. La couverture est Stable car les méthodes serveur, le runtime chat Gateway, les contrôleurs UI et les harnais E2E navigateur couvrent les chemins principaux. La qualité est Alpha car l'archive montre une large surface de bugs vécus autour de l'identité de session, la relecture de transcription, la livraison visible, la dérive de routage, l'état en cours obsolète et le rendu des messages.

## Portée de la catégorie

Cette catégorie couvre le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, les notes d'assistant injectées, la continuité de session entre rechargement/reconnexion, la préservation optimiste de la queue, l'isolation de livraison WebChat et la normalisation d'affichage.

## Fonctionnalités

- Projection chat.history : Couvre la projection chat.history sur le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et continuité de session associés.
- Cycle de vie chat.send : Couvre le cycle de vie chat.send sur le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et continuité de session associés.
- Abandon/rétention partielle : Couvre l'abandon/rétention partielle sur le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et continuité de session associés.
- Notes d'assistant injectées : Couvre les notes d'assistant injectées sur le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et continuité de session associés.
- Continuité de reconnexion : Couvre la continuité de reconnexion sur le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et continuité de session associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : Les tests des méthodes serveur et des contrôleurs UI couvrent `chat.history`, `chat.send`, abandon, projection de transcription, messages médias, statut d'outil visible, listes de session et flux chat moqués navigateur.
- Signaux négatifs : De nombreuses combinaisons impliquent des flux de fournisseur réels, des fichiers de session durables, un contexte de livraison sur canal externe et des reconnexions navigateur. Ceux-ci ont une couverture de régression mais moins de preuve navigateur en direct récurrente.
- Lacunes d'intégration : Ajouter une fumée de version pour la continuité de session redémarrage/reconnexion, visualisation de transcription canal-vers-WebChat, relecture de statut d'outil visible, historique d'assistant porteur de médias, persistance partielle d'abandon et récupération d'état en cours obsolète.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : Les requêtes larges `WebChat` ont retourné les problèmes ouverts #80855, #85702, #77136, #70330, #87321, #78885, #87649, #67735, #64917 et les PRs ouvertes associées #75776, #87471, #87476, #77611, #69084, #75254 et #80670.
- Rapports Discrawl : La recherche Discord a trouvé des rapports de mainteneur et du trafic de version nommant préservation d'envoi reconnexion webchat, corrections de routage visible-réponse, bugs d'origine WebChat obsolète et régressions Control UI/chat comme points chauds de version actifs.
- Bonnes qualités : Le runtime a une projection d'affichage explicite, un historique borné, une documentation transcription-vs-livraison, l'idempotence, l'état d'exécution actif, la gestion d'abandon, les suppléments médias et la réconciliation optimiste côté client.
- Mauvaises qualités : L'identité de session et la projection de livraison sont intrinsèquement subtiles, et l'archive montre des régressions répétées où WebChat affecte ou masque les réponses de canal, le contenu de transcription ou l'état d'exécution visible.
- Exclu de la qualité : La preuve unitaire, intégration, e2e, en direct et flux runtime réel affectent la couverture uniquement.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les docs archivées, source, test, Gitcrawl et preuves Discrawl couvrent la portée de taxonomie pour projection chat.history, cycle de vie chat.send, abandon/rétention partielle, notes d'assistant injectées, continuité de reconnexion.
- Signaux négatifs : la note archivée a précédé le score de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La continuité de session entre redémarrages, mise en veille et reconnexion reste fragile dans les preuves d'archive.
- La relecture WebChat peut toujours diverger de l'état de transcription durable ou de livraison visible pour les réponses porteur d'outil uniquement et porteur de médias.
- L'identité de session WebChat interagit toujours avec le routage de canal externe assez pour produire des régressions.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/webchat.md` documente les RPC WebChat, `chat.history` borné, projection d'affichage, modèle transcription vs livraison, messages injectés, rétention partielle d'abandon et utilisation à distance.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente la sémantique chat send/history, l'idempotence, l'actualisation d'historique final, les messages locaux optimistes, `/new`, `/reset`, `/stop` et les remplacements de session modèle/réflexion.
- `/Users/kevinlin/code/openclaw/docs/channels/channel-routing.md` documente le comportement WebChat comme surface de canal/session interne.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat.ts` implémente `chat.history`, `chat.send`, `chat.abort`, `chat.inject`, gestion des pièces jointes, ajout de transcription, suppléments médias et dispatch de réponse.
- `/Users/kevinlin/code/openclaw/src/gateway/chat-display-projection.ts` borne et normalise les lignes de transcription pour l'affichage WebChat.
- `/Users/kevinlin/code/openclaw/src/gateway/server-chat.ts` et `/Users/kevinlin/code/openclaw/src/gateway/live-chat-projector.ts` gèrent la projection d'événement chat en direct.
- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/chat.ts` charge l'historique, filtre les lignes masquées, préserve les queues optimistes et gère la relance au démarrage.
- `/Users/kevinlin/code/openclaw/ui/src/ui/app-chat.ts` coordonne l'envoi, l'abandon, l'actualisation du sélecteur de session, la mise en file d'attente et les remplacements de modèle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server.chat.gateway-server-chat.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server.chat.gateway-server-chat-b.test.ts` couvrent le comportement du serveur chat Gateway.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat.abort-persistence.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat.inject.parentid.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat-webchat-media.test.ts` couvrent la persistance d'abandon, les ID parent d'injection et les médias WebChat.
- `/Users/kevinlin/code/openclaw/ui/src/ui/e2e/chat-flow.e2e.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/e2e/chat-picker-pagination.e2e.test.ts` exercent les flux chat navigateur.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-codex-harness.live.test.ts` couvre les chemins Gateway chat harnais Codex en direct.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/chat.test.ts` couvre le comportement historique/envoi/abandon client.
- `/Users/kevinlin/code/openclaw/ui/src/ui/app-chat.test.ts` couvre l'envoi, l'abandon, l'état en attente et les interactions session/modèle.
- `/Users/kevinlin/code/openclaw/src/gateway/chat-sanitize.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/chat-attachments.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-chat.stream-text-merge.test.ts` couvrent les aides de projection chat de niveau inférieur.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "WebChat"`

Résultats :

- Retourné les problèmes ouverts #80855, #85702, #77136, #70330, #87321, #78885, #87649, #67735, #64917, #76104 et autres problèmes WebChat.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "WebChat"`

Résultats :

- Retourné les PRs ouvertes #75776, #87471, #87476, #77611, #69084, #75254, #80670, #68701, #80985 et autres.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "WebChat chat.history chat.send transcript session continuity"`

Résultats :

- Retourné le problème ouvert #70330, `WebChat can silently rotate agent:main:main after gateway restart, hiding prior session/checkpoints`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 20 "WebChat"`

Résultats :

- Trouvé le rapport quotidien du mainteneur notant la préservation d'envoi reconnexion webchat.
- Trouvé la discussion du mainteneur de la PR #87476 corrigeant le routage WebChat obsolète pour les conversations de canal externe.
- Trouvé le trafic de version disant que les transcriptions utilisent le même chemin nettoyé que WebChat, relecture CLI/TUI, miroirs Codex et provenance médias.
