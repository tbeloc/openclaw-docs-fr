---
read_when:
  - Protocole réseau unifié pour nœud de planification + client opérateur
  - Repenser l'approbation, l'appairage, TLS et l'état en ligne entre appareils
summary: Restructuration Clawnet : protocole réseau unifié, rôles, authentification, approbation, identité
title: Restructuration Clawnet
x-i18n:
  generated_at: "2026-02-03T07:55:03Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 719b219c3b326479658fe6101c80d5273fc56eb3baf50be8535e0d1d2bb7987f
  source_path: refactor/clawnet.md
  workflow: 15
---

# Restructuration Clawnet (Protocole + Authentification unifiés)

## Salut

Salut Peter — la direction est bonne ; cela déverrouillera une expérience utilisateur plus simple + une sécurité plus forte.

## Objectif

Un document unique et rigoureux pour :

- État actuel : protocoles, flux, limites de confiance.
- Points douloureux : approbation, routage multi-sauts, répétition UI.
- État nouveau proposé : un protocole, rôles délimités, authentification/appairage unifiés, épinglage TLS.
- Modèle d'identité : ID stable + alias mignons.
- Plan de migration, risques, questions ouvertes.

## Objectifs (issus des discussions)

- Tous les clients utilisent un protocole (app mac, CLI, iOS, Android, nœuds sans interface).
- Chaque participant au réseau est authentifié + apparié.
- Rôles clairs : nœud vs opérateur.
- Routage d'approbation centralisé vers l'emplacement de l'utilisateur.
- Tout le trafic distant utilise TLS chiffré + épinglage optionnel.
- Minimiser la duplication de code.
- Une seule machine ne devrait apparaître qu'une fois (pas d'entrées UI/nœud dupliquées).

## Non-objectifs (explicites)

- Supprimer la séparation des capacités (le principe du moindre privilège est toujours nécessaire).
- Exposer le plan de contrôle Gateway complet sans vérification de portée.
- Rendre l'authentification dépendante des étiquettes humaines (les alias restent non-sécuritaires).

---

# État actuel (Situation présente)

## Deux protocoles

### 1) WebSocket Gateway (plan de contrôle)

- Surface API complète : configuration, canaux, modèles, sessions, exécutions d'agents, journaux, nœuds, etc.
- Liaison par défaut : loopback. Accès distant via SSH/Tailscale.
- Authentification : via jeton/mot de passe dans `connect`.
- Pas d'épinglage TLS (dépend de loopback/tunnel).
- Code :
  - `src/gateway/server/ws-connection/message-handler.ts`
  - `src/gateway/client.ts`
  - `docs/gateway/protocol.md`

### 2) Bridge (transport de nœud)

- Surface de liste blanche étroite, identité de nœud + appairage.
- JSONL sur TCP ; TLS optionnel + épinglage d'empreinte de certificat.
- TLS publie l'empreinte dans le TXT de découverte d'appareil.
- Code :
  - `src/infra/bridge/server/connection.ts`
  - `src/gateway/server-bridge.ts`
  - `src/node-host/bridge-client.ts`
  - `docs/gateway/bridge-protocol.md`

## Clients du plan de contrôle actuels

- CLI → se connecte à Gateway WS via `callGateway` (`src/gateway/call.ts`).
- UI app macOS → Gateway WS (`GatewayConnection`).
- UI contrôle web → Gateway WS.
- ACP → Gateway WS.
- Contrôle navigateur utilise son propre serveur de contrôle HTTP.

## Nœuds actuels

- App macOS en mode nœud se connecte à Gateway bridge (`MacNodeBridgeSession`).
- Apps iOS/Android se connectent à Gateway bridge.
- Appairage + stockage de jeton par nœud sur Gateway.

## Flux d'approbation actuel (exec)

- Agent utilise `system.run` via Gateway.
- Gateway appelle le nœud via bridge.
- Nœud décide de l'approbation au moment de l'exécution.
- Invite UI affichée par app mac (quand nœud == app mac).
- Nœud retourne `invoke-res` à Gateway.
- Multi-sauts, UI liée à l'hôte du nœud.

## État en ligne actuel + identité

- Entrées d'état en ligne Gateway depuis clients WS.
- Entrées d'état en ligne de nœud depuis bridge.
- App mac peut afficher deux entrées pour la même machine (UI + nœud).
- Identité de nœud stockée dans magasin d'appairage ; identité UI séparée.

---

# Problèmes/Points douloureux

- Besoin de maintenir deux piles de protocoles (WS + Bridge).
- Approbation sur nœud distant : invite apparaît sur l'hôte du nœud, pas où se trouve l'utilisateur.
- Épinglage TLS existe uniquement dans bridge ; WS dépend de SSH/Tailscale.
- Identité dupliquée : même machine affichée comme plusieurs instances.
- Rôles flous : capacités UI + nœud + CLI sans séparation claire.

---

# État nouveau proposé (Clawnet)

## Un protocole, deux rôles

Protocole WS unique avec rôles + portées.

- **Rôle : node** (hôte de capacité)
- **Rôle : operator** (plan de contrôle)
- **Portées** optionnelles pour opérateur :
  - `operator.read` (état + visualisation)
  - `operator.write` (exécution d'agent, envoi)
  - `operator.admin` (configuration, canaux, modèles)

### Comportements des rôles

**Node**

- Peut enregistrer des capacités (`caps`, `commands`, permissions).
- Peut recevoir des commandes `invoke` (`system.run`, `camera.*`, `canvas.*`, `screen.record`, etc.).
- Peut envoyer des événements : `voice.transcript`, `agent.request`, `chat.subscribe`.
- Ne peut pas appeler les API du plan de contrôle configuration/modèles/canaux/sessions/agents.

**Operator**

- API du plan de contrôle complet, limité par portée.
- Reçoit toutes les approbations.
- N'exécute pas directement les opérations OS ; route vers les nœuds.

### Règles clés

Les rôles sont par connexion, pas par appareil. Un appareil peut ouvrir deux rôles séparément.

---

# Authentification + Appairage unifiés

## Identité du client

Chaque client fournit :

- `deviceId` (stable, dérivé de la clé d'appareil).
- `displayName` (nom humain).
- `role` + `scope` + `caps` + `commands`.

## Flux d'appairage (unifié)

- Client se connecte non authentifié.
- Gateway crée une **demande d'appairage** pour ce `deviceId`.
- Opérateur reçoit une invite ; approuve/rejette.
- Gateway émet une accréditation liée à :
  - Clé publique d'appareil
  - Rôle
  - Portée
  - Capacités/commandes
- Client persiste le jeton, réauthentifie la connexion.

## Authentification liée à l'appareil (éviter la relecture de jeton bearer)

Préféré : paire de clés d'appareil.

- Appareil génère une paire de clés une fois.
- `deviceId = fingerprint(publicKey)`.
- Gateway envoie un nonce ; appareil signe ; Gateway vérifie.
- Jeton émis à la clé publique (preuve de propriété), pas à une chaîne.

Alternatives :

- mTLS (certificat client) : le plus fort, complexité opérationnelle plus élevée.
- Jetons bearer à court terme uniquement comme phase temporaire (rotation précoce + révocation).

## Approbation silencieuse (inspirée par SSH)

Définir précisément pour éviter les faiblesses. Choisir l'une :

- **Loopback uniquement** : appairage automatique quand le client se connecte via loopback/socket Unix.
- **Défi SSH** : Gateway émet un nonce ; client prouve via SSH en le récupérant.
- **Fenêtre de présence physique** : après approbation locale sur UI d'hôte Gateway, permettre appairage automatique dans fenêtre courte (ex. 10 min).

Toujours enregistrer + journaliser les approbations automatiques.

---

# TLS partout (développement + production)

## Réutiliser le TLS bridge existant

Utiliser le runtime TLS actuel + épinglage d'empreinte :

- `src/infra/bridge/server/tls.ts`
- Logique de vérification d'empreinte dans `src/node-host/bridge-client.ts`

## Appliquer à WS

- Serveur WS utilise même certificat/clé + support d'épinglage TLS.
- Client WS peut épingler l'empreinte (optionnel).
- Découverte d'appareil publie TLS + empreinte pour tous les points de terminaison.
  - Découverte d'appareil est juste un localisateur ; jamais une ancre de confiance.

## Pourquoi

- Réduire la dépendance au secret de SSH/Tailscale.
- Sécuriser les connexions mobiles distantes par défaut.

---

# Repenser l'approbation (centralisée)

## Actuel

L'approbation se produit sur l'hôte du nœud (runtime de nœud app mac). L'invite apparaît où le nœud s'exécute.

## Proposé

L'approbation est **hébergée par Gateway**, UI transmise au client opérateur.

### Nouveau flux

1. Gateway reçoit intention `system.run` (agent).
2. Gateway crée enregistrement d'approbation : `approval.requested`.
3. UI opérateur affiche l'invite.
4. Décision d'approbation envoyée à Gateway : `approval.resolve`.
5. Si approuvé, Gateway appelle commande de nœud.
6. Nœud exécute, retourne `invoke-res`.

### Sémantique d'approbation (renforcée)

- Diffusée à tous les opérateurs ; seule UI active affiche modal (autres affichent toast).
- Premier résolveur gagne ; Gateway rejette résolutions ultérieures comme réglées.
- Délai d'expiration par défaut : rejeté après N secondes (ex. 60 sec), raison enregistrée.
- Résolution nécessite portée `operator.approvals`.

## Avantages

- Invite apparaît où se trouve l'utilisateur (mac/téléphone).
- Approbation cohérente pour nœuds distants.
- Runtime de nœud reste sans interface ; pas de dépendance UI.

---

# Exemples de clarté des rôles

## App iPhone

- **Rôle Node** pour : microphone, caméra, chat vocal, localisation, appel d'une touche.
- **operator.read** optionnel pour état et vues de chat.
- **operator.write/admin** optionnel uniquement si explicitement activé.

## App macOS

- Rôle Operator par défaut (UI de contrôle).
- Rôle Node quand "Mac Node" activé (system.run, écran, caméra).
- Deux connexions utilisent même `deviceId` → entrée UI fusionnée.

## CLI

- Toujours rôle Operator.
- Portées dérivées par sous-commande :
  - `status`, `logs` → read
  - `agent`, `message` → write
  - `config`, `channels` → admin
  - approbation + appairage → `operator.approvals` / `operator.pairing`

---

# Identité + Alias

## ID stable

Requis pour authentification ; ne change jamais.
Préféré :

- Empreinte de paire de clés (hash de clé publique).

## Alias mignons (thème homard)

Étiquettes humaines uniquement.

- Exemples : `scarlet-claw`, `saltwave`, `mantis-pinch`.
- Stockés dans registre Gateway, modifiables.
- Gestion des conflits : `-2`, `-3`.

## Groupement UI

Même `deviceId` entre rôles → ligne "instance" unique :

- Badges : `operator`, `node`.
- Affiche capacités + dernière connexion.

---

# Stratégie de migration

## Phase 0 : Documentation + Alignement

- Publier ce document.
- Inventorier tous les appels de protocole + flux d'approbation.

## Phase 1 : Ajouter rôles/portées à WS

- Étendre paramètres `connect` avec `role`, `scope`, `deviceId`.
- Ajouter restrictions de liste blanche pour rôle node.

## Phase 2 : Compatibilité Bridge

- Garder bridge en fonctionnement.
- Ajouter en parallèle support WS node.
- Limiter fonctionnalités via drapeau de configuration.

## Phase 3 : Approbation centralisée

- Ajouter événements demande + résolution d'approbation dans WS.
- Mettre à jour UI app mac pour inviter + répondre.
- Runtime de nœud arrête d'inviter UI.

## Phase 4 : Unification TLS

- Ajouter configuration TLS à WS utilisant runtime TLS bridge.
- Ajouter épinglage aux clients.

## Phase 5 : Déprécier Bridge

- Migrer nœuds iOS/Android/mac vers WS.
- Garder bridge comme secours ; supprimer après stabilisation.

## Phase 6 : Authentification liée à l'appareil

- Toutes connexions non-locales nécessitent identité basée clé.
- Ajouter UI révocation + rotation.

---

# Notes de sécurité

- Rôles/listes blanches appliqués à limite Gateway.
- Aucun client ne peut obtenir API "complet" sans portée operator.
- *Toutes* connexions nécessitent appairage.
- TLS + épinglage réduisent risque MITM pour appareils mobiles.
- Approbation silencieuse SSH est mesure de commodité ; toujours enregistrée + révocable.
- Découverte d'appareil jamais ancre de confiance.
- Déclarations de capacité validées par listes blanches serv
