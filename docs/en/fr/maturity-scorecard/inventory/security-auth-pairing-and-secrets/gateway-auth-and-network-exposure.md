---
title: "Sécurité, authentification, appairage et secrets - Note de maturité de l'authentification de la passerelle et de l'accès à distance"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de maturité de l'authentification de la passerelle et de l'accès à distance

## Résumé

L'authentification de la passerelle et l'exposition réseau sont implémentées comme une véritable limite de sécurité dans la configuration de démarrage, le lancement CLI, les wrappers d'authentification HTTP, l'authentification de la poignée de main WebSocket, les vérifications d'origine du navigateur, l'identité du proxy de confiance, l'identité Tailscale et les runbooks des opérateurs. La posture par défaut reste loopback-first ; l'exposition non-loopback nécessite une authentification par jeton/mot de passe ou proxy de confiance ; l'accès public ou par proxy du navigateur nécessite des origines explicites ; et l'identité Tailscale est délibérément plus étroite que l'authentification générale de l'API HTTP.

La couverture est Stable car les tests réels de Gateway/serveur exercent l'authentification par jeton/mot de passe, le mode `auth.mode: "none"` explicite, le comportement WebSocket de l'interface utilisateur de contrôle authentifiée par Tailscale, le comportement de l'interface utilisateur de contrôle par proxy de confiance, le durcissement des sockets pré-authentification, le rejet d'origine du navigateur, les garde-fous de démarrage non-loopback et le chargement d'authentification fail-closed de SecretRef. La qualité est Beta car la source et la documentation sont conscientes de la sécurité et largement alignées, mais les archives actualisées montrent toujours une confusion des opérateurs et des threads de durcissement ouverts autour du proxy de confiance, de Tailscale Serve/Funnel, `allowedOrigins`, l'identité du service et les modes d'échec du reverse-proxy/navigateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Authentification par jeton/mot de passe de la passerelle partagée : Authentification par jeton et mot de passe pour les clients HTTP et WebSocket de la passerelle, y compris la résolution d'authentification à l'exécution, la validation au démarrage, la comparaison de secret partagé et les conseils aux opérateurs.
- Mode d'authentification de la passerelle : Sélection du mode d'authentification de la passerelle, y compris le comportement d'ingestion privée et les avertissements des opérateurs pour l'exposition non sécurisée.
- Identité du proxy de confiance : Identité du proxy de confiance, gateway.trustedProxies, trustedProxy.userHeader, requiredHeaders, allowUsers, allowLoopback, validation de la source du reverse-proxy et comportement de portée
- Tailscale Serve/Funnel : Tailscale Serve/Funnel et règles d'exposition du reverse-proxy, y compris les en-têtes d'identité Tailscale, tailscale whois, exigences de mot de passe Funnel et séparation entre l'identité Control UI/WS et l'authentification de l'API HTTP
- Restrictions de liaison et d'origine : modes de liaison loopback/LAN/tailnet/personnalisé, vérifications d'exposition non-loopback, vérifications d'origine du navigateur, controlUi.allowedOrigins, risque de secours d'en-tête Host et gestion des en-têtes forwarded
- Authentification de la poignée de main WebSocket : Authentification de la poignée de main WebSocket, y compris l'ordre challenge/connect, l'authentification de l'appareil liée à nonce, l'authentification partagée, les vérifications d'origine du navigateur, les limites pré-authentification, le délai d'expiration du socket non authentifié et la rotation d'authentification partagée obsolète
- Documentation destinée aux opérateurs : Documentation et runbooks destinés aux opérateurs pour l'audit de sécurité, l'accès à distance, la restauration d'exposition, Tailscale, proxy de confiance, rotation des identifiants et sondage explicite des identifiants
- Interface utilisateur de contrôle du navigateur : Couvre l'interface utilisateur de contrôle du navigateur dans la confiance du navigateur Control UI/WebChat, l'appairage des appareils pour les clients du navigateur, les origines autorisées, le comportement Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant.
- Confiance du client distant : Couvre la confiance du client distant dans la confiance du navigateur Control UI/WebChat, l'appairage des appareils pour les clients du navigateur, les origines autorisées, le comportement Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant.

## Fonctionnalités

- Authentification par jeton/mot de passe de la passerelle partagée : Authentification par jeton et mot de passe pour les clients HTTP et WebSocket de la passerelle, y compris la résolution d'authentification à l'exécution, la validation au démarrage, la comparaison de secret partagé et les conseils aux opérateurs.
- Mode d'authentification de la passerelle : Sélection du mode d'authentification de la passerelle, y compris le comportement d'ingestion privée et les avertissements des opérateurs pour l'exposition non sécurisée.
- Identité du proxy de confiance : Identité du proxy de confiance, gateway.trustedProxies, trustedProxy.userHeader, requiredHeaders, allowUsers, allowLoopback, validation de la source du reverse-proxy et comportement de portée
- Tailscale Serve/Funnel : Tailscale Serve/Funnel et règles d'exposition du reverse-proxy, y compris les en-têtes d'identité Tailscale, tailscale whois, exigences de mot de passe Funnel et séparation entre l'identité Control UI/WS et l'authentification de l'API HTTP
- Restrictions de liaison et d'origine : modes de liaison loopback/LAN/tailnet/personnalisé, vérifications d'exposition non-loopback, vérifications d'origine du navigateur, controlUi.allowedOrigins, risque de secours d'en-tête Host et gestion des en-têtes forwarded
- Authentification de la poignée de main WebSocket : Authentification de la poignée de main WebSocket, y compris l'ordre challenge/connect, l'authentification de l'appareil liée à nonce, l'authentification partagée, les vérifications d'origine du navigateur, les limites pré-authentification, le délai d'expiration du socket non authentifié et la rotation d'authentification partagée obsolète
- Documentation destinée aux opérateurs : Documentation et runbooks destinés aux opérateurs pour l'audit de sécurité, l'accès à distance, la restauration d'exposition, Tailscale, proxy de confiance, rotation des identifiants et sondage explicite des identifiants
- Interface utilisateur de contrôle du navigateur : Couvre l'interface utilisateur de contrôle du navigateur dans la confiance du navigateur Control UI/WebChat, l'appairage des appareils pour les clients du navigateur, les origines autorisées, le comportement Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant.
- Confiance du client distant : Couvre la confiance du client distant dans la confiance du navigateur Control UI/WebChat, l'appairage des appareils pour les clients du navigateur, les origines autorisées, le comportement Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface utilisateur de contrôle du navigateur et de la confiance du client distant.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs :
  - Les tests réels de Gateway couvrent l'acceptation/rejet de l'authentification par mot de passe, les chemins de rejet de l'authentification par jeton, le mode `auth.mode: "none"` explicite loopback, le comportement WebSocket de l'interface utilisateur de contrôle authentifiée par Tailscale et les interactions d'authentification partagée/authentification d'appareil (`src/gateway/server.auth.modes.suite.ts:18`, `src/gateway/server.auth.modes.suite.ts:52`, `src/gateway/server.auth.modes.suite.ts:114`, `src/gateway/server.auth.modes.suite.ts:145`).
  - Les tests de durcissement du navigateur couvrent le rejet d'origine de l'attaquant, le rejet d'origine du proxy de confiance en dehors de `allowedOrigins`, les origines loopback forgées via les en-têtes proxy et la limitation du débit d'authentification d'origine du navigateur (`src/gateway/server.auth.browser-hardening.test.ts:153`, `src/gateway/server.auth.browser-hardening.test.ts:241`, `src/gateway/server.auth.browser-hardening.test.ts:316`, `src/gateway/server.auth.browser-hardening.test.ts:461`).
  - Les tests d'exécution de l'interface utilisateur de contrôle du proxy de confiance couvrent le rejet d'identité d'appareil manquante, l'effacement de portée sans appareil et la limitation de portée déclarée par proxy (`src/gateway/server.auth.control-ui.suite.ts:291`, `src/gateway/server.auth.control-ui.suite.ts:381`, `src/gateway/server.auth.control-ui.suite.ts:434`).
  - Les tests de durcissement pré-authentification couvrent le rejet de mise à niveau du gestionnaire indisponible, la fermeture du socket non authentifié inactif, le rejet de la trame connect pré-authentification surdimensionnée et les budgets de socket non authentifié (`src/gateway/server.preauth-hardening.test.ts:89`, `src/gateway/server.preauth-hardening.test.ts:132`, `src/gateway/server.preauth-hardening.test.ts:197`, `src/gateway/server.preauth-hardening.test.ts:243`).
  - Les tests de configuration d'exécution couvrent les exigences de configuration du proxy de confiance, l'autorisation LAN/jeton, le rejet LAN/sans authentification, la validation de liaison personnalisée et les exigences `allowedOrigins` de l'interface utilisateur de contrôle non-loopback (`src/gateway/server-runtime-config.test.ts:18`, `src/gateway/server-runtime-config.test.ts:75`, `src/gateway/server-runtime-config.test.ts:132`, `src/gateway/server-runtime-config.test.ts:203`).
  - Les tests d'exécution de SecretRef prouvent que les références d'authentification Gateway actives échouent fermées au démarrage et au rechargement à chaud plutôt que de tomber silencieusement en secours en texte brut (`src/secrets/runtime.gateway-auth.integration.test.ts:36`, `src/secrets/runtime.gateway-auth.integration.test.ts:67`).
  - Les tests d'intégration CLI/probe exercent le sondage explicite de jeton contre une Gateway en cours d'exécution et l'authentification d'appareil en cache après le premier sondage authentifié local (`src/gateway/probe.auth.integration.test.ts:82`).
- Signaux négatifs :
  - La preuve la plus forte est les tests réels de serveur/exécution locaux ; cet audit n'a pas trouvé un reverse-proxy nginx/Caddy/Pomerium/Cloudflare/Authentik en direct de bout en bout qui prouve les en-têtes d'identité, l'accès direct bloqué, `allowUsers` et les restrictions d'origine ensemble.
  - Le comportement de Tailscale est simulé et soutenu par la source, mais cet audit n'a pas trouvé une preuve récurrente du daemon Tailscale en direct pour les en-têtes d'identité Serve, l'application du mot de passe Funnel, l'identité obsolète ou les appareils appartenant à des balises.
  - L'exposition non-loopback est bien gardée dans les tests de source et de configuration d'exécution, mais il n'y a pas de scénario d'opérateur complet qui exerce la réachabilité du pare-feu, les tentatives de client distant non autorisé, les origines de navigateur autorisées et la restauration du runbook d'exposition.
  - L'audit de sécurité et la documentation/runbooks sont solides, mais les runbooks ne sont pas eux-mêmes automatisés en tant que vérifications de scénario de mise à niveau/sécurité.
- Lacunes d'intégration :
  - Ajouter un e2e de reverse-proxy réel avec en-têtes d'identité authentifiés, refus de backend direct, `trustedProxies`, `requiredHeaders`, `allowUsers`, `allowLoopback: false`, application d'origine du navigateur et sondes non authentifiées négatives.
  - Ajouter un scénario Tailscale Serve/Funnel en direct qui prouve la vérification de l'en-tête d'identité Serve, les exigences d'authentification partagée de l'API HTTP, les exigences de mot de passe Funnel et le comportement d'échec sans identité/appartenant à une balise.
  - Ajouter une couverture de fumée d'exposition non-loopback qui lie LAN/tailnet/personnalisé, vérifie les exigences de jeton/mot de passe/proxy de confiance, vérifie les clients distants non autorisés et valide la restauration à loopback.
  - Ajouter une preuve de scénario d'audit de sécurité/runbook récurrente avant de traiter ce composant comme Lovable.

## Score de Qualité

- Score : `Bêta (78%)`
- Rapports Gitcrawl :
  - Les threads ouverts trusted-proxy et identity montrent des lacunes opérationnelles inachevées : drapeaux d'intégration trusted-proxy (#73638/#73639), identité de service par rapport à l'authentification utilisateur (#69066), comportement utilisateur par défaut/fallback trusted-proxy (#23585), documentation de portée trusted-proxy (#80063/#85950), et correspondance trusted proxy voix/webhook (#86525/#86527).
  - Les problèmes ouverts Tailscale et remote-access montrent une ambiguïté produit : authentification secondaire optionnelle pour Tailscale Serve (#57110), fermeture WebSocket Android/Control UI après configuration Tailscale (#85966), confusion URL token et Tailscale Serve auth (#46919), et analyse URL LAN manuelle Android (#87216).
  - Les enregistrements origin et proxy ouverts montrent une friction d'exposition du navigateur : problème d'identité client Cloudflare tunnel Control UI (#78674), travail custom origin/CORS/allowed-origin (#38290/#68647/#73511), et comportement auth/401 reverse-proxy (#87268).
  - Les threads de renforcement auth ouverts montrent les arêtes vives de sécurité restantes : réutilisation de token hooks comme mot de passe Gateway (#87376/#87379), exposition `--password` en texte brut (#83880), tokens Gateway multiples (#43903), et préoccupations d'escalade de secret partagé trusted-operator (#78712).
- Rapports Discrawl :
  - Les résultats Discord récents montrent à plusieurs reprises des opérateurs déboguant `gateway.bind`, `gateway.auth.mode`, exposition LAN, comportement bind Docker, et pourquoi `auth.mode: "none"` est dangereux ou bloqué en dehors de loopback de confiance/ingress privé.
  - Les threads de support Tailscale montrent une confusion récurrente selon laquelle l'identité Tailscale Serve peut autoriser Control UI/WS mais pas les API HTTP normales, que Funnel manque d'en-têtes d'identité, et que les entrées exactes `gateway.controlUi.allowedOrigins` sont toujours requises.
  - Les threads reverse-proxy/trusted-proxy montrent des utilisateurs en difficulté avec les adresses IP source proxy du même hôte, injection d'en-têtes Apache/AuthentiK/Cloudflared, appels WebSocket CLI/TUI directs qui ne portent pas d'en-têtes d'identité proxy, et l'identité de l'appareil étant toujours requise pour certains flux de navigateur.
- Bonnes qualités :
  - La source utilise par défaut une sémantique auth explicite, rejette le mode token/password ambigu, valide le matériel token/password configuré, et maintient le mode trusted-proxy mutuellement exclusif avec l'auth token partagé (`src/gateway/auth-mode-policy.ts:4`, `src/gateway/auth.ts:222`, `src/gateway/startup-auth.ts:125`).
  - L'exposition non-loopback est bloquée sans auth partagé ou auth trusted-proxy aux limites CLI/runtime, tandis que les modes Tailscale serve/funnel sont forcés à loopback et `auth.mode: "none"` est rejeté pour les modes Tailscale dangereux (`src/cli/gateway-cli/run.ts:772`, `src/gateway/server-runtime-config.ts:57`, `src/config/validation.ts:833`, `src/config/validation.ts:860`).
  - La gestion trusted-proxy valide les adresses source proxy configurées, rejette loopback sauf autorisation explicite, rejette l'usurpation d'interface locale, applique les en-têtes requis et `allowUsers`, et échoue fermé quand les en-têtes transférés ne peuvent pas être approuvés (`src/gateway/auth.ts:270`, `src/gateway/net.ts:178`, `src/gateway/net.ts:193`).
  - L'exposition du navigateur est gardée par une politique `Origin` explicite, des vérifications same-origin privé/local, des `allowedOrigins` non-loopback, et des avertissements pour le fallback Host-header dangereux (`src/gateway/origin-check.ts:35`, `src/gateway/origin-check.ts:80`, `src/security/audit-gateway-config.ts:165`).
  - Le code de poignée de main WebSocket applique le séquençage challenge/connect, les vérifications d'origine du navigateur, les décisions auth partagé/appareil/trusted-proxy, les limites pré-auth, et les déconnexions de génération auth partagé obsolète (`src/gateway/server/ws-connection.ts:244`, `src/gateway/server/ws-connection/message-handler.ts:529`, `src/gateway/server/ws-connection/message-handler.ts:676`, `src/gateway/server/ws-connection/message-handler.ts:970`).
  - Les docs opérateur s'alignent étroitement avec la source : audit de sécurité, runbook d'exposition, auth trusted-proxy, Tailscale, accès distant, rotation des credentials, sondage explicite des credentials, et rollback décrivent tous les mêmes contraintes de haut niveau.
- Mauvaises qualités :
  - Le modèle de configuration sûr reste difficile à raisonner car le mode bind, le mode auth, l'origine Control UI, l'adresse IP source proxy, les en-têtes transférés, l'appairage d'appareil, le mode Tailscale, et le comportement HTTP-versus-WS interagissent tous.
  - L'opération trusted-proxy nécessite toujours une configuration proxy externe précise qu'OpenClaw ne peut pas entièrement vérifier : terminaison TLS, blocage backend direct, règles de réécriture/suppression d'en-têtes, identité authentifiée, et préservation d'adresse IP source.
  - L'identité Tailscale Serve est intentionnellement étroite mais facile à mal comprendre ; les utilisateurs continuent de s'attendre à ce qu'elle couvre les API HTTP, Funnel, les appareils étiquetés, ou les origines du navigateur sans configuration supplémentaire.
  - Plusieurs états opérateur à fort impact produisent toujours du trafic de support plutôt que des récupérations auto-explicatives : omissions de liste allowlist d'origine, token/password de profil incorrect, adresses IP source proxy du même hôte, comportement tunnel Cloudflare, et classification WebSocket local-versus-remote.
- Exclu de la qualité :
  - L'étendue de la preuve unitaire, intégration, e2e, live, et runtime réelle n'a pas été utilisée pour augmenter ou diminuer la Qualité. La preuve runtime est utilisée uniquement dans Coverage.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les docs archivées, source, test, Gitcrawl, et preuve Discrawl couvrent la portée taxonomie pour l'auth token/password Gateway partagé, le mode auth Gateway, l'identité trusted-proxy, Tailscale Serve/Funnel, les restrictions Bind et origin, l'auth poignée de main WebSocket, les docs opérateur, le Control UI navigateur, la confiance client distant.
- Signaux négatifs : la note archivée a précédé le scoring Complétude process-version-3, donc ce score est initialisé à partir de la même étendue de preuve et du registre de lacunes connues utilisé pour le score Coverage archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une intégration reverse-proxy réelle qui prouve l'identité trusted-proxy de bout en bout via un proxy concret, incluant l'accès direct bloqué, la suppression/réécriture d'en-têtes, `allowUsers`, les en-têtes manquants refusés, et l'application de l'origine.
- Ajouter un scénario Tailscale Serve/Funnel live récurrent avec les en-têtes d'identité Tailscale réels, les vérifications de mot de passe Funnel, le comportement tag-owned/no-identity, et les attentes auth token partagé API HTTP.
- Automatiser le runbook d'exposition comme un scénario : baseline loopback, exposition LAN/tailnet/custom délibérée, sonde distante non autorisée, sonde credential autorisée, validation d'origine Control UI, sortie audit de sécurité, rollback, et rotation token/password.
- Améliorer les diagnostics opérateur pour `allowedOrigins`, les reverse proxies du même hôte, le comportement tunnel Cloudflare, les credentials de profil incorrects, et les limites d'identité Tailscale Serve.
- Résoudre ou délimiter explicitement les threads d'archive ouverts autour de l'authentification secondaire Tailscale, la séparation d'identité de service, les tokens Gateway multiples, l'exposition CLI de mot de passe en texte brut, et les drapeaux d'intégration trusted-proxy.
- Rendre le modèle de confiance ingress public/privé plus visible dans les docs first-run et remote-access afin que `auth.mode: "none"` ne soit pas découvert via des tentatives LAN ou Tailscale échouées.

# Preuve

## Docs

- `docs/gateway/security/index.md:8` énonce le modèle de confiance de l'assistant personnel et avertit qu'OpenClaw n'est pas un système multi-locataire hostile.
- `docs/gateway/security/index.md:28` indique aux opérateurs d'utiliser le runbook d'exposition avant l'accès à distance, le proxy inverse ou l'exposition publique.
- `docs/gateway/security/index.md:36` documente `openclaw security audit` comme vérification de durcissement principale, y compris l'exposition de l'authentification Gateway.
- `docs/gateway/security/index.md:177` montre la ligne de base durcie avec `gateway.bind: "loopback"` et l'authentification par jeton.
- `docs/gateway/security/index.md:373` documente le proxy inverse et `trustedProxies`, y compris la règle selon laquelle les en-têtes de proxy ne sont pas approuvés sauf s'ils sont configurés.
- `docs/gateway/security/index.md:419` documente HSTS et `allowedOrigins`, y compris le comportement explicite des caractères génériques.
- `docs/gateway/security/index.md:746` documente les conseils d'exposition réseau : loopback par défaut, la liaison non-loopback nécessite un examen de l'authentification et du pare-feu, et Tailscale Serve est préféré.
- `docs/gateway/security/index.md:876` documente l'intégration du jeton Gateway généré et note que `gateway.remote.*` ne protège pas le serveur WS local par lui-même.
- `docs/gateway/security/index.md:895` documente l'acceptation en texte brut `ws://` uniquement pour l'utilisation privée/loopback et la classification à distance pour les contextes tailnet/LAN/proxy.
- `docs/gateway/security/index.md:919` documente les modes jeton, mot de passe, proxy de confiance et la rotation des identifiants.
- `docs/gateway/security/index.md:930` documente les en-têtes d'identité Tailscale Serve, `tailscale whois`, la limite Control UI/WS uniquement, et la recommandation de secours à secret partagé.
- `docs/gateway/security/exposure-runbook.md:11` avertit les opérateurs d'exposer la Gateway uniquement après avoir déterminé qui peut y accéder, qui s'authentifie et quels agents/outils sont accessibles.
- `docs/gateway/security/exposure-runbook.md:24` compare les modèles d'exposition loopback+SSH, Tailscale Serve, liaison tailnet/LAN, proxy inverse de confiance et Internet public.
- `docs/gateway/security/exposure-runbook.md:54` documente les vérifications de base, les sondes d'identifiants explicites et la règle selon laquelle les URL distantes explicites n'héritent pas automatiquement des identifiants de configuration.
- `docs/gateway/security/exposure-runbook.md:126` documente la liste de contrôle du proxy inverse : identité authentifiée par proxy, accès direct au backend bloqué, `trustedProxies`, en-têtes supprimés/réécrits, `allowUsers` et `allowLoopback`.
- `docs/gateway/security/exposure-runbook.md:155` documente la validation autorisée et non autorisée après modification.
- `docs/gateway/security/exposure-runbook.md:169` documente le retour à loopback et la rotation des jetons/mots de passe.
- `docs/gateway/trusted-proxy-auth.md:12` avertit que le mode proxy de confiance délègue l'authentification au proxy externe.
- `docs/gateway/trusted-proxy-auth.md:34` documente le flux de requête proxy de confiance : le proxy s'authentifie, injecte les en-têtes d'identité, et Gateway vérifie l'IP du proxy de confiance avant d'extraire l'identité.
- `docs/gateway/trusted-proxy-auth.md:52` documente le comportement d'appairage de Control UI et l'effacement de portée en mode proxy de confiance.
- `docs/gateway/trusted-proxy-auth.md:75` montre la configuration du proxy de confiance avec liaison LAN, `gateway.trustedProxies`, `auth.mode: "trusted-proxy"`, `userHeader`, `requiredHeaders`, `allowUsers` et `allowLoopback: false`.
- `docs/gateway/trusted-proxy-auth.md:106` documente les règles d'exécution : rejet de source loopback par défaut, `allowLoopback` même hôte, secours interne au mot de passe, `allowedOrigins` non-loopback et restrictions de secours direct d'en-têtes transférés.
- `docs/gateway/tailscale.md:9` documente Tailscale Serve/Funnel gardant la Gateway loopback tandis que Tailscale fournit le routage et les en-têtes d'identité.
- `docs/gateway/tailscale.md:23` documente les limites d'authentification d'identité Serve, `tailscale whois`, utilisation d'identité WS uniquement et exigences d'authentification partagée de l'API HTTP.
- `docs/gateway/tailscale.md:92` documente Funnel plus mot de passe partagé et recommande la gestion des mots de passe sauvegardés par l'environnement.
- `docs/gateway/tailscale.md:115` documente que Funnel refuse de s'exécuter sans authentification par mot de passe et que Serve/Funnel n'exposent que Control UI et WS de Gateway.
- `docs/gateway/remote.md:15` documente l'accès à la Gateway distante via Tailscale Serve, liaison tailnet/LAN de confiance ou tunnel SSH.
- `docs/gateway/remote.md:125` documente la précédence des identifiants et la sécurité du remplacement d'URL.
- `docs/gateway/remote.md:157` documente les règles de sécurité distante : garder loopback uniquement, le plaintext distant public doit utiliser `wss://`, les liaisons non-loopback ont besoin de jeton/mot de passe/proxy de confiance, les identifiants distants ne configurent pas l'authentification du serveur, l'identité Tailscale Serve est limitée et le loopback proxy de confiance nécessite un opt-in explicite.
- `docs/gateway/configuration-reference.md:524` documente les valeurs de liaison, les exigences d'authentification, le mode sans authentification explicite, la sémantique du proxy de confiance, `allowTailscale`, `allowedOrigins`, les attentes d'URL `wss://` publiques, le secours SecretRef et `trustedProxies`.
- `docs/cli/gateway.md:58` documente la liaison au-delà de loopback sans authentification comme bloquée et donne des alternatives explicites de jeton/mot de passe/proxy.
- `docs/cli/doctor.md:46` documente le support du docteur pour générer un jeton Gateway et signaler l'authentification gérée par SecretRef sans secours en texte brut.

## Source

- `src/config/types.gateway.ts:3` définit les modes de liaison Gateway.
- `src/config/types.gateway.ts:129` définit l'origine de Control UI et les drapeaux de secours dangereux.
- `src/config/types.gateway.ts:146` définit les modes d'authentification Gateway `none`, `token`, `password` et `trusted-proxy` plus les champs proxy de confiance et `allowTailscale`.
- `src/gateway/auth-resolve.ts:31` résout le mode d'authentification, le jeton/mot de passe et les valeurs par défaut Tailscale à partir de la configuration, de l'environnement et des remplacements.
- `src/gateway/auth-mode-policy.ts:4` rejette la configuration ambiguë jeton-plus-mot de passe sans mode d'authentification explicite.
- `src/gateway/startup-auth.ts:125` résout les SecretRefs d'authentification Gateway actifs, rejette les secrets d'espace réservé faibles, génère des jetons d'exécution uniquement où autorisé et échoue fermé pour les références actives non résolues.
- `src/gateway/auth.ts:222` valide les options d'authentification jeton/mot de passe/proxy de confiance configurées.
- `src/gateway/auth.ts:270` autorise les requêtes proxy de confiance en utilisant les adresses sources de confiance, `allowLoopback`, le rejet d'interface locale, les en-têtes requis, l'en-tête utilisateur et `allowUsers`.
- `src/gateway/auth.ts:354` autorise les requêtes jeton/mot de passe avec comparaison de secret sûre et comportement de limitation de débit.
- `src/gateway/auth.ts:400` centralise l'autorisation de connexion Gateway, y compris les branches Tailscale et proxy de confiance.
- `src/gateway/auth.ts:504` permet `auth.mode: "none"` explicite et limite l'authentification d'identité Tailscale aux contextes autorisés sans identifiants partagés explicites.
- `src/gateway/net.ts:178` vérifie les adresses de proxy de confiance avec correspondance IP/CIDR.
- `src/gateway/net.ts:193` résout l'IP client à partir des en-têtes transférés uniquement pour les proxies de confiance et échoue fermé sur les chaînes invalides ou non approuvées.
- `src/gateway/net.ts:250` résout les modes de liaison loopback, LAN, tailnet, auto et personnalisé.
- `src/gateway/origin-check.ts:35` analyse et vérifie les origines du navigateur par rapport aux listes d'autorisation explicites, aux hôtes privés de même origine, au loopback local et aux paramètres de secours dangereux.
- `src/gateway/origin-check.ts:80` restreint la confiance de même origine aux hôtes privés, `.local`, `.ts.net` et aux contextes clients loopback locaux.
- `src/cli/gateway-cli/run.ts:223` bloque le démarrage d'assistant non-loopback sans secret partagé sauf si le mode proxy de confiance est configuré.
- `src/cli/gateway-cli/run.ts:754` rejette le mode mot de passe sans mot de passe configuré et enregistre un avertissement explicite pour `auth.mode: "none"`.
- `src/cli/gateway-cli/run.ts:772` refuse la liaison non-loopback sans authentification jeton/mot de passe/proxy de confiance.
- `src/config/validation.ts:833` applique la liaison loopback Tailscale serve/funnel.
- `src/config/validation.ts:860` rejette `auth.mode: "none"` non sûr pour Tailscale serve/funnel.
- `src/shared/gateway-tailscale-auth-policy.ts:3` encode les politiques Tailscale sans authentification et Funnel avec mot de passe.
- `src/security/audit-gateway-config.ts:119` lève des conclusions critiques pour la liaison Gateway non-loopback sans authentification.
- `src/security/audit-gateway-config.ts:165` lève les conclusions d'origine Control UI non-loopback, les avertissements de caractères génériques et les avertissements de secours d'en-tête Host.
- `src/security/audit-gateway-config.ts:209` signale le secours `X-Real-IP` risqué.
- `src/security/audit-gateway-config.ts:242` signale la posture d'exposition Tailscale Funnel et Serve.
- `src/gateway/server/ws-connection.ts:244` enregistre l'hôte, l'origine et les en-têtes transférés et envoie `connect.challenge`.
- `src/gateway/server/ws-connection.ts:472` ferme les sockets non authentifiées inactives après le délai d'expiration de la poignée de main.
- `src/gateway/server/ws-connection/message-handler.ts:529` exige que la première trame soit une requête `connect` valide.
- `src/gateway/server/ws-connection/message-handler.ts:676` applique la politique d'origine du navigateur lors de la poignée de main WebSocket.
- `src/gateway/server/ws-connection/message-handler.ts:716` résout l'état jeton/mot de passe/authentification pour la requête de connexion.
- `src/gateway/server/ws-connection/message-handler.ts:747` retourne les messages d'échec d'authentification et ferme les poignées de main non autorisées.
- `src/gateway/server/ws-connection/message-handler.ts:970` vérifie l'authentification bootstrap/device/partagée et ferme les sessions d'authentification partagée obsolètes après rotation.
- `src/gateway/server/ws-connection/message-handler.ts:1055` résout les portées proxy de confiance et le comportement de saut d'appairage Control UI.
- `src/gateway/server/ws-connection/auth-context.ts:98` résout l'authentification partagée, les candidats de jeton bootstrap, les candidats de jeton device et la classification proxy de confiance.
- `src/gateway/server/ws-connection/connect-policy.ts:37` limite les sauts d'appairage Tailscale et `auth.mode: "none"` aux chemins Control UI d'opérateur.
- `src/gateway/server/ws-connection/handshake-auth-helpers.ts:53` limite le débit des échecs d'authentification d'origine du navigateur et n'exempte pas les origines de navigateur loopback.
- `src/gateway/server/ws-connection/handshake-auth-helpers.ts:197` classe la localité d'appairage pour les contextes locaux et distants.
- `src/gateway/server/ws-connection/handshake-auth-helpers.ts:307` vérifie les signatures de device liées à nonce.

## Tests d'intégration

- `src/gateway/server.auth.modes.suite.ts:18` couvre l'acceptation/rejet d'authentification par mot de passe du serveur réel.
- `src/gateway/server.auth.modes.suite.ts:52` couvre le rejet d'authentification par jeton du serveur réel et le rejet de device manquant de Control UI par défaut.
- `src/gateway/server.auth.modes.suite.ts:114` couvre la connexion loopback explicite `auth.mode: "none"` sans secret partagé.
- `src/gateway/server.auth.modes.suite.ts:145` couvre le comportement WebSocket Control UI authentifié par Tailscale, les exigences de device et les interactions de jeton partagé.
- `src/gateway/server.auth.browser-hardening.test.ts:153` couvre le rejet d'origine de navigateur attaquant.
- `src/gateway/server.auth.browser-hardening.test.ts:241` couvre le rejet d'origine proxy de confiance lorsqu'il n'est pas explicitement autorisé.
- `src/gateway/server.auth.browser-hardening.test.ts:316` couvre le rejet d'origine loopback forgée via les en-têtes transférés.
- `src/gateway/server.auth.browser-hardening.test.ts:461` couvre la limitation de débit d'échec d'authentification d'origine du navigateur.
- `src/gateway/server.auth.control-ui.suite.ts:291` couvre le comportement de rejet d'identité device Control UI proxy de confiance.
- `src/gateway/server.auth.control-ui.suite.ts:381` couvre l'effacement de portée sans device proxy de confiance.
- `src/gateway/server.auth.control-ui.suite.ts:434` couvre la limitation de portée déclarée par proxy.
- `src/gateway/server.preauth-hardening.test.ts:89` couvre le rejet de mise à niveau WebSocket lorsque les gestionnaires ne sont pas disponibles.
- `src/gateway/server.preauth-hardening.test.ts:132` couvre la fermeture de socket non authentifiée inactif après le délai d'expiration de la poignée de main.
- `src/gateway/server.preauth-hardening.test.ts:197` couvre le rejet de trame de connexion pré-authentification surdimensionnée.
- `src/gateway/server.preauth-hardening.test.ts:243` couvre l'application du budget de socket non authentifiée simultanée.
- `src/gateway/probe.auth.integration.test.ts:82` couvre le comportement de sonde/appel authentifié par jeton par rapport à un harnais Gateway en cours d'exécution.
- `src/secrets/runtime.gateway-auth.integration.test.ts:36` couvre l'échec de démarrage pour les SecretRefs d'authentification Gateway actifs non résolus.
- `src/secrets/runtime.gateway-auth.integration.test.ts:67` couvre le rejet de rechargement à chaud des références d'authentification Gateway actives non résolues avant de persister la mauvaise configuration.

## Tests unitaires

- `src/gateway/auth.test.ts:220` couvre la résolution du mode d'authentification explicite à partir de la configuration.
- `src/gateway/auth.test.ts:280` couvre le comportement d'autorisation `auth.mode: "none"` explicite.
- `src/gateway/auth.test.ts:331` couvre l'identité Tailscale désactivée par défaut et activée explicitement.
- `src/gateway/auth.test.ts:415` couvre l'authentification d'en-tête Tailscale désactivée sur les wrappers HTTP et activée sur les wrappers Control UI WS.
- `src/gateway/auth.test.ts:588` couvre les exigences d'authentification proxy de confiance et le comportement de liste d'autorisation.
- `src/gateway/auth.test.ts:1025` couvre le rejet proxy de confiance loopback sauf si `allowLoopback` est défini.
- `src/gateway/auth.test.ts:1153` couvre les vérifications d'en-tête requis et `allowUsers` pour les sources proxy autorisées loopback.
- `src/gateway/auth.test.ts:1206` couvre le comportement de rejet direct loopback d'en-tête transféré.
- `src/gateway/server/ws-connection/connect-policy.test.ts:243` couvre la désactivation dangereuse d'authentification device et les limites de saut d'appairage `auth.mode: "none"`.
- `src/gateway/server/ws-connection/connect-policy.test.ts:284` couvre le saut d'appairage Tailscale uniquement pour Control UI d'opérateur avec identité device.
- `src/gateway/server/ws-connection/handshake-auth-helpers.test.ts:27` couvre le comportement de clé de limitation de débit loopback d'origine du navigateur.
- `src/gateway/server/ws-connection/handshake-auth-helpers.test.ts:327` couvre la classification d'appairage secret partagé local par rapport à distant.
- `src/gateway/origin-check.test.ts:24` couvre l'acceptation LAN/tailnet privée de même origine, le rejet public et les limites loopback-local.
- `src/config/config.gateway-tailscale-bind.test.ts:23` couvre le rejet sans authentification pour Tailscale serve/funnel et les exigences de mot de passe Funnel.
- `src/config/config.gateway-tailscale-bind.test.ts:97` couvre le rejet de liaison non-loopback pour Tailscale serve/funnel.
- `src/security/audit-gateway.test.ts:42` couvre les conclusions d'audit pour la liaison non-loopback sans authentification.
- `src/security/audit-gateway-exposure.test.ts:114` couvre les conclusions d'origine manquante Control UI non-loopback.
- `src/security/audit-gateway-exposure.test.ts:163` couvre les conclusions de secours d'en-tête Host.
- `src/security/audit-gateway-exposure.test.ts:221` couvre les conclusions d'exposition proxy de confiance.
- `src/commands/configure.gateway.test.ts:141` couvre la génération de configuration Gateway proxy de confiance.
- `src/commands/configure.gateway.test.ts:175` couvre l'amorçage d'origine Tailscale et non-loopback.
- `src/gateway/server-runtime-config.test.ts:18` couvre les exigences de configuration proxy de confiance d'exécution.
- `src/gateway/server-runtime-config.test.ts:75` couvre l'autorisation LAN/jeton et le rejet LAN/sans authentification.
- `src/gateway/server-runtime-config.test.ts:132` couvre le rejet de secours loopback et la validation de liaison personnalisée.
- `src/gateway/server-runtime-config.test.ts:203` couvre les exigences `allowedOrigins` non-loopback.

## Requêtes Gitcrawl

- `gitcrawl search issues "gateway auth mode none trusted proxy non-loopback bind" -R openclaw/openclaw --state all --json number,title,url,state` n'a retourné aucune correspondance directe.
- `gitcrawl search issues "trusted proxy allowUsers allowLoopback gateway.auth.mode" -R openclaw/openclaw --state all --json number,title,url,state` n'a retourné aucune correspondance directe.
- `gitcrawl search issues "Control UI allowedOrigins origin websocket gateway auth" -R openclaw/openclaw --state all --json number,title,url,state` a retourné l'ouverture #78674, `[Bug]: Control UI sends null client.id/client.mode through Cloudflare tunnel`.
- `gitcrawl search prs "origin allowedOrigins" -R openclaw/openclaw --state all --json number,title,url,state` a retourné les PRs de durcissement/compatibilité d'origine ouvertes y compris #38290, #68647, #73511 et #85663.
- `gitcrawl search issues "origin not allowed" -R openclaw/openclaw --state all --json number,title,url,state` a retourné les problèmes d'origine et de tunnel ouverts y compris #46520 et #78674.
- `gitcrawl search issues "trusted proxy" -R openclaw/openclaw --state all --json number,title,url,state` a retourné les threads proxy de confiance et d'identité ouverts y compris #73638, #73639, #70729, #23585, #86525, #80063, #43786, #69066, #43903, #87268, #57110 et #87376.
- `gitcrawl search prs "trusted proxy" -R openclaw/openclaw --state all --json number,title,url,state` a retourné les PRs de durcissement/docs/config proxy de confiance ouvertes y compris #86527, #85950, #49107, #57889, #73163, #87379 et #85261.
- `gitcrawl search issues "Tailscale gateway auth" -R openclaw/openclaw --state all --json number,title,url,state` a retourné les threads Tailscale/authentification ouverts y compris #57110, #85750, #55915, #46919, #70729, #85966, #53274, #87216 et #65619.
- `gitcrawl search issues "gateway token password auth" -R openclaw/openclaw --state all --json number,title,url,state` a retourné les threads d'authentification/sécurité ouverts y compris #87376, #57110, #83880, #73638/#73639, #78712 et #72418.

## Requêtes Discrawl

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "gateway auth mode none trusted proxy non-loopback bind"` a retourné une réponse d'assistance récente expliquant que `127.0.0.1` n'est pas public, l'exposition dépend de `gateway.bind` et `gateway.auth.mode`, loopback+jeton/mot de passe est raisonnablement sécurisé, LAN/tailnet/personnalisé avec jeton/mot de passe est accessible à distance mais protégé, et `none` est risqué en dehors de l'entrée locale/privée.
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI allowedOrigins websocket auth Tailscale Serve"` a retourné six threads d'assistance sur `allowedOrigins` exact `https://<magicdns>.ts.net`, la réachabilité Tailscale par rapport au rejet d'origine du navigateur, les avertissements d'audit de sécurité pour le secours d'en-tête Host/authentification device désactivée/lacunes de limitation de débit et les limitations d'authentification HTTP/device non sécurisées d'autres machines.
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "gateway auth Tailscale Funnel password Serve identity headers"` a retourné des threads d'assistance clarifiant que l'authentification Tailscale sans jeton est uniquement pour Serve plus `allowTailscale`, couvre uniquement Control UI/WS, les API HTTP normales nécessitent toujours jeton/mot de passe, Funnel manque d'en-têtes d'identité et nécessite un mot de passe, et les jetons de profil incorrects causent HTTP 401.
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "OpenClaw reverse proxy trustedProxies x-forwarded-user"` a retourné un thread d'assistance proxy de confiance expliquant que le mode est pour les proxies inverses qui terminent TLS/authentifient/injectent les en-têtes d'identité et que les appels sandbox loopback directs n'autorisent pas automatiquement.
