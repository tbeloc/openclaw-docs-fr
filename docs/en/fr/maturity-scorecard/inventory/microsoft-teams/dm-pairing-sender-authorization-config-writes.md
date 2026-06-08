---
title: "Microsoft Teams - Note de Maturité Accès et Identité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Note de Maturité Accès et Identité

## Résumé

Les DM Teams et l'autorisation de l'expéditeur sont source-strong : le plugin utilise une politique d'entrée partagée, des ID d'objet AAD stables par défaut, des listes blanches de magasin d'appairage et des portes d'invocation explicites. La couverture reste Alpha car l'audit n'a pas trouvé de scénario d'appairage Teams en direct ou de preuve de flux d'administrateur d'entreprise pour les listes blanches résolues par Graph et les écritures de configuration.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Accès et Identité`
- Fusionnée à partir de : `Identité et Autorisation`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Appairage DM : Couvre l'appairage DM sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Identité stable de l'expéditeur : Couvre l'identité stable de l'expéditeur sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Listes blanches et groupes d'accès : Couvre les listes blanches et groupes d'accès sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Autorisation d'invocation et de commande : Couvre l'autorisation d'invocation et de commande sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Écritures de configuration originaires de Teams : Couvre les écritures de configuration originaires de Teams sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Invocations SSO Bot Framework : Couvre la gestion des invocations SSO Bot Framework et l'échange de jetons OAuth pour les utilisateurs Microsoft Teams.
- Stockage de jetons délégués : Couvre le stockage de jetons délégués, l'actualisation des jetons et la récupération pour l'authentification des utilisateurs Microsoft Teams.
- Recherche d'annuaire Graph : Couvre la résolution des jetons d'application Graph et le comportement de recherche d'annuaire pour le routage Teams et les métadonnées utilisateur.
- Recherche de profil de membre : Couvre la recherche d'informations de membre et la récupération de métadonnées utilisateur pour les conversations Microsoft Teams.
- Invocations SSO Bot Framework : Couvre la gestion des invocations SSO Bot Framework et l'échange de jetons OAuth pour les utilisateurs Microsoft Teams
- Stockage de jetons délégués : Couvre le stockage de jetons délégués, l'actualisation des jetons et la récupération pour l'authentification des utilisateurs Microsoft Teams
- Recherche d'annuaire Graph : Couvre la résolution des jetons d'application Graph et le comportement de recherche d'annuaire pour le routage Teams et les métadonnées utilisateur
- Recherche de profil de membre : Couvre la recherche d'informations de membre et la récupération de métadonnées utilisateur pour les conversations Microsoft Teams

## Fonctionnalités

- Appairage DM : Couvre l'appairage DM sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Identité stable de l'expéditeur : Couvre l'identité stable de l'expéditeur sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Listes blanches et groupes d'accès : Couvre les listes blanches et groupes d'accès sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Autorisation d'invocation et de commande : Couvre l'autorisation d'invocation et de commande sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Écritures de configuration originaires de Teams : Couvre les écritures de configuration originaires de Teams sur l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et comportement d'appairage DM et d'accès de l'expéditeur associé.
- Invocations SSO Bot Framework : Couvre la gestion des invocations SSO Bot Framework et l'échange de jetons OAuth pour les utilisateurs Microsoft Teams.
- Stockage de jetons délégués : Couvre le stockage de jetons délégués, l'actualisation des jetons et la récupération pour l'authentification des utilisateurs Microsoft Teams.
- Recherche d'annuaire Graph : Couvre la résolution des jetons d'application Graph et le comportement de recherche d'annuaire pour le routage Teams et les métadonnées utilisateur.
- Recherche de profil de membre : Couvre la recherche d'informations de membre et la récupération de métadonnées utilisateur pour les conversations Microsoft Teams.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (68%)`
- Signaux positifs : La source d'exécution gère la création de demande d'appairage, la correspondance d'ID stable, l'accès aux commandes, le repli de groupe et l'authentification d'invocation ; les tests unitaires exercent ces coutures de politique.
- Signaux négatifs : Aucun rapport de scénario d'appairage Teams en direct, d'expéditeur non autorisé, d'expéditeur autorisé ou d'écriture de configuration n'a été trouvé.
- Lacunes d'intégration : Preuve d'appairage soutenue par le locataire manquante avec ID d'objet AAD, noms résolus par Graph, groupes d'accès, expéditeurs inconnus et bascules d'écriture de configuration.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : Les recherches ciblées pour Teams `dmPolicy`, `allowFrom`, `groupPolicy` et appairage n'ont retourné aucun résultat direct.
- Rapports Discrawl : Les recherches ciblées d'appairage/autorisation n'ont retourné aucune ligne ; le contexte d'archive de canal d'entrée large discute du déplacement de la politique d'entrée de canal de message partagé dans le noyau tout en gardant les faits de plateforme propriétaires du plugin.
- Bonnes qualités : L'accès de l'expéditeur est fermé en cas d'échec, basé sur l'ID, basé sur une politique partagée, conscient de l'appairage et réutilisé pour les invocations de carte/connexion/retour et l'authentification d'approbation.
- Mauvaises qualités : La résolution de nom/UPN dépend de Graph et est intentionnellement dangereuse sauf si elle est activée ; les écritures de configuration sont activées par défaut lorsque la configuration de commande est activée ; la preuve d'administrateur en direct est manquante.
- Exclu de la qualité : Nombre de tests unitaires, profondeur de test d'autorisation et manque de tests d'appairage en direct.

## Score de Complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/microsoft-teams.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'appairage DM, l'identité stable de l'expéditeur, les listes blanches et groupes d'accès, l'autorisation d'invocation et de commande, les écritures de configuration originaires de Teams, les invocations SSO Bot Framework, le stockage de jetons délégués, la recherche d'annuaire Graph, la recherche de profil de membre.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter des scénarios d'appairage DM Teams en direct pour expéditeur inconnu, expéditeur approuvé, DM désactivé, liste blanche, DM ouvert et états d'écriture de configuration désactivés.
- Ajouter une preuve d'opérateur pour les noms d'utilisateur résolus par Graph et le comportement d'échec lorsque les permissions Graph sont manquantes.
- Ajouter un scénario d'authentification d'approbation spécifique à Teams avec des approbateurs GUID AAD.

## Preuves

### Docs

- `docs/channels/msteams.md` documente `dmPolicy="pairing"`, les ID d'objet AAD stables, les groupes d'accès, la correspondance de nom direct désactivée, la résolution de nom Graph et les écritures de configuration.
- `docs/channels/pairing.md` documente les canaux d'appairage pris en charge et indique que l'appairage DM n'accorde pas l'autorisation de groupe.
- `docs/channels/access-groups.md` documente le support des canaux pour les groupes d'accès d'expéditeur statiques.

### Source

- `extensions/msteams/src/monitor-handler/access.ts` résout l'accès de l'expéditeur via l'entrée de canal stable partagée, le magasin d'appairage, `allowFrom`, `groupAllowFrom`, les groupes d'accès, les portes de route et la politique d'identifiant mutable.
- `extensions/msteams/src/monitor-handler/message-handler.ts` supprime les DM non approuvés, crée des demandes d'appairage, enregistre les décisions de liste blanche, bloque les commandes de contrôle non autorisées et enregistre les références de conversation autorisées.
- `extensions/msteams/src/monitor-handler.ts` contrôle les invocations de carte, connexion et retour via la politique de l'expéditeur.
- `extensions/msteams/src/approval-auth.ts` normalise les approbateurs aux identités stables `user:<aad-guid>`.

### Tests d'intégration

- Aucun scénario d'appairage Teams en direct ou e2e n'a été trouvé par `rg`.
- La couverture du flux d'exécution est représentée par les tests de gestionnaire et de cycle de vie, pas par un flux DM soutenu par le locataire.

### Tests unitaires

- `extensions/msteams/src/monitor-handler/message-handler.authz.test.ts` couvre la séparation d'appairage DM, les contrôles non autorisés, les groupes d'accès, le filtrage de citation/thread et le comportement de la politique.
- `extensions/msteams/src/monitor.lifecycle.test.ts` couvre les portes d'authentification de carte, sondage et SSO.
- `extensions/msteams/src/channel.test.ts` couvre l'exposition d'authentification d'approbation et le comportement d'autorisation d'ID Teams stable.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "msteams Teams pairing allowFrom dmPolicy groupPolicy teams channels mention" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams dmPolicy allowFrom groupPolicy pairing" --json --limit 10`

Résultats :

- Les deux recherches ciblées ont retourné `[]`.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams pairing dmPolicy allowFrom sender authorization"`

Résultats :

- La requête ciblée n'a retourné aucune ligne.
