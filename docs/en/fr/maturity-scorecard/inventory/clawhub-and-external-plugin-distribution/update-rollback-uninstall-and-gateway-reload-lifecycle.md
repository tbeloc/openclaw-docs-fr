---
title: "ClawHub - Update, Rollback, Uninstall, and Gateway Reload Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - Update, Rollback, Uninstall, and Gateway Reload Lifecycle Maturity Note

## Résumé

La surface des commandes de cycle de vie est large : install, enable, disable, inspect,
update, downgrade, uninstall, registry refresh, et Gateway restart/reload
les attentes sont toutes documentées et implémentées. La couverture est Beta car une
couverture e2e de fixture réelle existe, y compris update/downgrade/uninstall, mais l'audit
n'a pas trouvé de preuve de ligne de version ClawHub et npm en direct. La qualité est Beta car
le modèle est compréhensible mais toujours divisé entre l'état du registre froid et
l'état d'exécution de la passerelle en direct.

## Portée de la catégorie

- Mise à jour par id de plugin, spécification npm, spécification ClawHub, canal bêta et marketplace.
- Sémantique de réinstallation par rapport à la mise à jour.
- Rétrogradation et sélecteurs épinglés.
- Nettoyage de la configuration/index/politique/fichier de désinstallation.
- Exigences de redémarrage/rechargement de la passerelle après install/update/uninstall.

## Fonctionnalités

- Mise à jour par id de plugin : Mise à jour par id de plugin, spécification npm, spécification ClawHub, canal bêta et marketplace
- Sémantique de réinstallation par rapport à la mise à jour : Portée des preuves pour la sémantique de réinstallation par rapport à la mise à jour.
- Rétrogradation : Rétrogradation et sélecteurs épinglés
- Nettoyage de la configuration/index/politique/fichier de désinstallation : Portée des preuves pour le nettoyage de la configuration/index/politique/fichier de désinstallation.
- Exigences de redémarrage/rechargement de la passerelle après : Exigences de redémarrage/rechargement de la passerelle après install/update/uninstall

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : les docs et e2e couvrent update, downgrade, uninstall, inspect,
  enable/disable, et marketplace update/uninstall.
- Signaux négatifs : aucune mise à jour ClawHub en direct, mise à jour npm dist-tag ou rollback
  sur un registre de packages externe réel n'a été trouvé dans l'audit.
- Lacunes d'intégration : le rollback est principalement modélisé comme reinstall/downgrade et
  nettoyage de désinstallation, pas comme un flux de travail d'opérateur de première classe.

## Score de qualité

- Score : `Beta (74%)`
- Bonnes qualités : la mise à jour réutilise les spécifications suivies, les sélecteurs exacts restent épinglés,
  la dérive d'intégrité peut échouer fermée, la désinstallation supprime l'état config/policy/index, et
  les docs indiquent clairement quand un redémarrage de la passerelle est requis.
- Mauvaises qualités : l'état froid `list`/`inspect` par rapport à l'état de la passerelle en direct reste un
  point de confusion pour l'opérateur, et l'automatisation du rechargement dépend de l'état de la passerelle gérée.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et flux d'exécution sont comptées
  uniquement sous Couverture, pas Qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs : les docs archivées, source, test, Gitcrawl et preuves Discrawl couvrent la portée de la taxonomie pour Mise à jour par id de plugin, Sémantique de réinstallation par rapport à la mise à jour, Rétrogradation, Nettoyage de la configuration/index/politique/fichier de désinstallation, Exigences de redémarrage/rechargement de la passerelle après.
- Signaux négatifs : la note archivée a précédé le score de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une section de rollback de première classe qui explique quand utiliser la mise à jour épinglée,
  la rétrogradation, la réinstallation avec force, ou la désinstallation/réinstallation.
- Ajouter des portes de mise à jour ClawHub et npm en direct pour les cas stable, bêta, exact et
  dérive d'intégrité.

## Preuves

### Docs

- `docs/tools/plugin.md:87` : l'installation, la mise à jour ou la désinstallation du code du plugin nécessite un redémarrage de la passerelle.
- `docs/cli/plugins.md:150` : `--force` est pour la réinstallation, tandis que les mises à niveau de routine doivent utiliser `plugins update`.
- `docs/cli/plugins.md:341` : la désinstallation supprime les entrées de configuration, les enregistrements d'index d'installation, les entrées de politique et les répertoires d'installation gérés.
- `docs/cli/plugins.md:355` : la surface de la commande update couvre id/spec, all, dry-run et unsafe override.
- `docs/cli/plugins.md:376` : les mises à jour du canal bêta essaient d'abord bêta et reviennent à default/latest le cas échéant.

### Source

- `src/cli/plugins-cli.ts:167` : enregistre `openclaw plugins update`.
- `src/plugins/update.ts` : implémente npm, ClawHub, git, marketplace, fallback bêta, dérive d'intégrité et mises à jour de plugins groupés externalisés.
- `src/plugins/uninstall.ts:538` : calcule les actions de désinstallation et le nettoyage sûr des répertoires.
- `src/plugins/uninstall.ts:614` : applique la suppression de répertoire après la planification de la désinstallation.

### Tests d'intégration

- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:45` : inspection d'exécution après installation.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:47` : flux de désactivation.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:50` : flux d'activation.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:53` : flux de mise à niveau.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:57` : flux de rétrogradation.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:68` : désinstallation avec code de plugin manquant.

### Tests unitaires

- `src/plugins/update.test.ts:2148` : met à jour les plugins installés via ClawHub via les métadonnées de package enregistrées.
- `src/plugins/update.test.ts:2213` : essaie ClawHub bêta pour les spécifications ClawHub par défaut sans persister la balise bêta.
- `src/plugins/update.test.ts:2296` : revient à npm pour les blocs d'artefacts ClawHub officiels de confiance.
- `src/plugins/update.test.ts:2767` : vérifie les installations de marketplace lors des mises à jour en mode dry-run.
- `src/plugins/uninstall.test.ts:1572` : supprime les répertoires d'installation gérés par ClawHub.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "plugin lifecycle matrix update uninstall" --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "plugin lifecycle install update downgrade uninstall corrupt plugin repair" --limit 5 --json`

Résultats :

- Les deux requêtes n'ont retourné aucun résultat, donc les preuves d'archive GitHub n'ont pas ajouté d'incidents de cycle de vie en direct au-delà des preuves de code/test.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "plugin update rollback uninstall ClawHub npm"`

Résultats :

- N'a retourné aucun résultat, donc les preuves d'archive Discord n'ont pas ajouté de preuve de cycle de vie pour rollback/update/uninstall.
