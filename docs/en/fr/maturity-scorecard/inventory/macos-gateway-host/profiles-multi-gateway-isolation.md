---
title: "macOS Gateway host - Profiles and Isolation Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# macOS Gateway host - Profiles and Isolation Maturity Note

## Résumé

Les profils et l'isolation multi-Gateway sont documentés et implémentés pour les opérateurs macOS qui exécutent un bot de secours ou des instances Gateway intentionnellement isolées. La documentation couvre les racines d'état/config/workspace spécifiques au profil, les ports dérivés, les étiquettes de service et les vérifications rapides. Le code source et les tests couvrent les étiquettes LaunchAgent spécifiques au profil et le comportement de l'environnement de service.

La couverture est Beta car il y a moins de preuves en direct d'isolation de profil macOS que de preuves de mode local Gateway unique. La qualité est Stable car le modèle est explicite et conservateur : un Gateway est recommandé par défaut, les profils étant réservés à l'isolation intentionnelle.

## Portée de la catégorie

Inclus dans cette catégorie :

- Étiquettes LaunchAgent spécifiques au profil : Étiquettes LaunchAgent spécifiques au profil et chemins plist
- Racines d'état/config/workspace spécifiques au profil : Racines d'état, de config et de workspace spécifiques au profil pour les Gateways locaux isolés.
- Ports dérivés : Ports dérivés et évitement des conflits multi-Gateway
- Configuration du bot de secours : Configuration du bot de secours et vérifications de l'opérateur
- Détection de processus Gateway supplémentaires : Détection d'état approfondie pour les services de type Gateway supplémentaires et les processus locaux en double.

## Fonctionnalités

- Étiquettes LaunchAgent spécifiques au profil : Étiquettes LaunchAgent spécifiques au profil et chemins plist
- Racines d'état/config/workspace spécifiques au profil : Racines d'état, de config et de workspace spécifiques au profil pour les Gateways locaux isolés.
- Ports dérivés : Ports dérivés et évitement des conflits multi-Gateway
- Configuration du bot de secours : Configuration du bot de secours et vérifications de l'opérateur
- Détection de processus Gateway supplémentaires : Détection d'état approfondie pour les services de type Gateway supplémentaires et les processus locaux en double.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : la documentation, la source d'étiquette launchd, les tests d'environnement de service, les tests de journal de redémarrage et le support de couverture e2e multi-Gateway soutiennent le modèle de profil prévu.
- Signaux négatifs : la preuve de profil est principalement orientée CLI/runtime, pas un flux de travail d'application macOS empaquetée avec plusieurs LaunchAgents gérés par l'application.
- Lacunes d'intégration : besoin de preuve en direct pour deux LaunchAgents de profil macOS, ports/état/config isolés, journaux séparés et ciblage d'application/opérateur propre.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : `multiple gateways macOS profile launchd port isolation rescue bot` n'a retourné aucun résultat ouvert.
- Rapports Discrawl : `multiple gateways profile rescue bot` a retourné des conseils utilisateur selon lesquels un Gateway est généralement suffisant, les gateways supplémentaires doivent être des configurations de secours/isolation intentionnelles, et la documentation a mis en avant un démarrage rapide du bot de secours.
- Bonnes qualités : la documentation décourage l'utilisation occasionnelle de multi-Gateway, le code source crée des étiquettes spécifiques au profil, les tests affirment les étiquettes/journaux spécifiques au profil, et la page multi-Gateways fournit une liste de contrôle d'isolation pratique.
- Mauvaises qualités : l'opération multi-Gateway augmente la charge de l'opérateur autour des ports, des plages CDP/navigateur, des noms de profil, des étiquettes de service et du ciblage.
- Exclu de la qualité : Les preuves uniquement liées à la couverture ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score d'exhaustivité

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les étiquettes LaunchAgent spécifiques au profil, les racines d'état/config/workspace spécifiques au profil, les ports dérivés, la configuration du bot de secours, la détection de processus Gateway supplémentaires.
- Signaux négatifs : la note archivée a précédé le score d'exhaustivité Completeness process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario d'isolation de profil macOS en direct avec deux LaunchAgents et deux plages de ports.
- Ajouter une sélection de profil orientée application ou des limites plus claires si l'application est destinée à gérer un seul Gateway local à la fois.
- Rendre les avertissements d'état approfondi pour les services supplémentaires plus faciles à mapper aux étiquettes de profil.

## Preuves

### Documentation

- `docs/gateway/multiple-gateways.md:9` : indique que la plupart des configurations ont besoin d'un Gateway et introduit l'utilisation du bot de secours/profil.
- `docs/gateway/multiple-gateways.md:24` : fournit un démarrage rapide du bot de secours.
- `docs/gateway/multiple-gateways.md:47` : documente les racines d'état/config/workspace/service par profil.
- `docs/gateway/multiple-gateways.md:78` : documente la configuration générale multi-Gateway.
- `docs/gateway/multiple-gateways.md:117` : documente la liste de contrôle d'isolation et les ports dérivés.
- `docs/gateway/multiple-gateways.md:158` : documente les vérifications rapides.
- `docs/gateway/index.md:152` : documente la liste de contrôle multi-Gateway à partir de la documentation principale du Gateway.
- `docs/cli/gateway.md:323` : documente les avertissements de sonde et la détection multi-Gateway.

### Code source

- `src/daemon/launchd.ts:111` : dérive les étiquettes LaunchAgent et les chemins plist, y compris les variantes spécifiques au profil.
- `src/daemon/launchd.ts:127` : dérive les chemins du répertoire/fichier/wrapper env.
- `src/daemon/service.ts:173` : lit l'état du service pour le profil/service sélectionné.
- `src/config/paths.ts:56` : résout les racines d'état utilisées par les instances Gateway spécifiques au profil.
- `src/config/paths.ts:151` : résout les chemins de config utilisés par les instances Gateway spécifiques au profil.
- `src/config/paths.ts:331` : résout les valeurs par défaut et les remplacements de port Gateway.

### Tests d'intégration

- `test/gateway.multi.e2e.test.ts:27` : lance deux instances Gateway et valide les hooks HTTP et l'appairage de nœud WebSocket.
- `scripts/e2e/parallels/macos-smoke.ts:923` : exécute l'état approfondi sur macOS, pertinent pour détecter la dérive de service/port bien que pas une voie multi-profil.

### Tests unitaires

- `src/daemon/service-env.test.ts:676` : vérifie le comportement de l'étiquette LaunchAgent/unité de service spécifique au profil.
- `src/daemon/service-env.test.ts:715` : vérifie le comportement de l'étiquette launchd spécifique au profil.
- `src/daemon/restart-logs.test.ts:39` : vérifie les journaux LaunchAgent macOS sous `~/Library/Logs/openclaw`.
- `src/daemon/restart-logs.test.ts:54` : vérifie les chemins de journal de redémarrage conscients du profil.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "multiple gateways macOS profile launchd port isolation rescue bot" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "multiple gateways profile rescue bot"
```

Résultats :

- Retourné le miroir PR #69803 du 21 avril 2026 pour la documentation mettant en avant le démarrage rapide du bot de secours.
- Retourné des conseils de support selon lesquels un Gateway est généralement suffisant et plusieurs Gateways sont pour les configurations de secours ou d'isolation intentionnelles.
- Retourné une explication de support de mars 2026 sur les avantages d'isolation et les coûts de conflit de port.
