---
title: "Chemin d'installation Nix - Note de maturité de remise d'installation"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Note de maturité de remise d'installation

## Résumé

Le dépôt OpenClaw public documente Nix comme un aperçu d'installation optionnelle pris en charge, mais remet délibérément le contrat de configuration faisant autorité au dépôt externe `openclaw/nix-openclaw`. C'est une limite d'opérateur raisonnable, mais cela laisse ce composant à la maturité M1 expérimentale du dépôt source OpenClaw seul : le dépôt local ne contient pas de flake, d'implémentation de module ou de preuve d'exécution qu'un utilisateur peut compléter le chemin d'installation Nix.

## Portée de la catégorie

Inclus dans cette catégorie :

- Aperçu d'installation Nix : Couvre l'aperçu d'installation Nix sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.
- Source de vérité nix-openclaw : Couvre la source de vérité nix-openclaw sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.
- Découverte d'installation : Couvre la découverte d'installation sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.
- Remise de vérification : Couvre la remise de vérification sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.

## Fonctionnalités

- Aperçu d'installation Nix : Couvre l'aperçu d'installation Nix sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.
- Source de vérité nix-openclaw : Couvre la source de vérité nix-openclaw sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.
- Découverte d'installation : Couvre la découverte d'installation sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.
- Remise de vérification : Couvre la remise de vérification sur la page d'installation Nix publique, la découverte de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager de première partie `nix-openclaw`. Il exclut l'implémentation réelle du dépôt externe `openclaw/nix-openclaw` et le comportement de remise de la documentation nix publique et nix-openclaw associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (25%)`
- Signaux positifs : La documentation publique décrit le chemin d'installation Nix, le démarrage rapide, la promesse de restauration, la remise Home Manager et l'attente de vérification.
- Signaux négatifs : Le dépôt source n'a pas de `flake.nix`, `flake.lock`, `default.nix` ou `shell.nix` en dehors des dossiers générés/build, donc le dépôt OpenClaw local ne peut pas lui-même prouver le chemin d'installation Nix.
- Lacunes d'intégration : Aucune preuve d'intégration locale, e2e, en direct ou de service Home Manager réel n'a été trouvée pour la remise d'installation.

## Score de qualité

- Score : `Expérimental (45%)`
- Rapports Gitcrawl : La recherche `nix-openclaw` retourne principalement des mentions Nix larges et des problèmes/PR ouverts adjacents à Nix plutôt qu'un fil de statut de support propre, ce qui rend les preuves de problèmes locaux au dépôt bruyantes.
- Rapports Discrawl : Les messages Discord actuels montrent un travail actif sur les plugins déclaratifs et une proposition `nix-openclaw`, ce qui est un signal de maintenance positif mais aussi une preuve que les éléments principaux bougent encore.
- Bonnes qualités : La documentation rend la limite de source de vérité explicite et garde la page locale comme un aperçu au lieu de prétendre que le dépôt OpenClaw possède le module Nix complet.
- Mauvaises qualités : La promesse de support reste divisée entre la documentation locale et l'implémentation externe, et la ligne de scorecard elle-même dit que le flux d'installation optionnel a besoin d'une promesse de support plus claire avant la promotion.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Expérimental (25%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'aperçu d'installation Nix, la source de vérité nix-openclaw, la découverte d'installation, la remise de vérification.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le dépôt source local ne contient pas l'implémentation du package/module Nix.
- La documentation demande aux utilisateurs de copier un modèle externe mais ne montre pas un modèle local enregistré ou un exemple épinglé dans ce dépôt.
- La page d'installation dit de vérifier que le service launchd s'exécute et que le bot répond, mais il n'y a pas de preuve d'exécution réelle locale attachée à cette instruction.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/install/nix.md:10` présente Nix comme une installation déclarative via `nix-openclaw`.
- `/Users/kevinlin/code/openclaw/docs/install/nix.md:13` dit que le dépôt `nix-openclaw` est la source de vérité et la page n'est qu'un aperçu.
- `/Users/kevinlin/code/openclaw/docs/install/nix.md:21` promet la restauration via `home-manager switch --rollback`.
- `/Users/kevinlin/code/openclaw/docs/install/nix.md:26` à `:41` donne un aperçu de démarrage rapide mais nécessite de copier le modèle de flake agent-first du dépôt externe.
- `/Users/kevinlin/code/openclaw/docs/install/index.md:140` lie la carte d'index d'installation à `/install/nix`.
- `/Users/kevinlin/code/openclaw/docs/start/docs-directory.md:23` inclut le mode Nix dans le répertoire de documentation.
- `/Users/kevinlin/code/openclaw/docs/start/showcase.md:294` répertorie l'empaquetage Nix avec un lien vers `openclaw/nix-openclaw`.

### Source

- `find /Users/kevinlin/code/openclaw ... -iname 'flake.nix' -o -iname 'flake.lock' -o -iname 'default.nix' -o -iname 'shell.nix'` n'a retourné aucun fichier de package Nix du dépôt source après élagage de `node_modules` et `dist`.
- `/Users/kevinlin/code/openclaw/docs/docs.json:668` redirige `/nix` vers `/install/nix`.
- `/Users/kevinlin/code/openclaw/docs/docs.json:1041` inclut `install/nix` dans la navigation de la documentation.

### Tests d'intégration

- Aucune preuve d'intégration locale, e2e, en direct, launchd/systemd ou Home Manager n'a été trouvée pour la remise de documentation publique elle-même.

### Tests unitaires

- Aucun test unitaire ne valide directement la remise de documentation publique ou les instructions de copie de modèle externe.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "nix-openclaw" --json`

Résultats :

- A retourné des éléments ouverts adjacents à Nix incluant la PR `#77843`, le problème `#9987`, le problème `#73328`, le problème `#70191`, la PR `#85238`, la PR `#79734`, le problème `#80536` et la PR `#82032` ; les résultats étaient larges car l'index de mots-clés a tokenisé `nix-openclaw`.
- Aucun problème local du dépôt prouvant la remise de documentation comme un chemin d'installation supporté de bout en bout n'a été trouvé dans cette requête.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "nix-openclaw"`

Résultats :

- `golden-path-deployments` le 2026-05-29 a lié la proposition `openclaw/nix-openclaw#96`.
- `maintainers` le 2026-05-29 a dit que les plugins déclaratifs dans `nix-openclaw` avaient un premier sous-ensemble fonctionnant.
- `golden-path-deployments` le 2026-05-28 a dit qu'un POC de plugin dans `nix-openclaw` ne faisait qu'un sous-ensemble de plugins intégrés.
