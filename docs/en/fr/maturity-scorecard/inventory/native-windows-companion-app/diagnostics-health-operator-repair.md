---
title: "Application compagne Windows native - Note de statut et de maturité de réparation"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Windows native - Note de statut et de maturité de réparation

## Résumé

Les diagnostics CLI/Gateway Windows natifs existent : documentation, code doctor/service,
inspection des tâches planifiées, repli du dossier de démarrage et validation smoke Parallels
existent. L'application compagne Windows n'a pas sa propre surface de diagnostic ou
de réparation dans la source prise en charge, et les preuves d'archive montrent une douleur continue des opérateurs Windows autour des tâches planifiées, des mises à jour, du statut lent et de la disponibilité de la passerelle.

## Portée de la catégorie

Inclus dans cette catégorie :

- États de santé de l'application : États de santé de l'application, disponibilité de la passerelle/nœud, panneaux de diagnostic, ouverture de journaux, statut de mise à jour, actions de réparation et comportement du bundle de support
- Réparation spécifique à l'application : Réparation spécifique à l'application pour l'appairage, les permissions, le cycle de vie du service, les versions obsolètes et l'incompatibilité de protocole
- Application de barre d'état système Windows : Application de barre d'état système Windows, icône de statut, menu de statut, notifications natives et contrôles de lancement/fermeture d'application
- Indicateurs de statut : Indicateurs de statut pour la passerelle, l'appairage de nœud, l'activité de travail et les mises à jour
- Permission de notification spécifique à l'application : Permission de notification spécifique à l'application et gestion des défaillances

## Fonctionnalités

- États de santé de l'application : États de santé de l'application, disponibilité de la passerelle/nœud, panneaux de diagnostic, ouverture de journaux, statut de mise à jour, actions de réparation et comportement du bundle de support
- Réparation spécifique à l'application : Réparation spécifique à l'application pour l'appairage, les permissions, le cycle de vie du service, les versions obsolètes et l'incompatibilité de protocole
- Application de barre d'état système Windows : Application de barre d'état système Windows, icône de statut, menu de statut, notifications natives et contrôles de lancement/fermeture d'application
- Indicateurs de statut : Indicateurs de statut pour la passerelle, l'appairage de nœud, l'activité de travail et les mises à jour
- Permission de notification spécifique à l'application : Permission de notification spécifique à l'application et gestion des défaillances

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (12%)`
- Signaux positifs : les chemins de diagnostic et de réparation de service CLI/Gateway Windows natifs existent et sont exercés en dehors de la surface de l'application.
- Signaux négatifs : aucune interface utilisateur de diagnostic d'application Windows, visionneuse de journaux, panneau de santé, action de réparation ou flux de travail d'incompatibilité de protocole au niveau de l'application n'existe.
- Lacunes d'intégration : aucun scénario de disponibilité, santé, journal, mise à jour ou réparation spécifique à l'application ne peut être exercé.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel sur
le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par
eux-mêmes.

## Score de qualité

- Score : `Expérimental (38%)`
- Rapports Gitcrawl : `#87156` suit la mise à jour du doctor Windows laissant le repli du dossier de démarrage de la passerelle obsolète et n'installant pas une tâche planifiée ; `#74163` suit plusieurs problèmes de plateforme Windows ; `#87205` note les chemins de migration et de redémarrage automatique des tâches planifiées non testés.
- Rapports Discrawl : le résumé d'archive du `2026-05-13` dit que l'installation/démarrage/mise à jour/redémarrage Windows natif s'est amélioré mais le cycle de vie des tâches planifiées, la stabilité de la passerelle et le polissage UX restent inachevés ; le commentaire d'examen du `2026-03-30` signale les budgets sans sortie `schtasks` serrés causant une détection d'exécution incorrecte.
- Bonnes qualités : les diagnostics CLI/Gateway adjacents ont des concepts de service clairs et des crochets de réparation.
- Mauvaises qualités : les diagnostics d'application manquent, et le dossier d'archive montre la confusion des opérateurs Windows autour exactement des états de service/mise à jour qu'une application devrait expliquer.
- Exclu de la qualité : les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer la qualité.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture de test unitaire, d'intégration, e2e, en direct ou d'exécution réel
comme entrée de notation.

## Score de complétude

- Score : `Expérimental (12%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-companion-app.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les états de santé de l'application, la réparation spécifique à l'application, l'application de barre d'état système Windows, les indicateurs de statut, la permission de notification spécifique à l'application.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du dossier de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune surface de diagnostic d'application Windows n'existe.
- Aucune orientation de santé ou de réparation spécifique à l'application n'existe pour la passerelle hors ligne, le nœud déconnecté, l'appairage obsolète, l'application obsolète ou l'incompatibilité de protocole.
- Aucun emplacement de journal d'application, bundle de support ou runbook d'opérateur n'existe.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:37-59` documente les avertissements CLI/Gateway Windows natifs et le démarrage géré.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md` couvre les diagnostics doctor/service largement.
- `/Users/kevinlin/code/openclaw/docs/gateway/index.md` documente `gateway status`, `gateway restart` et les commandes de service Windows natif.

### Source

- `/Users/kevinlin/code/openclaw/src/commands/doctor-gateway-services.ts` et `/Users/kevinlin/code/openclaw/src/commands/doctor-gateway-health.ts` implémentent les vérifications de passerelle adjacentes.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts` implémente la logique de statut/installation/repli des tâches planifiées Windows.
- `/Users/kevinlin/code/openclaw/src/infra/windows-task-restart.ts` implémente la remise de redémarrage des tâches planifiées.
- Aucune source de diagnostics d'application compagne Windows n'a été trouvée.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-windows-smoke.sh` et `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/windows-smoke.ts` couvrent le smoke CLI/Gateway Windows natif.
- Aucun test d'intégration de diagnostics d'application compagne Windows n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/doctor-gateway-services.test.ts`
- `/Users/kevinlin/code/openclaw/src/commands/doctor-gateway-health.test.ts`
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.test.ts`
- `/Users/kevinlin/code/openclaw/src/infra/windows-task-restart.test.ts`

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows scheduled task startup gateway update" --json`
- `gitcrawl search openclaw/openclaw --query "Windows companion diagnostics health status" --json`

Résultats :

- `#87156` problème ouvert : la mise à jour du doctor Windows laisse le repli du dossier de démarrage de la passerelle obsolète et n'installe pas de tâche planifiée.
- `#51486` PR : interroge directement le runtime de la tâche Windows.
- `#87205` PR : évite la réparation du daemon de passerelle sur incompatibilité de protocole et note que la migration des tâches planifiées/redémarrage automatique n'est pas testée.
- `#74163` PR de suivi inclut les problèmes de timeout de santé/statut Windows.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows scheduled task startup gateway update"`
- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows companion diagnostics health status"`

Résultats :

- Le résumé d'archive du `2026-05-13` dit que l'installation/démarrage/mise à jour/redémarrage Windows natif est pris en charge mais a toujours des bords aigus de tâches planifiées, de stabilité de passerelle et d'UX.
- Le rapport utilisateur du `2026-04-19` montre la sortie de statut Windows avec timeout de passerelle inaccessible tandis que la tâche planifiée et le repli du dossier de démarrage sont présents.
- Le rapport utilisateur du `2026-04-15` montre un statut de passerelle lent sur Windows.
- Le commentaire d'examen du `2026-03-30` sur `#57332` signale un budget sans sortie `schtasks` trop serré causant une détection/logique de repli d'exécution incorrecte.
