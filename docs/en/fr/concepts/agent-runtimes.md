---
summary: "Comment OpenClaw sépare les fournisseurs de modèles, les modèles, les canaux et les runtimes d'agent"
title: "Runtimes d'agent"
read_when:
  - You are choosing between PI, Codex, ACP, or another native agent runtime
  - You are confused by provider/model/runtime labels in status or config
  - You are documenting support parity for a native harness
---

Un **agent runtime** est le composant qui possède une boucle de modèle préparée : il reçoit l'invite, pilote la sortie du modèle, gère les appels d'outils natifs et retourne le tour terminé à OpenClaw.

Les runtimes sont faciles à confondre avec les fournisseurs car les deux apparaissent près de la configuration du modèle. Ce sont des couches différentes :

| Couche        | Exemples                              | Ce que cela signifie                                                                    |
| ------------- | ------------------------------------- | --------------------------------------------------------------------------------------- |
| Fournisseur   | `openai`, `anthropic`, `openai-codex` | Comment OpenClaw s'authentifie, découvre les modèles et nomme les références de modèle. |
| Modèle        | `gpt-5.5`, `claude-opus-4-6`          | Le modèle sélectionné pour le tour de l'agent.                                         |
| Agent runtime | `pi`, `codex`, runtimes basés sur ACP | La boucle de bas niveau qui exécute le tour préparé.                                   |
| Canal         | Telegram, Discord, Slack, WhatsApp    | Où les messages entrent et sortent d'OpenClaw.                                         |

Vous verrez également le mot **harness** dans le code et la configuration. Un harness est l'implémentation qui fournit un agent runtime. Par exemple, le harness Codex fourni implémente le runtime `codex`. La clé de configuration s'appelle toujours `embeddedHarness` pour la compatibilité, mais la documentation destinée aux utilisateurs et la sortie de statut devraient généralement dire runtime.

La configuration Codex courante utilise le fournisseur `openai` avec le runtime `codex` :

```json5
{
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
      embeddedHarness: {
        runtime: "codex",
      },
    },
  },
}
```

Cela signifie qu'OpenClaw sélectionne une référence de modèle OpenAI, puis demande au runtime app-server Codex d'exécuter le tour d'agent intégré. Cela ne signifie pas que le canal, le catalogue des fournisseurs de modèles ou le magasin de sessions OpenClaw devient Codex.

Pour la division du préfixe de la famille OpenAI, voir [OpenAI](/fr/providers/openai) et [Fournisseurs de modèles](/fr/concepts/model-providers). Pour le contrat de support du runtime Codex, voir [Codex harness](/fr/plugins/codex-harness#v1-support-contract).

## Propriété du runtime

Les différents runtimes possèdent différentes parties de la boucle.

| Surface                     | OpenClaw PI intégré                     | Codex app-server                                                                       |
| --------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------- |
| Propriétaire de la boucle   | OpenClaw via le runner PI intégré       | Codex app-server                                                                       |
| État du thread canonique    | Transcription OpenClaw                  | Thread Codex, plus miroir de transcription OpenClaw                                    |
| Outils dynamiques OpenClaw  | Boucle d'outils OpenClaw native         | Bridgé via l'adaptateur Codex                                                         |
| Outils shell et fichier     | Chemin PI/OpenClaw                      | Outils natifs Codex, bridgés via des hooks natifs où supportés                        |
| Moteur de contexte          | Assemblage de contexte OpenClaw natif   | Contexte assemblé par les projets OpenClaw dans le tour Codex                         |
| Compaction                  | OpenClaw ou moteur de contexte sélectionné | Compaction native Codex, avec notifications OpenClaw et maintenance du miroir         |
| Livraison de canal          | OpenClaw                                | OpenClaw                                                                                |

Cette division de propriété est la règle de conception principale :

- Si OpenClaw possède la surface, OpenClaw peut fournir un comportement normal des hooks de plugin.
- Si le runtime natif possède la surface, OpenClaw a besoin d'événements runtime ou de hooks natifs.
- Si le runtime natif possède l'état du thread canonique, OpenClaw doit mettre en miroir et projeter le contexte, pas réécrire les internals non supportés.

## Sélection du runtime

OpenClaw choisit un runtime intégré après la résolution du fournisseur et du modèle :

1. Le runtime enregistré d'une session gagne. Les changements de configuration ne basculent pas à chaud une transcription existante vers un système de thread natif différent.
2. `OPENCLAW_AGENT_RUNTIME=<id>` force ce runtime pour les sessions nouvelles ou réinitialisées.
3. `agents.defaults.embeddedHarness.runtime` ou `agents.list[].embeddedHarness.runtime` peut définir `auto`, `pi`, ou un id de runtime enregistré tel que `codex`.
4. En mode `auto`, les runtimes de plugin enregistrés peuvent revendiquer les paires fournisseur/modèle supportées.
5. Si aucun runtime ne revendique un tour en mode `auto` et que `fallback: "pi"` est défini (par défaut), OpenClaw utilise PI comme fallback de compatibilité. Définissez `fallback: "none"` pour que la sélection en mode `auto` non appariée échoue à la place.

Les runtimes de plugin explicites échouent fermés par défaut. Par exemple, `runtime: "codex"` signifie Codex ou une erreur de sélection claire sauf si vous définissez `fallback: "pi"` dans la même portée de remplacement. Un remplacement de runtime n'hérite pas d'un paramètre de fallback plus large, donc un `runtime: "codex"` au niveau de l'agent n'est pas silencieusement routé vers PI juste parce que les defaults utilisaient `fallback: "pi"`.

## Contrat de compatibilité

Quand un runtime n'est pas PI, il devrait documenter quelles surfaces OpenClaw il supporte. Utilisez cette forme pour la documentation du runtime :

| Question                                    | Pourquoi c'est important                                                                                      |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Qui possède la boucle de modèle ?           | Détermine où les retries, la continuation d'outils et les décisions de réponse finale se produisent.          |
| Qui possède l'historique du thread canonique ? | Détermine si OpenClaw peut éditer l'historique ou seulement le mettre en miroir.                              |
| Les outils dynamiques OpenClaw fonctionnent-ils ? | La messagerie, les sessions, cron et les outils possédés par OpenClaw en dépendent.                           |
| Les hooks d'outils dynamiques fonctionnent-ils ? | Les plugins s'attendent à `before_tool_call`, `after_tool_call` et middleware autour des outils possédés par OpenClaw. |
| Les hooks d'outils natifs fonctionnent-ils ? | Les outils shell, patch et possédés par le runtime ont besoin du support des hooks natifs pour la politique et l'observation. |
| Le cycle de vie du moteur de contexte s'exécute-t-il ? | Les plugins de mémoire et de contexte dépendent du cycle de vie assemble, ingest, after-turn et compaction. |
| Quelles données de compaction sont exposées ? | Certains plugins n'ont besoin que de notifications, tandis que d'autres ont besoin de métadonnées conservées/supprimées. |
| Qu'est-ce qui est intentionnellement non supporté ? | Les utilisateurs ne devraient pas supposer l'équivalence PI où le runtime natif possède plus d'état.          |

Le contrat de support du runtime Codex est documenté dans [Codex harness](/fr/plugins/codex-harness#v1-support-contract).

## Étiquettes de statut

La sortie de statut peut afficher à la fois les étiquettes `Execution` et `Runtime`. Lisez-les comme des diagnostics, pas comme des noms de fournisseurs.

- Une référence de modèle telle que `openai/gpt-5.5` vous indique le fournisseur/modèle sélectionné.
- Un id de runtime tel que `codex` vous indique quelle boucle exécute le tour.
- Une étiquette de canal telle que Telegram ou Discord vous indique où la conversation se déroule.

Si une session affiche toujours PI après avoir changé la configuration du runtime, démarrez une nouvelle session avec `/new` ou effacez la session actuelle avec `/reset`. Les sessions existantes conservent leur runtime enregistré afin qu'une transcription ne soit pas rejouée via deux systèmes de session natifs incompatibles.

## Connexes

- [Codex harness](/fr/plugins/codex-harness)
- [OpenAI](/fr/providers/openai)
- [Plugins de harness d'agent](/fr/plugins/sdk-agent-harness)
- [Boucle d'agent](/fr/concepts/agent-loop)
- [Modèles](/fr/concepts/models)
- [Statut](/fr/cli/status)
