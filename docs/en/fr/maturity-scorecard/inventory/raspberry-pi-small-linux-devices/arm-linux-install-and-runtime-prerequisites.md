---
title: "Raspberry Pi / petits appareils Linux - Note de maturité de configuration et de compatibilité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / petits appareils Linux - Note de maturité de configuration et de compatibilité

## Résumé

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / petits appareils Linux` / `Prérequis d'installation et d'exécution ARM Linux` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Inclus dans cette catégorie :

- Exigences matérielles et système d'exploitation 64 bits : Définit la configuration des exigences matérielles et système d'exploitation 64 bits, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Configuration du runtime Node : Définit la configuration du runtime Node, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Installation et intégration OpenClaw : Définit la configuration de l'installation et de l'intégration OpenClaw, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Vérification au premier lancement : Définit la configuration de la vérification au premier lancement, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Sélection du modèle Pi supporté : Définit la configuration de la sélection du modèle Pi supporté, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Limite ARM 64 bits : Définit la configuration de la limite ARM 64 bits, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Conseils pour appareils non supportés : Définit la configuration des conseils pour appareils non supportés, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Avertissements pour appareils lents : Définit la configuration des avertissements pour appareils lents, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Modes d'installation npm/pnpm/Bun : Définit la configuration des modes d'installation npm/pnpm/Bun, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Détection de l'architecture du programme d'installation : Définit la configuration de la détection de l'architecture du programme d'installation, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Vérifications optionnelles des binaires ARM : Définit la configuration des vérifications optionnelles des binaires ARM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Conseils de secours/compilation : Définit la configuration des conseils de secours/compilation, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.

## Fonctionnalités

- Exigences matérielles et système d'exploitation 64 bits : Définit la configuration des exigences matérielles et système d'exploitation 64 bits, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Configuration du runtime Node : Définit la configuration du runtime Node, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Installation et intégration OpenClaw : Définit la configuration de l'installation et de l'intégration OpenClaw, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Vérification au premier lancement : Définit la configuration de la vérification au premier lancement, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les prérequis de configuration ARM Linux.
- Sélection du modèle Pi supporté : Définit la configuration de la sélection du modèle Pi supporté, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Limite ARM 64 bits : Définit la configuration de la limite ARM 64 bits, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Conseils pour appareils non supportés : Définit la configuration des conseils pour appareils non supportés, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Avertissements pour appareils lents : Définit la configuration des avertissements pour appareils lents, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Modes d'installation npm/pnpm/Bun : Définit la configuration des modes d'installation npm/pnpm/Bun, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Détection de l'architecture du programme d'installation : Définit la configuration de la détection de l'architecture du programme d'installation, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Vérifications optionnelles des binaires ARM : Définit la configuration des vérifications optionnelles des binaires ARM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Conseils de secours/compilation : Définit la configuration des conseils de secours/compilation, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : La documentation Raspberry Pi nomme les modèles supportés, les niveaux de RAM, le système d'exploitation 64 bits, le swap, l'installation de Node 24, l'intégration au premier lancement, les commandes de vérification et les chemins de persistance. Le programme d'installation détecte les variantes Linux ARM et applique les minimums de Node.
- Signaux négatifs : Les limites des Pi 32 bits et plus anciens sont largement documentées plutôt qu'appliquées de bout en bout, et le programme d'installation local-prefix ne supporte que x64 plus la sélection de tarball Node arm64/aarch64.
- Lacunes d'intégration : Le test de fumée du programme d'installation Docker peut s'exécuter sur arm64, mais il n'y a pas de test de fumée de version Raspberry Pi réel récurrent dans les chemins inspectés.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : des problèmes d'installation ARM et de mémoire faible existent, y compris la confusion d'installation globale npm sur Raspberry Pi et les rapports systemd/session Linux arm64.
- Rapports Discrawl : les utilisateurs discutent de l'installation sur Pi 3B+, de l'exécution sur Pi 4 2GB et de la configuration sur des appareils aarch64 tels que Jetson Nano.
- Bonnes qualités : La documentation est pratique et spécifique concernant les modèles Pi, le système d'exploitation 64 bits, le swap et les modèles cloud. Le code source a une détection explicite de l'architecture ARM et des garde-fous de runtime Node.
- Mauvaises qualités : Les limites de support sont partiellement consultatives ; les chemins ARM/32 bits non supportés apparaissent plus tard comme des erreurs de programme d'installation ou de binaire au lieu d'une matrice de support initiale.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct, flux d'exécution et test de fumée manuel.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les exigences matérielles et système d'exploitation 64 bits, la configuration du runtime Node, l'installation et l'intégration OpenClaw, la vérification au premier lancement, la sélection du modèle Pi supporté, la limite ARM 64 bits, les conseils pour appareils non supportés, les avertissements pour appareils lents, les modes d'installation npm/pnpm/Bun, la détection de l'architecture du programme d'installation, les vérifications optionnelles des binaires ARM, les conseils de secours/compilation.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun chemin source inspecté ne mappe chaque génération de Pi et architecture de système d'exploitation à une politique explicite supportée/non supportée.
- Aucun artefact CI étiqueté matériel n'a été trouvé pour Pi 4, Pi 5, Pi Zero ou Pi OS.
- Le support du programme d'installation local-prefix est plus étroit que ce que la documentation Raspberry Pi implique pour les appareils plus anciens ou 32 bits.

## Preuves

### Documentation

- `docs/install/raspberry-pi.md:10-24` décrit une passerelle toujours active sur Raspberry Pi, nomme les niveaux Pi 5 et Pi 4, marque Pi Zero 2 W comme non recommandé et définit le matériel minimum et recommandé.
- `docs/install/raspberry-pi.md:26-33` énumère les prérequis : Pi 4/5 avec 2GB+, stockage, alimentation, réseau, système d'exploitation Raspberry Pi 64 bits ou Debian/Ubuntu ARM64, et 30 minutes.
- `docs/install/raspberry-pi.md:69-88` installe Node 24 via NodeSource et recommande le swap pour 2GB ou moins.
- `docs/install/index.md:10-14` indique Node 24 ou 22.19+ et le support macOS/Linux/Windows.
- `docs/help/faq-first-run.md:158-178` dit que Raspberry Pi peut exécuter Gateway, recommande 2GB+, système d'exploitation 64 bits, Node >=22, et avertit des problèmes de binaires ARM.

### Code source

- `scripts/install.sh:144-150` mappe `arm64`, `aarch64`, `armv7` et `armv6`.
- `scripts/install.sh:1472-1503` applique les assistants de version minimale de Node.
- `scripts/install.sh:1784-1867` installe Node Linux via les gestionnaires de paquets de distribution et les flux de style NodeSource.
- `scripts/install-cli.sh:338-346` supporte uniquement `arm64`/`aarch64` et `x64` pour les installations de tarball local-prefix.
- `src/daemon/runtime-paths.ts:60-62` et `src/daemon/runtime-paths.ts:149-190` résolvent les candidats Node Linux et avertissent en dessous du plancher de Node supporté.

### Tests d'intégration

- `scripts/test-install-sh-docker.sh:16-34` choisit la plateforme de fumée `linux/arm64` sur les hôtes Darwin arm64 et `linux/amd64` en CI.
- `scripts/docker/install-sh-e2e/run.sh:121-144` exécute le programme d'installation et vérifie la version CLI installée.
- `package.json:1735` et `package.json:1738` définissent les scripts e2e et de fumée d'installation.

### Tests unitaires

- Aucun test unitaire du programme d'installation spécifique à Raspberry Pi n'a été trouvé.
- Le comportement du chemin Node et de l'environnement de service du runtime est partiellement couvert par les tests daemon/runtime ailleurs, mais pas avec les fixtures Pi OS.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi ARM aarch64 arm64 Linux install Node openclaw"`

Résultats :

- Aucun thread correspondant retourné pour la requête d'installation large.

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi low memory OpenClaw"`

Résultats :

- Rapports retournés sur les limites de ressources adaptatives pour les appareils ARM/mémoire faible, la surcharge de découverte Raspberry Pi OS arm64, la confusion d'installation globale npm sur Raspberry Pi et la perte d'état de passerelle systemd Linux arm64.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi OpenClaw"`

Résultats :

- Trouvé un utilisateur du 24 mai demandant l'installation d'OpenClaw sur un Pi 3B+ pour l'automatisation WhatsApp et les attentes de mémoire.
- Trouvé un rapport du 21 mai d'un contributeur exécutant OpenClaw sur un Pi 4 2GB.
- Trouvé une messagerie du 19 mai qui nomme Raspberry Pi comme option d'hôte toujours actif.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "aarch64 OpenClaw"`

Résultats :

- Trouvé des threads de configuration/débogage sur des systèmes aarch64, y compris des environnements aarch64 minimaux manquant Git et des utilisateurs vérifiant `uname -m` plus les versions de Node.
