---
title: "Chemin du fournisseur Google - Note de maturité du cache de prompt"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Google - Note de maturité du cache de prompt

## Résumé

Gemini direct dispose d'un chemin géré `cachedContents` pour `cacheRetention`, de la gestion manuelle des requêtes `cachedContent`, et de la normalisation de l'utilisation de `cachedContentTokenCount` en `cacheRead` OpenClaw. La couverture est Alpha car la voie de régression de cache en direct trouvée dans cet audit est spécifique à Anthropic/OpenAI et aucune preuve spécifique à Google n'a été trouvée pour la création/réutilisation/actualisation du cache géré. La qualité est Beta car le comportement source est bien contenu, mais les archives montrent des conflits d'outils de cache, une confusion 429/backoff, et des malentendus de rapports.

## Portée de la catégorie

Inclus dans cette catégorie :

- Configuration de la rétention du cache : Couvre la configuration de la rétention du cache sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- CachedContents gérés : Couvre les cachedContents gérés sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- Handles cachedContent manuels : Couvre les handles cachedContent manuels sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- Comptabilité de l'utilisation du cache : Couvre la comptabilité de l'utilisation du cache sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- Diagnostics du cache et preuve en direct : Couvre les diagnostics du cache et la preuve en direct sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.

## Fonctionnalités

- Configuration de la rétention du cache : Couvre la configuration de la rétention du cache sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- CachedContents gérés : Couvre les cachedContents gérés sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- Handles cachedContent manuels : Couvre les handles cachedContent manuels sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- Comptabilité de l'utilisation du cache : Couvre la comptabilité de l'utilisation du cache sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.
- Diagnostics du cache et preuve en direct : Couvre les diagnostics du cache et la preuve en direct sur l'éligibilité du cache de prompt Gemini direct `google-generative-ai`, `cacheRetention`, création/réutilisation/actualisation des `cachedContents` gérés, configuration manuelle de `cachedContent`, et comportement associé du cache de prompt.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs : La source couvre l'éligibilité du cache, la politique de rétention du cache, la création/réutilisation/actualisation du contenu en cache géré, le patching de charge utile, le backoff de retry, et la normalisation de l'utilisation ; les tests unitaires couvrent les chemins principaux.
- Signaux négatifs : Aucune voie Google n'a été trouvée dans le runner de régression de cache en direct, et aucune preuve spécifique à Google en direct/e2e n'a été trouvée pour la création/réutilisation/actualisation du cache géré.
- Lacunes d'intégration : Le `cachedContent` manuel et le `cacheRetention` géré nécessitent une validation en direct avec les tours d'outils et le rapports de cache-hit.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : #51372 a demandé le support `cachedContents` Gemini et est fermé ; #71441 a corrigé les conflits de contenu en cache Google avec système/outils ; #62475 reste ouvert pour le cache de prompt keep-warm ; #86932 reste ouvert pour les avertissements de configuration de cache de prompt obsolète.
- Rapports Discrawl : Les recherches pour `Gemini cachedContent`, `Google cachedContents`, et `cacheRetention google` ont trouvé #71441, #51372, les discussions Gemini 429/backoff, et une préoccupation d'examen P1 concernant la préservation des outils avec le contenu en cache géré.
- Bonnes qualités : La source limite l'éligibilité aux familles Gemini directes, sépare les handles manuels de l'injection de cache géré, persiste l'état du cache, et mappe les compteurs de cache-read natifs du fournisseur en utilisation OpenClaw.
- Mauvaises qualités : Le comportement du cache reste opérationnellement difficile à raisonner, en particulier lorsque les outils, TTL, 429/backoff, et les grands compteurs `cacheRead` sont impliqués.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-provider-path.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour la configuration de la rétention du cache, les cachedContents gérés, les handles cachedContent manuels, la comptabilité de l'utilisation du cache, les diagnostics du cache et la preuve en direct.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Google est absent de la porte de régression de cache en direct trouvée lors de cet audit.
- Le contenu en cache géré avec les tours d'outils nécessite une preuve récurrente après le conflit antérieur #71441.
- Le `cachedContent` manuel est documenté et accepté par les paramètres supplémentaires, mais devrait continuer à être vérifié par rapport aux chemins actuels du générateur de requêtes.
- Les grandes valeurs `cacheRead` peuvent toujours confondre l'interprétation de l'opérateur de la comptabilité du contexte.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/reference/prompt-caching.md:151`
  documente le mappage Gemini `cachedContentTokenCount` vers `cacheRead` et les ressources `cachedContents` gérées pour `cacheRetention`.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:409` documente la réutilisation du cache Gemini direct, `cachedContent` et `cached_content`, et `cacheRead`.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:215`
  documente la configuration `cachedContent` Gemini direct.
- `/Users/kevinlin/code/openclaw/docs/reference/token-use.md:90` documente
  les champs d'utilisation natifs du fournisseur normalisés et les compteurs de cache.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/prompt-cache-retention.ts:6`
  limite l'éligibilité du cache Google aux modèles Gemini 2.5 et Gemini 3 directs.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/google-prompt-cache.ts:77`
  calcule le TTL et les digests de cache de prompt système.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/google-prompt-cache.ts:268`
  implémente le patching TTL du contenu en cache et la création POST.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/google-prompt-cache.ts:329`
  gère les entrées prêtes/échouées persistées, la réutilisation, l'actualisation, et le backoff de retry.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/google-prompt-cache.ts:444`
  enveloppe la fonction de flux et corrige les charges utiles sortantes avec `cachedContent`.
- `/Users/kevinlin/code/openclaw/src/llm/providers/google-shared.ts:542` mappe
  `cachedContentTokenCount` vers `cacheRead`.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/prompt-cache-observability.ts:144`
  commence l'observation du cache de prompt et détecte ultérieurement le comportement de rupture de cache.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/package.json:1739` définit `test:live:cache`.
- `/Users/kevinlin/code/openclaw/src/agents/live-cache-regression-baseline.ts:14`
  définit les lignes de base de cache en direct pour Anthropic et OpenAI uniquement.
- `/Users/kevinlin/code/openclaw/src/agents/live-cache-regression-runner.ts:329`
  tape les voies de cache répétées comme `anthropic | openai`.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:99`
  inclut les modèles Google dans la couverture de fournisseur en direct plus large, mais pas la couverture spécifique au cache.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/google-prompt-cache.test.ts:147`
  vérifie la création/réutilisation/actualisation et l'injection de charge utile gérée.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/prompt-cache-retention.test.ts:5`
  vérifie le mappage de rétention Google direct et l'éligibilité.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/prompt-cache-retention.test.ts:127`
  vérifie l'éligibilité de la famille Google direct et exclut Gemini Live.
- `/Users/kevinlin/code/openclaw/src/llm/providers/google-shared.test.ts:84`
  vérifie que `cachedContentTokenCount` devient `cacheRead`.

### Requêtes Gitcrawl

Requête : `gitcrawl search prs "Google prompt cache cachedContent" -R openclaw/openclaw --state all`

Résultats :

- A retourné #71441, un correctif fermé pour les conflits `cachedContent` Google avec système/outils.

Requête : `gitcrawl search issues "Google prompt cache cachedContent cacheRetention" -R openclaw/openclaw --state all`

Résultats :

- La requête exacte n'a retourné aucun résultat de problème direct.

Requête : `gitcrawl search issues "cachedContents cacheRetention Gemini" -R openclaw/openclaw --state all`

Résultats :

- A retourné #51372 demandant le support du contenu en cache Gemini, #62475 pour le cache de prompt keep-warm, et #86932 pour les avertissements de configuration de cache de prompt obsolète.

### Requêtes Discrawl

Requête : `discrawl search --limit 5 "Google prompt cache cachedContent cacheRetention"`

Résultats :

- A retourné l'historique d'examen PR #71441 et la préoccupation P1 concernant la préservation des outils avec le contenu en cache géré.

Requête : `discrawl search --limit 5 "Gemini cachedContent"`

Résultats :

- A retourné l'historique du support #51372 plus les discussions Gemini 429/backoff et cache TTL.

Requête : `discrawl search --limit 5 "cachedContentTokenCount cacheRead"`

Résultats :

- A retourné l'historique d'examen pour le mappage d'utilisation Google et les correctifs de double comptage du cache.
