```markdown
---
summary: "Plan de refactorisation : routage de l'hôte exec, approbations de nœuds et runner sans interface"
read_when:
  - Conception du routage de l'hôte exec ou des approbations exec
  - Implémentation du runner de nœud + IPC UI
  - Ajout des modes de sécurité de l'hôte exec et des commandes slash
title: "Refactorisation de l'hôte Exec"
---

# Plan de refactorisation de l'hôte exec

## Objectifs

- Ajouter `exec.host` + `exec.security` pour router l'exécution entre **sandbox**, **gateway** et **node**.
- Garder les valeurs par défaut **sûres** : pas d'exécution inter-hôtes sauf si explicitement activée.
- Diviser l'exécution en un **service runner sans interface** avec une UI optionnelle (app macOS) via IPC local.
- Fournir une **politique par agent**, liste d'autorisation, mode demande et liaison de nœud.
- Supporter les **modes demande** qui fonctionnent _avec_ ou _sans_ listes d'autorisation.
- Multi-plateforme : socket Unix + authentification par token (parité macOS/Linux/Windows).

## Non-objectifs

- Pas de migration de liste d'autorisation héritée ou support de schéma hérité.
- Pas de PTY/streaming pour l'exec de nœud (sortie agrégée uniquement).
- Pas de nouvelle couche réseau au-delà du Bridge + Gateway existants.

## Décisions (verrouillées)

- **Clés de config :** `exec.host` + `exec.security` (override par agent autorisé).
- **Élévation :** garder `/elevated` comme alias pour l'accès complet à la gateway.
- **Demande par défaut :** `on-miss`.
- **Stockage des approbations :** `~/.openclaw/exec-approvals.json` (JSON, pas de migration héritée).
- **Runner :** service système sans interface ; l'app UI héberge un socket Unix pour les approbations.
- **Identité du nœud :** utiliser le `nodeId` existant.
- **Authentification du socket :** socket Unix + token (multi-plateforme) ; division ultérieure si nécessaire.
- **État de l'hôte du nœud :** `~/.openclaw/node.json` (id du nœud + token d'appairage).
- **Hôte exec macOS :** exécuter `system.run` à l'intérieur de l'app macOS ; le service hôte du nœud transfère les requêtes via IPC local.
- **Pas d'assistant XPC :** s'en tenir au socket Unix + token + vérifications de pair.

## Concepts clés

### Hôte

- `sandbox` : exec Docker (comportement actuel).
- `gateway` : exec sur l'hôte gateway.
- `node` : exec sur le runner de nœud via Bridge (`system.run`).

### Mode de sécurité

- `deny` : toujours bloquer.
- `allowlist` : autoriser uniquement les correspondances.
- `full` : autoriser tout (équivalent à elevated).

### Mode demande

- `off` : ne jamais demander.
- `on-miss` : demander uniquement quand la liste d'autorisation ne correspond pas.
- `always` : demander à chaque fois.

La demande est **indépendante** de la liste d'autorisation ; la liste d'autorisation peut être utilisée avec `always` ou `on-miss`.

### Résolution de politique (par exec)

1. Résoudre `exec.host` (paramètre d'outil → override d'agent → défaut global).
2. Résoudre `exec.security` et `exec.ask` (même précédence).
3. Si l'hôte est `sandbox`, procéder avec l'exec sandbox local.
4. Si l'hôte est `gateway` ou `node`, appliquer la politique de sécurité + demande sur cet hôte.

## Sécurité par défaut

- `exec.host = sandbox` par défaut.
- `exec.security = deny` par défaut pour `gateway` et `node`.
- `exec.ask = on-miss` par défaut (pertinent uniquement si la sécurité l'autorise).
- Si aucune liaison de nœud n'est définie, **l'agent peut cibler n'importe quel nœud**, mais uniquement si la politique l'autorise.

## Surface de configuration

### Paramètres d'outil

- `exec.host` (optionnel) : `sandbox | gateway | node`.
- `exec.security` (optionnel) : `deny | allowlist | full`.
- `exec.ask` (optionnel) : `off | on-miss | always`.
- `exec.node` (optionnel) : id/nom du nœud à utiliser quand `host=node`.

### Clés de config (global)

- `tools.exec.host`
- `tools.exec.security`
- `tools.exec.ask`
- `tools.exec.node` (liaison de nœud par défaut)

### Clés de config (par agent)

- `agents.list[].tools.exec.host`
- `agents.list[].tools.exec.security`
- `agents.list[].tools.exec.ask`
- `agents.list[].tools.exec.node`

### Alias

- `/elevated on` = définir `tools.exec.host=gateway`, `tools.exec.security=full` pour la session de l'agent.
- `/elevated off` = restaurer les paramètres exec précédents pour la session de l'agent.

## Stockage des approbations (JSON)

Chemin : `~/.openclaw/exec-approvals.json`

Objectif :

- Politique locale + listes d'autorisation pour l'**hôte d'exécution** (gateway ou runner de nœud).
- Fallback de demande quand aucune UI n'est disponible.
- Identifiants IPC pour les clients UI.

Schéma proposé (v1) :

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

Notes :

- Pas de formats de liste d'autorisation hérités.
- `askFallback` s'applique uniquement quand `ask` est requis et qu'aucune UI n'est accessible.
- Permissions de fichier : `0600`.

## Service runner (sans interface)

### Rôle

- Appliquer `exec.security` + `exec.ask` localement.
- Exécuter les commandes système et retourner la sortie.
- Émettre des événements Bridge pour le cycle de vie exec (optionnel mais recommandé).

### Cycle de vie du service

- Launchd/daemon sur macOS ; service système sur Linux/Windows.
- Le JSON des approbations est local à l'hôte d'exécution.
- L'UI héberge un socket Unix local ; les runners se connectent à la demande.

## Intégration UI (app macOS)

### IPC

- Socket Unix à `~/.openclaw/exec-approvals.sock` (0600).
- Token stocké dans `exec-approvals.json` (0600).
- Vérifications de pair : même UID uniquement.
- Challenge/response : nonce + HMAC(token, request-hash) pour prévenir la relecture.
- TTL court (par ex., 10s) + charge utile max + limite de débit.

### Flux de demande (hôte exec app macOS)

1. Le service de nœud reçoit `system.run` de la gateway.
2. Le service de nœud se connecte au socket local et envoie la demande de prompt/exec.
3. L'app valide le pair + token + HMAC + TTL, puis affiche une boîte de dialogue si nécessaire.
4. L'app exécute la commande dans le contexte UI et retourne la sortie.
5. Le service de nœud retourne la sortie à la gateway.

Si l'UI est manquante :

- Appliquer `askFallback` (`deny|allowlist|full`).

### Diagramme (SCI)

```
Agent -> Gateway -> Bridge -> Node Service (TS)
                         |  IPC (UDS + token + HMAC + TTL)
                         v
                     Mac App (UI + TCC + system.run)
```

## Identité du nœud + liaison

- Utiliser le `nodeId` existant de l'appairage Bridge.
- Modèle de liaison :
  - `tools.exec.node` restreint l'agent à un nœud spécifique.
  - Si non défini, l'agent peut choisir n'importe quel nœud (la politique applique toujours les valeurs par défaut).
- Résolution de la sélection du nœud :
  - Correspondance exacte de `nodeId`
  - `displayName` (normalisé)
  - `remoteIp`
  - Préfixe de `nodeId` (>= 6 caractères)

## Événements

### Qui voit les événements

- Les événements système sont **par session** et affichés à l'agent à la prochaine invite.
- Stockés dans la file d'attente en mémoire de la gateway (`enqueueSystemEvent`).

### Texte de l'événement

- `Exec started (node=<id>, id=<runId>)`
- `Exec finished (node=<id>, id=<runId>, code=<code>)` + sortie optionnelle de queue
- `Exec denied (node=<id>, id=<runId>, <reason>)`

### Transport

Option A (recommandée) :

- Le runner envoie les trames Bridge `event` `exec.started` / `exec.finished`.
- Le `handleBridgeEvent` de la gateway mappe ces événements dans `enqueueSystemEvent`.

Option B :

- L'outil `exec` de la gateway gère le cycle de vie directement (synchrone uniquement).

## Flux d'exec

### Hôte sandbox

- Comportement `exec` existant (Docker ou hôte quand non sandboxé).
- PTY supporté en mode non-sandbox uniquement.

### Hôte gateway

- Le processus gateway s'exécute sur sa propre machine.
- Applique le `exec-approvals.json` local (sécurité/demande/liste d'autorisation).

### Hôte node

- La gateway appelle `node.invoke` avec `system.run`.
- Le runner applique les approbations locales.
- Le runner retourne stdout/stderr agrégés.
- Événements Bridge optionnels pour start/finish/deny.

## Limites de sortie

- Limiter stdout+stderr combinés à **200k** ; conserver **queue 20k** pour les événements.
- Tronquer avec un suffixe clair (par ex., `"… (truncated)"`).

## Commandes slash

- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>`
- Overrides par agent, par session ; non-persistants sauf s'ils sont sauvegardés via config.
- `/elevated on|off|ask|full` reste un raccourci pour `host=gateway security=full` (avec `full` ignorant les approbations).

## Histoire multi-plateforme

- Le service runner est la cible d'exécution portable.
- L'UI est optionnelle ; si manquante, `askFallback` s'applique.
- Windows/Linux supportent le même protocole JSON des approbations + socket.

## Phases d'implémentation

### Phase 1 : config + routage exec

- Ajouter le schéma de config pour `exec.host`, `exec.security`, `exec.ask`, `exec.node`.
- Mettre à jour le plumbing d'outil pour respecter `exec.host`.
- Ajouter la commande slash `/exec` et garder l'alias `/elevated`.

### Phase 2 : stockage des approbations + application gateway

- Implémenter le lecteur/writer `exec-approvals.json`.
- Appliquer la liste d'autorisation + modes de demande pour l'hôte `gateway`.
- Ajouter les limites de sortie.

### Phase 3 : application du runner de nœud

- Mettre à jour le runner de nœud pour appliquer la liste d'autorisation + demande.
- Ajouter le pont de prompt du socket Unix à l'UI de l'app macOS.
- Câbler `askFallback`.

### Phase 4 : événements

- Ajouter les événements Bridge nœud → gateway pour le cycle de vie exec.
- Mapper à `enqueueSystemEvent` pour les invites d'agent.

### Phase 5 : polish UI

- App Mac : éditeur de liste d'autorisation, sélecteur par agent, UI de politique de demande.
- Contrôles de liaison de nœud (optionnel).

## Plan de test

- Tests unitaires : correspondance de liste d'autorisation (glob + insensible à la casse).
- Tests unitaires : résolution de politique de précédence (paramètre d'outil → override d'agent → global).
- Tests d'intégration : flux de deny/allow/ask du runner de nœud.
- Tests d'événement Bridge : routage d'événement de nœud → événement système.

## Risques ouverts

- Indisponibilité de l'UI : s'assurer que `askFallback` est respecté.
- Commandes longues : s'appuyer sur timeout + limites de sortie.
- Ambiguïté multi-nœud : erreur sauf si liaison de nœud ou paramètre de nœud explicite.

## Docs connexes

- [Outil Exec](/tools/exec)
- [Approbations Exec](/tools/exec-approvals)
- [Nœuds](/nodes)
- [Mode Elevated](/tools/elevated)
```
