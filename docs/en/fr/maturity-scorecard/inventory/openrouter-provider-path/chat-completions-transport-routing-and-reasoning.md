---
title: "Chemin du fournisseur OpenRouter - Note de maturité du runtime de chat et de la normalisation"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenRouter - Note de maturité du runtime de chat et de la normalisation

## Résumé

Le transport de chat OpenRouter est implémenté via le chemin des complétions compatible OpenAI, les wrappers de flux propriétaires du fournisseur, les paramètres de routage assainis, les charges utiles de raisonnement OpenRouter, la politique de réflexion DeepSeek V4, le dépouillement de préfixe Anthropic, la suppression du raisonnement Hunter Alpha, et les vérifications de route vérifiée. La couverture est Beta car le composant dispose de tests ciblés substantiels mais de moins de fumées de version de bout en bout sur les backends OpenRouter représentatifs.

La qualité est Beta car l'implémentation dispose de garde-fous explicites, mais les rapports archivés montrent que le comportement du raisonnement spécifique au fournisseur/modèle peut toujours changer sous OpenClaw.

## Portée de la catégorie

Inclus dans cette catégorie :

- Route des complétions de chat : Couvre la route des complétions de chat sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Paramètres de routage du fournisseur : Couvre les paramètres de routage du fournisseur sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Remplacements de route par modèle : Couvre les remplacements de route par modèle sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Politique de charge utile de raisonnement : Couvre la politique de charge utile de raisonnement sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Variantes Anthropic/Gemini/DeepSeek : Couvre les variantes Anthropic/Gemini/DeepSeek sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Analyse du contenu en flux : Couvre l'analyse du contenu en flux sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Sortie visible reasoning_details : Couvre la sortie visible reasoning_details sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Préservation des deltas d'appel d'outil : Couvre la préservation des deltas d'appel d'outil sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Politique de relecture spécifique à la famille : Couvre la politique de relecture spécifique à la famille sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Normalisation du modèle de réponse et de l'utilisation : Couvre la normalisation du modèle de réponse et de l'utilisation sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- En-têtes d'attribution : Couvre les en-têtes d'attribution sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- En-têtes/TTL/effacement du cache de réponse : Couvre les en-têtes/TTL/effacement du cache de réponse sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- Marqueurs de contrôle de cache Anthropic : Couvre les marqueurs de contrôle de cache Anthropic sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- Mappage d'utilisation du cache : Couvre le mappage d'utilisation du cache sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- Exclusions de proxy personnalisées : Couvre les exclusions de proxy personnalisées sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.

## Fonctionnalités

- Route des complétions de chat : Couvre la route des complétions de chat sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Paramètres de routage du fournisseur : Couvre les paramètres de routage du fournisseur sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Remplacements de route par modèle : Couvre les remplacements de route par modèle sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Politique de charge utile de raisonnement : Couvre la politique de charge utile de raisonnement sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Variantes Anthropic/Gemini/DeepSeek : Couvre les variantes Anthropic/Gemini/DeepSeek sur le transport des complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de routage par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement de routage et de raisonnement de chat associé.
- Analyse du contenu en flux : Couvre l'analyse du contenu en flux sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Sortie visible reasoning_details : Couvre la sortie visible reasoning_details sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Préservation des deltas d'appel d'outil : Couvre la préservation des deltas d'appel d'outil sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Politique de relecture spécifique à la famille : Couvre la politique de relecture spécifique à la famille sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- Normalisation du modèle de réponse et de l'utilisation : Couvre la normalisation du modèle de réponse et de l'utilisation sur l'analyse des réponses en flux, l'extraction de la sortie visible à partir de `reasoning_details` OpenRouter, la préservation des deltas d'appel d'outil, la politique de relecture Mistral strict9, et le comportement de relecture et d'appel d'outil en flux associé.
- En-têtes d'attribution : Couvre les en-têtes d'attribution sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- En-têtes/TTL/effacement du cache de réponse : Couvre les en-têtes/TTL/effacement du cache de réponse sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- Marqueurs de contrôle de cache Anthropic : Couvre les marqueurs de contrôle de cache Anthropic sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- Mappage d'utilisation du cache : Couvre le mappage d'utilisation du cache sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.
- Exclusions de proxy personnalisées : Couvre les exclusions de proxy personnalisées sur l'attribution d'application OpenRouter, les en-têtes de cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache de prompt, le mappage d'utilisation cache-read/cache-write, la mise en porte de route vérifiée, et les exclusions de proxy personnalisées.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La fusion des paramètres de routage, les profils de raisonnement, le dépouillement de préfixe, la normalisation de l'URL de base, et le comportement de réflexion DeepSeek V4 disposent de tests ciblés.
- Signaux négatifs : La couverture est la plus forte aux coutures du wrapper et du transport ; il y a moins de preuve toujours active que le même comportement fonctionne en direct sur les routes Anthropic, DeepSeek, Google, OpenAI, MiniMax, et OpenRouter `auto`.
- Lacunes d'intégration : Ajouter des scénarios de transport de chat en direct pour un modèle Anthropic, un DeepSeek V4, un Gemini, et un modèle OpenRouter sans raisonnement avec les paramètres de routage activés.

## Score de qualité

- Score : `Beta (71%)`
- Rapports Gitcrawl : La requête OpenRouter large a retourné des rapports de modèle routé et d'erreur, tandis que les requêtes de routage/raisonnement exact n'ont retourné aucun nouveau résultat direct.
- Rapports Discrawl : La recherche Discord a trouvé des rapports d'avril 2026 où les modèles de raisonnement OpenRouter ont retourné du texte visible dans les champs de raisonnement ou `content: null`, conduisant à un repli ou une sortie vide sur les anciennes versions.
- Bonnes qualités : L'implémentation assainit les objets de routage du fournisseur, supprime les clés d'objet dangereuses, limite le routage aux routes de complétions de chat OpenRouter, normalise les URL de base obsolètes, et supprime le raisonnement proxy pour les références Hunter Alpha connues comme mauvaises.
- Mauvaises qualités : Le comportement du backend OpenRouter varie selon le fournisseur sous-jacent ; les champs de sortie de raisonnement, la forme du contenu, et le comportement du modèle côté fournisseur ont changé suffisamment pour nécessiter des cas spéciaux répétés.
- Exclu de la qualité : La profondeur des tests du wrapper et du transport n'est notée que sous Couverture.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openrouter-provider-path.md`.
- Signaux positifs : docs archivées, source, test, Gitcrawl et preuves Discrawl couvrent l'étendue de la taxonomie pour la route Chat completions, les paramètres de routage des fournisseurs, les remplacements de route par modèle, la politique de charge utile de raisonnement, les variantes Anthropic/Gemini/DeepSeek, l'analyse du contenu en flux, la sortie visible de reasoning_details, la préservation des deltas d'appels d'outils, la politique de relecture spécifique à la famille, la normalisation du modèle de réponse et de l'utilisation, les en-têtes d'attribution, les en-têtes/TTL/effacement du cache de réponse, les marqueurs de contrôle de cache Anthropic, le mappage d'utilisation du cache, les exclusions de proxy personnalisé.
- Signaux négatifs : la note archivée a précédé le score de complétude du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le routage `auto` et des fournisseurs OpenRouter peut sélectionner des backends avec une sémantique de raisonnement et d'appels d'outils différente de celle que le modèle configuré suggère.
- Le support du raisonnement est modélisé pour des familles spécifiques mais dépend toujours des métadonnées OpenRouter et du comportement observé du backend.
- Les routes de proxy personnalisé ignorent intentionnellement certains traitements spécifiques à OpenRouter, ce qui est correct mais augmente la surprise de l'opérateur lorsqu'une configuration OpenRouter copiée est réorientée.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente les métadonnées de routage des fournisseurs OpenRouter, le raisonnement proxy, la relecture du raisonnement DeepSeek V4, la gestion du préfixe Anthropic, le comportement de la route soutenue par Gemini et l'exclusion de la mise en forme native OpenAI uniquement.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md` résume l'attribution d'application de route vérifiée OpenRouter, le marqueur de cache, le comportement compatible OpenAI de style proxy et la gestion de la signature de pensée Gemini.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openrouter/provider-routing.ts` assainit et fusionne les paramètres de routage OpenRouter au niveau du fournisseur, du modèle et de la requête.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/stream.ts` injecte le routage, supprime les messages de préfixe Anthropic lorsque le raisonnement est activé, corrige la pensée DeepSeek V4 et limite le comportement aux routes OpenRouter vérifiées.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/thinking-policy.ts` définit les niveaux de pensée DeepSeek V4 et le support `xhigh`.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-completions.ts` mappe le raisonnement OpenRouter aux charges utiles `reasoning` imbriquées et transmet les préférences de routage des fournisseurs OpenRouter.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/openrouter/openrouter.live.test.ts` limite en direct une complétion OpenRouter réelle et la résolution dynamique du modèle.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.e2e.test.ts` couvre la résolution explicite du modèle OpenRouter via l'exécution de l'agent intégré.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.test.ts` vérifie la fusion et l'assainissement du routage des fournisseurs, la suppression du raisonnement Hunter Alpha, les niveaux de pensée DeepSeek V4, l'élimination du préfixe Anthropic, les exclusions de route personnalisée et la normalisation de l'URL de base.
- `/Users/kevinlin/code/openclaw/src/llm/providers/stream-wrappers/proxy.test.ts` couvre le comportement du wrapper OpenRouter, les en-têtes du cache de réponse et la limitation du marqueur de cache Anthropic.
- `/Users/kevinlin/code/openclaw/src/agents/openai-transport-stream.test.ts` couvre l'analyse des détails du raisonnement OpenRouter et le comportement de la sortie visible.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter provider routing reasoning DeepSeek Hunter Alpha"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter"`

Résultats :

- A retourné #87170 sur `Provider returned error` avec `auto`, #86880 sur débordement de contexte OpenRouter, #79047 sur commutateurs de modèle inter-backend et #7006 sur transparence du modèle routé.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter provider routing reasoning"`

Résultats :

- A trouvé des rapports d'avril 2026 sur les modèles OpenRouter retournant du texte de réponse dans les champs de raisonnement, les métadonnées de fournisseur obsolètes causant un repli de fournisseur et les corrections ultérieures pour l'analyse de `reasoning_details.response.output_text` / `response.text`.
