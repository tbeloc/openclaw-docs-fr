---
title: "Windows via WSL2 - Gateway Access and Exposure Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - Gateway Access and Exposure Maturity Note

## Summary

L'authentification et les secrets sont solides au niveau de la couche Gateway, mais l'exposition WSL2 rend la posture de l'opérateur plus délicate. Le même token/mot de passe Gateway, SecretRef, `.env`, URL distante, loopback, tunnel SSH, Tailscale et les règles d'audit de sécurité s'appliquent. Le risque spécifique à WSL2 est que l'hôte Gateway est Linux à l'intérieur d'une VM Windows, tandis que Control UI, Chrome, hôtes node, clients téléphone et les points d'entrée portproxy/Tailscale peuvent se trouver en dehors de cette VM.

## Category Scope

Inclus dans cette catégorie :

- Authentification par token/mot de passe Gateway : authentification par token et mot de passe Gateway pour les clients s'exécutant via WSL2.
- Identifiants du fournisseur : stockage et recherche des identifiants du fournisseur depuis l'environnement WSL2.
- SecretRefs d'authentification Gateway : gestion des SecretRef d'authentification Gateway pour les processus Gateway hébergés sur WSL2.
- Précédence des identifiants d'URL distante : précédence des identifiants d'URL distante lorsque les clients WSL2 se connectent à des Gateways locaux ou distants.
- Réseau virtuel WSL : comportement du réseau virtuel WSL et adressage hôte/invité.
- Configuration Windows portproxy : configuration de netsh interface portproxy Windows pour exposer les services WSL.
- Règles Windows Firewall : règles Windows Firewall pour l'accès Gateway WSL.
- URLs Gateway accessibles : URLs Gateway qui doivent être accessibles depuis les clients Windows, WSL2 et LAN.
- Exposition loopback et LAN : comportement d'écoute loopback par rapport à LAN pour l'exposition Gateway WSL2.
- Réseau IPv4 WSL2 : comportement spécifique à WSL2 de la famille de réseau IPv4.
- Accès distant Tailscale : comportement de Tailscale et d'accès distant où il intersecte la mise en réseau WSL2.

## Features

- Authentification par token/mot de passe Gateway : authentification par token et mot de passe Gateway pour les clients s'exécutant via WSL2.
- Identifiants du fournisseur : stockage et recherche des identifiants du fournisseur depuis l'environnement WSL2.
- SecretRefs d'authentification Gateway : gestion des SecretRef d'authentification Gateway pour les processus Gateway hébergés sur WSL2.
- Précédence des identifiants d'URL distante : précédence des identifiants d'URL distante lorsque les clients WSL2 se connectent à des Gateways locaux ou distants.
- Réseau virtuel WSL : comportement du réseau virtuel WSL et adressage hôte/invité.
- Configuration Windows portproxy : configuration de netsh interface portproxy Windows pour exposer les services WSL.
- Règles Windows Firewall : règles Windows Firewall pour l'accès Gateway WSL.
- URLs Gateway accessibles : URLs Gateway qui doivent être accessibles depuis les clients Windows, WSL2 et LAN.
- Exposition loopback et LAN : comportement d'écoute loopback par rapport à LAN pour l'exposition Gateway WSL2.
- Réseau IPv4 WSL2 : comportement spécifique à WSL2 de la famille de réseau IPv4.
- Accès distant Tailscale : comportement de Tailscale et d'accès distant où il intersecte la mise en réseau WSL2.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Beta (76%)`
- Positive signals: Gateway auth, SecretRef runtime behavior, `.env` service guidance, remote credential precedence, exposure runbook, and security audit docs are explicit; source/tests cover gateway-auth SecretRef activation, active-surface reasoning, and redaction.
- Negative signals: WSL2-specific auth proof is mostly inferred from general Gateway/Linux behavior plus WSL2 support reports.
- Integration gaps: no WSL2-specific exposure/auth scorecard was found for token auth, node-host pairing from Windows, Tailscale Serve, portproxy, Control UI device auth, and security audit in one flow.

## Quality Score

- Score: `Beta (73%)`
- Gitcrawl reports: `WSL2 SecretRef token auth Gateway` returned 0 hits, while broader WSL2 queries returned node-host/Control UI and gateway reachability issues where auth and exposure are part of the operator diagnosis.
- Discrawl reports: WSL2 SecretRef/auth search returned unresolved SecretRef runtime logs in WSL2, WSL2 Gateway token auth excerpts, and Windows node-host pairing/relay guidance. Portproxy/Tailscale searches returned reports where the Gateway is loopback/token protected inside WSL2 but external clients cannot route to it cleanly.
- Good qualities: source treats Gateway auth SecretRefs as active startup inputs, remote credentials require explicit handling, and docs discourage direct public exposure.
- Bad qualities: WSL2 makes "gateway host" ambiguous for users, especially when credentials are set in Windows PowerShell while the Gateway service reads Linux `.env`, or when Windows node hosts try to connect through loopback/portproxy.
- Excluded from quality: unit, integration, e2e, live, and runtime-flow test evidence is excluded from this Quality score.

## Completeness Score

- Score: `Beta (76%)`
- Surface instructions: evaluated against `references/completeness/windows-via-wsl2.md`.
- Positive signals: archived docs, source, test, Gitcrawl, and Discrawl evidence cover the taxonomy scope for Gateway token/password auth, Provider credentials, Gateway auth SecretRefs, Remote URL credential precedence, WSL virtual network, Windows portproxy setup, Windows Firewall rules, Reachable Gateway URLs, Loopback and LAN exposure, WSL2 IPv4 networking, Tailscale remote access.
- Negative signals: the archived note predated process-version-3 Completeness scoring, so this score is initialized from the same evidence breadth and known-gap record used for the archived Coverage score.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Besoin d'exemples spécifiques à WSL2 pour l'authentification des hôtes node Windows et le réappairage par rapport à une Gateway WSL2.
- Besoin de diagnostics qui expliquent quand l'authentification est configurée correctement mais que le routage Windows/WSL empêche le client d'atteindre la Gateway.
- Besoin de docs de plateforme Windows pour lier l'exposition portproxy/Tailscale au runbook d'exposition Gateway et à la liste de contrôle d'audit de sécurité.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/authentication.md:31`: les clés API du fournisseur doivent être placées sur l'hôte Gateway.
- `/Users/kevinlin/code/openclaw/docs/gateway/authentication.md:38`: les services Gateway systemd/launchd doivent lire les clés du fournisseur depuis `~/.openclaw/.env`.
- `/Users/kevinlin/code/openclaw/docs/gateway/secrets.md:11`: les SecretRefs évitent de stocker les identifiants pris en charge en texte brut dans la configuration.
- `/Users/kevinlin/code/openclaw/docs/gateway/secrets.md:27`: les secrets se résolvent en un snapshot d'exécution en mémoire et le démarrage échoue rapidement pour les refs actifs non résolus.
- `/Users/kevinlin/code/openclaw/docs/gateway/secrets.md:81`: les SecretRefs de token/mot de passe Gateway distants sont actifs pour les surfaces en mode distant ou d'exposition distante.
- `/Users/kevinlin/code/openclaw/docs/gateway/remote.md:84`: les appels `--url` explicites nécessitent un token/mot de passe explicite et ne reviennent pas aux identifiants de configuration/env.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/exposure-runbook.md:11`: le runbook d'exposition avertit de comprendre la réachabilité, l'authentification, les agents et les outils avant d'exposer la Gateway.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/exposure-runbook.md:24`: les modèles d'exposition définissent loopback, Tailscale Serve, liaison tailnet/LAN, proxy et risque public.

### Source

- `/Users/kevinlin/code/openclaw/src/secrets/runtime-gateway-auth-surfaces.ts:6`: les chemins de surface SecretRef d'authentification Gateway incluent les champs de token/mot de passe locaux et distants.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-gateway-auth-surfaces.ts:60`: la source évalue quelles surfaces d'authentification Gateway sont actives.
- `/Users/kevinlin/code/openclaw/src/gateway/auth.ts:344`: l'authentification Gateway évalue les origines de navigateur autorisées dans le cadre du contexte d'authentification.
- `/Users/kevinlin/code/openclaw/src/gateway/server.config-patch.test.ts:266`: la réponse de configuration masque les URLs CDP de navigateur portant des identifiants.
- `/Users/kevinlin/code/openclaw/src/gateway/net.ts:482`: les URLs `ws://` non-loopback sont traitées comme non sécurisées car les identifiants peuvent traverser le réseau.

### Integration tests

- `/Users/kevinlin/code/openclaw/src/secrets/runtime.gateway-auth.integration.test.ts:36`: le test d'intégration échoue rapidement lorsque le SecretRef d'authentification Gateway actif n'est pas résolu.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime.gateway-auth.integration.test.ts:67`: le test d'intégration rejette les refs d'authentification Gateway actifs non résolus avant de les persister.
- `/Users/kevinlin/code/openclaw/src/security/audit-gateway-exposure.test.ts`: l'audit d'exposition de gateway a une couverture au niveau du code source.

### Unit tests

- `/Users/kevinlin/code/openclaw/src/gateway/auth.test.ts:354`: les tests d'authentification couvrent `token_missing`.
- `/Users/kevinlin/code/openclaw/src/gateway/call.test.ts:991`: les tests d'appel rejettent les URLs distantes `ws://` non sécurisées.
- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.control-ui.suite.ts`: la suite d'authentification Control UI couvre l'identité de l'appareil, l'appairage et le comportement du token/mot de passe.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-gateway-local-surfaces.test.ts`: les tests de secrets couvrent le comportement de surface locale Gateway.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-gateway-auth-surfaces.test.ts`: les tests de secrets couvrent l'activation de surface d'authentification Gateway.

### Gitcrawl queries

Query:

- `gitcrawl search openclaw/openclaw --query "WSL2 SecretRef token auth Gateway" --mode keyword --limit 10 --json`
- `gitcrawl search openclaw/openclaw --query "WSL2 portproxy Gateway Windows host" --mode keyword --limit 10 --json`
- `gitcrawl search openclaw/openclaw --query "Windows WSL2 OpenClaw" --mode keyword --limit 12 --json`

Results:

- WSL2 SecretRef/token/auth returned 0 hits.
- WSL2 portproxy/Gateway returned PR #74163 with Windows portproxy/gateway platform context.
- Windows WSL2 OpenClaw returned WSL2 reachability and Control UI/Gateway issues, including #81873, #54669, #61616, #73836, #80336, #86752, and #87387.

### Discrawl queries

Query:

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 SecretRef token auth Gateway"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 portproxy Gateway Windows host"`

Results:

- SecretRef/token/auth query returned WSL2 Gateway logs with unresolved SecretRef diagnostics, WSL2 token-auth Gateway startup output, and auto-family WSL2 network policy logs.
- Portproxy/Gateway query returned WSL2 + Tailscale and Windows node-host reports where token auth and pairing were present but cross-host reachability or relay setup remained unclear.
