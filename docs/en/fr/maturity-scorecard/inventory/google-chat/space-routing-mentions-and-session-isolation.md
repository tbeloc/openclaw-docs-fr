---
title: "Google Chat - Conversation Routing and Delivery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Conversation Routing and Delivery Maturity Note

## Résumé

Le routage des espaces est la principale raison pour laquelle la surface reste en Alpha. L'implémentation dispose d'une politique d'entrée partagée, de clés `spaces/<id>` stables, d'extraction de mentions, de listes blanches d'expéditeurs de groupe, de groupes d'accès, d'invites de groupe et de protection contre les boucles de bot, mais les preuves d'archive incluent des rapports ouverts ou récents d'espaces étant silencieusement ignorés, des charges utiles de module complémentaire échouant, des configurations de groupe générique bloquant les expéditeurs, et des utilisateurs ayant besoin d'une OAuth utilisateur optionnelle pour recevoir le trafic sans mention.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Conversation Routing and Delivery`
- Fusionnée à partir de : `Conversation Access and Routing`, `Message Delivery and Actions`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Approbation d'appairage DM : Couvre l'approbation d'appairage DM dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage, et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Listes blanches d'expéditeurs : Couvre les listes blanches d'expéditeurs dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage, et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Correspondance d'identité Google Chat : Couvre la correspondance d'identité Google Chat dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage, et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Routage de session directe : Couvre le routage de session directe dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage, et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Diagnostics d'appairage : Couvre les diagnostics d'appairage dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage, et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Listes blanches d'espaces : Couvre les listes blanches d'espaces dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques, et le comportement de routage d'espaces et d'isolation de session associé.
- Contrôle d'accès aux mentions : Couvre le contrôle d'accès aux mentions dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques, et le comportement de routage d'espaces et d'isolation de session associé.
- Groupes d'accès d'expéditeur : Couvre les groupes d'accès d'expéditeur dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques, et le comportement de routage d'espaces et d'isolation de session associé.
- Isolation de session de groupe : Couvre l'isolation de session de groupe dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques, et le comportement de routage d'espaces et d'isolation de session associé.
- Protection contre les boucles de bot : Couvre la protection contre les boucles de bot dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques, et le comportement de routage d'espaces et d'isolation de session associé.
- Diagnostics d'espace : Couvre les diagnostics d'espace dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques, et le comportement de routage d'espaces et d'isolation de session associé.
- Pièces jointes entrantes : Couvre les pièces jointes entrantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison de réponses médias sortantes, `upload-file`, et le comportement de pièces jointes médias et de transfert de fichiers associé.
- Réponses médias sortantes : Couvre les réponses médias sortantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison de réponses médias sortantes, `upload-file`, et le comportement de pièces jointes médias et de transfert de fichiers associé.
- Action de téléchargement de message : Couvre l'action de téléchargement de message dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison de réponses médias sortantes, `upload-file`, et le comportement de pièces jointes médias et de transfert de fichiers associé.
- Contrôles de source et de taille de média : Couvre les contrôles de source et de taille de média dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison de réponses médias sortantes, `upload-file`, et le comportement de pièces jointes médias et de transfert de fichiers associé.
- Reçus de média et placement de fil : Couvre les reçus de média et le placement de fil dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison de réponses médias sortantes, `upload-file`, et le comportement de pièces jointes médias et de transfert de fichiers associé.
- Action d'envoi de texte : Couvre l'action d'envoi de texte dans la découverte d'outils de message Google Chat, `send`, `upload-file`, `react`, et le comportement d'actions de message, de réactions et d'authentification d'approbation associé.
- Action upload-file : Couvre l'action upload-file dans la découverte d'outils de message Google Chat, `send`, `upload-file`, `react`, et le comportement d'actions de message, de réactions et d'authentification d'approbation associé.
- Actions de réaction : Couvre les actions de réaction dans la découverte d'outils de message Google Chat, `send`, `upload-file`, `react`, et le comportement d'actions de message, de réactions et d'authentification d'approbation associé.
- Portes de capacité d'action : Couvre les portes de capacité d'action dans la découverte d'outils de message Google Chat, `send`, `upload-file`, `react`, et le comportement d'actions de message, de réactions et d'authentification d'approbation associé.
- Correspondance d'expéditeur d'approbation : Couvre la correspondance d'expéditeur d'approbation dans la découverte d'outils de message Google Chat, `send`, `upload-file`, `react`, et le comportement d'actions de message, de réactions et d'authentification d'approbation associé.
- Réponses conscientes du fil : Couvre les réponses conscientes du fil dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé.
- Réponses en diffusion et segmentées : Couvre les réponses en diffusion et segmentées dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé.
- Cycle de vie de l'espace réservé de saisie : Couvre le cycle de vie de l'espace réservé de saisie dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé.
- Réponses de source actuelle de l'outil de message : Couvre les réponses de source actuelle de l'outil de message dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé.
- Nettoyage NO_REPLY : Couvre le nettoyage NO_REPLY dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé.
- Rendu Markdown/texte : Couvre le rendu Markdown/texte dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé.
- Réponses conscientes du fil : Couvre les réponses conscientes du fil dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé
- Réponses en diffusion et segmentées : Couvre les réponses en diffusion et segmentées dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé
- Cycle de vie de l'espace réservé de saisie : Couvre le cycle de vie de l'espace réservé de saisie dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé
- Réponses de source actuelle de l'outil de message : Couvre les réponses de source actuelle de l'outil de message dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé
- Nettoyage NO_REPLY : Couvre le nettoyage NO_REPLY dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé
- Rendu Markdown/texte : Couvre le rendu Markdown/texte dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, la segmentation de texte, et le comportement de réponses filées, de diffusion en continu et de cycle de vie de saisie associé

## Fonctionnalités

- Conversation Routing and Delivery : Portée des preuves pour Conversation Routing and Delivery.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (58%)`
- Signaux positifs : Les tests locaux couvrent les portes de mention de groupe, les listes blanches d'expéditeurs de groupe, l'expansion de groupe d'accès, `systemPrompt`, l'application de clé d'espace stable, le rejet de clé de nom d'affichage obsolète, les faits de protection contre les boucles de bot, la suppression de messages créés par bot, et les différences de contexte DM par rapport au groupe.
- Signaux négatifs : Il n'y a pas de voie en direct d'espace Google Chat réel. Les sources et tests existants ne prouvent pas le contrat complet de livraison d'événements Google pour les espaces, en particulier la différence entre la livraison @mention de compte de service et la livraison d'espace de tous les messages souhaitée.
- Lacunes d'intégration : Ajouter un scénario d'espace en direct pour les groupes `spaces/<id>` autorisés, les groupes génériques, les modes mention-required et mention-disabled, les listes blanches d'expéditeurs, `botUser`, et un cas négatif pour les clés de groupe de nom d'affichage mutable.

## Score de Qualité

- Score : `Alpha (55%)`
- Rapports Gitcrawl : #58514 est ouvert pour les messages de groupe/espace retournant HTTP 200 mais sans session et sans réponse d'agent tandis que les DMs fonctionnent. #65007 est ouvert pour l'analyse de charge utile d'extension et le comportement de liste d'autorisation de groupe générique. #44347 demande la réception de tous les messages dans les espaces plutôt que seulement les @mentions, ce qui nécessite un OAuth utilisateur optionnel ou un modèle de livraison différent.
- Rapports Discrawl : `discrawl search "Google Chat space messages ignored" --limit 10` a retourné des commentaires #58514 identifiant une mauvaise classification de type d'espace et des suppressions silencieuses. `discrawl search "channels.googlechat groups requireMention" --limit 10` a retourné une configuration utilisateur avec plusieurs entrées `spaces/...`, `requireMention: false`, `groupPolicy: "allowlist"`, `botUser`, et `actions.reactions`, où le canal semblait configuré/en cours d'exécution mais les messages ne déclenchaient toujours pas de journaux utiles.
- Bonnes qualités : Le code ne repose plus sur des noms de salle mutables pour le routage, les groupes par défaut à liste d'autorisation, peut exiger des mentions, expose les invites de groupe, peut restreindre les expéditeurs par espace, supprime les événements créés par bot par défaut, et utilise la protection de boucle bot partagée lorsque les bots sont autorisés.
- Mauvaises qualités : Le comportement de l'espace est opérationnellement fragile. Le modèle de compte de service de Google Chat ne livre que le trafic de mention dans les espaces, `botUser` est facile à oublier, les variantes de charge utile d'application/extension ont été une source d'échec, et les archives actuelles incluent toujours des rapports de suppression silencieuse. C'est un risque produit/opérateur, pas seulement une complexité d'implémentation.
- Exclu de la qualité : La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Alpha (58%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-chat.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent l'étendue de la taxonomie pour le Routage et la Livraison de Conversation.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version-3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un vrai smoke d'espace qui prouve la création de clé de session en tant que `agent:<id>:googlechat:group:<spaceId>`.
- Documenter la limitation de livraison @mention du compte de service à côté de `requireMention`, pas seulement dans l'historique des problèmes.
- Rendre les suppressions d'espace silencieuses observables avec des journaux/statuts codés par raison pour les décisions de route de groupe, expéditeur, mention et analyse de charge utile.
- Décider si le générique `groups["*"]` signifie router tous les espaces avec mention gating ou router tous les espaces plus liste d'autorisation d'expéditeur, puis garder les docs/source/tests alignés.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md` : documente les DMs par rapport aux espaces, les clés de session de groupe, l'exigence @mention, `botUser`, `groupPolicy`, `groups`, `requireMention` par espace, `systemPrompt`, `allowBots`, et la protection de boucle bot.
- `/Users/kevinlin/code/openclaw/docs/channels/bot-loop-protection.md` : documente les faits de boucle bot de Google Chat clés par compte, espace et paire de bot.
- `/Users/kevinlin/code/openclaw/docs/channels/access-groups.md` : documente les entrées Google Chat dans les groupes d'accès des expéditeurs de messages génériques.
- `/Users/kevinlin/code/openclaw/docs/channels/channel-routing.md` : liste Google Chat comme canal de message configurable.

### Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-access.ts` : résout la configuration de groupe par ID d'espace stable, rejette les correspondances de nom d'affichage mutable, évalue la route de groupe et la politique d'expéditeur, extrait les mentions, calcule l'autorisation de commande, et retourne les paramètres d'invite de groupe/protection de boucle bot.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.ts` : distingue les événements de groupe par rapport aux événements directs, calcule les faits de boucle bot, résout les clés de route/session entrantes, construit le contexte avec `ChatType`, `WasMentioned`, `CommandAuthorized`, et les données d'invite de groupe.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/group-policy.ts` : délègue la résolution d'exigence de mention aux aides de politique de canal partagées.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.adapters.ts` : expose l'adaptateur de groupes et le collecteur d'avertissements de sécurité.
- `/Users/kevinlin/code/openclaw/src/config/types.googlechat.ts` : définit `groupPolicy`, `groupAllowFrom`, `groups`, `requireMention`, `botLoopProtection`, et `systemPrompt` par espace.

### Tests d'intégration

- Aucun scénario d'espace Google Chat en direct/e2e dédié n'a été trouvé sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/contracts/channel-import-guardrails.test.ts` : inclut Google Chat dans les garde-fous de contrat de plugin, mais ne prouve pas le routage d'espace réel.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-access.test.ts` : couvre les listes d'autorisation de groupe, les portes de mention, les groupes d'accès, le comportement de liste d'autorisation d'expéditeur vide, l'autorisation de commande de contrôle, les ID d'espace stables, les clés de groupe mutable dépréciées, le comportement de secours générique, et la suppression d'invite de groupe.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.test.ts` : couvre les faits de protection de boucle bot, la suppression de boucle bot avant les messages de saisie, et la séparation du contexte de thread DM.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/config-schema.test.ts` : couvre les valeurs par défaut de politique de groupe et la validation de configuration.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.test.ts` : couvre le comportement de capacité/configuration de plugin adjacent au routage de groupe.

### Requêtes Gitcrawl

Requête :

`gitcrawl gh issue view 58514 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné #58514 ouvert, où les messages de groupe ont reçu HTTP 200 mais aucune session de groupe ou réponse d'agent n'a été créée tandis que les DMs fonctionnaient.

Requête :

`gitcrawl gh issue view 65007 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné #65007 ouvert, qui signale les charges utiles d'extension valides rejetées comme invalides, les listes d'autorisation de groupe générique bloquant les expéditeurs, et les erreurs de ressource de thread dans les espaces.

Requête :

`gitcrawl gh issue view 44347 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné #44347 ouvert, demandant les réponses filetées de Google Chat et la réception optionnelle de tous les messages d'espace au-delà des @mentions, notant les limitations de livraison `chat.bot` du compte de service.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat space messages ignored" --limit 10`

Résultats :

- A retourné des commentaires du problème #58514 décrivant les DMs fonctionnant, les espaces étant mal classifiés/supprimés, et un chemin de correction vérifiant les champs de type d'espace Google Chat plus récents.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "channels.googlechat groups requireMention" --limit 10`

Résultats :

- A retourné une configuration réelle avec `groupPolicy: "allowlist"`, plusieurs entrées `spaces/...`, `requireMention: false`, `botUser`, et `dm.policy: "pairing"` où le statut a signalé le fonctionnement mais les messages n'ont pas produit de journaux utiles, mettant en évidence les lacunes de visibilité de l'opérateur.
