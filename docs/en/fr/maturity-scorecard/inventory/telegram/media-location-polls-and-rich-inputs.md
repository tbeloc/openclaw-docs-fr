---
title: "Telegram - Note de maturité des médias et du contenu enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Note de maturité des médias et du contenu enrichi

## Résumé

Le support des médias et des entrées enrichies de Telegram est large : les photos, documents, audio, voix,
vidéo, autocollants, groupes de médias, réactions, emplacements, lieux et sondages ont tous
des ancres source. C'est toujours en version bêta car les limites de l'API Bot de Telegram, les protections SSRF,
l'hydratation des autocollants, la livraison texte-plus-média et le comportement des sondages dans les forums créent
une grande matrice de cas limites.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Médias et contenu enrichi`
- Fusionnée à partir de : `Livraison de messages et médias enrichis`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Téléchargement de médias entrants : Téléchargement de médias entrants, espaces réservés, gestion de la taille des fichiers, groupes de médias, comportement local
- Notes vocales : Notes vocales, fichiers audio, notes vidéo, légendes, autocollants, cache d'autocollants et gestion du téléchargement de médias.
- Localisation : Extraction de localisation et de lieu dans le contexte du canal
- Envoi de sondages : Envoi de sondages, portes d'action de sondage, drapeaux de durée/confidentialité des sondages Telegram et routage des réponses.
- Réactions : Réactions, réactions d'accusé de réception, notifications de réaction et cache de messages envoyés
- Texte : Rendu de texte et HTML, conversion de type Markdown, repli d'analyse, aperçu de lien
- Diffusion en continu d'aperçu : Diffusion en continu d'aperçu, mode de progression, brouillons de progression d'outil natif, raisonnement
- Balises de fil de réponse : Balises de fil de réponse, guillemets natifs, paramètres de réponse, contexte de chaîne de réponse et ciblage de messages.
- Enregistrement durable des messages sortants : Enregistrement durable des messages sortants, cache de messages, résultats de livraison, nouvelle tentative et état de livraison.
- Notes vocales : Notes vocales, fichiers audio, notes vidéo, légendes, autocollants, cache d'autocollants et gestion du téléchargement de médias
- Envoi de sondages : Envoi de sondages, portes d'action de sondage, drapeaux de durée/confidentialité des sondages Telegram et routage des réponses
- Balises de fil de réponse : Balises de fil de réponse, guillemets natifs, paramètres de réponse, contexte de chaîne de réponse et ciblage de messages
- Enregistrement durable des messages sortants : Enregistrement durable des messages sortants, cache de messages, résultats de livraison, nouvelle tentative et état de livraison
- Téléchargement de médias entrants : Couvre le téléchargement de médias entrants, les espaces réservés, la gestion de la taille des fichiers, les groupes de médias et le comportement local.
- Notes vocales : Couvre les notes vocales, les fichiers audio, les notes vidéo, les légendes, les autocollants, le cache d'autocollants et le comportement.
- Extraction de localisation et de lieu dans le contexte du canal : Portée des preuves pour l'extraction de localisation et de lieu dans le contexte du canal
- Envoi de sondages : Couvre l'envoi de sondages, les portes d'action de sondage, les drapeaux de durée/confidentialité des sondages Telegram et le comportement.
- Réactions : Couvre les réactions, les réactions d'accusé de réception, les notifications de réaction et le comportement du cache de messages envoyés.

## Fonctionnalités

- Médias et contenu enrichi : Portée des preuves pour les médias et le contenu enrichi.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (74%)`
- Signaux positifs :
  de nombreuses branches de médias ont des tests unitaires et d'exécution, et la documentation explique le comportement audio, vidéo, autocollant, réaction, localisation et sondage visible par l'utilisateur.
- Signaux négatifs :
  les scénarios de paquets en direct ne couvrent pas toute la matrice média/localisation/sondage, et plusieurs chemins de médias dépendent de limites de l'API Bot ou de la mise en réseau de l'hôte.
- Lacunes d'intégration :
  ajouter une preuve en direct pour l'image, le document, la voix, la note vidéo, l'autocollant, la localisation,
  le lieu, le groupe de médias, le sondage, la livraison de fichier surdimensionné et le sondage ciblé par sujet.

## Score de qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl :
  #75156, #55917, #40991, #41779, #83748, #86161, #86176 et #80243 montrent des risques récents
  ou ouverts liés aux médias, autocollants, pièces jointes et actions d'édition.
- Rapports Discrawl :
  les notes de version signalent les corrections de médias de canal, mais le trafic des responsables/utilisateurs traite toujours
  les chemins de médias et de pièces jointes de Telegram comme une zone sujette aux régressions.
- Bonnes qualités :
  le téléchargement de médias est limité, la politique SSRF est explicite, les espaces réservés préservent
  la continuité des messages, les portes de sondage sont explicites et les entrées enrichies sont normalisées
  dans le contexte du canal.
- Mauvaises qualités :
  les limites de fichier de l'API Bot Telegram, les exceptions de proxy/réseau privé, les replis d'espace réservé de médias
  et les variantes d'autocollant/vidéo maintiennent le comportement de l'opérateur variable.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue de l'assurance qualité en direct et le nombre de tests n'ont pas
  été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les médias et le contenu enrichi.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Promouvoir la localisation, le sondage, l'autocollant et la preuve de groupe de médias dans les scénarios de version récurrents.
- Ajouter un tableau de support de médias visible par l'utilisateur pour les types Telegram entrants et sortants.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente l'audio,
  la vidéo, les autocollants, les réactions, les réactions d'accusé de réception, les limites de médias, le vidage de groupe de médias,
  les sondages Telegram, les cibles de sujet et la configuration des médias/réseau.
- `/Users/kevinlin/code/openclaw/docs/channels/location.md` couvre le comportement de localisation partagée.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot/delivery.resolve-media.ts`
  télécharge les médias Telegram avec la politique SSRF, la nouvelle tentative, la gestion de la taille, les racines locales de confiance
  et le repli d'espace réservé.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot/body-helpers.ts`
  extrait les localisations et les lieux.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.ts`
  porte la localisation et le contexte de médias dans les tours.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/send.ts` implémente
  les envois de médias, le comportement des notes vocales/vidéo et `sendPollTelegram`.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/sticker-cache.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/voice.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/poll-visibility.ts`
  implémentent le comportement spécifique aux autocollants, voix et sondages.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/telegram/telegram-live.runtime.ts`
  enregistre les types de médias observés et les métadonnées de bouton en ligne dans les artefacts en direct.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-rtt-driver.mjs`
  exerce la mécanique en direct de l'API Bot utilisée par les scénarios de message et de médias,
  bien que pas chaque variante de médias.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot.media.downloads-media-file-path-no-file-download.e2e.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot.media.stickers-and-fragments.e2e.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-dispatch.media-dedup.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-dispatch.sticker-media.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/sticker-cache.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/voice.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/poll-visibility.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/send.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Telegram attachment media" --json`

Résultats :

- #75156 problème ouvert : la première réponse de l'assistant peut livrer du texte mais supprimer la pièce jointe.
- #55917 problème ouvert : les documents Telegram arrivent parfois uniquement sous la forme
  `<media:document>`.
- #40991 problème ouvert : la vidéo entrante peut se dégrader en espace réservé `<media:video>`
  quand `getFile()` échoue.
- #41779 problème ouvert : l'action d'envoi de message ignore le tampon/nom de fichier pour les
  pièces jointes Telegram.
- #83748 problème ouvert : les autocollants entrants ne sont pas hydratés en tant que médias lisibles par l'agent.

Requête :

`gitcrawl search openclaw/openclaw --query "inline keyboard" --json`

Résultats :

- #86161 problème ouvert et #86176 PR ouvert : les éditions de messages de médias Telegram ont besoin
  du support de légende/reply-markup.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram media attachment"`

Résultats :

- `releases`, 2026-05-28 : le nettoyage de livraison de canal a signalé les réponses d'action durables de Telegram.
- `general`, 2026-05-28 : la demande de test bêta incluait les réponses durables `sendMessage` de Telegram
  sous les tests de canal.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram"`

Résultats :

- `clawtributors`, 2026-05-29 : l'utilisateur a dit que les sujets DM Telegram se cassent plus souvent
  et a décrit l'utilisation de groupes 1:1 avec des fils pour la communication persistante.
