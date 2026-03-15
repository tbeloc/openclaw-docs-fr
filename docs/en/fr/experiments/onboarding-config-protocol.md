---
summary: "Notes du protocole RPC pour l'assistant d'intégration et le schéma de configuration"
read_when: "Modification des étapes de l'assistant d'intégration ou des points de terminaison du schéma de configuration"
title: "Protocole d'intégration et de configuration"
---

# Protocole d'intégration + Configuration

Objectif : surfaces d'intégration + configuration partagées entre CLI, application macOS et interface Web.

## Composants

- Moteur d'assistant (session partagée + invites + état d'intégration).
- L'intégration CLI utilise le même flux d'assistant que les clients UI.
- Gateway RPC expose les points de terminaison de l'assistant + schéma de configuration.
- L'intégration macOS utilise le modèle d'étape de l'assistant.
- L'interface Web affiche les formulaires de configuration à partir du schéma JSON + indices UI.

## Gateway RPC

- `wizard.start` paramètres : `{ mode?: "local"|"remote", workspace?: string }`
- `wizard.next` paramètres : `{ sessionId, answer?: { stepId, value? } }`
- `wizard.cancel` paramètres : `{ sessionId }`
- `wizard.status` paramètres : `{ sessionId }`
- `config.schema` paramètres : `{}`
- `config.schema.lookup` paramètres : `{ path }`
  - `path` accepte les segments de configuration standard plus les identifiants de plugin délimités par des barres obliques, par exemple `plugins.entries.pack/one.config`.

Réponses (forme)

- Assistant : `{ sessionId, done, step?, status?, error? }`
- Schéma de configuration : `{ schema, uiHints, version, generatedAt }`
- Recherche de schéma de configuration : `{ path, schema, hint?, hintPath?, children[] }`

## Indices UI

- `uiHints` indexés par chemin ; métadonnées optionnelles (label/help/group/order/advanced/sensitive/placeholder).
- Les champs sensibles s'affichent comme des entrées de mot de passe ; aucune couche de masquage.
- Les nœuds de schéma non pris en charge reviennent à l'éditeur JSON brut.

## Notes

- Ce document est le seul endroit pour suivre les refactorisations de protocole pour l'intégration/configuration.
