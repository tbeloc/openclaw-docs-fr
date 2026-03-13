---
read_when:
  - 添加或修改会话工具时
summary: 用于列出会话、获取历史记录和发送跨会话消息的智能体会话工具
title: 会话工具
x-i18n:
  generated_at: "2026-02-03T07:46:54Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: cb6e0982ebf507bcf9de4bb17719759c2b6d3e519731c845580a55279084e4c8
  source_path: concepts/session-tool.md
  workflow: 15
---

# Outils de session

Objectif : ensemble d'outils petit et difficile à mal utiliser permettant aux agents de lister les sessions, d'obtenir l'historique et d'envoyer des messages entre sessions.

## Noms des outils

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`

## Modèle de clés

- Le bucket de chat direct principal est toujours la clé littérale `"main"` (résout à la clé principale de l'agent actuel).
- Les chats de groupe utilisent `agent:<agentId>:<channel>:group:<id>` ou `agent:<agentId>:<channel>:channel:<id>` (passer la clé complète).
- Les tâches planifiées utilisent `cron:<job.id>`.
- Les hooks utilisent `hook:<uuid>`, sauf s'ils sont explicitement définis.
- Les sessions Node utilisent `node-<nodeId>`, sauf s'ils sont explicitement définis.

`global` et `unknown` sont des valeurs réservées et ne seront jamais listées. Si `session.scope = "global"`, nous l'aliasons en `main` pour tous les outils, de sorte que l'appelant ne verra jamais `global`.

## sessions_list

Liste les sessions sous forme de tableau de lignes.

Paramètres :

- `kinds?: string[]` Filtre : n'importe lequel de `"main" | "group" | "cron" | "hook" | "node" | "other"`
- `limit?: number` Nombre maximum de lignes (par défaut : valeur par défaut du serveur, limite comme 200)
- `activeMinutes?: number` Uniquement les sessions mises à jour dans les N dernières minutes
- `messageLimit?: number` 0 = pas de messages (par défaut 0) ; >0 = inclure les N derniers messages

Comportement :

- `messageLimit > 0` récupère `chat.history` pour chaque session et inclut les N derniers messages.
- Les résultats des outils sont filtrés dans la sortie de la liste ; utilisez `sessions_history` pour obtenir les messages des outils.
- Lors de l'exécution dans une session d'agent **isolée en sandbox**, les outils de session sont par défaut **visibilité générée uniquement** (voir ci-dessous).

Structure de ligne (JSON) :

- `key` : clé de session (chaîne)
- `kind` : `main | group | cron | hook | node | other`
- `channel` : `whatsapp | telegram | discord | signal | imessage | webchat | internal | unknown`
- `displayName` (étiquette d'affichage de groupe si disponible)
- `updatedAt` (millisecondes)
- `sessionId`
- `model`, `contextTokens`, `totalTokens`
- `thinkingLevel`, `verboseLevel`, `systemSent`, `abortedLastRun`
- `sendPolicy` (si remplacement de session défini)
- `lastChannel`, `lastTo`
- `deliveryContext` (`{ channel, to, accountId }` normalisé si disponible)
- `transcriptPath` (chemin au mieux du répertoire de stockage + sessionId)
- `messages?` (uniquement si `messageLimit > 0`)

## sessions_history

Récupère l'historique d'une session.

Paramètres :

- `sessionKey` (obligatoire ; accepte la clé de session ou `sessionId` de `sessions_list`)
- `limit?: number` Nombre maximum de messages (limite du serveur)
- `includeTools?: boolean` (par défaut false)

Comportement :

- `includeTools=false` filtre les messages `role: "toolResult"`.
- Retourne un tableau de messages au format d'historique brut.
- Lorsqu'un `sessionId` est donné, OpenClaw le résout à la clé de session correspondante (les id manquants génèrent une erreur).

## sessions_send

Envoie un message à une autre session.

Paramètres :

- `sessionKey` (obligatoire ; accepte la clé de session ou `sessionId` de `sessions_list`)
- `message` (obligatoire)
- `timeoutSeconds?: number` (par défaut >0 ; 0 = envoyer et oublier)

Comportement :

- `timeoutSeconds = 0` : met en file d'attente et retourne `{ runId, status: "accepted" }`.
- `timeoutSeconds > 0` : attend jusqu'à N secondes pour la fin, puis retourne `{ runId, status: "ok", reply }`.
- Si l'attente expire : `{ runId, status: "timeout", error }`. L'exécution continue ; appelez `sessions_history` plus tard.
- Si l'exécution échoue : `{ runId, status: "error", error }`.
- Les notifications de livraison s'exécutent après la fin de l'exécution principale et sont au mieux ; `status: "ok"` ne garantit pas que la notification a été livrée.
- Attend via Gateway `agent.wait` (côté serveur), donc la reconnexion ne perd pas l'attente.
- Le contexte des messages agent-à-agent est injecté pour l'exécution principale.
- Après la fin de l'exécution principale, OpenClaw exécute une **boucle de réponse** :
  - Les tours 2 et suivants alternent entre le demandeur et l'agent cible.
  - Répondez exactement `REPLY_SKIP` pour arrêter les allers-retours.
  - Le nombre maximum de tours est `session.agentToAgent.maxPingPongTurns` (0–5, par défaut 5).
- Après la fin de la boucle, OpenClaw exécute une **étape de notification agent-à-agent** (agent cible uniquement) :
  - Répondez exactement `ANNOUNCE_SKIP` pour rester silencieux.
  - Toute autre réponse est envoyée au canal cible.
  - L'étape de notification inclut la demande d'origine + la réponse du tour 1 + la réponse aller-retour la plus récente.

## Champ Channel

- Pour les groupes, `channel` est le canal enregistré sur l'entrée de session.
- Pour les chats directs, `channel` est mappé à partir de `lastChannel`.
- Pour cron/hook/node, `channel` est `internal`.
- S'il manque, `channel` est `unknown`.

## Sécurité / Politique d'envoi

Blocage basé sur la politique par canal/type de chat (pas par id de session).

```json
{
  "session": {
    "sendPolicy": {
      "rules": [
        {
          "match": { "channel": "discord", "chatType": "group" },
          "action": "deny"
        }
      ],
      "default": "allow"
    }
  }
}
```

Remplacement au moment de l'exécution (par entrée de session) :

- `sendPolicy: "allow" | "deny"` (non défini = hériter de la configuration)
- Peut être défini via `sessions.patch` ou `/send on|off|inherit` (message seul propriétaire).

Points d'exécution :

- `chat.send` / `agent` (Gateway)
- Logique de livraison de réponse automatique

## sessions_spawn

Génère une exécution d'agent enfant dans une session isolée et notifie les résultats au canal de chat du demandeur.

Paramètres :

- `task` (obligatoire)
- `label?` (optionnel ; pour les journaux/UI)
- `agentId?` (optionnel ; générer sous un autre id d'agent si autorisé)
- `model?` (optionnel ; remplacer le modèle de l'agent enfant ; les valeurs invalides génèrent une erreur)
- `runTimeoutSeconds?` (par défaut 0 ; lorsqu'il est défini, abandonne l'exécution de l'agent enfant après N secondes)
- `cleanup?` (`delete|keep`, par défaut `keep`)

Liste d'autorisation :

- `agents.list[].subagents.allowAgents` : liste des id d'agent autorisés via `agentId` (`["*"]` autorise n'importe lequel). Par défaut : agent demandeur uniquement.

Découverte :

- Utilisez `agents_list` pour découvrir quels id d'agent sont autorisés pour `sessions_spawn`.

Comportement :

- Lance une nouvelle session `agent:<agentId>:subagent:<uuid>` avec `deliver: false`.
- L'agent enfant utilise par défaut l'ensemble complet des outils **moins les outils de session** (configurable via `tools.subagents.tools`).
- L'agent enfant n'est pas autorisé à appeler `sessions_spawn` (pas de génération enfant → enfant).
- Toujours non-bloquant : retourne immédiatement `{ status: "accepted", runId, childSessionKey }`.
- Après la fin, OpenClaw exécute l'**étape de notification** de l'agent enfant et publie les résultats au canal de chat du demandeur.
- Répondez exactement `ANNOUNCE_SKIP` dans l'étape de notification pour rester silencieux.
- Les réponses de notification sont normalisées en `Status`/`Result`/`Notes` ; `Status` provient du résultat d'exécution (pas du texte du modèle).
- Les sessions d'agent enfant sont automatiquement archivées après `agents.defaults.subagents.archiveAfterMinutes` (par défaut : 60).
- La réponse de notification contient une ligne de statistiques (temps d'exécution, nombre de tokens, sessionKey/sessionId, chemin de transcription et coût optionnel).

## Visibilité des sessions en sandbox

Les sessions isolées en sandbox peuvent utiliser les outils de session, mais par défaut elles ne peuvent voir que les sessions générées via `sessions_spawn`.

Configuration :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        // Par défaut : "spawned"
        sessionToolsVisibility: "spawned", // ou "all"
      },
    },
  },
}
```
