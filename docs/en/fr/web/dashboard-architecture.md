---
summary: "Tableaux de bord de session : plan d'architecture et de mise en œuvre (conception technique, pré-GA)"
read_when:
  - Implementing or reviewing the session dashboard (boards) feature
  - Changing widget hosting, the widget bridge, or board storage
title: "Architecture des tableaux de bord"
---

<Note>
Document de conception technique pour la fonctionnalité de tableau de bord de session, rédigé avant et pendant la mise en œuvre. Il est la source de vérité pour la construction. Lorsque la fonctionnalité est lancée, `/web/dashboard` devient la page visible par l'utilisateur et cette page reste comme référence d'architecture.
</Note>

## Vision

Travailler avec un agent aujourd'hui, c'est un flux de texte. Le tableau de bord en fait un établi : l'agent affiche des widgets en direct et interactifs ; l'utilisateur les épingle sur une surface persistante ; le chat s'ancre sur le côté (ou se cache) et le contenu principal est le tableau. Vous passez de « parler à l'agent » à « faire fonctionner un panneau de contrôle que l'agent a construit pour vous » sans jamais quitter la session.

Principes :

- **Un tableau est une face d'une session, pas un nouvel objet.** Chaque session (thread) a deux faces : la transcription et le tableau. Une session sans widgets épinglés est un simple chat. Épinglez un widget et le tableau existe. Les tableaux héritent de l'identité de la session, de la propriété de l'agent, de la dénomination, de l'épinglage et du cycle de vie. Il n'y a pas de `dashboard_create`, pas de registre de tableau, pas de modèle ACL séparé.
- **Parité avec l'agent.** Tout ce que l'utilisateur peut faire sur un tableau, l'agent peut le faire avec des outils : ajouter/mettre à jour/supprimer des widgets, les organiser, gérer les onglets, basculer l'onglet visible, ancrer ou masquer le chat.
- **Natif, pas intégré.** Le tableau est composé de composants Lit dans le shell de l'interface de contrôle (le même système de conception que le reste de l'application). Seul le _contenu_ du widget est isolé dans des iframes. Pas de barre d'adresse, pas de chrome du navigateur.
- **Petite surface d'agent.** Les widgets sont adressés par un nom stable et mis à jour sur place. La mise en page est une grille auto-compactante fluide ; l'agent parle de tailles et d'ancres, jamais de pixels ou de coordonnées.
- **Capacités plutôt que confiance.** Le code du widget est du HTML/JS arbitraire créé par l'agent dans un bac à sable strict. La portée (données de passerelle, actions, réseau) n'existe que par le biais d'un manifeste de capacité déclaré et accordé par l'opérateur.

## Concepts

| Concept             | Définition                                                                                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Session (thread)    | Session de passerelle existante, identifiée par `sessionKey` stable. Propriété d'un agent.                                                                        |
| Tableau             | La face widget d'une session. Existe ssi la session a des widgets/onglets. Survit à `/new`/`/reset` (attaché à `sessionKey`, pas à la transcription).                 |
| Onglet              | Une page de présentation d'un tableau : quels widgets, leur arrangement, et l'état d'ancrage du chat (`left`/`right`/`bottom`/`hidden`). Les tableaux commencent avec un onglet implicite. |
| Widget              | Programme HTML/JS nommé et isolé, propriété de la session. Adressé comme `sessionKey` + `name`. Mis à jour sur place par nom.                                              |
| Manifeste de capacité | Déclaration par widget de la portée : `data` (liaisons de lecture), `actions` (verbes autorisés), `prompt` (envoyer à la session), `net` (origines autorisées).                      |
| Épingle (widget)    | Déplacement d'un widget de transcription sur le tableau de la session (affordance utilisateur ou argument d'outil d'agent). Dépingler le supprime du tableau.                                         |
| Épingle (session)   | Épinglage existant de sessions dans la barre latérale. Une session épinglée avec un tableau s'ouvre sur sa face tableau.                                                                      |

## Flux UX

- **Graduation :** l'agent appelle `show_widget` dans n'importe quel chat → le widget s'affiche en ligne dans la transcription exactement comme aujourd'hui → le survol affiche **Épingler au tableau de bord** → le widget apparaît sur le tableau de la session. L'agent peut passer `pin: true` pour faire la même chose.
- **Vue tableau :** une session avec un tableau obtient un basculement de face (Chat / Tableau de bord). Vue tableau = bande d'onglets (uniquement si >1 onglet) + grille fluide + volet de chat ancré. Le dock de chat est redimensionnable, déplaçable (gauche/droite/bas) et réductible exactement comme la barre latérale. L'état du dock par onglet est mémorisé.
- **Glisser-déposer :** l'utilisateur fait glisser les widgets ; la grille se compacte automatiquement (les widgets flottent vers le haut, les voisins se reflètent). Le redimensionnement par poignée s'accroche aux étapes de taille. Pas de placement en pixels — pour personne.
- **Avertissement de réinitialisation :** `/new` / `/reset` sur une session avec tableau demande une confirmation dans l'interface Web (« le contexte se réinitialise, le tableau reste ») et conserve le tableau.
- **Barre latérale :** les sessions épinglées affichent leur face tableau quand elles en ont une. Le tableau de la session Accueil est le « tableau de bord de l'agent » par défaut.
- **Interactions** (trois niveaux, voir ci-dessous) : événements d'état silencieux, envois d'invite visibles et déclencheurs d'automatisation.

## Niveaux d'interaction

1. **Événements d'état (par défaut).** Les interactions de l'interface utilisateur du widget que le modèle devrait connaître mais ne pas traiter. `bridge.emitState({...})` ajoute un avis de session structuré (même mécanisme que les avis d'activité de groupe). Aucun tour d'agent n'est lancé ; le modèle voit les avis accumulés lors de sa prochaine exécution.
2. **Invites (conversation explicite).** `bridge.sendPrompt(text)` — nécessite l'activation de l'utilisateur ; envoie un message utilisateur visible dans la session (le chat ancré l'affiche). Limité en débit ; chaque envoi est confirmé par l'utilisateur sauf si le widget détient la subvention de capacité `prompt`.
3. **Automatisation.** `bridge.runAction(name, args)` — déclenche une action déclarée dans le manifeste. Ensemble de verbes initial : `cron.trigger` (exécuter un travail cron existant maintenant) et `binding.refresh`. Les travaux cron s'exécutent déjà dans des sessions d'exécution visibles et isolées et peuvent utiliser un modèle moins cher : c'est le chemin « le petit modèle alimente le widget ». Pas de sessions cachées nulle part.

## Modèle de widget et hébergement

Le HTML/JS du widget est créé par l'agent (généralement via `show_widget`), enveloppé
dans l'enveloppe de document standard (CSP meta, rapporteur de taille, amorçage du pont) et
rendu dans `<iframe sandbox="allow-scripts">` (jamais `allow-same-origin`).

- **Widgets en ligne (transcription)** conservent le pipeline canvas-document actuel :
  écrits sous le répertoire d'état, servis par la passerelle, élagués par portée, sans
  approbation (ils sont sans capacités par construction — les envois de prompt sont confirmés par l'utilisateur).
- **Widgets de tableau** sont l'état de session : les octets vivent dans la base de données SQLite
  de l'agent propriétaire (`board_widgets`), servis par une route de passerelle principale
  (`/__openclaw__/board/<agentId>/<sessionKey>/<name>/`) qui lit la base de données.
  L'épinglage d'un widget de transcription copie les octets. Limites : 256 Ko par widget,
  48 widgets par tableau.
- **Mise à jour sur place :** la réémission d'un widget avec le même `name` remplace les
  octets, incrémente `revision`, diffuse `board.changed`, et les vues en direct rechargent
  cet iframe uniquement.
- **Gel des octets :** les capacités accordées se lient au sha256 des octets du widget.
  Changer les octets conserve les subventions `data`/`net`/`actions` uniquement si la nouvelle
  révision déclare un sous-ensemble du manifeste accordé ; un manifeste élargi
  redemande à l'opérateur.

### Les widgets hébergent du contenu ; les applications MCP sont un type de contenu

Le **widget est la primitive OpenClaw** : la cellule de tableau nommée, épinglée, dimensionnée,
appartenant à la session avec un enregistrement de subvention. Ce qui s'affiche à l'intérieur est un
type de contenu :

- `html` — créé par l'agent via `show_widget`, octets dans le stockage du tableau.
- `mcp-app` — une vue d'application MCP tierce (`ui://` ressource d'un serveur configuré)
  hébergée à l'intérieur de la cellule du widget.

Les applications MCP ne définissent pas le modèle de widget ; les widgets ont acquis la capacité de les
héberger. L'identité, le placement, l'épinglage, les subventions et l'API côté auteur restent
OpenClaw — donc le code `show_widget` reste aussi court qu'aujourd'hui et n'a jamais
besoin de savoir que la spécification MCP Apps existe.

Infrastructure partagée en dessous (c'est là que la simplification se fait) :

- **Un hôte sandbox unique.** Les widgets `html` se rendent via le même pipeline
  renforcé que les applications MCP (double-iframe sur l'origine sandbox dédiée, CSP par widget
  déclaré et décodé en échec fermé) au lieu d'un deuxième hôte iframe sur mesure. Le proxy
  reçoit le HTML par valeur, donc le contenu local est le cas naturel.
- **Un modèle d'autorisation unique.** La portée d'un widget est une liste d'autorisation accordée,
  quel que soit son type : pour les widgets `html`, les outils hôtes ; pour les widgets `mcp-app`,
  les outils visibles par l'application du serveur (via le mécanisme `allowedAppToolNames` existant,
  rendu durable par widget au lieu de par exécution de frappe).
- **Outils hôtes pour les widgets `html`** (exposés sur le pont du widget, vérifiés
  par rapport à la subvention) :
  - `openclaw.prompt.send` — niveau 2 ; acheminé via le compositeur visible,
    confirmé par l'utilisateur sauf s'il est accordé
  - `openclaw.state.emit` — avis de session de niveau 1 (fusionnés, plafonnés en taille)
  - `openclaw.data.read` — liaisons paramétrées en lecture seule (ensemble RPC en lecture autorisée existant), résolues côté passerelle
  - `openclaw.cron.trigger` — automatisation de niveau 3
- **`net` = CSP.** La portée réseau utilise la déclaration CSP par widget déjà expédiée
  (`connect-src` origines) — le widget météo auto-mise à jour récupère son API directement
  depuis le sandbox, sans implication de la passerelle.
- **Subventions.** Un widget ne déclarant rien s'affiche immédiatement (en sandbox,
  `default-src 'none'`, les envois de prompt confirmés individuellement) — même confiance
  que les widgets de chat en ligne d'aujourd'hui. Les outils/origines déclarés mettent le widget
  en `pending` sur le tableau : une carte d'espace réserve les énumère lisiblement avec
  un **Autoriser**/**Rejeter** en un clic. Les subventions sont par nom de widget ; pour les widgets `html`
  elles sont gelées en octets (sha256), et les octets modifiés conservent la subvention uniquement si la
  déclaration a diminué.
- **Shim de création.** L'enveloppe de document injecte
  `window.openclaw.sendPrompt/emitState/read/call` comme l'API auteur stable ;
  que le transport en dessous soit notre canal ou l'AppBridge est un détail interne
  que l'auteur du widget ne voit jamais. Les rapports de taille et les jetons de thème
  empruntent le même pont.

### Affichage de la transcription : une carte de widget unique

L'affichage en ligne s'unifie sur la primitive de widget. Quand un résultat d'outil porte l'interface utilisateur —
sortie `show_widget` ou un résultat d'outil MCP avec une ressource d'application — le système
matérialise un **widget éphémère, auto-nommé** (scoped à la session, élagué) et
la transcription affiche une seule carte de widget qui se distribue sur le type de contenu.
L'affichage automatique de l'application MCP reste exactement comme la spécification l'attend (zéro travail de modèle supplémentaire) ;
c'est juste un widget en dessous. Cela supprime les cas spéciaux `mcpApp`
parallèles dans le rendu de chat (portillonnage de surface, déduplication séparée), donne à chaque
interface utilisateur en ligne la même affordance d'épinglage, et fait du registre de widget le chemin de réouverture principal
(la reconstruction de balayage de transcription reste comme solution de secours pour l'historique jamais épinglé).
L'hôte autonome en lecture seule avec ticket chevauche les tableaux comme une surface de réouverture
persistante — candidate de consolidation à évaluer en T6, non supposée.

Composition : v1 est l'adjacence de grille (widget chrome d'agent à côté d'un widget d'application sur
un onglet). v2 ajoute **des emplacements d'application gérés par l'hôte** — le HTML du widget d'agent
déclare une région d'emplacement et l'hôte compose la vraie vue d'application comme un sandbox frère.
L'application ne s'affiche jamais à l'intérieur de l'iframe de l'agent : l'imbrication briserait
l'identité du pont et permettrait le chevauchement/clickjack de l'interface utilisateur d'application accordée, donc l'emplacement est un
contrat de mise en page, pas une intégration.

### Widgets fournis par le serveur (applications MCP épinglées)

Avec l'hôte unifié, épingler une application MCP tierce est juste un widget dont
le contenu est récupéré du serveur au lieu d'être stocké : `board_widgets` conserve le
descripteur (`serverName`, `toolName`, `uiResourceUri`, `toolCallId` d'origine
+ `sessionKey`) au lieu d'octets HTML, et le tableau rémet la vue en location au-delà du
TTL de 10 minutes du tour de chat (en récupérant la ressource `ui://` sur obsolescence).
Les vues d'application MCP en ligne de chat obtiennent la même affordance **Épingler au tableau de bord**
que les widgets d'agent. Les vues réouvertes sont en lecture seule par conception ; les applications épinglées
qui doivent rester interactives obtiennent une subvention durable sur les outils visibles par l'application du serveur
(liste d'autorisation explicite affichée à l'opérateur lors de l'épinglage), découplée
de l'exécution de frappe. Les épingles non accordées restent en lecture seule — toujours utiles pour les tableaux de bord d'affichage.
v1 épingle au tableau du session d'origine ; l'épinglage entre sessions
a besoin d'un courtier de location et attend. Coordonner avec la PR ouverte #109807 (routage du compositeur `ui/message`,
propagation de thème/taille).

## Mise en page : grille fluide

12 colonnes, hauteur de ligne fixe, **compactage automatique** (gravité vers le haut, décalage au glissement —
sémantique gridstack, implémentée nativement ; les mathématiques de grille restent pures et
sans DOM). État de mise en page du widget par onglet : `{ name, w (1-12), h (rows) }` plus
ordre. Vocabulaire d'agent :

- `size`: `sm` (3×3) · `md` (6×4) · `lg` (8×6) · `xl` (12×8) · `full`
  (onglet widget unique)
- `after: <widgetName>` ancre de commande optionnelle ; omis = ajouter
- L'utilisateur glisse/redimensionne librement ; le même modèle d'ordre+taille fait l'aller-retour.

## Modèle de données (par base de données d'agent)

Nouvelles tables dans `agents/<agentId>/agent/openclaw-agent.sqlite`
(**nécessite une augmentation de version de schéma de base de données d'agent — approbation de l'opérateur requise
avant que cela ne soit déployé**) :

```sql
CREATE TABLE board_tabs (
  session_key TEXT NOT NULL,
  tab_id      TEXT NOT NULL,           -- slug
  title       TEXT NOT NULL,
  position    INTEGER NOT NULL,
  chat_dock   TEXT NOT NULL DEFAULT 'right',  -- left|right|bottom|hidden
  created_by  TEXT NOT NULL,           -- 'user' | 'agent'
  PRIMARY KEY (session_key, tab_id)
) STRICT;

CREATE TABLE board_widgets (
  session_key  TEXT NOT NULL,
  name         TEXT NOT NULL,          -- stable widget name
  tab_id       TEXT NOT NULL,
  title        TEXT,
  html         BLOB NOT NULL,          -- wrapped document source
  sha256       TEXT NOT NULL,
  revision     INTEGER NOT NULL,
  size_w       INTEGER NOT NULL,
  size_h       INTEGER NOT NULL,
  position     INTEGER NOT NULL,       -- order within tab (auto-compact input)
  manifest     TEXT NOT NULL DEFAULT '{}',  -- capability manifest JSON
  grant_state  TEXT NOT NULL DEFAULT 'none', -- none|pending|granted|rejected
  granted_sha  TEXT,                   -- byte-frozen grant
  created_by   TEXT NOT NULL,
  created_at   INTEGER NOT NULL,
  updated_at   INTEGER NOT NULL,
  PRIMARY KEY (session_key, name)
) STRICT;
```

L'existence du tableau = toute ligne pour le `sessionKey`. La suppression d'une session supprime ses
lignes de tableau. `/new`/`/reset` ne les touche pas.

## Surface de protocole

RPC (table de méthode principale, schémas typebox dans `gateway-protocol`) :

- `board.get { sessionKey }` → onglets + métadonnées de widget (pas d'octets) — `operator.read`
- `board.update { sessionKey, ops[] }` — CRUD d'onglet/réorganisation, déplacement/redimensionnement/
  suppression/dépinglage de widget, état d'amarrage, onglet de focus — `operator.write`
- `board.widget.put { sessionKey, name, html, manifest, placement }` —
  `operator.write` (chemin d'outil d'agent et chemin d'épinglage)
- `board.widget.grant { sessionKey, name, decision }` — `operator.approvals`
- `board.event { sessionKey, widget, payload }` — ingestion d'événement d'état de niveau 1 —
  `operator.write`

Événements (dans `EVENT_SCOPE_GUARDS`, portée de lecture) :

- `board.changed { sessionKey, revision, widget? }` — l'état persisté a changé ;
  l'interface utilisateur récupère (et recharge un iframe quand `widget` est présent).
- `board.command { sessionKey, command }` — lecteur d'interface utilisateur transitoire (l'agent bascule
  l'onglet visible, bascule l'amarrage de chat) — le modèle `ui.command`.

Les octets du widget sont servis sur la surface HTTP authentifiée, pas le socket.

## Outils d'agent

Trois outils au total (principal, toujours enregistré ; rendu porté sur la
capacité client `inline-widgets` comme aujourd'hui) :

- `show_widget { title, widget_code, name?, pin?, size?, tab?, after?,
capabilities? }` — créer/mettre à jour par nom ; `pin` le place sur le tableau.
  Sans `name`/`pin` il se comporte exactement comme aujourd'hui (en ligne, éphémère).
- `dashboard { action, ... }` — verbes de gestion du tableau : `read`, `tab_create`,
  `tab_update`, `tab_delete`, `tabs_reorder`, `widget_move`, `widget_remove`,
  `unpin`, `focus_tab`, `set_chat_dock`.
- Les outils `cron` existants couvrent le niveau d'automatisation ; aucun nouvel outil nécessaire.

Les descriptions d'outils enseignent le vocabulaire de taille/ancre et le modèle de niveau.
L'agent est informé des événements de niveau 1 de l'utilisateur via les avis de session, par ex.
`[dashboard] user clicked "Refresh" on widget weather (tab main)`.

## Ce que cela remplace

- **`extensions/workspaces` est supprimé.** Expérimental, `enabledByDefault:
false`, jamais dans une version stable (première apparition dans les bêtas 2026.7.2). Pas
  de migration ; une règle de docteur supprime les `<stateDir>/workspaces/` obsolètes s'ils sont présents.
  Idées récoltées : mathématiques de grille pure, modèle de sécurité du pont (amorçage du port,
  portillonnage de liaison, limites de débit), approbation gelée en octets.
- **L'hébergement de widget passe de `extensions/canvas` au cœur.** Le magasin de documents canvas,
  l'enveloppe de document, la fourniture HTTP et l'outil `show_widget` deviennent cœur
  (`src/canvas/`) ; le plugin conserve l'outil de contrôle node-canvas (`canvas`) et
  A2UI. L'annonce `pluginSurfaceUrls["canvas"]` et
  les chemins `/__openclaw__/canvas` sont des contrats de client natif expédiés et restent
  stables. Les sessions Discord conservent la variante `show_widget` appartenant à Discord.
- **WorkBoard n'est pas touché** (l'intégration est un programme de suivi).

## Non-objectifs (ce programme)

- Partage de tableau multi-utilisateur/ACL (futur ; arrivera via le partage de session).
- Rendu natif du tableau macOS/iOS (ils l'obtiennent partout où ils intègrent l'interface utilisateur de contrôle ;
  le chemin du widget en ligne est inchangé).
- Widgets de données intégrés (sessions/utilisation/cartes cron) — le pont de capacité plus
  les widgets créés par l'agent couvrent v1 ; un registre de type intégré peut venir plus tard.
- WorkBoard-sur-tableau de bord.

## Plan de mise en œuvre

Worktrees indépendants, construits avec Codex, révision+intégration séquentielle. Intégration-puis-correction.

| #   | Branche                              | Portée                                                                                                                                                                             | Dépend de                        |
| --- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| T1  | `claude/dashboard-remove-workspaces` | Supprimer le plugin workspaces + UI + docs + clés i18n ; règle de nettoyage doctor                                                                                               | —                                |
| T2  | `claude/dashboard-canvas-core`       | Promouvoir l'hébergement de widget + `show_widget` au cœur ; le plugin canvas conserve l'outil de nœud ; zéro changement de comportement                                          | —                                |
| T3  | `claude/dashboard-domain`            | Tables Agent-DB (bump de schéma), RPCs + événements `board.*`, outil `dashboard`, args pin/name/manifest `show_widget`, avis tier-1, reset-keeps-board                            | T2                               |
| T4  | `claude/dashboard-ui`                | Face du tableau + bande d'onglets + grille auto-compact fluide + dock de chat (gauche/droite/bas/masqué) + affordance d'épingle de transcription + face du tableau de la barre latérale + confirmation de réinitialisation | T3 (mock-first via fixtures de dev) |
| T5  | `claude/dashboard-capabilities`      | Magasin de subventions/UI + gel d'octets ; déplacer les widgets `html` sur l'hôte sandbox partagé ; outils d'hébergement (`openclaw.prompt.send/state.emit/data.read/cron.trigger`) ; CSP `net` ; shim de création | T3, T4                           |
| T7  | `claude/dashboard-mcp-apps`          | Type de contenu `mcp-app` : affordance d'épingle sur les vues d'application en ligne, stockage de descripteur, relance/actualisation de bail, subventions d'outil serveur durables (réutilise l'hôte MCP Apps expédié) | T3, T4                           |
| T6  | polish                               | E2E en direct sur une passerelle de brouillon (vraies clés), captures d'écran, corrections, réécriture `/web/dashboard` axée sur l'utilisateur, révision d'activation par défaut | tous                             |

Validation par règles de repo : vitest ciblé localement, portes complètes sur
Crabbox/Testbox, `$autoreview` avant chaque intégration, preuve en direct pour T6.
