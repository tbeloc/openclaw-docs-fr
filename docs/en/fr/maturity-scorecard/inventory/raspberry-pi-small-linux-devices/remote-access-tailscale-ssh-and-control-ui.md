---
title: "Raspberry Pi / small Linux devices - Remote Access and Auth Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / small Linux devices - Remote Access and Auth Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / small Linux devices` / `Remote Access, Tailscale, Ssh, and Control UI` dans l'inventaire de scorecard de la version actuelle du processus-version-3.

## Portée de la catégorie

Inclus dans cette catégorie :

- Authentification Headless API-key : Définit l'assemblage du contexte d'authentification Headless API-key, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Authentification Gateway shared-secret : Définit l'assemblage du contexte d'authentification Gateway shared-secret, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Approbations Device pairing : Définit l'assemblage du contexte des approbations Device pairing, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Gestion SecretRef : Définit l'assemblage du contexte de gestion SecretRef, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Récupération Token drift : Définit l'assemblage du contexte de récupération Token drift, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Accès SSH tunnel dashboard : Définit la configuration de l'accès SSH tunnel dashboard, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.
- Tailscale Serve/Funnel : Définit la configuration de Tailscale Serve/Funnel, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.
- Contrôles d'exposition Loopback/non-loopback : Définit la configuration des contrôles d'exposition Loopback/non-loopback, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.
- Accès Authenticated Control UI : Définit la configuration de l'accès Authenticated Control UI, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.

## Fonctionnalités

- Authentification Headless API-key : Définit l'assemblage du contexte d'authentification Headless API-key, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Authentification Gateway shared-secret : Définit l'assemblage du contexte d'authentification Gateway shared-secret, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Approbations Device pairing : Définit l'assemblage du contexte des approbations Device pairing, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Gestion SecretRef : Définit l'assemblage du contexte de gestion SecretRef, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Récupération Token drift : Définit l'assemblage du contexte de récupération Token drift, la persistance, la gestion de la pression des jetons et le comportement de récupération pour Gateway Auth, Device Pairing, et Secrets.
- Accès SSH tunnel dashboard : Définit la configuration de l'accès SSH tunnel dashboard, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.
- Tailscale Serve/Funnel : Définit la configuration de Tailscale Serve/Funnel, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.
- Contrôles d'exposition Loopback/non-loopback : Définit la configuration des contrôles d'exposition Loopback/non-loopback, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.
- Accès Authenticated Control UI : Définit la configuration de l'accès Authenticated Control UI, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Remote Access et Control UI.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : Les docs Gateway remote, Tailscale docs, et Raspberry Pi docs couvrent les tunnels SSH, les défauts loopback, Tailscale Serve/Funnel, la précédence d'authentification, les garde-fous non-loopback, et l'accès Control UI.
- Signaux négatifs : Les cas limites reverse-proxy et Tailscale/Pi apparaissent dans les problèmes GitHub, et le smoke test d'accès distant spécifique au matériel est absent.
- Lacunes d'intégration : Les tests de réseau Gateway existent, mais aucun test inspecté ne cible le comportement Raspberry Pi plus Tailscale ou SSH tunnel.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : les problèmes incluent les besoins de nom d'hôte pour laptop/server/Pi, les problèmes de contexte sécurisé reverse-proxy sur Linux/Pi/home server/VPS sans interface graphique, et les problèmes de plugin-loader Pi Tailscale-reachable.
- Rapports Discrawl : Les workflows Pi 5 Docker/Tailscale Serve et device approval sont discutés par les utilisateurs.
- Bonnes qualités : Les défauts de sécurité sont conservateurs : loopback et SSH/Tailscale sont le chemin le plus sûr, non-loopback nécessite une authentification, et Funnel public est protégé par mot de passe.
- Mauvaises qualités : L'histoire d'accès distant est puissante mais multi-couches, donc les problèmes de support impliquent souvent les règles de contexte sécurisé du navigateur, les en-têtes d'authentification, et le mode d'exposition tailnet/public.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, live, runtime-flow, et smoke test manuel.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Signaux positifs : les preuves docs archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour l'authentification Headless API-key, l'authentification Gateway shared-secret, les approbations Device pairing, la gestion SecretRef, la récupération Token drift, l'accès SSH tunnel dashboard, Tailscale Serve/Funnel, les contrôles d'exposition Loopback/non-loopback, l'accès Authenticated Control UI.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version-3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun smoke Pi plus Tailscale Serve récurrent n'a été trouvé.
- Le comportement du reverse proxy et du contexte sécurisé n'est pas résumé dans le guide Raspberry Pi.
- L'accès Control UI distant dépend de plusieurs docs plutôt que d'un flux de petit appareil.

## Preuves

### Docs

- `docs/install/raspberry-pi.md:107-128` vérifie l'état de Gateway et montre le tunneling SSH vers Control UI, avec un lien Tailscale.
- `docs/gateway/remote.md:8-16` encadre loopback, Tailscale Serve, et SSH comme les chemins distants principaux.
- `docs/gateway/remote.md:67-86` documente l'accès SSH tunnel et les identifiants explicites.
- `docs/gateway/remote.md:157-175` indique que loopback plus SSH/Tailscale est le plus sûr, les liaisons non-loopback nécessitent une authentification, et les SecretRefs échouent fermés.
- `docs/gateway/tailscale.md:9-17` décrit les modes Serve/Funnel.
- `docs/gateway/tailscale.md:92-127` documente les exigences de mot de passe Funnel public et les prérequis.

### Source

- `src/shared/gateway-bind-url.ts:21-46` résout les URL de liaison personnalisées, tailnet, et LAN et les erreurs.
- `src/gateway/auth-resolve.ts:31-105` résout le jeton Gateway auth, le mot de passe, et les autorisations Tailscale.
- `src/cli/gateway-cli/run.ts:25-48` le comportement est documenté dans les docs CLI soutenus par la source, y compris les garde-fous d'authentification non-loopback.

### Tests d'intégration

- `package.json:1653` définit `test:docker:gateway-network`.
- `package.json:1677`, `package.json:1678`, et `package.json:1679` définissent les entrées de test Gateway Docker live.
- Aucun test inspecté ne combine le matériel Raspberry Pi avec SSH ou Tailscale.

### Tests unitaires

- Les tests de liaison/authentification Gateway couvrent le comportement de la politique, mais aucun fixture d'accès distant spécifique à Pi n'a été trouvé.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi Tailscale gateway"`

Résultats :

- A retourné le problème #56276 sur la surface des noms d'hôte pour laptop/server/Raspberry Pi, le problème #53274 sur le contexte sécurisé sur les déploiements reverse-proxy HTTP pour Linux/Raspberry Pi/home server/VPS sans interface graphique, et le problème #78196 sur les plugins d'extension ignorés par une Gateway Pi Tailscale-reachable.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi device pairing OpenClaw"`

Résultats :

- A trouvé un plan Pi 5 Docker plus Tailscale Serve impliquant l'approbation d'appareil, ainsi que l'historique du support device-token et pairing.
