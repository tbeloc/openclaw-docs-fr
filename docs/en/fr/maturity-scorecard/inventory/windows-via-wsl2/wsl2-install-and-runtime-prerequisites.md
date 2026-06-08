---
title: "Windows via WSL2 - WSL Setup and Updates Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - WSL Setup and Updates Maturity Note

## Résumé

La préparation à l'installation et à l'exécution de WSL2 est la partie la plus solide de cette surface en dehors de la gestion des services systemd de base. La documentation recommande clairement WSL2 pour Windows, décrit la configuration de WSL2 + Ubuntu, exige systemd pour l'installation du service, et oriente les utilisateurs vers le flux d'installation/démarrage Linux. Le code source contient une détection explicite de WSL/WSL2 et une gestion spécifique à WSL2 de la famille réseau. Le risque restant est la confusion de l'opérateur entre PowerShell natif Windows, les shells WSL, les méthodes d'installation de Node/pnpm, et les flux source/package.

## Portée de la catégorie

Inclus dans cette catégorie :

- Installation de WSL2 + Ubuntu : exigences d'installation de WSL2 et Ubuntu.
- Runtime Node : exigences de runtime Node 24 et Node 22.19+ à l'intérieur de WSL2.
- Flux d'installation Linux à l'intérieur de WSL2 : flux d'installation et de démarrage Linux exécutés à l'intérieur de WSL2.
- Limite de runtime WSL2 : limite de runtime WSL2 et sa distinction par rapport aux installations Windows natives.
- Exigences de famille réseau WSL2 : exigences de famille réseau spécifiques à WSL2 qui affectent le démarrage de la passerelle.
- Installation source et construction à l'intérieur de WSL2 : flux de travail d'installation source et de construction à l'intérieur de la distribution WSL2.
- Mise à jour openclaw : mise à jour openclaw, changement de canal, diagnostics de simulation/statut
- npm/pnpm/git package-root : npm/pnpm/git package-root et changement de mode d'installation
- Redémarrage de passerelle systemd géré : redémarrage de passerelle systemd géré et remise de mise à jour
- Actualisation des métadonnées de service : actualisation des métadonnées de service après les mises à jour de la passerelle WSL2.
- Avertissements du gestionnaire de packages : avertissements du gestionnaire de packages observés à partir des installations source et package WSL2.

## Fonctionnalités

- Installation de WSL2 + Ubuntu : exigences d'installation de WSL2 et Ubuntu.
- Runtime Node : exigences de runtime Node 24 et Node 22.19+ à l'intérieur de WSL2.
- Flux d'installation Linux à l'intérieur de WSL2 : flux d'installation et de démarrage Linux exécutés à l'intérieur de WSL2.
- Limite de runtime WSL2 : limite de runtime WSL2 et sa distinction par rapport aux installations Windows natives.
- Exigences de famille réseau WSL2 : exigences de famille réseau spécifiques à WSL2 qui affectent le démarrage de la passerelle.
- Installation source et construction à l'intérieur de WSL2 : flux de travail d'installation source et de construction à l'intérieur de la distribution WSL2.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : la documentation indique que WSL2 est le chemin Windows recommandé ; des conseils d'installation WSL2 étape par étape existent ; les documents README et de démarrage définissent le plancher Node et le chemin d'intégration du daemon ; le code source détecte WSL/WSL2 et applique le comportement réseau spécifique à WSL2.
- Signaux négatifs : la preuve la plus forte en scénario réel est une sonde WSL2 de runner Windows plus des flux Linux/systemd, et non une exécution d'acceptation WSL2 complète d'installation/intégration/mise à jour.
- Lacunes d'intégration : aucune fiche de pointage WSL2 de première installation de bout en bout n'a été trouvée qui prouve l'installation WSL, l'installation OpenClaw, l'intégration, le service de passerelle, le tableau de bord, la mise à jour et le doctor en une seule exécution.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : `WSL2 install Node openclaw onboard` a retourné le problème ouvert #63740 pour une défaillance de syntaxe source/runtime WSL2, la PR #74163 résumant la lenteur Windows/onboard, et le problème #86612 pour les interactions de chemin Docker/WSL2 et de sandbox.
- Rapports Discrawl : les requêtes d'installation/support WSL2 ont retourné des conseils orientés utilisateur selon lesquels WSL2 est le chemin Windows plus stable, mais aussi une confusion répétée quant à savoir s'il faut exécuter les commandes dans PowerShell ou Ubuntu, la configuration de Node/pnpm, et le comportement de secours Windows natif.
- Bonnes qualités : la documentation est honnête sur le fait que WSL2 est le chemin d'expérience complète recommandé, et le code source sépare la détection WSL du comportement Windows natif au lieu de masquer WSL derrière des chaînes de plateforme.
- Mauvaises qualités : les conseils d'installation s'étendent sur la configuration WSL officielle, les installations de packages, les constructions source, l'activation de systemd, et le contraste Windows natif, ce qui laisse de la place aux utilisateurs pour exécuter la bonne commande dans le mauvais shell.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution sont exclues de ce score de qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/windows-via-wsl2.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'installation de WSL2 + Ubuntu, le runtime Node, le flux d'installation Linux à l'intérieur de WSL2, la limite de runtime WSL2, les exigences de famille réseau WSL2, l'installation source et la construction à l'intérieur de WSL2.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin d'une fiche de pointage WSL2 d'installation/intégration/mise à jour en direct répétée à partir d'une machine ou d'un runner Windows frais.
- Besoin de garde-fous plus explicites lorsque les utilisateurs commencent dans PowerShell natif mais ont l'intention de suivre le chemin WSL2.
- Besoin de documentation ou de diagnostics de première classe pour les performances de l'emplacement de l'espace de travail, en particulier en évitant les travaux source/dev de longue durée sous `/mnt/c/...`.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:10` : WSL2 est le chemin Windows plus stable et exécute CLI, Gateway et les outils à l'intérieur de Linux.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:17` : la section WSL2 lie le démarrage, l'installation/mise à jour et les documents d'installation WSL officiels de Microsoft.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:183` : l'installation WSL2 étape par étape commence par `wsl --install` et la sélection d'Ubuntu.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:198` : systemd WSL est requis pour l'installation de Gateway.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:221` : l'installation d'OpenClaw à l'intérieur de WSL suit le flux source/démarrage Linux.
- `/Users/kevinlin/code/openclaw/docs/start/getting-started.md:15` : Node 24 est recommandé et Node 22.19+ est supporté.
- `/Users/kevinlin/code/openclaw/docs/start/getting-started.md:20` : le démarrage indique aux utilisateurs Windows que WSL2 est plus stable et recommandé.
- `/Users/kevinlin/code/openclaw/README.md:33` : l'intégration fonctionne sur Windows via WSL2 et appelle ce chemin fortement recommandé.

### Source

- `/Users/kevinlin/code/openclaw/src/infra/wsl.ts:11` : la détection WSL vérifie `WSL_INTEROP`, `WSL_DISTRO_NAME` et `WSLENV`.
- `/Users/kevinlin/code/openclaw/src/infra/wsl.ts:22` : la détection WSL de synchronisation vérifie la plateforme Linux plus `/proc/version`.
- `/Users/kevinlin/code/openclaw/src/infra/wsl.ts:40` : la détection WSL2 vérifie l'état WSL plus les marqueurs du noyau tels que `wsl2` et `microsoft-standard`.
- `/Users/kevinlin/code/openclaw/src/infra/net/undici-family-policy.ts:12` : WSL2 désactive la sélection automatique de famille Node pour forcer IPv4 pour l'accessibilité du service hôte Windows.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/.github/workflows/windows-testbox-probe.yml:76` : le flux de travail Windows sonde la disponibilité de WSL2.
- `/Users/kevinlin/code/openclaw/.github/workflows/windows-testbox-probe.yml:127` : le flux de travail peut importer une distribution WSL2 Ubuntu jetable avant de sonder.
- `/Users/kevinlin/code/openclaw/.github/workflows/windows-testbox-probe.yml:142` : le flux de travail exécute les commandes Linux à l'intérieur de la distribution WSL sélectionnée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/infra/wsl.test.ts:62` : les tests unitaires couvrent la détection des variables d'environnement WSL.
- `/Users/kevinlin/code/openclaw/src/infra/wsl.test.ts:71` : les tests unitaires couvrent la détection WSL `/proc/version`.
- `/Users/kevinlin/code/openclaw/src/infra/wsl.test.ts:84` : les tests unitaires couvrent les marqueurs du noyau WSL2.
- `/Users/kevinlin/code/openclaw/src/infra/net/undici-global-dispatcher.test.ts:621` : les tests unitaires prouvent que WSL2 désactive `autoSelectFamily`.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "WSL2 install Node openclaw onboard" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "Windows WSL2 OpenClaw" --mode keyword --limit 12 --json`

Résultats :

- `WSL2 install Node openclaw onboard` a retourné 3 résultats : problème #63740 (`Source code corruption in dist/run-main-*.js`, WSL2 Ubuntu), PR #74163 (actualisation du problème Microsoft incluant la lenteur Windows onboard), et problème #86612 (boucle de redémarrage de passerelle Docker avec contexte de chemin WSL2).
- `Windows WSL2 OpenClaw` a retourné 12 résultats, incluant le verrouillage GPU/pilote WSL2 #86048, la PR de diagnostics d'environnement WSL #58853, le problème de réachabilité WSL/VM #73152, le problème de profil de navigateur WSL #81873, l'arrêt de la passerelle #61616, et plusieurs rapports Windows/WSL2 Control UI/Gateway.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 install Node openclaw onboard"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "Windows WSL2 OpenClaw"`

Résultats :

- La recherche d'installation/intégration WSL2 a retourné 8 résultats, incluant des conseils de support selon lesquels WSL2 est le chemin Windows recommandé, les avertissements d'installation Windows natifs, les rapports d'installation source WSL2, et les conseils de prérequis de première installation.
- La recherche Windows WSL2 OpenClaw a retourné 8 résultats, incluant l'aide utilisateur récente autour de la recommandation WSL2, les questions de forçage du runtime Windows, et les utilisateurs Windows étant orientés vers WSL2 pour une opération stable.
