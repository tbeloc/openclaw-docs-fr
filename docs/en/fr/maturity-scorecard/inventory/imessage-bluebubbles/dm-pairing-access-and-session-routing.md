---
title: "iMessage / BlueBubbles - Access and Identity Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Access and Identity Maturity Note

## Résumé

L'appairage DM, l'accès et le routage de session sont en version bêta. L'implémentation dispose de modes de politique clairs, d'un comportement d'appairage, d'un formatage de liste d'autorisation, d'une autorisation de commande, d'une normalisation de l'expéditeur et d'une liaison de conversation ACP. La principale limite de maturité n'est pas la forme du code ; c'est la quantité de variance d'identité à l'exécution : les numéros de téléphone, les e-mails Apple ID, les préfixes de service, les identifiants de chat et les anciennes clés de session doivent tous être mappés correctement.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Access and Identity`
- Fusionnée à partir de : `Conversation Routing and Access`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Autoriser les expéditeurs directs : Couvre Autoriser les expéditeurs directs dans `dmPolicy`, `allowFrom`, appairage, normalisation de l'identité de l'expéditeur et comportement d'appairage, d'accès et de routage de session DM associé.
- Router les conversations directes : Couvre Router les conversations directes dans `dmPolicy`, `allowFrom`, appairage, normalisation de l'identité de l'expéditeur et comportement d'appairage, d'accès et de routage de session DM associé.
- Lier les sessions ACP : Couvre Lier les sessions ACP dans `dmPolicy`, `allowFrom`, appairage, normalisation de l'identité de l'expéditeur et comportement d'appairage, d'accès et de routage de session DM associé.
- Politique de groupe : Couvre Politique de groupe dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation.
- Mentions : Couvre Mentions dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation.
- Invites système : Couvre Invites système dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation.
- Politique de groupe : Couvre Politique de groupe dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation
- Mentions : Couvre Mentions dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation
- Invites système : Couvre Invites système dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation

## Fonctionnalités

- Autoriser les expéditeurs directs : Couvre Autoriser les expéditeurs directs dans `dmPolicy`, `allowFrom`, appairage, normalisation de l'identité de l'expéditeur et comportement d'appairage, d'accès et de routage de session DM associé.
- Router les conversations directes : Couvre Router les conversations directes dans `dmPolicy`, `allowFrom`, appairage, normalisation de l'identité de l'expéditeur et comportement d'appairage, d'accès et de routage de session DM associé.
- Lier les sessions ACP : Couvre Lier les sessions ACP dans `dmPolicy`, `allowFrom`, appairage, normalisation de l'identité de l'expéditeur et comportement d'appairage, d'accès et de routage de session DM associé.
- Politique de groupe : Couvre Politique de groupe dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation.
- Mentions : Couvre Mentions dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation.
- Invites système : Couvre Invites système dans `groupPolicy`, `groupAllowFrom`, `groups`, entrées de registre générique, `requireMention`, modèles de mention, outils par groupe, invites système par groupe, sessions de groupe et avertissements pour erreur de configuration de liste d'autorisation.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - La documentation explique les modes de politique DM, la forme de la liste d'autorisation, les approbations d'appairage et le dépannage.
  - La source résout les décisions d'expéditeur direct, les demandes d'appairage, l'autorisation de commande, les liaisons de conversation et les alias d'identité de l'expéditeur.
  - Les tests unitaires couvrent les classes d'entrée de liste d'autorisation, l'authentification du magasin en mode appairage, la classification des commandes, les identifiants de conversation ACP actuels et le comportement de cible de l'outil de message.
  - Les scripts de seed/e2e du canal MCP incluent une conversation iMessage amorcée via les surfaces Gateway/MCP.
- Signaux négatifs :
  - Aucun scénario d'appairage DM iMessage en direct n'a été trouvé.
  - Les anciennes clés de session BlueBubbles ne sont pas transférées automatiquement.
  - La normalisation réelle des handles Apple reste plus large que les données de test synthétiques.
- Lacunes d'intégration :
  - Ajouter un flux DM en direct ou faux-imsg qui commence à partir de la politique d'appairage, envoie le premier DM, approuve, lie une conversation ACP et vérifie l'autorisation de commande ultérieure.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl :
  - `channels.imessage allowFrom` a retourné #73822 pour les numéros de téléphone SecretRef, #58057 pour la résolution d'identité dynamique pour les listes d'autorisation et #81876 pour le comportement de liste d'autorisation DM par défaut après l'amorçage du premier propriétaire.
  - `iMessage dmPolicy allowFrom pairing sender authorization` n'a retourné aucun résultat direct dans la dernière passe gitcrawl.
- Rapports Discrawl :
  - `iMessage dmPolicy allowFrom pairing sender authorization` n'a retourné aucun extrait.
  - `iMessage groupPolicy groups groupAllowFrom requireMention` a retourné des extraits de support qui discutent également des paramètres DM `dmPolicy` et `allowFrom`.
- Bonnes qualités :
  - Le chemin de configuration rejette les entrées de cible de chat dans `allowFrom` DM, réduisant une erreur de politique courante.
  - L'autorisation de commande est séparée de l'admission DM ordinaire si nécessaire.
  - La résolution de l'identifiant de conversation ACP gère les cibles iMessage directes et supprime les préfixes de canal.
  - L'échec de la demande d'appairage est surfacé comme une erreur d'exécution visible par l'opérateur.
- Mauvaises qualités :
  - Les formats d'identité sont nombreux et fournis par l'opérateur.
  - Les travaux SecretRef et d'identité dynamique dans les problèmes adjacents montrent que le modèle de configuration évolue toujours.
  - La migration de session à partir des anciennes clés BlueBubbles est une rupture documentée plutôt qu'une transition gérée par le code.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Autoriser les expéditeurs directs, Router les conversations directes, Lier les sessions ACP, Politique de groupe, Mentions, Invites système.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve d'appairage DM en direct est manquante.
- La normalisation des handles dépend des entrées réelles de téléphone/e-mail/préfixe de service.
- La continuité de la session BlueBubbles ancienne n'est pas automatique.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:223` : `channels.imessage.dmPolicy` contrôle les messages directs.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:227` : la politique de MD ouverte nécessite que `allowFrom` inclue `"*"`.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:230` : `channels.imessage.allowFrom` est le champ de liste blanche des MD.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:232` : les entrées de liste blanche doivent identifier les expéditeurs ; les cibles de conversation appartiennent aux listes blanches de groupe ou aux groupes.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:785` : le dépannage inclut `dmPolicy`, `allowFrom` et les approbations d'appairage.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:105` : `dmPolicy` de BlueBubbles correspond à `dmPolicy` d'iMessage.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:106` : `allowFrom` de BlueBubbles correspond à `allowFrom` d'iMessage, mais les approbations d'appairage sont transférées par handle, pas par token.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/setup-core.ts:62` : la configuration rejette les entrées de liste blanche de MD qui sont des cibles de conversation.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/setup-core.ts:138` : la configuration résout la politique de MD du compte avec l'appairage par défaut.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:200` : l'exécution normalise `allowFrom` de MD.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:225` : l'exécution définit par défaut la politique de MD à `pairing`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:571` : les décisions d'appairage sont converties en gestion des demandes d'appairage.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.ts:529` : les décisions d'expéditeur peuvent retourner une demande d'appairage.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.ts:532` : les journaux d'expéditeur bloqué incluent la politique de MD active.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.ts:684` : le contexte de réponse porte les informations de liste blanche pour l'authentification des commandes.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-seed.ts:51` : amorce une session avec le canal de contexte de livraison `imessage`.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:100` : le client MCP Docker du canal s'attend à un canal de contexte de livraison amorcé `imessage`.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:154` : la conversation amorcée est retournée comme `imessage`.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/commands-acp/context.test.ts:668` : le contexte ACP résout les identifiants de conversation de MD iMessage à partir des cibles actuelles.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.test.ts:888` : les MD en mode ouvert sans listes blanches ne sont pas auto-autorisés pour les commandes.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.test.ts:897` : la liste blanche du magasin en mode appairage autorise les commandes de MD.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.test.ts:912` : les commandes de contrôle iMessage autorisées deviennent des tours de commande texte.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-auth.test.ts:5` : l'authentification de l'approbateur autorise les handles et ignore les entrées de cible de conversation.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/commands-acp/context.test.ts:705` : le contexte ACP résout les identifiants de conversation de MD iMessage à partir des cibles actuelles.
- `/Users/kevinlin/code/openclaw/src/agents/tools/message-tool.test.ts:1493` : les tests d'outil de message définissent un plugin de canal iMessage pour le comportement de description/cible.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "channels.imessage allowFrom" --json --limit 6`

Résultats :

- #73822 : support SecretRef pour les numéros de téléphone dans les configurations de canal.
- #58057 : résolution d'identité dynamique pour les listes blanches.
- #81876 : comportement de liste blanche par défaut de MD de canal après l'amorçage du premier propriétaire.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage dmPolicy allowFrom pairing sender authorization" --json --limit 6`

Résultats :

- Aucun résultat direct dans la dernière passe.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage dmPolicy allowFrom pairing sender authorization" --limit 6`

Résultats :

- Aucun extrait retourné.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage groupPolicy groups groupAllowFrom requireMention" --limit 6`

Résultats :

- Les extraits de support incluaient des exemples de configuration avec `dmPolicy: "pairing"` et des conseils `allowFrom` aux côtés de la configuration de groupe.
