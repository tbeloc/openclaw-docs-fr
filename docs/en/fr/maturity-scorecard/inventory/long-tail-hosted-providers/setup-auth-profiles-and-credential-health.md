---
title: "Fournisseurs hébergés long-tail - Note de maturité des opérations de fournisseur"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs hébergés long-tail - Note de maturité des opérations de fournisseur

## Résumé

La configuration, les profils d'authentification et la santé des identifiants sont en Alpha. Les métadonnées du plan de contrôle pour l'authentification et la configuration sont larges et activement testées, mais la disponibilité pour les fournisseurs hébergés long-tail dépend toujours de l'ordre OAuth/profil/env spécifique au fournisseur, de l'état du compte régional, des chaînes d'identifiants et de la disponibilité des modèles.

## Portée de la catégorie

Inclus dans cette catégorie :

- Répertoire des fournisseurs : Couvre le répertoire des fournisseurs dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Catalogue d'installation des fournisseurs : Couvre le catalogue d'installation des fournisseurs dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Métadonnées du catalogue des modèles : Couvre les métadonnées du catalogue des modèles dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Vérifications de parité du catalogue : Couvre les vérifications de parité du catalogue dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Descripteurs de configuration du fournisseur : Couvre les descripteurs de configuration du fournisseur dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Profils d'authentification et alias : Couvre les profils d'authentification et alias dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Sondes de santé des identifiants : Couvre les sondes de santé des identifiants dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Rotation et récupération des clés : Couvre la rotation et la récupération des clés dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Fumée directe du fournisseur : Couvre la fumée directe du fournisseur dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.
- Fumée en direct de la passerelle : Couvre la fumée en direct de la passerelle dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.
- Sondes de statut des modèles : Couvre les sondes de statut des modèles dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.
- Trace de secours et réparation : Couvre la trace de secours et la réparation dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.

## Fonctionnalités

- Répertoire des fournisseurs : Couvre le répertoire des fournisseurs dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Catalogue d'installation des fournisseurs : Couvre le catalogue d'installation des fournisseurs dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Métadonnées du catalogue des modèles : Couvre les métadonnées du catalogue des modèles dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Vérifications de parité du catalogue : Couvre les vérifications de parité du catalogue dans le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des modèles de fournisseurs, les métadonnées du manifeste du fournisseur et le comportement associé du catalogue des fournisseurs et de la découverte.
- Descripteurs de configuration du fournisseur : Couvre les descripteurs de configuration du fournisseur dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Profils d'authentification et alias : Couvre les profils d'authentification et alias dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Sondes de santé des identifiants : Couvre les sondes de santé des identifiants dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Rotation et récupération des clés : Couvre la rotation et la récupération des clés dans les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification et le comportement associé de la configuration et de la santé des identifiants.
- Fumée directe du fournisseur : Couvre la fumée directe du fournisseur dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.
- Fumée en direct de la passerelle : Couvre la fumée en direct de la passerelle dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.
- Sondes de statut des modèles : Couvre les sondes de statut des modèles dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.
- Trace de secours et réparation : Couvre la trace de secours et la réparation dans la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement associé des diagnostics du fournisseur et de la réparation de secours.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (66%)`
- Signaux positifs :
  - `docs/plugins/manifest.md` documente les descripteurs de configuration et indique que `setup.providers[].envVars` est la surface de recherche d'authentification/statut du fournisseur préférée.
  - `docs/concepts/model-providers.md` documente la priorité de la source clé et la rotation des clés API de type limite de débit uniquement.
  - `docs/cli/models.md` documente `models status`, l'aperçu de l'authentification, les sondes en direct et les compartiments d'authentification/statut.
  - Les lectures de source `providerAuthEnvVars`, `setup.providers[].envVars` et les alias d'authentification pour la recherche de variables d'environnement du fournisseur.
  - La couverture unitaire préserve les métadonnées d'authentification du fournisseur et vérifie le comportement de suppression des secrets pour les variables d'environnement du fournisseur.
- Signaux négatifs :
  - Les colonnes d'authentification `models list` ne prouvent intentionnellement pas l'exactitude de la disponibilité d'exécution par modèle.
  - Les fournisseurs hébergés mélangent les clés API, OAuth, les marqueurs locaux, les chaînes d'identifiants AWS, les magasins de profils et les jetons spécifiques au plan.
  - Les sondes en direct sont optionnelles et peuvent consommer des jetons ou atteindre les limites du fournisseur.

## Score de qualité

- Score : `Alpha (62%)`
- Bonnes qualités :
  - La configuration basée sur le descripteur garde les faits d'authentification bon marché disponibles sans charger le runtime du fournisseur.
  - Les diagnostics d'authentification séparent l'état du modèle configuré/par défaut de la santé du profil OAuth.
  - La rotation des clés est intentionnellement limitée aux défaillances de type limite de débit et déduplique les sources.
  - La recherche de variables d'environnement du fournisseur se défend contre les clés de chaîne de prototypes et les fuites de secrets larges.
- Mauvaises qualités :
  - Les fournisseurs exposent toujours différentes sémantiques de disponibilité : les chaînes d'identifiants Bedrock, OAuth SuperGrok/X, l'authentification du plan de jetons MiniMax et les clés API proxy/passerelle ne sont pas interchangeables.
  - `models status` peut afficher des preuves d'authentification utilisables tandis qu'un modèle spécifique ou un plan de compte reste indisponible.
  - L'historique Discord montre des utilisateurs demandant comment les clés du fournisseur, `.env`, les profils d'authentification et les identifiants Bedrock interagissent.
- Exclus de la qualité :
  - Les preuves unitaires, d'intégration et en direct ont été utilisées uniquement pour le score de couverture.

## Score de complétude

- Score : `Alpha (66%)`
- Instructions de surface : évaluées par rapport à `references/completeness/long-tail-hosted-providers.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le répertoire des fournisseurs, le catalogue d'installation des fournisseurs, les métadonnées du catalogue des modèles, les vérifications de parité du catalogue, les descripteurs de configuration du fournisseur, les profils d'authentification et alias, les sondes de santé des identifiants, la rotation et la récupération des clés, la fumée directe du fournisseur, la fumée en direct de la passerelle, les sondes de statut des modèles, la trace de secours et la réparation.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un rapport de parité d'authentification du fournisseur qui vérifie que chaque manifeste de fournisseur hébergé a des variables d'environnement de configuration, des choix d'authentification, de la documentation et un comportement de statut.
- Ajouter un exercice de santé des identifiants à faible coût pour les fournisseurs proxy cloud/passerelle.
- Afficher des diagnostics de chaîne d'identifiants Bedrock et proxy plus clairs dans la sortie de santé d'authentification visible par l'utilisateur.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:490`: les descripteurs de configuration sont destinés aux métadonnées de configuration/intégration bon marché avant le chargement du runtime.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:525`: `setup.providers` et `setup.cliBackends` sont les surfaces de recherche préférées basées sur les descripteurs.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:531`: OpenClaw inclut `setup.providers[].envVars` dans les recherches génériques d'authentification des fournisseurs et de variables d'environnement.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:537`: OpenClaw peut dériver les choix de configuration à partir de `setup.providers[].authMethods`.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:61`: la rotation des clés API des fournisseurs prend en charge les remplacements en direct, les listes, les clés primaires et les clés numérotées.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:75`: la rotation n'est tentée que pour les réponses de limite de débit, tandis que les défaillances non liées à la limite de débit échouent immédiatement.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md:28`: `models status` affiche les valeurs par défaut/secours résolues ainsi qu'un aperçu de l'authentification.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md:37`: `--probe` exécute des sondes d'authentification en direct en tant que requêtes réelles.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md:51`: `models list` est en lecture seule et ne prouve pas la disponibilité exacte de l'exécution par modèle.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md:138`: les buckets d'état de sonde incluent `ok`, `auth`, `rate_limit`, `billing`, `timeout`, `format`, `unknown` et `no_model`.

### Source

- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.ts:178`: la recherche d'env du fournisseur lit le manifeste `providerAuthEnvVars`.
- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.ts:190`: la recherche d'env du fournisseur lit `setup.providers[].envVars`.
- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.ts:205`: la recherche d'env du fournisseur suit les alias d'authentification.
- `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.test.ts:699`: le registre de manifeste préserve les métadonnées d'env d'authentification du fournisseur à partir des manifestes de plugin.
- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.test.ts:10`: le nettoyage de l'authentification couvre plus de variables d'env du fournisseur que la liste des secrets globaux.
- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.test.ts:49`: la recherche d'env du fournisseur ignore les clés de la chaîne de prototypes.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:83`: les tests de modèles en direct directs peuvent sélectionner des fournisseurs avec `OPENCLAW_LIVE_PROVIDERS`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:85`: les tests en direct peuvent utiliser le magasin de profils et les secours d'env ou nécessiter uniquement l'authentification du magasin de profils.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:115`: Gateway live smoke peut sélectionner des fournisseurs avec `OPENCLAW_LIVE_GATEWAY_PROVIDERS`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:493`: les suites en direct de médias peuvent forcer l'authentification du magasin de profils avec `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1`.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.test.ts:699`: les métadonnées d'env d'authentification du fournisseur à partir des manifestes de plugin sont préservées.
- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.test.ts:10`: le nettoyage de l'authentification inclut les clés spécifiques au fournisseur telles que MiniMax.
- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.test.ts:49`: la collecte de variables d'env ignore la pollution de la chaîne de prototypes et retourne les clés réelles du fournisseur.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "provider auth setup env vars"` a retourné des résultats incluant #33329, #47684, #46184, #84804 et #84725.
- #47684 suit la synchronisation/auto-synchronisation de l'authentification pour la rotation des clés API entre les agents.
- #46184 décrit les défaillances OAuth de la CLI Gemini derrière un proxy HTTP, montrant la sensibilité de l'environnement d'authentification en dehors des chemins simples de clé API.
- #84804 signale la latence de configuration de l'authentification/options de démarrage du tour chaud de Codex, un signal de santé adjacent du profil/configuration.

### Requêtes Discrawl

- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "provider auth setup env vars" --limit 5` a retourné un commentaire Discord expliquant le secours `.env`, les variables d'env d'authentification du manifeste OpenRouter/Venice et le secours du profil d'authentification à env.
- La même recherche Discrawl a retourné le contexte de la PR #71226 : les fournisseurs de configuration descriptor-only déclarent des variables d'env, et la recherche d'authentification/env du fournisseur devait inclure `setup.providers[].envVars`.
- La même recherche Discrawl a retourné les conseils de support Bedrock : Bedrock utilise la chaîne de credentials du SDK AWS plutôt qu'une clé API OpenClaw.
- La même recherche Discrawl a retourné un commentaire d'examen d'outil d'image où `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `QWEN_API_KEY` et `MOONSHOT_API_KEY` configurés pourraient affecter la sélection automatique du fournisseur.
