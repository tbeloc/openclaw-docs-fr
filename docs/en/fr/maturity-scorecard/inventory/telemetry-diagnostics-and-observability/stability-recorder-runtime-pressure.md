---
title: "Observabilité - Note de maturité du Stability Recorder et Runtime Pressure"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de maturité du Stability Recorder et Runtime Pressure

## Résumé

Le stability recorder capture des événements runtime bornés et sans charge utile pour la pression mémoire, les grandes charges utiles, les avertissements de vivacité, l'état de session, l'état de la file d'attente, les appels de modèle, les appels d'outil, Talk, la livraison et la santé de l'exportateur. L'implémentation est prudente concernant la minimisation des données et la rétention bornée, mais la preuve de runtime-pressure est encore plus basée sur la source/test que sur l'opérateur en direct.

## Portée de la catégorie

- Stability recorder en processus borné et RPC `diagnostics.stability`.
- `openclaw gateway stability`, filtrage de stabilité, bundles de stabilité persistants et export-from-bundle.
- Événements de pression mémoire, avertissements de vivacité de la boucle d'événements, événements de charge utile surdimensionnée, résumés de file d'attente/session et snapshots fatals/shutdown/restart.
- Option de snapshot de pression mémoire critique avec preuve V8/cgroup/session-file.

## Fonctionnalités

- Stability recorder en processus borné : Stability recorder en processus borné et RPC diagnostics.stability
- openclaw gateway stability : openclaw gateway stability, filtrage de stabilité, bundles de stabilité persistants et export-from-bundle
- Événements de pression mémoire : Événements de pression mémoire, avertissements de vivacité de la boucle d'événements, événements de charge utile surdimensionnée, résumés de file d'attente/session et snapshots fatals/shutdown/restart
- Option de snapshot de pression mémoire critique : Option de snapshot de pression mémoire critique avec preuve V8/cgroup/session-file

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La projection de stabilité, le filtrage, les résumés mémoire/charge utile et le comportement du bundle persistant ont des tests ciblés et sont exercés par la marche RPC kitchen-sink.
- Signaux négatifs : Les scénarios de sortie fatale, timeout de shutdown, pression mémoire critique et saturation réelle de la boucle d'événements sont plus difficiles à prouver de manière répétée dans les tests locaux.
- Lacunes d'intégration : La preuve au niveau de la version devrait inclure une vraie passerelle produisant et exportant un bundle de stabilité sous pression simulée.

## Score de qualité

- Score : `Stable (80%)`
- Rapports Gitcrawl : La PR #84836 sur les délais d'expiration de récupération retardée est un élément pertinent de signal de pression, mais il n'y a pas un large cluster d'échecs du stability recorder.
- Rapports Discrawl : La requête de fonctionnalité exacte n'a retourné aucun résultat Discord direct, donc le silence de l'archive est neutre après les vérifications de fraîcheur.
- Bonnes qualités : Le recorder assainit les événements, utilise des codes de raison sûrs, limite la rétention, résume les événements mémoire et charge utile-large, et rédige les métadonnées du bundle persistant.
- Mauvaises qualités : Les opérateurs doivent toujours savoir quand inspecter `gateway stability` par rapport à l'export de diagnostics ou aux logs ; cette guidance de premier arrêt est dispersée.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux runtime ne sont comptées que sous Couverture, pas Qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Stability recorder en processus borné, openclaw gateway stability, Événements de pression mémoire, Option de snapshot de pression mémoire critique.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le comportement du bundle de pression mémoire critique est opt-in et devrait avoir une guidance de runbook plus claire.
- `diagnostics.stability` est puissant mais n'est pas encore présenté comme la timeline d'opérateur de premier arrêt principal dans la ligne de scorecard de maturité.

## Preuves

### Docs

- `docs/gateway/diagnostics.md` documente le stability recorder borné, les avertissements de vivacité, `openclaw gateway stability`, les bundles persistants et les options d'export.
- `docs/gateway/health.md` documente la pression mémoire, le délai de la boucle d'événements, les événements de charge utile surdimensionnée et la persistance fatale/restart.
- `docs/gateway/protocol.md` documente `diagnostics.stability` comme un RPC en lecture d'opérateur.

### Source

- `src/logging/diagnostic-stability.ts` implémente le recorder borné, la projection d'événement sans charge utile, le filtrage et les résumés.
- `src/logging/diagnostic-stability-bundle.ts` écrit les bundles persistants avec preuve réduite d'erreur, hôte, V8, cgroup, ressource et session-file.
- `src/gateway/server-methods/diagnostics.ts` expose `diagnostics.stability`.
- `src/gateway/server/event-loop-health.ts` et `src/logging/diagnostic-memory.ts` alimentent les événements de vivacité et mémoire.

### Tests d'intégration

- `scripts/e2e/kitchen-sink-rpc-walk.mjs` appelle `diagnostics.stability` et échoue sur les signaux d'instabilité rejetés/tronqués/fragmentés.
- `src/gateway/gateway-stability.test.ts` exerce les snapshots de stabilité à travers le comportement face à la passerelle.

### Tests unitaires

- `src/logging/diagnostic-stability.test.ts` couvre la projection sans charge utile, l'assainissement des raisons, les résumés mémoire et charge utile large, le filtrage et la rétention bornée.
- `src/logging/diagnostic-stability-bundle.test.ts` couvre le comportement du bundle persistant et la rédaction.
- `src/gateway/server-methods/diagnostics.test.ts` couvre la gestion RPC `diagnostics.stability`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "diagnostics stability memory pressure payload event loop" --limit 5`

Résultats :

- 1 résultat. PR #84836 `fix(gateway): surface delayed fetch timeouts` note la dérive de délai d'expiration retardée comme signal de pression de boucle d'événements pour les consommateurs de diagnostics en aval.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "diagnostics stability memory pressure payload event loop"`

Résultats :

- 0 résultats retournés pour la requête de fonctionnalité exacte.
