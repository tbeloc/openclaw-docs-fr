---
title: "Outils de recherche web - Note de disponibilité des outils et maturité de récupération"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche web - Note de disponibilité des outils et maturité de récupération

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche web` / `Exposition des outils, politique et câblage des outils d'exécution` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Inclus dans cette catégorie :

- web_search exposure : Définit la configuration d'exposition web_search, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- web_fetch exposure : Définit la configuration d'exposition web_fetch, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- x_search exposure : Définit la configuration d'exposition x_search, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- group:web policy : Définit la configuration de la politique group:web, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- disabled-state diagnostics : Définit la configuration des diagnostics d'état désactivé, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- provider/model gating : Définit la configuration du contrôle d'accès provider/model, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- URL fetch : Couvre l'invocation de l'outil URL fetch, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- HTML extraction : Couvre l'invocation de l'outil d'extraction HTML, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- PDF/text extraction : Couvre l'invocation de l'outil d'extraction PDF/texte, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Safe truncation : Couvre l'invocation de l'outil de troncature sécurisée, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Content citation handoff : Couvre l'invocation de l'outil de transmission des citations de contenu, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.

## Fonctionnalités

- web_search exposure : Définit la configuration d'exposition web_search, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- web_fetch exposure : Définit la configuration d'exposition web_fetch, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- x_search exposure : Définit la configuration d'exposition x_search, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- group:web policy : Définit la configuration de la politique group:web, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- disabled-state diagnostics : Définit la configuration des diagnostics d'état désactivé, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- provider/model gating : Définit la configuration du contrôle d'accès provider/model, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité des outils et la politique.
- URL fetch : Couvre l'invocation de l'outil URL fetch, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- HTML extraction : Couvre l'invocation de l'outil d'extraction HTML, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- PDF/text extraction : Couvre l'invocation de l'outil d'extraction PDF/texte, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Safe truncation : Couvre l'invocation de l'outil de troncature sécurisée, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Content citation handoff : Couvre l'invocation de l'outil de transmission des citations de contenu, l'exécution sur l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (83%)`

La couverture est stable car la documentation, la source de l'outil agent, les vérifications d'exécution, le comportement de la liste d'autorisation, le comportement de démarrage de la passerelle et les preuves d'archive couvrent la façon dont web_search et web_fetch sont exposés aux agents. Le score est limité par les preuves d'archive actives selon lesquelles les sous-agents et les listes d'autorisation spécifiques aux fournisseurs peuvent toujours supprimer les outils de manière inattendue pour les opérateurs.

## Score de qualité

- Score : `Stable (82%)`

La qualité est stable car l'exposition des outils est construite autour d'une politique de profil explicite et de liste d'autorisation, d'un contexte d'exécution lié tardivement et d'un contrôle d'accès provider/model au lieu d'exposer avec impatience les outils indisponibles. Le risque restant est que la disponibilité dépend de plusieurs entrées d'exécution, donc la raison visible par l'utilisateur pour laquelle un outil manque peut toujours être difficile à diagnostiquer.

## Score de complétude

- Score : `Stable (83%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : la documentation archivée, la source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'exposition web_search, l'exposition web_fetch, l'exposition x_search, la politique group:web, les diagnostics d'état désactivé, le contrôle d'accès provider/model, la récupération URL, l'extraction HTML, l'extraction PDF/texte, la troncature sécurisée, la transmission des citations de contenu.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:23` documente le profil de codage et `group:web`.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:35` mappe `group:web` à `web_search`, `x_search` et `web_fetch`.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:178` documente l'utilisation du profil d'outil et de la liste d'autorisation pour web_fetch et `group:web`.
- `/Users/kevinlin/code/openclaw/docs/tools/web.md:19` explique quand utiliser web_search, browser ou web_fetch.
- `/Users/kevinlin/code/openclaw/docs/help/faq.md:732` couvre l'activation des outils et des listes d'autorisation en termes visibles par l'opérateur.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search.ts:9` définit le schéma de l'outil web_search.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search.ts:67` construit la réponse d'état désactivé.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search.ts:83` lie tardivement le contexte d'exécution avant l'exécution de web_search.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ts:616` crée l'outil web_fetch avec les valeurs par défaut d'exécution et le secours du fournisseur.
- `/Users/kevinlin/code/openclaw/src/agents/codex-native-web-search-core.ts:177` corrige le comportement de l'outil natif et supprime le web_search géré si nécessaire.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.ts:263` résout la définition de l'outil web_search géré.
- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.ts:163` résout les définitions du fournisseur d'exécution web_fetch.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-search.md:43` vérifie le comportement d'exécution de web_search.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-fetch.md:43` vérifie le comportement d'exécution de web_fetch.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/openai-web-search-minimal/assertions.mjs:132` vérifie l'injection de recherche web native et le comportement de raisonnement minimal.
- `/Users/kevinlin/code/openclaw/src/gateway/server-startup-web-fetch-bind.test.ts:78` couvre la liaison de démarrage sans découverte précoce du fournisseur.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/tools/web-tools.enabled-defaults.test.ts:117` couvre le comportement d'activation par défaut des outils web.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search.late-bind.test.ts:65` couvre le contexte web_search lié tardivement.
- `/Users/kevinlin/code/openclaw/src/agents/tool-policy.test.ts:121` couvre les alias de groupe et le comportement de la politique.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/plugin-tool-allowlist-warnings.test.ts:316` couvre les avertissements pour les listes d'autorisation explicites et les outils de plugin.
- `/Users/kevinlin/code/openclaw/src/web-search/runtime.test.ts:753` couvre le chargement du fournisseur d'exécution délimité.
- `/Users/kevinlin/code/openclaw/src/web-fetch/runtime.test.ts:275` couvre les limites du bac à sable/exécution web_fetch.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a signalé la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29 810` threads, `11 181` threads ouverts et `18 594` clusters.

- `gitcrawl --json search issues -R openclaw/openclaw "no provider available web_search"` a retourné #87347 aucun fournisseur disponible, #85030 injection d'outil sous-agent et #80843 chaîne de secours.
- `gitcrawl --json search issues -R openclaw/openclaw "web_search"` a retourné #77826 l'exécution supprime les outils web du plugin, #85030 injection d'outil sous-agent, #87347 aucun fournisseur disponible et #87505 délai d'expiration.
- `gitcrawl --json search prs -R openclaw/openclaw "web_fetch"` a retourné #77859 préservation des métadonnées d'exécution, #85993 expansion de la capacité du navigateur et #86965 surfaçage de la progression.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a signalé l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1 487 061` messages, `25 819` canaux et zéro arriéré d'intégration.

- `discrawl search --mode hybrid --limit 12 "web_fetch web_search config provider api key"` a trouvé un thread de problème GitHub où les sous-agents générés via des sessions ne pouvaient pas accéder au navigateur, web_search ou web_fetch malgré la configuration de la liste d'autorisation.
- `discrawl search --mode hybrid --limit 12 "web_search no provider available Brave loaded web_fetch"` a trouvé des conseils d'opérateur expliquant les avertissements de liste d'autorisation lorsque web_search est indisponible et que Brave n'est pas configuré.
