---
title: "Application compagne Linux - Capacités Node-host, Outils Bureau et Note de Maturité des Approbations Exec"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Linux - Capacités Node-host, Outils Bureau et Note de Maturité des Approbations Exec

## Résumé

OpenClaw dispose d'un node host sans interface graphique multiplateforme et d'un riche modèle de node d'application compagne macOS, mais il n'existe pas d'application compagne Linux prise en charge pour fournir des approbations natives en contexte UI ou des invites de capacité bureau. Les preuves archivées incluent un bug d'approbation de node host Linux où l'absence d'une application compagne Linux était directement pertinente.

## Portée de la catégorie

- Identité de node native Linux et publicité de capacité.
- `system.run`, `system.notify`, `system.which`, et approbations médiées par l'application.
- Outils bureau tels que l'écran, la caméra, les notifications, Canvas et l'exécution de commandes locales.
- Surfaces adjacentes hors portée : node host sans interface graphique, mode node d'application compagne macOS, exec Gateway-host.

## Fonctionnalités

- Identité de node native Linux : identité de node native Linux et publicité de capacité
- Exécution de commandes hôte : exécution de commandes hôte via system.run et outils bureau connexes.
- Outils bureau : outils bureau tels que l'écran, la caméra, les notifications, Canvas et l'exécution de commandes locales

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (2%)`
- Signaux positifs : la documentation du node host sans interface graphique et la documentation des approbations exec existent pour l'exécution de commandes multiplateforme.
- Signaux négatifs : aucune application compagne Linux n'existe pour posséder les invites natives, l'exécution de commandes en contexte UI local ou les approbations de capacité bureau.
- Lacunes d'intégration : aucune preuve de capacité node-host d'application compagne Linux ou d'approbation exec médiée par l'application n'existe dans l'arborescence source actuelle.

## Score de qualité

- Score : `Experimental (22%)`
- Rapports Gitcrawl : la requête a retourné des problèmes ouverts pour les approbations TOTP et les courses d'allowlist plus des références de suivi larges ; le problème #47512 décrit spécifiquement l'échec d'approbation de node host Linux en raison de la socket d'approbation d'application compagne Linux manquante.
- Rapports Discrawl : les discussions d'assistance décrivent les permissions de l'application compagne macOS et le comportement de `system.run`, et les utilisateurs Linux/Windows sont dirigés vers le node host sans interface graphique ou d'autres nodes pour les capacités matérielles.
- Bonnes qualités : les modèles d'approbation exec sous-jacents et de node host sans interface graphique sont documentés et conscients de la sécurité.
- Mauvaises qualités : Linux n'a pas d'UX d'approbation médiée par l'application, pas de carte de permission native, pas de propriété de capacité bureau et pas de documentation expliquant comment une future application Linux devrait différer du node host sans interface graphique.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Experimental (2%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'identité de node native Linux, l'exécution de commandes hôte, les outils bureau.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Définir si l'application compagne Linux possède une socket d'approbation UI ou délègue au node host sans interface graphique.
- Définir les noms de capacité Linux, la sémantique de la carte de permission et les invites utilisateur.
- Ajouter une documentation spécifique à l'application pour `system.run`, les notifications, l'écran/caméra/média et le comportement de secours d'approbation.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/nodes/index.md:413` : le node host sans interface graphique est multiplateforme et expose `system.run` / `system.which`.
- `/Users/kevinlin/code/openclaw/docs/nodes/index.md:427` : l'appairage est toujours requis pour les nodes hosts sans interface graphique.
- `/Users/kevinlin/code/openclaw/docs/tools/exec.md:73` : les approbations gateway/node sont contrôlées par `~/.openclaw/exec-approvals.json`.
- `/Users/kevinlin/code/openclaw/docs/tools/exec.md:74` : `node` nécessite un node appairé, une application compagne ou un node host sans interface graphique.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md:38` : si l'UI de l'application compagne n'est pas disponible, les approbations de style invite se replient, refusant par défaut.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md:52` : l'application compagne macOS se présente comme un node avec les commandes Canvas, Camera, Screen et System.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-host-node-phases.ts:104` : l'exec de node nécessite un node appairé.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-host-node-phases.ts:130` : l'exec de node nécessite un node qui supporte `system.run`.
- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.ts:627` : la remise d'exec de l'application macOS est spécifique à l'application ; aucun équivalent Linux n'apparaît dans la source actuelle.
- Aucune source d'hôte d'approbation côté application `apps/linux`, d'hôte d'outil bureau ou d'invite de permission n'existe dans le checkout actuel.

### Tests d'intégration

- Aucun test d'intégration de capacité de node d'application compagne Linux ou d'approbation exec n'a été trouvé.
- Les tests de node host et exec existants exercent le comportement générique gateway/node, pas une UI d'approbation d'application Linux native.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/node-host/invoke-system-run.test.ts` : les tests de node host `system.run` existent pour le comportement générique.
- Aucun test unitaire d'approbation d'application compagne Linux n'a été trouvé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Linux companion system.run exec approvals node host" --mode keyword --limit 8 --json`
- `gitcrawl gh issue view 47512 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,url`

Résultats :

- La requête de fonctionnalité a retourné le problème ouvert #67440 pour TOTP optionnel sur les approbations exec, le problème ouvert #44749 pour le comportement de course d'allowlist et la PR de suivi large #74163 mentionnant les approbations exec du node host sans interface graphique.
- Le problème #47512 est intitulé `nodes run with arguments always denied on Linux node host: SYSTEM_RUN_DENIED: approval requires a stable executable path` ; son corps indique que la racine semble être que `exec-approvals.sock` n'est jamais créée sur Linux et il n'existe pas d'équivalent Linux de l'application compagne macOS pour gérer cette socket.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux companion system.run exec approvals node host"`

Résultats :

- La requête a retourné le problème #47512 avec les détails de refus du node host Linux, une explication d'assistance de l'application compagne macOS comme surface de node/permissions/approbation exec et une réponse d'assistance d'accès matériel expliquant que sans une application compagne native, les utilisateurs devraient utiliser d'autres nodes ou des chemins de node host sans interface graphique.
