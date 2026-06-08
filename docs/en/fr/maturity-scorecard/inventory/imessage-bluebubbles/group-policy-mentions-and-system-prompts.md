---
title: "iMessage / BlueBubbles - Group Policy, Mentions, and System Prompts Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Group Policy, Mentions, and System Prompts Maturity Note

## Résumé

La politique de groupe, les mentions et les invites système sont en version bêta. La documentation et l'exécution modélisent tous deux l'admission aux groupes iMessage comme deux portes : liste blanche d'expéditeur/chat et registre de groupe. Le composant dispose de tests solides autour de la gestion des mentions, du comportement de la liste blanche de groupe, du contexte de réponse et des journaux d'avertissement. Il reste en version bêta car le modèle d'opérateur est subtil, en particulier pour les configurations BlueBubbles migrées et pour le manque de métadonnées de mention natives fiables d'iMessage.

## Portée de la catégorie

Cette note couvre `groupPolicy`, `groupAllowFrom`, `groups`, les entrées de registre avec caractères génériques, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour les erreurs de configuration de liste blanche.

## Fonctionnalités

- Group Policy : Couvre la politique de groupe dans `groupPolicy`, `groupAllowFrom`, `groups`, les entrées de registre avec caractères génériques, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour les erreurs de configuration de liste blanche.
- Mentions : Couvre les mentions dans `groupPolicy`, `groupAllowFrom`, `groups`, les entrées de registre avec caractères génériques, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour les erreurs de configuration de liste blanche.
- System Prompts : Couvre les invites système dans `groupPolicy`, `groupAllowFrom`, `groups`, les entrées de registre avec caractères génériques, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour les erreurs de configuration de liste blanche.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (75%)`
- Signaux positifs :
  - La documentation explique les deux portes de groupe indépendantes et le piège de migration.
  - La source normalise les listes blanches de groupe, résout la politique de groupe, applique la politique de mention, émet des avertissements au démarrage/par chat et construit le contexte de groupe.
  - Les tests unitaires couvrent les groupes supprimés, le repli de liste blanche, les listes blanches explicitement vides, l'authentification des commandes de groupe, les exigences de caractères génériques et le comportement d'avertissement.
  - L'archive Discord contient des extraits de support réels pour les modèles de configuration de groupe.
- Signaux négatifs :
  - Aucun scénario de groupe iMessage en direct n'a été trouvé.
  - La détection de mention dépend des modèles de texte plutôt que des métadonnées natives d'iMessage.
  - Les configurations migrées peuvent bloquer silencieusement les groupes si l'entrée de caractère générique `groups` n'est pas copiée.
- Lacunes d'intégration :
  - Ajouter une voie de groupe iMessage en direct/faux pour le groupe autorisé, le groupe bloqué, la mention requise, pas de mention et les paramètres de prompt/outil par groupe.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl :
  - `channels.imessage.groups groupPolicy` a retourné #58057 pour la résolution d'identité dynamique et #79281 pour le préréglage de liaison de thread ACP par défaut mentionnant le groupage iMessage/BlueBubbles.
  - `iMessage groupPolicy groups groupAllowFrom requireMention` n'a retourné aucun résultat gitcrawl direct lors du dernier passage.
- Rapports Discrawl :
  - `iMessage groupPolicy groups groupAllowFrom requireMention` a retourné plusieurs extraits de support avec des exemples `groupPolicy: "allowlist"`, `groupAllowFrom`, `groups` et `requireMention`.
  - Une réponse de support de février 2026 a souligné que les groupes iMessage ont besoin de vérifications de gating de groupe et de gating de mention.
- Bonnes qualités :
  - La documentation et la source s'accordent sur le modèle à deux portes.
  - Les avertissements ciblent l'exact échec de migration : `groupPolicy="allowlist"` avec `groups` manquant ou vide.
  - L'implémentation distingue les entrées de liste blanche de conversation héritées, le `groupAllowFrom` explicite et l'autorisation de commande de contrôle de groupe.
  - Les paramètres de prompt/outil par groupe sont liés au résolveur de politique de groupe plutôt qu'à une branchement ad hoc.
- Mauvaises qualités :
  - La configuration est puissante mais facile à copier partiellement.
  - Le comportement de mention est intrinsèquement moins fiable que les mentions natives de Slack/Discord.
  - Les identifiants de chat de groupe peuvent être représentés comme chat id, chat guid ou chat identifier, ce qui augmente le risque d'erreur d'opérateur.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Beta (75%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la politique de groupe, les mentions et les invites système.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve de groupe en direct est manquante.
- Le gating de mention repose sur des modèles de texte configurés.
- La migration depuis BlueBubbles est vulnérable aux entrées `groups` de caractère générique manquantes.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:237` : `channels.imessage.groupPolicy` contrôle la gestion des groupes.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:243` : `channels.imessage.groupAllowFrom` est la liste blanche d'expéditeur de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:253` : la liste blanche d'expéditeur/cible de chat est la première porte de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:254` : `channels.imessage.groups` est la porte de registre de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:258` : l'avertissement au démarrage se déclenche lorsque le mode liste blanche a des groupes vides.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:126` : la documentation de migration décrit la porte de liste blanche d'expéditeur/cible de chat.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:127` : la documentation de migration décrit la porte de registre de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:138` : `groups` manquant est appelé comme l'échec de migration courant.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:644` : la référence de configuration avertit de configurer les identifiants de chat explicites ou les entrées de caractère générique avec le mode liste blanche de groupe.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:52` : le chemin de politique de groupe est `channels.imessage.groupPolicy`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:53` : le chemin de liste blanche de groupe est `channels.imessage.groupAllowFrom`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:208` : l'exécution résout la politique de groupe du fournisseur ouvert.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:550` : l'exécution avertit les opérateurs qui définissent le mode liste blanche de groupe sans groupes.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.ts:719` : le traitement entrant résout les exigences de mention de groupe.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/inbound-processing.ts:758` : les messages de groupe peuvent être ignorés lorsque la mention est requise et absente.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/commands-acp/context.test.ts:686` : le contexte ACP résout les identifiants de conversation de groupe iMessage à partir des cibles de chat explicites.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/commands-acp/context.test.ts:723` : le contexte ACP résout les identifiants de conversation de groupe iMessage à partir des cibles `chat_id`.
- Aucune voie de moniteur de groupe iMessage en direct n'a été trouvée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.gating.test.ts:137` : supprime les messages de groupe sans mention par défaut.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.gating.test.ts:155` : distribue les messages de groupe avec mention et construit une enveloppe de groupe.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.gating.test.ts:433` : bloque les messages de groupe lorsque `imessage.groups` est défini sans caractère générique.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.gating.test.ts:465` : honore la liste blanche de groupe et ignore les expéditeurs du magasin d'appairage dans les groupes.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.gating.test.ts:546` : `groupAllowFrom` explicitement vide empêche le repli de liste blanche de conversation héritée.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.gating.test.ts:613` : les commandes de contrôle de groupe ne sont pas autorisées à partir des entrées de liste blanche de conversation.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/group-allowlist-warnings.test.ts:13` : l'avertissement se déclenche lorsque le mode liste blanche a des groupes non définis.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/group-allowlist-warnings.test.ts:52` : l'avertissement ne se déclenche pas lorsqu'une entrée de groupe avec caractère générique existe.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "channels.imessage.groups groupPolicy" --json --limit 6`

Résultats :

- #58057 : résolution d'identité dynamique pour les listes blanches.
- #79281 : le préréglage de liaison de thread ACP par défaut référence le comportement de groupage iMessage/BlueBubbles.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage groupPolicy groups groupAllowFrom requireMention" --json --limit 6`

Résultats :

- Aucun résultat direct lors du dernier passage.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage groupPolicy groups groupAllowFrom requireMention" --limit 6`

Résultats :

- Plusieurs extraits de support de février et mars 2026 ont montré des exemples de configuration `groupPolicy: "allowlist"`, `groupAllowFrom`, `groups` et `requireMention`.
- Une réponse de support de février 2026 a averti que les groupes iMessage ont besoin de politique de groupe, de vérifications `groupAllowFrom` et de gating de mention.
