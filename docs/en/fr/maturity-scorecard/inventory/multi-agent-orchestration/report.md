---
title: "Rapport de maturité d'orchestration multi-agents"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Rapport de maturité d'orchestration multi-agents

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Beta (72%)`
- Qualité : `Beta (78%)`
- Complétude : `Beta (78%)`
- Fonctionnalités LTS : `0/6`

## Résumé

L'orchestration multi-agents est globalement en Beta. La configuration, l'isolation, le routage, le routage des comptes et les voies spécialisées disposent d'une couverture solide en documentation/source/tests ; la surface reste en dessous de Stable car la preuve complète e2e multi-canal en direct est limitée et l'identité des délégués reste davantage sous forme de politique/runbook que de flux de produit appliqué.

Ce rapport a été noté à partir de `source_ref=openclaw@29dd7847fd` avec un sous-agent dédié à cette surface. Les vérifications globales de fraîcheur des archives ont réussi avant la notation : `gitcrawl doctor --json` et `discrawl status --json`.

## Matrice

| Catégorie                                        | LTS | Couverture           | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                        |
| ----------------------------------------------- | --- | -------------------- | -------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| [Configuration d'agent](agent-setup.md)         | ❌  | `Beta (74%)`         | `Stable (82%)` | `Stable (84%)` | Ajouter des agents, Liste et suppression d'agents, Fichiers d'identité, Configuration non-interactive, Agent unique par défaut |
| [Isolation d'agent](agent-isolation.md)         | ❌  | `Stable (82%)`       | `Beta (78%)`   | `Beta (76%)`   | Séparation d'espace de travail, Séparation d'état, Séparation d'authentification, Séparation de session, Profils d'outils |
| [Routage de conversation](conversation-routing.md) | ❌  | `Beta (76%)`         | `Stable (84%)` | `Stable (86%)` | Sélection d'agent, Précédence de routage, Secours par défaut, Remplacements pairs, Exemples multi-canal |
| [Routage de compte](account-routing.md)         | ❌  | `Beta (78%)`         | `Stable (84%)` | `Stable (82%)` | Configuration multi-compte, Sélection de compte, Comptes par défaut, Identifiants de compte, Cibles de livraison |
| [Voies spécialisées](specialist-lanes.md)       | ❌  | `Beta (78%)`         | `Beta (74%)`   | `Beta (76%)`   | Contrats de voie, Transfert en arrière-plan, Contrôles de concurrence, Contrôles de priorité, Transfert du coordinateur |
| [Identités de délégué](delegate-identities.md)  | ❌  | `Experimental (45%)` | `Alpha (68%)`  | `Alpha (62%)`  | Délégués nommés, Modèle d'autorité, Niveaux de délégué, Délégation d'identité, Assistants organisationnels |

## Rubrique de notation

- Couverture :
  notation maturity-label pour l'intégration, e2e, en direct ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent
  fournir un contexte de support mais ne rendent jamais une fonctionnalité
  couverte par eux-mêmes.
- Qualité :
  notation maturity-label pour la robustesse de l'implémentation et
  opérationnelle. La couverture des tests unitaires, d'intégration, e2e, en
  direct et de flux runtime réel sont des entrées de Couverture uniquement ;
  elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation maturity-label pour la façon dont la catégorie livre complètement
  l'ensemble de capacités spécifiques à la surface prévue. Utilisez les
  instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez
  le libellé de maturité supérieur.
- Lacunes majeures en qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des
  fonctionnalités plutôt que comme dimension notée séparée.
