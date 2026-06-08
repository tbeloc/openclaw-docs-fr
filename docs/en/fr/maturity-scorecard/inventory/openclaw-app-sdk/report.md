---
title: "OpenClaw App SDK Maturity Report"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Rapport de Maturité du SDK OpenClaw App

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (75%)`
- Qualité : `Beta (75%)`
- Complétude : `Alpha (69%)`
- Fonctionnalités LTS : `0/6`

## Résumé

OpenClaw App SDK dispose d'un vrai package `@openclaw/sdk` implémenté avec de la documentation, des exports typés, une couverture e2e WebSocket, une couverture e2e réelle des événements Gateway, une couverture e2e des consommateurs de package, et une preuve Gateway en direct avec gating d'environnement. Les principaux limiteurs sont l'empaquetage privé/0.0.0-private, l'absence de `sdk-react` et `sdk-testing`, l'incomplétude de `gateway: "auto"` et des boutons de portée de haut niveau, le client généré en conception uniquement, les callbacks/questions d'approbation en conception uniquement, et une couverture fine en direct/runtime pour les helpers.

Ce rapport a été noté à partir de `source_ref=openclaw@29dd7847fd` avec un sous-agent dédié à cette surface. Les vérifications globales de fraîcheur des archives ont réussi avant la notation : `gitcrawl doctor --json` et `discrawl status --json`.

## Matrice

| Catégorie                                       | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                          |
| ----------------------------------------------- | --- | -------------- | -------------- | -------------- | -------------------------------------------------------------------------------------------------- |
| [Client API](client-api.md)                     | ❌  | `Stable (86%)` | `Stable (82%)` | `Beta (78%)`   | Points d'entrée SDK, Disposition des espaces de noms, Division de package, Limite App/plugin       |
| [Gateway Access](gateway-access.md)             | ❌  | `Beta (78%)`   | `Beta (74%)`   | `Alpha (64%)`  | Connexion Gateway, Configuration URL et token, Gateway auto, Transport personnalisé, Portées et redaction |
| [Agent Conversations](agent-conversations.md)   | ❌  | `Beta (78%)`   | `Stable (80%)` | `Stable (84%)` | Handles d'agent, Exécutions d'agent, Résultats d'exécution, Création de session, Envoi de session, Contrôles de session |
| [Events and Approvals](events-and-approvals.md) | ❌  | `Beta (74%)`   | `Beta (73%)`   | `Alpha (58%)`  | Flux d'événements, Enveloppe d'événement, Curseurs de relecture, Callbacks d'approbation, Questions |
| [Resource Helpers](resource-helpers.md)         | ❌  | `Alpha (58%)`  | `Beta (72%)`   | `Beta (70%)`   | Modèles, ToolSpace, Artefacts, Tâches, Environnements                                             |
| [Compatibility](compatibility.md)               | ❌  | `Beta (76%)`   | `Beta (70%)`   | `Alpha (62%)`  | Client généré, Wrappers ergonomiques, Appels non supportés, Alignement de schéma, Contrat de package public |

## Rubrique de notation

- Couverture :
  notation maturity-label pour l'intégration, e2e, en direct, ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de support
  mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation maturity-label pour la robustesse de l'implémentation et opérationnelle. Les tests
  unitaires, d'intégration, e2e, en direct, et de flux runtime réel sont des entrées de Couverture
  uniquement ; ils ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation maturity-label pour la façon dont la catégorie livre complètement
  l'ensemble de capacités spécifiques à la surface prévue. Utilisez les instructions de complétude
  liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou quand la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  une dimension de score séparée.
