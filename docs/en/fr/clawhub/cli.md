---
summary: "Points d'entrée CLI ClawHub pour découvrir, installer, publier et vérifier les compétences et plugins OpenClaw."
read_when:
  - You want to use ClawHub from the command line
  - You want to install ClawHub skills or plugins through OpenClaw
  - You want to publish ClawHub packages
title: "ClawHub CLI"
---

# ClawHub CLI

OpenClaw dispose de deux points d'entrée en ligne de commande pour ClawHub :

- `openclaw skills` et `openclaw plugins` installent et gèrent les packages ClawHub
  à l'intérieur d'OpenClaw.
- Le CLI autonome `clawhub` gère les flux de travail des éditeurs tels que la connexion,
  la publication, le transfert et la synchronisation.

## Découvrir et installer

Utilisez les commandes OpenClaw lorsque vous souhaitez installer ou mettre à jour des packages pour un
agent OpenClaw local ou une Gateway.

```bash
openclaw skills search "calendar"
openclaw skills install <slug>
openclaw skills update <slug>
openclaw skills verify <slug>

openclaw plugins search "calendar"
openclaw plugins install clawhub:<package>
openclaw plugins update <id-or-npm-spec>
```

Les installations de compétences ciblent par défaut le répertoire `skills/` de l'espace de travail actif. Ajoutez
`--global` pour installer dans le répertoire des compétences gérées partagées.

Les installations de plugins utilisent le préfixe `clawhub:` lorsque vous souhaitez une résolution ClawHub
au lieu de npm ou d'une autre source d'installation.

## Publier et maintenir

Installez le CLI ClawHub autonome pour les flux de travail des éditeurs :

```bash
npm i -g clawhub
clawhub login
```

Publiez les packages de plugins avec `clawhub package publish` :

```bash
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
clawhub package publish your-org/your-plugin@v1.0.0
```

Publiez les dossiers de compétences avec `clawhub skill publish` :

```bash
clawhub skill publish ./skills/review-helper
clawhub skill publish ./skills/review-helper --version 1.0.0
```

Lorsque l'état d'analyse des compétences locales ou la propriété des packages nécessite une maintenance, utilisez la
commande autonome appropriée :

```bash
clawhub sync --all
clawhub package transfer @old-owner/package --to new-owner
```

## Connexes

- [`openclaw skills`](/fr/cli/skills) - recherche, installation, mise à jour et
  vérification des compétences locales
- [`openclaw plugins`](/fr/cli/plugins) - recherche, installation, mise à jour et
  inspection des plugins
- [Publication ClawHub](/fr/clawhub/publishing) - portée du propriétaire, validation des versions
  et flux d'examen
- [Créer des compétences](/fr/tools/creating-skills) - création et flux de publication des compétences
- [Construire des plugins](/fr/plugins/building-plugins) - création de packages de plugins
