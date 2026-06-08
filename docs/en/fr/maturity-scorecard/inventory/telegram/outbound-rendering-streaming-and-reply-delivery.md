---
title: "Telegram - Note de maturité sur la livraison des messages et les médias enrichis"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Note de maturité sur la livraison des messages et les médias enrichis

## Résumé

Le texte sortant, le formatage, les aperçus en streaming, le threading des réponses et la livraison durable figurent parmi les domaines les mieux couverts de Telegram. L'implémentation gère le rendu HTML, le fallback, le chunking, les éditions d'aperçu, les voies de progression, les citations natives, les clôtures de réponse et les accusés de livraison. La qualité reste en Beta car les problèmes récents montrent toujours un comportement de pièces jointes/abandon, des changements de déduplication de flux d'aperçu, des corrections de chunking de tableau et une variation du comportement de progression visible par l'utilisateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Téléchargement de médias entrants : Téléchargement de médias entrants, espaces réservés, gestion de la taille des fichiers, groupes de médias, local
- Notes vocales : Notes vocales, fichiers audio, notes vidéo, légendes, autocollants, cache d'autocollants et gestion du téléchargement de médias.
- Localisation : Extraction de localisation et de lieu dans le contexte du canal
- Envoi de sondages : Envoi de sondages, portes d'action de sondage, drapeaux de durée/confidentialité des sondages Telegram et routage des réponses.
- Réactions : Réactions, réactions d'accusé de réception, notifications de réaction et cache de messages envoyés
- Texte : Rendu de texte et HTML, conversion de type Markdown, fallback d'analyse, aperçu de lien
- Streaming d'aperçu : Streaming d'aperçu, mode de progression, brouillons de progression d'outil natif, raisonnement
- Balises de threading de réponse : Balises de threading de réponse, citations natives, paramètres de réponse, contexte de chaîne de réponse et ciblage de message.
- Enregistrement durable des messages sortants : Enregistrement durable des messages sortants, cache de messages, résultats de livraison, nouvelle tentative et état de livraison.

## Fonctionnalités

- Téléchargement de médias entrants : Téléchargement de médias entrants, espaces réservés, gestion de la taille des fichiers, groupes de médias, local
- Notes vocales : Notes vocales, fichiers audio, notes vidéo, légendes, autocollants, cache d'autocollants et gestion du téléchargement de médias.
- Localisation : Extraction de localisation et de lieu dans le contexte du canal
- Envoi de sondages : Envoi de sondages, portes d'action de sondage, drapeaux de durée/confidentialité des sondages Telegram et routage des réponses.
- Réactions : Réactions, réactions d'accusé de réception, notifications de réaction et cache de messages envoyés
- Texte : Rendu de texte et HTML, conversion de type Markdown, fallback d'analyse, aperçu de lien
- Streaming d'aperçu : Streaming d'aperçu, mode de progression, brouillons de progression d'outil natif, raisonnement
- Balises de threading de réponse : Balises de threading de réponse, citations natives, paramètres de réponse, contexte de chaîne de réponse et ciblage de message.
- Enregistrement durable des messages sortants : Enregistrement durable des messages sortants, cache de messages, résultats de livraison, nouvelle tentative et état de livraison.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  la base de code dispose de tests dédiés pour l'envoi, la livraison, le formatage, le flux de brouillon,
  les paramètres de réponse, le streaming d'aperçu, les clôtures de réponse, la livraison de voie et les scénarios de streaming QA en direct.
- Signaux négatifs :
  la preuve en direct est optionnelle pour certains chemins finaux longs et de streaming, et elle ne
  couvre pas toutes les branches de texte plus média, mode de réponse et fallback d'erreur.
- Lacunes d'intégration :
  ajouter une preuve de version pour les citations de réponse sélectionnées, le fallback final porteur de médias,
  les brouillons de progression d'outil natif, le chunking long et le mode de progression sous latence Telegram réelle.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl :
  #72860, #75156, #75498, #85098, #83161, #77211, #84558 et #87425 montrent une variation récente dans la livraison de médias/texte, le streaming, les tableaux et les réponses réservées aux outils.
- Rapports Discrawl :
  les notes de version pour 2026.5.26 et 2026.5.27 mentionnent la dactylographie/progression Telegram,
  les réponses d'action durable et le renforcement des réponses visibles ; le chat des contributeurs a également
  signalé une dégradation de `/verbose`/progression d'outil.
- Bonnes qualités :
  la livraison est explicite sur les modes de fallback, le threading de réponse, l'échec d'analyse,
  le nettoyage d'aperçu obsolète et l'enregistrement durable des messages.
- Mauvaises qualités :
  le comportement sortant a de nombreux modes visibles et des régressions récentes visibles par l'utilisateur,
  de sorte que les opérateurs peuvent voir une livraison incorrecte même lorsque la passerelle reste active.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue du QA en direct et le nombre de tests n'ont pas
  été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le téléchargement de médias entrants, les notes vocales, la localisation, l'envoi de sondages, les réactions, le texte, le streaming d'aperçu, les balises de threading de réponse, l'enregistrement durable des messages sortants.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Maintenir le streaming, le threading de réponse et la livraison finale porteur de médias dans l'ensemble de fumée de version.
- Ajouter des diagnostics visibles par l'utilisateur pour quand l'édition d'aperçu est intentionnellement ignorée.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente l'aperçu du flux en direct,
  le formatage et le fallback HTML, les balises de threading de réponse, les contrôles d'erreur,
  les limites de chunk de texte, le mode chunk, la nouvelle tentative et le contexte de chaîne de réponse.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-dispatch.ts`
  possède la dispatch de réponse, le streaming d'aperçu, les voies de progression, les brouillons de progression d'outil natif,
  le flux de raisonnement et le fallback de livraison.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/send.ts` possède l'envoi de texte Telegram,
  le fallback HTML, le chunking, les nouvelles tentatives, la dactylographie, les éditions et les paramètres de thread.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/format.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/draft-stream.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/lane-delivery.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/telegram-reply-fence.ts`
  implémentent le rendu, le streaming, les voies et le comportement de clôture de réponse.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot/delivery.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot/reply-threading.ts`
  gèrent la livraison finale et les balises de réponse.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/telegram/telegram-live.runtime.ts`
  inclut le flux-final, la réutilisation d'aperçu final long, le final à trois chunks, le marqueur exact et les scénarios de message mentionné.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-rtt-driver.mjs`
  mesure le RTT de réponse du groupe Telegram et les messages SUT observés.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/send.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/telegram-outbound.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot/delivery.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/draft-stream.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/format.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/reply-parameters.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/lane-delivery.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/telegram-reply-fence.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/native-tool-progress-draft.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "telegram outbound streaming reply media" --json`

Résultats :

- #72860 problème ouvert : les réponses ordinaires de l'assistant peuvent perdre les pièces jointes d'image tandis que le texte est toujours livré.
- #75156 problème ouvert : la première réponse de l'assistant peut livrer du texte mais abandonner la pièce jointe.
- #85098 PR ouvert : honorer le mode tableau lors du chunking.
- #83161 PR ouvert : déplacer la déduplication en flux d'aperçu vers la couche de canal.

Requête :

`gitcrawl search openclaw/openclaw --query "telegram" --json`

Résultats :

- #77211 PR ouvert : préserver la progression d'outil par défaut lorsque le streaming d'aperçu est désactivé.
- #87425 PR ouvert : préserver le pied de page `/usage` pour les réponses réservées aux outils.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram commands"`

Résultats :

- `maintainers`, 2026-05-29 : les correctifs adjacents à la version incluaient une formulation Telegram obsolète autour de `/reasoning stream`.
- `clawtributors`, 2026-05-29 : les utilisateurs ont signalé une dégradation de Telegram `/verbose` après la mise à jour de 5.22 à 5.27.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram media attachment"`

Résultats :

- `releases`, 2026-05-28 : les notes de version ont mis en évidence les réponses Telegram durables `sendMessage`.
- `general`, 2026-05-28 : l'appel de test bêta a demandé aux utilisateurs de tester les réponses Telegram durables `sendMessage`.
