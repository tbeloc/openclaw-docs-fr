---
version: 3
---

# Approbations et exécution à distance

## Résumé

- Famille de fonctionnalités : Approbations et exécution à distance.
- Slug : approval-and-execution-safety.
- Couverture : 88/100, Oui.
- Qualité : 72/100, Moyen.
- Conclusion : Les API de demande/recherche/attente/résolution d'approbation d'exécution, les instantanés de politique d'approbation au niveau de la passerelle et du nœud local, la liaison `systemRunPlan` nœud-hôte, le rejet de mutation, les primitives d'approbation de plugin et le comportement de livraison d'agent strict par rapport au meilleur effort sont implémentés et documentés. La couverture est Oui car les tests réels de flux Gateway/WebSocket/serveur prouvent la résolution d'approbation d'exécution, la protection de contournement d'approbation node.invoke, le rejet de relecture nœud/appareil et le comportement de secours de livraison stricte.
- La qualité reste Moyen car les rapports d'archive ouverts montrent toujours des lacunes dans la route d'approbation et l'approbation de plugin, des préoccupations concernant la confidentialité du canal de groupe, des lacunes de consentement médiatisé par canal et des cas limites de secours de livraison.

## Fonctionnalités

- Approbations d'exécution : Demande d'approbation d'exécution, recherche, attente, résolution et API d'instantané de politique.
- Approbations de plugin : Flux de demande, d'attente et de résolution d'approbation de plugin.
- Approbations d'exécution de nœud : Relais de politique d'approbation d'exécution local au nœud via RPC de passerelle.
- Exécution de nœud approuvée : Liaison `systemRunPlan` canonique pour l'exécution nœud-hôte.
- Sécurité de mutation d'approbation : Rejet de `command`, `cwd`, `agentId` ou `sessionKey` mutés après la préparation d'approbation.
- Comportement de secours de livraison : Secours de livraison d'agent entre les routes livrables strictes et l'exécution en session uniquement.

## Fraîcheur de l'archive

- `gitcrawl doctor --json` : `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json` : `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 88/100.

Étiquette : Oui.

Signaux positifs :

- Les documents de protocole énumèrent les API de demande/obtention/liste/résolution/attente de décision d'approbation d'exécution, les API d'instantané de politique de passerelle, les API de relais de politique local au nœud et les API de demande/liste/attente de décision/résolution d'approbation de plugin (`docs/gateway/protocol.md:465`, `docs/gateway/protocol.md:470`).
- Les documents de protocole exposent les événements de cycle de vie `exec.approval.requested` / `exec.approval.resolved` et `plugin.approval.requested` / `plugin.approval.resolved` (`docs/gateway/protocol.md:503`, `docs/gateway/protocol.md:506`).
- Les documents de protocole indiquent que les approbations `host=node` nécessitent `systemRunPlan`, les transferts approuvés réutilisent le plan canonique et les `command`, `rawCommand`, `cwd`, `agentId` ou `sessionKey` mutés sont rejetés (`docs/gateway/protocol.md:621`, `docs/gateway/protocol.md:630`).
- Les documents de protocole définissent l'échec de livraison stricte par rapport au secours en session uniquement `bestEffortDeliver=true` (`docs/gateway/protocol.md:632`, `docs/gateway/protocol.md:636`).
- Les documents de sécurité décrivent la limite de confiance Gateway/nœud, clarifient que `sessionKey` est un contexte de routage plutôt qu'une authentification et documentent la liaison de contexte de demande exacte pour les approbations d'exécution (`docs/gateway/security/index.md:170`, `docs/gateway/security/index.md:183`).
- Les documents de sécurité distinguent l'appairage de nœud de l'approbation par commande, acheminent la politique `system.run` locale au nœud via le fichier d'approbations d'exécution du nœud et documentent le stockage `systemRunPlan` canonique plus le rejet d'édition d'appelant (`docs/gateway/security/index.md:498`, `docs/gateway/security/index.md:508`).
- La source enregistre les portées de méthode d'approbation et les gestionnaires pour les approbations d'exécution, les instantanés de politique d'approbation d'exécution, les relais de politique d'approbation local au nœud et les approbations de plugin (`src/gateway/methods/core-descriptors.ts:51`, `src/gateway/server-aux-handlers.ts:268`).
- Les gestionnaires d'approbation d'exécution prennent en charge la recherche/liste/demande, l'enregistrement de demande en deux phases avant la réponse, la validation `nodeId` et `systemRunPlan` pour host=node, la construction de liaison canonique et la diffusion d'événement de demande (`src/gateway/server-methods/exec-approval.ts:90`, `src/gateway/server-methods/exec-approval.ts:153`, `src/gateway/server-methods/exec-approval.ts:221`, `src/gateway/server-methods/exec-approval.ts:289`, `src/gateway/server-methods/exec-approval.ts:339`).
- Les API de politique d'approbation d'exécution au niveau de la passerelle et du nœud local sont séparées : les instantanés de passerelle lisent/écrivent la configuration d'approbation locale, tandis que `exec.approvals.node.get/set` relaie via les commandes `system.execApprovals.*` du nœud (`src/gateway/server-methods/exec-approvals.ts:98`, `src/gateway/server-methods/exec-approvals.ts:131`).
- Les approbations de plugin génèrent des ID `plugin:` au niveau du serveur, portent le contexte plugin/outil/session/source de tour, diffusent les événements de demande, attendent les décisions, valident les décisions autorisées et diffusent les événements résolus (`src/gateway/server-methods/plugin-approval.ts:28`, `src/gateway/server-methods/plugin-approval.ts:88`, `src/gateway/server-methods/plugin-approval.ts:110`, `src/gateway/server-methods/plugin-approval.ts:137`, `src/gateway/server-methods/plugin-approval.ts:160`, `src/gateway/server-methods/plugin-approval.ts:169`).
- Le transfert d'approbation nœud-hôte supprime les champs d'approbation contrôlés par l'appelant, nécessite un enregistrement d'approbation réel et un runId, lie l'utilisation d'approbation au contexte de nœud et d'appareil/client, réécrit la commande/cwd/agent/session à partir du `systemRunPlan` stocké, rejette les incompatibilités de liaison et consomme les approbations d'autorisation unique (`src/gateway/node-invoke-system-run-approval.ts:214`, `src/gateway/node-invoke-system-run-approval.ts:257`, `src/gateway/node-invoke-system-run-approval.ts:291`, `src/gateway/node-invoke-system-run-approval.ts:315`, `src/gateway/node-invoke-system-run-approval.ts:340`, `src/gateway/node-invoke-system-run-approval.ts:380`, `src/gateway/node-invoke-system-run-approval.ts:394`).
- La planification de livraison d'agent maintient les échecs de livraison stricte quand `bestEffortDeliver=false` et rétrograde les routes livrables internes ou manquantes à la session uniquement quand le meilleur effort est activé (`src/gateway/server-methods/agent.ts:1702`, `src/gateway/server-methods/agent.ts:1735`, `src/gateway/server-methods/agent.ts:1776`, `src/gateway/server-methods/agent.ts:1797`).
- Les tests réels Gateway/WebSocket couvrent le comportement du résolveur d'approbation local, le rejet de recherche d'approbation de boucle de retour à distance et la résolution d'approbation d'opérateur de connexion séparée (`src/gateway/operator-approvals-client.e2e.test.ts:83`, `src/gateway/operator-approvals-client.e2e.test.ts:139`, `src/agents/bash-tools.exec-gateway-approval.e2e.test.ts:63`).
- Les tests réels de flux Gateway/serveur couvrent le rejet de charge utile node.invoke avant le transfert, la liaison approbation/appareil, le rejet de relecture entre appareils, la relecture de reconnexion du serveur uniquement pour la même source de tour et le rejet de relecture entre nœuds (`src/gateway/server.node-invoke-approval-bypass.test.ts:409`, `src/gateway/server.node-invoke-approval-bypass.test.ts:503`, `src/gateway/server.node-invoke-approval-bypass.test.ts:581`, `src/gateway/server.node-invoke-approval-bypass.test.ts:681`).
- Les tests du serveur d'agent de passerelle couvrent l'erreur de livraison stricte et le routage du dernier canal avec `bestEffortDeliver` par défaut vrai pour le chemin d'exécution de chat actif (`src/gateway/server.agent.gateway-server-agent-a.test.ts:516`, `src/gateway/server.agent.gateway-server-agent-a.test.ts:579`).

Signaux négatifs :

- La couverture de bout en bout d'approbation de plugin est plus faible que celle d'approbation d'exécution. L'implémentation a des tests de gestionnaire/unité pour la demande, l'expiration sans route, la génération d'ID et les décisions autorisées, mais aucun test d'intégration WebSocket/canal complet comparable à `src/agents/bash-tools.exec-gateway-approval.e2e.test.ts:63`.
- Le chemin de sécurité s'étend sur les gestionnaires de demande de passerelle, le routage d'approbation partagé, la désinfection node.invoke, la préparation/exécution nœud-hôte, le suivi d'approbation d'outil bash, les aides SDK de plugin et les interfaces utilisateur d'approbation de canal. L'historique d'archive montre que cette largeur a produit des régressions répétées.
- `systemRunPlan` a des preuves fortes au niveau source/unité/flux serveur, mais la preuve nœud-hôte en direct sur les services de nœud Mac/Linux/Windows réels n'a pas été trouvée dans cette tranche.
- Le secours de livraison d'agent a des preuves de flux serveur, mais les rapports d'archive montrent que le comportement de secours de livraison et de route d'approbation produisent toujours des cas limites spécifiques au canal.

Lacunes d'intégration :

- Ajouter un test de flux d'approbation de plugin WebSocket/Gateway complet qui demande `plugin.approval.request`, livre à un client capable d'approbation ou à un runtime de canal, résout via `plugin.approval.resolve` et vérifie `plugin.approval.resolved`.
- Ajouter une preuve nœud-hôte en direct pour l'exécution approuvée `host=node` qui prépare `system.run.prepare`, stocke `systemRunPlan`, mute les entrées finales de commande/cwd/session et vérifie le comportement de fermeture en cas d'échec sur un service de nœud réel.
- Ajouter une preuve d'approbation native multi-canal pour le routage d'approbation privé/groupe car les discussions récentes Discord/iMessage/Slack montrent que le comportement de route et de duplication reste fragile.
- Ajouter une preuve de flux serveur pour le secours de livraison d'agent quand les routes de suivi d'approbation ne sont pas disponibles, pas seulement le chemin de livraison d'agent générique.

## Qualité

Score: 72/100.

Label: Moyen.

### Rapports Gitcrawl

- Requête : `gitcrawl search issues '"exec approval" OR "exec approvals" OR "exec.approval"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 20 résultats, tous fermés dans la page retournée. Les rapports notables incluent #15047 conflit entre `approvals.exec` et `exec-approvals.json` ; #16184 transfert d'approbation exec vers Telegram cassé ; #61600 erreur d'approbation trompeuse command-too-long ; #9063 sécurité full/ask off bloque toujours ; #22988 bot Discord ne reçoit pas `exec.approval.requested` ; #43989 socket d'approbation exec non créé/suspendu ; #19919 délai d'expiration d'approbation exec configurable ; #59125 comportement subagent `approvals.exec.mode` invalide.
- Requête : `gitcrawl search issues '"plugin approval" OR "plugin approvals" OR "plugin.approval"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 20 résultats. Les rapports ouverts incluent #75749 messages d'approbation plugin Telegram en double quand `turnSourceChannel` est null ; #74003 pas de route d'approbation plugin / `turnSourceChannel` non transmis ; #81901 contexte d'approbation plugin long format ; #86777 documenter la gestion du mode rapport Codex app-server de `requireApproval` plugin ; #79824 cartes d'approbation Feishu V2 échouent ; #78308 approbation médiatisée par canal pour les appels d'outils MCP. Les rapports fermés incluent #59671 approbation plugin bloquant deadlock `waitDecision`, #48515 primitive de routage d'approbation générique, #75696 approbation Computer Use refusée via élicitation MCP, #82485 race deliverTarget runtime approval-handler, #79157 approbations exec assistées par LLM / raisonnement politique, et #19072 approbations d'outils de première classe pause/interruption/reprise.
- Requête : `gitcrawl search issues '"systemRunPlan" OR "system.run.prepare" OR "system.run" "approval"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : aucun problème retourné.
- Requête : `gitcrawl search issues '"bestEffortDeliver" OR "session-only" OR "delivery fallback" OR "deliverable route"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : aucun problème retourné.
- Requête : `gitcrawl search issues 'node exec approval system.run node.invoke approval bypass' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 8 résultats, tous fermés dans la page retournée. Les rapports notables incluent #8682 contournement d'approbation exec via drapeaux contrôlés par le client dans `system.run` ; #10128 `node.invoke` permet à `operator.write` de contourner les approbations avec drapeau approuvé contrôlé par l'appelant ; #66136 host=node refuse les binaires chemin absolu sous full/off ; #65542 l'appairage d'appareil expose les nœuds capables d'exec avant approbation du nœud admin ; #65168 `node.invoke` accessible avant approbation d'appairage de nœud ; #66524 échec du binder fail-closed rejette toutes les commandes chemin absolu.
- Requête : `gitcrawl search issues 'node.invoke system.run approval runId approved approvalDecision' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : aucun problème retourné.
- Requête : `gitcrawl search issues 'agent delivery best effort session only deliver fallback' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 5 résultats. Le rapport ouvert #84297 indique que la superposition d'identité par agent est supprimée sur les annonces cron/pulsations Slack. Les rapports fermés incluent #21552 l'annonce cron échoue quand la cible/le canal de livraison n'est pas défini, #27131 routage cron/session de première classe, #22298 l'annonce cron isolée échoue avec appairage requis, et #67849 lag `sessions_send`.
- Requête : `gitcrawl search issues 'approval route no approval route turnSourceChannel approvals plugin exec' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 2 résultats : #74003 ouvert pour pas de route d'approbation plugin / `turnSourceChannel` manquant, et #85841 fermé pour approbations exec de pulsation attendant le délai d'expiration complet au lieu d'échouer rapidement sur surface non supportée.

### Rapports Discrawl

- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "exec approval"`
  Résultat : résultats récents des mainteneurs et clawtributors autour du déplacement de la logique de réaction d'approbation vers `plugin-sdk`, invites d'approbation exec native iMessage en double, rupture de token de carte/DM d'approbation exec Discord, discussion de moindre privilège de notice de route d'approbation Discord, approbations exec originaires de groupe routées vers DM pour éviter de divulguer les détails de commande/chemin, et support utilisateur autour du relais de hook natif et de la politique exec.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "plugin approval"`
  Résultat : résultats récents autour des PRs de résolution d'approbation HITL plugin externe (#82431/#82434/#82471), assistants de réaction d'approbation SDK plugin, résolution d'approbation soutenue par preuve, cartes d'approbation/statut durables, UX d'approbation clic obsolète Discord, et split notice de route d'approbation native/token.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "systemRunPlan"`
  Résultat : les résultats incluent le problème #55258 fermé comme implémenté pour l'approbation exec ciblée par nœud exécutée sur le nœud sélectionné, PR #59804 transfert de `systemRunPlan` dans le chemin d'approbation asynchrone, commentaires PR/révision avertissant que `systemRunPlan` manquant casse `host=node`, et support utilisateur expliquant les métadonnées d'approbation avec `systemRunPlan` / `systemRunBinding`.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "bestEffortDeliver"`
  Résultat : les résultats incluent PR fermée #53538 et #51948 autour de la dégradation de livraison best-effort vers session-only, PR #70585 annonce subagent livraison best-effort, guidance Discord DM route stricte avec `bestEffortDeliver=false`, révision d'enveloppe JSON d'échec de livraison, et corrections de fallback boot/startup de livraison.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "no approval route"`
  Résultat : les résultats incluent guidance mainteneur que la lecture de token de processus séparé doit être CLI/Docker-only, discussion contributeur du modèle action d'approbation/no-route dans #82431, problème fermé #67285 où les approbations no-route se résolvent comme état indisponible typé, problème fermé #43989 où no approval route expire immédiatement au lieu de suspendre, et problème fermé #66994 autour des invites malgré ask off.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "node.invoke approval"`
  Résultat : les résultats incluent discussion de politique nœud/fetch-fichier, problème #55258 implémenté avec `systemRunPlan`, bug critique pre-pairing node.invoke #65168/#65169, commentaires de révision sur transfert d'approbation fallback inline vers node invoke, préservation des métadonnées d'appareil demandeur, et analyse des remplacements d'environnement pour les charges utiles system.run.
- Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "delivery fallback"`
  Résultat : résultats récents axés sur le travail de fallback de livraison plus large : PRs de fallback de média généré, corrections d'origine livraison Feishu/Discord, et comportement de fallback canal/session. Aucun résultat spécifique à l'approbation n'a dominé cette requête.

### Bonnes qualités

- Les approbations exec et plugin partagent une mécanique d'approbation en attente commune tout en gardant les espaces de noms de méthode et les préfixes d'ID distincts.
- Le chemin d'approbation du nœud-hôte traite `systemRunPlan` comme l'autorité, pas les paramètres finaux `node.invoke` fournis par l'appelant, et vérifie la liaison nœud/appareil/session avant transfert.
- Les décisions d'approbation sont délimitées : les approbations plugin valident les décisions autorisées, les approbations exec consomment allow-once, et les commandes de nœud `system.execApprovals.*` directes sont bloquées via `node.invoke` générique.
- Les documents de protocole et de sécurité énoncent explicitement le modèle de sécurité et le comportement de mutation fail-closed, ce qui est important car les archives montrent que les utilisateurs et les mainteneurs construisent des clients opérateur personnalisés autour de ces RPCs.

### Mauvaises qualités

- Le routage d'approbation reste divisé entre les gestionnaires Gateway principaux, les gestionnaires d'approbation plugin, les runtimes d'approbation de canal natif, les assistants de réaction SDK plugin, et le code de suivi de livraison.
- Les rapports d'approbation plugin ouverts montrent des lacunes no-route, message en double, contexte long, rendu de carte Feishu, et approbation MCP médiatisée par canal.
- Les résultats d'archive montrent une confusion répétée autour de `approvals.exec`, des défauts d'approbation de nœud, des notices de route, des tokens de socket partagés, et si les cartes d'approbation divulguent les détails de commande sensibles dans les canaux de groupe.
- HITL plugin devient une surface plugin/API externe plus large, mais le comportement no-route, long-contexte, duplicate-delivery, et channel-rendering reste inégal dans les rapports d'archive ouverts.
- Les approbations MCP médiatisées par canal, la documentation du mode rapport app-server Codex pour `requireApproval` plugin, le raisonnement d'approbation assisté par LLM, et les délais d'expiration d'approbation configurables restent des lacunes d'attente dans les rapports d'archive.

## Lacunes connues

### Implémentées

- APIs de demande/obtention/liste/résolution/attente de décision d'approbation d'exécution et événements de cycle de vie (`docs/gateway/protocol.md:465`, `src/gateway/server-methods/exec-approval.ts:90`, `src/gateway/server-methods/approval-shared.ts:223`, `src/gateway/server-methods/approval-shared.ts:374`).
- Snapshot de politique d'approbation d'exécution de passerelle et relais de politique d'approbation d'exécution local au nœud via `exec.approvals.node.get/set` (`docs/gateway/protocol.md:468`, `src/gateway/server-methods/exec-approvals.ts:98`, `src/gateway/server-methods/exec-approvals.ts:131`).
- APIs de demande/liste/attente de décision/résolution d'approbation de plugin, IDs de plugin générés par le serveur, validation des décisions autorisées et événements de cycle de vie (`docs/gateway/protocol.md:470`, `src/gateway/server-methods/plugin-approval.ts:28`, `src/gateway/server-methods/plugin-approval.ts:88`, `src/gateway/server-methods/plugin-approval.ts:169`).
- Exigence et liaison canoniques de `systemRunPlan` nœud-hôte pour l'enregistrement d'approbation (`docs/gateway/protocol.md:625`, `src/gateway/server-methods/exec-approval.ts:199`, `src/gateway/server-methods/exec-approval.ts:221`, `src/gateway/server-methods/exec-approval.ts:289`).
- Rejet ou neutralisation de l'état de commande/cwd/agent/session muté après préparation d'approbation (`docs/gateway/protocol.md:626`, `src/gateway/node-invoke-system-run-approval.ts:340`, `src/gateway/node-invoke-system-run-approval.test.ts:284`).
- Flux de préparation et d'exécution approuvée du nœud-hôte, incluant `system.run.prepare`, demande d'approbation avec plan stocké et transfert approuvé de `node.invoke system.run` (`src/agents/bash-tools.exec-host-node-phases.ts:221`, `src/agents/bash-tools.exec-host-node.ts:85`, `src/agents/bash-tools.exec-host-node.ts:212`, `src/node-host/invoke.ts:442`).
- Revalidation d'opérande de fichier mutable du nœud-hôte et comportement de fermeture défaillante pour les charges utiles shell mutables/ambiguës (`src/node-host/invoke-system-run.ts:562`, `src/node-host/invoke-system-run-plan.test.ts:686`, `src/node-host/invoke-system-run-plan.test.ts:1059`).
- Secours de livraison d'agent entre les routes de livrables strictes et l'exécution en session uniquement (`docs/gateway/protocol.md:632`, `src/gateway/server-methods/agent.ts:1776`, `src/gateway/server-methods/agent.ts:1797`, `src/infra/outbound/best-effort-delivery.ts:42`).

### Manquantes

- Lacune de couverture : preuve complète d'intégration Gateway/WebSocket/plugin/canal pour les approbations de plugin.
- Lacune de couverture : preuve Gateway/nœud en direct sur les services de nœud-hôte réels pour le rejet de mutation `systemRunPlan` et la revalidation d'opérande mutable.
- Lacune de couverture : preuve d'approbation native multi-canal pour le routage d'approbation privée/groupe.
- Lacune de couverture : preuve de flux serveur pour le secours de livraison d'agent lorsque les routes de suivi d'approbation ne sont pas disponibles.
- Fermeture complète des rapports de non-route d'approbation de plugin, livraison dupliquée, contexte d'approbation long et rendu de carte Feishu.
- L'approbation médiatisée par canal de première classe pour le consentement MCP/appel d'outil est toujours ouverte.
- La documentation pour la gestion du mode rapport du serveur d'application Codex de `requireApproval` du plugin reste ouverte.
- Les cas limites de secours de livraison autour de l'identité cron/heartbeat/par-agent ne sont pas entièrement fermés.

### Demandes de fonctionnalités des utilisateurs-mainteneurs

- #74003 : corriger le comportement de non-route d'approbation de plugin lorsque `turnSourceChannel` n'est pas transmis.
- #75749 : empêcher les messages d'approbation de plugin Telegram en double lorsque `turnSourceChannel` est null.
- #81901 : prendre en charge le contexte d'approbation de plugin de forme longue.
- #86777 : documenter la gestion du mode rapport du serveur d'application Codex de `requireApproval` du plugin.
- #79824 : rendre les cartes d'approbation Feishu V2 correctement rendues/actionnées.
- #78308 : ajouter l'approbation médiatisée par canal pour les appels d'outil MCP / enveloppes de consentement.
- #79157 : ajouter le raisonnement d'approbation d'exécution ou de politique assisté par LLM.
- #19919 : délai d'expiration d'approbation d'exécution configurable.
- #84297 : préserver la superposition d'identité par agent pour les annonces cron/heartbeat Slack.

## Preuves

### Docs

- `docs/gateway/protocol.md:465` répertorie les API de demande/obtention/liste/résolution d'approbation exec.
- `docs/gateway/protocol.md:467` répertorie `exec.approval.waitDecision`.
- `docs/gateway/protocol.md:468` répertorie les snapshots de politique d'approbation exec de la passerelle.
- `docs/gateway/protocol.md:469` répertorie les API de relais de politique d'approbation exec locales au nœud.
- `docs/gateway/protocol.md:470` répertorie les API de demande/liste/waitDecision/résolution d'approbation plugin.
- `docs/gateway/protocol.md:503` documente les événements du cycle de vie d'approbation exec.
- `docs/gateway/protocol.md:505` documente les événements du cycle de vie d'approbation plugin.
- `docs/gateway/protocol.md:621` documente le comportement d'approbation exec.
- `docs/gateway/protocol.md:625` documente le `systemRunPlan` requis pour `host=node`.
- `docs/gateway/protocol.md:626` documente le transfert canonique post-approbation.
- `docs/gateway/protocol.md:628` documente le rejet de mutation d'appelant.
- `docs/gateway/protocol.md:632` documente le repli de livraison d'agent.
- `docs/gateway/security/index.md:170` documente la confiance Passerelle/nœud.
- `docs/gateway/security/index.md:180` indique que `sessionKey` est routage/contexte, pas authentification.
- `docs/gateway/security/index.md:181` définit les approbations exec comme des garde-fous d'intention d'opérateur.
- `docs/gateway/security/index.md:183` documente les limites de liaison exacte contexte-demande.
- `docs/gateway/security/index.md:498` documente l'appairage de nœud par rapport à l'approbation par commande.
- `docs/gateway/security/index.md:502` documente les approbations exec locales au nœud.
- `docs/gateway/security/index.md:505` documente le stockage canonique `systemRunPlan` et le rejet de modification d'appelant.

### Source

- `src/gateway/methods/core-descriptors.ts:51` mappe les méthodes d'approbation aux portées.
- `src/gateway/server-aux-handlers.ts:268` installe les gestionnaires d'approbation exec/plugin paresseux.
- `src/gateway/server-methods/exec-approval.ts:90` crée les gestionnaires de demande/obtention/liste d'approbation exec.
- `src/gateway/server-methods/exec-approval.ts:153` gère `exec.approval.request`.
- `src/gateway/server-methods/exec-approval.ts:199` résout le contexte de demande canonique à partir de `systemRunPlan`.
- `src/gateway/server-methods/exec-approval.ts:221` requiert `systemRunPlan` pour `host=node`.
- `src/gateway/server-methods/exec-approval.ts:289` construit la liaison d'approbation d'exécution système.
- `src/gateway/server-methods/exec-approval.ts:307` stocke les champs de charge utile de demande d'approbation.
- `src/gateway/server-methods/exec-approval.ts:339` enregistre les approbations en attente avant de répondre.
- `src/gateway/server-methods/exec-approvals.ts:98` implémente l'obtention/définition de la politique d'approbation exec de la passerelle.
- `src/gateway/server-methods/exec-approvals.ts:131` implémente le relais de politique d'approbation exec local au nœud.
- `src/gateway/server-methods/plugin-approval.ts:28` crée les gestionnaires d'approbation plugin.
- `src/gateway/server-methods/plugin-approval.ts:48` gère `plugin.approval.request`.
- `src/gateway/server-methods/plugin-approval.ts:88` construit la charge utile d'approbation plugin.
- `src/gateway/server-methods/plugin-approval.ts:110` génère les ID d'approbation `plugin:` côté serveur.
- `src/gateway/server-methods/plugin-approval.ts:137` diffuse les demandes d'approbation plugin.
- `src/gateway/server-methods/plugin-approval.ts:160` implémente `waitDecision` plugin.
- `src/gateway/server-methods/plugin-approval.ts:169` implémente la résolution d'approbation plugin.
- `src/gateway/node-invoke-sanitize.ts:5` achemine les paramètres `system.run` node.invoke à travers le désinfectant d'approbation.
- `src/gateway/server-methods/nodes.ts:1072` bloque l'utilisation directe de `system.execApprovals.*` via `node.invoke` générique.
- `src/gateway/server-methods/nodes.ts:1201` désinfecte les paramètres node.invoke avant transfert.
- `src/gateway/node-invoke-system-run-approval.ts:214` documente la garde de contournement d'approbation node.invoke.
- `src/gateway/node-invoke-system-run-approval.ts:257` requiert runId et gestionnaire d'approbation.
- `src/gateway/node-invoke-system-run-approval.ts:291` lie l'approbation au nœud cible.
- `src/gateway/node-invoke-system-run-approval.ts:315` lie l'approbation au contexte appareil/client.
- `src/gateway/node-invoke-system-run-approval.ts:340` résout le contexte d'exécution à partir de `systemRunPlan` stocké.
- `src/gateway/node-invoke-system-run-approval.ts:380` évalue la correspondance de liaison d'approbation.
- `src/gateway/node-invoke-system-run-approval.ts:394` consomme les décisions allow-once.
- `src/gateway/server-methods/agent.ts:1702` résout l'état du plan de livraison.
- `src/gateway/server-methods/agent.ts:1735` gère le repli de sélection de canal interne.
- `src/gateway/server-methods/agent.ts:1776` conserve les erreurs de cible stricte lorsque best effort est désactivé.
- `src/gateway/server-methods/agent.ts:1797` rétrograde la livraison interne à session uniquement lorsque best effort est activé.
- `src/infra/outbound/best-effort-delivery.ts:42` définit l'éligibilité de rétrogradation session uniquement.
- `src/agents/bash-tools.exec-host-node.ts:85` enregistre l'approbation exec host-nœud avec `systemRunPlan`.
- `src/agents/bash-tools.exec-host-node.ts:212` invoque le nœud `system.run` après approbation.
- `src/node-host/invoke.ts:442` gère `system.run.prepare`.
- `src/node-host/invoke-system-run.ts:287` valide le `systemRunPlan` entrant.
- `src/node-host/invoke-system-run.ts:562` revalide les opérandes de fichier mutables.

### Tests d'intégration

- `src/gateway/operator-approvals-client.e2e.test.ts:83` démarre un serveur Gateway réel et connecte les clients administrateur/demandeur pour la résolution d'approbation.
- `src/gateway/operator-approvals-client.e2e.test.ts:139` prouve que la configuration de loopback distant ne peut pas résoudre l'approbation source locale.
- `src/agents/bash-tools.exec-gateway-approval.e2e.test.ts:63` prouve que l'outil exec gateway de style OpenClaw demande et attend l'approbation sur des connexions séparées.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:409` prouve que les charges utiles node.invoke malformées/interdites sont rejetées avant transfert.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:503` prouve que les approbations se lient à la décision/appareil et bloquent la relecture inter-appareils.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:581` prouve que les approbations backend sans appareil ne font pont que pour la même source de tour.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:681` prouve que la relecture inter-nœuds est bloquée.
- `src/gateway/server.agent.gateway-server-agent-a.test.ts:516` prouve que la livraison stricte échoue lorsqu'aucun dernier canal n'existe.
- `src/gateway/server.agent.gateway-server-agent-a.test.ts:579` prouve que le routage du dernier canal définit par défaut `bestEffortDeliver` true pour les exécutions de chat actives.

### Tests unitaires

- `src/gateway/server-methods/plugin-approval.test.ts:151` vérifie les gestionnaires pour toutes les méthodes d'approbation plugin.
- `src/gateway/server-methods/plugin-approval.test.ts:172` vérifie l'enregistrement et la diffusion de demande d'approbation plugin en deux phases.
- `src/gateway/server-methods/plugin-approval.test.ts:218` vérifie que les approbations plugin sans route expirent immédiatement avec une décision nulle.
- `src/gateway/server-methods/plugin-approval.test.ts:345` vérifie les ID d'approbation plugin générés par le serveur et rejette les ID fournis par le plugin.
- `src/gateway/server-methods/plugin-approval.test.ts:399` vérifie la portée de la décision autorisée.
- `src/gateway/node-invoke-system-run-approval.test.ts:248` vérifie l'application de l'identité commandArgv.
- `src/gateway/node-invoke-system-run-approval.test.ts:284` vérifie que `systemRunPlan` contrôle la commande/cwd/agent/contexte de session transféré et ignore la falsification d'appelant.
- `src/gateway/node-invoke-system-run-approval.test.ts:341` vérifie que l'absence de liaison env rejette les remplacements.
- `src/gateway/node-invoke-system-run-approval.test.ts:359` vérifie le rejet de non-correspondance de hash env.
- `src/gateway/node-invoke-system-run-approval.test.ts:385` vérifie la consommation allow-once et le blocage de relecture.
- `src/gateway/node-invoke-system-run-approval.test.ts:443` vérifie le rejet de non-correspondance nœud/appareil.
- `src/gateway/node-invoke-system-run-approval.test.ts:585` vérifie l'élimination de relecture de chat backend de confiance et le comportement de même contexte.
- `src/gateway/node-invoke-system-run-approval.test.ts:738` vérifie le rejet de relecture backend sur les changements de cible session/agent/canal.
- `src/node-host/invoke-system-run-plan.test.ts:686` vérifie le comportement fail-closed pour les charges utiles shell mutables/ambiguës.
- `src/node-host/invoke-system-run-plan.test.ts:1059` vérifie que la revalidation d'opérande de fichier mutable échoue après mutation de script.
- `src/agents/bash-tools.exec.approval-id.test.ts:500` vérifie que la liste d'autorisation de nœud satisfaite ignore `exec.approval.request`.
- `src/agents/bash-tools.exec.approval-id.test.ts:980` vérifie que le suivi d'approbation exec utilise `bestEffortDeliver`.
- `src/agents/bash-tools.exec.approval-id.test.ts:1528` vérifie que l'approbation inline cron du nœud envoie `systemRunPlan` et runId approuvés.

### Requêtes Gitcrawl

- `gitcrawl search issues '"exec approval" OR "exec approvals" OR "exec.approval"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
- `gitcrawl search issues '"plugin approval" OR "plugin approvals" OR "plugin.approval"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
- `gitcrawl search issues '"systemRunPlan" OR "system.run.prepare" OR "system.run" "approval"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
- `gitcrawl search issues '"bestEffortDeliver" OR "session-only" OR "delivery fallback" OR "deliverable route"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
- `gitcrawl search issues 'node exec approval system.run node.invoke approval bypass' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
- `gitcrawl search issues 'node.invoke system.run approval runId approved approvalDecision' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
- `gitcrawl search issues 'agent delivery best effort session only deliver fallback' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
- `gitcrawl search issues 'approval route no approval route turnSourceChannel approvals plugin exec' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`

### Requêtes Discrawl

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "exec approval"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "plugin approval"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "systemRunPlan"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "bestEffortDeliver"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "no approval route"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "node.invoke approval"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "delivery fallback"`
