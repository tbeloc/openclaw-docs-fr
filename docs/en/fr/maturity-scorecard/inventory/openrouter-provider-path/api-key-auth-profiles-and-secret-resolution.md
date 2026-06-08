---
title: "Chemin du fournisseur OpenRouter - Note de maturité des profils d'authentification et des identifiants"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenRouter - Note de maturité des profils d'authentification et des identifiants

## Résumé

L'authentification par clé API OpenRouter est explicitement modélisée via les choix d'authentification, `OPENROUTER_API_KEY`, les profils d'authentification `openrouter:default`, la sortie de statut/sonde et les méthodes d'état d'authentification de la passerelle. La couverture est Beta car les surfaces d'authentification disposent de preuves unitaires et de commandes étendues, mais la preuve de version est fragmentée entre les chemins de commande, de passerelle et d'exécuteur. La qualité est Alpha car les archives GitHub et Discord montrent une confusion répétée des utilisateurs réels autour de `401 Missing Authentication header`, de l'inadéquation env/profil, de l'héritage de l'environnement de service et de la sélection de clé d'entrée de fournisseur.

## Portée de la catégorie

Cette catégorie couvre la découverte de `OPENROUTER_API_KEY`, le stockage d'intégration/choix d'authentification, `auth-profiles.json`, la visibilité de statut/sonde, la résolution de clé API du fournisseur, la gestion des secrets d'entrée de fournisseur, le comportement de l'environnement de la passerelle et les méthodes de suppression/statut d'authentification.

## Fonctionnalités

- OPENROUTER_API_KEY : Couvre OPENROUTER_API_KEY dans la découverte de `OPENROUTER_API_KEY`, le stockage d'intégration/choix d'authentification, `auth-profiles.json`, la visibilité de statut/sonde et le comportement associé des identifiants et profils d'authentification.
- Profils d'authentification et ordre d'authentification : Couvre les profils d'authentification et l'ordre d'authentification dans la découverte de `OPENROUTER_API_KEY`, le stockage d'intégration/choix d'authentification, `auth-profiles.json`, la visibilité de statut/sonde et le comportement associé des identifiants et profils d'authentification.
- Statut/sonde et suppression : Couvre le statut/sonde et la suppression dans la découverte de `OPENROUTER_API_KEY`, le stockage d'intégration/choix d'authentification, `auth-profiles.json`, la visibilité de statut/sonde et le comportement associé des identifiants et profils d'authentification.
- Résolution SecretRef/clé API d'entrée de fournisseur : Couvre la résolution SecretRef/clé API d'entrée de fournisseur dans la découverte de `OPENROUTER_API_KEY`, le stockage d'intégration/choix d'authentification, `auth-profiles.json`, la visibilité de statut/sonde et le comportement associé des identifiants et profils d'authentification.
- Héritage env de la passerelle : Couvre l'héritage env de la passerelle dans la découverte de `OPENROUTER_API_KEY`, le stockage d'intégration/choix d'authentification, `auth-profiles.json`, la visibilité de statut/sonde et le comportement associé des identifiants et profils d'authentification.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : Les tests de choix d'authentification couvrent les invites de clé API OpenRouter, la réutilisation d'env, les écritures de profil, le comportement du modèle par défaut et la préservation du défaut existant. Les tests de statut de passerelle couvrent la suppression de profil d'authentification et les marqueurs d'env OpenRouter.
- Signaux négatifs : La couverture est répartie entre l'infrastructure générique d'authentification de fournisseur et les métadonnées du plugin OpenRouter ; il n'y a pas un seul test d'intégration toujours actif pour la création de profil d'authentification, le redémarrage de la passerelle, le statut/sonde et une véritable complétion OpenRouter.
- Lacunes d'intégration : Ajouter une fumée au niveau de la passerelle qui écrit `openrouter:default`, redémarre la passerelle, sonde `openrouter/auto` et vérifie le chemin d'en-tête Authorization sortant.

## Score de qualité

- Score : `Alpha (64%)`
- Rapports Gitcrawl : La requête OpenRouter large a retourné #67423, où le routage d'authentification ignore le champ `apiKey` d'une entrée de fournisseur et se résout via l'ID de fournisseur canonique, plus les rapports de configuration/exécution associés.
- Rapports Discrawl : La recherche Discord a trouvé des rapports d'assistance d'avril 2026 où OpenClaw a vu `OPENROUTER_API_KEY` et/ou `openrouter:default`, mais les utilisateurs ont toujours rencontré `401 Missing Authentication header` ou ont dû raisonner sur le fait que le service de passerelle héritait de l'env shell.
- Bonnes qualités : La documentation explique la forme de profil d'authentification canonique et `OPENROUTER_API_KEY` ; les tests de commande préservent les défauts existants et évitent de remplacer la configuration du modèle lors de la réauthentification.
- Mauvaises qualités : Les rapports d'assistance réels montrent que la sortie de statut/sonde peut prouver la visibilité du profil tandis que la demande d'exécution échoue toujours, ce qui est une expérience opérateur à friction élevée.
- Exclu de la qualité : L'étendue des tests d'authentification et la couverture des tests de sonde sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openrouter-provider-path.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour OPENROUTER_API_KEY, Profils d'authentification et ordre d'authentification, Statut/sonde et suppression, Résolution SecretRef/clé API d'entrée de fournisseur, Héritage env de passerelle.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La documentation de l'opérateur oblige toujours les utilisateurs à comprendre l'env shell par rapport à l'env du processus de passerelle lorsque l'authentification OpenRouter échoue.
- Le routage de clé API d'entrée de fournisseur et le routage de profil d'authentification peuvent diverger pour les entrées de fournisseur divisées.
- La sortie de statut/sonde peut être techniquement correcte mais insuffisante pour prouver le chemin de demande exact utilisé par l'exécution défaillante.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente `OPENROUTER_API_KEY`, `openclaw onboard --auth-choice openrouter-api-key` et la sémantique du jeton porteur.
- `/Users/kevinlin/code/openclaw/docs/gateway/authentication.md` documente les profils d'authentification, les clés API du fournisseur, les contraintes SecretRef, `OPENROUTER_API_KEY`, la migration de profil plat hérité, le comportement de statut/sonde, l'ordre d'authentification et la suppression d'authentification.
- `/Users/kevinlin/code/openclaw/docs/help/environment.md` affiche `OPENROUTER_API_KEY` dans les exemples de variables d'environnement.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md` explique que les sondes de balayage OpenRouter nécessitent une clé OpenRouter à partir de profils d'authentification ou `OPENROUTER_API_KEY`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts` enregistre la méthode d'authentification par clé API OpenRouter avec l'ID de fournisseur `openrouter`, la variable d'env `OPENROUTER_API_KEY`, le modèle par défaut `openrouter/auto` et le fournisseur attendu `openrouter`.
- `/Users/kevinlin/code/openclaw/src/llm/env-api-keys.ts` mappe l'ID de fournisseur `openrouter` à `OPENROUTER_API_KEY`.
- `/Users/kevinlin/code/openclaw/src/agents/auth-profiles/*` implémente le stockage de profil d'authentification, l'ordre, l'état et la résolution des identifiants utilisés par OpenRouter.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/models-auth-status.ts` expose le comportement de statut d'authentification et de suppression de profil côté passerelle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre le comportement de liste/statut de modèle au niveau de la commande qui inclut l'authentification du fournisseur et les références natives OpenRouter.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.e2e.test.ts` vérifie que les exécutions OpenRouter intégrées entrent dans la résolution de modèle avec le fournisseur/modèle attendu.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/models-auth-status.test.ts` couvre la suppression de profil d'authentification et l'invalidation du cache via les méthodes de serveur de passerelle.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/auth-choice.test.ts` vérifie le choix d'authentification OpenRouter, `OPENROUTER_API_KEY`, la réutilisation d'env, `openrouter:default` et le comportement de préservation du modèle par défaut.
- `/Users/kevinlin/code/openclaw/src/agents/agent-auth-json.test.ts` couvre l'analyse et les mises à jour du profil de clé API `openrouter:default`.
- `/Users/kevinlin/code/openclaw/src/agents/auth-profiles/usage.test.ts` couvre l'état d'utilisation du profil OpenRouter, y compris la gestion des marqueurs de refroidissement.
- `/Users/kevinlin/code/openclaw/src/secrets/provider-env-vars.test.ts` couvre l'enregistrement des variables d'env du fournisseur y compris `OPENROUTER_API_KEY`.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OPENROUTER_API_KEY auth profile openrouter No API key"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter"`

Résultats :

- A retourné #67423 sur l'inadéquation du routeur d'authentification/clé d'entrée de fournisseur, #73496 dans le cluster de configuration/exécution et des rapports de configuration/exécution OpenRouter supplémentaires.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OPENROUTER_API_KEY auth profile"`

Résultats :

- A trouvé des rapports d'assistance d'avril 2026 montrant `OPENROUTER_API_KEY` présent dans l'env et `openrouter:default` présent dans `auth-profiles.json`, tandis que les utilisateurs voyaient toujours `401 Missing Authentication header`, des tours OpenRouter vides ou devaient déplacer la clé dans l'environnement hôte de la passerelle.
- A trouvé des extraits de statut/sonde où les sondes OpenRouter ont réussi mais l'état du modèle par défaut, l'héritage d'env ou les réponses d'exécution restaient confus.
