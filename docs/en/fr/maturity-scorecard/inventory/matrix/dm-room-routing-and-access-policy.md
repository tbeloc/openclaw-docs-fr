---
title: "Matrix - Access and Identity Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Access and Identity Maturity Note

## Summary

Matrix DM et le routage des salons sont riches en fonctionnalités : ils prennent en charge les listes blanches, les restrictions d'expéditeur de groupe, l'appairage, la classification des salons directs, la promotion des invitations récentes, la politique de boucle de bot, les portes de mention, l'état d'accès, le rechargement de liste blanche en direct et la sélection de route de session. La couverture est Beta car il existe de nombreuses routes unitaires et QA, mais c'est une large surface de politique avec état. La qualité est Beta car gitcrawl a des rapports ouverts pour l'analyse des mentions et la livraison des messages aux sessions.

## Normalization

Catégorie active après la normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Access and Identity`
- Fusionnée à partir de : `Conversation Routing and Access`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Category Scope

Inclus dans cette catégorie :

- Politique DM : politique DM, appairage, allowFrom, groupAllowFrom, listes blanches de salons et vérifications d'accès en direct.
- Classification des salons directs : classification des salons directs et décisions de routage adjacentes à la réparation
- Sélection de route entrante entre les DM liés à l'expéditeur : sélection de route entrante entre les DM liés à l'expéditeur, liaisons de salons et routes à portée de compte.
- Portes de mention : portes de mention, vérifications d'accès aux commandes slash, suppression de boucle de bot et admission de contexte.
- Routage des réponses de fil Matrix : routage des réponses de fil Matrix, extraction de racine/contexte de fil et placement de session conscient du fil.
- Gestionnaires de routage de fil Matrix persistants : gestionnaires de liaison de fil Matrix persistants, liaison de session enfant et suivi d'activité.
- Crochets de génération ACP/subagent : crochets de génération ACP/subagent et cibles de livraison Matrix pour les sessions enfants

## Features

- Politique DM : politique DM, appairage, allowFrom, groupAllowFrom, listes blanches de salons et vérifications d'accès en direct.
- Classification des salons directs : classification des salons directs et décisions de routage adjacentes à la réparation
- Sélection de route entrante entre les DM liés à l'expéditeur : sélection de route entrante entre les DM liés à l'expéditeur, liaisons de salons et routes à portée de compte.
- Portes de mention : portes de mention, vérifications d'accès aux commandes slash, suppression de boucle de bot et admission de contexte.
- Routage des réponses de fil Matrix : routage des réponses de fil Matrix, extraction de racine/contexte de fil et placement de session conscient du fil.
- Gestionnaires de routage de fil Matrix persistants : gestionnaires de liaison de fil Matrix persistants, liaison de session enfant et suivi d'activité.
- Crochets de génération ACP/subagent : crochets de génération ACP/subagent et cibles de livraison Matrix pour les sessions enfants

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Beta (74%)`
- Signaux positifs :
  - La documentation couvre la politique DM, l'appairage, la réparation de salon, les paramètres de groupe, l'accès aux commandes, la visibilité du contexte et la grammaire cible.
  - La source a une résolution de route entrante explicite, une normalisation de liste blanche, une classification de salon direct, une résolution de mention, un état d'accès, un historique de salon et des portes de gestionnaire.
  - Les tests unitaires couvrent les listes blanches, la classification des salons directs, la précédence des routes, les sessions DM par salon, le rechargement de liste blanche en direct, les portes de mention, l'appairage, les boucles de bot, le backlog de démarrage à froid, la déduplication durable et l'état d'accès.
  - Les scénarios QA couvrent les salons DM, les salons secondaires, le comportement allowBots, le rechargement de liste blanche à chaud, les réponses obsolètes, le blocage des commandes de contrôle et les avis DM partagés.
- Signaux négatifs :
  - La matrice de politique a de nombreuses combinaisons entre les comptes, les salons, les expéditeurs, les mentions, les fils et les heuristiques de salon direct.
  - Les rapports d'archive montrent que des défaillances de routage visibles par l'utilisateur se produisent toujours.
- Lacunes d'intégration :
  - Ajouter une matrice de routage en direct qui énumère le type de salon, l'ID de compte, le mode de liste blanche, l'état de mention, les métadonnées de salon direct et la cible de route.
  - Ajouter des preuves de version pour la politique d'accès au groupe Matrix et DM après le rechargement de configuration à chaud.
  - Ajouter un mappage direct des valeurs de politique DM documentées aux ID de scénario QA.

Étiquettes de couverture :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Quality Score

- Score: `Beta (72%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "matrix dm room allowlist pairing mention"` n'a retourné aucun résultat.
  - La requête large `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné le problème ouvert #83142 pour l'analyse des mentions du nom d'affichage, le problème ouvert #68188 pour les messages non livrés à une session d'agent, la PR ouverte #85172 pour la gestion `is_direct: false` et la PR ouverte #73455 pour les contrôles de participation/fraîcheur.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix DM room allowlist pairing mention"` n'a retourné aucun résultat.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions de version mentionnant le comportement de mention Matrix.
- Bonnes qualités :
  - La logique du gestionnaire a des portes explicites avant la distribution, y compris le type d'événement, l'identité de l'expéditeur, la politique de boucle de bot, la politique de salon/DM, les mentions, l'accès aux commandes, l'appairage et la résolution de route.
  - La sélection de route préserve la portée du compte et peut prioriser les liaisons de conversation d'exécution, les liaisons de salon configurées, les routes d'expéditeur DM et la portée de session DM par salon.
  - La classification des salons directs a plusieurs vetos et chemins d'invalidation du cache, réduisant la confiance accidentelle dans les métadonnées de salon Matrix obsolètes.
  - Le rechargement de liste blanche en direct est modélisé directement au lieu de nécessiter un redémarrage de passerelle pour chaque mise à jour d'expéditeur.
- Mauvaises qualités :
  - L'analyse des mentions et la livraison des routes ont des rapports ouverts actifs.
  - Le nombre de dimensions de politique rend les modèles mentaux des opérateurs difficiles, en particulier lorsque `m.direct`, la configuration de salon, la promotion des invitations récentes et les listes blanches ne sont pas d'accord.
  - Certaines métadonnées du serveur d'accueil Matrix peuvent être obsolètes ou incomplètes, ce qui pousse la correction dans la logique de secours.
- Exclu de la qualité :
  - Je n'ai pas augmenté ou diminué la qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réelle.

Étiquettes de qualité :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réelle comme entrée de notation.

## Completeness Score

- Score: `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la politique DM, la classification des salons directs, la sélection de route entrante entre les DM liés à l'expéditeur, les portes de mention, le routage des réponses de fil Matrix, les gestionnaires de routage de fil Matrix persistants, les crochets de génération ACP/subagent.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Construire un tableau de décision orienté opérateur pour la politique DM, la politique de salon, la politique de mention et la politique de boucle de bot.
- Fermer ou retester les rapports de mention et de livraison de route actifs avant de déplacer la qualité au-dessus de Beta.
- Ajouter un appendice de scorecard mappant chaque option de politique d'accès documentée à au moins un scénario QA Matrix.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:608` documente la politique des DM et des salons ainsi que l'appairage.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:656` documente la réparation directe des salons.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:704` documente les commandes slash dans les DM et les salons.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:812` documente la résolution des cibles.
- `/Users/kevinlin/code/openclaw/docs/channels/groups.md:296` documente le comportement de la liste blanche des groupes Matrix et les cibles de salons stables.
- `/Users/kevinlin/code/openclaw/docs/channels/bot-loop-protection.md:123` documente la protection contre les boucles de bots Matrix basée sur la paire compte, salon et bot.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.ts:569` filtre les événements, déduplique les messages entrants et classe les salons directs.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.ts:682` applique la politique des salons et les portes de la liste blanche.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.ts:803` gère la politique des DM et le comportement d'appairage.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.ts:909` résout les mentions, les routes, l'accès aux commandes et l'historique des salons en attente.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.ts:2136` distribue les messages entrants via le runtime du canal.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/route.ts:42` résout les routes entrantes Matrix et les clés de session.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/allowlist.ts:33` normalise et résout les entrées de la liste blanche des utilisateurs Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/direct.ts:45` implémente le suivi des salons directs et l'actualisation du cache.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/mentions.ts:114` supprime les préfixes de mention et valide les étiquettes de mention Matrix.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1378` autorise les messages des observateurs lorsque les remplacements de la liste blanche de l'expéditeur les incluent.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1444` exécute le trafic de salon `allowBots=mentions` mentionné via un bot observateur.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1491` bloque le trafic de bot non mentionné même lorsque le salon est ouvert.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1561` bloque les commandes de contrôle préfixées par MXID des observateurs non autorisés.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:1661` recharge à chaud les suppressions de la liste blanche des groupes dans une passerelle en cours d'exécution.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:2565` exécute le scénario DM par rapport au salon DM provisionné sans mention.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:4586` affiche l'avis de session DM partagée dans un salon DM secondaire.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/allowlist.test.ts:4` couvre la correspondance de la liste blanche Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/route.test.ts:72` préfère le routage DM lié à l'expéditeur par rapport aux liaisons de secours.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/route.test.ts:121` permet aux liaisons de salon ACP configurées de remplacer le routage parent-pair DM.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/direct.test.ts:86` traite les salons `m.direct` comme des DM.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/direct.test.ts:286` traite l'état de membre `is_direct: false` personnel comme un signal non-DM.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.test.ts:706` bloque les commandes de contrôle de salon des expéditeurs appairés DM uniquement.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.test.ts:811` traite les messages de salon mentionnés via le nom d'affichage.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/monitor/handler.test.ts:2053` couvre le comportement de rechargement de la liste blanche en direct.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/session-route.test.ts:189` couvre la réutilisation de la route de session sortante pour les DM Matrix.

### Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "matrix dm room allowlist pairing mention"` n'a retourné aucun résultat.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` a retourné #83142, #68188, #85172, #73455 et d'autres problèmes/PR adjacents au routage Matrix.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix DM room allowlist pairing mention"` n'a retourné aucun résultat.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné des discussions de version mentionnant la validation du canal Matrix et le comportement des mentions.
