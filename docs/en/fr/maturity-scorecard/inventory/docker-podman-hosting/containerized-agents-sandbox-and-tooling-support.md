---
title: "Hébergement Docker / Podman - Note de maturité du bac à sable d'agent et des outils"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de maturité du bac à sable d'agent et des outils

## Résumé

L'hébergement en conteneur chevauche l'histoire du bac à sable d'agent et des outils d'OpenClaw : la configuration de la passerelle Docker peut opter pour un bac à sable soutenu par le socket Docker, l'image peut installer l'interface de ligne de commande Docker, la documentation explique la portée du bac à sable et les limites de ressources, et la source contient des tests de bac à sable étendus. La couverture est bêta car le comportement du bac à sable Docker est bien représenté, mais ce composant s'étend sur deux concepts qui sont faciles à confondre pour les opérateurs : exécuter la passerelle dans un conteneur par rapport à l'utilisation de conteneurs pour isoler les outils d'agent. La qualité est à la limite alpha/bêta car les preuves d'archive montrent toujours une confusion concernant la mutabilité du système de fichiers du conteneur, le socket Docker, les dépendances et la posture du bac à sable.

## Portée de la catégorie

Inclus dans cette catégorie :

- Configuration de la passerelle Docker : configuration de la passerelle Docker avec OPENCLAW_SANDBOX, argument de construction Docker CLI, montage de socket, écritures de configuration du bac à sable et comportement de restauration
- Support du bac à sable d'agent soutenu par Docker : documentation du bac à sable d'agent soutenu par Docker, comportement de la source et tests qui affectent les opérateurs de passerelle hébergée en conteneur.
- Intégration des dépendances d'image de conteneur : intégration des dépendances d'image de conteneur pour les compétences/plugins/outils

## Fonctionnalités

- Configuration de la passerelle Docker : configuration de la passerelle Docker avec OPENCLAW_SANDBOX, argument de construction Docker CLI, montage de socket, écritures de configuration du bac à sable et comportement de restauration
- Support du bac à sable d'agent soutenu par Docker : documentation du bac à sable d'agent soutenu par Docker, comportement de la source et tests qui affectent les opérateurs de passerelle hébergée en conteneur.
- Intégration des dépendances d'image de conteneur : intégration des dépendances d'image de conteneur pour les compétences/plugins/outils

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (75%)`
- Signaux positifs : la documentation Docker explique l'activation du bac à sable d'agent avec `OPENCLAW_SANDBOX=1`, le chemin de socket Docker personnalisé, la restauration au bac à sable désactivé et la distinction entre le conteneur de passerelle et les conteneurs de bac à sable d'agent (`/Users/kevinlin/code/openclaw/docs/install/docker.md:316-337`, `/Users/kevinlin/code/openclaw/docs/install/docker.md:464-504`). Le Dockerfile peut installer l'interface de ligne de commande Docker avec vérification d'empreinte (`/Users/kevinlin/code/openclaw/Dockerfile:252-289`). Le script de configuration construit l'interface de ligne de commande dans l'image lorsque le bac à sable est demandé et évite d'exposer le socket si la configuration du bac à sable échoue. La source et les tests du bac à sable couvrent largement la validation du backend Docker.
- Signaux négatifs : Docker-in-Docker/exposition de socket et l'immuabilité du système de fichiers du conteneur de production sont des domaines à haut risque avec moins de preuves de bout en bout que le chemin de passerelle de base.
- Lacunes d'intégration : aucun scénario ne montre une passerelle hébergée Docker avec `OPENCLAW_SANDBOX=1` exécutant en toute sécurité plusieurs sessions d'agent tout en préservant les limites du socket Docker hôte et les installations de dépendances.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : les preuves de requête incluent le problème #86612 pour le comportement de boucle de redémarrage du bac à sable Docker avec les chemins hôte `/mnt/...`, le problème #7575 proposant Sysbox pour l'isolation du runtime Docker sécurisée, le problème #60827 pour les limites de ressources de conteneur par défaut, et le problème #71420/preuves d'archive Discord concernant les conteneurs de production n'ayant pas `/app` mutable.
- Rapports Discrawl : les preuves de requête incluent un rapport de responsable du 2026-04-25 selon lequel les correctifs de dépendances de conteneur supposaient que `/app` était mutable, ce qui échoue dans les configurations Kubernetes/conteneur de style production ; il note également que les configurations locales Docker/Podman sont plus permissives que les déploiements réels.
- Bonnes qualités : la configuration diffère le montage docker.sock jusqu'à ce que les conditions préalables soient remplies, réinitialise le mode bac à sable en cas d'échec de la configuration, vérifie l'empreinte de la clé de signature apt Docker, documente le non-montage du docker.sock hôte dans les conteneurs de bac à sable d'agent, et dispose d'une logique de validation explicite de liaison/réseau.
- Mauvaises qualités : la limite est difficile à expliquer, les archives de support montrent une confusion réelle, et certaines hypothèses de conteneur de production restent des points sensibles.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct et flux d'exécution.

## Score de complétude

- Score : `Bêta (75%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration de la passerelle Docker, le support du bac à sable d'agent soutenu par Docker, l'intégration des dépendances d'image de conteneur.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un diagramme de modèle de menace pour « Passerelle dans Docker » par rapport à « outils d'agent dans bac à sable Docker ».
- Ajouter un test de fumée de bac à sable hébergé Docker qui vérifie la gestion de docker.sock, la configuration du bac à sable, les limites de ressources et la restauration en cas d'échec.
- Documenter plus directement la stratégie de dépendance de conteneur immuable pour les plugins/compétences et les orchestrateurs de production.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/install/docker.md:316-337` documente `OPENCLAW_SANDBOX=1`, le chemin de socket personnalisé, la restauration en cas d'échec de la configuration au bac à sable désactivé et l'avertissement de ne pas monter le docker.sock hôte dans les conteneurs de bac à sable d'agent.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:464-504` explique le modèle de bac à sable d'agent, les portées, les politiques, les limites de ressources et la documentation connexe.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:11-31` avertit que les binaires externes requis doivent être intégrés dans l'image, pas installés à l'exécution.
- `/Users/kevinlin/code/openclaw/docs/install/docker.md:424-439` documente les options d'image pour utilisateurs avancés pour apt, Python, navigateur et téléchargements de navigateur persistants.

### Source

- `/Users/kevinlin/code/openclaw/Dockerfile:252-289` installe optionnellement l'interface de ligne de commande Docker après vérification de l'empreinte de la clé de signature apt Docker.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:281-283` valide le chemin du socket Docker lorsque le bac à sable est demandé.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:428-434` définit `OPENCLAW_INSTALL_DOCKER_CLI=1` pour les constructions locales activées par bac à sable.
- `/Users/kevinlin/code/openclaw/scripts/docker/setup.sh:460-462` conserve les arguments Compose de base sans superposition de bac à sable pour les chemins de restauration.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/docker-backend.test.ts` et les fichiers de bac à sable connexes couvrent le comportement du gestionnaire de bac à sable Docker.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/docker-setup.e2e.test.ts:567-620` vérifie le comportement de désactivation du bac à sable et ignore le redémarrage lorsque les écritures de configuration du bac à sable échouent.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox-agent-config.agent-specific-sandbox-config.e2e.test.ts` couvre le comportement de configuration du bac à sable Docker spécifique à l'agent.
- `/Users/kevinlin/code/openclaw/scripts/e2e/plugin-binding-command-escape-docker.sh` et les tests du plan Docker E2E couvrent l'échappement de commande dans les voies Docker.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/sandbox/validate-sandbox-security.test.ts` couvre le socket Docker, la configuration Docker, les chemins de conteneur réservés, les jointures d'espace de noms et la validation de montage de liaison.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/docker.test.ts` couvre les vérifications d'image Docker et les erreurs de démon.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/docker.config-hash-recreate.test.ts` couvre la récréation de conteneur partagé et le comportement de hachage de montage.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.build-docker-exec-args.test.ts` couvre le comportement du shell Docker exec et du PATH.

### Requêtes Gitcrawl

Requête : `openclaw update --container rebuild restart container image`

Résultats :

- Atteint le problème #86612 pour le contexte de boucle de redémarrage et bac à sable Docker.
- Atteint le problème #7575 proposant Sysbox Docker Runtime pour l'isolation de conteneur sécurisée.

Requête : `Docker VPS`

Résultats :

- Atteint le problème #60827 pour les limites de ressources de conteneur par défaut pour le bac à sable.
- Atteint le problème #57713 pour l'image de bac à sable par défaut manquant python3, cassant l'édition/écriture.

### Requêtes Discrawl

Requête : `container filesystem Docker plugin dependencies`

Résultats :

- Aucune sortie FTS directe pour cette requête exacte.

Requête : `Podman OpenClaw`

Résultats :

- Trouvé un message de responsable du 2026-04-25 : les configurations de conteneur/Kubernetes de production n'écrivent généralement pas à l'intérieur de `/app`, et les configurations locales Podman/Docker sont plus permissives que les déploiements du monde réel.
