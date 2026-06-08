---
title: "iMessage / BlueBubbles - imsg Transport, Host Requirements, and Permissions Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - imsg Transport, Host Requirements, and Permissions Maturity Note

## Résumé

Le composant de transport et d'exigences d'hôte est en version bêta. Le runtime supporté est clair : OpenClaw lance `imsg rpc` sur stdio sur un hôte macOS Messages connecté ou via un wrapper SSH transparent. La documentation et le code source couvrent les principaux contrôles d'opérateur, mais le composant est limité par l'état macOS en direct : Full Disk Access, Automation, statut du bridge API privée/SIP, comportement du wrapper distant et la disponibilité de `watch.subscribe` peuvent toujours échouer en dehors des tests contrôlés par le référentiel.

## Portée de la catégorie

Cette note couvre les `imsg rpc` locaux et distants, `cliPath`, `dbPath`, `remoteHost`, Full Disk Access, Automation, sondage du bridge API privée, détection de capacité RPC et comportement de statut/sondage. Hors de portée : politique DM/groupe, actions de message après que le bridge soit disponible et traduction de configuration BlueBubbles.

## Fonctionnalités

- Exécuter imsg localement : Couvre l'exécution d'imsg localement sur les `imsg rpc`, `cliPath`, `dbPath`, `remoteHost` locaux et distants, ainsi que le comportement de transport imsg, d'exigences d'hôte et de permissions associés.
- Exécuter via un wrapper SSH : Couvre l'exécution via un wrapper SSH sur les `imsg rpc`, `cliPath`, `dbPath`, `remoteHost` locaux et distants, ainsi que le comportement de transport imsg, d'exigences d'hôte et de permissions associés.
- Accorder les permissions macOS : Couvre l'octroi des permissions macOS sur les `imsg rpc`, `cliPath`, `dbPath`, `remoteHost` locaux et distants, ainsi que le comportement de transport imsg, d'exigences d'hôte et de permissions associés.
- Sonder la santé du runtime : Couvre le sondage de la santé du runtime sur les `imsg rpc`, `cliPath`, `dbPath`, `remoteHost` locaux et distants, ainsi que le comportement de transport imsg, d'exigences d'hôte et de permissions associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (72%)`
- Signaux positifs :
  - La documentation spécifie le contrat d'hôte, la forme du wrapper SSH, le modèle de permission, le bridge API privée et le flux de sondage de statut.
  - Le code source dispose d'un client RPC dédié, d'une sonde API privée, d'une sonde de statut à portée de compte, d'une garde par défaut non-mac et d'une promotion d'erreur Full Disk Access plus claire.
  - La couverture unitaire exerce le comportement de statut/sondage, `cliPath` et `dbPath` configurés, le support des méthodes de bridge et la réessai de démarrage de `watch.subscribe`.
  - Les tests de statut de passerelle exercent la dispatch de sonde `channels.status` détenue par le plugin.
- Signaux négatifs :
  - Aucune voie de test macOS/imsg en direct n'a été trouvée qui prouve un hôte Messages réel, les permissions TCC, Automation, le wrapper SSH et la sonde API privée ensemble.
  - Les preuves de terrain incluent les délais d'expiration et les défaillances de permissions `imsg rpc` ouverts/récents.
  - La correction du wrapper distant est documentée et gardée, mais pas exhaustivement prouvée sur la mise en mémoire tampon du shell, launchd, l'identité SSH et les états de veille Mac.
- Lacunes d'intégration :
  - Ajouter une voie Mac en direct contrôlée qui exécute `imsg rpc --help`, `imsg status --json`, `openclaw channels status --probe`, envoi basique et `watch.subscribe`.
  - Ajouter une preuve de wrapper SSH distant avec récupération de pièce jointe `remoteHost` et aucun fallback `chat.db` local par défaut.

## Score de qualité

- Score : `Bêta (70%)`
- Rapports Gitcrawl :
  - `imsg rpc timeout gateway` a retourné le problème ouvert #87263, « 5.22: imsg rpc watch.subscribe timeout on every gateway start - iMessage channel dead ».
  - `iMessage private API` a retourné le problème ouvert #84329 concernant les envois sortants préférant le transport IMCore configurable lorsque le support API privée existe, plus #79610 concernant les stderr AddressBook Apple bénins enregistrés au niveau d'erreur.
  - La recherche d'archive antérieure a également surfacé #79289 pour la sélection de permission Automation SSH distant et #78049/#69799 autour du contexte de service TCC/Full Disk Access.
- Rapports Discrawl :
  - `iMessage Full Disk Access Automation cliPath dbPath` a retourné un fil de support conseillant Full Disk Access pour le processus exécutant Gateway/`imsg`, Automation pour Messages et la définition en dur de `cliPath`/`dbPath`.
  - `imsg rpc timeout gateway` a retourné des extraits Discord avec des boucles `imsg rpc not ready` et une dégradation de la disponibilité.
  - Les requêtes étroites pour `channels status probe imsg private API` n'ont retourné aucun extrait.
- Bonnes qualités :
  - Le contrat d'opérateur est explicite et non caché derrière la sémantique du serveur BlueBubbles.
  - Le code sépare la disponibilité RPC, la disponibilité API privée et la détection de capacité d'action.
  - Les erreurs autour de Full Disk Access et du démarrage RPC ont un traitement dédié plutôt que de faire surface comme des défaillances de processus enfant génériques.
- Mauvaises qualités :
  - Le runtime dépend des permissions macOS et de l'état du bridge API privée en dehors du contrôle d'OpenClaw.
  - L'exécution distante dépend du comportement stdio transparent que les opérateurs peuvent facilement casser avec des wrappers ou des filtres shell.
  - Les rapports d'archive actifs montrent que le transport peut être la raison pour laquelle le canal iMessage entier semble mort même lorsque la configuration semble correcte.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Bêta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Exécuter imsg localement, Exécuter via un wrapper SSH, Accorder les permissions macOS, Sonder la santé du runtime.
- Signaux négatifs : la note archivée a précédé la notation de complétude Completeness version-3 de processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve d'hôte en direct manque des preuves du référentiel.
- Les défaillances TCC et Automation restent sensibles à l'opérateur.
- Le bridge API privée peut tomber après les modifications de Messages ou du système d'exploitation et nécessite une resonde ou une réparation `imsg launch`.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:10` : les déploiements supportés utilisent `imsg` sur un hôte macOS Messages connecté ou un wrapper SSH depuis Linux/Windows.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:19` : le statut est une intégration CLI externe native ; Gateway lance `imsg rpc` sur stdio.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:122` : les wrappers doivent se comporter comme des tuyaux JSON-RPC stdio transparents et longue durée.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:130` : les wrappers de mise en mémoire tampon peuvent ressembler à des pannes `imsg rpc timeout`.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:139` : Full Disk Access est requis pour le processus exécutant OpenClaw/`imsg`.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:140` : la permission Automation est requise pour envoyer via Messages.app.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:141` : les actions avancées nécessitent une configuration API privée/SIP.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:598` : les passerelles hors Mac doivent définir `cliPath` sur un wrapper SSH.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:637` : `remoteHost` active la récupération de pièce jointe SCP pour les wrappers SSH.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/client.ts:95` : le client RPC lance le `cliPath` configuré.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/client.ts:126` : la gestion des erreurs stdin enfant empêche les processus `imsg` morts de faire planter Gateway sur EPIPE asynchrone.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/probe.ts:164` : la sonde API privée inspecte `send-rich --help` pour le support des pièces jointes.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/probe.ts:213` : la sonde matérialise le statut API privée à partir de `imsg status --json`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/probe.ts:292` : la sonde RPC appelle `chats.list` via le même chemin client.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:241` : le runtime résout `remoteHost` explicite ou détecté automatiquement.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:989` : le moniteur démarre `watch.subscribe` avec les options de pièce jointe et de réaction.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:1013` : les retries de démarrage échouent les défaillances transitoires de `watch.subscribe`.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/channels.status.test.ts:213` : une sonde de statut iMessage détenue par le plugin est enregistrée dans la gestion du statut du canal Gateway.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/channels.status.test.ts:223` : `channels.status --probe` appelle la sonde iMessage une fois.
- `/Users/kevinlin/code/openclaw/src/commands/health.test.ts:323` : la sortie de santé inclut l'état configuré/sonde iMessage.
- Aucune voie d'intégration macOS/imsg en direct n'a été trouvée pour ce composant.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/status.test.ts:46` : refuse de lancer `imsg rpc` dans les environnements de test.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/status.test.ts:54` : promeut les bannières RPC Full Disk Access à une erreur de sonde publique.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/status.test.ts:188` : échoue rapidement pour les sondes `imsg` locales par défaut sur les hôtes non-mac.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/status.test.ts:206` : la sonde de statut utilise `cliPath` et `dbPath` à portée de compte.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/probe.test.ts:23` : le support des méthodes suit la liste de méthodes RPC explicite.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.watch-subscribe-retry.test.ts:81` : les délais d'expiration de démarrage transitoires de `watch.subscribe` sont retentés.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "imsg rpc timeout gateway" --json --limit 6`

Résultats :

- Problème ouvert #87263 : `5.22: imsg rpc watch.subscribe timeout on every gateway start - iMessage channel dead`.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage private API" --json --limit 6`

Résultats :

- Problème ouvert #84329 concernant les envois sortants préférant le transport IMCore configurable lorsque le support API privée est disponible.
- Problème ouvert #79610 concernant les stderr AddressBook Apple bénins enregistrés au niveau d'erreur sur le chemin API privée imsg standard.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage Full Disk Access Automation cliPath dbPath" --limit 6`

Résultats :

- Fil de support Discord `Probe failed - Error: imsg rpc exited (code 1)` le 2026-02-17 a recommandé de corriger Full Disk Access, Automation et de définir en dur `cliPath`/`dbPath`.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "imsg rpc timeout gateway" --limit 6`

Résultats :

- Les extraits Discord ont signalé des boucles `imsg rpc not ready`, des sorties de canal et une dégradation de la disponibilité lors du churn Gateway.
