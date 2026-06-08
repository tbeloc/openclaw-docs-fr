---
title: "Sécurité, authentification, appairage et secrets - Note de maturité pour l'appairage de nœuds, la confiance des capacités et les approbations d'exécution à distance"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de maturité pour l'appairage de nœuds, la confiance des capacités et les approbations d'exécution à distance

## Résumé

OpenClaw dispose d'un modèle de confiance de nœud solide : l'appairage de périphérique de nœud est séparé du `node.pair.*` hérité, l'exposition des commandes de nœud est filtrée jusqu'à l'établissement de la confiance, et les relais `system.run` à distance sont liés au contexte d'approbation. La couverture est Stable car les tests de flux source et serveur exercent l'appairage de nœud, l'auto-approbation CIDR de confiance, l'autorisation d'appairage de périphérique et la liaison d'approbation `node.invoke`. La qualité est Alpha car les preuves d'archive récentes incluent des régressions critiques d'exécution à distance et une confusion utilisateur autour de l'appairage de nœud, des mises à niveau de portée et des attentes inefficaces de refus de commande.

## Portée de la catégorie

Cette catégorie couvre l'appairage de nœud/périphérique pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'auto-approbation CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud, le transfert `node.invoke`, la liaison d'approbation `system.run` et les commandes de récupération visibles par l'opérateur pour la confiance de nœud.

## Fonctionnalités

- Appairage de nœud : couvre l'appairage de nœud sur l'appairage de nœud/périphérique pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'auto-approbation CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud, et le comportement connexe d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance.
- Confiance des capacités : couvre la confiance des capacités sur l'appairage de nœud/périphérique pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'auto-approbation CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud, et le comportement connexe d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance.
- Approbations d'exécution à distance : couvre les approbations d'exécution à distance sur l'appairage de nœud/périphérique pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'auto-approbation CIDR de confiance, les limites de confiance de commande/capacité déclarées par le nœud, et le comportement connexe d'appairage de nœud, de confiance de capacité et d'approbations d'exécution à distance.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (83%)`
- Signaux positifs : La documentation d'appairage de passerelle, la documentation de portée d'opérateur et la documentation d'hôte de nœud décrivent les demandes en attente, l'émission de jetons, l'expiration d'appairage, les limites d'auto-approbation, le contrôle de commande et les exigences d'administrateur pour les nœuds compatibles avec l'exécution. Les tests de flux serveur couvrent l'autorisation d'appairage de nœud, l'auto-approbation, l'approbation d'appairage de périphérique, la rotation de jetons et les régressions de contournement d'approbation.
- Signaux négatifs : La couverture est la plus forte autour des tests de flux passerelle/serveur. La preuve de topologie multi-hôte réelle pour Docker, Tailscale en espace utilisateur, les services de nœud macOS/Linux et l'UX de mise à niveau de commande de nœud est plus mince que la surface d'intégration locale.
- Lacunes d'intégration : Ajouter un test de fumée de version récurrente pour un nœud distant réel via Tailscale/Docker, une approbation explicite de mise à niveau de portée, une politique de refus/autorisation de commande de nœud et l'exécution d'approbation `system.run.prepare` plus `system.run` sur l'hôte de nœud.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : La requête de problème exacte ci-dessous n'a retourné aucune ligne directe, mais la requête de RP appariée a trouvé un travail de durcissement ouvert pour une porte de chemin de refus. Les anciennes RP de sécurité fermées dans l'archive Discord montrent l'exposition de commande de nœud avant l'approbation d'appairage et l'exposition d'exécution d'appairage de périphérique uniquement.
- Rapports Discrawl : La recherche Discord spécifique à la fonctionnalité a trouvé une confusion utilisateur/opérateur concernant l'appairage de nœud via Docker/Tailscale en espace utilisateur, la récupération `PAIRING_REQUIRED`, `AUTH_TOKEN_MISMATCH`, les détails de mise à niveau de portée et les discussions de RP de durcissement critique `node.invoke`.
- Bonnes qualités : L'auto-approbation de nœud est étroite, l'exposition de commande est limitée par l'état d'appairage et la politique de nœud global, les portées d'opérateur distinguent `operator.pairing` de `operator.admin`, et la liaison d'approbation lie les exécutions de nœud dangereuses au contexte d'exécution concret.
- Mauvaises qualités : Le dossier d'incident vécu inclut des contournements d'exécution à distance graves, les utilisateurs frappent toujours des cas limites de proxy/localité, et les conseils d'opérateur autour des demandes de nœud en attente par rapport aux demandes de périphérique en attente restent faciles à confondre.
- Exclu de la qualité : La largeur de couverture, la largeur des tests unitaires et la profondeur des tests d'intégration sont notées uniquement sous Couverture.

## Score de complétude

- Score : `Stable (83%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour l'appairage de nœud, la confiance des capacités, les approbations d'exécution à distance.
- Signaux négatifs : la note archivée a précédé la notation de complétude de version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du dossier de lacune connu utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'appairage de nœud sur réseau réel a toujours une variance opérationnelle élevée autour des proxies, des adresses de pont Docker, de la mise en réseau Tailscale en espace utilisateur et des ID de demande en attente obsolètes.
- Le refus de commande de nœud est une politique de nom de commande exacte, pas un filtrage de charge utile shell ; les utilisateurs relisent à plusieurs reprises cette limite.
- Des contrôles de refus difficiles supplémentaires pour les chemins dangereux sont toujours suivis comme un travail actif.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/pairing.md` documente l'appairage de nœud détenu par la passerelle, les demandes en attente, l'émission de jetons, le contrôle de commande, l'auto-approbation CIDR de confiance, l'auto-approbation de mise à niveau de métadonnées et le stockage sous `~/.openclaw/nodes`.
- `/Users/kevinlin/code/openclaw/docs/channels/pairing.md` documente l'appairage de périphérique de nœud WS, les limites d'amorçage du code de configuration, `devices approve`, les limites de portée de jetons de nœud et l'auto-approbation CIDR de confiance.
- `/Users/kevinlin/code/openclaw/docs/gateway/operator-scopes.md` documente les vérifications de portée au moment de l'approbation d'appairage de nœud et les exigences d'administrateur pour les listes de commandes compatibles avec l'exécution.
- `/Users/kevinlin/code/openclaw/docs/cli/approvals.md` et `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md` documentent la gestion des approbations d'exécution de passerelle/nœud.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/node-pairing-auto-approve.ts` restreint l'auto-approbation CIDR de confiance aux demandes fraîches `role=node` sans portées, sans marqueurs de navigateur/interface utilisateur de contrôle/WebChat et avec des preuves de source de confiance sans boucle locale.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/devices.ts` possède l'approbation de périphérique, la révocation, la rotation et le comportement de demande en attente.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/nodes.ts` gère l'énumération de nœud et le transfert `node.invoke`.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.ts` valide la liaison d'approbation pour le `system.run` de nœud distant.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run-plan.ts` lie le répertoire de travail canonique, l'exécutable et les opérandes de script mutables avant l'exécution soutenue par approbation.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server.node-pairing-authz.test.ts` couvre le comportement d'autorisation d'appairage de nœud.
- `/Users/kevinlin/code/openclaw/src/gateway/server.node-pairing-auto-approve.test.ts` couvre l'auto-approbation de nœud CIDR de confiance via la surface serveur.
- `/Users/kevinlin/code/openclaw/src/gateway/server.node-invoke-approval-bypass.test.ts` couvre le comportement historique de contournement d'approbation `node.invoke`.
- `/Users/kevinlin/code/openclaw/src/gateway/server.device-pair-approve-authz.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server.device-token-rotate-authz.test.ts` couvrent l'approbation de périphérique et l'autorisation de rotation de jetons.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/node-pairing-auto-approve.test.ts` couvre le prédicat d'auto-approbation CIDR de confiance pur.
- `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/node-invoke-system-run-approval-match.test.ts` couvrent la correspondance et la liaison d'approbation.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run-plan.test.ts`, `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run-allowlist.test.ts` et `/Users/kevinlin/code/openclaw/src/node-host/exec-policy.test.ts` couvrent la planification d'exécution côté nœud et la politique.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "node pairing node.invoke system.run approval bypass"`

Résultats :

- A retourné `[]` dans l'archive de problèmes locale actuelle.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "node.invoke approval bypass system.run"`

Résultats :

- A retourné la RP ouverte #81827, `feat(security/exec): add tools.exec.denyPathPatterns hard-deny gate (#74379)`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "node pairing node.invoke system.run approval bypass"`

Résultats :

- N'a retourné aucune ligne visible dans l'archive Discord locale actuelle.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "node pairing approve system.run"`

Résultats :

- A trouvé une sortie de support d'audit de sécurité avertissant que `gateway.nodes.denyCommands` utilise uniquement les noms de commande exacts.
- A trouvé des discussions de RP pour #65543 et #65169 décrivant des correctifs critiques pour l'exposition de commande de nœud d'appairage de périphérique uniquement et l'accessibilité `node.invoke` avant l'approbation d'appairage de nœud.
- A trouvé des conseils d'opérateur selon lesquels l'absence de `system.run.prepare` dans `nodes describe` signifie généralement qu'une demande de nœud en attente ou une mise à niveau de portée a toujours besoin d'approbation.
