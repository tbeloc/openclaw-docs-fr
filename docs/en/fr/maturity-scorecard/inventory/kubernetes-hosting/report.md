---
title: "Rapport de maturité d'hébergement Kubernetes"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Rapport de maturité d'hébergement Kubernetes

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Alpha (50%)`
- Qualité : `Beta (75%)`
- Complétude : `Beta (74%)`
- Fonctionnalités LTS : `0/4`

## Résumé

L'hébergement Kubernetes est un vrai chemin d'hébergement de cluster, mais précoce. La documentation, les scripts et les manifestes Kustomize prennent en charge le déploiement minimal de Gateway, l'amorçage Kind, les secrets Kubernetes, la configuration ConfigMap, l'état PVC, le service ClusterIP, les sondes et l'accès loopback conservateur. Les lacunes principales sont l'absence d'IC automatisé/en direct spécifique à Kubernetes, aucun chemin d'ingress/TLS/NetworkPolicy/sauvegarde empaqueté, et des conseils d'exposition en production qui sont consultatifs plutôt que représentés dans les manifestes.

Ce rapport a été noté à partir de `source_ref=openclaw@29dd7847fd` avec un sous-agent dédié à cette surface. Les vérifications de fraîcheur des archives globales ont réussi avant la notation : `gitcrawl doctor --json` et `discrawl status --json`.

## Matrice

| Catégorie                                                  | LTS | Couverture           | Qualité      | Complétude     | Fonctionnalités à évaluer                                                                  |
| --------------------------------------------------------- | --- | -------------------- | ------------ | -------------- | ------------------------------------------------------------------------------------------ |
| [Configuration du déploiement](deployment-setup.md)       | ❌  | `Alpha (55%)`        | `Beta (76%)` | `Stable (84%)` | Empaquetage Kustomize, Prérequis du cluster, Déploiement rapide, Application de manifeste, Validation Kind  |
| [Configuration et secrets](configuration-and-secrets.md)  | ❌  | `Alpha (52%)`        | `Beta (74%)` | `Beta (76%)`   | Instructions d'agent, Configuration Gateway, Secrets du fournisseur, Rotation des secrets, Image et espace de noms |
| [Accès et exposition](access-and-exposure.md)             | ❌  | `Experimental (43%)` | `Beta (72%)` | `Alpha (58%)`  | Accès par port-forward, Point de terminaison du service, Exposition Ingress, Authentification et TLS, Posture localhost   |
| [Cycle de vie du cluster](cluster-lifecycle.md)           | ❌  | `Alpha (50%)`        | `Beta (78%)` | `Beta (77%)`   | Disposition des ressources, Persistance d'état, Redéploiement, Démantèlement, Contexte de sécurité                       |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou
  les preuves de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de la mise en œuvre et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie fournit complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'
  étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme
  dimension notée séparée.
