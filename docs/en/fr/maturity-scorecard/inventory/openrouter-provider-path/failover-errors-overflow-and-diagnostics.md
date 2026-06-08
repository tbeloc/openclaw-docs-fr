---
title: "Chemin du fournisseur OpenRouter - Note de maturité de la récupération et des diagnostics du fournisseur"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenRouter - Note de maturité de la récupération et des diagnostics du fournisseur

## Résumé

La gestion des défaillances OpenRouter dispose d'une classification explicite du repli de modèle, d'une gestion `Provider returned error` limitée au fournisseur, de cas de limite de budget/clé, d'analyse du débordement de contexte, d'avertissements de statut/tarification, et de tests de politique de récupération gardée. La couverture est Beta car plusieurs classes d'erreurs importantes ont des tests directs, mais le parcours complet de l'opérateur à travers la passerelle, WebChat, cron et le repli de modèle n'est pas exercé uniformément.

La qualité est Alpha car les archives en direct montrent une confusion active ou récente spécifique à OpenRouter autour des blocages Retry-After, du débordement de contexte, de l'interrogation UI vide après 429/timeout, et des erreurs de fournisseur générique.

## Portée de la catégorie

Inclus dans cette catégorie :

- Classification Timeout/retry : Couvre la classification Timeout/retry sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Classification Auth/billing/key-limit : Couvre la classification Auth/billing/key-limit sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Débordement de contexte : Couvre le débordement de contexte sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Avis de repli de modèle : Couvre les avis de repli de modèle sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Avertissements de récupération gardée/tarification : Couvre les avertissements de récupération gardée/tarification sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.

## Fonctionnalités

- Classification Timeout/retry : Couvre la classification Timeout/retry sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Classification Auth/billing/key-limit : Couvre la classification Auth/billing/key-limit sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Débordement de contexte : Couvre le débordement de contexte sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Avis de repli de modèle : Couvre les avis de repli de modèle sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.
- Avertissements de récupération gardée/tarification : Couvre les avertissements de récupération gardée/tarification sur la classification timeout et retry d'OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification auth/billing/key-limit, l'analyse du débordement de contexte, et le comportement de basculement et de diagnostics associé.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : Les tests couvrent le repli de limite de budget de clé API OpenRouter, la gestion du marqueur de refroidissement hérité, le contexte d'erreur limité au fournisseur, les URL de récupération gardée OpenRouter, les expressions régulières de débordement de contexte, et la sortie d'avertissement de statut/tarification.
- Signaux négatifs : Le comportement d'erreur traverse le repli d'agent, le statut de passerelle, WebChat, cron, la récupération de fournisseur, et les réponses OpenRouter en amont ; la preuve de scénario au niveau de la version est fragmentée.
- Lacunes d'intégration : Ajouter des fumées de défaillance de bout en bout pour OpenRouter `Retry-After`, débordement de contexte, clé invalide, billing/key-limit, et `Provider returned error` avec une chaîne de repli configurée.

## Score de qualité

- Score : `Alpha (65%)`
- Rapports Gitcrawl : La requête OpenRouter large a retourné #83651 sur le blocage de repli Retry-After, #86880 sur le débordement de contexte OpenRouter, #87170 sur `Provider returned error` avec `auto`, #79803 sur l'interrogation WebChat après provider 429/idle timeout, et #68066 sur la discordance usage/coût.
- Rapports Discrawl : La recherche Discord a trouvé des discussions sur le repli et le timeout, y compris le timeout du fournisseur OpenRouter dans les sessions isolées cron, les commentaires d'examen de classification d'erreur de fournisseur, et les conseils pour maintenir les replis non-OpenRouter pour la résilience.
- Bonnes qualités : La documentation et les tests actuels montrent une gestion limitée au fournisseur au lieu d'une correspondance générique, la détection de débordement de contexte, et les avertissements de source de tarification dégradée.
- Mauvaises qualités : Les utilisateurs rencontrent toujours des messages d'erreur génériques qui nécessitent l'inspection des journaux, les réinitialisations de session, l'interprétation spécifique au fournisseur, ou la connaissance de la politique de repli.
- Exclu de la qualité : L'étendue du test du chemin d'erreur et la couverture des permutations de repli sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openrouter-provider-path.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour la classification Timeout/retry, la classification Auth/billing/key-limit, le débordement de contexte, les avis de repli de modèle, les avertissements de récupération gardée/tarification.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le comportement Retry-After et timeout côté fournisseur peut toujours bloquer ou confondre les chaînes de repli.
- Le texte générique OpenRouter en amont doit être classé sans étiqueter à tort les erreurs d'authentification et de facturation comme réessayables.
- Les diagnostics de passerelle/WebChat peuvent être en retard par rapport à la défaillance réelle du fournisseur, ce qui rend le comportement de l'interface utilisateur vide ou bloqué.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/concepts/model-failover.md` documente la classification timeout `Provider returned error` spécifique à OpenRouter et la gestion limitée au fournisseur de key-limit/billing.
- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente la configuration OpenRouter, l'URL de base, l'authentification, la sélection de modèle, et les détails de routage dont les opérateurs ont besoin lors du diagnostic.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md` documente le comportement de statut/sonde pour les fournisseurs configurés.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/model-fallback.ts` implémente le comportement de repli de modèle sur les fournisseurs.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-helpers/errors.ts` contient la classification fournisseur/erreur utilisée par les exécutions intégrées.
- `/Users/kevinlin/code/openclaw/src/llm/utils/overflow.ts` reconnaît les messages de longueur de contexte maximum OpenRouter.
- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-fetch.ts` construit le comportement de récupération gardée pour les points de terminaison OpenRouter.
- `/Users/kevinlin/code/openclaw/src/gateway/model-pricing-cache.ts` enregistre les défaillances de récupération de tarification OpenRouter comme statut dégradé au lieu d'une défaillance dure.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/model-fallback.run-embedded.e2e.test.ts` exerce le comportement de repli à travers les exécutions intégrées.
- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre le comportement de liste de modèles/statut à travers les surfaces de commande.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/openrouter.live.test.ts` gère en direct le comportement réel de complétion et de cache OpenRouter.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/model-fallback.test.ts` couvre les erreurs de limite de budget de clé API OpenRouter, les tentatives de repli OpenRouter, et le comportement du marqueur de refroidissement hérité.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run/helpers.resolve-error-context.test.ts` vérifie le contexte d'erreur fournisseur/modèle OpenRouter.
- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-fetch.test.ts` couvre la récupération gardée OpenRouter et la politique de point de terminaison.
- `/Users/kevinlin/code/openclaw/src/commands/gateway-status.test.ts` et `/Users/kevinlin/code/openclaw/src/commands/status-json-payload.test.ts` couvrent les avertissements dégradés de récupération de tarification OpenRouter.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter timeout Provider returned error context length key limit exceeded"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "provider returned error"`

Résultats :

- A retourné #87170 sur `Provider returned error` avec modèle auto, #79803 sur provider 429/idle timeout avec interrogation WebChat, #83225 sur le repli de modèle ne fonctionnant pas sur erreur de facturation, et plusieurs problèmes adjacents provider-error/fallback.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter"`

Résultats :

- A retourné #83651 sur le blocage de repli OpenRouter Retry-After et #86880 sur le débordement de contexte OpenRouter.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter Provider returned error timeout"`

Résultats :

- A trouvé des rapports de timeout de fournisseur OpenRouter dans les sessions isolées cron, une discussion d'examen de PR de classification de basculement, et des conseils de support selon lesquels `Provider returned error` et les chutes de transport doivent être classés dans le comportement de retry/fallback sans avaler les défaillances d'authentification ou de facturation.
