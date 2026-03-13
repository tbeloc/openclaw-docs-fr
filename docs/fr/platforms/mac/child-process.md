---
summary: "Cycle de vie de la passerelle sur macOS (launchd)"
read_when:
  - Intégration de l'application Mac avec le cycle de vie de la passerelle
title: "Cycle de vie de la passerelle"
---

# Cycle de vie de la passerelle sur macOS

L'application macOS **gère la passerelle via launchd** par défaut et ne lance
pas la passerelle en tant que processus enfant. Elle tente d'abord de se connecter à une
passerelle déjà en cours d'exécution sur le port configuré ; si aucune n'est accessible, elle active le
service launchd via l'interface de ligne de commande externe `openclaw` (pas de runtime intégré). Cela vous offre
un démarrage automatique fiable à la connexion et un redémarrage en cas de plantage.

Le mode processus enfant (passerelle lancée directement par l'application) **n'est pas utilisé** actuellement.
Si vous avez besoin d'un couplage plus étroit avec l'interface utilisateur, lancez la passerelle manuellement dans un terminal.

## Comportement par défaut (launchd)

- L'application installe un LaunchAgent par utilisateur étiqueté `ai.openclaw.gateway`
  (ou `ai.openclaw.<profile>` lors de l'utilisation de `--profile`/`OPENCLAW_PROFILE` ; l'ancien `com.openclaw.*` est supporté).
- Lorsque le mode Local est activé, l'application s'assure que le LaunchAgent est chargé et
  démarre la passerelle si nécessaire.
- Les journaux sont écrits dans le chemin du journal de passerelle launchd (visible dans les paramètres de débogage).

Commandes courantes :

```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

Remplacez l'étiquette par `ai.openclaw.<profile>` lors de l'exécution d'un profil nommé.

## Builds de développement non signés

`scripts/restart-mac.sh --no-sign` est destiné aux builds locaux rapides lorsque vous n'avez pas
de clés de signature. Pour empêcher launchd de pointer vers un binaire de relais non signé, il :

- Écrit `~/.openclaw/disable-launchagent`.

Les exécutions signées de `scripts/restart-mac.sh` effacent ce remplacement si le marqueur est
présent. Pour réinitialiser manuellement :

```bash
rm ~/.openclaw/disable-launchagent
```

## Mode attachement uniquement

Pour forcer l'application macOS à **ne jamais installer ou gérer launchd**, lancez-la avec
`--attach-only` (ou `--no-launchd`). Cela définit `~/.openclaw/disable-launchagent`,
de sorte que l'application ne se connecte qu'à une passerelle déjà en cours d'exécution. Vous pouvez basculer le même
comportement dans les paramètres de débogage.

## Mode distant

Le mode distant ne démarre jamais une passerelle locale. L'application utilise un tunnel SSH vers
l'hôte distant et se connecte via ce tunnel.

## Pourquoi nous préférons launchd

- Démarrage automatique à la connexion.
- Sémantique de redémarrage/KeepAlive intégrée.
- Journaux et supervision prévisibles.

Si un vrai mode processus enfant est jamais nécessaire à nouveau, il devrait être documenté comme un
mode distinct et explicite réservé au développement.
