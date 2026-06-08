---
title: "Slack - Access and Identity Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Access and Identity Maturity Note

## Résumé

L'accès Slack DM est implémenté avec appairage, listes blanches, mode ouvert gardé par `allowFrom: ["*"]`, contrôles de DM de groupe, héritage de compte et autorisation de commande. Le composant est en Beta car l'implémentation et la documentation sont larges, tandis que la confusion des opérateurs persiste autour de l'appairage dans l'hébergement géré, les remplacements au niveau du compte, les DM de groupe, les listes blanches des propriétaires et les contrôles manquants de liste blanche DM sortante.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Access and Identity`
- Fusionnée à partir de : `Conversation Access and Routing`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Listes blanches de canaux : Couvre les listes blanches de canaux, `groupPolicy`, portes canal/utilisateur, portes de mention et comportement de mention de sous-équipe.
- Routage des fils : Couvre le routage des fils Slack, le ciblage des réponses conscientes des fils et la liaison de session pour les fils de canal.
- Isolation de session : Couvre l'isolation de session sur les listes blanches de canaux, `groupPolicy`, portes canal/utilisateur, comportement de mention et de mention de sous-équipe, et le routage de canal/fil associé et le comportement d'isolation de session.
- Appairage DM : Couvre l'appairage DM sur le routage DM Slack, `dmPolicy`, `allowFrom`, approbations d'appairage, DM de groupe/MPIM, héritage de liste blanche au niveau du compte, autorisation de commande dans les DM et normalisation de l'identité de l'expéditeur.
- Autorisation de l'expéditeur : Couvre l'autorisation de l'expéditeur sur le routage DM Slack, `dmPolicy`, `allowFrom`, approbations d'appairage, DM de groupe/MPIM, héritage de liste blanche au niveau du compte, autorisation de commande dans les DM et normalisation de l'identité de l'expéditeur.

## Fonctionnalités

- Access and Identity : Portée des preuves pour Access and Identity.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : Les sources et les tests couvrent la précédence de la liste blanche, les garde-fous du mode ouvert, les messages d'appairage, l'authentification DM, l'héritage de compte nommé, les drapeaux DM de groupe, l'autorisation de commande et le comportement de liste blanche-bloc Slack en direct.
- Signaux négatifs : La voie Slack en direct est centrée sur les canaux et n'exécute pas encore un ensemble complet de scénarios d'appairage/ouverture/liste blanche/DM de groupe.
- Lacunes d'intégration : Besoin de couverture en direct pour l'appairage Slack DM pour la première fois, l'intégration de liste blanche gérée/RPC, les conflits de remplacement de compte, l'activation MPIM et la copie d'opérateur d'expéditeur bloqué.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : `#86983` demande une liste blanche DM sortante, et les résultats plus larges de Slack `dmPolicy allowFrom` incluent la confusion de fil/routage et de réécriture de configuration.
- Rapports Discrawl : Les fils de support montrent des utilisateurs d'hébergement géré demandant comment éviter l'appairage CLI, pourquoi `dmPolicy: "open"` demande toujours l'appairage et comment `allowFrom` au niveau supérieur par rapport au niveau du compte affecte le comportement.
- Bonnes qualités : Le schéma de configuration rejette `dmPolicy="open"` sans liste blanche générique, la documentation indique les politiques DM et la précédence multi-compte, et la source échoue les expéditeurs non autorisés fermés.
- Mauvaises qualités : L'appairage est toujours maladroit pour les installations sans terminal, la configuration au niveau du compte est facile à mal appliquer, le comportement DM de groupe est opt-in et les envois DM sortants ont moins de contrôle de politique que l'admission DM entrante.
- Exclu de la qualité : Nombre de tests unitaires, largeur de voie en direct et profondeur d'intégration.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les documents archivés, la source, le test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Access and Identity.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter l'appairage DM en direct, la liste blanche DM, l'ouverture DM et les scénarios MPIM.
- Ajouter des conseils de gestion d'appairage RPC/tableau de bord pour les déploiements Slack hébergés.
- Ajouter l'autorisation de cible DM sortante afin que `allowFrom` entrant n'implique pas des DM initiés par l'agent sans restriction.

## Preuves

### Docs

- `docs/channels/slack.md` documente `dmPolicy`, `allowFrom` canonique, drapeaux DM de groupe, précédence multi-compte, migration héritée et `openclaw pairing approve slack <code>`.
- `docs/channels/pairing.md` est lié à partir de la documentation Slack en tant que modèle d'appairage partagé.

### Source

- `extensions/slack/src/config-schema.ts` valide la politique DM et rejette la politique DM ouverte sans liste blanche générique.
- `extensions/slack/src/accounts.ts` résout `allowFrom` de compte par défaut/nommé et `dm.allowFrom` hérité.
- `extensions/slack/src/monitor/dm-auth.ts`, `extensions/slack/src/monitor/auth.ts` et `extensions/slack/src/monitor/message-handler/prepare.ts` appliquent l'autorisation de l'expéditeur Slack avant la distribution.
- `extensions/slack/src/monitor/slash.ts` applique l'autorisation de commande et les réponses d'expéditeur bloqué pour les commandes Slack.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` inclut `slack-allowlist-block`, qui vérifie les expéditeurs de canal bloqués dans un espace de travail en direct.
- Aucun scénario complet d'appairage Slack DM en direct ou MPIM n'a été trouvé.

### Tests unitaires

- `extensions/slack/src/config-schema.test.ts` couvre `dmPolicy="open"` et le comportement de politique hérité.
- `extensions/slack/src/accounts.test.ts` couvre la précédence de la liste blanche, l'héritage de compte nommé, la gestion des alias hérités et les clés de compte en casse mixte.
- `extensions/slack/src/monitor/dm-auth.test.ts`, `extensions/slack/src/monitor/allow-list.test.ts`, `extensions/slack/src/resolve-allowlist-common.test.ts` et `src/pairing/pairing-messages.test.ts` couvrent l'authentification DM et la copie d'appairage.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "Slack dmPolicy allowFrom pairing group DM authorization" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "slack dmPolicy allowFrom" --json`

Résultats :

- La recherche de problème ciblée a retourné `[]`.
- La requête plus large a retourné `#86983`, "Feature request: Outbound DM allowlist (dmAllowTo)", plus les résultats de configuration/routage adjacents impliquant Slack `dmPolicy` et `allowFrom`.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack dmPolicy allowFrom pairing"`

Résultats :

- A retourné les discussions de configuration hébergée et d'appairage Slack DM, y compris les frictions d'appairage sans CLI, `dmPolicy="open"` nécessitant `allowFrom: ["*"]`, les conseils de remplacement au niveau du compte, les notes de portée MPIM/session et la confusion d'exécution lorsque l'appairage apparaît toujours.
