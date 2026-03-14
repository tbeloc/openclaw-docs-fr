---
read_when:
  - Lors de l'exécution de scripts à partir du référentiel
  - Lors de l'ajout ou de la modification de scripts sous ./scripts
summary: Scripts du référentiel : objectif, portée et considérations de sécurité
title: Scripts
x-i18n:
  generated_at: "2026-02-01T21:38:11Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bfedc3c123c4a43b351f793e2137568786f90732723da5fd223c2a088bc59e43
  source_path: help/scripts.md
  workflow: 15
---

# Scripts

Le répertoire `scripts/` contient des scripts auxiliaires pour les flux de travail locaux et les tâches opérationnelles.
Utilisez ces scripts lorsqu'une tâche est explicitement liée à un script ; sinon, privilégiez l'utilisation de la CLI.

## Conventions

- Les scripts sont **optionnels** sauf s'ils sont référencés dans la documentation ou dans une liste de contrôle de publication.
- Privilégiez l'utilisation de l'interface CLI lorsqu'elle existe (par exemple : pour la surveillance de l'authentification, utilisez `openclaw models status --check`).
- Supposez que les scripts sont liés à un hôte spécifique ; lisez le contenu du script avant de l'exécuter sur une nouvelle machine.

## Script de surveillance de l'authentification

Pour la documentation du script de surveillance de l'authentification, consultez :
[/automation/auth-monitoring](/automation/auth-monitoring)

## Lors de l'ajout de scripts

- Gardez les scripts ciblés et documentés.
- Ajoutez une brève entrée dans la documentation pertinente (créez-en une si elle n'existe pas).
