---
summary: "Référence CLI pour `openclaw system` (événements système, heartbeat, présence)"
read_when:
  - Vous voulez mettre en file d'attente un événement système sans créer une tâche cron
  - Vous devez activer ou désactiver les heartbeats
  - Vous voulez inspecter les entrées de présence système
title: "system"
---

# `openclaw system`

Utilitaires au niveau système pour la Gateway : mettre en file d'attente des événements système, contrôler les heartbeats et afficher la présence.

## Commandes courantes

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system heartbeat enable
openclaw system heartbeat last
openclaw system presence
```

## `system event`

Mettre en file d'attente un événement système sur la session **main**. Le prochain heartbeat l'injectera sous forme de ligne `System:` dans le prompt. Utilisez `--mode now` pour déclencher le heartbeat immédiatement ; `next-heartbeat` attend le prochain tick planifié.

Drapeaux :

- `--text <text>` : texte d'événement système requis.
- `--mode <mode>` : `now` ou `next-heartbeat` (par défaut).
- `--json` : sortie lisible par machine.

## `system heartbeat last|enable|disable`

Contrôles du heartbeat :

- `last` : afficher le dernier événement heartbeat.
- `enable` : réactiver les heartbeats (utilisez ceci s'ils ont été désactivés).
- `disable` : mettre en pause les heartbeats.

Drapeaux :

- `--json` : sortie lisible par machine.

## `system presence`

Lister les entrées de présence système actuelles que la Gateway connaît (nœuds, instances et lignes d'état similaires).

Drapeaux :

- `--json` : sortie lisible par machine.

## Notes

- Nécessite une Gateway en cours d'exécution accessible par votre configuration actuelle (locale ou distante).
- Les événements système sont éphémères et ne sont pas conservés lors des redémarrages.
