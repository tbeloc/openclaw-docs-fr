---
title: "Chemin du fournisseur OpenAI / Codex - Note de maturité de compatibilité des outils et du contexte"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenAI / Codex - Note de maturité de compatibilité des outils et du contexte

## Résumé

La compatibilité des outils et du contexte dispose de preuves larges mais inégales. Les routes OpenAI/Codex prennent en charge les outils dynamiques OpenClaw, les outils Responses stricts, la politique de recherche web côté serveur, les images d'entrée, les superpositions de prompts GPT-5, les applications natives du plugin Codex, les moteurs de contexte autour des tours Codex, la compatibilité OpenResponses et les Chat Completions compatibles avec OpenAI. La couverture est Beta car certaines capacités sont testées dans les voies de compatibilité de la passerelle tandis que d'autres sont spécifiques au harnais/plugin. La qualité est Beta car les utilisateurs se demandent toujours si les outils natifs du fournisseur passent, et les preuves d'archives antérieures incluent un bug de relecture d'appel d'outil `openai-codex`.

## Portée de la catégorie

Cette catégorie couvre les outils côté fournisseur, l'injection de contexte, les entrées médias, la propriété des outils natifs par rapport aux clients, la compatibilité OpenAI Responses et la façon dont les modèles OpenAI/Codex reçoivent le contexte d'exécution OpenClaw.

## Fonctionnalités

- Contexte des outils : couvre le contexte des outils sur les outils côté fournisseur, l'injection de contexte, les entrées médias, la propriété des outils natifs par rapport aux clients, la compatibilité OpenAI Responses et la façon dont les modèles OpenAI/Codex reçoivent le contexte d'exécution OpenClaw.
- Compatibilité des capacités : couvre la compatibilité des capacités sur les outils côté fournisseur, l'injection de contexte, les entrées médias, la propriété des outils natifs par rapport aux clients, la compatibilité OpenAI Responses et la façon dont les modèles OpenAI/Codex reçoivent le contexte d'exécution OpenClaw.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : la documentation couvre les applications natives du plugin Codex, la compatibilité des entrées/outils OpenResponses, les outils de fonction Chat Completions, les superpositions de prompts GPT-5 et les tableaux de capacités du fournisseur.
- Signaux négatifs : les outils natifs du fournisseur, les outils natifs Codex, les outils dynamiques OpenClaw et les outils Responses côté serveur sont répartis sur des surfaces de compatibilité et des runtimes distincts.
- Lacunes d'intégration : plus de preuves de bout en bout sont nécessaires pour la recherche web côté serveur, les applications natives du plugin Codex et la relecture des images de résultats d'outils sur les versions actuelles du serveur d'applications Codex.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : #76413 enregistre un problème de relecture de session `openai-codex` après un appel d'outil antérieur ; #78573 montre la demande de support de recherche web natif du fournisseur dans les contextes de fournisseur compatibles avec OpenAI adjacents.
- Rapports Discrawl : une discussion sur les outils natifs du fournisseur explique qu'OpenClaw ne transmet pas automatiquement les outils natifs du fournisseur comme `x_search` de xAI car OpenClaw exécute généralement les outils de fonction côté client.
- Bonnes qualités : l'implémentation dispose d'une conversion d'outils stricte explicite, d'une politique de superposition de prompts et d'une configuration d'application native du plugin au lieu d'une transmission implicite.
- Mauvaises qualités : les outils natifs du fournisseur, les outils OpenClaw et les outils du serveur d'applications Codex sont conceptuellement assez proches pour que les utilisateurs puissent s'attendre au mauvais propriétaire d'exécution.
- Exclu de la qualité : la couverture de la passerelle et des tests unitaires a été utilisée uniquement pour la couverture.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le contexte des outils et la compatibilité des capacités.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le support des outils natifs du fournisseur devrait être plus explicite dans la sortie d'état du modèle/fournisseur.
- L'activation de l'application native du plugin Codex a une limite V1 étroite et a besoin de plus d'exemples de bout en bout.
- La relecture des appels d'outils et la relecture des images/résultats d'outils nécessitent une attention de régression récurrente.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente la recherche web côté serveur, la contribution de prompts GPT-5, les API OpenAI non-agent et le comportement de capacité image/modèle.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-native-plugins.md` documente les applications natives du plugin Codex, l'inventaire des applications, la configuration restrictive des applications de thread et la politique d'action destructrice.
- `/Users/kevinlin/code/openclaw/docs/gateway/openresponses-http-api.md` documente les éléments d'entrée OpenResponses, les outils clients, les images, les fichiers et les champs acceptés/ignorés.
- `/Users/kevinlin/code/openclaw/docs/gateway/openai-http-api.md` documente les contrats d'outils Chat Completions et les formes d'outils en streaming.

### Source

- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-responses-tools.ts` convertit les outils OpenClaw en outils de fonction Responses.
- `/Users/kevinlin/code/openclaw/src/agents/openai-strict-tool-setting.ts` active les outils stricts pour les routes OpenAI/Codex natives.
- `/Users/kevinlin/code/openclaw/src/agents/codex-native-web-search.ts` gère la politique de recherche web native Codex.
- `/Users/kevinlin/code/openclaw/extensions/openai/native-web-search.ts` enregistre la capacité de recherche web native OpenAI.
- `/Users/kevinlin/code/openclaw/extensions/openai/prompt-overlay.ts` contrôle le comportement de superposition de prompts GPT-5.
- `/Users/kevinlin/code/openclaw/src/gateway/openresponses-prompt.ts` construit des prompts d'agent compatibles avec OpenResponses.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/openresponses-http.test.ts` couvre les outils OpenResponses, les images/fichiers d'entrée et le comportement SSE.
- `/Users/kevinlin/code/openclaw/src/gateway/openresponses-parity.test.ts` couvre la parité de schéma OpenResponses pour les images d'entrée, les fichiers d'entrée, les métadonnées de phase assistant et les outils.
- `/Users/kevinlin/code/openclaw/src/gateway/openai-http.test.ts` couvre les outils de fonction Chat Completions, le streaming et les entrées de messages d'image.
- `/Users/kevinlin/code/openclaw/scripts/e2e/openai-chat-tools-docker.sh` est un E2E Docker pour les outils de chat compatibles avec OpenAI.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-responses-shared.test.ts` couvre la conversion d'outils stricts et la normalisation de schéma.
- `/Users/kevinlin/code/openclaw/src/agents/openai-responses.reasoning-replay.test.ts` couvre l'ordre de relecture des outils/raisonnement.
- `/Users/kevinlin/code/openclaw/src/config/web-search-codex-config.test.ts` couvre le comportement de configuration de recherche web Codex.
- `/Users/kevinlin/code/openclaw/extensions/openai/plugin-registration.contract.test.ts` couvre l'enregistrement de capacité du plugin OpenAI.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenAI web search server-side Responses tool"`

Résultats :

- A retourné #78573 sur le support de recherche web native pour les modèles GPT GitHub Copilot, pertinent pour les attentes d'outils natifs du fournisseur par rapport à OpenClaw.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenAI Responses reasoning replay function_call tool result"`

Résultats :

- A retourné #76413 sur la relecture d'une réponse d'assistant antérieure `openai-codex` après un appel d'outil.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "OpenAI web search server-side Responses tool"`

Résultats :

- A retourné une discussion sur les outils natifs du fournisseur expliquant qu'OpenClaw utilise normalement l'appel de fonction côté client et son propre outil `web_search` plutôt que de transmettre automatiquement les outils natifs du fournisseur.

Requête : `discrawl search --limit 10 "strict tools OpenAI Responses schema tool_choice"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies.
