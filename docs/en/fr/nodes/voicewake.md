---
summary: "Mots de réveil vocaux globaux (propriété de la passerelle) et leur synchronisation entre les nœuds"
read_when:
  - Modification du comportement ou des paramètres par défaut des mots de réveil vocaux
  - Ajout de nouvelles plates-formes de nœuds nécessitant une synchronisation des mots de réveil
title: "Voice Wake"
---

# Voice Wake (Mots de réveil globaux)

OpenClaw traite les **mots de réveil comme une liste globale unique** détenue par la **passerelle**.

- Il n'y a **pas de mots de réveil personnalisés par nœud**.
- **N'importe quel nœud/interface utilisateur d'application peut modifier** la liste ; les modifications sont conservées par la passerelle et diffusées à tous.
- macOS et iOS conservent des **bascules Voice Wake activé/désactivé** locales (l'expérience utilisateur et les permissions diffèrent).
- Android garde actuellement Voice Wake désactivé et utilise un flux manuel de microphone dans l'onglet Voice.

## Stockage (hôte de la passerelle)

Les mots de réveil sont stockés sur la machine de la passerelle à :

- `~/.openclaw/settings/voicewake.json`

Structure :

```json
{ "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }
```

## Protocole

### Méthodes

- `voicewake.get` → `{ triggers: string[] }`
- `voicewake.set` avec paramètres `{ triggers: string[] }` → `{ triggers: string[] }`

Remarques :

- Les déclencheurs sont normalisés (espaces supprimés, valeurs vides supprimées). Les listes vides reviennent aux valeurs par défaut.
- Les limites sont appliquées pour des raisons de sécurité (plafonds de nombre/longueur).

### Événements

- `voicewake.changed` charge utile `{ triggers: string[] }`

Qui le reçoit :

- Tous les clients WebSocket (application macOS, WebChat, etc.)
- Tous les nœuds connectés (iOS/Android), et aussi lors de la connexion du nœud comme un envoi initial d'« état actuel ».

## Comportement du client

### Application macOS

- Utilise la liste globale pour contrôler les déclencheurs `VoiceWakeRuntime`.
- La modification des « Mots de déclenchement » dans les paramètres Voice Wake appelle `voicewake.set` puis s'appuie sur la diffusion pour maintenir les autres clients synchronisés.

### Nœud iOS

- Utilise la liste globale pour la détection de déclenchement `VoiceWakeManager`.
- La modification des mots de réveil dans les paramètres appelle `voicewake.set` (via la passerelle WS) et maintient également la détection des mots de réveil locaux réactive.

### Nœud Android

- Voice Wake est actuellement désactivé dans les paramètres/runtime Android.
- La voix Android utilise la capture manuelle du microphone dans l'onglet Voice au lieu des déclencheurs de mots de réveil.
