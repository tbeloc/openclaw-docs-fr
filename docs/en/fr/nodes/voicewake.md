---
summary: "Mots de réveil vocaux globaux (propriété de la passerelle) et comment ils se synchronisent entre les nœuds"
read_when:
  - Changing voice wake words behavior or defaults
  - Adding new node platforms that need wake word sync
title: "Voice Wake"
---

# Voice Wake (Mots de réveil globaux)

OpenClaw traite **les mots de réveil comme une liste globale unique** détenue par la **Passerelle**.

- Il n'y a **pas de mots de réveil personnalisés par nœud**.
- **N'importe quel nœud/interface d'application peut modifier** la liste ; les modifications sont persistées par la Passerelle et diffusées à tous.
- macOS et iOS conservent des **bascules Voice Wake activé/désactivé** locales (l'UX et les permissions locales diffèrent).
- Android garde actuellement Voice Wake désactivé et utilise un flux micro manuel dans l'onglet Voice.

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

Notes :

- Les déclencheurs sont normalisés (espaces supprimés, vides supprimés). Les listes vides reviennent aux valeurs par défaut.
- Les limites sont appliquées pour la sécurité (plafonds de nombre/longueur).

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
- La modification des mots de réveil dans Paramètres appelle `voicewake.set` (via la WS de la Passerelle) et maintient également la détection locale des mots de réveil réactive.

### Nœud Android

- Voice Wake est actuellement désactivé dans le runtime/les paramètres Android.
- La voix Android utilise la capture micro manuelle dans l'onglet Voice au lieu des déclencheurs de mots de réveil.
