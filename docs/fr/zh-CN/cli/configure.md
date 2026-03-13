---
read_when:
  - Vous souhaitez ajuster interactivement les identifiants, les appareils ou les paramètres par défaut de l'agent
summary: "Référence CLI pour `openclaw configure` (invites de configuration interactives)"
title: configure
x-i18n:
  generated_at: "2026-02-03T07:44:46Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 9cb2bb5237b02b3a2dca71b5e43b11bd6b9939b9e4aa9ce1882457464b51efd2
  source_path: cli/configure.md
  workflow: 15
---

# `openclaw configure`

Invite interactive pour configurer les identifiants, les appareils et les valeurs par défaut de l'agent.

Remarque : **La section Modèles** contient maintenant une sélection multiple pour la liste d'autorisation `agents.defaults.models` (affichée dans `/model` et les sélecteurs de modèles).

Conseil : `openclaw config` sans sous-commande ouvre le même assistant. Utilisez `openclaw config get|set|unset` pour une édition non interactive.

Contenu connexe :

- Référence de configuration de la passerelle : [Configuration](/gateway/configuration)
- CLI Config : [Config](/cli/config)

Points importants :

- La sélection du lieu d'exécution de la passerelle met toujours à jour `gateway.mode`. Si c'est la seule chose dont vous avez besoin, vous pouvez sélectionner « Continuer » sans choisir d'autres sections.
- Les services orientés canaux (Slack/Discord/Matrix/Microsoft Teams) vous invitent à entrer une liste d'autorisation de canaux/salons lors de la configuration. Vous pouvez entrer des noms ou des ID ; l'assistant tentera de résoudre les noms en ID si possible.

## Exemples

```bash
openclaw configure
openclaw configure --section models --section channels
```
