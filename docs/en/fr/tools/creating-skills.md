---
title: "Créer des compétences"
summary: "Créer et tester des compétences d'espace de travail personnalisées avec SKILL.md"
read_when:
  - You are creating a new custom skill in your workspace
  - You need a quick starter workflow for SKILL.md-based skills
---

# Créer des compétences personnalisées 🛠

OpenClaw est conçu pour être facilement extensible. Les « compétences » sont le principal moyen d'ajouter de nouvelles capacités à votre assistant.

## Qu'est-ce qu'une compétence ?

Une compétence est un répertoire contenant un fichier `SKILL.md` (qui fournit des instructions et des définitions d'outils au LLM) et optionnellement des scripts ou des ressources.

## Étape par étape : Votre première compétence

### 1. Créer le répertoire

Les compétences se trouvent dans votre espace de travail, généralement `~/.openclaw/workspace/skills/`. Créez un nouveau dossier pour votre compétence :

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

### 2. Définir le `SKILL.md`

Créez un fichier `SKILL.md` dans ce répertoire. Ce fichier utilise le préambule YAML pour les métadonnées et Markdown pour les instructions.

```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

### 3. Ajouter des outils (Optionnel)

Vous pouvez définir des outils personnalisés dans le préambule ou instruire l'agent d'utiliser des outils système existants (comme `bash` ou `browser`).

### 4. Actualiser OpenClaw

Demandez à votre agent d'« actualiser les compétences » ou redémarrez la passerelle. OpenClaw découvrira le nouveau répertoire et indexera le `SKILL.md`.

## Bonnes pratiques

- **Soyez concis** : Instruisez le modèle sur _ce qu'il faut faire_, pas sur comment être une IA.
- **Sécurité d'abord** : Si votre compétence utilise `bash`, assurez-vous que les invites n'autorisent pas l'injection de commandes arbitraires à partir d'entrées utilisateur non fiables.
- **Testez localement** : Utilisez `openclaw agent --message "use my new skill"` pour tester.

## Compétences partagées

Vous pouvez également parcourir et contribuer des compétences à [ClawHub](https://clawhub.com).
