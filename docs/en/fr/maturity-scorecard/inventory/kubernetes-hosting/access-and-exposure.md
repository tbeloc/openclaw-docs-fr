---
title: "Hébergement Kubernetes - Note de Maturité d'Accès et d'Exposition"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Hébergement Kubernetes - Note de Maturité d'Accès et d'Exposition

## Résumé

La documentation recommande des modèles d'accès et d'exposition conservateurs. Les manifestes de service et de configuration exposent un chemin ClusterIP concret.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité d'Accès et d'Exposition définie par la taxonomie pour la surface d'hébergement Kubernetes.

## Fonctionnalités

- Accès par port-forward : chemin kubectl port-forward pour l'accès local à la Gateway.
- Point de terminaison de service : modèle d'accès Kubernetes Service pour la Gateway.
- Exposition Ingress : exposition Ingress et load-balancer au-delà du port-forward.
- Auth et TLS : authentification requise, TLS et contrôles d'origine pour les déploiements exposés.
- Posture localhost : hypothèses d'exécution au niveau du cluster et limites d'accès localhost.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Expérimental (43%)`
- Signaux positifs : La documentation recommande des modèles d'accès et d'exposition conservateurs ; les manifestes de service et de configuration exposent un chemin ClusterIP concret.
- Signaux négatifs : Les manifestes Ingress, TLS, NetworkPolicy et d'exposition en production ne sont pas fournis ; aucun test d'accès/exposition Kubernetes n'a été trouvé.
- Lacunes d'intégration : Les manifestes Ingress, TLS, NetworkPolicy et d'exposition en production ne sont pas fournis ; aucun test d'accès/exposition Kubernetes n'a été trouvé.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, live ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation recommande des modèles d'accès et d'exposition conservateurs ; les manifestes de service et de configuration exposent un chemin ClusterIP concret.
- Mauvaises qualités : Les manifestes Ingress, TLS, NetworkPolicy et d'exposition en production ne sont pas fournis.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, live et de flux d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, live ou d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Alpha (58%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/kubernetes-hosting.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'accès par port-forward, le point de terminaison de service, l'exposition Ingress, Auth et TLS, la posture localhost.
- Signaux négatifs : Les manifestes Ingress, TLS, NetworkPolicy et d'exposition en production ne sont pas fournis ; aucun test d'accès/exposition Kubernetes n'a été trouvé.
- Branches de capacité manquantes : Les manifestes Ingress, TLS, NetworkPolicy et d'exposition en production ne sont pas fournis ; aucun test d'accès/exposition Kubernetes n'a été trouvé.

Étiquettes de complétude : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La complétude mesure la façon dont cette catégorie fournit complètement l'ensemble de capacités de surface spécifique prévu. Le barème exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- Les manifestes Ingress, TLS, NetworkPolicy et d'exposition en production ne sont pas fournis.
- Aucun test d'accès/exposition Kubernetes n'a été trouvé.

## Preuves

### Docs

- `docs/install/kubernetes.md:76-81`
- `docs/install/kubernetes.md:143-151`
- `docs/install/kubernetes.md:169-176`
- `docs/gateway/remote.md:157-177`
- `docs/gateway/security/exposure-runbook.md:20-34`
- `docs/gateway/security/exposure-runbook.md:155-167`

### Source

- `scripts/k8s/manifests/service.yaml:1-15`
- `scripts/k8s/manifests/configmap.yaml:10-19`

### Tests d'intégration

- Aucun identifié dans cette tranche de notation.

### Tests unitaires

- Aucun test d'accès/exposition Kubernetes trouvé.

### Commandes de validation de surface

- `gitcrawl doctor --json` : `pass` - La fraîcheur des archives a été vérifiée avant la notation.
- `discrawl status --json` : `pass` - La fraîcheur des archives Discord a été vérifiée avant la notation.

### Requêtes Gitcrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `gitcrawl doctor --json` réussi ; les requêtes de problèmes spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation de sous-agent de surface.

### Requêtes Discrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `discrawl status --json` réussi ; les recherches Discord spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation de sous-agent de surface.

## Provenance d'Audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/kubernetes-hosting/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
