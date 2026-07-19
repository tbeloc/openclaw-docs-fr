---
summary: "Permettre à un agent d'organiser l'interface utilisateur Control connectée"
title: "Screen"
sidebarTitle: "Screen"
read_when:
  - You want an agent to split, focus, close, or navigate Control UI panes
  - You want an agent to show or hide the sidebar, terminal, or browser panels
  - You need the ui.command capability and fan-out contract
---

L'outil `screen` permet à un agent d'organiser l'interface utilisateur Control basée sur navigateur. C'est une surface de mise en page et de navigation typée, pas une capture d'écran ou une automatisation de navigateur.

L'outil n'est exposé que lorsque le client d'origine annonce la capacité `ui-commands`. Au moins une interface utilisateur Control capable doit toujours être connectée lors de l'exécution de l'outil ; sinon la Gateway retourne `UNAVAILABLE`.

## Actions

| Action                            | Effet                                      | Entrées optionnelles                         |
| --------------------------------- | ------------------------------------------ | -------------------------------------------- |
| `split_right`                     | Diviser le volet de session cible vers la droite | `sessionKey` (par défaut la session actuelle) |
| `split_down`                      | Diviser le volet de session cible vers le bas | `sessionKey` (par défaut la session actuelle) |
| `close_pane`                      | Fermer le volet de session cible           | `sessionKey` (par défaut la session actuelle) |
| `focus`                           | Mettre le focus sur le volet de session cible | `sessionKey` (par défaut la session actuelle) |
| `navigate`                        | Ouvrir la session cible                    | `sessionKey` (par défaut la session actuelle) |
| `sidebar_show` / `sidebar_hide`   | Afficher ou masquer la barre latérale principale | -                                            |
| `terminal_show` / `terminal_hide` | Afficher ou masquer le panneau terminal de l'opérateur | `dock` (`bottom` ou `right`) lors de l'affichage |
| `browser_show` / `browser_hide`   | Afficher ou masquer le panneau navigateur  | `dock` (`bottom` ou `right`) lors de l'affichage |

Une commande réussie retourne `{ "ok": true }` après que la Gateway diffuse l'événement `ui.command` typé.

## Routage et sécurité

Le protocole v1 envoie intentionnellement la commande à chaque interface utilisateur Control connectée qui annonce `ui-commands` ; il ne cible pas un onglet de navigateur spécifique. Cela importe lorsque le même opérateur a plusieurs tableaux de bord ouverts.

La Gateway RPC nécessite `operator.write`. L'outil ne peut modifier que l'état de présentation : il ne peut pas lire les pixels, prendre des captures d'écran, cliquer sur du contenu de page arbitraire, ou contourner les permissions des volets de session et d'opérateur sélectionnés.

## Connexes

- [Control UI](/fr/web/control-ui)
- [Gateway protocol](/fr/gateway/protocol#method-families)
- [Browser tool](/fr/tools/browser)
