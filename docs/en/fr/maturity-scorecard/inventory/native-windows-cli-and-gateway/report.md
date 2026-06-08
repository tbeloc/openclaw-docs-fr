---
title: "Rapport de maturité Windows natif"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité Windows natif

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (63%)`
- Complétude : `Alpha (68%)`
- Fonctionnalités LTS : `1/4`

## Résumé

Ce rapport promeut la preuve de maturité archivée `native-windows-cli-and-gateway` de `/Users/kevinlin/tmp/maturity/native-windows-cli-and-gateway` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuve archivée et du registre des lacunes connues, puis jointe au rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                      | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------ | --- | ------------- | ------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [CLI](native-powershell-install-and-cli-entrypoints.md)                        | ✅  | `Beta (72%)`  | `Alpha (66%)` | `Beta (72%)`  | Programme d'installation PowerShell, amorçage Node et gestionnaire de paquets, installation globale npm, lanceur CLI empaqueté, shims de commande Windows, intégration openclaw, configuration de passerelle locale, indicateurs d'installation du démon, limite de configuration native vs WSL                |
| [Gestion de passerelle](native-gateway-foreground-runtime-and-process-control.md) | ❌  | `Alpha (68%)` | `Alpha (62%)` | `Alpha (68%)` | passerelle openclaw, santé/disponibilité du runtime au premier plan, redémarrage/signal spécifique à Windows, mode premier plan non géré, installation de passerelle openclaw, fichiers lanceur de passerelle, statut du runtime de tâche planifiée, secours du dossier de démarrage, statut openclaw, inspection du service Windows, diagnostics post-installation |
| [Réseau](windows-host-networking-portproxy-and-remote-access.md)              | ❌  | `Alpha (58%)` | `Alpha (56%)` | `Alpha (58%)` | réseau hôte Windows natif, portproxy d'interface netsh, sortie de statut et de sonde de passerelle, loopback, LAN et limite WSL                                                                                                                                                                   |
| [Mises à jour](windows-update-restart-handoff-and-package-locks.md)            | ❌  | `Beta (74%)`  | `Alpha (68%)` | `Beta (74%)`  | mise à jour openclaw sur paquet Windows natif, arrêt/redémarrage de passerelle géré, remise de mise à jour détachée, verrous de paquet Windows                                                                                                                                                     |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie fournit complètement l'ensemble de capacités
  spécifiques à la surface. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. CLI

Ancres de recherche : configuration CLI Windows natif, install.ps1, PowerShell, openclaw.cmd, PATHEXT, intégration openclaw, configuration de passerelle locale, installation du démon.

Note de catégorie : [CLI](native-powershell-install-and-cli-entrypoints.md)

Décisions de notation :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (72%)`
- LTS : ✅

Fonctionnalités :

- Programme d'installation PowerShell : chemin et indicateurs du programme d'installation hébergé install.ps1 Windows natif.
- Amorçage Node et gestionnaire de paquets : amorçage Node, Git, pnpm, npm et PATH pour Windows natif.
- Installation globale npm : installation globale npm, installation de vérification git et openclaw.cmd généré.
- Lanceur CLI empaqueté : lanceur CLI openclaw empaqueté, version et points d'entrée doctor.
- Shims de commande Windows : lanceur .cmd Windows, PATHEXT et compatibilité shim du gestionnaire de paquets.
- Intégration openclaw : intégration openclaw et openclaw onboard --non-interactive sur Windows natif
- Configuration de passerelle locale : configuration de passerelle locale, choix d'authentification, gestion de SecretRef de jeton/mot de passe de passerelle et valeurs par défaut de point de terminaison local.
- Indicateurs d'installation du démon : indicateurs d'installation du démon pour l'intégration Windows natif.
- Limite de configuration native vs WSL : limite de configuration entre la passerelle Windows natif et le chemin WSL2 recommandé.

Docs principaux :

- `docs/install/index.md`
- `docs/install/installer.md`
- `docs/platforms/windows.md`
- `docs/start/getting-started.md`
- `docs/cli/onboard.md`

### 2. Gestion de passerelle

Ancres de recherche : passerelle openclaw, runtime au premier plan, gestion des signaux Windows, installation de passerelle openclaw, tâches planifiées, dossier de démarrage, statut openclaw, doctor openclaw, diagnostics de passerelle.

Note de catégorie : [Gestion de passerelle](native-gateway-foreground-runtime-and-process-control.md)

Décisions de notation :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Passerelle openclaw : passerelle openclaw, exécution de passerelle openclaw, statut de passerelle openclaw et comportement du processus au premier plan.
- Santé/disponibilité du runtime au premier plan : santé/disponibilité du runtime au premier plan et cibles de passerelle loopback local
- Redémarrage/signal spécifique à Windows : redémarrage/signal spécifique à Windows et comportement de contrôle de processus
- Mode premier plan non géré : attentes de l'opérateur lors de l'exécution sans tâche planifiée gérée.
- Installation de passerelle openclaw : installation de passerelle openclaw, statut, démarrage, arrêt, redémarrage et comportement de démarrage géré.
- Fichiers lanceur de passerelle : gateway.cmd généré et fichiers lanceur masqués pour le démarrage géré.
- Statut du runtime de tâche planifiée : statut du runtime de tâche planifiée, sélection d'utilisateur de tâche, secours listener/PID et réparation de tâche.
- Secours du dossier de démarrage : secours du dossier de démarrage lorsque le planificateur de tâches n'est pas disponible.
- Statut openclaw : statut openclaw, statut de passerelle openclaw, statut de passerelle --deep et conseils de réparation Windows.
- Inspection du service Windows : inspection du service Windows, analyse du runtime du planificateur de tâches, dossier de démarrage
- Diagnostics post-installation : diagnostics, statut et comportement de réparation attendus après l'installation Windows natif.

Docs principaux :

- `docs/platforms/windows.md`
- `docs/gateway/index.md`
- `docs/cli/gateway.md`
- `docs/cli/doctor.md`

### 3. Réseau

Ancres de recherche : portproxy, statut de passerelle, loopback, LAN.

Note de catégorie : [Réseau](windows-host-networking-portproxy-and-remote-access.md)

Décisions de notation :

- Couverture : `Alpha (58%)`
- Qualité : `Alpha (56%)`
- Complétude : `Alpha (58%)`
- LTS : ❌

Fonctionnalités :

- Réseau hôte Windows natif : liaison d'hôte Windows natif et comportement d'exposition de passerelle.
- Portproxy d'interface netsh : portproxy d'interface netsh, règles du pare-feu Windows et actualisation IP WSL
- Sortie de statut et de sonde de passerelle : statut de passerelle et sortie de sonde qui aident les opérateurs à vérifier le réseau Windows.
- Limites loopback, LAN et WSL : limites entre les modes d'exposition loopback, LAN et WSL.

Docs principaux :

- `docs/platforms/windows.md`
- `docs/gateway/index.md`
- `docs/cli/gateway.md`

### 4. Mises à jour

Ancres de recherche : mise à jour openclaw, verrous de paquet, remise de redémarrage.

Note de catégorie : [Mises à jour](windows-update-restart-handoff-and-package-locks.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Mise à jour openclaw sur paquet Windows natif : mises à jour de paquet Windows natif openclaw update
- Arrêt/redémarrage de passerelle géré : arrêt/redémarrage de passerelle géré et actualisation des métadonnées de service lors de la mise à jour
- Remise de mise à jour détachée : remise de mise à jour détachée à partir d'une passerelle en cours d'exécution.
- Verrous de paquet Windows : verrous de paquet Windows, comportement EBUSY/EPERM, échanges par étapes, fenêtre enfant

Docs principaux :

- `docs/install/updating.md`
- `docs/ci.md`

## Interprétation recommandée du tableau de bord

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors de portée pour cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les docs et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/native-windows-cli-and-gateway/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuve archivée :
  `/Users/kevinlin/tmp/maturity/native-windows-cli-and-gateway`.
