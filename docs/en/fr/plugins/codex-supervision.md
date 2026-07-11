---
summary: "Lister les sessions Codex natives non archivées et créer des branches à partir des sessions locales éligibles dans OpenClaw"
title: "Superviser les sessions Codex"
sidebarTitle: "Supervision Codex"
read_when:
  - Vous souhaitez que les sessions Codex Desktop ou CLI apparaissent dans OpenClaw
  - Vous devez créer une branche à partir d'une session Codex locale stockée ou inactive, ou l'archiver
  - Vous exposez les métadonnées de session Codex à partir de nœuds appairés
---

La supervision Codex est une capacité optionnelle du plugin officiel `codex`. Elle
affiche les sessions source Codex Desktop et CLI non archivées de l'ordinateur Gateway
et des ordinateurs appairés ayant opté pour cette fonctionnalité dans une seule page
**Sessions Codex**.

La version initiale maintient délibérément la propriété étroite :

- Une session locale stockée ou inactive peut créer un Chat OpenClaw verrouillé par modèle à partir
  de son historique utilisateur et assistant persistant délimité. Le premier message démarre un
  fork de snapshot natif, puis démarre le thread complet du harnais Codex avec exactement
  le modèle et le fournisseur que Codex App Server a sélectionnés pour ce fork. Les tours suivants
  restaurent la paire persistante du thread natif canonique tandis que la liaison supervisée
  empêche OpenClaw de substituer un autre runtime, modèle ou fallback. Un contrôle Codex natif
  séparé peut toujours modifier cette paire persistante. Une branche déjà créée ouvre son Chat existant.
- Une session stockée découverte à partir d'un autre processus Codex a une activité en direct inconnue.
  Elle peut créer une branche ou être archivée uniquement après que l'opérateur confirme qu'aucun
  autre client Codex ne l'utilise.
- Une source active reste visible mais ne peut pas créer de branche ou être archivée jusqu'à ce que
  son tour actuel se termine. Si elle a déjà un Chat supervisé, **Ouvrir Chat** reste disponible.
- Une session sur un nœud appairé reste visible en tant que métadonnées uniquement. La continuation
  à distance nécessite un futur pont de nœud de streaming ; l'archivage à distance nécessite
  également un bail de propriété de runner ou un cloisonnement équivalent.
- Les sessions archivées ne sont pas listées. Une session locale stockée ou inactive peut être
  archivée uniquement après que l'opérateur confirme qu'aucun autre client Codex ne l'utilise.

## Avant de commencer

- Installez le plugin officiel `@openclaw/codex` sur le Gateway. L'application OpenClaw
  macOS peut l'installer lorsque vous activez les fonctionnalités Codex ; les installations CLI
  peuvent exécuter `openclaw plugins install @openclaw/codex`.
- Installez et connectez-vous à Codex Desktop ou à la CLI Codex sur chaque ordinateur dont
  vous souhaitez lister les sessions.
- Appairez les ordinateurs distants en tant que nœuds OpenClaw. Chaque ordinateur doit opter
  pour cette fonctionnalité localement ; l'activation de la supervision uniquement sur le Gateway
  n'autorise pas un autre nœud.
- Utilisez un Gateway contrôlé par le propriétaire. Les titres de session, les répertoires de travail
  et les branches Git peuvent révéler des informations sensibles sur le projet.

## Activer la supervision

L'intégration guidée `openclaw onboard` et la configuration de première exécution macOS tentent
d'installer et d'activer la supervision Codex après avoir détecté une installation Codex native
et activé avec succès le backend d'inférence sélectionné. Codex n'a pas besoin d'être le backend
principal. La supervision devient disponible lorsque cette activation de plugin opportuniste réussit.
La disponibilité d'App Server est vérifiée lorsque la supervision se connecte pour la première fois.
Une désactivation explicite du plugin Codex ou un blocage de politique empêchent l'activation opportuniste,
et un `supervision.enabled: false` explicite existant reste un refus.

Les installations existantes peuvent activer la même capacité manuellement :

Activez le plugin `codex` et sa capacité de supervision dans `openclaw.json` :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          supervision: {
            enabled: true,
          },
        },
      },
    },
  },
}
```

Si `plugins.allow` est présent, incluez `codex`. Redémarrez le Gateway après
avoir modifié l'activation du plugin.

Sans paramètres de connexion `appServer` explicites, la supervision utilise une connexion
de supervision stdio gérée séparée contre le répertoire Codex natif de l'utilisateur. Le harnais
Codex ordinaire reste limité à l'agent par défaut. Cela rend les sessions natives visibles dans
les deux applications sans faire partager les tours OpenClaw ordinaires l'état Codex natif.
Définissez explicitement `appServer.homeScope: "user"` si le harnais doit partager cet état aussi.
La supervision honore les paramètres de connexion `appServer` explicites au lieu de les remplacer
par sa valeur par défaut du répertoire utilisateur local.

Un Chat créé via **Sessions Codex** n'est pas une session de harnais ordinaire.
Sa liaison de supervision privée utilise la connexion de supervision pour les lectures de source,
la création de branche canonique, l'injection d'historique et chaque tour ultérieur. Avec la
connexion de supervision locale par défaut, cela préserve le répertoire Codex natif de l'utilisateur,
l'authentification et la configuration du fournisseur sans modifier la valeur par défaut pour les
autres sessions.

Pour la connexion de supervision locale par défaut, le magasin est partagé avec les clients Codex
natifs. OpenClaw ne suppose pas qu'un autre client partage le même processus App Server en direct,
et la propriété du statut natif est locale au processus. Il traite donc un thread que son App Server
de supervision signale comme `notLoaded` comme **Stocké / activité inconnue**, et non comme inactif.

Appliquez le même refus sur chaque hôte de nœud sans interface graphique dont les sessions doivent
apparaître. L'application OpenClaw macOS native lit le même paramètre local lorsqu'elle annonce
son catalogue Codex au Gateway appairé. Ce catalogue Mac appairé natif ne supporte que la valeur
par défaut ou `appServer.transport: "stdio"` explicite avec un `appServer.homeScope: "user"` non défini
ou explicite. `command`, `args` et `clearEnv` sont honorés pour ce processus stdio. Si la configuration
Mac sélectionne `"unix"`, `"websocket"` ou `homeScope: "agent"`, l'application n'annonce pas la
capacité ou la commande du catalogue, et une invocation directe obsolète échoue au lieu d'exposer
le répertoire Codex utilisateur ou de générer un App Server stdio local différent.

Une commande de nœud nouvellement annoncée modifie la surface de commande approuvée du nœud.
Approuvez la mise à jour depuis l'hôte Gateway :

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

Ouvrez **Sessions Codex** dans l'interface de contrôle. La page liste les sessions non archivées
groupées par hôte. La recherche correspond aux titres de session normalisés ; l'actualisation et
la pagination par hôte préservent les hôtes sains lorsqu'un autre hôte est hors ligne ou indisponible.
Chaque page de recherche retournée analyse un nombre limité de pages natives par hôte plutôt que
d'envoyer la requête à App Server, car la recherche native peut également correspondre aux aperçus
de transcription. Utilisez **Charger plus** pour continuer les résultats plus anciens.

La disponibilité de l'hôte et le statut du thread sont séparés. **Hors ligne** ou **Indisponible**
décrit une actualisation d'hôte ; un hôte indisponible ne retourne aucune ligne de session actualisée
et ne change pas le statut natif d'un thread en `offline`. Les lignes de session utilisent les statuts
Codex tels que `idle`, `active`, `notLoaded` ou erreur. Un hôte défaillant ne masque pas les résultats
des hôtes sains.

## Utiliser la CLI de l'opérateur

La CLI du terminal expose le même catalogue non archivé et les actions de branche et d'archivage
locales au Gateway :

```bash
openclaw codex sessions [--search <text>] [--host <id>] [--limit <count>] [--cursor <cursor>] [--json] [--url <url>] [--token <token>] [--timeout <ms>] [--expect-final]
openclaw codex continue <thread-id> [--json] [--url <url>] [--token <token>] [--timeout <ms>] [--expect-final]
openclaw codex archive <thread-id> --confirm-no-other-runner [--json] [--url <url>] [--token <token>] [--timeout <ms>] [--expect-final]
```

Options de `openclaw codex sessions` :

- `--search <text>` recherche les titres de session sans tenir compte de la casse.
- `--host <id>` limite la réponse à un hôte de catalogue stable, tel que
  `gateway:local` ou `node:<node-id>`.
- `--limit <count>` définit 1 à 100 lignes par hôte ; la valeur par défaut est 50.
- `--cursor <cursor>` continue une page d'hôte et nécessite donc `--host`.
- `--json` imprime la réponse Gateway structurée.

Les trois commandes héritent de `--url`, `--token` et `--timeout <ms>` du
client Gateway ; le délai d'expiration par défaut est 30 000 ms. Elles exposent également
le commutateur partagé `--expect-final`, qui ne modifie pas ces RPC de supervision unaires.
Chaque commande nécessite la portée Gateway `operator.write`.
La sortie standard `-h, --help` est disponible sur chaque sous-commande.
Il n'y a pas d'option archivée ou include-archived. `sessions` peut lister les hôtes appairés,
mais `continue` et `archive` ciblent toujours `gateway:local` ; les lignes appairées sont
en lecture seule. L'archivage nécessite toujours `--confirm-no-other-runner`.

Ces commandes shell sont distinctes des commandes runtime `/codex` dans le chat.
`/codex threads [filter]` liste les threads App Server disponibles pour la connexion de
conversation actuelle. `/codex sessions --host <node>` liste les fichiers de session CLI
Codex reprennables sur un nœud, pas le catalogue de flotte de supervision. `/codex
resume` et `/codex bind` attachent la conversation actuelle au lieu de créer une branche
supervisée sûre, et un Chat supervisé verrouillé par modèle rejette ces mutations de liaison.
Il n'y a pas de commande runtime `/codex continue` ou `/codex archive`.

## Créer une branche à partir d'une session locale

Choisissez **Continuer en tant que branche** sur une ligne stockée ou inactive de l'ordinateur Gateway.
OpenClaw crée une entrée Chat normale, reflète l'historique de l'utilisateur et de l'assistant délimité
à travers le dernier tour persistant du terminal de la source (complété, interrompu ou
échoué), enregistre une branche de harnais en attente, et ouvre le Chat. Le sélecteur de modèle générique est verrouillé, mais aucun modèle ou fournisseur concret n'a été sélectionné pour le moment. La
source n'est pas reprise, et le thread de harnais canonique n'est pas encore démarré.
Répéter l'action ouvre le Chat existant au lieu de créer une autre
branche.

Le miroir conserve la queue visible la plus récente qui respecte les trois limites : au maximum 200
messages utilisateur ou assistant, 512 KiB de texte UTF-8 au total, et 64 KiB par
message. Les messages surdimensionnés sont tronqués avec un marqueur, et les messages plus anciens sont
omis lorsqu'une limite est atteinte. Une entrée image ou image locale devient l'espace réservé littéral
`[Image attachment]` ; les données d'image et les chemins locaux ne sont pas copiés.

Envoyez le premier message Chat normal pour commencer le travail. Le harnais Codex installe l'
approbation réelle, l'élicitation, l'événement et les gestionnaires de livraison. Il utilise un fork
natif temporaire sur la connexion de supervision pour épingler l'instantané source sans
fournir de modèle ou de remplacement de fournisseur. Codex App Server sélectionne les deux à partir de sa
configuration native actuelle et retourne la sélection réelle. Sur cette même
connexion, OpenClaw démarre le thread de harnais complet `appServer`-source canonique
sous son cwd et sa politique d'exécution avec exactement cette paire retournée, injecte l'
historique visible délimité, et archive le fork temporaire. Le thread canonique
a la surface complète de l'outil OpenClaw. C'est une branche d'historique visible, pas
un clone de déploiement natif complet : le raisonnement source, les appels d'outils et les résultats d'outils
sont omis. Ce tour et tous les tours ultérieurs restent sur la connexion Codex supervisée
plutôt que sur un autre runtime de modèle OpenClaw ou le harnais agent-home ordinaire.

La sélection retournée n'est pas une preuve du modèle historique de la source. Si la
configuration native actuelle diffère du modèle enregistré pour le dernier tour de la source, Codex émet son
avertissement normal de différence de modèle. OpenClaw utilise la paire retournée pour le démarrage du thread canonique. Codex persiste le modèle natif et le fournisseur du thread canonique, et les reprises ultérieures les préservent car
OpenClaw omet les remplacements de modèle et de fournisseur. Si le thread canonique est modifié
via un contrôle Codex natif séparé, OpenClaw accepte la sélection persistée de Codex. OpenClaw ne substitue jamais son modèle externe ou sa chaîne de secours.

Le Chat verrouillé par modèle supervisé ne peut pas être supprimé, changer de modèles, utiliser `/new`
ou `/reset`, invoquer l'action de réinitialisation de session Gateway, ou utiliser l'action générique
**Fork session**. Les mutations `/codex model <model>`, `/codex
bind`, `/codex resume` (y compris une session de nœud avec `--bind here`), et
`/codex detach` ou `/codex unbind` sont également rejetées car elles remplaceraient
ou effaceraient la liaison native verrouillée. La requête `/codex model` et `/codex fast`,
`/codex permissions`, et `/codex threads` restent disponibles. Démarrez une autre
session ordinaire lorsque vous voulez un modèle différent ou un thread frais.

Gardez la supervision activée pour ce Chat. Si la supervision est désactivée ou sa
liaison de connexion stockée devient indisponible ou incohérente, le tour échoue
fermé au lieu de passer à une session agent-home ordinaire.

Désactiver ou désinstaller le plugin `codex` ne libère pas cette propriété ou
ne rend pas le Chat éligible pour un autre modèle. Le Chat verrouillé reste préservé mais
indisponible ; réinstallez ou réactivez le même plugin et redémarrez la Gateway pour
le reprendre. Ce comportement d'échec fermé délibéré empêche le nettoyage de la rétention ou une
panne temporaire du plugin d'orpheliner silencieusement la liaison native.

L'outil agent `codex_threads` suit la même limite. Il ne peut pas attacher un
fork différent ou archiver le thread natif lié du Chat. La liste et les lectures
métadonnées uniquement restent disponibles. Les lectures de transcription brute nécessitent `allowRawTranscripts`.
Lorsque l'accès brut est désactivé, `codex_threads` rejette également la recherche de liste car
la recherche native inclut les aperçus de transcription ; l'interface utilisateur de contrôle et l'interface de ligne de commande de l'opérateur
fournissent toujours une recherche limitée au titre uniquement. Renommer, désarchiver, fork détaché, et
archiver un thread non lié non possédé nécessitent
`allowWriteControls`. Aucune option ne contourne la liaison verrouillée.

OpenClaw ne s'abonne pas aux demandes d'approbation ou n'y répond pas en se contentant de lister
le thread source ou d'afficher le Chat en attente. Démarrer un thread de harnais canonique distinct
au premier tour permet à un autre processus Codex de conserver la propriété de la source sans créer de
écrivains de déploiement concurrents.

L'interface de ligne de commande source originale ou VS Code reste visible pour les clients natifs et le
catalogue OpenClaw. La branche canonique est stockée en tant que thread Codex natif, mais
son type de source est `appServer` ; Codex Desktop ou un autre client natif peut filtrer
ce type de source, donc la branche elle-même n'est pas garantie d'apparaître dans chaque
vue d'historique natif.

Une ligne active signalée par App Server d'OpenClaw ne peut pas démarrer une nouvelle branche. Attendez
que le tour actuel se termine et actualisez le catalogue. Codex App Server
sérialise les mutations au sein d'un processus, mais il ne fournit pas un exécuteur exclusif
entre processus ou un bail de propriétaire d'approbation.

Pour une ligne **Stockée / activité inconnue**, le miroir Chat et l'épinglage d'instantané du premier tour
utilisent l'état de Codex à travers le dernier tour persistant terminal. Le thread
source n'est pas repris, interrompu ou archivé. Si un autre processus a un
tour en cours, son dernier travail en vol pourrait ne pas être présent dans la branche.

## Archiver une session locale

Choisissez **Archiver** sur une ligne Gateway-locale stockée ou inactive, puis confirmez qu'aucun
autre client Codex ou exécuteur OpenClaw n'utilise ce thread ou ses
descendants générés. OpenClaw lit fraîchement l'état local du processus, procède uniquement pour
`idle` ou `notLoaded`, appelle l'opération d'archivage Codex native, et supprime la
session de la liste non archivée. Codex natif tente également d'archiver les
descendants générés du thread.

L'archivage n'est pas disponible lorsque la lecture fraîche signale la session active ou dans un
état d'erreur, lorsqu'elle appartient à un nœud appairé, ou tandis qu'un Chat
supervisé nouvellement créé a toujours une branche en attente de cette source. Envoyez le premier message du Chat pour matérialiser sa branche canonique avant d'archiver la source.
L'archivage est également bloqué lorsqu'OpenClaw sait qu'une liaison active possède le
thread cible exact ou tout descendant généré non archivé. OpenClaw suit la
requête de descendant Codex expérimentale à travers chaque page ; une réponse invalide,
une défaillance de requête, un curseur ou thread répété, ou l'épuisement de la limite de sécurité rejettent
l'archivage.

La lecture, l'énumération des descendants et les demandes d'archivage ne sont pas une seule opération conditionnelle,
donc un tour peut toujours démarrer entre eux. L'état d'App Server n'est pas non plus
partagé entre les processus indépendants. La confirmation est donc la
limite de sécurité pour les clients inconnus et cette course : quittez ou vérifiez autrement
chaque autre client avant de confirmer. Restaurez un thread archivé avec Codex
Desktop, l'interface de ligne de commande Codex, ou un flux de gestion de thread natif autorisé par le propriétaire ;
il réapparaît après désarchivage.

```bash
codex unarchive <thread-id>
```

## Comprendre les limites des nœuds appairés

Les nœuds appairés exposent la commande
`codex.appServer.threads.list.v1` en lecture seule versionnée. La Gateway reçoit les
métadonnées normalisées, pas les points de terminaison App Server bruts ou les transcriptions. Le transport d'invocation de nœud actuel
est demande/réponse uniquement, donc il ne peut pas supporter l'événement, l'approbation et le
cycle de vie de streaming à longue durée de vie requis par le harnais Codex.

Pour cette raison, les lignes distantes restent visibles mais n'offrent pas **Continuer** ou
**Archiver**, même lorsque le thread distant est inactif. Utilisez Codex sur cet ordinateur
jusqu'à ce qu'un pont d'exécuteur de streaming côté nœud existe pour la continuation et une limite de propriété d'exécuteur sûre existe pour l'archivage.

## Métadonnées et permissions

Les lignes du catalogue peuvent inclure :

- identifiants de thread et de session
- titre et répertoire de travail
- état actuel et drapeaux d'attente actifs
- horodatages créés, mis à jour et d'activité
- source, fournisseur de modèle, version de l'interface de ligne de commande Codex et branche Git

La projection du nœud appairé exclut les aperçus de transcription, les tours, les chemins de déploiement,
le chemin d'accueil Codex, les télécommandes Git, les SHA de commit et les erreurs App Server brutes. L'accès au catalogue nécessite la portée `operator.write` Gateway car l'agrégation de flotte
utilise le chemin `node.invoke` standard, même si la commande de nœud est en lecture seule.

`supervision.allowRawTranscripts` et `supervision.allowWriteControls` régissent
l'agent autonome et les outils MCP autonomes. Les deux sont par défaut `false`. Avec
la supervision activée, `codex_threads` supprime les aperçus de transcription et les tours des
résultats de liste et de lecture métadonnées uniquement sauf si les transcriptions brutes sont autorisées ; une
lecture inclusive de tour échoue fermée. Chaque fork, renommage, archivage et désarchivage
nécessite des contrôles d'écriture. Ces options n'accordent pas d'actions d'interface utilisateur de contrôle supplémentaires ou ne contournent pas la liaison, l'hôte, l'état ou les vérifications de confirmation.

### Outils de compatibilité

Le plugin `codex` officiel conserve les cinq noms d'outil Supervisor expédiés pour
les clients agent et MCP autonomes existants :

- `codex_endpoint_probe`
- `codex_sessions_list`
- `codex_session_read`
- `codex_session_send`
- `codex_session_interrupt`

`codex_sessions_list` est chargé uniquement par défaut ; il n'y a pas de paramètre `loaded_only`. Définissez `include_stored: true` pour également lire les lignes stockées non archivées de la base de données d'état de Codex. Le plafond `max_stored_sessions` optionnel est par défaut 200 et accepte 1 à 1 000 lignes par point de terminaison. Il ne plafonne pas les lignes chargées.
Sans permission de transcription brute, les résultats de liste omettent les noms dérivés de transcription, les aperçus et les erreurs de point de terminaison détaillées.

`codex_session_read` nécessite `allowRawTranscripts` ; `include_turns: true`
demande en outre à Codex les tours.

`codex_session_send` et `codex_session_interrupt` nécessitent
`allowWriteControls`. Send accepte `mode: "auto" | "start" | "steer"`, mais
`"start"` est toujours refusé et à la fois `"auto"` et `"steer"` ne peuvent que diriger un
tour actif lisible. Un thread inactif est refusé avec des conseils pour utiliser **Codex
Sessions**, où le harnais complet installe l'approbation et les gestionnaires d'outils avant
la continuation. Interrupt nécessite également un tour actif lisible. Ces outils
ne reprennent pas ou ne démarrent pas un thread source inactif.

`openclaw doctor --fix` déplace une entrée `codex-supervisor` retirée, ses champs de point de terminaison et de permission, et les références de politique d'autorisation de plugin dans le plugin `codex` officiel sans écraser les paramètres canoniques explicites. L'adaptateur MCP de compatibilité autonome continue de charger les mêmes cinq outils à partir de ce plugin ; les variables d'environnement de politique héritée s'appliquent uniquement à l'intérieur de cet adaptateur de confiance.

Pour chaque champ de configuration de supervision, voir
[Référence du harnais Codex](/fr/plugins/codex-harness-reference#supervision).

## Dépannage

**Aucune session n'apparaît :** vérifiez que `@openclaw/codex` est installé, que le plugin et `supervision.enabled` sont vrais, que la liste d'autorisation de plugin actuelle permet `codex`, et que les sessions ne sont pas archivées. Redémarrez la Gateway ou le nœud après avoir modifié l'activation.

**Continuer est désactivé :** une ligne non mappée est active, appartient à un nœud appairé,
son hôte est hors ligne, ou une autre action est en attente. Les lignes stockées et inactives Gateway-locales offrent **Continuer en tant que branche** au lieu de la prise de contrôle de thread exact non sûre. Une ligne qui a déjà un Chat supervisé offre **Ouvrir Chat**.

**L'archivage est désactivé :** l'archivage est disponible pour les lignes stockées/activité inconnue et inactives Gateway-locales après confirmation d'aucun autre exécuteur. Les lignes actives, erreur,
hors ligne, nœud appairé, branche en attente et propriétaire de liaison exact connu restent en lecture seule pour l'archivage.

**Une session archivée a disparu :** c'est attendu. La page de supervision n'a pas de vue archivée. Exécutez `codex unarchive <thread-id>` ou utilisez Codex Desktop pour l'afficher à nouveau.

**L'ancienne configuration `codex-supervisor` reste :** exécutez `openclaw doctor --fix`. Doctor déplace l'entrée de plugin retirée et les références de politique de plugin associées dans
`plugins.entries.codex.config.supervision` sans écraser les paramètres Codex explicites.

## Connexes

- [Harnais Codex](/fr/plugins/codex-harness)
- [Référence du harnais Codex](/fr/plugins/codex-harness-reference)
- [Runtime du harnais Codex](/fr/plugins/codex-harness-runtime)
- [Architecture de supervision Codex](/fr/specs/codex-supervision)
- [Nœuds](/fr/nodes)
- [Sécurité de la passerelle](/fr/gateway/security)
