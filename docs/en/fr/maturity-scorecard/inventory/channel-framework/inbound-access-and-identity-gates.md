---
title: "Channel framework - Inbound Access and Identity Gates Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Channel framework - Inbound Access and Identity Gates Maturity Note

## Résumé

L'accès entrant et le contrôle d'accès par identité constituent l'une des parties les plus solides du framework de canal. Les modèles de code partagés acheminent les listes blanches de routes, l'appairage DM, les politiques de groupe, les groupes d'accès, l'activation par mention, l'autorisation de commande, l'autorisation d'événement et les projections d'admission assainies avant qu'un tour de canal n'atteigne la distribution d'agent.

La limite de maturité est la cohérence entre les fournisseurs et la migration historique. L'algèbre partagée est présente et bien testée, mais les preuves d'archive montrent qu'elle a été introduite pour remplacer les arbres d'authentification dupliqués spécifiques aux canaux, et la documentation doit encore faciliter la vérification du contrat inter-canaux pour les opérateurs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Appairage DM : Appairage DM et contrôles allowFrom de l'expéditeur
- Listes blanches de groupe/canal : Listes blanches de groupe/canal et listes blanches d'expéditeur
- Expansion du groupe d'accès : Expansion du groupe d'accès et assistants d'autorisation d'expéditeur
- Contrôle par mention : Contrôle par mention, mentions implicites, contournement de commande et admission consciente des boucles de bot
- Projections d'identité/route d'entrée assainies : Projections d'identité/route d'entrée assainies pour la distribution en aval

## Fonctionnalités

- Appairage DM : Appairage DM et contrôles allowFrom de l'expéditeur
- Listes blanches de groupe/canal : Listes blanches de groupe/canal et listes blanches d'expéditeur
- Expansion du groupe d'accès : Expansion du groupe d'accès et assistants d'autorisation d'expéditeur
- Contrôle par mention : Contrôle par mention, mentions implicites, contournement de commande et admission consciente des boucles de bot
- Projections d'identité/route d'entrée assainies : Projections d'identité/route d'entrée assainies pour la distribution en aval

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs :
  - La documentation couvre les groupes d'accès, l'appairage DM, la politique de groupe, les listes blanches de groupe, l'autorisation d'expéditeur de groupe et les exemples par canal (`docs/channels/access-groups.md:10`, `docs/channels/access-groups.md:121`, `docs/channels/groups.md:112`, `docs/channels/groups.md:286`, `docs/channels/groups.md:431`).
  - La source contient une logique d'admission partagée pour les décisions de route, commande, événement, activation, expéditeur, appairage, groupe d'accès et contrôle par mention (`src/channels/message-access/decision.ts:33`, `src/channels/message-access/decision.ts:70`, `src/channels/message-access/decision.ts:125`, `src/channels/message-access/decision.ts:204`, `src/channels/message-access/runtime.ts:598`).
  - La documentation des fournisseurs montre les portes partagées intégrées dans Discord, LINE, Signal, Google Chat, Matrix et le comportement de groupe (`docs/channels/discord.md:429`, `docs/channels/discord.md:532`, `docs/channels/line.md:139`, `docs/channels/signal.md:247`, `docs/channels/googlechat.md:162`, `docs/channels/matrix.md:652`).
  - La couverture unitaire exerce directement l'accès aux messages, la correspondance de liste blanche, le contrôle par mention et le contrôle de commande.
- Signaux négatifs :
  - La documentation est répartie sur des pages génériques et spécifiques aux fournisseurs, ce qui rend difficile pour les opérateurs de savoir quels champs participent à la même décision partagée.
  - Certaines pages de fournisseur décrivent toujours le comportement local plus profondément que le contrat d'entrée partagé.
  - Les preuves d'archive montrent que l'algèbre d'entrée partagée a été créée pour résoudre les implémentations d'authentification de canal dupliquées et divergentes.
- Lacunes d'intégration :
  - Aucune matrice en direct large n'a été trouvée qui exécute les mêmes scénarios d'appairage/groupe/mention/groupe d'accès sur tous les canaux pris en charge.
  - Les groupes d'accès ont une bonne couverture au niveau des assistants, mais les preuves actuelles ne prouvent pas que chaque fournisseur répertorié a un cas de conformité en direct.

## Score de qualité

- Score : `Beta (76%)`
- Justification de la qualité :
  - Le graphe de décision principal est explicite et composable ; les faits d'identité sont normalisés, les valeurs d'expéditeur brutes ne sont pas conservées inutilement, et les projections d'admission sont séparées de la distribution.
  - Les groupes d'accès sont documentés comme des alias de liste blanche plutôt que comme des octrois de rôle/propriétaire, réduisant les abus par les opérateurs.
  - Le contrôle par mention inclut la gestion explicite/implicite/contournement et préserve les règles de contournement de commande.
- Principaux risques de qualité :
  - Les opérateurs doivent toujours assembler la documentation générique, la documentation de canal et les exemples de configuration pour diagnostiquer pourquoi un message a été supprimé.
  - Certains canaux ont des formats d'expéditeur spéciaux, des ID de groupe, des drapeaux de bot ou une sémantique de mention native, donc le contrat partagé dépend des adaptateurs de fournisseur produisant des faits corrects.
  - L'archive montre des problèmes d'entrée à faible volume mais à fort impact autour du contrôle par mention et de la dérive de l'arbre d'authentification en amont.
- La notation de qualité exclut la quantité de tests ; les tests sont enregistrés uniquement comme preuve de couverture.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/channel-framework.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'appairage DM, les listes blanches de groupe/canal, l'expansion du groupe d'accès, le contrôle par mention, les projections d'identité/route d'entrée assainies.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Publier un tableau de décision d'entrée inter-canaux qui mappe l'appairage DM, la politique de groupe, les groupes d'accès, le contrôle par mention, les commandes et les classes d'événement aux résultats d'autorisation/suppression.
- Ajouter une fixture de conformance qui exécute les mêmes cas d'entrée sur chaque adaptateur de canal fourni qui prétend avoir un support d'accès partagé.
- Améliorer la sortie de statut/débogage afin que les opérateurs puissent voir la porte exacte qui a supprimé un message sans lire les journaux.

## Preuves

### Documentation

- `docs/channels/access-groups.md:10` décrit les groupes d'accès comme des listes de senders nommées référencées à partir des listes blanches de canaux ; `docs/channels/access-groups.md:14` avertit qu'ils n'accordent pas l'accès par eux-mêmes.
- `docs/channels/access-groups.md:121` à `docs/channels/access-groups.md:128` énumère les chemins d'autorisation de canaux de messages partagés et le support groupé actuel.
- `docs/channels/groups.md:112` à `docs/channels/groups.md:126` sépare l'autorisation de déclenchement de la visibilité du contexte et définit `allowlist`, `allowlist_quote` et le comportement du contexte de citation/réponse.
- `docs/channels/groups.md:286` à `docs/channels/groups.md:296` documentent la politique de groupe, la séparation des appairages DM et les mises en garde concernant la liste blanche Matrix.
- `docs/channels/groups.md:321` à `docs/channels/groups.md:323` documentent le comportement du groupe nécessitant une mention et les mentions implicites via les réponses/citations.
- `docs/channels/groups.md:428` à `docs/channels/groups.md:431` expliquent les clés de liste blanche de groupe et la confusion courante selon laquelle l'appairage DM n'autorise pas les commandes de groupe.
- `docs/channels/discord.md:429` à `docs/channels/discord.md:589` documentent l'appairage DM Discord, les groupes d'accès, la politique de groupe, le contrôle des mentions, les listes blanches de canaux/guildes et les contrôles de senders sensibles aux rôles.
- `docs/channels/line.md:139` à `docs/channels/line.md:145`, `docs/channels/signal.md:247` à `docs/channels/signal.md:258` et `docs/channels/googlechat.md:160` à `docs/channels/googlechat.md:164` montrent le câblage spécifique au fournisseur pour l'appairage et la liste blanche de groupe.

### Source

- `src/channels/message-access/decision.ts:33` à `src/channels/message-access/decision.ts:68` évaluent les portes de route et la politique de sender vide.
- `src/channels/message-access/decision.ts:70` à `src/channels/message-access/decision.ts:112` évaluent les portes de commande ; `src/channels/message-access/decision.ts:125` à `src/channels/message-access/decision.ts:164` évaluent les portes d'événement.
- `src/channels/message-access/decision.ts:204` à `src/channels/message-access/decision.ts:254` évalue les portes d'activation ; `src/channels/message-access/decision.ts:256` à `src/channels/message-access/decision.ts:328` compose le graphe de décision d'entrée du canal.
- `src/channels/message-access/runtime.ts:66` à `src/channels/message-access/runtime.ts:98` fusionne les listes `allowFrom` effectives ; `src/channels/message-access/runtime.ts:100` à `src/channels/message-access/runtime.ts:123` lit l'état du magasin d'appairage.
- `src/channels/message-access/runtime.ts:237` à `src/channels/message-access/runtime.ts:310` construit des résolveurs d'accès réutilisables ; `src/channels/message-access/runtime.ts:598` à `src/channels/message-access/runtime.ts:722` résout l'identité normalisée, les groupes d'accès, les faits de route, l'état, la décision et les projections assainies.
- `src/channels/mention-gating.ts:34` à `src/channels/mention-gating.ts:54` modélise les faits et la politique de mention ; `src/channels/mention-gating.ts:171` à `src/channels/mention-gating.ts:191` produit les décisions de mention entrantes.
- `src/channels/allowlist-match.ts:35` à `src/channels/allowlist-match.ts:80` compile et correspond aux entrées de liste blanche ; `src/channels/allowlist-match.ts:93` à `src/channels/allowlist-match.ts:122` supporte la correspondance simple de sender.
- `src/channels/command-gating.ts:8` à `src/channels/command-gating.ts:66` résout les portes de commande et de commande de contrôle.

### Tests d'intégration

- `scripts/e2e/npm-onboard-channel-agent-docker.sh:184` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:201` vérifie un tour d'agent local piloté par canal après la configuration pour les canaux courants, prouvant indirectement que l'admission atteint la distribution.
- `src/gateway/gateway-acp-bind.live.test.ts:565` exerce une conversation DM Slack synthétique liée à une session ACP en direct et réachemine le tour suivant, couvrant l'identité entrante admise via le routage.
- Aucune suite de conformité en direct large n'a été trouvée pour toutes les portes d'accès sur tous les canaux supportés.

### Tests unitaires

- `src/channels/message-access/message-access.test.ts:87` à `src/channels/message-access/message-access.test.ts:164` vérifie l'entrée du canal, les listes blanches de senders de route sans conserver les valeurs de sender brutes et la politique de refus quand le sender est vide.
- `src/channels/allowlist-match.test.ts:7` à `src/channels/allowlist-match.test.ts:50` vérifie l'invalidation du cache de liste blanche et le recalcul des candidats.
- `src/channels/mention-gating.test.ts:9` à `src/channels/mention-gating.test.ts:265` couvre les mentions explicites/implicites, le contournement, les mentions indisponibles, le comportement de contournement de commande et les aides de type de mention implicite.
- `src/channels/command-gating.test.ts:8` à `src/channels/command-gating.test.ts:99` couvre l'authentification de commande soutenue par un groupe d'accès et les portes de commande de contrôle.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "channel inbound allowlist pairing mention gating access group" --json --limit 8`

Résultats :

- A retourné le cluster de problème/PR #74163 avec une note de contrôle de mention Microsoft Teams indiquant que le comportement `suppressAlways` devrait être honoré, montrant que la sémantique d'entrée spécifique au fournisseur compte toujours.
- N'a pas retourné un grand cluster de bug ouvert actuel pour la requête d'entrée partagée exacte.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channel inbound allowlist pairing mention gating access group" --limit 8`

Résultats :

- A retourné une note de conception du responsable pour `channel_ingress_refactor.md` décrivant les arbres d'authentification en amont dupliqués et l'objectif d'une algèbre d'autorisation d'entrée centrale couvrant la politique DM/groupe, les listes blanches, les groupes d'accès, l'appairage, l'authentification de commande/événement et l'activation de mention.
- Cela soutient l'évaluation de la qualité selon laquelle le contrat partagé existe mais a été construit pour remplacer la logique spécifique au fournisseur précédemment divergente.
