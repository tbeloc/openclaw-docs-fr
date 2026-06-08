---
title: "Gateway Web App - Browser UI Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - Browser UI Maturity Note

## Résumé

Le shell Control UI du navigateur est une application Vite/Lit servie par Gateway de première classe avec routage par chemin de base, gestion des actifs statiques, en-têtes de sécurité, actifs de manifeste et de service-worker, et flux de construction/ouverture documentés. La couverture est Stable car le chemin de service HTTP et le comportement du service-worker ont des tests serveur et UI ciblés. La qualité est Beta car l'implémentation a des limites de routage et d'en-têtes fortes, mais les preuves d'archive montrent toujours des problèmes de service-worker obsolète, d'empaquetage d'actifs et de rechargement du navigateur comme risques opérateurs en direct.

## Portée de la catégorie

Inclus dans cette catégorie :

- Interface utilisateur hébergée par Gateway : Couvre l'interface utilisateur hébergée par Gateway sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Amorçage ouverture/authentification du tableau de bord : Couvre l'amorçage ouverture/authentification du tableau de bord sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Routage par chemin de base : Couvre le routage par chemin de base sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Récupération des actifs statiques : Couvre la récupération des actifs statiques sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Cible gatewayUrl de développement : Couvre la cible gatewayUrl de développement sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Métadonnées d'installation PWA : Couvre les métadonnées d'installation PWA sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- Mises à jour du service worker : Couvre les mises à jour du service worker sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- Clés VAPID : Couvre les clés VAPID sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- S'abonner/se désabonner : Couvre l'abonnement/désabonnement sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- Notifications de test : Couvre les notifications de test sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.

## Fonctionnalités

- Interface utilisateur hébergée par Gateway : Couvre l'interface utilisateur hébergée par Gateway sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Amorçage ouverture/authentification du tableau de bord : Couvre l'amorçage ouverture/authentification du tableau de bord sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Routage par chemin de base : Couvre le routage par chemin de base sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Récupération des actifs statiques : Couvre la récupération des actifs statiques sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Cible gatewayUrl de développement : Couvre la cible gatewayUrl de développement sur le service du bundle Control UI depuis Gateway, routage racine et chemin de base, comportement MIME/cache des actifs statiques, actifs PWA publics, et comportement de shell et routage de contrôle ui associé.
- Métadonnées d'installation PWA : Couvre les métadonnées d'installation PWA sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- Mises à jour du service worker : Couvre les mises à jour du service worker sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- Clés VAPID : Couvre les clés VAPID sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- S'abonner/se désabonner : Couvre l'abonnement/désabonnement sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.
- Notifications de test : Couvre les notifications de test sur les métadonnées d'installation PWA du navigateur, l'enregistrement du service-worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement d'installation pwa et de notifications web push associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : Les tests HTTP Gateway couvrent le service Control UI, le comportement auto-racine, le routage, CSP, la gestion MIME du manifeste et du service-worker, et les chemins e2e des médias d'assistant ; les tests UI couvrent le versioning du cache du service-worker et les flux de chat du navigateur simulés.
- Signaux négatifs : La couverture est la plus forte pour le comportement du serveur local et les flux du navigateur simulés. L'installation multi-navigateurs, l'installation PWA mobile, le rechargement du proxy inverse et la preuve de fraîcheur des actifs installés par paquet sont plus minces.
- Lacunes d'intégration : Ajouter un smoke test navigateur installé par paquet récurrent pour localhost, chemin de base, Tailscale Serve, authentification du proxy inverse, mise à jour du service-worker et invites d'installation PWA sur au moins Chromium plus un navigateur non-Chromium.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : Les requêtes de service-worker et PWA ont trouvé #87268 ouvert pour la gestion 401 de niveau supérieur du service-worker, #85939 pour le comportement des données de rechargement de page complète, #55600 pour l'affichage des actifs d'icône, et PR #87077 pour le contournement de la navigation de niveau supérieur.
- Rapports Discrawl : La requête exacte shell/PWA n'a retourné aucune ligne, mais le trafic d'archive Control UI plus large inclut la confusion d'intégration du panneau de contrôle hébergé et les notes de version autour des régressions Control UI/chat.
- Bonnes qualités : Le routage garde les routes API et plugin en dehors du catch-all SPA, la rétention du cache du service-worker est limitée par l'id de construction, Gateway applique des en-têtes statiques conservateurs, et les docs décrivent la récupération de page blanche et la réparation des incompatibilités de protocole.
- Mauvaises qualités : L'état du navigateur obsolète, les actifs du service-worker obsolète et la disponibilité des actifs empaquetés restent des modes de défaillance opérateurs récurrents, en particulier après les mises à niveau et les déploiements hébergés/proxy.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel affectent uniquement la couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'interface utilisateur hébergée par Gateway, l'amorçage ouverture/authentification du tableau de bord, le routage par chemin de base, la récupération des actifs statiques, la cible gatewayUrl de développement, les métadonnées d'installation PWA, les mises à jour du service worker, les clés VAPID, l'abonnement/désabonnement, les notifications de test.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'installation PWA mobile et le comportement de mise à jour du navigateur ont besoin d'une preuve de smoke de version explicite.
- Les déploiements hébergés et proxy inverse ont besoin d'un runbook de service-worker obsolète plus fort.
- Les problèmes d'empaquetage d'actifs apparaissent toujours dans l'historique d'archive même si le chemin du serveur HTTP local est bien défini.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente l'application Vite/Lit servie par la Gateway, l'URL par défaut, `gateway.controlUi.basePath`, le manifeste PWA, le service worker, la réparation des incompatibilités de protocole, la récupération de page blanche, et les commandes de build.
- `/Users/kevinlin/code/openclaw/docs/web/index.md` documente la surface web, les modes de liaison, la configuration Control UI activée par défaut, et la commande de build statique.
- `/Users/kevinlin/code/openclaw/docs/web/dashboard.md` documente le chemin d'ouverture du tableau de bord et la transmission d'authentification depuis `openclaw dashboard`.

## Source

- `/Users/kevinlin/code/openclaw/src/gateway/control-ui.ts` sert les actifs statiques, les actifs PWA publics, les routes de médias d'assistant, les routes d'avatar, et les en-têtes de sécurité Control UI.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-routing.ts` classifie les requêtes Control UI montées à la racine et au chemin de base tout en excluant `/api`, `/plugins`, et les routes de sonde.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-csp.ts` construit le CSP utilisé par les pages servies.
- `/Users/kevinlin/code/openclaw/ui/public/sw.js` implémente les gestionnaires d'installation, d'activation, d'élagage du cache, de récupération, de notification push, et de clic de notification.
- `/Users/kevinlin/code/openclaw/ui/src/main.ts` enregistre le service worker en production avec une requête d'ID de build et désenregistre les anciens workers de développement.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/control-ui.http.test.ts` couvre le service HTTP, le comportement des actifs statiques, le manifeste, et les routes du service worker.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui.auto-root.http.test.ts` couvre le service auto-root.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-routing.test.ts` couvre la classification du routage.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-csp.test.ts` couvre le comportement de l'en-tête CSP.
- `/Users/kevinlin/code/openclaw/ui/src/ui/e2e/chat-flow.e2e.test.ts` exerce le harnais UI servi à travers les flux de chat Gateway simulés.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/service-worker-cache.test.ts` couvre la gestion des versions du cache du service worker et les caches de build antérieurs conservés.
- `/Users/kevinlin/code/openclaw/ui/src/ui/mount-fallback.test.ts` couvre le comportement de secours du montage.
- `/Users/kevinlin/code/openclaw/src/infra/control-ui-assets.test.ts` couvre la résolution de la racine des actifs.

## Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "service worker Control UI"`

Résultats :

- Retourné ouvert #87268, `Control UI service worker swallows top-level 401 from reverse-proxy auth, suppressing browser native credentials dialog`.
- Retourné ouvert #85939, `Control UI: browser (F5) full-page reload re-fetches all API data - slow and state-less`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "service worker Control UI"`

Résultats :

- Retourné PR ouvert #87077, `fix(ui): bypass service worker for top-level navigations`.
- Retourné PR ouvert #74715, `fix(ui): show Communication Notifications tab`.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "PWA Control UI"`

Résultats :

- Retourné ouvert #55600, `Control UI header logo/icon not displaying after 2026.3.24 update`.

## Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI service worker PWA protocol mismatch blank page"`

Résultats :

- Aucune ligne retournée.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 20 "Control UI"`

Résultats :

- Trouvé une discussion de support du panneau de contrôle hébergé où l'accès direct au tableau de bord `fly.dev` était censé échouer derrière l'authentification hébergée.
- Trouvé du trafic de version et de mainteneur nommant les régressions Control UI/chat et l'état obsolète comme points chauds bêta/version.
