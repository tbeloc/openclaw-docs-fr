---
read_when:
  - 向新用户介绍 ClawHub
  - 安装、搜索或发布 Skills
  - 说明 ClawHub CLI 标志和同步行为
summary: ClawHub 指南：公共 Skills 注册中心 + CLI 工作流
title: ClawHub
x-i18n:
  generated_at: "2026-02-01T21:42:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8b7f8fab80a34e409f37fa130a49ff5b487966755a7b0d214dfebf5207c7124c
  source_path: tools/clawhub.md
  workflow: 15
---

# ClawHub

ClawHub est le **registre public des Skills pour OpenClaw**. C'est un service gratuit : tous les Skills sont publics, ouverts, et tout le monde peut les consulter, les partager et les réutiliser. Un Skill est simplement un dossier contenant un fichier `SKILL.md` (et des fichiers texte auxiliaires). Vous pouvez parcourir les Skills dans l'application web ou utiliser la CLI pour rechercher, installer, mettre à jour et publier des Skills.

Site web : [clawhub.com](https://clawhub.com)

## Pour qui (adapté aux débutants)

Si vous souhaitez ajouter de nouvelles fonctionnalités à vos agents OpenClaw, ClawHub est le moyen le plus simple de trouver et d'installer des Skills. Vous n'avez pas besoin de comprendre le fonctionnement du backend. Vous pouvez :

- Rechercher des Skills en langage naturel.
- Installer des Skills dans votre espace de travail.
- Mettre à jour les Skills ultérieurement avec une seule commande.
- Sauvegarder vos propres Skills en les publiant.

## Démarrage rapide (non-technique)

1. Installez la CLI (voir la section suivante).
2. Recherchez ce dont vous avez besoin :
   - `clawhub search "calendar"`
3. Installez un Skill :
   - `clawhub install <skill-slug>`
4. Démarrez une nouvelle session OpenClaw pour charger les nouveaux Skills.

## Installation de la CLI

Choisissez l'une des options suivantes :

```bash
npm i -g clawhub
```

```bash
pnpm add -g clawhub
```

## Positionnement dans OpenClaw

Par défaut, la CLI installe les Skills dans le répertoire `./skills` du répertoire de travail actuel. Si un espace de travail OpenClaw est configuré, `clawhub` revient à cet espace de travail, sauf si vous le remplacez via `--workdir` (ou `CLAWHUB_WORKDIR`). OpenClaw charge les Skills de l'espace de travail à partir de `<workspace>/skills`, et ils prendront effet à la **prochaine** session. Si vous utilisez déjà `~/.openclaw/skills` ou les Skills intégrés, les Skills de l'espace de travail ont la priorité.

Pour plus de détails sur le chargement, le partage et le contrôle d'accès des Skills, consultez
[Skills](/tools/skills).

## Fonctionnalités du service

- **Parcourir publiquement** les Skills et leur contenu `SKILL.md`.
- **Recherche** basée sur des vecteurs d'intégration (recherche vectorielle), pas seulement la correspondance de mots-clés.
- **Gestion des versions** avec support du versioning sémantique, des journaux de modifications et des étiquettes (y compris `latest`).
- **Téléchargement** de chaque version au format zip.
- **Étoiles et commentaires** pour les retours de la communauté.
- **Crochets de modération** pour l'approbation et l'audit.
- **API conviviale pour la CLI**, prenant en charge l'automatisation et les scripts.

## Commandes et paramètres de la CLI

Options globales (applicables à toutes les commandes) :

- `--workdir <dir>` : répertoire de travail (par défaut : répertoire actuel ; revient à l'espace de travail OpenClaw).
- `--dir <dir>` : répertoire des Skills, relatif au répertoire de travail (par défaut : `skills`).
- `--site <url>` : URL de base du site (connexion navigateur).
- `--registry <url>` : URL de base de l'API du registre.
- `--no-input` : désactiver les invites (mode non-interactif).
- `-V, --cli-version` : afficher la version de la CLI.

Authentification :

- `clawhub login` (flux navigateur) ou `clawhub login --token <token>`
- `clawhub logout`
- `clawhub whoami`

Options :

- `--token <token>` : coller un jeton API.
- `--label <label>` : étiquette pour le jeton de connexion navigateur stocké (par défaut : `CLI token`).
- `--no-browser` : ne pas ouvrir le navigateur (nécessite `--token`).

Recherche :

- `clawhub search "query"`
- `--limit <n>` : nombre maximum de résultats.

Installation :

- `clawhub install <slug>`
- `--version <version>` : installer une version spécifique.
- `--force` : remplacer si le dossier existe déjà.

Mise à jour :

- `clawhub update <slug>`
- `clawhub update --all`
- `--version <version>` : mettre à jour vers une version spécifique (slug unique uniquement).
- `--force` : forcer le remplacement lorsque les fichiers locaux ne correspondent à aucune version publiée.

Liste :

- `clawhub list` (lit `.clawhub/lock.json`)

Publication :

- `clawhub publish <path>`
- `--slug <slug>` : identifiant du Skill.
- `--name <name>` : nom d'affichage.
- `--version <version>` : version sémantique.
- `--changelog <text>` : texte du journal de modifications (peut être vide).
- `--tags <tags>` : étiquettes séparées par des virgules (par défaut : `latest`).

Suppression/Restauration (propriétaire/administrateur uniquement) :

- `clawhub delete <slug> --yes`
- `clawhub undelete <slug> --yes`

Synchronisation (analyser les Skills locaux + publier les Skills nouveaux/mis à jour) :

- `clawhub sync`
- `--root <dir...>` : répertoires racine d'analyse supplémentaires.
- `--all` : télécharger tout sans invite.
- `--dry-run` : afficher ce qui sera téléchargé.
- `--bump <type>` : type d'incrément de version pour les mises à jour `patch|minor|major` (par défaut : `patch`).
- `--changelog <text>` : journal de modifications pour les mises à jour non-interactives.
- `--tags <tags>` : étiquettes séparées par des virgules (par défaut : `latest`).
- `--concurrency <n>` : concurrence des vérifications du registre (par défaut : 4).

## Flux de travail courants pour les agents

### Rechercher des Skills

```bash
clawhub search "postgres backups"
```

### Télécharger de nouveaux Skills

```bash
clawhub install my-skill-pack
```

### Mettre à jour les Skills installés

```bash
clawhub update --all
```

### Sauvegarder vos Skills (publier ou synchroniser)

Pour un dossier de Skill unique :

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

Analyser et sauvegarder plusieurs Skills à la fois :

```bash
clawhub sync --all
```

## Détails avancés (technique)

### Gestion des versions et étiquettes

- Chaque publication crée une nouvelle **version sémantique** `SkillVersion`.
- Les étiquettes (comme `latest`) pointent vers une version ; déplacer une étiquette permet de revenir à une version antérieure.
- Le journal de modifications est joint à chaque version et peut être vide lors de la synchronisation ou de la publication d'une mise à jour.

### Modifications locales et versions du registre

Lors de la mise à jour, un hachage de contenu est utilisé pour comparer le contenu local des Skills avec les versions du registre. Si les fichiers locaux ne correspondent à aucune version publiée, la CLI demande une confirmation avant de remplacer (ou nécessite `--force` en mode non-interactif).

### Analyse de synchronisation et répertoires racine de secours

`clawhub sync` analyse d'abord le répertoire de travail actuel. S'il ne trouve pas de Skills, il revient aux anciens emplacements connus (par exemple `~/openclaw/skills` et `~/.openclaw/skills`). Ceci est conçu pour trouver les anciennes installations de Skills sans avoir besoin de drapeaux supplémentaires.

### Stockage et fichier de verrouillage

- Les Skills installés sont enregistrés dans `.clawhub/lock.json` dans le répertoire de travail.
- Les jetons d'authentification sont stockés dans le fichier de configuration de la CLI ClawHub (peut être remplacé via `CLAWHUB_CONFIG_PATH`).

### Télémétrie (comptage des installations)

Lorsque vous exécutez `clawhub sync` en étant connecté, la CLI envoie un instantané minimal pour le comptage des installations. Vous pouvez désactiver complètement cette fonctionnalité :

```bash
export CLAWHUB_DISABLE_TELEMETRY=1
```

## Variables d'environnement

- `CLAWHUB_SITE` : remplacer l'URL du site.
- `CLAWHUB_REGISTRY` : remplacer l'URL de l'API du registre.
- `CLAWHUB_CONFIG_PATH` : remplacer l'emplacement où la CLI stocke les jetons/configurations.
- `CLAWHUB_WORKDIR` : remplacer le répertoire de travail par défaut.
- `CLAWHUB_DISABLE_TELEMETRY=1` : désactiver la télémétrie pour `sync`.
