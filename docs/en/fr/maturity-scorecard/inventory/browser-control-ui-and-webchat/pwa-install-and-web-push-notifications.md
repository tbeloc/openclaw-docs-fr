---
title: "Gateway Web App - PWA Install and Web Push Notifications Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - PWA Install and Web Push Notifications Maturity Note

## Résumé

L'interface de contrôle fournit un manifeste PWA, l'enregistrement du service worker en production, les appels d'interface utilisateur d'abonnement aux notifications push web, la gestion des clés VAPID, les abonnements aux notifications push persistants, et les méthodes Gateway pour s'abonner, se désabonner, récupérer les clés publiques VAPID et envoyer des notifications de test. La couverture est Beta car la persistance et les méthodes serveur ont des tests, mais le comportement réel des notifications du navigateur et des PWA installées est moins prouvé. La qualité est Beta car la conception est explicite et délimitée, tandis que les preuves d'archive et la source actuelle montrent que c'est plus récent et facile à confondre avec le push APNS natif.

## Portée de la catégorie

Cette catégorie couvre les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker en production, la gestion des événements push, le comportement des clics de notification, la génération des clés VAPID/les remplacements d'env, le stockage des abonnements aux notifications push web, les RPC Gateway `push.web.*`, et les contrôles de notification de l'interface de contrôle qui les appellent.

## Fonctionnalités

- Métadonnées d'installation PWA : Couvre les métadonnées d'installation PWA dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker en production, la gestion des événements push, le comportement des clics de notification, et le comportement associé d'installation PWA et de notifications push web.
- Mises à jour du service worker : Couvre les mises à jour du service worker dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker en production, la gestion des événements push, le comportement des clics de notification, et le comportement associé d'installation PWA et de notifications push web.
- Clés VAPID : Couvre les clés VAPID dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker en production, la gestion des événements push, le comportement des clics de notification, et le comportement associé d'installation PWA et de notifications push web.
- S'abonner/se désabonner : Couvre S'abonner/se désabonner dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker en production, la gestion des événements push, le comportement des clics de notification, et le comportement associé d'installation PWA et de notifications push web.
- Notifications de test : Couvre les notifications de test dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker en production, la gestion des événements push, le comportement des clics de notification, et le comportement associé d'installation PWA et de notifications push web.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : Les tests source couvrent la gestion des clés VAPID, le stockage des abonnements, les méthodes push Gateway, le comportement du cache du service worker, et la fourniture du manifeste public/service worker.
- Signaux négatifs : Les abonnements réels aux notifications push du navigateur nécessitent des contextes sécurisés et un comportement de permission du navigateur/système d'exploitation. Le comportement de réveil des PWA installées et le comportement des clics/focus de notification manquent de preuves de scénarios en direct larges.
- Lacunes d'intégration : Ajouter un test de fumée en direct du navigateur pour s'abonner/se désabonner/envoyer une notification de test sur localhost HTTPS ou Tailscale Serve, focus/ouverture PWA installée, nettoyage des abonnements expirés, et refus de permission du navigateur.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : Les requêtes de notifications push web ont trouvé la PR #73894, `Add Control UI notification controls and web push test fixes`, plus la PR du service worker #87077 et le problème PWA/icône #55600.
- Rapports Discrawl : La requête exacte de notifications push web n'a retourné aucune ligne ; le trafic plus large de l'interface de contrôle montre que les notifications et le comportement du service worker sont toujours adjacents à la version.
- Bonnes qualités : Web Push est séparé du push APNS, les identifiants VAPID peuvent être épinglés à l'env, les abonnements sont indexés par point de terminaison, les RPC push sont limités en écriture par l'opérateur, et le service worker maintient la gestion de la charge utile de notification petite.
- Mauvaises qualités : Le push du navigateur dépend du contexte sécurisé, de l'UX de permission du navigateur, du comportement des PWA installées, et des détails du service worker spécifiques au navigateur qui ne sont pas encore représentés par une preuve en direct récurrente.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel affectent uniquement la couverture.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les métadonnées d'installation PWA, les mises à jour du service worker, les clés VAPID, S'abonner/se désabonner, les notifications de test.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La documentation ne fournit pas encore de guide opérationnel étape par étape pour les défaillances de permission de notification du navigateur.
- Le comportement des PWA installées a besoin de preuves multi-navigateurs et mobiles.
- Web Push peut être confondu avec le push APNS natif relayé par relais à moins que la documentation et l'interface utilisateur maintiennent la limite évidente.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente le manifeste PWA, le service worker, les fichiers VAPID, les remplacements d'env VAPID, les RPC `push.web.*`, et la limite du push de relais APNS iOS.
- `/Users/kevinlin/code/openclaw/docs/gateway/protocol.md` répertorie `push.web.vapidPublicKey`, `push.web.subscribe`, `push.web.unsubscribe`, et `push.web.test`.

### Source

- `/Users/kevinlin/code/openclaw/ui/public/manifest.webmanifest` est le manifeste PWA.
- `/Users/kevinlin/code/openclaw/ui/public/sw.js` implémente les gestionnaires de push et de clic de notification.
- `/Users/kevinlin/code/openclaw/ui/src/main.ts` enregistre le service worker en production.
- `/Users/kevinlin/code/openclaw/ui/src/ui/push-subscription.ts` demande la permission, lit les clés VAPID, s'abonne, se désabonne et envoie des pushes de test.
- `/Users/kevinlin/code/openclaw/src/infra/push-web.ts` gère les clés VAPID et la persistance des abonnements.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/push.ts` expose les RPC Gateway de notifications push web.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/push.test.ts` couvre la gestion des RPC push Gateway.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui.http.test.ts` couvre la fourniture du manifeste et du service worker.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/infra/push-web.test.ts` couvre la génération des clés VAPID, les remplacements d'env, l'enregistrement/la liste/la suppression des abonnements et les envois.
- `/Users/kevinlin/code/openclaw/ui/src/ui/service-worker-cache.test.ts` couvre la gestion des versions du cache du service worker.
- `/Users/kevinlin/code/openclaw/src/gateway/protocol/push.test.ts` couvre les schémas de protocole pour les charges utiles push.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Control UI web push PWA VAPID notification service worker"`

Résultats :

- Retourné `[]`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "web push"`

Résultats :

- Retourné la PR ouverte #73894, `Add Control UI notification controls and web push test fixes`.
- Retourné les PR adjacentes #73923, #73987, #87077 et #87192.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "PWA Control UI"`

Résultats :

- Retourné l'ouverture #55600, `Control UI header logo/icon not displaying after 2026.3.24 update`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI web push PWA VAPID notification service worker"`

Résultats :

- Retourné aucune ligne.
