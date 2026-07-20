---
summary: "Tableaux de bord de session : widgets créés par l'agent, tableaux, onglets et chat ancré"
read_when:
  - Using or explaining session dashboards in the Control UI
  - Deciding what agents can do on a board and what needs an operator grant
title: "Tableaux de bord de session"
---

Chaque fil de discussion dans l'interface de contrôle a deux facettes : la conversation que vous connaissez, et un **tableau de bord** — une grille de widgets en direct que votre agent crée pour vous. Un fil sans widgets, c'est juste du chat. Dès qu'un widget est épinglé, un bouton bascule **Chat | Tableau de bord** apparaît dans l'en-tête, et le tableau de bord devient la surface principale avec votre chat ancré à côté.

Il n'y a rien à configurer et aucune application séparée à paramétrer : les tableaux de bord sont une fonctionnalité centrale, appartenant au fil, stockés avec l'agent, et ils survivent à `/new` et `/reset` (le contexte de la conversation s'efface ; le tableau reste).

## Créer un tableau de bord en demandant

Demandez à votre agent ce que vous voulez voir :

> Create a widget named revenue-graph: an interactive bar chart of monthly
> revenue. Add "Bars" and "Trend" buttons that switch views. Pin it to my
> dashboard.

L'agent affiche d'abord le widget en ligne dans le chat, pour que vous puissiez le regarder avant qu'il n'aille ailleurs. À partir de là :

- **Vous l'épinglez** : survolez un widget en ligne et choisissez **Épingler au tableau de bord**.
- **Ou l'agent l'épingle** directement quand vous le demandez, et le met à jour plus tard par nom — les widgets ont des noms stables, donc « mettre à jour revenue-graph avec les chiffres de juin » remplace le contenu sur place tandis que le tableau reste immobile.

Les widgets sont de petites applications autonomes (HTML/JS/SVG dans un bac à sable strict). Les boutons et les bascules de vue à l'intérieur d'un widget fonctionnent immédiatement — changer la vue d'un graphique ne nécessite jamais l'agent.

## Le tableau

- **Grille fluide.** Glissez les widgets par leur poignée ; tout se réorganise et se compacte automatiquement. Redimensionnez par poignée ou choisissez un préréglage de taille (petit, moyen, grand, très grand) dans le menu du widget. Personne ne place de pixels — ni vous, ni l'agent.
- **Onglets.** Un tableau peut avoir plusieurs pages — par exemple, un onglet de vue d'ensemble et un onglet ciblé avec un grand widget. Chaque onglet se souvient de sa propre position d'ancrage du chat.
- **Chat ancré.** Sur la face du tableau de bord, votre conversation s'ancre à gauche, à droite ou en bas, se redimensionne comme la barre latérale, et peut être complètement masquée — l'agent vous entend toujours quand vous la ramenez.
- **Parité de l'agent.** Tout ce que vous pouvez faire, l'agent peut le faire avec son outil `dashboard` : ajouter, mettre à jour, déplacer, redimensionner et supprimer des widgets, gérer les onglets, basculer l'onglet visible, et déplacer ou masquer l'ancrage du chat. Demandez « mets le chat à gauche et affiche l'onglet finances » et regardez ça se faire.

## Ce que les widgets sont autorisés à faire

Un widget qui ne fait que rendre n'a besoin d'aucune approbation — il apparaît instantanément, exactement comme les widgets de chat en ligne, et son accès réseau est complètement désactivé.

Les widgets qui veulent de la **portée** doivent la déclarer, et vous l'accordez une fois par widget avec un seul appui :

- **Réseau** (`net`) : récupérer les origines HTTPS déclarées directement depuis le bac à sable — par exemple, une carte météo qui se rafraîchit elle-même à partir d'une API.
- **Données de passerelle** (`data`) : flux en lecture seule comme les sessions, l'utilisation ou l'état cron, résolus par la passerelle — le widget ne détient jamais votre jeton.
- **Automatisation** (`actions`) : déclencher un travail cron spécifique, pour qu'un bouton puisse exécuter une tâche réelle (qui peut utiliser un modèle plus petit) sans réveiller votre conversation principale.
- **Invite** (`prompt`) : envoyer des messages dans votre fil sans la confirmation par clic que les widgets non approuvés nécessitent.

Les autorisations sont liées aux octets exacts du widget et à la révision que vous avez examinée. Si l'agent change le widget et demande _plus_ que ce que vous avez approuvé, il revient en attente ; rafraîchir le contenu dans les mêmes permissions conserve l'autorisation. Les interactions de widget que l'agent devrait connaître (filtres que vous avez cliqués, vues que vous avez basculées) le rejoignent silencieusement comme des avis de session — il reste informé sans être interrompu.

## Applications MCP sur le tableau

Si votre passerelle a des serveurs MCP configurés, les applications MCP interactives qui apparaissent dans le chat peuvent être épinglées comme n'importe quel widget. Les applications épinglées reviennent à la vie sur le tableau avec des sessions fraîches ; par défaut, elles sont en affichage uniquement, et accorder au widget ses outils de serveur déclarés le rend entièrement interactif — avec la même approbation en un appui, liée à la révision, que tout le reste.

## Bon à savoir

- Réinitialiser un fil qui a un tableau demande une confirmation et conserve le tableau.
- Supprimer un fil supprime son tableau.
- Les tableaux vivent sur votre passerelle (dans la base de données de l'agent propriétaire) et apparaissent sur chaque appareil à partir duquel vous vous connectez.
- Le modèle de sécurité, les détails de stockage et la justification de la conception vivent dans [Architecture des tableaux de bord](/fr/web/dashboard-architecture), y compris les compromis du bac à sable documentés.
