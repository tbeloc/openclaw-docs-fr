---
title: "Observabilité - Note de Maturité de la Journalisation"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité de la Journalisation

## Résumé

La surface de journalisation est un outil d'opérateur puissant : les journaux de fichiers JSONL, les styles de console, les enregistreurs de sous-système, la rédaction, la journalisation Control UI et CLI, la RPC de passerelle `logs.tail`, le comportement de secours et la corrélation de trace sont documentés et implémentés. Le principal risque de qualité est la cohérence à long terme sur chaque récepteur qui peut afficher des journaux ou des charges utiles d'outils.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Journaux de fichiers JSONL de la passerelle roulante : Journaux de fichiers JSONL de la passerelle roulante et sortie console
- Journaux openclaw : journaux openclaw, openclaw logs --follow, modes JSON/plain/color/timezone et comportement de secours local
- Passerelle RPC logs.tail : comportement logs.tail, statut et vérification visible par l'opérateur.
- Modèles de rédaction et récepteurs : console, journaux de fichiers, enregistrements de journaux OTLP, texte de transcription, événements d'appel d'outil Control UI, exports de support et journaux de protocole WS
- Champs de corrélation de trace : Champs de corrélation de trace sur les enregistrements de journaux et les événements de diagnostic liés.

## Fonctionnalités

- Journaux de fichiers JSONL de la passerelle roulante : Journaux de fichiers JSONL de la passerelle roulante et sortie console
- Journaux openclaw : journaux openclaw, openclaw logs --follow, modes JSON/plain/color/timezone et comportement de secours local
- Passerelle RPC logs.tail : comportement logs.tail, statut et vérification visible par l'opérateur.
- Modèles de rédaction et récepteurs : console, journaux de fichiers, enregistrements de journaux OTLP, texte de transcription, événements d'appel d'outil Control UI, exports de support et journaux de protocole WS
- Champs de corrélation de trace : Champs de corrélation de trace sur les enregistrements de journaux et les événements de diagnostic liés.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs : La journalisation dispose de docs dédiées, de tests CLI, de tests unitaires log-tail, de tests de rédaction, de tests de transport et de validation de gestionnaire RPC.
- Signaux négatifs : Il y a moins de preuve end-to-end du rendu des journaux Control UI et du comportement de tail distant que du chemin CLI/file-log principal.
- Lacunes d'intégration : Le suivi des journaux de passerelle distante et le secours du journal systemd sont testés au niveau unitaire CLI mais nécessitent une preuve récurrente sur hôte réel.

## Score de Qualité

- Score : `Stable (84%)`
- Rapports Gitcrawl : Le résultat principal de l'archive est la PR #74252, un correctif de rapport de rotation de journaux, qui indique une maintenance active plutôt qu'une défaillance systémique de la journalisation.
- Rapports Discrawl : La requête de fonctionnalité exacte n'a retourné aucun résultat Discord direct, donc le silence de l'archive est neutre après les vérifications de fraîcheur.
- Bonnes qualités : L'implémentation limite les lectures de tail de journaux, rédige avant de retourner les lignes, valide les paramètres RPC, gère les fichiers rotatifs et a un comportement de secours local explicite.
- Mauvaises qualités : La politique de rédaction s'étend sur de nombreux récepteurs, donc les régressions peuvent apparaître lorsque de nouvelles surfaces de diagnostic contournent les aides partagées.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution sont comptées uniquement sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les journaux de fichiers JSONL de la passerelle roulante, les journaux openclaw, la passerelle RPC logs.tail, les modèles de rédaction et récepteurs, les champs de corrélation de trace.
- Signaux négatifs : la note archivée a précédé la notation de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Le rendu des journaux Control UI est moins directement représenté dans la piste de preuve que la journalisation CLI et RPC tail.
- La documentation de l'opérateur pourrait mieux croiser les drapeaux de diagnostics ciblés de la page de journalisation principale.

## Preuves

### Docs

- `docs/logging.md` documente les journaux de fichiers, la journalisation CLI, les journaux Control UI, les formats, les niveaux de journalisation, les diagnostics de transport de modèle ciblés, la corrélation de trace et la rédaction.
- `docs/gateway/logging.md` documente les surfaces de journalisation de passerelle, la configuration du logger de fichier, la capture de console, les styles de journalisation WS et le formatage des sous-systèmes.
- `docs/cli/logs.md` documente les drapeaux `openclaw logs`, le secours local, le secours du journal systemd et le comportement de retry.

### Source

- `src/logging/logger.ts`, `src/logging/subsystem.ts`, `src/logging/config.ts`, `src/logging/redact.ts` et `src/logging/log-tail.ts` implémentent la création de journaux, la configuration, la rédaction et la journalisation.
- `src/gateway/server-methods/logs.ts` expose `logs.tail` avec validation de schéma et lectures limitées.
- `src/cli/logs-cli.ts` implémente le formatage CLI, le secours local, le secours du journal systemd et le comportement de retry.
- `src/gateway/ws-logging.ts` implémente les modes de journalisation du protocole WS de passerelle.

### Tests d'intégration

- `src/cli/gateway-rpc.runtime.test.ts` mappe `openclaw logs` à `logs.tail`.
- `src/cli/logs-cli.test.ts` exerce le comportement de secours et de suivi CLI contre les limites gateway/runtime simulées.

### Tests unitaires

- `src/logging/log-tail.test.ts` vérifie la rédaction et le comportement de tail.
- `src/logging/redact.test.ts`, `src/logging/logger-redaction-behavior.test.ts`, `src/logging/logger-settings.test.ts`, `src/logging/logger-transport.test.ts` et `src/logging/parse-log-line.test.ts` couvrent les aides de journalisation et de rédaction principales.
- `src/gateway/server-methods/server-methods.test.ts` couvre la validation RPC `logs.tail` et les réponses.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "logging logs tail redaction request trace" --limit 5`

Résultats :

- 2 résultats. La PR #74252 corrige le rapport de rotation de journaux, et la PR #87141 inclut le renforcement de la journalisation de trace du cycle de vie du plugin.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "logging logs tail redaction request trace"`

Résultats :

- 0 résultats retournés pour la requête de fonctionnalité exacte.
