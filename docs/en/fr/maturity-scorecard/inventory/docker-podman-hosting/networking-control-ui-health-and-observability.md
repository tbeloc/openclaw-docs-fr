---
title: "Hébergement Docker / Podman - Note de maturité pour la mise en réseau, l'interface de contrôle, la santé et l'observabilité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de maturité pour la mise en réseau, l'interface de contrôle, la santé et l'observabilité

## Résumé

L'hébergement Docker et Podman dispose de paramètres de mise en réseau bien documentés : Docker Compose publie les ports Gateway/bridge, définit par défaut la Gateway sur `lan` à l'intérieur du conteneur, mappe `host.docker.internal`, désactive Bonjour par défaut et documente les sondes de santé ainsi que les métriques authentifiées. Podman publie uniquement la boucle locale par défaut et recommande Tailscale géré par l'hôte. La couverture se situe à la limite bêta/stable car les véritables voies e2e couvrent les chemins de mise en réseau, mais les preuves source/archive montrent toujours les risques liés aux healthcheck, à l'IP du bridge, au contexte sécurisé et à la disponibilité au redémarrage.

## Portée de la catégorie

- Publication de ports Docker Compose et Podman, mode de liaison, accès au fournisseur local de l'hôte, Bonjour, Tailscale et origines de l'interface de contrôle.
- Points de terminaison de santé des conteneurs, healthchecks Dockerfile/Compose, `openclaw health`, journaux et docs métriques/OTel.
- Exclut la sémantique générale du protocole Gateway non spécifique à l'hébergement de conteneurs.

## Fonctionnalités

- Docker Compose : publication de ports Docker Compose et Podman, mode de liaison, accès au fournisseur local de l'hôte, Bonjour, Tailscale et origines de l'interface de contrôle
- Points de terminaison de santé des conteneurs : points de terminaison de santé des conteneurs, healthchecks Dockerfile/Compose, openclaw health, journaux et docs métriques/OTel

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`
- Signaux positifs : la documentation Docker couvre les points de terminaison de santé, la santé profonde authentifiée, LAN par rapport à la boucle locale, les fournisseurs locaux de l'hôte, les paramètres par défaut de Bonjour, OTel, Prometheus, l'appairage de l'interface de contrôle et le dépannage des cibles Docker (`/Users/kevinlin/code/openclaw/docs/install/docker.md:162-228`, `/Users/kevinlin/code/openclaw/docs/install/docker.md:230-268`, `/Users/kevinlin/code/openclaw/docs/install/docker.md:532-553`). La documentation Podman couvre la publication de boucle locale et les conseils Tailscale (`/Users/kevinlin/code/openclaw/docs/install/podman.md:106-126`, `/Users/kevinlin/code/openclaw/docs/install/podman.md:172-192`). La source couvre les healthchecks Compose, la publication de ports, la synchronisation d'origine et la sélection de liaison de gateway.
- Signaux négatifs : le comportement du réseau des conteneurs diffère selon Docker Desktop, Linux Engine, Podman machine, macvlan, les proxies inverses VPS et les gestionnaires de fournisseurs ; pas toutes les variantes ont une preuve de scénario direct.
- Lacunes d'intégration : aucune matrice e2e unique ne prouve le contexte sécurisé de l'interface de contrôle, l'accès au fournisseur hôte, Tailscale, le démarrage à froid du healthcheck et la disponibilité au redémarrage sur Docker et Podman.

## Score de qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl : les preuves de requête incluent le problème #75701 / PR #75809 pour le comportement faux malsain du démarrage à froid du healthcheck, le problème #78136 pour healthz/readyz signalant OK pendant que la file d'attente se vide après le redémarrage de Docker, le problème #71493 / PR #71503 autour de `gateway.bind=lan` annonçant les IPs du bridge Docker et le problème #71669 / #32473 pour les frictions du contexte sécurisé de l'interface de contrôle.
- Rapports Discrawl : les preuves de requête incluent l'aide à l'installation Docker/VPS, les commentaires de bloqueur de version VPS faible spécification et les entrées Freshbits pour la gestion de l'interface bridge et le renforcement Podman/Docker.
- Bonnes qualités : la documentation sépare clairement les ports hôte publiés du mode de liaison des conteneurs, utilise des routes de métriques authentifiées, mappe les fournisseurs locaux de l'hôte et préfère la boucle locale/Tailscale géré par l'hôte pour Podman.
- Mauvaises qualités : la sémantique de santé/disponibilité et le comportement du contexte sécurisé/appairage sont toujours des pièges fréquents pour les opérateurs ; la gestion de l'interface bridge/virtuelle est suffisamment subtile pour avoir nécessité des correctifs basés sur les problèmes.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct et flux d'exécution.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Docker Compose, Points de terminaison de santé des conteneurs.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une carte de dépannage de mise en réseau des conteneurs du symptôme à l'hôte/runtime probable : DNS Docker Desktop, passerelle hôte Linux Engine, machine Podman, IP VPS brute, Tailscale, proxy inverse.
- Résoudre ou documenter les problèmes de période de démarrage du healthcheck Dockerfile et de disponibilité au redémarrage.
- Ajouter une fumée de version qui sonde l'authentification de l'appareil de l'interface de contrôle à partir du contexte du navigateur hôte, pas seulement `/healthz` et l'état CLI.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/install/docker.md:162-195` documente l'export OTel sortant et le scraping Prometheus authentifié.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:197-214` documente `/healthz`, `/readyz`, le healthcheck intégré et la santé profonde authentifiée.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:216-255` documente LAN par rapport à la boucle locale et `host.docker.internal` pour les fournisseurs locaux de l'hôte.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:257-268` documente les limitations Bonjour/mDNS dans la mise en réseau bridge Docker.
- `/Users/kevinlin/code/openclaw/docs/install/podman.md:106-126` recommande Tailscale géré par l'hôte pour Podman et les ports publiés de boucle locale.

### Source

- `/Users/kevinlin/code/openclaw/docker-compose.yml:53-90` mappe les fournisseurs locaux de l'hôte, supprime les capacités de mise en réseau, publie les ports, démarre la Gateway avec `--bind lan` et définit le healthcheck Compose.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:125-155` synchronise `gateway.mode`, `gateway.bind` et les origines autorisées de l'interface de contrôle pour Docker.
- `/Users/kevinlin/code/openclaw/scripts/run-openclaw-podman.sh:349-481` synchronise les origines locales de l'interface de contrôle pour la configuration Podman.
- `/Users/kevinlin/code/openclaw/scripts/run-openclaw-podman.sh:561-575` publie les ports gateway et bridge Podman sur l'interface hôte configurée et démarre la gateway.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/gateway-network-docker.sh` est la voie e2e de mise en réseau Docker.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:844-896` vérifie que les scénarios d'état de la voie Docker incluent les scénarios adjacents gateway/network et de mise à jour dans le plan.
- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:370-412` vérifie que la mise en réseau Docker au moment de la configuration évite le sidecar avant que la gateway n'existe et épingle les chemins env de configuration.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/shared/gateway-bind-url.test.ts` couvre la résolution d'URL `gateway.bind`.
- `/Users/kevinlin/code/openclaw/src/infra/container-environment.test.ts` couvre la détection de conteneur Docker/Podman/Kubernetes.
- `/Users/kevinlin/code/openclaw/src/dockerfile.test.ts:253-330` vérifie les modèles d'exécution et le comportement d'exécution Dockerfile.

### Requêtes Gitcrawl

Requête : `Docker HEALTHCHECK`

Résultats :

- Atteint le problème #75701 et PR #75809 pour le comportement faux malsain du démarrage à froid.
- Atteint le problème #78136 pour le redémarrage de la gateway Docker en processus laissant les files d'attente se vider tandis que healthz/readyz signalent OK.

Requête : `Docker VPS`

Résultats :

- Atteint le problème #71669 pour l'UX d'avertissement de connexion sécurisée et le problème #32473 pour le comportement du contexte sécurisé/identité de l'appareil Docker Hostinger VPS.
- Atteint le problème #53599 pour la régression du relais de navigateur affectant l'utilisation Docker/VPS à distance.

### Requêtes Discrawl

Requête : `Docker VPS`

Résultats :

- Trouvé une demande d'installation Docker Hetzner du 2026-05-28 où les problèmes Telegram et Gateway sont apparus lors des tests finaux.
- Trouvé un commentaire de bloqueur de version VPS faible spécification du 2026-05-27 et une discussion du mainteneur du 2026-05-23 sur la stratégie de repro Docker/VPS.

Requête : `Podman OpenClaw`

Résultats :

- Trouvé des références d'archive à l'utilisation de conteneur Podman et des mainteneurs discutant de la sélection de l'interface bridge/virtuelle dans les correctifs `gateway.bind=lan`.
