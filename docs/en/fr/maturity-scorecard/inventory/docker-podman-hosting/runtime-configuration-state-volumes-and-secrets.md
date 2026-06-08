---
title: "Hébergement Docker / Podman - Note de Maturité des Opérations de Conteneurs"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de Maturité des Opérations de Conteneurs

## Résumé

OpenClaw dispose de conseils substantiels en matière de persistance Docker/Podman et de garanties de sécurité des sources : Compose et Podman lient tous deux la configuration, l'espace de travail et l'état secret du profil d'authentification à des chemins d'hôte stables ; les scripts de configuration génèrent ou réutilisent les jetons de passerelle ; la configuration Docker pré-crée les répertoires et répare la propriété ; Podman applique les permissions de répertoire/fichier privé sans racine. La couverture est stable car la documentation et les tests exercent de nombreux chemins de persistance et de secrets. La qualité est bêta car les preuves d'archive montrent que la confusion de persistance et de mise à jour reste courante dans les environnements Docker et VPS hébergés.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Routage CLI d'hôte dans Docker/Podman en cours d'exécution : Routage CLI d'hôte dans les conteneurs Docker/Podman en cours d'exécution
- Ciblage de Conteneur : Couvre le Ciblage de Conteneur sur le routage CLI d'hôte dans les conteneurs Docker/Podman en cours d'exécution. Comportement de `--container` et `OPENCLAW_CONTAINER`, gestion de l'env, détection d'exécution ambiguë, garde de proxy de bouclage, et comportement de ciblage de conteneur CLI d'hôte et de cycle de vie de mise à jour associés.
- Conseils de mise à jour/reconstruction/redémarrage de conteneur pour Docker : Conseils de mise à jour/reconstruction/redémarrage de conteneur pour les hôtes Docker et Podman
- Docker Compose : Montages secrets de configuration/espace de travail/profil d'authentification Docker Compose et Podman
- Génération de jetons de passerelle : Génération de jetons de passerelle, réutilisation, persistance `.env`, et origines autorisées de l'interface utilisateur de contrôle
- Propriété : Propriété, permissions, comportement de montage SELinux, et survie d'état lors du remplacement de conteneur
- Docker Compose : Publication de ports Docker Compose et Podman, mode de liaison, accès au fournisseur local d'hôte, Bonjour, Tailscale, et origines de l'interface utilisateur de contrôle
- Points de terminaison de santé de conteneur : Points de terminaison de santé de conteneur, vérifications de santé Dockerfile/Compose, santé openclaw, journaux, et documentation des métriques/OTel
- Documentation Docker d'hébergement Fournisseur/VPS : Documentation Docker d'hébergement Fournisseur/VPS et runbooks opérationnels
- Conseils de persistance/mise à jour Docker VM : Conseils de persistance/mise à jour Docker VM, adjacence Hetzner/Hostinger/DigitalOcean, avertissements Kubernetes/conteneur, et exposition sécurisée
- Mise à jour orientée opérateur : Mise à jour orientée opérateur, sauvegarde, persistance, faible mémoire, et conseils de dépannage

## Fonctionnalités

- Routage CLI d'hôte dans Docker/Podman en cours d'exécution : Routage CLI d'hôte dans les conteneurs Docker/Podman en cours d'exécution
- Ciblage de Conteneur : Couvre le Ciblage de Conteneur sur le routage CLI d'hôte dans les conteneurs Docker/Podman en cours d'exécution. Comportement de `--container` et `OPENCLAW_CONTAINER`, gestion de l'env, détection d'exécution ambiguë, garde de proxy de bouclage, et comportement de ciblage de conteneur CLI d'hôte et de cycle de vie de mise à jour associés.
- Conseils de mise à jour/reconstruction/redémarrage de conteneur pour Docker : Conseils de mise à jour/reconstruction/redémarrage de conteneur pour les hôtes Docker et Podman
- Docker Compose : Montages secrets de configuration/espace de travail/profil d'authentification Docker Compose et Podman
- Génération de jetons de passerelle : Génération de jetons de passerelle, réutilisation, persistance `.env`, et origines autorisées de l'interface utilisateur de contrôle
- Propriété : Propriété, permissions, comportement de montage SELinux, et survie d'état lors du remplacement de conteneur
- Docker Compose : Publication de ports Docker Compose et Podman, mode de liaison, accès au fournisseur local d'hôte, Bonjour, Tailscale, et origines de l'interface utilisateur de contrôle
- Points de terminaison de santé de conteneur : Points de terminaison de santé de conteneur, vérifications de santé Dockerfile/Compose, santé openclaw, journaux, et documentation des métriques/OTel
- Documentation Docker d'hébergement Fournisseur/VPS : Documentation Docker d'hébergement Fournisseur/VPS et runbooks opérationnels
- Conseils de persistance/mise à jour Docker VM : Conseils de persistance/mise à jour Docker VM, adjacence Hetzner/Hostinger/DigitalOcean, avertissements Kubernetes/conteneur, et exposition sécurisée
- Mise à jour orientée opérateur : Mise à jour orientée opérateur, sauvegarde, persistance, faible mémoire, et conseils de dépannage

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs : La documentation Docker décrit les répertoires de configuration/espace de travail/secret de profil d'authentification montés par liaison, l'état du package de plugin installé, les points chauds de croissance de disque, les permissions/EACCES, et les tableaux de persistance VM (`/Users/kevinlin/code/openclaw/docs/install/docker.md:270-299`, `/Users/kevinlin/code/openclaw/docs/install/docker.md:382-396`, `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:120-139`). La documentation Podman décrit l'état d'hôte `~/.openclaw`, `.env`, l'espace de travail, le jeton, et les montages de liaison (`/Users/kevinlin/code/openclaw/docs/install/podman.md:155-192`). La source implémente l'épinglage de chemin, la gestion des fichiers de jeton, les montages de volume, la réparation de propriété, les vérifications de chemin privé, et les options de montage SELinux.
- Signaux négatifs : la couverture ne prouve pas que tous les gestionnaires Docker hébergés préservent les chemins de montage attendus, et la documentation laisse certaines sémantiques de persistance spécifiques au fournisseur aux plates-formes externes.
- Lacunes d'intégration : aucun scénario de persistance Docker hébergé récurrent ne prouve la suppression de clé API, les profils d'authentification, les racines de package de plugin, les fichiers d'espace de travail, et `.env` lors du redémarrage/recréation pour les déploiements de style Hostinger/Coolify.

## Score de Qualité

- Score : `Bêta (74%)`
- Rapports Gitcrawl : Les preuves de requête incluent le problème #86612 pour le comportement de boucle de redémarrage avec le bac à sable Docker et les chemins d'hôte `/mnt/...`, le problème #53628 pour la gestion XDG config dans une installation Docker Hetzner, et les résultats Docker/VPS autour de la persistance, de la mise à jour, et de la confusion du fournisseur.
- Rapports Discrawl : Les preuves de requête incluent les messages Docker Hostinger où les clés API/paramètres UI ont été retournés après redémarrage en raison de credentials sauvegardés par env ou de persistance `/home/node/.openclaw` manquante suspectée, et un thread de mise à jour Docker VPS où les utilisateurs ont été invités à mettre à jour les images/redéployer plutôt que d'exécuter la mise à jour dans le conteneur.
- Bonnes qualités : La configuration Docker sépare les clés secrètes du profil d'authentification de la configuration OpenClaw, pré-crée les répertoires d'agent/session, utilise les montages de liaison d'hôte, chowns uniquement l'état monté limité, et évite d'imprimer les jetons de passerelle. Les scripts Podman exigent l'exécution sans racine, les répertoires privés possédés, et les permissions `.env` réservées au propriétaire.
- Mauvaises qualités : le contrat de persistance est techniquement correct mais facile à violer dans Docker géré par fournisseur, Compose personnalisé, ou les configurations de mismatch racine/utilisateur.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct, et flux d'exécution.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : la documentation archivée, la source, le test, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour le Routage CLI d'hôte dans Docker/Podman en cours d'exécution, le Ciblage de Conteneur, les Conseils de mise à jour/reconstruction/redémarrage de conteneur pour Docker, Docker Compose, la Génération de jetons de passerelle, la Propriété, Docker Compose, les Points de terminaison de santé de conteneur, la Documentation Docker d'hébergement Fournisseur/VPS, les Conseils de persistance/mise à jour Docker VM, la Mise à jour orientée opérateur.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une liste de contrôle de persistance Docker hébergée qui nomme `openclaw.json`, `.env`, les profils d'authentification, le répertoire de clé de profil d'authentification, les racines de plugin, les sessions, et les fichiers d'espace de travail.
- Ajouter un appel "ne pas exécuter la mise à jour à l'intérieur du conteneur" Docker/Podman à côté de la documentation de persistance.
- Enregistrer une preuve de redémarrage/recréation récurrente que la suppression de clé API et les modifications de configuration survivent au cycle de vie Docker hébergé attendu.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/install/docker.md:270-299` documente l'état Docker monté, le stockage de clé de profil d'authentification, l'état du package de plugin, et les points chauds de croissance de disque.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:382-396` documente les exigences de propriété uid 1000 et les avertissements de propriété de plugin.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:120-139` mappe l'état Docker de longue durée par rapport à l'état de conteneur/image éphémère.
- `/Users/kevinlin/code/openclaw/docs/install/podman.md:155-192` documente la configuration Podman, l'espace de travail, le jeton, les montages de liaison, les origines autorisées, et le comportement du fichier env Quadlet.

### Source

- `/Users/kevinlin/code/openclaw/docker-compose.yml:12-44` épingle les chemins d'état/configuration/espace de travail côté conteneur et monte par liaison la configuration, l'espace de travail, et les répertoires secrets de profil d'authentification.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:59-123` lit les jetons de passerelle à partir de la configuration ou `.env`.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:264-320` initialise les répertoires secrets d'hôte configuration/espace de travail/authentification et exporte les chemins de configuration Docker.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:557-573` répare la propriété du répertoire de données monté par liaison sans traverser les limites de montage d'espace de travail.
- `/Users/kevinlin/code/openclaw/scripts/run-openclaw-podman.sh:161-195` lit une liste d'autorisation Podman `.env` restreinte après validation des permissions de fichier et répertoire réservées au propriétaire.
- `/Users/kevinlin/code/openclaw/scripts/run-openclaw-podman.sh:491-575` crée/réutilise le jeton/configuration, synchronise les origines, applique les options de montage SELinux, et monte par liaison la configuration/espace de travail dans les conteneurs de configuration et de passerelle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:262-301` vérifie la persistance env Docker, la configuration du volume d'accueil, la suppression de jeton, et la synchronisation de configuration.
- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:439-511` vérifie les répertoires d'identité de configuration, les répertoires d'agent/session, la séparation du répertoire secret de profil d'authentification, et la réparation de propriété limitée.
- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:513-565` vérifie le comportement de réutilisation de jeton de configuration et `.env`.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/config/config.sandbox-docker.test.ts` couvre le comportement de configuration de bac à sable lié à Docker.
- `/Users/kevinlin/code/openclaw/src/security/audit-sandbox-docker-config.test.ts` couvre le comportement d'audit de sécurité du bac à sable Docker.
- `/Users/kevinlin/code/openclaw/src/infra/container-environment.test.ts` couvre la détection d'environnement de conteneur.

### Requêtes Gitcrawl

Requête : `Docker volume EACCES OPENCLAW_WORKSPACE_DIR OPENCLAW_CONFIG_DIR`

Résultats :

- Atteint le problème #86612 pour la boucle de redémarrage de passerelle Docker impliquant `OPENCLAW_CONFIG_DIR`, `OPENCLAW_WORKSPACE_DIR`, le mode bac à sable, et les chemins d'hôte `/mnt/...`.

Requête : `Docker VPS`

Résultats :

- Atteint le problème #53628 pour la gestion de `${XDG_CONFIG_HOME}` dans une installation Docker Hetzner.
- Atteint le problème #32473 pour le comportement d'identité de contexte sécurisé/appareil Docker Hostinger VPS.

### Requêtes Discrawl

Requête : `Docker update VPS OpenClaw`

Résultats :

- Trouvé un thread Docker Hostinger du 2026-04-19 où les clés API/paramètres ont été retournés après redémarrage, avec des causes suspectées incluant les credentials sauvegardés par env ou la persistance `/home/node/.openclaw` manquante.
- Trouvé un thread d'échec de mise à jour Docker VPS du 2026-04-13 où les utilisateurs ont discuté de la mise à jour de l'image GHCR/redéploiement plutôt que de modifier le Dockerfile ou de mettre à jour à l'intérieur du conteneur.

Requête : `Docker VPS`

Résultats :

- Trouvé une demande d'aide d'installation Docker Hetzner du 2026-05-28 et une discussion de mise à jour Docker VPS du 2026-05-23, montrant que les conseils de persistance/mise à jour restent un terrain de support actif.
