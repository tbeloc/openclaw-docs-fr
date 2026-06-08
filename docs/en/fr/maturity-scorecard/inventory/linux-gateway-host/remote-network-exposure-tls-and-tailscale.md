---
title: "Hôte de passerelle Linux - Note de maturité de l'accès à distance et de la sécurité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hôte de passerelle Linux - Note de maturité de l'accès à distance et de la sécurité

## Résumé

L'accès à distance à la passerelle Linux a des paramètres de sécurité par défaut solides : liaison de loopback, authentification explicite pour l'accès non-loopback, conseils de tunnel SSH, modes Tailscale Serve/Tailnet, exigences TLS pour WebSocket public, conseils d'origine autorisée et runbooks de restauration. La couverture est bêta car la surface s'étend sur plusieurs modes d'exposition et les preuves de support actif montrent toujours une confusion autour de l'authentification Tailscale, du comportement de l'interface de contrôle et du TLS sur l'accès VPS/IP brut.

## Portée de la catégorie

Inclus dans cette catégorie :

- Exposition du réseau distant : Définit l'autorisation d'exposition du réseau distant, la confiance, les limites de sécurité et les contrôles d'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- TLS : Définit l'autorisation TLS, la confiance, les limites de sécurité et les contrôles d'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- Tailscale : Définit l'autorisation Tailscale, la confiance, les limites de sécurité et les contrôles d'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- Protections d'exposition de la passerelle : Définit les vérifications d'exposition, les avertissements de réseau non sécurisé et les contrôles d'opérateur pour les limites de sécurité de la passerelle Linux.
- Modes d'authentification de la passerelle : Définit l'authentification par jeton/mot de passe, la résolution de secret partagé et la vérification d'opérateur pour l'authentification de la passerelle Linux.
- Gestion des secrets : Définit la configuration de la gestion des secrets, les identifiants, la configuration et le comportement de vérification d'opérateur pour la sécurité, l'authentification et la gestion des secrets.

## Fonctionnalités

- Exposition du réseau distant : Définit l'autorisation d'exposition du réseau distant, la confiance, les limites de sécurité et les contrôles d'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- TLS : Définit l'autorisation TLS, la confiance, les limites de sécurité et les contrôles d'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- Tailscale : Définit l'autorisation Tailscale, la confiance, les limites de sécurité et les contrôles d'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- Protections d'exposition de la passerelle : Définit les vérifications d'exposition, les avertissements de réseau non sécurisé et les contrôles d'opérateur pour les limites de sécurité de la passerelle Linux.
- Modes d'authentification de la passerelle : Définit l'authentification par jeton/mot de passe, la résolution de secret partagé et la vérification d'opérateur pour l'authentification de la passerelle Linux.
- Gestion des secrets : Définit la configuration de la gestion des secrets, les identifiants, la configuration et le comportement de vérification d'opérateur pour la sécurité, l'authentification et la gestion des secrets.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`
- Justification : le modèle de sécurité est documenté et implémenté, mais la surface d'opérateur inclut plusieurs choix de déploiement et couches d'identité qui ne sont pas encore regroupés dans un seul flux de décision d'accès à distance Linux simple.
- Lacunes : Le comportement de l'interface de contrôle via l'accès Tailscale/VPS et les règles TLS pour les points de terminaison publics bruts restent dispersés dans les runbooks et les discussions de support.

## Score de qualité

- Score : `Bêta (74%)`
- Justification : les protections expédiées sont solides, mais les preuves d'archive montrent un travail actif des utilisateurs et des responsables autour de l'authentification Tailscale, des avertissements et de l'accès à l'interface utilisateur à distance.
- Exclu de la qualité : preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-gateway-host.md`.
- Signaux positifs : les preuves d'archives, de source, de test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'exposition du réseau distant, TLS, Tailscale, les protections d'exposition de la passerelle, les modes d'authentification de la passerelle, la gestion des secrets.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un sélecteur d'accès à distance Linux unique couvrant le tunnel SSH, Tailscale Serve, la liaison directe tailnet, la liaison LAN et le TLS public.
- Clarifier le comportement de l'interface de contrôle et les attentes d'authentification pour les opérateurs Tailscale/VPS.

## Preuves

### Docs

- `docs/gateway/remote.md:8-17` définit l'accès à distance de la passerelle et l'exposition en loopback en premier via Tailscale, LAN ou SSH.
- `docs/gateway/remote.md:67-86` documente l'utilisation du tunnel SSH et les drapeaux explicites de jeton/mot de passe.
- `docs/gateway/remote.md:125-142` documente la précédence des identifiants pour l'accès local et distant.
- `docs/gateway/remote.md:157-177` documente la valeur par défaut du loopback, le `ws://` privé, le `wss://` public, l'authentification non-loopback, le comportement de fermeture défaillante de SecretRef, les empreintes TLS et les détails de Tailscale Serve.
- `docs/gateway/tailscale.md:9-21` documente les modes Serve et Funnel tout en gardant la passerelle liée au loopback.
- `docs/gateway/security/exposure-runbook.md:52-110` documente les vérifications de base et la configuration sûre minimale.

### Source

- `src/gateway/net.ts:262-317` résout les hôtes de liaison loopback, tailnet, LAN, personnalisés et conscients des conteneurs.
- `src/gateway/net.ts:319-338` garde Tailscale Serve sur loopback et définit le mode conteneur séparément par défaut.
- `src/gateway/server-tailscale.ts:19-55` démarre Serve/Funnel et enregistre les URL servies ou les défaillances.
- `src/shared/gateway-bind-url.ts:13-47` résout les URL de liaison pour les modes personnalisés, tailnet et LAN.
- `src/gateway/auth-resolve.ts:31-105` résout le mode d'authentification de la passerelle, les entrées de jeton/mot de passe et le comportement d'authentification Tailscale.
- `src/security/audit-gateway-exposure.test.ts:39-187` enregistre les attentes d'audit d'exposition pour les drapeaux dangereux, les liaisons non-loopback, les origines de caractères génériques et la solution de secours d'en-tête d'hôte.

### Tests d'intégration

- `src/config/config.gateway-tailscale-bind.test.ts` couvre la configuration de liaison Tailscale.
- `src/gateway/server-tailscale.test.ts` couvre le comportement du processus Serve/Funnel.
- `src/security/audit-gateway-exposure.test.ts` couvre les cas de risque d'exposition qui importent pour les hôtes distants Linux.

### Tests unitaires

- `src/shared/gateway-bind-url.test.ts` couvre la résolution d'URL de liaison distante.
- `src/shared/tailscale-status.test.ts` couvre l'analyse de l'état Tailscale.
- `src/security/audit-gateway-http-auth.test.ts` et `src/security/audit-gateway-auth-selection.test.ts` couvrent la sélection d'authentification et le comportement d'audit d'exposition HTTP.

### Requêtes Gitcrawl

- La requête spécifique `gateway bind tailnet Tailscale TLS allowed origins remote access Linux` n'a retourné aucun résultat.
- La requête plus large `tailnet Tailscale` a retourné le problème #57110 pour l'authentification secondaire optionnelle en mode Tailscale Serve, le problème #85750 pour l'avatar de l'interface de contrôle 401 via Tailscale, la PR #73163 pour les avertissements d'accès à l'interface de contrôle non sécurisée, le problème #56118 pour le nœud distant sur le proxy du navigateur VPS/tailnet et la PR #81306 pour garder la liaison loopback explicite épinglée.

### Requêtes Discrawl

- La requête `Tailscale tailnet OpenClaw gateway` a trouvé le problème d'état Tailscale #71123 et la PR #71354, plus les conseils d'opérateur tels que `sudo tailscale set --operator=$USER`, `openclaw gateway restart`, `tailscale serve status` et `sudo tailscale serve --bg --yes 18789`.
- La requête `gateway run port` a trouvé des conseils de support selon lesquels l'accès public iOS/VPS nécessite `wss://` plutôt que l'accès WebSocket brut non sécurisé.
