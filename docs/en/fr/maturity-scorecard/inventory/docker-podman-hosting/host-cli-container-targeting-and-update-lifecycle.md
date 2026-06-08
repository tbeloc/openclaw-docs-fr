---
title: "Docker / Podman hosting - Host CLI Container Targeting and Update Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Docker / Podman hosting - Host CLI Container Targeting and Update Lifecycle Maturity Note

## Résumé

Le ciblage Host CLI est implémenté via `openclaw --container` / `OPENCLAW_CONTAINER`, avec détection d'exécution sur Podman et Docker, nettoyage d'environnement, sécurité du proxy loopback et rejet explicite de `openclaw update` en mode ciblage conteneur. La couverture est bêta car le code et les tests unitaires couvrent le contrat de routage principal, et les canaux de version Docker couvrent les scénarios de mise à niveau, mais la documentation est plus claire pour Podman que pour Docker. La qualité est bêta car les archives montrent que la confusion du cycle de vie de mise à jour Docker reste courante.

## Portée de la catégorie

- Routage Host CLI dans les conteneurs Docker/Podman en cours d'exécution.
- Comportement de `--container` et `OPENCLAW_CONTAINER`, gestion de l'environnement, détection d'exécution ambiguë, garde du proxy loopback et commandes de mise à jour bloquées.
- Conseils de mise à jour/reconstruction/redémarrage de conteneur pour les hôtes Docker et Podman.
- Exclut le chemin de mise à jour npm/natif général d'OpenClaw en dehors des conteneurs.

## Fonctionnalités

- Routage Host CLI dans les conteneurs Docker/Podman en cours d'exécution : Routage Host CLI dans les conteneurs Docker/Podman en cours d'exécution
- Ciblage de conteneur : Couvre le ciblage de conteneur sur le routage Host CLI dans les conteneurs Docker/Podman en cours d'exécution. Comportement de `--container` et `OPENCLAW_CONTAINER`, gestion de l'environnement, détection d'exécution ambiguë, garde du proxy loopback et comportement de ciblage de conteneur host cli et cycle de vie de mise à jour associés.
- Conseils de mise à jour/reconstruction/redémarrage de conteneur pour Docker : Conseils de mise à jour/reconstruction/redémarrage de conteneur pour les hôtes Docker et Podman

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`
- Signaux positifs : La documentation Podman fait explicitement du Host CLI le plan de contrôle et montre `OPENCLAW_CONTAINER=openclaw`, `openclaw dashboard --no-open`, `openclaw gateway status --deep`, `openclaw doctor` et connexion au canal (`/Users/kevinlin/code/openclaw/docs/install/podman.md:12-15`, `/Users/kevinlin/code/openclaw/docs/install/podman.md:91-104`). La source implémente l'analyse des options racine, la détection d'exécution sur Podman/Docker, le nettoyage de l'environnement, la garde du proxy loopback et le blocage des mises à jour. Les tests couvrent la sémantique du routage de conteneur.
- Signaux négatifs : La documentation Docker s'appuie toujours davantage sur `docker compose run --rm openclaw-cli` que sur le Host CLI `--container`, donc l'abstraction partagée est documentée de manière inégale.
- Lacunes d'intégration : aucun test en direct/réel Docker/Podman ne prouve le routage Host CLI contre les conteneurs en cours d'exécution sur les deux exécutions et la messagerie du cycle de vie de mise à jour.

## Score de qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl : Les preuves de requête incluent les frictions de mise à jour Docker/VPS, le comportement de boucle de redémarrage du problème #86612 et le problème #39659 pour la gestion multi-instance de première classe pour les installations Docker.
- Rapports Discrawl : Les preuves de requête incluent les threads de mise à jour Hostinger/Docker où les utilisateurs ont essayé des chemins de mise à jour dans le conteneur ou via la console du fournisseur et les responsables ont clarifié les attentes de redéploiement d'image/gestionnaire de mise à jour.
- Bonnes qualités : le CLI empêche la classe la plus dangereuse de mise à jour erronée dans le conteneur en échouant `openclaw update` avec un message de reconstruction/redémarrage, supprime les remplacements d'authentification/environnement de la passerelle hôte et détecte les noms de conteneur ambigus sur Podman/Docker.
- Mauvaises qualités : la documentation orientée utilisateur et les flux de travail Docker gérés par le fournisseur ne donnent toujours pas une histoire unique et faisant autorité du cycle de vie de mise à jour pour chaque type d'installation de conteneur.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct et flux d'exécution.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl et preuves Discrawl couvrent la portée de la taxonomie pour le routage Host CLI dans les conteneurs Docker/Podman en cours d'exécution, le ciblage de conteneur, les conseils de mise à jour/reconstruction/redémarrage de conteneur pour Docker.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter la documentation Docker pour `openclaw --container <name>` parallèlement à la section Host CLI Podman.
- Ajouter une section de mise à jour de conteneur unique : extraction d'image GHCR/redéploiement, reconstruction/redémarrage de source, reconstruction/redémarrage d'image Podman et chemin de mise à jour géré par le fournisseur.
- Ajouter un test d'exécution qui affirme le message de mise à jour bloquée et le nettoyage de l'environnement Host CLI par rapport à un conteneur Docker/Podman réellement en cours d'exécution.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/podman.md:12-15` indique que le CLI `openclaw` hôte est le plan de contrôle et la gestion quotidienne utilise `openclaw --container`.
- `/Users/kevinlin/code/openclaw/docs/install/podman.md:91-104` documente `OPENCLAW_CONTAINER=openclaw` et les commandes Host CLI courantes.
- `/Users/kevinlin/code/openclaw/docs/install/podman.md:203-209` documente que `openclaw update` échoue avec `--container` et l'image doit être reconstruite/extraite puis redémarrée.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:140-148` documente les mises à jour Docker VM comme `git pull`, `docker compose build` et `docker compose up -d`.

### Source

- `/Users/kevinlin/code/openclaw/src/cli/container-target.ts:32-64` analyse `--container` et `OPENCLAW_CONTAINER`.
- `/Users/kevinlin/code/openclaw/src/cli/container-target.ts:81-127` recherche un conteneur en cours d'exécution sur Podman et Docker et rejette les noms ambigus.
- `/Users/kevinlin/code/openclaw/src/cli/container-target.ts:129-176` construit les arguments d'exécution de conteneur et rejette le `OPENCLAW_PROXY_URL` loopback sauf s'il est explicitement autorisé.
- `/Users/kevinlin/code/openclaw/src/cli/container-target.ts:216-230` supprime les remplacements d'authentification/environnement de profil/passerelle hôte des invocations ciblées par conteneur.
- `/Users/kevinlin/code/openclaw/src/cli/container-target.ts:232-282` bloque les commandes de mise à jour avec `openclaw update is not supported with --container; rebuild or restart the container image instead.`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:647-658` planifie la migration de mise à jour sur les lignes de base et les scénarios de nettoyage.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:844-896` mappe les scénarios d'état de la voie Docker `update-channel-switch` et `upgrade-survivor`.
- `/Users/keviewlin/code/openclaw/test/scripts/targeted-docker-lane-groups.test.ts:20-56` fragmente le survivant de mise à niveau publié par ligne de base.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/container-target.test.ts` couvre l'analyse de la cible de conteneur CLI, la sélection d'exécution, le dépouille de l'environnement, le rejet du proxy loopback, les noms ambigus et le blocage des mises à jour.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:560-658` couvre l'expansion du plan de survivant de mise à niveau et de migration de mise à jour.

### Requêtes Gitcrawl

Requête : `openclaw update --container rebuild restart container image`

Résultats :

- Atteint le problème #86612 avec le contexte de boucle de redémarrage Docker et la sortie de configuration sur la reconstruction avec `OPENCLAW_INSTALL_DOCKER_CLI`.
- Atteint le problème #7575 où la mise à jour/reconstruction du bac à sable Docker fait partie d'une proposition d'exécution sécurisée.

Requête : `Docker VPS`

Résultats :

- Atteint le problème #39659 pour la gestion multi-instance de première classe pour les installations Docker sur VPS/serveur.
- Atteint plusieurs problèmes Docker/VPS où la sémantique d'exécution et de mise à jour font partie du contexte de support utilisateur.

### Requêtes Discrawl

Requête : `Docker update VPS OpenClaw`

Résultats :

- Trouvé un thread Hostinger Docker du 2026-04-19 où le chemin correct a été décrit comme une mise à jour Docker Manager/fournisseur plutôt que de modifier `/usr/local/bin/openclaw` à l'intérieur du conteneur.
- Trouvé un thread d'échec de mise à jour Docker VPS du 2026-04-13 où les utilisateurs ont été conseillés de mettre à jour l'image GHCR et de redéployer.

Requête : `Podman OpenClaw`

Résultats :

- Trouvé des rapports d'utilisateurs sur l'opération de conteneur Podman, mais aucun thread de mise à jour Podman à haut volume dans les résultats supérieurs retournés.
