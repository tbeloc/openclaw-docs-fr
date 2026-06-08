---
title: "Linux Gateway host - Diagnostics and Repair Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Linux Gateway host - Diagnostics and Repair Maturity Note

## Résumé

Les opérateurs Linux Gateway disposent d'une boîte à outils de diagnostic robuste : `openclaw status --deep`, `openclaw logs --follow`, doctor inspect/repair/lint, bundles de diagnostic Gateway, snapshots de stabilité, fallback journal, réparation de service et vérifications de santé/readiness. La qualité est en bêta car les preuves actuelles montrent des faux positifs du doctor, des états tool-schema invalides manqués, des problèmes de sortie `--fix` en état propre, des lacunes de fichier de verrouillage obsolète et une rotation de token surprenante.

## Portée de la catégorie

Inclus dans cette catégorie :

- Rapports de diagnostic Gateway : Couvre l'état Gateway, la sortie de diagnostic, la gestion des défaillances et la réparation par l'opérateur pour les workflows de diagnostic, logs, doctor et repair.
- Suivi des logs Gateway : Couvre la visualisation des logs, le suivi des logs, le comportement de fallback local et l'état des logs Gateway visible par l'opérateur.
- Vérifications Doctor : Couvre les vérifications `openclaw doctor`, les sondes de santé Gateway et les diagnostics de l'opérateur pour les déploiements Linux Gateway.
- Guidance de réparation de l'opérateur : Couvre la gestion des défaillances, la guidance de réparation et les étapes de récupération pour les diagnostics Linux Gateway et les résultats du doctor.

## Fonctionnalités

- Rapports de diagnostic Gateway : Couvre l'état Gateway, la sortie de diagnostic, la gestion des défaillances et la réparation par l'opérateur pour les workflows de diagnostic, logs, doctor et repair.
- Suivi des logs Gateway : Couvre la visualisation des logs, le suivi des logs, le comportement de fallback local et l'état des logs Gateway visible par l'opérateur.
- Vérifications Doctor : Couvre les vérifications `openclaw doctor`, les sondes de santé Gateway et les diagnostics de l'opérateur pour les déploiements Linux Gateway.
- Guidance de réparation de l'opérateur : Couvre la gestion des défaillances, la guidance de réparation et les étapes de récupération pour les diagnostics Linux Gateway et les résultats du doctor.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Justification : la surface de diagnostic couvre l'état, les logs, le doctor, l'export de diagnostic, la réparation, l'état du service et les vérifications de readiness avec le comportement systemd spécifique à Linux.
- Lacunes : certains cas de réparation Linux sont dispersés dans les notes du doctor, les docs de mise à jour, les docs de service et les discussions d'archive.

## Score de qualité

- Score : `Beta (78%)`
- Justification : les outils de diagnostic sont étendus, mais les preuves d'archive actives montrent des faux positifs, des erreurs manquées et un comportement de réparation surprenant pour l'opérateur.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, live et runtime-flow.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-gateway-host.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les rapports de diagnostic Gateway, le suivi des logs Gateway, les vérifications Doctor, la guidance de réparation de l'opérateur.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Rendre la sortie doctor/repair plus sûre autour des fixes en état propre, de la rotation de token, des verrous obsolètes et des avertissements SecretRef.
- Consolider le diagnostic Linux Gateway dans un seul arbre de décision allant du statut aux logs au doctor à l'export de diagnostic.

## Preuves

### Docs

- `docs/cli/status.md:20-40` documente les sondes profondes et la sortie d'état pour Gateway, node, runtime du service hôte, mise à jour et SecretRefs.
- `docs/cli/logs.md:11-12` documente le suivi des logs Gateway à distance via RPC ; `docs/cli/logs.md:60-63` documente le fallback du journal systemd utilisateur actif Linux et le comportement de reconnexion.
- `docs/cli/doctor.md:18-34` décrit le comportement health, inspect, repair et lint du doctor.
- `docs/cli/doctor.md:188-218` documente la gestion systemd-unavailable Linux, le comportement de sauvegarde, la réparation de mise à jour, les réécritures de service, le fallback env, la réparation de service et les avertissements SecretRef.
- `docs/gateway/diagnostics.md:10-16` décrit les exports de diagnostic désinfectés ; `docs/gateway/diagnostics.md:75-90` liste les fichiers inclus.
- `docs/gateway/index.md:331-359` documente les vérifications opérationnelles, la readiness et les signatures de défaillance courantes.

### Source

- `src/cli/daemon-cli/status.gather.ts:101-139` charge les informations de sonde Gateway, auth, system inspect, audit, TLS et restart-health.
- `src/cli/daemon-cli/status.gather.ts:168-252` construit les configs et la sortie de statut rapide/complet.
- `src/cli/logs-cli.ts` implémente le streaming des logs Gateway et le comportement de fallback.
- `src/commands/doctor.ts` coordonne les vérifications de santé et de réparation du doctor.
- `src/daemon/service.ts:134-232` collecte les problèmes de réparation de service et démarre/répare le service Gateway.

### Tests d'intégration

- `src/cli/logs-cli.test.ts:415-471` couvre le fallback du journal systemd actif.
- `src/commands/doctor-gateway-services.test.ts` couvre les sauts de service actifs, les réparations de mise à jour systemd, la persistance des tokens et les services systemd utilisateur hérités.
- `src/commands/gateway-readiness.test.ts` couvre le comportement de readiness.

### Tests unitaires

- `src/commands/doctor-format.test.ts:5-29` couvre la sortie d'hygiène cgroup systemd suspecte.
- `src/cli/daemon-cli/status.gather.test.ts` couvre les branches de collecte d'état.
- `src/gateway/diagnostics.test.ts` couvre le comportement d'export de diagnostic.

### Requêtes Gitcrawl

- La requête spécifique `doctor logs diagnostics systemd Linux port runtime repair gateway` n'a retourné aucun résultat.
- La requête plus large `doctor logs` a retourné le problème #50561 pour l'application automatique des fixes doctor sûrs au démarrage de Gateway, le problème #80435 pour la sortie trailer `doctor --fix` en état propre, la PR #59196 pour les vérifications de santé d'espace disque, le problème #65201 pour un faux avertissement de token auth Gateway avec des secrets, le problème #49036 pour la détection de fichier de verrouillage Gateway obsolète, le problème #87270 pour le schéma d'outil personnalisé actif non supporté non détecté par doctor, le problème #87517 pour la rotation silencieuse de `gateway.auth.token` par `doctor --fix` et le problème #87312 pour le faux signalement de version Chrome.

### Requêtes Discrawl

- La requête `openclaw doctor logs` a trouvé un crash de schéma d'outil non supporté du 2026-05-27 que le doctor n'a pas détecté.
- La même requête a trouvé une guidance de support courante pour exécuter `openclaw models status`, `openclaw doctor` et `openclaw logs --follow`.
