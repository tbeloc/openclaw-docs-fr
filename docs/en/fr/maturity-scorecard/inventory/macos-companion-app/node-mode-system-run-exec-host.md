---
title: "Application compagne macOS - Note de Maturité des Capacités Natives"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne macOS - Note de Maturité des Capacités Natives

## Résumé

Le runtime du nœud d'application macOS est large : il annonce les commandes Canvas, A2UI, screen, system, notification, camera, browser et location, se connecte à Gateway en tant que nœud, et achemine `system.run` via la politique d'approbation détenue par l'application et l'IPC local. La couverture est Alpha car le chemin de commande/runtime est implémenté avec une preuve ciblée, mais la source actuelle manque toujours de `system.run.prepare` dans la liste des commandes du nœud macOS tandis que les chemins nœud-hôte principaux l'attendent pour les flux d'exécution préparés. La qualité est Alpha en raison des preuves d'archive actives autour du support de préparation manquant, du flottement des nœuds, des incompatibilités de liste blanche et de l'UX d'approbation d'exécution.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Connexion de session du nœud Mac : Connexion de session du nœud Mac, annonce de capacité et de commande
- system.run : system.run, system.which, system.notify, approbations d'exécution get/set
- Politique d'approbation d'exécution : Politique d'approbation d'exécution, hôte d'exécution d'application, socket local et émission d'événement
- Demandes de permission : Demandes de permission, interrogation de statut, interface utilisateur des paramètres et annonce de permission du nœud
- Persistance TCC : Persistance TCC, exigences de signature et conseils de permission sécurisée détenue par l'application

## Fonctionnalités

- Connexion de session du nœud Mac : Connexion de session du nœud Mac, annonce de capacité et de commande
- system.run : system.run, system.which, system.notify, approbations d'exécution get/set
- Politique d'approbation d'exécution : Politique d'approbation d'exécution, hôte d'exécution d'application, socket local et émission d'événement
- Demandes de permission : Demandes de permission, interrogation de statut, interface utilisateur des paramètres et annonce de permission du nœud
- Persistance TCC : Persistance TCC, exigences de signature et conseils de permission sécurisée détenue par l'application

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (66%)`
- Signaux positifs : Les tests Swift couvrent l'annonce de commande, les chemins de refus/événement `system.run`, le rejet de remplacement d'env, `system.which`, le contrôle d'accès screen/camera, l'authentification socket d'approbations d'exécution/gardes de chemin, et le comportement d'invite d'approbation. Les tests TypeScript couvrent la planification `system.run` nœud-hôte et le comportement de secours exec-host d'application.
- Signaux négatifs : La liste de commandes natives inclut `system.run` mais pas `system.run.prepare`, tandis que la source principale a un traitement explicite de `system.run.prepare` pour les phases d'exécution de nœud préparées. Aucun scénario en direct ne prouve qu'un agent réel invoque `system.run` via le chemin d'application macOS de bout en bout.
- Lacunes d'intégration : Besoin d'un scénario `system.run` d'application-nœud en direct qui exerce la préparation, l'invite d'approbation, l'autorisation unique, l'autorisation permanente, le refus, l'émission d'événement, la troncature de sortie et le secours en cas d'échec.

## Score de Qualité

- Score : `Alpha (60%)`
- Rapports Gitcrawl : Les résultats incluent le problème #83958 pour le flottement du nœud d'application macOS et les délais d'expiration des invocations Gateway, le problème #9876 demandant plus de contexte dans les fenêtres contextuelles d'approbation d'exécution, le problème #44749 pour la course de dernière écriture gagnante d'autorisation permanente, et plusieurs PR d'approbation d'exécution. Une recherche/inspection de source plus large a trouvé des suivi ouverts `system.run.prepare` (#37591/#38781) mirrorés dans discrawl.
- Rapports Discrawl : L'archive Discord inclut la fermeture #49031 disant que l'ancien rapport manquant `system.run.prepare` a été remplacé mais la lacune restante est suivie par #37591/#38781 ; elle inclut également le commentaire #37591 disant que le main actuel manque toujours de support macOS `system.run.prepare`.
- Bonnes qualités : L'implémentation valide les formes de commande, filtre les remplacements d'env risqués, stocke la politique par agent, supporte les modes ask/allowlist/full, protège l'IPC socket avec des concepts de token/HMAC/TTL, et émet des événements d'exécution.
- Mauvaises qualités : L'incompatibilité du contrat d'exécution préparé est un risque produit sérieux. Les approbations d'exécution ont également des problèmes connus d'UX/contexte et de cohérence de liste blanche, et le flottement d'application-nœud peut rendre la politique correcte inaccessible.
- Exclu de la qualité : La couverture de test unitaire, intégration, e2e, en direct et de flux runtime réel n'a pas été utilisée pour augmenter ou diminuer la Qualité.

## Score de Complétude

- Score : `Alpha (66%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour la connexion de session du nœud Mac, system.run, la politique d'approbation d'exécution, les demandes de permission, la persistance TCC.
- Signaux négatifs : la note archivée a précédé la notation de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter et prouver le support du nœud macOS pour `system.run.prepare` ou mettre à jour le contrat exec-host principal afin que le nœud d'application ne soit pas censé l'implémenter.
- Prouver `system.run` en direct via une application signée empaquetée avec invite d'approbation et retour de sortie.
- Améliorer le contexte d'invite pour la session/demandeur et réconcilier le comportement de concurrence d'autorisation permanente.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` documente les capacités du nœud, `system.run`, la carte de permission et les approbations d'exécution stockées sous `~/.openclaw/exec-approvals.json`.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/xpc.md` documente le modèle IPC Gateway/nœud/application pour les approbations d'exécution et `system.run`.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/permissions.md` explique pourquoi le contexte TCC détenu par l'application est important pour le travail privilégié.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/NodeMode/MacNodeModeCoordinator.swift` construit les caps/commandes du nœud et démarre la session du nœud Gateway.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/NodeMode/MacNodeRuntime.swift` distribue les invocations du nœud, y compris `system.run`, `system.which`, `system.notify` et les approbations d'exécution get/set.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ExecApprovals.swift` définit le fichier d'approbation local, les valeurs par défaut, les entrées de liste blanche, le chemin du socket et le stockage de politique.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ExecApprovalEvaluation.swift` résout la sécurité, le mode ask, l'assainissement d'env, les correspondances de liste blanche et l'autorisation automatique de compétence.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.ts` préfère l'hôte exec d'application mac quand configuré et refuse avec `COMPANION_APP_UNAVAILABLE` si requis mais inaccessible.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke.ts` et `/Users/kevinlin/code/openclaw/src/infra/node-commands.ts` incluent `system.run.prepare`, mais l'énumération de commande Swift macOS/l'annonce ne le fait pas.

### Tests d'intégration

- Aucun scénario d'intégration `system.run` d'application-nœud macOS en direct n'a été trouvé.
- `/Users/kevinlin/code/openclaw/test/fixtures/system-run-approval-binding-contract.json` et les tests TS node-host exercent la planification `system.run` principale, pas l'application empaquetée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/MacNodeRuntimeTests.swift` couvre le comportement de commande d'invocation du nœud, les événements de refus `system.run`, le rejet de remplacement d'env, le contrôle d'accès screen/camera et l'actualisation de l'hôte A2UI.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/MacNodeModeCoordinatorTests.swift` couvre l'annonce de commande et les différences de capacité distante/locale.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/ExecApprovalsSocketAuthTests.swift`, `ExecApprovalsSocketPathGuardTests.swift`, `ExecHostRequestEvaluatorTests.swift`, `ExecAllowlistTests.swift` et `ExecApprovalPromptLayoutTests.swift` couvrent l'infrastructure d'approbation.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.test.ts` couvre la sémantique d'exécution préparé principal et de secours exec-host d'application.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS system.run exec approval node host" --json`

Résultats :

- Problème #83958 `macOS app node regresses in 2026.5.18: flaps online/offline and gateway invokes time out`.
- Problème #9876 `Show session and requester context in macOS exec approval popup`.
- Problème #44749 `Concurrent allow-always approvals silently lose allowlist entries`.
- Les PR #84645, #84172, #80922, #78793 et #82596 montrent un churn actif dans la planification d'approbation d'exécution et l'UX.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS system.run"`

Résultats :

- 2026-04-26 Miroir GitHub pour #49031 dit que l'ancien rapport manquant `system.run.prepare` d'application compagne macOS a été remplacé, mais la lacune restante est suivie par #37591/#38781.
- 2026-04-26 Miroir GitHub pour #37591 dit que le main actuel manque toujours le support macOS `system.run.prepare` tandis que le chemin d'exécution du nœud l'exige.
- 2026-04-26 Miroir GitHub pour #71877 note que l'éligibilité du bin de compétence macOS distante a été corrigée après la gestion de la réponse de carte d'objet `system.which`.
