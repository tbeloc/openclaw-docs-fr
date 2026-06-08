---
title: "Observabilité - Note de Maturité de la Collecte de Diagnostics"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité de la Collecte de Diagnostics

## Résumé

L'export de diagnostics est le chemin de rapport de bug partageable pour les opérateurs locaux et les utilisateurs de commandes de chat. Il collecte la forme de configuration assainie, les résumés de journaux, les snapshots de statut et de santé, les bundles de stabilité, les manifestes et les notes de confidentialité. Le modèle de confidentialité est explicite, mais les preuves d'archive incluent au moins une constatation d'examen concernant la redaction des chemins Windows, maintenant la qualité en dessous de Stable.

## Portée de la Catégorie

Inclus dans cette catégorie :

- export de diagnostics de passerelle openclaw : export de diagnostics de passerelle openclaw et options --json / --output / log-size
- openclaw gateway stability --bundle : openclaw gateway stability --bundle latest --export
- Chat /diagnostics : Chat /diagnostics et flux d'approbation /codex diagnostics
- Composition du zip de support : Composition du zip de support, chemins relatifs sûrs, fichiers config/status/health/log/stability assainis, et manifeste de confidentialité
- Enregistreur de stabilité borné en processus : Enregistreur de stabilité borné en processus et diagnostics.stability RPC
- openclaw gateway stability : openclaw gateway stability, filtrage de stabilité, bundles de stabilité persistants, et export-from-bundle
- Événements de pression mémoire : Événements de pression mémoire, avertissements de vivacité de boucle d'événements, événements de charge utile surdimensionnée, résumés de file d'attente/session, et snapshots fatals/arrêt/redémarrage
- Option de snapshot de pression mémoire critique : Option de snapshot de pression mémoire critique avec preuves V8/cgroup/session-file

## Fonctionnalités

- export de diagnostics de passerelle openclaw : export de diagnostics de passerelle openclaw et options --json / --output / log-size
- openclaw gateway stability --bundle : openclaw gateway stability --bundle latest --export
- Chat /diagnostics : Chat /diagnostics et flux d'approbation /codex diagnostics
- Composition du zip de support : Composition du zip de support, chemins relatifs sûrs, fichiers config/status/health/log/stability assainis, et manifeste de confidentialité
- Enregistreur de stabilité borné en processus : Enregistreur de stabilité borné en processus et diagnostics.stability RPC
- openclaw gateway stability : openclaw gateway stability, filtrage de stabilité, bundles de stabilité persistants, et export-from-bundle
- Événements de pression mémoire : Événements de pression mémoire, avertissements de vivacité de boucle d'événements, événements de charge utile surdimensionnée, résumés de file d'attente/session, et snapshots fatals/arrêt/redémarrage
- Option de snapshot de pression mémoire critique : Option de snapshot de pression mémoire critique avec preuves V8/cgroup/session-file

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (76%)`
- Signaux positifs : La composition d'export, la redaction, la gestion des défaillances de snapshot, l'export CLI et l'initiation de commande de chat ont des tests ciblés.
- Signaux négatifs : La preuve complète de commande de chat vers export approuvé est plus étroite que la preuve d'export CLI local.
- Lacunes d'intégration : Les flux de bundle de support doivent être réexécutés sur les formes de chemins macOS, Linux, Windows et le routage privé de chat de groupe.

## Score de Qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : La requête exacte a trouvé un élément de diagnostic de bundle de plugin de support plutôt qu'un défaut d'export direct.
- Rapports Discrawl : Un commentaire d'examen sur la PR #70324 a trouvé une redaction de préfixe de chemin Windows sensible à la casse dans les exports de support, ce qui est un risque de qualité de confidentialité concret.
- Bonnes qualités : L'exportateur utilise des chemins zip sûrs, des écritures de fichiers en mode restreint, des assistants de redaction, des snapshots assainis et des notes de confidentialité du manifeste.
- Mauvaises qualités : Les artefacts de support sont sensibles par nature, et la correction de la redaction doit être maintenue sur les conventions de chemins du système d'exploitation et les champs de snapshot nouvellement ajoutés.
- Exclus de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution sont comptées uniquement sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'export de diagnostics de passerelle openclaw, openclaw gateway stability --bundle, Chat /diagnostics, Composition du zip de support, Enregistreur de stabilité borné en processus, openclaw gateway stability, Événements de pression mémoire, Option de snapshot de pression mémoire critique.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- La documentation avertit les utilisateurs d'examiner les bundles, mais le premier runbook d'arrêt pourrait inclure plus d'exemples pour inspecter le contenu d'export avant de partager.
- La redaction des chemins Windows et des noms d'utilisateur nécessite un examen soutenu car ce chemin est conçu pour le partage de support.

## Preuves

### Docs

- `docs/gateway/diagnostics.md` documente l'export CLI, la commande de chat, le contenu du zip de support, le modèle de confidentialité, l'enregistreur de stabilité, les options utiles et la désactivation des diagnostics.
- `docs/gateway/health.md` pointe les rapports de bugs vers `openclaw gateway diagnostics export`.
- `docs/plugins/codex-harness.md` lie les diagnostics du harnais Codex à la limite d'export de la passerelle.

### Source

- `src/logging/diagnostic-support-export.ts` construit les manifestes, la forme de configuration, les journaux assainis, les snapshots et les fichiers de bundle de stabilité.
- `src/logging/diagnostic-support-bundle.ts` écrit les fichiers de bundle de support sûrs et les archives zip.
- `src/logging/diagnostic-support-redaction.ts` et `src/logging/diagnostic-support-log-redaction.ts` assainissent les chaînes, les chemins, les journaux et les snapshots.
- `src/cli/gateway-cli/register.ts` câble `openclaw gateway diagnostics export` et l'export de stabilité.
- `src/auto-reply/reply/commands-diagnostics.ts` implémente le routage privé `/diagnostics` et le comportement d'approbation.

### Tests d'intégration

- `src/cli/gateway-cli.coverage.test.ts` exerce l'export de diagnostics de passerelle avec des snapshots de santé au meilleur effort.
- `src/agents/bash-tools.exec-host-gateway.test.ts` inclut le chemin de commande exec pour `openclaw gateway diagnostics export --json`.

### Tests unitaires

- `src/logging/diagnostic-support-export.test.ts` vérifie la sortie zip partageable, l'omission des corps de chats/webhooks/secrets bruts, l'assainissement du bundle de stabilité importé, la tolérance aux défaillances de snapshot et la redaction de chemin.
- `src/logging/diagnostic-support-bundle.test.ts` vérifie les chemins de bundle sûrs et l'écriture.
- `src/auto-reply/reply/commands-diagnostics.test.ts` vérifie le comportement de la commande de diagnostics de chat.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "gateway diagnostics export support bundle redaction" --limit 5`

Résultats :

- 1 résultat. La PR #87141 mentionne le support d'inspection du serveur de bundle et le durcissement des diagnostics ; aucun bug d'export actif direct n'a été retourné par cette requête exacte.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "gateway diagnostics export support bundle redaction"`

Résultats :

- 1 résultat. Un commentaire d'examen du 2026-04-22 sur la PR #70324 a signalé que `redactKnownPathPrefixesForSupport` correspondait aux préfixes de chemin Windows de manière sensible à la casse, risquant des fuites de chemin de profil local/nom d'utilisateur lorsque la casse diffère.
