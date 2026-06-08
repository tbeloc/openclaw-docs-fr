---
title: "OpenAI / Codex provider path - Native Codex Harness Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# OpenAI / Codex provider path - Native Codex Harness Maturity Note

## Résumé

Le harnais natif Codex app-server est largement documenté et dispose de preuves d'exécution significatives. Il couvre le démarrage du app-server stdio géré, les connexions WebSocket du app-server, les contrôles `/codex`, la liaison/reprise/compaction des threads natifs, la direction des files d'attente, les hooks natifs, les ponts d'approbation, la politique de sandbox, les applications de plugins natifs, Computer Use et le téléchargement de diagnostics. La couverture est Stable car il existe des docs, des modules source, des tests unitaires ciblés, Docker E2E et des sondes de harnais en direct optionnelles. La qualité est Beta car la limite est complexe et les discussions archivées montrent toujours une confusion sur l'utilisation, la compaction, `codex/*` par rapport à `openai-codex/*`, et la propriété des outils native-vs-OpenClaw.

## Portée de la catégorie

Inclus dans cette catégorie :

- Native Codex App-server Harness : Couvre le harnais natif Codex App-server sur le chemin d'exécution natif Codex app-server utilisé par les tours d'agent OpenAI lorsque le harnais Codex possède l'identité du thread, la boucle de modèle natif, la compaction, les outils natifs et les contrôles du app-server natif.
- Thread Lifecycle : Couvre le cycle de vie du thread sur le chemin d'exécution natif Codex app-server utilisé par les tours d'agent OpenAI lorsque le harnais Codex possède l'identité du thread, la boucle de modèle natif, la compaction, les outils natifs et les contrôles du app-server natif.

## Fonctionnalités

- Native Codex App-server Harness : Couvre le harnais natif Codex App-server sur le chemin d'exécution natif Codex app-server utilisé par les tours d'agent OpenAI lorsque le harnais Codex possède l'identité du thread, la boucle de modèle natif, la compaction, les outils natifs et les contrôles du app-server natif.
- Thread Lifecycle : Couvre le cycle de vie du thread sur le chemin d'exécution natif Codex app-server utilisé par les tours d'agent OpenAI lorsque le harnais Codex possède l'identité du thread, la boucle de modèle natif, la compaction, les outils natifs et les contrôles du app-server natif.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : Les docs couvrent la configuration, les limites d'exécution, la configuration de référence, les plugins natifs, Computer Use, les approbations, le sandboxing et les diagnostics ; les tests de harnais en direct et Docker E2E couvrent le comportement réel de la passerelle/app-server.
- Signaux négatifs : De nombreuses capacités sont optionnelles, dépendantes du compte ou dépendantes de la version, donc la preuve de version est répartie sur plusieurs voies spécialisées.
- Lacunes d'intégration : Les applications de plugins natifs, les approbations du gardien, l'aperçu du exec-server sandbox et les déploiements du app-server WebSocket distant nécessitent une preuve récurrente de la version actuelle.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : La requête a retourné #85914 sur la création de la récupération d'échec d'appel d'outil en tant que capacité de boucle d'exécution native OpenClaw, qui est adjacente à la limite harnais/outil natif.
- Rapports Discrawl : La discussion du responsable du 2026-04-24 a soutenu que le chemin du app-server Codex n'est pas seulement un autre backend de lancement car il possède l'identité du thread natif, le comportement de reprise/compaction, le compte/modèle/statut, les permissions, les contrôles rapides/arrêt/direction/liaison, la liaison dynamique des outils, la mise en miroir des transcriptions et les diagnostics.
- Bonnes qualités : Les docs sont explicites sur les limites du propriétaire et le comportement de fermeture en cas d'échec ; la source a des surfaces d'extension et de tâche nommées au lieu de ponts ad hoc.
- Mauvaises qualités : Opérationnellement, le harnais exige toujours que les utilisateurs comprennent l'état du app-server, l'état du thread Codex, l'état de la session OpenClaw et la propriété des outils.
- Exclu de la qualité : La couverture des tests du harnais a été considérée uniquement pour la couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Native Codex App-server Harness, Thread Lifecycle.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La dérive de version du app-server natif nécessite une preuve de scorecard de version.
- L'accessibilité des applications de plugins natifs et la politique d'action destructrice sont intentionnellement étroites et peuvent surprendre les opérateurs.
- Les comparaisons d'utilisation entre le chemin du fournisseur OpenAI/Codex et le chemin du harnais natif restent un sujet de support.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness.md` documente la configuration, la sélection d'exécution, les contrôles `/codex`, les modèles de déploiement et la vérification.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness-runtime.md` documente les liaisons de threads, les hooks, les outils, les approbations, la direction des files d'attente, le téléchargement de commentaires, la compaction et les miroirs de transcription.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness-reference.md` documente les champs de configuration du app-server, le transport, les modes d'approbation/sandbox, l'isolation d'authentification et l'exécution native en sandbox.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-native-plugins.md` documente la migration des applications de plugins natifs Codex, l'inventaire des applications, la configuration des applications de threads et la politique d'action destructrice.

### Source

- `/Users/kevinlin/code/openclaw/src/plugins/codex-app-server-extension-types.ts` définit les hooks d'événements d'extension pour les résultats d'outils du app-server Codex.
- `/Users/kevinlin/code/openclaw/src/plugins/codex-app-server-extension-factory.ts` répertorie les usines d'extension du app-server Codex actives.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/codex-native-task-runtime.ts` expose les aides locaux uniquement pour la mise en miroir des sous-agents Codex natifs dans l'état de la tâche OpenClaw.
- `/Users/kevinlin/code/openclaw/src/tasks/codex-native-subagent-task.ts` possède l'identité de la tâche du sous-agent Codex natif et la gestion de l'état obsolète.
- `/Users/kevinlin/code/openclaw/src/commands/codex-runtime-plugin-install.ts` gère l'installation du plugin d'exécution Codex fourni.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/gateway-codex-harness.live.test.ts` contient des sondes de harnais Codex en direct optionnelles pour la passerelle, `/codex status`, les modèles, l'image/image de chat, MCP, le sous-agent, le gardien et les variantes du mode code.
- `/Users/kevinlin/code/openclaw/scripts/e2e/codex-media-path-docker.sh` exécute un E2E Docker du chemin média Codex avec les journaux de la passerelle et du app-server.
- `/Users/kevinlin/code/openclaw/scripts/e2e/codex-on-demand-docker.sh` couvre le comportement du plugin/exécution Codex à la demande.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/system-prompt.test.ts` couvre la préférence des commandes du app-server Codex natif par rapport à ACP lorsqu'elles sont disponibles.
- `/Users/kevinlin/code/openclaw/src/agents/cli-runner.spawn.test.ts` couvre la transmission du système prompt Codex dans l'exécution de type CLI/app-server.
- `/Users/kevinlin/code/openclaw/extensions/openai/openclaw.plugin.test.ts` et les tests de contrat d'enregistrement de plugin couvrent l'enregistrement du plugin OpenAI/Codex.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "codex app-server harness thread compact /codex status native codex"`

Résultats :

- A retourné #85914, une demande de fonctionnalité autour de la récupération d'échec d'appel d'outil de boucle d'exécution native.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "codex app-server harness thread compact /codex status native codex"`

Résultats :

- A retourné le contexte d'examen du responsable du 2026-04-24 expliquant pourquoi le chemin du app-server Codex possède l'identité du thread natif, le comportement de reprise/compaction, le compte/modèle/statut, les permissions, les contrôles, la liaison dynamique des outils et la mise en miroir des transcriptions.
- A retourné la discussion du 2026-04-14 distinguant l'utilisation du fournisseur `openai-codex/*` de l'utilisation du harnais natif `codex/*` et les compromis de compaction.
