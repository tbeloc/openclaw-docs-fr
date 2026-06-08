---
title: "Google Chat - Webhook Auth Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Webhook Auth Maturity Note

## Résumé

L'ingestion par webhook a une implémentation relativement mature pour une surface Alpha : elle utilise le pipeline de requête webhook partagé, limite le débit par chemin et adresse IP client, vérifie les jetons bearer et add-on du corps, valide la forme de la charge utile et enregistre les raisons de rejet. Le score reste en dessous de Stable en raison des preuves d'archive montrant des boucles 401 récentes, des échecs d'analyse de charge utile add-on et une confusion de liaison de cible, et parce qu'il n'existe pas de voie webhook Google Chat en direct prouvant le chemin complet de Google à la passerelle.

## Portée de la catégorie

Inclus dans cette catégorie :

- Gestion du chemin webhook : couvre la gestion du chemin webhook dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Vérification des jetons Chat standard : couvre la vérification des jetons Chat standard dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Vérification des jetons add-on Workspace : couvre la vérification des jetons add-on Workspace dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Liaison d'audience et appPrincipal : couvre la liaison d'audience et appPrincipal dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Sélection de cible de chemin partagé : couvre la sélection de cible de chemin partagé dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Diagnostics de rejet d'authentification : couvre les diagnostics de rejet d'authentification dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.

## Fonctionnalités

- Gestion du chemin webhook : couvre la gestion du chemin webhook dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Vérification des jetons Chat standard : couvre la vérification des jetons Chat standard dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Vérification des jetons add-on Workspace : couvre la vérification des jetons add-on Workspace dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Validation d'audience et appPrincipal : couvre la liaison d'audience et appPrincipal dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Sélection de cible de chemin partagé : couvre la sélection de cible de chemin partagé dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.
- Diagnostics de rejet d'authentification : couvre les diagnostics de rejet d'authentification dans le gestionnaire de requête webhook HTTP, la normalisation des chemins, les exigences JSON/méthode, la gestion du corps pré-auth et post-auth, et le comportement de vérification d'ingestion et d'authentification webhook associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`
- Signaux positifs : les tests unitaires exercent le câblage du pipeline webhook partagé, la dérivation de clé de limite de débit derrière les proxies de confiance, la conversion de charge utile add-on, le rejet de jeton manquant, la sélection de cible quand un candidat échoue et un autre vérifie, les avertissements appPrincipal et le renforcement du transport google-auth. La source utilise des assistants d'ingestion partagés plutôt qu'un gestionnaire HTTP brut personnalisé.
- Signaux négatifs : la couverture est principalement au niveau unitaire et simulée. Il n'existe pas de test dédié en direct/e2e qui reçoit une véritable requête Google Chat de Google, vérifie le comportement JWT/certificat réel et distribue un événement réel via la passerelle sous exposition HTTPS publique.
- Lacunes d'intégration : ajouter une preuve webhook en direct pour les charges utiles Chat standard et add-on Workspace, couvrant à la fois `audienceType: "app-url"` et `project-number`, avec les journaux de rejet d'authentification attendus pour `appPrincipal` manquant/incorrect.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : #65007 est ouvert pour le rejet d'analyse de charge utile add-on rejetant les événements d'espace valides et le comportement de liste d'autorisation de caractères génériques. Les rapports fermés/récents #35095, #53888, #57542, #67786 et #71078 montrent que l'authentification app-url, appPrincipal et les défaillances 401 silencieuses étaient un véritable modèle de support. #77307 signale une régression où l'envoi de message Google Chat a échoué avec `unsupported_grant_type` après que de courts correctifs n'aient pas résolu le problème.
- Rapports Discrawl : `discrawl search "Google Chat appPrincipal" --limit 10` a retourné plusieurs commentaires de problèmes et notes d'examen confirmant que l'exigence appPrincipal/JWT `sub` a dérouté les opérateurs et que la journalisation/les avertissements ont été ajoutés ultérieurement. `discrawl search "Google Chat setup service account audience" --limit 10` a retourné un fil d'aide Discord débogage des 401 persistants et des questions d'émetteur/certificat add-on.
- Bonnes qualités : l'implémentation s'authentifie avant les lectures complètes du corps quand un bearer d'en-tête est présent, utilise un petit budget de corps pré-auth pour les jetons add-on, enregistre les raisons de rejet explicites uniquement quand tous les candidats échouent, utilise des assistants de cible/authentification partagés, prend en charge les chemins webhook partagés et protège les récupérations d'authentification/certificat Google avec une politique SSRF en liste blanche et des limites de taille de réponse.
- Mauvaises qualités : le contrat de produit est toujours nuancé : les jetons d'émetteur Chat standard, les jetons d'émetteur add-on, les audiences `app-url`, les audiences `project-number`, les liaisons de principal numériques et l'exposition de chemin webhook public peuvent tous échouer différemment. Les rapports d'archive montrent que ces défaillances ressemblaient historiquement à des boucles 401 génériques ou `invalid payload` jusqu'aux améliorations de journalisation récentes.
- Exclu de la qualité : la présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-chat.md`.
- Signaux positifs : les preuves d'archive, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la gestion du chemin webhook, la vérification des jetons Chat standard, la vérification des jetons add-on Workspace, la validation d'audience et appPrincipal, la sélection de cible de chemin partagé, les diagnostics de rejet d'authentification.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve d'authentification en direct pour les charges utiles API Chat standard et les charges utiles add-on Workspace.
- Faire en sorte que la sortie d'échec d'authentification pointe vers le champ Google Cloud exact qui doit fournir `appPrincipal`.
- Maintenir la synchronisation entre la documentation webhook et les avertissements de démarrage avec les branches exactes de `verifyGoogleChatRequest`.
- Ajouter un test de fumée de version pour l'exposition de chemin public uniquement afin que les opérateurs n'exposent pas accidentellement les routes du tableau de bord aux côtés de `/googlechat`.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md` : explique l'exposition du webhook HTTPS public, le routage par chemin uniquement via Tailscale/Caddy/Cloudflare, la vérification du jeton porteur Google Chat, `audienceType`, `audience`, le support de pré-authentification des modules complémentaires, le routage de session et le dépannage des webhooks.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md` : documente les champs `channels.googlechat` incluant `audienceType`, `audience`, `webhookPath` et `webhookUrl`.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md` : référence les contrôles de correspondance de noms mutables Google Chat.

## Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-webhook.ts` : normalise les chemins des webhooks, utilise des gardes de requête partagées, limite les lectures de corps de modules complémentaires pré-authentifiés, analyse les charges utiles des modules complémentaires en événements standard, vérifie les cibles, enregistre les raisons de rejet d'authentification et distribue les événements acceptés de manière asynchrone.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/auth.ts` : vérifie les jetons d'ID d'URL d'application, les JWT signés par le numéro de projet, les jetons d'émetteur Chat, les jetons d'émetteur de module complémentaire et les principaux de module complémentaire attendus.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/google-auth.runtime.ts` : restreint les récupérations d'authentification Google aux suffixes d'hôte Google, préserve le comportement du proxy/mTLS, limite les corps de réponse, valide les champs de point de terminaison des identifiants et évite la mutation gaxios au niveau du processus.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-routing.ts` : enregistre et sélectionne les cibles des webhooks par chemin normalisé.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/gateway.ts` : démarre les moniteurs de webhooks par compte et enregistre les métadonnées de chemin/statut d'exécution.

## Tests d'intégration

- Aucun test de webhook Google Chat en direct dédié n'a été trouvé sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/test/scripts/bundled-plugin-build-entries.test.ts` : couvre Google Chat en tant qu'entrée de construction de module complémentaire groupé/externe, ce qui protège l'empaquetage mais ne prouve pas l'authentification du webhook en direct.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor-webhook.test.ts` : couvre le câblage du pipeline partagé, les clés de limite de débit, la conversion de charge utile de module complémentaire, le rejet de jeton manquant, la copie d'avertissement et la sélection de cible de chemin partagé.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/monitor.webhook-routing.test.ts` : couvre le routage et l'enregistrement des cibles de webhook.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/google-auth.runtime.test.ts` : couvre les récupérations d'authentification protégées par SSRF, la traduction proxy/mTLS, les limites de réponse, les transports isolés, la normalisation des en-têtes et la validation du compte de service.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/google-auth.runtime.test.ts` et `/Users/kevinlin/code/openclaw/extensions/googlechat/src/doctor-contract.test.ts` : fournissent une couverture de régression d'authentification/configuration adjacente au chemin du webhook.

## Requêtes Gitcrawl

Requête :

`gitcrawl search issues "Google Chat invalid payload" --repo openclaw/openclaw --limit 15 --json number,title,state,updatedAt,url`

Résultats :

- Retourné ouvert #65007, `Google Chat add-on payload parsing rejects valid space events and wildcard group allowlist still blocks senders`, mis à jour 2026-05-19.

Requête :

`gitcrawl gh issue view 71078 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- Retourné fermé #71078, `Observability gap: verifyGoogleChatRequest reject reasons are swallowed; missing appPrincipal presents as opaque 401`, mis à jour 2026-04-27.

Requête :

`gitcrawl gh issue view 77307 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- Retourné ouvert #77307, un rapport de régression Google Chat où un canal précédemment fonctionnel a échoué avec `unsupported_grant_type` après une mise à niveau entre 2026-04-29 et 2026-05-02.

## Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat appPrincipal" --limit 10`

Résultats :

- Retourné les commentaires de problème et la discussion de PR pour #35095, #67786, #57542 et #71078 expliquant que `appPrincipal` doit être la valeur numérique JWT `sub`, pas l'e-mail du compte de service, et que les défaillances d'authentification silencieuses ont été traitées ultérieurement avec des avertissements et des journaux de rejet.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat setup service account audience" --limit 10`

Résultats :

- Retourné un fil de configuration/débogage où un utilisateur a tracé les 401 persistants au traitement de l'émetteur/certificat du module complémentaire et au comportement audience/appPrincipal.
