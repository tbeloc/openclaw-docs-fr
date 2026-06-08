---
title: "WhatsApp - Native Controls and Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Native Controls and Approvals Maturity Note

## Résumé

Les approbations et réactions natives WhatsApp sont en Beta pour la Couverture et Stables pour la Qualité. La source sépare les approbateurs d'approbation des listes blanches de canaux, supporte les cibles d'approbateurs explicites, lie les décisions de réaction aux cibles d'invite persistantes, et gère le comportement de mise à jour/annulation d'invite. La Couverture reste en Beta car une preuve d'approbation en direct existe mais devrait rester un scénario récurrent pour les routes d'approbation exec et plugin.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Native Controls and Approvals`
- Fusionnée depuis : `Native Approvals`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Exec natif : Livraison d'approbation exec natif et plugin via WhatsApp
- Résolution de cible d'approbateur : Résolution de cible d'approbateur, éligibilité de cible DM/groupe, suppression de route, et livraison d'approbation.

## Fonctionnalités

- Exec natif : Livraison d'approbation exec natif et plugin via WhatsApp
- Résolution de cible d'approbateur : Résolution de cible d'approbateur, éligibilité de cible DM/groupe, suppression de route, et livraison d'approbation.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : la documentation couvre les approbations exec/plugin, `/approve` manuel, comportement de réaction natif, et séparation d'autorisation ; l'assurance qualité en direct a des scénarios d'approbation natif WhatsApp sélectionnables pour les approbations exec et plugin.
- Signaux négatifs : les scénarios d'approbation natif ne font pas partie de l'ensemble WhatsApp en direct standard par défaut, et la preuve d'archive est principalement une discussion adjacente plutôt que des défauts WhatsApp actuels.
- Lacunes d'intégration : ajouter une preuve en direct routinière pour la livraison d'invite exec et plugin, la mise à jour, la décision de réaction, l'annulation, le nettoyage de cible obsolète, et la suppression d'origine de groupe.

## Score de qualité

- Score : `Stable (84%)`
- Rapports Gitcrawl : `whatsapp native approval reaction exec plugin` a surfacé uniquement du bruit de formatage d'approbation iMessage adjacent, pas un problème WhatsApp direct.
- Rapports Discrawl : `whatsapp native approval reaction exec plugin` a surfacé la discussion des mainteneurs et la PR #86735 autour de la centralisation de la logique de réaction d'approbation dans plugin-sdk pour iMessage, WhatsApp, et Signal.
- Bonnes qualités : l'autorisation n'est pas déduite des listes blanches de canaux, les cibles d'approbateurs sont explicites, le routage d'origine de groupe nécessite des approbateurs éligibles, les cibles de réaction sont persistantes et nettoyées, les décisions obsolètes sont résolues défensivement, et le comportement de mise à jour/annulation d'invite est spécifique au canal.
- Mauvaises qualités : l'état de cible de réaction persistante est au mieux un effort autour des messages supprimés ou obsolètes, et la livraison dépend toujours de la même santé d'écouteur actif et de session Baileys que les messages sortants.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct, et du flux d'exécution réel n'a pas augmenté ou diminué ce score de Qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : la documentation archivée, la source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Exec natif, Résolution de cible d'approbateur.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Inclure les scénarios d'approbation natif exec et plugin WhatsApp dans la couverture en direct récurrente ou une porte de version équivalente.
- Ajouter des diagnostics opérationnels explicites de cible obsolète et de message supprimé.
- Garder la documentation des approbateurs d'approbation proche de la documentation des listes blanches de canaux pour éviter l'inférence non sécurisée par les opérateurs.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:178` documente les invites d'approbation, l'indépendance exec/plugin, `allowFrom` d'approbateur, et le comportement `/approve` manuel.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:455` documente les niveaux de réaction et les réactions ack/status.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:584` documente les portes d'écriture d'action et de config.

### Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-native.ts:203` active le routage d'approbation basé sur les paramètres de canal et de compte.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-native.ts:250` détermine l'éligibilité de session et de cible explicite.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-native.ts:316` résout les cibles d'origine et les exigences d'approbateur de groupe.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-native.ts:383` résout le routage DM d'approbateur et la suppression.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-native.ts:425` expose la capacité d'approbation natif WhatsApp.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-handler.runtime.ts:94` livre, met à jour, lie, délie, et annule les invites d'approbation natif.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-auth.ts:22` autorise les décisions d'approbation des approbateurs configurés.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-reactions.ts:37` définit le stockage de cible de réaction persistant.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-reactions.ts:263` résout les décisions de réaction entrantes et le nettoyage de cible obsolète.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:47` liste `whatsapp-approval-exec-native` et `whatsapp-approval-plugin-native`.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:676` gère la demande d'approbation, la décision, et la correspondance de message en direct.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.test.ts:167` vérifie que les scénarios d'approbation natif sont sélectionnables en dehors de l'ensemble par défaut.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.test.ts:194` vérifie que la config active les approbations natives pour les scénarios d'approbation.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-native.test.ts:1` couvre le comportement du routage d'approbation natif.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-handler.runtime.test.ts:1` couvre le comportement de livraison, mise à jour, liaison, déliaison, et annulation à l'exécution.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-auth.test.ts:1` couvre l'autorisation d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-reactions.test.ts:1` couvre la résolution de décision de réaction et les cibles persistantes.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/reaction-level.test.ts:1` couvre le comportement du niveau de réaction.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp native approval reaction exec plugin" --json`

Résultats :

- A surfacé uniquement du bruit de formatage d'approbation iMessage adjacent, pas un défaut d'approbation WhatsApp direct.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp native approval reaction exec plugin" --limit 5`

Résultats :

- A retourné la discussion des mainteneurs et la PR #86735 autour de la centralisation de la logique de réaction d'approbation dans plugin-sdk pour les canaux avec approbations de réaction, y compris WhatsApp.
