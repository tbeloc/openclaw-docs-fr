---
title: "Google Chat - Note de Maturité des Médias et du Contenu Enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Note de Maturité des Médias et du Contenu Enrichi

## Résumé

Le support des médias Google Chat est structurellement présent pour les téléchargements entrants et les téléchargements sortants, avec des limites de taille, la gestion des racines locales, les jetons de téléchargement et les reçus de médias. Il reste une zone Alpha faible car les téléchargements de pièces jointes Google Chat nécessitent OAuth utilisateur pour certains déploiements réels, la preuve en direct est manquante, et les preuves d'archive lient les médias aux problèmes OAuth ouverts et de cycle de vie de saisie/thread.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Médias et Contenu Enrichi`
- Fusionnée à partir de : `Livraison des Messages et Actions`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Pièces jointes entrantes : Couvre les pièces jointes entrantes dans le téléchargement de pièces jointes Google Chat entrantes, la remise du magasin de médias, la livraison des réponses de médias sortants, `upload-file`, et le comportement associé des pièces jointes de médias et du transfert de fichiers.
- Réponses de médias sortants : Couvre les réponses de médias sortants dans le téléchargement de pièces jointes Google Chat entrantes, la remise du magasin de médias, la livraison des réponses de médias sortants, `upload-file`, et le comportement associé des pièces jointes de médias et du transfert de fichiers.
- Action de téléchargement de message : Couvre l'action de téléchargement de message dans le téléchargement de pièces jointes Google Chat entrantes, la remise du magasin de médias, la livraison des réponses de médias sortants, `upload-file`, et le comportement associé des pièces jointes de médias et du transfert de fichiers.
- Contrôles de source et de taille des médias : Couvre les contrôles de source et de taille des médias dans le téléchargement de pièces jointes Google Chat entrantes, la remise du magasin de médias, la livraison des réponses de médias sortants, `upload-file`, et le comportement associé des pièces jointes de médias et du transfert de fichiers.
- Reçus de médias et placement dans les threads : Couvre les reçus de médias et le placement dans les threads dans le téléchargement de pièces jointes Google Chat entrantes, la remise du magasin de médias, la livraison des réponses de médias sortants, `upload-file`, et le comportement associé des pièces jointes de médias et du transfert de fichiers.
- Action d'envoi de texte : Couvre l'action d'envoi de texte dans la découverte des actions des outils de messages Google Chat, `send`, `upload-file`, `react`, et le comportement associé des actions de messages, des réactions et de l'authentification d'approbation.
- Action upload-file : Couvre l'action upload-file dans la découverte des actions des outils de messages Google Chat, `send`, `upload-file`, `react`, et le comportement associé des actions de messages, des réactions et de l'authentification d'approbation.
- Actions de réaction : Couvre les actions de réaction dans la découverte des actions des outils de messages Google Chat, `send`, `upload-file`, `react`, et le comportement associé des actions de messages, des réactions et de l'authentification d'approbation.
- Portes de capacité d'action : Couvre les portes de capacité d'action dans la découverte des actions des outils de messages Google Chat, `send`, `upload-file`, `react`, et le comportement associé des actions de messages, des réactions et de l'authentification d'approbation.
- Correspondance de l'expéditeur d'approbation : Couvre la correspondance de l'expéditeur d'approbation dans la découverte des actions des outils de messages Google Chat, `send`, `upload-file`, `react`, et le comportement associé des actions de messages, des réactions et de l'authentification d'approbation.
- Réponses conscientes des threads : Couvre les réponses conscientes des threads dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé des réponses en thread, du streaming et du cycle de vie de saisie.
- Réponses en streaming et segmentées : Couvre les réponses en streaming et segmentées dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé des réponses en thread, du streaming et du cycle de vie de saisie.
- Cycle de vie de l'indicateur de saisie : Couvre le cycle de vie de l'indicateur de saisie dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé des réponses en thread, du streaming et du cycle de vie de saisie.
- Réponses de source actuelle de l'outil de message : Couvre les réponses de source actuelle de l'outil de message dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé des réponses en thread, du streaming et du cycle de vie de saisie.
- Nettoyage NO_REPLY : Couvre le nettoyage NO_REPLY dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé des réponses en thread, du streaming et du cycle de vie de saisie.
- Rendu Markdown/texte : Couvre le rendu Markdown/texte dans la propagation des ressources de thread entrantes, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement associé des réponses en thread, du streaming et du cycle de vie de saisie.

## Fonctionnalités

- Médias et Contenu Enrichi : Portée des preuves pour Médias et Contenu Enrichi.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (55%)`
- Signaux positifs : Les tests locaux vérifient le chargement de fichiers locaux avec `mediaLocalRoots`, le chargement d'URL distantes avec des limites de taille, la propagation des jetons de téléchargement de pièces jointes, les reçus de médias, les légendes de texte, les alias `upload-file`, la substitution de nom de fichier, et la plomberie de téléchargement de pièces jointes entrantes via les tests de moniteur.
- Signaux négatifs : Je n'ai trouvé aucune voie en direct réelle de médias Google Chat. La source peut appeler les API de téléchargement/téléchargement Google Chat, mais la couverture ne prouve pas le comportement réel de la portée OAuth Google Chat, le rejet de fichiers volumineux, les médias entrants des espaces et des DM, le texte+médias avec des indicateurs de saisie, ou les envois de médias multi-comptes contre la plateforme.
- Lacunes d'intégration : Ajouter une suite de médias en direct pour le téléchargement de pièces jointes entrantes, le téléchargement local sortant, le téléchargement distant sortant, le rejet de fichiers surdimensionnés, la réponse texte+médias, l'`upload-file` de l'outil de message, et la livraison de médias préservant les threads.

## Score de Qualité

- Score : `Alpha (50%)`
- Rapports Gitcrawl : #9764 est ouvert car les téléchargements de médias nécessitent OAuth utilisateur au-delà du chemin du compte de service. #82014 et #39843 montrent que les flux de médias/actions peuvent interagir mal avec les indicateurs de saisie. #69422 et #42510 montrent que les métadonnées de thread sont fragiles pour les réponses en streaming/segmentées, ce qui affecte également les réponses de médias avec des légendes.
- Rapports Discrawl : `discrawl search "Google Chat reactions media upload OAuth" --limit 10` a retourné des commentaires #9764 confirmant que la branche principale actuelle manque toujours d'OAuth utilisateur et que les chemins de téléchargement de médias utilisent le chemin du jeton du compte de service. `discrawl search "Google Chat typing indicator" --limit 10` a retourné plusieurs PR de nettoyage de médias+texte/saisie et des commentaires de problèmes.
- Bonnes qualités : L'implémentation limite les octets de médias, utilise des chargeurs de médias sortants partagés, supporte les lectures restreintes à la racine locale, télécharge via le point de terminaison de pièce jointe multipart de Google Chat, enregistre les reçus de livraison de médias, et enregistre les téléchargements entrants via le pipeline de médias partagé.
- Mauvaises qualités : La capacité du produit est limitée par la portée d'authentification Google : l'authentification du compte de service ne suffit pas pour tous les cas d'utilisation de médias/téléchargement. Le comportement de réponse texte+médias a un historique récent de perte de texte silencieuse et de corrections de nettoyage d'indicateurs. Sans preuves de médias en direct, les opérateurs ne peuvent pas compter sur le transfert de fichiers comme une capacité Google Chat de première classe.
- Exclu de la qualité : La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Alpha (55%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-chat.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Médias et Contenu Enrichi.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter OAuth utilisateur optionnel ou des diagnostics explicites non pris en charge pour les chemins de téléchargement qui ne peuvent pas fonctionner avec l'authentification du compte de service.
- Prouver les médias entrants et sortants dans un vrai DM et espace Google Chat.
- Ajouter la documentation de l'opérateur pour `mediaMaxMb`, les portées de téléchargement de l'API Google Chat, et les limitations du compte de service.
- Garder les réponses de médias liées au même thread et au même cycle de vie d'indicateur de saisie que les réponses de texte.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md` : documente les pièces jointes médias, `mediaMaxMb`, les paramètres `upload-file`, `media`/`filePath`/`path`, et le téléchargement des pièces jointes via l'API Chat.
- `/Users/kevinlin/code/openclaw/docs/cli/message.md` : inclut des exemples Google Chat `message send` et des conseils de ciblage de canal.
- `/Users/kevinlin/code/openclaw/docs/nodes/media-understanding.md` : documente la transmission générique de médias, que Google Chat utilise après le téléchargement des fichiers entrants.
- `/Users/kevinlin/code/openclaw/docs/reference/secretref-credential-surface.md` : note les surfaces SecretRef du compte de service Google Chat dont dépendent les appels API médias.

## Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/api.ts` : implémente `uploadGoogleChatAttachment`, `downloadGoogleChatMedia`, et les lectures de buffer limitées par la taille de réponse.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.ts` : télécharge la première pièce jointe entrante et l'enregistre dans le magasin de médias partagé avant de construire le contexte du message.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-reply-delivery.ts` : télécharge les pièces jointes de réponse sortantes, supprime ou met à jour les espaces réservés de saisie, et envoie les légendes avec les jetons de pièce jointe téléchargés.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.adapters.ts` : implémente les envois de médias attachés, le chargement de médias locaux/distants, le compte/canal `mediaMaxMb`, et les reçus de médias.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/actions.ts` : implémente les alias médias `upload-file` et `send` pour `media`, `filePath`, et `path`.

## Tests d'intégration

- Aucun scénario média Google Chat en direct/e2e dédié n'a été trouvé sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/test/scripts/bundled-plugin-build-entries.test.ts` : protège les entrées de construction du plugin groupé, mais pas le transfert de médias réel.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.test.ts` : vérifie les preuves de capacité média de l'adaptateur de message Google Chat, le chargement de fichiers racine locaux, les plafonds d'octets de médias distants, les reçus de médias, et le threading de configuration de compte.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/actions.test.ts` : vérifie les envois de médias et `upload-file` via la gestion des actions, y compris les lectures de fichiers locaux et le remplacement de nom de fichier.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.reply-delivery.test.ts` : couvre la livraison de réponse média et le comportement de secours texte/saisie.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.test.ts` : couvre la plomberie de téléchargement de pièce jointe entrante via le pipeline de surveillance.

## Requêtes Gitcrawl

Requête :

`gitcrawl gh issue view 9764 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné l'ouverture #9764, indiquant que les réactions, les téléchargements de médias et les messages directs proactifs nécessitent des portées OAuth au niveau de l'utilisateur et sont limités par le modèle actuel réservé au compte de service.

Requête :

`gitcrawl search issues "Google Chat media attachment upload reactions" --repo openclaw/openclaw --limit 15 --json number,title,state,updatedAt,url`

Résultats :

- N'a retourné aucun résultat direct. Le signal média pertinent provenait de #9764 et des problèmes de saisie/thread trouvés par des requêtes Google Chat plus larges.

Requête :

`gitcrawl gh issue view 82014 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné l'ouverture #82014, qui affecte les réponses visibles de l'outil de message et le nettoyage des espaces réservés de saisie, y compris les réponses visibles contenant des médias.

## Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat reactions media upload OAuth" --limit 10`

Résultats :

- A retourné la discussion #9764 confirmant que Google Chat OAuth au niveau de l'utilisateur est toujours manquant et que les chemins de téléchargement de médias utilisent toujours les chemins de jeton de compte de service.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat typing indicator" --limit 10`

Résultats :

- A retourné le contexte PR/issue #71498, #70923 et #65570 pour la perte de texte silencieuse lorsque les réponses Google Chat contiennent des médias plus du texte avec les indicateurs de saisie activés.
