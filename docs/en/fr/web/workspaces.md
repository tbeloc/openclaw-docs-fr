---
summary: "Espaces de travail composables par agent dans l'interface de contrôle"
read_when:
  - Building or rearranging workspace tabs and widgets
  - Letting an agent compose a workspace
  - Reviewing the custom-widget approval and sandbox model
title: "Workspaces"
---

L'onglet **Workspaces** dans l'[interface de contrôle](/fr/web/control-ui) est une surface que vous et vos agents arrangez ensemble. Les onglets, les widgets, leurs positions sur une grille de 12 colonnes et leurs liaisons de données vivent tous dans un seul document. Tout ce qui peut modifier ce document peut composer l'espace de travail : vous, la CLI `openclaw workspaces`, ou un agent appelant les outils `workspace_*`.

Chaque écriture passe par le même chemin validé, donc la disposition d'un humain et celle d'un agent ne peuvent pas diverger. Chaque écriture acceptée augmente une version et diffuse `plugin.workspaces.changed`, de sorte que la modification d'un agent apparaît dans un navigateur déjà ouvert sans rechargement.

## Activer les Workspaces

Le plugin Workspaces fourni est désactivé par défaut. Dans l'interface de contrôle, ouvrez **Plugins**, trouvez **Workspaces**, et sélectionnez **Enable**. Vous pouvez également l'activer à partir de la CLI :

```sh
openclaw plugins enable workspaces
```

L'activation du plugin ajoute l'onglet **Workspaces** et rend disponibles la CLI `openclaw workspaces` et les outils agent `workspace_*`. La désactivation supprime ces surfaces sans supprimer la base de données de l'espace de travail ou les ressources des widgets.

## L'espace de travail par défaut

Au premier chargement, vous obtenez un espace de travail **Overview** : cartes de coûts et de jetons, santé des instances, sessions, statut cron et un flux d'activité. C'est du contenu d'espace de travail ordinaire — déplacez-le, réduisez-le, masquez-le ou supprimez-le.

## Widgets intégrés

Neuf widgets de confiance sont fournis avec le plugin et s'affichent en tant qu'interface propriétaire :

`stat-card`, `markdown`, `table`, `iframe-embed`, `sessions`, `usage`, `cron`,
`instances`, `activity`.

Les widgets déclarent les données via des **liaisons**, ils ne récupèrent jamais par eux-mêmes :

| Liaison  | Se résout en                                                                                               |
| -------- | --------------------------------------------------------------------------------------------------------- |
| `static` | Une valeur littérale stockée dans le document (8 KB max).                                                        |
| `file`   | Un fichier JSON, Markdown ou CSV sous `<stateDir>/workspaces/data/`, optionnellement restreint par un pointeur JSON. |
| `rpc`    | L'une des méthodes de passerelle en lecture seule d'une liste d'autorisation fixe, résolue par l'interface de contrôle de confiance.                |

La liaison `file` est le moyen le plus simple de mettre vos propres chiffres dans un espace de travail : écrivez un fichier JSON dans le répertoire de données et pointez une `stat-card` dessus.

## Provenance

Les onglets et les widgets portent un timbre `createdBy` — `user`, `system`, ou `agent:<id>` — défini par celui qui a effectué l'écriture. Il ne peut pas être fourni par l'appelant, donc un agent ne peut pas étiqueter son travail comme le vôtre, et la puce "AI" sur un widget créé par un agent signifie toujours ce qu'elle dit.

## Widgets personnalisés

Un agent peut créer un vrai widget HTML avec `workspace_widget_scaffold` (ou vous pouvez le faire avec `openclaw workspaces widget-scaffold <name>`). Le code créé par un agent est traité comme hostile :

- Un widget échafaudé entre dans le registre comme **pending**. Aucun iframe n'est créé, et la route d'actif retourne 404 pour ses fichiers, jusqu'à ce qu'un opérateur l'approuve.
- L'approbation est une décision distincte de la modification d'une disposition : `workspaces.widget.approve` nécessite la portée `operator.approvals`, la même portée qui protège les approbations d'exécution.
- Un widget approuvé s'affiche dans un `<iframe sandbox="allow-scripts">` — jamais `allow-same-origin` — donc son origine est opaque et il ne peut pas accéder au DOM, au stockage ou aux cookies du parent.
- Ses ressources sont servies avec `connect-src 'none'`, bloquant les réseaux de scripts tels que `fetch`, XHR et WebSockets. Il ne détient aucune accréditation et ne communique jamais avec la passerelle.
- Les données ne lui parviennent que via un pont `postMessage` versionné. Le code personnalisé peut recevoir des liaisons `static` déclarées, qui sont déjà des valeurs d'espace de travail créées par un agent ou un opérateur. Les liaisons RPC et fichier restent dans les widgets intégrés de confiance : les navigateurs permettent à un enfant en bac à sable de naviguer dans son propre cadre, donc les données privilégiées ne sont jamais affichées dans du HTML créé par un agent.

L'envoi d'une invite dans le chat à partir d'un widget nécessite en outre une capacité de manifeste, une confirmation par invocation citant le texte exact, et passe une limite de débit.

## CLI

```sh
openclaw workspaces tabs list
openclaw workspaces tabs create --title Financials
openclaw workspaces widget-scaffold revenue-chart --title "Revenue Chart"
openclaw workspaces widget-approve revenue-chart
```

`widget-approve` nécessite un appareil associé à la portée `operator.approvals` ; l'approbation à partir de l'interface de contrôle ne l'est pas, car le navigateur la détient déjà.

## Stockage

Le document d'espace de travail, le registre de widgets personnalisés et un anneau d'annulation de 20 entrées vivent dans `<stateDir>/workspaces/workspaces.sqlite`. Les ressources de widgets créées par un agent restent sur le disque sous `<stateDir>/workspaces/widgets/<name>/`, et les données de liaison de fichier sous `<stateDir>/workspaces/data/`, car un agent les crée avec des outils de fichier ordinaires et la route du widget sert leurs octets.
