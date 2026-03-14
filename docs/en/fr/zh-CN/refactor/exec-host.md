# Plan de refonte de l'hôte Exec

## Objectifs

- Ajouter `exec.host` + `exec.security` pour router l'exécution entre le **bac à sable**, la **passerelle Gateway** et les **nœuds**.
- Maintenir la sécurité par défaut : pas d'exécution inter-hôtes sauf activation explicite.
- Diviser l'exécution en **service de runner sans interface**, connecté optionnellement à une UI (application macOS) via IPC local.
- Fournir des **politiques par agent**, listes blanches, mode interrogation et liaison de nœuds.
- Supporter le **mode interrogation** *avec* ou *sans* liste blanche.
- Multi-plateforme : socket Unix + authentification par token (cohérence macOS/Linux/Windows).

## Non-objectifs

- Aucune migration de liste blanche héritée ou support de schéma hérité.
- Pas de PTY/streaming pour exec de nœud (sortie agrégée uniquement).
- Aucune nouvelle couche réseau au-delà du Bridge + Gateway existants.

## Décisions (verrouillées)

- **Clés de configuration :** `exec.host` + `exec.security` (permettre les remplacements par agent).
- **Élévation :** Conserver `/elevated` comme alias pour accès complet à la Gateway.
- **Défaut d'interrogation :** `on-miss`.
- **Stockage des approbations :** `~/.openclaw/exec-approvals.json` (JSON, pas de migration héritée).
- **Runner :** Service système sans interface ; l'application UI héberge le socket Unix pour les approbations.
- **Identité du nœud :** Utiliser le `nodeId` existant.
- **Authentification du socket :** Socket Unix + token (multi-plateforme) ; scission ultérieure si nécessaire.
- **État de l'hôte du nœud :** `~/.openclaw/node.json` (id du nœud + token d'appairage).
- **Hôte exec macOS :** Exécuter `system.run` dans l'application macOS ; le service hôte du nœud transfère les requêtes via IPC local.
- **Pas de helper XPC :** S'en tenir aux sockets Unix + token + vérification des pairs.

## Concepts clés

### Hôtes

- `sandbox` : Exec Docker (comportement actuel).
- `gateway` : Exécution sur l'hôte Gateway.
- `node` : Exécution sur le runner du nœud via Bridge (`system.run`).

### Modes de sécurité

- `deny` : Toujours bloquer.
- `allowlist` : Autoriser uniquement les correspondances.
- `full` : Tout autoriser (équivalent au mode élevé).

### Modes d'interrogation

- `off` : Ne jamais interroger.
- `on-miss` : Interroger uniquement si la liste blanche ne correspond pas.
- `always` : Interroger à chaque fois.

L'interrogation est **indépendante** de la liste blanche ; la liste blanche peut être utilisée avec `always` ou `on-miss`.

### Résolution de politique (par exécution)

1. Résoudre `exec.host` (paramètre d'outil → remplacement d'agent → défaut global).
2. Résoudre `exec.security` et `exec.ask` (même priorité).
3. Si l'hôte est `sandbox`, continuer l'exécution locale du bac à sable.
4. Si l'hôte est `gateway` ou `node`, appliquer la politique de sécurité + interrogation sur cet hôte.

## Sécurité par défaut

- Défaut `exec.host = sandbox`.
- Défaut `exec.security = deny` pour `gateway` et `node`.
- Défaut `exec.ask = on-miss` (pertinent uniquement si la sécurité le permet).
- Si aucune liaison de nœud n'est définie, **l'agent peut diriger vers n'importe quel nœud**, mais uniquement si la politique le permet.

## Surface de configuration

### Paramètres d'outil

- `exec.host` (optionnel) : `sandbox | gateway | node`.
- `exec.security` (optionnel) : `deny | allowlist | full`.
- `exec.ask` (optionnel) : `off | on-miss | always`.
- `exec.node` (optionnel) : ID/nom du nœud à utiliser quand `host=node`.

### Clés de configuration (globales)

- `tools.exec.host`
- `tools.exec.security`
- `tools.exec.ask`
- `tools.exec.node` (liaison de nœud par défaut)

### Clés de configuration (par agent)

- `agents.list[].tools.exec.host`
- `agents.list[].tools.exec.security`
- `agents.list[].tools.exec.ask`
- `agents.list[].tools.exec.node`

### Alias

- `/elevated on` = Définir `tools.exec.host=gateway`, `tools.exec.security=full` pour la session d'agent.
- `/elevated off` = Restaurer les paramètres exec précédents pour la session d'agent.

## Stockage des approbations (JSON)

Chemin : `~/.openclaw/exec-approvals.json`

Utilisation :

- **Politique locale + liste blanche** pour l'hôte d'exécution (Gateway ou runner du nœud).
- Secours d'interrogation quand aucune UI n'est disponible.
- Identifiants IPC pour les clients UI.

Schéma recommandé (v1) :

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64-opaque-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny"
  },
  "agents": {
    "agent-id-1": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [
        {
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 0,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

Remarques :

- Aucun format de liste blanche hérité.
- `askFallback` s'applique uniquement si `ask` est nécessaire et que l'UI n'est pas accessible.
- Permissions de fichier : `0600`.

## Service de runner (sans interface)

### Rôle

- Appliquer localement `exec.security` + `exec.ask`.
- Exécuter les commandes système et retourner la sortie.
- Émettre des événements Bridge pour le cycle de vie exec (optionnel mais recommandé).

### Cycle de vie du service

- Launchd/daemon sur macOS ; service système sur Linux/Windows.
- JSON d'approbation local à l'hôte d'exécution.
- UI héberge le socket Unix local ; le runner se connecte à la demande.

## Intégration UI (application macOS)

### IPC

- Socket Unix à `~/.openclaw/exec-approvals.sock` (0600).
- Token stocké dans `exec-approvals.json` (0600).
- Vérification des pairs : UID identique uniquement.
- Défi/réponse : nonce + HMAC(token, request-hash) pour prévenir la relecture.
- TTL court (par ex. 10s) + charge utile maximale + limitation de débit.

### Flux d'interrogation (hôte exec de l'application macOS)

1. Le service du nœud reçoit `system.run` de la Gateway.
2. Le service du nœud se connecte au socket local et envoie une demande d'invite/exec.
3. L'application vérifie le pair + token + HMAC + TTL, puis affiche une boîte de dialogue si nécessaire.
4. L'application exécute la commande dans le contexte UI et retourne la sortie.
5. Le service du nœud retourne la sortie à la Gateway.

Si l'UI est manquante :

- Appliquer `askFallback` (`deny|allowlist|full`).

### Diagramme (SCI)

```
Agent -> Gateway -> Bridge -> Node Service (TS)
                         |  IPC (UDS + token + HMAC + TTL)
                         v
                     Mac App (UI + TCC + system.run)
```

## Identité du nœud + liaisons

- Utiliser le `nodeId` existant de l'appairage Bridge.
- Modèle de liaison :
  - `tools.exec.node` restreint l'agent à un nœud spécifique.
  - Si non défini, l'agent peut sélectionner n'importe quel nœud (la politique applique toujours les défauts).
- Résolution de sélection du nœud :
  - Correspondance exacte de `nodeId`
  - `displayName` (normalisé)
  - `remoteIp`
  - Préfixe de `nodeId` (>= 6 caractères)

## Événements

### Qui voit les événements

- Les événements système sont **par session**, affichés à l'agent à l'invite suivante.
- Stockés dans la file d'attente mémoire de la Gateway (`enqueueSystemEvent`).

### Texte des événements

- `Exec started (node=<id>, id=<runId>)`
- `Exec finished (node=<id>, id=<runId>, code=<code>)` + queue de sortie optionnelle
- `Exec denied (node=<id>, id=<runId>, <reason>)`

### Transport

Option A (recommandée) :

- Le runner envoie une trame Bridge `event` `exec.started` / `exec.finished`.
- La Gateway `handleBridgeEvent` mappe ceux-ci à `enqueueSystemEvent`.

Option B :

- La Gateway gère directement le cycle de vie dans l'outil `exec` (synchrone uniquement).

## Flux Exec

### Hôte bac à sable

- Comportement `exec` existant (Docker ou hôte quand pas de bac à sable).
- PTY supporté uniquement en mode non-bac à sable.

### Hôte Gateway

- Le processus Gateway exécute sur sa propre machine.
- Applique localement `exec-approvals.json` (sécurité/interrogation/liste blanche).

### Hôte du nœud

- La Gateway appelle `node.invoke` avec `system.run`.
- Le runner applique les approbations locales.
- Le runner retourne stdout/stderr agrégés.
- Événements Bridge optionnels pour début/fin/refus.

## Limite de sortie

- Limite combinée stdout+stderr de **200k** ; réserver **queue de 20k** pour les événements.
- Utiliser une troncature avec suffixe clair (par ex. `"… (truncated)"`).

## Commandes slash

- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>`
- Remplacements par agent, par session ; non persistants sauf sauvegarde via configuration.
- `/elevated on|off|ask|full` reste un raccourci pour `host=gateway security=full` (`full` ignore les approbations).

## Solution multi-plateforme

- Le service de runner est une cible d'exécution portable.
- L'UI est optionnelle ; si manquante, appliquer `askFallback`.
- Support Windows/Linux avec le même JSON d'approbation + protocole socket.

## Phases d'implémentation

### Phase 1 : Configuration + routage exec

- Ajouter le schéma de configuration pour `exec.host`, `exec.security`, `exec.ask`, `exec.node`.
- Mettre à jour le pipeline d'outils pour respecter `exec.host`.
- Ajouter la commande slash `/exec` et conserver l'alias `/elevated`.

### Phase 2 : Stockage des approbations + application Gateway

- Implémenter le lecteur/writer `exec-approvals.json`.
- Appliquer la liste blanche + mode interrogation pour l'hôte `gateway`.
- Ajouter la limite de sortie.

### Phase 3 : Application du runner du nœud

- Mettre à jour le runner du nœud pour appliquer la liste blanche + interrogation.
- Ajouter le pontage du socket Unix vers l'UI de l'application macOS.
- Connecter `askFallback`.

### Phase 4 : Événements

- Ajouter les événements Bridge pour le cycle de vie exec nœud → Gateway.
- Mapper à `enqueueSystemEvent` pour l'invite d'agent.

### Phase 5 : Perfectionnement UI

- Application Mac : éditeur de liste blanche, commutateurs par agent, UI de politique d'interrogation.
- Contrôles de liaison de nœud (optionnel).

## Plan de test

- Tests unitaires : correspondance de liste blanche (glob + insensible à la casse).
- Tests unitaires : priorité de résolution de politique (paramètre d'outil → remplacement d'agent → global).
- Tests d'intégration : flux de refus/autorisation/interrogation du runner du nœud.
- Tests d'événements Bridge : routage événement nœud → événement système.

## Risques ouverts

- UI indisponible : assurer le respect de `askFallback`.
- Commandes longues : dépendre du timeout + limite de sortie.
- Ambiguïté multi-nœud : erreur sauf liaison de nœud ou paramètre de nœud explicite.

## Documentation connexe

- [Outil Exec](/tools/exec)
- [Approbations d'exécution](/tools/exec-approvals)
- [Nœuds](/nodes)
- [Mode élevé](/tools/elevated)
