---
title: "Native Windows companion app - Desktop Tools and Permissions Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Native Windows companion app - Desktop Tools and Permissions Maturity Note

## Résumé

La branche principale actuelle contient la politique de passerelle pour les nœuds Windows et les commandes de compagnon Windows sûres, mais l'application compagnon Windows native qui annoncerait et exécuterait ces commandes n'est pas présente. Ce composant obtient un crédit de couverture modeste pour la politique d'exécution et les tests autour des paramètres par défaut des nœuds Windows, et non pour une implémentation d'application prise en charge.

## Portée de la catégorie

Inclus dans cette catégorie :

- Identité du nœud Windows : identité du nœud Windows et annonce des capacités.
- Exécution de commandes hôte : exécution de commandes hôte via system.run et les outils de bureau associés.
- Politique de commande de bureau : politique d'autorisation/refus de commande de bureau pour les outils Windows natifs.
- Invites d'approbation d'application : invites d'interface utilisateur d'application pour les commandes de bureau sensibles à l'approbation.
- Capture d'écran et de médias : capture d'instantané d'écran, enregistrement et affordances de capture de médias natifs.
- Comportement de l'hôte Canvas : comportement de l'hôte Canvas et A2UI dans une application compagnon Windows native.
- Intégrations de shell Windows : intégrations de shell Windows et de style PowerToys pour le bureau.
- Secrets d'application : secrets d'application, persistance des jetons, IPC local sécurisé, identité de signature d'application, posture d'autorisation AppContainer ou de bureau
- ACL Windows : ACL Windows et hygiène du système de fichiers pour l'état détenu par l'application
- Approbation de commande : approbation de commande et gating de capacité dangereuse tel que présenté aux utilisateurs

## Fonctionnalités

- Identité du nœud Windows : identité du nœud Windows et annonce des capacités.
- Exécution de commandes hôte : exécution de commandes hôte via system.run et les outils de bureau associés.
- Politique de commande de bureau : politique d'autorisation/refus de commande de bureau pour les outils Windows natifs.
- Invites d'approbation d'application : invites d'interface utilisateur d'application pour les commandes de bureau sensibles à l'approbation.
- Capture d'écran et de médias : capture d'instantané d'écran, enregistrement et affordances de capture de médias natifs.
- Comportement de l'hôte Canvas : comportement de l'hôte Canvas et A2UI dans une application compagnon Windows native.
- Intégrations de shell Windows : intégrations de shell Windows et de style PowerToys pour le bureau.
- Secrets d'application : secrets d'application, persistance des jetons, IPC local sécurisé, identité de signature d'application, posture d'autorisation AppContainer ou de bureau
- ACL Windows : ACL Windows et hygiène du système de fichiers pour l'état détenu par l'application
- Approbation de commande : approbation de commande et gating de capacité dangereuse tel que présenté aux utilisateurs

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (12%)`
- Signaux positifs : la politique de nœud de passerelle a des paramètres par défaut Windows explicites pour les commandes de compagnon sûres et les portes de médias dangereuses.
- Signaux négatifs : aucun runtime de nœud compagnon Windows, courtier de commande, interface utilisateur d'invite, socket d'application ou chemin d'approbation d'exécution hébergé par l'application n'est présent dans la branche principale actuelle.
- Lacunes d'intégration : aucun `system.run` médiatisé par l'application, invite d'approbation, autorisation/refus de commande ou flux de résultat de commande ne peut être exercé via une application Windows prise en charge.

Étiquettes de couverture :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Experimental (40%)`
- Rapports Gitcrawl : `#74163` suit les problèmes de nœud/processus Windows ; `#81673` référence le travail de suite compagnon/barre système/empaquetage de nœud.
- Rapports Discrawl : `#71876` le miroir GitHub dit que les nœuds Windows ont été traités comme des hôtes d'exécution Linux/sans tête et les commandes de compagnon d'application sûres ont été filtrées jusqu'à ce que le travail de politique aborde la liste d'autorisation par défaut ; `#71884` ouvert pour autoriser les commandes de nœud compagnon Windows sûres.
- Bonnes qualités : la politique de passerelle distingue les commandes Windows sûres des commandes de médias dangereuses et échoue fermée pour les commandes à haut risque.
- Mauvaises qualités : l'exécution réelle de l'application, les invites, l'IPC et l'expérience utilisateur de l'opérateur sont en dehors de la source prise en charge actuelle.
- Exclu de la qualité : les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer la qualité.

Étiquettes de qualité :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture de test unitaire, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'exhaustivité

- Score : `Experimental (12%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-companion-app.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'identité du nœud Windows, l'exécution de commandes hôte, la politique de commande de bureau, les invites d'approbation d'application, la capture d'écran et de médias, le comportement de l'hôte Canvas, les intégrations de shell Windows, les secrets d'application, l'ACL Windows, l'approbation de commande.
- Signaux négatifs : la note archivée a précédé la notation d'exhaustivité de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune source de runtime de nœud compagnon Windows ou IPC d'application n'existe dans la branche principale actuelle.
- Aucune interface utilisateur d'approbation d'exécution d'application Windows, socket local/courtier ou persistance d'invite.
- Aucune guidance d'application prise en charge n'explique comment les commandes de nœud Windows déclarées doivent être examinées ou réappairées.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/nodes/index.md` documente le comportement général des nœuds.
- `/Users/kevinlin/code/openclaw/docs/tools/exec.md` et `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md` documentent les concepts d'exécution et d'approbation, mais pas une implémentation d'application compagnon Windows.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md` ne documente pas le comportement du nœud hôte de l'application Windows.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/node-command-policy.ts:64-73` définit les commandes de nœud à haut risque.
- `/Users/kevinlin/code/openclaw/src/gateway/node-command-policy.ts:75-105` inclut Windows dans les paramètres par défaut de la plateforme avec liste de caméras, localisation, appareil, système et commandes d'instantané d'écran.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-misc.test.ts:879-902` affirme que les commandes de compagnon Windows sûres sont autorisées tandis que les commandes de médias dangereuses restent bloquées.
- Aucun runtime de nœud compagnon Windows n'a été trouvé.

### Tests d'intégration

- Aucun test d'intégration de nœud compagnon Windows pris en charge n'a été trouvé.
- Les tests de nœud de passerelle et d'exécution adjacents existent en dehors de la surface de l'application.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/gateway-misc.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/node-command-policy.test.ts`
- `/Users/kevinlin/code/openclaw/src/infra/exec-approvals.test.ts`
- `/Users/kevinlin/code/openclaw/src/infra/system-run-approval-binding.test.ts`

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows node default allowlist companion commands" --json`
- `gitcrawl search openclaw/openclaw --query "safe Windows companion commands" --json`

Résultats :

- `#74163` PR ouvert incluant les problèmes de nœud/processus Windows.
- `#81673` mentionne la portée de la suite compagnon Windows/barre système/empaquetage de nœud via les résultats de requête associés.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows node default allowlist companion commands"`
- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows tray app companion node"`

Résultats :

- `2026-04-26` le miroir GitHub pour `#71876` dit que les nœuds Windows filtraient les commandes de compagnon sûres telles que `canvas.*`, `camera.list`, `location.get` et `screen.snapshot`.
- `2026-04-26` le miroir GitHub pour `#71884` a ouvert une PR pour autoriser les commandes de nœud compagnon Windows sûres.
- `2026-03-13` le miroir GitHub décrit `openclaw/openclaw-windows-node` comme une suite compagnon Windows avec application de barre système, bibliothèque partagée, nœud et extension PowerToys.
