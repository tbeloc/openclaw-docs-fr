---
title: "Application compagnon Windows native - Note de maturité Tray, Status et Notifications natives"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon Windows native - Note de maturité Tray, Status et Notifications natives

## Résumé

La forme compagnon Windows souhaitée inclut une application de barre système et une surface de statut, mais le main OpenClaw actuel n'en fournit pas. Les preuves d'archive font référence à une suite externe `openclaw-windows-node` avec portée d'application System Tray, et les commentaires d'examen sur les PRs compagnon Windows antérieures mentionnent le comportement du badge/statut de la barre système. Ce n'est pas un support source atterri pour la ligne de scorecard.

## Portée de la catégorie

- Application de barre système Windows, icône de statut, menu de statut, notifications natives, et contrôles de lancement/fermeture d'application.
- Indicateurs de statut pour Gateway, appairage de nœud, activité de travail et mises à jour.
- Permission de notification spécifique à l'application et gestion des défaillances.

## Fonctionnalités

- Application de barre système Windows : Application de barre système Windows, icône de statut, menu de statut, notifications natives, et contrôles de lancement/fermeture d'application
- Indicateurs de statut : Indicateurs de statut pour Gateway, appairage de nœud, activité de travail et mises à jour
- Permission de notification spécifique à l'application : Permission de notification spécifique à l'application et gestion des défaillances

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (5%)`
- Signaux positifs : les preuves d'archive montrent que le travail tray/status a été proposé et développé en dehors de la surface d'application actuellement supportée.
- Signaux négatifs : le main actuel n'a pas de source d'application tray Windows, runtime tray, contrôleur d'icône/menu d'application, pont de notification native, ou boucle de statut au niveau de l'application.
- Lacunes d'intégration : aucun scénario de lancement d'application, tray-state, notification, statut Gateway, ou update-state ne peut être exécuté pour une application compagnon Windows supportée.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, e2e, live, ou les preuves de flux runtime réel sur le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Experimental (35%)`
- Rapports Gitcrawl : `#81673` mentionne la portée de la suite compagnon Windows/system tray/node packaging ; `#73315` est une PR d'application de bureau multiplateforme, pas de support atterri.
- Rapports Discrawl : `openclaw-windows-node` est décrit comme une suite compagnon Windows avec application System Tray, bibliothèque partagée, nœud et extension PowerToys ; un commentaire d'examen sur `#54588` signale un comportement de badge tray/UI refresh obsolète après la suppression du nœud distant.
- Bonnes qualités : la propriété tray/status souhaitée est identifiable à partir de l'activité d'archive.
- Mauvaises qualités : aucune implémentation supportée, contrat UX, comportement de secours, ou docs d'opérateur n'existent dans le main actuel.
- Exclu de la qualité : les preuves unitaires, d'intégration, e2e, live et runtime-flow n'ont pas été utilisées pour augmenter ou diminuer la qualité.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture de test unitaire, d'intégration, e2e, live ou runtime réel comme entrée de notation.

## Score de complétude

- Score : `Experimental (5%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-companion-app.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'application system tray Windows, les indicateurs de statut, la permission de notification spécifique à l'application.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune source tray ou menu de statut ne vit dans le repo OpenClaw supporté.
- Aucun contrat de notification d'application n'est documenté pour Windows.
- L'UX de statut pour Gateway, nœud, appairage, mise à jour et activité de travail est indéfini dans les docs actuels.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md` ne documente pas une application tray/status Windows.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` documente le comportement compagnon de la barre de menu macOS, qui est un contexte de parité adjacent mais pas un support Windows.

### Source

- `/Users/kevinlin/code/openclaw/apps/` n'a pas de répertoire d'application Windows.
- `/Users/kevinlin/code/openclaw/src/gateway/node-command-policy.ts:75-105` inclut les défauts de commande de nœud Windows, mais c'est une politique Gateway, pas une application tray.

### Tests d'intégration

- Aucun test d'intégration tray compagnon Windows n'a été trouvé.
- Le smoke Parallels Windows existant se concentre sur l'installation CLI/Gateway, la mise à jour et le comportement de tour d'agent.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/gateway-misc.test.ts:879-902` vérifie les défauts de politique de commande de nœud compagnon Windows sûrs.
- Aucun test unitaire tray/status Windows n'a été trouvé dans le main actuel.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows tray app companion node" --json`
- `gitcrawl search openclaw/openclaw --query "safe Windows companion commands" --json`

Résultats :

- `#81673` problème ouvert mentionne le travail de suite compagnon Windows/system tray/node.
- `#74163` PR de suivi ouvert surfaces les problèmes de plateforme Windows, mais pas de support tray atterri.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows tray app companion node"`

Résultats :

- `2026-03-13` Le miroir GitHub décrit `openclaw/openclaw-windows-node` comme une suite compagnon Windows avec application System Tray, bibliothèque partagée, nœud et extension Command Palette PowerToys.
- `2026-03-28` commentaire d'examen sur `#54588` signale un état obsolète de badge tray/UI refresh après la suppression du nœud distant.
- `2026-04-26` Le miroir GitHub pour `#71876` dit que l'application tray Windows est maintenant un nœud compagnon complet, mais c'est un contexte d'archive/prototype plutôt qu'une source main actuelle.
