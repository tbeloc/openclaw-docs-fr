---
title: "Chemin du fournisseur OpenRouter - Note de maturité du catalogue de modèles et de la découverte dynamique"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenRouter - Note de maturité du catalogue de modèles et de la découverte dynamique

## Résumé

Le support du catalogue de modèles OpenRouter est solide : OpenClaw fournit des valeurs par défaut statiques, une capacité de chargement dynamique `/models`, une analyse de références OpenRouter imbriquées, une analyse de modèles gratuits en métadonnées uniquement et sondée, des filtres de modèles en direct, et un comportement de liste de modèles pour les identifiants OpenRouter natifs. La couverture est Stable car le catalogue principal et le comportement des modèles dynamiques sont couverts par les tests source et les tests de catalogue contrôlés en direct.

La qualité est Beta car le catalogue gratuit d'OpenRouter et la disponibilité des modèles en amont sont volatiles, et les discussions d'assistance archivées avertissent à plusieurs reprises que les modèles gratuits/capables d'outils utilisables peuvent changer rapidement.

## Portée de la catégorie

Cette catégorie couvre les lignes de catalogue statique, la découverte dynamique des capacités des modèles, la normalisation des identifiants de modèles, les références `openrouter/<provider>/<model>`, `openrouter/auto`, l'analyse des modèles gratuits OpenRouter, les filtres de modèles en direct, le comportement du sélecteur/liste de modèles, et le comportement du cache pour OpenRouter `/models`.

## Fonctionnalités

- Lignes de catalogue statique : Couvre les lignes de catalogue statique dans les lignes de catalogue statique, la découverte dynamique des capacités des modèles, la normalisation des identifiants de modèles, les références `openrouter/<provider>/<model>`, et le comportement associé du catalogue de modèles et de la découverte dynamique.
- Découverte dynamique /models : Couvre la découverte dynamique /models dans les lignes de catalogue statique, la découverte dynamique des capacités des modèles, la normalisation des identifiants de modèles, les références `openrouter/<provider>/<model>`, et le comportement associé du catalogue de modèles et de la découverte dynamique.
- openrouter/auto et références imbriquées : Couvre openrouter/auto et les références imbriquées dans les lignes de catalogue statique, la découverte dynamique des capacités des modèles, la normalisation des identifiants de modèles, les références `openrouter/<provider>/<model>`, et le comportement associé du catalogue de modèles et de la découverte dynamique.
- Analyse/sondage de modèles gratuits : Couvre l'analyse/sondage de modèles gratuits dans les lignes de catalogue statique, la découverte dynamique des capacités des modèles, la normalisation des identifiants de modèles, les références `openrouter/<provider>/<model>`, et le comportement associé du catalogue de modèles et de la découverte dynamique.
- Cache du sélecteur/liste de modèles : Couvre le cache du sélecteur/liste de modèles dans les lignes de catalogue statique, la découverte dynamique des capacités des modèles, la normalisation des identifiants de modèles, les références `openrouter/<provider>/<model>`, et le comportement associé du catalogue de modèles et de la découverte dynamique.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La source inclut les valeurs par défaut du catalogue statique, la résolution dynamique des capacités à partir de `/models` d'OpenRouter, les couches de cache disque et mémoire, l'analyse des références imbriquées, la documentation du scanner, et les tests de catalogue contrôlés en direct.
- Signaux négatifs : Le comportement du catalogue en direct et du sondage dépend de la disponibilité externe d'OpenRouter et de l'état de la clé ; les tests toujours actifs valident principalement l'analyse et le comportement des capacités simulées.
- Lacunes d'intégration : Ajouter une preuve de version planifiée qui exécute `openclaw models scan --no-probe`, un sondage avec une clé, et une vérification du sélecteur/liste de modèles par rapport à au moins un identifiant de modèle OpenRouter nouvellement ajouté.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : La requête de problème OpenRouter large a retourné #10687 pour la découverte de modèles entièrement dynamique, #80347 pour les entrées de modèles obsolètes/supprimées après configuration, #7006 pour exposer le modèle réel utilisé par `openrouter/auto`, et #68066 pour la précision des coûts sur les modèles acheminés.
- Rapports Discrawl : La recherche Discord a trouvé des conseils communautaires pour exécuter `openclaw models scan`, des avertissements selon lesquels les modèles gratuits disparaissent ou cessent d'être capables d'outils, et des conseils pour utiliser `--no-probe` lorsque l'analyse capable d'outils échoue.
- Bonnes qualités : La détection dynamique des capacités réduit l'usure du catalogue codé en dur ; la documentation indique explicitement aux utilisateurs que le sondage nécessite une clé et que la sortie en métadonnées uniquement est informative.
- Mauvaises qualités : `openrouter/auto` et l'acheminement des modèles gratuits peuvent masquer quel backend a réellement traité la demande, et les utilisateurs doivent réexécuter les analyses à mesure que le catalogue d'OpenRouter change.
- Exclu de la qualité : La profondeur des tests de catalogue et les tests d'analyse contrôlés en direct sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openrouter-provider-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les lignes de catalogue statique, la découverte dynamique /models, openrouter/auto et les références imbriquées, l'analyse/sondage de modèles gratuits, le cache du sélecteur/liste de modèles.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La disponibilité des modèles gratuits OpenRouter est suffisamment volatile pour que la documentation ait besoin d'un étalonnage récurrent.
- Les analyses en métadonnées uniquement peuvent identifier les candidats mais ne peuvent pas prouver qu'un modèle configuré fonctionnera pour les sessions d'agent activées par les outils.
- `openrouter/auto` a toujours des lacunes en matière de transparence et de coûts des modèles acheminés dans les problèmes archivés.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente `openrouter/auto`, les références concrètes `openrouter/<provider>/<model>`, et les exemples de secours Kimi.
- `/Users/kevinlin/code/openclaw/docs/concepts/models.md` documente l'analyse des modèles gratuits OpenRouter, le mode métadonnées uniquement, les exigences de sondage, le classement, et la sélection de secours.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md` documente les références OpenRouter imbriquées et `models scan`.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md` répertorie OpenRouter dans le tableau des fournisseurs groupés et résume les particularités spécifiques aux routes.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openrouter/provider-catalog.ts` définit le catalogue OpenRouter statique et la normalisation de l'URL de base.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts` implémente la résolution dynamique des modèles et appelle `loadOpenRouterModelCapabilities`.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/openrouter-model-capabilities.ts` implémente le cache `/models` d'OpenRouter, l'analyse, la récupération, et la recherche des capacités des modèles.
- `/Users/kevinlin/code/openclaw/src/commands/models/scan.ts` implémente l'analyse et le sondage des modèles gratuits OpenRouter.
- `/Users/kevinlin/code/openclaw/src/agents/live-model-filter.ts` organise les candidats de modèles en direct OpenRouter.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/openrouter/openrouter.live.test.ts` contrôle les vérifications du catalogue de modèles OpenRouter et la complétion dynamique des modèles.
- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` vérifie les identifiants natifs OpenRouter canoniques dans la sortie de la liste de modèles.
- `/Users/kevinlin/code/openclaw/src/commands/models.set.e2e.test.ts` couvre le comportement de l'ensemble de modèles via l'interface de ligne de commande.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.test.ts` vérifie l'enregistrement dynamique des fournisseurs, les identifiants natifs, la normalisation de l'URL de base, et le comportement du catalogue.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/openrouter-model-capabilities.test.ts` couvre l'analyse du contexte/jeton max, l'invalidation du cache ancien, les métadonnées de support des outils, et le comportement de cache miss.
- `/Users/kevinlin/code/openclaw/src/commands/models/scan.test.ts` couvre le comportement de l'analyse et de la sélection du sondage.
- `/Users/kevinlin/code/openclaw/src/agents/model-compat.test.ts` couvre le comportement de la matrice de modèles en direct OpenRouter organisée.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter models scan openrouter auto dynamic capabilities model refs"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter"`

Résultats :

- A retourné #10687 sur la découverte de modèles entièrement dynamique, #80347 sur les entrées de modèles obsolètes/supprimées, #7006 sur la transparence des modèles acheminés `openrouter/auto`, #68066 sur la génération de rapports de coûts acheminés, et #63145 sur les vérifications de santé par modèle.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter models scan"`

Résultats :

- A trouvé des conseils communautaires de mai et avril 2026 pour exécuter `openclaw models scan`, pour le réexécuter fréquemment car les modèles gratuits OpenRouter changent, pour utiliser `--no-probe` lorsque les analyses capables d'outils échouent, et pour traiter le chat simple sans outil comme un mode de récupération temporaire.
