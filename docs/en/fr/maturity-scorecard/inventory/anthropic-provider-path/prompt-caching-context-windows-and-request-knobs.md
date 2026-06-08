---
title: "Chemin du fournisseur Anthropic - Note de maturité du cache d'invite et du contexte"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Anthropic - Note de maturité du cache d'invite et du contexte

## Résumé

La mise en cache des invites Anthropic et la mise en forme des requêtes sont de première classe : la documentation explique
`cacheRetention`, les fenêtres de contexte de 1M, le mode rapide et la résolution des problèmes de contexte long ;
la source injecte les marqueurs de cache, supprime les bêtas retirées, applique les boutons de niveau de service,
et normalise les métadonnées de contexte GA 1M. La couverture est Stable car la documentation, la source,
et les tests couvrent les principaux boutons. La qualité est Beta car les archives Discord/GitHub
montrent que les utilisateurs ont toujours besoin d'aide concernant les attentes de TTL du cache, les limites de TTL long des fournisseurs personnalisés, les 429 de contexte long, et l'éligibilité des jetons de configuration/clés API.

## Portée de la catégorie

Inclus dans cette catégorie :

- Rétention du cache : Couvre la rétention du cache sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Limite de cache d'invite système : Couvre la limite de cache d'invite système sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Contexte 1M : Couvre le contexte 1M sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Mode rapide/niveau de service : Couvre le mode rapide/niveau de service sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Diagnostics du cache : Couvre les diagnostics du cache sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.

## Fonctionnalités

- Rétention du cache : Couvre la rétention du cache sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Limite de cache d'invite système : Couvre la limite de cache d'invite système sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Contexte 1M : Couvre le contexte 1M sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Mode rapide/niveau de service : Couvre le mode rapide/niveau de service sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.
- Diagnostics du cache : Couvre les diagnostics du cache sur les boutons de requête spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache d'invite, marqueurs de contrôle de cache, limite de cache d'invite système, dimensionnement du contexte 1M, et comportement associé du cache d'invite et du contexte.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La documentation couvre la mise en cache des invites, l'ordre de fusion de cacheRetention, le comportement direct de TTL 5 minutes et 1 heure d'Anthropic, le contexte 1M, le mode rapide, et la correction des 429 ; la source et les tests couvrent les marqueurs de cache, les remplacements de fenêtre de contexte, la suppression des bêtas, le comportement du niveau de service, et les valeurs par défaut du cache.
- Signaux négatifs : La preuve en direct du comportement de cache-hit et de l'éligibilité du contexte 1M dépend de l'état du compte en amont et n'est pas entièrement couverte par les tests locaux déterministes.
- Lacunes d'intégration : L'audit a trouvé la preuve docs/source/test mais pas un artefact de smoke test de cache-hit et de contexte 1M répété d'Anthropic.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : #37966 signale `cacheRetention` ignoré pour les modèles Anthropic proxifiés par LiteLLM ; #62475 demande des pings de maintien au chaud du cache d'invite ; #63030 signale une dérive d'assemblage d'invite système causant l'invalidation du cache Anthropic ; PR #79370 corrige cacheRetention explicite pour les modèles OpenRouter vers Anthropic.
- Rapports Discrawl : Les résultats de l'archive Discord incluent des questions de cache 1 heure de fournisseur personnalisé, une confusion de cache-hit Haiku, des conseils de limite de cache d'invite système, et une résolution des problèmes d'utilisation supplémentaire du contexte 1M 429.
- Bonnes qualités : La politique de cache est centralisée, le TTL long est contrôlé par endpoint, les en-têtes bêta 1M retirés sont supprimés, l'authentification par clé API obtient des valeurs par défaut conservatrices, et la documentation distingue Anthropic direct des comportements personnalisés/proxy.
- Mauvaises qualités : Les utilisateurs doivent toujours raisonner sur les TTL, le heartbeat, l'élagage du contexte, l'éligibilité du compte de contexte long, le comportement du jeton de configuration par rapport à la clé API, et les limitations des endpoints personnalisés.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/anthropic-provider-path.md`.
- Signaux positifs : les archives de documentation, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour la rétention du cache, la limite de cache d'invite système, le contexte 1M, le mode rapide/niveau de service, les diagnostics du cache.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuve` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le contexte 1M peut être correctement dimensionné localement tout en échouant en amont pour
  l'éligibilité du compte.
- Le TTL de cache long ne s'applique pas uniformément aux hôtes personnalisés compatibles Anthropic arbitraires,
  ce qui est facile à mal configurer.
- La preuve de cache-hit est principalement dérivée de l'utilisation et nécessite des captures de scénarios en direct répétées
  pour la préparation à la version.

## Preuve

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente les valeurs par défaut de la réflexion Claude 4.6, `cacheRetention`, le mode rapide, les médias, le contexte 1M, et la résolution des problèmes pour les identifiants invalides/manquants.
- `/Users/kevinlin/code/openclaw/docs/reference/prompt-caching.md` documente la mise en cache de l'API Anthropic direct, l'ordre de fusion de `cacheRetention`, l'élagage du cache-ttl, le maintien au chaud du heartbeat, le TTL 1 heure Anthropic direct, la gestion du cache Anthropic OpenRouter, et les limites de cache d'invite système.
- `/Users/kevinlin/code/openclaw/docs/gateway/troubleshooting.md` documente `HTTP 429: rate_limit_error: Extra usage is required for long context requests` et les corrections.
- `/Users/kevinlin/code/openclaw/docs/gateway/heartbeat.md` documente les intervalles de heartbeat, y compris un intervalle plus long pour l'authentification OAuth/jeton Anthropic.

### Source

- `/Users/kevinlin/code/openclaw/extensions/anthropic/config-defaults.ts` amorce `contextPruning.mode: "cache-ttl"`, les intervalles de heartbeat, la clé API `cacheRetention: "short"`, et les valeurs par défaut du runtime Claude CLI.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/stream-wrappers.ts` supprime les bêtas context-1m retirées, ajoute les en-têtes bêta Anthropic, injecte les paramètres de niveau de service/mode rapide pour les clés API, et supprime le préfixe de réflexion non sécurisé.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-payload-policy.ts` applique les marqueurs de contrôle de cache Anthropic aux tours système et utilisateur de fin, respecte les limites de cache d'invite système, contrôle le TTL long par endpoint, et injecte le niveau de service.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.ts` résout la rétention du cache, applique le contrôle de cache aux charges utiles système/outil/message, et enregistre les compteurs d'utilisation du cache.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/register.runtime.ts` applique les métadonnées de contexte GA 1M aux modèles Claude 4.x modernes.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` inclut les profils de modèles Anthropic en direct qui exercent les références de modèles Claude modernes.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic.setup-token.live.test.ts` env-gates la complétion de jeton de configuration en direct, prouvant indirectement que les boutons de requête peuvent coexister avec l'authentification de jeton résolue.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/anthropic/stream-wrappers.test.ts` couvre la suppression des bêtas, la préservation des bêtas OAuth, l'injection/les sauts du niveau de service, le comportement du mode rapide, et la suppression du préfixe de réflexion.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-payload-policy.test.ts` couvre l'application des marqueurs de cache, le contrôle par endpoint, la gestion de la limite d'invite système, et la politique de niveau de service.
- `/Users/kevinlin/code/openclaw/src/llm/providers/stream-wrappers/anthropic-cache-control-payload.test.ts` couvre le comportement du marqueur de charge utile de contrôle de cache.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/extra-params.cache-retention-default.test.ts` couvre la sémantique du cache de la famille Anthropic et la rétention explicite.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/index.test.ts` couvre la normalisation du contexte 1M et les valeurs par défaut de cacheRetention de clé API.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic 429 long context extra usage required fallback"`

Résultats :

- N'a retourné aucun résultat direct pour cette requête GitHub exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic prompt caching cacheRetention"`

Résultats :

- #37966 `[Bug]: cacheRetention ignored for LiteLLM-proxied Anthropic models`.
- #62475 demande des pings de maintien au chaud du cache d'invite.
- #63030 signale des différences d'assemblage d'invite système causant l'invalidation continue du cache Anthropic.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "anthropic cacheRetention"`

Résultats :

- #79370 `fix(cache): honour explicit cacheRetention for OpenRouter to Anthropic models`.
- #76741 `fix(kimi): strip anthropic cache markers`.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "Claude 4.6 1M context Anthropic 429"`

Résultats :

- A retourné des fils de support de mars 2026 expliquant `HTTP 429: rate_limit_error: Extra usage is required for long context requests`, les exigences d'utilisation supplémentaire, l'éligibilité de la clé API, et les modifications de configuration pour supprimer `context1m`.

Requête : `discrawl search --limit 10 "Anthropic prompt caching cacheRetention OpenClaw"`

Résultats :

- A retourné des fils de support de mise en cache d'invite sur les taux de cache-hit Haiku, `cacheRetention` configurable, la division statique/dynamique d'invite système, les limitations de cache 1 heure de fournisseur personnalisé, et les pics d'écriture du cache.
