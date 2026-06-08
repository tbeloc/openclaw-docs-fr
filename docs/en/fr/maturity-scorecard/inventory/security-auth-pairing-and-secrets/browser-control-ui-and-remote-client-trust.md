---
title: "Sécurité, authentification, appairage et secrets - Note de maturité de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de maturité de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant

## Résumé

L'interface utilisateur de contrôle et la confiance du contrôle du navigateur disposent de garde-fous architecturaux solides : authentification WebSocket, vérifications d'origine, appairage d'appareils, stockage de jetons de session, configuration d'exécution authentifiée, authentification des routes de contrôle du navigateur et vérifications d'audit de sécurité pour les bascules risquées. La couverture est Stable car la passerelle et l'extension du navigateur disposent de tests de flux serveur ciblés pour l'authentification du navigateur, les origines, l'appairage de l'interface utilisateur de contrôle et les routes de contrôle du navigateur fermées par défaut. La qualité est Alpha car l'historique Discord et GitHub montrent des problèmes répétés à fort impact et une confusion persistante des opérateurs autour des proxies inverses, de Tailscale Serve, des bascules non sécurisées, de l'identité du navigateur obsolète et du stockage des jetons.

## Portée de la catégorie

Cette catégorie couvre la confiance du navigateur de l'interface utilisateur de contrôle/WebChat, l'appairage d'appareils pour les clients du navigateur, les origines autorisées, le comportement de Tailscale/proxy de confiance pour les sessions du navigateur, l'authentification du point de terminaison de configuration d'exécution, l'authentification des routes HTTP de contrôle du navigateur, les risques de stockage du navigateur et les chemins de réparation des opérateurs distants/proxy.

## Fonctionnalités

- Interface utilisateur de contrôle du navigateur : couvre l'interface utilisateur de contrôle du navigateur dans la confiance du navigateur de l'interface utilisateur de contrôle/WebChat, l'appairage d'appareils pour les clients du navigateur, les origines autorisées, le comportement de Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant.
- Confiance du client distant : couvre la confiance du client distant dans la confiance du navigateur de l'interface utilisateur de contrôle/WebChat, l'appairage d'appareils pour les clients du navigateur, les origines autorisées, le comportement de Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : la documentation de l'interface utilisateur de contrôle et la documentation du contrôle du navigateur décrivent le comportement d'authentification et d'appairage ; les tests de flux serveur couvrent le renforcement du navigateur, l'authentification de l'interface utilisateur de contrôle, les listes blanches d'origines, le comportement des jetons par défaut, les modes Tailscale/proxy de confiance et les chemins fermés par défaut d'authentification du contrôle du navigateur.
- Signaux négatifs : la preuve de topologie réelle de proxy inverse/Tailscale Serve/navigateur mobile est encore plus mince que les tests de flux serveur locaux, et le comportement de mise à niveau du service worker/identité obsolète reste opérationnellement délicat.
- Lacunes d'intégration : ajouter une fumée de version pour l'interface utilisateur de contrôle sur localhost, proxy HTTPS inverse, Tailscale Serve, profil de navigateur frais, identité de navigateur obsolète et routes de contrôle du navigateur sous les modes jeton, mot de passe, proxy de confiance et aucun/ingress privé.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : la requête de problème exacte a retourné le problème ouvert #46919, `Token URL Disabled Via Config`. La requête de RP connexe a retourné le PR ouvert #73163 pour les avertissements d'accès non sécurisé à l'interface utilisateur de contrôle, plus d'autres RP de navigateur/interface utilisateur actifs adjacents aux surfaces de service worker et d'outils.
- Rapports Discrawl : la recherche Discord a trouvé le PR #64165 sur les secrets d'authentification d'appareil réutilisables dans le stockage du navigateur, l'examen du PR #43613 sur les sessions d'opérateur de l'interface utilisateur de contrôle authentifiées par Tailscale et des cas d'assistance répétés pour `pairing required`, `allowInsecureAuth`, origines autorisées, URL de passerelle localStorage obsolètes, en-têtes de proxy inverse et comportement de stockage des jetons.
- Bonnes qualités : la politique d'origine du navigateur, l'identité de l'appareil, l'état de l'appareil appairé, l'authentification de la configuration d'exécution et l'authentification du secret partagé du contrôle du navigateur sont explicitement implémentées et documentées.
- Mauvaises qualités : la confiance du navigateur est une limite UX à haut risque ; les preuves d'assistance montrent que les utilisateurs s'appuient fréquemment sur des bascules dangereuses ou un état de navigateur obsolète lors du débogage, et le problème de stockage du navigateur était de haute gravité.
- Exclu de la qualité : la largeur de couverture, la largeur des tests unitaires et la profondeur des tests d'intégration ne sont notées que sous Couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'interface utilisateur de contrôle du navigateur, la confiance du client distant.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La configuration du proxy inverse et de Tailscale de l'interface utilisateur de contrôle reste difficile à diagnostiquer sans les journaux de passerelle et les détails de DevTools du navigateur.
- L'identité locale du navigateur et le stockage des jetons ont connu un renforcement important.
- L'API de contrôle du navigateur n'hérite intentionnellement pas des modes d'identité de proxy de confiance/Tailscale, ce qui est plus sûr mais facile à mal comprendre.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente l'authentification WebSocket du navigateur, l'appairage d'appareils, les conditions d'omission de Tailscale Serve, le stockage des jetons, l'authentification de la configuration d'exécution, les origines autorisées et le comportement du PWA/service worker.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-control.md` documente les routes HTTP de contrôle du navigateur, les exigences d'authentification et les avertissements de loopback uniquement pour `auth.mode=none` et proxy de confiance.
- `/Users/kevinlin/code/openclaw/docs/gateway/trusted-proxy-auth.md` et `/Users/kevinlin/code/openclaw/docs/gateway/tailscale.md` documentent les chemins de proxy porteurs d'identité.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/audit-checks.md` documente les vérifications d'audit d'origine de l'interface utilisateur de contrôle, d'authentification non sécurisée, d'authentification d'appareil désactivée et d'authentification du contrôle du navigateur.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/auth.ts` autorise l'authentification par jeton/mot de passe/proxy de confiance/Tailscale et la politique d'origine du navigateur.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/message-handler.ts` applique l'authentification de la poignée de main WebSocket, l'identité de l'appareil, les portées et le comportement de la connexion de l'interface utilisateur de contrôle.
- `/Users/kevinlin/code/openclaw/src/gateway/origin-check.ts` gère la politique d'origine.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server.ts` et `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/control-auth.ts` implémentent le comportement d'authentification HTTP du contrôle du navigateur.
- `/Users/kevinlin/code/openclaw/ui/src` contient le client du navigateur de l'interface utilisateur de contrôle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.browser-hardening.test.ts` couvre le comportement d'origine et de renforcement du navigateur.
- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.control-ui.suite.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server.auth.control-ui.test.ts` couvrent le comportement d'authentification de l'interface utilisateur de contrôle.
- `/Users/kevinlin/code/openclaw/src/gateway/server.auth.modes.suite.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server.auth.default-token.suite.ts` couvrent les modes d'authentification et le comportement du serveur de jeton par défaut.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server.auth-fail-closed.test.ts` et `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server.auth-token-gates-http.test.ts` couvrent l'authentification des routes de contrôle du navigateur.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/auth.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/auth-surface-resolution.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/connection-auth.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/http-utils.authorize-request.test.ts` couvrent les aides d'authentification de niveau inférieur.
- `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/auth-context.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server/ws-connection/handshake-auth-helpers.test.ts` couvrent les aides d'état d'authentification WS.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/control-auth.test.ts`, `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/control-auth.auto-token.test.ts` et `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/routes/permissions.test.ts` couvrent l'authentification du contrôle du navigateur et les routes de permissions.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "browser control auth control ui device pairing origin"`

Résultats :

- A retourné le problème ouvert #46919, `[Feature]: Token URL Disabled Via Config`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "gateway auth trusted proxy browser control auth"`

Résultats :

- A retourné les PR ouverts incluant #73163 `fix(gateway): warn for insecure Control UI access`, #87077 `fix(ui): bypass service worker for top-level navigations`, #63919 `feat(gateway): wire coding tools into /tools/invoke HTTP surface` et #84247 `Feat/browser screenshot vision`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "browser control auth control ui device pairing origin"`

Résultats :

- A trouvé l'examen du PR #43613 clarifiant que les sessions d'opérateur de l'interface utilisateur de contrôle authentifiées par Tailscale peuvent ignorer un aller-retour d'appairage uniquement lorsque l'identité de l'appareil reste intacte.
- A trouvé le PR #64165 décrivant les secrets d'authentification d'appareil réutilisables de haute gravité dans le stockage du navigateur.
- A trouvé plusieurs cas d'assistance pour `pairing required`, `allowInsecureAuth`, configuration de proxy de confiance/origine, URL de passerelle localStorage obsolètes et comportement de stockage des jetons.
