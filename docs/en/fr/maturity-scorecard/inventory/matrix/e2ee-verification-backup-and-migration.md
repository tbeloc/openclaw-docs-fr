---
title: "Matrix - Note de Maturité du Chiffrement et de la Vérification"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Note de Maturité du Chiffrement et de la Vérification

## Résumé

Le chiffrement E2EE de Matrix est largement implémenté : les conseils de configuration, la vérification au démarrage, les clés de récupération, le stockage des secrets, l'amorçage de la signature croisée, la vérification SAS, l'hygiène des appareils, la sauvegarde des clés de salle, les médias chiffrés, la migration de la cryptographie héritée et les instantanés de migration disposent tous de preuves de source et d'assurance qualité. La couverture est Beta car l'empreinte des tests et de l'assurance qualité est large. La qualité est Alpha car gitcrawl a plusieurs rapports ouverts sur la récupération E2EE, la signature croisée, la réinitialisation forcée et la persistance.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Chiffrement et Vérification`
- Fusionnée à partir de : `Chiffrement et Vérification`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du chiffrement : Configuration du chiffrement, disponibilité de la cryptographie, stockage des clés de récupération et stockage des secrets.
- Téléchargement/téléversement de médias chiffrés : Téléchargement/téléversement de médias chiffrés et avis de vérification au démarrage
- État hérité : État hérité et migration de la cryptographie, instantanés de migration et réparation du démarrage de la passerelle.

## Fonctionnalités

- Configuration du chiffrement : Configuration du chiffrement, disponibilité de la cryptographie, stockage des clés de récupération et stockage des secrets.
- Téléchargement/téléversement de médias chiffrés : Téléchargement/téléversement de médias chiffrés et avis de vérification au démarrage
- État hérité : État hérité et migration de la cryptographie, instantanés de migration et réparation du démarrage de la passerelle.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - La documentation couvre la configuration du chiffrement, les signaux de confiance, les commandes de vérification, l'état de la sauvegarde/restauration/réinitialisation, les avis de vérification, l'hygiène des appareils, les chemins du magasin de cryptographie et le flux de migration.
  - La source implémente le stockage des clés de récupération, l'amorçage du stockage des secrets, la signature croisée, les actions de vérification SAS, la vérification au démarrage, le téléversement de médias chiffrés, la migration de la cryptographie héritée et les instantanés de migration.
  - Les tests unitaires couvrent les actions de vérification, l'amorçage de la cryptographie, le magasin des clés de récupération, le gestionnaire de vérification, la migration de la cryptographie héritée, la persistance IndexedDB et les commandes CLI de vérification.
  - L'assurance qualité Matrix couvre les salles E2EE isolées, la configuration des clés de récupération, la configuration invalide des clés de récupération, l'auto-vérification, la restauration de la sauvegarde, la récupération E2EE destructive et l'échec de l'amorçage du serveur d'accueil défaillant.
- Signaux négatifs :
  - La correction E2EE dépend du comportement du serveur d'accueil, de l'état de la cryptographie du SDK Matrix, de la persistance locale, de la confiance d'identité et de la disponibilité de la sauvegarde.
  - Les rapports E2EE actifs montrent que les chemins destructifs et de récupération restent fragiles.
- Lacunes d'intégration :
  - Ajouter des exécutions E2EE en direct récurrentes sur les serveurs d'accueil fronts MAS et non-MAS.
  - Ajouter des artefacts de version qui prouvent la restauration des clés de récupération, la restauration de la sauvegarde et l'auto-vérification après le redémarrage de la passerelle.
  - Ajouter un mappage explicite réussi/échoué pour les scénarios de perte d'état de cryptographie destructive.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel sur le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "Matrix recovery key cross-signing backup"` a retourné les problèmes ouverts #78396 pour la réinitialisation forcée de la signature croisée corrompant l'état E2EE, #73480 pour l'échec de la clé de récupération, #74504 pour l'échec de l'amorçage de Synapse fronté MAS, #76611 pour la persistance du magasin de cryptographie, plus la PR ouverte #74509 pour la gestion MSC3967.
  - La requête large `gitcrawl --json search openclaw/openclaw --query "Matrix"` a également retourné la PR ouverte #74529 pour la gestion de la collision d'ID OTK `/keys/upload`.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix E2EE verification backup recovery key"` a retourné une entrée de miroir GitHub pour la PR #71311 ajoutant une couverture de récupération de sauvegarde E2EE destructive.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions de version Matrix et des notes de validation bêta.
- Bonnes qualités :
  - La documentation E2EE distingue l'accès aux clés de récupération, la santé de la sauvegarde, la publication de la signature croisée, la confiance d'identité complète et l'hygiène des appareils.
  - Le code d'amorçage retarde la mutation du stockage des secrets pour la réparation de signature croisée forcée et supporte le secours UIA par mot de passe.
  - Les actions de vérification maintiennent l'auto-vérification dans une session client Matrix démarrée et attendent la confiance d'identité complète.
  - La migration crée des instantanés de sauvegarde et sépare la migration de l'état hérité de la préparation de l'état chiffré.
- Mauvaises qualités :
  - Les rapports d'archive actifs couvrent exactement les chemins E2EE les plus risqués : récupération, amorçage de signature croisée, réinitialisation forcée, téléversement OTK et persistance.
  - Certaines réparations peuvent être destructives ou nécessiter l'intention de l'opérateur, donc les valeurs par défaut doivent rester conservatrices.
  - La variance du SDK Matrix et du serveur d'accueil rend cette surface plus difficile à garantir que la messagerie non chiffrée.
- Exclus de la qualité :
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

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la Configuration du chiffrement, le Téléchargement/téléversement de médias chiffrés, l'État hérité.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Retester ou fermer #78396, #73480, #74504, #74509, #74529 et #76611 avant d'augmenter la Qualité au-dessus d'Alpha.
- Ajouter une preuve en direct actuelle pour les serveurs d'accueil fronts MAS.
- Garder les scénarios de récupération E2EE destructive isolés et clairement étiquetés dans les rapports d'assurance qualité.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:275` documente la configuration du chiffrement, l'état, les signaux de confiance et les commandes de vérification.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:360` documente l'état de la sauvegarde/restauration/réinitialisation et les commandes du cycle de vie de la vérification.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:429` documente la vérification au démarrage, les avis, la gestion des appareils supprimés/invalides, l'hygiène des appareils et les chemins du magasin cryptographique.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix-migration.md:21` documente les snapshots de migration et les changements d'état couverts.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix-migration.md:135` documente le flux de migration chiffrée.

## Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/verification.ts:25` nécessite le chiffrement avant les actions de vérification.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/verification.ts:171` attend l'état de confiance de vérification automatique complète.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/verification.ts:238` énumère et demande les vérifications Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/sdk/crypto-bootstrap.ts:48` amorce le stockage secret et la signature croisée.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/sdk/crypto-bootstrap.ts:199` gère la réinitialisation et la réparation forcées de la signature croisée.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/send/media.ts:203` télécharge les médias chiffrés.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/startup.ts:113` exécute la vérification au démarrage E2EE.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/legacy-crypto.ts:121` détecte l'état chiffré Matrix hérité.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/migration-snapshot-backup.ts:65` crée ou réutilise les snapshots de sauvegarde pré-migration.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server.startup-matrix-migration.integration.test.ts:4` couvre le câblage de la maintenance du canal de démarrage de la passerelle pour la migration Matrix.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1012` provisionne des salons chiffrés isolés pour les scénarios E2EE.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1049` exécute une régression E2EE `state_after` à travers le proxy de défaut.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4983` ignore les réponses E2EE obsolètes lors de la vérification d'un avis de vérification.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:5093` applique une clé de récupération avant de restaurer les clés de salle sauvegardées.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:5226` maintient l'accès à la sauvegarde de la clé de récupération distinct de la confiance d'identité Matrix.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:5415` exécute la vérification automatique Matrix via la commande CLI interactive.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:7031` exécute l'amorçage E2EE Matrix en défaut via un point de terminaison serveur d'accueil réel défaillant.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/verification.test.ts:218` prépare le chiffrement local avant l'état de vérification.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/verification.test.ts:429` maintient la vérification automatique dans une session client démarrée.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/verification.test.ts:500` attend la confiance d'identité Matrix complète.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/actions/verification.test.ts:627` attend la publication des clés de signature croisée.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/sdk/crypto-bootstrap.test.ts:180` amorce la signature croisée et le stockage secret.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/sdk/crypto-bootstrap.test.ts:367` évite de muter le stockage secret avant que la réparation forcée échoue sans UIA de mot de passe.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/sdk/recovery-key-store.test.ts:118` charge les clés de récupération stockées.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/legacy-crypto.test.ts:90` extrait les clés de sauvegarde enregistrées dans le nouveau chemin de clé de récupération.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/sdk/idb-persistence.test.ts:116` sérialise les opérations de persistance concurrentes.

## Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "Matrix recovery key cross-signing backup"` a retourné #78396, #73480, #74504, #74509 et #76611.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné #74529 et des résultats E2EE Matrix plus larges.

## Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix E2EE verification backup recovery key"` a retourné une entrée de miroir GitHub pour la couverture de récupération de sauvegarde E2EE destructive PR #71311.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné une discussion de validation de version et bêta Matrix.
