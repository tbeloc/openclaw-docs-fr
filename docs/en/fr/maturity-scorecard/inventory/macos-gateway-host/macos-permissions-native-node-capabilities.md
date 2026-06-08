---
title: "Hôte macOS Gateway - Note de maturité des permissions et des capacités natives"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hôte macOS Gateway - Note de maturité des permissions et des capacités natives

## Résumé

Les permissions macOS et les capacités natives des nœuds sont implémentées, mais c'est le composant le plus faible de la surface de l'hôte macOS Gateway. L'application dispose de gestionnaires de permissions explicites pour l'accessibilité, AppleScript, l'enregistrement d'écran, l'audio, la caméra, la parole, la localisation, les notifications et la mise en éveil vocal. La documentation explique les capacités des nœuds et la posture de sécurité. La piste de preuve en direct est plus mince, et les preuves d'archive montrent des lacunes visibles par l'utilisateur autour de la publicité des capacités `screen.record` et `system.run`.

## Portée de la catégorie

Inclus dans cette catégorie :

- Invites et statut des permissions TCC macOS : invites et statut des permissions TCC macOS pour l'accessibilité, AppleScript, l'enregistrement d'écran, le microphone, la reconnaissance vocale, la caméra, la localisation, les notifications et la mise en éveil vocal
- Exposition des capacités natives des nœuds : exposition des capacités natives des nœuds pour les opérations d'écran/canevas/navigateur/système
- Politique system.run : politique system.run et attentes d'exécution des nœuds locaux/distants
- Support piloté par les permissions : support piloté par les permissions et diagnostics des opérateurs

## Fonctionnalités

- Invites et statut des permissions TCC macOS : invites et statut des permissions TCC macOS pour l'accessibilité, AppleScript, l'enregistrement d'écran, le microphone, la reconnaissance vocale, la caméra, la localisation, les notifications et la mise en éveil vocal
- Exposition des capacités natives des nœuds : exposition des capacités natives des nœuds pour les opérations d'écran/canevas/navigateur/système
- Politique system.run : politique system.run et attentes d'exécution des nœuds locaux/distants
- Support piloté par les permissions : support piloté par les permissions et diagnostics des opérateurs

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (62%)`
- Signaux positifs : la documentation, la source PermissionManager de l'application, les tests Swift ciblés et la documentation d'assistance couvrent le comportement prévu des permissions et des capacités.
- Signaux négatifs : les véritables flux TCC macOS sont difficiles à automatiser, et les preuves inspectées n'ont pas montré de preuve de bout en bout pour chaque permission se transformant en la capacité de nœud distant attendue.
- Lacunes d'intégration : `screen.record`, `system.run.prepare`, les approbations d'exécution et l'enregistrement des nœuds distants nécessitent des preuves macOS de pile complète plus solides de l'application au Gateway.

## Score de qualité

- Score : `Beta (73%)`
- Rapports Gitcrawl : `macOS node system.run capability screen recording permissions` a retourné le problème ouvert #57169 pour la capacité d'écran du nœud macOS annoncée tandis que le runtime bloque `screen.record`.
- Rapports Discrawl : `macOS permissions screen recording system.run` a retourné des fils de support de mars et avril où les utilisateurs avaient accordé les permissions macOS mais `system.run` ou `system.run.prepare` était manquant ou rejeté.
- Bonnes qualités : l'application centralise les vérifications de permissions et expose une carte de statut des permissions ; la documentation distingue l'hôte de nœud CLI/sans interface de l'application macOS et souligne la nature sensible à la sécurité de `system.run`.
- Mauvaises qualités : la publicité des capacités et l'état des permissions peuvent diverger du comportement de la liste d'autorisation/politique du runtime, ce qui rend le mode d'échec difficile à raisonner pour les opérateurs.
- Exclu de la qualité : les preuves de couverture uniquement ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score de complétude

- Score : `Alpha (62%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les invites et le statut des permissions TCC macOS, l'exposition des capacités natives des nœuds, la politique system.run, le support piloté par les permissions.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une voie d'application macOS en direct qui accorde ou remplace les permissions TCC et prouve l'enregistrement des capacités des nœuds.
- Rendre les prérequis de `system.run` et la disponibilité de `system.run.prepare` visibles dans les diagnostics de l'application.
- Ajouter une distinction d'opérateur plus claire entre le mode de nœud d'application macOS et le mode d'hôte de nœud CLI/sans interface.

## Preuves

### Documentation

- `docs/platforms/macos.md:52` : documente les capacités des nœuds et l'IPC local pour les opérations macOS natives.
- `docs/platforms/macos.md:77` : documente les approbations d'exécution et le filtrage de l'environnement.
- `docs/platforms/mac/remote.md:84` : documente les permissions distantes et les notes de sécurité pour l'application macOS.
- `docs/platforms/macos.md:141` : documente les permissions d'intégration dans le cadre de la configuration de l'application.

### Source

- `apps/macos/Sources/OpenClaw/PermissionManager.swift:25` : assure les permissions demandées.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:54` : gère les permissions de notification.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:77` : gère l'automatisation AppleScript.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:85` : gère l'accessibilité.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:96` : gère l'enregistrement d'écran.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:104` : gère le microphone.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:122` : gère la reconnaissance vocale.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:134` : gère la caméra.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:152` : gère la localisation.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:177` : gère les permissions de mise en éveil vocal.
- `apps/macos/Sources/OpenClaw/PermissionManager.swift:188` : construit la carte de statut des permissions.

### Tests d'intégration

- `scripts/e2e/parallels/macos-smoke.ts:1006` : vérifie un tour d'agent macOS après la configuration, mais ne prouve pas toutes les permissions natives des nœuds.
- `test/gateway.multi.e2e.test.ts:27` : couvre les contrats d'appairage des nœuds pertinents pour l'enregistrement des capacités des nœuds distants.

### Tests unitaires

- `apps/macos/Tests/OpenClawIPCTests/PermissionManagerLocationTests.swift:5` : couvre le comportement des permissions de localisation.
- `apps/macos/Tests/OpenClawIPCTests/TailscaleIntegrationSectionTests.swift:49` : vérifie l'hydratation de la configuration de l'application sans écraser les paramètres distants existants, pertinent pour la configuration des nœuds distants.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:148` : couvre la construction de commandes SSH distantes pour le mode distant orienté nœud.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "macOS permissions screen recording accessibility system.run gateway node" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

Requête :

```bash
gitcrawl search issues "macOS node system.run capability screen recording permissions" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Problème ouvert #57169 : `[Bug]: macOS node advertises screen capability but runtime blocks screen.record via platform allowlist`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "macOS permissions screen recording system.run"
```

Résultats :

- Retourné un rapport d'assistance d'avril 2026 où un nœud macOS s'est réenregistré mais `system.run` n'apparaissait plus dans les capacités malgré les permissions accordées.
- Retourné des rapports de mars 2026 où `system.run` ou `system.run.prepare` était manquant/rejeté même avec les paramètres d'accessibilité, AppleScript, enregistrement d'écran et approbation d'exécution configurés.
- Retourné des conseils distinguant l'exécution de commandes d'hôte de nœud CLI/sans interface des capacités de caméra/écran/localisation de l'application macOS.
