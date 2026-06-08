---
title: "Google Chat - Note de maturité des contrôles natifs et des approbations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Note de maturité des contrôles natifs et des approbations

## Résumé

Google Chat expose des primitives d'action utiles : envois de texte, `upload-file`, ajout/liste/suppression de réactions, normalisation des cibles et correspondance des expéditeurs d'approbation via des identifiants utilisateur stables. La maturité est Alpha car plusieurs capacités d'action dépendent d'une authentification OAuth utilisateur qui n'est pas implémentée, les réponses des outils de message interagissent mal avec le threading et les espaces réservés de saisie, et le canal n'a pas de parité de surface interactive riche ou de commande native avec Slack/Discord.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Contrôles natifs et approbations`
- Fusionnée à partir de : `Livraison des messages et actions`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Pièces jointes entrantes : Couvre les pièces jointes entrantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Réponses médias sortantes : Couvre les réponses médias sortantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Action de téléchargement de message : Couvre l'action de téléchargement de message dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Contrôles de source et de taille des médias : Couvre les contrôles de source et de taille des médias dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Reçus médias et placement des threads : Couvre les reçus médias et le placement des threads dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Action d'envoi de texte : Couvre l'action d'envoi de texte dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Action upload-file : Couvre l'action upload-file dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Actions de réaction : Couvre les actions de réaction dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Portes de capacité d'action : Couvre les portes de capacité d'action dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Correspondance des expéditeurs d'approbation : Couvre la correspondance des expéditeurs d'approbation dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Réponses conscientes des threads : Couvre les réponses conscientes des threads dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Réponses en streaming et chunked : Couvre les réponses en streaming et chunked dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Cycle de vie de l'espace réservé de saisie : Couvre le cycle de vie de l'espace réservé de saisie dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Réponses message-tool source actuelle : Couvre les réponses message-tool source actuelle dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Nettoyage NO_REPLY : Couvre le nettoyage NO_REPLY dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Rendu Markdown/texte : Couvre le rendu Markdown/texte dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.

## Fonctionnalités

- Pièces jointes entrantes : Couvre les pièces jointes entrantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Réponses médias sortantes : Couvre les réponses médias sortantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Action de téléchargement de message : Couvre l'action de téléchargement de message dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Contrôles de source et de taille des médias : Couvre les contrôles de source et de taille des médias dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Reçus médias et placement des threads : Couvre les reçus médias et le placement des threads dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file` et le comportement associé des pièces jointes médias et du transfert de fichiers.
- Action d'envoi de texte : Couvre l'action d'envoi de texte dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Action upload-file : Couvre l'action upload-file dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Actions de réaction : Couvre les actions de réaction dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Portes de capacité d'action : Couvre les portes de capacité d'action dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Correspondance des expéditeurs d'approbation : Couvre la correspondance des expéditeurs d'approbation dans la découverte d'actions de l'outil de message Google Chat, `send`, `upload-file`, `react` et le comportement associé des actions de message, des réactions et de l'authentification des approbations.
- Réponses conscientes des threads : Couvre les réponses conscientes des threads dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Réponses en streaming et chunked : Couvre les réponses en streaming et chunked dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Cycle de vie de l'espace réservé de saisie : Couvre le cycle de vie de l'espace réservé de saisie dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Réponses message-tool source actuelle : Couvre les réponses message-tool source actuelle dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Nettoyage NO_REPLY : Couvre le nettoyage NO_REPLY dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.
- Rendu Markdown/texte : Couvre le rendu Markdown/texte dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte et le comportement associé des réponses threadées, du streaming et du cycle de vie de la saisie.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (62%)`
- Signaux positifs : Les tests locaux vérifient la découverte d'actions, le gating des réactions au niveau du compte, les envois de messages avec médias téléchargés, les remplacements de noms de fichiers `upload-file`, la suppression des réactions appartenant uniquement à l'application, la normalisation des cibles et les preuves de capacité de l'adaptateur de messages de canal pour les hooks de texte/média/thread/envoi de messages.
- Signaux négatifs : Il n'y a pas de voie d'action Google Chat en direct prouvant les portées de réaction, la correspondance des expéditeurs d'approbation, la livraison message-tool source actuelle ou le comportement des actions de pièces jointes par rapport aux autorisations de l'API Google Chat.
- Lacunes d'intégration : Ajouter une suite d'actions en direct pour `message(action=send)`, les envois threadés source actuelle, l'ajout/suppression/liste de réactions avec OAuth utilisateur ou des avertissements explicites non pris en charge, et l'autorisation d'approbation à partir d'un identifiant utilisateur Google Chat réel.

## Score de Qualité

- Score : `Alpha (58%)`
- Rapports Gitcrawl : #9764 est ouvert car les réactions, les téléchargements de médias et les messages directs proactifs nécessitent un OAuth utilisateur optionnel au-delà du jeton de compte de service actuel. #82014 signale que les réponses de l'outil de message ne consomment pas les espaces réservés de saisie. #80995 signale que les réponses de l'outil de message échappent aux threads. #39843 signale que les réactions uniquement plus `NO_REPLY` laissent les indicateurs de saisie visibles.
- Rapports Discrawl : `discrawl search "Google Chat reactions media upload OAuth" --limit 10` a retourné la discussion #9764 selon laquelle la branche principale actuelle n'a toujours pas de surface de credentials OAuth utilisateur Google Chat et que les chemins de réaction/téléchargement/DM proactif utilisent toujours les jetons de compte de service `chat.bot`. `discrawl search "Google Chat message tool" --limit 10` a retourné le contexte de l'outil de message/source actuelle, y compris la mention de Google Chat dans les tests de version de canal et les préoccupations adjacentes de livraison de l'outil de message.
- Bonnes qualités : L'adaptateur d'action est petit, conscient du compte et explicite sur les comptes activés et les portes d'action. Il utilise les lecteurs de paramètres d'actions de canal partagées, résout les cibles par la recherche d'espace Google Chat, prend en charge les alias de paramètres de médias locaux et distants, et supprime uniquement les réactions effectuées par les identités de l'application.
- Mauvaises qualités : La surface d'action annonce des capacités qui sont structurellement implémentées mais limitées par les réalités de la portée d'authentification Google. La livraison actuelle de l'outil de message n'est pas suffisamment intégrée au cycle de vie de saisie provisoire de Google Chat, et les commandes natives sont déclarées non prises en charge. Les opérateurs peuvent voir les actions dans les descriptions d'outils sans une distinction suffisamment claire entre les opérations prises en charge par le compte de service et celles nécessitant un OAuth utilisateur.
- Exclu de la qualité : La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Alpha (62%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-chat.md`.
- Signaux positifs : les preuves des docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les pièces jointes entrantes, les réponses de médias sortants, l'action de téléchargement de message, les contrôles de source et de taille de médias, les reçus de médias et le placement des threads, l'action d'envoi de texte, l'action de téléchargement de fichier, les actions de réaction, les portes de capacité d'action, la correspondance de l'expéditeur d'approbation, les réponses conscientes des threads, les réponses en streaming et par chunks, le cycle de vie des espaces réservés de saisie, les réponses de l'outil de message/source actuelle, le nettoyage de `NO_REPLY`, le rendu Markdown/texte.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un OAuth utilisateur optionnel pour les opérations de réactions, de téléchargement de pièces jointes et de DM proactif ou masquer/refuser ces actions avec des diagnostics clairs par action lorsqu'elles ne sont pas disponibles.
- Router les envois de l'outil de message/source actuelle via le même cycle de vie de thread et d'espace réservé de saisie que les réponses automatiques.
- Ajouter des scénarios d'approbation Google Chat utilisant des approbateurs stables `users/<id>` et rejetant les entrées d'approbateur d'email mutables.
- Faire en sorte que la découverte d'actions distingue les envois de texte qui fonctionnent avec l'authentification du compte de service des opérations qui nécessitent un OAuth utilisateur.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md` : documente `actions.reactions`, `typingIndicator`, les actions de message `send` et `upload-file`, les paramètres de téléchargement et les limitations du compte de service pour le mode de saisie de réaction.
- `/Users/kevinlin/code/openclaw/docs/tools/reactions.md` : documente la sémantique de réaction Google Chat pour la suppression d'emoji vide et `remove: true`.
- `/Users/kevinlin/code/openclaw/docs/cli/message.md` : inclut des exemples Google Chat `openclaw message send --channel googlechat --target spaces/AAA...` et des conseils de format de cible.
- `/Users/kevinlin/code/openclaw/docs/tools/slash-commands.md` : note que Google Chat manque de commandes natives et utilise des commandes texte où elles sont activées.

### Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/actions.ts` : implémente la découverte et la gestion des actions pour `send`, `upload-file`, `react` et `reactions`, y compris les alias de médias et la suppression de réactions appartenant à l'application.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.ts` : enregistre l'adaptateur d'action, la description de l'outil de message, les capacités du canal et l'adaptateur d'authentification d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/approval-auth.ts` : normalise les approbateurs stables `users/<id>` et rejette les entrées d'approbateur d'email mutables.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/api.ts` : implémente l'envoi de message, le téléchargement de pièces jointes, la recherche de messages directs et les appels de création/liste/suppression de réactions.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/targets.ts` : normalise les cibles `spaces/...`, `users/...`, les préfixes et les cibles d'email brutes avant les envois d'action.

### Tests d'intégration

- Aucun scénario d'action/réaction/approbation Google Chat en direct dédié n'a été trouvé sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/test/scripts/bundled-plugin-build-entries.test.ts` : inclut Google Chat dans les vérifications d'entrées de construction de plugin groupé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/actions.test.ts` : couvre la découverte d'actions, les portes de réaction à portée de compte, les chemins d'envoi/téléchargement de médias, les alias de téléchargement de fichier, la substitution de nom de fichier et la suppression de réactions appartenant à l'application.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/approval-auth.test.ts` : couvre la normalisation de l'authentification d'approbation Google Chat et le comportement de correspondance des approbateurs.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.test.ts` : vérifie les preuves de capacité de l'adaptateur de message, la résolution de cible, le comportement d'envoi sortant texte/médias et le threading de compte.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/targets.test.ts` : couvre la normalisation de cible et le comportement de recherche de messages directs.

### Requêtes Gitcrawl

Requête :

`gitcrawl gh issue view 9764 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné l'ouverture #9764, qui indique que l'authentification du compte de service limite les réactions, les téléchargements de médias et les DM proactifs et propose un OAuth utilisateur optionnel.

Requête :

`gitcrawl gh issue view 82014 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné l'ouverture #82014, signalant que les réponses de l'outil de message/source actuelle Google Chat contournent le nettoyage des espaces réservés de saisie.

Requête :

`gitcrawl gh issue view 80995 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné l'ouverture #80995, signalant que les réponses de l'outil de message Google Chat peuvent être publiées en dehors du thread d'origine.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat reactions media upload OAuth" --limit 10`

Résultats :

- A retourné la discussion #9764 selon laquelle l'OAuth utilisateur est toujours absent et que les chemins de réaction/téléchargement/DM proactif continuent d'utiliser le chemin du jeton de compte de service.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat message tool" --limit 10`

Résultats :

- A retourné le contexte de version et de problème où le comportement de l'outil de message/thread Google Chat fait partie du registre actif de test et de débogage du canal.
