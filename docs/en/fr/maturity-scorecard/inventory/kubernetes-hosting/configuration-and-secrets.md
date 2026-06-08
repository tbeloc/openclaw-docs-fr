---
title: "Hébergement Kubernetes - Note de Maturité Configuration et Secrets"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Hébergement Kubernetes - Note de Maturité Configuration et Secrets

## Résumé

La documentation et les scripts de déploiement couvrent les Secrets Kubernetes et la configuration de Gateway basée sur ConfigMap. Le manifeste de déploiement intègre la configuration, le secret et l'environnement d'exécution dans le pod.

## Portée de la catégorie

Cette catégorie couvre la zone de capacité Configuration et Secrets définie par la taxonomie pour la surface d'hébergement Kubernetes.

## Fonctionnalités

- Instructions d'agent : injection d'instructions d'agent basée sur ConfigMap.
- Configuration Gateway : configuration Gateway basée sur ConfigMap.
- Secrets de fournisseur : configuration de clé de fournisseur basée sur Kubernetes Secret.
- Rotation de secret : attentes de correction de clé de fournisseur et redéploiement.
- Image et namespace : épinglage d'image personnalisée et remplacement de namespace.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (52%)`
- Signaux positifs : la documentation et les scripts de déploiement couvrent les Secrets Kubernetes et la configuration de Gateway basée sur ConfigMap ; le manifeste de déploiement intègre la configuration, le secret et l'environnement d'exécution dans le pod.
- Signaux négatifs : aucun test automatisé de secret/config Kubernetes n'a été trouvé ; la rotation de secret et le durcissement de production ne sont pas profondément intégrés.
- Lacunes d'intégration : aucun test automatisé de secret/config Kubernetes n'a été trouvé ; la rotation de secret et le durcissement de production ne sont pas profondément intégrés.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, live ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : vérification de fraîcheur globale réussie ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : la documentation et les scripts de déploiement couvrent les Secrets Kubernetes et la configuration de Gateway basée sur ConfigMap ; le manifeste de déploiement intègre la configuration, le secret et l'environnement d'exécution dans le pod.
- Mauvaises qualités : la rotation de secret et le durcissement de production ne sont pas profondément intégrés.
- Exclus de la qualité : la couverture des tests unitaires, d'intégration, e2e, live et d'exécution réel a été utilisée uniquement pour la couverture et non comme entrées de qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, live ou d'exécution réel comme entrée de notation.

## Score d'exhaustivité

- Score : `Beta (76%)`
- Instructions de surface : noté par rapport à `.agents/skills/claw-score/references/completeness/kubernetes-hosting.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les instructions d'agent, la configuration Gateway, les secrets de fournisseur, la rotation de secret, l'image et le namespace.
- Signaux négatifs : aucun test automatisé de secret/config Kubernetes n'a été trouvé ; la rotation de secret et le durcissement de production ne sont pas profondément intégrés.
- Branches de capacité manquantes : aucun test automatisé de secret/config Kubernetes n'a été trouvé ; la rotation de secret et le durcissement de production ne sont pas profondément intégrés.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités spécifiques à la surface prévu. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes connues

- Aucun test automatisé de secret/config Kubernetes n'a été trouvé.
- La rotation de secret et le durcissement de production ne sont pas profondément intégrés.

## Preuves

### Docs

- `docs/install/kubernetes.md:94-141`
- `docs/gateway/secrets.md:25-37`
- `docs/help/environment.md:25-36`

### Source

- `scripts/k8s/deploy.sh:85-159`
- `scripts/k8s/deploy.sh:164-207`
- `scripts/k8s/manifests/configmap.yaml:8-38`
- `scripts/k8s/manifests/deployment.yaml:63-98`

### Tests d'intégration

- Aucun identifié dans cette tranche de notation.

### Tests unitaires

- Aucun test de secret/config Kubernetes trouvé.

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

## Provenance de l'audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/kubernetes-hosting/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
