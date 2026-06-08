---
title: "Microsoft Teams - Sso, Delegated Auth, Graph Directory, and Member Info Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Sso, Delegated Auth, Graph Directory, and Member Info Maturity Note

## Résumé

La prise en charge de Teams Graph et de l'authentification déléguée est importante pour l'utilisation en entreprise, mais elle manque encore de preuves. La source couvre l'authentification unique Bot Framework, le stockage/l'actualisation des jetons OAuth délégués, la résolution des jetons Graph, la recherche d'annuaire, les informations de membre et la détection des rôles/portées Graph. La couverture et la qualité restent Alpha car ces flux dépendent de l'enregistrement des applications de locataire, du consentement administrateur et de la configuration Graph inter-locataires qui manquent de preuves de scénario durables et ont encore des travaux d'archive actifs.

## Portée de la catégorie

Cette catégorie couvre les appels SSO Bot Framework, l'échange de jetons OAuth, le stockage et l'actualisation des jetons délégués, la résolution des jetons d'application Graph, les portées et rôles Graph, l'énumération des pairs/groupes d'annuaire, la recherche d'utilisateurs Graph, l'action d'informations de membre, l'accès Graph inter-locataires et les limitations de Graph en Chine.

## Fonctionnalités

- Appels SSO Bot Framework : Couvre la gestion des appels SSO Bot Framework et l'échange de jetons OAuth pour les utilisateurs Microsoft Teams.
- Stockage des jetons délégués : Couvre le stockage des jetons délégués, l'actualisation des jetons et la récupération pour l'authentification des utilisateurs Microsoft Teams.
- Recherche d'annuaire Graph : Couvre la résolution des jetons d'application Graph et le comportement de recherche d'annuaire pour le routage Teams et les métadonnées utilisateur.
- Recherche de profil de membre : Couvre la recherche d'informations de membre et la récupération de métadonnées utilisateur pour les conversations Microsoft Teams.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (60%)`
- Signaux positifs : La documentation et la source couvrent la configuration SSO, l'authentification déléguée, les jetons Graph, l'énumération d'annuaire, les informations de membre, les sondes de rôles/portées Graph et les prérequis de consentement administrateur.
- Signaux négatifs : Aucun scénario Teams SSO en direct, consentement délégué, informations de membre ou Graph inter-locataires n'a été trouvé.
- Lacunes d'intégration : Preuve manquante pour l'échange de jetons réussi, consentement manquant, jetons délégués expirés, octrois de consentement administrateur, Graph inter-locataires et comportement Graph désactivé en Chine.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : La recherche large a retourné `#78839` porte d'action d'informations de membre, `#77784` authentification déléguée pour les outils de plugin, `#67174/#87169` travail de locataire Teams Graph séparé et commentaires d'examen sur l'authentification Graph fédérée.
- Rapports Discrawl : La requête SSO/authentification déléguée ciblée n'a retourné aucune ligne ; la recherche large a retourné une discussion sur la migration du SDK Teams et des préoccupations concernant les membres/contexte.
- Bonnes qualités : La gestion des appels SSO est protégée par authentification, les jetons sont persistés avec les métadonnées de connexion, les sondes signalent les rôles/portées Graph et les actions d'annuaire/membre sont séparées derrière les adaptateurs d'exécution.
- Mauvaises qualités : Le comportement de Graph dépend de l'état du locataire administrateur, des autorisations, de la configuration inter-locataires et des points de terminaison cloud ; le travail d'archive actif montre que cette surface est encore en mouvement.
- Exclu de la qualité : Étendue des tests unitaires, couverture des maquettes d'annuaire et absence de tests SSO en direct.

## Score de complétude

- Score : `Alpha (60%)`
- Instructions de surface : évaluées par rapport à `references/completeness/microsoft-teams.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les appels SSO Bot Framework, le stockage des jetons délégués, la recherche d'annuaire Graph et la recherche de profil de membre.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario d'entreprise en direct pour l'échange de jetons SSO Bot Framework et l'utilisation des jetons Graph délégués.
- Ajouter des scénarios pour le consentement administrateur manquant, les jetons délégués expirés et la configuration du locataire Graph inter-locataires.
- Ajouter le comportement documenté de la Chine/21Vianet pour les assistants Graph désactivés.

## Preuves

### Documentation

- `docs/channels/msteams.md` documente l'authentification fédérée, les autorisations Graph, les exigences d'informations de membre, les médias/historique activés par Graph, la configuration liée à l'authentification déléguée, la sortie de la sonde de rôles/portées Graph et les limitations de Graph en Chine.

### Source

- `src/config/types.msteams.ts` définit la configuration `delegatedAuth` et `sso`.
- `extensions/msteams/src/monitor.ts` enregistre les gestionnaires d'appels de connexion, délègue via les gestionnaires SDK et persiste les jetons SSO après les événements de connexion autorisés.
- `extensions/msteams/src/sso.ts` gère l'échange de jetons Bot Framework et les flux de vérification d'état.
- `extensions/msteams/src/sso-token-store.ts` persiste les métadonnées des jetons SSO.
- `extensions/msteams/src/oauth.ts`, `oauth.flow.ts`, `oauth.token.ts` et `token.ts` implémentent OAuth délégué, rappel local, actualisation des jetons et stockage des jetons délégués.
- `extensions/msteams/src/graph.ts` résout les jetons Graph.
- `extensions/msteams/src/directory-live.ts`, `graph-users.ts`, `graph-members.ts` et `channel.runtime.ts` implémentent les adaptateurs d'exécution d'annuaire et d'informations de membre.
- `extensions/msteams/src/probe.ts` signale les rôles/portées Graph et l'état des jetons délégués.

### Tests d'intégration

- Aucun scénario Teams SSO/authentification déléguée/informations de membre en direct n'a été trouvé par `rg`.
- `directory-live.test.ts` est simulé et ne prouve pas un vrai locataire Graph.

### Tests unitaires

- `extensions/msteams/src/monitor-handler.sso.test.ts` et `monitor.lifecycle.test.ts` couvrent les portes d'authentification des appels de connexion et le routage.
- `extensions/msteams/src/sso-token-store.test.ts` couvre le stockage des jetons.
- `extensions/msteams/src/oauth.test.ts` couvre les assistants OAuth délégués.
- `extensions/msteams/src/graph.test.ts` couvre le comportement des jetons Graph.
- `extensions/msteams/src/directory-live.test.ts`, `graph-users.test.ts` si présent et `graph-members.test.ts` couvrent les flux d'annuaire/membre simulés.
- `extensions/msteams/src/probe.test.ts` couvre la sortie de la sonde.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "msteams SSO delegated auth Graph tenant member-info" --json --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams Microsoft Teams" --json --limit 10`

Résultats :

- La requête SSO/authentification déléguée ciblée a retourné `[]`.
- La recherche large a retourné `#78839`, `#77784`, `#67174` et `#87169` couvrant les informations de membre, l'authentification déléguée et le travail de locataire Graph.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams SSO delegated auth Graph tenant member-info"`

Résultats :

- La requête ciblée n'a retourné aucune ligne.
