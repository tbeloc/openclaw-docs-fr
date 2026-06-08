---
title: "Sécurité, authentification, appairage et secrets - Profils d'authentification des fournisseurs et note de maturité de la santé des clés API"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Profils d'authentification des fournisseurs et note de maturité de la santé des clés API

## Résumé

OpenClaw expose une surface d'authentification des fournisseurs mature couvrant OAuth, les clés API, les profils d'authentification, l'ordre d'authentification, les sondes, le statut et la réparation du docteur. La couverture est Beta car de nombreux flux d'authentification des fournisseurs sont testés, y compris la rotation des credentials de bout en bout, mais le parcours complet de l'opérateur couvrant la connexion, le statut, la compaction, les sous-agents et les solutions de secours spécifiques aux fournisseurs est encore fragmenté. La qualité est Alpha car les archives GitHub et Discord actuelles montrent de nombreuses défaillances actives de routage OAuth/clé API `openai-codex` et un comportement confus de réparation du statut/docteur.

## Portée de la catégorie

Cette catégorie couvre les credentials des fournisseurs et la santé de l'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification, sortie du statut/sonde du modèle, solution de secours du fournisseur, suppression des credentials, propagation des credentials des sous-agents et conseils de réparation des clés manquantes destinés aux utilisateurs.

## Fonctionnalités

- Profils d'authentification des fournisseurs : Couvre les profils d'authentification des fournisseurs couvrant les credentials des fournisseurs et la santé de l'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportement connexe des profils d'authentification des fournisseurs et de la santé des clés API.
- Santé des clés API : Couvre la santé des clés API couvrant les credentials des fournisseurs et la santé de l'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportement connexe des profils d'authentification des fournisseurs et de la santé des clés API.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation d'authentification des fournisseurs est extensive ; le runtime du profil d'authentification, l'actualisation OAuth, l'ordre d'authentification, l'état du profil, le choix d'authentification, le statut/sonde et la rotation des credentials ont des tests larges.
- Signaux négatifs : La couverture est répartie sur des fichiers spécifiques aux fournisseurs et au runtime. OAuth OpenAI/Codex bénéficie d'une attention particulière, mais la preuve de version multi-fournisseurs est inégale et l'authentification des fournisseurs de longue traîne dépend des manifestes de plugins.
- Lacunes d'intégration : Ajouter une matrice de scénarios de version pour la connexion, le collage de clé, l'actualisation OAuth, le statut/sonde, la compaction, les sous-agents, la suppression des credentials et la solution de secours du fournisseur couvrant OpenAI/Codex, Anthropic, Google, OpenRouter et au moins un fournisseur de plugin.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : La requête de problème exacte a retourné de nombreuses défaillances actives du profil d'authentification, y compris #84252, #87677, #85797, #86820, #75739, #86470, #76690, #87051, #83223 et le suivi de parité runtime connexe.
- Rapports Discrawl : La recherche Discord a trouvé des rapports d'utilisateurs répétés où OAuth Codex semble valide mais le runtime échoue toujours avec `No API key found`, le statut/sonde donne une sortie contradictoire, la compaction perd le routage OAuth et les utilisateurs ont besoin d'une réparation manuelle du profil/config.
- Bonnes qualités : La documentation distingue l'authentification de la passerelle de l'authentification du fournisseur, définit la forme canonique du magasin de credentials, documente les contraintes SecretRef, fournit des vérifications de sonde/statut et explique le comportement de suppression de l'authentification du fournisseur.
- Mauvaises qualités : Les rapports actifs montrent que le nommage des routes, l'ordre d'authentification, la propagation des sous-agents, la compaction et la dérive du chemin de génération d'images cassent toujours les utilisateurs réels de manière confuse.
- Exclu de la qualité : La largeur de couverture, la largeur des tests unitaires et la profondeur des tests d'intégration ne sont notées que sous Couverture.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les profils d'authentification des fournisseurs et la santé des clés API.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuve` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La réparation de la route OAuth Codex et la migration des alias des fournisseurs produisent toujours des problèmes actifs.
- L'état du profil d'authentification peut être perdu ou mal interprété dans les sous-agents, la compaction et les chemins de capacité spécifiques aux fournisseurs.
- La sortie du statut et de la sonde peut être techniquement précise mais toujours confuse lorsque les chemins de métadonnées et de credentials runtime ne sont pas d'accord.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/authentication.md` documente les clés API des fournisseurs, OAuth, `auth-profiles.json`, les contraintes SecretRef, le comportement du statut/sonde, l'ordre d'authentification, l'épinglage de session et la suppression de l'authentification.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md` documente les flux d'authentification et de statut du modèle.
- `/Users/kevinlin/code/openclaw/docs/providers/openai.md`, `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` et `/Users/kevinlin/code/openclaw/docs/providers/google.md` documentent la configuration représentative du fournisseur.
- `/Users/kevinlin/code/openclaw/docs/concepts/oauth.md` documente la sémantique du stockage et du flux OAuth.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/auth-profiles.runtime.ts` et `/Users/kevinlin/code/openclaw/src/agents/auth-profiles/*` implémentent le stockage du profil d'authentification, l'actualisation OAuth, l'ordre, l'état et la résolution des credentials.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-auth-profile.ts` et `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` transportent l'état du profil d'authentification sélectionné dans l'exécution du runtime.
- `/Users/kevinlin/code/openclaw/src/commands/models/list.status.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/models-auth-status.ts` exposent le statut d'authentification via les méthodes CLI et Gateway.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-auth-profile-config.ts` répare la configuration du profil d'authentification héritée ou obsolète.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.run-embedded-agent.auth-profile-rotation.e2e.test.ts` couvre la rotation du profil d'authentification dans les exécutions d'agents intégrés.
- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre la présentation de la liste/statut du modèle via les flux CLI.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` couvre les conseils de clé manquante, les défaillances `openai-codex` obsolètes, les tentatives et l'état de solution de secours du profil d'authentification.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/auth-profile-runtime-contract.test.ts` couvre les contrats du profil d'authentification du serveur d'application Codex.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/auth-profiles/*.test.ts` couvre l'actualisation OAuth, l'ordre, les remplacements de session, l'observation d'état, la portabilité et le comportement du magasin de profils.
- `/Users/kevinlin/code/openclaw/src/commands/models.auth.provider-resolution.test.ts` couvre la résolution de l'authentification du fournisseur pour les commandes de modèle.
- `/Users/kevinlin/code/openclaw/src/commands/auth-choice.apply.api-providers.test.ts` couvre le mappage du choix d'authentification du fournisseur.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/models-auth-status.test.ts` couvre les méthodes d'authentification du statut de la passerelle.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "No API key found openai-codex auth profile OAuth"`

Résultats :

- A retourné les problèmes actifs #84252, #87677, #85797, #86820, #75739, #86470, #76690, #87051, #84110, #77467, #59405, #86567, #83223 et #80171.
- Les résultats se regroupent autour de la réparation OAuth Codex, des embeddings de mémoire, de la génération d'images, de la solution de secours de compaction, de la propagation du profil d'authentification aux sous-agents, de la recherche de route migrée et de la parité du runtime.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "No API key found openai-codex auth profile OAuth"`

Résultats :

- A trouvé des rapports d'assistance d'avril 2026 où les utilisateurs ont terminé l'intégration OAuth mais les exécutions d'agents ont toujours échoué avec `No API key found`, le statut/sonde affichait un état d'authentification contradictoire et les mainteneurs ont identifié des régressions de version autour de l'authentification du fournisseur `openai-codex`.
- A trouvé des conseils de configuration plus anciens nécessitant des métadonnées et une connexion explicites du profil d'authentification `openai-codex:default`.
