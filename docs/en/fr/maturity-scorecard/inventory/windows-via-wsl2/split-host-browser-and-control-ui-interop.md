---
title: "Windows via WSL2 - Browser and Control UI Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - Browser and Control UI Maturity Note

## Résumé

L'interopérabilité du navigateur split-host et de l'interface utilisateur de contrôle dispose d'un runbook dédié solide, mais reste une véritable zone de risque bêta. La topologie commune est claire : la passerelle s'exécute dans WSL2, l'interface utilisateur de contrôle s'ouvre à partir de localhost Windows, et Chrome Windows est contrôlé via CDP distant brut accessible depuis WSL2. La qualité reste bêta car les preuves d'archive montrent que les utilisateurs confondent toujours les défaillances d'origine/authentification de l'interface utilisateur de contrôle, la réachabilité du CDP distant, le MCP Chrome local de l'hôte et le comportement du relais nœud-hôte.

## Portée de la catégorie

Inclus dans cette catégorie :

- Passerelle WSL2 avec navigateur Windows : Passerelle WSL2 avec navigateur Windows et Chrome Windows
- URL de l'interface utilisateur de contrôle Windows : URL de l'interface utilisateur de contrôle Windows et conseils d'origine
- CDP distant brut vers Chrome Windows : Accès CDP distant brut de WSL2 à une instance Chrome Windows.
- MCP Chrome local de l'hôte : MCP Chrome local de l'hôte et limite de session existante
- cdpUrl du profil de navigateur : cdpUrl du profil de navigateur et configuration attachOnly
- Diagnostics en couches : Diagnostics en couches pour les défaillances d'authentification/origine/CDP

## Fonctionnalités

- Passerelle WSL2 avec navigateur Windows : Passerelle WSL2 avec navigateur Windows et Chrome Windows
- URL de l'interface utilisateur de contrôle Windows : URL de l'interface utilisateur de contrôle Windows et conseils d'origine
- CDP distant brut vers Chrome Windows : Accès CDP distant brut de WSL2 à une instance Chrome Windows.
- MCP Chrome local de l'hôte : MCP Chrome local de l'hôte et limite de session existante
- cdpUrl du profil de navigateur : cdpUrl du profil de navigateur et configuration attachOnly
- Diagnostics en couches : Diagnostics en couches pour les défaillances d'authentification/origine/CDP

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (72%)`
- Signaux positifs : la documentation de dépannage WSL2 + CDP distant Windows couvre la configuration complète en couches ; les documents de navigateur définissent CDP distant, `attachOnly`, les limites de session existante et les défaillances de préparation CDP ; les documents et le code source de l'interface utilisateur de contrôle appliquent les règles d'origine et d'authentification d'appareil.
- Signaux négatifs : il s'agit principalement de documentation et de comportement du code source, sans e2e spécifique à WSL2 pour navigateur/interface utilisateur de contrôle qui ouvre Chrome Windows à partir d'une passerelle WSL2.
- Lacunes d'intégration : aucune preuve en direct n'a été trouvée pour `openclaw browser open`, `browser tabs`, authentification de l'interface utilisateur de contrôle et CDP distant de bout en bout après les modifications du réseau Windows/WSL.

## Score de qualité

- Score : `Bêta (70%)`
- Rapports Gitcrawl : `WSL2 Windows browser CDP Control UI` a retourné le problème #73836 pour la réactivité de l'interface utilisateur de contrôle/passerelle dans Windows + WSL2 et PR #74163 avec contexte d'actualisation du problème Microsoft. `Windows WSL2 OpenClaw` a retourné le problème #81873 pour la confusion session existante/CDP, le problème #54669 pour la rupture IPv6/portproxy de Chrome et le problème #87387 pour l'état faux en cours de l'interface utilisateur de contrôle WSL2.
- Rapports Discrawl : la recherche navigateur/CDP WSL2 a retourné les commentaires du problème #41553, PR #42027 et la discussion utilisateur/support expliquant que le CDP distant brut est viable mais que le MCP Chrome local de l'hôte n'est pas un pont WSL2-vers-Windows.
- Bonnes qualités : les documents sont inhabituellement explicites sur l'ordre des couches, les vérifications curl exactes, la configuration `cdpUrl`, localhost de l'interface utilisateur de contrôle et les messages d'erreur trompeurs.
- Mauvaises qualités : les défaillances visibles par l'utilisateur chevauchent toujours la réachabilité du réseau, l'origine de l'interface utilisateur de contrôle, le jeton/appairage, le CDP HTTP et la préparation du CDP WebSocket.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont exclues de ce score de qualité.

## Score d'exhaustivité

- Score : `Bêta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/windows-via-wsl2.md`.
- Signaux positifs : les preuves de documents archivés, de code source, de test, de Gitcrawl et de Discrawl couvrent la portée de la taxonomie pour la passerelle WSL2 avec navigateur Windows, l'URL de l'interface utilisateur de contrôle Windows, le CDP distant brut vers Chrome Windows, le MCP Chrome local de l'hôte, cdpUrl du profil de navigateur, diagnostics en couches.
- Signaux négatifs : la note archivée a précédé la notation d'exhaustivité de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin d'un test de fumée CDP distant WSL2 + Chrome Windows automatisé avec un véritable point de terminaison de navigateur Windows.
- Besoin d'une commande de diagnostic unifiée qui résume l'état de l'origine/authentification de l'interface utilisateur de contrôle et du CDP HTTP/WebSocket en un seul endroit.
- Besoin d'une distinction de produit plus claire entre le relais nœud-hôte Windows, le CDP brut et le MCP Chrome de session existante pour les configurations WSL2 sur la même machine.

## Preuves

### Documents

- `/Users/kevinlin/code/openclaw/docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md:10` : le guide définit la configuration split-host et pourquoi les défaillances en couches sont confuses.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md:16` : le CDP distant brut est le modèle WSL2-vers-Windows recommandé.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md:28` : la session existante/profil utilisateur est uniquement pour la passerelle et Chrome sur le même hôte.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md:64` : l'interface utilisateur de contrôle Windows doit utiliser `http://127.0.0.1:18789/` sauf si une configuration HTTPS délibérée existe.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md:95` : les utilisateurs WSL2 doivent curl le point de terminaison CDP Windows exact destiné à `cdpUrl`.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md:117` : l'exemple de profil de navigateur distant définit `cdpUrl` et `attachOnly`.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md:175` : les erreurs courantes trompeuses distinguent l'authentification/origine de l'interface utilisateur de contrôle, la réachabilité du CDP et l'utilisation abusive de session existante.
- `/Users/kevinlin/code/openclaw/docs/tools/browser.md:309` : la documentation générale du navigateur définit les profils CDP distants.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:485` : les déploiements d'interface utilisateur de contrôle non-loopback publics doivent configurer les origines autorisées.

### Code source

- `/Users/kevinlin/code/openclaw/src/infra/browser-open.ts:68` : le support d'ouverture de navigateur Linux détecte WSL et préfère `wslview` quand disponible.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/message-handler.ts:679` : la passerelle vérifie l'origine du navigateur par rapport à `gateway.controlUi.allowedOrigins`.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/message-handler.ts:877` : la passerelle enregistre `control-ui-insecure-auth` pour les défaillances d'identité d'appareil de l'interface utilisateur de contrôle non sécurisée.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/connect-policy.ts:131` : la politique d'identité d'appareil de l'interface utilisateur de contrôle n'autorise l'authentification non sécurisée que pour localhost quand explicitement configurée.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-assistant-media.e2e.test.ts` : la couverture e2e de l'interface utilisateur de contrôle existe pour le comportement de la passerelle/interface utilisateur de contrôle, bien que pas pour Chrome Windows WSL2.
- `/Users/kevinlin/code/openclaw/src/gateway/server-plugin-bootstrap.browser-plugin.integration.test.ts` : l'intégration de démarrage du plugin de navigateur existe pour le comportement de démarrage de la passerelle.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/startup-control-ui-origins.test.ts:16` : les tests de démarrage ensemencent les origines localhost/127.0.0.1 pour la liaison LAN.
- `/Users/kevinlin/code/openclaw/src/gateway/server.config-patch.test.ts:266` : les tests de réponse de configuration masquent les identifiants `cdpUrl` du navigateur.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/connect-policy.test.ts:80` : les tests de politique de connexion couvrent le rejet de l'interface utilisateur de contrôle non sécurisée.
- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.control-ui.suite.ts` : la suite d'authentification de l'interface utilisateur de contrôle couvre l'appairage et le comportement d'authentification.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "WSL2 Windows browser CDP Control UI" --mode keyword --limit 10 --json`
- `gitcrawl search openclaw/openclaw --query "Windows WSL2 OpenClaw" --mode keyword --limit 12 --json`

Résultats :

- WSL2 Windows browser CDP Control UI a retourné le problème #73836 et PR #74163.
- Windows WSL2 OpenClaw a retourné 12 résultats, incluant le problème de profil de navigateur #81873, le problème IPv6/portproxy de Chrome #54669, le problème d'état faux en cours de l'interface utilisateur de contrôle #87387, l'arrêt de la passerelle #61616, la réachabilité du placeholder #80336 et les problèmes de réactivité de la passerelle WSL2.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 Windows browser CDP Control UI"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 portproxy Gateway Windows host"`

Résultats :

- La recherche navigateur/CDP WSL2 a retourné 8 résultats, incluant les commentaires du problème #41553, PR #42027, les conseils de support pour le CDP distant brut et le dépannage de l'origine de l'interface utilisateur de contrôle.
- La recherche portproxy/passerelle a retourné des rapports de relais nœud-hôte Windows et de relais d'extension Chrome qui chevauchent la configuration du navigateur split-host.
