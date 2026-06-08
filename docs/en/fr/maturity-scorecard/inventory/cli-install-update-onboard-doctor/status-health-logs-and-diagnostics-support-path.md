---
title: CLI - Note de maturité de l'observabilité CLI
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# CLI - Note de maturité de l'observabilité CLI

## Résumé

OpenClaw expose une forte observabilité orientée opérateur via `status`, `health`,
`logs`, la stabilité de la passerelle et les chemins d'export de diagnostics. La couverture est solide
car la documentation et les implémentations de commandes sont larges ; la qualité est meilleure que
la moyenne mais toujours limitée par les rapports de blocage et les problèmes de clarté d'état mixte.

## Portée de la catégorie

Cette catégorie couvre les commandes d'observabilité orientées lecture et les diagnostics
de support partageables. Elle ne couvre pas les actions de réparation du doctor ou les commandes
de mutation du cycle de vie de la passerelle.

## Fonctionnalités

- Snapshots d'état : openclaw status et les drapeaux associés résument l'état d'exécution, la santé de la configuration et le contexte de mise à jour.
- Snapshots de santé : openclaw health fournit une lecture rapide de la santé de la passerelle et supporte une sortie détaillée ou JSON.
- Suivi des journaux à distance : openclaw logs suit les journaux de la passerelle via RPC, y compris le mode suivi et la sortie JSON.
- Export de diagnostics : Les bundles de diagnostics de passerelle peuvent être exportés localement pour les rapports de bugs et les flux de travail de support.
- Redaction sûre pour le support : Les chemins de diagnostics et d'état documentent les attentes en matière de confidentialité et de redaction avant de partager les résultats.

## Fraîcheur de l'archive

- gitcrawl: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`, `api_supported=false`, `github_token_present=false`.
- discrawl: `generated_at=2026-05-30T01:10:41Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs :
  - `docs/cli/status.md`, `docs/cli/health.md`, `docs/cli/logs.md` et `docs/gateway/diagnostics.md` documentent clairement les flux opérateur.
  - Les implémentations de status et health sont substantielles dans `src/commands/status.ts`, `src/commands/status.scan.ts`, `src/commands/status.summary.ts` et `src/commands/health.ts`.
  - Les chemins de diagnostics de passerelle et de stabilité sont implémentés via `src/cli/gateway-cli/register.ts` et les méthodes RPC de passerelle sous `src/gateway/server-methods/diagnostics.ts`.
  - La surface d'état a une couverture JSON et de chemin rapide extensive dans ses fichiers de test.
- Signaux négatifs :
  - L'ampleur des commandes d'observabilité augmente la chance de décalages entre les chemins rapides, les chemins profonds et les chemins de sonde de passerelle.
  - Les logs et diagnostics s'étendent sur les couches d'implémentation CLI et passerelle.
- Lacunes d'intégration :
  - Aucune suite e2e CLI large n'a été trouvée qui pilote status, health, logs et l'export de diagnostics ensemble contre une passerelle en direct.

## Score de qualité

- Score : `Beta (74%)`
- Rapports de Gitcrawl :
  - La requête `gitcrawl search issues "status health logs diagnostics" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné des problèmes ouverts incluant `#42252 Improve doctor/gateway diagnostics clarity for mixed LaunchAgent/runtime states` et `#84012 openclaw status CLI command hangs before connecting to gateway`.
- Rapports de Discrawl :
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw status health logs diagnostics"` a retourné des listes de contrôle d'incidents de mainteneur qui dépendent de `gateway diagnostics export`, `gateway stability`, `health`, `gateway status --json` et `logs`.
  - Les résultats d'archive incluent également des exemples d'export de diagnostics réussis avec contenu de bundle redacté et instructions de support.
- Bonnes qualités :
  - Les chemins de status en lecture seule par rapport aux chemins d'état profond sont documentés explicitement.
  - L'export de diagnostics a une histoire claire de confidentialité/redaction.
  - Les opérateurs ont plusieurs chemins pour rassembler des preuves de support limitées sans fouille manuelle du système de fichiers.
- Mauvaises qualités :
  - Les blocages de status et la clarté d'état mixte sont toujours des domaines problématiques actifs.
  - La surface d'observabilité s'étend sur suffisamment de modes pour que certaines confusions d'opérateur restent inévitables.
- Exclus de la qualité :
  - Les suites de test de status, health et diagnostics ci-dessous contribuent à la couverture uniquement.

## Lacunes connues

- Aucun e2e CLI en direct unique pour le chemin complet du bundle de support n'a été trouvé.
- La messagerie d'état mixte entre status, doctor et la réalité du service géré est toujours sous pression.

## Preuves

### Docs

- `docs/cli/status.md`
- `docs/cli/health.md`
- `docs/cli/logs.md`
- `docs/gateway/diagnostics.md`

### Source

- `src/commands/status.ts`
- `src/commands/status.scan.ts`
- `src/commands/status.summary.ts`
- `src/commands/health.ts`
- `src/cli/gateway-cli/register.ts`
- `src/gateway/server-methods/diagnostics.ts`

### Tests d'intégration

- Aucun trouvé pour un flux CLI de bundle de support en direct complet.

### Tests unitaires

- `src/commands/status-json-runtime.test.ts`
- `src/commands/status.scan.test.ts`
- `src/commands/status.scan.fast-json.test.ts`
- `src/commands/status.service-summary.test.ts`
- `src/commands/health.test.ts`
- `src/gateway/server-methods/diagnostics.test.ts`

### Commandes de validation de surface

- `none declared in taxonomy`: `pass` - La surface CLI ne déclare pas de commandes de validation supplémentaires pour la notation.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "status health logs diagnostics" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`

Résultats :

- `[{"number":44297,"state":"open","title":"Surface Slack external arg-menu fallback as a visible health signal","url":"https://github.com/openclaw/openclaw/issues/44297"},{"number":86599,"state":"open","title":"[Bug]: Local model provider calls thread block gateway event loop on Windows beta; trivial infer run takes ~4 minutes","url":"https://github.com/openclaw/openclaw/issues/86599"},{"number":42252,"state":"open","title":"Improve doctor/gateway diagnostics clarity for mixed LaunchAgent/runtime states","url":"https://github.com/openclaw/openclaw/issues/42252"},{"number":48104,"state":"open","title":"Model safety/alignment can block explicitly authorized operational tasks (e.g. SSH diagnostics)","url":"https://github.com/openclaw/openclaw/issues/48104"},{"number":84012,"state":"open","title":"openclaw status CLI command hangs before connecting to gateway (v2026.5.18)","url":"https://github.com/openclaw/openclaw/issues/84012"}]`

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw status health logs diagnostics"`

Résultats :

- Les conseils d'incident de mainteneur dépendent de cette surface pour le débogage de première ligne.
- Les exemples d'archive montrent l'export de diagnostics produisant des bundles assainis avec des snapshots de status, health, logs et stabilité pour les flux de travail de support.
