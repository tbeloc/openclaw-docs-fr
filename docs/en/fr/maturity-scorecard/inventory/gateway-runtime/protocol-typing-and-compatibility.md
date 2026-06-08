---
title: Gateway Runtime WebSocket Feature Matrix - Protocol Compatibility
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: Protocol compatibility
feature_slug: protocol-typing-and-compatibility
---

# Compatibilité des protocoles

## Résumé

OpenClaw dispose d'un contrat de protocole réellement centré sur TypeBox : les formes de requête, réponse, événement, connexion et hello-ok sont définies dans TypeBox, exportées en tant que types TypeScript dérivés, compilées en validateurs d'exécution, et utilisées par la poignée de main Gateway et la distribution des méthodes. Le chemin de génération du modèle de protocole Swift et la garde au niveau du protocole natif montrent un travail intentionnel de compatibilité des clients natifs, et le pont TCP hérité est explicitement documenté comme supprimé en faveur du protocole Gateway WebSocket.

L'écart de maturité concerne moins l'existence d'un contrat typé que le fait que toutes les surfaces de clients générées et externes restent consommables et sans dérive. Les docs locales et les scripts ne s'accordent toujours pas sur les emplacements des artefacts générés, `dist/protocol.schema.json` est généré mais gitignored et absent dans ce checkout, `@openclaw/sdk` est privé, et les preuves d'archive montrent une dérive répétée du modèle Swift, des échecs de vérification de protocole, des demandes de SDK/OpenAPI publiques, et des difficultés de mise à niveau dues à la non-concordance protocole/version.

## Fonctionnalités

- Schéma de protocole publié : TypeBox comme source de vérité du protocole.
- Validation des requêtes à l'exécution : Validateurs d'exécution pour les charges utiles du protocole.
- Export JSON Schema : JSON Schema généré pour les charges utiles du protocole.
- Modèles de client Swift : Génération de modèles Swift.
- Négociation de version : Constantes de protocole actuelles et comportement de plage de protocole supportée.
- Valeurs par défaut du transport client : Valeurs par défaut du client pour les délais d'expiration des requêtes, la reconnexion exponentielle et la gestion des ticks.
- Évolution rétrocompatible : Discipline d'évolution additive pour les nouvelles méthodes, événements ou champs de charge utile.

## Fraîcheur de l'archive

- `gitcrawl doctor --json`: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json`: `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 72

Étiquette : Partielle

Signaux positifs :

- TypeBox est la source de vérité documentée pour le protocole Gateway WebSocket,
  la validation d'exécution, l'export JSON Schema et la génération de code Swift
  (`docs/concepts/typebox.md:8`, `docs/concepts/typebox.md:54`,
  `docs/concepts/typebox.md:64`).
- Les docs d'architecture décrivent la Gateway comme une API WS typée qui valide
  les trames entrantes par rapport à JSON Schema (`docs/concepts/architecture.md:27`,
  `docs/concepts/architecture.md:119`).
- Les docs de protocole documentent la négociation de plage de connexion, les constantes v4 actuelles,
  les commandes de schéma/modèle générées, et les valeurs par défaut du client pour le délai d'expiration des requêtes,
  le délai d'expiration du défi, la reconnexion exponentielle et le délai d'expiration du tick
  (`docs/gateway/protocol.md:641`, `docs/gateway/protocol.md:652`).
- Les schémas d'exécution couvrent les paramètres de connexion, la politique hello-ok, les formes de trame, et
  le comportement strict `additionalProperties: false`
  (`src/gateway/protocol/schema/frames.ts:20`,
  `src/gateway/protocol/schema/frames.ts:73`,
  `src/gateway/protocol/schema/frames.ts:138`).
- Le serveur Gateway valide la requête de connexion initiale et les trames de requête post-poignée de main
  avant la distribution (`src/gateway/server/ws-connection/message-handler.ts:523`,
  `src/gateway/server/ws-connection/message-handler.ts:1891`).
- Une couverture réelle du flux Gateway/serveur existe pour les lignes de base de compatibilité d'authentification,
  le comportement de non-concordance de version de nœud, et les flux SDK sur WebSocket
  (`src/gateway/server.auth.compat-baseline.test.ts:96`,
  `src/gateway/server.node-version-mismatch.test.ts:15`,
  `packages/sdk/src/index.e2e.test.ts:566`).
- Les gardes unitaires/contrats compilent les validateurs exportés et vérifient les constantes de protocole natif
  par rapport à la source de vérité TypeScript
  (`src/gateway/protocol/index.test.ts:46`,
  `src/gateway/protocol/native-protocol-levels.guard.test.ts:56`).

Signaux négatifs :

- La couverture est toujours dominée par les tests de schéma/validateur/garde, pas les flux de bout en bout
  sur chaque surface de client généré et chemin de compatibilité.
- Le générateur Swift écrit actuellement uniquement
  `apps/shared/OpenClawKit/Sources/OpenClawProtocol/GatewayModels.swift`, tandis que
  `package.json` vérifie toujours un chemin inexistant
  `apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`
  (`scripts/protocol-gen-swift.ts:26`, `package.json:1577`).
- Les docs disent que le JSON Schema généré est dans le repo à
  `dist/protocol.schema.json`, mais `.gitignore` ignore ce fichier et le fichier
  est absent dans le checkout actuel (`docs/concepts/typebox.md:290`,
  `.gitignore:196`).
- La garde de compatibilité native vérifie les constantes de protocole Swift et Android au niveau du protocole,
  mais pas une surface de modèle de charge utile Kotlin/Android générée
  (`src/gateway/protocol/native-protocol-levels.guard.test.ts:82`,
  `apps/android/app/src/main/java/ai/openclaw/app/gateway/GatewayProtocol.kt:3`).

Lacunes d'intégration :

- Aucune preuve d'intégration complète trouvée qui régénère JSON Schema et les modèles Swift,
  démarre une Gateway, et pilote les clients générés/natifs et JavaScript
  à travers la même suite de compatibilité.
- Aucune preuve en direct ou e2e trouvée pour la non-concordance de protocole/version N-1 du nœud ; la preuve du flux serveur actuel
  inclut un chemin de rejet de non-concordance à la place
  (`src/gateway/server.node-version-mismatch.test.ts:56`).
- Aucun flux SDK tiers public ou génération OpenAPI/Swagger n'est complet,
  malgré les demandes d'archive pour les deux.

## Qualité

Score : 70

Étiquette : Moyen

Rapports Gitcrawl :

- Requête :
  `gitcrawl search issues "gateway websocket client sdk" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
  a retourné 8 résultats ouverts. Résultat pertinent : #49178
  `[Feature]: Reusable gateway WebSocket client SDK package`, ouvert
  2026-03-17, mis à jour 2026-05-24. Le corps du fil dit que CLI et Control UI
  implémentent indépendamment le même protocole et demande un `@openclaw/gateway-client`
  partagé avec poignée de main, requête/réponse, reconnexion,
  gestion des événements et types TypeScript.
- Requête :
  `gitcrawl threads openclaw/openclaw --numbers 49178 --include-closed --json`
  a retourné le problème #49178 ouvert avec les étiquettes `P2`,
  `clawsweeper:needs-maintainer-review`,
  `clawsweeper:needs-product-decision`, et `impact:security`.
- Requête :
  `gitcrawl search issues "gateway protocol version" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
  a retourné 20 résultats ouverts. Résultats pertinents : #83736
  `[Bug]: Gateway should tolerate minor node version skew during subordinate node upgrades`,
  #49178 SDK WebSocket réutilisable, #85966 Android UI/operator WebSocket se ferme
  silencieusement après l'appairage des nœuds, #74635 battement de cœur rejeté pour propriété inattendue, et plusieurs correspondances sémantiques non liées.
- Requête :
  `gitcrawl threads openclaw/openclaw --numbers 83736 --include-closed --json`
  a retourné le problème #83736 ouvert. Le corps signale qu'une Gateway 2026.5.12 rejette un
  nœud subordonné 2026.5.7 avec le protocole 3 alors que la gateway attendait le protocole
  4, isolant le nœud jusqu'à une réparation hors bande.
- Requête :
  `gitcrawl threads openclaw/openclaw --numbers 85966 --include-closed --json`
  a retourné le problème #85966 ouvert. Le corps signale que le WebSocket de l'opérateur Android
  réessaie de se fermer avec `code=1000 reason=bye` après l'appairage des nœuds, laissant l'application
  dans une boucle de connexion.
- Requête :
  `gitcrawl search issues "protocol schema swift" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
  a retourné 2 résultats ouverts : #87473 et #46664 ; aucun titre n'était directement un
  problème de dérive de modèle Swift.
- Requête :
  `gitcrawl threads openclaw/openclaw --numbers 41476 --include-closed --json`
  a retourné la PR fermée #41476 `build(protocol): regenerate Swift models after
pending node work schemas`, dont le corps dit que les schémas TypeBox ont été ajoutés sans
  exécuter `pnpm protocol:gen:swift`, ce qui a causé l'échec de `protocol:check`
  à l'échelle du dépôt.
- Requête :
  `gitcrawl search issues "bridge protocol removed" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
  a retourné `[]`.
- Requête :
  `gitcrawl search issues "TypeBox gateway protocol" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
  a retourné 2 résultats ouverts : #56068 et #61368 ; aucun titre n'était directement sur
  la dactylographie du protocole Gateway.
- Requête :
  `gitcrawl search issues "Swift GatewayModels" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
  a retourné une correspondance sémantique ouverte, #87132, pas directement sur les
  GatewayModels générés.

Rapports Discrawl :

- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway protocol version"`
  a retourné 10 messages. Les rapports pertinents incluaient une mise à jour bêta du 2026-05-09
  dans `#clawtributors` décrivant les sondes de redémarrage de la gateway frappant à plusieurs reprises
  une incompatibilité de protocole WebSocket, un rapport d'aide Android du 2026-05-19 avec
  `Gateway error: protocol mismatch`, et une note du responsable du 2026-05-24 sur un
  champ de schéma additif avec `GATEWAY_PROTOCOL_VERSION` inchangé.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "TypeBox gateway protocol"`
  a retourné 8 messages. Les rapports pertinents incluaient le problème #33624 restant ouvert
  parce que le projet a une documentation de protocole WebSocket et un générateur
  TypeBox-vers-JSON-Schema mais pas de schéma Swagger/OpenAPI exposé, plus des conseils utilisateur
  pointant les clients personnalisés vers la documentation TypeBox/protocole.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "GatewayModels Swift protocol"`
  a retourné 10 messages, tous matériellement pertinents pour la dérive Swift générée ou
  les échecs de `protocol:check`. Les messages citaient des champs `GatewayModels.swift` obsolètes,
  la régénération manquante après les changements de schéma, et les échecs répétés de vérification de protocole
  sur les PR non liées.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "legacy bridge removed gateway websocket"`
  a retourné un message pertinent du 2026-01-20 : la configuration `bridge` a été supprimée,
  la documentation était obsolète, et les nœuds utilisent maintenant le protocole WebSocket Gateway
  directement.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway websocket client sdk"`
  a retourné 10 messages. Les rapports pertinents incluaient les commentaires du problème #49178 demandant
  un client WebSocket Node/TypeScript consommable, un client inverse-engineered tiers, et des exemples utilisateur
  d'utilisation directe de WS.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "protocol:check GatewayModels"`
  a retourné 10 messages, citant à plusieurs reprises les échecs de `protocol:check` causés par
  les modèles Swift générés obsolètes.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "protocol mismatch gateway expected"`
  a retourné 3 messages, incluant la note de mise à niveau bêta du 2026-05-09 où une
  sonde CLI utilisait le protocole 3 tandis que la gateway attendait le protocole 4.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "openapi schema gateway protocol"`
  a retourné un message pertinent d'archive GitHub pour le problème #33624.

Bonnes qualités :

- Structure TypeBox source-de-vérité claire avec types TS dérivés
  (`src/gateway/protocol/schema/types.ts:1`).
- Les validateurs d'exécution sont compilés paresseusement à partir des schémas TypeBox et exposés en tant que
  validateurs réutilisables (`src/gateway/protocol/index.ts:450`).
- La poignée de main côté serveur et la validation des requêtes échouent fermées sur les
  trames mal formées (`src/gateway/server/ws-connection/message-handler.ts:527`,
  `src/gateway/server/ws-connection/message-handler.ts:1892`).
- Les constantes de version sont centralisées, et les constantes de protocole natif générées
  sont présentes dans l'artefact du modèle Swift (`src/gateway/protocol/version.ts:1`,
  `apps/shared/OpenClawKit/Sources/OpenClawProtocol/GatewayModels.swift:1`).
- Les valeurs par défaut du client pour le délai d'expiration des requêtes, le backoff de reconnexion et la gestion des ticks
  sont explicites dans le code et la documentation (`src/gateway/client.ts:264`,
  `src/gateway/client.ts:1123`, `src/gateway/client.ts:1152`,
  `docs/gateway/protocol.md:657`).
- La suppression du pont TCP hérité est explicite dans la documentation, et l'ancien
  fichier `src/gateway/server-bridge.ts` est absent dans ce checkout
  (`docs/gateway/bridge-protocol.md:10`).

Mauvaises qualités :

- Les preuves d'archive montrent que la dérive Swift générée a à plusieurs reprises cassé
  `protocol:check` et les PR non liées, ce qui réduit la certitude dans la discipline de publication
  autour des changements de schéma/codegen.
- L'arborescence source a des références de surface codegen obsolètes ou contradictoires :
  `package.json` vérifie un chemin généré macOS inexistant, tandis que le générateur Swift
  écrit uniquement le chemin OpenClawKit partagé (`package.json:1577`,
  `scripts/protocol-gen-swift.ts:26`).
- L'artefact JSON Schema est décrit comme généré et hébergé dans le dépôt, mais il est
  ignoré et absent localement, affaiblissant la consommation tierce du contrat de protocole
  (`docs/concepts/typebox.md:292`, `.gitignore:196`).
- La compatibilité du protocole est intentionnellement stricte à la v4 actuelle ; les rapports d'archive
  montrent que cela crée des difficultés de mise à niveau pour les nœuds subordonnés et les sondes de redémarrage.
- Le SDK réutilisable existe uniquement en tant que package d'espace de travail privé `@openclaw/sdk`,
  pas le client Gateway public et agnostique de plateforme demandé par les utilisateurs
  (`packages/sdk/package.json:2`, `packages/sdk/package.json:4`).

## Lacunes connues

- Le SDK client WebSocket Gateway public, réutilisable et agnostique de plateforme reste ouvert
  en tant que #49178 ; le package SDK local est privé. Les résultats de `gateway websocket
client sdk` de Discrawl incluent l'utilisation de clients personnalisés tiers et un
  client inverse-engineered, indiquant une demande pour un chemin de consommation officiel documenté.
- Le schéma OpenAPI/Swagger exposé reste ouvert en tant que #33624 ; le JSON Schema généré
  existe en tant que sortie de script mais n'est pas présent en tant qu'artefact de dépôt engagé/actuel
  dans ce checkout.
- La compatibilité de décalage de version pour les nœuds subordonnés n'est pas complète ; #83736 demande
  une tolérance N-1 ou un chemin RPC de maintenance stable.
- La documentation et les scripts de codegen ont besoin d'un nettoyage autour des chemins générés actuels et de savoir si
  le JSON Schema généré est un artefact engagé, un artefact de construction ou un artefact publié.
- Les résultats de `protocol:check GatewayModels` de Discrawl montrent des frictions responsable/utilisateur
  causées par les modèles Swift générés obsolètes bloquant le travail non lié.

## Preuves

Docs :

- `docs/gateway/protocol.md:10` - Le protocole WS Gateway est le plan de contrôle unique et le transport des nœuds.
- `docs/gateway/protocol.md:641` - versioning, comportement de la plage de protocole et commandes de génération.
- `docs/gateway/protocol.md:657` - tableau des constantes/valeurs par défaut du client.
- `docs/concepts/architecture.md:27` - API WS typée et validation JSON Schema.
- `docs/concepts/typebox.md:8` - TypeBox pilote la validation à l'exécution, l'export JSON Schema et la génération de code Swift.
- `docs/concepts/typebox.md:263` - comportement de la génération de code Swift et compatibilité ascendante des frames inconnues.
- `docs/concepts/typebox.md:297` - flux de travail de changement de schéma.
- `docs/gateway/bridge-protocol.md:10` - suppression du pont TCP hérité.

Source :

- `src/gateway/protocol/version.ts:1` - constantes de protocole actuelles.
- `src/gateway/protocol/schema/frames.ts:20` - `ConnectParamsSchema`.
- `src/gateway/protocol/schema/frames.ts:73` - `HelloOkSchema` et champs de politique.
- `src/gateway/protocol/schema/frames.ts:138` - schémas de frames de requête/réponse/événement.
- `src/gateway/protocol/schema/protocol-schemas.ts:282` - registre `ProtocolSchemas`.
- `src/gateway/protocol/schema/types.ts:1` - types TypeScript dérivés avec `Static`.
- `src/gateway/protocol/index.ts:450` - compilation paresseuse du validateur TypeBox.
- `src/gateway/server/ws-connection/message-handler.ts:523` - validation du frame de connexion initial.
- `src/gateway/server/ws-connection/message-handler.ts:614` - négociation de la plage de protocole et gestion des incompatibilités.
- `src/gateway/server/ws-connection/message-handler.ts:1822` - la politique hello-ok annonce les limites de charge utile et de tick.
- `src/gateway/client.ts:298` - valeur par défaut du délai d'expiration de la requête.
- `src/gateway/client.ts:591` - le client stocke l'intervalle de tick annoncé depuis hello-ok.
- `src/gateway/client.ts:1123` - comportement de backoff de reconnexion.
- `src/gateway/client.ts:1152` - watchdog de tick.
- `scripts/protocol-gen.ts:9` - génération de JSON Schema.
- `scripts/protocol-gen-swift.ts:26` - chemin de sortie généré Swift.
- `apps/shared/OpenClawKit/Sources/OpenClawProtocol/GatewayModels.swift:1` - fichier Swift généré.
- `apps/android/app/src/main/java/ai/openclaw/app/gateway/GatewayProtocol.kt:3` - constantes de protocole Android.
- `.gitignore:196` - le JSON Schema généré est ignoré.
- `package.json:1577` - commande `protocol:check` et chemin généré macOS obsolète.

Tests d'intégration :

- `src/gateway/server.auth.compat-baseline.test.ts:96` - suite de compatibilité de base d'authentification du serveur réel.
- `src/gateway/server.node-version-mismatch.test.ts:15` - test du serveur pour la garde de non-concordance de version de nœud local.
- `packages/sdk/src/index.e2e.test.ts:363` - SDK WebSocket e2e avec Gateway factice.
- `packages/sdk/src/index.e2e.test.ts:566` - chemin e2e SDK Gateway réel.

Tests unitaires :

- `src/gateway/protocol/index.test.ts:46` - les validateurs paresseux exportés valident et conservent les erreurs lisibles.
- `src/gateway/protocol/index.test.ts:73` - tous les validateurs de protocole exportés se compilent.
- `src/gateway/protocol/native-protocol-levels.guard.test.ts:56` - garde de niveau de protocole natif.
- `src/gateway/protocol/channels.schema.test.ts:5` - tests de compilation et de validation du schéma de canal.
- `src/gateway/protocol/schema/agent.test.ts:37` - validation stricte de la charge utile TypeBox pour les paramètres d'agent.
- `src/gateway/protocol/exec-approvals-validators.test.ts:8` - validateurs de protocole d'approbation d'exécution.
- `src/gateway/client.test.ts:930` - le client JS annonce la plage de compatibilité de protocole par défaut.
- `src/gateway/client.test.ts:1524` - le client JS arrête les boucles de reconnexion en cas d'échecs de connexion d'authentification/style de protocole non récupérables.

Requêtes Gitcrawl :

- `gitcrawl doctor --json`
- `gitcrawl search issues "gateway websocket client sdk" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
- `gitcrawl threads openclaw/openclaw --numbers 49178 --include-closed --json`
- `gitcrawl search issues "gateway protocol version" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
- `gitcrawl threads openclaw/openclaw --numbers 83736 --include-closed --json`
- `gitcrawl threads openclaw/openclaw --numbers 85966 --include-closed --json`
- `gitcrawl search issues "protocol schema swift" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
- `gitcrawl threads openclaw/openclaw --numbers 41476 --include-closed --json`
- `gitcrawl search issues "bridge protocol removed" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
- `gitcrawl search issues "TypeBox gateway protocol" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`
- `gitcrawl search issues "Swift GatewayModels" -R openclaw/openclaw --state open --json number,title,url,state,createdAt,updatedAt`

Requêtes Discrawl :

- `discrawl status --json`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway protocol version"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "TypeBox gateway protocol"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "GatewayModels Swift protocol"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "legacy bridge removed gateway websocket"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway websocket client sdk"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "protocol:check GatewayModels"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "protocol mismatch gateway expected"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "openapi schema gateway protocol"`
