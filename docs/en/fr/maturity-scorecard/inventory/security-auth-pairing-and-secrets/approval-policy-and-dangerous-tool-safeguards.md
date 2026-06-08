---
title: "Sécurité, authentification, appairage et secrets - Note de Maturité de la Politique d'Approbation et des Protections des Outils"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de Maturité de la Politique d'Approbation et des Protections des Outils

## Résumé

OpenClaw dispose d'une pile d'approbation bien développée pour l'exécution sur l'hôte, les approbations de plugins, les approbations natives des canaux, les approbations nœud-hôte, les listes blanches, la politique de demande et la liaison d'approbation. La couverture est Stable car le comportement d'approbation est exercé sur Gateway, l'hôte nœud, les assistants infra, les flux SDK/plugin et de nombreux plugins de canaux. La qualité est Beta car l'architecture est robuste mais le registre vécu inclut toujours des travaux de durcissement ouverts, des demandes d'authentification plus forte comme TOTP, et une confusion récurrente des opérateurs autour de YOLO, des listes blanches exactes, des bacs sûrs et ce que les approbations protègent ou non.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Politique d'Approbation : Couvre la Politique d'Approbation sur la politique d'approbation d'exécution, les magasins d'approbation locaux à l'hôte, les modes de liste blanche et de demande, les protections des outils dangereux, le routage d'approbation natif/chat, le routage d'approbation de plugin, les décisions d'approbation, la liaison d'approbation et la gestion CLI orientée opérateur.
- Protections des Outils Dangereux : Couvre les Protections des Outils Dangereux sur la politique d'approbation d'exécution, les magasins d'approbation locaux à l'hôte, les modes de liste blanche et de demande, les protections des outils dangereux, le routage d'approbation natif/chat, le routage d'approbation de plugin, les décisions d'approbation, la liaison d'approbation et la gestion CLI orientée opérateur.

## Fonctionnalités

- Politique d'Approbation : Couvre la Politique d'Approbation sur la politique d'approbation d'exécution, les magasins d'approbation locaux à l'hôte, les modes de liste blanche et de demande, les protections des outils dangereux, le routage d'approbation natif/chat, le routage d'approbation de plugin, les décisions d'approbation, la liaison d'approbation et la gestion CLI orientée opérateur.
- Protections des Outils Dangereux : Couvre les Protections des Outils Dangereux sur la politique d'approbation d'exécution, les magasins d'approbation locaux à l'hôte, les modes de liste blanche et de demande, les protections des outils dangereux, le routage d'approbation natif/chat, le routage d'approbation de plugin, les décisions d'approbation, la liaison d'approbation et la gestion CLI orientée opérateur.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (86%)`
- Signaux positifs : La documentation des approbations d'exécution est détaillée ; Gateway et l'hôte nœud appliquent la politique et la liaison d'approbation ; les tests couvrent les classificateurs d'approbation, l'affichage, les filtres de demande, les redirecteurs, les approbations de canaux, les approbations de plugins, la planification nœud-hôte et les appels d'approbation e2e SDK.
- Signaux négatifs : Certaines protections, comme les modèles de chemin de refus dur et l'authentification plus forte de l'approbateur, restent un travail actif plutôt qu'un comportement de version stable.
- Lacunes d'intégration : Ajouter une preuve de scénario récurrente pour l'exécution gateway-hôte, l'exécution nœud-hôte, l'absence d'interface utilisateur, le routage d'approbation natif sur les canaux principaux, le transfert d'approbation de plugin et les transitions de politique de refus/autorisation.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : La requête de problème exacte a retourné le problème ouvert #67440 pour TOTP optionnel sur les approbations d'exécution. La requête PR a retourné la PR ouverte #81827 pour le portail de refus dur `tools.exec.denyPathPatterns`.
- Rapports Discrawl : La recherche exacte n'a retourné aucune ligne visible, mais les résultats Discord d'audit de sécurité plus larges montrent des utilisateurs confondant `gateway.nodes.denyCommands` avec le filtrage de shell et voyant des sorties critiques/avertissement sur les groupes ouverts, les petits modèles non sandboxés et les surfaces activées pour l'exécution.
- Bonnes qualités : Les décisions d'approbation lient le contexte de commande concret, l'alternative de demande échoue fermée par défaut, les approbations de plugin sont séparées des approbations d'exécution et la documentation avertit que les approbations ne sont pas une isolation par utilisateur ou une politique de système de fichiers en lecture seule.
- Mauvaises qualités : La surface de politique est complexe, les défauts YOLO peuvent surprendre les opérateurs, les listes blanches de commandes exactes sont faciles à surestimer et des améliorations supplémentaires de refus dur et d'authentification d'approbateur sont toujours ouvertes.
- Exclu de la qualité : La largeur de couverture, la largeur des tests unitaires et la profondeur des tests d'intégration sont notées uniquement sous Couverture.

## Score de Complétude

- Score : `Stable (86%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la Politique d'Approbation, les Protections des Outils Dangereux.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucune vérification d'approbateur TOTP ou à deux facteurs intégrée n'existe encore pour les approbations d'exécution.
- Le durcissement du chemin de refus est toujours un travail PR actif.
- Les opérateurs ont toujours besoin d'une éducation prudente que la politique d'approbation, la politique de sandbox, la visibilité des outils et l'accès aux canaux sont des couches séparées.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md` documente le modèle de confiance d'approbation d'exécution, les boutons de politique, le comportement de liste blanche, l'alternative de demande, l'évaluation stricte en ligne, le mode YOLO et la liaison d'approbation.
- `/Users/kevinlin/code/openclaw/docs/cli/approvals.md` documente `openclaw approvals` et `openclaw exec-policy`.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-permission-requests.md` documente les approbations de plugin, le comportement de décision, le routage et comment les approbations de plugin diffèrent des approbations d'exécution.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/audit-checks.md` documente les vérifications d'audit d'exécution dangereux, bac sûr, canal ouvert, sandbox, plugin et surface d'outil.

### Source

- `/Users/kevinlin/code/openclaw/src/infra/exec-approvals.ts` implémente la politique d'approbation d'exécution et les assistants de stockage.
- `/Users/kevinlin/code/openclaw/src/node-host/exec-policy.ts`, `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.ts` et `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run-plan.ts` appliquent la politique d'exécution nœud-hôte.
- `/Users/kevinlin/code/openclaw/src/infra/system-run-approval-binding.ts` et `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.ts` lient le contexte d'approbation aux commandes dangereuses.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/plugin-approval.ts` et `/Users/kevinlin/code/openclaw/src/infra/plugin-approvals.ts` implémentent les flux d'approbation de plugin.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-gateway-approval.e2e.test.ts` couvre l'approbation d'exécution gateway-hôte.
- `/Users/kevinlin/code/openclaw/src/gateway/operator-approvals-client.e2e.test.ts` couvre le comportement du client d'approbation opérateur.
- `/Users/kevinlin/code/openclaw/packages/sdk/src/index.e2e.test.ts` couvre les méthodes de liste/réponse d'approbation SDK.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/exec-approvals.test.ts`, `/Users/kevinlin/code/openclaw/extensions/discord/src/exec-approvals.test.ts`, `/Users/kevinlin/code/openclaw/extensions/slack/src/exec-approvals.test.ts` et `/Users/kevinlin/code/openclaw/extensions/matrix/src/exec-approvals.test.ts` couvrent la gestion des approbations de canaux.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/infra/exec-approvals-policy.test.ts`, `/Users/kevinlin/code/openclaw/src/infra/exec-approvals-safe-bins.test.ts`, `/Users/kevinlin/code/openclaw/src/infra/exec-approval-request-filters.test.ts` et `/Users/kevinlin/code/openclaw/src/infra/system-run-approval-context.test.ts` couvrent les éléments internes de la politique d'approbation.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run-plan.test.ts`, `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run-allowlist.test.ts` et `/Users/kevinlin/code/openclaw/src/node-host/exec-policy.test.ts` couvrent la planification nœud-hôte et le comportement de liste blanche.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/plugin-approval.test.ts` et `/Users/kevinlin/code/openclaw/src/plugin-sdk/approval-auth-helpers.test.ts` couvrent le comportement d'approbation de plugin.
- `/Users/kevinlin/code/openclaw/src/acp/approval-classifier.test.ts` couvre la classification d'approbation.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "exec approvals system.run allowlist ask policy sandbox"`

Résultats :

- A retourné le problème ouvert #67440, `[Feature][Security]: Add optional TOTP (authenticator app code) to exec approvals`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "node.invoke approval bypass system.run"`

Résultats :

- A retourné la PR ouverte #81827, `feat(security/exec): add tools.exec.denyPathPatterns hard-deny gate (#74379)`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "exec approvals system.run allowlist ask policy sandbox"`

Résultats :

- N'a retourné aucune ligne visible.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "node pairing approve system.run"`

Résultats :

- A trouvé des sorties d'audit de sécurité avertissant que les entrées `gateway.nodes.denyCommands` sont des noms de commande exacts, pas des filtres de texte shell.
- A trouvé des conseils selon lesquels l'exécution nœud nécessite `system.run.prepare` dans la liste de commandes nœud et les mises à niveau d'approbation/portée nœud en attente en cas d'absence.
