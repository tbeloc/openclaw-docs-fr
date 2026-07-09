---
summary: "Contrôle du bureau piloté par agent sur un nœud macOS appairé via l'outil computer et la commande de nœud computer.act"
read_when:
  - Permettre à l'agent de passerelle de voir et contrôler un bureau Mac
  - Armement, permissions ou sécurité pour l'utilisation de l'ordinateur
  - Extension de la commande de nœud computer.act ou de ses exécutants
title: "Utilisation de l'ordinateur"
---

L'utilisation de l'ordinateur permet à l'agent de passerelle de voir et contrôler un bureau **macOS** appairé : il capture une capture d'écran avec la commande de nœud `screen.snapshot` existante et pilote le pointeur et le clavier via une seule commande de nœud dangereuse, `computer.act`. L'ensemble d'actions reflète l'outil `computer_20251124` d'Anthropic, de sorte que tout modèle capable de vision peut le piloter via l'outil agent `computer` intégré.

L'agent émet une commande uniforme, `computer.act` ; il ne peut pas savoir comment un nœud l'exécute. Un nœud macOS exécute `computer.act` en processus avec le moteur d'automatisation Peekaboo intégré (permissions TCC correctes, aucun processus supplémentaire). D'autres plates-formes peuvent exécuter la même commande ultérieurement sans modifier le contrat face à l'agent.

## Exigences

- Un nœud **macOS** appairé (l'application OpenClaw macOS s'exécutant en mode nœud).
- Paramètre de l'application macOS **Allow Computer Control** activé (par défaut : désactivé).
- Permission **Accessibility** macOS accordée à OpenClaw (pour l'injection de pointeur/clavier) et permission **Screen Recording** (pour `screen.snapshot`).
- La commande `computer.act` armée sur la passerelle (elle est dangereuse et désarmée par défaut).
- Un modèle d'agent capable de vision.

## L'outil agent `computer`

L'outil `computer` intégré prend une action par appel. Les coordonnées sont en pixels dans la capture d'écran la plus récente ; le nœud les mappe aux points d'affichage.

- Lectures : `screenshot`.
- Pointeur : `left_click`, `right_click`, `middle_click`, `double_click`, `triple_click`, `mouse_move`, `left_click_drag` (avec `startCoordinate`), `left_mouse_down`, `left_mouse_up`.
- Défilement : `scroll` avec `scrollDirection` (`up|down|left|right`) et `scrollAmount` (coches de molette).
- Clavier : `type` (texte), `key` (combinaison telle que `cmd+shift+t` ou `Return`), `hold_key` (combinaison `text` maintenue pendant `duration` secondes).
- Rythme : `wait` (`duration` secondes).

Les touches de modification se trouvent sur le champ `text` sur les actions de clic et de défilement (`shift`, `ctrl`, `alt`, `cmd`). Après une action d'entrée, l'outil retourne une capture d'écran actualisée pour que le modèle puisse observer le résultat. Si plusieurs nœuds compatibles avec l'ordinateur sont connectés, passez `node` explicitement.

Les captures d'écran sont conservées **modèle uniquement** : elles ne sont jamais livrées automatiquement au canal de chat. Traitez tout contenu à l'écran comme une entrée non fiable ; l'outil avertit le modèle de ne pas suivre les instructions à l'écran qui entrent en conflit avec la demande de l'utilisateur.

## La commande de nœud `computer.act`

`computer.act` est la seule commande de nœud par laquelle l'outil achemine l'entrée (`node.invoke` avec `command: "computer.act"`). Elle est :

- **Dangereuse par défaut** : listée dans les commandes de nœud dangereuses intégrées et exclue de la liste d'autorisation d'exécution jusqu'à ce qu'elle soit explicitement armée. Un nœud macOS peut toujours la déclarer lors de l'appairage pour que la surface soit approuvée une fois.
- **macOS uniquement** aujourd'hui : annoncée uniquement par un nœud macOS qui a **Allow Computer Control** activé.

Les lectures réutilisent `screen.snapshot` ; il n'y a pas de deuxième chemin de capture. Voir [Nœuds de caméra et d'écran](/fr/nodes/camera) pour la commande de capture partagée.

## Activer et armer

1. Dans l'application macOS, activez **Settings -> Allow Computer Control**, puis accordez **Accessibility** et **Screen Recording** lorsque vous y êtes invité.
2. Approuvez la mise à jour d'appairage sur la passerelle (une nouvelle commande force le réappairage).
3. Armez `computer.act` pour une fenêtre délimitée. Le plugin `phone-control` expose un groupe `computer` :

   ```text
   /phone arm computer 30m
   /phone status
   /phone disarm
   ```

   L'armement nécessite `operator.admin` (ou le propriétaire) et expire automatiquement. L'armement bascule uniquement ce que la passerelle peut invoquer ; l'application macOS applique toujours son paramètre **Allow Computer Control** et sa permission Accessibility. Les opérateurs peuvent équivalemment ajouter `computer.act` à `gateway.nodes.allowCommands`.

## Sécurité

- Rien n'est autonome : `computer.act` reste désarmé jusqu'à ce qu'un opérateur l'arme, et chaque couche (liste d'autorisation de passerelle, paramètre macOS, permission Accessibility) doit être d'accord.
- Les captures d'écran sont modèle uniquement et ne sont jamais envoyées automatiquement au chat (problème [#44759](https://github.com/openclaw/openclaw/issues/44759)).
- Traitez le contenu de l'écran comme non fiable ; il peut contenir une injection d'invite.

## Relation avec d'autres chemins de contrôle de bureau

C'est le chemin piloté par agent. Voir [Pont Peekaboo](/fr/platforms/mac/peekaboo) pour savoir comment il se rapporte à l'hôte PeekabooBridge, Codex Computer Use et le MCP `cua-driver` direct.
