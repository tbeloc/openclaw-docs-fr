---
title: "Chemin d'installation Nix - Note de maturité pour la configuration immuable et les éditions de source en priorité agent"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Note de maturité pour la configuration immuable et les éditions de source en priorité agent

## Résumé

Le signal Nix local le plus fort est la protection en écriture de configuration immuable. OpenClaw centralise le message d'erreur, bloque les chemins larges de mutation de configuration, et oriente les utilisateurs et les agents vers la source Nix. Le composant manque encore d'une preuve complète à l'exécution que chaque writer visible par l'utilisateur passe par la protection dans un déploiement Nix réel.

## Portée de la catégorie

Cette catégorie couvre la protection `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction de source Nix en priorité agent.

## Fonctionnalités

- Protection de configuration immuable : Couvre la protection de configuration immuable sur la protection `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction de source Nix en priorité agent.
- Refus du writer de configuration : Couvre le refus du writer de configuration sur la protection `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction de source Nix en priorité agent.
- Éditions Nix en priorité agent : Couvre les éditions Nix en priorité agent sur la protection `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du writer de configuration, et l'instruction de source Nix en priorité agent.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (45%)`
- Signaux positifs : Plusieurs chemins de source appellent la protection centralisée, et la documentation nomme les mutateurs exacts qui doivent refuser d'éditer `openclaw.json`.
- Signaux négatifs : La preuve est principalement une couverture de commande/chemin de source ; aucune exécution réelle de magasin Nix immuable n'a été trouvée sur tous les mutateurs.
- Lacunes d'intégration : Aucun e2e n'a prouvé un refus réel de configuration gérée par Nix, configuration, intégration, ensemble de configuration, commandes de plugin, mise à jour, et réparation doctor dans un flux installé.

## Score de qualité

- Score : `Alpha (55%)`
- Rapports Gitcrawl : `config immutable Nix` a retourné la PR `#79734`, qui dit que `--dry-run` devrait fonctionner en mode Nix où la configuration est immuable.
- Rapports Discrawl : Un fil de discussion de mainteneur de mai 2026 a dit que la PR `#78047` a corrigé la limite de politique pour les écritures de configuration automatiques/à l'exécution, tout en signalant également un problème doctor plus étroit à suivre séparément.
- Bonnes qualités : Le texte d'erreur est explicite, central, actionnable, et lie à la fois le démarrage rapide en priorité agent et l'aperçu Nix.
- Mauvaises qualités : Le contexte d'archive montre que cette limite était une véritable source de confusion et a nécessité un travail de rétrofit ; l'implémentation actuelle repose toujours sur chaque writer utilisant la protection partagée.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct, et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Expérimental (45%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de taxonomie pour la protection de configuration immuable, le refus du writer de configuration, les éditions Nix en priorité agent.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La protection de source est large mais pas automatiquement exhaustive pour les écritures de fichier direct futures.
- Le référentiel local ne peut pas valider si les éditions de source Nix externes sont correctes car le module vit en dehors de ce référentiel.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/nix.md:67` à `:73` énumère les changements en mode Nix et dit que les agents doivent éditer `programs.openclaw.config` ou `instances.<name>.config` dans la source Nix.
- `/Users/kevinlin/code/openclaw/docs/cli/setup.md:15` dit que `openclaw setup` est pour les installations mutables et refuse les écritures en mode Nix.

### Source

- `/Users/kevinlin/code/openclaw/src/config/nix-mode-write-guard.ts:3` à `:7` définit les URLs Nix et le code d'erreur `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`.
- `/Users/kevinlin/code/openclaw/src/config/nix-mode-write-guard.ts:15` à `:23` formate le message de configuration immuable visible par l'utilisateur et dit aux utilisateurs de ne pas exécuter setup, intégration, mise à jour, mutateurs de plugin, réparation/génération de token doctor, ou ensemble de configuration contre le fichier.
- `/Users/kevinlin/code/openclaw/src/config/nix-mode-write-guard.ts:27` à `:36` lance une exception quand `resolveIsNixMode` est vrai.
- `rg -n "assertConfigWriteAllowedInCurrentMode(" /Users/kevinlin/code/openclaw/src` a trouvé des appels de protection dans IO/mutation de configuration, installation de plugin d'intégration, commande de mise à jour, installation/mise à jour/désinstallation/exécution de plugin, santé doctor, et commandes de plugin de réponse automatique.

### Tests d'intégration

- Aucun test d'intégration de flux installé unique couvrant tous les mutateurs de configuration immuable n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/onboarding-plugin-install.test.ts:262` à `:283` vérifie que les installations de plugin d'intégration non ignorées refusent en mode Nix.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.policy.test.ts:96` à `:105` vérifie que l'activation de plugin refuse avant la mutation de configuration.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/commands-plugins.test.ts:308` à `:319` vérifie que l'activation de plugin de réponse automatique refuse en mode Nix.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "config immutable Nix" --json`

Résultats :

- A retourné la PR `#79734` (`feat(doctor): add --dry-run flag to preview config changes without applying`) avec un extrait notant la compatibilité dry-run en mode Nix où la configuration est immuable.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "doctor Nix mode"`

Résultats :

- `maintainers` le 2026-05-06 a dit que la PR `#78047` a corrigé la limite de politique pour les écritures de configuration automatiques/à l'exécution et le mode Nix/immuable.
- Le même message a dit qu'un problème doctor plus étroit devrait toujours être suivi séparément, diminuant les preuves de soutien que chaque chemin de réparation est réglé.
