---
title: "Hébergement Docker / Podman - Note de maturité des runbooks VPS hébergés par le fournisseur et de l'opérateur"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de maturité des runbooks VPS hébergés par le fournisseur et de l'opérateur

## Résumé

L'utilisation de Docker/VPS hébergés par le fournisseur est bien représentée dans la documentation via le runtime Docker VM, Hetzner, Hostinger, DigitalOcean, Kubernetes et les conseils VPS génériques. La couverture est bêta car la documentation est large et pratique, et la source supporte les primitives Docker requises, mais la preuve de scénario est plus faible sur les gestionnaires spécifiques aux fournisseurs. La qualité est à la limite bêta/alpha car les preuves d'archive montrent une confusion active de l'opérateur autour des mises à jour Hostinger/Coolify, des contextes sécurisés de l'interface de contrôle, de la configuration Telegram/Gateway, de l'état persistant et du comportement des VPS bas de gamme.

## Portée de la catégorie

- Documentation d'hébergement Docker VPS/fournisseur et runbooks opérationnels.
- Conseils de persistance/mise à jour Docker VM, adjacence Hetzner/Hostinger/DigitalOcean, avertissements Kubernetes/conteneur et exposition sécurisée.
- Conseils opérationnels de mise à jour, sauvegarde, persistance, faible mémoire et dépannage.
- Exclut l'hébergement natif Gateway systemd Linux sauf où la documentation le compare à Docker.

## Fonctionnalités

- Documentation d'hébergement Docker VPS/fournisseur : Documentation d'hébergement Docker VPS/fournisseur et runbooks opérationnels
- Conseils de persistance/mise à jour Docker VM : Conseils de persistance/mise à jour Docker VM, adjacence Hetzner/Hostinger/DigitalOcean, avertissements Kubernetes/conteneur et exposition sécurisée
- Mise à jour opérationnelle : Mise à jour opérationnelle, sauvegarde, persistance, faible mémoire et conseils de dépannage

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`
- Signaux positifs : La documentation Docker oriente les utilisateurs VPS vers la documentation Hetzner et Docker VM Runtime (`/Users/kevinlin/code/openclaw/docs/install/docker.md:458-462`). Docker VM Runtime couvre la cuisson binaire, la construction/lancement, le tableau de persistance et les mises à jour (`/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:11-148`). La notation de l'hôte Linux a déjà trouvé une documentation VPS/conteneur/cloud plus large dans `docs/vps.md`, `docs/install/hetzner.md`, `docs/install/digitalocean.md`, `docs/install/kubernetes.md` et `docs/install/podman.md`.
- Signaux négatifs : Les gestionnaires Docker spécifiques aux fournisseurs et les hôtes en un clic sont opérationnellement différents de la source Compose, et la ligne de la fiche d'évaluation dit explicitement que la promotion nécessite une fumée de version récurrente pour le comportement de mise à niveau et de volume.
- Lacunes d'intégration : aucune fumée soutenue par le fournisseur ne capture la mise à jour Docker Hostinger/Coolify/Hetzner plus le comportement de persistance de bout en bout.

## Score de qualité

- Score : `Bêta (70%)`
- Rapports Gitcrawl : Les preuves de requête incluent le problème #32473 pour le contexte sécurisé Hostinger Docker/identité de l'appareil, #71669 pour l'UX d'avertissement, #39659 pour la gestion multi-instance Docker, #53628 pour XDG config dans Hetzner Docker, #53599 pour la régression du relais navigateur Docker/VPS, #53600 pour les performances VPS contraintes et #75827 pour la balise `main` GHCR obsolète.
- Rapports Discrawl : Les preuves de requête incluent l'aide récente d'installation Hetzner Docker, les problèmes de mise à jour/persistance Hostinger Docker, les questions de mise à niveau Docker VPS, la confusion de mise à jour du vieux conteneur Coolify/OpenClaw et les commentaires de bloqueur de version VPS bas de gamme.
- Bonnes qualités : la documentation indique aux opérateurs de cuire les binaires, de persister l'état en dehors des conteneurs, de reconstruire/redémarrer les images pour les mises à jour, de sécuriser l'accès Gateway exposé et d'éviter les installations à l'exécution.
- Mauvaises qualités : Docker hébergé par le fournisseur reste une surface lourde en support avec de nombreuses formes de déploiement que la documentation ne peut pas entièrement normaliser.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct et flux d'exécution.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la documentation d'hébergement Docker VPS/fournisseur, les conseils de persistance/mise à jour Docker VM, la mise à jour opérationnelle.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des runbooks Docker spécifiques au fournisseur pour Hostinger/Coolify/Hetzner qui nomment les chemins de mise à jour pris en charge, les emplacements de persistance et les exigences de contexte sécurisé du proxy inverse.
- Ajouter une fumée récurrente pour la mise à niveau de l'image Docker plus la persistance du volume dans un environnement en forme de VM.
- Ajouter une liste de contrôle de l'opérateur pour « est-ce un problème Docker, un problème VPS, un problème de gestionnaire de fournisseur ou un problème de configuration OpenClaw ? »

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/install/docker.md:458-462` oriente les utilisateurs Docker VPS vers Hetzner et Docker VM Runtime.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:11-31` avertit que les binaires installés à l'exécution sont perdus au redémarrage.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:82-118` documente la construction/lancement, OOM pendant la construction, la vérification binaire et les journaux Gateway.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:120-148` documente le flux de persistance d'état et de mise à jour.
- `/Users/kevinlin/code/openclaw/docs/install/hetzner.md` documente la configuration Hetzner Docker VPS.
- `/Users/kevinlin/code/openclaw/docs/install/hostinger.md` et `/Users/kevinlin/code/openclaw/docs/install/kubernetes.md` couvrent les chemins de déploiement hébergés/conteneur adjacents.

### Source

- `/Users/kevinlin/code/openclaw/docker-compose.yml:41-68` fournit la persistance Compose de base et la forme de port que la documentation du fournisseur peut adapter.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:538-555` construit ou extrait l'image demandée.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:557-619` corrige les permissions du répertoire de données, exécute l'intégration, synchronise la configuration et démarre la passerelle.
- `/Users/kevinlin/code/openclaw/scripts/lib/docker-build.sh:88-125` enveloppe les constructions Docker avec les tentatives BuildKit et la gestion des délais d'expiration.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:647-658` vérifie l'expansion du scénario/ligne de base de migration de mise à jour.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:898-925` mappe l'installation E2E aux voies d'installation de package spécifiques au fournisseur.
- `/Users/kevinlin/code/openclaw/test/scripts/targeted-docker-lane-groups.test.ts:20-56` fragmente le survivant de mise à niveau publié par ligne de base pour les exécutions ciblées.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/test/scripts/docker-build-helper.test.ts` vérifie le comportement du helper de construction Docker, les délais d'expiration, le nettoyage et les montages de package.
- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` vérifie le câblage du flux de travail de package/version Docker.

### Requêtes Gitcrawl

Requête : `Docker VPS`

Résultats :

- Atteint les problèmes #71669, #39659, #32473, #53628, #53599, #53600, #64293, #83960, #60827, #57713 et autres threads de support et de régression liés à Docker/VPS.

Requête : `Hostinger Docker`

Résultats :

- Atteint le problème #32473 pour le comportement du contexte sécurisé Hostinger VPS Docker Control UI/identité de l'appareil.

### Requêtes Discrawl

Requête : `Docker VPS`

Résultats :

- Trouvé une demande d'aide d'installation Hetzner Docker du 2026-05-28.
- Trouvé une question de mise à jour Docker VPS du 2026-05-23.
- Trouvé un utilisateur Coolify/Docker du 2026-04-22 posant des questions sur les anciens problèmes de mise à jour du conteneur OpenClaw.

Requête : `Docker update VPS OpenClaw`

Résultats :

- Trouvé un fil Hostinger Docker du 2026-04-19 avec des problèmes de mise à jour et de persistance et des conseils sur les chemins de mise à jour du gestionnaire Docker/fournisseur.
