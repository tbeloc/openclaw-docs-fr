---
title: "Linux Gateway host - Security, Auth, and Secret Handling Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Linux Gateway host - Security, Auth, and Secret Handling Maturity Note

## Résumé

La sécurité de Linux Gateway dispose de contrôles par défaut stables : liaison en loopback, authentification requise pour l'accès non-loopback, modes token/password, support SecretRef, résolution fail-closed des entrées secrètes, authentification du fournisseur sur l'hôte Gateway, audit d'exposition et credentials CLI distants explicites. La qualité est bêta car les preuves d'archive montrent toujours des diagnostics SecretRef et des décalages de résolution auth status-vs-Gateway.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Linux Gateway représentée par ces fonctionnalités de taxonomie :

- Security, Auth, and Secret Handling: Portée des preuves pour Security, Auth, and Secret Handling.

## Fonctionnalités

- Gateway exposure safeguards: Définit les vérifications d'exposition, les avertissements unsafe-network et les contrôles d'opérateur pour les limites de sécurité de Linux Gateway.
- Gateway authentication modes: Définit l'authentification token/password, la résolution de secret partagé et la vérification d'opérateur pour l'authentification de Linux Gateway.
- Secret Handling: Définit le comportement de configuration, credential et vérification d'opérateur pour Secret Handling, Security, Auth, and Secret Handling.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Justification : la documentation et le code source couvrent l'authentification Gateway, les credentials distants, le placement env du fournisseur de modèle, les SecretRefs, le filtrage des entrées secrètes, les gardes non-loopback et l'audit d'exposition.
- Lacunes : le comportement de l'opérateur SecretRef est documenté mais dispersé sur les pages secrets, authentication, doctor, remote et CLI.

## Score de qualité

- Score : `Beta (76%)`
- Justification : le modèle de sécurité est solide, mais les preuves d'archive actives montrent un décalage de diagnostic SecretRef et une dérive de résolution status/deep-probe qui peuvent induire en erreur les opérateurs Linux.
- Exclus de la qualité : preuves de tests unitaires, intégration, e2e, live et runtime-flow.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-gateway-host.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour Gateway exposure safeguards, Gateway authentication modes, Secret Handling.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aligner le comportement `status --deep`, doctor, Gateway runtime et service install pour les SecretRefs d'authentification Gateway.
- Rendre les causes d'échec SecretRef explicites pour les environnements de service Linux, en particulier les chemins de fournisseur de fichiers sous `/etc`.

## Preuves

### Docs

- `docs/gateway/authentication.md:23-58` explique l'authentification du fournisseur sur l'hôte Gateway et le placement d'environnement pour systemd/launchd.
- `docs/gateway/secrets.md:11-38` documente les SecretRefs, le risque de texte brut, le comportement de snapshot runtime, les références actives fail-fast et le rechargement atomique.
- `docs/gateway/secrets.md:66-100` documente le filtrage de surface active et les diagnostics SecretRef d'authentification/remote Gateway.
- `docs/gateway/secrets.md:112-163` documente les contrats SecretRef env/file/exec.
- `docs/gateway/remote.md:125-177` documente la précédence des credentials, le comportement fail-closed SecretRef, les règles TLS/public et les limites d'authentification Tailscale Serve.
- `docs/gateway/security/exposure-runbook.md:74-110` documente la configuration d'exposition distante minimale sûre.

### Source

- `src/gateway/auth-resolve.ts:31-105` résout le mode d'authentification configuré, l'entrée token/password et le comportement d'authentification Tailscale.
- `src/gateway/credentials-secret-inputs.ts:55-86` résout les chaînes d'entrée secrète et détecte les SecretRefs Gateway configurés.
- `src/gateway/credentials-secret-inputs.ts:110-181` gère les chemins du mode d'authentification local et le comportement de sentinelle path-can-win.
- `src/cli/daemon-cli/install.ts:220-239` résout et persiste les tokens d'installation Gateway.
- `src/cli/gateway-cli/run.ts:223-232` applique l'authentification explicite avant la liaison non-loopback.

### Tests d'intégration

- `src/commands/doctor-gateway-services.test.ts` couvre la persistance du token de service Gateway et le comportement de réparation lié à l'authentification.
- `src/cli/daemon-cli/install.integration.test.ts` couvre le comportement d'authentification/token au moment de l'installation.
- `src/gateway/server.auth.default-token.test.ts` et `src/gateway/server.auth.modes.suite.ts` couvrent les modes d'authentification Gateway.

### Tests unitaires

- `src/gateway/resolve-configured-secret-input-string.test.ts` couvre la résolution SecretRef.
- `src/config/types.secrets.resolution.test.ts` et `src/config/types.secrets.test.ts` couvrent le comportement de configuration secrète.
- `src/cli/command-secret-gateway.test.ts` et `src/commands/gateway-install-token.test.ts` couvrent les flux CLI secret/token.
- `src/security/audit-gateway-auth-selection.test.ts` couvre la sélection d'authentification pour l'audit d'exposition.

### Requêtes Gitcrawl

- La requête spécifique `Gateway token SecretRef service env auth Linux control UI origins exposure` n'a retourné aucun résultat.
- La requête plus large `SecretRef token` a retourné le problème #77687 pour le rapport doctor Gateway auth SecretRef indisponible alors qu'il se résout, PR #84224 pour la gestion des SecretRefs Gateway dans les vérifications d'authentification, PR #77698 pour la résolution des SecretRefs de token Gateway, PR #68280 pour la sonde locale fail-fast auth, problème #65201 pour les avertissements de token d'authentification faux et problème #81547 pour la résolution SecretRef CLI/TUI à partir des fournisseurs de fichiers `/etc`.

### Requêtes Discrawl

- La requête `Gateway auth token SecretRef` a trouvé une discussion du mainteneur du 2026-05-29 sur le problème #87815 où `status --deep` résout les SecretRefs de statut mais pas le token/password d'authentification Gateway.
- La même requête a trouvé une discussion de PR #84224 et des avertissements doctor faux quand `gateway.auth.token` est configuré comme un SecretRef.
