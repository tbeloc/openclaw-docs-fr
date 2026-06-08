---
title: "Automatisation des navigateurs et outils exec/sandbox - Note de maturité de l'API Direct Tool Invoke et Node System.run"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation des navigateurs et outils exec/sandbox - Note de maturité de l'API Direct Tool Invoke et Node System.run

## Résumé

L'API d'invocation d'outil directe et le `system.run` des nœuds sont Stables en couverture et Bêta en qualité. Le chemin d'invocation directe HTTP et RPC est documenté, limité par authentification, filtré par politique, conscient des hooks et couvert par des tests. Le `system.run` des nœuds a des exigences explicites d'appairage/administration, une politique d'approbation locale au nœud, une liaison de plan d'approbation et un rejet de dérive. La qualité reste Bêta car le point de terminaison est intentionnellement un accès opérateur complet, la liste de refus strict est critique pour la sécurité, et le `system.run` des nœuds est l'exécution de commandes distantes sur une machine appairée.

## Portée de la catégorie

Cette note couvre HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, sémantique du corps de la requête et de l'authentification, restauration de portée opérateur à secret partagé, filtrage des politiques, hooks avant appel d'outil, liste de refus HTTP, formes de réponse, portées d'appairage de nœuds, relais de commande de nœud, `system.run`, `system.run.prepare`, `system.which`, liaison de plan d'approbation et politique exec nœud-hôte.

## Fonctionnalités

- API Direct Tool Invoke : Couvre l'API Direct Tool Invoke sur HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, sémantique du corps de la requête et de l'authentification, restauration de portée opérateur à secret partagé, et comportement associé de l'API d'invocation d'outil directe et du system.run des nœuds.
- Node System.run : Couvre Node System.run sur HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, sémantique du corps de la requête et de l'authentification, restauration de portée opérateur à secret partagé, et comportement associé de l'API d'invocation d'outil directe et du system.run des nœuds.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - Les docs couvrent l'authentification `/tools/invoke`, la forme de la requête, le comportement de politique/routage, la limite de sécurité, la liste de refus strict, la forme de réponse et la personnalisation.
  - Les docs de protocole couvrent `tools.invoke`, les portées de nœud, les approbations d'appairage de nœud et la liaison d'approbation exec pour `system.run`.
  - La source partage l'invocation HTTP/RPC directe via `invokeGatewayTool`, applique la résolution d'outil limitée à Gateway, exécute les hooks avant appel d'outil et mappe les erreurs.
  - Les tests couvrent l'authentification HTTP, le refus de politique, les entrées de refus strict, le fallback d'outil plugin, l'enveloppe RPC, les charges utiles nécessitant approbation, la liaison d'approbation de nœud et la politique system.run nœud-hôte.
- Signaux négatifs :
  - `/tools/invoke` n'est intentionnellement pas un modèle d'authentification délégué étroit par utilisateur.
  - L'approbation du `system.run` des nœuds et la dérive de la liste d'autorisation ont un historique actuel de problèmes/PR.
- Lacunes d'intégration :
  - Ajouter un smoke direct-invoke qui prouve que chaque outil de refus strict par défaut reste refusé tandis qu'un outil plugin/core à faible risque reste appelable.
  - Ajouter une voie d'intégration nœud-hôte qui prouve que la liaison du plan d'approbation rejette la commande, le répertoire de travail, l'agent et la dérive de session après approbation.

## Score de qualité

- Score : `Beta (79%)`
- Rapports Gitcrawl :
  - `tools invoke system.run approval node invoke` a retourné le problème #77096 sur la confiance du répertoire de travail symlink, PR #80532 pour `allowSymlinkPath`, PR #81827 pour `tools.exec.denyPathPatterns`, PR #78226 pour la réécriture de la liste d'autorisation des nœuds restaurant les approbations exec révoquées, PR #85543 pour le fallback shell des nœuds, PR #70543 pour le mode auto normalisé et PR #81488 pour le renforcement env d'approbation exec des nœuds.
- Rapports Discrawl :
  - `tools invoke system run` a retourné les conseils du 2026-04-27 recommandant `/tools/invoke` pour le fanout n8n vers plusieurs threads Feishu, plus des commentaires d'archive disant que le `nodes invoke system.run` direct est remplacé par `exec host=node` et que le comportement de sortie/approbation de `system.run`/`exec` est sensible à la sécurité.
- Bonnes qualités :
  - L'invocation directe HTTP utilise le chemin d'authentification et de limite de débit Gateway, et l'authentification à secret partagé restaure intentionnellement les valeurs par défaut d'opérateur complet.
  - Les refus stricts HTTP par défaut bloquent exec, shell, mutation de fichier, génération de session, envoi de session, cron, gateway et relais de nœud.
  - RPC `tools.invoke` retourne une enveloppe typée plutôt que de lever une exception via les refus de politique/approbation.
  - L'appairage de nœud nécessite l'administration pour les requêtes `system.run`/`system.which`.
  - Le `system.run` des nœuds approuvé transfère uniquement les champs autorisés et revalide les détails du plan d'approbation.
- Mauvaises qualités :
  - Une identité Gateway bearer valide est un accès propriétaire/opérateur pour ce point de terminaison.
  - La liste de refus strict est un contrôle critique ; le `gateway.tools.allow` personnalisé peut intentionnellement supprimer des entrées.
  - L'exécution de nœud dépend de la confiance du dispositif appairé plus la politique d'approbation locale au nœud, rendant la dérive et les bugs de réécriture à fort impact.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, live et runtime-flow ont affecté la couverture uniquement.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'API Direct Tool Invoke et Node System.run.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'invocation d'outil directe doit rester documentée comme réservée aux opérateurs sauf si OpenClaw ajoute un modèle d'authentification délégué plus étroit.
- La liaison d'approbation du `system.run` des nœuds et l'état de la liste d'autorisation locale au nœud doivent rester sous audit de sécurité actif.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/tools-invoke-http-api.md:9`: la documentation indique que `/tools/invoke` est toujours activé et utilise l'authentification Gateway plus la politique d'outils.
- `/Users/kevinlin/code/openclaw/docs/gateway/tools-invoke-http-api.md:43`: la documentation identifie le point de terminaison comme surface d'accès complet de l'opérateur.
- `/Users/kevinlin/code/openclaw/docs/gateway/tools-invoke-http-api.md:89`: la documentation décrit le comportement de la politique et du routage.
- `/Users/kevinlin/code/openclaw/docs/gateway/tools-invoke-http-api.md:101`: la documentation indique que les approbations d'exécution ne constituent pas une limite d'autorisation distincte pour l'invocation HTTP directe.
- `/Users/kevinlin/code/openclaw/docs/gateway/tools-invoke-http-api.md:107`: la documentation énumère les outils refusés par défaut, notamment exec, shell, mutation de fichiers, sessions, cron, gateway et nodes.
- `/Users/kevinlin/code/openclaw/docs/gateway/operator-scopes.md:99`: l'approbation d'appairage de nœud dérive des portées supplémentaires requises à partir de la liste de commandes.
- `/Users/kevinlin/code/openclaw/docs/gateway/operator-scopes.md:104`: `system.run`, `system.run.prepare` et `system.which` nécessitent l'appairage plus l'administrateur.
- `/Users/kevinlin/code/openclaw/docs/gateway/protocol.md:573`: `tools.invoke` invoque un outil disponible via le même chemin de politique que `/tools/invoke`.
- `/Users/kevinlin/code/openclaw/docs/gateway/protocol.md:627`: les approbations d'exécution pour l'utilisation de nœud utilisent le `systemRunPlan` canonique et rejettent la mutation après approbation.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.ts:17`: le gestionnaire HTTP achemine `/tools/invoke`.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.ts:45`: les commentaires documentent le modèle de confiance d'opérateur complet à secret partagé.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.ts:63`: l'analyse du corps applique une taille maximale du corps.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.ts:77`: l'invocation directe HTTP appelle `invokeGatewayTool` partagé.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/tools-invoke.ts:32`: le gestionnaire RPC `tools.invoke` valide les paramètres et appelle le chemin d'invocation partagé.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-shared.ts:146`: l'invocation partagée résout le nom de l'outil, les arguments, la session, les outils à portée de politique, les hooks et le mappage des erreurs.
- `/Users/kevinlin/code/openclaw/src/gateway/tool-resolution.ts:105`: l'invocation directe HTTP applique la liste de refus dur HTTP Gateway par défaut.
- `/Users/kevinlin/code/openclaw/src/security/dangerous-tools.ts:9`: la liste de refus HTTP par défaut inclut exec, shell, mutation de fichiers, orchestration de session, cron, gateway et nodes.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.ts:190`: le transfert `system.run` du nœud utilise une liste blanche de champs pris en charge.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.ts:214`: les champs de remplacement d'approbation sont acceptés uniquement avec un enregistrement d'approbation réel.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.ts:212`: le node-host envoie les événements exec refusés et les résultats en cas d'échec de la politique.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:440`: la suite de tests d'invocation directe HTTP exerce le comportement HTTP réel.
- `/Users/kevinlin/code/openclaw/src/gateway/operator-approvals-client.e2e.test.ts:1`: la couverture e2e d'approbation d'opérateur existe.
- `/Users/kevinlin/code/openclaw/src/gateway/server.node-invoke-approval-bypass.test.ts:1`: la couverture de régression de contournement d'approbation d'invocation de nœud existe.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:610`: vérifie que les outils refusés/bloqués par profil retournent 404.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:638`: vérifie que HTTP refuse `sessions_spawn` même lorsque la politique d'agent l'autorise.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:853`: vérifie que l'authentification bearer à secret partagé est un accès d'opérateur complet sur `/tools/invoke`.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:924`: vérifie que la liste de refus HTTP s'étend aux outils d'exécution et de fichiers à haut risque.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:966`: vérifie l'enveloppe RPC `tools.invoke`.
- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:996`: vérifie le refus typé d'approbation nécessaire lorsque le hook de politique bloque.
- `/Users/kevinlin/code/openclaw/src/gateway/system-run-approval-binding.test.ts:1`: les tests de liaison d'approbation system.run existent.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.test.ts:1`: les tests d'approbation system.run d'invocation de nœud existent.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.test.ts:1`: les tests system.run du node-host existent.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "tools invoke system.run approval node invoke" --json`

Résultats :

- Problème ouvert #77096 : opt-in symlink cwd pour `system.run` lié à l'approbation.
- PR ouvert #80532 : ajouter la configuration `allowSymlinkPath`.
- PR ouvert #81827 : ajouter `tools.exec.denyPathPatterns`.
- PR ouvert #78226 : la réécriture de la liste blanche de nœud peut restaurer les approbations exec révoquées.
- PR ouvert #85543 : réessayer le secours shell du nœud sur ENOENT.
- PR ouvert #70543 : ajouter le mode auto normalisé.
- PR ouvert #81488 : renforcer l'env de précontrôle d'approbation exec du nœud.

### Requêtes Discrawl

Requête :

`discrawl search --mode fts --limit 5 "tools invoke system run"`

Résultats :

- 2026-04-27 l'archive de support recommande `/tools/invoke` pour le fanout n8n après
  les exécutions de webhook d'analyse uniquement.
- 2026-04-25 les commentaires de l'archive OpenClaw indiquent que les chemins directs `nodes invoke system.run`
  ont été remplacés par `exec host=node` et que l'exécution du shell du nœud achemine
  via exec conscient de l'approbation.
