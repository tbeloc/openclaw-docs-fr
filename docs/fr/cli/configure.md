---
summary: "Référence CLI pour `openclaw configure` (invites de configuration interactive)"
read_when:
  - Vous souhaitez ajuster les identifiants, appareils ou paramètres par défaut de l'agent de manière interactive
title: "configure"
---

# `openclaw configure`

Invite interactive pour configurer les identifiants, appareils et paramètres par défaut de l'agent.

Remarque : La section **Model** inclut désormais une sélection multiple pour la liste d'autorisation `agents.defaults.models` (ce qui s'affiche dans `/model` et le sélecteur de modèle).

Conseil : `openclaw config` sans sous-commande ouvre le même assistant. Utilisez `openclaw config get|set|unset` pour les modifications non-interactives.

Liens connexes :

- Référence de configuration de la passerelle : [Configuration](/gateway/configuration)
- CLI Config : [Config](/cli/config)

Remarques :

- Le choix du lieu d'exécution de la passerelle met toujours à jour `gateway.mode`. Vous pouvez sélectionner « Continuer » sans les autres sections si c'est tout ce dont vous avez besoin.
- Les services orientés canaux (Slack/Discord/Matrix/Microsoft Teams) demandent des listes d'autorisation de canaux/salons lors de la configuration. Vous pouvez entrer des noms ou des identifiants ; l'assistant résout les noms en identifiants si possible.
- Si vous exécutez l'étape d'installation du démon, l'authentification par jeton nécessite un jeton, et `gateway.auth.token` est géré par SecretRef. La configuration valide le SecretRef mais ne persiste pas les valeurs de jeton en texte brut résolues dans les métadonnées d'environnement du service superviseur.
- Si l'authentification par jeton nécessite un jeton et que le SecretRef de jeton configuré n'est pas résolu, la configuration bloque l'installation du démon avec des conseils de correction actionnables.
- Si à la fois `gateway.auth.token` et `gateway.auth.password` sont configurés et que `gateway.auth.mode` n'est pas défini, la configuration bloque l'installation du démon jusqu'à ce que le mode soit défini explicitement.

## Exemples

```bash
openclaw configure
openclaw configure --section model --section channels
```
