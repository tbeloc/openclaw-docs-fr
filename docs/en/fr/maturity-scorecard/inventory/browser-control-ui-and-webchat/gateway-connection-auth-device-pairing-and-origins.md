---
title: "Gateway Web App - Browser Access and Trust Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - Browser Access and Trust Maturity Note

## Résumé

L'accès au navigateur de l'interface utilisateur de contrôle et de WebChat dispose d'une machinerie d'authentification et de confiance substantielle : authentification par secret partagé WebSocket, authentification par mot de passe, identité Tailscale Serve, authentification par proxy de confiance, politique d'origine du navigateur, identité de l'appareil, appairage, mises à niveau de portée, authentification du point de terminaison de configuration d'exécution, et avertissements documentés en mode non sécurisé. La couverture est Stable car les tests de flux serveur ciblent directement ces chemins. La qualité est Alpha car les preuves d'archive montrent une confusion répétée de l'opérateur autour de l'appairage, de l'état du navigateur obsolète, de Tailscale/origines autorisées, des bascules non sécurisées, et du stockage des jetons d'appareil côté navigateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Appairage d'appareil : couvre l'appairage d'appareil sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Authentification par jeton/mot de passe : couvre l'authentification par jeton/mot de passe sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Authentification Tailscale Serve : couvre l'authentification Tailscale Serve sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Authentification par proxy de confiance : couvre l'authentification par proxy de confiance sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Origines autorisées/gatewayUrl : couvre les origines autorisées/gatewayUrl sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.

## Fonctionnalités

- Appairage d'appareil : couvre l'appairage d'appareil sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Authentification par jeton/mot de passe : couvre l'authentification par jeton/mot de passe sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Authentification Tailscale Serve : couvre l'authentification Tailscale Serve sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Authentification par proxy de confiance : couvre l'authentification par proxy de confiance sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.
- Origines autorisées/gatewayUrl : couvre les origines autorisées/gatewayUrl sur la configuration de connexion Gateway Control UI/WebChat, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification par proxy de confiance et Tailscale Serve, et le comportement connexe de connexion gateway, d'authentification, d'appairage d'appareil, et d'origines distantes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : les suites d'authentification Gateway couvrent les modes d'authentification Control UI, le renforcement du navigateur, les listes blanches d'origines, le comportement des jetons par défaut, l'appairage d'appareil, et la rotation des jetons partagés ; la documentation couvre les flux locaux, tailnet, Tailscale Serve, proxy de confiance, HTTP non sécurisé, et serveur de développement distant.
- Signaux négatifs : la preuve du navigateur réel pour les combinaisons proxy/Tailscale Serve/navigateur mobile est plus mince que la preuve du flux serveur, et le comportement d'identité du navigateur obsolète est plus souvent couvert par des tests de régression que par des scénarios de fumée de version.
- Lacunes d'intégration : ajouter des fumées de version de navigateur récurrentes pour profil frais, profil obsolète, mise à niveau de portée, Tailscale Serve, proxy de confiance, proxy inverse avec origines autorisées, et amorçage `gatewayUrl` du serveur de développement distant.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : la requête d'authentification a retourné #46919 pour la désactivation de l'URL de jeton, PR #73163 pour les avertissements d'accès Control UI non sécurisé, et les PR adjacentes de renforcement de la sécurité Control UI/service-worker #63919 et #84247.
- Rapports Discrawl : la recherche Discord a trouvé la discussion de révision PR #43613 clarifiant que les sessions d'opérateur Control UI authentifiées par Tailscale peuvent ignorer un tour d'appairage uniquement lorsque l'identité de l'appareil du navigateur reste intacte, PR #64165 sur les secrets d'authentification d'appareil réutilisables dans le stockage du navigateur, et les cas d'assistance pour `pairing required`, `allowInsecureAuth`, les URL de gateway localStorage obsolètes, les origines autorisées, les invites de jeton, et la configuration Tailscale/proxy de confiance.
- Bonnes qualités : le modèle de confiance est explicite, limité par portée, et documenté. Les modes loopback local, Tailscale Serve, proxy de confiance, et secret partagé ont des chemins de code distincts et des avertissements de sécurité.
- Mauvaises qualités : l'authentification du navigateur est une limite UX à haut risque. Les opérateurs atteignent souvent des bascules dangereuses ou des réparations d'état de navigateur obsolète avant de comprendre quelle porte a échoué.
- Exclu de la qualité : la preuve unitaire, d'intégration, e2e, en direct, et de flux d'exécution réel affectent uniquement la couverture.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour l'appairage d'appareil, l'authentification par jeton/mot de passe, l'authentification Tailscale Serve, l'authentification par proxy de confiance, les origines autorisées/gatewayUrl.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La configuration du proxy/Tailscale reste difficile à déboguer sans journaux et outils de développement du navigateur.
- L'identité locale du navigateur et le stockage des jetons d'appareil ont connu un changement de renforcement sérieux.
- La différence entre l'authentification Control UI, l'authentification HTTP API, l'authentification HTTP de contrôle du navigateur, et l'appairage de nœud est facile à mal comprendre.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente l'authentification WebSocket, l'appairage d'appareil, l'approbation automatique locale, le comportement de Tailscale Serve, l'authentification de la configuration d'exécution, HTTP non sécurisé, les origines autorisées, `gatewayUrl`, et l'amorçage du fragment de jeton.
- `/Users/kevinlin/code/openclaw/docs/web/dashboard.md` documente l'authentification du tableau de bord, les attentes de stockage des jetons/mots de passe, les étapes de réparation non autorisées/1008, et `openclaw dashboard`.
- `/Users/kevinlin/code/openclaw/docs/gateway/tailscale.md` documente l'authentification Serve/Funnel, la vérification de l'en-tête d'identité, et les exigences d'identité d'appareil du navigateur.
- `/Users/kevinlin/code/openclaw/docs/gateway/remote.md` documente les règles de sécurité Gateway distante, les tunnels SSH, Tailscale, et l'accès WebChat distant.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/auth.ts` résout et valide les modes d'authentification gateway.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/message-handler.ts` applique l'authentification de la poignée de main WebSocket, l'identité de l'appareil, les portées, et le comportement du client Control UI.
- `/Users/kevinlin/code/openclaw/src/gateway/origin-check.ts` implémente la politique d'origine du navigateur.
- `/Users/kevinlin/code/openclaw/src/gateway/device-auth.ts` implémente les aides d'authentification d'appareil.
- `/Users/kevinlin/code/openclaw/ui/src/ui/device-auth.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/device-identity.ts` gèrent l'identité de l'appareil côté navigateur.
- `/Users/kevinlin/code/openclaw/ui/src/ui/control-ui-auth.ts` résout les en-têtes d'authentification pour les récupérations HTTP Control UI.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.browser-hardening.test.ts` couvre le comportement d'authentification et de renforcement du navigateur.
- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.control-ui.suite.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server.auth.control-ui.test.ts` couvrent les flux d'authentification Control UI.
- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.modes.suite.ts` couvre les modes d'authentification, y compris le comportement de Tailscale et du proxy de confiance.
- `/Users/kevinlin/code/openclaw/src/gateway/server.device-pair-approve-supersede.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server.device-token-rotate-authz.test.ts` couvrent les opérations d'appairage et de rotation de jeton d'appareil.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/auth.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/auth-surface-resolution.test.ts`, et `/Users/kevinlin/code/openclaw/src/gateway/origin-check.test.ts` couvrent les aides d'authentification/origine de niveau inférieur.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/auth-context.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/handshake-auth-helpers.test.ts` couvrent les aides de poignée de main.
- `/Users/kevinlin/code/openclaw/ui/src/ui/connect-error.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/connect-error.node.test.ts` couvrent le formatage des erreurs de connexion côté client.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "browser control auth control ui device pairing origin"`

Résultats :

- A retourné l'ouverture #46919, `[Feature]: Token URL Disabled Via Config`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "gateway auth trusted proxy browser control auth"`

Résultats :

- A retourné la PR ouverte #73163, `fix(gateway): warn for insecure Control UI access`.
- A retourné la PR ouverte #87077, `fix(ui): bypass service worker for top-level navigations`.
- A retourné les PR adjacentes du navigateur/Gateway #63919 et #84247.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "browser control auth control ui device pairing origin"`

Résultats :

- A trouvé la révision PR #43613 clarifiant que les sessions d'opérateur Control UI authentifiées par Tailscale peuvent ignorer un tour d'appairage uniquement lorsque l'identité de l'appareil du navigateur reste intacte.
- A trouvé la PR #64165 décrivant les secrets d'authentification d'appareil réutilisables à haute sévérité dans le stockage du navigateur.
- A trouvé les cas d'assistance pour `pairing required`, `allowInsecureAuth`, la configuration du proxy de confiance/origine, les URL de gateway localStorage obsolètes, les origines autorisées, les invites de jeton, et la configuration Tailscale/proxy de confiance.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "pairing required allowInsecureAuth Control UI Tailscale Serve localStorage"`

Résultats :

- A trouvé les conseils d'assistance utilisateur pour effacer les données du site, inspecter les erreurs WebSocket du navigateur, vérifier `allowedOrigins`, et éviter `dangerouslyDisableDeviceAuth` en dehors des expériences temporaires.
