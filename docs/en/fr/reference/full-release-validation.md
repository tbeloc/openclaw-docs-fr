---
summary: "Étapes complètes de validation de version, workflows enfants, profils de version, handles de réexécution et preuves"
title: "Validation complète de la version"
read_when:
  - Exécution ou réexécution de la validation complète de la version
  - Comparaison des profils de validation de version stable et complète
  - Débogage des défaillances d'étape de validation de version
---

`Full Release Validation` est le parapluie de version. C'est le seul point d'entrée manuel pour la preuve de pré-version, mais la plupart du travail se fait dans les workflows enfants afin qu'une boîte défaillante puisse être réexécutée sans redémarrer toute la version.

Exécutez-le à partir d'une référence de workflow de confiance, normalement `main`, et transmettez la branche de version, l'étiquette ou le SHA de commit complet en tant que `ref` :

```bash
gh workflow run full-release-validation.yml \
  --ref main \
  -f ref=release/YYYY.M.D \
  -f provider=openai \
  -f mode=both \
  -f release_profile=stable
```

Les workflows enfants utilisent la référence de workflow de confiance pour le harnais et l'entrée `ref` pour le candidat en cours de test. Cela maintient la nouvelle logique de validation disponible lors de la validation d'une branche de version ou d'une étiquette plus ancienne.

## Étapes de haut niveau

| Étape                 | Détails                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Résolution de la cible     | **Tâche :** `Resolve target ref`<br />**Workflow enfant :** aucun<br />**Prouve :** résout la branche de version, l'étiquette ou le SHA de commit complet et enregistre les entrées sélectionnées.<br />**Réexécution :** réexécutez le parapluie si cela échoue.                                                                                                                                                              |
| Vitest et CI normal  | **Tâche :** `Run normal full CI`<br />**Workflow enfant :** `CI`<br />**Prouve :** graphique CI complet manuel par rapport à la référence cible, y compris les voies Linux Node, les fragments de plugins groupés, les contrats de canal, la compatibilité Node 22, `check`, `check-additional`, la fumée de construction, les vérifications de documentation, les compétences Python, Windows, macOS, l'i18n de l'interface utilisateur de contrôle et Android via le parapluie.<br />**Réexécution :** `rerun_group=ci`. |
| Pré-version du plugin     | **Tâche :** `Run plugin prerelease validation`<br />**Workflow enfant :** `Plugin Prerelease`<br />**Prouve :** vérifications statiques de plugin spécifiques à la version, couverture de plugin agentique, fragments de lot d'extension complets et voies Docker de pré-version de plugin.<br />**Réexécution :** `rerun_group=plugin-prerelease`.                                                                                                       |
| Vérifications de version        | **Tâche :** `Run release/live/Docker/QA validation`<br />**Workflow enfant :** `OpenClaw Release Checks`<br />**Prouve :** fumée d'installation, vérifications de packages multi-OS, suites live/E2E, chunks de chemin de version Docker, acceptation de package, parité QA Lab, matrice live et Telegram live.<br />**Réexécution :** `rerun_group=release-checks` ou un handle de vérifications de version plus étroit.                                |
| Telegram post-publication | **Tâche :** `Run post-publish Telegram E2E`<br />**Workflow enfant :** `NPM Telegram Beta E2E`<br />**Prouve :** preuve Telegram de package publié optionnel lorsque `npm_telegram_package_spec` est défini.<br />**Réexécution :** `rerun_group=npm-telegram`.                                                                                                                                                     |
| Vérificateur de parapluie     | **Tâche :** `Verify full validation`<br />**Workflow enfant :** aucun<br />**Prouve :** revérifie les conclusions d'exécution enfant enregistrées et ajoute les tableaux de tâches les plus lentes des workflows enfants.<br />**Réexécution :** réexécutez uniquement cette tâche après réexécution d'un enfant défaillant au vert.                                                                                                                                                   |

Pour `ref=main` et `rerun_group=all`, un parapluie plus récent remplace un plus ancien. Lorsque le parent est annulé, son moniteur annule tout workflow enfant qu'il a déjà envoyé. Les exécutions de validation de branche de version et d'étiquette ne s'annulent pas mutuellement par défaut.

## Étapes des vérifications de version

`OpenClaw Release Checks` est le plus grand workflow enfant. Il résout la cible une fois et prépare un artefact `release-package-under-test` partagé lorsque les étapes orientées package ou Docker en ont besoin.

| Étape               | Détails                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cible de version      | **Tâche :** `Resolve target ref`<br />**Workflow de support :** aucun<br />**Tests :** référence sélectionnée, SHA attendu optionnel, profil, groupe de réexécution et filtre de suite live ciblé.<br />**Réexécution :** `rerun_group=release-checks`.                                                                                                                                                                           |
| Artefact de package    | **Tâche :** `Prepare release package artifact`<br />**Workflow de support :** aucun<br />**Tests :** empaquette ou résout une tarball candidate et télécharge `release-package-under-test` pour les vérifications orientées package en aval.<br />**Réexécution :** le package affecté, le groupe multi-OS ou live/E2E.                                                                                           |
| Fumée d'installation       | **Tâche :** `Run install smoke`<br />**Workflow de support :** `Install Smoke`<br />**Tests :** chemin d'installation complet avec réutilisation d'image de fumée Dockerfile racine, installation de package QR, fumées Docker racine et passerelle, tests Docker du programme d'installation, fumée d'image du fournisseur global Bun et E2E Docker de plugin groupé rapide.<br />**Réexécution :** `rerun_group=install-smoke`.                                         |
| Multi-OS            | **Tâche :** `cross_os_release_checks`<br />**Workflow de support :** `OpenClaw Cross-OS Release Checks (Reusable)`<br />**Tests :** voies fraîches et de mise à niveau sur Linux, Windows et macOS pour le fournisseur et le mode sélectionnés, en utilisant la tarball candidate plus un package de base.<br />**Réexécution :** `rerun_group=cross-os`.                                                                                                       |
| Repo et E2E live   | **Tâche :** `Run repo/live E2E validation`<br />**Workflow de support :** `OpenClaw Live And E2E Checks (Reusable)`<br />**Tests :** E2E de référentiel, cache live, streaming websocket OpenAI, fragments de fournisseur live natif et de plugin, et harnais de modèle/backend/passerelle live soutenus par Docker sélectionnés par `release_profile`.<br />**Réexécution :** `rerun_group=live-e2e`, optionnellement avec `live_suite_filter`. |
| Chemin de version Docker | **Tâche :** `Run Docker release-path validation`<br />**Workflow de support :** `OpenClaw Live And E2E Checks (Reusable)`<br />**Tests :** chunks Docker de chemin de version par rapport à l'artefact de package partagé.<br />**Réexécution :** `rerun_group=live-e2e`.                                                                                                                                                      |
| Acceptation de package  | **Tâche :** `Run package acceptance`<br />**Workflow de support :** `Package Acceptance`<br />**Tests :** compatibilité de dépendance de canal groupé native d'artefact, fixtures de package de plugin hors ligne et acceptation de package Telegram OpenAI simulé par rapport à la même tarball.<br />**Réexécution :** `rerun_group=package`.                                                                                       |
| Parité QA           | **Tâche :** `Run QA Lab parity lane` et `Run QA Lab parity report`<br />**Workflow de support :** tâches directes<br />**Tests :** packs de parité agentique candidat et de base, puis le rapport de parité.<br />**Réexécution :** `rerun_group=qa-parity` ou `rerun_group=qa`.                                                                                                                                       |
| Matrice live QA      | **Tâche :** `Run QA Lab live Matrix lane`<br />**Workflow de support :** tâche directe<br />**Tests :** profil QA matrice live rapide dans l'environnement `qa-live-shared`.<br />**Réexécution :** `rerun_group=qa-live` ou `rerun_group=qa`.                                                                                                                                                                        |
| Telegram live QA    | **Tâche :** `Run QA Lab live Telegram lane`<br />**Workflow de support :** tâche directe<br />**Tests :** Telegram live QA avec baux de credential Convex CI.<br />**Réexécution :** `rerun_group=qa-live` ou `rerun_group=qa`.                                                                                                                                                                                    |
| Vérificateur de version    | **Tâche :** `Verify release checks`<br />**Workflow de support :** aucun<br />**Tests :** tâches de vérification de version requises pour le groupe de réexécution sélectionné.<br />**Réexécution :** réexécutez après que les tâches enfants ciblées réussissent.                                                                                                                                                                                 |

## Chunks de chemin de publication Docker

L'étape de chemin de publication Docker exécute ces chunks lorsque `live_suite_filter` est
vide :

| Chunk                                                                                       | Couverture                                                                |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `core`                                                                                      | Lanes de fumée de chemin de publication Docker principal.                                   |
| `package-update-openai`                                                                     | Comportement d'installation et de mise à jour du package OpenAI.                             |
| `package-update-anthropic`                                                                  | Comportement d'installation et de mise à jour du package Anthropic.                          |
| `package-update-core`                                                                       | Comportement du package et de la mise à jour indépendant du fournisseur.                           |
| `plugins-runtime-plugins`                                                                   | Lanes d'exécution de plugin qui exercent le comportement du plugin.                     |
| `plugins-runtime-services`                                                                  | Lanes d'exécution de plugin soutenus par un service ; inclut OpenWebUI si demandé. |
| `plugins-runtime-install-a` à `plugins-runtime-install-h`                             | Lots d'installation/exécution de plugin divisés pour la validation de publication parallèle.   |
| `bundled-channels-core`                                                                     | Comportement Docker du canal groupé.                                        |
| `bundled-channels-update-a`, `bundled-channels-update-discord`, `bundled-channels-update-b` | Comportement de mise à jour du canal groupé.                                        |
| `bundled-channels-contracts`                                                                | Vérifications de contrat du canal groupé dans le chemin de publication Docker.             |

Utilisez `docker_lanes=<lane[,lane]>` ciblé sur le workflow live/E2E réutilisable lorsque
un seul lane Docker a échoué. Les artefacts de publication incluent des commandes de réexécution par lane avec réutilisation d'artefacts de package et d'entrées d'image si disponibles.

## Profils de publication

`release_profile` contrôle uniquement l'étendue live/fournisseur dans les vérifications de publication. Il
ne supprime pas l'IC complet normal, la préversion du plugin, l'installation de fumée, l'acceptation du package,
QA Lab, ou les chunks du chemin de publication Docker.

| Profil   | Utilisation prévue                      | Couverture live/fournisseur incluse                                                                                                                                               |
| --------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `minimum` | Fumée critique de publication la plus rapide.   | Chemin live OpenAI/principal, modèles live Docker pour OpenAI, passerelle native principale, profil de passerelle OpenAI native, plugin OpenAI native, et passerelle live Docker OpenAI.               |
| `stable`  | Profil d'approbation de publication par défaut. | `minimum` plus Anthropic, Google, MiniMax, backend, harnais de test live native, backend CLI live Docker, liaison ACP Docker, harnais Codex Docker, et un fragment de fumée OpenCode Go. |
| `full`    | Balayage consultatif large.             | `stable` plus fournisseurs consultatifs, fragments live de plugin, et fragments live de média.                                                                                                  |

## Ajouts réservés à full

Ces suites sont ignorées par `stable` et incluses par `full` :

| Zone                             | Couverture réservée à full                                                              |
| -------------------------------- | ------------------------------------------------------------------------------- |
| Modèles live Docker               | OpenCode Go, OpenRouter, xAI, Z.ai, et Fireworks.                              |
| Passerelle live Docker              | Fragment consultatif pour DeepSeek, Fireworks, OpenCode Go, OpenRouter, xAI, et Z.ai. |
| Profils de fournisseur de passerelle native | Fireworks, DeepSeek, fragments de modèle OpenCode Go complets, OpenRouter, xAI, et Z.ai.  |
| Fragments live de plugin native        | Plugins A-K, L-N, O-Z autre, Moonshot, et xAI.                                 |
| Fragments live de média native         | Groupes audio, musique Google, musique MiniMax, et vidéo A-D.                       |

`stable` inclut `native-live-src-gateway-profiles-opencode-go-smoke` ; `full`
utilise à la place les fragments de modèle OpenCode Go plus larges.

## Réexécutions ciblées

Utilisez `rerun_group` pour éviter de répéter les boîtes de publication non liées :

| Handle              | Portée                                             |
| ------------------- | ------------------------------------------------- |
| `all`               | Toutes les étapes de validation de publication complète.               |
| `ci`                | Enfant IC complet manuel uniquement.                        |
| `plugin-prerelease` | Enfant de préversion de plugin uniquement.                     |
| `release-checks`    | Toutes les étapes de vérification de publication OpenClaw.               |
| `install-smoke`     | Installation de fumée jusqu'aux vérifications de publication.             |
| `cross-os`          | Vérifications de publication multi-OS.                          |
| `live-e2e`          | Validation du chemin de publication Repo/live E2E et Docker. |
| `package`           | Acceptation du package.                               |
| `qa`                | Parité QA plus lanes live QA.                     |
| `qa-parity`         | Lanes de parité QA et rapport uniquement.                  |
| `qa-live`           | Matrice QA live et Telegram uniquement.                |
| `npm-telegram`      | E2E Telegram post-publication optionnel uniquement.          |

Utilisez `live_suite_filter` avec `rerun_group=live-e2e` lorsqu'une suite live a échoué.
Les identifiants de filtre valides sont définis dans le workflow live/E2E réutilisable, y compris
`docker-live-models`, `live-gateway-docker`,
`live-gateway-anthropic-docker`, `live-gateway-google-docker`,
`live-gateway-minimax-docker`, `live-gateway-advisory-docker`,
`live-cli-backend-docker`, `live-acp-bind-docker`, et
`live-codex-harness-docker`.

## Preuves à conserver

Conservez le résumé `Full Release Validation` comme index au niveau de la publication. Il lie
les identifiants d'exécution enfant et inclut les tableaux des tâches les plus lentes. Pour les défaillances, inspectez d'abord le
workflow enfant, puis réexécutez le plus petit handle correspondant ci-dessus.

Artefacts utiles :

- `release-package-under-test` de `OpenClaw Release Checks`
- Artefacts du chemin de publication Docker sous `.artifacts/docker-tests/`
- Acceptation du package `package-under-test` et artefacts d'acceptation Docker
- Artefacts de vérification de publication multi-OS pour chaque OS et suite
- Artefacts de parité QA, Matrice et Telegram

## Fichiers de workflow

- `.github/workflows/full-release-validation.yml`
- `.github/workflows/openclaw-release-checks.yml`
- `.github/workflows/openclaw-live-and-e2e-checks-reusable.yml`
- `.github/workflows/plugin-prerelease.yml`
- `.github/workflows/install-smoke.yml`
- `.github/workflows/openclaw-cross-os-release-checks-reusable.yml`
- `.github/workflows/package-acceptance.yml`
