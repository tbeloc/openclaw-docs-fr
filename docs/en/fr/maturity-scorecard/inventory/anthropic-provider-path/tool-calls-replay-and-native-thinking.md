---
title: "Chemin du fournisseur Anthropic - Note de maturité des outils et de la réflexion"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Anthropic - Note de maturité des outils et de la réflexion

## Résumé

La gestion des appels d'outils et de la réflexion native d'Anthropic est large : OpenClaw convertit les outils en schémas Anthropic, mappe les noms d'outils Claude Code sous OAuth, préserve la réflexion signée/rédactée, assainit la relecture malformée, gère les médias des résultats d'outils, et mappe les niveaux de réflexion à l'effort du fournisseur. La couverture est Stable car la source et les tests couvrent les transformations clés et la relecture en direct. La qualité est Beta car les incidents archivés montrent que le streaming des appels d'outils et la relecture de la réflexion ont été des points de régression fréquents.

## Portée de la catégorie

Cette catégorie couvre la sémantique des tours spécifique à Anthropic dans les exécutions d'agents : déclarations d'outils, conversion de blocs d'utilisation d'outils, conversion de résultats d'outils, normalisation des identifiants d'appels d'outils, gestion JSON partielle, mappage des noms d'outils Claude Code, blocs de réflexion native, réflexion rédactée, relecture de réflexion signée, effort/défauts de réflexion, et validation des tours pour la relecture.

## Fonctionnalités

- Blocs d'utilisation d'outils : Couvre les blocs d'utilisation d'outils dans la sémantique des tours spécifique à Anthropic dans les exécutions d'agents : déclarations d'outils, conversion de blocs d'utilisation d'outils, conversion de résultats d'outils, normalisation des identifiants d'appels d'outils, et comportements connexes des outils et de la réflexion.
- Relecture des résultats d'outils : Couvre la relecture des résultats d'outils dans la sémantique des tours spécifique à Anthropic dans les exécutions d'agents : déclarations d'outils, conversion de blocs d'utilisation d'outils, conversion de résultats d'outils, normalisation des identifiants d'appels d'outils, et comportements connexes des outils et de la réflexion.
- Récupération JSON partielle : Couvre la récupération JSON partielle dans la sémantique des tours spécifique à Anthropic dans les exécutions d'agents : déclarations d'outils, conversion de blocs d'utilisation d'outils, conversion de résultats d'outils, normalisation des identifiants d'appels d'outils, et comportements connexes des outils et de la réflexion.
- Réflexion native : Couvre la réflexion native dans la sémantique des tours spécifique à Anthropic dans les exécutions d'agents : déclarations d'outils, conversion de blocs d'utilisation d'outils, conversion de résultats d'outils, normalisation des identifiants d'appels d'outils, et comportements connexes des outils et de la réflexion.
- Relecture de réflexion signée/rédactée : Couvre la relecture de réflexion signée/rédactée dans la sémantique des tours spécifique à Anthropic dans les exécutions d'agents : déclarations d'outils, conversion de blocs d'utilisation d'outils, conversion de résultats d'outils, normalisation des identifiants d'appels d'outils, et comportements connexes des outils et de la réflexion.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La source gère la réflexion native Anthropic, la relecture de réflexion signée/rédactée, la conversion de schémas d'outils, le regroupement des résultats d'outils, les résultats d'outils image, les alias d'outils Claude Code, le nettoyage des brouillons JSON partiels, et la validation de relecture ; les tests couvrent la réflexion signée, la relecture d'utilisation d'outils, les arguments d'outils malformés, et la relecture d'outils en direct.
- Signaux négatifs : Plusieurs cas sont couverts par des tests ciblés et des tests en direct avec portail d'environnement plutôt que par des scénarios d'outils Anthropic de bout en bout toujours actifs.
- Lacunes d'intégration : La preuve complète du scénario d'appel d'outils en direct est limitée par `ANTHROPIC_LIVE_TEST` et les identifiants du fournisseur.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : #60593 suit les erreurs d'analyse JSON de streaming Anthropic récurrentes ; PR #68565 préserve les blocs de réflexion signée/rédactée ; PR #70372 supprime la fuite de narration de réflexion ; PR #87346 fusionne les tours d'assistant consécutives dans la validation ; PR #61151 supprime les artefacts de streaming `partialJson` de la réparation de l'historique de session.
- Rapports Discrawl : Les résultats de l'archive Discord incluent la corruption de session à partir d'appels d'outils de streaming tronqués, les erreurs d'analyse brutes des deltas d'appels d'outils Anthropic, et les correctifs en aval pour la récupération JSON partielle.
- Bonnes qualités : L'implémentation préserve la réflexion signée par le fournisseur, supprime le raisonnement synthétique de la relecture Anthropic native, fusionne les résultats d'outils consécutifs, force les arguments d'appels d'outils malformés, et évite de persister les tampons de brouillon de streaming.
- Mauvaises qualités : Le streaming des appels d'outils est l'un des bords Anthropic les plus changeants car JSON partiel, signatures de réflexion, points de terminaison compatibles avec le fournisseur, et validation de relecture interagissent.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/anthropic-provider-path.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour les blocs d'utilisation d'outils, la relecture des résultats d'outils, la récupération JSON partielle, la réflexion native, la relecture de réflexion signée/rédactée.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve en direct est la plus forte pour l'acceptation de relecture synthétique, pas pour chaque type d'invocation d'outil réel.
- Le comportement des appels d'outils et de la réflexion diffère entre Anthropic direct et les fournisseurs compatibles avec Anthropic, augmentant la pression de maintenance.
- Les incidents historiques montrent que JSON partiel et l'affichage de la réflexion peuvent corrompre l'historique de session ou fuir du texte confus s'ils ne sont pas soigneusement normalisés.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente les défauts de réflexion Claude 4.6, les remplacements `/think`, le comportement du cache, et la gestion des médias/documents.
- `/Users/kevinlin/code/openclaw/docs/gateway/cli-backends.md` documente le mode de permission Claude CLI, le mappage d'effort `/think`, les outils de pont MCP, et le comportement de session.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md` couvre le comportement du modèle/fournisseur qui alimente les choix de transport des outils et de la réflexion.

### Source

- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.ts` implémente `convertTools`, `convertMessages`, `normalizeToolCallId`, relecture de réflexion signée/rédactée, accumulation `input_json_delta`, blocs d'utilisation d'outils, regroupement des résultats d'outils, et construction de demande d'effort de réflexion.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.ts` implémente la coercion d'arguments d'outils côté transport, la préservation d'entiers non sûrs, la gestion du contenu de raisonnement pour les flux compatibles, et le comportement de relecture de réflexion native Anthropic.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/thinking.ts` enveloppe les flux Anthropic avec récupération de réflexion et bloque les relances de streaming en double après le début de la sortie.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/replay-policy.ts` définit la politique de relecture Anthropic incluant les identifiants d'outils stricts, la préservation de signature, la validation des tours, et l'autorisation des résultats d'outils synthétiques.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.anthropic-tool-replay.live.test.ts` porte avec portail d'environnement l'acceptation de relecture Anthropic en direct pour le texte régulier, l'espace réservé de raisonnement omis, et l'historique de relecture d'appels d'outils.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.live.test.ts` couvre le comportement d'abandon de flux en direct adjacent au streaming d'outils/réflexion.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.test.ts` couvre les deltas d'utilisation d'outils d'entiers non sûrs, le remappage des noms d'outils OAuth, l'ingestion de réflexion signée, plusieurs deltas de signature, la relecture compatible `reasoning_content`, les schémas d'outils malformés, les arguments d'appels d'outils malformés, les résultats d'outils vides, les résultats d'outils image, et le mappage d'effort de réflexion.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.test.ts` couvre la préservation de la charge utile de relecture de réflexion signée.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/index.test.ts` couvre la politique de relecture et le mode de sortie de raisonnement natif.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/cli-shared.test.ts` couvre le mappage d'effort de réflexion Claude CLI.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "anthropic thinking signature replay cache_control"`

Résultats :

- Aucun résultat direct pour cette requête de problème exacte.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "Anthropic thinking"`

Résultats :

- #70372 supprime la fuite de narration de réflexion dans les messages de canal pour Anthropic/Bedrock.
- #68565 préserve les blocs de réflexion signée/rédactée.
- #87346 fusionne les tours d'assistant consécutives dans la validation des tours.
- #85381 émet des événements `thinking_delta` et gère la forme de bloc unique rédactée.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic tool call streaming JSON parse error"`

Résultats :

- #60593 signale les erreurs d'analyse JSON de streaming Anthropic récurrentes.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "Anthropic tool call streaming parse JSON"`

Résultats :

- Résultats archivés retournés des rapports d'utilisateurs et des notifications PR pour la corruption d'appels d'outils de streaming tronqués, les erreurs d'analyse brutes, l'assainissement des caractères de contrôle, et la récupération des arguments d'appels d'outils.

Requête : `discrawl search --limit 10 "Anthropic thinking signature cache control"`

Résultats :

- Aucun résultat direct pour cette requête exacte.
