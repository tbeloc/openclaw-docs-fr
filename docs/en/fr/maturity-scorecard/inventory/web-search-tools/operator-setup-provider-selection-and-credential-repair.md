---
title: "Outils de recherche web - Note de maturité de configuration et diagnostics"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche web - Note de maturité de configuration et diagnostics

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche web` / `Configuration de l'opérateur, sélection du fournisseur et réparation des identifiants` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Inclus dans cette catégorie :

- Identifiants du fournisseur : Définit la configuration des identifiants du fournisseur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Sélection du fournisseur par défaut : Définit la configuration de la sélection du fournisseur par défaut, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Réparation des identifiants : Définit la configuration de la réparation des identifiants, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Vérifications d'état : Définit la configuration des vérifications d'état, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Erreurs de quota : Couvre l'état des erreurs de quota, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Contrôles de cache : Couvre l'état des contrôles de cache, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Diagnostics du fournisseur : Couvre l'état des diagnostics du fournisseur, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Réessai et basculement : Couvre l'état du réessai et du basculement, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Réparation par l'opérateur : Couvre l'état de la réparation par l'opérateur, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.

## Fonctionnalités

- Identifiants du fournisseur : Définit la configuration des identifiants du fournisseur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Sélection du fournisseur par défaut : Définit la configuration de la sélection du fournisseur par défaut, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Réparation des identifiants : Définit la configuration de la réparation des identifiants, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Vérifications d'état : Définit la configuration des vérifications d'état, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et la réparation des identifiants.
- Erreurs de quota : Couvre l'état des erreurs de quota, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Contrôles de cache : Couvre l'état des contrôles de cache, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Diagnostics du fournisseur : Couvre l'état des diagnostics du fournisseur, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Réessai et basculement : Couvre l'état du réessai et du basculement, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.
- Réparation par l'opérateur : Couvre l'état de la réparation par l'opérateur, les diagnostics, la gestion des défaillances et la réparation par l'opérateur pour la fiabilité du fournisseur et les diagnostics.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`

La couverture est stable car la documentation et le code source couvrent la configuration au premier lancement, le choix du fournisseur, les alternatives env/clé API, les fournisseurs sans clé, les SecretRefs, la configuration canonique détenue par le plugin, la validation des fournisseurs obsolètes, la migration du docteur et la sélection web_fetch séparée. Le score est limité par l'absence de preuve end-to-end toujours active pour configurer plus réparation du docteur plus redémarrage de la passerelle pour chaque fournisseur, et les résultats d'archive montrent toujours une confusion de l'opérateur autour des clés, des listes blanches et des états sans fournisseur.

## Score de qualité

- Score : `Beta (76%)`

La qualité est Beta car la direction de la configuration canonique est solide, mais le chemin de l'opérateur s'étend sur de nombreuses classes d'identifiants, la migration de la configuration héritée, le chargement de l'env du service, l'activation du plugin, les listes blanches, les fournisseurs expérimentaux sans clé et l'état de la passerelle sensible au redémarrage. Les preuves d'archive actuelles montrent que ces cas limites fuient toujours dans les défaillances de configuration visibles par l'utilisateur.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : les preuves archivées de la documentation, du code source, des tests, de Gitcrawl et de Discrawl couvrent la portée de la taxonomie pour les identifiants du fournisseur, la sélection du fournisseur par défaut, la réparation des identifiants, les vérifications d'état, les erreurs de quota, les contrôles de cache, les diagnostics du fournisseur, le réessai et le basculement, la réparation par l'opérateur.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/tools/web.md:27` documente `openclaw configure --section web`, le choix du fournisseur et le stockage des identifiants.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:100` liste les fournisseurs pris en charge et les exigences en matière d'identifiants.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:170` documente l'ordre de détection automatique, les chemins de clé env/plugin, le basculement sans clé et les SecretRefs.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:227` documente la configuration canonique détenue par le plugin, la validation des fournisseurs obsolètes, `doctor --fix` et la sélection web_fetch séparée.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:19` documente web_fetch comme activé par défaut.
- `/Users/kevinlin/code/openclaw/docs/help/faq.md:732` donne des conseils à l'opérateur pour activer web_search/web_fetch, les variables env, la configuration détenue par le plugin, les listes blanches et le chargement de l'env du démon.

### Code source

- `/Users/kevinlin/code/openclaw/src/flows/search-setup.ts:403` implémente la sélection du fournisseur, les valeurs par défaut, les invites d'identifiants, la gestion des fournisseurs sans clé, la configuration Grok soutenue par OAuth, le mode SecretRef et la finalisation de la configuration.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.ts:153` résout les fournisseurs web_search explicites et détectés automatiquement à partir des identifiants, des profils d'authentification et du basculement sans clé.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.ts:424` exécute le fournisseur sélectionné et le comportement de basculement.
- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.ts:107` résout la sélection du fournisseur web_fetch.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/legacy-web-search-migrate.ts:12` mappe la configuration web_search héritée aux propriétaires de plugins.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/legacy-web-fetch-migrate.ts:38` migre la configuration de récupération Firecrawl.
- `/Users/kevinlin/code/openclaw/src/config/validation.ts:1337` valide les fournisseurs web_search configurés et émet des conseils d'installation ou du docteur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-search.md:11` définit la couverture de parité d'exécution pour web_search.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-fetch.md:11` définit la couverture de parité d'exécution pour web_fetch.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/openai-web-search-minimal/scenario.sh:57` exécute le chemin de passerelle de recherche web OpenAI natif.
- `/Users/kevinlin/code/openclaw/src/gateway/server-startup-web-fetch-bind.test.ts:78` vérifie le démarrage de la passerelle avec la configuration web_fetch sans identifiants.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/legacy-web-search-migrate.test.ts:9` couvre la migration à partir de la configuration héritée `tools.web.search.*`.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/legacy-web-fetch-migrate.test.ts:9` couvre la migration de récupération Firecrawl.
- `/Users/kevinlin/code/openclaw/src/config/config.web-search-provider.test.ts:305` couvre l'acceptation de la configuration du fournisseur.
- `/Users/kevinlin/code/openclaw/src/config/config.web-search-provider.test.ts:597` couvre la détection automatique env.
- `/Users/kevinlin/code/openclaw/src/flows/search-setup.test.ts:212` couvre la configuration détenue par le fournisseur et soutenue par OAuth.
- `/Users/kevinlin/code/openclaw/src/flows/search-setup.test.ts:406` couvre la configuration du fournisseur du catalogue d'installation.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a signalé la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29 810` threads, `11 181` threads ouverts et `18 594` clusters.

- `gitcrawl --json search issues -R openclaw/openclaw "web_search"` a retourné des problèmes de configuration et d'exécution ouverts incluant #87347 aucun fournisseur disponible malgré Brave chargé, #77826 outils web du plugin supprimés à l'exécution, #80843 chaîne de basculement et #87505 régression de délai d'attente.
- `gitcrawl --json search issues -R openclaw/openclaw "web_fetch"` a retourné des problèmes de configuration et de sécurité de récupération ouverts incluant #39604 opt-in réseau privé, #82685 limites de corps d'extraction, #41993 défaillances d'utilisation spéciale IPv6 et #87505 régression de délai d'attente.
- `gitcrawl --json search prs -R openclaw/openclaw "web_search"` a retourné le routage du fournisseur actif, l'instantané de démarrage, SecretRef, le basculement et le travail de proxy incluant #77736, #86828, #76146, #63571 et #61413.
- `gitcrawl --json search prs -R openclaw/openclaw "web_fetch"` a retourné la récupération Firecrawl/Tavily active, réseau privé, progression, durcissement d'injection et travail de métadonnées d'exécution incluant #75218, #39630, #86965, #87758 et #77859.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a signalé l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1 487 061` messages, `25 819` canaux et zéro arriéré d'intégration.

- `discrawl search --mode hybrid --limit 12 "web_search no provider available Brave loaded web_fetch"` a trouvé des conseils de support distinguant web_fetch de web_search et expliquant que la recherche a besoin d'une clé de fournisseur configurée.
- `discrawl search --mode hybrid --limit 12 "web_fetch web_search config provider api key"` a trouvé des threads de configuration pour activer les deux outils, le placement de la clé Brave, les listes blanches `group:web` et les commentaires d'examen de la configuration du fournisseur.
- `discrawl search --mode hybrid --limit 12 "openclaw configure --section web Brave API key web_search web_fetch"` a trouvé des conseils répétés à l'opérateur pour utiliser `openclaw configure --section web`, redémarrer la passerelle et mettre les clés dans l'env de la passerelle.
- `discrawl search --mode hybrid --limit 12 "web_search migration doctor --fix tools.web.search"` a trouvé des discussions de migration où l'état hérité `tools.web.search` nécessitait une réparation du docteur.
