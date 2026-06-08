---
title: "Signal - Diagnostics, Config Status, and Operator Guardrails Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Diagnostics, Config Status, and Operator Guardrails Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Diagnostics, Config Status, and Operator Guardrails` dans l'inventaire de scorecard actuel process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Signal représentée par ces fonctionnalités de taxonomie :

- Diagnostics, Config Status, and Operator Guardrails: Portée des preuves pour Diagnostics, Config Status, and Operator Guardrails.

## Fonctionnalités

- Status probes: Définit le comportement de configuration, d'authentification, de configuration et de vérification d'opérateur pour Status probes dans Diagnostics, Config Status, and Operator Guardrails.
- Setup diagnostics: Définit le comportement de configuration, d'authentification, de configuration et de vérification d'opérateur pour Setup diagnostics dans Diagnostics, Config Status, and Operator Guardrails.
- Account safety guardrails: Définit le comportement de configuration, d'authentification, de configuration et de vérification d'opérateur pour Account safety guardrails dans Diagnostics, Config Status, and Operator Guardrails.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Alpha (55%)`

La couverture est Alpha car la documentation et le code source couvrent la configuration, le statut et le dépannage, mais les transcriptions de statut en direct, doctor, account-state et failure-mode sont minces.

## Score de qualité

- Score: `Alpha (60%)`

La qualité est Alpha car les vérifications de statut et de configuration existent, mais l'historique des opérateurs montre que les probes peuvent réussir tandis que le chemin de réception est cassé, et les protections account-state restent trop dépendantes de l'état externe `signal-cli`. Exclus de la qualité : les preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution ; celles-ci affectent uniquement la couverture.

## Score de complétude

- Score: `Alpha (55%)`
- Instructions de surface: évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs: la documentation archivée, le code source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Status probes, Setup diagnostics, Account safety guardrails.
- Signaux négatifs: la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Docs

- `docs/channels/signal.md` lignes 103-160 couvrent la configuration multi-compte, l'enregistrement SMS, les commandes d'installation, le captcha, les probes doctor/status et les avertissements d'appairage.
- `docs/channels/signal.md` lignes 346-363 listent les vérifications de dépannage pour le chemin binaire, la liste des comptes, la probe de statut et les vérifications supplémentaires.
- `docs/channels/signal.md` lignes 367-372 documentent les notes de sécurité et d'isolation des comptes.

### Source

- `src/config/types.signal.ts` définit les champs de configuration typés pour les comptes, le mode API, le comportement de réception, le délai d'expiration du démarrage, les contrôles de groupe, les limites et les réactions.
- `extensions/signal/src/setup-surface.ts` rapporte le statut binaire et de compte dans la surface de configuration.
- `extensions/signal/src/setup-core.ts` émet des conseils de fin de configuration qui indiquent aux opérateurs d'exécuter le statut du canal.
- `extensions/signal/src/probe.ts` enveloppe `signalCheck` et `version` pour le statut.
- `extensions/signal/src/monitor/tool-result.ts` limite la disponibilité au démarrage et gère les défaillances de sortie du daemon.
- `extensions/signal/src/daemon.ts` classe les logs daemon courants et expose l'état stop/exited.

### Tests d'intégration

- `extensions/signal/src/probe.contract.test.ts` couvre le contrat de probe.
- Aucun `channels.status` en direct, `channel doctor`, récupération de compte ou transcript de failure-mode n'a été trouvé dans `qa/`, `test/` ou `tests`.

### Tests unitaires

- `extensions/signal/src/core.test.ts` couvre la fallback de probe/version/failure et le statut de configuration avec les comptes configurés.
- `extensions/signal/src/monitor.tool-result.autostart.test.ts` couvre les délais d'expiration de disponibilité, les remplacements de délai d'expiration de démarrage, la sortie du daemon pendant le démarrage et l'arrêt après abandon.
- `extensions/signal/src/daemon.test.ts` couvre la classification des logs.
- `extensions/signal/src/install-signal-cli.test.ts` couvre le comportement du programme d'installation gardé qui affecte la sécurité de la configuration de l'opérateur.

### Requêtes Gitcrawl

- Requête: `Signal inbound SSE listener wedged channels status`
  - Résultats: le problème ouvert `#75426` rapporte un état où la sortie et la probe fonctionnaient tandis que l'inbound était bloqué et `channels status` a expiré.
- Requête: `Signal account registered false deletion`
  - Résultats: le problème ouvert `#66119` rapporte une mutation de fichier de compte menant à la suppression du compte.
- Requête: `Signal support Note-to-Self linked-device`
  - Résultats: la PR ouverte `#75890` suit le mode linked-device Note-to-Self, montrant l'expansion continue du mode opérateur.

### Requêtes Discrawl

- Requête: `Signal account registered false deletion`
  - Résultats: le contenu du miroir Discord GitHub a répété le problème `#66119` et le résumé de suppression de compte.
- Requête: `Signal inbound SSE listener wedged channels status`
  - Résultats: le contenu du miroir Discord correspondait au problème `#75426`, renforçant que le comportement de statut/probe n'est pas suffisant pour prouver la santé de la réception.
- Requête: `Signal support Note-to-Self linked-device`
  - Résultats: aucun transcript d'opérateur affiché n'a prouvé que le mode linked-device avait été déployé et exercé.
