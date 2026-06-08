---
title: "Chemin d'installation Nix - Note de maturité du cycle de vie des plugins"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Note de maturité du cycle de vie des plugins

## Résumé

OpenClaw bloque les commandes de cycle de vie des plugins mutables en mode Nix et dispose d'une autorisation de politique de lien physique ciblée pour les racines de plugins sous `/nix/store`. Cette posture source est bonne, mais les preuves opérationnelles actuelles montrent que le support déclaratif des plugins est toujours incomplet dans `nix-openclaw`, y compris un rapport récent de rupture de plugin Slack après l'externalisation des plugins.

## Portée de la catégorie

Inclus dans cette catégorie :

- Refus de commande de cycle de vie : Couvre le refus de commande de cycle de vie sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.
- Sélection déclarative des plugins : Couvre la sélection déclarative des plugins sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.
- Chargement des plugins du magasin Nix : Couvre le chargement des plugins du magasin Nix sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.
- Sécurité des liens physiques : Couvre la sécurité des liens physiques sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.

## Fonctionnalités

- Refus de commande de cycle de vie : Couvre le refus de commande de cycle de vie sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.
- Sélection déclarative des plugins : Couvre la sélection déclarative des plugins sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.
- Chargement des plugins du magasin Nix : Couvre le chargement des plugins du magasin Nix sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.
- Sécurité des liens physiques : Couvre la sécurité des liens physiques sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation des plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative des plugins.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (40%)`
- Signaux positifs : Les chemins CLI et de réponse automatique vérifient que les mutateurs de cycle de vie des plugins refusent en mode Nix ; la politique de lien physique couvre les racines de plugins `/nix/store`.
- Signaux négatifs : Il n'y a pas de e2e local au repo pour un ensemble de plugins déclaratifs intégrés dans une fermeture Nix et chargés par une passerelle en cours d'exécution.
- Lacunes d'intégration : Aucune preuve en direct ne couvre les plugins Slack/officiels externes après la limite d'externalisation des plugins Nix.

## Score de qualité

- Score : `Expérimental (35%)`
- Rapports Gitcrawl : `nix-openclaw plugins` a retourné le problème `#80536` autour des superpositions de flocons Nix en aval et PR `#80497` ; `hardlink Nix plugin` n'a retourné aucun résultat.
- Rapports Discrawl : L'archive Discord récente montre que le support des plugins `nix-openclaw` ne couvrait qu'un sous-ensemble de plugins intégrés, une rupture Slack après l'externalisation des plugins, et un échec de construction du wrapper `openclaw-qmd`.
- Bonnes qualités : Les commandes de plugins mutables échouent fermées, et les liens physiques `/nix/store` sont traités comme une exception spécifique du magasin immuable au lieu d'affaiblir largement le renforcement des plugins.
- Mauvaises qualités : Le support déclaratif des plugins à l'exécution est visiblement inachevé et a été signalé comme ne supportant pas les plugins npm à l'exécution dans une version récente de `nix-openclaw`.
- Exclus de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Expérimental (40%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le refus de commande de cycle de vie, la sélection déclarative des plugins, le chargement des plugins du magasin Nix, la sécurité des liens physiques.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les plugins déclaratifs sont un travail actif, pas un contrat de support établi.
- Le repo OpenClaw dispose de garde-fous et d'exceptions de lien physique, mais le support du module Nix réel pour la sélection des plugins vit en externe.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/manage-plugins.md:141` à `:143` indique que les commandes d'installation, mise à jour, désinstallation, activation et désactivation des plugins sont désactivées en mode Nix et doivent être gérées dans la source Nix.
- `/Users/kevinlin/code/openclaw/docs/tools/plugin.md:262` répertorie `OPENCLAW_NIX_MODE=1` bloquant les commandes de cycle de vie et indique aux utilisateurs de modifier la sélection des plugins dans la source Nix.

### Source

- `/Users/kevinlin/code/openclaw/src/cli/plugins-install-command.ts:572` appelle la garde d'écriture de configuration Nix avant la mutation d'installation du plugin.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-update-command.ts:29` et `/Users/kevinlin/code/openclaw/src/cli/plugins-uninstall-command.ts:34` appellent la garde pour la mise à jour/désinstallation.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.runtime.ts:168` et `:213` gardent les mutations de configuration d'activation/désactivation des plugins.
- `/Users/kevinlin/code/openclaw/src/plugins/hardlink-policy.ts:6` à `:16` documente `/nix/store` dans `OPENCLAW_NIX_MODE` comme contexte de lien physique autorisé.
- `/Users/kevinlin/code/openclaw/src/plugins/hardlink-policy.ts:25` à `:35` rejette les fichiers de plugins liés physiquement sauf si l'origine est groupée ou la racine est un chemin du magasin Nix en mode Nix.

### Tests d'intégration

- Aucun e2e de plugin déclaratif construit avec Nix n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.install.test.ts:432` à `:436` vérifie que l'installation du plugin refuse en mode Nix avant les effets secondaires du programme d'installation.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.update.test.ts:83` à `:88` vérifie que la mise à jour du plugin refuse avant le travail du gestionnaire de paquets.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.uninstall.test.ts:62` à `:67` vérifie que la désinstallation du plugin refuse avant la planification de la suppression de fichiers.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.policy.test.ts:96` à `:101` vérifie que l'activation du plugin refuse avant la mutation de configuration.
- `/Users/kevinlin/code/openclaw/src/plugins/hardlink-policy.test.ts:27` à `:45` vérifie que le mode Nix seul est insuffisant et que la racine `/nix/store` est requise.
- `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.test.ts:2612` à `:2635` vérifie que les liens physiques de manifeste de configuration en dehors de `/nix/store` sont toujours rejetés en mode Nix.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "nix-openclaw plugins" --json`

Résultats :

- A retourné le problème `#80536`, impliquant des ajouts de schéma de configuration de superposition de flocons Nix en aval non détectés par le validateur d'exécution.
- A retourné PR `#80497`, une PR d'événement de diagnostic du SDK de plugin avec des extraits adjacents à Nix.

Requête :

`gitcrawl search openclaw/openclaw --query "hardlink Nix plugin" --json`

Résultats :

- A retourné `hits: []`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "nix store plugin"`

Résultats :

- `golden-path-deployments` le 2026-05-28 a signalé que les plugins `nix-openclaw` n'étaient pas encore supportés pour une version car les installations npm arbitraires via Nix étaient compliquées.
- Le même fil a signalé que Slack était cassé sur `nix-openclaw` après `v2026.5.26` parce que Slack s'était déplacé vers un plugin npm à l'exécution et `nix-openclaw` avait marqué les plugins npm à l'exécution comme non supportés.
- `maintainers` le 2026-05-08 a décrit PR `#79344` assouplissant la politique de lien physique pour les utilisateurs Nix afin que les plugins normaux puissent utiliser des liens physiques vers `/nix/store`.
