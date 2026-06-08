---
title: Rapport de Maturité du Runtime Gateway
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
---

# Rapport de Maturité du Runtime Gateway

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Stable (81%)`
- Qualité : `Alpha (69%)`
- Complétude : `Stable (80%)`
- Fonctionnalités LTS : `12/13`

## Résumé

Ce rapport développe la surface de la fiche d'évaluation nommée « Gateway
runtime » à partir de la [fiche d'évaluation de maturité](https://gist.github.com/vincentkoc/a21bc88d47f2b2b46cc7f339c7e47039)
publiée dans les familles de fonctionnalités significatives qu'OpenClaw devrait
évaluer sous cette seule ligne.

La première version de ce rapport a uniquement décomposé la surface. Cette
itération conserve cette décomposition et ajoute une première rubrique afin que
les futures révisions de maturité, les vérifications de version et les études
de scénarios puissent distinguer les fonctionnalités Gateway bien couvertes des
domaines qui sont présents dans le code mais encore minces en termes de preuve
d'intégration ou qui présentent des risques de qualité en exploitation.

## Matrice

| Catégorie                                                                    | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Approbations et Exécution Distante](approval-and-execution-safety.md)      | ✅  | `Stable (88%)` | `Beta (72%)`   | `Beta (78%)`   | Approbations d'exécution, Approbations de plugin, Approbations d'exécution de nœud, Exécution de nœud approuvée, Sécurité de mutation d'approbation, Comportement de secours de livraison                                                                                                                                                                                                                                          |
| [APIs HTTP](http-apis.md)                                                   | ✅  | `Stable (88%)` | `Beta (74%)`   | `Beta (72%)`   | APIs compatibles OpenAI, API d'invocation d'outils, Accès à l'API Admin, Ingestion de hook                                                                                                                                                                                                                                                                                                                                        |
| [Surface Web Hébergée](hosted-web-surface.md)                               | ✅  | `Stable (88%)` | `Beta (74%)`   | `Beta (72%)`   | Interface de contrôle, Hébergement WebChat, Routes web de plugin, Routes Canvas et A2UI                                                                                                                                                                                                                                                                                                                                            |
| [APIs RPC Gateway et Événements](core-rpc-coverage.md)                      | ✅  | `Alpha (68%)`  | `Alpha (57%)`  | `Stable (88%)` | APIs de santé, APIs d'identité et de présence, APIs de modèle, APIs d'utilisation et de mémoire, APIs de session, APIs de chat, APIs de canal, APIs de connexion web et de réveil, APIs de configuration et de secrets, APIs de mise à jour et de configuration, APIs d'agent et d'artefact, APIs de tâche et d'automatisation, APIs d'outil et de compétence, Enveloppes de requête et d'événement, Effets secondaires idempotents, Découverte de méthode, Découverte d'événement, Résultats acceptés puis finaux, Ordre des événements, Actualisation d'état après lacunes |
| [Authentification et Appairage d'Appareil](device-identity-auth-and-pairing.md) | ✅  | `Stable (88%)` | `Beta (72%)`   | `Stable (82%)` | Connexion par secret partagé, Authentification par proxy de confiance, Mode d'ingestion privée, Signature de défi d'appareil, Jetons d'appareil, Bootstrap par code de configuration, Récupération d'incompatibilité d'authentification, Migration d'authentification d'appareil, Appairage de client, Appairage de nœud                                                                                                                  |
| [Accès Réseau et Découverte](network-exposure-and-transport-selection.md)   | ✅  | `Alpha (68%)`  | `Alpha (62%)`  | `Beta (74%)`   | Accès loopback et LAN, Accès Tailnet, Tunnels SSH, Découverte de point de terminaison, Points de terminaison enregistrés, Épinglage TLS                                                                                                                                                                                                                                                                                            |
| [Nœuds et Capacités Distantes](node-transport-and-capability-relay.md)      | ❌  | `Stable (84%)` | `Alpha (63%)`  | `Beta (76%)`   | Présence de nœud, Capacités de nœud, Inventaire de nœud, Actions de nœud, Événements de nœud, Livraison de travail en attente, Capacités d'appareil distant, Commandes d'hôte distant                                                                                                                                                                                                                                              |
| [Santé, Diagnostics et Réparation](observability-health-and-repair.md)      | ✅  | `Alpha (68%)`  | `Alpha (62%)`  | `Beta (78%)`   | Snapshots de santé, Disponibilité du canal, Diagnostics de stabilité, Diagnostics de charge utile, Exports de diagnostics, Vérifications Doctor, Suivi des journaux                                                                                                                                                                                                                                                                 |
| [Compatibilité de Protocole](protocol-typing-and-compatibility.md)          | ✅  | `Beta (72%)`   | `Beta (70%)`   | `Stable (84%)` | Schéma de protocole publié, Validation de requête d'exécution, Export JSON Schema, Modèles de client Swift, Négociation de version, Valeurs par défaut de transport client, Évolution rétrocompatible                                                                                                                                                                                                                               |
| [Rôles et Permissions](roles-scopes-and-operator-policy.md)                 | ✅  | `Stable (85%)` | `Alpha (62%)`  | `Stable (80%)` | Négociation de rôle, Permissions d'opérateur, Actions contrôlées par approbation, Déclarations de nœud non approuvé, Portée des événements                                                                                                                                                                                                                                                                                        |
| [Cycle de Vie Gateway](runtime-lifecycle-and-supervision.md)                | ✅  | `Stable (86%)` | `Stable (82%)` | `Stable (88%)` | Démarrage au premier plan, Installation de service, Redémarrage et arrêt, État du service, Paramètres de liaison et de port, Rechargement de configuration, Isolation multi-gateway                                                                                                                                                                                                                                                |
| [Contrôles de Sécurité](security-and-hardening-posture.md)                  | ✅  | `Stable (84%)` | `Beta (74%)`   | `Stable (80%)` | Authentification non-loopback, Exceptions de proxy de confiance, Limites de confiance Gateway et nœud, Auto-approbation CIDR de confiance, Gestion de protocole en cas d'échec, Garanties d'exécution distante                                                                                                                                                                                                                     |
| [Connexion WebSocket](websocket-handshake-and-session-establishment.md)     | ✅  | `Stable (84%)` | `Beta (76%)`   | `Stable (82%)` | Transport WebSocket, Défi de connexion, Requête de connexion, Négociation de version de protocole, Snapshot hello-ok, Nouvelle tentative de démarrage, Limites de session, URLs de surface de plugin                                                                                                                                                                                                                              |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou
  preuve de flux d'exécution serveur/runtime dans la catégorie. Les tests
  unitaires peuvent fournir un contexte de support mais ne rendent jamais une
  fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation
  et opérationnelle. La couverture des tests unitaires, d'intégration, e2e, en
  direct et de flux d'exécution runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre
  l'ensemble de capacités spécifiques à la surface prévu. Utilisez les
  instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez
  l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités
  détaillées plutôt que comme une dimension de score séparée.

## Inventaire détaillé des fonctionnalités

### 1. Approbations et exécution à distance

Ancres de recherche : gateway runtime and websocket protocol gateway runtime websocket feature matrix: approval and execution safety, gateway runtime websocket feature matrix: approval and execution safety.

Remarque de catégorie : [Approbations et exécution à distance](approval-and-execution-safety.md)

Décisions de score :

- Couverture : `Stable (88%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Approbations d'exécution : API de demande d'approbation d'exécution, recherche, attente, résolution et snapshot de politique.
- Approbations de plugin : Flux de demande d'approbation de plugin, attente et résolution.
- Approbations d'exécution de nœud : Relais de politique d'approbation d'exécution local au nœud via Gateway RPC.
- Exécution de nœud approuvée : Liaison canonique `systemRunPlan` pour l'exécution nœud-hôte.
- Sécurité de mutation d'approbation : Rejet de `command`, `cwd`, `agentId` ou `sessionKey` mutés après la préparation de l'approbation.
- Comportement de secours de livraison : Secours de livraison d'agent entre les routes livrables strictes et l'exécution en session uniquement.

Documentation principale :

- `docs/gateway/protocol.md`
- `docs/gateway/security/index.md`

Lacunes majeures en qualité/complétude :

- Les pistes de preuve en direct Linux systemd et Windows Scheduled Task macOS.
- Les modes de rechargement manquent de preuve complète d'édition à chaud ou de redémarrage Gateway.

### 2. API HTTP

Ancres de recherche : gateway http api, openai compatible http api, tools invoke http api, admin http rpc, hook ingress.

Remarque de catégorie : [API HTTP](http-apis.md)

Décisions de score :

- Couverture : `Stable (88%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (72%)`
- LTS : ✅

Fonctionnalités :

- API compatibles OpenAI : API HTTP compatibles OpenAI (`/v1/models`, `/v1/chat/completions`, `/v1/responses`, `/v1/embeddings`).
- API d'invocation d'outil : Chemin d'invocation d'outils HTTP.
- Accès API Admin : Route de plugin RPC HTTP admin optionnelle.
- Ingress de hook : Hébergement de hook et routes d'ingress HTTP.

Documentation principale :

- `docs/gateway/index.md`
- `docs/gateway/openai-http-api.md`
- `docs/gateway/openresponses-http-api.md`
- `docs/gateway/tools-invoke-http-api.md`
- `docs/automation/hooks.md`
- `docs/web/index.md`

Lacunes majeures en qualité/complétude :

- Aucun flux de travail découverte-à-connexion de bout en bout.
- Les flux de travail tunnel SSH, topologie distante et épinglage d'empreinte WSS restent
  incomplets.

### 3. Surface Web hébergée

Ancres de recherche : hosted web surface, control ui gateway, webchat gateway, plugin http route gateway, canvas a2ui gateway.

Remarque de catégorie : [Surface Web hébergée](hosted-web-surface.md)

Décisions de score :

- Couverture : `Stable (88%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (72%)`
- LTS : ✅

Fonctionnalités :

- Interface de contrôle : Hébergement de l'interface de contrôle sur le serveur Gateway.
- Hébergement WebChat : Hébergement WebChat.
- Routes web de plugin : Surfaces HTTP Canvas et autres plugins servies par Gateway.
- Routes Canvas et A2UI : Documents Canvas, transport A2UI et routes de plugin hébergées dans le navigateur sous le serveur HTTP Gateway.

Documentation principale :

- `docs/gateway/index.md`
- `docs/concepts/architecture.md`
- `docs/web/control-ui.md`
- `docs/web/webchat.md`
- `docs/refactor/canvas.md`

Lacunes majeures en qualité/complétude :

- La tentative de redémarrage en attente du sidecar de démarrage manque de preuve complète du flux Gateway.
- L'actualisation de `pluginSurfaceUrls` et la forme complète de `hello-ok` restent
  incomplètes au niveau du flux Gateway.

### 4. API RPC Gateway et événements

Ancres de recherche : core rpc coverage, rpc framing, control-plane semantics, hello-ok.features.methods, hello-ok.features.events, event sequence, idempotencyKey.

Remarque de catégorie : [API RPC Gateway et événements](core-rpc-coverage.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (57%)`
- Complétude : `Stable (88%)`
- LTS : ✅

Fonctionnalités :

- API de santé : RPC `health` et `status`.
- API d'identité et de présence : `gateway.identity.get`, `system-presence`, `system-event` et RPC de battement cardiaque.
- API de modèles : RPC `models.list`.
- API d'utilisation et de mémoire : Résumés d'utilisation et RPC de disponibilité de la mémoire.
- API de session : RPC `sessions.*`.
- API de chat : RPC `chat.*` et `agent.wait`.
- API de canal : RPC `channels.status` et `channels.logout`.
- API de connexion web et de réveil : RPC `web.login.*`, `push.test` et `voicewake.*`.
- API de configuration et secrets : RPC `config.*` et `secrets.*`.
- API de mise à jour et configuration : RPC `update.*` et `wizard.*`.
- API d'agent et d'artefact : RPC `agents.*`, fichiers d'agent, environnements et artefacts.
- API de tâche et d'automatisation : RPC `wake`, `cron.*` et `tasks.*`.
- API d'outil et de compétence : RPC `commands.list`, `tools.*` et `skills.*`.
- Enveloppes de demande et d'événement : Formes de cadre de demande, réponse et événement.
- Effets secondaires idempotents : Exigences d'idempotence pour les méthodes avec effets secondaires.
- Découverte de méthode : Découverte de méthode via `hello-ok.features.methods`.
- Découverte d'événement : Découverte d'événement via `hello-ok.features.events`.
- Résultats acceptés puis finaux : Accusé de réception accepté immédiat plus résultat final ultérieur.
- Ordre des événements : Gestion de la séquence et ordre monotone des événements par client.
- Actualisation d'état après lacunes : Modèle sans relecture et récupération explicite de lacunes via actualisation d'état.

Documentation principale :

- `docs/gateway/protocol.md`
- `docs/gateway/index.md`
- `docs/concepts/architecture.md`

Lacunes majeures en qualité/complétude :

- La portée de la diffusion et le comportement de fermeture en cas d'événement inconnu nécessitent une preuve
  de bout en bout plus large.
- La méfiance envers les réclamations de nœud nécessite une couverture de scénario plus complète.

### 5. Authentification et appairage des appareils

Ancres de recherche : gateway runtime and websocket protocol device identity, auth, and pairing, device identity, auth, and pairing.

Remarque de catégorie : [Authentification et appairage des appareils](device-identity-auth-and-pairing.md)

Décisions de score :

- Couverture : `Stable (88%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Connexion par secret partagé : Authentification par secret partagé via jeton ou mot de passe.
- Authentification par proxy de confiance : Modes d'authentification par proxy de confiance et porteur d'identité.
- Mode d'ingress privé : Comportement `gateway.auth.mode: "none"` d'ingress privé et ses limites.
- Signature de défi d'appareil : Signature d'identité d'appareil contre le nonce de défi.
- Jetons d'appareil : Émission de jeton d'appareil, persistance, réutilisation de reconnexion, rotation et révocation.
- Bootstrap de code de configuration : Flux de jeton de code de configuration de bootstrap et remise de jeton d'opérateur délimitée.
- Récupération d'incompatibilité d'authentification : Sémantique de récupération pour `AUTH_TOKEN_MISMATCH` et `AUTH_SCOPE_MISMATCH`.
- Migration d'authentification d'appareil : Erreurs de migration d'authentification d'appareil et comportement de signature v2/v3 requis.
- Appairage de client : Exigences d'appairage d'appareil pour les nouveaux clients.
- Appairage de nœud : Flux d'appairage de nœud, y compris les demandes en attente, les approbations, l'expiration et les limites d'auto-approbation CIDR de confiance ou de mise à niveau de métadonnées.

Documentation principale :

- `docs/gateway/protocol.md`
- `docs/gateway/pairing.md`
- `docs/gateway/security/index.md`

Lacunes majeures en qualité/complétude :

- Les cycles de vie d'ingress distant sont inégaux.
- Les variantes de migration d'authentification et l'UX d'appairage/preuve multiplateforme nécessitent une
  couverture plus complète.

### 6. Accès réseau et découverte

Ancres de recherche : gateway runtime and websocket protocol network exposure and transport selection, network exposure and transport selection.

Remarque de catégorie : [Accès réseau et découverte](network-exposure-and-transport-selection.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (62%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Accès loopback et LAN : Exposition Gateway loopback et LAN.
- Accès Tailnet : Exposition Gateway face à Tailnet et routage MagicDNS/Tailscale.
- Tunnels SSH : Tunneling SSH comme chemin distant de secours.
- Découverte de point de terminaison : Découverte Bonjour/DNS-SD, DNS-SD large zone et indices de transport annoncés.
- Points de terminaison enregistrés : Points de terminaison Gateway distants enregistrés et ordre de préférence de route.
- Épinglage TLS : Activation TLS et épinglage d'empreinte de certificat optionnel.

Documentation principale :

- `docs/gateway/index.md`
- `docs/gateway/discovery.md`
- `docs/gateway/protocol.md`

Lacunes majeures en qualité/complétude :

- La récupération de lacune et la dérive de découverte d'événement ne sont pas largement intégrées.
- L'ordre multi-client délimité et l'idempotence générique restent incomplets.

### 7. Nœuds et capacités distantes

Ancres de recherche : gateway runtime and websocket protocol node transport and capability relay, node transport and capability relay.

Remarque de catégorie : [Nœuds et capacités distantes](node-transport-and-capability-relay.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Alpha (63%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Présence de nœud : Présence de nœud dans le même plan de contrôle WS que les clients opérateur.
- Capacités de nœud : Déclaration de capacité de nœud au moment de la connexion.
- Inventaire de nœud : `node.list`, `node.describe` et visibilité de nommage/état.
- Actions de nœud : `node.invoke` et `node.invoke.result`.
- Événements de nœud : `node.event`, en particulier `node.presence.alive`.
- Livraison de travail en attente : API de travail en attente pour les nœuds connectés et déconnectés.
- Capacités d'appareil distant : Relais de surfaces de capacité distante telles que caméra, canvas, écran, localisation, voix et navigateur.
- Commandes d'hôte distant : Relais de surfaces de capacité de commande d'hôte distant.

Documentation principale :

- `docs/gateway/protocol.md`
- `docs/concepts/architecture.md`
- `docs/nodes/index.md`

Lacunes majeures en qualité/complétude :

- `commands.list`, `skills.*`, `tasks.*`, `cron.*`, `web.login.*`,
  `push.test`, `tools.invoke`, artefacts et environnements nécessitent un
  flux de fumée Core RPC complet.

### 8. Santé, diagnostics et réparation

Ancres de recherche : gateway runtime and websocket protocol observability, health, and repair, observability, health, and repair.

Remarque de catégorie : [Santé, diagnostics et réparation](observability-health-and-repair.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (62%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Snapshots de santé : Snapshots `health` et `status`.
- Disponibilité du canal : Sondage de disponibilité du canal via Gateway en cours d'exécution.
- Diagnostics de stabilité : Sortie de l'enregistreur de stabilité.
- Diagnostics de charge utile : Diagnostics `payload.large`.
- Exports de diagnostics : Contenu d'export de diagnostics, modèle de confidentialité et déclencheurs CLI/chat.
- Vérifications Doctor : Vérifications Doctor pour la fraîcheur du protocole UI, la dérive de service, la dérive d'authentification/appairage, les collisions de port, les meilleures pratiques de sandbox/runtime et les problèmes d'installation source.
- Suivi des journaux : Suivi des journaux et visibilité du signal opérationnel.

Documentation principale :

- `docs/gateway/index.md`
- `docs/gateway/diagnostics.md`
- `docs/gateway/doctor.md`

Lacunes majeures en qualité/complétude :

- Le travail en attente hors ligne et le comportement de réveil/drainage restent minces.
- La parité de plateforme entre caméra, canvas, écran, localisation, voix, navigateur,
  transfert de fichiers et commandes d'hôte reste incomplète.

### 9. Compatibilité de protocole

Ancres de recherche : gateway runtime and websocket protocol protocol typing and compatibility, protocol typing and compatibility.

Remarque de catégorie : [Compatibilité de protocole](protocol-typing-and-compatibility.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Beta (70%)`
- Complétude : `Stable (84%)`
- LTS : ✅

Fonctionnalités :

- Schéma de protocole publié : TypeBox comme source de vérité du protocole.
- Validation de demande à l'exécution : Validateurs à l'exécution pour les charges utiles de protocole.
- Export JSON Schema : JSON Schema généré pour les charges utiles de protocole.
- Modèles de client Swift : Génération de modèle Swift.
- Négociation de version : Constantes de protocole actuelles et comportement de plage de protocole supportée.
- Valeurs par défaut de transport client : Valeurs par défaut client pour les délais d'expiration de demande, le backoff de reconnexion et la gestion des ticks.
- Évolution rétrocompatible : Discipline d'évolution additive pour les nouvelles méthodes, événements ou champs de charge utile.

Documentation principale :

- `docs/gateway/protocol.md`
- `docs/concepts/architecture.md`
- `docs/concepts/typebox.md`
- `docs/gateway/bridge-protocol.md`

Lacunes majeures en qualité/complétude :

- Les approbations de plugin et la largeur de liaison `systemRunPlan` nécessitent une preuve
  d'intégration Gateway plus forte.
- Le relais de politique d'exécution de nœud et la sémantique de livraison de secours restent incomplets.

### 10. Rôles et permissions

Ancres de recherche : gateway runtime and websocket protocol gateway runtime websocket feature matrix: roles, scopes, and operator policy, gateway runtime websocket feature matrix: roles, scopes, and operator policy.

Remarque de catégorie : [Rôles et permissions](roles-scopes-and-operator-policy.md)

Décisions de score :

- Couverture : `Stable (85%)`
- Qualité : `Alpha (62%)`
- Complétude : `Stable (80%)`
- LTS : ✅

Fonctionnalités :

- Négociation de rôle : Négociation de rôle `operator` versus `node`.
- Permissions d'opérateur : Portées d'opérateur principales telles que `operator.read`, `operator.write`, `operator.admin`, `operator.approvals`, `operator.pairing` et `operator.talk.secrets`.
- Actions contrôlées par approbation : Exigences de portée supplémentaires au moment de l'approbation pour l'appairage et les commandes de nœud dangereuses.
- Déclarations de nœud non approuvé : `caps`, `commands` et `permissions` déclarés par nœud comme réclamations plutôt que vérité approuvée.
- Portée d'événement : Portée d'événement de diffusion, y compris le comportement de fermeture en cas d'échec pour les familles d'événements inconnues.

Documentation principale :

- `docs/gateway/protocol.md`
- `docs/gateway/security/index.md`

Lacunes majeures en qualité/complétude :

- Le flux de plugin activé RPC HTTP Admin reste incomplet.
- Les chemins d'authentification Canvas/plugin web et la limite de produit statique-vs-WS WebChat
  nécessitent une preuve et une définition plus nettes.

### 11. Cycle de vie Gateway

Ancres de recherche : gateway runtime and websocket protocol runtime lifecycle and supervision, runtime lifecycle and supervision.

Remarque de catégorie : [Cycle de vie Gateway](runtime-lifecycle-and-supervision.md)

Décisions de score :

- Couverture : `Stable (86%)`
- Qualité : `Stable (82%)`
- Complétude : `Stable (88%)`
- LTS : ✅

Fonctionnalités :

- Démarrage au premier plan : Démarrage au premier plan local via `openclaw gateway`.
- Installation de service : Installation de cycle de vie supervisé sur macOS, utilisateur Linux/systemd et planification de tâche Windows native.
- Redémarrage et arrêt : Comportement correct de `restart` et `stop` pour les installations supervisées.
- Statut de service : Comportement de statut pour les installations supervisées.
- Paramètres de liaison et de port : Précédence de liaison et de port entre les drapeaux CLI, les variables d'env, la configuration et les métadonnées de superviseur persistées.
- Rechargement de configuration : Modes de rechargement de configuration : `off`, `hot`, `restart` et `hybrid`.
- Isolation multi-gateway : Isolation de plusieurs gateways sur un hôte, y compris la séparation de configuration/état/espace de travail.

Documentation principale :

- `docs/gateway/index.md`
- `docs/concepts/architecture.md`

Lacunes majeures en qualité/complétude :

- L'export de diagnostics en direct, `/diagnostics`, la persistance de stabilité et les boucles de réparation doctor
  sont manquants ou incomplets.
- La validation active du schéma d'outil et la preuve de santé du canal manquée nécessitent une
  couverture plus forte.

### 12. Contrôles de sécurité

Ancres de recherche : gateway runtime and websocket protocol security and hardening posture, security and hardening posture.

Remarque de catégorie : [Contrôles de sécurité](security-and-hardening-posture.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Beta (74%)`
- Complétude : `Stable (80%)`
- LTS : ✅

Fonctionnalités :

- Authentification non-loopback : Authentification requise pour l'exposition non-loopback.
- Exceptions de proxy de confiance : Exceptions d'authentification d'appareil de proxy de confiance et plan de contrôle.
- Limites de confiance Gateway et nœud : Définition de domaine de confiance Gateway/nœud.
- Auto-approbation CIDR de confiance : Limites CIDR de confiance pour l'auto-approbation de nœud.
- Gestion de protocole en fermeture : Comportement rapide/fermeture en cas de violations de protocole et de familles d'événements inconnues.
- Protections d'exécution distante : Posture de sécurité autour de l'exécution de nœud distant et du relais de contrôle de navigateur.

Documentation principale :

- `docs/gateway/security/index.md`
- `docs/gateway/protocol.md`
- `docs/gateway/discovery.md`

Lacunes majeures en qualité/complétude :

- La couverture est principalement basée sur le schéma/garde plutôt que sur la preuve client à l'exécution.
- Les clients générés, la négociation de version de protocole et la suppression de pont hérité
  nécessitent plus de preuve d'intégration à l'exécution.

### 13. Connexion WebSocket

Ancres de recherche : gateway runtime and websocket protocol websocket handshake and session establishment, websocket handshake and session establishment.

Remarque de catégorie : [Connexion WebSocket](websocket-handshake-and-session-establishment.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Beta (76%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Transport WebSocket : Transport WebSocket avec cadres texte JSON.
- Défi de connexion : `connect.challenge` obligatoire avant la connexion.
- Demande de connexion : Demande `connect` obligatoire du premier cadre.
- Négociation de version de protocole : Négociation de plage de protocole (`minProtocol`/`maxProtocol`).
- Snapshot hello-ok : Structure de charge utile `hello-ok` requise : identité du serveur, authentification négociée, découverte de fonctionnalité, snapshot et limites de politique.
- Tentative de démarrage : Comportement `UNAVAILABLE` du sidecar de démarrage retentable pendant le démarrage de Gateway.
- Limites de session : Annonce de politique post-établissement de liaison (`maxPayload`, `maxBufferedBytes`, `tickIntervalMs`).
- URL de surface de plugin : Émission et actualisation optionnelles de `pluginSurfaceUrls`.

Documentation principale :

- `docs/gateway/protocol.md`
- `docs/concepts/architecture.md`

## Interprétation recommandée de la fiche d'évaluation

Pour la notation de maturité, cette surface ne doit pas être traitée comme « la Gateway fonctionne »
ou « la WebSocket se connecte ». Elle doit être traitée comme un ensemble de contrats du plan de contrôle :

- fiabilité des processus
- accessibilité du transport
- exactitude de la poignée de main et de l'authentification
- application de l'autorisation et de la portée
- exactitude des RPC/événements
- exactitude du relais de nœud
- diagnosticabilité opérationnelle
- compatibilité et sécurité de la mise à niveau

Si la ligne unique de la fiche d'évaluation reste trop large, la division future la plus claire est :

1. Runtime et opérations de la Gateway
2. Compatibilité du protocole Gateway et du client
3. Authentification, appairage et sécurité de la Gateway
4. Relais de nœud et approbations de la Gateway

## Hors du champ d'application de cette surface

Ceux-ci sont adjacents à la Gateway, mais ne doivent pas être notés principalement sous cette
surface :

- Qualité du produit spécifique au canal comme le comportement de Telegram, Discord ou Slack.
- Qualité du modèle ou latence spécifiques au fournisseur.
- Qualité de l'interface utilisateur de contrôle ou de l'expérience utilisateur de l'application mobile en tant que surfaces d'application autonomes.
- Qualité de la parole/voix en tant que flux de travail produit, au-delà de la correction du protocole/plan de contrôle.
- Routes HTTP spécifiques aux plugins ou logique métier des plugins au-delà des responsabilités d'hébergement et de politique de la Gateway.

## Cadre source

- `docs/gateway/index.md` pour le cycle de vie de la Gateway, le modèle d'exécution, la supervision,
l'accès à distance et les vérifications opérationnelles.
- `docs/gateway/protocol.md` pour la poignée de main, l'encadrement, les rôles/portées, les familles de méthodes,
les approbations, l'authentification, l'appairage, TLS et le versioning.
- `docs/concepts/architecture.md` pour les limites de flux Gateway/client/nœud et les invariants.
- `docs/gateway/discovery.md` pour la sélection du transport, la découverte Bonjour/Tailscale/SSH et la politique de route distante.
- `docs/gateway/pairing.md` pour l'appairage de nœud, l'émission de jetons, l'approbation automatique et les limites de confiance.
- `docs/gateway/diagnostics.md` et `docs/gateway/doctor.md` pour l'observabilité, l'export de diagnostics et la couverture de réparation.
- `docs/gateway/security/index.md` pour le modèle de confiance Gateway/nœud et les limites de renforcement de la sécurité.
- `.mem/main/specs/25-lts-release-placeholder/reports/openclaw-domain-entity-taxonomy.md`
pour les ancres d'ontologie et la dénomination.
