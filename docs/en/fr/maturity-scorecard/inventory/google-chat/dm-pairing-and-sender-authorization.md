---
title: "Google Chat - Note de Maturité d'Accès et d'Identité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Note de Maturité d'Accès et d'Identité

## Résumé

L'accès aux messages directs est l'un des domaines les plus solides de Google Chat. La documentation décrit les formats d'appairage et de cibles stables, et la source utilise le résolveur d'entrée de canal partagé pour la politique DM, les listes blanches de magasin d'appairage, les groupes d'accès et la gestion des identifiants mutables. Le score reste Beta plutôt que Stable car les preuves sont principalement simulées et parce que la sémantique d'identité de Google Chat est facile à mal configurer lorsque les utilisateurs mélangent les e-mails bruts et les valeurs `users/<id>`.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Accès et Identité`
- Fusionnée à partir de : `Accès et Routage des Conversations`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Approbation d'appairage DM : Couvre l'approbation d'appairage DM dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Listes blanches d'expéditeurs : Couvre les listes blanches d'expéditeurs dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Correspondance d'identité Google Chat : Couvre la correspondance d'identité Google Chat dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Routage de session directe : Couvre le routage de session directe dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Diagnostics d'appairage : Couvre les diagnostics d'appairage dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Listes blanches d'espaces : Couvre les listes blanches d'espaces dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Contrôle des mentions : Couvre le contrôle des mentions dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Groupes d'accès d'expéditeur : Couvre les groupes d'accès d'expéditeur dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Isolation de session de groupe : Couvre l'isolation de session de groupe dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Protection contre les boucles de bot : Couvre la protection contre les boucles de bot dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Diagnostics d'espace : Couvre les diagnostics d'espace dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.

## Fonctionnalités

- Approbation d'appairage DM : Couvre l'approbation d'appairage DM dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Listes blanches d'expéditeurs : Couvre les listes blanches d'expéditeurs dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Correspondance d'identité Google Chat : Couvre la correspondance d'identité Google Chat dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Routage de session directe : Couvre le routage de session directe dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Diagnostics d'appairage : Couvre les diagnostics d'appairage dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, les défis d'appairage et le comportement d'appairage DM et d'autorisation d'expéditeur associé.
- Listes blanches d'espaces : Couvre les listes blanches d'espaces dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Contrôle des mentions : Couvre le contrôle des mentions dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Groupes d'accès d'expéditeur : Couvre les groupes d'accès d'expéditeur dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Isolation de session de groupe : Couvre l'isolation de session de groupe dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Protection contre les boucles de bot : Couvre la protection contre les boucles de bot dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.
- Diagnostics d'espace : Couvre les diagnostics d'espace dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, les groupes génériques et le comportement de mentions de routage d'espace et d'isolation de session associé.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (70%)`
- Signaux positifs : Les tests locaux couvrent l'émission de défi d'appairage, les décisions de liste blanche DM, le blocage des e-mails bruts sauf si la correspondance dangereuse est activée, `users/<email>` n'étant pas traité comme des entrées de liste blanche d'e-mail, la correspondance d'ID utilisateur, l'expansion du groupe d'accès, les écritures de politique DM de l'assistant de configuration, les chemins de politique DM spécifiques au compte et l'omission des métadonnées de fil de message direct.
- Signaux négatifs : Je n'ai trouvé aucun scénario d'appairage DM Google Chat en direct qui commence par un expéditeur inconnu, vérifie le message d'appairage réel dans Google Chat, approuve le code et confirme qu'un DM ultérieur crée la session directe attendue.
- Lacunes d'intégration : Ajouter un test de fumée DM Google Chat réel qui exerce l'expéditeur inconnu, la livraison du défi, l'approbation d'appairage, la persistance de la liste blanche et la création de session post-approbation.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : L'ensemble large des problèmes Google Chat montre que les DM fonctionnent souvent lorsque les espaces échouent. #58514 dit explicitement que les DM créent des sessions `agent:X:googlechat:direct:spaces/Y` tandis que les espaces ne le font pas. Aucun résultat gitcrawl actuel des requêtes d'appairage DM spécifiques aux fonctionnalités n'a identifié une défaillance d'appairage DM dédiée ouverte.
- Rapports Discrawl : `discrawl search "Google Chat DMs work spaces" --limit 10` a renvoyé une configuration utilisateur où `openclaw channels status --probe` a signalé Google Chat configuré/en cours d'exécution/fonctionne avec `dm:pairing`, tandis que l'utilisateur avait toujours des problèmes de livraison de messages. `discrawl search "Google Chat space messages ignored" --limit 10` a renvoyé les commentaires #58514 confirmant que les DM fonctionnaient tandis que les espaces étaient mal classés ou supprimés.
- Bonnes qualités : La politique DM utilise des aides d'entrée partagées, la valeur par défaut est l'appairage plutôt que l'accès ouvert, le mode ouvert générique est protégé par schéma, les ID d'expéditeur se normalisent en ressources utilisateur Google Chat stables, la correspondance d'e-mail brut est réservée aux cas d'urgence uniquement, et la réponse d'appairage est envoyée via le même chemin d'envoi Google Chat.
- Mauvaises qualités : Les identités Google Chat restent confuses pour les opérateurs car les e-mails bruts, `users/<id>`, `users/<email>` et les préfixes `googlechat:` ont des sémantiques différentes. La résolution de cible de message direct dépend toujours de l'API Google Chat `spaces:findDirectMessage`, qui peut échouer pour les alias d'e-mail sous l'authentification du compte de service.
- Exclu de la qualité : La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-chat.md`.
- Signaux positifs : les docs archivées, la source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'approbation d'appairage DM, les listes blanches d'expéditeurs, la correspondance d'identité Google Chat, le routage de session directe, les diagnostics d'appairage, les listes blanches d'espaces, le contrôle des mentions, les groupes d'accès d'expéditeur, l'isolation de session de groupe, la protection contre les boucles de bot, les diagnostics d'espace.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un test de fumée DM en direct avec un ID utilisateur Google Chat réel et une approbation d'appairage.
- Améliorer la documentation avec un tableau d'identité court : `users/<id>` stable, compatibilité d'e-mail brut, `users/<email>` déprécié et formes de cible préfixées.
- Afficher un diagnostic plus direct lorsque la résolution DM proactive échoue parce que l'authentification du compte de service ne peut pas rechercher un alias d'e-mail.
- Inclure l'état de la politique DM et de la liste blanche à portée de compte dans la sortie de configuration/statut.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md` : documente le comportement par défaut de l'appairage DM, `openclaw pairing approve googlechat <code>`, format de cible de message direct `users/<userId>`, compatibilité d'email brut uniquement sous correspondance de nom dangereuse, et configuration `dm.policy`/`dm.allowFrom`.
- `/Users/kevinlin/code/openclaw/docs/channels/pairing.md` : liste `googlechat` comme canal d'appairage pris en charge.
- `/Users/kevinlin/code/openclaw/docs/channels/access-groups.md` : documente les groupes `message.senders` avec des membres Google Chat tels que `users/1234567890`.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md` : répète les conseils de configuration DM Google Chat et de correspondance de nom mutable.

## Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-access.ts` : applique la politique DM via le résolveur d'entrée de canal partagé, lit les listes blanches du magasin d'appairage, émet des défis d'appairage, gère la correspondance d'alias d'email brut uniquement lorsque la correspondance dangereuse est activée, et bloque les DM non autorisés.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.adapters.ts` : définit les chemins d'adaptateur de sécurité DM, la normalisation de l'expéditeur, le texte de notification d'approbation d'appairage, et la normalisation de cible sortante.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/setup-surface.ts` : câble la configuration de la politique DM et les écritures allowFrom à portée de compte.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/targets.ts` : normalise les formes de cible `users/...`, email brut et préfixé, et résout les cibles utilisateur en espaces de message direct.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/doctor.ts` : avertit sur les entrées de liste blanche Google Chat mutables.

## Tests d'intégration

- Aucun scénario d'appairage DM Google Chat en direct dédié n'a été trouvé sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/setup-wizard-helpers.test.ts` : inclut des scénarios d'aide de configuration Google Chat qui écrivent `channels.googlechat.dm.allowFrom` et `channels.googlechat.dm.policy`, ce qui est plus proche de l'intégration de configuration que de la preuve de canal en direct.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-access.test.ts` : couvre les contrôles de correspondance d'email brut, le comportement de dépréciation `users/<email>`, la correspondance d'ID utilisateur, l'émission de défi d'appairage, l'expansion de groupe d'accès, les décisions d'expéditeur groupe/DM, et le blocage de commande de contrôle.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/setup.test.ts` : couvre les valeurs par défaut de la politique DM, les chemins de politique spécifiques au compte, les écritures de caractère générique de politique ouverte, et le comportement d'invite allowFrom.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/targets.test.ts` : couvre la normalisation de cible Google Chat et la résolution d'espace sortant.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/config-schema.test.ts` : couvre les règles de schéma de politique DM telles que `open` nécessitant `allowFrom: ["*"]`.

## Requêtes Gitcrawl

Requête :

`gitcrawl search issues "Google Chat direct messages pairing users email allowlist" --repo openclaw/openclaw --limit 15 --json number,title,state,updatedAt,url`

Résultats :

- N'a retourné aucun résultat direct. C'est neutre après des vérifications de fraîcheur d'archive réussies ; les preuves connexes provenaient de problèmes Google Chat plus larges et de discrawl.

Requête :

`gitcrawl gh issue view 58514 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné l'ouverture #58514, où les DM ont été signalés comme fonctionnant et créant des sessions directes tandis que les messages d'espace/groupe retournaient HTTP 200 et étaient silencieusement ignorés.

## Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat DMs work spaces" --limit 10`

Résultats :

- A retourné un rapport utilisateur avec `openclaw channels status --probe` montrant `Google Chat default: enabled, configured, running, dm:pairing, works`, aux côtés d'une configuration utilisant `dm.policy: "pairing"`.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat space messages ignored" --limit 10`

Résultats :

- A retourné la discussion #58514 confirmant la division observée : les DM fonctionnaient correctement tandis que les messages d'espace/groupe étaient supprimés jusqu'à ce que la gestion du type d'espace soit corrigée.
