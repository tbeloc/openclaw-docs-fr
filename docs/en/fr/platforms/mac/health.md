---
summary: "Comment l'application macOS signale les états de santé de la passerelle/Baileys"
read_when:
  - Debugging mac app health indicators
title: "Vérifications de santé"
---

# Vérifications de santé sur macOS

Comment vérifier si le canal lié est sain à partir de l'application de la barre de menu.

## Barre de menu

- Le point d'état reflète désormais la santé de Baileys :
  - Vert : lié + socket ouvert récemment.
  - Orange : connexion/nouvelle tentative.
  - Rouge : déconnecté ou sonde échouée.
- La deuxième ligne affiche « linked · auth 12m » ou affiche la raison de l'échec.
- L'élément de menu « Run Health Check » déclenche une sonde à la demande.

## Paramètres

- L'onglet Général gagne une carte Santé affichant : âge de l'authentification liée, chemin/nombre du magasin de sessions, heure de la dernière vérification, dernier code d'erreur/statut, et boutons pour Exécuter la vérification de santé / Afficher les journaux.
- Utilise un instantané en cache pour que l'interface utilisateur se charge instantanément et se dégrade gracieusement en mode hors ligne.
- **Onglet Canaux** affiche l'état du canal + contrôles pour WhatsApp/Telegram (connexion QR, déconnexion, sonde, dernière déconnexion/erreur).

## Fonctionnement de la sonde

- L'application exécute `openclaw health --json` via `ShellExecutor` toutes les ~60s et à la demande. La sonde charge les identifiants et signale l'état sans envoyer de messages.
- Mettez en cache le dernier bon instantané et la dernière erreur séparément pour éviter le scintillement ; affichez l'horodatage de chacun.

## En cas de doute

- Vous pouvez toujours utiliser le flux CLI dans [Gateway health](/gateway/health) (`openclaw status`, `openclaw status --deep`, `openclaw health --json`) et suivre `/tmp/openclaw/openclaw-*.log` pour `web-heartbeat` / `web-reconnect`.
