---
title: "Raspberry Pi / small Linux devices - Gateway Auth, Device Pairing, and Secrets Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / small Linux devices - Gateway Auth, Device Pairing, and Secrets Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / small Linux devices` / `Device Pairing, Secrets, and Operator Auth` dans l'inventaire de scorecard actuel de la version 3 du processus.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Raspberry Pi / small Linux devices représentée par ces fonctionnalités de taxonomie :

- Device Pairing, Secrets, and Operator Auth : Portée des preuves pour Device Pairing, Secrets, and Operator Auth.

## Fonctionnalités

- Headless API-key auth : Définit l'assemblage du contexte Headless API-key auth, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, and Secrets.
- Gateway shared-secret auth : Définit l'assemblage du contexte Gateway shared-secret auth, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, and Secrets.
- Device pairing approvals : Définit l'assemblage du contexte Device pairing approvals, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, and Secrets.
- SecretRef handling : Définit l'assemblage du contexte SecretRef handling, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, and Secrets.
- Token drift recovery : Définit l'assemblage du contexte Token drift recovery, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, and Secrets.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : L'appairage de passerelle, le CLI de périphérique, les SecretRefs, la configuration des clés API et la priorité de l'authentification à distance sont documentés et soutenus par la source. La documentation Raspberry Pi recommande les clés API plutôt que OAuth pour les configurations sans interface.
- Signaux négatifs : Les flux de travail d'authentification spécifiques à Raspberry Pi sont assemblés à partir de plusieurs documents, et les rapports d'archive montrent des problèmes de jeton obsolète et d'OAuth Codex sur les déploiements Pi/systemd.
- Lacunes d'intégration : Les flux d'appairage/authentification ont une couverture dans les suites Gateway/device, mais aucun test de fumée d'authentification matérielle Pi inspecté n'a été trouvé.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : Les rapports SecretRef et Pi/systemd existent, y compris une mention de chemin SecretRef managed-systemd Raspberry Pi 5 aarch64.
- Rapports Discrawl : Les utilisateurs Pi rencontrent des boucles d'appairage obligatoire, des jetons de périphérique obsolètes, des ruptures d'appairage de périphérique `/tmp`/plugin, et des défaillances d'authentification Codex sous systemd.
- Bonnes qualités : La documentation recommande des clés API prévisibles pour les hôtes de longue durée et les SecretRefs échouent fermés.
- Mauvaises qualités : L'authentification sans interface reste un domaine de support utilisateur fréquent car elle combine l'appairage de périphérique, l'authentification Gateway, la persistance systemd, les jetons CLI et l'authentification de canal/outil.
- Exclus de la qualité : preuves de test unitaire, intégration, e2e, en direct, flux d'exécution et test de fumée manuel.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Headless API-key auth, Gateway shared-secret auth, Device pairing approvals, SecretRef handling, Token drift recovery.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun démarrage rapide Raspberry Pi ne consolide l'authentification Gateway, l'appairage de périphérique, les SecretRefs et les identifiants de canal dans un flux vérifié unique.
- La récupération de jeton de périphérique obsolète est documentée dans la documentation CLI, mais les rapports d'archive Pi montrent que les utilisateurs restent bloqués.
- Aucun fixture d'authentification systemd Pi ou test de fumée matériel n'a été trouvé.

## Preuves

### Docs

- `docs/install/raspberry-pi.md:92-104` recommande les clés API plutôt que OAuth pour les configurations sans interface et appelle Telegram le plus facile pour un Pi sans interface.
- `docs/gateway/authentication.md:13-19` dit que les clés API sont les plus prévisibles pour les hôtes Gateway toujours actifs.
- `docs/gateway/authentication.md:23-43` indique aux utilisateurs de mettre les clés dans `~/.openclaw/.env` pour systemd/launchd.
- `docs/gateway/secrets.md:11-20` décrit les SecretRefs comme un moyen de réduire l'exposition des identifiants en texte brut.
- `docs/gateway/secrets.md:93-108` couvre les diagnostics d'authentification Gateway et la validation d'intégration pour les SecretRefs.
- `docs/gateway/pairing.md:25-44` décrit la demande en attente, l'approbation, l'émission de jeton, la reconnexion et le flux de travail CLI convivial sans interface.
- `docs/cli/devices.md:51-83` documente le flux d'approbation de périphérique et l'aperçu de la dernière demande.

### Source

- `src/gateway/auth-resolve.ts:31-105` résout le jeton/mot de passe/défaut d'authentification Gateway et l'autorisation Tailscale.
- `src/gateway/credentials-secret-inputs.ts:55-86` résout SecretInput et les SecretRefs configurés.
- `src/gateway/credentials-secret-inputs.ts:110-181` détermine si les chemins SecretRef Gateway peuvent gagner.
- `src/commands/status.gateway-probe.ts:8-21` résout l'authentification de sonde Gateway.

### Tests d'intégration

- Les flux d'authentification Gateway et d'appairage de périphérique sont couverts par les suites Gateway/device, mais aucun test d'intégration inspecté n'est étiqueté pour Raspberry Pi.
- Aucun test de fumée d'authentification matérielle n'a été trouvé pour Pi plus systemd plus appairage de périphérique.

### Tests unitaires

- Le comportement d'authentification, SecretRef et d'appairage a des tests ciblés au niveau de la source dans les zones Gateway/device.
- Aucun fixture unitaire n'a modélisé le stockage des identifiants systemd Pi/headless.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi device pairing gateway token"`

Résultats :

- Aucun fil correspondant retourné.

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi systemd Gateway auth SecretRef"`

Résultats :

- RP retourné #78555, avec des extraits mentionnant les affectations SecretRef `sibling_ref` et une Gateway managed-systemd Pi 5 aarch64 `rpi-2712`.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi device pairing OpenClaw"`

Résultats :

- Sortie Pi `devices list` trouvée, boucles d'appairage obligatoire/native, `/tmp` lecture seule cassant le comportement de mémoire/plugin/device pairing, plans d'approbation Pi 5 Docker/Tailscale Serve, décalage de jeton de périphérique obsolète et luttes de configuration Pi 5 Ollama/Gateway/Telegram locales.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi Codex auth systemd"`

Résultats :

- Historique de support systemd Pi/Linux trouvé avec défaillances OAuth Codex répétées.
