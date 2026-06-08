---
title: "Chemin du fournisseur Anthropic - Note de maturité du backend Claude CLI"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Anthropic - Note de maturité du backend Claude CLI

## Résumé

Le runtime Claude CLI est un backend fourni supporté avec documentation, enregistrement de plugin, configuration du pont MCP, paramètres par défaut de session stdio en direct, normalisation du mode de permission, reprise de session et mappage d'effort `/think`. La couverture est Stable car le contrat principal du runtime est documenté et implémenté. La qualité est Alpha car les preuves d'archive montrent des défaillances visibles par l'utilisateur autour de l'enregistrement du backend, de l'exécution de la passerelle systemd/root, des permissions, de la mise en mémoire tampon des flux et de la reprise de session.

## Portée de la catégorie

Cette catégorie couvre le chemin Claude CLI local de l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses paramètres par défaut de commande/args/env, le pont d'outil MCP, le mode d'outil natif, les sessions JSONL stdio en direct, le mappage du mode de permission, les args d'effort de réflexion, la persistance de l'ID de session, la validation de la transcription et le comportement du prélude de secours.

## Fonctionnalités

- Sélection du runtime : couvre la sélection du runtime sur le chemin Claude CLI local de l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses paramètres par défaut de commande/args/env, le pont d'outil MCP, le mode d'outil natif et le comportement du backend claude cli associé.
- Continuité de session : couvre la continuité de session sur le chemin Claude CLI local de l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses paramètres par défaut de commande/args/env, le pont d'outil MCP, le mode d'outil natif et le comportement du backend claude cli associé.
- Pont MCP/outil : couvre le pont MCP/outil sur le chemin Claude CLI local de l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses paramètres par défaut de commande/args/env, le pont d'outil MCP, le mode d'outil natif et le comportement du backend claude cli associé.
- Mappage du mode de permission : couvre le mappage du mode de permission sur le chemin Claude CLI local de l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses paramètres par défaut de commande/args/env, le pont d'outil MCP, le mode d'outil natif et le comportement du backend claude cli associé.
- Prélude de secours : couvre le prélude de secours sur le chemin Claude CLI local de l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses paramètres par défaut de commande/args/env, le pont d'outil MCP, le mode d'outil natif et le comportement du backend claude cli associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : la documentation couvre la configuration de Claude CLI, la configuration, les sessions, les permissions, l'effort de réflexion et le prélude de secours ; la source enregistre un backend complet avec des paramètres par défaut stdio en direct et un pont MCP ; les tests couvrent l'enregistrement du backend et la normalisation de la configuration.
- Signaux négatifs : la couverture Claude CLI en direct est largement indirecte via les définitions de flux de travail d'acceptation de package et les tests de plugin/unité plutôt qu'un seul test de runtime en direct dans cet audit.
- Lacunes d'intégration : les chemins de session de canal et de passerelle daemon/root ont des défaillances archivées qui ne sont pas évidemment couvertes par les tests de backend ciblés.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : #70279 signale que le backend est ignoré sur une passerelle root gérée par systemd ; #85408 signale des drapeaux MCP codés en dur bloquant les MCPs de portée utilisateur ; #85601 signale une course tempDir de configuration MCP fournie ; #86050 signale que la passerelle met en mémoire tampon les événements de flux Claude CLI ; #78828 signale des blocages du mode de permission de la passerelle root.
- Rapports Discrawl : les résultats de l'archive Discord incluent `MissingAgentHarnessError: claude-cli is not registered` dans les chats de groupe tandis que les DM fonctionnaient, plus des conseils montrant une divergence de chemin de configuration sur le routage de session.
- Bonnes qualités : le backend a des args par défaut conservateurs, efface l'env Claude/Anthropic hérité qui pourrait diriger les processus enfants, sérialise les exécutions, valide la reprise de transcription de projet et mappe la politique d'exécution OpenClaw en mode de permission Claude.
- Mauvaises qualités : le chemin dépend de l'installation CLI externe, de la connexion locale, du PATH de l'hôte, des fichiers de transcription de projet locaux, de la recherche de runtime de session/canal et du comportement CLI détenu par le fournisseur.
- Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux de runtime réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/anthropic-provider-path.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la sélection du runtime, la continuité de session, le pont MCP/outil, le mappage du mode de permission, le prélude de secours.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le chemin Claude CLI est opérationnellement sensible à la configuration de l'hôte et au routage de session.
- Les chemins de session de groupe/canal ont montré une divergence de recherche de runtime par rapport aux chemins de session DM/principale.
- Certains correctifs apparaissent comme des PR/problèmes actifs ou récents, donc le registre de support vécu est toujours bruyant.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/gateway/cli-backends.md` documente le backend `claude-cli`, le comportement du pont MCP, le support de session, le mappage de permission natif, le mappage d'effort de réflexion, les prérequis de connexion, la reprise de session et le prélude de secours.
- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente Claude CLI comme le chemin de réutilisation des identifiants locaux de l'hôte et avertit des attentes du même hôte.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md` recommande les références de modèle `anthropic/*` canoniques plus `agentRuntime.id: "claude-cli"` limité au modèle.

### Source

- `/Users/kevinlin/code/openclaw/extensions/anthropic/cli-backend.ts` enregistre `claude-cli` avec `bundleMcp`, pont de fichier de configuration Claude, mode d'outil natif, args json de flux, sessions stdio en direct, args d'image limités à l'espace de travail, IDs de session, resemis de transcription brute, paramètres par défaut de chien de garde et sérialisation.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/cli-shared.ts` efface les variables env Anthropic/Claude héritées, normalise `--setting-sources`, mappe la politique d'exécution OpenClaw en mode de permission Claude et mappe les niveaux de réflexion OpenClaw en `--effort`.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/config-defaults.ts` remplit `agentRuntime.id: "claude-cli"` pour les références Anthropic canoniques sélectionnées lorsque l'authentification Claude CLI est sélectionnée.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-claude-cli.ts` vérifie la résolution de commande, les identifiants, la santé du répertoire d'espace de travail/projet et les agents de runtime Claude CLI actifs.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` vérifie le câblage du flux de travail Anthropic et Claude CLI en direct, y compris `OPENCLAW_LIVE_CLI_BACKEND_MODEL=claude-cli/claude-sonnet-4-6` et l'installation de package de `@anthropic-ai/claude-code`.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker.sh` et `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts` couvrent la notification de canal MCP/encadrement de permission adjacent au mode de canal Claude.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/anthropic/index.test.ts` vérifie l'enregistrement du backend `claude-cli`, les paramètres par défaut de configuration, la migration d'authentification et l'authentification synthétique.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/cli-shared.test.ts` vérifie les args de permission, les sources de paramètres sûrs, le mappage d'effort, la normalisation de configuration et la configuration de resemis de transcription.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-claude-cli.test.ts` couvre les diagnostics du docteur pour le chemin Claude CLI.
- `/Users/kevinlin/code/openclaw/src/plugins/bundle-claude-inspect.test.ts` couvre le comportement d'inspection Claude fourni.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "claude-cli live session resume transcript missing permission mode"`

Résultats :

- Aucun résultat direct pour cette requête combinée exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Claude CLI OpenClaw MCP allowedTools permission-mode"`

Résultats :

- #85408 `openclaw agent CLI spawn hardcodes --strict-mcp-config + --allowedTools mcp__openclaw__*, blocking user-scope MCPs`.
- #85601 `[regression] Bundled MCP config tempDir race still present`.
- #86050 `[Bug]: Gateway buffers claude-cli stream events; surfaces only see the final assembled message`.
- #78828 `Claude CLI on root gateway: inferred bypassPermissions breaks, acceptEdits partly works, blocked turns can stall until timeout`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "claude-cli"`

Résultats :

- Retourné des PR actives/récentes incluant #73122 garde-fous d'enregistrement du backend, #74990 chemin d'abonnement dans l'assistant d'intégration, #85505 mode d'époque d'authentification CLI réservé à l'hôte, #87702 nettoyage de variable env lors du lancement de Claude, #77148 fork de session à la reprise, #86649 deltas de streaming de message partiel et #86568 saut de refroidissement d'authentification pour les fournisseurs CLI.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "Claude CLI OpenClaw auth login claude-cli"`

Résultats :

- Retourné un fil de support du 26 mai 2026 où les DM Discord fonctionnaient mais les chats de groupe échouaient avec `MissingAgentHarnessError: Requested agent harness "claude-cli" is not registered`, plus des entrées d'archive plus anciennes fermant les problèmes de persistance Claude CLI et notant la délégation CLI implémentée.

Requête : `discrawl search --limit 10 "Anthropic usage status Claude API key"`

Résultats :

- Retourné des conseils d'avril 2026 recommandant le chemin de sous-processus CLI pour l'utilisation de l'abonnement Claude et avertissant de la configuration directe de clé API/facturation API.
