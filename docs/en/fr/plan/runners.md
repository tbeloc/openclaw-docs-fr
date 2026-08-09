---
summary: Un modèle de placement unique pour les sessions — la passerelle, les appareils appairés et les boîtes cloud sont tous des runners ; les clients se connectent aux sessions, jamais aux runners.
title: Plan des runners
read_when:
  - Concevoir ou examiner où les sessions s'exécutent (passerelle, appareil, cloud)
  - Modifier le sélecteur Where, l'appairage d'appareils ou les surfaces de dispatch des workers
  - Nommer quoi que ce soit autour des sessions, des appareils ou du placement
---

## Statut

Proposition, révision 1. Implémentation en cours (build autonome démarré
2026-08-08 ; cette section suit le statut en direct — mettez-la à jour dans chaque PR qui
avance une étape).

| #   | Étape                                                | Statut      | PRs |
| --- | ---------------------------------------------------- | ----------- | --- |
| 0   | Ce plan                                              | en révision | —   |
| 1a  | Nommage : session copy revert                        | non démarré | —   |
| 1b  | Nommage : consolidation des appareils               | non démarré | —   |
| 1c  | Nettoyage : fusion node-pairing → device-pairing    | non démarré | —   |
| 2   | `openclaw resume` + web Continue in terminal        | non démarré | —   |
| 3   | Appairage one-paste `oc-pair://`                    | non démarré | —   |
| 4   | Picker + enrichment + modèle de lecture des projets | non démarré | —   |
| 5   | Device runners                                       | non démarré | —   |
| 6   | Mouvements stop-and-continue                         | non démarré | —   |
| 7   | Suppressions (ssh sandbox, openshell, clones exec-host) | non démarré | —   |

Historique de la proposition : direction convenue 2026-08-08 après une
enquête basée sur le code (trois lectures approfondies des piles worker, exec et node),
une enquête industrielle (Amp runners/orbs, Cursor 3 location picker,
Claude Code teleport, Codex cloud, VS Code tunnels, Tailscale auth keys), et
trois révisions adversariales dont les verdicts de rejet sont intégrés ci-dessous comme des
non-objectifs explicites. S'appuie directement sur l'architecture cloud-workers expédiée
(`docs/plan/cloud-workers.md`, `docs/gateway/cloud-workers.md`) ; elle ne la
remplace pas.

## Problème

OpenClaw a trois réponses déconnectées à « où le travail s'exécute-t-il » :

- **Les nœuds** reçoivent uniquement les appels `exec host=node` transférés ; la boucle de tour ne
  quitte jamais la passerelle. Un Mac Studio toujours actif d'un utilisateur est moins capable en tant que
  hôte de session qu'un bail AWS jetable.
- **Les cloud workers** hébergent des sessions complètes, avec une machine d'état de placement
  durable, mais uniquement contre les baux de fournisseur éphémères.
- **Le backend ssh sandbox** est un troisième chemin d'exécution à distance (identifiants SSH tenus par la passerelle,
  remoting par outil) qui duplique la forme que les cloud workers ont remplacée.

L'interface utilisateur reflète la fragmentation : le placement est choisi une fois dans le
popover de nouvelle session à partir d'une liste plate mélangeant trois ontologies (passerelle, nœuds exec, profils cloud),
puis devient invisible et immuable. La configuration du placement est dispersée
dans `tools.exec.*`, `agents.entries.*.tools.exec.node`,
`agents.defaults.sandbox.*`, `gateway.nodes.*`, et `cloudWorkers.profiles`.
Le vocabulaire a dérivé : l'interface Control dit « thread » (renommage de copie juillet 2026, PRs
110933/110973) tandis que l'interface CLI, le protocole, les magasins et les docs disent « session » ;
le matériel appairé est « nodes » dans les routes/i18n et « devices » dans les chemins/étiquettes.

## Modèle et vocabulaire

```
Session   détenue par la passerelle : transcription, identité, placement, worktree géré.
          Les clients (web, TUI, app macOS, canaux) se connectent aux sessions,
          jamais aux runners. Un seul nom, partout : session.
Runner    n'importe quoi qui peut héberger la boucle de tour d'une session :
            - la passerelle elle-même (le runner que vous obtenez gratuitement)
            - un appareil appairé (via un fournisseur de worker soutenu par un nœud ; voir ci-dessous)
            - une boîte cloud (fournisseur de worker crabbox existant)
Isolation une propriété DU runner, pas un lieu :
            boîte cloud      -> la machine est la limite
            passerelle/appareil -> aucune | docker | podman (sandbox existant)
Device    matériel appairé (« nœuds » d'aujourd'hui). Les appareils contribuent
          des capacités (caméra, canvas, exec) en tant que périphériques ; un appareil
          devient un runner uniquement via le chemin d'admission du worker.
Project   identité du repo : remote.origin.url normalisée, avec l'empreinte digitale du repo
          16 caractères existante comme secours sans remote. Dérivée,
          jamais enregistrée.
Checkout  projet × runner = { runnerId, path } — où un projet
          existe physiquement. Les runners cloud n'en ont pas ; ils matérialisent
          un checkout frais par session.
Folder    l'échappatoire non-git : un chemin simple sur un runner
          (flux de navigation d'aujourd'hui, inchangé).
Turn      une tentative de travail prompt-to-response à l'intérieur d'une session
          (correspond à ACP et au protocole worker).
```

Rulings de nommage (décidé par l'opérateur 2026-08-08) :

- **session** est le seul nom de produit pour une conversation. La copie Control-UI
  « thread » est annulée (i18n + littéraux de test ; les identifiants techniques n'ont jamais
  changé). Industrie : 9–2 pour session parmi les produits d'agent ; ACP dit session ;
  « thread » entre en collision avec les concepts de transport de sous-thread Discord/Slack/Telegram.
- **devices** est le mot orienté utilisateur pour le matériel appairé ; « nodes » reste
  vocabulaire de protocole/interne uniquement. La dette route/i18n (`nodes` route id,
  `/settings/devices` path, `nodes.*` clés i18n) se consolide sur devices.
- Les nouvelles ergonomies CLI se déploient en tant que **verbes** (`openclaw resume`),
  jamais une deuxième commande de nom à côté de `openclaw sessions`.
- « runner » est un concept interne/docs ; la copie UI dit « Runs on … ».

VISION.md gagne un paragraphe : la passerelle est le coordinateur et le runner par défaut ;
chaque autre machine — la vôtre ou louée — peut être un runner ; les clients
se connectent aux sessions, donc où une session s'exécute ne change jamais comment vous lui parlez.

## Ce que les révisions adversariales ont tué (maintenant des non-objectifs)

- **Pas de registre Places.** `environments.list`
  (`src/gateway/server-methods/environments.ts:143-157`) retourne déjà le
  modèle de lecture fusionné : entrée de passerelle, catalogue de nœuds (appairés + présence en direct),
  environnements de worker, profils cloud. Un registre persisté dupliquerait
  les faits de présence ; un RPC renommé est un deuxième chemin. Nous enrichissons `EnvironmentSummary`
  de manière additive à la place.
- **Pas de boucles de tour sur le rôle de nœud.** Le protocole de nœud a déjà été rejeté
  comme transport de boucle (cloud-workers.md §4) : un nœud connecté peut émettre
  des événements de nœud arbitraires, donc son plafond de capacité n'est pas une limite d'entrée.
  L'entrée du worker reste une liste d'autorisation fermée à trois méthodes
  (`packages/gateway-protocol/src/schema/worker-admission.ts:32-34`) avec
  des identifiants par dispatch frappés et admission de hash de bundle exact
  (`src/gateway/worker-environments/admission.ts:80-104`). Les appareils deviennent
  des runners uniquement en exécutant `openclaw worker` sous cette admission.
- **Pas de dispatch dans un checkout en direct.** La synchronisation de l'espace de travail nécessite la propriété exclusive
  du répertoire distant (essuyé à chaque synchronisation,
  `workspace-sync-setup-script.ts:29`) ; reconcile traite la divergence du
  manifeste de base comme une sortie de worker. Les device runners utilisent le même répertoire privé
  par session sous `$HOME/.openclaw-worker/` que le fournisseur static-ssh qa-lab
  prouve aujourd'hui.
- **Pas de pliage de `exec host=node`.** Le routage exec par appel est ~5k LOC de
  machinerie d'approbation fail-closed à quatre couches (vérifications TOCTOU de passerelle, plancher de politique de nœud,
  liaison de hash `systemRunPlan` revalidée sur le nœud,
  réévaluation locale du nœud). Il sert un produit différent (une commande dans un
  domaine de politique différent) et reste inchangé.
- **Pas de ligne sandbox-as-a-place.** Sandbox est une configuration d'isolation par agent
  sans surface de remplacement par session ; une ligne de sélecteur ferait silencieusement rien pour
  les agents non configurés.
- **Pas de verbes de mobilité faux.** `sessions.dispatch` accepte les placements `local|reclaimed`
  et les profils cloud uniquement (`sessions-dispatch.ts:166-176`) ; il n'y a pas de pause
  et pas de déplacement machine-à-machine. L'interface utilisateur affiche uniquement ce que le
  backend fait : affichage + réclamation maintenant ; déplacement-comme-stop-and-continue après le déploiement des device runners.
- **Pas de pré-approbation exec dans les liens d'appairage.** Le flux one-paste peut
  pré-approuver les portées de présence uniquement ; `system.run` et la synchronisation de dossier passent toujours par la
  porte d'approbation en attente existante ou de vérification SSH
  (`src/gateway/node-pairing-ssh-verify.ts`).
- **Pas de migration en direct, pas de fédération multi-passerelle, pas de téléphones en tant que runners.**

## Composants

### 1. Ergonomie de continuation de session (indépendant, livré en premier)

Déjà vrai par construction : la transcription et le placement vivent sur la
passerelle, l'inférence provient de la passerelle dans chaque placement, et
l'interface TUI est un client de passerelle complet (`openclaw tui --session <key>`, sélecteur Ctrl+P,
reprise de dernière session — `src/tui/tui-last-session.ts`). Démarrez une session sur le
web s'exécutant dans le cloud ; l'interface TUI s'attache et dirige la route vers le worker.

Le delta est uniquement ergonomique :

- `openclaw resume [query]` — correspondance floue des sessions récentes entre agents par
  nom/clé ; aucune requête n'ouvre un sélecteur ; se résout en `tui --session <key>`.
- Bouton « Continuer dans le terminal » de l'interface web sur les lignes de session : affiche la commande exacte
  (`openclaw resume <key>`), reflétant l'affordance de reprise de terminal que
  les catalogues de sessions Codex/Claude ont déjà.
- Aucune nouvelle surface de protocole ; `sessions.list` porte déjà ce dont le résolveur
  a besoin.

### 2. Appairage d'appareil en un seul collage (indépendant)

Réutilisez le flux de code de configuration livré : `PairingSetupPayload = { url, urls?,
bootstrapToken }` blob base64url (`src/pairing/setup-code.ts:40-44,406-410`),
jeton bootstrap à usage unique de 10 minutes, `bootstrapProfile: "node"`
(`src/shared/device-bootstrap-profile.ts:61-94`), frappe RPC
`device.pair.setupCode` (`src/gateway/server-methods/device-pair-setup.ts`).

Lacunes à combler :

- Wrapper de schéma `oc-pair://<setupCode>` (charge utile inchangée).
- Chemin de remboursement `openclaw node run --pair <code|url>` : décoder le blob, configurer
  l'hôte/port/jeton, se connecter (aujourd'hui seuls les drapeaux `--host/--port/--tls-fingerprint`
  existent, `src/node-host/runner.ts:27-37`).
- Ajouter l'empreinte TLS à `PairingSetupPayload` (l'hôte de nœud accepte déjà
  un code PIN ; le blob ne peut pas le porter).
- Exposer le profil bootstrap `node` dans la boîte de dialogue d'appairage de l'interface de contrôle
  (RPC uniquement aujourd'hui, `ui/src/lib/device-pair-setup.ts`).
- Division de clé de style Tailscale, énoncée dans la documentation : le jeton d'appairage est de courte durée
  et à usage unique ; la credential d'appareil résultante est de longue durée ; révoquer l'une
  ne révoque jamais l'autre.

L'escalade d'exécution/portée est inchangée : la première demande `system.run` atterrit en
approbation en attente ou approuve automatiquement via vérification SSH.

### 3. Exécuteurs d'appareil (le cœur)

Un exécuteur d'appareil est la pile de worker existante pointée vers une machine persistante.
Preuve que la pile est prête :

- Le contrat de fournisseur est minuscule et générique SSH
  (`src/plugins/capability-provider.types.ts:97-114`) : `provision → {leaseId,
ssh}`, `inspect`, `destroy`. Le fournisseur SSH statique du laboratoire QA
  (`extensions/qa-lab/src/static-ssh-worker-provider.ts:70-91`) enveloppe déjà
  un hôte persistant avec une destruction sans opération, et le travail de synchronisation/réconciliation fonctionne sans modification
  car l'espace de travail distant est un miroir privé par session.
- L'admission, la machine d'état de placement, les magasins SQLite, la transcription CAS,
  le proxy d'inférence, et le runtime `openclaw worker` n'ont essentiellement besoin d'aucun
  changement ; l'admission est basée sur les credentials, non sur le transport.
- La couture est `WorkerTunnelHandle`
  (`src/gateway/worker-environments/tunnel-contract.ts:74`, 85 lignes) :
  exécution de commande d'espace de travail + synchronisation + arrêt derrière une poignée, actuellement
  SSH uniquement (`worker-turn-launcher.ts:337-344`, `workspace-sync-scripts.ts`).

Éléments de travail :

- **Fournisseur de worker `device`** : `provision` mappe un profil à un appareil
  appairé et connecté existant ; `destroy` libère le bail logique. Configuration :
  `cloudWorkers.profiles.<id> = { provider: "device", settings: { device:
"<id-or-name>" } }` (bikeshed : renommer le bloc de configuration en
  `runners.profiles` avec une migration doctor — décider à la révision).
- **Variante de tunnel** : soit (a) SSH vers l'appareil comme n'importe quel worker (l'appareil
  exécute sshd ; le plus simple, réutilise tout), soit (b) une implémentation `WorkerTunnelHandle`
  qui multiplex les commandes d'espace de travail et le socket worker
  sur la connexion de passerelle existante de l'appareil. Livrez (a) en premier ; (b) est une
  optimisation décidée à la révision.
- **Runtime épinglé avec consentement** : la passerelle pousse son bundle
  avec hash de contenu (bootstrap existant, `bootstrap.ts:26-104`) dans
  `$HOME/.openclaw-worker/` sur l'appareil. L'installation d'un runtime sur une machine personnelle
  nécessite une approbation d'opérateur unique par appareil, affichée dans
  l'interface d'appairage/approbation. L'admission de version exacte reste ; le décalage de version est résolu
  en réinstallant le bundle, jamais en relâchant la vérification.
- **Sémantique hors ligne/drainage** (le seul vrai nouveau sous-système) : les machines personnelles
  s'endorment et ne peuvent pas être détruites. Nouvelle gestion de placement pour
  `runner-offline` : la perte de battement marque le placement avec une raison enregistrée,
  visible par l'opérateur (Doctrine Produit : aucun non-résultat silencieux) ; les résultats
  intermédiaires sont préservés (machinerie de clôture existante) ; la session offre
  « continuer sur la passerelle » (récupérer) ou « attendre l'appareil ». Réutilisez le
  sous-système de nudge de réveil (`src/gateway/node-wake-state.ts`) où l'appareil a un canal de réveil.
- **Isolation sur les exécuteurs d'appareil** : worker-in-docker optionnel sur l'appareil,
  même axe de bac à sable que les sessions locales de passerelle. Les exécuteurs cloud conservent
  la permission complète dans la boîte (la machine est la limite).

### 3b. Projets (modèle de lecture dérivé)

OpenClaw calcule déjà l'identité du projet deux fois sans la nommer : le
service worktree dérive `originUrl` + une empreinte de repo de 16 caractères
(`src/agents/worktrees/service.ts:199-205`), et le catalogue de sessions groupe
les lignes Codex/Claude par dossier de projet, pliant `.claude/worktrees/<name>` dans
son repo d'origine. Ce composant le promeut à un modèle de lecture de première classe —
dérivé, jamais enregistré, même motif que `environments.list` :

- **Modèle de lecture `projects.list`** (calculé à la demande, aucun nouveau magasin) : grouper
  les checkouts connus par empreinte de repo → `{ name, originUrl, checkouts:
[{runnerId, path}], lastUsedAt }`. Sources : lignes de session
  (`execCwd`/`execNode`), le registre de worktree géré, et
  les répertoires de travail annoncés par l'appareil (ci-dessous). La « nature GitHub » est juste l'hôte originUrl
  affiché comme sous-titre ; aucune intégration de forge requise pour le modéliser.
- **Annonce de checkout d'appareil** : la passerelle ne peut pas grouper
  les checkouts entre exécuteurs aujourd'hui car elle n'apprend jamais l'origine d'un checkout d'appareil. L'activation
  de l'exécuteur d'appareil (composant 3) ajoute des paires `{path, originUrl}` à
  la poignée de main de l'appareil — l'idée d'hôte Amp + répertoire de travail atterrissant dans la bonne couture.
  Petit, additif, et envoyé uniquement pour les chemins que l'opérateur a activés.
- **Flux du sélecteur** : projet en premier (puce ⌃J), puis la puce Where affine à
  « où ce projet existe-t-il » — chemins de checkout comme sous-titres de ligne ; les exécuteurs
  sans checkout sont listés honnêtement (« pas de checkout · clones depuis l'origine
  à la première session ») ; le cloud est toujours éligible (clone frais). Les récents se groupent
  par projet au lieu de dédupliquer les paires brutes `(folder, node)`
  (`ui/src/pages/new-session/recent-places.ts`). « Pas de projet » conserve
  le navigateur de dossiers par exécuteur existant comme échappatoire.
- **L'intégration de forge est une phase ultérieure, séparable** : listes de repos depuis GitHub,
  cloner un repo que vous n'avez jamais touché, statut PR sur les lignes de session. Le modèle
  dérivé n'en a besoin d'aucun ; la création de projet de style enregistrement (le
  motif de produit cloud uniquement) est explicitement rejetée — les projets apparaissent
  car vous avez travaillé dessus.

### 4. Convergence de l'interface utilisateur

Règle de conception (décidée par l'opérateur, 2026-08-08) : **l'état normal est silencieux ; seules
les exceptions parlent.** Pas de points en ligne, pas d'étiquettes persistant/jetable/périphérique,
pas de pilules de statut — être listé dans le sélecteur signifie déjà utilisable,
et l'opérateur sait ce que sont ses propres appareils. Le texte de statut n'apparaît que pour
les exceptions (« hors ligne · 2h », la bannière runner-offline) ou les faits que
l'opérateur ne peut pas déduire (temps de provisionnement, « s'exécute dans docker »). Les puces de capacité restent : ce sont
des faits structurés, non du statut. Le placement sur une session en cours d'exécution est du texte discret (« sur aws »),
non un widget badgé — le spinner d'activité porte déjà la vivacité.

- **Enrichir `EnvironmentSummary` de manière additive** (protocole, pas de migration) :
  `trust: "persistent" | "disposable"`, `sessionHost: boolean`, `platform`,
  et pour les profils une étiquette `class` fournie par le fournisseur. Aucun champ de tarification jusqu'à
  ce qu'un fournisseur en fournisse réellement.
- **Sélecteur Where regroupé** (`ui/src/pages/new-session/place-picker.ts`) :
  sections « Cette passerelle » / « Vos appareils » (appareils capables de session, connectés
  uniquement — les téléphones et appareils hors ligne restent cachés par gating) / « Cloud ».
  Le dossier et la destination restent orthogonaux. Copie : « S'exécute sur {place} ».
- **Puce de placement** sur l'en-tête de session : affiche le placement actuel et
  l'état ; le menu offre exactement la récupération (« Ramener à la maison ») pour les placements cloud
  aujourd'hui, plus les mouvements stop-and-continue une fois que les exécuteurs d'appareil sont livrés. Réutilise
  l'abonnement de placement que les badges de la barre latérale consomment déjà.
- **Page Appareils** : plier les sessions en direct par appareil dans la surface existante
  `ui/src/pages/nodes/` (renommée en appareils de bout en bout). Aucun nouvel élément de navigation de haut niveau ;
  le pied du sélecteur « Connecter un appareil… » renvoie ici.
- **Vague de nommage** (un PR, tôt, avant que la nouvelle copie ne soit déployée) : revenir fil → session dans la copie de l'interface de contrôle ; consolider nœuds → appareils dans l'id de route, les clés i18n,
  et les étiquettes. Alias de route selon le mécanisme d'alias existant de l'interface utilisateur.

### 5. Suppressions et déduplications (chacune gated sur son remplacement)

| Cible                                                                                                                                                                                                    | Taille     | Gate                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------ |
| backend sandbox SSH + pont remote-fs (`src/agents/sandbox/ssh*.ts`)                                                                                                                                     | ~2,35k LOC | les exécuteurs d'appareil couvrent le cas « outils sur mon serveur »                 |
| chevauchement openshell (`extensions/openshell`)                                                                                                                                                        | ~3,4k LOC  | vérifier l'utilisation réelle en premier ; même forme de transport SSH                  |
| clones structurels exec-host (`bash-tools.exec-host-gateway.ts` vs `exec-host-node*.ts` : allowlist eval, auto-review, timeout-fallback, follow-up delivery ; node host re-clone l'analyse une troisième fois) | ~3k de ~5k | extraire une machine d'état d'approbation partagée ; la liaison de plan du nœud reste |
| façade `node-pairing.ts` sur `device-pairing.ts` + shims de migration                                                                                                                                   | moyen      | terminer la fusion ; un vocabulaire                                  |
| observateurs de placement UI (`cloud-recovery-state.ts` + boucles de réconciliation de la page de sessions)                                                                                            | moyen      | un contrôleur de surveillance de placement                                  |

Le LOC de production net sur tout le plan est ciblé négatif : les composants 1–2
sont de petits ajouts ; le composant 3 est principalement un plugin de fournisseur + une variante de tunnel
contre une machinerie réutilisée ; le composant 5 supprime plus qu'il n'ajoute.

## Travaux antérieurs (ce que nous copions, ce que nous ignorons)

- **Amp agents-anywhere** : runners comme entrées de sélecteur de première classe ; identité = hôte + répertoire de travail avec nom épinglé optionnel → nous utilisons l'ID d'appareil et annonçons les répertoires de travail. Amp laisse le comportement du runner hors ligne non documenté ; notre état enregistré `runner-offline` est l'amélioration délibérée.
- **Clés d'authentification Tailscale** : clé d'appairage à usage unique de courte durée vs identifiant d'appareil de longue durée, révocation séparée → copiée dans le composant 2.
- **Claude Code teleport** : la continuation re-matérialise l'état car leur session cloud existe ailleurs ; les sessions détenues par la passerelle d'OpenClaw rendent la continuation en pièce jointe uniquement — plus simple, pas de mouvement d'état. Leur sémantique fork-not-move informe notre cadrage stop-and-continue.
- **Sélecteur de localisation Cursor 3** : Local/Worktree/Cloud/SSH dans un seul menu déroulant valide l'UX du sélecteur unique ; leur transfert cloud en direct expédié bugué — nous ne tentons pas les mouvements en direct.
- **devcontainer.json** : si/quand la configuration d'environnement détenue par le repo arrive pour les profils de worker, adopter la spécification plutôt que d'inventer un format (l'environment.json propriétaire de Cursor a accumulé de la dette ; Gitpod a migré vers la spécification).

## Jalons

Série de PR indépendamment fusionnables, à peu près dans l'ordre ; 1–3 peuvent s'entrelacer.

1. **Vague de nommage** : revert de copie de session + consolidation des appareils (UI/i18n/tests uniquement ; aucune modification de protocole ou CLI).
2. **Ergonomie de continuation** : `openclaw resume`, web "Continue in terminal".
3. **Appairage** : `oc-pair://`, `node run --pair`, épingle TLS dans la charge utile, profil de nœud dans l'UI d'appairage.
4. **Sélecteur + enrichissement** : champs `EnvironmentSummary` additifs, regroupement du sélecteur Where, puce de placement (affichage + réclamation), modèle de lecture `projects.list` + flux de sélecteur orienté projet (checkouts côté passerelle uniquement jusqu'à ce que 5 ajoute l'annonce d'appareil).
5. **Runners d'appareil** : fournisseur de worker d'appareil (transport SSH en premier), installation de bundle épinglée avec consentement par appareil, annonce de checkout (`{path, originUrl}` dans la poignée de main d'activation), sémantique de placement `runner-offline` avec raisons enregistrées, isolation optionnelle worker-in-docker.
   Les tests d'injection de fautes (appareil en veille au milieu du tour, redémarrage de la passerelle avec appareil hors ligne, expiration des identifiants) ferment la sortie — même barre que les workers cloud définissent.
6. **Mouvements stop-and-continue** (verbe de puce "Move to…") : drain + réclamation + re-dispatch vers un autre runner, réutilisant la barrière de migration.
7. **Suppressions** : backend sandbox ssh, chevauchement openshell, extraction de clone exec-host, fusion appairage nœud/appareil — chacun dans sa propre PR avec preuve que le remplacement le couvre.

## Questions ouvertes

- Nommage de la configuration : conserver `cloudWorkers.profiles` (compat) ou migrer vers `runners.profiles` via doctor au jalon 5 ?
- Transport du runner d'appareil (a) sshd vs (b) connexion de passerelle multiplexée : expédier (a) en premier ; (b) vaut-il la surface de protocole du tout ?
- `openclaw resume` devrait-il également démarrer la passerelle/TUI en mode local quand aucune passerelle n'est accessible, ou échouer avec des conseils ?
- Contrat de configuration détenue par le repo (devcontainer.json) pour les profils de worker : ce plan ou un suivi ?
- Intégration Forge (listes de repos GitHub, clone-anywhere, statut PR sur les lignes de session) : explicitement hors de ce plan ; suivi une fois que le modèle de projet dérivé a une utilisation.
- Collision de nommage de projet : `openclaw fleet` et les docs multi-locataires utilisent "project" vaguement par endroits — balayer pendant la vague de nommage pour garder "project" exclusivement pour l'identité du repo.
