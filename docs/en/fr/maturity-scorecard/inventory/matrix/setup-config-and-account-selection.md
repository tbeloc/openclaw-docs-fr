---
title: "Matrix - Channel Setup and Operations Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Channel Setup and Operations Maturity Note

## Résumé

La configuration de Matrix a un vrai contrat de plugin groupé : métadonnées du manifeste, métadonnées du package, points d'entrée de configuration, configuration étendue au compte, raccourcis d'environnement, contrôles de réseau privé, paramètres de proxy, sélection de compte par défaut, auto-adhésion aux invitations, listes blanches et amorçage du chiffrement sont tous représentés dans la documentation, le code source et les tests. La couverture est Beta car il existe des preuves larges de configuration et d'assurance qualité, mais pas une seule matrice d'installation en direct qui exerce chaque variante de compte et d'environnement. La qualité est Beta car la structure est mature mais la surface est large et liée au risque opérationnel actif de Matrix.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Channel Setup and Operations`
- Fusionnée à partir de : `Setup and Repair`, `Runtime Lifecycle`
- Score reporté : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Identité du plugin Matrix : identité du plugin Matrix, métadonnées d'installation, entrées de runtime/configuration et configuration du compte.
- Assistant de configuration : assistant de configuration, adaptateur de configuration, validation, amorçage post-écriture et configuration du compte.
- Découverte de compte : découverte de compte, règles de compte par défaut, comptes soutenus par env et métadonnées de compte stockées.
- Avertissements Matrix doctor : avertissements Matrix doctor, normalisation de la configuration et nettoyage de la configuration de plugin obsolète.
- Sonde/statut Matrix : sonde/statut Matrix, recherche de répertoire en direct, diagnostics CLI et statut runtime d'assurance qualité.
- Résolution du client Matrix partagé : résolution du client Matrix partagé et cycle de vie du client actif
- Démarrage du moniteur : démarrage du moniteur, statut de synchronisation, gestion des arrêts fatals, suivi des tâches et comportement du gestionnaire d'événements.
- Maintenance au démarrage : maintenance au démarrage pour la synchronisation des profils, vérifications de vérification, restauration de sauvegarde et réparation au démarrage.
- Avertissements Matrix doctor : couvre les avertissements Matrix doctor, la normalisation de la configuration, le comportement de nettoyage de la configuration de plugin obsolète.
- Sonde/statut Matrix : couvre la sonde/statut Matrix, la recherche de répertoire en direct, les diagnostics CLI et le comportement runtime d'assurance qualité.
- Démarrage du moniteur : démarrage du moniteur, statut de synchronisation, gestion des arrêts fatals, suivi des tâches et comportement du gestionnaire d'événements
- Maintenance au démarrage : maintenance au démarrage pour la synchronisation des profils, vérifications de vérification, restauration de sauvegarde et réparation au démarrage

## Fonctionnalités

- Identité du plugin Matrix : identité du plugin Matrix, métadonnées d'installation, entrées de runtime/configuration et configuration du compte.
- Assistant de configuration : assistant de configuration, adaptateur de configuration, validation, amorçage post-écriture et configuration du compte.
- Découverte de compte : découverte de compte, règles de compte par défaut, comptes soutenus par env et métadonnées de compte stockées.
- Avertissements Matrix doctor : avertissements Matrix doctor, normalisation de la configuration et nettoyage de la configuration de plugin obsolète.
- Sonde/statut Matrix : sonde/statut Matrix, recherche de répertoire en direct, diagnostics CLI et statut runtime d'assurance qualité.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - La documentation couvre les sources d'installation, le flux de configuration, les options d'authentification, les variables env étendues au compte, les valeurs par défaut d'auto-adhésion aux invitations, les listes blanches et les valeurs par défaut multi-compte.
  - Le code source contient des métadonnées de manifeste/package, un schéma de configuration typé, des assistants de sélection de compte, des capacités de configuration, un proxy d'assistant de configuration, un adaptateur de configuration et un amorçage post-écriture.
  - Les tests unitaires et runtime couvrent les raccourcis env, la promotion de compte, les invites de réseau privé, les listes blanches, les cibles d'invitation stables, l'ambiguïté du compte par défaut, la validation de la configuration et l'amorçage du chiffrement après la configuration.
  - Les preuves d'intégration incluent le runtime d'assurance qualité Matrix injectant un compte Matrix temporaire et dérivant la configuration de la passerelle DM plus multi-room.
- Signaux négatifs :
  - Je n'ai pas trouvé une seule voie d'installation ou de mise à niveau en direct récurrente qui exerce toutes les variantes de configuration ensemble : ClawHub, npm, source locale, identifiants stockés, identifiants soutenus par env, comptes nommés, proxy, opt-in de réseau privé, auto-adhésion et amorçage du chiffrement.
  - Les requêtes de configuration gitcrawl et discrawl étroites n'ont retourné aucun résultat de problème spécifique à la configuration, donc les preuves d'archive ne sont pas assez approfondies pour prouver la stabilité de la configuration du monde réel par elles-mêmes.
- Lacunes d'intégration :
  - Ajouter une matrice de configuration en direct couvrant la source d'installation, le mode de compte, l'authentification env/stockée, le proxy, le réseau privé, l'auto-adhésion et l'amorçage du chiffrement.
  - Ajouter un scénario de mise à niveau récurrent qui commence à partir de la configuration Matrix de niveau supérieur hérité et vérifie la promotion de compte plus la sélection du compte par défaut.
  - Lier la sortie du statut de configuration aux vérifications de disponibilité de la passerelle après l'amorçage post-écriture.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux runtime réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "matrix setup account config autoJoin"` n'a retourné aucun résultat.
  - La requête `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné des résultats opérationnels Matrix larges, incluant les problèmes ouverts #68188 pour les messages Matrix configurés n'atteignant pas la session de l'agent et #83142 pour l'analyse des mentions.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix setup account config autoJoin"` n'a retourné aucun résultat.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné une discussion de version et de scorecard mentionnant la validation du canal Matrix et l'approche de notation du scorecard de maturité.
- Bonnes qualités :
  - La documentation sépare clairement l'installation, la configuration, l'authentification, les variables env du compte, les variables env de clé de récupération, l'opt-in du serveur d'accueil privé/LAN, le proxy, les règles de compte par défaut et la résolution de cible.
  - Le schéma de configuration utilise des structures imbriquées typées de compte/action/thread/approbation/réseau au lieu de clés ad hoc.
  - La sélection de compte échoue fermée lorsque plusieurs comptes existent sans un compte par défaut explicite.
  - Le code de configuration sépare le chargement de configuration paresseux de la mutation d'état de configuration et de l'amorçage post-écriture.
- Mauvaises qualités :
  - La configuration est répartie sur la documentation, CLI, l'adaptateur de configuration, la résolution de compte, la découverte d'identifiants soutenus par env et l'amorçage runtime, ce qui crée de nombreux cas limites visibles par l'opérateur.
  - Les rapports d'archive Matrix larges montrent que les défaillances de compte configuré de bout en bout sont possibles même lorsque la configuration semble complète.
  - La configuration du réseau privé et du proxy reste intrinsèquement risquée car elle touche à la politique SSRF et à la disponibilité du réseau local.
- Exclu de la qualité :
  - Je n'ai pas augmenté ou diminué la qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct ou runtime.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou runtime comme entrée de notation.

## Score d'exhaustivité

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'identité du plugin Matrix, l'assistant de configuration, la découverte de compte, les avertissements Matrix doctor, la sonde/statut Matrix.
- Signaux négatifs : la note archivée a précédé la notation d'exhaustivité de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un seul rapport d'assurance qualité de configuration qui mappe la source d'installation, le mode d'authentification, le mode de compte, le mode réseau, l'auto-adhésion et l'amorçage du chiffrement à la disponibilité de la passerelle observée.
- Ajouter des preuves de scorecard pour le comportement de configuration ClawHub et npm, pas seulement le comportement de checkout de source.
- Maintenir la documentation et les exemples de schéma de configuration en synchronisation pour les variables env étendues au compte et les variables env de clé de récupération.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:12` documente
  l'installation à partir de ClawHub, npm, ou une extraction locale.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:30` documente la configuration,
  les choix d'authentification, le flux de l'assistant, le raccourci env, et l'amorçage E2EE.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:81` documente
  le comportement `autoJoin` désactivé par défaut et les listes blanches d'invitations.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:130` documente
  la dénomination des variables env du compte Matrix et les variables env de clé de récupération.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:710` documente
  le comportement multi-compte et compte par défaut.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:758` documente
  l'opt-in du serveur d'accueil privé/LAN et la configuration du proxy.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/openclaw.plugin.json:1`
  déclare l'id du plugin Matrix fourni, l'alias de commande, le canal, les variables env, et
  le schéma de configuration.
- `/Users/kevinlin/code/openclaw/extensions/matrix/package.json:32` déclare
  les métadonnées de l'extension Matrix, l'entrée de configuration, le chemin de la documentation du canal, les capacités,
  les spécifications d'installation, et la compatibilité des versions.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/config-schema.ts:14`
  définit l'action Matrix, la liaison de thread, l'approbation exec, la salle, le réseau, et le
  schéma de configuration racine.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/account-selection.ts:139`
  résout les ids de compte, les comptes configurés, et les exigences de compte par défaut.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/channel.setup.ts:12`
  expose les capacités de configuration, le comportement de rechargement, et les hooks du schéma de configuration.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/setup-core.ts:45`
  implémente le proxy de l'assistant de configuration et l'adaptateur de configuration.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/accounts.ts:145`
  résout l'activation du compte, le serveur d'accueil, l'id utilisateur, les identifiants en cache, et
  la configuration du compte.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/runtime.test.ts:202`
  vérifie l'injection temporaire de compte Matrix dans la configuration de la passerelle QA.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/runtime.test.ts:275`
  vérifie la configuration dérivée de DM Matrix et multi-salle à partir de la topologie provisionnée.
- `/Users/kevinlin/code/openclaw/src/commands/agents.bind.matrix.integration.test.ts:21`
  vérifie la résolution de la liaison du plugin Matrix lorsque l'id de compte est omis.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/onboarding.test.ts:28`
  couvre la configuration du raccourci env pour les comptes non-défaut.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/onboarding.test.ts:70`
  couvre la configuration du raccourci env via l'auto-adhésion aux invitations.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/onboarding.test.ts:317`
  couvre les écritures de liste blanche et d'accès aux salles.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/onboarding.test.ts:477`
  couvre les invites de compte par défaut pour plusieurs comptes nommés.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/setup-core.test.ts:284`
  couvre le passage d'un compte à l'authentification basée sur env.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/setup-core.test.ts:412`
  couvre l'opt-in de configuration de réseau privé.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/channel.setup.test.ts:133`
  couvre l'amorçage de vérification pour les comptes chiffrés nouvellement ajoutés.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/account-selection.test.ts:44`
  couvre les exigences explicites par défaut pour plusieurs comptes.

### Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "matrix setup account config autoJoin"`
  n'a retourné aucun résultat.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné des
  résultats Matrix larges, incluant #68188, #83142, #73480, #85620, #87307, #81892,
  #80432, #76611, et les PRs ouvertes associées.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix setup account config autoJoin"`
  n'a retourné aucun résultat.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"`
  a retourné des discussions de version référençant le comportement de mention Matrix et une
  discussion de mainteneur sur l'approche de notation de la scorecard de maturité.
