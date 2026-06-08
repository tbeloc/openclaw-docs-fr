---
title: "Hébergement Docker / Podman - Note de Maturité de Configuration de Conteneur"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de Maturité de Configuration de Conteneur

## Résumé

Le chemin de première exécution Docker est documenté et implémenté autour de `scripts/docker/setup.sh`, `docker-compose.yml`, intégration automatique, génération/réutilisation de jetons, écritures de configuration pré-démarrage et accès hôte à l'interface de contrôle. La couverture est stable car le flux de configuration dispose de tests e2e ciblés plus une large réutilisation de voies de version Docker. La qualité reste bêta car les preuves d'archive montrent toujours une confusion de configuration Docker autour du mode sandbox, des fuites de chemins hôte, des vérifications de santé, des contextes sécurisés et des attentes de mise à jour VPS/fournisseur.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Script de Configuration d'Image Locale : Couvre le script de configuration d'image locale sur `./scripts/docker/setup.sh` configuration d'image locale et d'image GHCR. Forme de passerelle Docker Compose et CLI sidecar. Intégration automatique de première exécution, gestion des jetons, défauts de liaison/origine et commandes de configuration de canal post-démarrage. Notes de première exécution Docker uniquement et comportement de configuration de première exécution, installation et composition associés.
- Passerelle Docker Compose : Forme de passerelle Docker Compose et CLI sidecar
- Intégration automatique de première exécution : Intégration automatique de première exécution, gestion des jetons, défauts de liaison/origine et commandes de configuration de canal post-démarrage
- Notes de première exécution Docker uniquement : Notes de première exécution Docker uniquement, excluant la configuration Podman sans racine et les internals du protocole Gateway général
- Scripts de configuration Podman et modèle Quadlet : Docs de configuration Podman, scripts/podman/setup.sh, scripts/run-openclaw-podman.sh et scripts/podman/openclaw.container.in
- Configuration d'image Podman sans racine : Configuration d'image Podman sans racine, lancement, configuration/intégration, routage CLI hôte, démarrage automatique Quadlet et vérifications de propriétaire/permission

## Fonctionnalités

- Script de Configuration d'Image Locale : Couvre le script de configuration d'image locale sur `./scripts/docker/setup.sh` configuration d'image locale et d'image GHCR. Forme de passerelle Docker Compose et CLI sidecar. Intégration automatique de première exécution, gestion des jetons, défauts de liaison/origine et commandes de configuration de canal post-démarrage. Notes de première exécution Docker uniquement et comportement de configuration de première exécution, installation et composition associés.
- Passerelle Docker Compose : Forme de passerelle Docker Compose et CLI sidecar
- Intégration automatique de première exécution : Intégration automatique de première exécution, gestion des jetons, défauts de liaison/origine et commandes de configuration de canal post-démarrage
- Notes de première exécution Docker uniquement : Notes de première exécution Docker uniquement, excluant la configuration Podman sans racine et les internals du protocole Gateway général
- Scripts de configuration Podman et modèle Quadlet : Docs de configuration Podman, scripts/podman/setup.sh, scripts/run-openclaw-podman.sh et scripts/podman/openclaw.container.in
- Configuration d'image Podman sans racine : Configuration d'image Podman sans racine, lancement, configuration/intégration, routage CLI hôte, démarrage automatique Quadlet et vérifications de propriétaire/permission

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (84%)`
- Signaux positifs : La documentation Docker couvre les prérequis, la construction/extraction, l'intégration automatique, l'accès à l'interface de contrôle, l'utilisation du CLI sidecar, la configuration de canal, la configuration manuelle, les variables d'environnement, les sondes de santé et le dépannage (`/Users/kevinlin/code/openclaw/docs/install/docker.md:17-228`, `/Users/kevinlin/code/openclaw/docs/install/docker.md:506-554`). `scripts/docker/setup.sh` implémente les vérifications de dépendances, la réutilisation/génération de jetons, l'épinglage d'environnement CLI pré-démarrage, l'intégration, la synchronisation de configuration et le démarrage de passerelle (`/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:245-362`, `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:575-619`). `src/docker-setup.e2e.test.ts` vérifie les montages de volume d'accueil, les arguments de construction, la rédaction de jetons, l'intégration pré-démarrage, les répertoires pré-créés, le repli sandbox et l'épinglage de chemin de configuration (`/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:262-620`).
- Signaux négatifs : la couverture est la plus forte pour l'assistant Compose supporté, mais plus mince pour les variantes Compose non gérées, les wrappers Docker hébergés par fournisseur et les gestionnaires Docker GUI.
- Lacunes d'intégration : les preuves de version prouvent de nombreuses voies Docker via le planificateur, mais il n'y a pas de matrice de scénario de première exécution récurrente pour Docker Desktop, Linux Engine, les wrappers de style Hostinger/Coolify et Compose activé sandbox dans le même artefact.

## Score de Qualité

- Score : `Bêta (76%)`
- Rapports Gitcrawl : Les preuves de requête incluent le problème ouvert #86612 pour une boucle de redémarrage de passerelle Docker avec `OPENCLAW_SANDBOX=1` et chemins hôte `/mnt/...`, les problèmes #71669 et #32473 pour le rejet de contexte sécurisé de l'interface de contrôle sur Docker/VPS et le problème #75701 / PR #75809 pour le comportement de démarrage à froid du healthcheck Dockerfile.
- Rapports Discrawl : Les preuves de requête incluent une demande d'aide d'installation Docker Hetzner du 2026-05-28 où la configuration de Telegram et Gateway a échoué, une discussion de mainteneur du 2026-05-23 sur la pratique de repro Docker/VPS et les entrées Freshbits pour l'ajout de configuration Docker `OPENCLAW_SKIP_ONBOARDING`.
- Bonnes qualités : le script de première exécution valide les montages, évite d'utiliser `openclaw-cli` avant l'existence du conteneur de passerelle, supprime l'impression de jetons, épingle les chemins d'état côté conteneur et répare la propriété de montage de liaison avant l'intégration.
- Mauvaises qualités : le chemin supporté s'attend toujours à ce que les opérateurs comprennent la mise en réseau hôte Docker, l'état monté, les risques de socket sandbox et le comportement de mise à jour spécifique au fournisseur ; les preuves d'archive montrent que ces domaines sont des sources de support actives.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct et flux d'exécution.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour Script de Configuration d'Image Locale, Passerelle Docker Compose, Intégration automatique de première exécution, Notes de première exécution Docker uniquement, Scripts de configuration Podman et modèle Quadlet, Configuration d'image Podman sans racine.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de version de processus 3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une matrice de support de première exécution qui sépare Docker Engine, Docker Desktop, les wrappers Hostinger/Coolify et la configuration Docker activée sandbox.
- Publier un court avertissement "Chemin de mise à jour Docker" près de la configuration de première exécution afin que les utilisateurs n'exécutent pas `openclaw update` à l'intérieur des conteneurs recréés.
- Capturer la fumée de version récurrente pour la première exécution Docker avec et sans `OPENCLAW_SKIP_ONBOARDING`, `OPENCLAW_HOME_VOLUME` et sandbox activé.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/docker.md:17-94` documente les prérequis Docker, le script de configuration, l'option d'image pré-construite, l'intégration, l'entrée de jeton de l'interface de contrôle et les commandes de configuration de canal.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:96-145` documente la configuration manuelle de Docker Compose et les variables d'environnement de configuration.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:216-228` explique le comportement de liaison Docker LAN par rapport à loopback.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:532-553` documente l'appairage et le dépannage de cible Docker.

### Source

- `/Users/kevinlin/code/openclaw/docker-compose.yml:1-129` définit le service `openclaw-gateway`, le sidecar `openclaw-cli`, les montages d'état/config/workspace, l'espace de noms réseau partagé, les options de sécurité, les ports, la commande et le healthcheck.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:245-362` valide Docker/Compose, les chemins de montage, le socket sandbox, le fuseau horaire, les répertoires d'état, la réutilisation/génération de jetons et les exports d'env de configuration.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:575-619` exécute l'intégration via le conteneur de passerelle, synchronise la configuration de passerelle, imprime les commandes de configuration de canal et démarre la passerelle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:262-301` vérifie les défauts d'env, les montages de volume d'accueil, les arguments de construction, la suppression de jetons, l'intégration pré-démarrage et la synchronisation de configuration.
- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:370-412` vérifie que le script de configuration évite le CLI réseau partagé avant le démarrage de la passerelle et épingle les chemins d'état de configuration au moment de la configuration à l'intérieur du conteneur.
- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:439-620` vérifie la création de répertoire d'identité, la persistance du fuseau horaire, les répertoires d'agent, le répertoire secret du profil d'authentification, la réutilisation de jetons, la désactivation sandbox et le comportement de repli sandbox.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/dockerfile.test.ts:22-94` vérifie la forme de base/runtime Dockerfile, les utilitaires runtime, l'installation optionnelle du navigateur et l'ordre de construction.
- `/Users/kevinlin/code/openclaw/src/docker-image-digests.test.ts:125-148` vérifie les images de base Docker épinglées par digest et les mises à jour Docker Dependabot.

### Requêtes Gitcrawl

Requête : `Docker setup OPENCLAW_SKIP_ONBOARDING OPENCLAW_HOME_VOLUME`

Résultats :

- Problème ouvert #86612 trouvé, `Boucle de redémarrage du conteneur de passerelle Docker quand OPENCLAW_SANDBOX=1 et OPENCLAW_HOME=/mnt/...`.
- PR ouverte #61464 trouvée, `Docker: ajouter des assistants de migration Mac et de maintien de l'activité`, avec sortie de configuration Docker réelle.

Requête : `Docker VPS`

Résultats :

- Problème #71669 trouvé pour l'UX d'avertissement quand la configuration de l'interface de contrôle rejette les connexions Docker/VPS non sécurisées.
- Problème #32473 trouvé pour le comportement de contexte sécurisé/identité d'appareil Docker Hostinger VPS.
- Problème #39659 trouvé pour la gestion multi-instance de première classe pour les installations Docker.

### Requêtes Discrawl

Requête : `Docker setup OPENCLAW_SKIP_ONBOARDING OPENCLAW_HOME_VOLUME`

Résultats :

- Aucune correspondance retournée par `discrawl search --mode fts --limit 10`.

Requête : `Docker VPS`

Résultats :

- Demande d'aide d'installation Docker Hetzner du 2026-05-28 trouvée signalant des problèmes de Telegram et Gateway.
- Discussion de mainteneur du 2026-05-23 trouvée sur l'utilisation de Docker/VPS pour les vérifications de repro de problèmes frais.
- Utilisateur demandant le 2026-05-23 comment mettre à jour un VPS Docker d'OpenClaw 4.15 à la dernière version.
