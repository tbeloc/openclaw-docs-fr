---
title: "Automatisation des navigateurs et outils exec/sandbox - Note de maturité des approbations Host Exec et du mode élevé"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation des navigateurs et outils exec/sandbox - Note de maturité des approbations Host Exec et du mode élevé

## Résumé

Les approbations Host exec et le mode élevé sont Stables. L'implémentation dispose d'un système d'approbation en couches, d'une inscription d'approbation en deux phases, de la mise en évidence des commandes, de la planification des safe-bin et des listes blanches, d'une gestion stricte de l'inline-eval, de la liaison d'approbation des nœuds et d'une documentation claire du mode élevé. Elle reste en dessous de Lovable car la politique est intentionnellement complexe et les erreurs de configuration des utilisateurs/opérateurs créent toujours un risque réel.

## Portée de la catégorie

Cette note couvre la politique d'approbation exec, l'état des approbations locales, l'inscription et l'attente des demandes d'approbation, la consommation allow-once, les safe bins, les safe builtins, l'eval inline strict, la planification de l'interpréteur, les étendues de commandes, la liaison du plan d'approbation `system.run` des nœuds, la livraison de suivi et le mode élevé.

## Fonctionnalités

- Approbations Host Exec : Couvre les approbations Host Exec dans la politique d'approbation exec, l'état des approbations locales, l'inscription et l'attente des demandes d'approbation, la consommation allow-once et les comportements connexes des approbations host exec et du mode élevé.
- Mode élevé : Couvre le mode élevé dans la politique d'approbation exec, l'état des approbations locales, l'inscription et l'attente des demandes d'approbation, la consommation allow-once et les comportements connexes des approbations host exec et du mode élevé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs :
  - La documentation couvre les approbations exec basiques et avancées, les safe bins, les listes blanches, l'eval inline strict, le transfert d'approbation, les approbations dans le même chat et le mode élevé.
  - La source implémente l'inscription en deux phases avant de retourner l'approbation en attente, la recherche en attente, l'expiration, la consommation atomique allow-once et la reprise de suivi.
  - Les tests couvrent l'analyse des demandes d'approbation, les étendues de commandes, les minuteurs du gestionnaire, la correspondance des listes blanches, la politique des safe-bin, l'eval inline strict, la parité d'approbation, le routage d'approbation natif et la liaison des nœuds.
  - Le chemin `system.run` des nœuds supprime les champs de contrôle utilisateur et revalide les approbations par rapport aux plans canoniques de commande/cwd/session.
- Signaux négatifs :
  - Les rapports d'archive montrent toujours une confusion des opérateurs autour de `security=full`, `ask=off`, des safe bins, de l'eval inline et du routage d'approbation des nœuds.
  - Le mode élevé contourne intentionnellement le sandboxing pour exec et doit être raisonné avec la politique des outils et les approbations ensemble.
- Lacunes d'intégration :
  - Ajouter un smoke test UX opérateur qui guide un utilisateur d'une commande bloquée à l'approbation, allow-once, allow-always et au mode élevé sur les hôtes gateway et node.
  - Ajouter une matrice spécifique au scorecard pour les combinaisons de safe bins, safe builtins, interpréteurs, wrappers shell et eval inline strict.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl :
  - `exec approval safe bins` a retourné la PR #79363 pour les safe builtins opt-in, le problème #46056 sur les builtins shell et les portes d'approbation, la PR #71154 autour de l'analyse des commandes en liste blanche, la PR #80922 routant allow-always via le planificateur de commandes et la PR #84172 révisant les candidats d'autorisation de commandes.
  - `tools invoke system.run approval node invoke` a retourné le problème #77096 sur la confiance du cwd symlink, la PR #81827 ajoutant denyPathPatterns, la PR #78226 sur la réécriture de la liste blanche des nœuds restaurant les approbations révoquées et la PR #81488 renforçant la vérification préalable d'approbation exec des nœuds env.
- Rapports Discrawl :
  - `exec approvals safe bins elevated` a retourné une réponse d'assistance du 2026-03-06 expliquant que `security="full"` plus `ask="off"` est un accès shell brut sur l'hôte sélectionné, soumis uniquement à la politique des outils et à un état d'approbations plus strict.
- Bonnes qualités :
  - L'inscription d'approbation est en deux phases pour éviter les courses `/approve` orphelines.
  - Le gestionnaire d'approbation conserve brièvement les entrées résolues pour les attentes et consomme les décisions allow-once de manière atomique.
  - Les paramètres d'approbation hôte incluent la commande, argv, le plan system run, cwd, env, hôte, id de nœud, sécurité, ask, étendues de commandes, demandeur et source de tour.
  - Le transfert des nœuds supprime les champs de contrôle d'approbation de l'entrée non fiable et ne restaure que l'état d'approbation fiable à partir des enregistrements d'approbation Gateway.
  - La documentation élevée dit explicitement qu'elle ne remplace pas la politique des outils.
- Mauvaises qualités :
  - La sémantique des safe-bin et des listes blanches est difficile à expliquer car les wrappers shell, les builtins, les interpréteurs, l'eval inline, la confiance stdin et la confiance du chemin interagissent tous.
  - `security`, `ask`, l'état élevé et les valeurs par défaut d'approbation locales peuvent produire un résultat plus strict ou plus permissif que prévu si les opérateurs ne configurent qu'une seule couche.
  - La livraison d'approbation native est répartie sur les canaux et peut échouer de manière à ressembler à un échec de politique exec.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, live et runtime-flow n'ont affecté que la couverture.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les approbations Host Exec et le mode élevé.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La politique d'approbation a besoin de diagnostics plus clairs lorsque l'état des approbations locales et `tools.exec.*` ne sont pas d'accord.
- La politique des safe-bin, eval inline strict et interpréteur doit rester sous examen de sécurité.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md:11` : les approbations sont documentées comme faisant partie d'une pile de garde-fous avec la politique des outils et le mode élevé.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md:18` : la documentation indique que le plus strict de `tools.exec.*` et l'état des approbations locales gagne.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md:48` : la documentation décrit les hôtes gateway/node, le modèle de confiance, la liaison de fichiers et la dérive.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md:115` : la documentation couvre la sécurité, ask, fallback, eval inline strict, la mise en évidence des commandes et les safe bins.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals-advanced.md:14` : la documentation explique les safe bins comme stdin uniquement et non comme une confiance générique.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals-advanced.md:66` : la documentation couvre les répertoires de confiance, le chaînage shell, les wrappers et l'eval inline strict.
- `/Users/kevinlin/code/openclaw/docs/tools/elevated.md:9` : le mode élevé est documenté comme une échappatoire exec sandbox-to-host.
- `/Users/kevinlin/code/openclaw/docs/tools/elevated.md:103` : l'élevé ne remplace pas la politique des outils ou la sélection d'hôte.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-approval-request.ts:116` : l'inscription de la demande d'approbation se produit avant de retourner `approval-pending`.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-approval-request.ts:137` : waitDecision gère le timeout/approbation manquante comme une décision nulle.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-approval-request.ts:269` : les paramètres d'approbation hôte incluent le plan system run, env, cwd, hôte, sécurité, ask, étendues de commandes, demandeur et source de tour.
- `/Users/kevinlin/code/openclaw/src/gateway/exec-approval-manager.ts:54` : le gestionnaire d'approbation suit les enregistrements d'approbation en attente.
- `/Users/kevinlin/code/openclaw/src/gateway/exec-approval-manager.ts:118` : la résolution d'approbation enregistre la décision et planifie le nettoyage.
- `/Users/kevinlin/code/openclaw/src/gateway/exec-approval-manager.ts:175` : les décisions allow-once sont consommées de manière atomique.
- `/Users/kevinlin/code/openclaw/src/gateway/exec-approval-manager.ts:200` : la recherche d'approbation supporte les résultats exacts, préfixe, ambigus et aucun.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.ts:190` : le transfert system.run met en liste blanche les champs compris par l'hôte node.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.ts:214` : les champs de contrôle d'approbation sont contrôlés par un enregistrement d'approbation exec réel.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.ts:106` : la phase de politique system.run des nœuds porte la sécurité, la liste blanche, les safe bins, l'eval inline strict et les décisions d'approbation.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-gateway-approval.e2e.test.ts:1` : la couverture e2e existe pour les approbations Gateway exec.
- `/Users/kevinlin/code/openclaw/src/gateway/operator-approvals-client.e2e.test.ts:1` : la couverture e2e du client d'approbation opérateur existe.
- `/Users/kevinlin/code/openclaw/src/infra/approval-native-delivery.test.ts:1` : la couverture de livraison d'approbation native existe.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-approval-request.test.ts:94` : vérifie que les décisions d'approbation de chaîne sont retournées.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-approval-request.test.ts:183` : vérifie que l'id de réponse d'inscription est utilisé lors de l'attente d'une décision.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-approval-request.test.ts:276` : vérifie que les étendues de commandes sont ajoutées aux charges utiles d'inscription d'approbation hôte.
- `/Users/kevinlin/code/openclaw/src/gateway/exec-approval-manager.test.ts:9` : vérifie le comportement du gestionnaire d'approbation.
- `/Users/kevinlin/code/openclaw/src/infra/exec-approvals-safe-bins.test.ts:1` : les tests de politique des safe-bin existent.
- `/Users/kevinlin/code/openclaw/src/infra/system-run-approval-binding.test.ts:1` : les tests de liaison d'approbation system.run existent.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.test.ts:1` : les tests d'approbation system.run des nœuds Gateway existent.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "exec approval safe bins" --json`

Résultats :

- PR ouverte #79363 : `tools.exec.safeBuiltins` opt-in.
- Problème ouvert #46056 : les builtins shell déclenchent toujours la porte d'approbation avec liste blanche.
- PR ouverte #71154 : accepter la nouvelle ligne antislash POSIX dans les commandes en liste blanche.
- PR ouverte #80922 : router allow-always via le planificateur d'autorisation de commandes.
- PR ouverte #84172 : réviser les candidats d'autorisation de commandes.

Requête :

`gitcrawl search openclaw/openclaw --query "tools invoke system.run approval node invoke" --json`

Résultats :

- Problème ouvert #77096 : opt-in symlink cwd pour `system.run` lié à l'approbation.
- PR ouverte #81827 : ajouter la porte hard-deny `tools.exec.denyPathPatterns`.
- PR ouverte #78226 : la réécriture de la liste blanche des nœuds peut restaurer les approbations exec révoquées.
- PR ouverte #81488 : renforcer la vérification préalable d'approbation exec des nœuds env.

### Requêtes Discrawl

Requête :

`discrawl search --mode fts --limit 5 "exec approvals safe bins elevated"`

Résultats :

- Une réponse d'assistance du 2026-03-06 explique que `security="full"` plus `ask="off"` signifie un accès shell brut sur l'hôte gateway/node lorsque la politique des outils et l'état des approbations locales le permettent.
