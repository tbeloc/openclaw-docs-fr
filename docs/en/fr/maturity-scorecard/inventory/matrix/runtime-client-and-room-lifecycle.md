---
title: "Matrix - Note de Maturité du Cycle de Vie du Runtime"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Note de Maturité du Cycle de Vie du Runtime

## Résumé

Le cycle de vie du runtime est l'un des points forts de Matrix. Le moniteur utilise l'amorçage partagé du client, la publication du statut de démarrage, le suivi du cycle de vie de la synchronisation, la gestion des tâches entrantes, l'arrêt gracieux, le nettoyage du drainage de déchiffrement et la maintenance au démarrage. La couverture est Beta car ce comportement a des preuves solides en termes de tests unitaires et d'assurance qualité, mais la preuve en direct n'est pas suffisante pour qualifier chaque redémarrage et chemin de persistance de Stable. La qualité est Beta car les problèmes d'archive ouverts soulèvent toujours des préoccupations concernant l'arrêt du client partagé et la persistance du magasin de chiffrement.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Résolution du client Matrix partagé : résolution du client Matrix partagé et cycle de vie du client actif
- Démarrage du moniteur : démarrage du moniteur, statut de synchronisation, gestion de l'arrêt fatal, suivi des tâches et comportement du gestionnaire d'événements.
- Maintenance au démarrage : maintenance au démarrage pour la synchronisation de profil, les vérifications de vérification, la restauration de sauvegarde et la réparation au démarrage.

## Fonctionnalités

- Résolution du client Matrix partagé : résolution du client Matrix partagé et cycle de vie du client actif
- Démarrage du moniteur : démarrage du moniteur, statut de synchronisation, gestion de l'arrêt fatal, suivi des tâches et comportement du gestionnaire d'événements.
- Maintenance au démarrage : maintenance au démarrage pour la synchronisation de profil, les vérifications de vérification, la restauration de sauvegarde et la réparation au démarrage.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs :
  - La source dispose d'un amorçage explicite du client partagé, de la disponibilité, de la gestion du client actif, de la publication du statut, de la surveillance du cycle de vie de la synchronisation, du câblage du gestionnaire, du suivi des tâches, de l'arrêt et des chemins de libération du client.
  - Les tests unitaires couvrent le démarrage du moniteur, les transitions de synchronisation, les erreurs fatales, les défaillances de démarrage, la libération du client partagé, le drainage du déchiffrement, l'arriéré de démarrage obsolète et l'enregistrement de la liaison des threads.
  - L'assurance qualité Matrix couvre l'interrogation du statut de disponibilité, la disponibilité au redémarrage, la déduplication du redémarrage, les curseurs de synchronisation obsolètes et la synchronisation incrémentale après redémarrage.
- Signaux négatifs :
  - Les rapports d'archive ouverts montrent que le comportement de persistance et d'arrêt présente toujours un risque réel pour l'utilisateur final.
  - Certaines preuves du cycle de vie se trouvent dans les tests du harnais de scénario plutôt que dans des preuves de version en direct répétées sur les serveurs d'accueil et les plates-formes.
- Lacunes d'intégration :
  - Ajouter une voie de redémarrage/persistance en direct récurrente qui exerce l'arrêt du client partagé, la persistance finale d'IndexedDB, la reprise du curseur de synchronisation et le drainage du gestionnaire en file d'attente.
  - Ajouter une preuve de version pour la disponibilité de Matrix sur au moins une topologie de salle chiffrée et une topologie de salle non chiffrée.
  - Enregistrer des instantanés de statut et d'état de synchronisation de Matrix par version pour les exécutions du cycle de vie échouées et réussies.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, l'e2e, la direct ou les preuves du flux d'exécution réel sur le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "matrix runtime lifecycle sync monitor"` a retourné le problème ouvert #76611 concernant la persistance du magasin de chiffrement Matrix et les assistants d'arrêt de synchronisation qui n'attendent pas la persistance finale.
  - La requête large `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné la PR ouverte #76709 pour les assistants d'arrêt du client partagé asynchrone et le problème ouvert #68188 pour les messages reçus mais non livrés à une session d'agent.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix runtime sync monitor lifecycle"` n'a retourné aucun résultat.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions de version mentionnant le comportement de mention Matrix et la validation du canal bêta.
- Bonnes qualités :
  - Le code d'exécution est structuré autour d'un moniteur, d'un amorçage du client partagé, d'une gestion explicite de l'abandon, d'un état de synchronisation fatal, d'un contrôleur de statut et d'un nettoyage à l'arrêt.
  - La maintenance au démarrage est séparée de la boucle principale du moniteur et peut enregistrer ou abandonner indépendamment.
  - La logique du cycle de vie de la synchronisation distingue l'arrêt intentionnel des états STOPPED ou d'erreur inattendus.
  - L'arrêt draine les déchiffrements en attente et attend les tâches suivies avant la libération du client.
- Mauvaises qualités :
  - Les problèmes du cycle de vie sensibles à la persistance sont actifs dans gitcrawl, en particulier le comportement de persistance finale et de redémarrage.
  - Le runtime Matrix dépend du comportement de synchronisation du serveur d'accueil externe et de l'état du SDK Matrix, donc la robustesse varie selon les déploiements.
  - Le cycle de vie touche E2EE, les liaisons de threads, les caches de salle directe, le statut et le nettoyage sortant, ce qui augmente le couplage des défaillances.
- Exclu de la qualité :
  - Je n'ai pas augmenté ou diminué la Qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réelle.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réelle comme entrée de notation.

## Score de Complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la résolution du client Matrix partagé, le démarrage du moniteur, la maintenance au démarrage.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Enregistrer un rapport de redémarrage en direct qui prouve la persistance du client final et la reprise du curseur de synchronisation après un vrai redémarrage de passerelle.
- Suivre le statut de l'assistant d'arrêt du client partagé par rapport à #76611 et #76709 avant d'augmenter la Qualité.
- Ajouter des diagnostics du cycle de vie visibles par l'opérateur pour connecter le statut du moniteur avec les conseils de réparation.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:81` documente le comportement du cycle de vie de la salle autour de la jointure automatique et des cibles d'invitation stables.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:429` documente la vérification au démarrage, les avis de vérification, la gestion des appareils invalides, l'hygiène des appareils et les chemins du magasin de chiffrement.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix-migration.md:76` documente le flux de mise à niveau recommandé et l'ordre de redémarrage.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/client-bootstrap.ts:55` protège le runtime Node uniquement et résout les clients actifs/partagés.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/client-bootstrap.ts:112` gère la disponibilité et le nettoyage.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.ts:122` démarre la configuration du moniteur et résout le contexte d'exécution/authentification.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.ts:224` initialise le contrôleur de statut, l'exécuteur de tâches et l'état du cycle de vie de la synchronisation.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.ts:238` draine les déchiffrements en attente, attend l'exécuteur de tâches et libère le client lors de l'arrêt.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.ts:482` démarre le client Matrix, enregistre le contexte d'exécution, exécute la maintenance au démarrage et attend l'arrêt fatal ou l'abandon.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/sync-lifecycle.ts:19` implémente la surveillance de l'état de synchronisation fatal.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/startup.ts:54` effectue la synchronisation du profil au démarrage et la persistance de la configuration.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/runtime.test.ts:578` utilise le délai d'attente du scénario pour la disponibilité de Matrix après redémarrage.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/runtime.test.ts:635` traite uniquement les comptes Matrix connectés et sains comme prêts.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1763` met en file d'attente un déclencheur lors du redémarrage avant de prouver que la synchronisation incrémentale continue.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1858` échoue si un événement Matrix géré est redelivré après redémarrage de la passerelle.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1955` force un curseur de synchronisation persistant obsolète et s'attend à ce que la déduplication entrante absorbe la relecture.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.test.ts:572` couvre le statut de démarrage déconnecté et le statut de synchronisation connecté.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.test.ts:690` couvre les erreurs de synchronisation fatales échouant la tâche du canal.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.test.ts:756` couvre l'abandon lors du démarrage bloqué et la libération du client partagé.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/index.test.ts:891` couvre l'arrêt de la synchronisation, le drainage des déchiffrements, l'attente des gestionnaires et la persistance.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/sync-lifecycle.test.ts:62` couvre les erreurs de synchronisation inattendues.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/sync-lifecycle.test.ts:169` couvre les erreurs fatales qui ne sont pas dégradées lors de l'arrêt.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/startup.test.ts:210` couvre les appareils obsolètes, la vérification en attente et les sauvegardes héritées restaurées.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/plugin-entry.runtime.test.ts:89` couvre le chargement du wrapper d'exécution de source-checkout.

### Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "matrix runtime lifecycle sync monitor"` a retourné le problème ouvert #76611.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné #76611, #76709, #68188 et des problèmes de runtime Matrix plus larges.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix runtime sync monitor lifecycle"` n'a retourné aucun résultat.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions de version qui incluaient des notes de validation du canal Matrix.
