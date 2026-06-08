---
title: "Matrix - Note de Maturité des Approbations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Note de Maturité des Approbations

## Résumé

Les approbations natives de Matrix ont une surface d'implémentation solide : enregistrement de la capacité d'approbation exec et plugin, restrictions des approbateurs, suppression sur le même canal, correspondance de la cible d'origine, cibles DM des approbateurs, adaptateur de livraison natif, événements de métadonnées Matrix, ancres de réaction, état de cible de réaction persistant et résolution de passerelle. La couverture est Alpha car la preuve directe d'approbation Matrix en direct est plus mince que le reste de Matrix. La qualité est Beta car la source est robuste, mais discrawl a un commentaire d'examen sur les indices de réaction sur les messages d'approbation fragmentés.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Exec natif Matrix : exec natif Matrix et capacité d'approbation de plugin
- Résolution de cible d'origine à partir du tour Matrix : résolution de cible d'origine à partir de la source du tour Matrix, secours de session et routage d'approbation.
- Résolution de cible DM d'approbateur : résolution de cible DM d'approbateur, suppression de secours de transfert et livraison d'approbation native.
- Métadonnées d'approbation Matrix : métadonnées d'approbation Matrix, indices de réaction, persistance d'ancre de réaction et état de décision.

## Fonctionnalités

- Exec natif Matrix : exec natif Matrix et capacité d'approbation de plugin
- Résolution de cible d'origine à partir du tour Matrix : résolution de cible d'origine à partir de la source du tour Matrix, secours de session et routage d'approbation.
- Résolution de cible DM d'approbateur : résolution de cible DM d'approbateur, suppression de secours de transfert et livraison d'approbation native.
- Métadonnées d'approbation Matrix : métadonnées d'approbation Matrix, indices de réaction, persistance d'ancre de réaction et état de décision.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (64%)`
- Signaux positifs :
  - La documentation documente les approbations exec et les clés de configuration d'approbation Matrix.
  - La source dispose de l'enregistrement de capacité, de la correspondance d'origine, des cibles DM d'approbateur, de la réparation DM, des métadonnées d'approbation, des tentatives, du secours de fragment, de la persistance de cible de réaction et de la résolution de passerelle.
  - Les tests unitaires couvrent les descriptions de configuration, la correspondance de cible d'origine, les cibles d'approbateur, la suppression sur le même canal, les approbateurs plugin vs exec, la livraison à l'exécution, les ancres de réaction, l'état de réaction persistant et la résolution de passerelle.
  - L'assurance qualité Matrix couvre l'écho de réaction d'approbation et la réutilisation d'approbation observée.
- Signaux négatifs :
  - La preuve directe d'intégration d'approbation Matrix est beaucoup plus étroite que la preuve de routage, de média ou de E2EE.
  - Le texte d'approbation long/fragmenté et le placement d'ancre de réaction ont un historique d'examen.
- Lacunes d'intégration :
  - Ajouter des scénarios d'approbation en direct pour approbation exec, approbation plugin, cible DM uniquement, cible canal d'origine, target=both, texte d'approbation fragmenté et redémarrage de passerelle.
  - Ajouter une preuve de version que les ancres de réaction survivent au redémarrage du processus via l'état de cible persistant.
  - Ajouter une documentation montrant le comportement de réaction d'approbation pour les messages d'approbation fragmentés.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl --json search openclaw/openclaw --query "Matrix exec approvals reactions"` n'a retourné aucun résultat.
  - La requête large `gitcrawl --json search openclaw/openclaw --query "Matrix"` n'a pas mis en évidence une panne d'approbation Matrix majeure, mais les problèmes plus larges d'envoi/routage Matrix affectent toujours les chemins de livraison d'approbation.
- Rapports Discrawl :
  - La requête `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix exec approvals approval reactions"` a retourné un commentaire d'examen GitHub sur la PR #60931 : « matrix: add exec approval reaction shortcuts » ; le commentaire avertissait que les approbations longues pourraient placer l'indice « React here » dans un fragment ultérieur tandis que les réactions étaient ancrées au premier fragment.
  - La requête large `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné une discussion générale de version et de scorecard.
- Bonnes qualités :
  - La capacité d'approbation native restreint les approbateurs et sépare l'authentification d'approbation de plugin de la configuration d'approbation exec.
  - La correspondance de cible d'origine normalise les cibles d'utilisateur et de salle Matrix tout en préservant les identifiants de fil.
  - La livraison à l'exécution réessaye les défaillances d'envoi transitoires et les défaillances de réparation de salle directe.
  - Les métadonnées d'approbation sont versionnées et les réactions ont un état de cible persistant.
- Mauvaises qualités :
  - La couverture est étroite et le meilleur signal d'archive est une préoccupation de fragmentation au moment de l'examen plutôt qu'une preuve de succès en direct répétée.
  - La livraison d'approbation dépend de l'envoi, de la réparation de salle, de la réaction et des surfaces de résolution de passerelle fonctionnant toutes ensemble.
  - Les ancres de réaction peuvent être subtiles lorsque le contenu d'approbation est fragmenté.
- Exclu de la qualité :
  - Je n'ai pas augmenté ou diminué la Qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réelle.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réelle comme entrée de notation.

## Score de Complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/matrix.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour exec natif Matrix, résolution de cible d'origine à partir du tour Matrix, résolution de cible DM d'approbateur, métadonnées d'approbation Matrix.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter des scénarios d'approbation natifs Matrix au profil Matrix critique pour la version.
- Revalider le texte d'approbation fragmenté avec les indices et ancres de réaction.
- Ajouter une section de documentation d'opérateur montrant comment les cibles d'approbation Matrix, les approbateurs et la suppression d'origine interagissent.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:678` documente les approbations exec.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:895` documente les références de configuration d'approbation.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:658` documente la configuration de canal soutenue par plugin Matrix.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.ts:61` résout les cibles d'origine Matrix à partir de la source du tour.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.ts:152` crée le résolveur de cible d'origine natif Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.ts:182` résout les cibles DM d'approbateur Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.ts:199` crée la capacité d'approbation native Matrix restreinte par approbateur.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-handler.runtime.ts:46` définit les métadonnées d'approbation Matrix versionnées.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-handler.runtime.ts:182` réessaye la livraison d'approbation Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-handler.runtime.ts:201` prépare les cibles d'approbation et répare les salles directes pour les cibles d'utilisateur.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-reactions.ts:25` définit l'état de cible de réaction persistant.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-reactions.ts:164` énumère les liaisons et indices de réaction d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/exec-approval-resolver.ts:8` résout les décisions d'approbation Matrix via le résolveur de passerelle partagé.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:581` attend l'écho de réaction d'approbation Matrix avant d'attendre la décision.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenarios.test.ts:676` réutilise les événements d'approbation Matrix observés dans les attentes de cible de canal et DM.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.test.ts:48` décrit les capacités de livraison d'approbation native Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.test.ts:76` résout les cibles d'origine à partir de la source du tour Matrix.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.test.ts:102` résout les cibles DM d'approbateur.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.test.ts:180` maintient l'authentification d'approbation de plugin indépendante des approbateurs exec.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-handler.runtime.test.ts:179` envoie le contenu d'approbation Matrix versionné pour les approbations exec en attente.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-handler.runtime.test.ts:297` lie les réactions d'approbation Matrix avant de publier les réactions d'option.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-handler.runtime.test.ts:430` bascule vers la livraison Matrix fragmentée.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-reactions.test.ts:33` résout les événements d'ancre d'approbation enregistrés aux décisions d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-reactions.test.ts:111` persiste les cibles de réaction d'approbation lorsque l'état d'exécution est disponible.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/exec-approval-resolver.test.ts:17` soumet les résolutions d'approbation via le résolveur de passerelle partagé.

### Requêtes Gitcrawl

- `gitcrawl --json search openclaw/openclaw --query "Matrix exec approvals reactions"` n'a retourné aucun résultat.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` n'a pas retourné de panne spécifique à l'approbation majeure dans l'ensemble retourné, mais a retourné des problèmes plus larges d'envoi/routage Matrix.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix exec approvals approval reactions"` a retourné un commentaire d'examen GitHub sur la PR #60931 avertissant des indices de réaction et des ancres pour le texte d'approbation fragmenté long.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` a retourné une discussion générale de version et de scorecard.
