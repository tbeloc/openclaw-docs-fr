---
title: "Hébergement Kubernetes - Note de Maturité de Configuration de Déploiement"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Hébergement Kubernetes - Note de Maturité de Configuration de Déploiement

## Résumé

La documentation et les scripts couvrent la configuration minimale du déploiement et l'amorçage de Kind. Les manifestes Kustomize fournissent une base déployable concrète.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité de Configuration de Déploiement définie par la taxonomie pour la surface d'hébergement Kubernetes.

## Fonctionnalités

- Empaquetage Kustomize : posture de déploiement en priorité Kustomize et Helm non-objectif.
- Prérequis du cluster : accès au cluster, contexte kubectl et prérequis de clé de fournisseur.
- Déploiement rapide : chemin de déploiement de cluster en une seule commande.
- Application de manifeste : flux de travail de création de secret et d'application de manifeste étape par étape.
- Validation Kind : flux de travail de test de cluster Kind local.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (55%)`
- Signaux positifs : La documentation et les scripts couvrent la configuration minimale du déploiement et l'amorçage de Kind ; les manifestes Kustomize fournissent une base déployable concrète.
- Signaux négatifs : Aucune preuve CI automatisée ou en direct spécifique à Kubernetes n'a été trouvée.
- Lacunes d'intégration : Aucune preuve CI automatisée ou en direct spécifique à Kubernetes n'a été trouvée.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, en direct ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : Vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : Vérification de fraîcheur globale réussie ; aucune recherche Discord spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation et les scripts couvrent la configuration minimale du déploiement et l'amorçage de Kind ; les manifestes Kustomize fournissent une base déployable concrète.
- Mauvaises qualités : Aucune faiblesse spécifique à la qualité de mise en œuvre n'a été identifiée séparément des autres classes de lacunes dans cette tranche de notation.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/kubernetes-hosting.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'empaquetage Kustomize, les prérequis du cluster, le déploiement rapide, l'application de manifeste, la validation Kind.
- Signaux négatifs : Aucune preuve CI automatisée ou en direct spécifique à Kubernetes n'a été trouvée.
- Branches de capacité manquantes : Aucune preuve CI automatisée ou en direct spécifique à Kubernetes n'a été trouvée.

Étiquettes de complétude : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La complétude mesure la façon dont cette catégorie fournit complètement l'ensemble de capacités spécifiques à la surface prévu. Le barème exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- Aucune preuve CI automatisée ou en direct spécifique à Kubernetes n'a été trouvée.

## Preuves

### Docs

- `docs/install/kubernetes.md:9`
- `docs/install/kubernetes.md:11-19`
- `docs/install/kubernetes.md:21-50`
- `docs/install/kubernetes.md:52-81`
- `docs/install/kubernetes.md:178-190`

### Source

- `scripts/k8s/deploy.sh:21-25`
- `scripts/k8s/deploy.sh:213-223`
- `scripts/k8s/create-kind.sh:122-127`
- `scripts/k8s/create-kind.sh:169-194`
- `scripts/k8s/manifests/kustomization.yaml:1-7`

### Tests d'intégration

- Aucun identifié dans cette tranche de notation.

### Tests unitaires

- Aucune correspondance dans `test`, `.github/workflows`, ou `package.json`.

### Commandes de validation de surface

- `gitcrawl doctor --json` : `pass` - La fraîcheur de l'archive a été vérifiée avant la notation.
- `discrawl status --json` : `pass` - La fraîcheur de l'archive Discord a été vérifiée avant la notation.

### Requêtes Gitcrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `gitcrawl doctor --json` réussi ; les requêtes de problèmes spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation de sous-agent de surface.

### Requêtes Discrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `discrawl status --json` réussi ; les recherches Discord spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation de sous-agent de surface.

## Provenance d'Audit

- Source de score : `docs/kevinslin/maturity-scorecard/inventory/kubernetes-hosting/scores.yaml`.
- Source de métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
