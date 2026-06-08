---
title: "Raspberry Pi / small Linux devices - Package Manager and ARM Binary Compatibility Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / small Linux devices - Package Manager and ARM Binary Compatibility Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / small Linux devices` / `Package Manager and Arm Binary Policy` dans l'inventaire du scorecard de la version actuelle du processus (process-version-3).

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Raspberry Pi / small Linux devices représentée par ces fonctionnalités de taxonomie :

- Package Manager and Arm Binary Policy: Portée des preuves pour Package Manager and Arm Binary Policy.

## Fonctionnalités

- npm/pnpm/Bun install modes: Définit la configuration des modes d'installation npm/pnpm/Bun, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Package Manager and ARM Binary Compatibility.
- Installer architecture detection: Définit la configuration de la détection d'architecture du programme d'installation, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Package Manager and ARM Binary Compatibility.
- Optional ARM binary checks: Définit la configuration des vérifications ARM binaires optionnelles, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Package Manager and ARM Binary Compatibility.
- Fallback/build guidance: Définit la configuration des conseils de secours/construction, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Package Manager and ARM Binary Compatibility.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Alpha (68%)`
- Signaux positifs: La documentation d'installation définit Node comme le runtime Gateway, autorise les points d'entrée npm/pnpm/Bun et avertit que Bun n'est pas recommandé pour Gateway. La documentation Raspberry Pi avertit explicitement que les outils CLI Go/Rust optionnels peuvent ne pas être fournis avec des builds ARM.
- Signaux négatifs: La politique du gestionnaire de paquets est répartie entre la documentation d'installation générique, la documentation de plateforme et les notes Raspberry Pi. La gestion des binaires natifs optionnels est surtout une mise en garde plutôt qu'un tableau de compatibilité découvrable.
- Lacunes d'intégration: L'installation smoke valide l'artefact npm général, mais il n'y a pas de matrice binaire native ARM trouvée ou de smoke spécifique au gestionnaire de paquets Pi.

## Score de qualité

- Score: `Alpha (66%)`
- Rapports Gitcrawl: Les résultats d'archive incluent la confusion d'installation npm sur Raspberry Pi et les problèmes de chaîne d'outils ARM/faible mémoire.
- Rapports Discrawl: Les threads QMD, binaire natif et empaquetage ARM montrent des timeouts répétés Pi 5/aarch64 et un comportement natif manquant ou lent.
- Bonnes qualités: La documentation fait de Node le chemin conservateur et avertit explicitement de la variance des binaires ARM.
- Mauvaises qualités: Les utilisateurs rencontrent toujours des problèmes de binaires natifs/groupés après l'installation, et la documentation ne centralise pas les fonctionnalités optionnelles sûres sur arm64.
- Exclus de la qualité: preuves de test unitaire, intégration, e2e, live, runtime-flow et smoke manual.

## Score de complétude

- Score: `Alpha (68%)`
- Instructions de surface: évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Signaux positifs: Les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les modes d'installation npm/pnpm/Bun, la détection d'architecture du programme d'installation, les vérifications ARM binaires optionnelles, les conseils de secours/construction.
- Signaux négatifs: La note archivée a précédé le scoring de complétude de process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les mises en garde visibles par l'opérateur.

## Lacunes connues

- Aucun tableau de compatibilité inspecté ne répertorie les outils optionnels par `linux-arm64`, `aarch64`, `armv7` ou `armv6`.
- Le support de Bun est documenté comme possible pour l'installation CLI mais non recommandé pour le runtime Gateway, ce qui peut toujours être confus sur les petits appareils.
- Les diagnostics du gestionnaire de paquets ne semblent pas préflight la disponibilité des binaires natifs optionnels.

## Preuves

### Docs

- `docs/platforms/linux.md:10-12` dit que Gateway est entièrement supporté sur Linux avec Node.js recommandé et Bun non recommandé.
- `docs/install/index.md:68-106` documente les modes d'installation npm, pnpm et Bun tout en gardant Node recommandé pour le runtime Gateway.
- `docs/install/raspberry-pi.md:193-196` dit que la plupart des fonctionnalités fonctionnent sur ARM64, mais les outils CLI Go/Rust optionnels peuvent ne pas être fournis avec des builds ARM et les opérateurs doivent vérifier `linux-arm64`/`aarch64`.
- `docs/install/installer.md:241-254` documente les drapeaux du programme d'installation pour la version Node et le préfixe npm sur Linux.

### Source

- `scripts/install-cli.sh:338-346` accepte uniquement `arm64`/`aarch64` et `x64` pour le chemin de la tarball Node du préfixe local.
- `scripts/install-cli.sh:391-431` lie un runtime Node local et vérifie `node:sqlite`.
- `scripts/install.sh:1746-1781` gère l'installation Node Alpine Linux et vérifie Node >=22.19.
- `src/daemon/service-env.ts:169-195` porte les emplacements bin du gestionnaire de paquets tels que le préfixe npm, pnpm, Bun et les chemins locaux de l'utilisateur dans les environnements de service.
- `src/daemon/service-env.ts:300-330` résout les chemins bin utilisateur Linux incluant `.local`, `.npm-global`, `.bun`, `.nix-profile` et pnpm.

### Tests d'intégration

- `scripts/docker/install-sh-e2e/run.sh:121-144` exerce la sortie du programme d'installation par rapport à l'artefact npm construit.
- `scripts/docker/install-sh-smoke/run.sh` effectue la validation smoke du programme d'installation.
- Aucun test d'intégration inspecté ne valide les binaires de plugin ou d'assistant ARM natifs optionnels sur le matériel Raspberry Pi.

### Tests unitaires

- La couverture unitaire n'a pas été trouvée pour la politique des binaires ARM optionnels.
- Les tests d'environnement de service couvrent indirectement la propagation du chemin du gestionnaire de paquets, mais pas la sémantique du gestionnaire de paquets Pi.

### Requêtes Gitcrawl

Requête: `gitcrawl search openclaw/openclaw --json --query "ARM binary linux-arm64 aarch64 OpenClaw skill"`

Résultats:

- Aucun thread correspondant retourné.

Requête: `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi low memory OpenClaw"`

Résultats:

- Retourné la confusion d'installation npm globale Raspberry Pi et les rapports liés à ARM/faible mémoire.

### Requêtes Discrawl

Requête: `/Users/kevinlin/.local/bin/discrawl search --limit 5 "ARM binary OpenClaw"`

Résultats:

- Trouvé des rapports selon lesquels OpenClaw CLI est terriblement lent sur Raspberry Pi, les timeouts QMD ARM/Pi 5, les conflits de binaires natifs Oracle ARM et les lacunes binaires QMD sur les plates-formes ARM.

Requête: `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi QMD memory OpenClaw"`

Résultats:

- Trouvé une boucle de timeout d'intégration QMD aarch64 Pi 5 avec le churn de construction node-llama-cpp et une solution de contournement utilisant le mode BM25/search.
