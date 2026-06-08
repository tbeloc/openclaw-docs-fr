---
title: "Automatisation des navigateurs et outils exec/sandbox - Note de maturité sur la sécurité des navigateurs, SSRF et le contrôle à distance"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation des navigateurs et outils exec/sandbox - Note de maturité sur la sécurité des navigateurs, SSRF et le contrôle à distance

## Résumé

La sécurité des navigateurs, SSRF et le contrôle à distance sont en version Bêta. Les contrôles sont réels :
authentification du contrôle du navigateur, garde-fous de navigation stricte, politique SSRF, résultats d'audit CDP à distance,
politique de réachabilité loopback/CDP et vérifications de navigation post-action.
Le score reste Bêta car le comportement localhost/file/private-network est toujours
surprenant pour les utilisateurs, le CDP à distance est intrinsèquement sensible, et les exceptions de politique
doivent être gérées avec précision.

## Portée de la catégorie

Cette note couvre l'authentification du contrôle du navigateur, la validation des URL de navigation, les garde-fous de navigation retardés, la politique SSRF stricte de réseau privé, les protocoles non pris en charge, la réachabilité CDP à distance et les avertissements d'audit, le contournement loopback/CDP pour le plan de contrôle propre d'OpenClaw, et la documentation de sécurité des navigateurs.

## Fonctionnalités

- Sécurité des navigateurs : Couvre la sécurité des navigateurs sur l'authentification du contrôle du navigateur, la validation des URL de navigation, les garde-fous de navigation retardés, la politique SSRF stricte de réseau privé, et le comportement associé de sécurité des navigateurs, ssrf et contrôle à distance.
- SSRF : Couvre SSRF sur l'authentification du contrôle du navigateur, la validation des URL de navigation, les garde-fous de navigation retardés, la politique SSRF stricte de réseau privé, et le comportement associé de sécurité des navigateurs, ssrf et contrôle à distance.
- Contrôle à distance : Couvre le contrôle à distance sur l'authentification du contrôle du navigateur, la validation des URL de navigation, les garde-fous de navigation retardés, la politique SSRF stricte de réseau privé, et le comportement associé de sécurité des navigateurs, ssrf et contrôle à distance.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`
- Signaux positifs :
  - La documentation décrit la politique SSRF des navigateurs, la gestion loopback/réseau privé, le risque CDP à distance et l'exposition du contrôle du navigateur.
  - Le code source applique les vérifications de navigation avant et après les actions et les instantanés.
  - Le code source audite l'authentification du contrôle du navigateur manquante, le CDP à distance HTTP et les hôtes CDP à distance privés.
  - Les tests couvrent le comportement du garde-fou de navigation, les gardes post-action de session existante, l'authentification loopback, la validation du profil à distance et les résultats d'audit de sécurité.
- Signaux négatifs :
  - Le comportement de sécurité n'est pas uniforme sur les chemins du navigateur géré, de la session existante, du CDP à distance et du navigateur sandbox.
  - Les preuves d'archive en direct montrent que les utilisateurs rencontrent toujours `navigation du navigateur bloquée par la politique` pour les URL localhost et file et ont besoin de clarification.
- Lacunes d'intégration :
  - Ajouter une matrice de sécurité en direct pour le navigateur géré, la session existante, le CDP à distance et le sandbox qui prouve le comportement localhost, file, réseau privé et liste d'autorisation explicite.
  - Ajouter des exemples de documentation qui associent les flux de travail courants du tableau de bord local à la liste d'autorisation SSRF exacte ou à la cible de profil plus sûre.

## Score de qualité

- Score : `Bêta (74%)`
- Rapports Gitcrawl :
  - `navigation CDP SSRF à distance du navigateur bloquée` a retourné le problème ouvert #67966 pour l'interception de navigation Playwright en mode navigateur local-géré.
  - La recherche plus large `sandbox du navigateur` a retourné le problème #84942 sur l'inadéquation cible/sandbox du navigateur, le problème #52662 pour les backends sandbox/navigateur non-Docker, le problème #64383 sur la simplification du chemin CDP du navigateur sandbox et le problème #43803 sur le rechargement à chaud du profil du navigateur.
- Rapports Discrawl :
  - `navigation du navigateur bloquée par la politique` a retourné un rapport du 2026-05-11 où HTTPS public a réussi mais `127.0.0.1`, `localhost` et `file://` ont échoué avec des messages de politique/protocole non pris en charge du navigateur.
  - La même requête a retourné une discussion d'archive sur les correctifs SSRF CDP loopback et les exigences de révision de sécurité/redaction d'URL.
- Bonnes qualités :
  - L'authentification du contrôle du navigateur est générée/persistée via l'authentification de la passerelle et peut échouer de manière sécurisée.
  - Les vérifications de navigation bloquent les protocoles non pris en charge, l'accès strict au réseau privé et les chaînes de redirection bloquées.
  - Les points de terminaison CDP à distance sont audités pour HTTP simple et les hôtes privés/internes.
  - Les interactions de session existante revérifient les URL des onglets actuels et nouvellement ouverts après la navigation retardée.
- Mauvaises qualités :
  - La politique est précise mais difficile à expliquer : le contrôle CDP loopback peut être autorisé tandis que la navigation du navigateur vers loopback reste bloquée.
  - Les flux de travail `file://` et localhost/dashboard sont des cas courants de développement local mais peuvent être rejetés par défaut.
  - Le CDP à distance est un point de terminaison de contrôle de confiance, et la documentation doit continuer à rappeler aux utilisateurs de ne pas l'exposer facilement.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, en direct et flux d'exécution affectées
    Couverture uniquement.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves de documentation archivée, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la sécurité des navigateurs, SSRF, contrôle à distance.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le modèle de sécurité a besoin d'une sortie "pourquoi bloqué" plus claire pour les destinations du navigateur localhost, file, CDP à distance et réseau privé.
- La posture de sécurité du CDP à distance doit rester sous audit actif car c'est un plan de contrôle du navigateur, pas une navigation web normale.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/tools/browser.md:216` : la documentation du navigateur pointe vers la gestion de la politique SSRF.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-control.md:360` : la documentation de sécurité avertit sur l'évaluation du navigateur, l'accès privé à la passerelle/nœud, la protection CDP à distance et les exemples SSRF stricts.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md:240` : la documentation de sécurité appelle la dérive d'approbation exec et l'exposition du contrôle du navigateur comme domaines d'examen.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md:1174` : les destinations du navigateur privé/interne/usage spécial restent bloquées sauf si explicitement autorisées.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/audit-checks.md:80` : le tableau d'audit inclut le CDP à distance sur HTTP et les résultats d'hôte privé.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/audit-checks.md:89` : le tableau d'audit inclut la découverte critique de publication non-loopback du conteneur du navigateur sandbox.

### Code source

- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/navigation-guard.ts:10` : seules les URL http/https et about:blank sont des cibles de navigation de navigateur valides.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/navigation-guard.ts:90` : les vérifications d'URL de navigation bloquent le protocole non pris en charge, SSRF strict routé par proxy et les noms d'hôte non autorisés.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/navigation-guard.ts:151` : les chaînes de redirection post-navigation sont vérifiées.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/control-auth.ts:17` : l'authentification du contrôle du navigateur se résout à partir de l'authentification de la passerelle.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/control-auth.ts:117` : l'authentification du contrôle du navigateur peut être générée et persistée.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/cdp-reachability-policy.ts:19` : la réachabilité CDP contourne loopback local uniquement pour le plan de contrôle propre d'OpenClaw.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/security-audit.ts:68` : l'audit de sécurité du navigateur émet une découverte critique lorsque les routes HTTP de contrôle n'ont pas d'authentification.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/security-audit.ts:93` : l'audit avertit lorsque le CDP à distance utilise HTTP.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/security-audit.ts:102` : l'audit avertit lorsque le CDP à distance cible des hôtes privés/internes sous l'opt-in du réseau privé.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/browser-cdp-snapshot-docker.sh:84` : l'E2E du navigateur Docker vérifie l'opération du navigateur basée sur CDP en direct.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/chrome.loopback-ssrf.integration.test.ts:1` : la couverture d'intégration existe pour le comportement SSRF loopback.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/pw-tools-core.interactions.navigation-guard.test.ts:73` : vérifie que le garde-fou de navigation post-clic s'exécute lorsque la navigation commence après un clic.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/pw-tools-core.interactions.navigation-guard.test.ts:267` : vérifie que la navigation privée de sous-cadre uniquement est bloquée.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/routes/agent.act.existing-session-navigation-guard.test.ts:131` : vérifie que l'interaction de session existante vérifie la navigation après clic et soumission de clé.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/routes/agent.act.existing-session-navigation-guard.test.ts:219` : vérifie que les URL d'onglet nouvellement ouvert bloquées échouent de manière sécurisée.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/profiles-service.test.ts:225` : vérifie que le mode SSRF strict rejette le CDP à distance du réseau privé.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server.auth-token-gates-http.test.ts:1` : vérifie les portes de jeton d'authentification HTTP du navigateur.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/security-audit.test.ts:1` : vérifie les résultats d'audit de sécurité du navigateur.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "browser SSRF remote CDP navigation blocked" --json`

Résultats :

- Problème ouvert #67966 : Interception de navigation Playwright pour le mode navigateur local-géré.

Requête :

`gitcrawl search openclaw/openclaw --query "browser sandbox" --json`

Résultats :

- Problème ouvert #84942 : les rapports de politique sandbox indiquent sandboxé tandis que target=sandbox navigateur n'est pas disponible.
- Problème ouvert #52662 : le sandbox du navigateur devrait supporter les backends non-Docker.
- Problème ouvert #64383 : évaluer la simplification du chemin CDP du navigateur sandbox.

### Requêtes Discrawl

Requête :

`discrawl search --mode fts --limit 5 "browser navigation blocked policy"`

Résultats :

- Rapport clawtributors du 2026-05-11 : HTTPS public a réussi, tandis que `127.0.0.1`,
  `localhost` et les URL du tableau de bord `file://` ont échoué avec des messages de politique du navigateur ou de protocole non pris en charge.
- Commentaires d'archive OpenClaw du 2026-04-25 décrivant les correctifs SSRF CDP loopback et les exigences de révision de sécurité/redaction d'URL pour l'exposition de l'URL de l'onglet.
