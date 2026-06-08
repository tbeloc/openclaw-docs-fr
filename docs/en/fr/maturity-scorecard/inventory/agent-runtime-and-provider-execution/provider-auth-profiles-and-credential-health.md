---
title: "Agent Runtime - Provider Auth Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Agent Runtime - Provider Auth Maturity Note

## Résumé

L'authentification des fournisseurs est suffisamment large pour couvrir la configuration, la sélection, les vérifications de santé, le basculement et les diagnostics visibles par l'opérateur dans une seule catégorie. La documentation explique les clés API, OAuth, les basculements fournisseur/profil d'authentification, la sortie de statut et de sonde, la réparation des routes obsolètes et les conseils de redémarrage. La source valide la compatibilité fournisseur/profil, porte l'état des candidats de basculement, classe les défaillances structurées du fournisseur et formate les conseils de récupération pour clé manquante, actualisation OAuth, capacité et redémarrage. La qualité reste Alpha car les preuves d'archive montrent toujours des défaillances répétées de l'opérateur autour de la réparation de la route OAuth Codex, de la propagation des profils, de la sémantique du basculement de quota, de l'état de basculement collant et de la découverte de clé de fournisseur.

## Portée de la catégorie

Cette catégorie couvre les identifiants de fournisseur, la santé du profil d'authentification et le comportement de récupération du fournisseur visible par l'opérateur : flux de connexion et de collage de clé, sélection du profil d'authentification du fournisseur, réparation du docteur et du statut, basculement d'authentification, chaînes de basculement du fournisseur, récupération de quota et de capacité, conseils de clé manquante et OAuth, conseils de redémarrage et de route obsolète, diagnostics structurés, propagation des identifiants du sous-agent et erreurs d'exécution liées aux identifiants.

## Fonctionnalités

- Configuration de connexion et de clé API : flux de connexion, OAuth et collage de clé pour l'accès au fournisseur.
- Sélection du profil d'authentification : sélection et validation des profils d'authentification du fournisseur.
- Vérifications de santé des identifiants : vérifications de santé des identifiants du docteur, du statut et des signaux de réparation associés.
- Basculement d'authentification : comportement de basculement d'authentification du même fournisseur et entre profils.
- Récupération du basculement du fournisseur : comportement de basculement du fournisseur et du profil d'authentification en cas d'échec de l'exécution.
- Récupération de limite de débit et de capacité : chemins de récupération pour les défaillances de quota, de capacité et de limite de débit.
- Conseils de clé manquante et OAuth : conseils de l'opérateur pour les clés manquantes, l'état OAuth expiré et les défaillances d'authentification associées.
- Récupération de redémarrage et de route obsolète : récupération de l'état de route obsolète, des exigences de redémarrage et de la dérive de fournisseur associée.
- Diagnostics structurés du fournisseur : erreurs et diagnostics structurés du fournisseur livrés dans les journaux ou les réponses de l'agent.
- Propagation des identifiants du sous-agent : propagation des identifiants du fournisseur dans les flux d'exécution du sous-agent et délégués.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`

La couverture est forte pour OpenAI/Codex, Anthropic, Google, les commandes de modèle, l'état de basculement et la copie de récupération visible par l'opérateur, mais l'authentification du fournisseur et les diagnostics couvrent toujours de nombreux flux et ne sont pas encore représentés par une seule matrice de preuve opérateur de bout en bout.

## Score de qualité

- Score : `Alpha (66%)`

Le comportement d'authentification/profil reste un point de douleur opérationnel fréquent, en particulier lorsque OAuth Codex, les routes API OpenAI directes, la compaction, les sous-agents, la réparation du docteur et le comportement de basculement de quota se chevauchent.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/agent-runtime-and-provider-execution.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration de connexion et de clé API, la sélection du profil d'authentification, les vérifications de santé des identifiants, le basculement d'authentification, la récupération du basculement du fournisseur, la récupération de limite de débit et de capacité, les conseils de clé manquante et OAuth, la récupération de redémarrage et de route obsolète, les diagnostics structurés du fournisseur, la propagation des identifiants du sous-agent.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La réparation de la route OAuth Codex produit toujours des rapports GitHub et Discord ouverts récents.
- Les flux de sous-agent et de compaction peuvent perdre ou réinterpréter l'état du profil d'authentification.
- Les défaillances du fournisseur à l'échelle du quota et spécifiques au compte ont besoin d'une sémantique de basculement plus claire.
- La récupération de l'état de route `openai-codex` obsolète dépend toujours de la réparation du docteur et des conseils explicites.
- Certains diagnostics de clé manquante et de basculement sont forts dans les tests mais toujours trop difficiles pour que les opérateurs les mappent à la cause racine.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/cli/models.md` documente l'aperçu du statut/authentification du modèle, le dépannage OAuth Codex, l'énumération des profils d'authentification, la connexion, le collage de clé API, OpenAI API par rapport à ChatGPT/OAuth, et les notes CLI Claude.
- `/Users/kevinlin/code/openclaw/docs/concepts/models.md` documente la sélection du modèle principal, les secours, le basculement d'authentification du fournisseur, les sélections de secours automatiques, les sélections strictes de l'utilisateur, et le changement de modèle en direct.
- `/Users/kevinlin/code/openclaw/docs/cli/agent.md` documente le comportement de secours de la passerelle, les métadonnées de secours intégrées, le délai d'expiration de la passerelle, l'ID de session/exécution de secours, et `chat.abort` SIGTERM/SIGINT.
- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente `openai`, `openai-codex`, la dénomination du plugin Codex et `agentRuntime`, la sélection de route OpenAI/Codex, la configuration OAuth Codex, et le comportement de réparation du docteur.
- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente l'authentification par clé API par rapport à CLI Claude et les références Anthropic canoniques avec `agentRuntime.id: "claude-cli"`.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md` documente l'authentification du plugin Google, la configuration OAuth CLI Gemini, et le comportement d'avertissement/alias.
- `/Users/kevinlin/code/openclaw/docs/tools/subagents.md` documente la résolution d'authentification du sous-agent par ID d'agent et le secours aux profils principaux.

## Source

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/model-selection.ts` valide les remplacements de profil d'authentification par rapport aux fournisseurs d'authentification acceptés, efface les remplacements invalides, et gère l'état hérité obsolète `openai-codex`.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` porte l'état du profil d'authentification du candidat de secours, applique les modifications d'authentification du changement de modèle en direct, préserve le secours d'authentification du même fournisseur, et supprime les ID de profil d'authentification lors du changement de fournisseur.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-codex-responses.ts` classe les erreurs réessayables et configure le comportement de délai d'expiration/nouvelle tentative pour le transport Codex Responses.
- `/Users/kevinlin/code/openclaw/src/agents/transport-stream-shared.ts` construit des flux d'échec structurés avec les détails d'erreur.
- `/Users/kevinlin/code/openclaw/src/commands/auth-choice.apply.api-providers.test.ts` mappe les choix de fournisseur de clé API/jeton pour les flux d'authentification.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre la présentation du statut/authentification du catalogue pour les fournisseurs.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` couvre les conseils d'échec d'actualisation OAuth, les conseils de clé API manquante, les échecs de clé manquante `openai-codex` obsolète pointant vers la réparation du docteur, l'état du profil d'authentification lors des nouvelles tentatives, le suppression du profil d'authentification lors du changement de fournisseur, et le secours d'authentification du même fournisseur.
- `/Users/kevinlin/code/openclaw/src/commands/models.set.e2e.test.ts` couvre la normalisation du secours dans le comportement de la commande de modèle.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/auth-choice.apply.api-providers.test.ts` couvre le mappage des choix d'authentification pour les fournisseurs de clé API/jeton.
- `/Users/kevinlin/code/openclaw/src/commands/models.auth.provider-resolution.test.ts` couvre la résolution d'authentification du fournisseur pour les commandes de modèle.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` inclut une couverture de régression du profil d'authentification ciblée.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-codex-responses.test.ts` couvre les délais d'expiration du transport et le comportement websocket/SSE alimentant les décisions de nouvelle tentative.
- `/Users/kevinlin/code/openclaw/src/agents/transport-stream-shared.test.ts` couvre le nettoyage des échecs et les flux d'échec non vides.

## Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "No API key found provider openai-codex auth profile"` a retourné de nombreux problèmes actifs, notamment #84252 sur le docteur/statut laissant le side-car d'authentification OAuth `openai-codex` partiellement réparé, #87677 sur les intégrations de mémoire via le runtime OAuth Codex, #86470 sur le docteur réécrivant `openai-codex/*` en `openai/*`, #85797 sur la génération d'images nécessitant une clé API malgré OAuth, #86820 sur la compaction se repliant sur l'API OpenAI directe, #87051 sur le profil OAuth ne se propageant pas aux sessions du sous-agent, #83223 sur les routes migrées recherchant toujours l'authentification `openai-codex` avant le secours, et #80171 sur la parité du runtime QA.
- `gitcrawl --json search issues -R openclaw/openclaw "openai-codex Anthropic Google provider tool call"` a retourné #80667 sur `trajectory.jsonl` manquant pour les sessions pures `claude-cli` et #78196 sur le comportement du chargeur de plugin d'extension.
- `gitcrawl --json search issues -R openclaw/openclaw "provider error guidance reauth fallback"` n'a retourné aucune correspondance directe.
- `gitcrawl --json search issues -R openclaw/openclaw "rate limit fallback usage limit openai-codex"` a retourné #85103 sur la chaîne de secours du modèle ne se déclenchant pas pour l'épuisement du quota à l'échelle du fournisseur, #87467 sur le secours automatique du taux limite restant épinglé au secours après la récupération primaire, #79604 sur la rotation des profils d'authentification au sein d'un candidat avant le fournisseur suivant, et #79611 sur le basculement du fournisseur du plugin de mémoire active et le délai d'expiration.
- `gitcrawl --json search prs -R openclaw/openclaw "provider error descriptors fallback rate limit"` a retourné #86642 ajoutant des descripteurs d'erreur de fournisseur structurés.
- `gitcrawl --json search prs -R openclaw/openclaw "agent runner fallback model switch"` a retourné des PR incluant #85235 sur les diagnostiques message-tool-only, #80482 sur les échecs de facturation de clé API en ligne de refroidissement, #62682 sur l'abandon terminal par rapport aux échecs réessayables, et #86089 sur les réponses de récupération de redémarrage.

## Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "No API key found provider openai-codex"` a retourné des rapports de mai 2026 autour du routage OAuth/Codex OpenAI, des erreurs de plugin avec `No API key found for provider "openai-codex"`, l'authentification Codex existante n'étant plus reconnue après la reconstruction, les échecs de routage API directs, et les utilisateurs voyant des clés OpenAI manquantes malgré OAuth Codex.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "reauth provider auth profile"` a retourné des rapports d'actualisation/persistance d'authentification Codex, des problèmes de portée, un ordre d'authentification obsolète, des échecs de rotation de jeton, et une confusion de commande reauth plus ancienne.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "openai-codex provider routing"` a retourné des notes de mainteneur/utilisateur sur la résolution du profil d'authentification, le routage de compaction, la configuration du contexte, l'ordre d'authentification, l'état de route obsolète, et les conseils de réparation du docteur.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "usage limit fallback openai-codex"` a retourné des discussions sur le secours de facturation/utilisation CLI Claude perdant le contexte, le basculement OAuth Codex multi-compte, les conseils d'authentification/fournisseur de limite de taux OpenAI, les chemins de limite/défi du backend Codex, les erreurs de limite de taux/ID de compte, les configurations de secours, et le basculement de modèle étant bloqué ou collant.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "model fallback decision"` a retourné des journaux de décision de secours récents pour les délais d'expiration openai-codex, les cas sans clé API, les délais d'expiration OpenRouter, les erreurs de porteur manquant, les réponses vides Anthropic, et les boucles de réparation de session.
