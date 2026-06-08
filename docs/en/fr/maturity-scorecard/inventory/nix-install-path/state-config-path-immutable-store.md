---
title: "Chemin d'installation Nix - Note de Maturité Config et State"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Note de Maturité Config et State

## Résumé

OpenClaw sépare clairement l'état mutable des remplacements de chemin de configuration et documente que les utilisateurs Nix doivent définir explicitement `OPENCLAW_CONFIG_PATH` et `OPENCLAW_STATE_DIR`. Le code source et les tests couvrent la résolution des chemins, y compris les chemins de configuration `/nix/store`. Les preuves d'archive d'opérateurs montrent toujours une mauvaise configuration et une confusion concernant le système de fichiers en lecture seule, donc ce composant n'est pas prêt pour une promotion au-delà de la couverture expérimentale.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Garde de configuration immuable : Couvre la garde de configuration immuable sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction Nix source en priorité agent.
- Refus du writer de configuration : Couvre le refus du writer de configuration sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction Nix source en priorité agent.
- Éditions Nix en priorité agent : Couvre les éditions Nix en priorité agent sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction Nix source en priorité agent.
- Chemin de configuration explicite : Couvre le chemin de configuration explicite sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.
- Répertoire d'état inscriptible : Couvre le répertoire d'état inscriptible sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.
- Support de configuration du store immuable : Couvre le support de configuration du store immuable sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.
- Vérifications d'intégrité d'état : Couvre les vérifications d'intégrité d'état sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.

## Fonctionnalités

- Garde de configuration immuable : Couvre la garde de configuration immuable sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction Nix source en priorité agent.
- Refus du writer de configuration : Couvre le refus du writer de configuration sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction Nix source en priorité agent.
- Éditions Nix en priorité agent : Couvre les éditions Nix en priorité agent sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction Nix source en priorité agent.
- Chemin de configuration explicite : Couvre le chemin de configuration explicite sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.
- Répertoire d'état inscriptible : Couvre le répertoire d'état inscriptible sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.
- Support de configuration du store immuable : Couvre le support de configuration du store immuable sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.
- Vérifications d'intégrité d'état : Couvre les vérifications d'intégrité d'état sur les variables d'environnement config/state, les attentes du store immuable, la résolution des chemins, les vérifications d'intégrité d'état autour de `/nix/store`, et les conseils d'exécution que l'état doit rester inscriptible.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Expérimental (45%)`
- Signaux positifs : Les remplacements de chemin de configuration et de répertoire d'état ont des tests dédiés, y compris un chemin de configuration `/nix/store`.
- Signaux négatifs : Les tests ne prouvent pas une configuration complète gérée par Nix plus un répertoire d'état inscriptible sur le démarrage de la passerelle, les sessions, les plugins, les sauvegardes et les flux doctor.
- Lacunes d'intégration : Aucun scénario d'installation Nix réel ne valide que la configuration immuable et l'état inscriptible sont correctement provisionnés ensemble.

## Score de Qualité

- Score : `Alpha (50%)`
- Rapports Gitcrawl : `OPENCLAW_CONFIG_PATH OPENCLAW_STATE_DIR` retourne de nombreuses PR/issues ouvertes utilisant des environnements config/state isolés, plus l'issue `#57408` concernant le `.env` local du projet étant ignoré et revenant à `~/.openclaw/openclaw.json`.
- Rapports Discrawl : Un message d'un mainteneur actuel soulève le risque d'empaquetage déclaratif/Nix autour de l'état d'exécution inscriptible et les migrations tolérant les répertoires config/plugin en lecture seule.
- Bonnes qualités : La résolution des chemins est explicite et la documentation dit aux utilisateurs Nix de garder l'état d'exécution et la configuration en dehors du store immuable.
- Mauvaises qualités : Les rapports d'archive montrent que le comportement des chemins config/state reste une préoccupation récurrente des opérateurs et mainteneurs, en particulier lorsque la configuration est en lecture seule ou que l'état est accidentellement partagé.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Expérimental (45%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la garde de configuration immuable, le refus du writer de configuration, les éditions Nix en priorité agent, le chemin de configuration explicite, le répertoire d'état inscriptible, le support de configuration du store immuable, les vérifications d'intégrité d'état.
- Signaux négatifs : la note archivée a précédé le score de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucune preuve de flux d'installation local ne démontre un chemin de configuration du store Nix avec un répertoire d'état inscriptible séparé.
- Le tableau de documentation donne les valeurs par défaut mais n'inclut pas un exemple local complet de première partie des chemins Nix prévus.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/nix.md:75` à `:83` dit qu'OpenClaw lit la configuration JSON5 depuis `OPENCLAW_CONFIG_PATH`, stocke les données mutable dans `OPENCLAW_STATE_DIR`, et les utilisateurs Nix doivent définir ces variables explicitement pour garder l'état d'exécution et la configuration en dehors du store immuable.
- `/Users/kevinlin/code/openclaw/docs/start/getting-started.md:142` à `:143` liste les remplacements `OPENCLAW_STATE_DIR` et `OPENCLAW_CONFIG_PATH`.

### Source

- `/Users/kevinlin/code/openclaw/src/config/paths.ts:58` à `:68` résout `OPENCLAW_STATE_DIR`.
- `/Users/kevinlin/code/openclaw/src/config/paths.ts:152` à `:161` résout `OPENCLAW_CONFIG_PATH`.
- `/Users/kevinlin/code/openclaw/src/config/paths.ts:199` à `:206` utilise `OPENCLAW_STATE_DIR` pour les candidats de chemin de configuration lorsque le remplacement de configuration est absent.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-state-integrity.ts:708` à `:738` traite `/nix/store` comme un contexte de store immuable pour les vérifications d'intégrité d'état/configuration.

### Tests d'intégration

- Aucune preuve d'intégration d'installation Nix complète n'a été trouvée pour la séparation config/state.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/config/config.nix-integration-u3-u5-u9.test.ts:42` à `:106` teste les remplacements de répertoire d'état et de chemin de configuration, y compris `OPENCLAW_CONFIG_PATH: "/nix/store/abc/openclaw.json"`.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/ConfigStoreTests.swift:73` à `:135` exerce le comportement du magasin de configuration macOS avec `OPENCLAW_CONFIG_PATH`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "OPENCLAW_CONFIG_PATH OPENCLAW_STATE_DIR" --json`

Résultats :

- A retourné de nombreuses PR/issues ouvertes utilisant des environnements config/state temporaires comme harnais de preuve d'exécution.
- L'issue ouverte notable `#57408` dit que le `.env` local du projet a été ignoré et `OPENCLAW_CONFIG_PATH` est revenu à `~/.openclaw/openclaw.json`.
- L'issue ouverte `#84313` référence différentes limites `OPENCLAW_CONFIG_PATH` et `OPENCLAW_STATE_DIR` dans un bug d'isolation de sauvegarde de credentials.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "OPENCLAW_CONFIG_PATH OPENCLAW_STATE_DIR"`

Résultats :

- Les messages du bot GitHub incluent des exemples de preuves d'exécution isolées temporaires `OPENCLAW_CONFIG_PATH` et `OPENCLAW_STATE_DIR`.
- Un fil `nix-openclaw Gateway start blocked` du 2026-02-05 montrait l'env du service avec les deux variables et un `openclaw.json` vide.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "openclaw config read-only Nix"`

Résultats :

- Les `mainteneurs` le 2026-05-08 ont dit que les flux de travail déclaratifs/Nix sont généralement corrects si la configuration reste sauvegardée par fichier, mais le chemin d'état d'exécution doit être inscriptible et les migrations doivent tolérer les répertoires config/plugin en lecture seule.
- Un rapport utilisateur du 2026-03-01 a souligné que la source du store Nix est en lecture seule et appartient à un autre utilisateur.
