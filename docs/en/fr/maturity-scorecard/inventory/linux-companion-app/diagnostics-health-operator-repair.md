---
title: "Application compagne Linux - Note de maturité du statut et des diagnostics"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Linux - Note de maturité du statut et des diagnostics

## Résumé

Les diagnostics de la passerelle Linux sont documentés via l'interface CLI, l'interface de contrôle, les journaux, le doctor et les conseils systemd. Une application compagne Linux native devrait consolider ceux-ci en surfaces de disponibilité, diagnostics et réparation au niveau de l'application ; la PR ouverte #59859 revendique un tel travail, mais aucun diagnostic d'application Linux pris en charge n'est enregistré.

## Portée de la catégorie

Inclus dans cette catégorie :

- Disponibilité de l'application Linux native : États de disponibilité de l'application Linux native
- Affichage de la santé/statut de la passerelle : Comportement, statut et vérification visible par l'opérateur de la santé/statut de la passerelle.
- Ouverture de journaux/transcriptions : Ouverture de journaux/transcriptions et gestion des ressources consciente de la localité
- Affordances Doctor/réparation : Affordances Doctor/réparation et diagnostics du cycle de vie systemd
- Élément de plateau/statut Linux : Comportement, statut et vérification visible par l'opérateur de l'élément de plateau/statut Linux.
- Ligne de statut d'exécution : Ligne de statut d'exécution et notifications natives
- Intégration de l'environnement de bureau : Intégration de l'environnement de bureau pour le comportement du plateau GNOME/KDE/Wayland/X11

## Fonctionnalités

- Disponibilité de l'application Linux native : États de disponibilité de l'application Linux native
- Affichage de la santé/statut de la passerelle : Comportement, statut et vérification visible par l'opérateur de la santé/statut de la passerelle.
- Ouverture de journaux/transcriptions : Ouverture de journaux/transcriptions et gestion des ressources consciente de la localité
- Affordances Doctor/réparation : Affordances Doctor/réparation et diagnostics du cycle de vie systemd
- Élément de plateau/statut Linux : Comportement, statut et vérification visible par l'opérateur de l'élément de plateau/statut Linux.
- Ligne de statut d'exécution : Ligne de statut d'exécution et notifications natives
- Intégration de l'environnement de bureau : Intégration de l'environnement de bureau pour le comportement du plateau GNOME/KDE/Wayland/X11

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (8%)`
- Signaux positifs : Les diagnostics CLI de la passerelle Linux et la documentation systemd existent, et la PR ouverte #59859 signale la vérification de la disponibilité/diagnostics au niveau de l'application.
- Signaux négatifs : aucune source de diagnostics d'application Linux native enregistrée ou test de réparation au niveau de l'application n'existe.
- Lacunes d'intégration : aucune preuve de scénario doctor/statut/journal/transcription ou réparation d'application Linux native n'existe dans l'arborescence source actuelle.

## Score de qualité

- Score : `Expérimental (38%)`
- Rapports Gitcrawl : La requête de diagnostics Linux a retourné une PR de suivi large, tandis que la PR #59859 revendique la disponibilité/diagnostics et le repli de ressources conscient de la localité.
- Rapports Discrawl : la requête spécifique aux diagnostics n'a retourné aucune preuve de version prise en charge directe ; les commentaires du problème #75 mentionnent les jalons des diagnostics Linux en cours.
- Bonnes qualités : les diagnostics CLI/Gateway sous-jacents sont documentés, et les PR Linux ouvertes nomment les états de disponibilité importants et les risques de ressources locales par rapport à distantes.
- Mauvaises qualités : la documentation actuelle ne fournit pas de flux de travail de diagnostic Linux au niveau de l'application, de taxonomie de disponibilité, d'UX de réparation ou de chemin d'escalade officiel.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Expérimental (8%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la disponibilité de l'application Linux native, l'affichage de la santé/statut de la passerelle, l'ouverture de journaux/transcriptions, les affordances Doctor/réparation, l'élément de plateau/statut Linux, la ligne de statut d'exécution, l'intégration de l'environnement de bureau.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Définir les états de disponibilité au niveau de l'application, de l'absence de configuration à la configuration, l'installation du service, la connexion, la dégradation et la distance.
- Ajouter la gestion de la localité des journaux/transcriptions Linux native.
- Documenter les actions de réparation que l'application peut déclencher par rapport aux actions qui restent CLI uniquement.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:58` : La documentation Linux dirige les utilisateurs vers `openclaw doctor` pour la réparation/migration.
- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:64` : Le comportement du service utilisateur systemd Linux est documenté.
- `/Users/kevinlin/code/openclaw/docs/start/openclaw.md:224` : la liste de contrôle opérationnelle inclut `openclaw status`, `openclaw status --all`, `openclaw status --deep`, et `openclaw health --json`.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:117` : l'interface utilisateur de contrôle du navigateur inclut les panneaux cron, compétences, nœuds et approbation d'exécution, qui sont des surfaces d'opérateur adjacentes.

### Source

- La source actuelle a le code de diagnostics et de statut CLI/Gateway, mais aucune source de diagnostics d'application `apps/linux` au niveau de l'application.
- `/Users/kevinlin/code/openclaw/src/commands/status.scan.ts` et les fichiers `src/commands/doctor-*` associés sont des chemins de diagnostics CLI/Gateway, pas l'interface utilisateur de l'application compagne Linux.

### Tests d'intégration

- Aucun test d'intégration de diagnostics/santé/réparation d'application Linux native n'a été trouvé.
- Le fumage du programme d'installation CLI Linux existe, mais il ne lance pas ou ne vérifie pas une interface utilisateur de diagnostics d'application compagne.

### Tests unitaires

- Aucun test unitaire de diagnostics compagne Linux n'a été trouvé.
- Les tests unitaires de statut/doctor existants couvrent le comportement CLI/Gateway en dehors de cette surface d'application native.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Linux companion diagnostics health status doctor" --mode keyword --limit 8 --json`
- `gitcrawl gh pr view 59859 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`

Résultats :

- La requête de diagnostics a retourné la PR de suivi large #74163, pas un résultat de diagnostic compagne Linux atterri.
- La PR #59859 revendique la modélisation d'exécution/disponibilité Linux, l'intégration, les diagnostics, les notifications, l'intégration systemd et la vérification manuelle des états de disponibilité ; elle reste ouverte.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux companion diagnostics health status doctor"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux Windows Clawdbot Apps issue 75"`

Résultats :

- La requête spécifique aux diagnostics n'a retourné aucun résultat direct.
- La requête du problème #75 a retourné des commentaires de jalons d'application Linux qui mentionnent les diagnostics et la progression de la disponibilité, mais pas une version prise en charge enregistrée.
