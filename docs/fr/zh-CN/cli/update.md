---
read_when:
  - 你想安全地更新源码检出
  - 你需要了解 `--update` 简写行为
summary: "`openclaw update` 的 CLI 参考（相对安全的源码更新 + Gateway 网关自动重启）"
title: update
x-i18n:
  generated_at: "2026-02-03T07:45:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3a08e8ac797612c498eef54ecb83e61c9a1ee5de09162a01dbb4b3bd72897206
  source_path: cli/update.md
  workflow: 15
---

# `openclaw update`

Mettez à jour OpenClaw en toute sécurité et basculez entre les canaux stable/beta/dev.

Si vous avez installé via **npm/pnpm** (installation globale, sans métadonnées git), la mise à jour s'effectue via le processus du gestionnaire de paquets décrit dans [Mise à jour](/install/updating).

## Utilisation

```bash
openclaw update
openclaw update status
openclaw update wizard
openclaw update --channel beta
openclaw update --channel dev
openclaw update --tag beta
openclaw update --no-restart
openclaw update --json
openclaw --update
```

## Options

- `--no-restart` : Ignorer le redémarrage du service Gateway après une mise à jour réussie.
- `--channel <stable|beta|dev>` : Définir le canal de mise à jour (git + npm ; persisté dans la configuration).
- `--tag <dist-tag|version>` : Remplacer uniquement pour cette mise à jour le dist-tag npm ou la version.
- `--json` : Afficher le JSON `UpdateRunResult` lisible par machine.
- `--timeout <seconds>` : Délai d'expiration pour chaque étape (par défaut 1200 secondes).

Remarque : La rétrogradation nécessite une confirmation, car les anciennes versions peuvent corrompre la configuration.

## `update status`

Affiche le canal de mise à jour actuel + tag/branche/SHA git (pour les extractions de source), ainsi que la disponibilité des mises à jour.

```bash
openclaw update status
openclaw update status --json
openclaw update status --timeout 10
```

Options :

- `--json` : Afficher le JSON de statut lisible par machine.
- `--timeout <seconds>` : Délai d'expiration de la vérification (par défaut 3 secondes).

## `update wizard`

Processus interactif pour sélectionner le canal de mise à jour et confirmer si Gateway doit redémarrer après la mise à jour (redémarrage par défaut). Si vous sélectionnez `dev` mais n'avez pas d'extraction git, il vous proposera d'en créer une.

## Fonctionnement

Lorsque vous basculez explicitement de canal (`--channel ...`), OpenClaw maintient également la cohérence de la méthode d'installation :

- `dev` → Assure l'existence d'une extraction git (par défaut : `~/openclaw`, peut être remplacée via `OPENCLAW_GIT_DIR`), la met à jour et installe le CLI global à partir de cette extraction.
- `stable`/`beta` → Installe depuis npm avec le dist-tag correspondant.

## Processus d'extraction Git

Canaux :

- `stable` : Extrait le dernier tag non-beta, puis construit + doctor.
- `beta` : Extrait le dernier tag `-beta`, puis construit + doctor.
- `dev` : Extrait `main`, puis fetch + rebase.

Aperçu général :

1. Nécessite un arbre de travail propre (aucune modification non validée).
2. Basculer vers le canal sélectionné (tag ou branche).
3. Récupérer en amont (dev uniquement).
4. Dev uniquement : Pré-vérifier lint + construction TypeScript dans un arbre de travail temporaire ; si le dernier commit échoue, revenir jusqu'à 10 commits en arrière pour trouver la dernière construction propre.
5. Rebase vers le commit sélectionné (dev uniquement).
6. Installer les dépendances (pnpm en priorité ; npm comme alternative).
7. Construire + construire l'interface de contrôle.
8. Exécuter `openclaw doctor` comme vérification finale de « mise à jour sécurisée ».
9. Synchroniser les plugins vers le canal actuel (dev utilise les extensions groupées ; stable/beta utilise npm) et mettre à jour les plugins installés via npm.

## Raccourci `--update`

`openclaw --update` est réécrit en `openclaw update` (pratique pour les scripts shell et de démarrage).

## Voir aussi

- `openclaw doctor` (offre une option pour exécuter d'abord la mise à jour sur une extraction git)
- [Canaux de développement](/install/development-channels)
- [Mise à jour](/install/updating)
- [Référence CLI](/cli)
