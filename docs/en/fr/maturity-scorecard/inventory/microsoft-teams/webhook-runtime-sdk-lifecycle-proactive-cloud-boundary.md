---
title: "Microsoft Teams - Webhook Runtime, SDK Lifecycle, and Proactive Cloud Boundary Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Webhook Runtime, SDK Lifecycle, and Proactive Cloud Boundary Maturity Note

## Résumé

Le chemin webhook/runtime Teams est l'une des familles Teams les plus solides. La source utilise le SDK Teams pour l'authentification et les activités typées, dispose d'un renforcement HTTP explicite et valide les limites `serviceUrl` proactives sur les clouds publics et non publics. La couverture est Beta car il existe une preuve locale de serveur/runtime et les documents affirment une validation en direct sur le cloud public, mais la preuve actuelle du cloud non public et de l'opération proactive n'est pas une preuve en direct durable.

## Portée de la catégorie

Cette catégorie couvre le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-gate bearer, les limites de corps JSON, les gestionnaires d'invocation typés, le transfert de points de terminaison hérités, le routage des sondages/consentement de fichier/connexion/retour d'information/activité, les délais d'expiration du serveur, l'arrêt, les références de conversation stockées, les envois/modifications/suppressions proactifs et les limites d'URL de service pour Public, GCC, GCC High, DoD et China/21Vianet.

## Fonctionnalités

- Webhook Runtime : Couvre Webhook Runtime sur le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-gate bearer, les limites de corps JSON et le comportement associé du webhook runtime, du cycle de vie du SDK et de la limite de cloud proactive.
- SDK Lifecycle : Couvre SDK Lifecycle sur le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-gate bearer, les limites de corps JSON et le comportement associé du webhook runtime, du cycle de vie du SDK et de la limite de cloud proactive.
- Proactive Cloud Boundary : Couvre Proactive Cloud Boundary sur le démarrage du serveur webhook, la gestion de l'authentification/JWT du SDK, la pré-gate bearer, les limites de corps JSON et le comportement associé du webhook runtime, du cycle de vie du SDK et de la limite de cloud proactive.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`
- Signaux positifs : Les documents indiquent que le chemin soutenu par le SDK est validé en direct pour le cloud public, et les tests locaux de serveur/runtime couvrent le webhook, le cycle de vie, les délais d'expiration, la validation du cloud, les références proactives et les coutures d'authentification du SDK.
- Signaux négatifs : Aucun rapport de scénario durable sur le cloud public ou le cloud souverain n'a été trouvé pour les opérations proactives d'envoi/modification/suppression, de consentement de fichier, de carte, de sondage et en file d'attente.
- Lacunes d'intégration : Preuve en direct manquante pour GCC, GCC High, DoD, China et actualisation des références stockées après les modifications de cloud/URL de service.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : `#76262` a refondu Teams sur le SDK Teams et a signalé les correctifs de streaming/carte/modification/suppression/SSO ; les recherches de problèmes d'URL de service ciblées n'ont retourné aucun résultat direct.
- Rapports Discrawl : La recherche large `msteams` a retourné une préoccupation d'examen du responsable pour la grande migration du SDK Teams et les avertissements antérieurs concernant l'authentification JSON, la sémantique des réponses d'invocation, le routage `serviceUrl` stocké et le contournement de l'âge de la version.
- Bonnes qualités : Le runtime valide l'authentification avant la distribution, limite les corps de requête, centralise le routage d'invocation typé, applique les délais d'expiration du serveur, échoue fermé pour les URL de service non prises en charge et stocke les données de référence de locataire/service pour les envois proactifs.
- Mauvaises qualités : La migration du SDK est importante et récente ; le cloud public est le seul cloud validé en direct documenté, tandis que le support du cloud non public est principalement soutenu par la source/documentation.
- Exclu de la qualité : Étendue des tests, nombre de tests de serveur local et manque de couverture e2e en direct.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/microsoft-teams.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Webhook Runtime, SDK Lifecycle, Proactive Cloud Boundary.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario en direct sur le cloud public qui couvre les DM entrants, le canal entrant, la réponse proactive, la modification/suppression, la carte, le consentement de fichier et la réponse finale en file d'attente.
- Ajouter des scénarios de contrat de cloud non public ou des vérifications d'état explicitement non pris en charge.
- Ajouter des notes de version qui expliquent la limite de compatibilité de la migration du SDK Teams.

## Preuve

### Docs

- `docs/channels/msteams.md` documente les délais d'expiration du webhook, la messagerie proactive, la validation en direct du cloud public, la configuration `cloud` et `serviceUrl` du cloud non public, les hôtes proactifs acceptés, le comportement de China et les exigences d'actualisation de l'URL de service.

### Source

- `extensions/msteams/src/monitor.ts` démarre le webhook Express, pré-gate l'authentification Bearer manquante, limite la taille du corps JSON, délègue au SDK Teams, enregistre les gestionnaires typés de carte/consentement de fichier/connexion/retour d'information/activité, applique les délais d'expiration du webhook et expose l'arrêt.
- `extensions/msteams/src/sdk.ts` charge l'authentification du SDK Teams et l'intégration du fournisseur de jetons.
- `extensions/msteams/src/cloud.ts` résout la configuration du cloud et valide les limites d'URL de service proactives.
- `extensions/msteams/src/sdk-proactive.ts` construit les références de conversation du SDK, valide les URL de service stockées/configurées et envoie/met à jour/supprime les activités proactives.
- `extensions/msteams/src/bot-framework-service-url.ts` normalise les URL de service Bot Framework.

### Tests d'intégration

- `extensions/msteams/src/monitor.test.ts` exerce un chemin de serveur HTTP/socket local pour le comportement du délai d'expiration du webhook.
- Aucun fichier de scénario e2e durable sur le cloud public Teams ou le cloud souverain n'a été trouvé par `rg`.

### Tests unitaires

- `extensions/msteams/src/cloud.test.ts` couvre la validation des limites d'URL de service et de cloud.
- `extensions/msteams/src/sdk-proactive.test.ts` couvre la gestion des références proactives.
- `extensions/msteams/src/monitor.lifecycle.test.ts` couvre les gestionnaires typés et le routage de la pré-gate d'authentification.
- `extensions/msteams/src/auth-coverage.test.ts` couvre les coutures de validation des jetons.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "msteams Teams serviceUrl webhook proactive send cloud USGov DoD China" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams file consent serviceUrl" --json --limit 10`

Résultats :

- La recherche de problèmes d'URL de service ciblée a retourné `[]`.
- La requête d'URL de service plus large a retourné `#76262`, "fix(msteams): rebase TeamsSDK patterns to simplify Teams Integration".

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams serviceUrl proactive public cloud GCC China"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams"`

Résultats :

- La requête d'URL de service ciblée n'a retourné aucune ligne.
- La requête large `msteams` a retourné une discussion d'examen de la migration du SDK Teams, y compris une mise en garde du responsable concernant l'analyse de l'authentification, les réponses d'invocation, le routage de l'URL de service stockée et la nécessité de tests de fumée de locataire Teams réels.
