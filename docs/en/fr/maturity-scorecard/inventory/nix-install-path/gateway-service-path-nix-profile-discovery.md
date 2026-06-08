---
title: "Chemin d'installation Nix - Note de Maturité du Runtime de Service et des Guards"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Note de Maturité du Runtime de Service et des Guards

## Résumé

OpenClaw dispose d'un support source pour injecter les binaires de profil Nix dans les PATHs de service de passerelle et de la documentation expliquant la précédence de `NIX_PROFILES`. C'est important pour les outils installés via Nix utilisés par les plugins et les sous-processus de passerelle. Le composant reste expérimental car les preuves se concentrent sur les fonctions de construction de chemin et l'historique d'archive montre que les problèmes de PATH de service continuent d'apparaître dans les flux de travail des opérateurs.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Découverte du PATH du profil Nix : Couvre la découverte du PATH du profil Nix sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Précédence du profil : Couvre la précédence du profil sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Repli du PATH du service : Couvre le repli du PATH du service sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Limites binaires de confiance : Couvre les limites binaires de confiance sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Refus d'écriture de configuration : Couvre le refus d'écriture de configuration sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Refus de réparation du docteur : Couvre le refus de réparation du docteur sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Transfert de mise à jour : Couvre le transfert de mise à jour sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Transfert du cycle de vie du service : Couvre le transfert du cycle de vie du service sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.

## Fonctionnalités

- Découverte du PATH du profil Nix : Couvre la découverte du PATH du profil Nix sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Précédence du profil : Couvre la précédence du profil sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Repli du PATH du service : Couvre le repli du PATH du service sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Limites binaires de confiance : Couvre les limites binaires de confiance sur la gestion de `NIX_PROFILES`, le repli `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd, et les règles adjacentes de résolution binaire sécurisée.
- Refus d'écriture de configuration : Couvre le refus d'écriture de configuration sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Refus de réparation du docteur : Couvre le refus de réparation du docteur sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Transfert de mise à jour : Couvre le transfert de mise à jour sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Transfert du cycle de vie du service : Couvre le transfert du cycle de vie du service sur `openclaw setup`, les modes réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Expérimental (38%)`
- Signaux positifs : Les tests unitaires couvrent le repli Linux, l'ordre de `NIX_PROFILES`, l'omission par défaut macOS, l'inclusion explicite macOS, et la précédence multi-profil.
- Signaux négatifs : Aucun test ne démarre un vrai service launchd/systemd produit par un module Nix et ne vérifie l'exécution de commandes via le PATH résultant.
- Lacunes d'intégration : Aucune preuve de shell-out de passerelle/plugin en direct n'a été trouvée pour les binaires gérés par Nix dans les environnements de service.

## Score de Qualité

- Score : `Expérimental (45%)`
- Rapports Gitcrawl : `nix profile` a retourné la PR `#85238` concernant l'inclusion des bins pnpm 11 dans le PATH de la passerelle, montrant que la surface du PATH du service reste un domaine de support actif.
- Rapports Discrawl : L'archive Discord inclut des commentaires de bot GitHub autour de la PR `#59935`, incluant une discussion d'examen sur le comportement moderne du repli du profil Nix et la supersession ultérieure.
- Bonnes qualités : La construction du PATH préserve la précédence de droite à gauche de Nix et évite de faire confiance à `NIX_PROFILES` arbitraire dans le résolveur binaire sécurisé séparé.
- Mauvaises qualités : Le repli documente et implémente toujours le `~/.nix-profile/bin` hérité, tandis que l'examen d'archive a soulevé des préoccupations concernant les chemins de profil plus récents.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Expérimental (38%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la découverte du PATH du profil Nix, la précédence du profil, le repli du PATH du service, les limites binaires de confiance, le refus d'écriture de configuration, le refus de réparation du docteur, le transfert de mise à jour, le transfert du cycle de vie du service.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucune preuve de service installé ne valide le comportement documenté de launchd/systemd.
- Les emplacements de profil Nix modernes au-delà de `~/.nix-profile/bin` nécessitent une interprétation de support prudente.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/nix.md:87` à `:95` documente la découverte du PATH du service, la précédence de droite à gauche de `NIX_PROFILES`, le repli vers `~/.nix-profile/bin`, et l'applicabilité à launchd macOS et systemd Linux.

### Source

- `/Users/kevinlin/code/openclaw/src/daemon/service-env.ts:198` à `:214` implémente la logique du PATH du profil Nix et la précédence de droite à gauche de `NIX_PROFILES`.
- `/Users/kevinlin/code/openclaw/src/daemon/service-env.ts:277` à `:320` câble les bins du profil Nix Home Manager dans la construction du PATH du service macOS et Linux.
- `/Users/kevinlin/code/openclaw/src/infra/resolve-system-bin.ts:113` à `:116` n'en dérive intentionnellement pas les répertoires de recherche de binaires système de confiance à partir de `NIX_PROFILES` contrôlé par env.

### Tests d'intégration

- Aucune preuve d'intégration launchd/systemd/Home Manager n'a été trouvée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/daemon/service-env.test.ts:357` à `:469` couvre le comportement de repli, omission, `NIX_PROFILES`, et précédence.
- `/Users/kevinlin/code/openclaw/src/infra/resolve-system-bin.test.ts:244` à `:264` vérifie que les entrées `NIX_PROFILES` contrôlées par env et les chemins directs du magasin ne sont pas de confiance par le résolveur binaire système sécurisé.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "NIX_PROFILES" --json`

Résultats :

- A retourné `hits: []`.

Requête :

`gitcrawl search openclaw/openclaw --query "nix profile" --json`

Résultats :

- A retourné la PR `#85238` (`fix: include pnpm 11 bins in gateway PATH`) avec un extrait contenant `~/.nix-profile/bin`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "NIX_PROFILES"`

Résultats :

- Le message du bot GitHub du 2026-04-25 a dit que la PR `#44433` a été remplacée par `#59935`, qui a implémenté le support du PATH du service Nix Home Manager avec la couverture de précédence de `NIX_PROFILES`.
- Un commentaire d'examen sur la PR `#59935` a soulevé une préoccupation selon laquelle le repli `~/.nix-profile/bin` peut manquer les emplacements de profil actif Nix plus récents.
- Un autre commentaire d'examen a soutenu que `NIX_PROFILES=""` n'est pas une opération Nix standard et devrait suivre les modèles truthy/falsy des variables env existantes.
