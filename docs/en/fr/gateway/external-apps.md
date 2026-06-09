---
summary: "Chemin d'intégration actuel pour les applications externes, scripts, tableaux de bord, tâches CI et extensions IDE"
title: "Intégrations Gateway pour applications externes"
sidebarTitle: "Applications externes"
read_when:
  - You are building an external app, script, dashboard, CI job, or IDE extension that talks to OpenClaw
  - You are choosing between Gateway RPC and the Plugin SDK
  - You are integrating with Gateway agent runs, sessions, events, approvals, models, or tools
---

Les applications externes doivent communiquer avec OpenClaw via le protocole Gateway aujourd'hui. Utilisez les méthodes Gateway WebSocket et RPC quand un script, un tableau de bord, une tâche CI, une extension IDE ou un autre processus souhaite démarrer des exécutions d'agent, diffuser des événements, attendre les résultats, annuler du travail ou inspecter les ressources Gateway.

<Warning>
  Il n'y a pas encore de package client npm public. N'ajoutez pas les noms de packages client OpenClaw comme dépendances d'application jusqu'à ce que les notes de version annoncent un package publié et que cette page inclue les instructions d'installation.
</Warning>

<Note>
  Cette page concerne le code en dehors du processus OpenClaw. Le code de plugin qui s'exécute à l'intérieur d'OpenClaw doit utiliser les sous-chemins documentés `openclaw/plugin-sdk/*` à la place.
</Note>

## Ce qui est disponible aujourd'hui

| Surface                                 | Statut | À utiliser pour                                                                                    |
| --------------------------------------- | ------ | -------------------------------------------------------------------------------------------------- |
| [Protocole Gateway](/fr/gateway/protocol)   | Prêt   | Transport WebSocket, établissement de connexion, portées d'authentification, versioning du protocole et événements.         |
| [Référence RPC Gateway](/fr/reference/rpc) | Prêt   | Méthodes Gateway actuelles pour les agents, sessions, tâches, modèles, outils, artefacts et approbations. |
| [`openclaw agent`](/fr/cli/agent)          | Prêt   | Intégration de script unique quand l'appel du CLI est suffisant.                           |
| [`openclaw message`](/fr/cli/message)      | Prêt   | Envoi de messages ou d'actions de canal à partir de scripts.                                                             |

L'arborescence source contient du travail interne sur une future bibliothèque client, mais ce n'est pas une surface d'installation publique. Traitez-le comme un détail d'implémentation en aperçu jusqu'à ce que les packages soient publiés et versionnés.

## Chemin recommandé

1. Exécutez ou découvrez une Gateway.
2. Connectez-vous via le [protocole Gateway](/fr/gateway/protocol).
3. Appelez les méthodes RPC documentées à partir de la [référence RPC Gateway](/fr/reference/rpc).
4. Épinglez la version d'OpenClaw que vous testez.
5. Revérifiez la référence RPC lors de la mise à niveau d'OpenClaw.

Pour les exécutions d'agent, commencez par le RPC `agent` et associez-le à `agent.wait` quand vous avez besoin d'un résultat terminal. Pour l'état de conversation durable, utilisez les méthodes `sessions.*`. Pour les intégrations UI, abonnez-vous aux événements Gateway et rendez uniquement les familles d'événements que votre application comprend.

## Code d'application vs code de plugin

Utilisez Gateway RPC quand le code se trouve en dehors d'OpenClaw :

- Scripts Node qui démarrent ou observent les exécutions d'agent
- Tâches CI qui appellent une Gateway
- tableaux de bord et panneaux d'administration
- extensions IDE
- ponts externes qui n'ont pas besoin de devenir des plugins de canal
- tests d'intégration avec des transports Gateway faux ou réels

Utilisez le Plugin SDK quand le code s'exécute à l'intérieur d'OpenClaw :

- plugins de fournisseur
- plugins de canal
- outils ou hooks de cycle de vie
- plugins de harnais d'agent
- assistants d'exécution de confiance

Les applications externes ne doivent pas importer `openclaw/plugin-sdk/*` ; ces sous-chemins sont destinés aux plugins chargés par OpenClaw.

## Connexes

- [Protocole Gateway](/fr/gateway/protocol)
- [Référence RPC Gateway](/fr/reference/rpc)
- [Commande CLI agent](/fr/cli/agent)
- [Commande CLI message](/fr/cli/message)
- [Boucle d'agent](/fr/concepts/agent-loop)
- [Runtimes d'agent](/fr/concepts/agent-runtimes)
- [Sessions](/fr/concepts/session)
- [Tâches en arrière-plan](/fr/automation/tasks)
- [Agents ACP](/fr/tools/acp-agents)
- [Aperçu du Plugin SDK](/fr/plugins/sdk-overview)
