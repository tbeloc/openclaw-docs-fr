---
version: 3
---

# Rôles et Permissions

## Résumé

- Famille de fonctionnalités : Rôles et permissions.
- Slug : roles-scopes-and-operator-policy.
- Couverture : 85/100, Oui.
- Qualité : 62/100, Moyen.
- Conclusion : le chemin d'autorisation du protocole et du serveur couvre le modèle central de rôle/portée, y compris la négociation des rôles d'opérateur/nœud, les portées d'opérateur principales, les approbations d'appairage, les déclarations de commandes déclarées par le nœud et les listes blanches côté serveur. La couverture est limitée par l'absence de preuve réelle du serveur pour la portée des événements de diffusion et le comportement de fermeture en cas d'échec pour les familles d'événements inconnues. La qualité reste Moyen en raison des rapports récurrents de réparation de portée et de blocage d'approbation, des régressions de portée d'opérateur ouvertes et de la confusion opérationnelle autour des octrois de portée.

## Fonctionnalités

- Négociation des rôles : négociation des rôles `operator` versus `node`.
- Permissions d'opérateur : Portées d'opérateur principales telles que `operator.read`, `operator.write`, `operator.admin`, `operator.approvals`, `operator.pairing` et `operator.talk.secrets`.
- Actions contrôlées par approbation : Exigences de portée supplémentaires au moment de l'approbation pour l'appairage et les commandes de nœud dangereuses.
- Déclarations de nœud non fiables : `caps`, `commands` et `permissions` déclarés par le nœud en tant que réclamations plutôt que vérité fiable.
- Portée des événements : Portée des événements de diffusion, y compris le comportement de fermeture en cas d'échec pour les familles d'événements inconnues.

## Fraîcheur de l'archive

- `gitcrawl doctor --json` : `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json` : `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 85/100.

Étiquette : Oui.

Signaux positifs :

- Les docs du protocole définissent la poignée de main rôle/portée WebSocket et exposent l'écho rôle/portée dans `hello-ok` (`docs/gateway/protocol.md:10`, `docs/gateway/protocol.md:55`, `docs/gateway/protocol.md:87`).
- Les docs du protocole spécifient les rôles opérateur/nœud, les portées d'opérateur communes, les exemples de portée de méthode, la stratification d'approbation d'appairage de nœud et les caps/commandes/permissions déclarés par le nœud en tant que réclamations non fiables appliquées par les listes blanches Gateway (`docs/gateway/protocol.md:223`, `docs/gateway/protocol.md:245`, `docs/gateway/protocol.md:263`).
- Les docs de portée d'opérateur énoncent le modèle de menace de domaine de confiance local, les exigences de rôle, l'exact/secours administrateur pour les portées futures, la sémantique d'approbation d'appairage et le comportement d'identité de jeton partagé (`docs/gateway/operator-scopes.md:10`, `docs/gateway/operator-scopes.md:19`, `docs/gateway/operator-scopes.md:31`, `docs/gateway/operator-scopes.md:93`, `docs/gateway/operator-scopes.md:110`).
- La source centralise les portées connues et la politique de méthode via `src/gateway/operator-scopes.ts:1`, `src/gateway/method-scopes.ts:31`, `src/gateway/method-scopes.ts:132`, `src/gateway/method-scopes.ts:147` et `src/gateway/methods/core-descriptors.ts:18`.
- Les tests réels Gateway/serveur couvrent l'application des rôles, le comportement de la liste blanche de commandes de nœud, le filtrage des demandes de nœud en attente, l'exposition de commande au moment de l'approbation, les jetons d'opérateur QR/code de configuration limités et l'omission de portée sur l'authentification par jeton partagé (`src/gateway/server.roles-allowlist-update.test.ts:231`, `src/gateway/server.roles-allowlist-update.test.ts:339`, `src/gateway/server.roles-allowlist-update.test.ts:518`, `src/gateway/server.auth.control-ui.suite.ts:1060`, `src/gateway/server.auth.default-token.suite.ts:235`).
- L'application de la portée des événements de diffusion est implémentée et testée unitairement pour les événements d'approbation/appairage, la restriction de lecture de classe de chat, la restriction d'écriture/administration de plugin, le comportement de fermeture en cas d'échec pour les événements inconnus et la séquence contiguë par client après filtrage (`src/gateway/server-broadcast.ts:21`, `src/gateway/server-broadcast.ts:62`, `src/gateway/gateway-misc.test.ts:356`, `src/gateway/gateway-misc.test.ts:405`, `src/gateway/gateway-misc.test.ts:437`, `src/gateway/gateway-misc.test.ts:461`, `src/gateway/gateway-misc.test.ts:534`).

Signaux négatifs :

- Le modèle de portée a des ruptures historiques répétées autour de `operator.admin`, `operator.talk.secrets`, réparation de portée basse et flux d'approbation d'appareil/nœud. Les rapports fermés incluent #56390, #76349, #77195, #79775 et #84144.
- Les rapports gitcrawl ouverts décrivent toujours des régressions ou des blocages de portée d'opérateur : #74484, #77807 et #85966.
- Les preuves d'archive Discord montrent que les mainteneurs et les utilisateurs ont répétitivement eu besoin de clarifications ou de contournements pour les octrois de portée, l'identité d'approbation CLI, l'appairage Docker et l'amorçage de portée de secret Talk.
- La portée de diffusion a de bonnes preuves unitaires, mais aucun test Gateway/WebSocket d'intégration/e2e/en direct situé pour les familles d'événements inconnues ou le filtrage d'événements de plugin sur les clients WebSocket réels.

Lacunes d'intégration :

- Ajouter un test de diffusion Gateway/WebSocket réel qui prouve que les familles d'événements inconnues se ferment, que les clients à portée limitée ne reçoivent pas les événements filtrés et que la séquence par client reste contiguë dans le chemin d'envoi du serveur réel.
- Ajouter un test d'intégration de chemin de récupération pour un jeton d'opérateur appairé à portée basse qui ne peut pas approuver/rejeter une demande de réparation de portée plus large, correspondant à l'ouverture #74484.
- Ajouter un test d'intégration de client Gateway interne ou de génération de session pour la propagation de `operator.write`, correspondant à l'ouverture #77807.
- Ajouter une preuve de régression WebSocket mobile/opérateur ou proxy de confiance pour la gestion des rôles/portées après l'appairage de nœud, correspondant à l'ouverture #85966.

## Qualité

Score: 62/100.

Label: Moyen.

### Rapports Gitcrawl

- Requête : `gitcrawl search issues "AUTH_SCOPE_MISMATCH" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : aucun problème ouvert.
- Requête : `gitcrawl search issues "node.pair.approve operator.pairing" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : #85966 ouvert, « Android UI/operator WebSocket closes silently after node pair approval » ; #62765 ouvert, Teams pairing/dmPolicy report with related unpaired-sender behavior.
- Requête : `gitcrawl search issues "broadcast scoping unknown event families" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : aucun problème ouvert.
- Requête : `gitcrawl search issues "operator.talk.secrets" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : aucun problème ouvert.
- Requête : `gitcrawl search issues "missing scope operator.admin devices approve" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : #74484 ouvert, « Gateway pairing scope deadlock: CLI cannot approve/reject auto-reissued over-scoped repair requests » ; #77807 ouvert, « `sessions_spawn` fails with missing scope `operator.write` despite full-scope operator token ».
- Requête : `gitcrawl search issues "device approve missing scope operator.talk.secrets" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #56390 fermé, « CLI cannot approve device pairing: missing `operator.talk.secrets` scope » ; #77195 fermé, « [2026.5.2 Regression] CLI device lacks operator.admin, creating approval deadlock » ; #52749 fermé, « cli can't connect to gateway ».
- Requête : `gitcrawl search issues "device approve missing scope operator.admin" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : seize résultats, incluant #76349, #77195, #79775, #56173, #55995, #76956, #84144, #21593, #50514, et #46689.
- Requête : `gitcrawl search issues "browser.request operator.admin scope upgrade" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #50640 fermé pour approbation silencieuse automatique des demandes de mise à niveau de portée ; #76956 fermé et #79775 fermé pour les défaillances de portée d'approbation d'appareil ; #80589 fermé pour proxy de confiance `operator.read` ; #78508 fermé pour historique de chat `operator.read` manquant.
- Requête : `gitcrawl search issues "operator scope mismatch gateway" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : vingt résultats, incluant #79292 fermé pour rejet silencieux de portée d'opérateur incompatible, #52085 fermé pour TUI/gateway-client manquant `operator.read`, #17523 fermé pour boucles d'authentification et défaillances de validation de portée, #85966 ouvert, et #78727 fermé pour boucles de demande de mise à niveau de portée.
- Requête : `gitcrawl search issues "node pairing operator.pairing operator.admin" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : vingt résultats, incluant #21470, #55995/#56173, #56390, #65542, #72006, #77195, #79775, et #84144.
- Requête : `gitcrawl search issues "broadcast scoping operator.read" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #57756 fermé, « session-key-based session access is not scoped to the calling operator client/device ».
- Requête : `gitcrawl threads openclaw/openclaw --numbers 74484,77807,85966 --include-closed --json`
  Résultat : #74484 reste ouvert pour un interblocage d'approbation de réparation à faible portée ; #77807 reste ouvert pour `operator.write` manquant dans `sessions_spawn` ; #85966 reste ouvert pour le comportement de fermeture silencieuse du WebSocket Android UI/operator après approbation d'appairage de nœud et demande si `operator.pairing` doit être accordé automatiquement.
- Requête : `gitcrawl threads openclaw/openclaw --numbers 56390,76349,77195,79775,84144 --include-closed --json`
  Résultat : les cinq sont fermés mais documentent les régressions antérieures dans les portées CLI par défaut, l'approbation de propriété/admin d'appareil, et les exigences de portée d'approbation de nœud.

### Rapports Discrawl

- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "operator scopes gateway"`
  Résultat : résultats maintainer-security-ops et clawtributors autour de l'authentification de boucle arrière du backend Gateway et du comportement de secret partagé délimité ; PR #81563 sur `browser.request` nécessitant `operator.admin` ; une note du responsable du 3 mai indiquant que `docs/gateway/operator-scopes.md` a été écrit en raison de la confusion ; rapports de support utilisateur pour `devices approve` manquant `operator.admin` et limites d'appairage Docker CLI.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "node.pair.approve operator.pairing"`
  Résultat : PR #60461 nécessitant `operator.pairing` pour les approbations de nœud ; discussion d'examen autour de l'alignement de portée pairing/write/admin ; notes maintainer-security-ops sur la rotation de jeton d'appareil.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "operator.talk.secrets"`
  Résultat : support mobile/Talk et références PR #85690 pour restaurer `operator.talk.secrets` au bootstrap QR pour iOS/Android ; conseils orientés utilisateur pour inclure `operator.talk.secrets` dans la configuration d'appairage ; problème fermé #60076 sur approbation d'appareil CLI manquant cette portée.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "broadcast scoping operator.read"`
  Résultat : aucun résultat.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "AUTH_SCOPE_MISMATCH"`
  Résultat : fils de support pour Control UI, profils de navigateur, travaux cron VPS, UmbrelOS, et configuration Tailscale avec symptômes de portée manquante ou d'incompatibilité de portée.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "missing scope operator.admin devices approve"`
  Résultat : rapport utilisateur du 2 mai indiquant que `devices approve` a échoué malgré `operator.admin` visible ; défaillance d'approbation Docker CLI ; problème fermé associé #60076 et fils de support pour `operator.admin`/`operator.read`.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "operator.pairing operator.admin"`
  Résultat : discussion utilisateur/responsable sur les portées larges du tableau de bord, les journaux de mise à niveau de portée, et les défaillances d'appairage Docker CLI.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "operator scopes confusion"`
  Résultat : note du responsable indiquant que le document operator-scopes a été créé en raison de la confusion ; préoccupations concernant le cache de portée pertinentes pour la version ; explication Android distinguant les autorisations demandées des portées Gateway accordées.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "broadcast scoping unknown future event"`
  Résultat : aucun résultat.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "node commands claims allowlist"`
  Résultat : discussion macOS node exec/automation indiquant que `gateway.nodes.allowCommands`, les commandes déclarées par nœud, et les approbations exec doivent tous s'aligner ; allowCommands seul ne rend pas une commande supportée.

### Bonnes qualités

- L'autorisation est divisée en petits modules de politique nommés au lieu d'être dispersée dans les gestionnaires : les définitions de portée connues, la recherche de portée de méthode, la gestion des préfixes réservés, la politique de rôle, et les gardes de portée de diffusion sont des fichiers séparés.
- Le serveur refuse par défaut les méthodes non classifiées pour les opérateurs non-administrateurs et traite les familles d'événements futures inconnues comme non livrables sauf si une règle explicite les autorise (`src/gateway/method-scopes.ts:132`, `src/gateway/server-broadcast.ts:62`).
- La sémantique de rôle/portée de base est représentée de manière cohérente dans les documents de protocole, les documents de portée d'opérateur, les portées CLI par défaut, les descripteurs de méthode, et la politique d'autorisation d'exécution (`docs/gateway/protocol.md:223`, `docs/gateway/operator-scopes.md:31`, `src/gateway/operator-scopes.ts:1`, `src/gateway/method-scopes.ts:31`, `src/gateway/methods/core-descriptors.ts:18`).
- La politique d'approbation d'appairage transmet les portées de l'appelant à travers les chemins d'approbation d'appareil et de nœud, incluant les exigences de portée de nœud dérivées de commande (`src/gateway/server-methods/devices.ts:209`, `src/gateway/server-methods/nodes.ts:742`, `docs/gateway/operator-scopes.md:63`, `docs/gateway/operator-scopes.md:93`).
- Le bootstrap de code QR/configuration accorde délibérément un jeton d'opérateur de première exécution limité et exclut la portée admin/appairage, ce qui maintient la transition d'interface de première exécution plus étroite qu'une credential d'opérateur complète (`docs/gateway/protocol.md:150`, `src/gateway/server/ws-connection/message-handler.ts:1168`).
- Les caps/commandes/permissions déclarées par nœud sont réconciliées par la politique côté serveur et l'état d'approbation en attente avant de devenir une surface de nœud en direct effective (`src/gateway/server/ws-connection/message-handler.ts:1545`, `src/gateway/server-methods/nodes.ts:772`).
- Les documents de protocole et de sécurité expliquent maintenant que les portées sont des garde-fous locaux pour un domaine d'opérateur de confiance, pas une autorisation multi-locataire hostile (`docs/gateway/operator-scopes.md:10`, `docs/gateway/security/index.md:8`, `docs/gateway/security/index.md:128`).

### Mauvaises qualités

- Les rapports ouverts montrent que le modèle crée toujours des interblocages de récupération lorsqu'une identité d'opérateur appairée existante a moins de portées qu'une demande de réparation ou de mise à niveau n'en a besoin.
- Il y a un churn historique visible dans les portées CLI/jeton par défaut, en particulier `operator.admin`, `operator.read`, `operator.write`, et `operator.talk.secrets`.
- Les flux de proxy mobile/de confiance et de client Gateway interne ont toujours des problèmes de propagation de portée ouverts ou récemment fermés.
- Les diagnostics de portée sont divisés entre les codes d'erreur, le comportement de fermeture de connexion, l'expérience utilisateur d'appairage, et les documents ; l'historique de support d'archive montre que le modèle reste difficile à raisonner pour les utilisateurs et les responsables.

## Lacunes connues

- #74484 demande un chemin de réparation/bootstrap minimal de rétrogradation afin que la CLI puisse échapper à un interblocage de réparation à faible portée sans suppression manuelle d'identité.
- #77807 demande une propagation de portée fiable pour les chemins internes `sessions_spawn`/Gateway client lorsqu'un jeton d'opérateur à portée complète est disponible.
- #85966 demande un comportement Android UI/operator WebSocket qui ne ferme pas silencieusement après approbation d'appairage de nœud et clarifie si `operator.pairing` doit faire partie de l'ensemble de portée d'opérateur accordé Android.
- Les fils de support Discord demandent des conseils opérationnels plus clairs pour l'appairage Docker/CLI, l'approbation d'appareil avec `operator.admin`, et les clients Talk nécessitant `operator.talk.secrets`.
- Lacune de couverture : la portée de diffusion manque de preuve de flux serveur Gateway/WebSocket réelle localisée pour les événements inconnus et les familles d'événements de plugin.

## Preuve

### Docs

- `docs/gateway/protocol.md:10` indique que la passerelle WebSocket est à la fois un plan de contrôle et un transport de nœud, les clients déclarant leur rôle et leur portée lors de la poignée de main.
- `docs/gateway/protocol.md:55` montre les paramètres de connexion portant `role`, `scopes`, `caps`, `commands`, et `permissions`.
- `docs/gateway/protocol.md:87` montre `hello-ok` retournant le rôle/les portées authentifiés.
- `docs/gateway/protocol.md:150` documente l'amorçage du code QR/setup et les portées de jeton d'opérateur bornées au premier démarrage.
- `docs/gateway/protocol.md:223` définit les rôles et les portées communes.
- `docs/gateway/protocol.md:245` documente les vérifications de portée au niveau de la méthode et au niveau de la commande.
- `docs/gateway/protocol.md:263` documente les capacités déclarées par le nœud comme des réclamations, non comme une vérité de confiance.
- `docs/gateway/protocol.md:314` documente la portée des événements de diffusion et le comportement de fermeture en cas d'échec pour les familles inconnues.
- `docs/gateway/operator-scopes.md:10` définit la limite de sécurité de l'opérateur local de confiance.
- `docs/gateway/operator-scopes.md:31` énumère la sémantique de portée et le comportement de portée future inconnue.
- `docs/gateway/operator-scopes.md:45` explique la portée de la méthode comme la première porte d'autorisation.
- `docs/gateway/operator-scopes.md:93` documente l'approbation d'appairage de nœud et les portées supplémentaires dérivées de commandes.
- `docs/gateway/security/index.md:166` résume les garde-fous de portée d'opérateur et le modèle de passerelle/nœud de confiance.
- `docs/gateway/security/index.md:201` documente les résultats courants qui ne sont intentionnellement pas traités comme des vulnérabilités.

### Source

- `src/gateway/operator-scopes.ts:1` définit les portées d'opérateur connues.
- `src/gateway/method-scopes.ts:31` définit les portées d'opérateur CLI par défaut.
- `src/gateway/method-scopes.ts:132` définit par défaut les méthodes non classifiées pour refuser les opérateurs non-administrateurs.
- `src/gateway/method-scopes.ts:147` autorise les appels de méthode par rapport aux portées d'opérateur.
- `src/gateway/methods/core-descriptors.ts:18` mappe les méthodes de passerelle de base aux rôles/portées.
- `src/shared/gateway-method-policy.ts:1` réserve les préfixes d'administrateur et normalise les portées de méthode de plugin.
- `src/gateway/role-policy.ts:3` analyse et autorise les rôles.
- `src/gateway/server-methods.ts:215` applique l'autorisation de rôle et de portée avant la distribution.
- `src/gateway/server-methods.ts:592` applique la gestion des requêtes, les vérifications de disponibilité au démarrage, la recherche de méthode et la politique de portée d'exécution du plugin.
- `src/gateway/server/ws-connection/message-handler.ts:645` analyse l'état de rôle/portée de la poignée de main.
- `src/gateway/server/ws-connection/message-handler.ts:781` efface les portées non liées lorsque l'authentification par jeton partagé n'a pas d'identité d'appareil.
- `src/gateway/server/ws-connection/message-handler.ts:1095` vérifie l'accès à l'état d'appairage avec le rôle et la portée.
- `src/gateway/server/ws-connection/message-handler.ts:1168` documente le comportement du jeton d'opérateur borné du code de configuration.
- `src/gateway/server/ws-connection/message-handler.ts:1388` valide les mises à niveau de rôle/portée appairées.
- `src/gateway/server/ws-connection/message-handler.ts:1545` réconcilie les réclamations de capacités/commandes/permissions de nœud dans la surface autorisée effective.
- `src/gateway/server-broadcast.ts:21` définit les gardes de portée d'événement.
- `src/gateway/server-broadcast.ts:62` implémente l'autorisation de portée d'événement et le comportement de fermeture en cas d'échec pour les événements inconnus.
- `src/gateway/server-methods/nodes.ts:742` applique les portées de l'appelant lors de l'approbation d'appairage de nœud.
- `src/gateway/server-methods/devices.ts:209` applique les vérifications de rôle/portée de l'appelant lors de l'approbation d'appairage d'appareil.

### Tests d'intégration

- `src/gateway/server.roles-allowlist-update.test.ts:89` installe la suite de serveur Control UI connectée.
- `src/gateway/server.roles-allowlist-update.test.ts:231` prouve l'application du rôle de passerelle sur WebSocket.
- `src/gateway/server.roles-allowlist-update.test.ts:339` prouve le comportement de la liste d'autorisation de commande de nœud via le flux d'invocation/résultat de nœud.
- `src/gateway/server.roles-allowlist-update.test.ts:479` prouve que les commandes déclarées autorisées sont masquées avant l'approbation d'appairage de nœud.
- `src/gateway/server.roles-allowlist-update.test.ts:518` prouve que les commandes en direct sont actualisées après l'approbation d'appairage de nœud en attente.
- `src/gateway/server.roles-allowlist-update.test.ts:587` prouve que les listes d'autorisation actuelles sont revérifiées avant d'exposer les commandes en direct approuvées.
- `src/gateway/server.roles-allowlist-update.test.ts:654` prouve que seules les commandes autorisées sont enregistrées dans les demandes de nœud en attente.
- `src/gateway/server.node-pairing-authz.test.ts:234` prouve que l'approbation de nœud rejette `operator.admin` dérivé de commande manquant et `operator.pairing` manquant via RPC serveur.
- `src/gateway/server.node-pairing-authz.test.ts:315` prouve que les reconnexions appairées demandent un réappairage lorsque des commandes mises à niveau apparaissent.
- `src/gateway/server.auth.control-ui.suite.ts:906` prouve que les mises à niveau de portée Control UI en boucle fermée nécessitent une approbation.
- `src/gateway/server.auth.control-ui.suite.ts:1060` prouve que la remise d'opérateur borné QR/setup-code inclut les approbations/lecture/talk.secrets/écriture et exclut l'administrateur/appairage.
- `src/gateway/server.auth.control-ui.suite.ts:1190` prouve que le jeton d'opérateur borné émis rejette les demandes d'administrateur/appairage.
- `src/gateway/server.auth.default-token.suite.ts:235` prouve que la santé reste disponible mais le statut d'administrateur est restreint lorsque les portées sont vides.
- `src/gateway/server.auth.default-token.suite.ts:246` prouve que `hello-ok` efface les portées pour l'authentification par jeton partagé sans appareil.
- `src/gateway/server.auth.default-token.suite.ts:268` prouve que `hello-ok` rapporte les portées de jeton persistées lors de la réutilisation d'un jeton d'appareil.

### Tests unitaires

- `src/gateway/gateway-misc.test.ts:356` teste le filtrage de diffusion d'approbation/appairage et les diffusions ciblées par portée.
- `src/gateway/gateway-misc.test.ts:405` teste la portée de lecture pour les événements de classe chat.
- `src/gateway/gateway-misc.test.ts:437` teste que les événements de diffusion de plugin sont limités à l'écriture/administrateur.
- `src/gateway/gateway-misc.test.ts:461` teste que les événements inconnus refusent et que les événements de passerelle sont classifiés.
- `src/gateway/gateway-misc.test.ts:534` teste que la séquence d'événement par client récepteur reste contiguë après filtrage.
- `src/gateway/server.node-pairing-authz.test.ts:157` teste les portées requises dérivées de commande dans les assistants d'approbation d'appairage de nœud direct.

### Requêtes Gitcrawl

- `gitcrawl doctor --json`
  Résultat : `last_sync_at=2026-05-28T05:29:12.208862Z`, `thread_count=87334`, `open_thread_count=7657`, `cluster_count=18605`.
- `gitcrawl search issues "AUTH_SCOPE_MISMATCH" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : aucun problème ouvert.
- `gitcrawl search issues "node.pair.approve operator.pairing" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : #85966 ouvert ; #62765 ouvert.
- `gitcrawl search issues "broadcast scoping unknown event families" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : aucun problème ouvert.
- `gitcrawl search issues "operator.talk.secrets" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : aucun problème ouvert.
- `gitcrawl search issues "missing scope operator.admin devices approve" -R openclaw/openclaw --state open --json number,title,url,state`
  Résultat : #74484 ouvert ; #77807 ouvert.
- `gitcrawl search issues "device approve missing scope operator.talk.secrets" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #56390 fermé ; #77195 fermé ; #52749 fermé.
- `gitcrawl search issues "device approve missing scope operator.admin" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : seize résultats, incluant #76349, #77195, #79775, #56173, #55995, #76956, #84144, #21593, #50514, et #46689.
- `gitcrawl search issues "browser.request operator.admin scope upgrade" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #50640 fermé, #76956 fermé, #79775 fermé, #80589 fermé, #78508 fermé, et rapports de portée connexes.
- `gitcrawl search issues "operator scope mismatch gateway" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : vingt résultats, incluant #79292 fermé, #52085 fermé, #17523 fermé, #85966 ouvert, et #78727 fermé.
- `gitcrawl search issues "node pairing operator.pairing operator.admin" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : vingt résultats, incluant #21470, #55995/#56173, #56390, #65542, #72006, #77195, #79775, et #84144.
- `gitcrawl search issues "broadcast scoping operator.read" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #57756 fermé.
- `gitcrawl threads openclaw/openclaw --numbers 74484,77807,85966 --include-closed --json`
  Résultat : #74484 blocage d'approbation de réparation de portée basse ouvert ; #77807 `operator.write` manquant ouvert ; #85966 fermeture WebSocket d'opérateur Android après appairage de nœud ouvert.
- `gitcrawl threads openclaw/openclaw --numbers 56390,76349,77195,79775,84144 --include-closed --json`
  Résultat : les cinq fermés, documentant les régressions antérieures de portée par défaut, d'approbation et d'approbation de nœud.

### Requêtes Discrawl

- `discrawl status --json`
  Résultat : `generated_at=2026-05-28T05:38:34Z`, `state=current`, `last_sync_at=2026-05-28T00:14:43Z`, `messages=1483985`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "operator scopes gateway"`
  Résultat : authentification en boucle fermée/secret partagé de passerelle, `browser.request` `operator.admin`, confusion de documentation de portées d'opérateur, rapports d'approbation d'appareil et d'appairage CLI Docker.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "node.pair.approve operator.pairing"`
  Résultat : PR #60461, discussions d'alignement appairage/écriture/administrateur, et notes de rotation de jeton d'appareil.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "operator.talk.secrets"`
  Résultat : discussions d'amorçage mobile/Talk, PR #85690, conseils utilisateur pour inclure `operator.talk.secrets`, et problème fermé #60076.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "broadcast scoping operator.read"`
  Résultat : aucun résultat.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "AUTH_SCOPE_MISMATCH"`
  Résultat : Control UI, profil navigateur, cron VPS, UmbrelOS, et fils de support Tailscale avec symptômes de portée.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "missing scope operator.admin devices approve"`
  Résultat : rapport utilisateur du 2 mai, échec d'approbation CLI Docker, problème #60076, et fils de support `operator.admin`/`operator.read`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "operator.pairing operator.admin"`
  Résultat : préoccupations de portée du tableau de bord, journaux de mise à niveau de portée, et échecs d'appairage CLI Docker.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "operator scopes confusion"`
  Résultat : documentation de portée créée par le responsable, préoccupations de cache de portée pertinentes à la version, et explication de rôle/portée Android.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "broadcast scoping unknown future event"`
  Résultat : aucun résultat.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "node commands claims allowlist"`
  Résultat : discussions d'exécution/automatisation macOS montrant allowCommands, commandes déclarées, et les approbations doivent s'aligner.
