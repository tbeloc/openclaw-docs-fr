---
title: "Microsoft Teams - Note de Maturité du Routage et de la Livraison des Conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Note de Maturité du Routage et de la Livraison des Conversations

## Résumé

Le routage Teams dispose d'une implémentation runtime large et de preuves d'archive significatives provenant de correctifs de thread/session de type production. La couverture atteint Beta car la source et les tests couvrent les listes blanches imbriquées, les portes de mention, les sessions de thread, le contexte parent et la récupération de thread Graph. La qualité reste Alpha car l'historique d'archive montre des régressions réelles autour de l'isolation des sessions de thread, des cibles de réponse sortantes, de la pagination et de la gestion des threads croisés avec débounce.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Routage et Livraison des Conversations`
- Fusionnée à partir de : `Routage des Conversations`, `Webhook et Livraison`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Listes blanches d'équipe et de canal : Couvre les listes blanches Teams/canal, les ID de conversation stables, `channels.msteams.teams`, le routage avec caractères génériques et la résolution des noms d'équipe/canal.
- Réponses de canal déterministes : Couvre le routage déterministe des réponses vers le canal Teams où un message est arrivé et les protections de routage avec caractères génériques.
- Accès aux groupes contrôlé par mention : Couvre `groupPolicy`, `groupAllowFrom`, `requireMention` et les réponses de groupe ou canal contrôlées par mention.
- Routage de session : Couvre le routage déterministe des réponses, les clés de session, les liaisons de canal et l'isolation des conversations pour les salles et canaux Microsoft Teams.
- Contexte de réponse et de thread : Couvre le contexte de réponse, les messages sources cités, le routage conscient des threads et le contexte de salle pour les conversations Teams.
- Formatage et segmentation du texte : Couvre le formatage et la segmentation du texte sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Cartes adaptatives et de présentation : Couvre les cartes adaptatives et de présentation sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Streaming de progression : Couvre le streaming de progression sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Accusés de réception et erreurs de livraison : Couvre les accusés de réception et erreurs de livraison sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Réponses en file d'attente et proactives : Couvre les réponses en file d'attente et proactives sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Runtime Webhook : Couvre le Runtime Webhook sur le démarrage du serveur webhook, la gestion auth/JWT du SDK, la pré-porte bearer, les limites de corps JSON et le comportement runtime webhook, le cycle de vie du SDK et le comportement de limite cloud proactif associé.
- Cycle de Vie du SDK : Couvre le Cycle de Vie du SDK sur le démarrage du serveur webhook, la gestion auth/JWT du SDK, la pré-porte bearer, les limites de corps JSON et le comportement runtime webhook, le cycle de vie du SDK et le comportement de limite cloud proactif associé.
- Limite Cloud Proactive : Couvre la Limite Cloud Proactive sur le démarrage du serveur webhook, la gestion auth/JWT du SDK, la pré-porte bearer, les limites de corps JSON et le comportement runtime webhook, le cycle de vie du SDK et le comportement de limite cloud proactif associé.
- Formatage et segmentation du texte : Couvre le formatage et la segmentation du texte sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé
- Cartes adaptatives et de présentation : Couvre les cartes adaptatives et de présentation sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé
- Streaming de progression : Couvre le streaming de progression sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé
- Accusés de réception et erreurs de livraison : Couvre les accusés de réception et erreurs de livraison sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé
- Réponses en file d'attente et proactives : Couvre les réponses en file d'attente et proactives sur la segmentation du texte sortant, la conversion de tableau markdown, le séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé
- Runtime Webhook : Couvre le Runtime Webhook sur le démarrage du serveur webhook, la gestion auth/JWT du SDK, la pré-porte bearer, les limites de corps JSON et le comportement runtime webhook, le cycle de vie du SDK et le comportement de limite cloud proactif associé
- Cycle de Vie du SDK : Couvre le Cycle de Vie du SDK sur le démarrage du serveur webhook, la gestion auth/JWT du SDK, la pré-porte bearer, les limites de corps JSON et le comportement runtime webhook, le cycle de vie du SDK et le comportement de limite cloud proactif associé
- Limite Cloud Proactive : Couvre la Limite Cloud Proactive sur le démarrage du serveur webhook, la gestion auth/JWT du SDK, la pré-porte bearer, les limites de corps JSON et le comportement runtime webhook, le cycle de vie du SDK et le comportement de limite cloud proactif associé

## Fonctionnalités

- Listes blanches d'équipe et de canal : Couvre les listes blanches Teams/canal, les ID de conversation stables, `channels.msteams.teams`, le routage avec caractères génériques et la résolution des noms d'équipe/canal.
- Réponses de canal déterministes : Couvre le routage déterministe des réponses vers le canal Teams où un message est arrivé et les protections de routage avec caractères génériques.
- Accès aux groupes contrôlé par mention : Couvre `groupPolicy`, `groupAllowFrom`, `requireMention` et les réponses de groupe ou canal contrôlées par mention.
- Routage de session : Couvre le routage déterministe des réponses, les clés de session, les liaisons de canal et l'isolation des conversations pour les salles et canaux Microsoft Teams.
- Contexte de réponse et de thread : Couvre le contexte de réponse, les messages sources cités, le routage conscient des threads et le contexte de salle pour les conversations Teams.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (72%)`
- Signaux positifs : Les docs, la source runtime et les tests ciblés couvrent les listes blanches d'équipe/canal imbriquées, les portes de mention, le style de réponse, les clés de session, le contexte parent du thread et la récupération de thread Graph.
- Signaux négatifs : Aucun fichier de scénario de routage de thread Teams en direct actuel n'a été trouvé ; la preuve d'archive est principalement une discussion de problème/PR et une confirmation de production plutôt qu'une voie de test reproductible.
- Lacunes d'intégration : Scénarios en direct manquants pour les publications par rapport aux threads style UI, les réponses de thread de canal, le repli de niveau supérieur, la pagination de thread long et le filtrage du contexte supplémentaire sous les listes blanches.

## Score de Qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : La recherche par mot-clé ciblée pour les termes thread/session n'a retourné aucun résultat, mais la recherche d'archive Teams large et discrawl ont surfacé les PR/problèmes de session de thread.
- Rapports Discrawl : `msteams thread session replyToId routing` a retourné `#62713` avec un commentaire d'examen P1 sur la coalescence de débounce entrant fusionnant les messages de différents threads de canal ; la recherche large a également surfacé `#59294`, `#66771` et `#69428` discussion autour de l'isolation des threads, du `replyToId` sortant, des clés de session malformées et de la pagination.
- Bonnes qualités : Le routage est d'abord basé sur l'ID, contrôlé par mention par défaut, imbriqué par équipe et canal, et la source isole maintenant les threads de canal et récupère le contexte parent/thread avec dégradation gracieuse.
- Mauvaises qualités : L'API Teams n'expose pas le style UI du canal, donc `replyStyle` est configuré par l'opérateur ; le comportement thread/session a un historique de régression récent.
- Exclu de la qualité : Nombre de tests unitaires, largeur des tests de route et lacunes de preuve en direct.

## Score de Complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/microsoft-teams.md`.
- Signaux positifs : les preuves d'archive docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les listes blanches d'équipe et de canal, les réponses de canal déterministes, l'accès aux groupes contrôlé par mention, le routage de session, le contexte de réponse et de thread.
- Signaux négatifs : la note d'archive antérieure à la version 3 du processus de notation de Complétude, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une fiche de routage en direct pour les canaux de style publications et threads Teams.
- Ajouter des scénarios soutenus par locataire pour plusieurs threads simultanés dans un canal, les envois avec débounce et la pagination de thread long.
- Ajouter des diagnostics d'opérateur pour un mauvais `replyStyle` et des références de thread stockées obsolètes.

## Preuves

### Docs

- `docs/channels/msteams.md` documente `groupPolicy`, `groupAllowFrom`, listes d'autorisation imbriquées Teams/canal, IDs de conversation stables, résolution Graph, `replyStyle`, préservation du contexte de fil, contexte historique, extraction d'ID Team/Canal, et limitations de canal privé.
- `docs/channels/groups.md` documente le comportement de groupe inter-canal, les portes de mention, les mentions implicites, les clés de session de groupe, et les restrictions d'outils par groupe.
- `docs/channels/channel-routing.md` est la référence de routage partagée.

### Source

- `extensions/msteams/src/policy.ts` résout les listes d'autorisation imbriquées team/canal, la politique d'outils, les exigences de mention, et la précédence du style de réponse.
- `extensions/msteams/src/monitor-handler/message-handler.ts` supprime les expéditeurs de groupe bloqués, résout les clés de route/session, applique les portes de mention, stocke les références de conversation, construit les IDs de canal natifs, récupère les réponses de fil Graph, filtre le contexte supplémentaire, et envoie les réponses.
- `extensions/msteams/src/monitor-handler/thread-session.ts` isole les sessions de fil de canal.
- `extensions/msteams/src/thread-parent-context.ts` implémente l'injection de contexte parent en cache.
- `extensions/msteams/src/graph-thread.ts` résout les IDs d'équipe et récupère les messages parent et de réponse avec des avertissements de pagination.

### Tests d'intégration

- Aucune voie de routage Teams en direct/e2e réelle n'a été trouvée par `rg`.
- Les références de discussion d'archive confirment la production sur les corrections de session de fil antérieures, mais cet audit n'a pas trouvé d'artefact de scénario enregistré.

### Tests unitaires

- `extensions/msteams/src/policy.test.ts` couvre la configuration de route et la politique de réponse.
- `extensions/msteams/src/monitor-handler/message-handler.thread-session.test.ts` couvre l'isolation de session de fil.
- `extensions/msteams/src/monitor-handler/message-handler.thread-parent.test.ts` et `extensions/msteams/src/thread-parent-context.test.ts` couvrent l'injection et la mise en cache du contexte parent.
- `extensions/msteams/src/resolve-allowlist.test.ts` couvre la résolution de liste d'autorisation team/canal et utilisateur.
- `extensions/msteams/src/channel.actions.test.ts` couvre le routage d'action d'ID de canal natif.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "msteams thread session routing replyToId channel" --json --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams thread session replyToId thread context" --json --limit 10`

Résultats :

- Les deux recherches gitcrawl ciblées ont retourné `[]`.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams thread session replyToId routing"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams groupPolicy groupAllowFrom requireMention team channel"`

Résultats :

- La requête de fil a retourné `#62713`, incluant un commentaire d'examen P1 pour inclure l'identité de fil dans le partitionnement de déduplication.
- La requête de politique de groupe n'a retourné aucune ligne.
