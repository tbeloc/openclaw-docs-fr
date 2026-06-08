---
title: "Automatisation des navigateurs et outils exec/sandbox - Note de maturité de la politique de sandbox et d'outils"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation des navigateurs et outils exec/sandbox - Note de maturité de la politique de sandbox et d'outils

## Résumé

Les backends de sandbox et l'isolation de l'espace de travail sont Stables en couverture et Bêta en qualité. Les backends Docker, SSH et OpenShell sont documentés et représentés dans les sources/tests ; l'accès à l'espace de travail, les montages de liaison, le pont du système de fichiers, le registre et les gardes de chemin sont substantiels. La qualité reste Bêta car la parité des chemins Docker-in-Docker, le comportement du pont de backend distant, la traduction des chemins de lecture/écriture et les limites du backend de navigateur restent opérationnellement fragiles.

## Portée de la catégorie

Inclus dans cette catégorie :

- Backends de Sandbox : couvre les backends de sandbox sur les modes de sandbox, les portées, les racines de l'espace de travail, workspaceAccess et le comportement connexe des backends de sandbox et de l'isolation de l'espace de travail.
- Isolation de l'espace de travail : couvre l'isolation de l'espace de travail sur les modes de sandbox, les portées, les racines de l'espace de travail, workspaceAccess et le comportement connexe des backends de sandbox et de l'isolation de l'espace de travail.
- Navigateur en sandbox : couvre le navigateur en sandbox sur la configuration du navigateur en sandbox, la création du conteneur de navigateur Docker, l'authentification du relais CDP, le flux de mot de passe/jeton noVNC et le comportement connexe du navigateur en sandbox et des outils dynamiques codex.
- Outils dynamiques Codex : couvre les outils dynamiques Codex sur la configuration du navigateur en sandbox, la création du conteneur de navigateur Docker, l'authentification du relais CDP, le flux de mot de passe/jeton noVNC et le comportement connexe du navigateur en sandbox et des outils dynamiques codex.
- Politique d'outils : couvre la politique d'outils sur les profils d'outils, les groupes d'outils, la politique d'autorisation/refus, la politique du fournisseur et le comportement connexe de la politique d'outils et du comportement des portes d'outils de sandbox.
- Portes d'outils de Sandbox : couvre les portes d'outils de sandbox sur les profils d'outils, les groupes d'outils, la politique d'autorisation/refus, la politique du fournisseur et le comportement connexe de la politique d'outils et du comportement des portes d'outils de sandbox.

## Fonctionnalités

- Backends de Sandbox : couvre les backends de sandbox sur les modes de sandbox, les portées, les racines de l'espace de travail, workspaceAccess et le comportement connexe des backends de sandbox et de l'isolation de l'espace de travail.
- Isolation de l'espace de travail : couvre l'isolation de l'espace de travail sur les modes de sandbox, les portées, les racines de l'espace de travail, workspaceAccess et le comportement connexe des backends de sandbox et de l'isolation de l'espace de travail.
- Navigateur en sandbox : couvre le navigateur en sandbox sur la configuration du navigateur en sandbox, la création du conteneur de navigateur Docker, l'authentification du relais CDP, le flux de mot de passe/jeton noVNC et le comportement connexe du navigateur en sandbox et des outils dynamiques codex.
- Outils dynamiques Codex : couvre les outils dynamiques Codex sur la configuration du navigateur en sandbox, la création du conteneur de navigateur Docker, l'authentification du relais CDP, le flux de mot de passe/jeton noVNC et le comportement connexe du navigateur en sandbox et des outils dynamiques codex.
- Politique d'outils : couvre la politique d'outils sur les profils d'outils, les groupes d'outils, la politique d'autorisation/refus, la politique du fournisseur et le comportement connexe de la politique d'outils et du comportement des portes d'outils de sandbox.
- Portes d'outils de Sandbox : couvre les portes d'outils de sandbox sur les profils d'outils, les groupes d'outils, la politique d'autorisation/refus, la politique du fournisseur et le comportement connexe de la politique d'outils et du comportement des portes d'outils de sandbox.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (85%)`
- Signaux positifs :
  - Les docs couvrent les outils en sandbox, les modes, les portées, la matrice des backends Docker/SSH/OpenShell, la parité des chemins Docker-in-Docker, l'accès à l'espace de travail, les liaisons et le support du backend de navigateur.
  - La source dispose d'un registre de backends, de backends Docker et SSH, de la résolution de contexte, de la disposition de l'espace de travail, du pont du système de fichiers, de la garde de chemin et des mises à jour du registre.
  - Les tests couvrent le registre de backends, le gestionnaire de backends Docker, le backend SSH, la fusion de la configuration de sandbox, l'explication de sandbox, les montages de l'espace de travail, les spécifications de liaison, les vérifications des limites du pont FS, le pont FS du backend e2e, le pont FS distant et les chemins de médias de sandbox.
  - Les docs et la source échouent explicitement lorsqu'un backend ne supporte pas les sandboxes de navigateur.
- Signaux négatifs :
  - Les rapports d'archive incluent les boucles de redémarrage de la passerelle Docker, l'absence de python dans les chemins du pont FS de sandbox et la confusion des chemins d'écriture/lecture de sandbox.
  - SSH/OpenShell sont plus canoniques à distance et ne supportent pas les conteneurs de navigateur en sandbox.
- Lacunes d'intégration :
  - Ajouter une matrice de backends qui exécute le même flux exec/read/write/edit/apply_patch sur Docker, SSH et OpenShell.
  - Ajouter un test de déploiement Docker-in-Docker pour la parité des chemins d'hôte et les écritures de battement cardiaque du pont FS.

## Score de qualité

- Score : `Bêta (78%)`
- Rapports Gitcrawl :
  - `sandbox docker fs bridge` a retourné la PR #56785 pour les conseils manquants sur python3, le problème #86612 pour la boucle de redémarrage de la passerelle Docker avec sandbox activé, le problème #7575 pour le runtime Sysbox et la PR #69824 pour la consolidation du runtime ACP.
  - `sandbox backend workspaceAccess bind fs bridge openshell ssh docker` n'a retourné aucun résultat ciblé ; des requêtes de sandbox plus larges étaient nécessaires.
- Rapports Discrawl :
  - `sandbox backend fs bridge` a retourné des fils de support du 2026-04-16 expliquant les exigences python de l'image Docker, le risque du pont distant SSH/OpenShell et que l'écriture/édition utilise un assistant Python à l'intérieur du runtime de sandbox actif plutôt que le Python de l'hôte.
  - La même archive incluait également un rapport de crochet/espace de travail de sandbox où les écritures en sandbox n'étaient pas visibles sur le chemin d'hôte attendu, montrant pourquoi les diagnostics de traduction de chemin sont importants.
- Bonnes qualités :
  - L'enregistrement du backend est explicite et échoue lorsqu'un backend non enregistré est demandé.
  - Le contexte de sandbox résout l'état d'exécution effectif, la disposition de l'espace de travail, le backend, le support du navigateur, le pont FS et l'entrée du registre en un seul chemin.
  - Le pont du système de fichiers utilise des gardes de chemin, des entrées épinglées, des vérifications d'accès et des commandes shell de backend au lieu d'écritures d'hôte directes.
  - Le backend Docker signale la correspondance des étiquettes de configuration et les erreurs de suppression du runtime.
- Mauvaises qualités :
  - La socket Docker, la parité des chemins d'hôte, les montages de liaison et les superpositions en lecture seule sont puissants mais faciles à mal configurer.
  - Les backends distants ont un support de navigateur plus faible et s'appuient sur les hypothèses de l'environnement shell distant.
  - Le comportement de WorkspaceAccess peut être surprenant car l'espace de travail de l'agent, l'espace de travail de sandbox et l'état canonique distant peuvent diverger.
- Exclu de la qualité :
  - Les preuves des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont affecté que la couverture.

## Score de complétude

- Score : `Stable (85%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves archivées des docs, sources, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les backends de Sandbox, l'isolation de l'espace de travail, le navigateur en sandbox, les outils dynamiques Codex, la politique d'outils et les portes d'outils de sandbox.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les backends SSH et OpenShell ont besoin d'une preuve de parité plus forte par rapport à Docker pour la mutation de fichiers et l'exécution de processus.
- Les diagnostics de sandbox doivent rendre évidents les erreurs de propriété de chemin et de parité de chemin hôte-vs-conteneur.

# Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:9`: la documentation indique qu'OpenClaw peut exécuter des outils à l'intérieur des backends sandbox tandis que Gateway reste sur l'hôte.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:15`: l'exécution des outils et le navigateur sandbox optionnel sont couverts par le sandboxing.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:39`: les modes sandbox incluent off, non-main, et all.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:58`: la portée du sandbox contrôle la réutilisation des conteneurs agent/session/shared.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:66`: la documentation des backends liste Docker, SSH, et OpenShell.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:78`: la matrice des backends montre que Docker supporte le sandbox navigateur tandis que SSH/OpenShell ne le font pas.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:94`: l'avertissement Docker-in-Docker documente les exigences de parité du chemin d'accès à l'hôte et du pont FS.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md:42`: la vérification rapide de sécurité du bind mount avertit du perçage du système de fichiers sandbox.
- `/Users/kevinlin/code/openclaw/docs/tools/multi-agent-sandbox-tools.md:181`: les paramètres sandbox par agent remplacent les valeurs par défaut globales.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/sandbox/backend.ts:43`: le registre backend enregistre les backends sandbox.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/backend.ts:70`: l'absence de fabrique backend lève une guidance de configuration exploitable.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/backend.ts:83`: les backends Docker et SSH sont enregistrés.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/docker-backend.ts:32`: le backend Docker assure un conteneur et retourne un handle capable d'exec.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/docker-backend.ts:63`: le backend Docker annonce la capacité navigateur.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/context.ts:130`: la résolution du contexte sandbox commence à partir du statut runtime effectif.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/context.ts:145`: la disposition de l'espace de travail est assurée avant la création du backend.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/context.ts:159`: le contexte nécessite la fabrique backend configurée.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/context.ts:201`: le backend sans capacité navigateur échoue quand le sandbox navigateur est activé.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/fs-bridge.ts:34`: le pont système de fichiers sandbox est créé pour un contexte sandbox.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/fs-bridge.ts:83`: les écritures nécessitent un accès en écriture et des vérifications de sécurité du chemin.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/fs-bridge.ts:251`: les commandes planifiées revérifient les gardes de chemin avant l'exécution.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/sandbox/fs-bridge.backend.e2e.test.ts:72`: la couverture e2e du backend local existe pour le comportement du pont fs sandbox.
- `/Users/kevinlin/code/openclaw/test/scripts/sandbox-common-smoke-workflow.test.ts:1`: la couverture smoke du script existe pour le flux de travail sandbox courant.
- `/Users/kevinlin/code/openclaw/scripts/test-live-cli-backend-docker.sh:346`: le script Docker backend live existe pour la validation du backend CLI.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/sandbox/backend.test.ts:8`: vérifie le comportement du registre backend sandbox.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/docker-backend.test.ts:46`: vérifie le comportement du gestionnaire backend sandbox Docker.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/ssh-backend.test.ts:139`: vérifie le comportement du backend sandbox SSH.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/fs-bridge.boundary.test.ts:18`: vérifie que les écritures dans les bind mounts en lecture seule sont bloquées.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/fs-bridge.boundary.test.ts:62`: vérifie que les échappements de symlink préexistants sont rejetés.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/workspace-mounts.test.ts:1`: les tests de montage d'espace de travail existent.
- `/Users/kevinlin/code/openclaw/src/commands/sandbox-explain.test.ts:1`: les tests sandbox explain existent.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "sandbox docker fs bridge" --json`

Résultats :

- PR ouverte #56785 : guidance sandbox quand python3 est manquant.
- Problème ouvert #86612 : boucle de redémarrage du conteneur gateway Docker quand sandbox est activé.
- Problème ouvert #7575 : runtime Docker Sysbox pour l'isolation sécurisée des conteneurs.

Requête :

`gitcrawl search openclaw/openclaw --query "sandbox backend workspaceAccess bind fs bridge openshell ssh docker" --json`

Résultats :

- Aucun résultat ciblé retourné ; les requêtes plus larges `sandbox docker fs bridge` et `sandbox browser` ont fourni les preuves d'archive actuelles.

### Requêtes Discrawl

Requête :

`discrawl search --mode fts --limit 5 "sandbox backend fs bridge"`

Résultats :

- 2026-04-16 l'archive de support explique les exigences python de l'image sandbox Docker, le risque du pont FS distant SSH/OpenShell, et que le code helper write/edit s'exécute à l'intérieur du runtime sandbox actif.
- 2026-04-08 le rapport hook/sandbox workspace montre un chemin d'écriture en sandbox où les effets du système de fichiers hôte visibles n'étaient pas clairs, renforçant l'écart de diagnostic de chemin.
