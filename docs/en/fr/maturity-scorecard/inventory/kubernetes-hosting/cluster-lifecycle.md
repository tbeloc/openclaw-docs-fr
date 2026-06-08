---
title: "Hébergement Kubernetes - Note de Maturité du Cycle de Vie du Cluster"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Hébergement Kubernetes - Note de Maturité du Cycle de Vie du Cluster

## Résumé

La documentation et les manifestes couvrent le cycle de vie local, les sondes, l'état des PVC et le comportement de redémarrage de base. Le script de déploiement gère les étapes de configuration adjacentes au déploiement.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité du Cycle de Vie du Cluster définie par la taxonomie pour la surface d'hébergement Kubernetes.

## Fonctionnalités

- Disposition des ressources : inventaire des espaces de noms, déploiements, services, PVC, ConfigMaps et secrets.
- Persistance d'état : attentes d'état sauvegardées par PVC et implications de nettoyage.
- Redéploiement : réappliquer les manifestes et le flux de redémarrage des pods.
- Démantèlement : suppression de l'espace de noms et chemin de nettoyage des PVC.
- Contexte de sécurité : notes sur la sécurité des pods, la portée de l'espace de noms et l'isolation à l'exécution.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (50%)`
- Signaux positifs : La documentation et les manifestes couvrent le cycle de vie local, les sondes, l'état des PVC et le comportement de redémarrage de base ; le script de déploiement gère les étapes de configuration adjacentes au déploiement.
- Signaux négatifs : Les runbooks de sauvegarde/restauration, de mise à niveau, de mise à l'échelle et d'exploitation du cluster ne sont pas entièrement packagés ; aucun test de cycle de vie Kubernetes n'a été trouvé.
- Lacunes d'intégration : Les runbooks de sauvegarde/restauration, de mise à niveau, de mise à l'échelle et d'exploitation du cluster ne sont pas entièrement packagés ; aucun test de cycle de vie Kubernetes n'a été trouvé.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, en direct ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation et les manifestes couvrent le cycle de vie local, les sondes, l'état des PVC et le comportement de redémarrage de base ; le script de déploiement gère les étapes de configuration adjacentes au déploiement.
- Mauvaises qualités : Les runbooks de sauvegarde/restauration, de mise à niveau, de mise à l'échelle et d'exploitation du cluster ne sont pas entièrement packagés.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel n'a été utilisée que pour la couverture et non comme entrées de qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'Exhaustivité

- Score : `Beta (77%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/kubernetes-hosting.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la disposition des ressources, la persistance d'état, le redéploiement, le démantèlement et le contexte de sécurité.
- Signaux négatifs : Les runbooks de sauvegarde/restauration, de mise à niveau, de mise à l'échelle et d'exploitation du cluster ne sont pas entièrement packagés ; aucun test de cycle de vie Kubernetes n'a été trouvé.
- Branches de capacité manquantes : Les runbooks de sauvegarde/restauration, de mise à niveau, de mise à l'échelle et d'exploitation du cluster ne sont pas entièrement packagés ; aucun test de cycle de vie Kubernetes n'a été trouvé.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités spécifiques à la surface prévu. Le barème exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- Les runbooks de sauvegarde/restauration, de mise à niveau, de mise à l'échelle et d'exploitation du cluster ne sont pas entièrement packagés.
- Aucun test de cycle de vie Kubernetes n'a été trouvé.

## Preuves

### Documentation

- `docs/install/kubernetes.md:83-92`
- `docs/install/kubernetes.md:153-167`
- `docs/install/kubernetes.md:169-176`
- `docs/gateway/index.md:40-49`
- `docs/gateway/index.md:135-147`

### Source

- `scripts/k8s/deploy.sh:75-79`
- `scripts/k8s/deploy.sh:213-219`
- `scripts/k8s/manifests/deployment.yaml:12-23`
- `scripts/k8s/manifests/deployment.yaml:99-146`
- `scripts/k8s/manifests/pvc.yaml:1-12`

### Tests d'intégration

- Aucun identifié dans cette tranche de notation.

### Tests unitaires

- Aucun test de cycle de vie Kubernetes trouvé.

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

## Provenance de l'Audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/kubernetes-hosting/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
