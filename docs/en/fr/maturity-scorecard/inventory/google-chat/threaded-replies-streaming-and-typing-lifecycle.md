---
title: "Google Chat - Threaded Replies Streaming and Typing Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Threaded Replies Streaming and Typing Lifecycle Maturity Note

## Summary

Les réponses en fil de discussion et le cycle de vie de la saisie sont la famille Google Chat la plus faible en trafic élevé. La source dispose de champs de fil explicites, d'options de secours API, d'un comportement de réponse durable et d'une logique de mise à jour/secours des espaces réservés de saisie, mais les preuves d'archive actuelles sont denses avec des fuites de fil ouvertes, des espaces réservés de saisie obsolètes, du markdown brut, `replyToMode`, et des problèmes de livraison d'outils de message.

## Category Scope

Cette note couvre la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, la coalescence du streaming de blocs, les réponses finales durables, les modes d'indicateur de saisie, le comportement de mise à jour/suppression/secours des espaces réservés, le cycle de vie `NO_REPLY`, et le placement des réponses de source actuelle de l'outil de message. Elle exclut la configuration/authentification, la politique d'admission d'espace, l'authentification de téléchargement de médias et le comportement générique du pipeline de réponse en dehors de l'adaptateur Google Chat.

## Features

- Thread-aware replies: Couvre les réponses conscientes du fil de discussion dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé du streaming de réponses en fil de discussion et du cycle de vie de la saisie.
- Streaming and chunked replies: Couvre les réponses en streaming et segmentées dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé du streaming de réponses en fil de discussion et du cycle de vie de la saisie.
- Typing placeholder lifecycle: Couvre le cycle de vie de l'espace réservé de saisie dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé du streaming de réponses en fil de discussion et du cycle de vie de la saisie.
- Message-tool current-source replies: Couvre les réponses de source actuelle de l'outil de message dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé du streaming de réponses en fil de discussion et du cycle de vie de la saisie.
- NO_REPLY cleanup: Couvre le nettoyage `NO_REPLY` dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé du streaming de réponses en fil de discussion et du cycle de vie de la saisie.
- Markdown/text rendering: Couvre le rendu Markdown/texte dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé du streaming de réponses en fil de discussion et du cycle de vie de la saisie.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Coverage Score

- Score: `Alpha (57%)`
- Positive signals: Les tests locaux couvrent l'omission de métadonnées de fil DM, la suppression de boucle de bot avant la saisie, les avertissements de secours en mode réaction et les chemins de livraison de réponse tels que la mise à jour/suppression de l'espace réservé de saisie et le secours texte+média. L'expéditeur API définit l'option de secours de message en fil de Google Chat lorsqu'un fil est fourni.
- Negative signals: Je n'ai trouvé aucun scénario de réponse en fil de discussion Google Chat en direct et aucune version standard prouvant les longues réponses en streaming, les réponses visibles de l'outil de message, les suites en attente, `replyToMode: "off"`, et le nettoyage `NO_REPLY` dans un fil d'espace Google Chat réel.
- Integration gaps: Ajouter des scénarios de fil en direct pour réponse courte, réponse longue segmentée, streaming de blocs, réponse de l'outil de message à la source actuelle, `replyToMode: "off"` explicite, réponse média+texte, et `NO_REPLY` après sortie réaction/action uniquement.

## Quality Score

- Score: `Alpha (52%)`
- Gitcrawl reports: Les problèmes ouverts incluent #80995 pour les réponses de l'outil de message s'échappant des fils, #82014 pour les réponses de l'outil de message ne modifiant pas les espaces réservés de saisie, #44347 pour les réponses en fil de discussion de base et la livraison d'espace tous les messages, #42510 pour `replyToMode: "off"` ne supprimant pas les fils, #69422 pour les métadonnées de fil fuyant à travers les réponses de bloc en streaming, #39843 pour les indicateurs de saisie persistant après `NO_REPLY` plus réaction, et #49350 pour le markdown brut plus la mauvaise identité de saisie. Les #64313/#70041 fermés montrent les corrections récentes de placement de fil/chunk de retry mais n'effacent pas l'ensemble ouvert actif.
- Discrawl reports: `discrawl search "Google Chat thread replies" --limit 10` a retourné les demandes de test de version bêta pour le comportement de fil DM Google Chat, les commentaires de reproduction #69422, la fuite de chunk #70041, et la discussion de secours de fil #64313. `discrawl search "Google Chat typing indicator" --limit 10` a retourné #39843, #71498, #70923, #67055, #65570, et les commentaires associés autour de la saisie obsolète et les corrections de perte de texte silencieuse.
- Good qualities: L'adaptateur utilise le nom de fil de Google Chat en contexte, définit `messageReplyOption` pour le secours de fil, peut mettre à jour un espace réservé de saisie dans le premier chunk, supprime les espaces réservés avant les envois de médias, revient à des envois frais si les modifications échouent, et rend le mode de saisie de réaction explicite comme non pris en charge avec l'authentification du compte de service.
- Bad qualities: Le modèle de réponse fuit toujours les détails du cycle de vie spécifiques au canal. Les réponses de l'outil de message contournent le nettoyage normal des espaces réservés, les chunks en streaming de blocs peuvent perdre l'identité du fil, `NO_REPLY` peut laisser des messages de saisie visibles, le rendu markdown ne correspond pas aux attentes de Google Chat, et la sémantique du mode de réponse a dérivé de l'attente de l'utilisateur.
- Excluded from quality: La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Completeness Score

- Score: `Alpha (57%)`
- Surface instructions: évalué par rapport à `references/completeness/google-chat.md`.
- Positive signals: les preuves archivées, source, test, Gitcrawl et Discrawl couvrent l'étendue de la taxonomie pour les réponses conscientes du fil, les réponses en streaming et segmentées, le cycle de vie de l'espace réservé de saisie, les réponses de source actuelle de l'outil de message, le nettoyage `NO_REPLY`, le rendu Markdown/texte.
- Negative signals: la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Missing capability branches: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Faire de l'identité du fil un champ sortant de première classe dans les charges utiles de réponse, la coalescence de blocs, les files d'attente de suivi, les envois d'outils de message et les reçus de livraison.
- Nettoyer les espaces réservés de saisie pour les réponses de l'outil de message de source actuelle et les chemins `NO_REPLY` exacts.
- Assurer que `replyToMode: "off"` supprime toute propagation de fil Google Chat, y compris les messages de saisie et les réponses de médias.
- Convertir ou supprimer Markdown de manière cohérente pour les règles de rendu en texte brut de Google Chat.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md`: documente les clés de session groupe/DM, `replyToMode`, `typingIndicator`, les actions de message, les champs cibles de fil, et le dépannage.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md`: documente `blockStreamingCoalesce` et note les valeurs par défaut de Google Chat parmi les remplacements de canal.
- `/Users/kevinlin/code/openclaw/docs/concepts/message-lifecycle-refactor.md`: appelle le comportement de l'adaptateur de réception/envoi de Google Chat avec les relations de fil mappées aux espaces et aux identifiants de fil.

### Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.ts`: extrait le `message.thread.name` entrant, construit le contexte de réponse, envoie les messages de saisie et achemine la livraison via le runner entrant du canal partagé.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-durable.ts`: active uniquement le secours final durable lorsqu'aucun espace réservé de saisie ne possède la livraison visible.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-reply-delivery.ts`: met à jour ou supprime les espaces réservés de saisie, segmente le texte, envoie les réponses de médias, télécharge les pièces jointes et revient lorsque les modifications d'espace réservé échouent.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/api.ts`: envoie les messages avec le corps `thread` optionnel et `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.adapters.ts`: configure la segmentation sortante, le mode de livraison directe et la gestion des cibles de fil/réponse pour les résultats attachés.

### Integration tests

- Aucun scénario de fil/saisie Google Chat en direct dédié n'a été trouvé sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/ui/src/ui/e2e/chat-flow.e2e.test.ts` couvre WebChat, pas Google Chat, et a été traité comme hors de portée.

### Unit tests

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.test.ts`: couvre la suppression de boucle de bot avant la saisie et le contexte de réponse DM omettant les métadonnées de fil.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.reply-delivery.test.ts`: couvre le comportement de livraison de réponse Google Chat autour des messages de saisie, la livraison texte/médias et les chemins de secours.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.test.ts`: couvre les métadonnées du plugin de canal/capacités adjacentes au fil et au streaming de blocs.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/actions.test.ts`: couvre les envois d'outils de message avec `threadId`, ce qui est pertinent pour le placement des réponses de source actuelle.

### Gitcrawl queries

Query:

`gitcrawl search issues "Google Chat" --repo openclaw/openclaw --limit 20 --json number,title,state,updatedAt,url`

Results:

- A retourné les problèmes de fil/saisie ouverts #80995, #82014, #44347, #49350, #42510, #69422, et #39843.

Query:

`gitcrawl gh issue view 69422 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Results:

- A retourné l'ouverture #69422, signalant que les chunks Google Chat en streaming atterrissent en dehors du fil d'origine car l'identité sortante/coalesceur ne porte pas les métadonnées de fil.

Query:

`gitcrawl gh issue view 82014 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Results:

- A retourné l'ouverture #82014, signalant que les réponses de l'outil de message contournent le cycle de vie de mise à jour de l'espace réservé Google Chat et laissent des messages `_BotName is typing..._` obsolètes.

Query:

`gitcrawl gh issue view 39843 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Results:

- A retourné l'ouverture #39843, signalant un indicateur de saisie persistant après un flux de réaction plus `NO_REPLY`.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search "Google Chat thread replies" --limit 10`

Results:

- A retourné les conseils de test de version bêta pour le comportement de fil DM Google Chat, la discussion de reproduction #69422, la fuite de chunk #70041, et les commentaires de secours de fil #64313.

Query:

`/Users/kevinlin/.local/bin/discrawl search "Google Chat typing indicator" --limit 10`

Results:

- A retourné les discussions actives et récentes du cycle de vie de saisie incluant #39843, #71498, #70923, #67055, et #65570, couvrant les espaces réservés obsolètes, la perte de texte silencieuse, replyToMode, et le nettoyage média+texte.
