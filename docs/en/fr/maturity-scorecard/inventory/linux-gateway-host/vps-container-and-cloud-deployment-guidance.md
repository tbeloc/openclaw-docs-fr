---
title: "Linux Gateway host - Deployment Targets Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Linux Gateway host - Deployment Targets Maturity Note

## Résumé

OpenClaw dispose de conseils d'hébergement Linux larges couvrant VPS, Docker, Hetzner, DigitalOcean, Kubernetes et Podman. La forme sécurisée recommandée est cohérente : utilisateurs non-root, état persistant, Gateway en loopback en premier, tunnel SSH ou Tailscale, authentification explicite lors de l'exposition au-delà du loopback, et réglage à faible mémoire. La couverture et la qualité sont en version bêta car la matrice fournisseur/conteneur est large et les preuves d'archive montrent toujours des frictions de support pour les contextes sécurisés Docker/VPS, le comportement du relais de navigateur, la configuration XDG, les hôtes à faibles spécifications et la gestion multi-instances.

## Portée de la catégorie

Inclus dans cette catégorie :

- VPS : Définit le comportement de configuration VPS, d'authentification, de configuration et de vérification de l'opérateur pour les conseils de déploiement Vps, Container et Cloud.
- Container : Définit le comportement de configuration Container, d'authentification, de configuration et de vérification de l'opérateur pour les conseils de déploiement Vps, Container et Cloud.
- Cloud Deployment Guidance : Définit le comportement de configuration Cloud Deployment Guidance, d'authentification, de configuration et de vérification de l'opérateur pour les conseils de déploiement Vps, Container et Cloud.

## Fonctionnalités

- VPS : Définit le comportement de configuration VPS, d'authentification, de configuration et de vérification de l'opérateur pour les conseils de déploiement Vps, Container et Cloud.
- Container : Définit le comportement de configuration Container, d'authentification, de configuration et de vérification de l'opérateur pour les conseils de déploiement Vps, Container et Cloud.
- Cloud Deployment Guidance : Définit le comportement de configuration Cloud Deployment Guidance, d'authentification, de configuration et de vérification de l'opérateur pour les conseils de déploiement Vps, Container et Cloud.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`
- Justification : la documentation couvre de nombreuses variantes de déploiement Linux et la source dispose du support conteneur/runtime, mais l'ampleur est plus grande que la maturité de chaque chemin fournisseur.
- Lacunes : il n'existe pas de matrice de support unique qui classe VPS, Docker, Podman, Kubernetes et les fournisseurs spécifiques par utilisation recommandée, posture d'authentification, modèle de persistance et limites connues.

## Score de qualité

- Score : `Bêta (72%)`
- Justification : l'histoire du déploiement est utilisable pour les opérateurs expérimentés, mais les preuves d'archive montrent un risque substantiel visible par l'utilisateur dans les variantes conteneur/VPS.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, live et runtime-flow.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-gateway-host.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour VPS, Container, Cloud Deployment Guidance.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même ampleur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une matrice de support de déploiement d'hôte Linux pour VPS, Docker, Podman, Kubernetes et la documentation spécifique au fournisseur.
- Marquer les chemins de déploiement recommandés pour les utilisateurs normaux par rapport aux opérateurs expérimentés.
- Consolider la faible mémoire, le relais de navigateur, le contexte sécurisé et le dépannage de la configuration XDG pour les hôtes VPS/conteneur.

## Preuves

### Docs

- `docs/vps.md:11-44` documente la configuration du serveur Linux/VPS, le choix du fournisseur, l'état détenu par Gateway, l'accès à l'interface utilisateur de contrôle/Tailscale/SSH, les sauvegardes et les paramètres par défaut sécurisés.
- `docs/vps.md:79-132` documente le réglage des petites VM et ARM, le réglage systemd, le cache de compilation, `OPENCLAW_NO_RESPAWN` et les contrôles de mémoire.
- `docs/install/docker.md:26-60` documente la configuration de Gateway conteneurisée et l'écriture de jetons ; `docs/install/docker.md:216-228` explique les modes de liaison LAN par rapport au loopback.
- `docs/install/hetzner.md:11-24` documente Gateway persistant sur Hetzner VPS avec Docker et son modèle de sécurité.
- `docs/install/digitalocean.md:41-91` couvre les utilisateurs non-root, l'installation Node/OpenClaw, linger, systemd, swap et les vérifications de journal.
- `docs/install/kubernetes.md:143-152` documente l'authentification, TLS et les origines lors de l'exposition au-delà du port-forward.
- `docs/install/podman.md:127-153` documente l'opération Quadlet/systemd utilisateur, les journaux et linger.

### Source

- `src/infra/container-environment.ts:3-52` détecte les environnements de conteneur à partir des sentinelles et cgroups.
- `src/cli/container-target.ts:32-64` analyse la sélection de cible de conteneur et `OPENCLAW_CONTAINER`.
- `src/cli/container-target.ts:159-176` rejette l'utilisation non sécurisée du proxy loopback sauf si explicitement autorisée.
- `scripts/docker/setup.sh:125-155` synchronise la configuration de Gateway et les origines autorisées pour l'accès au conteneur non-loopback.
- `scripts/run-openclaw-podman.sh:206-213` applique les attentes Podman sans root.
- `scripts/k8s/deploy.sh:85-159` applique les secrets via un chemin temporaire et préserve/génère les jetons Gateway sans écrire les secrets dans le checkout.

### Tests d'intégration

- `test/scripts/docker-build-helper.test.ts`, `test/scripts/docker-e2e-plan.test.ts` et `test/scripts/live-docker-stage.test.ts` couvrent les plans de conteneur Linux Docker et en étapes.
- `src/docker-setup.e2e.test.ts` couvre le comportement de configuration Docker.
- `src/cli/container-target.test.ts` couvre le comportement d'exécution de cible de conteneur.

### Tests unitaires

- `src/dockerfile.test.ts` enregistre les attentes de runtime Docker, CA, Python/tini, dépendance du navigateur, target-platform et élagage pnpm.
- `src/infra/container-environment.test.ts` couvre la détection de conteneur.
- `src/cli/container-target.test.ts` couvre le rejet du proxy non sécurisé et le dépouillage de l'environnement.

### Requêtes Gitcrawl

- La requête spécifique `VPS Docker container Hetzner DigitalOcean GCP Oracle Kubernetes Podman OpenClaw` n'a retourné aucun résultat.
- La requête plus large `Docker VPS` a retourné le problème #71669 pour les avertissements de connexion sécurisée de l'interface utilisateur de contrôle Docker/VPS, le problème #39659 pour la gestion multi-instances de première classe, le problème #32473 pour le comportement du contexte sécurisé sur Hostinger VPS Docker, le problème #53628 pour la gestion de la configuration XDG dans Docker/Hetzner, le problème #53599 pour la régression du relais de navigateur sur Docker/VPS et le problème #53600 pour les performances VPS limitées.

### Requêtes Discrawl

- La requête `Docker VPS OpenClaw` a trouvé une demande d'aide d'installation Hetzner Docker/Gateway/Telegram du 2026-05-28.
- La même requête a trouvé des responsables discutant des bloqueurs VPS à faible spécification et de la pratique de tester les cas CLI/source/conteneur-friendly dans Docker ou VPS.
