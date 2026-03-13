---
read_when:
  - Vous souhaitez mettre en file d'attente des événements système sans créer de tâche cron
  - Vous devez activer ou désactiver les battements de cœur
  - Vous souhaitez vérifier les entrées d'état en ligne du système
summary: "Référence CLI pour `openclaw system` (événements système, battements de cœur, présence)"
title: system
x-i18n:
  generated_at: "2026-02-03T07:45:23Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 36ae5dbdec327f5a32f7ef44bdc1f161bad69868de62f5071bb4d25a71bfdfe9
  source_path: cli/system.md
  workflow: 15
---

# `openclaw system`

Outils auxiliaires au niveau système pour la passerelle Gateway : mise en file d'attente d'événements système, contrôle des battements de cœur et affichage de la présence.

## Commandes courantes

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system heartbeat enable
openclaw system heartbeat last
openclaw system presence
```

## `system event`

Met en file d'attente un événement système sur la session **principale**. Le prochain battement de cœur l'injectera en tant que ligne `System:` dans l'invite. Utilisez `--mode now` pour déclencher immédiatement un battement de cœur ; `next-heartbeat` attend le prochain moment de battement de cœur planifié.

Drapeaux :

- `--text <text>` : texte d'événement système obligatoire.
- `--mode <mode>` : `now` ou `next-heartbeat` (par défaut).
- `--json` : sortie lisible par machine.

## `system heartbeat last|enable|disable`

Contrôle des battements de cœur :

- `last` : affiche le dernier événement de battement de cœur.
- `enable` : réactive les battements de cœur (utilisez cette commande s'ils ont été désactivés précédemment).
- `disable` : suspend les battements de cœur.

Drapeaux :

- `--json` : sortie lisible par machine.

## `system presence`

Liste les entrées d'état en ligne du système actuellement connues de la passerelle Gateway (nœuds, instances et lignes d'état similaires).

Drapeaux :

- `--json` : sortie lisible par machine.

## Remarques

- Nécessite une passerelle Gateway en cours d'exécution, accessible via votre configuration actuelle (locale ou distante).
- Les événements système sont temporaires et ne persisteront pas après un redémarrage.
