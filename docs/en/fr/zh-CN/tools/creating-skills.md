---
title: Créer des Skills
x-i18n:
  generated_at: "2026-02-03T10:10:19Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ad801da34fe361ffa584ded47f775d1c104a471a3f7b7f930652255e98945c3a
  source_path: tools/creating-skills.md
  workflow: 15
---

# Créer des Skills personnalisés 🛠

OpenClaw est conçu pour être facilement extensible. Les « Skills » sont le principal moyen d'ajouter de nouvelles fonctionnalités à votre assistant.

## Qu'est-ce qu'un Skill ?

Un Skill est un répertoire contenant un fichier `SKILL.md` (qui fournit des instructions et des définitions d'outils pour le LLM), accompagné optionnellement de scripts ou de ressources.

## Guide étape par étape : votre premier Skill

### 1. Créer un répertoire

Les Skills se trouvent dans votre espace de travail, généralement `~/.openclaw/workspace/skills/`. Créez un nouveau dossier pour votre Skill :

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

### 2. Définir `SKILL.md`

Créez un fichier `SKILL.md` dans ce répertoire. Ce fichier utilise un frontmatter YAML pour les métadonnées et du Markdown pour les instructions.

```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

### 3. Ajouter des outils (optionnel)

Vous pouvez définir des outils personnalisés dans le frontmatter, ou indiquer à l'agent d'utiliser des outils système existants (comme `bash` ou `browser`).

### 4. Actualiser OpenClaw

Demandez à votre agent d'« actualiser les skills » ou redémarrez la passerelle Gateway. OpenClaw découvrira le nouveau répertoire et indexera le fichier `SKILL.md`.

## Bonnes pratiques

- **Soyez clair et concis** : indiquez au modèle *ce qu'il faut faire*, pas comment être une IA.
- **Sécurité d'abord** : si votre Skill utilise `bash`, assurez-vous que le prompt n'autorise pas l'injection de commandes arbitraires à partir d'entrées utilisateur non fiables.
- **Testez localement** : utilisez `openclaw agent --message "use my new skill"` pour tester.

## Partager des Skills

Vous pouvez également parcourir et contribuer des Skills sur [ClawHub](https://clawhub.com).
