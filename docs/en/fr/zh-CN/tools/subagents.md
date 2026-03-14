---
read_when:
  - 你想通过智能体执行后台/并行工作
  - 你正在更改 sessions_spawn 或子智能体工具策略
summary: 子智能体：生成隔离的智能体运行，并将结果通告回请求者聊天
title: 子智能体
x-i18n:
  generated_at: "2026-02-03T10:12:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3c83eeed69a65dbbb6b21a386f3ac363d3ef8f077f0e03b834c3f0a9911dca7c
  source_path: tools/subagents.md
  workflow: 15
---

# Sous-agents

Les sous-agents sont des exécutions d'agents en arrière-plan générées à partir d'une exécution d'agent existante. Ils s'exécutent dans leur propre session (`agent:<agentId>:subagent:<uuid>`) et **annoncent** les résultats au canal de chat du demandeur une fois terminés.

## Commandes slash

Utilisez `/subagents` pour vérifier ou contrôler les exécutions de sous-agents de la **session actuelle** :

- `/subagents list`
- `/subagents kill <id|#|all>`
- `/subagents log <id|#> [limit] [tools]`
- `/subagents info <id|#>`
- `/subagents send <id|#> <message>`
- `/subagents steer <id|#> <message>`
- `/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]`

`/subagents info` affiche les métadonnées d'exécution (statut, horodatages, id de session, chemin de transcription, nettoyage).

### Comportement de lancement

`/subagents spawn` lance un sous-agent en arrière-plan comme commande utilisateur, qui envoie un message de fin résumé au canal de chat du demandeur une fois la tâche terminée.

- La commande est non-bloquante et retourne d'abord le `runId`.
- Une fois terminé, le sous-agent publie un message résumé/résultat au canal de chat du demandeur.
- `--model` et `--thinking` peuvent remplacer les paramètres uniquement pour cette exécution.
- Les détails et résultats peuvent être consultés après la fin via `info`/`log`.

Objectifs principaux :

- Paralléliser le travail de « recherche / tâches longues / outils lents » sans bloquer l'exécution principale.
- Maintenir les sous-agents isolés par défaut (séparation de session + isolation sandbox optionnelle).
- Garder l'interface des outils difficile à abuser : les sous-agents n'obtiennent **pas** les outils de session par défaut.
- Éviter l'expansion imbriquée : les sous-agents ne peuvent pas générer de sous-agents.

Remarque sur les coûts : chaque sous-agent a **son propre** contexte et utilisation de tokens. Pour les tâches lourdes ou répétitives, configurez un modèle moins cher pour les sous-agents tout en utilisant un modèle de meilleure qualité pour l'agent principal. Vous pouvez configurer cela via `agents.defaults.subagents.model` ou par remplacement par agent.

## Outils

Utilisation de `sessions_spawn` :

- Lance une exécution de sous-agent (`deliver: false`, file d'attente globale : `subagent`)
- Puis exécute l'étape d'annonce et publie la réponse d'annonce au canal de chat du demandeur
- Modèle par défaut : hérité de l'appelant, sauf si vous avez défini `agents.defaults.subagents.model` (ou `agents.list[].subagents.model` par agent) ; le `sessions_spawn.model` explicite a toujours la priorité.
- Réflexion par défaut : héritée de l'appelant, sauf si vous avez défini `agents.defaults.subagents.thinking` (ou `agents.list[].subagents.thinking` par agent) ; le `sessions_spawn.thinking` explicite a toujours la priorité.

Paramètres de l'outil :

- `task` (obligatoire)
- `label?` (optionnel)
- `agentId?` (optionnel ; si autorisé, générer sous un autre id d'agent)
- `model?` (optionnel ; remplacer le modèle du sous-agent ; les valeurs invalides sont ignorées, le sous-agent s'exécutera avec le modèle par défaut et affichera un avertissement dans le résultat de l'outil)
- `thinking?` (optionnel ; remplacer le niveau de réflexion de l'exécution du sous-agent)
- `runTimeoutSeconds?` (par défaut `0` ; si défini, l'exécution du sous-agent s'arrête après N secondes)
- `cleanup?` (`delete|keep`, par défaut `keep`)

Liste d'autorisation :

- `agents.list[].subagents.allowAgents` : liste des ids d'agents qui peuvent être spécifiés via `agentId` (`["*"]` autorise n'importe lequel). Par défaut : agent demandeur uniquement.

Découverte :

- Utilisez `agents_list` pour voir les ids d'agents actuellement autorisés pour `sessions_spawn`.

Archivage automatique :

- Les sessions de sous-agents sont automatiquement archivées après `agents.defaults.subagents.archiveAfterMinutes` (par défaut : 60).
- L'archivage utilise `sessions.delete` et renomme les transcriptions en `*.deleted.<timestamp>` (même dossier).
- `cleanup: "delete"` archive immédiatement après l'annonce (les transcriptions sont toujours conservées par renommage).
- L'archivage automatique est au mieux un effort ; si la passerelle redémarre, les minuteurs en attente sont perdus.
- `runTimeoutSeconds` n'archive **pas** automatiquement ; il arrête simplement l'exécution. La session est conservée jusqu'à l'archivage automatique.

## Authentification

L'authentification des sous-agents est résolue par **id d'agent**, pas par type de session :

- La clé de session du sous-agent est `agent:<agentId>:subagent:<uuid>`.
- Le magasin d'authentification est chargé à partir du `agentDir` de cet agent.
- Le fichier de configuration d'authentification de l'agent principal est fusionné comme **secours** ; le fichier d'agent remplace le fichier principal en cas de conflit.

Remarque : la fusion est cumulative, donc le fichier de configuration principal est toujours disponible comme secours. L'isolation complète de l'authentification par agent n'est pas encore prise en charge.

## Annonce

Les sous-agents rapportent via l'étape d'annonce :

- L'étape d'annonce s'exécute dans la session du sous-agent (pas la session du demandeur).
- Si le sous-agent répond exactement `ANNOUNCE_SKIP`, rien n'est publié.
- Sinon, la réponse d'annonce est publiée au canal de chat du demandeur via un appel `agent` ultérieur (`deliver=true`).
- La réponse d'annonce conserve le routage des threads/sujets lorsqu'il est disponible (threads Slack, sujets Telegram, threads Matrix).
- Les messages d'annonce sont normalisés en un modèle stable :
  - `Status:` dérivé du résultat d'exécution (`success`, `error`, `timeout` ou `unknown`).
  - `Result:` contenu résumé de l'étape d'annonce (ou `(not available)` s'il manque).
  - `Notes:` détails d'erreur et autre contexte utile.
- `Status` n'est pas déduit de la sortie du modèle ; il provient du signal de résultat d'exécution.

La charge utile d'annonce inclut une ligne de statistiques à la fin (même si elle est enveloppée) :

- Temps d'exécution (par exemple `runtime 5m12s`)
- Utilisation des tokens (entrée/sortie/total)
- Coût estimé lors de la configuration de la tarification du modèle (`models.providers.*.models[].cost`)
- `sessionKey`, `sessionId` et chemin de transcription (pour que l'agent principal puisse récupérer l'historique via `sessions_history` ou vérifier les fichiers sur le disque)

## Politique des outils (outils des sous-agents)

Par défaut, les sous-agents obtiennent **tous les outils sauf les outils de session** :

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`

Remplacer via la configuration :

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 1,
      },
    },
  },
  tools: {
    subagents: {
      tools: {
        // deny a la priorité
        deny: ["gateway", "cron"],
        // si allow est défini, passe en mode liste blanche uniquement (deny a toujours la priorité)
        // allow: ["read", "exec", "process"]
      },
    },
  },
}
```

## Concurrence

Les sous-agents utilisent un canal de file d'attente dédié en processus :

- Nom du canal : `subagent`
- Concurrence : `agents.defaults.subagents.maxConcurrent` (par défaut `8`)

## Arrêt

- L'envoi de `/stop` dans le chat du demandeur arrête la session du demandeur et arrête toute exécution de sous-agent actif générée à partir de celle-ci.

## Limitations

- L'annonce des sous-agents est **au mieux un effort**. Si la passerelle redémarre, le travail d'« annonce de réponse » en attente est perdu.
- Les sous-agents partagent toujours les ressources du même processus de passerelle ; considérez `maxConcurrent` comme une soupape de sécurité.
- `sessions_spawn` est toujours non-bloquant : il retourne immédiatement `{ status: "accepted", runId, childSessionKey }`.
- Le contexte du sous-agent injecte uniquement `AGENTS.md` + `TOOLS.md` (pas `SOUL.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md` ou `BOOTSTRAP.md`).
