---
title: "Sécurité, authentification, appairage et secrets - Note de maturité de l'appairage des appareils et des nœuds"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de maturité de l'appairage des appareils et des nœuds

## Résumé

L'identité de l'appareil et l'appairage de l'opérateur sont implémentés comme une véritable surface du plan de contrôle de la passerelle, et non simplement comme de la documentation. Le code actuel signe les identités d'appareil liées à des nonces, émet des jetons d'amorçage de code de configuration, crée des demandes d'appairage d'appareil en attente, émet des jetons d'appareil par rôle, réutilise les jetons stockés lors de la reconnexion, fait tourner et révoque les jetons dans les limites de rôle/portée approuvées, et traite spécialement les flux locaux de l'interface utilisateur de contrôle/WebChat et du backend.

La couverture est Stable car les tests réels de la passerelle/serveur exercent les flux d'exécution les plus importants : appairage automatique de l'interface utilisateur de contrôle local, remise d'amorçage par code QR/configuration, réutilisation et révocation des jetons d'appareil, rotation d'authentification partagée, autorisation de rotation/révocation des jetons d'appareil, approbation automatique d'appairage de nœud et appairage de nœud multi-passerelle. La qualité est Bêta car la source est consciente de la sécurité et bien documentée, mais les archives actualisées montrent toujours des défaillances d'appairage ouvertes, des rapports de course de code de configuration, des blocages de portée, une confusion mobile/nœud, des limites de débit manquantes et des difficultés de récupération côté opérateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Codes de configuration : Codes de configuration et UX d'appairage QR pour l'intégration mobile/nœud via le plugin device-pair
- Création d'identité d'appareil : Création d'identité d'appareil, stockage, identifiants d'appareil dérivés de clé publique, signature de défi et vérification du serveur
- Émission de jetons d'appareil : Émission de jetons d'appareil, réutilisation de reconnexion, récupération de non-concordance de jetons, rotation de jetons, révocation de jetons et nettoyage de jetons obsolètes
- Approbations d'appairage d'appareil pour l'opérateur : Approbations d'appairage d'appareil pour les rôles d'opérateur et de nœud, y compris les demandes en attente, les mises à niveau de rôle/portée et les demandes de réparation
- Portées d'opérateur qui contrôlent l'appairage : Portées d'opérateur qui contrôlent l'appairage, la gestion des jetons d'appareil, l'appairage de nœud et les approbations de rôle/portée à risque plus élevé
- Interface utilisateur de contrôle local : Interface utilisateur de contrôle local, WebChat, proxy de confiance et comportement d'appairage automatique ou d'exception sans appareil où cela affecte l'appairage de l'opérateur
- Migration d'authentification : Migration d'authentification et erreurs de récupération pour la signature d'appareil pré-défi, la dérive de jetons, la non-concordance de portée et la configuration d'authentification de passerelle mixte
- Documentation côté opérateur : Documentation côté opérateur pour les appareils, l'appairage, WebChat, l'interface utilisateur de contrôle, l'authentification du protocole et le dépannage
- Appairage de nœud : Couvre l'appairage de nœud sur l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud et le comportement d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance associé.
- Confiance de capacité : Couvre la confiance de capacité sur l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud et le comportement d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance associé.
- Approbations d'exécution à distance : Couvre les approbations d'exécution à distance sur l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud et le comportement d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance associé.

## Fonctionnalités

- Codes de configuration : Codes de configuration et UX d'appairage QR pour l'intégration mobile/nœud via le plugin device-pair
- Création d'identité d'appareil : Création d'identité d'appareil, stockage, identifiants d'appareil dérivés de clé publique, signature de défi et vérification du serveur
- Émission de jetons d'appareil : Émission de jetons d'appareil, réutilisation de reconnexion, récupération de non-concordance de jetons, rotation de jetons, révocation de jetons et nettoyage de jetons obsolètes
- Approbations d'appairage d'appareil pour l'opérateur : Approbations d'appairage d'appareil pour les rôles d'opérateur et de nœud, y compris les demandes en attente, les mises à niveau de rôle/portée et les demandes de réparation
- Portées d'opérateur qui contrôlent l'appairage : Portées d'opérateur qui contrôlent l'appairage, la gestion des jetons d'appareil, l'appairage de nœud et les approbations de rôle/portée à risque plus élevé
- Interface utilisateur de contrôle local : Interface utilisateur de contrôle local, WebChat, proxy de confiance et comportement d'appairage automatique ou d'exception sans appareil où cela affecte l'appairage de l'opérateur
- Migration d'authentification : Migration d'authentification et erreurs de récupération pour la signature d'appareil pré-défi, la dérive de jetons, la non-concordance de portée et la configuration d'authentification de passerelle mixte
- Documentation côté opérateur : Documentation côté opérateur pour les appareils, l'appairage, WebChat, l'interface utilisateur de contrôle, l'authentification du protocole et le dépannage
- Appairage de nœud : Couvre l'appairage de nœud sur l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud et le comportement d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance associé.
- Confiance de capacité : Couvre la confiance de capacité sur l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud et le comportement d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance associé.
- Approbations d'exécution à distance : Couvre les approbations d'exécution à distance sur l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud et le comportement d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance associé.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs :
  - Les tests réels de la passerelle couvrent l'appairage automatique de l'opérateur de l'interface utilisateur de contrôle local et le comportement de mise à niveau de portée (`src/gateway/server.auth.control-ui.suite.ts:848`, `src/gateway/server.auth.control-ui.suite.ts:1588`).
  - Les tests réels de la passerelle couvrent l'amorçage QR/code de configuration, la remise de jetons nœud/opérateur limitée, l'approbation de mise à niveau de rôle d'amorçage, le rejet d'amorçage non-baseline et le rejet de jetons d'appareil révoqués (`src/gateway/server.auth.control-ui.suite.ts:1031`, `src/gateway/server.auth.control-ui.suite.ts:1451`, `src/gateway/server.auth.control-ui.suite.ts:1543`, `src/gateway/server.auth.control-ui.suite.ts:1840`).
  - Les tests d'exécution couvrent la rotation d'authentification partagée préservant les sessions de jetons d'appareil valides et la déconnexion des sessions étiquetées par l'émetteur après la rotation de jetons partagés (`src/gateway/server.shared-auth-rotation.test.ts:187`, `src/gateway/server.shared-auth-rotation.test.ts:203`, `src/gateway/server.shared-auth-rotation.test.ts:217`, `src/gateway/server.shared-auth-rotation.test.ts:246`).
  - Les tests d'autorisation d'exécution couvrent le refus de rotation/révocation inter-appareils de jetons d'appareil, la rotation/révocation inter-appareils d'administrateur, les protections de jetons de rôle de nœud et les gardes de portée d'approbation d'appareil (`src/gateway/server.device-token-rotate-authz.test.ts:188`, `src/gateway/server.device-token-rotate-authz.test.ts:237`, `src/gateway/server.device-token-rotate-authz.test.ts:279`, `src/gateway/server.device-pair-approve-authz.test.ts:169`).
  - Les tests d'exécution couvrent le comportement d'appairage de nœud CIDR de confiance et les portées d'approbation d'appairage de nœud (`src/gateway/server.node-pairing-auto-approve.test.ts:88`, `src/gateway/server.node-pairing-auto-approve.test.ts:122`, `src/gateway/server.node-pairing-authz.test.ts:157`).
  - La couverture E2E démarre deux passerelles et exerce WS, les hooks HTTP et l'appairage de nœud (`test/gateway.multi.e2e.test.ts:27`).
- Signaux négatifs :
  - La couverture est la plus forte dans les tests réels locaux/d'exécution du serveur ; cet audit n'a pas trouvé de preuve en direct fraîche pour iOS, Android, Tailscale Serve, Docker, NAS ou le cycle de vie d'appairage de proxy inverse public.
  - L'appairage automatique spécifique à WebChat et la persistance des jetons d'appareil sont principalement couverts par les chemins de code partagés Control UI/Gateway et les tests d'aide/unité plutôt que par un flux d'appairage E2E WebChat dédié.
  - Les chemins de code de configuration et d'amorçage ont des tests d'exécution solides, mais les résultats des archives incluent toujours des rapports de course de code de configuration ouverts, donc le signal de support d'intégration n'est pas Lovable.
- Lacunes d'intégration :
  - Ajouter une preuve de code de configuration mobile en direct pour iOS et Android sur `wss://`, LAN privé `ws://` et Tailscale Serve.
  - Ajouter un E2E d'appairage/reconnexion WebChat dédié qui prouve l'identité de l'appareil, la réutilisation du jeton d'appareil stocké et la récupération de mise à niveau de portée à partir du flux visible du navigateur.
  - Ajouter un test de fumée d'appairage de passerelle Docker/NAS/non-macOS pour les chemins de preuve-réponse et de nonce de connexion actuels.
  - Fermer la preuve de course de code de configuration autour de la relance de jetons d'amorçage consommés avant de traiter la couverture QR/code de configuration comme Lovable.

## Score de Qualité

- Score : `Beta (73%)`
- Rapports Gitcrawl :
  - Les problèmes ouverts montrent le risque actuel affectant l'opérateur : Échec d'appairage de réponse de preuve Trim OS/TerraMaster (#86778), blocage de portée pour les demandes de réparation CLI approve/reject (#74484), fermeture Android UI/opérateur après appairage de nœud (#85966), course de code de configuration réouvrant les jetons d'amorçage consommés (#78276), préoccupation concernant le contournement d'auto-appairage du backend (#72418), course Android zero-command/connect-nonce (#87058), et conseils manquants sur les erreurs d'appairage (#67618).
  - Les PR ouvertes montrent un travail de renforcement actif plutôt qu'un comportement établi : actualisation de la dernière visite de l'appareil appairé (#81189), limitation de débit pour les RPC de gestion d'appairage/jeton d'appareil (#84617), liaison de jeton d'amorçage (#80896), liaison de code de configuration aux approbations de nœud (#46794), correction de course de code de configuration (#78277), et authentification d'appairage mobile LAN privé (#78807).
  - L'historique d'archive montre également des lacunes de produit autour de l'isolation de jeton de passerelle multi-utilisateur (#43903), appairage mobile de style invitation (#55914), séparation d'identité service/utilisateur (#69066), et portées de jeton de passerelle configurables (#80836).
- Rapports Discrawl :
  - Les résultats récents du support Discord incluent les utilisateurs et les responsables diagnostiquant `appairage requis`, boucles de mise à niveau de portée, identités d'appareil obsolètes, contexte d'approbation hôte/invité Docker, échecs de configuration QR/TLS mobile, confusion d'appairage WebChat/Control UI, et boucles de jeton d'amorçage obsolète.
  - La discussion des responsables souligne les identités `gateway-client` internes obsolètes causant des échecs de mise à niveau de portée pour les approbations natives, tandis que plusieurs fils d'aide utilisateur acheminent toujours les gens à travers les flux de travail `openclaw devices list`, `approve`, `rotate`, ou réinitialisation d'identité.
  - La communauté confond régulièrement l'appairage de nœud, l'appairage d'opérateur, l'appairage DM/canal, et l'appairage WebChat/Control UI, ce qui montre que le modèle mental de l'opérateur reste difficile même si la documentation couvre maintenant les flux.
- Bonnes qualités :
  - L'identité de l'appareil utilise des ID dérivés de clé publique et des signatures liées à nonce sur les chemins CLI/natif et Control UI du navigateur (`src/infra/device-identity.ts:219`, `src/infra/device-identity.ts:278`, `src/infra/device-identity.ts:317`, `ui/src/ui/device-identity.ts:61`, `ui/src/ui/device-identity.ts:109`).
  - L'authentification du serveur sépare l'authentification partagée, les jetons d'amorçage et les jetons d'appareil, et préfère l'authentification d'amorçage explicite lorsque la remise QR/code de configuration a besoin de cette classification (`src/gateway/server/ws-connection/auth-context.ts:98`, `src/gateway/server/ws-connection/auth-context.ts:188`).
  - L'approbation d'appairage, l'approbation d'amorçage, l'émission de jeton, la rotation et la révocation restent limitées aux rôles approuvés et aux portées de l'appelant (`src/infra/device-pairing.ts:617`, `src/infra/device-pairing.ts:734`, `src/infra/device-pairing.ts:924`, `src/infra/device-pairing.ts:988`, `src/infra/device-pairing.ts:1077`, `src/infra/device-pairing.ts:1138`).
  - Les portées d'amorçage de code de configuration sont sur liste blanche et excluent intentionnellement `operator.admin` et `operator.pairing` (`src/shared/device-bootstrap-profile.ts:13`, `src/shared/device-bootstrap-profile.ts:22`, `src/shared/device-bootstrap-profile.ts:46`).
  - La logique de reconnexion du client stocke les jetons d'appareil, réutilise les portées mises en cache uniquement lors de la réutilisation des jetons mis en cache, efface les jetons stockés obsolètes en cas de non-concordance de jeton d'appareil, et limite les tentatives de non-concordance de jeton partagé aux points de terminaison de confiance (`src/gateway/client.ts:581`, `src/gateway/client.ts:605`, `src/gateway/client.ts:802`, `src/gateway/client.ts:877`, `src/gateway/client.ts:929`, `src/gateway/client.ts:948`).
  - La documentation de l'opérateur est inhabituellement explicite sur les portées d'appairage, la sécurité du code de configuration, la récupération de la dérive de jeton, l'approbation automatique locale de Control UI, et les diagnostics de migration d'authentification (`docs/gateway/protocol.md:150`, `docs/gateway/protocol.md:692`, `docs/gateway/protocol.md:754`, `docs/cli/devices.md:123`, `docs/gateway/troubleshooting.md:384`, `docs/web/control-ui.md:61`).
- Mauvaises qualités :
  - Le contrat de sécurité est complexe et dépend de la préservation des invariants sur l'identité de l'appareil, l'état d'amorçage, la génération d'authentification partagée, la poignée de main WebSocket, l'état d'appairage d'appareil, l'état d'appairage de nœud, le stockage local de Control UI, et le comportement de secours CLI.
  - Il y a encore des problèmes de qualité ouverts dans les domaines sensibles à la sécurité : courses de code de configuration, limites de débit de gestion d'appairage/jeton, blocages de portée d'appairage, échec de réponse de preuve sur un OS NAS, et contournement possible d'auto-appairage du backend.
  - L'UX de l'opérateur reste difficile : les archives montrent une confusion répétée entre les rôles de nœud et d'opérateur, non-concordance de jeton d'appareil par rapport à non-concordance de portée, secours Docker local, appairage Control UI/WebChat, et appairage DM/canal.
  - Le comportement de migration et de récupération d'authentification est documenté, mais les clients plus anciens et les identités obsolètes produisent toujours des échecs `appairage requis` et de mise à niveau de portée à friction élevée dans les fils de support réels.
- Exclu de la qualité :
  - L'étendue des tests unitaires, d'intégration, e2e, en direct et en temps réel n'a pas été utilisée pour augmenter ou diminuer la Qualité. Les preuves de test sont utilisées uniquement dans la Couverture.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : la documentation archivée, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les Codes de configuration, la Création d'identité d'appareil, l'Émission de jeton d'appareil, les Approbations d'appairage d'appareil pour l'opérateur, les Portées d'opérateur qui contrôlent l'appairage, le Control UI local, la Migration d'authentification, la Documentation orientée opérateur, l'Appairage de nœud, la Confiance de capacité, les Approbations d'exécution à distance.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Fermer la gestion de la course du code de configuration pour les jetons d'amorçage consommés (#78276/#78277) et prouver le résultat par rapport aux flux de nouvelle tentative et de reconnexion QR/code de configuration.
- Terminer la limitation de débit ou les contrôles d'abus équivalents pour l'appairage d'appareil et les RPC de gestion de jeton (#84617).
- Résoudre ou rétrograder explicitement l'échec actuel de réponse de preuve sur Trim OS/TerraMaster NAS (#86778).
- Clarifier ou corriger les blocages de portée d'appairage pour les flux de réparation/approbation CLI (#74484) et les échecs d'identité `gateway-client` interne obsolète discutés dans discrawl.
- Ajouter des affordances orientées opérateur pour les flux de travail d'appairage de style list-approved/revoke/invite (#56621/#55914) s'ils restent des objectifs de produit.
- Améliorer la copie de rôle/portée où les utilisateurs confondent l'appairage de nœud avec l'appairage d'opérateur, en particulier pour Android/iOS et Control UI/WebChat.
- Renforcer l'isolation de jeton multi-utilisateur et la séparation d'identité de service, ou documenter la limite de confiance d'opérateur unique plus en évidence (#43903/#69066).
- Ajouter une preuve d'appairage mobile en direct, Tailscale Serve, Docker/NAS, et navigateur distant avant de relever la Couverture en Lovable.

## Preuves

### Docs

- `docs/gateway/protocol.md:27` documente la négociation de défi/réponse de connexion avec `connect.challenge`.
- `docs/gateway/protocol.md:118` documente `hello-ok.auth` avec et sans jetons d'appareil.
- `docs/gateway/protocol.md:150` documente l'amorçage par code QR/configuration retournant un jeton de nœud principal plus un jeton d'opérateur limité.
- `docs/gateway/protocol.md:692` documente l'émission de jeton d'appareil, la persistance, la réutilisation de la portée de reconnexion et la précédence d'authentification.
- `docs/gateway/protocol.md:718` documente le comportement retentable `PAIRING_REQUIRED` tandis que l'amorçage par code de configuration non-baseline attend l'approbation.
- `docs/gateway/protocol.md:727` documente les exigences de portée de rotation/révocation de jeton d'appareil et la mutation de jeton limité.
- `docs/gateway/protocol.md:754` documente l'identité de l'appareil, les limites d'approbation automatique locale, les exceptions sans appareil et les exigences de nonce signé.
- `docs/gateway/protocol.md:783` documente les diagnostics de migration d'authentification d'appareil pour les clients hérités.
- `docs/cli/devices.md:51` documente l'approbation exacte de l'ID de demande, les aperçus de mise à niveau et l'examen de la portée/rôle.
- `docs/cli/devices.md:123` documente la rotation du jeton d'appareil.
- `docs/cli/devices.md:145` documente la révocation du jeton d'appareil.
- `docs/cli/devices.md:194` documente la récupération de dérive de jeton.
- `docs/channels/pairing.md:111` documente Telegram `/pair`, code de configuration, balayage QR et approbation.
- `docs/channels/pairing.md:119` documente le contenu de la charge utile du code de configuration et l'objectif du jeton d'amorçage.
- `docs/channels/pairing.md:126` documente les portées de remise QR/code de configuration limitées.
- `docs/channels/pairing.md:167` documente l'approbation automatique de nœud CIDR de confiance et exclut l'approbation automatique d'opérateur/navigateur/Interface de contrôle/WebChat.
- `docs/gateway/pairing.md:10` documente l'appairage détenu par Gateway et la distinction entre appairage d'appareil et appairage de nœud.
- `docs/gateway/pairing.md:125` documente l'approbation automatique d'appareil CIDR de confiance.
- `docs/gateway/pairing.md:153` documente l'approbation automatique de mise à niveau des métadonnées.
- `docs/gateway/operator-scopes.md:31` documente les niveaux de portée d'opérateur.
- `docs/gateway/operator-scopes.md:63` documente les vérifications au moment de l'approbation d'appairage d'appareil.
- `docs/web/control-ui.md:61` documente l'approbation automatique de l'Interface de contrôle en boucle locale et les exigences d'appairage à distance/Tailnet.
- `docs/web/control-ui.md:480` documente la gestion des fragments de jeton, le comportement de mémoire uniquement du mot de passe et les exigences explicites de credentials d'interface utilisateur à distance.
- `docs/web/webchat.md:73` documente les options d'authentification WebChat/Gateway incluant jeton, mot de passe, Tailscale, proxy de confiance et credentials à distance.

### Source

- `src/infra/device-identity.ts:219` charge ou crée l'identité d'appareil CLI/natif persistée.
- `src/infra/device-identity.ts:278` signe les charges utiles d'authentification d'appareil.
- `src/infra/device-identity.ts:299` dérive les ID d'appareil à partir des clés publiques.
- `src/infra/device-identity.ts:317` vérifie les signatures d'appareil.
- `ui/src/ui/device-identity.ts:61` charge ou crée l'identité d'appareil de l'Interface de contrôle du navigateur dans le stockage local.
- `ui/src/ui/device-identity.ts:109` signe les charges utiles d'appareil de l'Interface de contrôle du navigateur.
- `ui/src/ui/device-auth.ts:42` charge les jetons d'appareil du navigateur stockés.
- `ui/src/ui/device-auth.ts:53` stocke les jetons d'appareil du navigateur.
- `ui/src/ui/control-ui-auth.ts:23` préfère `hello.auth.deviceToken` au jeton/mot de passe configuré pour l'authentification HTTP de l'Interface de contrôle.
- `src/gateway/device-auth.ts:36` construit les charges utiles d'authentification d'appareil v3 avec les champs de plateforme et de famille d'appareil.
- `src/gateway/server/ws-connection/auth-context.ts:98` résout les candidats de jeton partagé, d'amorçage et d'appareil.
- `src/gateway/server/ws-connection/auth-context.ts:188` vérifie les jetons d'amorçage avant le secours au jeton d'appareil.
- `src/gateway/server/ws-connection/auth-context.ts:210` vérifie les candidats de jeton d'appareil et mappe les défaillances.
- `src/gateway/server/ws-connection/message-handler.ts:668` détecte les clients Interface de contrôle, interface utilisateur du navigateur, WebChat et application native.
- `src/gateway/server/ws-connection/message-handler.ts:970` résout l'authentification de connexion finale et l'état de génération du jeton d'appareil.
- `src/gateway/server/ws-connection/message-handler.ts:1150` décide de l'appairage silencieux local et de l'approbation automatique de nœud CIDR de confiance.
- `src/gateway/server/ws-connection/message-handler.ts:1191` limite l'appairage d'amorçage QR/code de configuration silencieux au profil de configuration exact.
- `src/gateway/server/ws-connection/message-handler.ts:1210` crée des demandes d'appairage d'appareil en attente.
- `src/gateway/server/ws-connection/message-handler.ts:1245` approuve silencieusement les demandes d'appairage local/amorçage éligibles.
- `src/gateway/server/ws-connection/message-handler.ts:1516` émet des jetons d'appareil après appairage approuvé.
- `src/gateway/server/ws-connection/message-handler.ts:1545` émet des jetons de remise d'amorçage supplémentaires limités.
- `src/gateway/server/ws-connection/message-handler.ts:1858` rachète/révoque les jetons d'amorçage après connexion.
- `src/infra/device-bootstrap.ts:228` émet les jetons d'amorçage du code de configuration.
- `src/infra/device-bootstrap.ts:407` vérifie les jetons d'amorçage, la liaison appareil/clé publique et les listes blanches de rôle/portée.
- `src/shared/device-bootstrap-profile.ts:13` définit les portées de remise d'opérateur QR/code de configuration.
- `src/shared/device-bootstrap-profile.ts:22` définit le profil d'amorçage de configuration intégré.
- `src/infra/device-pairing.ts:559` crée ou actualise les demandes d'appairage d'appareil en attente.
- `src/infra/device-pairing.ts:617` approuve l'appairage d'appareil et frappe les jetons de rôle.
- `src/infra/device-pairing.ts:734` approuve l'appairage d'appareil d'amorçage dans les limites du profil d'amorçage.
- `src/infra/device-pairing.ts:924` vérifie les jetons d'appareil appairés.
- `src/infra/device-pairing.ts:988` assure/réutilise les jetons d'appareil à l'intérieur des lignes de base approuvées.
- `src/infra/device-pairing.ts:1077` fait tourner les jetons d'appareil.
- `src/infra/device-pairing.ts:1138` révoque les jetons d'appareil.
- `src/gateway/server-methods/devices.ts:175` implémente `device.pair.list`.
- `src/gateway/server-methods/devices.ts:209` implémente l'autorisation `device.pair.approve`.
- `src/gateway/server-methods/devices.ts:341` implémente `device.pair.remove`.
- `src/gateway/server-methods/devices.ts:400` implémente `device.token.rotate`.
- `src/gateway/server-methods/devices.ts:496` implémente `device.token.revoke`.
- `src/gateway/node-pairing-auto-approve.ts:36` exclut l'Interface de contrôle/WebChat/navigateur et les flux de mise à niveau de l'approbation automatique de nœud CIDR de confiance.
- `src/gateway/client.ts:581` stocke les jetons d'appareil de `hello-ok`.
- `src/gateway/client.ts:605` gère la nouvelle tentative de jeton d'appareil stocké après non-correspondance.
- `src/gateway/client.ts:802` réutilise les portées en cache uniquement lors de la réutilisation des jetons d'appareil en cache.
- `src/gateway/client.ts:877` contrôle la nouvelle tentative de jeton stocké.
- `src/gateway/client.ts:929` restreint la nouvelle tentative automatique de jeton d'appareil à la boucle locale ou au TLS épinglé.
- `src/gateway/client.ts:948` sélectionne la précédence du jeton partagé, du jeton d'appareil, du jeton stocké, du jeton d'amorçage et du jeton de signature.
- `extensions/device-pair/index.ts:505` formate les réponses du code de configuration collable.
- `extensions/device-pair/index.ts:537` formate les conseils d'appairage QR et la copie de sécurité.
- `extensions/device-pair/index.ts:599` émet les charges utiles de configuration avec le profil d'amorçage d'appairage.
- `extensions/device-pair/index.ts:663` enregistre `/pair` avec `operator.pairing`.
- `extensions/device-pair/index.ts:800` envoie les médias QR lorsqu'ils sont pris en charge.
- `extensions/device-pair/index.ts:835` rend le secours QR WebChat.
- `extensions/device-pair/pair-command-auth.ts:31` résout l'autorisation de la commande `/pair` pour les appelants WebChat/internes et les propriétaires de canal.

### Tests d'intégration

- `src/gateway/server.auth.control-ui.suite.ts:848` couvre l'approbation automatique d'appairage d'opérateur de l'Interface de contrôle local-direct.
- `src/gateway/server.auth.control-ui.suite.ts:1031` couvre le code de configuration QR retournant un jeton de nœud plus une remise d'opérateur limité.
- `src/gateway/server.auth.control-ui.suite.ts:1451` couvre les mises à niveau de rôle d'authentification d'amorçage nécessitant une approbation.
- `src/gateway/server.auth.control-ui.suite.ts:1543` couvre l'appairage d'opérateur d'amorçage non-baseline étant retenu pour approbation explicite.
- `src/gateway/server.auth.control-ui.suite.ts:1588` couvre l'approbation automatique d'appairage de nœud local-direct suivie de l'approbation de portée d'opérateur.
- `src/gateway/server.auth.control-ui.suite.ts:1840` couvre le rejet de jeton d'appareil révoqué.
- `src/gateway/server.auth.control-ui.suite.ts:1863` couvre les connexions d'authentification partagée de boucle locale du serveur sans appairage d'appareil.
- `src/gateway/server.shared-auth-rotation.test.ts:187` couvre les sessions WebSocket à authentification partagée se fermant après rotation d'authentification.
- `src/gateway/server.shared-auth-rotation.test.ts:203` couvre les sessions de jeton d'appareil existantes restant connectées après rotation de jeton partagé.
- `src/gateway/server.shared-auth-rotation.test.ts:217` couvre les sessions de jeton d'appareil marquées par l'émetteur se fermant après rotation de jeton partagé.
- `src/gateway/server.shared-auth-rotation.test.ts:246` couvre les jetons d'appareil du navigateur marqués par l'émetteur lors de la reconnexion.
- `src/gateway/server.device-token-rotate-authz.test.ts:188` couvre le déni de rotation/révocation inter-appareils pour les appelants de jeton d'appareil.
- `src/gateway/server.device-token-rotate-authz.test.ts:237` couvre la rotation/révocation inter-appareils d'administrateur.
- `src/gateway/server.device-token-rotate-authz.test.ts:279` couvre le déni d'opérateur limité par portée d'appairage pour la rotation de jeton de nœud révoqué.
- `src/gateway/server.device-pair-approve-authz.test.ts:169` couvre les limites de portée d'appelant sur l'approbation d'appareil.
- `src/gateway/server.node-pairing-auto-approve.test.ts:88` couvre le déni par défaut pour l'appairage de nœud direct non-boucle locale.
- `src/gateway/server.node-pairing-auto-approve.test.ts:122` couvre l'approbation automatique de nœud CIDR de confiance.
- `src/gateway/server.node-pairing-authz.test.ts:157` couvre les exigences de portée d'approbation d'appairage de nœud.
- `test/gateway.multi.e2e.test.ts:27` couvre deux instances de gateway en direct avec WS, HTTP et appairage de nœud.

### Tests unitaires

- `src/gateway/device-auth.test.ts:18` couvre les vecteurs de charge utile d'authentification d'appareil v2.
- `src/gateway/device-auth.test.ts:34` couvre les vecteurs de charge utile d'authentification d'appareil v3.
- `src/gateway/client.test.ts:668` couvre l'effacement des jetons obsolètes lors de la fermeture de non-correspondance de jeton d'appareil.
- `src/gateway/client.test.ts:1329` couvre les portées de jeton d'appareil stocké.
- `src/gateway/client.test.ts:1409` couvre l'utilisation du jeton d'amorçage lorsqu'aucun jeton partagé ou d'appareil n'est disponible.
- `src/gateway/client.test.ts:1429` couvre la priorité explicite du jeton d'appareil.
- `src/gateway/client.test.ts:1476` couvre la nouvelle tentative avec jeton d'appareil stocké après non-correspondance de jeton partagé sur les points de terminaison de confiance.
- `src/gateway/client.test.ts:1597` couvre le comportement de reconnexion pour `PAIRING_REQUIRED` retentable.
- `src/gateway/method-scopes.test.ts:283` couvre la portée `operator.pairing` pour les approbations d'appairage de nœud.
- `src/gateway/node-pairing-auto-approve.test.ts:124` couvre l'exclusion de l'Interface de contrôle/WebChat de l'approbation automatique de nœud.
- `src/gateway/server/ws-connection/handshake-auth-helpers.test.ts:141` couvre le comportement du helper d'appairage local WebChat.
- `extensions/device-pair/index.test.ts:1` couvre le comportement de la commande code de configuration/QR via les API de plugin simulées.
- `extensions/device-pair/pair-command-auth.test.ts:4` couvre la gestion de la portée de la commande d'appairage pour les appelants gateway et canal.

### Requêtes Gitcrawl

Requête : `gitcrawl search issues "device pairing" -R openclaw/openclaw --state all --json number,title,state,url --limit 12`

Résultats :

- Les résultats spécifiques aux fonctionnalités ouvertes incluaient #86778, #74484, #77807, #55914, #85966, #78276, #43903, #87058, #72418, #80828, #85868 et #67618.
- Ces résultats montrent le risque actuel autour des défaillances de preuve-réponse, des blocages de portée, du comportement de fermeture de nœud/opérateur Android, des courses de code de configuration, de l'isolation de jeton multi-utilisateur, des préoccupations de contournement d'auto-appairage du serveur et des conseils manquants sur les erreurs d'appairage.

Requête : `gitcrawl search issues "setup code bootstrap token pairing" -R openclaw/openclaw --state all --json number,title,state,url --limit 12`

Résultats :

- Les résultats ouverts incluaient #78276 pour les courses de code de configuration ravivant les jetons d'amorçage consommés et #48471 pour l'amorçage local en une ligne sur le daemon, l'authentification du tableau de bord et la configuration du propriétaire Telegram.
- Le chemin du code de configuration est implémenté, mais les preuves d'archive maintiennent la gestion des courses d'amorçage et la configuration du premier opérateur comme risques de qualité actifs.

Requête : `gitcrawl search issues "device token rotate revoke" -R openclaw/openclaw --state all --json number,title,state,url --limit 12`

Résultats :

- Les résultats étaient des problèmes de gouvernance des credentials plus larges (#59165, #71116) plutôt que des bugs directs de rotation/révocation.
- Le risque direct de rotation/révocation était mieux représenté par les résultats de PR et les sources/tests que par cette requête de problème.

Requête : `gitcrawl search issues "Control UI pairing WebChat device token" -R openclaw/openclaw --state all --json number,title,state,url --limit 12`

Résultats :

- Les résultats ouverts incluaient #43903 pour l'isolation de plusieurs jetons gateway/multi-utilisateur, #46656 pour le support de bouton en ligne WebChat/Interface de contrôle et #28847 pour les refroidissements de clé de fournisseur.
- Le signal pertinent est que l'appairage de l'Interface de contrôle/WebChat chevauche les attentes d'isolation de jeton multi-utilisateur non résolues.

Requête : `gitcrawl search issues "auth migration device pairing" -R openclaw/openclaw --state all --json number,title,state,url --limit 12`

Résultats :

- Les résultats ouverts incluaient #87058 pour la course de nouvelle tentative de nonce de connexion Android et #69066 pour la séparation de l'identité du service interne de l'authentification utilisateur.
- Les rapports de migration/limite d'authentification continuent à croiser l'appairage lorsque les identités obsolètes ou les appelants de service interne frappent la politique d'appairage d'appareil.

Requête : `gitcrawl search issues "operator scope pairing" -R openclaw/openclaw --state all --json number,title,state,url --limit 12`

Résultats :

- Les résultats ouverts incluaient #74484, #77807, #85966, #72418, #81876, #80836, #73864, #78276, #28847, #84989, #69066 et #78225.
- Les signaux spécifiques aux composants les plus forts sont le blocage de portée, la confusion de rôle Android, le possible contournement d'auto-appairage local, les portées de jeton configurables, la division d'identité de service et les courses de code de configuration.

Requête : `gitcrawl search prs "device pairing token" -R openclaw/openclaw --state all --json number,title,state,url --limit 10`

Résultats :

- Les résultats de PR ouverts incluaient #81189, #84617, #66257, #80896, #46794, #80656, #80779, #73163, #77538 et #81333.
- Ceux-ci montrent le travail actif sur l'actualisation du dernier vu, les limites de taux de gestion d'appairage/jeton, le secours local, la liaison de jeton d'amorçage, la liaison de code de configuration, la compatibilité v2, le routage d'approbation obsolète, les avertissements d'Interface de contrôle non sécurisée et les limites de cadre de connexion.

Requête : `gitcrawl search prs "setup code bootstrap" -R openclaw/openclaw --state all --json number,title,state,url --limit 10`

Résultats :

- Les résultats de PR ouverts incluaient #78277, #46794, #63113, #84657, #78807, #84424, #79756, #83235, #82955 et #81300.
- Les résultats spécifiques aux composants montrent le travail de correction de course de code de configuration, la liaison d'approbation de code de configuration/nœud et l'authentification d'appairage mobile LAN privé toujours en vol.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 10 "device pairing"`

Résultats :

- Les résultats incluaient les conseils de support récents pour l'appairage mobile/nœud, les journaux de gateway en direct montrant l'appairage d'appareil `auto-approved` local, les utilisateurs bloqués par la ré-approbation de portée CLI, la confusion nœud-vs-opérateur, et les diagnostics de connexion de gateway Android.
- Le signal de qualité le plus fort est que les utilisateurs ont toujours besoin de conseils de triage guidés pour déterminer si un appareil est appairé en tant que nœud, en tant qu'opérateur ou seulement en attente.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 10 "setup code bootstrap token"`

Résultats :

- Les résultats incluaient la sortie iOS Alpha `/pair qr` avec des problèmes de certificat IP `wss://`, les notes du mainteneur selon lesquelles le main actuel utilise des jetons d'amorçage de courte durée et le stockage de jeton d'appareil, un examen HarmonyOS qui a manqué le champ d'authentification du jeton d'amorçage et les rapports Android/Samsung de boucles de réutilisation de jeton d'amorçage obsolète.
- L'UX du code de configuration est réelle et documentée, mais TLS, la compatibilité des clients et la récupération de jeton d'amorçage obsolète restent des sujets de support récurrents.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 10 "device token mismatch pairing required"`

Résultats :

- Les résultats incluaient les threads de support utilisateur diagnostiquant `pairing required`, `scope-upgrade`, l'Interface de contrôle n'affichant pas la sortie de l'agent, la dérive de jeton, l'appairage de boucle locale, `openclaw devices rotate`, les remplacements d'environnement obsolètes et les boucles de reconnexion de mise à jour macOS.
- Cela réduit la qualité car le chemin de récupération opérationnelle est toujours trop facile à mal diagnostiquer comme un problème générique de modèle, cron, tableau de bord ou gateway.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI pairing WebChat"`

Résultats :

- Les résultats incluaient les notes de version et les commentaires de support selon lesquels l'Interface de contrôle/WebChat fonctionnait après l'intégration tandis que la configuration de canal ignorée échouait, plus les commentaires de problème sur la régression d'authentification d'appareil du navigateur WebChat/Interface de contrôle et la migration d'appairage de l'Interface de contrôle.
- L'Interface de contrôle/WebChat sont utilisables, mais les archives montrent qu'ils font toujours partie de la migration d'authentification et de la gestion des attentes d'appairage.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 10 "operator scope pairing required"`

Résultats :

- Les résultats incluaient les journaux `scope-upgrade` bruts, le diagnostic de secours d'appairage hôte/invité Docker, l'analyse du mainteneur des identités `gateway-client` internes obsolètes, les fermetures de problème pour l'appairage de boucle locale `pairing required` et les commentaires d'examen Android avertissant que l'ajout de `operator.admin` par défaut force les mises à niveau de portée.
- Le risque de qualité n'est pas l'absence de fonctionnalité ; c'est que les identités obsolètes et les portées demandées peuvent toujours créer des blocages d'opérateur difficiles à démêler.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 10 "auth migration pairing"`

Résultats :

- Les résultats incluaient les notes de refonte d'entrée de canal, les commentaires de migration d'authentification WebSocket, les notes d'examen de remise de code de configuration, les mentions de freshbits du code de configuration d'authentification partagée et les conseils de version sur les changements d'authentification cassants lorsque `gateway.auth.token` et `gateway.auth.password` sont tous deux configurés sans mode explicite.
- La migration d'authentification reste liée à l'appairage car les clients hérités, l'état obsolète et la configuration d'authentification mixte peuvent apparaître comme des défaillances d'appairage.
