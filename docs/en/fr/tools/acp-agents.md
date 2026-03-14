# Agents ACP

Les sessions du [protocole client agent (ACP)](https://agentclientprotocol.com/) permettent à OpenClaw d'exécuter des harnesses de codage externes (par exemple Pi, Claude Code, Codex, OpenCode et Gemini CLI) via un plugin backend ACP.

Si vous demandez à OpenClaw en langage naturel « exécute ceci dans Codex » ou « démarre Claude Code dans un thread », OpenClaw doit router cette demande vers le runtime ACP (et non vers le runtime natif du sous-agent).

## Flux opérateur rapide

Utilisez ceci quand vous voulez un runbook `/acp` pratique :

1. Créez une session :
   - `/acp spawn codex --mode persistent --thread auto`
2. Travaillez dans le thread lié (ou ciblez explicitement cette clé de session).
3. Vérifiez l'état du runtime :
   - `/acp status`
4. Ajustez les options du runtime selon les besoins :
   - `/acp model <provider/model>`
   - `/acp permissions <profile>`
   - `/acp timeout <seconds>`
5. Guidez une session active sans remplacer le contexte :
   - `/acp steer tighten logging and continue`
6. Arrêtez le travail :
   - `/acp cancel` (arrêter le tour actuel), ou
   - `/acp close` (fermer la session + supprimer les liaisons)

## Démarrage rapide pour les utilisateurs

Exemples de demandes naturelles :

- « Démarre une session Codex persistante dans un thread ici et garde-la concentrée. »
- « Exécute ceci comme une session ACP Claude Code unique et résume le résultat. »
- « Utilise Gemini CLI pour cette tâche dans un thread, puis garde les suites dans le même thread. »

Ce qu'OpenClaw doit faire :

1. Choisir `runtime: "acp"`.
2. Résoudre la cible de harness demandée (`agentId`, par exemple `codex`).
3. Si la liaison de thread est demandée et que le canal actuel la supporte, lier la session ACP au thread.
4. Router les messages de suivi du thread vers la même session ACP jusqu'à ce qu'elle soit défocalisée/fermée/expirée.

## ACP versus sous-agents

Utilisez ACP quand vous voulez un runtime de harness externe. Utilisez les sous-agents quand vous voulez des exécutions déléguées natives d'OpenClaw.

| Zone          | Session ACP                           | Exécution de sous-agent                |
| ------------- | ------------------------------------- | -------------------------------------- |
| Runtime       | Plugin backend ACP (par exemple acpx) | Runtime natif de sous-agent OpenClaw   |
| Clé de session| `agent:<agentId>:acp:<uuid>`          | `agent:<agentId>:subagent:<uuid>`      |
| Commandes principales | `/acp ...`                            | `/subagents ...`                       |
| Outil de création | `sessions_spawn` avec `runtime:"acp"` | `sessions_spawn` (runtime par défaut)  |

Voir aussi [Sous-agents](/tools/subagents).

## Sessions liées à un thread (indépendantes du canal)

Quand les liaisons de thread sont activées pour un adaptateur de canal, les sessions ACP peuvent être liées à des threads :

- OpenClaw lie un thread à une session ACP cible.
- Les messages de suivi dans ce thread sont routés vers la session ACP liée.
- La sortie ACP est renvoyée au même thread.
- Défocaliser/fermer/archiver/expiration du délai d'inactivité ou de l'âge maximum supprime la liaison.

Le support de liaison de thread est spécifique à l'adaptateur. Si l'adaptateur de canal actif ne supporte pas les liaisons de thread, OpenClaw retourne un message clair indiquant que c'est non supporté/indisponible.

Drapeaux de fonctionnalité requis pour ACP lié à un thread :

- `acp.enabled=true`
- `acp.dispatch.enabled` est activé par défaut (définir `false` pour mettre en pause la distribution ACP)
- Drapeau de création de thread ACP de l'adaptateur de canal activé (spécifique à l'adaptateur)
  - Discord : `channels.discord.threadBindings.spawnAcpSessions=true`
  - Telegram : `channels.telegram.threadBindings.spawnAcpSessions=true`

### Canaux supportant les threads

- Tout adaptateur de canal qui expose la capacité de liaison de session/thread.
- Support intégré actuel :
  - Threads/canaux Discord
  - Sujets Telegram (sujets de forum dans les groupes/supergroupes et sujets DM)
- Les canaux de plugin peuvent ajouter le support via la même interface de liaison.

## Paramètres spécifiques au canal

Pour les workflows non éphémères, configurez les liaisons ACP persistantes dans les entrées `bindings[]` de niveau supérieur.

### Modèle de liaison

- `bindings[].type="acp"` marque une liaison de conversation ACP persistante.
- `bindings[].match` identifie la conversation cible :
  - Canal ou thread Discord : `match.channel="discord"` + `match.peer.id="<channelOrThreadId>"`
  - Sujet de forum Telegram : `match.channel="telegram"` + `match.peer.id="<chatId>:topic:<topicId>"`
- `bindings[].agentId` est l'id d'agent OpenClaw propriétaire.
- Les remplacements ACP optionnels se trouvent sous `bindings[].acp` :
  - `mode` (`persistent` ou `oneshot`)
  - `label`
  - `cwd`
  - `backend`

### Valeurs par défaut du runtime par agent

Utilisez `agents.list[].runtime` pour définir les valeurs par défaut ACP une fois par agent :

- `agents.list[].runtime.type="acp"`
- `agents.list[].runtime.acp.agent` (id du harness, par exemple `codex` ou `claude`)
- `agents.list[].runtime.acp.backend`
- `agents.list[].runtime.acp.mode`
- `agents.list[].runtime.acp.cwd`

Ordre de précédence des remplacements pour les sessions liées ACP :

1. `bindings[].acp.*`
2. `agents.list[].runtime.acp.*`
3. Valeurs par défaut ACP globales (par exemple `acp.backend`)

Exemple :

```json5
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
      },
      {
        id: "claude",
        runtime: {
          type: "acp",
          acp: { agent: "claude", backend: "acpx", mode: "persistent" },
        },
      },
    ],
  },
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "discord",
        accountId: "default",
        peer: { kind: "channel", id: "222222222222222222" },
      },
      acp: { label: "codex-main" },
    },
    {
      type: "acp",
      agentId: "claude",
      match: {
        channel: "telegram",
        accountId: "default",
        peer: { kind: "group", id: "-1001234567890:topic:42" },
      },
      acp: { cwd: "/workspace/repo-b" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "discord", accountId: "default" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "telegram", accountId: "default" },
    },
  ],
  channels: {
    discord: {
      guilds: {
        "111111111111111111": {
          channels: {
            "222222222222222222": { requireMention: false },
          },
        },
      },
    },
    telegram: {
      groups: {
        "-1001234567890": {
          topics: { "42": { requireMention: false } },
        },
      },
    },
  },
}
```

Comportement :

- OpenClaw s'assure que la session ACP configurée existe avant utilisation.
- Les messages dans ce canal ou sujet sont routés vers la session ACP configurée.
- Dans les conversations liées, `/new` et `/reset` réinitialisent la même clé de session ACP en place.
- Les liaisons de runtime temporaires (par exemple créées par les flux de focus de thread) s'appliquent toujours le cas échéant.

## Démarrer les sessions ACP (interfaces)

### Depuis `sessions_spawn`

Utilisez `runtime: "acp"` pour démarrer une session ACP à partir d'un tour d'agent ou d'un appel d'outil.

```json
{
  "task": "Open the repo and summarize failing tests",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session"
}
```

Notes :

- `runtime` est par défaut `subagent`, donc définissez explicitement `runtime: "acp"` pour les sessions ACP.
- Si `agentId` est omis, OpenClaw utilise `acp.defaultAgent` quand il est configuré.
- `mode: "session"` nécessite `thread: true` pour maintenir une conversation liée persistante.

Détails de l'interface :

- `task` (requis) : invite initiale envoyée à la session ACP.
- `runtime` (requis pour ACP) : doit être `"acp"`.
- `agentId` (optionnel) : id du harness cible ACP. Revient à `acp.defaultAgent` s'il est défini.
- `thread` (optionnel, par défaut `false`) : demander le flux de liaison de thread où supporté.
- `mode` (optionnel) : `run` (unique) ou `session` (persistant).
  - par défaut `run`
  - si `thread: true` et mode omis, OpenClaw peut par défaut utiliser un comportement persistant selon le chemin du runtime
  - `mode: "session"` nécessite `thread: true`
- `cwd` (optionnel) : répertoire de travail du runtime demandé (validé par la politique du backend/runtime).
- `label` (optionnel) : étiquette orientée opérateur utilisée dans le texte de session/bannière.
- `resumeSessionId` (optionnel) : reprendre une session ACP existante au lieu d'en créer une nouvelle. L'agent rejoue son historique de conversation via `session/load`. Nécessite `runtime: "acp"`.
- `streamTo` (optionnel) : `"parent"` diffuse les résumés de progression initiale de l'exécution ACP vers la session du demandeur en tant qu'événements système.
  - Quand disponible, les réponses acceptées incluent `streamLogPath` pointant vers un journal JSONL limité à la session (`<sessionId>.acp-stream.jsonl`) que vous pouvez suivre pour l'historique complet du relais.

### Reprendre une session existante

Utilisez `resumeSessionId` pour continuer une session ACP précédente au lieu de recommencer à zéro. L'agent rejoue son historique de conversation via `session/load`, il reprend donc avec le contexte complet de ce qui s'est passé avant.

```json
{
  "task": "Continue where we left off — fix the remaining test failures",
  "runtime": "acp",
  "agentId": "codex",
  "resumeSessionId": "<previous-session-id>"
}
```

Cas d'usage courants :

- Transférer une session Codex de votre ordinateur portable à votre téléphone — dites à votre agent de reprendre où vous vous étiez arrêté
- Continuer une session de codage que vous avez démarrée de manière interactive dans la CLI, maintenant sans tête via votre agent
- Reprendre le travail qui a été interrompu par un redémarrage de passerelle ou un délai d'inactivité

Notes :

- `resumeSessionId` nécessite `runtime: "acp"` — retourne une erreur s'il est utilisé avec le runtime du sous-agent.
- `resumeSessionId` restaure l'historique de conversation ACP en amont ; `thread` et `mode` s'appliquent toujours normalement à la nouvelle session OpenClaw que vous créez, donc `mode: "session"` nécessite toujours `thread: true`.
- L'agent cible doit supporter `session/load` (Codex et Claude Code le font).
- Si l'id de session n'est pas trouvé, la création échoue avec une erreur claire — pas de retour silencieux à une nouvelle session.

### Test de fumée de l'opérateur

Utilisez ceci après un déploiement de passerelle quand vous voulez une vérification en direct rapide que la création ACP fonctionne réellement de bout en bout, pas seulement en passant les tests unitaires.

Porte recommandée :

1. Vérifiez la version/commit de la passerelle déployée sur l'hôte cible.
2. Confirmez que la source déployée inclut l'acceptation de la lignée ACP dans
   `src/gateway/sessions-patch.ts` (sessions `subagent:* ou acp:*`).
3. Ouvrez une session de pont ACPX temporaire vers un agent en direct (par exemple
   `razor(main)` sur `jpclawhq`).
4. Demandez à cet agent d'appeler `sessions_spawn` avec :
   - `runtime: "acp"`
   - `agentId: "codex"`
   - `mode: "run"`
   - task: `Reply with exactly LIVE-ACP-SPAWN-OK`
5. Vérifiez que l'agent rapporte :
   - `accepted=yes`
   - une vraie `childSessionKey`
   - pas d'erreur de validateur
6. Nettoyez la session de pont ACPX temporaire.

Exemple d'invite à l'agent en direct :

```text
Use the sessions_spawn tool now with runtime: "acp", agentId: "codex", and mode: "run".
Set the task to: "Reply with exactly LIVE-ACP-SPAWN-OK".
Then report only: accepted=<yes/no>; childSessionKey=<value or none>; error=<exact text or none>.
```

Notes :

- Gardez ce test de fumée sur `mode: "run"` sauf si vous testez intentionnellement
  les sessions ACP persistantes liées à un thread.
- Ne nécessitez pas `streamTo: "parent"` pour la porte de base. Ce chemin dépend des
  capacités du demandeur/session et est une vérification d'intégration séparée.
- Traitez le test `mode: "session"`
