---
title: "Application compagnon macOS - Note de Maturité WebChat"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon macOS - Note de Maturité WebChat

## Résumé

L'application macOS intègre l'interface utilisateur WebChat partagée en tant que fenêtre/panneau natif SwiftUI soutenu par des appels RPC Gateway et des flux d'événements. Elle prend en charge la commutation de session, les contrôles de modèle/réflexion, la santé, l'abandon, la compaction, la réinitialisation, les pièces jointes et les paramètres par défaut de session principale via `OpenClawChatUI`. La couverture est Beta car les chemins de transport de chat natifs sont implémentés avec preuve de fumée de support, mais un scénario WebChat d'application en direct via Gateway local et distant n'a pas été trouvé. La qualité est Alpha car les preuves d'archive montrent des gels WebChat actifs, des régressions de continuité de transcription/session et un scintillement de credential natif.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Fenêtre WebChat SwiftUI native : Fenêtre WebChat SwiftUI native et panneau de menu
- Transport de chat Gateway : Transport de chat Gateway, contrôles de session/modèle/réflexion, mappage d'événements et santé
- Réutilisation du plan de données local et distant : Réutilisation du plan de données local et distant entre les sessions WebChat natives.

## Fonctionnalités

- Fenêtre WebChat SwiftUI native : Fenêtre WebChat SwiftUI native et panneau de menu
- Transport de chat Gateway : Transport de chat Gateway, contrôles de session/modèle/réflexion, mappage d'événements et santé
- Réutilisation du plan de données local et distant : Réutilisation du plan de données local et distant entre les sessions WebChat natives.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (72%)`
- Signaux positifs : La documentation et le code source couvrent le lancement de WebChat, les plans de données locaux/distants, les méthodes/événements Gateway, les paramètres par défaut de session et la journalisation de débogage. Les tests de fumée instancient les contrôleurs de fenêtre et de panneau avec un transport factice. L'interface utilisateur WebChat partagée a une couverture plus large du navigateur/interface de contrôle dans les surfaces adjacentes.
- Signaux négatifs : Aucun test WebChat en direct d'application macOS n'a été trouvé qui envoie un vrai tour Gateway, gère la reconnexion, bascule les sessions et maintient le même état de panneau/fenêtre.
- Lacunes d'intégration : Besoin d'un scénario WebChat natif local et distant couvrant `chat.history`, `chat.send`, les événements en continu, l'abandon, la commutation de session, le sommeil/reconnexion et la récupération après redémarrage de Gateway.

## Score de Qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : Les résultats incluent des problèmes WebChat pour l'entrée lente (#54874), les blocs d'injection de mémoire divulgués (#64613), les défaillances de rendu (#77136), la réécriture de transcription (#77012), les messages perdus lors de la reconnexion (#45952), les messages finaux en double (#85771), la réinitialisation de session après déconnexion/sommeil réseau (#87700) et le scintillement de credential natif (#85352).
- Rapports Discrawl : Le rapport de support utilisateur du 2026-05-21 indique que WebChat macOS se verrouille après une invite et force une nouvelle session par message. La discussion de test de version appelle à plusieurs reprises WebChat/mobile/interface de contrôle comme focus de régression.
- Bonnes qualités : WebChat natif utilise une abstraction de transport partagée, mappe les événements Gateway santé/chat/agent/session, persiste le niveau de réflexion, prend en charge le commutateur de session et partage la plomberie de connexion distante/locale.
- Mauvaises qualités : La continuité de session WebChat et le rendu ont un grand registre de régression vécue. L'application native ajoute une autre couche où les portes de credential, le cycle de vie du panneau/fenêtre et l'état du tunnel distant peuvent diverger.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la Qualité.

## Score de Complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Fenêtre WebChat SwiftUI native, Transport de chat Gateway, Réutilisation du plan de données local et distant.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Besoin d'un scénario de reconnexion/sommeil/redémarrage Gateway WebChat natif en direct.
- Besoin d'un test de régression de verrouillage de session pour le rapport de support de gel à une invite.
- Besoin de preuve d'application native que l'état de credential, la connexion de contrôle et l'historique de chat sont chargés sans scintillement ou réinitialisation.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/webchat.md` documente WebChat SwiftUI natif, les modes locaux/distants, le lancement/débogage, les méthodes/événements Gateway, le comportement de session et les limitations connues.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` référence WebChat via tunnel distant et contrôles d'application.
- `/Users/kevinlin/code/openclaw/docs/web/webchat.md` documente le comportement WebChat partagé utilisé par le pont natif.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/WebChatManager.swift` gère les contrôleurs de fenêtre/panneau, la clé de session active, la clé de session préférée et la réinitialisation du tunnel.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/WebChatSwiftUI.swift` implémente `MacGatewayChatTransport`, mappe les poussées Gateway aux événements de chat, crée des fenêtres/panneaux SwiftUI et achemine les contrôles de session/modèle/réflexion.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/GatewayConnection.swift` fournit le transport de requête/événement Gateway partagé.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit` et `OpenClawChatUI` fournissent les modèles/vues de chat partagés.

### Tests d'intégration

- Aucun scénario WebChat en direct d'application native Gateway n'a été trouvé.
- `/Users/kevinlin/code/openclaw/qa/scenarios/channels/webchat-direct-reply-routing.md` couvre le routage de réponse directe WebChat au niveau du canal, pas le panneau d'application native macOS.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/WebChatSwiftUISmokeTests.swift` instancie les contrôleurs de fenêtre et de panneau WebChat avec un transport factice.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/WebChatManagerTests.swift` vérifie le comportement de la clé de session préférée.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/WebChatMainSessionKeyTests.swift` couvre le mappage de clé de session principale.
- `/Users/kevinlin/code/openclaw/ui/src/ui/app-gateway-chat-load.node.test.ts` et les tests d'interface utilisateur connexes couvrent le comportement WebChat côté navigateur, pas le comportement spécifique à l'application native.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS WebChat" --json`

Résultats :

- Problème #54874 `Saisie lente dans l'entrée webchat avec délai de frappe`.
- Problème #64613 `chat.history divulgue les blocs d'injection de mémoire au niveau du système à l'interface utilisateur WebChat`.
- Problème #77136 `WebChat ne parvient pas à rendre certains messages d'assistant`.
- Problème #77012 `La transcription de session WebChat est réécrite à chaque tour`.
- Problème #45952 `Webchat : messages perdus lors de la reconnexion WebSocket`.
- Problème #85771 `L'interface utilisateur WebChat rend les messages d'assistant en double`.
- Problème #87700 `La session webchat de l'interface de contrôle se réinitialise silencieusement après déconnexion/sommeil réseau`.
- Problème #85352 `L'application de barre de menu macOS affiche la porte de credential lors de l'ouverture`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS WebChat"`

Résultats :

- Rapport de support utilisateur du 2026-05-21 : WebChat macOS se verrouille après une invite et nécessite une nouvelle session à chaque message.
- Proposition de test de version du 2026-05-26 inclut les gels WebChat/appel d'outil comme focus de régression.
- Rapport du 2026-05-27 énumère les titres WebChat parmi les sujets fermés les plus importants.
