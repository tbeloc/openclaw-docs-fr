---
title: Supervision Codex
summary: "Architecture et limite de produit pour superviser les sessions Codex natives depuis OpenClaw."
read_when:
  - Designing Codex session discovery, continuation, or archive behavior
  - Changing the Codex Sessions Control UI or Gateway RPCs
  - Extending Codex supervision across paired nodes
---

# Supervision Codex

## Objectif

La supervision Codex permet à un opérateur OpenClaw de découvrir les sessions Codex natives et,
lorsque c'est sûr, de créer une branche locale via la surface OpenClaw Chat normale.
Codex App Server reste le propriétaire du thread et de la boucle de modèle. OpenClaw fournit le
catalogue de flotte, l'interface utilisateur opérateur authentifiée, la liaison de session et la livraison de canal.

La fonctionnalité appartient au plugin officiel `codex`. Il n'y a pas de plugin
Supervisor séparé ou de deuxième implémentation de protocole Codex.

## Limite de produit

Activez la fonctionnalité avec :

```text
plugins.entries.codex.config.supervision.enabled = true
```

Le produit initial actif est intentionnellement plus petit que le plan de flotte à long terme :

- Lister uniquement les threads Codex non archivés.
- Regrouper les lignes de nœud local et opt-in par identité d'hôte stable.
- Créer une branche Chat normale, verrouillée par modèle, à partir d'un thread stocké ou inactif local à Gateway, démarrer son thread de harnais Codex complet au premier tour, ou ouvrir le Chat créé pour une branche antérieure.
- Archiver un thread stocké ou inactif local à Gateway uniquement après confirmation explicite d'absence d'autre exécuteur.
- Afficher les sources locales actives sans contrôles de nouvelle branche ou d'archive tout en permettant l'ouverture d'un Chat supervisé existant.
- Afficher les lignes de nœud appairé comme métadonnées en lecture seule.
- Isoler les défaillances de catalogue par hôte.

Le catalogue est la collection non archivée. Une ligne dans celui-ci peut toujours avoir un statut de tour inactif, actif, `notLoaded` ou erreur.

La supervision reste opt-in. L'intégration guidée tente d'installer et d'activer après la détection réussie d'installation Codex native et après que le backend d'inférence sélectionné réussisse sa vérification en direct, indépendamment du backend principal que l'utilisateur sélectionne. La supervision s'active uniquement lorsque cette configuration de plugin opportuniste réussit. Un plugin explicitement désactivé, un bloc de politique ou
`supervision.enabled: false` reste autoritaire.

## Propriété

Le plugin `codex` possède tout le comportement de Codex App Server :

- découverte de point de terminaison et cycle de vie de connexion
- initialisation de protocole et vérifications de version
- gestion des listes de threads, lecture, reprise, archivage et événements
- ponts d'approbation et d'entrée utilisateur
- liaisons de thread native aux sessions OpenClaw
- application du modèle et du harnais Codex uniquement après continuation

L'interface utilisateur de contrôle et la Gateway consomment ce service détenu par le plugin. Elles ne lisent pas directement les fichiers de déploiement Codex et n'implémentent pas un autre client App Server.

La topologie locale par défaut est :

```text
Codex Desktop -> private stdio App Server -> user Codex home
                                             ^
OpenClaw Codex plugin -> supervision App Server connection
  (defaults to managed user-home stdio; explicit appServer settings are honored)
  -> passive source catalog and read
  -> snapshot pin -> canonical appServer-source branch
  -> visible-history injection and every later supervised Chat turn

Ordinary OpenClaw Codex sessions -> managed agent-home stdio by default
  -> ordinary full harness threads -> OpenClaw Chat and channel delivery
```

L'activation de la supervision ne change pas le harnais Codex ordinaire : il reste agent-scoped par défaut. La connexion de supervision séparée utilise par défaut le stdio user-home géré, de sorte que ses opérations de catalogue et d'instantané voient les threads stockés natifs. Les paramètres de connexion `appServer` explicites sont honorés. Lorsque `homeScope` n'est pas défini, la connexion de supervision le résout en `"user"` pour stdio ou Unix et `"agent"` pour WebSocket. Définissez `appServer.homeScope: "user"` explicitement uniquement lorsque le harnais ordinaire doit également partager la maison Codex native. Un Chat créé via Codex Sessions est l'exception : sa liaison de supervision privée maintient les lectures de source, la création de branche canonique et les tours ultérieurs sur la connexion de supervision. Le statut en direct et la propriété restent locaux au processus ; un thread inconnu du processus de supervision d'OpenClaw est `notLoaded` même lorsque Codex Desktop l'exécute activement.

Codex a un daemon local canonique expérimental avec un contrat de bootstrap géré par l'installateur séparé. Cette fonctionnalité ne doit pas amorcer, revendiquer ou supposer ce daemon implicitement.

## Flux de catalogue

La méthode Gateway `codex.sessions.list` demande toujours `archived: false` et
les types de source interactifs `cli` et `vscode`. Elle combine :

1. Résultats `thread/list` locaux à Gateway à partir du serveur d'application de supervision,
   qui utilise par défaut le stdio user-home géré.
2. Résultats `codex.appServer.threads.list.v1` de chaque nœud connecté et opt-in.

L'implémentation de nœud appairé macOS native supporte uniquement un `appServer.transport: "stdio"` non défini/par défaut ou explicite avec une portée de supervision non définie/par défaut ou explicite `appServer.homeScope: "user"`. Elle porte `command`, `args` configurés et `clearEnv` normalisé dans le processus enfant. Avec `"unix"`, `"websocket"` ou `homeScope: "agent"` explicite, elle n'annonce ni la capacité de catalogue ni la commande ; l'invocation directe échoue également fermée. Elle ne doit jamais exposer la maison Codex utilisateur pour une configuration agent-scoped ou substituer stdio local pour un point de terminaison explicite.

La projection normalise les identifiants, le titre, cwd, le statut, les drapeaux d'attente actifs, les horodatages, la source, le fournisseur de modèle, la version Codex et la branche Git. Les nœuds appairés ne retournent pas d'aperçus de transcription, de tours, de chemins de déploiement, de chemins de maison Codex, de télécommandes Git, de SHA de commit, de points de terminaison bruts ou d'erreurs App Server brutes.

Les défaillances d'hôte restent locales à chaque résultat d'hôte. Un nœud hors ligne ou un App Server local indisponible n'efface pas les hôtes sains de la page. La connectivité est une propriété d'hôte, pas un statut de thread : un résultat d'hôte échoué ne contient pas de lignes de session fraîches et ne projette pas `offline` sur les threads natifs.

La découverte de catalogue est passive. L'énumération ou la lecture de métadonnées ne doivent pas appeler
`thread/resume`, s'abonner le client OpenClaw aux demandes de thread en direct ou
répondre à une approbation.

La recherche est titre uniquement et insensible à la casse. Pour chaque page de catalogue retournée, la
Gateway et le Mac appairé analysent un nombre limité de pages natives sans passer
la requête à App Server, car la recherche native peut également correspondre aux aperçus de transcription. Le curseur natif retourné permet aux appelants de continuer l'analyse.

## Limite de l'interface de ligne de commande opérateur

Le plugin enregistre trois commandes shell soutenues par Gateway :

```text
openclaw codex sessions [--search <text>] [--host <id>] [--limit <count>] [--cursor <cursor>] [--json] [gateway-options]
openclaw codex continue <thread-id> [--json] [gateway-options]
openclaw codex archive <thread-id> --confirm-no-other-runner [--json] [gateway-options]
```

`[gateway-options]` est `--url <url>`, `--token <token>`, `--timeout <ms>` et
le commutateur `--expect-final` hérité. Le délai d'attente par défaut est 30 000 ms ;
`--expect-final` n'a aucun effet supplémentaire pour ces RPC unaires. La recherche de session
est titre uniquement et insensible à la casse ; chaque réponse analyse une chaîne de page native bornée, et `--cursor` continue les résultats plus anciens. La limite par défaut est 50 par hôte
et accepte 1 à 100, et un curseur nécessite une destination `--host`
stable. Aucune commande n'accepte
une option archivée/inclure-archivée. Seules `sessions` peuvent cibler les hôtes appairés ;
`continue` et `archive` envoient toujours `hostId: "gateway:local"`, et archive
nécessite le drapeau de confirmation explicite.

L'espace de noms shell n'est pas l'espace de noms runtime `/codex` en chat. En
particulier, `/codex sessions --host <node>` énumère les fichiers de session Codex CLI sur un
nœud, `/codex threads` énumère les threads App Server pour la connexion de conversation actuelle, et `/codex resume` ou `/codex bind` mute la liaison de cette conversation. Ces commandes ne remplacent pas `codex.sessions.continue`, et il n'y a pas de commande runtime `/codex continue` ou `/codex archive`.

## Continuation locale

Pour une ligne Gateway-locale stockée ou inactive, l'interface utilisateur appelle
`codex.sessions.continue` avec les identifiants d'hôte et de thread. Le plugin :

1. Réutilise le Chat supervisé existant lorsque la source en possède déjà un.
2. Sinon, projette l'historique borné de l'utilisateur et de l'assistant à travers le dernier tour terminal persistant de la source (complété, interrompu ou échoué) dans un nouveau Chat OpenClaw et enregistre une branche de harnais en attente.
3. Stocke la politique de verrouillage de modèle Codex uniquement en attente, et non une sélection concrète de modèle ou de fournisseur, plus l'étendue de la connexion de supervision privée, et retourne la `sessionKey` OpenClaw.

La projection d'historique sélectionne la queue la plus récente des messages visibles de l'utilisateur et de l'assistant, avec des limites strictes de 200 messages, 512 KiB de texte UTF-8 au total, et 64 KiB par message. Elle remplace les entrées d'image et d'image locale par `[Image attachment]`, ne copie jamais les charges utiles ou les chemins d'image, et omet le raisonnement, les appels d'outils et les résultats d'outils.

L'interface utilisateur navigue vers le Chat normal avec cette clé de session. Aucun thread de harnais canonique n'existe encore. Au premier tour du Chat normal, le harnais installe les vrais gestionnaires d'approbation, d'élicitation, d'événement et de livraison de Codex, puis :

1. Utilise la connexion de supervision pour appeler le `thread/fork` natif sans modèle ni remplacement de fournisseur et épingle l'instantané source persistant. L'état actuel du `ConfigManager` de Codex sélectionne le modèle et le fournisseur, et la réponse fork rapporte la paire réelle. Si le modèle diffère du dernier modèle enregistré dans la source, Codex émet son avertissement normal de différence de modèle.
2. Sur cette même connexion, démarre le thread de harnais Codex complet canonique avec `threadSource: "appServer"`, le répertoire de travail OpenClaw, la politique, la configuration, l'environnement, la surface complète de l'outil de harnais OpenClaw, et exactement le modèle et le fournisseur retournés par le fork pour ce démarrage initial.
3. Injecte l'historique borné visible de l'utilisateur et de l'assistant à travers cette connexion, valide la liaison canonique sans abandonner son étendue de supervision, exécute le tour, et archive le fork temporaire.

Avant le premier tour, le Chat est une branche en attente verrouillée avec un miroir d'historique visible ; après, chaque tour de modèle s'exécute à travers le thread de harnais Codex canonique sur la connexion de supervision. La branche n'est pas un clone de déploiement natif complet : le raisonnement source, les appels d'outils et les résultats d'outils sont délibérément omis. Si l'épinglage d'instantané ou la création de thread canonique échoue, la branche en attente reste réessayable. Une course de liaison, une supervision désactivée, ou une connexion de supervision indisponible ou non correspondante échoue fermée avant l'exécution du tour au lieu de revenir au harnais de maison d'agent ordinaire.

Cela garantit la sélection détenue par Codex, et non la préservation du modèle historique de la source. La paire retournée par le fork est utilisée pour le démarrage du thread canonique, et Codex persiste le modèle natif et le fournisseur de ce thread. Les reprises ultérieures omettent les remplacements de modèle et de fournisseur OpenClaw, donc Codex restaure la paire persistée. Si un contrôle Codex natif séparé modifie le thread canonique, OpenClaw accepte cette sélection persistée native. La chaîne de modèle et de secours OpenClaw externe ne la remplace jamais.

Les changements de modèle, la suppression de session et les opérations de réinitialisation/nouvelle session échouent fermées pour le Chat verrouillé par modèle supervisé. La mutation `/codex model <model>`, `/codex bind`, `/codex resume` (y compris le nœud `--bind here`), et `/codex detach` ou `/codex unbind` échouent également fermées car elles remplacent ou effacent la liaison. La requête `/codex model` et `/codex fast`, `/codex permissions`, et `/codex threads` restent disponibles. L'outil agent `codex_threads` ne peut pas attacher un nouveau fork ou archiver le thread natif lié. La liste et les lectures seules de métadonnées restent disponibles ; les champs de transcription nécessitent `supervision.allowRawTranscripts`, tandis que le renommage, l'archivage non archivé, le fork détaché et l'archivage d'un thread non lié nécessitent `supervision.allowWriteControls`. Aucune option ne peut remplacer la liaison verrouillée. La suppression ou la réinitialisation de l'entrée OpenClaw abandonnerait autrement la liaison native et créerait ou permettrait un thread générique derrière une session ressemblant à Codex. La maintenance de la rétention préserve donc les entrées verrouillées par modèle même lorsqu'elles dépassent les limites ordinaires d'âge, de nombre ou de budget disque. La désactivation ou la désinstallation du plugin propriétaire conserve également le verrouillage et le marqueur de propriété du plugin. Le Chat reste indisponible et échoue fermé jusqu'à ce que le même plugin soit réactivé ; le nettoyage ne le convertit jamais en session de modèle ordinaire.

La source n'est jamais reprise ou mutée par cette action. Le fork temporaire épingle un instantané ; ce n'est pas le thread de continuation durable. Le démarrage d'un thread de harnais canonique distinct au premier tour empêche OpenClaw de devenir un écrivain source concurrent simplement parce que l'état local du processus n'a pas vu un tour détenu par Desktop. Le miroir d'historique visible et l'instantané épinglé peuvent omettre le travail qui n'a pas encore été complété dans une source active. La source CLI ou VS Code d'origine reste admissible pour les catalogues natifs et OpenClaw. La branche canonique reste un thread Codex natif dans le magasin de supervision, mais les clients natifs peuvent filtrer son type de source `appServer`, donc la visibilité Codex Desktop n'est pas un contrat.

## Comportement d'archivage

Pour une ligne Gateway-locale stockée ou inactive, `codex.sessions.archive` nécessite un `confirmNoOtherRunner: true` explicite, lit à nouveau l'état local du processus actuel, procède uniquement pour `idle` ou `notLoaded`, appelle le `thread/archive` natif, et retourne le succès uniquement après que Codex accepte l'opération. La ligne quitte alors le catalogue non archivé.

Un statut actif ou d'erreur de la lecture à nouveau rejette l'archivage. Il en va de même pour une branche supervisée en initialisation ou en attente de la source : le premier tour du Chat doit matérialiser sa branche canonique avant que la source puisse être archivée. Un propriétaire de liaison OpenClaw actif connu pour la cible exacte ou tout descendant non archivé généré rejette également l'archivage. OpenClaw pagine la relation expérimentale `thread/list ancestorThreadId` de Codex et échoue fermée sur les erreurs de requête ou de réponse, les cycles de curseur ou de thread, et l'épuisement des limites de sécurité. L'archivage natif peut arrêter le travail parent et descendant chargé, donc l'archivage n'est pas un raccourci d'interruption. La lecture, l'énumération des descendants et les appels d'archivage ne sont pas atomiques. Un client indépendant peut toujours posséder ou démarrer du travail sur une ligne qui semble inactive ou `notLoaded` localement. La confirmation sans autre exécuteur couvre les clients inconnus et cette course jusqu'à ce que Codex ait un archivage conditionnel ou un bail entre processus. L'archivage de nœud appairé est interdit.

Il n'y a pas de vue archivée dans Codex Sessions. Un thread restauré avec `thread/unarchive` dans une autre surface Codex autorisée par le propriétaire devient à nouveau admissible pour le catalogue non archivé.

## Sécurité des threads actifs

Codex sérialise les mutations pour un thread parmi les clients d'un App Server, mais il n'expose pas un bail exclusif d'exécuteur entre processus ou de propriétaire d'approbation. Les App Servers stdio indépendants peuvent ajouter au même déploiement, tandis que chacun ne voit que son propre statut en mémoire. Les demandes d'approbation peuvent également atteindre chaque abonné d'un serveur, la première réponse valide complétant la demande.

Par conséquent :

- les clients de catalogue passifs ne s'abonnent pas ou refusent automatiquement les approbations
- les lignes actuellement signalées comme actives n'exposent ni une nouvelle branche ni Archive
- une source non mappée devient une branche d'historique visible dont le thread de harnais canonique ne reprend jamais la source
- `notLoaded` est affiché comme activité inconnue et ne peut être archivé qu'après confirmation informée sans autre exécuteur
- l'archivage local nécessite cette confirmation plus une lecture `idle` ou `notLoaded` à nouveau, tout en reconnaissant la course de protocole entre la lecture et l'archivage

L'interruption et la passation entre plusieurs clients sont des décisions de produit futures. Elles ne sont pas impliquées par l'affichage d'une ligne active.

## Limite de nœud appairé

L'invocation de nœud est actuellement requête/réponse uniquement. Elle peut retourner en toute sécurité les métadonnées de catalogue bornées, mais elle ne peut pas transporter le flux d'événements long terme, les demandes d'approbation, les appels d'outils, l'annulation et les deltas d'assistant requis par une exécution de harnais Codex.

Le contrat de nœud initial est donc la liste uniquement. Les lignes distantes restent visibles mais **Continue** et **Archive** ne sont pas disponibles, quel que soit le statut inactif. Une vraie continuation distante nécessite un exécuteur côté nœud et un pont de streaming qui préserve les mêmes invariants d'approbation et de liaison que le harnais local.

## Autorisations

Chaque ordinateur s'inscrit localement. L'activation de la Gateway n'autorise pas un autre nœud à lire ses métadonnées Codex. La capacité de nœud doit passer l'approbation d'appairage normal et de politique de commande.

La liste de flotte utilise l'étendue `operator.write` Gateway car elle invoque des nœuds appairés. La continuation locale et l'archivage sont des actions d'opérateur authentifiées et restent soumis aux vérifications d'hôte et de statut.

L'accès agent autonome et MCP autonome est séparé. Les contrats d'outils `codex_endpoint_probe`, `codex_sessions_list`, `codex_session_read`, `codex_session_send` et `codex_session_interrupt` expédiés restent détenus par le plugin `codex`. Avec la supervision activée, les lectures de transcription `codex_threads` brutes et les champs de liste dérivés de transcription nécessitent également `supervision.allowRawTranscripts` ; chaque fork, renommage, archivage ou archivage non archivé de `codex_threads` nécessite `supervision.allowWriteControls`. Les deux politiques sont désactivées par défaut.

## Compatibilité

`openclaw doctor --fix` migre la configuration `plugins.entries.codex-supervisor` expédiée, y compris les points de terminaison et les politiques de transcription/écriture, plus les références d'autorisation/refus de plugin dans `plugins.entries.codex.config.supervision`. Les valeurs de destination canonique explicites gagnent les conflits. Le code d'exécution utilise uniquement la forme de plugin `codex` canonique après la migration.

Le plugin officiel conserve exactement cinq outils de compatibilité Supervisor : `codex_endpoint_probe`, `codex_sessions_list`, `codex_session_read`, `codex_session_send` et `codex_session_interrupt`. La liste de session est chargée uniquement par défaut ; il n'y a pas de paramètre `loaded_only`. `include_stored: true` ajoute des lignes de base de données d'état non archivées, bornées par point de terminaison par `max_stored_sessions` (par défaut 200, plage acceptée 1 à 1 000) ; les lignes chargées ne sont pas limitées par ce paramètre. Les champs dérivés de transcription et les lectures restent contrôlés par `allowRawTranscripts` ; l'envoi et l'interruption restent contrôlés par `allowWriteControls`.

L'envoi de compatibilité ne démarre ni ne reprend jamais un thread inactif. `mode: "start"` est toujours refusé ; `"auto"` et `"steer"` ne dirigent qu'un tour actif lisible. L'interruption nécessite également un tour actif lisible. Les routes de continuation inactive vers Codex Sessions afin que le harnais complet possède les approbations, les outils et la liaison. L'adaptateur MCP hérité autonome résout ces mêmes outils à partir du plugin officiel et est le seul chemin qui honore les variables d'environnement de politique héritage conservées.

Le catalogue de juillet, la méthode Gateway, la capacité de nœud et l'enregistrement CLI n'avaient pas été expédiés sous l'ancien identifiant de plugin. Ils passent directement à la propriété `codex` sans une deuxième façade d'exécution.

## Travail futur

- exécuteur de streaming côté nœud et pont d'événement pour continuation distante
- baux d'exécuteur explicites et de propriétaire d'approbation pour passation de client simultanée
- archivage distant après un bail de propriété d'exécuteur ou équivalent de clôture existe
- interruption et observation de session active plus riche
- passation auditée entre Codex Desktop, CLI et OpenClaw

La navigation archivée ne fait pas partie de la barre latérale de supervision prévue. Les surfaces Codex natives restent le chemin de récupération pour les threads archivés.

## Tests d'acceptation

- L'activation de la supervision répertorie les sessions locales non archivées.
- Les sessions archivées n'apparaissent jamais dans la réponse du catalogue ou l'interface utilisateur.
- Les hôtes sains restent visibles lorsqu'un autre hôte échoue ; un hôte indisponible retourne aucune ligne nouvelle au lieu d'inventer un statut de session hors ligne.
- Une ligne locale stockée ou inactive crée un miroir Chat avec un verrouillage de modèle/runtime Codex uniquement ; le premier tour épingle un instantané temporaire et démarre le thread du harnais complet canonique, et répéter Continue ouvre le Chat existant.
- Le premier tour omet les remplacements de modèle/fournisseur sur la branche d'instantané et épingle le démarrage canonique à la paire exacte retournée par Codex, même lorsque Codex avertit que son modèle actuel diffère du dernier modèle enregistré de la source.
- Les liaisons supervisées en attente et validées utilisent la connexion de supervision pour l'accès à la source, la création de branche canonique et chaque tour ultérieur ; les sessions Codex ordinaires restent limitées à l'agent.
- Les reprises ultérieures omettent les remplacements de modèle/fournisseur OpenClaw, préservent la sélection persistante canonique de Codex, acceptent les modifications natives distinctes de ce thread et ne substituent jamais le modèle OpenClaw externe ou la chaîne de secours.
- La désactivation de la supervision ou la perte du cycle de vie de la liaison/connexion échoue de manière fermée au lieu de déplacer le Chat vers le harnais agent-home ordinaire.
- Un Chat verrouillé par modèle supervisé ne peut pas être supprimé tant qu'il protège la liaison native.
- Le Chat miroir contient au maximum 200 messages utilisateur et assistant, 512 Kio au total et 64 Kio par message. Les images deviennent des espaces réservés ; le raisonnement source, les appels d'outils, les résultats d'outils, les charges utiles d'images et les chemins locaux ne sont pas clonés.
- Le flux de branche ne reprend jamais le thread source.
- La source originale reste admissible pour les deux catalogues. La branche native canonique utilise le type de source `appServer` et n'est pas garantie d'apparaître dans Codex Desktop.
- Les sources locales actives ne peuvent pas créer une branche ou être archivées ; un Chat supervisé existant peut toujours s'ouvrir.
- Les lignes d'activité inconnue peuvent se brancher sans confirmation ; l'archivage nécessite une confirmation explicite sans autre exécuteur.
- Une source avec une branche supervisée en initialisation ou en attente ne peut pas être archivée jusqu'à ce que le premier tour Chat matérialise la branche canonique.
- Un propriétaire de liaison actif connu pour la cible exacte ou tout descendant généré non archivé bloque l'archivage ; les défaillances d'énumération des descendants échouent de manière fermée, et la confirmation explicite reste responsable des clients inconnus et de la course statut-à-archiver.
- L'archivage local stocké ou inactif confirmé supprime la ligne après le succès natif.
- Les lignes à nœuds appairés restent visibles sans Continue ou Archive.
- L'énumération passive ne s'abonne jamais aux approbations de thread ni n'y répond.
- La configuration Supervisor héritée migre vers la forme de configuration Codex canonique.
- La liste héritée est chargée uniquement par défaut, l'énumération stockée obéit à sa limite par point de terminaison, et l'envoi de compatibilité ne démarre ni ne reprend jamais un thread inactif.
