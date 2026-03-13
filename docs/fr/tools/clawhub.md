---
summary: "Guide ClawHub : registre public de compétences + workflows CLI"
read_when:
  - Introducing ClawHub to new users
  - Installing, searching, or publishing skills
  - Explaining ClawHub CLI flags and sync behavior
title: "ClawHub"
---

# ClawHub

ClawHub est le **registre public de compétences pour OpenClaw**. C'est un service gratuit : toutes les compétences sont publiques, ouvertes et visibles par tous pour le partage et la réutilisation. Une compétence est simplement un dossier contenant un fichier `SKILL.md` (plus des fichiers texte de support). Vous pouvez parcourir les compétences dans l'application web ou utiliser la CLI pour rechercher, installer, mettre à jour et publier des compétences.

Site : [clawhub.ai](https://clawhub.ai)

## Ce qu'est ClawHub

- Un registre public pour les compétences OpenClaw.
- Un stockage versionné des bundles de compétences et des métadonnées.
- Une surface de découverte pour la recherche, les tags et les signaux d'utilisation.

## Comment ça fonctionne

1. Un utilisateur publie un bundle de compétences (fichiers + métadonnées).
2. ClawHub stocke le bundle, analyse les métadonnées et attribue une version.
3. Le registre indexe la compétence pour la recherche et la découverte.
4. Les utilisateurs parcourent, téléchargent et installent les compétences dans OpenClaw.

## Ce que vous pouvez faire

- Publier de nouvelles compétences et de nouvelles versions de compétences existantes.
- Découvrir des compétences par nom, tags ou recherche.
- Télécharger des bundles de compétences et inspecter leurs fichiers.
- Signaler les compétences abusives ou dangereuses.
- Si vous êtes modérateur, masquer, afficher, supprimer ou bannir.

## Pour qui c'est (convivial pour les débutants)

Si vous souhaitez ajouter de nouvelles capacités à votre agent OpenClaw, ClawHub est le moyen le plus facile de trouver et d'installer des compétences. Vous n'avez pas besoin de savoir comment fonctionne le backend. Vous pouvez :

- Rechercher des compétences en langage naturel.
- Installer une compétence dans votre espace de travail.
- Mettre à jour les compétences plus tard avec une seule commande.
- Sauvegarder vos propres compétences en les publiant.

## Démarrage rapide (non technique)

1. Installez la CLI (voir la section suivante).
2. Recherchez quelque chose dont vous avez besoin :
   - `clawhub search "calendar"`
3. Installez une compétence :
   - `clawhub install <skill-slug>`
4. Démarrez une nouvelle session OpenClaw pour qu'elle détecte la nouvelle compétence.

## Installer la CLI

Choisissez l'une des options :

```bash
npm i -g clawhub
```

```bash
pnpm add -g clawhub
```

## Comment ça s'intègre dans OpenClaw

Par défaut, la CLI installe les compétences dans `./skills` sous votre répertoire de travail actuel. Si un espace de travail OpenClaw est configuré, `clawhub` revient à cet espace de travail sauf si vous remplacez `--workdir` (ou `CLAWHUB_WORKDIR`). OpenClaw charge les compétences de l'espace de travail depuis `<workspace>/skills` et les détectera dans la **prochaine** session. Si vous utilisez déjà `~/.openclaw/skills` ou des compétences groupées, les compétences de l'espace de travail ont la priorité.

Pour plus de détails sur la façon dont les compétences sont chargées, partagées et contrôlées, voir
[Skills](/tools/skills).

## Aperçu du système de compétences

Une compétence est un bundle versionné de fichiers qui enseigne à OpenClaw comment effectuer une tâche spécifique. Chaque publication crée une nouvelle version, et le registre conserve un historique des versions pour que les utilisateurs puissent auditer les modifications.

Une compétence typique comprend :

- Un fichier `SKILL.md` avec la description principale et l'utilisation.
- Des configs, scripts ou fichiers de support optionnels utilisés par la compétence.
- Des métadonnées telles que les tags, le résumé et les exigences d'installation.

ClawHub utilise les métadonnées pour alimenter la découverte et exposer en toute sécurité les capacités des compétences. Le registre suit également les signaux d'utilisation (comme les étoiles et les téléchargements) pour améliorer le classement et la visibilité.

## Ce que le service fournit (fonctionnalités)

- **Navigation publique** des compétences et de leur contenu `SKILL.md`.
- **Recherche** alimentée par des embeddings (recherche vectorielle), pas seulement des mots-clés.
- **Versioning** avec semver, changelogs et tags (y compris `latest`).
- **Téléchargements** en zip par version.
- **Étoiles et commentaires** pour les retours de la communauté.
- **Hooks de modération** pour les approbations et les audits.
- **API conviviale pour la CLI** pour l'automatisation et les scripts.

## Sécurité et modération

ClawHub est ouvert par défaut. N'importe qui peut télécharger des compétences, mais un compte GitHub doit avoir au moins une semaine pour publier. Cela aide à ralentir les abus sans bloquer les contributeurs légitimes.

Signalement et modération :

- Tout utilisateur connecté peut signaler une compétence.
- Les raisons du signalement sont requises et enregistrées.
- Chaque utilisateur peut avoir jusqu'à 20 signalements actifs à la fois.
- Les compétences avec plus de 3 signalements uniques sont masquées automatiquement par défaut.
- Les modérateurs peuvent afficher les compétences masquées, les afficher, les supprimer ou bannir les utilisateurs.
- L'abus de la fonction de signalement peut entraîner des interdictions de compte.

Intéressé par devenir modérateur ? Demandez sur le Discord OpenClaw et contactez un modérateur ou un responsable.

## Commandes et paramètres CLI

Options globales (s'appliquent à toutes les commandes) :

- `--workdir <dir>` : Répertoire de travail (par défaut : répertoire actuel ; revient à l'espace de travail OpenClaw).
- `--dir <dir>` : Répertoire des compétences, relatif à workdir (par défaut : `skills`).
- `--site <url>` : URL de base du site (connexion navigateur).
- `--registry <url>` : URL de base de l'API du registre.
- `--no-input` : Désactiver les invites (non interactif).
- `-V, --cli-version` : Afficher la version de la CLI.

Authentification :

- `clawhub login` (flux navigateur) ou `clawhub login --token <token>`
- `clawhub logout`
- `clawhub whoami`

Options :

- `--token <token>` : Collez un jeton API.
- `--label <label>` : Label stocké pour les jetons de connexion navigateur (par défaut : `CLI token`).
- `--no-browser` : Ne pas ouvrir de navigateur (nécessite `--token`).

Recherche :

- `clawhub search "query"`
- `--limit <n>` : Nombre maximum de résultats.

Installation :

- `clawhub install <slug>`
- `--version <version>` : Installer une version spécifique.
- `--force` : Remplacer si le dossier existe déjà.

Mise à jour :

- `clawhub update <slug>`
- `clawhub update --all`
- `--version <version>` : Mettre à jour vers une version spécifique (slug unique uniquement).
- `--force` : Remplacer quand les fichiers locaux ne correspondent à aucune version publiée.

Liste :

- `clawhub list` (lit `.clawhub/lock.json`)

Publication :

- `clawhub publish <path>`
- `--slug <slug>` : Slug de la compétence.
- `--name <name>` : Nom d'affichage.
- `--version <version>` : Version semver.
- `--changelog <text>` : Texte du changelog (peut être vide).
- `--tags <tags>` : Tags séparés par des virgules (par défaut : `latest`).

Suppression/restauration (propriétaire/admin uniquement) :

- `clawhub delete <slug> --yes`
- `clawhub undelete <slug> --yes`

Synchronisation (analyser les compétences locales + publier les nouvelles/mises à jour) :

- `clawhub sync`
- `--root <dir...>` : Racines d'analyse supplémentaires.
- `--all` : Télécharger tout sans invites.
- `--dry-run` : Afficher ce qui serait téléchargé.
- `--bump <type>` : `patch|minor|major` pour les mises à jour (par défaut : `patch`).
- `--changelog <text>` : Changelog pour les mises à jour non interactives.
- `--tags <tags>` : Tags séparés par des virgules (par défaut : `latest`).
- `--concurrency <n>` : Vérifications du registre (par défaut : 4).

## Workflows courants pour les agents

### Rechercher des compétences

```bash
clawhub search "postgres backups"
```

### Télécharger de nouvelles compétences

```bash
clawhub install my-skill-pack
```

### Mettre à jour les compétences installées

```bash
clawhub update --all
```

### Sauvegarder vos compétences (publier ou synchroniser)

Pour un dossier de compétences unique :

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

Pour analyser et sauvegarder de nombreuses compétences à la fois :

```bash
clawhub sync --all
```

## Détails avancés (technique)

### Versioning et tags

- Chaque publication crée une nouvelle `SkillVersion` **semver**.
- Les tags (comme `latest`) pointent vers une version ; déplacer les tags vous permet de revenir en arrière.
- Les changelogs sont attachés par version et peuvent être vides lors de la synchronisation ou de la publication de mises à jour.

### Modifications locales vs versions du registre

Les mises à jour comparent le contenu de la compétence locale aux versions du registre en utilisant un hash de contenu. Si les fichiers locaux ne correspondent à aucune version publiée, la CLI demande avant de remplacer (ou nécessite `--force` dans les exécutions non interactives).

### Analyse de synchronisation et racines de secours

`clawhub sync` analyse d'abord votre workdir actuel. Si aucune compétence n'est trouvée, elle revient aux emplacements hérités connus (par exemple `~/openclaw/skills` et `~/.openclaw/skills`). Ceci est conçu pour trouver les anciennes installations de compétences sans drapeaux supplémentaires.

### Stockage et fichier de verrouillage

- Les compétences installées sont enregistrées dans `.clawhub/lock.json` sous votre workdir.
- Les jetons d'authentification sont stockés dans le fichier de configuration de la CLI ClawHub (remplacer via `CLAWHUB_CONFIG_PATH`).

### Télémétrie (comptages d'installation)

Lorsque vous exécutez `clawhub sync` connecté, la CLI envoie un snapshot minimal pour calculer les comptages d'installation. Vous pouvez désactiver cela entièrement :

```bash
export CLAWHUB_DISABLE_TELEMETRY=1
```

## Variables d'environnement

- `CLAWHUB_SITE` : Remplacer l'URL du site.
- `CLAWHUB_REGISTRY` : Remplacer l'URL de l'API du registre.
- `CLAWHUB_CONFIG_PATH` : Remplacer où la CLI stocke le jeton/config.
- `CLAWHUB_WORKDIR` : Remplacer le workdir par défaut.
- `CLAWHUB_DISABLE_TELEMETRY=1` : Désactiver la télémétrie sur `sync`.
