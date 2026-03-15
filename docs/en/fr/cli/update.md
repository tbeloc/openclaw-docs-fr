---
summary: "Référence CLI pour `openclaw update` (mise à jour de source sûre + redémarrage automatique de la passerelle)"
read_when:
  - Vous voulez mettre à jour une extraction de source en toute sécurité
  - Vous devez comprendre le comportement du raccourci `--update`
title: "update"
---

# `openclaw update`

Mettez à jour OpenClaw en toute sécurité et basculez entre les canaux stable/beta/dev.

Si vous avez installé via **npm/pnpm** (installation globale, sans métadonnées git), les mises à jour se font via le flux du gestionnaire de paquets dans [Updating](/fr/install/updating).

## Utilisation

```bash
openclaw update
openclaw update status
openclaw update wizard
openclaw update --channel beta
openclaw update --channel dev
openclaw update --tag beta
openclaw update --dry-run
openclaw update --no-restart
openclaw update --json
openclaw --update
```

## Options

- `--no-restart`: ignorer le redémarrage du service Gateway après une mise à jour réussie.
- `--channel <stable|beta|dev>`: définir le canal de mise à jour (git + npm; persisté dans la config).
- `--tag <dist-tag|version>`: remplacer la dist-tag npm ou la version pour cette mise à jour uniquement.
- `--dry-run`: prévisualiser les actions de mise à jour prévues (flux canal/tag/cible/redémarrage) sans écrire la config, installer, synchroniser les plugins ou redémarrer.
- `--json`: imprimer le JSON `UpdateRunResult` lisible par machine.
- `--timeout <seconds>`: délai d'attente par étape (par défaut 1200s).

Remarque: les rétrograder nécessitent une confirmation car les versions plus anciennes peuvent casser la configuration.

## `update status`

Afficher le canal de mise à jour actif + git tag/branche/SHA (pour les extractions de source), plus la disponibilité des mises à jour.

```bash
openclaw update status
openclaw update status --json
openclaw update status --timeout 10
```

Options:

- `--json`: imprimer le JSON de statut lisible par machine.
- `--timeout <seconds>`: délai d'attente pour les vérifications (par défaut 3s).

## `update wizard`

Flux interactif pour choisir un canal de mise à jour et confirmer s'il faut redémarrer la Gateway après la mise à jour (par défaut redémarrer). Si vous sélectionnez `dev` sans extraction git, il propose d'en créer une.

## Ce qu'il fait

Lorsque vous changez explicitement de canaux (`--channel ...`), OpenClaw maintient également la méthode d'installation alignée:

- `dev` → assure une extraction git (par défaut: `~/openclaw`, remplacer avec `OPENCLAW_GIT_DIR`), la met à jour et installe le CLI global à partir de cette extraction.
- `stable`/`beta` → installe depuis npm en utilisant la dist-tag correspondante.

La mise à jour automatique du cœur Gateway (lorsqu'elle est activée via la config) réutilise le même chemin de mise à jour.

## Flux d'extraction git

Canaux:

- `stable`: extraire la dernière balise non-bêta, puis construire + doctor.
- `beta`: extraire la dernière balise `-beta`, puis construire + doctor.
- `dev`: extraire `main`, puis récupérer + rebaser.

Haut niveau:

1. Nécessite un répertoire de travail propre (pas de modifications non validées).
2. Bascule vers le canal sélectionné (balise ou branche).
3. Récupère en amont (dev uniquement).
4. Dev uniquement: vérification préalable lint + construction TypeScript dans un répertoire de travail temporaire; si le sommet échoue, remonte jusqu'à 10 commits pour trouver la construction propre la plus récente.
5. Rebaser sur le commit sélectionné (dev uniquement).
6. Installe les dépendances (pnpm préféré; npm en secours).
7. Construit + construit l'interface utilisateur de contrôle.
8. Exécute `openclaw doctor` comme vérification finale de "mise à jour sûre".
9. Synchronise les plugins avec le canal actif (dev utilise les extensions groupées; stable/beta utilise npm) et met à jour les plugins installés via npm.

## Raccourci `--update`

`openclaw --update` se réécrit en `openclaw update` (utile pour les shells et les scripts de lanceur).

## Voir aussi

- `openclaw doctor` (propose d'exécuter la mise à jour en premier sur les extractions git)
- [Development channels](/fr/install/development-channels)
- [Updating](/fr/install/updating)
- [CLI reference](/fr/cli)
