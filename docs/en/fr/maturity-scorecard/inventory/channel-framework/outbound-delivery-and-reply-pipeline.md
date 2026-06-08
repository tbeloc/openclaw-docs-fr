---
title: "Cadre de canal - Note de maturité du pipeline de livraison sortante et de réponse"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Cadre de canal - Note de maturité du pipeline de livraison sortante et de réponse

## Résumé

La livraison sortante et la gestion des réponses disposent d'un noyau partagé mature. Le noyau de tour achemine les réponses assemblées via une livraison sortante durable, les adaptateurs exposent la sémantique de réception de texte/média/sondage, le pipeline de réponse supporte les transformations de canal et les rappels de saisie, et le contexte d'envoi durable suit les résultats de rendu/envoi/édition/suppression/validation/échec.

La limite de maturité concerne les cas limites de livraison spécifiques au fournisseur. La mécanique de livraison centrale est solide, mais les preuves d'archive montrent des corrections récentes pour la livraison d'assistant vide, la livraison de sujet Telegram, les défaillances de livraison de texte/outil mixte, et le nettoyage de livraison de canal sur Telegram, iMessage, Slack, Matrix et Discord.

## Portée de la catégorie

Inclus dans cette catégorie :

- Livraison automatique de réponse finale : Livraison automatique de réponse finale et livraison visible strictement message-outil uniquement
- Orchestration d'envoi sortant durable : Orchestration d'envoi sortant durable, reçus, défaillances partielles et chemins de secours
- Transformations du pipeline de réponse : Transformations du pipeline de réponse, rappels de saisie, diffusion en continu de brouillon et réactions de statut
- Pont adaptateur sortant du fournisseur : Pont adaptateur sortant du fournisseur et capacités de message

## Fonctionnalités

- Livraison automatique de réponse finale : Livraison automatique de réponse finale et livraison visible strictement message-outil uniquement
- Orchestration d'envoi sortant durable : Orchestration d'envoi sortant durable, reçus, défaillances partielles et chemins de secours
- Transformations du pipeline de réponse : Transformations du pipeline de réponse, rappels de saisie, diffusion en continu de brouillon et réactions de statut
- Pont adaptateur sortant du fournisseur : Pont adaptateur sortant du fournisseur et capacités de message

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - Les docs décrivent les modes de réponse visibles, la suppression message-outil uniquement, les exceptions de commande native, la livraison stricte de salle ambiante, les aperçus de diffusion en continu/progression et les options de livraison spécifiques au fournisseur (`docs/channels/groups.md:46`, `docs/channels/groups.md:54`, `docs/channels/groups.md:106`, `docs/channels/ambient-room-events.md:47`, `docs/channels/discord.md:684`, `docs/gateway/config-channels.md:807`).
  - La source centrale du noyau centralise le pipeline de réponse, la livraison durable, le contexte d'envoi durable, le pont adaptateur sortant, la boucle de diffusion en continu de brouillon, les réactions de statut et les exigences de livraison.
  - La couverture unitaire est approfondie pour la livraison durable, les résultats du contexte d'envoi, les reçus de l'adaptateur sortant, les capacités, la diffusion en continu de brouillon et les réactions de statut.
  - Les harnais de canal Docker et MCP exercent la livraison en forme de canal après la configuration.
- Signaux négatifs :
  - Les cas limites spécifiques au fournisseur émergent toujours dans les résultats d'archive, en particulier autour des sujets Telegram et de la livraison de texte/outil mixte.
  - Les modes de réponse visibles sont documentés sur les pages de groupe, ambiante, fournisseur et config ; le modèle mental de l'opérateur n'est pas centralisé.
  - Aucune preuve actuelle ne montre que chaque adaptateur dispose d'un cas de conformité de livraison durable équivalent.
- Lacunes d'intégration :
  - La preuve en direct de la durabilité de la livraison n'est pas uniforme sur tous les canaux officiels.
  - La suppression message-outil uniquement et le comportement de réponse finale automatique nécessitent une matrice E2E inter-canal plus large.

## Score de qualité

- Score : `Beta (75%)`
- Justification de la qualité :
  - Les résultats de livraison sont explicites : les résultats supprimés, livrés, défaillance partielle, non supporté et échoué sont représentés plutôt que cachés derrière des exceptions génériques.
  - Le contexte d'envoi durable conserve les plans rendus rejouables et transmet les reçus de l'adaptateur, ce qui est une conception opérationnelle solide pour les tentatives et le débogage.
  - Le cadre distingue le texte assistant final, les envois message-outil, les éditions de brouillon, les réactions de statut et les réponses de commande native.
- Principaux risques de qualité :
  - Les capacités du fournisseur diffèrent considérablement, donc le pont adaptateur doit préserver le comportement nuancé de reçu et d'échec.
  - Les opérateurs peuvent mal configurer les modes de réponse visible et observer des tours "silencieux" réussis à moins que les docs/statut n'expliquent clairement la suppression.
  - Les preuves d'archive récentes montrent que cette couche reçoit toujours des corrections de nettoyage multi-canal.
- La notation de qualité exclut la quantité de tests ; les tests sont enregistrés uniquement comme preuve de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/channel-framework.md`.
- Signaux positifs : les preuves d'archive docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Livraison automatique de réponse finale, Orchestration d'envoi sortant durable, Transformations du pipeline de réponse, Pont adaptateur sortant du fournisseur.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une suite de conformité du fournisseur pour réponse finale automatique, envoi message-outil, final supprimé, défaillance partielle, réconciliation d'envoi inconnu, édition/suppression et secours média.
- Consolider le comportement de réponse visible dans un tableau d'opérateur unique avec les clés de config exactes et les exceptions de canal.
- Faciliter l'inspection des résumés de résultats de livraison à partir de `channels status` ou des traces de tour.

# Preuve

## Docs

- `docs/channels/groups.md:46` à `docs/channels/groups.md:54` décrivent les réponses visibles automatiques et le mode visible-reply de `message_tool`.
- `docs/channels/groups.md:106` documente les exceptions de visible-reply des commandes slash natives.
- `docs/channels/ambient-room-events.md:47` et `docs/channels/ambient-room-events.md:181` documentent la livraison visible stricte pour les salons ambiants et la suppression du texte final sauf si l'outil de message publie.
- `docs/channels/discord.md:648` à `docs/channels/discord.md:684` décrivent les modes de réponse, les aperçus de liens et la livraison de streaming/progression.
- `docs/channels/matrix.md:197` à `docs/channels/matrix.md:233` documentent les aperçus de streaming Matrix, le comportement d'aperçu de progression des outils, les réponses finales multimédias et les compromis de limite de débit.
- `docs/gateway/config-channels.md:807` à `docs/gateway/config-channels.md:809` expliquent le symptôme « l'agent a fonctionné mais pas de réponse visible » et le comportement de rechargement à chaud pour la configuration visible-reply.

## Source

- `src/channels/turn/kernel.ts:348` à `src/channels/turn/kernel.ts:428` assemblent les tours de canal et acheminent les réponses via une livraison durable avec observation post-livraison.
- `src/channels/turn/kernel.ts:453` à `src/channels/turn/kernel.ts:764` enregistrent, distribuent, finalisent, suppriment et exécutent les tours de canal sur les chemins d'adaptateur préparés/complets.
- `src/channels/message/reply-pipeline.ts:28` à `src/channels/message/reply-pipeline.ts:91` construisent le pipeline de réponse avec le mode de livraison source, les transformations de canal, la saisie et les rappels de cycle de vie.
- `src/channels/turn/durable-delivery.ts:19` à `src/channels/turn/durable-delivery.ts:226` modélisent les résultats de livraison, la résolution cible/réponse/thread, les vérifications de support et le comportement final de livraison durable.
- `src/channels/message/send.ts:40` à `src/channels/message/send.ts:102` modélisent les statuts de résultat d'envoi ; `src/channels/message/send.ts:155` à `src/channels/message/send.ts:349` implémentent l'orchestration de rendu/aperçu/envoi/édition/suppression/validation/échec du contexte d'envoi durable.
- `src/channels/message/outbound-bridge.ts:27` à `src/channels/message/outbound-bridge.ts:167` définissent les méthodes d'adaptateur sortant, les formes de résultat/reçu et le comportement du pont d'adaptateur.
- `src/channels/draft-stream-loop.ts:10` à `src/channels/draft-stream-loop.ts:127` implémentent le streaming de brouillon limité et la gestion du vidage.
- `src/channels/status-reactions.ts:14` à `src/channels/status-reactions.ts:501` implémentent les adaptateurs de réaction de statut, les valeurs par défaut, le débounce et le nettoyage terminal.

## Tests d'intégration

- `scripts/e2e/npm-onboard-channel-agent-docker.sh:184` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:201` vérifient un tour de canal après la configuration pour Telegram, Discord et Slack.
- `scripts/e2e/mcp-channels-docker.sh:29` et `scripts/e2e/mcp-channels-docker-client.ts:97` à `scripts/e2e/mcp-channels-docker-client.ts:311` exercent le comportement d'envoi/conversation/pièce jointe du canal MCP dans Docker.
- Aucune matrice de conformité de livraison en direct tous canaux n'a été trouvée.

## Tests unitaires

- `src/channels/turn/kernel.test.ts:201` à `src/channels/turn/kernel.test.ts:599` couvrent la livraison sortante durable, la propagation des résultats de livraison, la préparation de la charge utile, les chemins non pris en charge/d'échec, la livraison personnalisée, la livraison héritée, les options du pipeline de réponse et l'enregistrement de session avant la distribution.
- `src/channels/turn/kernel.test.ts:633` à `src/channels/turn/kernel.test.ts:1147` couvrent la distribution préparée, les abandons de boucle bot, la distribution en observation uniquement, le nettoyage de l'historique de groupe, les abandons de contrôle préalable, les adaptateurs personnalisés et la finalisation de distribution échouée.
- `src/channels/turn/durable-delivery.test.ts:72` à `src/channels/turn/durable-delivery.test.ts:192` couvrent les cibles null explicites, le repli de thread, la réconciliation d'envoi inconnu et les défaillances partielles.
- `src/channels/message/send.test.ts:66` à `src/channels/message/send.test.ts:626` couvrent le rendu d'envoi durable, les plans rejouables, les signaux, la politique de file d'attente, les reçus multipartites, l'édition/suppression, les envois supprimés, l'annulation de hook, les défaillances partielles et les hooks d'échec.
- `src/channels/message/outbound-bridge.test.ts:27` à `src/channels/message/outbound-bridge.test.ts:229` couvrent le texte, la charge utile riche, les reçus de sondage, les méthodes déclarées, les accusés de réception, et les métadonnées de cycle de vie.
- `src/channels/message/capabilities.test.ts:4` à `src/channels/message/capabilities.test.ts:43` couvrent les exigences de livraison finale durable.
- `src/channels/draft-stream-loop.test.ts:30` à `src/channels/draft-stream-loop.test.ts:156` couvrent les défaillances de vidage en arrière-plan et la préservation du texte en attente.
- `src/channels/status-reactions.test.ts:198` à `src/channels/status-reactions.test.ts:654` couvrent le comportement du contrôleur de réaction, la déduplication, le nettoyage, les emojis personnalisés, le timing, les erreurs et les constantes.

## Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "channel outbound delivery reply pipeline durable receipt" --json --limit 8`

Résultats :

- N'a retourné aucun résultat, ce qui est neutre après les vérifications de fraîcheur et suggère aucun large cluster actuel avec ces termes de framework exacts.

Requête : `gitcrawl search openclaw/openclaw --query "empty assistant delivery Telegram topic channel delivery" --json --limit 8`

Résultats :

- A retourné le problème #87711 concernant la livraison d'assistant vide sur un sujet Telegram.
- A retourné le problème #48709 concernant les défaillances de livraison Telegram causées par du texte/outil mixte.
- A retourné le problème #87744 concernant les tours Telegram soutenus par Codex qui expirent.

Requête : `gitcrawl search openclaw/openclaw --query "Telegram action replies durable Slack delivered finals iMessage duplicate approval sends" --json --limit 8`

Résultats :

- N'a retourné aucun résultat gitcrawl pour la formulation de note de version ; discrawl a trouvé la mise à jour du responsable correspondante.

## Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channel outbound delivery reply pipeline durable receipt" --limit 8`

Résultats :

- A retourné null, ce qui est neutre après les vérifications de fraîcheur.

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "empty assistant delivery Telegram topic channel delivery" --limit 8`

Résultats :

- A retourné null, ce qui est neutre après les vérifications de fraîcheur.

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "Telegram action replies durable iMessage duplicate approval sends Slack delivered finals" --limit 8`

Résultats :

- A retourné une note de version du 2026-05-27 indiquant que la livraison de canal a reçu un nettoyage : les réponses d'action Telegram sont durables, iMessage évite les envois d'approbation en double, Slack conserve les finales livrées, les mentions Matrix se comportent correctement et les avertissements d'outil récupérés Discord restent en dehors des réponses réussies.
