---
title: "Chemin du fournisseur Anthropic - Note de maturité de la sémantique des tours et du transport des requêtes"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Anthropic - Note de maturité de la sémantique des tours et du transport des requêtes

## Résumé

Le transport Messages Anthropic direct est profondément implémenté : il construit
les charges utiles de requête Anthropic, gère les en-têtes de clé API et OAuth/token, 
décode les événements SSE, suit l'utilisation, mappe les raisons d'arrêt, gère les 
abandons et supporte les points de terminaison compatibles avec Anthropic. La couverture 
est Stable car la source et les tests exercent le comportement principal de la charge 
utile et du flux. La qualité est Beta car les preuves d'archive montrent des défaillances 
récurrentes de flux malformés/tronqués et d'appels d'outils qui ont nécessité des 
corrections répétées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Transport API-key/OAuth : Couvre le transport API-key/OAuth sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Charges utiles Messages : Couvre les charges utiles Messages sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Décodage du flux : Couvre le décodage du flux sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Utilisation et raisons d'arrêt : Couvre l'utilisation et les raisons d'arrêt sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Gestion des abandons/erreurs : Couvre la gestion des abandons/erreurs sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Blocs d'utilisation d'outils : Couvre les blocs d'utilisation d'outils sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Relecture du résultat d'outil : Couvre la relecture du résultat d'outil sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Récupération JSON partielle : Couvre la récupération JSON partielle sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Réflexion native : Couvre la réflexion native sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Relecture de la réflexion signée/rédactée : Couvre la relecture de la réflexion signée/rédactée sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.

## Fonctionnalités

- Transport API-key/OAuth : Couvre le transport API-key/OAuth sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Charges utiles Messages : Couvre les charges utiles Messages sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Décodage du flux : Couvre le décodage du flux sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Utilisation et raisons d'arrêt : Couvre l'utilisation et les raisons d'arrêt sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Gestion des abandons/erreurs : Couvre la gestion des abandons/erreurs sur le comportement direct de requête et flux Anthropic `api: "anthropic-messages"` : configuration du transport API-key et OAuth, en-têtes bêta Anthropic, normalisation de l'ID de modèle pour les hôtes directs, construction de charge utile et comportement API anthropic direct associé.
- Blocs d'utilisation d'outils : Couvre les blocs d'utilisation d'outils sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Relecture du résultat d'outil : Couvre la relecture du résultat d'outil sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Récupération JSON partielle : Couvre la récupération JSON partielle sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Réflexion native : Couvre la réflexion native sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.
- Relecture de la réflexion signée/rédactée : Couvre la relecture de la réflexion signée/rédactée sur la sémantique des tours spécifique à Anthropic dans les exécutions d'agent : déclarations d'outils, conversion de bloc d'utilisation d'outils, conversion de résultat d'outil, normalisation de l'ID d'appel d'outil et comportement associé des outils et de la réflexion.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : La source de transport couvre la construction du client, les en-têtes, les charges utiles, l'itération des événements SSE, la comptabilité d'utilisation, la gestion des abandons et le comportement des points de terminaison compatibles ; les tests unitaires couvrent Anthropic direct, OAuth, les points de terminaison personnalisés, les SSE malformés, l'entrée d'outil d'utilisation d'entier non sûr et le comportement d'abandon ; un test de transport en direct couvre l'abandon de flux HTTP réel.
- Signaux négatifs : Certains comportements de fournisseur en direct sont contrôlés par env et la dérive de flux spécifique au fournisseur ne peut pas être entièrement prouvée à partir des tests locaux.
- Lacunes d'intégration : L'audit a trouvé une preuve d'abandon en direct et une couverture unitaire extensive, mais pas de preuve en direct répétée pour chaque combinaison de modèle/authentification Anthropic.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : #60593 signale des erreurs d'analyse JSON de flux Anthropic récurrentes où le basculement a souvent échoué ; PR #62429 a assaini les caractères de contrôle dans l'analyse JSON de flux Anthropic ; PR #61349 a supprimé les erreurs d'analyse JSON brutes des flux d'appels d'outils tronqués ; PR #86959 a finalisé les flux de réponse gérés abandonnés pour libérer les sockets.
- Rapports Discrawl : Les résultats d'archive Discord incluent la corruption de session à partir d'appels d'outils de flux tronqués, les erreurs d'analyse brutes envoyées aux utilisateurs et les corrections d'analyse de flux Anthropic.
- Bonnes qualités : Le transport classe les SSE malformés comme une erreur de transport stable, préserve les champs d'utilisation du fournisseur, évite les en-têtes bêta Anthropic directs sur les hôtes personnalisés, annule les lectures bloquées lors de l'abandon et sépare le comportement de l'en-tête de clé API de celui d'OAuth.
- Mauvaises qualités : Les formes de flux Anthropic et compatibles avec Anthropic ont produit des incidents opérationnels récurrents autour de JSON malformé, de deltas d'outils partiels, de caractères de contrôle et de flux abandonnés.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/anthropic-provider-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le transport API-key/OAuth, les charges utiles Messages, le décodage du flux, l'utilisation et les raisons d'arrêt, la gestion des abandons/erreurs, les blocs d'utilisation d'outils, la relecture du résultat d'outil, la récupération JSON partielle, la réflexion native, la relecture de la réflexion signée/rédactée.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La dérive de flux du fournisseur reste une source récurrente de défauts.
- Certains fournisseurs compatibles ont besoin d'une gestion personnalisée pour la classification des points de terminaison,
  les marqueurs de cache, le contenu de raisonnement et l'assainissement du flux.
- Les combinaisons de modèle/authentification Anthropic directs ont besoin d'une preuve en direct récurrente au-delà
  des tests de transport simulé locaux.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente les routes de clé API et CLI Claude, les paramètres par défaut de la réflexion, la mise en cache des invites, le mode rapide, les médias et le comportement du contexte 1M.
- `/Users/kevinlin/code/openclaw/docs/reference/prompt-caching.md` documente les compteurs d'utilisation Anthropic et le comportement du cache que le transport signale.
- `/Users/kevinlin/code/openclaw/docs/gateway/troubleshooting.md` documente les erreurs 429 de contexte long Anthropic et les conseils de secours.

### Source

- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.ts` implémente la construction du client SDK Anthropic, la gestion des en-têtes OAuth/clé API, la rétention du cache, le décodage SSE, les événements de contenu/outil/réflexion, la comptabilité d'utilisation, le mappage des raisons d'arrêt, la conversion de messages, la conversion d'images et la conversion d'outils.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.ts` implémente le transport de récupération gardé, le dépouillage direct de l'ID de modèle Anthropic, la classification des points de terminaison, les en-têtes bêta, les en-têtes d'identité OAuth, la comptabilité d'utilisation/coût, la classification des flux malformés et le streaming sûr pour l'abandon.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/stream-wrappers.ts` compose les wrappers d'en-tête bêta, mode rapide, niveau de service et préfixe de réflexion autour des flux Anthropic.
- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-fetch.ts` fournit la plomberie de récupération de modèle gardée utilisée par le transport.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.live.test.ts` démarre un serveur SSE HTTP de bouclage et prouve que le transport Anthropic abandonne un flux réel en vol.
- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` vérifie le câblage du profil de fumée de passerelle Anthropic en direct.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.test.ts` couvre l'utilisation de la récupération gardée, le dépouillage de l'ID de modèle, le comportement des en-têtes de point de terminaison personnalisé, la classification des flux malformés, la préservation des entiers non sûrs, le remappage de l'identité/outil OAuth, les blocs de texte/réflexion, les abandons et la forme de demande de réflexion adaptative.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.test.ts` couvre le comportement de construction du client SDK et les charges utiles de relecture de réflexion signées.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/stream-wrappers.test.ts` couvre le dépouillage bêta, les en-têtes bêta OAuth/par défaut, l'injection/sauts de niveau de service et le dépouillage du préfixe de réflexion.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-payload-policy.test.ts` couvre la mise en forme de la politique de cache et de niveau de service Anthropic.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic tool call streaming JSON parse error"`

Résultats :

- #60593 `Erreurs récurrentes d'analyse JSON de streaming Anthropic (Sonnet 4.5 / Opus) - le basculement échoue souvent à récupérer`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "anthropic streaming"`

Résultats :

- #62112 préserve la gestion du refus Anthropic.
- #74432 honore `ANTHROPIC_BASE_URL`.
- #86649 relaie les messages partiels de l'assistant CLI Claude comme des deltas de streaming.
- #75136 préserve l'utilisation du flux Anthropic.
- #62429 et #61349 sont apparus dans les résultats d'archive comme des correctifs d'analyse de flux/appel d'outil.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "Anthropic tool call streaming parse JSON"`

Résultats :

- Ont retourné des rapports d'avril 2026 pour la corruption de session à partir d'appels d'outil de streaming Anthropic tronqués, problème #69846, PR #62429 pour l'assainissement des caractères de contrôle, PR #61349 pour la suppression des erreurs d'analyse brutes et PR #44237 pour la récupération des arguments d'appel d'outil à partir de `partialJson`.

Requête : `discrawl search --limit 10 "Anthropic thinking signature cache control"`

Résultats :

- N'a retourné aucun résultat direct pour cette requête exacte.
