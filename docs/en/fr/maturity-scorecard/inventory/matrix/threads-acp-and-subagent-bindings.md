---
title: "Matrix - Note de Maturité du Routage et de la Livraison des Conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Note de Maturité du Routage et de la Livraison des Conversations

## Résumé

Le support des threads Matrix et de la liaison des sous-agents est substantiel mais toujours risqué.
La source implémente les clés de route des threads, le contexte du démarreur de thread, les gestionnaires de liaison persistants,
la liaison des sessions enfants, le nettoyage du balayeur, les hooks de spawn ACP, et la résolution des cibles de livraison. La couverture est Beta car l'assurance qualité Matrix couvre les remplacements de threads
et les chemins de spawn des sous-agents, mais la qualité est Alpha car gitcrawl a un rapport ouvert indiquant que les réponses aux threads Matrix ont été envoyées comme des réponses normales et les commandes slash sont devenues silencieuses.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Routage et Livraison des Conversations`
- Fusionnée à partir de : `Routage et Accès des Conversations`, `Outils de Messagerie et de Salons`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Politique DM : politique DM, appairage, allowFrom, groupAllowFrom, listes blanches de salons, et vérifications d'accès en direct.
- Classification direct-room : classification direct-room et décisions de routage adjacentes à la réparation
- Sélection de route entrante sur les DM liés à l'expéditeur : sélection de route entrante sur les DM liés à l'expéditeur, liaisons de salons, et routes à portée de compte.
- Portes de mention : portes de mention, vérifications d'accès aux commandes slash, suppression des boucles de bot, et admission de contexte.
- Routage des réponses aux threads Matrix : routage des réponses aux threads Matrix, extraction de la racine/contexte du thread, et placement de session conscient des threads.
- Gestionnaires de routage des threads Matrix persistants : gestionnaires de liaison des threads Matrix persistants, liaison des sessions enfants, et suivi des activités.
- Hooks de spawn ACP/sous-agent : hooks de spawn ACP/sous-agent et cibles de livraison Matrix pour les sessions enfants
- Découverte d'actions de canal : découverte d'actions de canal, portes d'actions à portée de compte, et schémas d'outils
- Envoi/lecture/édition/suppression de messages : envoi/lecture/édition/suppression de messages, vote sur sondage, ajout/suppression/liste de réactions, épingles, et outils de salon connexes.
- Chargement des médias de profil : chargement des médias de profil à partir d'une URL ou d'un chemin local.
- Texte Matrix sortant : texte Matrix sortant, médias, médias chiffrés, sondage, saisie, reçu de lecture, et comportement de livraison.
- Métadonnées de présentation des messages : métadonnées de présentation des messages, métadonnées de mention Matrix, et comportement de livraison fragmenté.
- Gestion des défaillances de médias entrants : gestion des défaillances de téléchargement de médias entrants lorsqu'elles affectent les réponses sortantes.
- Envoi/lecture/édition/suppression de messages : envoi/lecture/édition/suppression de messages, vote sur sondage, ajout/suppression/liste de réactions, épingles, et outils de salon connexes
- Chargement des médias de profil : chargement des médias de profil à partir d'une URL ou d'un chemin local
- Texte Matrix sortant : texte Matrix sortant, médias, médias chiffrés, sondage, saisie, reçu de lecture, et comportement de livraison
- Métadonnées de présentation des messages : métadonnées de présentation des messages, métadonnées de mention Matrix, et comportement de livraison fragmenté
- Gestion des défaillances de médias entrants : gestion des défaillances de téléchargement de médias entrants lorsqu'elles affectent les réponses sortantes

## Fonctionnalités

- Routage et Livraison des Conversations : portée des preuves pour le Routage et la Livraison des Conversations.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (72%)`
- Signaux positifs :
  - Les docs couvrent les threads Matrix, `sessionScope`, `threadReplies`, `/focus`,
    `/acp spawn`, et la configuration de liaison des threads.
  - La source a des clés de route de thread sensibles à la casse, extraction de la racine du thread,
    persistance de l'état de liaison, adaptateurs de liaison enfants, logique unbind/sweeper,
    hooks de spawn des sous-agents, et récupération de route de session sortante.
  - Les tests unitaires couvrent le routage des threads, le contexte du démarreur de thread, l'API de liaison des threads publics, les liaisons persistantes, le spawn des sous-agents, la résolution des cibles de livraison, et la récupération de la route de session.
  - L'assurance qualité Matrix couvre les remplacements de threads de salon et DM ainsi que les scénarios de spawn de threads des sous-agents.
- Signaux négatifs :
  - Le comportement des threads est complexe car il traverse les identifiants d'événements Matrix, les clés de session OpenClaw, le cycle de vie des sessions enfants ACP, et le placement des réponses sortantes.
  - Les preuves d'archive actives montrent des régressions de threads visibles par l'utilisateur.
- Lacunes d'intégration :
  - Ajouter une voie critique de version Matrix thread qui couvre les threads de salon de haut niveau, les remplacements de threads DM, le spawn des sous-agents enfants, la livraison finale, et le redémarrage.
  - Ajouter des preuves en direct pour la gestion des commandes slash à l'intérieur des threads Matrix.
  - Ajouter des liens d'artefacts des défaillances d'assurance qualité aux identifiants d'événements racine/réponse Matrix.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux frontières partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct, ou les preuves du flux d'exécution réel sur le composant. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "matrix thread replies acp subagent binding"` a retourné la PR ouverte #69824 pour la consolidation du runtime ACP.
  - La requête large `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné le problème ouvert #87307 pour les réponses aux threads Matrix envoyées comme des réponses normales et `/status` plus `/model` silencieux, la PR ouverte #71738 pour l'historique des threads Matrix et le placement des réponses, la PR ouverte #85112 pour le contournement des mentions dans les threads liés, et le problème ouvert #78249 pour le comportement manquant d'injection/chemin/shell des compétences Matrix comparé à WebChat.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix thread replies ACP subagent binding"` n'a retourné aucun résultat.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné une discussion générale sur les versions et les scorecards Matrix.
- Bonnes qualités :
  - Les identifiants de thread préservent la casse de l'identifiant d'événement Matrix dans les clés de route.
  - La persistance de la liaison est à portée de compte et sensible au répertoire d'état.
  - Le code de liaison enfant distingue le placement de salon de haut niveau du placement de thread existant.
  - Les hooks des sous-agents échouent fermés lorsque les liaisons de threads Matrix ou les sessions de spawn ne sont pas disponibles.
- Mauvaises qualités :
  - Le rapport ouvert actif de réponse aux threads et de commande silencieuse maintient ceci à Alpha.
  - La correction des threads dépend des métadonnées de session actuelles, des métadonnées de relation Matrix, de la disponibilité de l'événement racine du salon, et du cycle de vie de la session enfant.
  - Le comportement ACP/sous-agent est toujours lié à la consolidation du runtime plus large.
- Exclu de la qualité :
  - Je n'ai pas augmenté ou diminué la Qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct, ou d'exécution réelle.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux frontières partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct, ou d'exécution réelle comme entrée de notation.

## Score de Complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour le Routage et la Livraison des Conversations.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Fermer ou retester #87307 avant d'augmenter la Qualité au-dessus d'Alpha.
- Ajouter des tests de commande en direct à l'intérieur des threads Matrix liés.
- Préserver la casse de l'identifiant d'événement Matrix et les diagnostics d'événement racine dans les artefacts d'échec des threads.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:502` documente
  les fils de discussion Matrix.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:541` documente
  le comportement de `/focus`.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:555` documente
  `/acp spawn` et la configuration de liaison des fils de discussion.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/thread-bindings.ts:44`
  définit les chemins d'état de liaison et le comportement de chargement/persistance.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/thread-bindings.ts:198`
  gère la mise en file d'attente du chargement et de la persistance des liaisons.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/thread-bindings.ts:410`
  crée les liaisons de fils de discussion Matrix actuels/enfants.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/thread-bindings.ts:497`
  gère le débindage et le nettoyage du balayeur.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/threads.ts:11`
  préserve les clés de session de fil de discussion Matrix sensibles à la casse.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/thread-context.ts:50`
  résout et met en cache le contexte racine du fil de discussion.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/thread-binding-api.ts:4`
  expose le placement de liaison de fil de discussion Matrix et la résolution de conversation.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/subagent-hooks.ts:105`
  lie les sous-agents générés aux fils de discussion Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/session-route.ts:74`
  résout les routes sortantes à partir des métadonnées de session Matrix.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:2643`
  exécute les scénarios de remplacement de fil de discussion de salle contre la salle principale.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:2690`
  exécute la génération de fil de discussion de sous-agent contre un fil de discussion enfant.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:2807`
  échoue la génération de fil de discussion de sous-agent lorsque Matrix manque de crochets de sous-agent.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:2841`
  échoue la génération de fil de discussion de sous-agent sur les erreurs d'outil surfacées.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4510`
  utilise les scénarios de remplacement de fil de discussion DM contre la salle DM provisionnée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/threads.test.ts:5`
  couvre les sessions plates lorsque les réponses de fil de discussion sont désactivées.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/threads.test.ts:18`
  couvre le routage racine de fil de discussion entrant.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/thread-context.test.ts:40`
  résout et met en cache le contexte du démarreur de fil de discussion.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/thread-binding-api.test.ts:7`
  couvre le comportement de l'API publique de liaison de fil de discussion Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/thread-bindings.test.ts:189`
  crée des liaisons de fil de discussion Matrix enfants à partir du contexte de salle de niveau supérieur.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/thread-bindings.test.ts:691`
  vide la persistance tactile en attente à l'arrêt.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/subagent-hooks.test.ts:208`
  permet la génération de sous-agent lié au fil de discussion par défaut.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/subagent-hooks.test.ts:631`
  résout la cible de livraison enfant avec l'identifiant du fil de discussion.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/session-route.test.ts:277`
  récupère les routes de fil de discussion Matrix et préserve la casse de l'identifiant d'événement.

### Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "matrix thread replies acp subagent binding"`
  a retourné la PR ouverte #69824.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné #87307,
  #71738, #85112, #78249, et d'autres résultats adjacents aux fils de discussion Matrix.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix thread replies ACP subagent binding"`
  n'a retourné aucun résultat.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"`
  a retourné des discussions générales sur les versions et les scorecards Matrix.
