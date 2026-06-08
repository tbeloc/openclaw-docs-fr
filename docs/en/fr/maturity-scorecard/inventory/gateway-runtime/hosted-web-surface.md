---
title: Gateway Runtime - Hosted Web Surface Maturity Note
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: Hosted Web Surface
feature_slug: hosted-web-surface
---

# Surface Web hébergée

## Résumé

OpenClaw héberge les surfaces orientées navigateur via le serveur HTTP Gateway,
y compris les routes de ressources/configuration/médias de l'interface de contrôle, le comportement WebChat, les routes web des plugins et les routes du navigateur Canvas/A2UI. La couverture reste forte car les preuves archivées incluent la couverture e2e des médias de l'interface de contrôle, la couverture de la précédence des routes des plugins, les tests Gateway en mode WebChat et les tests d'enregistrement des routes Canvas. La qualité reste Beta car les rapports historiques et ouverts couvrent toujours l'empaquetage de l'interface de contrôle, la précédence/authentification des routes des plugins, la couverture du flux Gateway Canvas/A2UI et la documentation WebChat obsolète.

Scores :

- Couverture : `88` - `Stable`
- Qualité : `74` - `Beta`
- Complétude : `72` - `Beta`

## Fonctionnalités

- Interface de contrôle : Hébergement de l'interface de contrôle sur le serveur Gateway.
- Hébergement WebChat : Hébergement de WebChat.
- Routes web des plugins : Surfaces HTTP Canvas et autres plugins servies par le Gateway.
- Routes Canvas et A2UI : Documents Canvas, transport A2UI et routes des plugins hébergées dans le navigateur sous le serveur HTTP Gateway.

## Couverture

Score : `88`

Signaux positifs :

- La documentation Gateway décrit un port multiplexé qui sert les routes HTTP des plugins et l'interface de contrôle aux côtés du protocole Gateway.
- La documentation de l'interface de contrôle décrit la configuration d'exécution hébergée par Gateway et le comportement WebSocket sur le même port.
- La source ordonne les routes des plugins avant le catch-all de l'interface de contrôle afin que les surfaces web des plugins restent accessibles.
- Les tests couvrent les routes de médias de l'interface de contrôle, le mode Gateway WebChat, la précédence des routes des plugins et l'enregistrement des routes Canvas.

Signaux négatifs :

- La couverture de l'hôte Canvas/A2UI est plus forte aux niveaux d'enregistrement des plugins et d'hôte local qu'à un scénario complet de route/authentification/capacité de nœud du plugin Gateway.
- La documentation WebChat est divisée entre l'ancien langage d'hébergement statique et les descriptions actuelles de chat natif/interface de contrôle.

## Qualité

Score : `74`

Bonnes qualités :

- La propriété des routes est explicite : les routes HTTP intégrées précèdent les routes des plugins, et les routes des plugins précèdent le routage catch-all de l'interface de contrôle.
- Les routes HTTP des plugins ont un comportement d'authentification Gateway fail-closed et une distribution de méthodes délimitée.
- L'interface de contrôle dispose de chemins dédiés pour la configuration d'exécution, les médias d'assistant, l'avatar et la diffusion de fichiers statiques.

Mauvaises qualités :

- L'historique d'archive inclut l'empaquetage de l'interface de contrôle et les problèmes 404.
- L'authentification des routes web des plugins, la précédence et les limites de portée ont fait l'objet de rapports répétés.
- La maturité du navigateur Canvas/A2UI nécessite une preuve de scénario au niveau Gateway.

## Complétude

Score : `72`

Signaux positifs :

- La catégorie capture les surfaces hébergées dans le navigateur séparément des API HTTP appelables, ce qui facilite le scoring indépendant de l'interface de contrôle, WebChat, des routes web des plugins et de Canvas/A2UI.

Branches de capacité manquantes :

- Test Canvas/A2UI au niveau Gateway couvrant l'authentification et le comportement de l'URL de capacité de nœud.
- Documentation WebChat mise à jour qui indique clairement si WebChat est une interface utilisateur statique hébergée, un chat de l'interface de contrôle, un chat natif ou une combinaison.
- Un scénario de surface web co-hébergée prouvant que l'interface de contrôle et les routes web des plugins coexistent sur un Gateway monté à la racine.

## Preuves

- Docs : `docs/gateway/index.md`, `docs/concepts/architecture.md`, `docs/web/control-ui.md`, `docs/web/webchat.md`, `docs/refactor/canvas.md`.
- Source : `src/gateway/server-http.ts`, `src/gateway/control-ui.ts`, `src/gateway/server/plugins-http.ts`, `src/gateway/server-runtime-state.ts`, `src/plugins/registry.ts`, `src/plugin-sdk/gateway-method-runtime.ts`, `extensions/canvas/index.ts`.
- Tests : `src/gateway/control-ui-assistant-media.e2e.test.ts`, `src/gateway/server.chat.gateway-server-chat.test.ts`, `src/gateway/server.plugin-http-auth.test.ts`, `src/gateway/server/plugins-http.test.ts`, `extensions/canvas/index.test.ts`, `extensions/canvas/src/host/server.test.ts`.
- Requêtes d'archive : Problèmes Gateway de l'interface de contrôle, problèmes Gateway des routes HTTP des plugins, problèmes Gateway WebChat et preuves de routes Canvas/A2UI de l'exécution du score archivé.
