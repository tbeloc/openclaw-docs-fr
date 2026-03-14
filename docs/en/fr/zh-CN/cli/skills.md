---
read_when:
  - Vous voulez voir quelles Skills sont disponibles et prêtes à être exécutées
  - Vous voulez déboguer les fichiers binaires/variables d'environnement/configurations manquants des Skills
summary: "Référence CLI pour `openclaw skills` (list/info/check) et qualification des skills"
title: skills
x-i18n:
  generated_at: "2026-02-03T07:45:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 7878442c88a27ec8033f3125c319e9a6a85a1c497a404a06112ad45185c261b0
  source_path: cli/skills.md
  workflow: 15
---

# `openclaw skills`

Vérifiez les Skills (intégrées + espace de travail + surcharges hébergées) et voyez lesquelles sont admissibles et lesquelles manquent de conditions requises.

Contenu connexe :

- Système Skills : [Skills](/tools/skills)
- Configuration Skills : [Skills configuration](/tools/skills-config)
- Installation ClawHub : [ClawHub](/tools/clawhub)

## Commandes

```bash
openclaw skills list
openclaw skills list --eligible
openclaw skills info <name>
openclaw skills check
```
