---
title: "Signal - Note de Maturité de Configuration et d'Exploitation des Canaux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Note de Maturité de Configuration et d'Exploitation des Canaux

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Configuration, Installation et Approvisionnement de Compte` dans l'inventaire actuel de la fiche d'évaluation de la version 3 du processus.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Configuration et Exploitation des Canaux`
- Fusionnée à partir de : `Configuration et Santé des Comptes`, `Transport`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du lien QR : Définit le comportement de configuration du lien QR, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Enregistrement SMS : Définit le comportement d'enregistrement SMS, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Configuration de l'installateur et du binaire : Définit le comportement de configuration de l'installateur et du binaire, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Approvisionnement du compte conteneur : Définit le comportement d'approvisionnement du compte conteneur, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Sondes d'état : Définit le comportement des sondes d'état, d'identification, de configuration et de vérification de l'opérateur pour les Diagnostics, État de la Configuration et Garde-fous de l'Opérateur.
- Diagnostics de configuration : Définit le comportement des diagnostics de configuration, d'identification, de configuration et de vérification de l'opérateur pour les Diagnostics, État de la Configuration et Garde-fous de l'Opérateur.
- Garde-fous de sécurité des comptes : Définit le comportement des garde-fous de sécurité des comptes, d'identification, de configuration et de vérification de l'opérateur pour les Diagnostics, État de la Configuration et Garde-fous de l'Opérateur.

## Fonctionnalités

- Configuration du lien QR : Définit le comportement de configuration du lien QR, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Enregistrement SMS : Définit le comportement d'enregistrement SMS, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Configuration de l'installateur et du binaire : Définit le comportement de configuration de l'installateur et du binaire, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Approvisionnement du compte conteneur : Définit le comportement d'approvisionnement du compte conteneur, d'identification, de configuration et de vérification de l'opérateur pour la Configuration, Installation et Approvisionnement de Compte.
- Sondes d'état : Définit le comportement des sondes d'état, d'identification, de configuration et de vérification de l'opérateur pour les Diagnostics, État de la Configuration et Garde-fous de l'Opérateur.
- Diagnostics de configuration : Définit le comportement des diagnostics de configuration, d'identification, de configuration et de vérification de l'opérateur pour les Diagnostics, État de la Configuration et Garde-fous de l'Opérateur.
- Garde-fous de sécurité des comptes : Définit le comportement des garde-fous de sécurité des comptes, d'identification, de configuration et de vérification de l'opérateur pour les Diagnostics, État de la Configuration et Garde-fous de l'Opérateur.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (58%)`

La couverture est Alpha car la documentation et les tests unitaires couvrent la plupart des branches de configuration, mais il n'y a pas de transcription d'enregistrement en direct, de liaison QR, de captcha ou d'approvisionnement de compte liée à la source actuelle.

## Score de Qualité

- Score : `Alpha (62%)`

La qualité est Alpha car la source dispose d'un assistant de configuration cohérent et d'un installateur protégé, mais l'historique de l'opérateur montre toujours des risques d'état de compte et la documentation demande aux utilisateurs de gérer manuellement l'état fragile du compte Signal externe. Exclus de la qualité : preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution ; ceux-ci affectent uniquement la Couverture.

## Score de Complétude

- Score : `Alpha (58%)`
- Instructions de surface : évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration du lien QR, l'enregistrement SMS, la configuration de l'installateur et du binaire, l'approvisionnement du compte conteneur, les sondes d'état, les diagnostics de configuration et les garde-fous de sécurité des comptes.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `docs/channels/signal.md` lignes 1-9 décrivent Signal comme une intégration externe `signal-cli` avec des options de daemon natif et de conteneur.
- `docs/channels/signal.md` lignes 11-28 listent les prérequis, les conseils de numéro séparé, la configuration QR/SMS et l'approbation d'appairage.
- `docs/channels/signal.md` lignes 30-54 documentent la configuration minimale : `account`, `cliPath`, `configPath`, `dmPolicy` et `allowFrom`.
- `docs/channels/signal.md` lignes 80-160 couvrent la liaison QR, l'enregistrement SMS, les commandes d'installation, le captcha, la détection d'état et le risque de déauthentification.
- `docs/channels/signal.md` lignes 185-240 couvrent la configuration du mode conteneur et le `MODE=json-rpc` requis.
- `docs/plugins/reference/signal.md` identifie le paquet comme `@openclaw/signal` et la surface du canal comme `signal`.

### Source

- `extensions/signal/openclaw.plugin.json` déclare le plugin de canal `signal` et le comportement au démarrage.
- `extensions/signal/package.json` expose les champs de configuration CLI tels que `--signal-number`, les options d'hôte/port HTTP, les étiquettes et le chemin de la documentation Signal.
- `src/config/types.signal.ts` définit les champs par compte incluant `account`, `cliPath`, `configPath`, `httpUrl`, `autoStart`, `startupTimeoutMs`, le mode de réception, les groupes, les limites de chunk et les portes de réaction.
- `extensions/signal/src/setup-core.ts` implémente les invites de configuration, l'analyse `allowFrom`, les valeurs par défaut `dmPolicy`, la clé par compte, l'entrée du chemin CLI, la validation du numéro Signal et la note d'achèvement de la sonde d'état.
- `extensions/signal/src/setup-surface.ts` vérifie le binaire local et les comptes configurés, et expose le flux d'installation automatique optionnel.
- `extensions/signal/src/install-signal-cli.ts` télécharge les builds natifs officiels, revient à Homebrew sur macOS et rejette les entrées d'archive non sécurisées.
- `extensions/signal/src/probe.ts` exécute `signalCheck` et `version` pour la détection de configuration/état.

### Tests d'intégration

- Aucun enregistrement en direct, liaison QR, captcha ou approvisionnement de conteneur n'a été trouvé dans `qa/`, `test/` ou l'arborescence de l'extension Signal.
- `extensions/signal/src/probe.contract.test.ts` fournit une couverture d'état au niveau du contrat mais n'exerce pas un compte Signal réel.

### Tests unitaires

- `extensions/signal/src/install-signal-cli.test.ts` couvre la sélection des actifs de version pour Linux, macOS et Windows ; les métadonnées de version mal formées ; le délai d'expiration de la récupération ; l'extraction d'archive et le rejet de zip-slip.
- `extensions/signal/src/core.test.ts` couvre le repli de sonde/version/échec, l'état de configuration pour les chemins CLI par compte/compte par défaut, la suppression d'approbation locale, la construction d'adaptateur durable, la classification des journaux de daemon et l'analyse de configuration pour les listes blanches UUID/wildcard.

### Requêtes Gitcrawl

- Requête : `Signal signal-cli install registration captcha`
  - Résultats : aucun fil d'exécution d'installation ciblé n'a été retourné.
- Requête : `Signal account registered false deletion`
  - Résultats : le problème ouvert `#66119` signale qu'une mise à jour a défini `registered=false` dans un fichier de compte `signal-cli` et a causé la suppression du compte.
- Requête : `Signal signal-cli`
  - Résultats : les résultats plus larges incluent la configuration, le daemon et les problèmes du cycle de vie des comptes, mais pas une transcription d'approvisionnement réussie actuelle.

### Requêtes Discrawl

- Requête : `Signal signal-cli install registration captcha`
  - Résultats : aucune transcription d'opérateur affichée n'a montré une exécution d'installation et d'enregistrement réussie actuelle.
- Requête : `Signal account registered false deletion`
  - Résultats : le contenu du miroir GitHub Discord a répété le problème `#66119`, y compris le résumé de suppression du compte.
- Requête : `Signal dmPolicy pairing allowFrom uuid`
  - Résultats : la discussion d'assistance des 25 et 26 février 2026 a montré que les opérateurs avaient besoin d'aide pour configurer `allowFrom` et l'appairage après la configuration.
