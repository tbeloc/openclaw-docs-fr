---
summary: "Utilisez les sessions d'exécution ACP pour Pi, Claude Code, Codex, OpenCode, Gemini CLI et autres agents de harnais"
read_when:
  - Running coding harnesses through ACP
  - Setting up thread-bound ACP sessions on thread-capable channels
  - Binding Discord channels or Telegram forum topics to persistent ACP sessions
  - Troubleshooting ACP backend and plugin wiring
  - Operating /acp commands from chat
title: "Agents ACP"
---

# Agents ACP

Les sessions du [protocole client agent (ACP)](https://agentclientprotocol.com/) permettent à OpenClaw d'exécuter des harnais de codage externes (par exemple Pi, Claude Code, Codex, OpenCode et Gemini CLI) via un plugin backend ACP.

Si vous demandez à OpenClaw en langage naturel « exécuter ceci dans Codex » ou « démarrer Claude Code dans un thread », OpenClaw devrait acheminer cette demande vers le runtime ACP (et non le runtime natif du sous-agent).

## Flux opérateur rapide

Utilisez ceci quand vous voulez un runbook `/acp` pratique :

1. Générer une session :
   - `/acp spawn codex --mode persistent --thread auto`
2. Travailler dans le thread lié (ou cibler explicitement cette clé de session).
3. Vérifier l'état du runtime :
   - `/acp status`
4. Ajuster les options du runtime selon les besoins :
   - `/acp model <provider/model>`
   - `/acp permissions <profile>`
   - `/acp timeout <seconds>`
5. Ajuster une session active sans remplacer le contexte :
   - `/acp steer tighten logging and continue`
6. Arrêter le travail :
   - `/acp cancel` (arrêter le tour actuel), ou
   - `/acp close` (fermer la session + supprimer les liaisons)

## Démarrage rapide pour les humains

Exemples de demandes naturelles :

- « Démarrer une session Codex persistante dans un thread ici et la garder concentrée. »
- « Exécuter ceci comme une session ACP Claude Code unique et résumer le résultat. »
- « Utiliser Gemini CLI pour cette tâche dans un thread, puis garder les suites dans le même thread. »

Ce qu'OpenClaw devrait faire :

1. Choisir `runtime: "acp"`.
2. Résoudre la cible de harnais demandée (`agentId`, par exemple `codex`).
3. Si la liaison de thread est demandée et que le canal actuel la supporte, lier la session ACP au thread.
4. Acheminer les messages de thread de suivi vers la même session ACP jusqu'à ce qu'elle soit défocalisée/fermée/expirée.

## ACP versus sous-agents

Utilisez ACP quand vous voulez un runtime de harnais externe. Utilisez les sous-agents quand vous voulez des exécutions déléguées natives OpenClaw.

| Zone          | Session ACP                           | Exécution de sous-agent                |
| ------------- | ------------------------------------- | -------------------------------------- |
| Runtime       | Plugin backend ACP (par exemple acpx) | Runtime natif de sous-agent OpenClaw   |
| Clé de session| `agent:<agentId>:acp:<uuid>`          | `agent:<agentId>:subagent:<uuid>`      |
| Commandes principales | `/acp ...`                            | `/subagents ...`                       |
| Outil de génération | `sessions_spawn` avec `runtime:"acp"` | `sessions_spawn` (runtime par défaut)  |

Voir aussi [Sous-agents](/tools/subagents).

## Sessions liées aux threads (agnostiques du canal)

Quand les liaisons de thread sont activées pour un adaptateur de canal, les sessions ACP peuvent être liées aux threads :

- OpenClaw lie un thread à une session ACP cible.
- Les messages de suivi dans ce thread s'acheminent vers la session ACP liée.
- La sortie ACP est renvoyée au même thread.
- Défocaliser/fermer/archiver/expiration du délai d'inactivité ou de l'âge maximum supprime la liaison.

Le support de liaison de thread est spécifique à l'adaptateur. Si l'adaptateur de canal actif ne supporte pas les liaisons de thread, OpenClaw retourne un message clair non supporté/indisponible.

Drapeaux de fonctionnalité requis pour ACP lié aux threads :

- `acp.enabled=true`
- `acp.dispatch.enabled` est activé par défaut (définir `false` pour mettre en pause la distribution ACP)
- Drapeau de génération de thread ACP de l'adaptateur de canal activé (spécifique à l'adaptateur)
  - Discord : `channels.discord.threadBindings.spawnAcpSessions=true`
  - Telegram : `channels.telegram.threadBindings.spawnAcpSessions=true`

### Canaux supportant les threads

- Tout adaptateur de canal qui expose la capacité de liaison de session/thread.
- Support intégré actuel :
  - Threads/canaux Discord
  - Sujets Telegram (sujets de forum dans les groupes/supergroupes et sujets DM)
- Les canaux de plugin peuvent ajouter le support via la même interface de liaison.

## Paramètres spécifiques au canal

Pour les flux non éphémères, configurez les liaisons ACP persistantes dans les entrées `bindings[]` de niveau supérieur.

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
- `agents.list[].runtime.acp.agent` (id du harnais, par exemple `codex` ou `claude`)
- `agents.list[].runtime.acp.backend`
- `agents.list[].runtime.acp.mode`
- `agents.list[].runtime.acp.cwd`

Ordre de précédence de remplacement pour les sessions liées ACP :

1. `bindings[].acp.*`
2. `agents.list[].runtime.acp.*`
3. valeurs par défaut ACP globales (par exemple `acp.backend`)

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
- Les messages dans ce canal ou sujet s'acheminent vers la session ACP configurée.
- Dans les conversations liées, `/new` et `/reset` réinitialisent la même clé de session ACP en place.
- Les liaisons de runtime temporaires (par exemple créées par des flux de focus de thread) s'appliquent toujours où présentes.

## Démarrer les sessions ACP (interfaces)

### À partir de `sessions_spawn`

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
- Si `agentId` est omis, OpenClaw utilise `acp.defaultAgent` quand configuré.
- `mode: "session"` nécessite `thread: true` pour maintenir une conversation liée persistante.

Détails de l'interface :

- `task` (requis) : invite initiale envoyée à la session ACP.
- `runtime` (requis pour ACP) : doit être `"acp"`.
- `agentId` (optionnel) : id du harnais cible ACP. Revient à `acp.defaultAgent` s'il est défini.
- `thread` (optionnel, par défaut `false`) : demander le flux de liaison de thread où supporté.
- `mode` (optionnel) : `run` (unique) ou `session` (persistant).
  - par défaut `run`
  - si `thread: true` et mode omis, OpenClaw peut par défaut utiliser le comportement persistant par chemin de runtime
  - `mode: "session"` nécessite `thread: true`
- `cwd` (optionnel) : répertoire de travail du runtime demandé (validé par la politique backend/runtime).
- `label` (optionnel) : étiquette orientée opérateur utilisée dans le texte de session/bannière.
- `resumeSessionId` (optionnel) : reprendre une session ACP existante au lieu d'en créer une nouvelle. L'agent rejoue son historique de conversation via `session/load`. Nécessite `runtime: "acp"`.
- `streamTo` (optionnel) : `"parent"` diffuse les résumés de progression initiale de l'exécution ACP vers la session du demandeur en tant qu'événements système.
  - Quand disponible, les réponses acceptées incluent `streamLogPath` pointant vers un journal JSONL scoped de session (`<sessionId>.acp-stream.jsonl`) que vous pouvez suivre pour l'historique complet du relais.

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

- Transférer une session Codex de votre ordinateur portable à votre téléphone — dites à votre agent de reprendre où vous l'aviez laissé
- Continuer une session de codage que vous avez démarrée de manière interactive dans la CLI, maintenant sans tête via votre agent
- Reprendre le travail qui a été interrompu par un redémarrage de passerelle ou un délai d'inactivité

Notes :

- `resumeSessionId` nécessite `runtime: "acp"` — retourne une erreur s'il est utilisé avec le runtime du sous-agent.
- `resumeSessionId` restaure l'historique de conversation ACP en amont ; `thread` et `mode` s'appliquent toujours normalement à la nouvelle session OpenClaw que vous créez, donc `mode: "session"` nécessite toujours `thread: true`.
- L'agent cible doit supporter `session/load` (Codex et Claude Code le font).
- Si l'id de session n'est pas trouvé, la génération échoue avec une erreur claire — pas de repli silencieux vers une nouvelle session.

### Test de fumée de l'opérateur

Utilisez ceci après un déploiement de passerelle quand vous voulez une vérification en direct rapide que la génération ACP fonctionne réellement de bout en bout, pas seulement en passant les tests unitaires.

Porte recommandée :

1. Vérifier la version/commit de la passerelle déployée sur l'hôte cible.
2. Confirmer que la source déployée inclut l'acceptation de la lignée ACP dans
   `src/gateway/sessions-patch.ts` (sessions `subagent:* ou acp:*`).
3. Ouvrir une session de pont ACPX temporaire vers un agent en direct (par exemple
   `razor(main)` sur `jpclawhq`).
4. Demander à cet agent d'appeler `sessions_spawn` avec :
   - `runtime: "acp"`
   - `agentId: "codex"`
   - `mode: "run"`
   - task: `Reply with exactly LIVE-ACP-SPAWN-OK`
5. Vérifier que l'agent rapporte :
   - `accepted=yes`
   - une vraie `childSessionKey`
   - pas d'erreur de validateur
6. Nettoyer la session de pont ACPX temporaire.

Exemple d'invite à l'agent en direct :

```text
Use the sessions_spawn tool now with runtime: "acp", agentId: "codex", and mode: "run".
Set the task to: "Reply with exactly LIVE-ACP-SPAWN-OK".
Then report only: accepted=<yes/no>; childSessionKey=<value or none>; error=<exact text or none>.
```

Notes :

- Gardez ce test de fumée sur `mode: "run"` sauf si vous testez intentionnellement
  les sessions ACP persistantes liées aux threads.
- Ne nécessitez pas `streamTo: "parent"` pour la porte de base. Ce chemin dépend des
  capacités du demandeur/session et est une vérification d'intégration séparée.
- Traitez le test `mode: "session"` lié aux threads comme une deuxième passe d'intégration
  plus riche à partir d'un vrai thread Discord ou sujet Telegram.

## Compatibilité sandbox

Les sessions ACP s'exécutent actuellement sur le runtime hôte, et non à l'intérieur du sandbox OpenClaw.

Limitations actuelles :

- Si la session du demandeur est sandboxée, les spawns ACP sont bloqués pour `sessions_spawn({ runtime: "acp" })` et `/acp spawn`.
  - Erreur : `Sandboxed sessions cannot spawn ACP sessions because runtime="acp" runs on the host. Use runtime="subagent" from sandboxed sessions.`
- `sessions_spawn` avec `runtime: "acp"` ne supporte pas `sandbox: "require"`.
  - Erreur : `sessions_spawn sandbox="require" is unsupported for runtime="acp" because ACP sessions run outside the sandbox. Use runtime="subagent" or sandbox="inherit".`

Utilisez `runtime: "subagent"` quand vous avez besoin d'une exécution appliquée par le sandbox.

### Depuis la commande `/acp`

Utilisez `/acp spawn` pour un contrôle explicite de l'opérateur depuis le chat si nécessaire.

```text
/acp spawn codex --mode persistent --thread auto
/acp spawn codex --mode oneshot --thread off
/acp spawn codex --thread here
```

Drapeaux clés :

- `--mode persistent|oneshot`
- `--thread auto|here|off`
- `--cwd <absolute-path>`
- `--label <name>`

Voir [Slash Commands](/tools/slash-commands).

## Résolution de la cible de session

La plupart des actions `/acp` acceptent une cible de session optionnelle (`session-key`, `session-id`, ou `session-label`).

Ordre de résolution :

1. Argument cible explicite (ou `--session` pour `/acp steer`)
   - essaie la clé
   - puis l'ID de session en forme UUID
   - puis le label
2. Liaison de thread actuelle (si cette conversation/thread est liée à une session ACP)
3. Fallback de session du demandeur actuel

Si aucune cible ne se résout, OpenClaw retourne une erreur claire (`Unable to resolve session target: ...`).

## Modes de thread de spawn

`/acp spawn` supporte `--thread auto|here|off`.

| Mode   | Comportement                                                                                                    |
| ------ | --------------------------------------------------------------------------------------------------------------- |
| `auto` | Dans un thread actif : lie ce thread. En dehors d'un thread : crée/lie un thread enfant si supporté.           |
| `here` | Requiert le thread actif actuel ; échoue si pas dans un.                                                       |
| `off`  | Pas de liaison. La session démarre non liée.                                                                   |

Notes :

- Sur les surfaces sans liaison de thread, le comportement par défaut est effectivement `off`.
- Le spawn lié au thread requiert le support de la politique de canal :
  - Discord : `channels.discord.threadBindings.spawnAcpSessions=true`
  - Telegram : `channels.telegram.threadBindings.spawnAcpSessions=true`

## Contrôles ACP

Famille de commandes disponible :

- `/acp spawn`
- `/acp cancel`
- `/acp steer`
- `/acp close`
- `/acp status`
- `/acp set-mode`
- `/acp set`
- `/acp cwd`
- `/acp permissions`
- `/acp timeout`
- `/acp model`
- `/acp reset-options`
- `/acp sessions`
- `/acp doctor`
- `/acp install`

`/acp status` affiche les options de runtime effectives et, quand disponibles, les identifiants de session au niveau du runtime et du backend.

Certains contrôles dépendent des capacités du backend. Si un backend ne supporte pas un contrôle, OpenClaw retourne une erreur de contrôle non supporté claire.

## Livre de recettes des commandes ACP

| Commande             | Ce qu'elle fait                                           | Exemple                                                        |
| -------------------- | --------------------------------------------------------- | -------------------------------------------------------------- |
| `/acp spawn`         | Créer une session ACP ; liaison de thread optionnelle.    | `/acp spawn codex --mode persistent --thread auto --cwd /repo` |
| `/acp cancel`        | Annuler le tour en vol pour la session cible.             | `/acp cancel agent:codex:acp:<uuid>`                           |
| `/acp steer`         | Envoyer une instruction de direction à la session active. | `/acp steer --session support inbox prioritize failing tests`  |
| `/acp close`         | Fermer la session et délier les cibles de thread.         | `/acp close`                                                   |
| `/acp status`        | Afficher le backend, mode, état, options de runtime.      | `/acp status`                                                  |
| `/acp set-mode`      | Définir le mode de runtime pour la session cible.         | `/acp set-mode plan`                                           |
| `/acp set`           | Écriture générique d'option de configuration de runtime.  | `/acp set model openai/gpt-5.2`                                |
| `/acp cwd`           | Définir le répertoire de travail de runtime.              | `/acp cwd /Users/user/Projects/repo`                           |
| `/acp permissions`   | Définir le profil de politique d'approbation.             | `/acp permissions strict`                                      |
| `/acp timeout`       | Définir le timeout de runtime (secondes).                 | `/acp timeout 120`                                             |
| `/acp model`         | Définir le modèle de runtime.                             | `/acp model anthropic/claude-opus-4-5`                         |
| `/acp reset-options` | Supprimer les surcharges d'option de runtime de session.  | `/acp reset-options`                                           |
| `/acp sessions`      | Lister les sessions ACP récentes du store.                | `/acp sessions`                                                |
| `/acp doctor`        | Santé du backend, capacités, corrections actionnables.    | `/acp doctor`                                                  |
| `/acp install`       | Imprimer les étapes d'installation et d'activation.       | `/acp install`                                                 |

`/acp sessions` lit le store pour la session liée actuelle ou la session du demandeur. Les commandes qui acceptent les tokens `session-key`, `session-id`, ou `session-label` résolvent les cibles via la découverte de session de passerelle, y compris les racines `session.store` personnalisées par agent.

## Mappage des options de runtime

`/acp` a des commandes de commodité et un setter générique.

Opérations équivalentes :

- `/acp model <id>` mappe à la clé de configuration de runtime `model`.
- `/acp permissions <profile>` mappe à la clé de configuration de runtime `approval_policy`.
- `/acp timeout <seconds>` mappe à la clé de configuration de runtime `timeout`.
- `/acp cwd <path>` met à jour directement la surcharge de cwd de runtime.
- `/acp set <key> <value>` est le chemin générique.
  - Cas spécial : `key=cwd` utilise le chemin de surcharge de cwd.
- `/acp reset-options` efface toutes les surcharges de runtime pour la session cible.

## Support du harnais acpx (actuel)

Alias de harnais intégrés acpx actuels :

- `pi`
- `claude`
- `codex`
- `opencode`
- `gemini`
- `kimi`

Quand OpenClaw utilise le backend acpx, préférez ces valeurs pour `agentId` sauf si votre configuration acpx définit des alias d'agent personnalisés.

L'utilisation directe de la CLI acpx peut aussi cibler des adaptateurs arbitraires via `--agent <command>`, mais cette échappatoire brute est une fonctionnalité de la CLI acpx (pas le chemin normal `agentId` d'OpenClaw).

## Configuration requise

Baseline ACP core :

```json5
{
  acp: {
    enabled: true,
    // Optionnel. Par défaut true ; définir false pour mettre en pause la dispatch ACP tout en gardant les contrôles /acp.
    dispatch: { enabled: true },
    backend: "acpx",
    defaultAgent: "codex",
    allowedAgents: ["pi", "claude", "codex", "opencode", "gemini", "kimi"],
    maxConcurrentSessions: 8,
    stream: {
      coalesceIdleMs: 300,
      maxChunkChars: 1200,
    },
    runtime: {
      ttlMinutes: 120,
    },
  },
}
```

La configuration de liaison de thread est spécifique à l'adaptateur de canal. Exemple pour Discord :

```json5
{
  session: {
    threadBindings: {
      enabled: true,
      idleHours: 24,
      maxAgeHours: 0,
    },
  },
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        spawnAcpSessions: true,
      },
    },
  },
}
```

Si le spawn ACP lié au thread ne fonctionne pas, vérifiez d'abord le drapeau de fonctionnalité de l'adaptateur :

- Discord : `channels.discord.threadBindings.spawnAcpSessions=true`

Voir [Configuration Reference](/gateway/configuration-reference).

## Configuration du plugin pour le backend acpx

Installer et activer le plugin :

```bash
openclaw plugins install acpx
openclaw config set plugins.entries.acpx.enabled true
```

Installation d'espace de travail local pendant le développement :

```bash
openclaw plugins install ./extensions/acpx
```

Puis vérifiez la santé du backend :

```text
/acp doctor
```

### Configuration de la commande et de la version acpx

Par défaut, le plugin acpx (publié comme `@openclaw/acpx`) utilise le binaire épinglé local du plugin :

1. La commande par défaut est `extensions/acpx/node_modules/.bin/acpx`.
2. La version attendue par défaut est l'épingle de l'extension.
3. Le démarrage enregistre le backend ACP immédiatement comme non prêt.
4. Un travail d'assurance en arrière-plan vérifie `acpx --version`.
5. Si le binaire local du plugin est manquant ou ne correspond pas, il exécute :
   `npm install --omit=dev --no-save acpx@<pinned>` et re-vérifie.

Vous pouvez surcharger la commande/version dans la configuration du plugin :

```json
{
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "command": "../acpx/dist/cli.js",
          "expectedVersion": "any"
        }
      }
    }
  }
}
```

Notes :

- `command` accepte un chemin absolu, un chemin relatif, ou un nom de commande (`acpx`).
- Les chemins relatifs se résolvent depuis le répertoire de l'espace de travail OpenClaw.
- `expectedVersion: "any"` désactive la correspondance stricte de version.
- Quand `command` pointe vers un binaire/chemin personnalisé, l'auto-installation locale du plugin est désactivée.
- Le démarrage d'OpenClaw reste non-bloquant pendant que la vérification de santé du backend s'exécute.

Voir [Plugins](/tools/plugin).

## Configuration des permissions

Les sessions ACP s'exécutent de manière non-interactive — il n'y a pas de TTY pour approuver ou refuser les invites de permission d'écriture de fichier et d'exécution de shell. Le plugin acpx fournit deux clés de configuration qui contrôlent comment les permissions sont gérées :

### `permissionMode`

Contrôle quelles opérations l'agent du harnais peut effectuer sans demander.

| Valeur          | Comportement                                                  |
| --------------- | ------------------------------------------------------------- |
| `approve-all`   | Auto-approuver toutes les écritures de fichier et commandes.  |
| `approve-reads` | Auto-approuver les lectures uniquement ; écritures et exec requièrent des invites. |
| `deny-all`      | Refuser toutes les invites de permission.                     |

### `nonInteractivePermissions`

Contrôle ce qui se passe quand une invite de permission serait affichée mais qu'aucun TTY interactif n'est disponible (ce qui est toujours le cas pour les sessions ACP).

| Valeur | Comportement                                                          |
| ------ | --------------------------------------------------------------------- |
| `fail` | Abandonner la session avec `AcpRuntimeError`. **(par défaut)**        |
| `deny` | Refuser silencieusement la permission et continuer (dégradation gracieuse). |

### Configuration

Définir via la configuration du plugin :

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw config set plugins.entries.acpx.config.nonInteractivePermissions fail
```

Redémarrez la passerelle après avoir modifié ces valeurs.

> **Important :** OpenClaw utilise actuellement par défaut `permissionMode=approve-reads` et `nonInteractivePermissions=fail`. Dans les sessions ACP non-interactives, toute écriture ou exec qui déclenche une invite de permission peut échouer avec `AcpRuntimeError: Permission prompt unavailable in non-interactive mode`.
>
> Si vous avez besoin de restreindre les permissions, définissez `nonInteractivePermissions` à `deny` pour que les sessions se dégradent gracieusement au lieu de planter.

## Dépannage

| Symptôme                                                                 | Cause probable                                                                  | Solution                                                                                                                                                         |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ACP runtime backend is not configured`                                  | Plugin backend manquant ou désactivé.                                           | Installez et activez le plugin backend, puis exécutez `/acp doctor`.                                                                                             |
| `ACP is disabled by policy (acp.enabled=false)`                          | ACP désactivé globalement.                                                      | Définissez `acp.enabled=true`.                                                                                                                                   |
| `ACP dispatch is disabled by policy (acp.dispatch.enabled=false)`        | Dispatch depuis les messages de thread normal désactivé.                        | Définissez `acp.dispatch.enabled=true`.                                                                                                                         |
| `ACP agent "<id>" is not allowed by policy`                              | Agent non dans la liste d'autorisation.                                         | Utilisez un `agentId` autorisé ou mettez à jour `acp.allowedAgents`.                                                                                            |
| `Unable to resolve session target: ...`                                  | Jeton clé/id/label invalide.                                                    | Exécutez `/acp sessions`, copiez la clé/étiquette exacte, réessayez.                                                                                            |
| `--thread here requires running /acp spawn inside an active ... thread`  | `--thread here` utilisé en dehors d'un contexte de thread.                      | Déplacez-vous vers le thread cible ou utilisez `--thread auto`/`off`.                                                                                           |
| `Only <user-id> can rebind this thread.`                                 | Un autre utilisateur possède la liaison de thread.                              | Reliez en tant que propriétaire ou utilisez un thread différent.                                                                                                 |
| `Thread bindings are unavailable for <channel>.`                         | L'adaptateur manque de capacité de liaison de thread.                           | Utilisez `--thread off` ou déplacez-vous vers un adaptateur/canal supporté.                                                                                     |
| `Sandboxed sessions cannot spawn ACP sessions ...`                       | Le runtime ACP est côté hôte ; la session du demandeur est en sandbox.          | Utilisez `runtime="subagent"` depuis les sessions en sandbox, ou exécutez ACP spawn depuis une session non-sandbox.                                             |
| `sessions_spawn sandbox="require" is unsupported for runtime="acp" ...`  | `sandbox="require"` demandé pour le runtime ACP.                                | Utilisez `runtime="subagent"` pour le sandboxing requis, ou utilisez ACP avec `sandbox="inherit"` depuis une session non-sandbox.                               |
| Missing ACP metadata for bound session                                   | Métadonnées de session ACP obsolètes/supprimées.                                | Recréez avec `/acp spawn`, puis reliez/focalisez le thread.                                                                                                     |
| `AcpRuntimeError: Permission prompt unavailable in non-interactive mode` | `permissionMode` bloque les écritures/exécutions en session ACP non-interactive. | Définissez `plugins.entries.acpx.config.permissionMode` sur `approve-all` et redémarrez la passerelle. Voir [Configuration des permissions](#permission-configuration). |
| ACP session fails early with little output                               | Les invites de permission sont bloquées par `permissionMode`/`nonInteractivePermissions`. | Vérifiez les journaux de la passerelle pour `AcpRuntimeError`. Pour les permissions complètes, définissez `permissionMode=approve-all` ; pour une dégradation gracieuse, définissez `nonInteractivePermissions=deny`. |
| ACP session stalls indefinitely after completing work                    | Le processus Harness s'est terminé mais la session ACP n'a pas signalé l'achèvement. | Surveillez avec `ps aux \| grep acpx` ; tuez manuellement les processus obsolètes.                                                                              |
