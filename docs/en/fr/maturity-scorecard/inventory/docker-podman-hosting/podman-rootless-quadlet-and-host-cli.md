---
title: "Hébergement Docker / Podman - Note de maturité Podman Rootless, Quadlet et Host CLI"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de maturité Podman Rootless, Quadlet et Host CLI

## Résumé

Le support de Podman suit une conception rootless claire : configuration utilisateur actuel, CLI hôte comme plan de contrôle, `~/.openclaw` monté sur l'hôte, Quadlet/systemd optionnel, ports publiés en loopback, espace de noms utilisateur `keep-id`, et routage `openclaw --container`. La couverture est bêta car la documentation et les scripts sont spécifiques et renforcés, mais moins de preuves e2e et unitaires spécifiques à Podman sont visibles que pour Docker. La qualité est bêta car les archives montrent des dérives antérieures de configuration Podman et des questions de support, bien que les scripts actuels résolvent plusieurs anciens modes de défaillance.

## Portée de la catégorie

- Documentation de configuration Podman, script de configuration, script d'exécution hôte, et modèle de conteneur Quadlet.
- Configuration d'image Podman rootless, lancement, configuration/intégration, routage CLI hôte, démarrage automatique Quadlet, et vérifications de propriétaire/permissions.
- Exclut Docker Compose et Kubernetes.

## Fonctionnalités

- Scripts de configuration Podman et modèle Quadlet : documentation de configuration Podman, scripts/podman/setup.sh, scripts/run-openclaw-podman.sh, et scripts/podman/openclaw.container.in
- Configuration d'image Podman rootless : configuration d'image Podman rootless, lancement, configuration/intégration, routage CLI hôte, démarrage automatique Quadlet, et vérifications de propriétaire/permissions

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (74%)`
- Signaux positifs : la documentation Podman couvre le modèle prévu, les prérequis, le démarrage rapide, les détails de configuration, Quadlet, l'intégration, l'authentification du modèle, la CLI hôte par défaut, Tailscale, la configuration/stockage, les commandes utiles, et le dépannage (`/Users/kevinlin/code/openclaw/docs/install/podman.md:8-216`). La source valide l'exécution non-root, les répertoires/fichiers privés, les noms d'images, les ports, la sécurité des chemins, la création de jetons/configuration, la synchronisation d'origine, `keep-id`, les options de montage SELinux, et l'installation de Quadlet.
- Signaux négatifs : l'inventaire de tests a une couverture de configuration Docker forte mais beaucoup moins de visibilité de tests spécifiques à Podman ; Podman s'appuie sur le comportement des scripts shell qui est plus difficile à vérifier sans smoke runtime.
- Lacunes d'intégration : il n'y a pas de smoke runtime Podman récurrent qui prouve le lancement rootless, la configuration/intégration, le routage CLI hôte, le démarrage automatique Quadlet, et les conseils de redémarrage/mise à jour sur les machines Podman Linux et macOS.

## Score de qualité

- Score : `Bêta (76%)`
- Rapports Gitcrawl : Les preuves de requête incluent le problème fermé #53827 pour les défaillances antérieures de permissions tar temporaire d'image sauvegardée Podman, PR #63407 / archive Freshbits pour le câblage de `OPENCLAW_INSTALL_BROWSER` dans la configuration Podman, et le problème #71493 / PR #71503 pour la sélection d'adresse d'interface bridge Docker/Podman.
- Rapports Discrawl : Les preuves de requête incluent un utilisateur décrivant OpenClaw s'exécutant dans un conteneur Podman sur Rocky Linux le 2026-05-11, un utilisateur demandant des conseils de configuration de conteneur le 2026-05-01, et des entrées Freshbits pour le renforcement de build-arg et de configuration Podman.
- Bonnes qualités : les scripts préfèrent fortement l'opération rootless, rejettent les valeurs d'image/chemin non sécurisées, gardent le travail d'image dans le magasin Podman de l'utilisateur appelant, utilisent `.env` réservé au propriétaire, génèrent des valeurs par défaut Quadlet renforcées, et font de `openclaw --container` le chemin de contrôle hôte.
- Mauvaises qualités : Podman a moins d'historique d'opérateur visible que Docker, le comportement d'authentification de l'appareil de la machine Podman macOS nécessite des conseils spéciaux, et la personnalisation de Quadlet reste manuelle.
- Exclu de la qualité : preuves de tests unitaires, d'intégration, e2e, en direct, et de flux runtime.

## Score de complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les scripts de configuration Podman et le modèle Quadlet, la configuration d'image Podman rootless.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une voie smoke Podman qui couvre la configuration rootless, `launch`, `launch setup`, `openclaw --container`, et le démarrage automatique Quadlet.
- Ajouter des conseils de mise à jour Podman explicites à côté des conseils de mise à jour Docker.
- Ajouter le dépannage de la machine Podman macOS autour de l'authentification de l'appareil de l'interface utilisateur de contrôle et de l'accès Tailscale.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/install/podman.md:8-23` définit le modèle rootless prévu et les prérequis.
- `/Users/kevinlin/code/openclaw/docs/install/podman.md:24-60` documente le démarrage rapide, les détails de configuration, la sélection d'image, la création de configuration/jeton, et la configuration de Quadlet.
- `/Users/kevinlin/code/openclaw/docs/install/podman.md:85-126` documente l'authentification du modèle, la CLI hôte par défaut, la mise en garde d'authentification de l'appareil macOS, et les conseils Tailscale.
- `/Users/kevinlin/code/openclaw/docs/install/podman.md:127-216` documente Quadlet, la configuration/stockage, les commandes utiles, et le dépannage.

### Source

- `/Users/kevinlin/code/openclaw/scripts/podman/setup.sh:1-17` énonce le modèle de configuration rootless utilisateur actuel et les modes de configuration.
- `/Users/kevinlin/code/openclaw/scripts/podman/setup.sh:349-414` nécessite Podman, rejette root, valide les chemins/image/ports, crée des répertoires de configuration/espace de travail privés, et construit/tire l'image.
- `/Users/kevinlin/code/openclaw/scripts/podman/setup.sh:416-493` génère jeton/configuration, amorce les origines, installe Quadlet, et imprime les commandes suivantes.
- `/Users/kevinlin/code/openclaw/scripts/run-openclaw-podman.sh:206-213` rejette l'exécution root.
- `/Users/kevinlin/code/openclaw/scripts/run-openclaw-podman.sh:491-575` crée jeton/configuration, applique le comportement de l'espace de noms utilisateur et du montage SELinux, exécute la configuration, et lance le conteneur de passerelle.
- `/Users/kevinlin/code/openclaw/scripts/podman/openclaw.container.in:1-32` définit le conteneur Quadlet rootless, `keep-id`, les montages de volume, le fichier env, la publication de port loopback, et la politique de redémarrage.

### Tests d'intégration

- Aucun test smoke runtime Podman dédié n'a été trouvé dans l'inventaire de tests local actuel.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts` couvre les voies de version Docker, mais le runtime Podman n'est pas une voie planifiée de première classe là-bas.
- `/Users/kevinlin/code/openclaw/src/cli/container-target.test.ts` couvre le comportement de routage CLI hôte Docker/Podman partagé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/container-target.test.ts` couvre l'analyse/routage `--container`, les noms Docker/Podman ambigus, le rejet du proxy loopback, et le comportement de mise à jour bloquée.
- `/Users/kevinlin/code/openclaw/src/infra/container-environment.test.ts` couvre la détection de sentinelle de conteneur Podman/Kubernetes/Docker.

### Requêtes Gitcrawl

Requête : `Podman setup fails loading saved image`

Résultats :

- Problème fermé #53827, `Podman setup fails loading saved image as openclaw user due to temp tar permissions` ; l'archive discrawl enregistre plus tard sa fermeture après que la configuration actuelle ait gardé le travail dans le contexte Podman rootless de l'utilisateur appelant.

Requête : `OPENCLAW_INSTALL_BROWSER`

Résultats :

- PR #61464 et problème #86612 avec sortie de configuration Docker/Podman impliquant `OPENCLAW_INSTALL_BROWSER`.

### Requêtes Discrawl

Requête : `Podman OpenClaw`

Résultats :

- Rapport d'utilisateur du 2026-05-11 d'OpenClaw s'exécutant dans un conteneur Podman sur Rocky Linux avec proxying d'injection de credentials.
- Entrées Freshbits du 2026-04-29 pour `podman: wire OPENCLAW_INSTALL_BROWSER build-arg to setup script`.
- Note de fermeture de problème du 2026-04-25 pour #53827 décrivant le modèle de configuration Podman rootless-user actuel.
