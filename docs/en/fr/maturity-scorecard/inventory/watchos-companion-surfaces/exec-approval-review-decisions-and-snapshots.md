---
title: "watchOS companion surfaces - Exec Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Exec Approvals Maturity Note

## Résumé

Le support des approbations exec sur la montre est la fonctionnalité la plus spécifique à watchOS : la montre peut afficher les approbations en attente, demander des snapshots, envoyer des décisions d'autorisation unique ou de refus, et recevoir les mises à jour résolues/expirées. La couverture est Alpha car les tests source et ciblés couvrent le pont, et les preuves d'archive indiquent que les mainteneurs l'utilisent, mais aucun scénario d'approbation de montre en direct reproductible n'est vérifié.

La qualité est Alpha car l'implémentation prend au sérieux la sécurité et la récupération, tandis que la documentation de version/support garde toujours la surface interne.

## Portée de la catégorie

Inclus dans cette catégorie :

- Invite d'approbation exec sur la montre : Invite d'approbation exec sur la montre, snapshot, résoudre, résolu et payloads expirés
- Interface utilisateur de liste/détail d'approbation sur la montre : Interface utilisateur de liste/détail d'approbation sur la montre et boutons de décision
- Mise en cache des invites côté iPhone : Mise en cache des invites côté iPhone, publication des invites de montre, gestion des snapshots et résolution

## Fonctionnalités

- Invite d'approbation exec sur la montre : Invite d'approbation exec sur la montre, snapshot, résoudre, résolu et payloads expirés
- Interface utilisateur de liste/détail d'approbation sur la montre : Interface utilisateur de liste/détail d'approbation sur la montre et boutons de décision
- Mise en cache des invites côté iPhone : Mise en cache des invites côté iPhone, publication des invites de montre, gestion des snapshots et résolution

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (54%)`
- Signaux positifs : Les tests couvrent la présentation d'une invite d'approbation se synchronisant avec la montre, la publication de snapshot demandant les approbations mises en cache en arrière-plan, l'omission de snapshot au premier plan, les ID de récupération en attente, l'effacement des ID de récupération, les chemins de reconnexion conscients de l'arrière-plan, la classification des erreurs obsolètes/indisponibles et le comportement de réinitialisation des tentatives d'invite.
- Signaux négatifs : Aucune preuve en direct n'a été trouvée pour une demande d'approbation exec Gateway réelle livrée à une Apple Watch, examinée sur la montre, résolue via la session opérateur iPhone et reflétée à l'agent.
- Lacunes d'intégration : Besoin d'un scénario d'approbation réel pour l'invite en attente, la demande de snapshot, l'autorisation unique, le refus, l'obsolète/non trouvé, l'indisponible autoriser toujours, le délai d'expiration/expiration, le changement de disponibilité de la montre et le nettoyage des notifications.

## Score de qualité

- Score : `Alpha (64%)`
- Rapports Gitcrawl : `gitcrawl search openclaw/openclaw --query "watch exec approval" --json` n'a pas trouvé d'incident d'implémentation de montre direct ; il a retourné des correspondances génériques de mots-clés exec approval/watch. `gitcrawl search openclaw/openclaw --query "iOS Watch exec approvals" --json` et les recherches de numéro de PR pour les anciens PR de changelog n'ont retourné aucun résultat du magasin gitcrawl actuel.
- Rapports Discrawl : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "exec-approval on my watch"` a trouvé des commentaires de mainteneur du 2026-04-17 disant que l'approbation exec sur la montre est utilisée souvent, plus une préoccupation de sécurité antérieure selon laquelle les notifications push pourraient exposer des informations sensibles et devraient ouvrir l'application/dialogue à la place. `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "watch approval"` a trouvé une discussion selon laquelle l'approbation iOS + montre serait utile une fois publiée.
- Bonnes qualités : L'implémentation évite l'approbation par texte de notification uniquement en maintenant un chemin d'examen structuré dans l'application sur la montre, persiste l'état du pont d'approbation en attente, gère le nettoyage résolu/expiré et supporte la reconnexion consciente de l'arrière-plan pour les chemins d'examen/résolution de la montre.
- Mauvaises qualités : L'approbation sur la montre n'est pas décrite comme un support public. Le texte de commande sensible à la sécurité est toujours une partie essentielle de l'interface utilisateur d'examen de la montre, donc la politique de rédaction/affichage a besoin d'une décision de produit claire avant une version plus large.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (54%)`
- Instructions de surface : évaluées par rapport à `references/completeness/watchos-companion-surfaces.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'invite d'approbation exec sur la montre, l'interface utilisateur de liste/détail d'approbation sur la montre, la mise en cache des invites côté iPhone.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario d'approbation exec de bout en bout utilisant une véritable Apple Watch et une commande nécessitant une approbation.
- Documenter exactement quels détails de commande peuvent apparaître sur la montre et ce qui est retenu des notifications push.
- Ajouter des étapes de runbook publiques/internes pour les approbations en attente qui ne peuvent pas se charger car la session opérateur iPhone est déconnectée.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md` et `docs/tools/exec-approvals-advanced.md` documentent les approbations exec en général, pas l'examen spécifique à la montre.
- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente les flux d'aperçu interne iOS et push, mais pas l'utilisation de l'approbation sur la montre.

### Source

- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawKit/WatchCommands.swift` définit les types de messages d'invite d'approbation exec sur la montre, résoudre, résolu, expiré, snapshot et snapshot-request.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/WatchInboxStore.swift` stocke et met à jour les enregistrements d'approbation de la montre.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/WatchInboxView.swift` rend les écrans de liste/détail d'approbation et les boutons Autoriser une fois/Refuser.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/WatchConnectivityReceiver.swift` analyse les invites d'approbation, les mises à jour résolues/expirées, les snapshots et envoie les payloads de résolution/snapshot-request.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel.swift` met en cache les invites d'approbation, publie les invites/snapshots de montre, gère les événements de résolution de montre, récupère les approbations en attente et résout via `exec.approval.resolve`.

### Tests d'intégration

- Aucun scénario d'approbation de montre en direct n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/NodeAppModelInvokeTests.swift` couvre la synchronisation des invites de montre, le comportement des demandes de snapshot, les ID de récupération en attente, la classification obsolète/indisponible, la reconnexion consciente de l'arrière-plan et la réinitialisation des tentatives.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/ExecApprovalNotificationBridgeTests.swift` couvre l'analyse des notifications d'approbation exec iOS et le nettoyage des push résolus, adjacent à la récupération d'approbation de montre.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "watch exec approval" --json`

Résultats :

- Aucun incident d'implémentation de montre direct actuel ; correspondances génériques de mots-clés exec approval/watch uniquement.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS Watch exec approvals" --json`

Résultats :

- Aucun résultat.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "exec-approval on my watch"`

Résultats :

- Les commentaires de mainteneur du 2026-04-17 indiquent que l'approbation exec sur la montre est utilisée souvent.
- La discussion antérieure du 2026-04-03 a signalé un risque de sécurité provenant de détails sensibles dans les notifications push et un plan pour déplacer l'examen dans une application/dialogue.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "watch approval"`

Résultats :

- La discussion des mainteneurs a présenté l'approbation iOS + montre comme utile une fois l'application publiée.
