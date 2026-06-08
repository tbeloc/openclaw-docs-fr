---
title: "Microsoft Teams - Webhook and Delivery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Webhook and Delivery Maturity Note

## Résumé

La livraison sortante Teams dispose d'une large surface source pour le texte, les médias, les charges utiles, les cartes de présentation sémantique, les sondages, les flux de progression natifs, les reçus et les indices d'erreur. La couverture reste Alpha car l'audit a trouvé un code unitaire et d'exécution solide mais pas de scénarios durables d'envoi/flux/carte Teams en direct. La qualité est également Alpha car l'historique récent de migration du SDK a explicitement corrigé le comportement de flux, de carte adaptative, d'édition/suppression et de retour d'information visibles par l'utilisateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Formatage et segmentation du texte : Couvre le formatage et la segmentation du texte dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Cartes adaptatives et de présentation : Couvre les cartes adaptatives et de présentation dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Flux de progression : Couvre le flux de progression dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Reçus et erreurs de livraison : Couvre les reçus et erreurs de livraison dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Réponses en file d'attente et proactives : Couvre les réponses en file d'attente et proactives dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Webhook Runtime : Couvre Webhook Runtime dans le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-porte du porteur, les limites du corps JSON et le comportement d'exécution webhook, de cycle de vie du SDK et de limite de cloud proactive associé.
- Cycle de vie du SDK : Couvre le cycle de vie du SDK dans le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-porte du porteur, les limites du corps JSON et le comportement d'exécution webhook, de cycle de vie du SDK et de limite de cloud proactive associé.
- Limite de cloud proactive : Couvre la limite de cloud proactive dans le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-porte du porteur, les limites du corps JSON et le comportement d'exécution webhook, de cycle de vie du SDK et de limite de cloud proactive associé.

## Fonctionnalités

- Formatage et segmentation du texte : Couvre le formatage et la segmentation du texte dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Cartes adaptatives et de présentation : Couvre les cartes adaptatives et de présentation dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Flux de progression : Couvre le flux de progression dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Reçus et erreurs de livraison : Couvre les reçus et erreurs de livraison dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Réponses en file d'attente et proactives : Couvre les réponses en file d'attente et proactives dans la segmentation du texte sortant, la conversion de tableau markdown, la séquençage des médias de charge utile, le rendu de présentation sémantique et le comportement de livraison et de rendu sortant associé.
- Webhook Runtime : Couvre Webhook Runtime dans le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-porte du porteur, les limites du corps JSON et le comportement d'exécution webhook, de cycle de vie du SDK et de limite de cloud proactive associé.
- Cycle de vie du SDK : Couvre le cycle de vie du SDK dans le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-porte du porteur, les limites du corps JSON et le comportement d'exécution webhook, de cycle de vie du SDK et de limite de cloud proactive associé.
- Limite de cloud proactive : Couvre la limite de cloud proactive dans le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-porte du porteur, les limites du corps JSON et le comportement d'exécution webhook, de cycle de vie du SDK et de limite de cloud proactive associé.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs : Les docs et la source couvrent la livraison durable de texte/médias/charge utile, les flux de progression DM natifs, la réserve de bloc, les cartes adaptatives, les cartes de présentation et les reçus ; les tests ciblés couvrent de nombreuses coutures sortantes.
- Signaux négatifs : Aucun scénario Teams en direct/e2e enregistré n'a été trouvé pour les envois réels, le flux natif, les cartes, les présentations ou les réponses finales proactives.
- Lacunes d'intégration : Preuve de scénario en direct manquante pour la fermeture du flux natif DM, la réserve de canal/groupe, l'envoi de carte adaptative, l'envoi de présentation, l'édition/suppression et les réponses en file d'attente longue durée.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : `msteams streaming adaptive card Action.Execute feedback` a retourné `#76262`, qui prétend corriger les migrations du SDK Teams autour des votes de sondage de carte adaptative, des envois CLI de carte adaptative, des retours d'information, des cartes de flux et du comportement d'édition/suppression.
- Rapports Discrawl : La recherche ciblée de flux/carte adaptative n'a retourné aucune ligne, mais la large recherche `msteams` incluait une discussion de mainteneur selon laquelle `#76262` corrige la finalisation du flux, les boutons de carte adaptative, les défaillances silencieuses d'édition/suppression et l'arrêt du crash en milieu de flux.
- Bonnes qualités : L'adaptateur sortant utilise des aides de charge utile partagées, prend en charge les cartes de présentation, émet des reçus, classe les erreurs et gère la progression native DM séparément du comportement de réserve de canal/groupe.
- Mauvaises qualités : Le rendu Teams diffère de Slack/Discord, les menus de sélection se dégradent en texte, le support de flux natif est plus étroit que tous les modes sortants et le churn de migration du SDK est récent.
- Exclu de la qualité : Profondeur des tests unitaires, nombre de tests sortants et manque de preuve e2e en direct.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/microsoft-teams.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le formatage et la segmentation du texte, les cartes adaptatives et de présentation, le flux de progression, les reçus et erreurs de livraison, les réponses en file d'attente et proactives, Webhook Runtime, Cycle de vie du SDK, Limite de cloud proactive.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des scénarios sortants Teams en direct pour la segmentation du texte, la progression native, la réserve de canal, les cartes adaptatives, les cartes de présentation, l'édition/suppression et les réponses finales en file d'attente.
- Ajouter la documentation de l'opérateur pour quand le flux natif par rapport à la réserve de bloc/progression est utilisé.
- Ajouter une preuve de version que les régressions de migration du SDK sont fermées dans un vrai locataire.

## Preuves

### Docs

- `docs/channels/msteams.md` documente les limites de formatage, les cartes de présentation, les formats cibles, la messagerie proactive, le style de réponse et les risques de délai d'expiration du webhook.
- `docs/concepts/progress-drafts.md` documente le flux de progression Teams natif dans les chats personnels et le comportement de livraison de bloc.
- `docs/concepts/streaming.md` documente Teams comme l'exception de flux de progression natif.

### Source

- `extensions/msteams/src/outbound.ts` déclare la livraison durable de texte/médias/charge utile, la segmentation du texte, le support des sondages, les capacités de présentation, la séquençage des médias et les reçus de canal attachés.
- `extensions/msteams/src/send.ts` envoie des messages, des sondages, des cartes, des médias et retourne des reçus et des indices d'erreur.
- `extensions/msteams/src/reply-dispatcher.ts` achemine les réponses en tour et proactives et canalise les événements d'agent dans le comportement de flux/progression.
- `extensions/msteams/src/reply-stream-controller.ts` gère l'état du flux Teams natif, les deltas, la fermeture finale, les métadonnées de retour d'information et le comportement de réserve.
- `extensions/msteams/src/presentation.ts` rend les charges utiles de présentation sémantique en tant que cartes adaptatives Teams.

### Tests d'intégration

- Aucune voie sortante Teams en direct/e2e n'a été trouvée par `rg`.
- La configuration vitest Teams limite les tests à `extensions/msteams/**/*.test.ts`, ce qui est large mais pas une voie de locataire en direct.

### Tests unitaires

- `extensions/msteams/src/outbound.test.ts` couvre le comportement de l'adaptateur sortant.
- `extensions/msteams/src/reply-dispatcher.test.ts` couvre la distribution des réponses, la réserve et les messages d'erreur.
- `extensions/msteams/src/reply-stream-controller.test.ts` couvre le delta de flux natif, la fermeture, l'annulation et le comportement de réserve.
- `extensions/msteams/src/channel.actions.test.ts` couvre le rendu de carte de présentation et la validation de cible d'action.
- `extensions/msteams/src/presentation.test.ts` n'était pas présent ; le comportement de présentation est exercé par le biais de tests de canal/action.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "msteams streaming adaptive card Action.Execute feedback" --json --limit 10`

Résultats :

- A retourné `#76262`, "fix(msteams): rebase TeamsSDK patterns to simplify Teams Integration", avec des extraits de carte adaptative et de retour d'information.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams streaming adaptive card outbound proactive"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams"`

Résultats :

- La requête de flux ciblée n'a retourné aucune ligne.
- La large requête `msteams` a retourné une discussion de migration du SDK Teams qui référençait des corrections de flux, de carte adaptative, d'édition/suppression et de retour d'information visibles par l'utilisateur.
