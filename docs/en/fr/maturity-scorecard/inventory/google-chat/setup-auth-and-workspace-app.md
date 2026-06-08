---
title: "Google Chat - Note de Maturité de Configuration de Canal et Opérations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Note de Maturité de Configuration de Canal et Opérations

## Résumé

La configuration de Google Chat est documentée et intégrée via la surface de configuration du plugin, mais elle reste une expérience d'opérateur Alpha car une installation réussie dépend de l'état du projet Google Cloud, de l'activation de l'API Chat, du JSON du compte de service, du routage HTTPS public, de la visibilité de l'application Google Chat, de la correspondance de l'audience du webhook, et parfois du principal numérique du module complémentaire. La documentation explique le chemin heureux, mais les preuves archivées montrent que les utilisateurs passent toujours des heures sur les problèmes d'appPrincipal, 401 et de configuration d'espace.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Configuration de Canal et Opérations`
- Fusionnée à partir de : `Configuration et Opérations`, `Authentification Webhook`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du projet Google Cloud : Couvre la configuration du projet Google Cloud dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants JSON/fichier/env du compte de service, `audienceType`, et le comportement d'authentification de configuration et d'application d'espace de travail associé.
- Configuration de l'application Chat : Couvre la configuration de l'application Chat dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants JSON/fichier/env du compte de service, `audienceType`, et le comportement d'authentification de configuration et d'application d'espace de travail associé.
- Configuration du compte de service : Couvre la configuration du compte de service dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants JSON/fichier/env du compte de service, `audienceType`, et le comportement d'authentification de configuration et d'application d'espace de travail associé.
- Audience du webhook et chemin : Couvre l'audience du webhook et le chemin dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants JSON/fichier/env du compte de service, `audienceType`, et le comportement d'authentification de configuration et d'application d'espace de travail associé.
- Visibilité de l'espace de travail et statut de l'application : Couvre la visibilité de l'espace de travail et le statut de l'application dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants JSON/fichier/env du compte de service, `audienceType`, et le comportement d'authentification de configuration et d'application d'espace de travail associé.
- Configuration guidée du canal : Couvre la configuration guidée du canal dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants JSON/fichier/env du compte de service, `audienceType`, et le comportement d'authentification de configuration et d'application d'espace de travail associé.
- Résolution de compte : Couvre la résolution de compte dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé.
- SecretRefs du compte de service : Couvre les SecretRefs du compte de service dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé.
- Identifiants de fichier env et en ligne : Couvre les identifiants de fichier env et en ligne dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé.
- Statut du canal et sondes : Couvre le statut du canal et les sondes dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé.
- Diagnostics du répertoire et mutable-id : Couvre les diagnostics du répertoire et mutable-id dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé.
- Installation NPM et ClawHub : Couvre l'installation NPM et ClawHub dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé.
- Routage de la documentation et du catalogue des plugins : Couvre le routage de la documentation et du catalogue des plugins dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé.
- Alias et étiquettes de canal : Couvre les alias et étiquettes de canal dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé.
- Interface utilisateur de statut d'opérateur : Couvre l'interface utilisateur de statut d'opérateur dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé.
- Métadonnées d'installation/mise à jour : Couvre les métadonnées d'installation/mise à jour dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé.
- Gestion du chemin webhook : Couvre la gestion du chemin webhook dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé.
- Vérification du jeton Chat standard : Couvre la vérification du jeton Chat standard dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé.
- Vérification du jeton du module complémentaire Workspace : Couvre la vérification du jeton du module complémentaire Workspace dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé.
- Validation de l'audience et du principal d'application : Couvre la liaison de l'audience et du principal d'application dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé.
- Sélection de cible à chemin partagé : Couvre la sélection de cible à chemin partagé dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé.
- Diagnostics de rejet d'authentification : Couvre les diagnostics de rejet d'authentification dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé.
- Résolution de compte : Couvre la résolution de compte dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé
- SecretRefs du compte de service : Couvre les SecretRefs du compte de service dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé
- Identifiants de fichier env et en ligne : Couvre les identifiants de fichier env et en ligne dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé
- Statut du canal et sondes : Couvre le statut du canal et les sondes dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé
- Diagnostics du répertoire et mutable-id : Couvre les diagnostics du répertoire et mutable-id dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement de statut et de diagnostics des secrets multi-comptes associé
- Installation NPM et ClawHub : Couvre l'installation NPM et ClawHub dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé
- Routage de la documentation et du catalogue des plugins : Couvre le routage de la documentation et du catalogue des plugins dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé
- Alias et étiquettes de canal : Couvre les alias et étiquettes de canal dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé
- Interface utilisateur de statut d'opérateur : Couvre l'interface utilisateur de statut d'opérateur dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé
- Métadonnées d'installation/mise à jour : Couvre les métadonnées d'installation/mise à jour dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références de plugin, le catalogue officiel de plugins externes, et le comportement d'interface utilisateur d'opérateur de distribution de plugin et de documentation associé
- Gestion du chemin webhook : Couvre la gestion du chemin webhook dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé
- Vérification du jeton Chat standard : Couvre la vérification du jeton Chat standard dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé
- Vérification du jeton du module complémentaire Workspace : Couvre la vérification du jeton du module complémentaire Workspace dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé
- Liaison de l'audience et du principal d'application : Couvre la liaison de l'audience et du principal d'application dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé
- Sélection de cible à chemin partagé : Couvre la sélection de cible à chemin partagé dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé
- Diagnostics de rejet d'authentification : Couvre les diagnostics de rejet d'authentification dans le gestionnaire de requête webhook HTTP, la normalisation du chemin, les exigences JSON/méthode, la gestion du corps pré-authentification et post-authentification, et le comportement d'ingestion webhook et de vérification d'authentification associé

## Fonctionnalités

- Configuration du projet Google Cloud : Couvre la configuration du projet Google Cloud dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement de l'authentification de configuration et de l'application d'espace de travail associés.
- Configuration de l'application Chat : Couvre la configuration de l'application Chat dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement de l'authentification de configuration et de l'application d'espace de travail associés.
- Configuration du compte de service : Couvre la configuration du compte de service dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement de l'authentification de configuration et de l'application d'espace de travail associés.
- Audience et chemin du webhook : Couvre l'audience et le chemin du webhook dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement de l'authentification de configuration et de l'application d'espace de travail associés.
- Visibilité de l'espace de travail et statut de l'application : Couvre la visibilité de l'espace de travail et le statut de l'application dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement de l'authentification de configuration et de l'application d'espace de travail associés.
- Configuration guidée des canaux : Couvre la configuration guidée des canaux dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement de l'authentification de configuration et de l'application d'espace de travail associés.
- Résolution des comptes : Couvre la résolution des comptes dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs du compte de service, et le comportement associé du statut des secrets multi-comptes et des diagnostics.
- SecretRefs du compte de service : Couvre les SecretRefs du compte de service dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs du compte de service, et le comportement associé du statut des secrets multi-comptes et des diagnostics.
- Identifiants du fichier env et en ligne : Couvre les identifiants du fichier env et en ligne dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs du compte de service, et le comportement associé du statut des secrets multi-comptes et des diagnostics.
- Statut du canal et sondes : Couvre le statut du canal et les sondes dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs du compte de service, et le comportement associé du statut des secrets multi-comptes et des diagnostics.
- Diagnostics du répertoire et de l'identifiant mutable : Couvre les diagnostics du répertoire et de l'identifiant mutable dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs du compte de service, et le comportement associé du statut des secrets multi-comptes et des diagnostics.
- Installation NPM et ClawHub : Couvre l'installation NPM et ClawHub dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références du plugin, le catalogue officiel des plugins externes, et le comportement associé de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Routage de la documentation et du catalogue des plugins : Couvre le routage de la documentation et du catalogue des plugins dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références du plugin, le catalogue officiel des plugins externes, et le comportement associé de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Alias et étiquettes des canaux : Couvre les alias et étiquettes des canaux dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références du plugin, le catalogue officiel des plugins externes, et le comportement associé de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Interface utilisateur du statut de l'opérateur : Couvre l'interface utilisateur du statut de l'opérateur dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références du plugin, le catalogue officiel des plugins externes, et le comportement associé de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Métadonnées d'installation/mise à jour : Couvre les métadonnées d'installation/mise à jour dans les métadonnées du plugin npm/ClawHub, la navigation dans la documentation, les références du plugin, le catalogue officiel des plugins externes, et le comportement associé de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs : La surface de configuration n'est pas seulement de la prose. Les métadonnées du plugin exposent `@openclaw/googlechat`, les alias des canaux, le chemin de la documentation, les options d'ajout CLI pour les champs de chemin/audience du webhook, les noms des variables d'environnement, les points d'entrée de configuration, et un assistant de configuration interactif. Les tests unitaires couvrent la validation des entrées de configuration, la correction des comptes, la sélection des identifiants d'environnement, les écritures de politique DM au niveau du compte, le démarrage du chemin du webhook, le comportement de fusion des comptes, et la validation du fichier du compte de service.
- Signaux négatifs : Je n'ai trouvé aucune voie QA en direct/e2e dédiée à Google Chat comparable à Discord ou Slack. La couverture est donc principalement une preuve de contrat de configuration/configuration locale, et non une exécution e2e fraîche via la console Google Cloud, la visibilité de l'application d'espace de travail, l'exposition publique du webhook, le redémarrage de la passerelle, et la livraison réelle des DM/espaces Google Chat.
- Lacunes d'intégration : Ajouter un scénario de configuration en direct contrôlé qui commence par une configuration minimale, installe le plugin, vérifie le chemin du fichier/env du compte de service, valide `audienceType`/`audience`/`appPrincipal`, démarre la passerelle, reçoit un webhook Google Chat réel, et confirme que `openclaw channels status --probe` rapporte un état de configuration exploitable.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : L'ensemble des problèmes Google Chat inclut des défaillances adjacentes à la configuration ouvertes telles que #58514 pour les messages d'espace ignorés silencieusement tandis que les DM fonctionnent et #65007 pour les incompatibilités de charge utile d'extension et de liste d'autorisation de groupe générique. Les problèmes de configuration/authentification fermés mais récents #53888, #57542, #67786, #35095, et #71078 montrent que les exigences `appPrincipal`/JWT `sub` et les boucles 401 silencieuses étaient des pièges réels pour les opérateurs.
- Rapports Discrawl : `discrawl search "Google Chat setup service account audience" --limit 10` a retourné des conseils de configuration selon lesquels le JSON du compte de service plus `audienceType: "app-url"` et l'URL publique du webhook sont l'histoire centrale de l'espace de travail. Il a également retourné des discussions répétées d'avril 2026 sur le fait que `appPrincipal` a besoin du JWT `sub`, et non de l'e-mail du compte de service, et un avis d'examen avertissant que l'exigence de `appPrincipal` sans mise à jour de la configuration guidée casserait la configuration des canaux.
- Bonnes qualités : La documentation du canal donne un chemin de configuration pour les débutants, des recettes d'URL publiques pour Tailscale Funnel, Caddy et Cloudflare Tunnel, des formats cibles, l'appairage, les points forts de la configuration, et le dépannage. La source maintient la résolution des identifiants du compte de service localisée, supporte les identifiants fichier/en ligne/env, supporte les valeurs par défaut partagées par compte, et valide les champs de point de terminaison du compte de service Google avant de transmettre les identifiants à google-auth.
- Mauvaises qualités : Le contrat de configuration traverse trop de surfaces d'administration externes pour l'UX actuelle. La visibilité de l'application, la disponibilité de l'URL du webhook, les charges utiles Chat d'extension par rapport aux charges utiles Chat standard, le `appPrincipal` numérique, et le statut de la console Google Cloud sont faciles à mal configurer. Certains de ces risques sont maintenant avertis, mais la documentation et l'assistant de configuration ne rendent toujours pas chaque valeur requise du côté Google auto-découverte.
- Exclu de la qualité : La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-chat.md`.
- Signaux positifs : les preuves archivées de la documentation, de la source, des tests, de Gitcrawl et de Discrawl couvrent l'étendue de la taxonomie pour la configuration du projet Google Cloud, la configuration de l'application Chat, la configuration du compte de service, l'audience et le chemin du webhook, la visibilité de l'espace de travail et le statut de l'application, la configuration guidée des canaux, la résolution des comptes, les SecretRefs du compte de service, les identifiants du fichier env et en ligne, le statut du canal et les sondes, les diagnostics du répertoire et de l'identifiant mutable, l'installation NPM et ClawHub, le routage de la documentation et du catalogue des plugins, les alias et étiquettes des canaux, l'interface utilisateur du statut de l'opérateur, les métadonnées d'installation/mise à jour.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Étendre la configuration guidée pour capturer ou expliquer `appPrincipal` lorsque `audienceType` est `app-url` et que l'application utilise des jetons d'extension.
- Ajouter une liste de contrôle de l'opérateur qui distingue les jetons d'émetteur Chat standard des jetons d'extension d'espace de travail et explique quels champs sont requis pour chacun.
- Ajouter une preuve de configuration en direct qui exerce le flux documenté de Google Cloud et de l'application Google Chat par rapport à une véritable application d'espace de travail privée.
- Rendre les diagnostics d'activation du plugin, de source d'identifiants du compte de service, d'URL du webhook et d'incompatibilité d'audience visibles à partir du même chemin de configuration/statut.

# Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md` : documente l'installation, la configuration initiale de Google Cloud, le JSON du compte de service, la configuration de l'application Google Chat, la visibilité de l'application, l'exposition publique du webhook HTTPS, `audienceType`, `audience`, `webhookPath`, `serviceAccountFile`, `serviceAccountRef`, les formats cibles, l'appairage, les points clés de la configuration, et le dépannage 405/plugin-disabled.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/googlechat.md` : identifie le plugin comme `@openclaw/googlechat`, distribué via npm et ClawHub, avec la surface de canal `googlechat`.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md` : inclut le bloc de configuration du canal Google Chat et l'avertissement de correspondance des noms mutables.
- `/Users/kevinlin/code/openclaw/docs/start/wizard-cli-reference.md` : répertorie Google Chat comme un canal supporté par l'assistant utilisant le JSON du compte de service plus l'audience du webhook.

### Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/package.json` : déclare les métadonnées du paquet, les options d'ajout CLI pour `--webhook-path`, `--webhook-url`, `--audience-type`, et `--audience`, les métadonnées d'installation npm/ClawHub, et la compatibilité d'hôte.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/openclaw.plugin.json` : déclare l'ID de canal `googlechat`, le comportement au démarrage, et les variables d'environnement `GOOGLE_CHAT_SERVICE_ACCOUNT` et `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE`.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/setup-core.ts` : construit les correctifs de configuration de compte à partir des entrées de configuration token/token-file/audience/webhook et valide que la configuration non-env inclut le JSON du compte de service ou le fichier.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/setup-surface.ts` : implémente l'assistant de configuration interactif, la détection des identifiants d'env, les invites de fichier/inline du compte de service, l'invite d'audience, et la configuration de la politique DM.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/accounts.ts` : résout la configuration de compte fusionnée, le repli d'env du compte par défaut, les sources d'identifiants inline/fichier, et les valeurs par défaut partagées par compte.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/google-auth.runtime.ts` : valide la forme des identifiants du compte de service et les points de terminaison Google Auth de confiance, limite la taille du fichier d'identifiants, supporte les montages de secrets avec lien symbolique, et utilise un transport google-auth protégé contre SSRF.

### Tests d'intégration

- Aucune voie de configuration Google Chat live/e2e dédiée n'a été trouvée sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/test/scripts/bundled-plugin-build-entries.test.ts` : inclut Google Chat dans les vérifications d'entrée de construction de plugin groupé/externe.
- `/Users/kevinlin/code/openclaw/src/plugins/official-external-plugin-catalog.test.ts` : affirme que le catalogue officiel de plugins externes résout `googlechat` en `@openclaw/googlechat`.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/setup.test.ts` : couvre la validation de l'adaptateur de configuration, le correctif de configuration, les invites de l'assistant, le statut, la résolution du chemin de la politique DM, le démarrage du moniteur, le repli des identifiants d'env, et l'héritage de configuration multi-compte.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/google-auth.runtime.test.ts` : couvre les récupérations d'auth protégées, le comportement du proxy/mTLS, les limites de réponse, les transports isolés, la normalisation des en-têtes, la validation du point de terminaison du compte de service, les fichiers avec lien symbolique, et les erreurs de lecture de fichier masquées.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/config-schema.test.ts` : couvre les valeurs par défaut et la validation du schéma de configuration de Google Chat.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "Google Chat" --repo openclaw/openclaw --limit 20 --json number,title,state,updatedAt,url`

Résultats :

- A retourné les problèmes Google Chat ouverts #65007, #80995, #82014, #44347, #49350, #77307, #58514, #42510, #9764, #69422, et #39843, montrant que le canal a un risque actif de configuration/runtime.

Requête :

`gitcrawl gh issue view 53888 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné le problème fermé #53888, `Google Chat: silent webhook auth failures + undocumented appPrincipal requirement`, mis à jour le 2026-04-28. Il a été traité comme une confusion de configuration-auth récente maintenant partiellement résolue, pas un bloqueur ouvert.

Requête :

`gitcrawl gh issue view 57542 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Résultats :

- A retourné le problème fermé #57542, `Google Chat app-url auth requires appPrincipal = JWT sub, but this is undocumented and auth failures are silent`, mis à jour le 2026-04-28.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat setup service account audience" --limit 10`

Résultats :

- A retourné les conseils de configuration de l'espace de travail décrivant le JSON du compte de service, `audienceType: "app-url"`, et l'URL publique du webhook `/googlechat` comme le chemin principal de l'application Google Chat.
- A retourné les commentaires de problème d'avril 2026 et la discussion d'examen expliquant que `appPrincipal` doit être la valeur numérique JWT `sub`, pas l'e-mail du compte de service, et que les modifications du flux de configuration sont nécessaires avant de le rendre obligatoire.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "Google Chat appPrincipal" --limit 10`

Résultats :

- A retourné la discussion #35095/#67786/#57542/#71078 selon laquelle la journalisation du rejet d'auth et les avertissements au démarrage aident maintenant, mais que le contrat appPrincipal était un mode de défaillance d'opérateur récurrent.
