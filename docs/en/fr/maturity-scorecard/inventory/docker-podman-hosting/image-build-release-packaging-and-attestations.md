---
title: "Hébergement Docker / Podman - Note de Maturité de la Validation et de la Publication d'Images"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de Maturité de la Validation et de la Publication d'Images

## Résumé

Le pipeline officiel d'images Docker est l'une des parties les plus solides de la surface : le Dockerfile est multi-étapes, avec digests épinglés, sans root, orienté BuildKit, et les workflows de publication publient des manifestes amd64, arm64, slim, browser et multi-plateforme avec des vérifications d'attestation SBOM/provenance. La couverture est stable car les preuves de source, de workflow et de test exercent tous le pipeline. La qualité reste à la limite bêta/stable car les preuves d'archive montrent une balise `main` obsolète et des problèmes de démarrage à froid du healthcheck qui affectent la confiance des opérateurs dans les images publiées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Étapes de construction du Dockerfile racine : Étapes de construction du Dockerfile racine, contenu de l'image d'exécution, arguments de construction optionnels pour le navigateur et Docker CLI
- Workflow de publication Docker : Workflow de publication Docker pour la publication GHCR, les balises multi-arch, les manifestes et la vérification d'attestation
- Génération d'artefacts de package Docker E2E : Génération d'artefacts de package Docker E2E et assistants de construction partagés
- Scripts de plan/planificateur Docker E2E : Scripts de plan/planificateur Docker E2E, métadonnées de voie, regroupement ciblé, génération d'artefacts de package et action d'hydratation GitHub
- Installation du chemin de publication : Installation du chemin de publication, mise à jour, scénarios de survie de mise à niveau, fournisseur en direct, plugin, Open WebUI et planification du nettoyage

## Fonctionnalités

- Étapes de construction du Dockerfile racine : Étapes de construction du Dockerfile racine, contenu de l'image d'exécution, arguments de construction optionnels pour le navigateur et Docker CLI
- Workflow de publication Docker : Workflow de publication Docker pour la publication GHCR, les balises multi-arch, les manifestes et la vérification d'attestation
- Génération d'artefacts de package Docker E2E : Génération d'artefacts de package Docker E2E et assistants de construction partagés
- Scripts de plan/planificateur Docker E2E : Scripts de plan/planificateur Docker E2E, métadonnées de voie, regroupement ciblé, génération d'artefacts de package et action d'hydratation GitHub
- Installation du chemin de publication : Installation du chemin de publication, mise à jour, scénarios de survie de mise à niveau, fournisseur en direct, plugin, Open WebUI et planification du nettoyage

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (86%)`
- Signaux positifs : La couverture du Dockerfile inclut les images de base avec digests épinglés, les copies de manifeste optimisées, les montages de cache BuildKit, l'élagage de production, les arguments de construction optionnels pour le navigateur et Docker CLI, les répertoires d'état pré-créés, l'exécution sans root, `tini`, et le healthcheck intégré (`/Users/kevinlin/code/openclaw/Dockerfile:10-24`, `/Users/kevinlin/code/openclaw/Dockerfile:70-142`, `/Users/kevinlin/code/openclaw/Dockerfile:236-330`). Le workflow de publication Docker construit des images amd64 et arm64, des variantes de navigateur, des manifestes et des vérifications d'attestation (`/Users/kevinlin/code/openclaw/.github/workflows/docker-release.yml:156-192`, `/Users/kevinlin/code/openclaw/.github/workflows/docker-release.yml:347-383`, `/Users/kevinlin/code/openclaw/.github/workflows/docker-release.yml:517-654`).
- Signaux négatifs : la couverture de construction/publication est principalement une preuve de pipeline CI et statique ; elle ne prouve pas que chaque dépendance d'exécution installée par les arguments de construction fournis par l'utilisateur.
- Lacunes d'intégration : aucun rapport unique ne lie chaque politique de balise GHCR, variante d'image, actualisation de digest de base, attestation et résultat de fumée post-publication ensemble pour les opérateurs.

## Score de Qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : Les preuves de requête incluent le problème #75827 pour une balise Docker `ghcr.io/openclaw/openclaw:main` obsolète, les problèmes #75701 et PR #75809 pour le comportement faux malsain au démarrage à froid `HEALTHCHECK --start-period=15s`, et PR #87508 pour le filtrage de matrice du workflow de publication.
- Rapports Discrawl : Les preuves de requête incluent les entrées Freshbits pour les correctifs de package de publication et de construction Podman/Docker, plus une discussion de fumée de publication/mise à niveau clarifiant que la fumée de mise à niveau existe mais n'était pas une liste de contrôle nommée.
- Bonnes qualités : les constructions de publication utilisent des actions Docker épinglées, des images de base avec digests épinglés, la publication multi-plateforme, des variantes de navigateur explicites, SBOM/provenance, la vérification d'attestation et des outils d'artefacts de package dédiés.
- Mauvaises qualités : la fraîcheur de l'image `main` et le comportement du healthcheck ont des rapports d'archive ouverts ; ceux-ci sont visibles par les opérateurs car ils affectent la sémantique "extraire la dernière image" et la santé d'orchestration.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct et flux d'exécution.

## Score de Complétude

- Score : `Stable (86%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les étapes de construction du Dockerfile racine, le workflow de publication Docker, la génération d'artefacts de package Docker E2E, les scripts de plan/planificateur Docker E2E, l'installation du chemin de publication.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par les opérateurs.

## Lacunes Connues

- Publier un contrat compact de publication d'image Docker couvrant la sémantique exacte des balises pour `latest`, `main`, version, `slim`, navigateur, amd64, arm64 et remplissage manuel.
- Résoudre ou documenter explicitement le problème du démarrage à froid du healthcheck du Dockerfile pour les hôtes et les orchestrateurs.
- Ajouter un résumé d'artefact de publication visible pour la vérification d'attestation et les résultats de fumée d'image.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/docker.md:36-45` documente l'utilisation des images GHCR pré-construites et des balises courantes.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:146-154` documente les arguments de construction apt et de package Python au moment de l'image.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:449-454` documente les métadonnées de l'image de base et l'actualisation du digest Dependabot.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:11-31` explique que les binaires externes requis doivent être intégrés aux images, puis reconstruits/redémarrés en cas de modification.

### Source

- `/Users/kevinlin/code/openclaw/Dockerfile:10-24` épingle les digests de l'image de base Node et Bun et explique l'actualisation de base.
- `/Users/kevinlin/code/openclaw/Dockerfile:70-142` utilise les montages de cache BuildKit, les paramètres d'installation/élagage d'architecture cible et l'élagage des dépendances de production.
- `/Users/kevinlin/code/openclaw/Dockerfile:167-208` installe les utilitaires système d'exécution, copie les actifs d'exécution et prépare pnpm/Corepack pour une utilisation sans root.
- `/Users/kevinlin/code/openclaw/Dockerfile:236-330` supporte les arguments de construction optionnels pour le navigateur/Docker CLI, crée des répertoires d'état appartenant à node, s'exécute en tant que `node`, et définit le healthcheck OCI.
- `/Users/kevinlin/code/openclaw/.github/workflows/docker-release.yml:156-192` construit/pousse les images amd64 normales et de navigateur avec SBOM et provenance.
- `/Users/kevinlin/code/openclaw/.github/workflows/docker-release.yml:347-383` construit/pousse les images arm64 normales et de navigateur avec SBOM et provenance.
- `/Users/kevinlin/code/openclaw/.github/workflows/docker-release.yml:517-654` crée des manifestes multi-plateforme et vérifie les attestations Docker.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/docker-build-helper.test.ts:106-132` vérifie le routage de construction BuildKit et l'utilisation de l'assistant de script de construction partagé.
- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts:235-296` vérifie le câblage du package Docker E2E et du workflow de survie de mise à niveau publié.
- `/Users/kevinlin/code/openclaw/test/scripts/verify-docker-attestations.test.ts:54-133` vérifie la résolution d'attestation d'index d'image et le rapport SBOM/provenance manquant.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/dockerfile.test.ts:30-115` vérifie les étapes d'exécution bookworm/slim, CA/Python/tini, les dépendances optionnelles du navigateur et les paramètres d'installation/élagage de plateforme cible.
- `/Users/kevinlin/code/openclaw/src/dockerfile.test.ts:117-251` vérifie les vérifications de modules natifs, les manifestes d'installation, la copie de scripts de cycle de vie, les commandes de construction, l'élagage et les copies d'actifs d'exécution.
- `/Users/kevinlin/code/openclaw/src/docker-image-digests.test.ts:125-148` vérifie que les images de base du Dockerfile sélectionnées sont épinglées aux digests sha256 et que les mises à jour Docker Dependabot restent activées.

### Requêtes Gitcrawl

Requête : `Docker release ghcr image main latest`

Résultats :

- Atteint le problème #75827, `ghcr.io/openclaw/openclaw:main Docker tag is not auto-rebuilt on commits to git main; stale by weeks`.
- Atteint le problème #75701 pour les images `latest`, `main` et version actuelles affectées par le comportement du healthcheck au démarrage à froid.

Requête : `Docker HEALTHCHECK`

Résultats :

- Atteint le problème #75701 et PR #75809 sur le comportement faux malsain au démarrage à froid `HEALTHCHECK --start-period=15s`.
- Atteint le problème #78136 sur le redémarrage en processus Docker laissant les files d'attente se vider tandis que les points de terminaison de santé signalent OK.

### Requêtes Discrawl

Requête : `Docker E2E release upgrade survivor`

Résultats :

- Trouvé une discussion du 2026-05-02 clarifiant que la machinerie explicite de fumée de publication/mise à niveau existe, incluant la fumée d'installation, les voies fraîches et de mise à niveau multi-OS, et `scripts/e2e/upgrade-survivor-docker.sh`.

Requête : `Podman OpenClaw`

Résultats :

- Trouvé les entrées Freshbits pour `fix(ci): build complete release package artifacts` et le câblage des arguments de construction Podman, montrant que le durcissement de la publication/construction était actif dans l'archive.
