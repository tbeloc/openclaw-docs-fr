---
title: "iOS app - Chat and Sessions Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Chat and Sessions Maturity Note

## Résumé

L'application iOS dispose d'une surface de chat dédiée aux opérateurs : une session Gateway dédiée aux opérateurs, un onglet Chat, une interface de chat native partagée, des liens de session du centre de commande, un routage des agents, un partage/transfert de lien profond et des invites d'approbation exécutive. La couverture est Expérimentale car la plupart des preuves sont au niveau source et unité/smoke ; le seul script iOS en direct actuel exerce les capacités des nœuds, non le flux de travail chat/opérateur. La qualité est Expérimentale car l'implémentation a une bonne structure de sécurité et de produit, mais les preuves d'archive actuelles montrent des régressions récentes dans la livraison de chat iOS, les commandes slash, le partage de transcription et la portée des opérateurs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Sessions de chat et contrôles des opérateurs : Transport de session opérateur, onglet Chat, compositeur/historique/streaming/affichage des outils de chat, centre de commande, permissions et contrôles de session.

## Fonctionnalités

- Sessions de chat et contrôles des opérateurs : Transport de session opérateur, onglet Chat, compositeur/historique/streaming/affichage des outils de chat, centre de commande, permissions et contrôles de session.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimentale (40%)`
- Signaux positifs : La source implémente un WebSocket opérateur secondaire, `chat.history`, `chat.send`, `chat.abort`, `sessions.list`, `sessions.create`, réinitialisation/compactage, `agent.wait`, gestion des événements chat/agent, lignes du centre de commande de session active, partage/transfert de lien profond et interface utilisateur d'examen d'approbation exécutive.
- Signaux négatifs : Aucune preuve iOS en direct/e2e actuelle n'a été trouvée pour installer/appairer/ouvrir Chat/envoyer/diffuser/afficher les outils/changer de session/partager/lien profond/approbation en tant que flux unique. Le script d'exécution iOS actuel couvre un nœud iOS connecté et `node.invoke`, non l'onglet chat opérateur ou le compositeur.
- Lacunes d'intégration : Ajouter un e2e de périphérique appairé ou simulateur qui pilote l'onglet Chat par rapport à une véritable Gateway, envoie des pièces jointes texte et image, valide le streaming/cartes d'outils/historique, bascule les sessions depuis le Centre de commande, exerce l'intake de partage/lien profond et résout une approbation exécutive.

Étiquettes de couverture :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

## Score de qualité

- Score : `Expérimentale (44%)`
- Rapports Gitcrawl : Le problème ouvert #80231 signale que les messages de chat de groupe iOS ne se mettent pas à jour en temps réel ; la PR ouverte #86737 identifie `IOSGatewayChatTransport.setActiveSessionKey` comme un no-op et ajoute un travail d'abonnement à la transcription par session. La PR #86936 signale que les images de Share Extension iOS atteignent l'agent mais perdent les métadonnées multimédias dans les transcriptions. La PR #79985 documente que la visibilité des agents iOS/Android/TUI dépend de la Gateway `agents.list`, qui diffère intentionnellement de la portée CLI.
- Rapports Discrawl : Les enregistrements miroir Discord/GitHub documentent les chats iOS antérieurs bloqués par les restrictions de rôle de nœud, les régressions `/compact` et slash-command, la consommation manquante de `chat.side_result`, les problèmes de build/métadonnées de ShareExtension et les résultats d'examen de compatibilité de portée/reconnexion d'approbation opérateur.
- Bonnes qualités : L'application sépare les sessions de nœud et d'opérateur, utilise des portées d'opérateur explicites, garde les commandes de nœud hors du socket opérateur, limite le débit et confirme les liens profonds d'agent non fiables, supprime les champs de livraison non fiables, persiste les agents sélectionnés par passerelle et expose les décisions d'approbation via les lignes du centre de commande et une carte modale.
- Mauvaises qualités : Le transport actuel n'a toujours pas de corps d'abonnement de session active et aucun mappage d'événement `session.message` visible dans `IOSGatewayChatTransport`, donc les mises à jour de chat multi-agent/groupe dépendent d'événements chat/agent plus faibles et de fallbacks d'actualisation. Le transport iOS n'implémente pas les RPC de patch de modèle ou de réflexion, et plusieurs chemins de chat opérateur sont toujours en cours de réparation dans les enregistrements d'archive ouverts.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réelle n'a pas été utilisée pour augmenter ou diminuer la qualité.

Étiquettes de qualité :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

## Score d'exhaustivité

- Score : `Expérimentale (40%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les sessions de chat et les contrôles des opérateurs.
- Signaux négatifs : la note archivée a précédé le scoring d'exhaustivité de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles aux opérateurs.

## Lacunes connues

- La source actuelle a besoin d'un chemin de transcription par session abonné pour les chats de groupe iOS, plus une gestion visible pour les événements `session.message` d'assistant.
- Le flux de travail chat/opérateur iOS a besoin d'une preuve d'exécution répétable qui couvre l'onglet Chat, le transfert de session du Centre de commande, le partage/transfert de lien profond et les approbations exécutives.
- Les contrôles de modèle/réflexion sont présents dans l'interface de chat partagée mais ne sont pas entièrement soutenus par les RPC de transport iOS.
- La persistance des médias de Share Extension et la parité de transcription sont toujours représentées par un travail de réparation d'archive ouvert.

# Preuve

## Docs

- `/Users/kevinlin/code/claw/maintainers/docs/kevinslin/maturity-scorecard/maturity-scorecard.md` liste `iOS app | M1 Experimental | High | Internal preview / super-alpha. TestFlight and relay-backed push flows exist, but no public distribution yet.`
- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente le nœud iOS, le nœud authentifié plus les sessions d'opérateur, `gateway.identity.get`, les limites de premier plan, et la relation nœud-commande iOS.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` indique que l'application est super-alpha/usage interne uniquement, et liste Chat + Talk via la session de passerelle d'opérateur plus le transfert de lien profond d'extension de partage comme surfaces de travail concrètes.

## Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel.swift` possède des sessions `nodeGateway` et `operatorGateway` séparées, démarre la boucle d'opérateur avec `role: "operator"` et les portées `operator.read`/`operator.write`/`operator.talk.secrets`, actualise la config/agents/route de partage, dérive `chatSessionKey` limité à l'agent, transfère les liens profonds d'agent, et résout les approbations d'exécution.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Chat/IOSGatewayChatTransport.swift` mappe la session d'opérateur iOS à `sessions.create`, `chat.abort`, `sessions.list`, `sessions.reset`, `sessions.compact`, `chat.history`, `chat.send`, `agent.wait`, `health`, et les événements serveur `chat`/`agent`.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Design/ChatProTab.swift` intègre `OpenClawChatView` avec le transport iOS, la pilule de connexion, l'affichage de l'agent, et le basculement Talk.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Design/CommandCenterTab.swift` affiche l'état de la passerelle, les approbations en attente, les sessions de chat actives/récentes de `sessions.list`, et achemine les lignes vers Chat.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawChatUI/ChatViewModel.swift`, `ChatView.swift`, et `ChatComposer.swift` implémentent l'amorçage de l'historique, les envois optimistes, le texte d'assistant en continu, l'affichage des outils en attente, les pièces jointes, l'abandon/actualisation/réinitialisation/compactage, les choix de session, l'interface utilisateur du modèle/réflexion, et l'actualisation de premier plan.
- `/Users/kevinlin/code/openclaw/apps/ios/ShareExtension/ShareViewController.swift` envoie le texte/les images partagés à la passerelle en tant que `agent.request` via `node.event`.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Gateway/DeepLinkAgentPromptAlert.swift` et `ExecApprovalPromptDialog.swift` fournissent l'interface utilisateur de confirmation et d'approbation locale.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/dev/ios-node-e2e.ts` se connecte à une véritable passerelle en tant qu'opérateur, trouve un nœud iOS connecté, et invoque des commandes de nœud ; il ne couvre pas l'interface utilisateur de l'onglet Chat/compositeur/historique/session.
- `/Users/kevinlin/code/openclaw/package.json` a les scripts `ios:build` et `ios:run` pour la construction/lancement du simulateur, mais aucune assertion de flux de travail chat/opérateur scriptée n'a été trouvée.
- Aucun e2e iOS actuellement enregistré n'a été trouvé pour `chat.send` via une application iOS appairée, l'affichage réel du streaming/des outils, le transfert de session du Centre de commande, la livraison de partage/lien profond, ou la résolution d'approbation d'exécution.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/IOSGatewayChatTransportTests.swift` couvre l'encodage des requêtes de transport iOS, la gestion du statut `agent.wait`, les paramètres de liste de session, les paramètres d'envoi de chat, et le comportement d'échec rapide lorsque la passerelle est déconnectée.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/NodeAppModelInvokeTests.swift` couvre `chatSessionKey`, les sessions limitées à l'agent, la confirmation de lien profond/limites de débit/contournement de clé, et le comportement de récupération d'invite d'approbation d'exécution/montre.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/GatewayConnectionControllerTests.swift` couvre la construction de portée d'opérateur et le comportement rétrocompatible `operator.approvals`.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/SwiftUIRenderSmokeTests.swift` vérifie que `RootTabs` et les surfaces de paramètres construisent une hiérarchie de vues.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Tests/OpenClawKitTests/ChatViewModelTests.swift` et les tests de chat partagés adjacents couvrent le modèle de chat partagé, les choix de session, les événements de streaming/finaux, les pièces jointes, les commandes slash, le comportement de compactage/réinitialisation, le markdown, et les aides du compositeur.

## Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "openclaw-ios chat" --json`

Résultats :

- A retourné le problème ouvert #80231 `Group chat messages don't update in real-time on iOS — requires exit and re-entry`.
- A retourné la PR ouverte #86737 `fix(ios): subscribe to per-session transcripts so group chats update in real time (#80231)`.
- A retourné la PR ouverte #50483 `fix(ios): stabilize chat streaming layout and session flow`.
- A retourné la PR ouverte #86936 `fix(gateway): persist media metadata in agent.request transcripts`.
- A retourné la PR ouverte #73711 `feat(chat/ios): photos-picker-style attachment thumbnails with persistent add-more tile`.
- A retourné la PR ouverte #79985 `docs+tests: clarify agents.list visibility scope across CLI and Gateway`.

Requête :

`gitcrawl search openclaw/openclaw --query "IOSGatewayChatTransport" --json`

Résultats :

- A retourné la PR ouverte #86737 ; l'extrait identifie `IOSGatewayChatTransport.setActiveSessionKey` comme un stub commenté uniquement.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS group chat real time session.message" --json`

Résultats :

- A retourné le problème ouvert #80231 et la PR ouverte #86737 pour les mises à jour en temps réel du chat de groupe et le travail de transcription par session.

Requête :

`gitcrawl threads openclaw/openclaw --numbers 80231 --include-closed --json`

Résultats :

- Le corps du problème #80231 signale que les réponses de chat de groupe Aight/iOS n'apparaissent pas automatiquement et nécessitent de quitter/réentrer le chat ; les étiquettes incluent `impact:session-state` et `impact:message-loss`.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS agent request share extension attachments" --json`

Résultats :

- A retourné la PR ouverte #86936 ; le corps indique que les images partagées via l'extension de partage iOS atteignent la passerelle via `agent.request` mais les métadonnées multimédias n'ont pas été conservées dans l'historique des transcriptions.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS exec approval operator approvals" --json`

Résultats :

- N'a retourné aucun résultat.

## Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "IOSGatewayChatTransport"`

Résultats :

- A retourné les commentaires d'examen du miroir GitHub pour #53843 et #45444 sur le support manquant de `/compact` de transport iOS et iOS ne consommant pas les événements `chat.side_result`.
- A retourné les messages de dev et d'architecture du 2026-02-03/04 demandant si le chat iOS était intentionnellement bloqué parce que l'application utilisait une connexion de rôle de nœud tandis que `chat.send`/`chat.history` nécessitaient un accès d'opérateur.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS Share Extension"`

Résultats :

- A retourné le texte du miroir #44914 sur la rupture de construction ShareExtension après que `GatewayNodeSession.connect` ait acquis `bootstrapToken`.
- A retourné le texte du miroir #60339 sur les références multimédias de partage/chemin de nœud iOS non conservées dans les transcriptions.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "operator.approvals iOS"`

Résultats :

- A retourné les commentaires d'examen #63697 et #60238 sur le respect de `includeApprovalScope`, les portées de reconnexion d'opérateur rétrocompatibles, et l'évitement des mises à niveau forcées de portée `operator.approvals` sur les appairages iOS hérités.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "chat.side_result iOS"`

Résultats :

- A retourné le commentaire d'examen #45444 selon lequel iOS ne consommait pas les événements `chat.side_result`, risquant la perte de la sortie de question secondaire jusqu'à ce que le support d'événement en direct existe.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS chat /compact"`

Résultats :

- A retourné l'historique d'examen/commentaire #63697 sur le routage des commandes slash via la passerelle et le comportement de nouvelle tentative après `/compact`.
- A retourné le commentaire d'examen #53843 selon lequel le support manquant de `compactSession` iOS ferait échouer `/compact` dans la feuille de chat iOS.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Aight group chat"`

Résultats :

- N'a retourné aucune ligne.
