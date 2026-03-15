---
summary: "Refonte Clawnet : unifier le protocole réseau, les rôles, l'authentification, les approbations, l'identité"
read_when:
  - Planning a unified network protocol for nodes + operator clients
  - Reworking approvals, pairing, TLS, and presence across devices
title: "Refonte Clawnet"
---

# Refonte Clawnet (unification protocole + authentification)

## Salut

Salut Peter — excellente direction ; cela déverrouille une UX plus simple + une sécurité plus forte.

## Objectif

Document unique et rigoureux pour :

- État actuel : protocoles, flux, limites de confiance.
- Points douloureux : approbations, routage multi-saut, duplication UI.
- État proposé : un protocole, rôles délimités, authentification/appairage unifié, épinglage TLS.
- Modèle d'identité : IDs stables + slugs mignons.
- Plan de migration, risques, questions ouvertes.

## Objectifs (issus de la discussion)

- Un protocole pour tous les clients (app mac, CLI, iOS, Android, nœud headless).
- Chaque participant réseau authentifié + apparié.
- Clarté des rôles : nœuds vs opérateurs.
- Approbations centrales acheminées vers l'utilisateur.
- Chiffrement TLS + épinglage optionnel pour tout le trafic distant.
- Duplication de code minimale.
- Une seule machine doit apparaître une fois (pas d'entrée dupliquée UI/nœud).

## Non-objectifs (explicites)

- Supprimer la séparation des capacités (toujours besoin du moindre privilège).
- Exposer le plan de contrôle de la passerelle sans vérifications de portée.
- Rendre l'authentification dépendante des étiquettes humaines (les slugs restent non-sécurité).

---

# État actuel (tel quel)

## Deux protocoles

### 1) WebSocket de passerelle (plan de contrôle)

- Surface API complète : config, canaux, modèles, sessions, exécutions d'agent, logs, nœuds, etc.
- Liaison par défaut : loopback. Accès distant via SSH/Tailscale.
- Authentification : token/mot de passe via `connect`.
- Pas d'épinglage TLS (repose sur loopback/tunnel).
- Code :
  - `src/gateway/server/ws-connection/message-handler.ts`
  - `src/gateway/client.ts`
  - `docs/gateway/protocol.md`

### 2) Bridge (transport de nœud)

- Surface d'allowlist étroite, identité de nœud + appairage.
- JSONL sur TCP ; TLS optionnel + épinglage d'empreinte de certificat.
- TLS annonce l'empreinte dans TXT de découverte.
- Code :
  - `src/infra/bridge/server/connection.ts`
  - `src/gateway/server-bridge.ts`
  - `src/node-host/bridge-client.ts`
  - `docs/gateway/bridge-protocol.md`

## Clients du plan de contrôle aujourd'hui

- CLI → Gateway WS via `callGateway` (`src/gateway/call.ts`).
- UI app macOS → Gateway WS (`GatewayConnection`).
- Web Control UI → Gateway WS.
- ACP → Gateway WS.
- Le contrôle navigateur utilise son propre serveur de contrôle HTTP.

## Nœuds aujourd'hui

- App macOS en mode nœud se connecte au bridge de passerelle (`MacNodeBridgeSession`).
- Les apps iOS/Android se connectent au bridge de passerelle.
- Appairage + token par nœud stockés sur la passerelle.

## Flux d'approbation actuel (exec)

- L'agent utilise `system.run` via Gateway.
- Gateway invoque le nœud sur le bridge.
- Le runtime du nœud décide de l'approbation.
- Invite UI affichée par l'app mac (quand nœud == app mac).
- Le nœud retourne `invoke-res` à Gateway.
- Multi-saut, UI liée à l'hôte du nœud.

## Présence + identité aujourd'hui

- Entrées de présence de passerelle à partir de clients WS.
- Entrées de présence de nœud à partir du bridge.
- L'app mac peut afficher deux entrées pour la même machine (UI + nœud).
- Identité du nœud stockée dans le magasin d'appairage ; identité UI séparée.

---

# Problèmes / points douloureux

- Deux piles de protocoles à maintenir (WS + Bridge).
- Approbations sur nœuds distants : l'invite apparaît sur l'hôte du nœud, pas où se trouve l'utilisateur.
- Épinglage TLS existe uniquement pour le bridge ; WS dépend de SSH/Tailscale.
- Duplication d'identité : la même machine s'affiche comme plusieurs instances.
- Rôles ambigus : les capacités UI + nœud + CLI ne sont pas clairement séparées.

---

# État proposé (Clawnet)

## Un protocole, deux rôles

Protocole WS unique avec rôle + portée.

- **Rôle : nœud** (hôte de capacité)
- **Rôle : opérateur** (plan de contrôle)
- **Portée** optionnelle pour l'opérateur :
  - `operator.read` (statut + visualisation)
  - `operator.write` (exécution d'agent, envois)
  - `operator.admin` (config, canaux, modèles)

### Comportements des rôles

**Nœud**

- Peut enregistrer les capacités (`caps`, `commands`, permissions).
- Peut recevoir les commandes `invoke` (`system.run`, `camera.*`, `canvas.*`, `screen.record`, etc).
- Peut envoyer des événements : `voice.transcript`, `agent.request`, `chat.subscribe`.
- Ne peut pas appeler les APIs du plan de contrôle config/modèles/canaux/sessions/agent.

**Opérateur**

- API du plan de contrôle complet, contrôlée par la portée.
- Reçoit toutes les approbations.
- N'exécute pas directement les actions du système d'exploitation ; les achemine vers les nœuds.

### Règle clé

Le rôle est par connexion, pas par appareil. Un appareil peut ouvrir les deux rôles, séparément.

---

# Authentification + appairage unifié

## Identité du client

Chaque client fournit :

- `deviceId` (stable, dérivé de la clé de l'appareil).
- `displayName` (nom humain).
- `role` + `scope` + `caps` + `commands`.

## Flux d'appairage (unifié)

- Le client se connecte sans authentification.
- Gateway crée une **demande d'appairage** pour ce `deviceId`.
- L'opérateur reçoit une invite ; approuve/refuse.
- Gateway émet des identifiants liés à :
  - clé publique de l'appareil
  - rôle(s)
  - portée(s)
  - capacités/commandes
- Le client persiste le token, se reconnecte authentifié.

## Authentification liée à l'appareil (éviter la relecture du token porteur)

Préféré : paires de clés d'appareil.

- L'appareil génère une paire de clés une fois.
- `deviceId = fingerprint(publicKey)`.
- Gateway envoie un nonce ; l'appareil signe ; gateway vérifie.
- Les tokens sont émis à une clé publique (preuve de possession), pas une chaîne.

Alternatives :

- mTLS (certificats clients) : le plus fort, plus de complexité opérationnelle.
- Tokens porteurs de courte durée uniquement comme phase temporaire (rotation + révocation précoce).

## Approbation silencieuse (heuristique SSH)

Définissez-la précisément pour éviter un maillon faible. Préférez l'une :

- **Local uniquement** : auto-appairage quand le client se connecte via loopback/socket Unix.
- **Défi via SSH** : gateway émet un nonce ; le client prouve SSH en le récupérant.
- **Fenêtre de présence physique** : après une approbation locale sur l'UI de l'hôte de la passerelle, permettre l'auto-appairage pendant une courte fenêtre (par ex. 10 minutes).

Toujours enregistrer + enregistrer les auto-approbations.

---

# TLS partout (dev + prod)

## Réutiliser le TLS bridge existant

Utiliser le runtime TLS actuel + épinglage d'empreinte :

- `src/infra/bridge/server/tls.ts`
- logique de vérification d'empreinte dans `src/node-host/bridge-client.ts`

## Appliquer à WS

- Le serveur WS supporte TLS avec le même certificat/clé + empreinte.
- Les clients WS peuvent épingler l'empreinte (optionnel).
- La découverte annonce TLS + empreinte pour tous les points de terminaison.
  - La découverte est uniquement des indices de localisateur ; jamais une ancre de confiance.

## Pourquoi

- Réduire la dépendance à SSH/Tailscale pour la confidentialité.
- Rendre les connexions mobiles distantes sûres par défaut.

---

# Refonte des approbations (centralisée)

## Actuel

L'approbation se produit sur l'hôte du nœud (runtime du nœud de l'app mac). L'invite apparaît où le nœud s'exécute.

## Proposé

L'approbation est **hébergée par la passerelle**, l'UI livrée aux clients opérateurs.

### Nouveau flux

1. Gateway reçoit l'intention `system.run` (agent).
2. Gateway crée un enregistrement d'approbation : `approval.requested`.
3. L'UI de l'opérateur affiche l'invite.
4. La décision d'approbation est envoyée à la passerelle : `approval.resolve`.
5. Gateway invoque la commande du nœud si approuvée.
6. Le nœud s'exécute, retourne `invoke-res`.

### Sémantique d'approbation (durcissement)

- Diffuser à tous les opérateurs ; seule l'UI active affiche une modale (les autres reçoivent un toast).
- La première résolution gagne ; la passerelle rejette les résolutions ultérieures comme déjà réglées.
- Délai d'expiration par défaut : refuser après N secondes (par ex. 60s), enregistrer la raison.
- La résolution nécessite la portée `operator.approvals`.

## Avantages

- L'invite apparaît où se trouve l'utilisateur (mac/téléphone).
- Approbations cohérentes pour les nœuds distants.
- Le runtime du nœud reste headless ; pas de dépendance UI.

---

# Exemples de clarté des rôles

## App iPhone

- **Rôle de nœud** pour : mic, caméra, chat vocal, localisation, push-to-talk.
- **Opérateur.read** optionnel pour le statut et la vue de chat.
- **Opérateur.write/admin** optionnel uniquement s'il est explicitement activé.

## App macOS

- Rôle d'opérateur par défaut (UI de contrôle).
- Rôle de nœud quand "Mac node" est activé (system.run, écran, caméra).
- Même deviceId pour les deux connexions → entrée UI fusionnée.

## CLI

- Rôle d'opérateur toujours.
- Portée dérivée par sous-commande :
  - `status`, `logs` → read
  - `agent`, `message` → write
  - `config`, `channels` → admin
  - approbations + appairage → `operator.approvals` / `operator.pairing`

---

# Identité + slugs

## ID stable

Requis pour l'authentification ; ne change jamais.
Préféré :

- Empreinte de paire de clés (hash de clé publique).

## Slug mignon (thème homard)

Étiquette humaine uniquement.

- Exemple : `scarlet-claw`, `saltwave`, `mantis-pinch`.
- Stocké dans le registre de la passerelle, modifiable.
- Gestion des collisions : `-2`, `-3`.

## Groupement UI

Même `deviceId` entre les rôles → ligne "Instance" unique :

- Badge : `operator`, `node`.
- Affiche les capacités + dernière vue.

---

# Stratégie de migration

## Phase 0 : Document + alignement

- Publier ce document.
- Inventorier tous les appels de protocole + flux d'approbation.

## Phase 1 : Ajouter les rôles/portées à WS

- Étendre les paramètres `connect` avec `role`, `scope`, `deviceId`.
- Ajouter le contrôle d'allowlist pour le rôle de nœud.

## Phase 2 : Compatibilité Bridge

- Garder le bridge en cours d'exécution.
- Ajouter le support du nœud WS en parallèle.
- Fonctionnalités de porte derrière le drapeau de configuration.

## Phase 3 : Approbations centrales

- Ajouter les événements de demande + résolution d'approbation dans WS.
- Mettre à jour l'UI de l'app mac pour inviter + répondre.
- Le runtime du nœud arrête d'inviter l'UI.

## Phase 4 : Unification TLS

- Ajouter la configuration TLS pour WS en utilisant le runtime TLS du bridge.
- Ajouter l'épinglage aux clients.

## Phase 5 : Déprécier le bridge

- Migrer le nœud iOS/Android/mac vers WS.
- Garder le bridge comme secours ; supprimer une fois stable.

## Phase 6 : Authentification liée à l'appareil

- Exiger l'identité basée sur les clés pour toutes les connexions non-locales.
- Ajouter l'UI de révocation + rotation.

---

# Notes de sécurité

- Rôle/allowlist appliqué à la limite de la passerelle.
- Aucun client n'obtient l'API "complète" sans portée d'opérateur.
- Appairage requis pour _toutes_ les connexions.
- TLS + épinglage réduit le risque MITM pour mobile.
- L'approbation silencieuse SSH est une commodité ; toujours enregistrée + révocable.
- La découverte n'est jamais une ancre de confiance.
- Les revendications de capacité sont vérifiées par rapport aux allowlists du serveur par plateforme/type.

# Streaming + charges utiles volumineuses (médias de nœud)

Le plan de contrôle WS convient aux petits messages, mais les nœuds font aussi :

- clips caméra
- enregistrements d'écran
- flux audio

Options :

1. Trames binaires WS + chunking + règles de contrepression.
2. Point de terminaison de streaming séparé (toujours TLS + authentification).
3. Garder le bridge plus longtemps pour les commandes gourmandes en médias, migrer en dernier.

Choisissez-en un avant l'implémentation pour éviter la dérive.

# Politique de capacité + commande

- Les capacités/commandes signalées par le nœud sont traitées comme des **revendications**.
- Gateway applique les allowlists par plateforme.
- Toute nouvelle commande nécessite l'approbation de l'opérateur ou un changement d'allowlist explicite.
- Auditer les modifications avec horodatages.

# Audit + limitation de débit

- Journal : demandes d'appairage, approbations/refus, émission/rotation/révocation de tokens.
- Limitation de débit du spam d'appairage et des invites d'approbation.

# Hygiène du protocole

- Version de protocole explicite + codes d'erreur.
- Règles de reconnexion + politique de battement cardiaque.
- TTL de présence et sémantique de dernière vue.

---

# Questions ouvertes

1. Appareil unique exécutant les deux rôles : modèle de token
   - Recommander des tokens séparés par rôle (nœud vs opérateur).
   - Même deviceId ; portées différentes ; révocation plus claire.

2. Granularité de la portée de l'opérateur
   - read/write/admin + approbations + appairage (minimum viable).
   - Considérer les portées par fonctionnalité plus tard.

3. UX de rotation + révocation de token
   - Auto-rotation au changement de rôle.
   - UI pour révoquer par deviceId + rôle.

4. Découverte
   - Étendre le TXT Bonjour actuel pour inclure l'empreinte WS TLS + indices de rôle.
   - Traiter comme des indices de localisateur uniquement.

5. Approbation inter-réseau
   - Diffuser à tous les clients opérateurs ; l'UI active affiche une modale.
   - La première réponse gagne ; la passerelle applique l'atomicité.

---

# Résumé (TL;DR)

- Aujourd'hui : plan de contrôle WS + transport de nœud Bridge.
- Douleur : approbations + duplication + deux piles.
- Proposition : un protocole WS avec rôles + portées explicites, appairage + épinglage TLS unifié, approbations hébergées par la passerelle, IDs d'appareil stables + slugs mignons.
- Résultat : UX plus simple, sécurité plus forte, moins de duplication, meilleur routage mobile.
