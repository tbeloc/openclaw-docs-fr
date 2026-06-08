---
title: "Discord - Message and Media Delivery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Message and Media Delivery Maturity Note

## Summary

Cette note migre les preuves de maturité archivées pour `Discord` / `Outbound Message Rendering and Delivery` dans l'inventaire de scorecard de la version actuelle du processus-version-3.

## Category Scope

Inclus dans cette catégorie :

- Direct and thread sends: Couvre les envois directs et les envois de threads. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- Text chunking and reply mode: Couvre le chunking de texte et le mode de réponse. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- Draft and progress edits: Couvre les brouillons et les éditions de progression. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- Mention and embed rendering: Couvre le rendu des mentions et des embeds. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- REST retry and final delivery: Couvre les tentatives REST et la livraison finale. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- File uploads: Téléchargements de fichiers sortants à partir d'URL et de chemins locaux, y compris les contraintes de livraison et le comportement de suivi.
- Component file and media-gallery blocks: Blocs de fichiers et de galerie de médias du composant v2 pour la livraison de médias Discord.
- Video caption follow-up: Gestion des légendes vidéo et livraison de suivi réservée aux médias dans les conversations Discord.
- Voice-message upload: Envois de messages vocaux Discord avec conversion OGG/Opus, génération de forme d'onde, métadonnées de durée et gestion d'URL de téléchargement.
- Inbound attachment context: Contexte de pièce jointe entrante mis à disposition pour les réponses Discord et les tours d'agent.

## Features

- Direct and thread sends: Couvre les envois directs et les envois de threads. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- Text chunking and reply mode: Couvre le chunking de texte et le mode de réponse. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- Draft and progress edits: Couvre les brouillons et les éditions de progression. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- Mention and embed rendering: Couvre le rendu des mentions et des embeds. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- REST retry and final delivery: Couvre les tentatives REST et la livraison finale. Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, chunking de texte, suivi de médias, et comportement de rendu et de livraison de messages sortants associés.
- File uploads: Téléchargements de fichiers sortants à partir d'URL et de chemins locaux, y compris les contraintes de livraison et le comportement de suivi.
- Component file and media-gallery blocks: Blocs de fichiers et de galerie de médias du composant v2 pour la livraison de médias Discord.
- Video caption follow-up: Gestion des légendes vidéo et livraison de suivi réservée aux médias dans les conversations Discord.
- Voice-message upload: Envois de messages vocaux Discord avec conversion OGG/Opus, génération de forme d'onde, métadonnées de durée et gestion d'URL de téléchargement.
- Inbound attachment context: Contexte de pièce jointe entrante mis à disposition pour les réponses Discord et les tours d'agent.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Stable (84%)`

La couverture est forte pour le chemin d'exécution principal. L'arborescence source a une couverture réelle d'envoi/relecture Discord via le script e2e macOS Parallels, les scénarios en direct du laboratoire QA pour les réponses canary, les réponses de threads/fichiers, les réactions de statut et les flux gérés par mention, plus les tests de flux d'exécution pour la finalisation de l'aperçu des brouillons, la livraison de secours standard, l'utilisation de références de réponse, le secours média/erreur, les éditions de progression, la sortie finale chunked et la livraison durable partagée.

La couverture n'est pas plus élevée car la preuve en direct/e2e n'est pas une seule matrice de bout en bout qui exerce chaque option sortante risquée ensemble. Le chunking, `replyToMode`, la suppression d'embed, la réécriture d'alias de mention, le comportement de reconnexion/tentative, les brouillons de progression en streaming et le suivi de médias ont chacun des preuves, mais plusieurs sont prouvés par des harnais de flux d'exécution ou au niveau de l'adaptateur plutôt que par une exécution de transport Discord en direct. Gitcrawl a également toujours des rapports d'exécution ouverts autour de la perte de livraison de reconnexion, des lacunes de brouillon de progression et de l'échec sortant déclenché par TTS/voix, donc la surface d'intégration est large mais pas entièrement scellée par une preuve en direct.

## Quality Score

- Score: `Beta (76%)`

L'implémentation a une architecture cohérente : Discord utilise le pipeline sortant partagé, retourne des reçus, applique des drapeaux de message explicites, chunke le texte avant d'atteindre les limites Discord, supprime les embeds d'URL par défaut, supporte les embeds explicites et les charges utiles du composant v2, réécrit les alias de mention configurés, préserve les références de réponse sur les envois chunked, émet des éditions de brouillon/progression en direct et enveloppe les envois sortants directs avec la gestion des tentatives REST. La gestion des erreurs est également utile en pratique : les défaillances de permission manquante, DM bloqué, envoi de thread, pièce jointe et visibilité de canal sont mappées à des erreurs spécifiques à Discord exploitables.

La qualité est maintenue à Beta par le risque opérationnel actuel, non par le nombre de tests. Gitcrawl et discrawl montrent tous deux des problèmes de qualité de livraison actifs ou récents : les fenêtres de reconnexion peuvent perdre des messages sortants sans une file d'attente durable, le mode de progression peut produire du silence ou écraser le texte de raisonnement antérieur, le streaming partiel/bloc peut afficher des fragments de mi-sortie trompeurs, les chemins cron/TTS peuvent signaler le succès tandis que la livraison Discord ne se produit pas, et le comportement de mention de réponse reste ambigu pour certains modes de réponse natifs. Il y a aussi un rapport de sécurité/qualité ouvert sur la fuite de métadonnées dans la livraison de threads Discord, même si la source actuelle achemine maintenant les charges utiles de canal frontal final via les chemins de désinfectant. Ce sont des risques de livraison et de rendu visibles par l'utilisateur dans la surface de canal actif.

Les entrées de qualité excluent délibérément le volume de test unitaire, les tests manquants et la profondeur d'intégration générale. Le score est basé sur l'architecture, le comportement de la source actuelle, la sémantique documentée et les rapports en direct/archivés des défaillances de rendu et de livraison sortants.

## Completeness Score

- Score: `Stable (84%)`
- Surface instructions: evaluated against `references/completeness/discord.md`.
- Positive signals: archived docs, source, test, Gitcrawl, and Discrawl evidence cover the taxonomy scope for Direct and thread sends, Text chunking and reply mode, Draft and progress edits, Mention and embed rendering, REST retry and final delivery, File uploads, Component file and media-gallery blocks, Video caption follow-up, Voice-message upload, Inbound attachment context.
- Negative signals: the archived note predated process-version-3 Completeness scoring, so this score is initialized from the same evidence breadth and known-gap record used for the archived Coverage score.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- See the score-specific negative signals and archived evidence below.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:212` documente la sélection de jetons par appel pour les envois sortants avancés et la politique de nouvelle tentative spécifique au compte.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:343` indique que les résultats d'interaction du composant v2 Discord reviennent à la même conversation et suivent `replyToMode`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:648` documente `channels.discord.replyToMode`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:667` documente la suppression d'intégration de lien générée par défaut, les remplacements par compte, la suppression par message `suppressEmbeds: false`, et la distinction par rapport aux intégrations explicites.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:684` documente les réponses de brouillon en continu et les modes `off`, `partial`, `block` et `progress`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:979` documente `mentionAliases` pour les mentions sortantes déterministes.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1117` énumère les actions de message sortant incluant `sendMessage`, `editMessage`, `deleteMessage` et `threadReply`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1137` documente le support de charge utile des composants v2, les intégrations héritées et les valeurs par défaut de suppression d'aperçu d'URL.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1716` regroupe la référence de configuration pour `replyToMode`, `textChunkLimit`, `chunkMode`, `maxLinesPerMessage`, les paramètres de diffusion en continu, les médias et les nouvelles tentatives.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-outbound.md:2` décrit l'API de cycle de vie sortant partagée pour les envois durables, les reçus, l'aperçu en direct et les assistants du pipeline de réponse.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-outbound.md:14` divise les responsabilités entre la couche de file d'attente/durabilité/nouvelle tentative/crochets/reçus du noyau et la couche d'envoi/édition/suppression native du plugin.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-outbound.md:95` documente la diffusion en continu de brouillon, les assistants de progression et les résultats de charge utile envoyée/supprimée/échouée.

## Source

- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.message-request.ts:47` construit les charges utiles de message Discord, gère les charges utiles du composant v2, les intégrations, les fichiers, les drapeaux et les références de réponse avec `fail_if_not_exists: false`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/chunk.ts:148` divise le texte sortant par caractère et limites de lignes souples tout en préservant les blocs de code clôturés.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.shared.ts:157` mappe les échecs d'envoi Discord en erreurs exploitables pour les permissions manquantes, les MP bloqués, la permission d'envoi de fil et la permission de pièce jointe.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.shared.ts:296` envoie du texte divisé, applique les composants et les intégrations uniquement au premier morceau, préserve les drapeaux et porte les références de réponse à travers les morceaux.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.shared.ts:355` envoie des médias avec division de légende, références de réponse, morceaux de suivi et identifiants de message de plateforme retournés.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.outbound.ts:148` résout la configuration Discord sortante, le compte, la division, les lignes max, la suppression d'intégration, les alias de mention, les destinataires de canal et les chemins d'envoi de texte/médias.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.outbound.ts:187` gère les envois de démarrage de fil de forum/canal de médias et la livraison de suivi dans le fil créé.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/mentions.ts:94` réécrit les alias de mention en texte brut configurés/sauvegardés en cache tout en préservant les poignées inconnues, les mentions réservées et les portées de code.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/draft-stream.ts:55` crée et édite des aperçus de brouillon en direct avec les limites de taille Discord, les références de réponse, `allowed_mentions: { parse: [] }` et les drapeaux de suppression d'intégration.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.draft-preview.ts:46` résout les modes de diffusion en continu et crée des contrôleurs d'aperçu de brouillon pour le comportement partiel, bloc et progression.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.process.ts:599` finalise un aperçu de brouillon sûr par édition, sinon revient à la livraison Discord standard pour les médias, les erreurs, les balises de réponse explicites ou la sortie multi-morceau.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/reply-delivery.ts:158` assainit les charges utiles du canal avant et délègue les réponses finales via l'expéditeur de lot de message durable partagé.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/outbound-adapter.ts:106` expose les capacités de livraison directe Discord, le diviseur de texte, l'assainisseur, les drapeaux de capacité durable-final et les crochets d'envoi.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/outbound-adapter.ts:167` enveloppe les envois de texte directs avec `withDiscordDeliveryRetry` et préserve l'identité du webhook/fil si disponible.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/delivery-retry.ts:10` définit les valeurs par défaut de nouvelle tentative de livraison Discord et la classification de nouvelle tentative transitoire pour les échecs REST 429 et 5xx.
- `/Users/kevinlin/code/openclaw/src/channels/turn/durable-delivery.ts:126` implémente la livraison de réponse entrante durable final uniquement via `sendDurableMessageBatch`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.ts:85` enregistre l'adaptateur de message Discord avec aperçu de brouillon, finalisation d'aperçu, mises à jour de progression et capacités durable-final.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/macos-discord.ts:27` configure Discord dans un invité macOS, exécute `doctor --fix`, redémarre la passerelle, sonde l'état du canal, envoie un vrai message Discord, attend la visibilité de l'API hôte, publie l'entrée hôte et relit le message dans l'invité.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:49` définit des scénarios Discord en direct pour les réponses de canari, le contrôle des mentions, les pièces jointes de fichier de réponse de fil et les réactions d'état.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:289` vérifie qu'une mention du pilote de canari Discord reçoit la réponse de marqueur attendue du système en test.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:356` couvre le comportement de pièce jointe filePath de réponse de fil dans le runtime Discord en direct.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/live-smoke.live.test.ts:7` fournit une fumée en direct contrôlée pour résoudre l'identité du bot et les métadonnées de la passerelle.
- `/Users/kevinlin/code/openclaw/scripts/dev/discord-acp-plain-language-smoke.ts:685` envoie un message de pilote en direct via les chemins de jeton/webhook/CLI Discord OpenClaw et valide les identifiants de message retournés.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.process.test.ts:1848` couvre la finalisation du flux d'exécution via l'édition d'aperçu lorsque la réponse finale tient dans un seul morceau.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.process.test.ts:1866` couvre la diffusion en continu de progression dans les aperçus de brouillon Discord et le comportement d'édition d'aperçu final.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.process.test.ts:1981` couvre le repli multi-morceau à la livraison standard.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.process.test.ts:2036` couvre le nettoyage de brouillon lorsque la livraison finale de repli échoue.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.process.test.ts:2088` couvre le repli de balise de réponse explicite à la livraison standard.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.process.test.ts:2109` couvre le repli final des médias à la livraison normale et le nettoyage de brouillon.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/reply-delivery.test.ts:107` couvre le pont des réponses Discord régulières vers le sortant partagé avec `replyToMode`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/reply-delivery.test.ts:469` couvre les réponses de fil liées réécrivant la cible parent, le fil, la persona et le contexte de session.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/durable-delivery.test.ts:43` couvre la livraison finale durable en éventail des morceaux planifiés et la nouvelle tentative d'une défaillance de deuxième morceau transitoire.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.message-adapter.test.ts:78` prouve les drapeaux de capacité durable-final pour le texte, les médias, le sondage, la charge utile, le silence, la réponse, le fil et les crochets.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.message-adapter.test.ts:227` prouve les capacités d'aperçu en direct et de finaliseur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/draft-stream.test.ts:26` couvre la création/édition d'aperçu sur le même message avec références de réponse.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/draft-stream.test.ts:60` couvre la suppression de mention d'aperçu avec `allowed_mentions`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/draft-stream.test.ts:91` couvre la suppression d'intégration de lien d'aperçu.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:196` couvre les envois de base et la suppression d'intégration par défaut.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:221` couvre les remplacements `suppressEmbeds` par message et par compte.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:269` couvre les envois silencieux et les envois d'intégration explicites.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:304` couvre la réécriture de mention via le cache, les alias et la sélection de compte par défaut.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:384` couvre la livraison de fil automatique de forum et la division de suivi de forum long.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:455` couvre les MP utilisateur et les cibles numériques nues.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:491` couvre les indices de permission manquante.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:559` couvre la livraison de médias.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.sends-basic-channel-messages.test.ts:663` couvre les références de réponse à travers les morceaux et les suivis de division de légende de médias.

## Requêtes Gitcrawl

- `gitcrawl doctor --json` a vérifié la version gitcrawl `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594` et `repository_count=2`.
- `gitcrawl search issues "Discord outbound message delivery chunk replyToMode suppressEmbeds mentions retry" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` n'a retourné aucun résultat direct.
- `gitcrawl search issues "Discord preview streaming progress draft edit final delivery" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` a retourné un faux positif Mattermost, pas de preuve Discord sortante.
- `gitcrawl search issues "Discord delivery failed reply duplicate missing permissions chunk embeds" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` n'a retourné aucun résultat direct.
- `gitcrawl search issues "Discord durable delivery retry outbound message send" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` a retourné `#85422`, un problème de repli de modèle avec des symptômes de canal mais pas une cause racine Discord sortante.
- `gitcrawl search openclaw/openclaw --query "Discord replyToMode" --json` a surfacé `#51534` demandant l'injection de mention explicite pour les réponses de guilde, `#80234` sur les mentions de réponse de bot implicites, `#74077` sur les commandes de mode de diffusion en continu d'aperçu et les problèmes de routage/configuration connexes.
- `gitcrawl search openclaw/openclaw --query "Discord suppressEmbeds" --json` n'a retourné aucun résultat.
- `gitcrawl search openclaw/openclaw --query "Discord streaming progress draft" --json` a surfacé `#83307` commentaire d'assistant dans les brouillons de progression, `#85465` corrections de sortie de commande final/statut de progression, `#83983` remplacement de flux de raisonnement, `#78561` fragments partiel/bloc trompeurs et `#87704` comportement de silence mort du mode progression.
- `gitcrawl search openclaw/openclaw --query "Discord outbound delivery" --json` a surfacé `#84952` échec d'annonce cron via l'adaptateur sortant voix Discord, `#56610` file d'attente de livraison/nouvelle tentative sur reconnexion WebSocket, `#81226` remplissage de message manqué après reconnexion, `#39847` fuite de métadonnées dans la livraison sortante, `#80445` livraisons `message.send` visibles en double et les problèmes de durcissement de livraison/routage connexes.
- `gitcrawl threads openclaw/openclaw --numbers 51534,80234,83307,83983,78561,87704,56610,84952,39847,85465 --include-closed --json` a confirmé les rapports ouverts pour l'ambiguïté de mention de réponse, les lacunes de rendu/brouillon de progression, la perte de livraison de reconnexion, l'échec sortant TTS/voix et la fuite de métadonnées.
- `gitcrawl threads openclaw/openclaw --numbers 84952,85422,80445,81226 --include-closed --json` a confirmé l'échec de l'adaptateur sortant voix/TTS et les préoccupations de reconnexion/livraison en double, avec certaines preuves de PR explicitement décrites comme preuve non-production.

## Requêtes Discrawl

- `discrawl status --json` a été vérifié en direct pendant cet audit. La fraîcheur enregistrée demandée est conservée exactement dans Archive Freshness ; le statut en direct a également signalé l'état `current`, les mêmes champs de synchronisation/comptage et le partage distant `git@github.com-personal:openclaw/discord-store.git`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "Discord outbound delivery"` a trouvé une discussion opérationnelle récente de Discord TTS disant qu'un fichier opus local a été créé tandis que `lastOutboundAt` n'a pas changé et aucun envoi sortant/média Discord n'a été visible dans les journaux de passerelle ; il a également trouvé des rapports de mise à niveau/reconnexion plus anciens, une passe de réponse visible entrante/sortante beta2 et des commentaires GitHub fermant le travail de pipeline sortant partagé et de répartiteur redémarrage-sûr.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "Discord replyToMode"` a trouvé une discussion PR que `replyToMode: "all"` ne consomme plus l'état de réponse, les configurations utilisateur définissant `replyToMode: "off"` pour éviter les pings de réponse natifs et la discussion du résolveur de route connexe.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "Discord progress draft"` a trouvé une discussion actuelle sur le commentaire de diffusion en continu Discord en `mode: "progress"`, les problèmes fermés pour les aperçus de brouillon de progression d'outil en direct et les éditions d'aperçu final, et l'historique plus ancien montrant la migration de configuration du mode de diffusion en continu de l'ancien `streamMode`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "Discord delivery retry queue"` a trouvé le travail de durcissement de livraison/nouvelle tentative en double fermé, le problème de file d'attente/nouvelle tentative de reconnexion ouvert et les références de file d'attente de livraison plus anciennes pour la récupération sortante en attente.
