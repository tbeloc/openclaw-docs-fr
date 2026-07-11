---
summary: Exécutez des sessions d'agent sur des machines SSH éphémères avec inférence proxifiée par passerelle et streaming de barre latérale en direct.
title: Plan des workers cloud
read_when:
  - Conception ou implémentation de l'approvisionnement des workers cloud, du mode worker ou de la transmission de session
  - Modification des environnements.*, du protocole worker, de l'ingestion de transcription ou des RPC de proxy d'inférence
  - Examen de la posture de sécurité de l'exécution d'agent à distance
---

## Statut

Proposition, révision 3. Non implémentée. Direction convenue en juillet 2026 ; la révision 2 a intégré les conclusions de l'examen contradictoire (protocole worker dédié, machines d'état de placement/environnement, synchronisation entrante consciente de git, transmission v1 unidirectionnelle, formulation de sécurité à sortie contrôlée). La révision 3 règle le modèle de propriété de synchronisation (l'auteur worker valide, la passerelle adopte et publie), ajoute un mode de synchronisation simple sans git, corrige l'exécution worker à plein-dans-la-boîte, déplace la politique internet au moment de l'approvisionnement et restaure la distribution d'agent à la jalon 3.

## Problème

Les sessions d'agent OpenClaw exécutent leur boucle, leurs outils et leur inférence à l'intérieur du processus de passerelle sur une seule machine. Le calcul est limité par cette machine, les tâches longues l'occupent et le travail parallèle entre en concurrence pour l'utiliser. Les produits hébergés (agents cloud Cursor, Claude Code sur le web, Codex cloud) résolvent ce problème avec des bacs à sable cloud éphémères par tâche, mais ils nécessitent une infrastructure de fournisseur et une confiance envers le fournisseur.

Les opérateurs qui possèdent déjà des machines de rechange (ou peuvent les louer à bas prix) n'ont aucun moyen de dire : exécutez cette session là-bas, affichez-la dans ma barre latérale comme n'importe quelle autre session, et jetez la machine après.

## Objectifs

- Exécuter une session d'agent complète (boucle + outils) sur une machine distante éphémère (« worker cloud ») tandis que la session apparaît et se diffuse dans l'interface utilisateur de contrôle exactement comme une session locale.
- Aucune information d'identification permanente sur le worker (aucune authentification de fournisseur, aucun jeton forge) et aucune sortie réseau directe ; la boîte a seulement besoin d'un sshd accessible.
- Approvisionnement, synchronisation, exécution, collecte, destruction — entièrement automatisés, fournisseur-enfichable (premier fournisseur : CLI de bail de style Crabbox).
- Distribuer le travail en cours d'exécution de la passerelle à un worker à une limite de tour sans perdre la transcription, l'identité de session ou (lorsque les octets de demande restent équivalents) l'affinité du cache du fournisseur ; récupérer les résultats en toute sécurité.
- Les humains (interface utilisateur) et les agents (outil) peuvent distribuer le travail à un worker cloud.
- Prendre en charge les sessions de plusieurs jours ; la durée de vie est une politique, pas une limite codée en dur.

## Non-objectifs (v1)

- Aucun harnais de codage externe (Claude Code, Codex CLI) sur les workers. Les sessions worker exécutent uniquement le runner intégré d'OpenClaw. Le support des harnais est un opt-in v2 car les harnais font leur propre inférence avec leurs propres identifiants.
- Aucun meilleur-de-N / fan-out de tentative parallèle.
- Aucune dépendance VPN/tailnet. Le transport est SSH uniquement.
- Aucun nouveau runtime de bac à sable. La machine worker est la limite d'isolation ; le sandboxing du système d'exploitation dans la boîte peut se superposer plus tard.
- Aucune migration en direct symétrique en v1 : la distribution est locale → worker ; worker → local nécessite une session arrêtée plus une réconciliation d'espace de travail complétée. La transmission bidirectionnelle en direct s'appuie sur la même machinerie de barrière plus tard.
- Aucun état JSON côté passerelle ; l'environnement, le placement, le curseur et l'état de subvention vivent dans SQLite.

## Art antérieur (ce que nous copions, ce que nous inversons)

- Agents cloud Cursor : la boucle d'agent s'exécute dans leur cloud ; la VM est une cible d'exécution d'outil ; magasin de conversation append-only diffusé à tous les clients ; démarrage à chaud snapshot-après-installation ; les workers auto-hébergés sont des processus worker sortants uniquement. Nous copions le « la source de vérité de la conversation reste sur l'orchestrateur » et le modèle de streaming ; nous inversons le placement de la boucle (voir la décision ci-dessous).
- Codex cloud : runtime à deux phases — phase de configuration en réseau, puis phase d'agent hors ligne avec secrets supprimés ; cache d'état de conteneur pour les suites rapides. Nous copions la division de phase comme notre posture de sortie et l'idée de cache pour les images chaudes v2.
- Claude Code sur le web : VM par session ; proxy git isolant les identifiants (les vrais jetons n'entrent jamais dans le bac à sable, la poussée est restreinte à la branche de session) ; snapshot du système de fichiers après la configuration ; transmission de téléportation = branche poussée + historique rejoué. Nous copions l'isolation des identifiants et le cadrage de transmission, mais la synchronisation sortante est rsync depuis la passerelle afin que les arbres de travail sales fonctionnent et qu'aucun jeton forge n'existe près de la boîte.
- Agent de codage Copilot : sortie par défaut-refuser avec liste blanche de registre de paquets. Notre état stable par défaut est plus fort (aucune sortie directe du tout) car l'inférence et la recherche web arrivent via le tunnel SSH — mais voir Sécurité pour savoir pourquoi c'est « sortie contrôlée », pas « sortie zéro ».

## Décision architecturale : boucle sur le worker, inférence via la passerelle

Trois placements ont été envisagés :

1. La boucle reste sur la passerelle, le worker exécute les outils (modèle Cursor). Domaine de défaillance le plus sûr (transcription, inférence, approbations, récupération de redémarrage restent tous locaux) et un jalon de première préférence pour les examinateurs. Rejeté comme architecture de produit : les outils non-exec d'OpenClaw sont des opérations de système de fichiers en processus, donc chaque lecture/édition/grep de fichier devient un aller-retour réseau ou une grande refonte de surface d'outil en RPC d'espace de travail grossier ; le comportement d'exécution est bavard et limité par la latence. Nous réutilisons son esprit où il est déjà construit (déchargement d'exec vers les nœuds) mais ne construisons pas la couche de remoting d'outil.
2. Boucle et inférence toutes deux sur le worker. Domaine de défaillance le plus simple, mais les identifiants de modèle (y compris les profils OAuth) doivent être expédiés vers des machines jetables, la passerelle perd le contrôle de politique/routage/audit, et la migration change l'identité d'appel du fournisseur, invalidant les caches du fournisseur.
3. Boucle + outils sur le worker, appels de modèle proxifiés via la passerelle. Choisi. Un aller-retour par tour de modèle au lieu de par appel d'outil ; les outils s'exécutent à côté du code ; la passerelle reste le propriétaire unique des profils d'authentification, du routage du fournisseur et de la politique ; le worker ne détient aucun secret.

Le coût de l'option 3 est une dépendance de passerelle synchrone pendant chaque tour de modèle, donc ses règles de durabilité font partie de la décision, pas une réflexion après coup :

- La perte de passerelle en milieu de tour échoue l'appel de fournisseur actif. Le tour est marqué comme échoué et est réessayé en tant que nouveau tour après reconnexion ; il n'y a pas de relecture transparente d'un flux de fournisseur en vol (risque de double facturation/double appel d'outil).
- Chaque opération worker↔passerelle porte une identité durable (voir Protocole Worker) afin que les reconnexions reprennent ou récupèrent les résultats terminaux mis en cache au lieu de rester en suspens.
- La passerelle est un composant géré en capacité : les limites de workers concurrents, le contrôle de flux et l'élimination de charge sont dans le champ d'application pour v1 (voir Capacité).

Parce que la passerelle stocke à la fois la transcription et provient tout le trafic du fournisseur, la session est indépendante de l'emplacement : déplacer la boucle entre la passerelle et le worker ne change rien du côté du fournisseur et rien dans le chemin de données de l'interface utilisateur. C'est ce qui rend la distribution et la récupération bon marché.

## Composants

### 1. Machine d'état d'environnement + contrat de fournisseur

`environments.*` dans le protocole de passerelle est actuellement une projection de statut uniquement. Le noyau durable est un enregistrement d'environnement et une machine d'état appartenant à SQLite, conçus avant les formes RPC :

`requested → provisioning → bootstrapping → ready → (attached|idle) → draining → destroying → destroyed | failed | orphaned`

- L'approvisionnement est sûr en cas de panne : la ligne d'intention est persistée avant l'appel du fournisseur, avec un identifiant d'opération déterministe, de sorte qu'un redémarrage de la passerelle peut adopter un bail en vol au lieu de double-approvisionner ou d'abandonner une machine payante.
- La réconciliation au redémarrage et un balayeur d'orphelins (fournisseur `inspect` vs. enregistrements locaux) sont des exigences v1, pas du durcissement.

Contrat de fournisseur (implémenté par plugin ; aucun nom de fournisseur ou politique dans le noyau) :

```ts
type WorkerProvider = {
  id: string;
  provision(profile: WorkerProfile, opId: string): Promise<WorkerLease>; // → ssh host/port/user/key material
  inspect(lease: { leaseId: string; profile: WorkerProfile }): Promise<LeaseStatus>; // adopt/health/orphan sweep
  renew?(leaseId: string): Promise<void>; // long-lived sessions vs provider TTLs
  destroy(lease: { leaseId: string; profile: WorkerProfile }): Promise<void>; // idempotent, returns only on proof of teardown
};
```

RPCs : `environments.create`, `environments.destroy`, `environments.list/status` étendu (fournisseur, identifiant de bail, état, âge, temps d'inactivité, sessions attachées). Premiers fournisseurs : un wrapper CLI de bail de forme Crabbox (chemin produit) et un fournisseur d'hôte SSH statique marqué comme développement uniquement — un worker sur un hôte partagé peut lire des données d'hôte non liées, donc les hôtes statiques sont pour le développement de fonctionnalités, pas la posture par défaut.

### 2. Bootstrap du worker : installer OpenClaw sur la boîte

Aucun artefact worker sur mesure, et aucune dépendance à la disponibilité de npm :

- Installation canonique pour tous les modes : un bundle worker produit par la passerelle, avec hachage de contenu (la sortie de construction propre de la passerelle empaquetée en tarball), poussée via SSH et installée sur la boîte. Cela couvre les builds de développement et les commits non publiés par construction.
- `npm i -g openclaw@<exact gateway version>` est une optimisation lorsque la passerelle exécute une version publiée ; jamais `latest`.
- Le bootstrap est idempotent ; un bail chaud avec un hachage de bundle correspondant ignore l'installation. Les machines brutes peuvent avoir besoin d'une phase de chaîne d'outils en réseau (runtime Node) — partie de la phase de configuration, fermée après.
- La poignée de main vérifie le hachage de construction du worker, l'ensemble de fonctionnalités du protocole et la compatibilité du runtime. Les vérifications de version/protocole de passerelle existantes sont insuffisantes pour cela (les nœuds tunnelisés SSH sont exemptés du rejet de version exacte), donc l'admission du worker fait sa propre vérification de build exacte.

Le mode worker (`openclaw worker`) est un point d'entrée, pas un fork : gestion de la connexion plus le runner d'agent intégré, avec persistance de session et appels de modèle soutenus par des RPCs de passerelle. Il ne doit pas démarrer les surfaces de passerelle : aucun canal, aucun démarrage automatique de plugin au-delà de l'ensemble d'outils de session, répertoire d'état jetable, aucun profil d'authentification local.

### 3. Transport : tout sur une seule connexion SSH

La passerelle possède la connectivité ; le worker n'a besoin que de sshd :

- La passerelle ouvre SSH au worker (identifiants du bail du fournisseur, clé d'hôte épinglée à partir de la sortie d'approvisionnement — pas de `StrictHostKeyChecking=no`) et établit un tunnel inverse qui transfère un socket local du worker vers le point de terminaison WS de la passerelle.
- Le trafic de contrôle/modèle et le transfert d'espace de travail utilisent des canaux SSH séparés afin que rsync ne puisse pas bloquer la tête de ligne des flux de jetons.
- Le cycle de vie du tunnel (keepalive, reconnexion avec backoff) est détenu par le runtime d'environnement sur la passerelle. Un scintillement de tunnel est invisible au niveau de la session : l'état du protocole durable (ci-dessous) permet au worker de se réattacher et de reprendre.

### 4. Protocole worker (dédié ; pas le protocole de nœud)

L'examen contradictoire contre les coutures de nœud actuelles a exclu la réutilisation simple : les invocations de nœud en attente sont des promesses locales au processus qui meurent avec la connexion, les clés d'idempotence du nœud sont analysées mais non dédupliquées, et — décisif — un nœud connecté peut émettre des événements de nœud ordinaires (y compris les demandes d'exécution d'agent), donc « type de nœud + plafond de capacité » n'est pas une limite de sécurité d'entrée. Les workers obtiennent donc un rôle `worker` authentifié avec une liste d'autorisation RPC/événement fermée et versionnée ; les connexions worker ne peuvent pas atteindre aucun gestionnaire d'événements de nœud hérité.

Identité et identifiants : l'approvisionnement crée un identifiant worker de courte durée lié à l'identifiant d'environnement, à la clé worker, au hachage du bundle, à la session unique autorisée, à l'ensemble RPC autorisé et à une expiration. L'appairage vérifié SSH s'applique toujours (nous avons approvisionné la boîte et tenons la clé), mais l'autorisation provient de l'identifiant créé, pas de la surface de nœud déclarée.

Sémantique d'opération durable (forme empruntée au runtime ACP existant et à son registre d'événements — poignées stables, sérialisation par session, relecture durable `(session, seq)`) :

- Chaque opération est délimitée `(sessionId, lifecycleRevision, runId, ownerEpoch, streamKind, seq)`.
- Les époques de propriété clôturent les workers obsolètes : un worker de remplacement avance l'époque ; les résultats tardifs de l'ancienne époque sont rejetés de manière déterministe.
- Livraison au moins une fois avec curseurs ACK persistés et résultats terminaux mis en cache dans SQLite ; la déduplication est déterministe. Aucune promesse d'exactement une fois.
- Cadres explicites pour annuler, fermer, reprendre et résultats terminaux ; contrôle de flux basé sur le crédit/fenêtre sur les flux.
- La négociation des fonctionnalités du protocole est indépendante de la version générale du protocole de nœud.

### 5. RPCs du backend de session

Deux contrats distincts — la base de code actuelle sépare les mutations de transcription durable (détenues par le gestionnaire de session, arbre JSONL avec état parent/feuille) des événements en direct locaux au processus (deltas de streaming, cycle de vie des outils, approbations), et le protocole worker doit préserver cette séparation :

- Commits de transcription durable : le worker soumet des lots d'ajout sémantique avec `runEpoch` + compare-and-swap de base-feuille ; le gestionnaire de session de passerelle génère les identifiants d'entrée et les identifiants parents. Le worker ne peut jamais fournir de lignes de transcription de confiance, d'identifiants d'entrée, d'identifiants parents ou d'identifiants de session étrangers.
- Événements en direct rejouables : une union d'événements typée avec numéros de séquence worker, ACKs de passerelle, rétention bornée et clôture d'événement tardif, alimentant le fanout d'événement d'agent existant afin que la vue de chat, les lignes d'outils et la logique non lue/statut se comportent de manière identique aux sessions locales.

Proxy d'inférence : réutiliser le vocabulaire d'événement du client de flux proxy runtime existant (`src/agents/runtime/proxy.ts`) mais déplacer la limite de confiance. Le worker envoie uniquement l'identité de session/exécution, une référence de modèle approuvée, le contexte et les options de génération contraintes ; la passerelle résout le fournisseur, le point de terminaison, l'authentification, les en-têtes, le routage et la politique de coût à partir de son propre catalogue. Un objet modèle fourni par le worker (par exemple `baseUrl` contrôlé par un attaquant) est rejeté. Les limites de taille de demande, l'annulation, l'audit et la relecture de résultat terminal s'appliquent. Les outils résidents de la passerelle (websearch) s'exécutent sur la passerelle et retournent les résultats sur le même canal.

### 6. Synchronisation de l'espace de travail

L'ancre de synchronisation est un espace de travail local de passerelle avec propriété de placement exclusif : pour les espaces de travail git, un worktree géré dédié (les métadonnées de worktree géré existantes — branche, base, propriété de snapshot — sont la fondation) ; pour les espaces de travail non-git, un répertoire cible appartenant à la passerelle. Jamais le checkout en direct de l'utilisateur. La propriété exclusive pendant que la session est placée à distance est ce qui rend la synchronisation entrante sans conflit par construction.

Fractionnement de propriété — commit vs. publication :

- L'agent côté worker crée des commits normalement dans sa copie (`git commit` est une opération locale sans identifiant ; l'identité de l'auteur est projetée à partir de la configuration de la passerelle). Ces commits sont des objets inertes jusqu'à ce que la passerelle les adopte.
- La passerelle fait tout ce qui nécessite de la confiance : vérifier que les commits entrants s'appuient sur la base enregistrée, avancer rapidement le worktree local, pousser, créer des PR et signature/re-signature optionnelle — tout avec les identifiants locaux de la passerelle. Le worker ne détient jamais les identifiants git ou forge et ne touche jamais à un distant.

Deux modes de synchronisation, sélectionnés selon que l'espace de travail est un référentiel git :

- Mode Git. Sortant : rsync le worktree (fichiers non validés et non suivis éligibles inclus ; style crabbox include/exclude, `.worktreeinclude` respecté) sur l'identité SSH du tunnel, enregistré comme un manifeste de base immuable (hachages de contenu + commit de base). Entrant : les nouveaux commits reviennent sous forme de bundle git ou de ref temporaire par rapport à la base enregistrée ; les artefacts non suivis reviennent via un manifeste explicite avec vérifications de taille/type/confinement de symlink. L'adoption vérifie l'ascendance de base et s'arrête en cas de divergence — rien ne remplace silencieusement l'un ou l'autre côté. Les suppressions, renommages, sous-modules et échappements de symlink sont gérés par les règles de manifeste, pas les heuristiques rsync.
- Mode simple (pas de git — par exemple, construire un projet à partir de zéro sur la boîte). La sortie est la même rsync + manifeste de base. L'entrée est un miroir diffé par manifeste dans le répertoire cible appartenant à la passerelle avec propagation de suppression. Sûr pour la même raison que le mode git : la propriété exclusive signifie qu'aucune édition locale concurrente n'existe pour entrer en conflit ; le manifeste de base détecte toujours la dérive locale inattendue et s'arrête au lieu de remplacer.

La création de points de contrôle protège les sessions de plusieurs jours de la perte de bail : points de contrôle entrants périodiques (commits de branche de session en mode git, snapshots de manifeste en mode simple) ; la cadence est la politique de profil (par défaut basée sur les tours).

### 7. Machine d'état de placement, sessions et interface utilisateur

Le placement du runtime est une machine d'état appartenant à SQLite, clée à la session, pas une paire de champs de ligne lâches :

`local → requested → provisioning → syncing → starting → active(worker) → draining → reconciling → local | reclaimed | failed`

Il persiste l'identifiant d'environnement, la génération de transition, l'époque de propriétaire actif, le manifeste de base de l'espace de travail, le hachage du bundle worker et les derniers curseurs ACK. L'admission de tour réclame atomiquement le placement avant que l'une ou l'autre boucle ne démarre un tour, de sorte qu'un message local admis par rapport à un snapshot obsolète ne peut jamais faire la course avec un tour worker — exactement une boucle possède la session à tout moment.

Interface utilisateur :

- Une session worker est une ligne de session ordinaire plus les métadonnées de placement. Elle vit dans le magasin normal, liste via `sessions.list`, flux via les abonnements existants — la barre latérale et le chat n'ont besoin d'aucun nouveau chemin de données, seulement de présentation : un badge worker et le statut de placement/environnement (`provisioning / syncing / running / idle / reconciling / reclaimed`).
- UX de création : la barre de destination de session cible (redessin de la barre latérale des sessions) gagne une destination de worker cloud aux côtés de la passerelle et du nœud. Nécessite un profil de fournisseur configuré ; la fonctionnalité est invisible jusqu'à ce qu'elle soit configurée.
- Dispatch d'agent : un outil de session permet à un agent de confier du travail à un worker cloud comme le ferait un humain (sous-session soutenue par worker, style subagent). Livré dans le même jalon que le dispatch humain, fermé par la même configuration de fournisseur opt-in. La récursion est bornée structurellement (les sessions worker ne peuvent pas elles-mêmes dispatcher des workers en v1) ; le contrôle des dépenses est la comptabilité/audit par environnement, pas la machinerie de quota.

## Dispatch et transfert

v1 est délibérément asymétrique :

- Local → worker (dispatch) : franchir la barrière de migration ci-dessous, provisionner ou réutiliser un worker, synchroniser, basculer le placement, le tour suivant s'exécute à distance.
- Worker → local (pull-back) : arrêter la session (drainer le worker selon la même barrière), compléter la réconciliation entrante, basculer le placement vers local. Pas une migration en direct.
- Transfert symétrique en direct (déplacer une session activement travaillée dans les deux directions sans arrêt) réutilise la même barrière et la machinerie de réconciliation et est livré après que les tests d'injection de pannes prouvent la barrière.

Barrière de migration (« limite de tour » seule est insuffisante — les approbations, les processus d'arrière-plan et les fusions de transcription de verrous libérés peuvent la traverser) :

1. Arrêter l'admission de nouveaux tours (réclamation de placement).
2. Annuler ou drainer les exécutions actives.
3. Révoquer les approbations d'exécution en attente et les subventions d'exécution.
4. Drainer les écritures côté transcription et les ACK d'événements en direct.
5. Terminer les processus enfants du worker.
6. Clôturer l'ancien propriétaire en avançant l'époque du propriétaire.
7. Réconcilier l'espace de travail (entrant, conscient des conflits).
8. Activer le nouveau propriétaire.

Affinité du cache : parce que les demandes de fournisseur proviennent de la passerelle dans les deux placements, l'affinité du cache est préservée lorsque la demande de fournisseur sérialisée reste équivalente — même ordre d'outils, instructions système, wrappers de fournisseur et métadonnées de cache (qui restent côté passerelle). C'est une propriété testable, pas une hypothèse : les tests d'équivalence d'octets entre les placements local/worker par transport de fournisseur supporté font partie du jalon qui introduit la boucle worker.

## Modèle de sécurité

Énoncé précisément : le worker n'a pas de sortie réseau directe et pas de credentials de fournisseur/forge permanentes. Ce n'est pas « zéro sortie » — l'inférence et les outils exécutés par la passerelle sont des canaux de sortie contrôlés (un worker injecté par prompt peut toujours mettre les octets de l'espace de travail dans le contexte du modèle ou les requêtes de recherche web). En conséquence :

- Comptabilité de sortie contrôlée : audit par environnement et comptabilité visible par l'opérateur sur le proxy d'inférence et les outils de passerelle. Les limites de débit/octets existent comme contrôle de flux de protocole (capacité), pas comme machinerie de quota de dépenses.
- L'entrée du worker vers la passerelle est la liste d'autorisation du protocole worker fermée ; les écritures de transcription sont structurellement contraintes (ids générés par la passerelle, session unique liée).
- L'exécution du worker a des permissions complètes dans la boîte. La boîte est jetable et sans credentials, donc l'approbation par commande ajoute des frictions sans rien protéger ; la limite gardée est la réconciliation entrante et l'audit. L'exécution ne traverse jamais le chemin d'approbation du nœud de la passerelle.
- La politique Internet est une décision du fournisseur au moment de la provision : le profil d'environnement décide à la création de la boîte (pare-feu/groupe de sécurité/réseau sans sortie), optionnellement avec une phase de configuration en réseau que le fournisseur ferme avant la phase d'agent. Core n'implémente pas un basculement réseau d'exécution.
- Hygiène de la boîte au moment de la provision : point de terminaison de métadonnées cloud bloqué ou absence vérifiée, pas de profil d'instance, pas d'agent SSH hérité, pas de socket Docker, env/home propre. Clés d'hôte SSH épinglées à partir de la sortie de provisioning.
- Les approbations et la politique pour tout ce qui est côté passerelle (push, PR, appels de fournisseur) continuent à s'exécuter sur la passerelle.

Rayon d'explosion d'une session worker compromise : la copie de l'espace de travail synchronisée plus ce que les canaux proxy audités permettent — pas de credentials, pas de réseau direct, pas de surface de passerelle au-delà de la liste d'autorisation.

## Capacité

La passerelle relaie chaque prompt et flux de tokens pour N workers, donc v1 énonce un modèle de capacité au lieu de le découvrir en production : limites de workers concurrents par passerelle, fenêtres de crédit par flux (la file d'attente du flux d'événements actuel est non bornée et le plafond du tampon de socket du nœud force-ferme les consommateurs lents — tous deux inadaptés sans modification), spooling disque borné pour les rafales et délestage de charge avec états de contre-pression visibles dans l'interface utilisateur. Le transfert d'espace de travail reste sur son propre canal SSH.

## Cycle de vie

- L'arrêt automatique inactif et le TTL sont une politique de profil de fournisseur, pas des constantes fixes. Les valeurs par défaut sont généreuses avec un keep-alive explicite ; le travail de plusieurs jours est de première classe (le `renew` du fournisseur existe pour les backends basés sur des baux) ; une session avec un tour en vol ou une activité récente n'est jamais réclamée.
- En cas de mort du worker ou de réclamation : le placement se déplace vers `reclaimed`, la ligne de session reste, le message suivant provisionne un worker frais et se resynchronise à partir du dernier checkpoint. La conversation n'est jamais perdue (magasin côté passerelle) ; les modifications de l'espace de travail depuis le dernier checkpoint sont perdues et l'interface utilisateur le dit.
- Réutilisation de bail chaud dès le premier jour (fournisseurs qui le supportent) ; l'instantané d'image après bootstrap est le chemin de démarrage rapide v2.

## Surface de configuration

Minimale et opt-in : un bloc de profil de fournisseur (id de fournisseur, référence credentials/CLI, règles de synchronisation, politique de durée de vie, budgets, phase de configuration optionnelle) plus sélection de placement par session. Pas de nouvelles variables d'environnement. Les installations non configurées ne voient rien.

## Jalons

L'implémentation arrive sous forme de petites PR indépendamment fusionnables ; chaque jalon ci-dessous est une série de PR, pas un seul changement.

1. Fondations : machine d'état d'environnement + contrat de fournisseur + fournisseur en forme de crabbox (SSH statique comme harnais de dev), bootstrap du bundle worker + handshake d'admission, tunnel SSH + épinglage de clé d'hôte, snapshot de worktree géré + synchronisation sortante (modes git + plain). Balayage des orphelins + adoption de redémarrage.
2. Protocole worker + boucle worker : rôle worker authentifié, ops/epochs/curseurs ACK durables, commit de transcription + contrats d'événements en direct, proxy d'inférence avec modèles résolus par la passerelle, contrôle de flux. Un fournisseur, dispatch humain de nouvelles sessions uniquement, pas de transfert. Les tests d'injection de pannes (partition de tunnel, redémarrage de passerelle, mort du worker) gardent la sortie.
3. Dispatch + pull-back + dispatch d'agent : barrière de migration, machine d'état de placement câblée à la barre cible de l'interface utilisateur, réconciliation entrante + checkpoints, audit par environnement, limites de capacité, outil de dispatch d'agent (les sessions worker ne peuvent pas se récurser). Tests d'équivalence d'octets de cache de prompt.
4. Transfert symétrique en direct, après preuve d'injection de pannes du jalon 3.

Plus tard : harnais ACP sur les workers en tant qu'opt-in d'hydratation de credentials par environnement ; démarrage rapide snapshot/image chaud ; fan-out (N baux, même prompt) ; sandboxing OS en boîte ; capture d'artefacts plus riche via le schéma d'artefacts.

## Questions ouvertes

- Disponibilité des plugins/compétences sur les workers : les compétences portées par le repo se synchronisent avec l'espace de travail gratuitement ; les compétences/plugins d'agent configurés par la passerelle ont besoin d'une décision de synchronisation ou d'exclusion explicite (le manifeste d'outil/plugin fait partie du handshake d'admission de toute façon).
- Cadence de checkpoint par défaut : basée sur les tours vs. basée sur le temps pour les sessions très bavardes.
- Comment les profils d'environnement interagissent avec le routage multi-agent (profils par défaut par agent vs. sélection par session uniquement).
