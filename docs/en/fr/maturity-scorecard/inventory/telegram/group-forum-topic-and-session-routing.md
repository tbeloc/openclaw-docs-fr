---
title: "Telegram - Note de maturité du routage et de la livraison des conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Note de maturité du routage et de la livraison des conversations

## Résumé

Le support des groupes Telegram, supergroupes, sujets de forum et routage de session est large mais reste l'un des composants Telegram les plus risqués. La source et la documentation couvrent les ID de groupe, les portes de mention, la configuration des sujets, les agents par sujet, la liaison des sujets ACP et les clés de session conscientes des threads. Les preuves d'archive récentes montrent toujours que les réponses de groupe et de sujet de forum sont routées au mauvais endroit, donc la qualité reste Alpha.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Routage et livraison des conversations`
- Fusionnée à partir de : `Accès et routage des conversations`, `Livraison des messages et médias enrichis`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Modes dmPolicy : appairage, liste d'autorisation, ouvert et désactivé
- Approbation du code d'appairage : approbation du code d'appairage, amorçage du premier propriétaire et commands.ownerAllowFrom
- Normalisation de l'ID utilisateur Telegram numérique avec préfixes telegram: et tg:
- allowFrom : allowFrom, groupAllowFrom, groupes d'accès et limites DM-versus-groupe
- DM non autorisé : DM non autorisé, groupe, commande, rappel et gestion des réactions
- Listes blanches de groupe : listes blanches de groupe, groupPolicy, groupAllowFrom et gestion des portes de mention
- ID de chat négatif de supergroupe : ID de chat négatif de supergroupe et héritage de configuration de groupe/sujet
- Clés de session de sujet de forum : clés de session de sujet de forum, message_thread_id, comportement du sujet Général et routage des sujets.
- Routage des sujets ACP : liaison des sujets ACP et /acp spawn --thread
- Construction de clé de session : construction de clé de session, correspondance de route de conversation et cible de réponse
- Téléchargement de médias entrants : téléchargement de médias entrants, espaces réservés, gestion de la taille des fichiers, groupes de médias, local
- Notes vocales : notes vocales, fichiers audio, notes vidéo, légendes, autocollants, cache d'autocollants et gestion du téléchargement de médias.
- Localisation : extraction de localisation et de lieu dans le contexte du canal
- Envoi de sondage : envoi de sondage, portes d'action de sondage, drapeaux de durée/confidentialité de sondage Telegram et routage des réponses.
- Réactions : réactions, réactions d'accusé de réception, notifications de réaction et cache de messages envoyés
- Texte : rendu de texte et HTML, conversion de type Markdown, repli d'analyse et aperçu de lien
- Diffusion en continu d'aperçu : diffusion en continu d'aperçu, mode de progression, brouillons de progression d'outil natif, raisonnement
- Balises de threading de réponse : balises de threading de réponse, guillemets natifs, paramètres de réponse, contexte de chaîne de réponse et ciblage de message.
- Enregistrement durable des messages sortants : enregistrement durable des messages sortants, cache de messages, résultats de livraison, nouvelle tentative et état de livraison.
- Notes vocales : notes vocales, fichiers audio, notes vidéo, légendes, autocollants, cache d'autocollants et gestion du téléchargement de médias
- Envoi de sondage : envoi de sondage, portes d'action de sondage, drapeaux de durée/confidentialité de sondage Telegram et routage des réponses
- Balises de threading de réponse : balises de threading de réponse, guillemets natifs, paramètres de réponse, contexte de chaîne de réponse et ciblage de message
- Enregistrement durable des messages sortants : enregistrement durable des messages sortants, cache de messages, résultats de livraison, nouvelle tentative et état de livraison

## Fonctionnalités

- Routage et livraison des conversations : portée des preuves pour le routage et la livraison des conversations.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  la configuration de groupe, l'accès au groupe, les ID de conversation de sujet, les liaisons de thread, les tests de route
  et les scénarios de mention de groupe en direct sont tous présents.
- Signaux négatifs :
  la preuve en direct est forte pour les mentions de groupe bot-à-bot mais plus faible pour les sujets de forum,
  les agents par sujet, la liaison des sujets ACP, la migration de groupe et la récupération de chaîne de réponse.
- Lacunes d'intégration :
  ajouter une preuve en direct récurrente pour les sujets de supergroupe, le sujet Général, les sujets DM,
  `agentId` par sujet, la liaison des sujets ACP, la migration de groupe et la récupération de route
  après redémarrage.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl :
  #77576 et #86262 signalent que les réponses de groupe/sujet Telegram sont routées via webchat
  ou DM au lieu de Telegram ; #80804 signale que `sendMessage` du sujet de forum échoue
  avec `chat not found`.
- Rapports Discrawl :
  les notes de version et les discussions des utilisateurs soulignent la fiabilité du sujet de forum Telegram,
  les correctifs de sujet/progression et les utilisateurs s'appuyant sur des groupes 1:1 avec threads pour contourner le comportement du sujet DM.
- Bonnes qualités :
  le modèle de routage est explicite, déterministe et conscient des sujets ; la documentation avertit des ID de groupe par rapport aux ID d'expéditeur et explique l'héritage des sujets.
- Mauvaises qualités :
  les régressions de mauvaise route cassent directement le contrat de canal visible par l'utilisateur, et
  le comportement de sujet/session est assez complexe pour que les attentes des opérateurs restent
  fragiles.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue de l'assurance qualité en direct et le nombre de tests n'ont pas
  été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le routage et la livraison des conversations.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Promouvoir les scénarios en direct de sujet de forum et d'agent par sujet dans la fumée de version.
- Ajouter des diagnostics directs pour « pourquoi cette réponse de groupe ou de sujet a-t-elle été routée ici ? »
- Maintenir le routage de groupe/sujet en dessous de la maturité DM principale jusqu'à ce que les régressions de route ouvertes soient fermées.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente la politique de groupe,
  le comportement de mention, les sujets de forum, l'héritage des sujets, les agents par sujet,
  la liaison des sujets ACP et le routage des sujets DM.
- `/Users/kevinlin/code/openclaw/docs/channels/groups.md` et
  `/Users/kevinlin/code/openclaw/docs/channels/channel-routing.md` fournissent le
  contexte partagé de groupe et de routage.
- `/Users/kevinlin/code/openclaw/docs/concepts/multi-agent.md` est lié pour
  le routage multi-agent.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.ts`
  résout les drapeaux de forum, les ID de sujet, la configuration de groupe/sujet, la route et les
  métadonnées de session.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/conversation-route.ts`
  et `/Users/kevinlin/code/openclaw/extensions/telegram/src/topic-conversation.ts`
  définissent les formes de route/session Telegram.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/thread-bindings.ts`
  et `/Users/kevinlin/code/openclaw/extensions/telegram/src/threading-tool-context.ts`
  implémentent le contexte d'outil lié au sujet et les liaisons ACP.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-policy.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-access.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-config-helpers.ts`
  implémentent la politique de groupe/sujet.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/telegram/telegram-live.runtime.ts`
  inclut `telegram-mentioned-message-reply`, `telegram-mention-gating` et
  les scénarios de statut de session actuelle.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-rtt-driver.mjs` envoie
  des mentions de groupe et vérifie que le SUT répond dans le groupe Telegram cible.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/topic-conversation.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.thread-binding.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.topic-agentid.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.dm-topic-threadid.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.acp-bindings.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/session-route.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/thread-bindings.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-migration.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Telegram group session responses route webchat" --json`

Résultats :

- #77576 problème ouvert : les réponses de session de groupe Telegram sont routées vers webchat au lieu
  de revenir à Telegram.
- #80804 problème ouvert : `sendMessage` Telegram échoue avec `chat not found` pour un
  sujet de forum de supergroupe.

Requête :

`gitcrawl search openclaw/openclaw --query "telegram forum topic routing session webchat dm" --json`

Résultats :

- #86262 problème ouvert : les réponses du sujet de forum Telegram sont routées vers DM au lieu de
  groupe.
- #80804 problème ouvert : échec d'envoi du sujet de forum malgré les permissions d'administrateur et un
  appel API direct fonctionnant.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram forum topic"`

Résultats :

- `general`, 2026-05-26 : l'utilisateur a soulevé la fiabilité de Telegram/sujet de forum comme
  ajoutant de la valeur.
- `releases`, 2026-05-27 : les notes de version ont indiqué que Telegram conserve
  la saisie/progression et le contexte du sujet de forum.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram group routing"`

Résultats :

- `maintainer-security-ops`, 2026-05-27 : la discussion a décrit l'historique de groupe et
  l'autorisation d'outil comme sémantique de confiance inter-canaux.
- `clawtributors`, 2026-05-08 : le balayage de version/régression a listé le routage de groupe Telegram parmi les
  problèmes pressants.
