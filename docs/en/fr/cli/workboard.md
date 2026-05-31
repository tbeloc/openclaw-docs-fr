---
summary: "Référence CLI pour les cartes `openclaw workboard`, la dispatch et les exécutions de workers"
read_when:
  - You want to inspect or create Workboard cards from the terminal
  - You want to dispatch Workboard worker runs from the CLI
  - You are debugging Workboard CLI or slash command behavior
title: "Workboard CLI"
---

`openclaw workboard` est la surface terminale du plugin
[Workboard](/fr/plugins/workboard) fourni. Elle permet à un opérateur de lister les cartes, créer une
carte, inspecter une carte et demander à la Gateway en cours d'exécution de dispatcher le travail prêt dans
les exécutions de workers subagent.

Activez le plugin avant d'utiliser la commande :

```bash
openclaw plugins enable workboard
openclaw gateway restart
```

## Utilisation

```bash
openclaw workboard list [--board <id>] [--status <status>] [--json]
openclaw workboard create <title...> [--notes <text>] [--status <status>] [--priority <priority>] [--agent <id>] [--board <id>] [--labels <items>] [--json]
openclaw workboard show <id> [--json]
openclaw workboard dispatch [--url <url>] [--token <token>] [--timeout <ms>] [--json]
```

La commande lit et écrit dans la même base de données SQLite appartenant au plugin utilisée par
le tableau de bord et les outils d'agent Workboard. Les identifiants de cartes peuvent être passés par identifiant complet ou par un
préfixe non ambigu quand une commande accepte un identifiant de carte.

## `list`

```bash
openclaw workboard list
openclaw workboard list --board default --status ready
openclaw workboard list --json
```

La sortie texte est compacte :

```text
7f4a2c10  ready     high    default agent-a  Fix stale worker heartbeat
```

Les colonnes sont le préfixe d'id, le statut, la priorité, l'id du tableau, l'id d'agent optionnel et le titre.

Drapeaux :

| Drapeau             | Objectif                                 |
| ------------------- | ---------------------------------------- |
| `--board <id>`      | Limiter les résultats à un espace de noms de tableau |
| `--status <status>` | Limiter les résultats à un statut Workboard |
| `--json`            | Imprimer la liste complète des cartes en JSON machine |

## `create`

```bash
openclaw workboard create "Fix stale worker heartbeat" --priority high --labels bug,workboard
openclaw workboard create "Write Workboard docs" --status ready --agent docs-agent --board docs --notes "Cover CLI, slash command, dispatch, and SQLite state."
```

Drapeaux :

| Drapeau                 | Objectif                                |
| ----------------------- | --------------------------------------- |
| `--notes <text>`        | Notes initiales de la carte             |
| `--status <status>`     | Statut initial, par défaut `todo`       |
| `--priority <priority>` | Priorité, par défaut `normal`           |
| `--agent <id>`          | Assigner la carte à un agent ou id propriétaire |
| `--board <id>`          | Stocker la carte sur un espace de noms de tableau |
| `--labels <items>`      | Étiquettes séparées par des virgules     |
| `--json`                | Imprimer la carte créée en JSON machine |

`create` écrit directement dans l'état SQLite de Workboard. La carte est immédiatement
visible dans l'onglet Workboard de l'interface utilisateur Control et pour les outils Workboard.

## `show`

```bash
openclaw workboard show 7f4a2c10
openclaw workboard show 7f4a2c10 --json
```

La sortie texte imprime la ligne de carte compacte et les notes. La sortie JSON retourne l'enregistrement de carte complet, y compris les métadonnées d'exécution, les tentatives, les commentaires, les liens, la preuve,
les artefacts, les journaux de workers, l'état du protocole, les diagnostics et les métadonnées d'automatisation.

## `dispatch`

```bash
openclaw workboard dispatch
openclaw workboard dispatch --json
openclaw workboard dispatch --url http://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

`dispatch` appelle d'abord la méthode RPC de la Gateway en cours d'exécution
`workboard.cards.dispatch`. Ce chemin utilise le même runtime subagent que
l'action de dispatch du tableau de bord, donc les cartes prêtes peuvent devenir des sessions de workers réelles.

La boucle de dispatch :

1. Promeut les enfants prêts pour les dépendances à `ready`.
2. Bloque les réclamations expirées ou les exécutions de workers expirées.
3. Enregistre les métadonnées de dispatch sur les cartes prêtes.
4. Sélectionne un petit lot de cartes prêtes non réclamées.
5. Réclame chaque carte sélectionnée pour le dispatcher ou l'agent assigné.
6. Démarre une exécution de worker subagent avec un contexte de carte limité et le jeton de réclamation de carte.
7. Stocke l'id d'exécution de worker, la clé de session, le statut d'exécution et le journal de worker sur
   la carte.

La sélection est intentionnellement conservatrice. Un dispatch démarre au maximum trois
workers par défaut, ignore les cartes archivées ou déjà réclamées, et démarre seulement une
carte par propriétaire ou agent en un seul passage. Les cartes déjà possédées par un travail actif en cours d'exécution
ou en révision sont laissées pour un dispatch ultérieur.

Si le démarrage du worker échoue après qu'une carte soit réclamée, Workboard bloque cette carte,
efface la réclamation et enregistre l'échec dans l'exécution de la carte et les métadonnées du journal de worker. Cela garde les démarrages échoués visibles au lieu de retourner silencieusement la
carte à la file d'attente.

Si aucune cible Gateway explicite n'est fournie et que la Gateway locale est indisponible
ou n'expose pas encore la méthode de dispatch Workboard, la CLI revient à
la dispatch basée sur les données par rapport à l'état Workboard local. La dispatch basée sur les données peut toujours
promouvoir les dépendances, nettoyer les réclamations obsolètes et bloquer les exécutions expirées, mais elle
ne démarre pas les workers. Les échecs d'authentification, de permission, de validation et les échecs pour une
cible `--url` ou `--token` explicite sont signalés directement.

La sortie texte rapporte les démarrages de workers :

```text
dispatch complete: started=2 failures=0
```

La sortie de secours est explicite :

```text
gateway unavailable; data dispatch only: promoted=1 blocked=0
```

La sortie JSON inclut le résultat de dispatch. La dispatch soutenue par Gateway peut inclure
`started` et `startFailures` ; la secours basée sur les données inclut
`gatewayUnavailable: true`. Les jetons de réclamation sont masqués de la sortie JSON de carte.

## Parité des Commandes Slash

Les canaux compatibles avec les commandes peuvent utiliser la commande slash correspondante :

```text
/workboard list
/workboard show 7f4a2c10
/workboard create Fix stale worker heartbeat
/workboard dispatch
```

La dispatch de commande slash utilise également le runtime subagent de Gateway, elle suit donc le
même comportement de réclamation, de démarrage de worker et d'échec que le tableau de bord et le chemin Gateway CLI.

`/workboard list` et `/workboard show` sont des commandes de lecture pour les expéditeurs de commandes autorisés. `/workboard create` et `/workboard dispatch` mutent l'état du tableau et
nécessitent le statut de propriétaire sur les surfaces de chat ou un client Gateway avec `operator.write`
ou `operator.admin`.

## Permissions

Le chemin de dispatch CLI appelle Gateway RPC avec les portées `operator.read` et
`operator.write`. Un jeton Gateway en lecture seule peut inspecter les données Workboard
par le biais de méthodes de lecture, mais il ne peut pas créer de cartes ou dispatcher de workers.

Les commandes locales `list`, `create` et `show` opèrent sur le répertoire d'état OpenClaw local utilisé par le profil actuel. Utilisez `--dev` ou `--profile <name>` sur la
commande `openclaw` de haut niveau quand vous avez besoin d'une racine d'état différente.

## Dépannage

### Aucune Carte n'Apparaît

Confirmez que le plugin est activé pour le même profil et la même racine d'état :

```bash
openclaw plugins inspect workboard --runtime --json
```

Si le tableau de bord affiche les cartes mais la CLI ne le fait pas, vérifiez que les deux commandes utilisent
le même paramètre `--dev` ou `--profile`.

### Dispatch Dit Data-Only

Démarrez ou redémarrez la Gateway :

```bash
openclaw gateway restart
openclaw gateway status --deep
```

Puis réessayez `openclaw workboard dispatch`. La secours basée sur les données est utile pour le nettoyage d'état local, mais les exécutions de workers ont besoin d'une Gateway active.

### Dispatch ne Démarre Rien

Vérifiez qu'il y a au moins une carte `ready` sans réclamation active :

```bash
openclaw workboard list --status ready
```

Les cartes peuvent également être ignorées quand le même propriétaire a déjà un travail actif en cours d'exécution
ou en révision. Déplacez le travail terminé vers `done`, libérez les réclamations obsolètes par le biais des outils Workboard, ou exécutez dispatch à nouveau après que le worker actif se termine.

## Connexes

- [Plugin Workboard](/fr/plugins/workboard)
- [Référence CLI](/fr/cli)
- [Commandes slash](/fr/tools/slash-commands)
- [Interface utilisateur Control](/fr/web/control-ui)
