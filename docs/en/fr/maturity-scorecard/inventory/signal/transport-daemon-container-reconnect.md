---
title: "Signal - Transport Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Transport Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Transport, Daemon, Container, and Reconnect` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Inclus dans cette catégorie :

- Transport daemon natif : Couvre le routage du transport daemon natif, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.
- Transport conteneur : Couvre le routage du transport conteneur, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.
- Sélection du mode API : Couvre le routage de la sélection du mode API, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.
- Réception reconnect/readiness : Couvre le routage de la réception reconnect/readiness, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.

## Fonctionnalités

- Transport daemon natif : Couvre le routage du transport daemon natif, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.
- Transport conteneur : Couvre le routage du transport conteneur, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.
- Sélection du mode API : Couvre le routage de la sélection du mode API, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.
- Réception reconnect/readiness : Couvre le routage de la réception reconnect/readiness, la liaison de session, l'historique et le contexte de conversation pour Transport, Daemon, Container, et Reconnect.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (60%)`

La couverture est Alpha car les chemins de transport daemon natif et conteneur sont documentés et testés unitairement, mais aucune preuve SSE en direct ou de réception conteneur n'a été trouvée pour la source actuelle.

## Score de qualité

- Score : `Alpha (58%)`

La qualité est Alpha car l'adaptateur est large mais les rapports d'historique d'opérateur récents signalent un blocage de réception entrant, et la source arrête toujours le daemon avec un chemin `SIGTERM` fire-and-forget. Exclus de la qualité : preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution ; ceux-ci affectent uniquement la couverture.

## Score de complétude

- Score : `Alpha (60%)`
- Instructions de surface : évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le transport daemon natif, le transport conteneur, la sélection du mode API, la réception reconnect/readiness.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Docs

- `docs/channels/signal.md` lignes 170-183 décrivent le JSON-RPC daemon natif plus SSE.
- `docs/channels/signal.md` lignes 185-240 décrivent le mode REST/WebSocket conteneur bbernhard, `apiMode`, `MODE=json-rpc`, les opérations supportées et les notes opérationnelles.
- `docs/channels/signal.md` lignes 263-268 indiquent que le mode natif utilise SSE, le mode conteneur utilise la réception WebSocket, et les deux normalisent les enveloppes avant le routage.
- `docs/channels/signal.md` lignes 346-363 listent les commandes de dépannage du transport et les défaillances courantes.

### Source

- `extensions/signal/src/client-adapter.ts` résout `apiMode`, met en cache le mode détecté automatiquement, préfère le mode natif quand disponible, mappe les appels RPC aux implémentations natives/conteneur, diffuse les événements via SSE natif ou WebSocket conteneur, et récupère les pièces jointes via les deux adaptateurs.
- `extensions/signal/src/sse-reconnect.ts` exécute une boucle de reconnexion consciente de l'abandon avec backoff après la fin du flux ou une erreur.
- `extensions/signal/src/daemon.ts` construit les arguments du daemon natif, résout les chemins de config `~`, classe les journaux, lance `signal-cli daemon --http`, et expose l'état stop/exited.
- `extensions/signal/src/monitor/tool-result.ts` démarre le daemon, attend la readiness, diffuse les événements et s'arrête à l'abandon.

### Tests d'intégration

- `extensions/signal/src/approval-handler.runtime.test.ts` exerce la livraison d'exécution via l'adaptateur d'approbation mais ne prouve pas le transport Signal en direct.
- Aucun scénario de réception SSE en direct ou de réception WebSocket conteneur n'a été trouvé dans `qa/`, `test/`, ou `tests`.

### Tests unitaires

- `extensions/signal/src/client-container.test.ts` valide `/v1/about`, les règles de mise à niveau WebSocket, l'analyse des messages reçus, le mappage des requêtes REST, la dactylographie, les reçus, les récupérations de pièces jointes, les réactions et le mappage RPC.
- `extensions/signal/src/monitor.tool-result.autostart.test.ts` couvre les vérifications de readiness bornées, le remplacement du délai d'expiration de démarrage, les arguments daemon du chemin de config, les plafonds de délai d'expiration, l'échec rapide à la sortie du daemon et l'arrêt après abandon.
- `extensions/signal/src/monitor.tool-result.pairs-uuid-only-senders-uuid-allowlist-entry.test.ts` couvre la reconnexion après les erreurs de flux.
- `extensions/signal/src/daemon.test.ts` couvre l'expansion du chemin de config et la classification des journaux.

### Requêtes Gitcrawl

- Requête : `Signal inbound SSE listener wedged channels status`
  - Résultats : le problème ouvert `#75426` signale que les sorties et les sondes peuvent fonctionner tandis que les DM entrants ne sont pas fiables et `channels status` expire.
- Requête : `Signal daemon stop race orphaned`
  - Résultats : le problème ouvert `#22676` signale un comportement de course/processus orphelin à l'arrêt du daemon ; la PR ouverte `#71863` propose d'attendre l'arrêt du daemon au redémarrage.
- Requête : `Signal apiMode container WebSocket receive`
  - Résultats : aucun résultat compact actuel n'a prouvé un chemin de réception conteneur en direct.

### Requêtes Discrawl

- Requête : `Signal apiMode container WebSocket receive`
  - Résultats : un examen Discord du 2026-04-26 de la PR `#16085` a dit que main n'avait alors que JSON-RPC/SSE natif et manquait `apiMode` ; la source actuelle implémente maintenant `apiMode`, donc ceci a été traité comme une dérive historique à vérifier, pas une défaillance actuelle.
- Requête : `Signal daemon stop race orphaned`
  - Résultats : les commentaires du miroir GitHub Discord pour le problème `#22676` ont dit que la course était toujours non corrigée lors des examens d'avril.
- Requête : `Signal inbound SSE listener wedged channels status`
  - Résultats : le contenu du miroir GitHub Discord correspondait au problème `#75426` et au rapport de blocage de réception/statut.
