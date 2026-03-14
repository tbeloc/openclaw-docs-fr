---
read_when:
  - Lors de l'intégration du cycle de vie de Gateway avec une application macOS
summary: Cycle de vie de Gateway (launchd) sur macOS
title: Cycle de vie de Gateway
x-i18n:
  generated_at: "2026-02-03T07:52:31Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 9b910f574b723bc194ac663a5168e48d95f55cb468ce34c595d8ca60d3463c6a
  source_path: platforms/mac/child-process.md
  workflow: 15
---

# Cycle de vie de Gateway sur macOS

Les applications macOS **gèrent Gateway par défaut via launchd** et ne génèrent pas
Gateway en tant que processus enfant. Elles tentent d'abord de se connecter à une
instance Gateway déjà en cours d'exécution sur le port configuré ; si elle n'est pas accessible, elles activent le
service launchd via l'interface CLI externe `openclaw` (sans runtime intégré).
Cela vous offre un démarrage automatique fiable au moment de la connexion et un redémarrage après un plantage.

Le mode processus enfant (où l'application génère directement Gateway) **n'est actuellement pas utilisé**.
Si vous avez besoin d'un couplage plus étroit avec l'interface utilisateur, exécutez Gateway manuellement dans le terminal.

## Comportement par défaut (launchd)

- L'application installe un LaunchAgent par utilisateur marqué `bot.molt.gateway`
  (ou `bot.molt.<profile>` lors de l'utilisation de `--profile`/`OPENCLAW_PROFILE` ; les anciens `com.openclaw.*` sont supportés).
- Lorsque le mode local est activé, l'application s'assure que le LaunchAgent est chargé et
  démarre Gateway si nécessaire.
- Les journaux sont écrits dans le chemin du journal launchd Gateway (visible dans les paramètres de débogage).

Commandes courantes :

```bash
launchctl kickstart -k gui/$UID/bot.molt.gateway
launchctl bootout gui/$UID/bot.molt.gateway
```

Lors de l'exécution d'un profil nommé, remplacez l'étiquette par `bot.molt.<profile>`.

## Builds de développement non signés

`scripts/restart-mac.sh --no-sign` est utilisé pour les builds locaux rapides sans clé de signature. Pour éviter que launchd ne pointe vers un binaire relais non signé, il :

- Écrit `~/.openclaw/disable-launchagent`.

L'exécution signée de `scripts/restart-mac.sh` efface ce remplacement si le marqueur existe. Pour réinitialiser manuellement :

```bash
rm ~/.openclaw/disable-launchagent
```

## Mode connexion uniquement

Pour forcer l'application macOS à **ne jamais installer ou gérer launchd**, démarrez-la avec
`--attach-only` (ou `--no-launchd`). Cela définit `~/.openclaw/disable-launchagent`,
de sorte que l'application se connecte uniquement à une instance Gateway déjà en cours d'exécution. Vous pouvez basculer le même
comportement dans les paramètres de débogage.

## Mode distant

Le mode distant ne démarre jamais une instance Gateway locale. L'application utilise un
tunnel SSH vers l'hôte distant et se connecte via ce tunnel.

## Pourquoi nous préférons launchd

- Démarrage automatique au moment de la connexion.
- Sémantique de redémarrage/KeepAlive intégrée.
- Journalisation et gouvernance prévisibles.

Si un vrai mode processus enfant est à nouveau nécessaire à l'avenir, il devrait être documenté en tant que
mode de développement distinct et explicite uniquement.
