---
summary: "Référence CLI pour `openclaw backup` (créer des archives de sauvegarde locales)"
read_when:
  - Vous voulez une archive de sauvegarde de première classe pour l'état local d'OpenClaw
  - Vous voulez prévisualiser les chemins qui seraient inclus avant une réinitialisation ou une désinstallation
title: "backup"
---

# `openclaw backup`

Créez une archive de sauvegarde locale pour l'état, la configuration, les identifiants, les sessions et optionnellement les espaces de travail d'OpenClaw.

```bash
openclaw backup create
openclaw backup create --output ~/Backups
openclaw backup create --dry-run --json
openclaw backup create --verify
openclaw backup create --no-include-workspace
openclaw backup create --only-config
openclaw backup verify ./2026-03-09T00-00-00.000Z-openclaw-backup.tar.gz
```

## Notes

- L'archive inclut un fichier `manifest.json` avec les chemins sources résolus et la disposition de l'archive.
- La sortie par défaut est une archive `.tar.gz` horodatée dans le répertoire de travail actuel.
- Si le répertoire de travail actuel se trouve à l'intérieur d'un arborescence source sauvegardée, OpenClaw revient à votre répertoire personnel pour l'emplacement d'archive par défaut.
- Les fichiers d'archive existants ne sont jamais écrasés.
- Les chemins de sortie à l'intérieur des arborescences d'état/espace de travail source sont rejetés pour éviter l'auto-inclusion.
- `openclaw backup verify <archive>` valide que l'archive contient exactement un manifeste racine, rejette les chemins d'archive de style traversée, et vérifie que chaque charge utile déclarée dans le manifeste existe dans la tarball.
- `openclaw backup create --verify` exécute cette validation immédiatement après l'écriture de l'archive.
- `openclaw backup create --only-config` sauvegarde uniquement le fichier de configuration JSON actif.

## Ce qui est sauvegardé

`openclaw backup create` planifie les sources de sauvegarde à partir de votre installation locale d'OpenClaw :

- Le répertoire d'état retourné par le résolveur d'état local d'OpenClaw, généralement `~/.openclaw`
- Le chemin du fichier de configuration actif
- Le répertoire OAuth / identifiants
- Les répertoires d'espace de travail découverts à partir de la configuration actuelle, sauf si vous passez `--no-include-workspace`

Si vous utilisez `--only-config`, OpenClaw ignore la découverte d'état, d'identifiants et d'espace de travail et archive uniquement le chemin du fichier de configuration actif.

OpenClaw canonicalise les chemins avant de construire l'archive. Si la configuration, les identifiants ou un espace de travail se trouvent déjà à l'intérieur du répertoire d'état, ils ne sont pas dupliqués en tant que sources de sauvegarde de niveau supérieur séparées. Les chemins manquants sont ignorés.

La charge utile de l'archive stocke le contenu des fichiers de ces arborescences sources, et le `manifest.json` intégré enregistre les chemins sources absolus résolus plus la disposition de l'archive utilisée pour chaque actif.

## Comportement de configuration invalide

`openclaw backup` contourne intentionnellement la vérification préalable de configuration normale pour pouvoir toujours aider lors de la récupération. Comme la découverte d'espace de travail dépend d'une configuration valide, `openclaw backup create` échoue maintenant rapidement lorsque le fichier de configuration existe mais est invalide et que la sauvegarde d'espace de travail est toujours activée.

Si vous souhaitez toujours une sauvegarde partielle dans cette situation, réexécutez :

```bash
openclaw backup create --no-include-workspace
```

Cela maintient l'état, la configuration et les identifiants dans le champ d'application tout en ignorant complètement la découverte d'espace de travail.

Si vous avez seulement besoin d'une copie du fichier de configuration lui-même, `--only-config` fonctionne également lorsque la configuration est malformée car elle ne repose pas sur l'analyse de la configuration pour la découverte d'espace de travail.

## Taille et performance

OpenClaw n'applique pas de limite de taille de sauvegarde maximale intégrée ou de limite de taille par fichier.

Les limites pratiques proviennent de la machine locale et du système de fichiers de destination :

- Espace disponible pour l'écriture d'archive temporaire plus l'archive finale
- Temps pour parcourir les grands arborescences d'espace de travail et les compresser dans un `.tar.gz`
- Temps pour rescanner l'archive si vous utilisez `openclaw backup create --verify` ou exécutez `openclaw backup verify`
- Comportement du système de fichiers au chemin de destination. OpenClaw préfère une étape de publication de lien physique sans écrasement et revient à une copie exclusive lorsque les liens physiques ne sont pas pris en charge

Les grands espaces de travail sont généralement le principal moteur de la taille de l'archive. Si vous souhaitez une sauvegarde plus petite ou plus rapide, utilisez `--no-include-workspace`.

Pour l'archive la plus petite, utilisez `--only-config`.
