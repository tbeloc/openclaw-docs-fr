---
title: "Gateway Web App - Operator Console Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - Operator Console Maturity Note

## Résumé

L'interface utilisateur de contrôle expose les diagnostics opérationnels via des snapshots de santé/statut/débogage, des journaux d'événements, la queue du journal de passerelle, les actions/statuts de mise à jour, le statut du modèle, l'utilisation, les résumés d'activité et les entrées de navigateur de tâches longues/performances. La couverture est Beta car de nombreux contrôleurs et RPC de passerelle sont testés, mais les runbooks d'opérateur complets via le navigateur sont moins complets que les diagnostics CLI. La qualité est Beta car l'interface utilisateur affiche un état utile, tandis que l'archive du trafic montre que les opérateurs ont souvent encore besoin d'assistance pour interpréter la santé de la passerelle, l'accès hébergé, les exécutions actives et l'état du panneau.

## Portée de la catégorie

Inclus dans cette catégorie :

- Santé/statut/modèles : Couvre Santé/statut/modèles dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Queue de journal en direct : Couvre Queue de journal en direct dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Exécution/statut de mise à jour : Couvre Exécution/statut de mise à jour dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Résumés d'activité : Couvre Résumés d'activité dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Télémétrie de timing RPC : Couvre Télémétrie de timing RPC dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Canaux/connexion : Couvre Canaux/connexion dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.
- Gestionnaire de session et historique : Couvre le gestionnaire de session de l'interface utilisateur de contrôle du navigateur, l'historique de session, la présence d'instance, les approbations, les diagnostics et les onglets de journal.
- Cron : Couvre Cron dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.
- Compétences/nœuds : Couvre Compétences/nœuds dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.
- Approbations d'exécution/agents : Couvre Approbations d'exécution/agents dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.

## Fonctionnalités

- Santé/statut/modèles : Couvre Santé/statut/modèles dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Queue de journal en direct : Couvre Queue de journal en direct dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Exécution/statut de mise à jour : Couvre Exécution/statut de mise à jour dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Résumés d'activité : Couvre Résumés d'activité dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Télémétrie de timing RPC : Couvre Télémétrie de timing RPC dans Debug, Logs, Update, Activity et les comportements de diagnostics, journaux, mise à jour et activité associés.
- Canaux/connexion : Couvre Canaux/connexion dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.
- Gestionnaire de session et historique : Couvre le gestionnaire de session de l'interface utilisateur de contrôle du navigateur, l'historique de session, la présence d'instance, les approbations, les diagnostics et les onglets de journal.
- Cron : Couvre Cron dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.
- Compétences/nœuds : Couvre Compétences/nœuds dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.
- Approbations d'exécution/agents : Couvre Approbations d'exécution/agents dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les affiche.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : Les tests de passerelle couvrent les méthodes de santé/statut/journal/mise à jour ; les tests de contrôleur/vue de l'interface utilisateur couvrent les journaux, l'utilisation, le débogage, l'activité, l'aperçu, le quota du fournisseur et les assistants de performance.
- Signaux négatifs : Les flux de diagnostic du navigateur sont principalement testés en tant que contrôleurs/vues individuels. Les scénarios complets « quelque chose ne va pas, utilisez l'interface utilisateur pour diagnostiquer et mettre à jour » sont moins matures que les workflows CLI doctor/log/status.
- Lacunes d'intégration : Ajouter une preuve de scénario de navigateur pour le diagnostic d'exécution bloquée, la queue de journal en direct, la confusion de santé des canaux, la mise à jour d'exécution/reconnexion/statut, la portée d'utilisation et le comportement d'effacement/export d'activité.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : La requête spécifique de journaux/santé/mise à jour a retourné `[]` ; les PR larges de l'interface utilisateur de contrôle ont retourné #84290 pour les résultats de santé de fraîcheur de l'interface utilisateur, #80192 pour l'activité Codex native sûre dans l'interface utilisateur de contrôle, #87147 pour la portée de la page d'utilisation et #73836 pour la régression de réactivité.
- Rapports Discrawl : La recherche Discord a trouvé une assistance où les opérateurs ont été invités à utiliser `status`, `health`, `logs` et l'interface utilisateur de contrôle pour distinguer l'authentification hébergée, la santé de la passerelle et l'état de l'agent.
- Bonnes qualités : Les journaux sont supprimés et analysés de manière défensive, l'activité masque les arguments et ne stocke que les aperçus assainis, les sondes de canal conservent les snapshots précédents en cas de délai d'attente, et les bannières de statut de mise à jour incluent des raisons exploitables.
- Mauvaises qualités : Les diagnostics sont répartis sur plusieurs onglets, et les conseils « ce que je devrais regarder en premier » destinés aux opérateurs dans le navigateur sont toujours plus faibles que les runbooks en ligne de commande.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel affectent uniquement la couverture.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Santé/statut/modèles, Queue de journal en direct, Exécution/statut de mise à jour, Résumés d'activité, Télémétrie de timing RPC, Canaux/connexion, Gestionnaire de session et historique, Cron, Compétences/nœuds, Approbations d'exécution/agents.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'interface utilisateur de contrôle a besoin d'un chemin de diagnostic plus serré de « le chat est bloqué » à l'état de session, l'activité, les journaux, la santé et la récupération.
- Les flux de mise à jour ont besoin d'une preuve plus forte pour les bannières de redémarrage/reconnexion/statut dans les passerelles installées par paquet.
- L'activité est intentionnellement éphémère et locale au navigateur, elle ne remplace donc pas les diagnostics durables.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente Debug, Logs, Update, journal d'événements, timings RPC, timings de rendu de chat/config lent, entrées de réactivité du navigateur et le comportement de confidentialité de l'onglet Activity.
- `/Users/kevinlin/code/openclaw/docs/gateway/health.md`, `/Users/kevinlin/code/openclaw/docs/gateway/diagnostics.md` et `/Users/kevinlin/code/openclaw/docs/gateway/logging.md` documentent les capacités de diagnostic de passerelle sous-jacentes.

### Source

- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/logs.ts` charge et analyse `logs.tail`.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/activity.ts` affiche l'activité d'outil locale au navigateur avec les arguments masqués et les aperçus tronqués.
- `/Users/kevinlin/code/openclaw/ui/src/ui/activity-model.ts` construit les entrées d'activité à partir des événements d'outil.
- `/Users/kevinlin/code/openclaw/ui/src/ui/control-ui-performance.ts` suit la réactivité du navigateur et les entrées de timing de rendu.
- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/health.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/debug.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/usage.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/provider-quota-summary.ts` soutiennent les vues de diagnostic.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/logs.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-methods/health.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update.ts` exposent les méthodes de passerelle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server.health.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-methods/usage.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/diagnostics.test.ts` couvrent les méthodes de diagnostic de passerelle.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-stability.test.ts` couvre les diagnostics de stabilité.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/logs.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/usage.node.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/debug.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/usage.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/activity.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/control-ui-performance.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/usage-cache-status.test.ts` couvrent les diagnostics de l'interface utilisateur.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Control UI logs health update debug activity"`

Résultats :

- A retourné `[]`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "Control UI"`

Résultats :

- A retourné les PR adjacentes aux diagnostics #84290, #80192, #87147, #73894 et #80670.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI logs health update debug activity"`

Résultats :

- A trouvé des conseils d'assistance qui traitent la WebSocket de passerelle comme la source de vérité pour le chat, les sessions, cron, les canaux, le débogage, les modèles, les journaux et les événements en direct.
- A trouvé des exemples de triage de configuration demandant aux utilisateurs d'exécuter status, health et logs pour distinguer la santé de la passerelle des problèmes de canal/configuration.
