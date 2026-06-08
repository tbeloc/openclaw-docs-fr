---
title: "Windows via WSL2 - Wsl Networking and Portproxy Exposure Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - Wsl Networking and Portproxy Exposure Maturity Note

## Résumé

La mise en réseau WSL est documentée et partiellement supportée par le comportement d'exécution conscient de WSL2, mais elle reste l'un des principaux points de douleur des opérateurs. La documentation explique comment modifier les adresses IP WSL, le `portproxy` Windows, les règles de pare-feu, les adresses d'écoute LAN et les URL de passerelle accessibles. Les preuves archivées montrent toujours des défaillances de Tailscale, de nœud Android, de relais Chrome, d'interface de contrôle et de portproxy où le réseau virtuel WSL et le pare-feu Windows rendent difficile l'atteinte d'une configuration OpenClaw correcte.

## Portée de la catégorie

- Réseau virtuel WSL et modification de l'adresse IP WSL.
- Configuration de `netsh interface portproxy` Windows et actualisation.
- Règles du pare-feu Windows pour les ports transférés.
- URL de passerelle qui doivent être accessibles à partir des nœuds distants.
- Sémantique des adresses d'écoute LAN par rapport à la boucle locale.
- Comportement de la famille réseau IPv4 spécifique à WSL2.
- Accès à distance Tailscale uniquement où il croise la mise en réseau WSL2.

## Fonctionnalités

- Réseau virtuel WSL : comportement du réseau virtuel WSL et adressage hôte/invité.
- Configuration de portproxy Windows : configuration de netsh interface portproxy Windows pour exposer les services WSL.
- Règles du pare-feu Windows : règles du pare-feu Windows pour l'accès à la passerelle WSL.
- URL de passerelle accessibles : URL de passerelle qui doivent être accessibles à partir des clients Windows, WSL2 et LAN.
- Exposition de boucle locale et LAN : comportement d'écoute de boucle locale par rapport à LAN pour l'exposition de la passerelle WSL2.
- Mise en réseau IPv4 WSL2 : comportement de la famille réseau IPv4 spécifique à WSL2.
- Accès à distance Tailscale : comportement de Tailscale et d'accès à distance où il croise la mise en réseau WSL2.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`
- Signaux positifs : la documentation Windows inclut un runbook portproxy avec des commandes PowerShell, la configuration du pare-feu, les étapes d'actualisation et les avertissements concernant les URL des nœuds distants ; la documentation sur l'accès à distance et l'exposition explique les modèles de boucle locale/Tailscale/tunnel ; la source gère la sélection IPv4 spécifique à WSL2.
- Signaux négatifs : la documentation couvre le chemin manuel, mais la source ne possède pas le cycle de vie de portproxy Windows ou l'état du pare-feu Windows.
- Lacunes d'intégration : aucun e2e de mise en réseau WSL2 n'a été trouvé qui prouve l'accessibilité de la passerelle à partir de l'hôte Windows, du périphérique LAN, du périphérique tailnet et du nœud distant après les modifications d'adresse IP WSL.

## Score de qualité

- Score : `Alpha (65%)`
- Rapports Gitcrawl : `WSL2 portproxy Gateway Windows host` a retourné la PR #74163 avec des entrées d'actualisation de problèmes Microsoft incluant les défaillances de portproxy Windows et les déconnexions de passerelle de plateforme Windows. `Windows WSL2 OpenClaw` a retourné les problèmes #54669, #73152, #81873, #80336, #73836 et #86752 touchant l'accessibilité WSL2 et la réactivité de la passerelle.
- Rapports Discrawl : la recherche WSL2 portproxy a retourné des rapports d'accessibilité Tailscale/Android, des rapports de défaillance de relais de nœud-hôte WSL2, des défaillances de liaison de relais Chrome et des conseils d'assistance indiquant que les configurations brutes de portproxy et les configurations Tailscale doubles sont fragiles.
- Bonnes qualités : la documentation est explicite sur la modification des adresses IP WSL, la configuration du pare-feu et la différence entre les adresses d'écoute locales uniquement et LAN.
- Mauvaises qualités : le produit ne peut pas abstraire de manière fiable le pare-feu Windows, le mode de mise en réseau WSL, l'actualisation de portproxy et le routage tailnet ; les utilisateurs ont toujours besoin d'un dépannage réseau multicouche.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution sont exclues de ce score de qualité.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/windows-via-wsl2.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le réseau virtuel WSL, la configuration de portproxy Windows, les règles du pare-feu Windows, les URL de passerelle accessibles, l'exposition de boucle locale et LAN, la mise en réseau IPv4 WSL2, l'accès à distance Tailscale.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin de vérifications `doctor` ou `status` qui peuvent identifier les cibles portproxy obsolètes et les blocages de pare-feu.
- Besoin d'un modèle WSL2 + Tailscale recommandé dans la documentation de la plateforme Windows, pas seulement des conseils généraux sur Tailscale.
- Besoin de preuves en direct pour l'accessibilité de l'hôte Windows, du périphérique LAN et du périphérique tailnet par rapport à une passerelle WSL2.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:138` : la section portproxy explique que WSL a son propre réseau virtuel.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:140` : la documentation indique que les services à l'intérieur de WSL nécessitent le transfert d'un port Windows vers l'adresse IP WSL actuelle.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:152` : le runbook obtient l'adresse IP WSL en utilisant `wsl -d $Distro -- hostname -I`.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:155` : le runbook ajoute une règle `netsh interface portproxy` v4-to-v4.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:159` : le runbook ajoute une règle du pare-feu Windows.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:176` : les notes indiquent que les nœuds distants ont besoin d'une URL de passerelle accessible, pas `127.0.0.1`.
- `/Users/kevinlin/code/openclaw/docs/gateway/remote.md:15` : la documentation distante décrit la liaison de boucle locale plus Tailscale, LAN/tailnet de confiance ou le transfert SSH.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/exposure-runbook.md:24` : le runbook d'exposition compare les modèles de boucle locale, Tailscale Serve, liaison tailnet/LAN, proxy et publics.

### Source

- `/Users/kevinlin/code/openclaw/src/infra/net/undici-family-policy.ts:12` : WSL2 désactive la sélection automatique de famille car WSL2 a une connectivité IPv6 instable.
- `/Users/kevinlin/code/openclaw/src/infra/wsl.ts:40` : la détection WSL2 identifie les noyaux WSL2 standard Microsoft.
- `/Users/kevinlin/code/openclaw/src/infra/browser-open.ts:68` : la gestion de l'ouverture du navigateur Linux vérifie si le processus s'exécute sous WSL.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/gateway-network/client.mjs` : le client e2e gateway-network exerce les chemins d'accessibilité réseau.
- `/Users/kevinlin/code/openclaw/scripts/e2e/gateway-network-docker.sh` : l'e2e gateway-network Docker existe pour le comportement réseau général, mais pas pour portproxy WSL2/Windows.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/infra/net/undici-global-dispatcher.test.ts:621` : WSL2 désactive `autoSelectFamily` dans la configuration du dispatcher.
- `/Users/kevinlin/code/openclaw/src/infra/net/fetch-guard.ssrf.test.ts` : les tests de garde SSRF/fetch utilisent la simulation de politique de famille WSL2.
- `/Users/kevinlin/code/openclaw/src/infra/net/ssrf.dispatcher.test.ts:129` : les tests du dispatcher SSRF réutilisent la politique auto-famille WSL2 globale pour les dispatchers épinglés.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "WSL2 portproxy Gateway Windows host" --mode keyword --limit 10 --json`
- `gitcrawl search openclaw/openclaw --query "Windows WSL2 OpenClaw" --mode keyword --limit 12 --json`

Résultats :

- La requête portproxy a retourné la PR #74163, incluant les entrées d'actualisation de problèmes Microsoft pour les défaillances de portproxy Windows et les déconnexions de passerelle de plateforme Windows.
- La requête Windows WSL2 OpenClaw a retourné 12 résultats incluant la demande de documentation WSL/VM/Tailscale #73152, le problème de profil de navigateur #81873, le problème IPv6/portproxy #54669, l'accessibilité de passerelle d'espace réservé #80336, l'arrêt de passerelle WSL2 #61616, la privation de ressources de boucle d'événement Docker/WSL2 #86752 et les rapports de réactivité de l'interface de contrôle/passerelle.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 portproxy Gateway Windows host"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 systemd gateway install loginctl portproxy"`

Résultats :

- La requête WSL2 portproxy a retourné 8 résultats, incluant les défaillances d'accessibilité WSL2 + Tailscale Android, les rapports de relais d'extension Chrome, la confusion d'appairage de nœud-hôte WSL2 et les conseils d'utiliser Tailscale Serve hôte Windows uniquement ou portproxy avec prudence.
- La requête systemd/install/portproxy plus large a retourné un résumé d'assistance listant la mise en réseau WSL2, les E/S de fichiers, le démarrage automatique et les compromis d'intégration native Windows.
