---
title: Gateway Runtime WebSocket Feature Matrix - Nodes and Remote Capabilities
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: Nodes and remote capabilities
feature_slug: node-transport-and-capability-relay
---

# Nœuds et capacités distantes

## Résumé

OpenClaw dispose d'un vrai transport de nœud dans le plan de contrôle WebSocket de la passerelle. Les nœuds se connectent avec `role: "node"`, déclarent les capacités/commandes/permissions, deviennent visibles via `node.list`/`node.describe`, et reçoivent les événements `node.invoke.request` qui sont complétés avec `node.invoke.result`. La surface de relais couvre les commandes principales de caméra/canevas/écran/localisation/notification/système, le proxy du navigateur, Talk PTT, et les commandes de nœud-hôte du plugin de transfert de fichiers fourni.

L'écart de maturité n'est pas l'existence du plan de contrôle. C'est que le relais de capacité large est inégalement prouvé : les flux d'invocation/liste de nœud de base ont une preuve serveur et e2e, la preuve de capacité Android est en direct/préconditionné, et certains flux hors ligne ou en arrière-plan sont lourd en gestionnaires/unités. Les preuves d'archive montrent également des problèmes répétés dans le monde réel autour des délais d'expiration d'invocation, de la visibilité du travail en attente/appairage, de la publicité des commandes, et de la disponibilité des capacités spécifiques à la plateforme.

## Fonctionnalités

- Présence de nœud : Présence de nœud dans le même plan de contrôle WS que les clients opérateurs.
- Capacités de nœud : Déclaration de capacité de nœud au moment de la connexion.
- Inventaire de nœud : `node.list`, `node.describe`, et visibilité du nommage/état.
- Actions de nœud : `node.invoke` et `node.invoke.result`.
- Événements de nœud : `node.event`, en particulier `node.presence.alive`.
- Livraison de travail en attente : API de travail en attente pour les nœuds connectés et déconnectés.
- Capacités de périphérique distant : Relais des surfaces de capacité distante telles que caméra, canevas, écran, localisation, voix et navigateur.
- Commandes d'hôte distant : Relais des surfaces de capacité de commande d'hôte distant.

## Fraîcheur de l'archive

- `gitcrawl doctor --json`: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json`: `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 84

Étiquette : Oui

Signaux positifs :

- La documentation définit les clients de nœud comme des clients WebSocket sur le même port avec `role: "node"` et des capacités/commandes explicites, et énumère les exemples de caméra/canevas/écran/localisation/voix dans la charge utile de connexion (`docs/gateway/protocol.md:180`, `docs/gateway/protocol.md:196`, `docs/gateway/protocol.md:198`).
- La documentation d'architecture de la passerelle indique que les nœuds se connectent au même serveur WebSocket et exposent `canvas.*`, `camera.*`, `screen.record`, et `location.get` (`docs/concepts/architecture.md:15`, `docs/concepts/architecture.md:40`).
- La documentation du protocole énumère `node.list`, `node.describe`, `node.invoke`, `node.invoke.result`, `node.event`, `node.pending.pull`, `node.pending.ack`, `node.pending.enqueue`, et `node.pending.drain` (`docs/gateway/protocol.md:453`).
- Le schéma de protocole typé couvre les revendications de capacité de nœud, l'invocation/résultat, `node.event`, les charges utiles de présence-vivante, et les formes de drain/enqueue de travail en attente (`src/gateway/protocol/schema/nodes.ts:23`, `src/gateway/protocol/schema/nodes.ts:107`, `src/gateway/protocol/schema/nodes.ts:118`, `src/gateway/protocol/schema/nodes.ts:138`, `src/gateway/protocol/schema/nodes.ts:147`).
- Les gestionnaires de passerelle enregistrent la famille de méthodes de nœud complète via des gestionnaires de base paresseux (`src/gateway/server-methods.ts:482`, `src/gateway/server-methods.ts:490`, `src/gateway/server-methods.ts:501`).
- Un vrai test e2e multi-passerelle démarre deux passerelles, connecte les clients de nœud sur WS, et attend que `node.list` affiche chaque nœud connecté appairé (`test/gateway.multi.e2e.test.ts:27`, `test/helpers/gateway-e2e-harness.ts:129`, `test/helpers/gateway-e2e-harness.ts:203`).
- Les vrais tests de serveur WS couvrent la visibilité des commandes, l'actualisation de l'approbation d'appairage, et les allers-retours `node.invoke`/`node.invoke.result` pour `canvas.snapshot` (`src/gateway/server.roles-allowlist-update.test.ts:437`, `src/gateway/server.roles-allowlist-update.test.ts:446`, `src/gateway/server.roles-allowlist-update.test.ts:567`).
- La suite de capacité en direct Android est préconditionné mais réel : elle se connecte à une passerelle en direct, appelle `node.list`, `node.describe`, et exécute les commandes `node.invoke` annoncées incluant `camera.snap` et `location.get` (`src/gateway/android-node.capabilities.live.test.ts:161`, `src/gateway/android-node.capabilities.live.test.ts:179`, `src/gateway/android-node.capabilities.live.test.ts:517`, `src/gateway/android-node.capabilities.live.test.ts:541`, `src/gateway/android-node.capabilities.live.test.ts:577`).

Signaux négatifs :

- La couverture est la plus forte pour la mécanique de liste/appairage/invocation et plus faible pour chaque famille de capacité individuelle en tant que flux de passerelle réel.
- `node.pending.enqueue`/`node.pending.drain` et le comportement de réveil APNs sont principalement testés par gestionnaire/unité, pas e2e complet avec un nœud physique déconnecté (`src/gateway/server-methods/nodes-pending.test.ts:112`, `src/gateway/server-methods/nodes.invoke-wake.test.ts:591`).
- Les assistants de relais multimédia d'agent et CLI sont bien testés mais principalement via des appels de passerelle simulés, donc ils ne satisfont pas par eux-mêmes la preuve de couverture-Oui pour le transport de passerelle (`src/cli/program.nodes-media.e2e.test.ts:38`, `src/agents/openclaw-tools.camera.test.ts:150`).
- Le proxy du navigateur et le relais de transfert de fichiers sont implémentés via des plugins fournis, mais leur preuve est principalement une couverture d'unité/contrat plus des tests de plugin ciblés, pas un scénario e2e unique de nœud-hôte/navigateur/transfert de fichiers dans cet audit.

Lacunes d'intégration :

- Aucun e2e ne couvre la connexion de nœud -> `node.list`/`node.describe` -> `node.invoke` -> `node.invoke.result` sur les familles caméra/canevas/écran/localisation, proxy du navigateur, Talk PTT, transfert de fichiers, et commandes d'hôte.
- Aucun e2e ne prouve le travail en attente durable pour un nœud hors ligne se reconnectant et drainant le travail en attente après un chemin de réveil.
- La preuve en direct Android est conditionnée par un vrai nœud Android connecté et ne couvre pas la parité iOS/macOS/Windows/Linux pour les mêmes commandes annoncées.
- La présence vivante est documentée et testée par unité, mais le chemin mobile en arrière-plan durable n'est pas prouvé par un réveil en arrière-plan en direct dans cette tranche.

## Qualité

Score: 63

Label: Moyen

Rapports Gitcrawl :

- Requête : `gitcrawl search openclaw/openclaw --query "node.invoke" --mode keyword --limit 20 --json`
  - Résultat : 20 résultats retournés.
  - Signaux de qualité notables : PR ouverte #85916 "fix(gateway): require admin scope for browser proxy invoke"; problèmes fermés #58903 "Disconnected Node causes false 'Rate Limit' errors (node.invoke timeout misclassified)", #5639 "iOS app: node.invoke commands timeout", #17356 "node.invoke intermittent 30s timeout", et demande de fonctionnalité #68090 pour un délai d'expiration `node.invoke` configurable; PR fermées #1357, #1607, #78351, #83976, et PR ouverte #83980 pointent toutes vers des travaux de délai d'expiration d'invocation, résultat tardif, reconnexion ou stabilité des nœuds.
- Requête : `gitcrawl search openclaw/openclaw --query "node.presence.alive" --mode keyword --limit 20 --json`
  - Résultat : 14 résultats retournés.
  - Signaux de qualité notables : PR #73373 et #73330 ajoutent des balises de présence vivante authentifiées; PR ouverte #63123 ajoute le support de balise vivante en arrière-plan iOS; PR #39796 corrige le comportement de socket obsolète lié à la vivacité des battements de cœur.
- Requête : `gitcrawl search openclaw/openclaw --query "node.pending" --mode keyword --limit 20 --json`
  - Résultat : 20 résultats retournés.
  - Signaux de qualité notables : PR #41409 ajoute les primitives de travail de nœud en attente; PR #58179 et PR #55653 corrigent les fuites d'état de travail en attente; les problèmes #6836, #38124, #84642, #17443, #12856, #24998, et #50343 signalent l'invisibilité d'appairage/travail en attente, les délais d'expiration ou les listes en attente vides.
- Requête : `gitcrawl search openclaw/openclaw --query "node.list node.describe" --mode keyword --limit 20 --json`
  - Résultat : 20 résultats retournés.
  - Signaux de qualité notables : problèmes ouverts #51903 (incompatibilité de schéma de l'outil de description des nœuds), #57775 (commandes d'approbation d'exécution Windows non annoncées), et #61569 (ID de nœud personnalisé non respecté); les problèmes fermés #58158/#58159 et #59012 signalent l'absence d'annonce de commande de caméra/microphone.
- Requête : `gitcrawl search openclaw/openclaw --query "camera canvas screen location voice browser node" --mode keyword --limit 20 --json`
  - Résultat : 1 résultat retourné, principalement du bruit (#29416 rapport de schéma invalide qui mentionne le texte de capacité des nœuds).
- Requête : `gitcrawl search openclaw/openclaw --query "file.fetch node host protocol" --mode keyword --limit 20 --json`
  - Résultat : 20 résultats retournés.
  - Signal de qualité notable : PR #74134 ajoute le plugin de transfert de fichiers groupé pour les opérations de fichiers binaires sur les nœuds; la plupart des autres résultats étaient du bruit de chemin/protocole non pertinent.

Rapports Discrawl :

- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.invoke"`
  - Résultat : 10 résultats retournés.
  - Rapports notables : discussion du responsable le 2026-04-28 proposant `file.fetch` / `dir.list` / `dir.fetch` sur `node.invoke`; les messages du miroir GitHub ultérieurs font référence à #58903, #55258, #42590, #46669, et #43287 autour du délai d'expiration, exécution ciblée par nœud, proxy de navigateur et comportement de relais de nœud.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.presence.alive"`
  - Résultat : 3 résultats retournés.
  - Rapports notables : PR #63123 balise vivante en arrière-plan ouverte/commentée/examinée, y compris les commentaires d'examen sur l'accélération de l'horloge murale.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.pending"`
  - Résultat : 10 résultats retournés.
  - Rapports notables : l'examen de PR #61719 avertit de préserver les ID de nœud limités à l'appareil pour les flux de travail en attente; la discussion PR #58179 couvre la correction de fuite mémoire de travail en attente et la preuve de fusion.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.list node.describe"`
  - Résultat : 6 résultats retournés.
  - Rapports notables : un fil "How to best practice for multi agent" demande un comportement d'interface utilisateur de nœud de style Mission-Control et appelle `node.list`, `node.describe`, `node.invoke` générique, capacités/permissions brutes, et boutons courants de canevas/caméra/écran/localisation/système.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "camera canvas screen location voice browser node"`
  - Résultat : `null` (0 résultats retournés).
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "camera.snap screen.record location.get"`
  - Résultat : 1 résultat retourné.
  - Rapport notable : les conseils utilisateur indiquent que les nœuds peuvent exécuter des commandes, envoyer des notifications, prendre des captures d'écran de caméra/enregistrements d'écran, et obtenir la localisation, tout en notant que les cas d'utilisation de bot Discord uniquement n'ont généralement pas besoin de nœuds.

Bonnes qualités :

- La surface du protocole est soutenue par un schéma et enregistrée par méthode, pas du JSON ad hoc (`src/gateway/protocol/schema/nodes.ts:107`, `src/gateway/server-methods.ts:490`).
- `NodeRegistry` maintient les sessions de nœud, les capacités/commandes déclarées/effectives, les promesses d'invocation en attente, les sondes de connectivité, les délais d'expiration et la gestion des résultats tardifs centralisés (`src/gateway/node-registry.ts:153`, `src/gateway/node-registry.ts:397`).
- La passerelle filtre les commandes effectives via la politique de plateforme et les déclarations de nœud avant de les transférer, et les valeurs par défaut dangereuses nécessitent un consentement explicite (`src/gateway/node-command-policy.ts:64`, `src/gateway/node-command-policy.ts:316`, `src/gateway/node-command-policy.ts:398`).
- La visibilité des nœuds fusionne les sessions en direct, l'appairage d'appareil, l'appairage de nœud, les noms, les commandes, les permissions, l'état connecté et les métadonnées `lastSeen` dans un seul catalogue (`src/gateway/node-catalog.ts:90`, `src/gateway/node-catalog.ts:122`).
- La présence vivante est liée à l'appareil authentifié, accélérée et persiste dans les métadonnées d'appairage de nœud/appareil (`src/gateway/server-node-events.ts:847`).
- Les surfaces de relais détenues par les plugins utilisent les mêmes coutures d'invocation de nœud et de politique : le navigateur enregistre `browser.proxy` comme commande de nœud-hôte (`extensions/browser/plugin-registration.ts:57`), et le transfert de fichiers enregistre les commandes de nœud-hôte dangereuses plus une politique d'invocation de nœud (`extensions/file-transfer/index.ts:41`, `extensions/file-transfer/index.ts:88`).

Mauvaises qualités :

- Les preuves d'archive montrent des bogues de fiabilité répétés visibles par l'utilisateur dans la gestion du délai d'expiration/reconnexion de `node.invoke`, la visibilité de l'appairage/travail en attente et l'annonce de commande.
- `node.pending` a deux concepts connexes : l'extraction/accusé de réception d'action de nœud connecté dans `src/gateway/server-methods/nodes.ts` et le drainage/enqueue de travail en attente durable dans `src/gateway/server-methods/nodes-pending.ts`. La distinction est implémentée mais facile à confondre opérationnellement.
- Les types de travail en attente sont actuellement étroits (`status.request` et `location.request`), donc l'API ne modélise pas encore les commandes de nœud déconnecté arbitraires (`src/gateway/protocol/schema/nodes.ts:4`).
- Le relais de navigateur et de transfert de fichiers ajoute des capacités utiles détenues par les plugins, mais la posture de qualité dépend de l'alignement de l'enregistrement, des métadonnées de commande et de la politique locale de chaque plugin avec la politique de nœud de la passerelle.
- Le relais vocal est présent en tant qu'événements/commandes PTT Talk, mais la documentation le rend plus difficile à raisonner que le relais de caméra/canevas/écran/localisation.
- Les preuves source et archive montrent des lacunes d'attentes autour de la sémantique de description de l'outil de nœud, l'annonce de commande d'approbation d'exécution Windows, le respect de l'ID de nœud personnalisé, le comportement du délai d'expiration `node.invoke` configurable et le support de `node.presence.alive` en arrière-plan.

## Lacunes connues

- `node.pending` n'est pas une file d'attente générale de commandes déconnectées durables. L'API de travail durable typée est limitée à `status.request` et `location.request`, tandis que la mise en file d'attente de commandes restreinte au premier plan est une file d'attente d'action en mémoire distincte.
- Il n'existe pas de matrice de compatibilité source/archive unique qui explique la disponibilité du relais par plateforme sur les commandes de caméra, canevas, écran, localisation, voix/Talk, navigateur, transfert de fichiers et hôte.
- Certaines capacités de plateforme restent conditionnelles au produit : la documentation note les exigences de premier plan pour le canevas/caméra et la disponibilité dépendante de la plateforme de `screen.record` (`docs/nodes/index.md:273`, `docs/nodes/index.md:288`).
- Les éléments d'archive ouverts indiquent les lacunes de produit restantes autour de la `describe` de l'outil d'agent, l'annonce de commande d'approbation d'exécution Windows, le respect de l'ID de nœud personnalisé, les délais d'expiration `node.invoke` configurables et la présence vivante en arrière-plan.
- Le fil Discord "How to best practice for multi agent" demande une découverte d'interface utilisateur de nœud qui limite les actions de `hello-ok.features.methods`, affiche les capacités et permissions brutes, fournit `node.invoke` générique et ajoute des boutons pour les commandes courantes de canevas/caméra/écran/localisation/système.

## Preuves

### Docs

- `docs/gateway/protocol.md:180` - exemple de connexion de nœud.
- `docs/gateway/protocol.md:196` - `role: "node"` dans la connexion.
- `docs/gateway/protocol.md:198` - exemple de caps/commands/permissions.
- `docs/gateway/protocol.md:263` - contrat caps/commands/permissions.
- `docs/gateway/protocol.md:274` - section présence avec `node.list`
  `lastSeenAtMs`/`lastSeenReason`.
- `docs/gateway/protocol.md:283` - `node.presence.alive`.
- `docs/gateway/protocol.md:453` - liste des méthodes node pairing/invoke/pending.
- `docs/concepts/architecture.md:15` - les nœuds se connectent via WebSocket.
- `docs/concepts/architecture.md:40` - les nœuds partagent le serveur WS et exposent
  canvas/camera/screen/location.
- `docs/nodes/index.md:10` - les nœuds utilisent le même WebSocket Gateway et `node.invoke`.
- `docs/nodes/index.md:191` - portes de politique de commande de nœud.
- `docs/nodes/index.md:217` - docs snapshot/control de canvas.
- `docs/nodes/index.md:254` - docs photo/vidéo de caméra.
- `docs/nodes/index.md:277` - docs d'enregistrement d'écran.
- `docs/nodes/index.md:293` - docs de localisation.
- `docs/nodes/index.md:368` - notes de liaison system.run et exec-node.
- `docs/nodes/index.md:409` - carte de permissions dans `node.list`/`node.describe`.

### Source

- `src/gateway/protocol/schema/nodes.ts:23` - schéma de charge utile `node.presence.alive`.
- `src/gateway/protocol/schema/nodes.ts:47` - champs de demande d'appairage de nœud.
- `src/gateway/protocol/schema/nodes.ts:93` - schéma de paramètres `node.list`.
- `src/gateway/protocol/schema/nodes.ts:102` - schéma de paramètres `node.describe`.
- `src/gateway/protocol/schema/nodes.ts:107` - schéma de paramètres `node.invoke`.
- `src/gateway/protocol/schema/nodes.ts:118` - schéma de paramètres `node.invoke.result`.
- `src/gateway/protocol/schema/nodes.ts:138` - schéma de paramètres `node.event`.
- `src/gateway/protocol/schema/nodes.ts:147` - schéma de paramètres `node.pending.drain`.
- `src/gateway/protocol/schema/nodes.ts:176` - schéma de paramètres `node.pending.enqueue`.
- `src/gateway/server-methods.ts:482` - enregistrement du gestionnaire paresseux de méthode de nœud.
- `src/gateway/server-methods/nodes.ts:916` - gestionnaire `node.list`.
- `src/gateway/server-methods/nodes.ts:939` - gestionnaire `node.describe`.
- `src/gateway/server-methods/nodes.ts:984` - gestionnaire `node.pending.pull`.
- `src/gateway/server-methods/nodes.ts:1019` - gestionnaire `node.pending.ack`.
- `src/gateway/server-methods/nodes.ts:1046` - gestionnaire `node.invoke`.
- `src/gateway/server-methods/nodes.ts:1346` - gestionnaire `node.event`.
- `src/gateway/server-methods/nodes.handlers.invoke-result.ts:25` -
  gestionnaire `node.invoke.result`.
- `src/gateway/server-methods/nodes-pending.ts:31` -
  gestionnaires `node.pending.drain`/`node.pending.enqueue`.
- `src/gateway/node-registry.ts:153` - registre de nœud connecté.
- `src/gateway/node-registry.ts:397` - transfert d'invocation de nœud.
- `src/gateway/node-catalog.ts:122` - état de nœud fusionné list/describe.
- `src/gateway/server-node-events.ts:847` - persistance d'événement présence alive.
- `src/gateway/node-command-policy.ts:75` - valeurs par défaut de commande de plateforme.
- `src/gateway/node-command-policy.ts:398` - application de liste d'autorisation/commande déclarée.
- `extensions/browser/plugin-registration.ts:57` - commande d'hôte de nœud `browser.proxy`.
- `extensions/browser/src/gateway/browser-request.ts:187` - la route Gateway du navigateur invoque un nœud navigateur.
- `extensions/file-transfer/index.ts:41` - commandes d'hôte de nœud file-transfer.
- `extensions/file-transfer/src/tools/file-fetch-tool.ts:52` - file fetch utilise
  `node.invoke`.

### Tests d'intégration

- `test/gateway.multi.e2e.test.ts:27` - e2e multi-gateway réel avec appairage de nœud.
- `test/helpers/gateway-e2e-harness.ts:129` - l'assistant e2e de connexion de nœud utilise
  le rôle `node`, caps, commands, et l'identité de l'appareil.
- `test/helpers/gateway-e2e-harness.ts:203` - e2e attend l'état connecté/apparié `node.list`.
- `src/gateway/server.node-pairing-authz.test.ts:41` - assistant client WS de nœud réel.
- `src/gateway/server.node-pairing-authz.test.ts:112` - assertion de visibilité de commande `node.list` WS réelle.
- `src/gateway/server.roles-allowlist-update.test.ts:437` - `node.invoke` WS réel vers nœud connecté.
- `src/gateway/server.roles-allowlist-update.test.ts:446` - le nœud envoie
  `node.invoke.result`.
- `src/gateway/server.roles-allowlist-update.test.ts:518` - l'approbation actualise les commandes de nœud en direct puis l'invocation réussit.
- `src/gateway/android-node.capabilities.live.test.ts:506` - suite de capacité de nœud Android en direct.
- `src/gateway/android-node.capabilities.live.test.ts:517` - `node.list` en direct.
- `src/gateway/android-node.capabilities.live.test.ts:541` - `node.describe` en direct.
- `src/gateway/android-node.capabilities.live.test.ts:577` - boucle d'exécution de commande annoncée en direct.

### Tests unitaires

- `src/gateway/server-node-events.test.ts:1269` - persistance présence alive.
- `src/gateway/server-node-events.test.ts:1295` - présence alive rejette l'identité d'appareil authentifiée manquante.
- `src/gateway/server-node-events.test.ts:1352` - limitation de débit présence alive.
- `src/gateway/node-pending-work.test.ts:15` - travail en attente de statut de base.
- `src/gateway/node-pending-work.test.ts:26` - déduplique et reconnaît.
- `src/gateway/node-pending-work.test.ts:67` - élagage d'état en attente.
- `src/gateway/server-methods/nodes-pending.test.ts:62` - gestionnaire drain en attente.
- `src/gateway/server-methods/nodes-pending.test.ts:112` - file d'attente et réveille le nœud déconnecté.
- `src/gateway/server-methods/nodes.invoke-wake.test.ts:506` - le chemin de réveil indisponible conserve la réponse non connectée.
- `src/gateway/server-methods/nodes.invoke-wake.test.ts:591` - réveil APNs puis réessai d'invocation.
- `src/gateway/server-methods/nodes.invoke-wake.test.ts:633` - la commande Talk PTT diffuse `talk.event` canonique.
- `src/gateway/node-command-policy.test.ts:40` - politique de commande plateforme/par défaut.
- `src/gateway/node-registry.test.ts:557` - la mise à jour du registre préserve les commandes déclarées.
- `src/agents/openclaw-tools.camera.test.ts:195` - l'outil caméra d'agent émet `camera.snap`.
- `src/agents/openclaw-tools.camera.test.ts:530` - l'outil de localisation d'agent émet `location.get`.
- `extensions/browser/src/gateway/browser-request.profile-from-body.test.ts:103`
  - la demande de proxy du navigateur invoque `browser.proxy`.
- `extensions/file-transfer/src/shared/lazy-node-invoke-policy.test.ts:38` -
  commandes de politique file-transfer.

### Requêtes Gitcrawl

- `gitcrawl doctor --json`
  - `last_sync_at=2026-05-28T05:29:12.208862Z`,
    `thread_count=87334`, `open_thread_count=7657`,
    `cluster_count=18605`.
- `gitcrawl search openclaw/openclaw --query "node.invoke" --mode keyword --limit 20 --json`
  - 20 résultats ; notables #85916 PR ouvert, #58903, #5639, #17356, #68090, #1357,
    #1607, #78351, #83976, #83980.
- `gitcrawl search openclaw/openclaw --query "node.presence.alive" --mode keyword --limit 20 --json`
  - 14 résultats ; notables #73373, #63123, #73330, #39796.
- `gitcrawl search openclaw/openclaw --query "node.pending" --mode keyword --limit 20 --json`
  - 20 résultats ; notables #41409, #58179, #55653, #6836, #38124, #84642, #17443,
    #12856, #24998, #50343.
- `gitcrawl search openclaw/openclaw --query "node.list node.describe" --mode keyword --limit 20 --json`
  - 20 résultats ; notables #51903, #57775, #61569, #58158, #58159, #59012.
- `gitcrawl search openclaw/openclaw --query "camera canvas screen location voice browser node" --mode keyword --limit 20 --json`
  - 1 résultat ; #29416, principalement bruyant.
- `gitcrawl search openclaw/openclaw --query "file.fetch node host protocol" --mode keyword --limit 20 --json`
  - 20 résultats ; notable #74134.

### Requêtes Discrawl

- `discrawl status --json`
  - `generated_at=2026-05-28T05:47:35Z`, `state=current`,
    `last_sync_at=2026-05-28T00:14:43Z`, `messages=1483985`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.invoke"`
  - 10 résultats ; notable discussion du responsable du 2026-04-28 pour file fetch/list/fetch
    commandes de nœud, plus rapports de miroir GitHub pour #58903, #55258, #42590,
    #46669, et #43287.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.presence.alive"`
  - 3 résultats ; PR #63123 ouvert/commenté/examiné.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.pending"`
  - 10 résultats ; examen d'identité pending-work PR #61719 et discussion de fuite mémoire pending-work PR #58179.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "node.list node.describe"`
  - 6 résultats ; fil de demande/guidance utilisateur pour node UI list/describe/invoke.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "camera canvas screen location voice browser node"`
  - résultat `null`, traité comme 0 résultats.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "camera.snap screen.record location.get"`
  - 1 résultat ; guidance utilisateur listant snapshot caméra, enregistrement d'écran, et exemples de capacité de nœud de localisation.
