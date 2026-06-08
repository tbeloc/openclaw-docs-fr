---
title: "iMessage / BlueBubbles - Actions natifs, API privée et note de maturité de l'outil de message"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Actions natifs, API privée et note de maturité de l'outil de message

## Résumé

Les actions natifs, l'API privée et le comportement de l'outil de message sont en version bêta. La surface d'action est large et explicitement contrôlée : réagir, modifier, annuler l'envoi, répondre, effets, indicateurs de lecture/saisie, envois enrichis et gestion de groupe dépendent du pont API privée `imsg` et des sondes de capacité. Le composant n'est pas stable car l'état de l'API privée est fragile, le support des actions varie selon la version `imsg`/macOS, et les archives montrent un travail actif autour des envois enrichis et du formatage des actions.

## Portée de la catégorie

Cette note couvre la détection d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, la modification/annulation d'envoi/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action.

## Fonctionnalités

- Actions natifs : couvre les actions natifs sur la détection d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, la modification/annulation d'envoi/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action.
- API privée : couvre l'API privée sur la détection d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, la modification/annulation d'envoi/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action.
- Outil de message : couvre l'outil de message sur la détection d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, la modification/annulation d'envoi/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (73%)`
- Signaux positifs :
  - La documentation énumère les capacités d'action et les exigences de l'API privée.
  - La source contrôle les actions par état de configuration et de sonde, reprobe paresseusement l'état du pont inconnu, résout les identifiants courts et les cibles de chat, et vérifie le support de `send-rich --file`.
  - Les tests couvrent la publicité des actions, les portes désactivées par configuration, le mappage des tapbacks, la résolution des cibles de chat, la propagation du chemin db et les pièces jointes de réponse enrichie.
  - Les tests de l'outil de message couvrent la grammaire cible iMessage et les descriptions délimitées par canal.
- Signaux négatifs :
  - Aucune voie d'action en direct n'a été trouvée pour les opérations réelles de Messages.app réagir/modifier/annuler l'envoi/répondre et de gestion de groupe.
  - La capacité de l'API privée dépend de `imsg launch`, des paramètres SIP, de la version macOS et de la version `imsg` installée.
  - Les problèmes d'archive montrent des raffinements continus des actions/médias/envois enrichis.
- Lacunes d'intégration :
  - Ajouter une voie Mac contrôlée qui effectue une action d'API privée réussie de chaque classe et un résultat de porte indisponible attendu.
  - Ajouter une intégration fake-imsg autour des sélecteurs `imsg status --json`/méthodes rpc et de la visibilité des actions de l'outil de message.

## Score de qualité

- Score : `Bêta (71%)`
- Rapports Gitcrawl :
  - `iMessage private API` a retourné #84329 pour la préférence de transport IMCore/API privée configurable, #79610 pour le bruit stderr sur le chemin de l'API privée et les notes de version bêta adjacentes mentionnant les diagnostics de réaction/API privée iMessage.
  - `iMessage send-rich` a retourné #84329, #87597 et #85954.
  - `iMessage private API react edit unsend reply sendWithEffect group management` n'a retourné aucun résultat direct dans la dernière passe.
- Rapports Discrawl :
  - `iMessage private API` a retourné les notes de version bêta mentionnant les diagnostics de réaction/API privée iMessage.
  - `iMessage send-rich` a retourné des extraits de mainteneur sur les pièces jointes de réponse iMessage via `send-rich --file`.
- Bonnes qualités :
  - La disponibilité des actions n'est pas codée en dur ; elle utilise l'état de la sonde et les vérifications de capacité.
  - L'état du pont inconnu garde les actions visibles mais reprobe paresseusement à la première utilisation, évitant une UX faux-négatif obsolète.
  - Les portes de configuration sont appliquées au moment de la publicité et de l'exécution.
  - Les pièces jointes de réponse enrichie échouent bruyamment lorsque la version `imsg` installée manque de `send-rich --file`.
- Mauvaises qualités :
  - Le pont API privée est une dépendance externe intrinsèquement fragile.
  - L'état du pont en cache peut dériver après le redémarrage de Messages jusqu'à la reprise.
  - La surface d'action est suffisamment large pour que chaque incompatibilité de version macOS/imsg puisse créer un cas limite visible par l'utilisateur.
- Exclu de la qualité :
  - Les preuves des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Bêta (73%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les actions natifs, l'API privée et l'outil de message.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve d'action avancée en direct est manquante.
- La dérive de capacité `imsg` et la disponibilité de l'API privée restent visibles par l'opérateur.
- Les médias/actions enrichis ont une churn de champ récente.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:499` : la disponibilité de l'API privée expose les actions natives iMessage via l'outil de message.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:525` : l'action réagir mappe aux tapbacks supportés.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:528` : l'action modifier est disponible sur les versions macOS/API privée supportées.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:529` : l'action annuler l'envoi est disponible sur les versions macOS/API privée supportées.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:541` : l'état inconnu laisse les actions visibles et reprobe paresseusement au dispatch.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:546` : les reçus de lecture et les bulles de saisie dépendent du pont.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:218` : la liste de contrôle de migration indique aux opérateurs de tester les actions réagir, modifier, annuler l'envoi, répondre, média et groupe.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:84` : la base du plugin déclare la capacité média.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:85` : la base du plugin déclare la capacité réactions.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:86` : la base du plugin déclare la capacité modifier.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:87` : la base du plugin déclare la capacité annuler l'envoi.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:88` : la base du plugin déclare la capacité répondre.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:89` : la base du plugin déclare la capacité effets.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:90` : la base du plugin déclare la capacité gestion de groupe.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.ts:412` : le dispatch d'action lit l'état de l'API privée en cache.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.ts:420` : le dispatch d'action effectue une sonde d'API privée en ligne si nécessaire.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.ts:425` : le pont indisponible bloque les actions d'API privée.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.ts:559` : la réponse avec pièce jointe nécessite `send-rich --file`.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/tools/message-tool.test.ts:1493` : les tests de l'outil de message créent un plugin de canal iMessage avec chemin docs.
- `/Users/kevinlin/code/openclaw/src/agents/tools/message-tool.test.ts:1508` : les descriptions de l'outil de message incluent des indices de cible chat iMessage/SMS.
- Aucune voie d'action d'API privée en direct n'a été trouvée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.test.ts:98` : les actions d'API privée ne sont pas annoncées lorsque le pont est connu comme indisponible.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.test.ts:113` : les actions d'API privée restent annoncées lorsque l'état du pont est inconnu.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.test.ts:135` : les actions de parité BlueBubbles sont annoncées lorsque les sélecteurs d'API privée sont disponibles.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.test.ts:165` : les portes d'action configurées sont respectées.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.test.ts:234` : les réactions de l'outil de message mappent aux types de tapback imsg.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.test.ts:419` : les pièces jointes de buffer hydratées passent par `sendRichMessage` lorsqu'elles sont supportées.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.runtime.test.ts:33` : le `dbPath` configuré est passé aux commandes du pont API privée.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/actions.runtime.test.ts:93` : les cibles de chat direct synthétisées se résolvent par rapport à `chats.list`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage private API" --json --limit 6`

Résultats :

- Problème ouvert #84329 : les envois sortants doivent préférer le transport IMCore configurable lorsqu'il est disponible.
- Problème ouvert #79610 : AddressBook Apple bénin enregistré au niveau d'erreur.
- Extraits de version/archive mentionnent les diagnostics de réaction/API privée iMessage.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage send-rich" --json --limit 6`

Résultats :

- Problème ouvert #84329, problème ouvert #87597 et problème ouvert #85954.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage private API" --limit 6`

Résultats :

- Les notes de version bêta ont mentionné les diagnostics de réaction/API privée iMessage.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage send-rich" --limit 6`

Résultats :

- Les extraits de mainteneur ont référencé les pièces jointes de réponse iMessage fusionnées via `send-rich --file`.
