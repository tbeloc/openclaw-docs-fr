---
title: "macOS Gateway host - Remote Gateway Mode Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# macOS Gateway host - Remote Gateway Mode Maturity Note

## Résumé

Le mode Remote Gateway est documenté et implémenté avec un modèle de transport clair :
l'application macOS peut se connecter à une Gateway distante via un tunnel SSH ou directement en ws/wss,
Tailscale est le chemin de réseau privé recommandé à faible friction, et l'application
démarre un hôte de nœud local au lieu d'une Gateway locale en mode distant.

La couverture est Beta car les preuves sont solides dans les docs/source/tests unitaires mais
plus minces pour les scénarios d'application empaquetée vers Gateway distante. La qualité est Stable car
le modèle de transport et d'authentification est explicite, avec rejet du texte brut direct,
précédence token/password/fingerprint, et gestion du cycle de vie du tunnel.

## Portée de la catégorie

Inclus dans cette catégorie :

- macOS app "Remote over SSH" : modes macOS app "Remote over SSH" et Gateway distante directe
- Configuration du tunnel SSH : configuration du tunnel SSH, propriété stable du forward local, et redémarrage/backoff du tunnel
- Tailscale MagicDNS : guidance Tailscale MagicDNS, Serve, et Funnel pour l'accès distant
- Token/password/TLS fingerprint du point de terminaison distant : résolution du token/password/TLS fingerprint du point de terminaison distant
- Démarrage de l'hôte de nœud local : démarrage de l'hôte de nœud local et suppression de la Gateway locale en mode distant

## Fonctionnalités

- macOS app "Remote over SSH" : modes macOS app "Remote over SSH" et Gateway distante directe
- Configuration du tunnel SSH : configuration du tunnel SSH, propriété stable du forward local, et redémarrage/backoff du tunnel
- Tailscale MagicDNS : guidance Tailscale MagicDNS, Serve, et Funnel pour l'accès distant
- Token/password/TLS fingerprint du point de terminaison distant : résolution du token/password/TLS fingerprint du point de terminaison distant
- Démarrage de l'hôte de nœud local : démarrage de l'hôte de nœud local et suppression de la Gateway locale en mode distant

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : docs en mode distant, docs de transport, source de l'application, source du endpoint-store, source du SSH tunnel manager, et les tests unitaires du command resolver couvrent le comportement conçu.
- Signaux négatifs : les preuves inspectées ici n'ont pas montré de test E2E d'application empaquetée en mode distant qui configure SSH/Tailscale, appaire/authentifie, démarre l'hôte de nœud, et prouve la commande/contrôle via la Gateway distante.
- Lacunes d'intégration : propriété du tunnel SSH gérée par l'application, invites de TLS fingerprint ws/wss directes, chemins Tailscale Serve/Funnel, et appairage du nœud hôte distant ont besoin de voies de publication en direct plus fortes.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : `macOS remote gateway SSH tunnel Tailscale direct wss tlsFingerprint` n'a retourné aucun résultat ouvert ou fermé spécifique à la fonctionnalité ; `macOS companion app remote gateway tunnel canvas unauthorized node` n'a retourné aucun résultat ouvert.
- Rapports Discrawl : `mac app remote gateway ssh tunnel` a retourné des threads de support sur le fallback du tunnel SSH, Tailscale comme chemin recommandé pour l'application et la Gateway distante, éviter les conflits de port-forward manuels avec le tunnel appartenant à l'application, et un cas de confusion Canvas unauthorized/node-registration.
- Bonnes qualités : la source sépare les modes SSH et direct, rejette les points de terminaison texte brut public non sécurisés sauf s'ils sont approuvés, centralise la précédence des identifiants, possède un forward SSH local stable, et garde le démarrage de la Gateway locale désactivé en mode distant.
- Mauvaises qualités : la confusion de l'opérateur persiste autour de la question de savoir si l'application macOS est uniquement un opérateur, un nœud, ou les deux ; le comportement Canvas/auth et les conflits de tunnel manuels montrent que le modèle d'utilisateur distant a besoin d'une preuve de produit plus claire.
- Exclu de la qualité : les preuves de couverture uniquement ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour macOS app "Remote over SSH", configuration du tunnel SSH, Tailscale MagicDNS, Token/password/TLS fingerprint du point de terminaison distant, démarrage de l'hôte de nœud local.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un E2E en mode distant empaquetée qui pilote les paramètres de l'application via un tunnel SSH, puis vérifie la connectivité de la Gateway et l'enregistrement du nœud.
- Clarifier la distinction app/nœud/opérateur dans la documentation de dépannage distant.
- Ajouter des diagnostics explicites pour les conflits de tunnel manuels sur le port forward local stable de l'application.

## Preuves

### Docs

- `docs/platforms/mac/remote.md:8` : documente le contrôle distant depuis l'application macOS et la division du transport SSH vs direct.
- `docs/platforms/mac/remote.md:18` : documente la topologie distante, `sshTarget`, `url`, loopback local, et comportement de l'hôte de nœud local.
- `docs/platforms/mac/remote.md:37` : documente les prérequis distants, PATH pour les shells non interactifs, et Tailscale.
- `docs/platforms/mac/remote.md:45` : documente `openclaw-mac configure-remote`.
- `docs/platforms/mac/remote.md:84` : documente les notes de permissions/sécurité distantes.
- `docs/gateway/remote.md:18` : documente la topologie du mode distant de l'application macOS.
- `docs/gateway/remote.md:67` : documente la configuration du tunnel SSH CLI et l'avertissement d'authentification.
- `docs/gateway/remote.md:157` : documente les règles de sécurité, l'épinglage TLS, et l'authentification Tailscale Serve.
- `docs/gateway/tailscale.md:9` : documente les modes Serve et Funnel tout en gardant la Gateway liée au loopback.

### Source

- `apps/macos/Sources/OpenClaw/ConnectionModeCoordinator.swift:57` : le mode distant arrête la Gateway locale, démarre le service de nœud, assure le tunnel de contrôle distant, et configure le canal de contrôle.
- `apps/macos/Sources/OpenClaw/GatewayRemoteConfig.swift:42` : résout le transport comme direct, SSH, ou hérité.
- `apps/macos/Sources/OpenClaw/GatewayRemoteConfig.swift:88` : résout l'URL distante, le token, le password, et le TLS fingerprint.
- `apps/macos/Sources/OpenClaw/GatewayRemoteConfig.swift:174` : normalise l'URL ws/wss et rejette les points de terminaison texte brut public sauf s'ils sont approuvés.
- `apps/macos/Sources/OpenClaw/GatewayEndpointStore.swift:291` : stocke les modes local, distant direct, et tunnel distant.
- `apps/macos/Sources/OpenClaw/GatewayEndpointStore.swift:343` : assure le tunnel de contrôle distant avant d'utiliser le point de terminaison.
- `apps/macos/Sources/OpenClaw/RemoteTunnelManager.swift:15` : réutilise un tunnel en cours d'exécution ou le redémarre quand l'écouteur est absent.
- `apps/macos/Sources/OpenClaw/RemoteTunnelManager.swift:38` : démarre le tunnel SSH avec les paramètres distants configurés et un port local stable préféré.
- `apps/macos/Sources/OpenClaw/TailscaleService.swift:103` : résout l'état MagicDNS/IP et hydrate les paramètres du point de terminaison à partir des données Tailscale.

### Tests d'intégration

- `scripts/e2e/parallels/macos-smoke.ts:1006` : le smoke macOS guest atteint un premier tour d'agent après la configuration de la Gateway, mais il est orienté mode local plutôt qu'un test d'application en mode distant dédié.
- `test/gateway.multi.e2e.test.ts:27` : la couverture d'appairage multi-Gateway/nœud exerce les contrats Gateway/nœud pertinents pour l'opération du nœud distant.

### Tests unitaires

- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:148` : couvre la construction de commande SSH pour le mode distant.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:182` : charge les paramètres distants à partir de la config.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:204` : rejette les cibles SSH non sécurisées.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:210` : assure que la commande daemon locale ignore les valeurs par défaut distantes.
- `apps/macos/Tests/OpenClawIPCTests/TailscaleIntegrationSectionTests.swift:8` : couvre les vues non installées/Serve.
- `apps/macos/Tests/OpenClawIPCTests/TailscaleIntegrationSectionTests.swift:32` : couvre le comportement de la vue Funnel.
- `apps/macos/Tests/OpenClawIPCTests/TailscaleIntegrationSectionTests.swift:49` : vérifie que l'hydratation ne réécrit pas la config existante.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "macOS remote gateway SSH tunnel Tailscale direct wss tlsFingerprint" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

Requête :

```bash
gitcrawl search issues "macOS remote gateway SSH tunnel Tailscale direct wss tlsFingerprint" -R openclaw/openclaw --state closed --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "mac app remote gateway ssh tunnel"
```

Résultats :

- Retourné un thread Canvas MacOS d'avril 2026 où le fallback du tunnel SSH était valide mais Tailscale était recommandé pour l'application et la Gateway distante.
- Retourné une guidance MacOS Node Setup de mars 2026 recommandant le mode macOS app "Remote over SSH" et avertissant de ne pas exécuter un tunnel manuel qui entre en conflit avec le forward appartenant à l'application.
- Retourné un cas de confusion Canvas unauthorized/node-registration pour une application de bureau macOS connectée à une Gateway distante.
