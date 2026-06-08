---
title: "Chemin du fournisseur OpenRouter - Note de maturité d'attribution et de mise en cache"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenRouter - Note de maturité d'attribution et de mise en cache

## Résumé

L'attribution et le comportement de cache d'OpenRouter sont explicitement implémentés : les routes OpenRouter vérifiées reçoivent des en-têtes d'attribution d'application documentés, des en-têtes de cache de réponse optionnels, des marqueurs `cache_control` Anthropic contrôlés par route, l'éligibilité au cache-TTL pour DeepSeek/Moonshot/ZAI, et la cartographie d'utilisation cache-read/cache-write spécifique à OpenRouter. La couverture est Beta car les tests de wrapper sont ciblés, mais la preuve de cache en direct est contrôlée et le comportement du prompt-cache reste dépendant du fournisseur.

La qualité est Beta car la source actuelle est prudente, mais les archives montrent des régressions récentes de cache-control, des erreurs de charge utile de cache visibles par l'utilisateur, et des préoccupations concernant le couplage du cache de démarrage/tarification.

## Portée de la catégorie

Cette catégorie couvre l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et clear, les marqueurs cache-control Anthropic, la rétention du prompt-cache, la cartographie d'utilisation cache-read/cache-write, le contrôle de route vérifiée, et les exclusions de proxy personnalisé.

## Fonctionnalités

- En-têtes d'attribution : Couvre les en-têtes d'attribution dans l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et clear, les marqueurs cache-control Anthropic, la rétention du prompt-cache, la cartographie d'utilisation cache-read/cache-write, le contrôle de route vérifiée, et les exclusions de proxy personnalisé.
- En-têtes de cache de réponse/TTL/clear : Couvre les en-têtes de cache de réponse/TTL/clear dans l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et clear, les marqueurs cache-control Anthropic, la rétention du prompt-cache, la cartographie d'utilisation cache-read/cache-write, le contrôle de route vérifiée, et les exclusions de proxy personnalisé.
- Marqueurs cache-control Anthropic : Couvre les marqueurs cache-control Anthropic dans l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et clear, les marqueurs cache-control Anthropic, la rétention du prompt-cache, la cartographie d'utilisation cache-read/cache-write, le contrôle de route vérifiée, et les exclusions de proxy personnalisé.
- Cartographie d'utilisation du cache : Couvre la cartographie d'utilisation du cache dans l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et clear, les marqueurs cache-control Anthropic, la rétention du prompt-cache, la cartographie d'utilisation cache-read/cache-write, le contrôle de route vérifiée, et les exclusions de proxy personnalisé.
- Exclusions de proxy personnalisé : Couvre les exclusions de proxy personnalisé dans l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et clear, les marqueurs cache-control Anthropic, la rétention du prompt-cache, la cartographie d'utilisation cache-read/cache-write, le contrôle de route vérifiée, et les exclusions de proxy personnalisé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : Les tests couvrent les en-têtes d'attribution, le comportement d'activation/désactivation/actualisation/TTL du cache de réponse, les exclusions de route vérifiée, les marqueurs cache-control Anthropic, et la cartographie d'utilisation du cache.
- Signaux négatifs : Le comportement du cache en direct est contrôlé par l'environnement et le support du fournisseur ; la sémantique du prompt-cache varie selon les upstreams routés par OpenRouter.
- Lacunes d'intégration : Ajouter une preuve de cache en direct programmée pour les routes OpenRouter Anthropic et DeepSeek, y compris les en-têtes de cache de réponse, l'observation des jetons en cache, et les cas négatifs de proxy personnalisé.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : La requête OpenRouter large a retourné #63034 pour cache-control ne s'appliquant pas aux messages de conversation et #68066 pour l'inadéquation des coûts d'utilisation en streaming OpenRouter ; la recherche PR a retourné #63062, #79370, et #87562 comme correctifs connexes.
- Rapports Discrawl : La recherche Discord a trouvé un rapport visible par l'utilisateur en mai 2026 `cache_control: Extra inputs are not permitted` et une discussion sur les récupérations de catalogue de tarification OpenRouter/LiteLLM ralentissant le démarrage.
- Bonnes qualités : L'implémentation limite les en-têtes spécifiques à OpenRouter aux routes OpenRouter vérifiées, supporte les paramètres de cache de réponse explicites, et évite d'injecter des marqueurs OpenRouter dans les proxies personnalisés arbitraires.
- Mauvaises qualités : Le comportement du cache est toujours sensible à la sémantique du fournisseur upstream, à la famille de modèles, à la classe de route, et à la compatibilité de la charge utile.
- Exclu de la qualité : La profondeur des tests unitaires et les tests de cache contrôlés en direct sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openrouter-provider-path.md`.
- Signaux positifs : les archives de docs, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour les en-têtes d'attribution, les en-têtes de cache de réponse/TTL/clear, les marqueurs cache-control Anthropic, la cartographie d'utilisation du cache, les exclusions de proxy personnalisé.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuve` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La mise en cache des réponses, les marqueurs de prompt-cache, et l'utilisation des jetons en cache sont des concepts distincts que les docs expliquent mais que les utilisateurs peuvent toujours confondre.
- La compatibilité de la charge utile cache-control dépend du fournisseur upstream réel derrière OpenRouter.
- La récupération du catalogue de tarification/cache a généré des préoccupations chez l'opérateur lorsque des chemins de démarrage de passerelle non liés contactent OpenRouter.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente les en-têtes d'attribution d'application, la mise en cache des réponses, les marqueurs cache Anthropic, le contrôle de route vérifiée, les exclusions de proxy personnalisé, et les distinctions cache-control.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md` résume le comportement d'attribution et de marqueur de cache contrôlé par route d'OpenRouter.
- `/Users/kevinlin/code/openclaw/docs/reference/prompt-caching.md` documente les concepts de prompt-cache adjacents à cette surface.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/provider-attribution.ts` définit les en-têtes d'attribution documentés d'OpenRouter et le contrôle de point de terminaison vérifiée.
- `/Users/kevinlin/code/openclaw/src/llm/providers/stream-wrappers/proxy.ts` résout les en-têtes de cache de réponse OpenRouter, le serrage TTL, le cache clear, les marqueurs cache Anthropic, et la normalisation de charge utile de raisonnement.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-completions.ts` applique le contrôle de cache Anthropic et mappe `cached_tokens` / `cache_write_tokens` à l'utilisation.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts` marque les familles de modèles OpenRouter éligibles au comportement TTL du cache.
- `/Users/kevinlin/code/openclaw/src/gateway/model-pricing-cache.ts` récupère et canonicalise les métadonnées de tarification OpenRouter.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/openrouter/openrouter.live.test.ts` contrôle en direct l'observation de cache-read pour un modèle OpenRouter DeepSeek lorsque `OPENCLAW_LIVE_CACHE_TEST=1`.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.e2e.test.ts` couvre la résolution du modèle OpenRouter dans le runtime intégré.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/llm/providers/stream-wrappers/proxy.test.ts` couvre les en-têtes d'attribution OpenRouter, les en-têtes de cache de réponse, le serrage TTL, le clear, les désactivations de préset, les exclusions de proxy personnalisé, et le contrôle de marqueur cache-control Anthropic.
- `/Users/kevinlin/code/openclaw/src/agents/provider-attribution.test.ts` couvre l'attribution OpenRouter et la classification des points de terminaison.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/extra-params.openrouter-cache-control.test.ts` couvre le comportement cache-control OpenRouter Anthropic.
- `/Users/kevinlin/code/openclaw/src/gateway/model-pricing-cache.test.ts` couvre la recherche de tarification OpenRouter et la gestion des défaillances.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter cache headers attribution cache_control cached_tokens"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "OpenRouter"`

Résultats :

- A retourné #63062 sur l'application de cache_control aux messages de conversation sur le chemin OpenRouter, #79370 sur la rétention de cache explicite pour les modèles OpenRouter Anthropic, #87562 sur la réconciliation des coûts en streaming, et #71807 sur la découverte du plugin de catalogue de tarification.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter cache"`

Résultats :

- A trouvé une discussion de support en mai 2026 avec `messages.30.content.1.text.cache_control: Extra inputs are not permitted`, plus une discussion d'avril 2026 sur la récupération du modèle de tarification OpenRouter/LiteLLM causant des délais de démarrage de passerelle et des commentaires #7006 sur la visibilité de l'utilisation/coût `openrouter/auto`.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter cache_control cached_tokens"`

Résultats :

- N'a retourné aucun résultat.
