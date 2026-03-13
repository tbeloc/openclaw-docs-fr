---
read_when:
  - Lors de l'ajustement de la fréquence des battements de cœur ou des messages
  - Lors du choix entre les battements de cœur et cron pour les tâches planifiées
summary: Interrogation des messages et règles de notification par battement de cœur
title: Battement de cœur
x-i18n:
  generated_at: "2026-02-03T07:48:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 18b017066aa2c41811b985564dd389834906f4576e85b576fb357a0eff482e69
  source_path: gateway/heartbeat.md
  workflow: 15
---

# Battement de cœur (Passerelle Gateway)

> **Battement de cœur vs Cron ?** Consultez [Cron vs Battement de cœur](/automation/cron-vs-heartbeat) pour savoir quand utiliser quelle solution.

Le battement de cœur exécute des **tours d'agent périodiques** dans la session principale, permettant au modèle de vous rappeler les éléments nécessitant attention sans vous déranger.

## Démarrage rapide (débutants)

1. Gardez le battement de cœur activé (par défaut `30m`, `1h` pour Anthropic OAuth/setup-token) ou définissez votre propre fréquence.
2. Créez une simple liste de contrôle `HEARTBEAT.md` dans l'espace de travail de l'agent (optionnel mais recommandé).
3. Décidez où les messages de battement de cœur doivent être envoyés (par défaut `target: "last"`).
4. Optionnel : activez l'envoi du contenu de raisonnement du battement de cœur pour plus de transparence.
5. Optionnel : limitez le battement de cœur aux heures actives (heure locale).

Exemple de configuration :

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // Optionnel : envoie également un message `Reasoning:` séparé
      },
    },
  },
}
```

## Valeurs par défaut

- Intervalle : `30m` (ou `1h` lorsque le mode d'authentification détecté est Anthropic OAuth/setup-token). Définissez `agents.defaults.heartbeat.every` ou `agents.list[].heartbeat.every` pour un agent unique ; utilisez `0m` pour désactiver.
- Contenu de l'invite (configurable via `agents.defaults.heartbeat.prompt`) :
  `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`
- L'invite de battement de cœur est envoyée **telle quelle** en tant que message utilisateur. L'invite système contient une section "Heartbeat" et l'exécution est marquée en interne.
- Les heures actives (`heartbeat.activeHours`) sont vérifiées selon le fuseau horaire configuré. En dehors de la plage horaire, les battements de cœur sont ignorés jusqu'au prochain cycle d'horloge dans la plage horaire.

## Utilisation de l'invite de battement de cœur

L'invite par défaut est intentionnellement conçue pour être large :

- **Tâches en arrière-plan** : "Consider outstanding tasks" incite l'agent à examiner les éléments en attente (boîte de réception, calendrier, rappels, travail en file d'attente) et à signaler tout élément urgent.
- **Vérification humaine** : "Checkup sometimes on your human during day time" incite à envoyer occasionnellement des messages légers du type "Y a-t-il quelque chose avec lequel je peux vous aider ?", mais en évitant les perturbations nocturnes en utilisant votre fuseau horaire local configuré (voir [/concepts/timezone](/concepts/timezone)).

Si vous souhaitez que le battement de cœur exécute des tâches très spécifiques (par exemple "vérifier les statistiques Gmail PubSub" ou "valider la santé de la passerelle Gateway"), définissez `agents.defaults.heartbeat.prompt` (ou `agents.list[].heartbeat.prompt`) sur un contenu personnalisé (envoyé tel quel).

## Conventions de réponse

- S'il n'y a rien qui nécessite attention, répondez **`HEARTBEAT_OK`**.
- Pendant l'exécution du battement de cœur, lorsque `HEARTBEAT_OK` apparaît au **début ou à la fin** de la réponse, OpenClaw le traite comme une confirmation. Ce marqueur est supprimé et si le contenu restant est **≤ `ackMaxChars`** (par défaut : 300), la réponse est supprimée.
- Si `HEARTBEAT_OK` apparaît au **milieu** de la réponse, il n'est pas traité spécialement.
- Pour les alertes, **ne pas** inclure `HEARTBEAT_OK` ; retournez uniquement le texte d'alerte.

En dehors du battement de cœur, les `HEARTBEAT_OK` inattendus au début/à la fin des messages sont supprimés et enregistrés ; les messages contenant uniquement `HEARTBEAT_OK` sont supprimés.

## Configuration

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // Par défaut : 30m (0m pour désactiver)
        model: "anthropic/claude-opus-4-5",
        includeReasoning: false, // Par défaut : false (envoie un message `Reasoning:` séparé si disponible)
        target: "last", // last | none | <channel id> (core ou plugin, par ex. "bluebubbles")
        to: "+15551234567", // Remplacement optionnel spécifique au canal
        prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        ackMaxChars: 300, // Nombre maximum de caractères autorisés après HEARTBEAT_OK
      },
    },
  },
}
```

### Portée et priorité

- `agents.defaults.heartbeat` définit le comportement global du battement de cœur.
- `agents.list[].heartbeat` fusionne au-dessus ; si un agent a un bloc `heartbeat`, **seuls ces agents** exécutent le battement de cœur.
- `channels.defaults.heartbeat` définit les valeurs par défaut de visibilité pour tous les canaux.
- `channels.<channel>.heartbeat` remplace les valeurs par défaut du canal.
- `channels.<channel>.accounts.<id>.heartbeat` (canaux multi-comptes) remplace les paramètres du canal unique.

### Battement de cœur d'agent unique

Si une entrée `agents.list[]` contient un bloc `heartbeat`, **seuls ces agents** exécutent le battement de cœur. Le bloc d'agent unique fusionne au-dessus de `agents.defaults.heartbeat` (vous pouvez donc définir une fois les valeurs par défaut partagées, puis les remplacer par agent).

Exemple : deux agents, seul le deuxième exécute le battement de cœur.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
      },
    },
    list: [
      { id: "main", default: true },
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "whatsapp",
          to: "+15551234567",
          prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        },
      },
    ],
  },
}
```

### Description des champs

- `every` : intervalle de battement de cœur (chaîne de durée ; unité par défaut = minutes).
- `model` : remplacement de modèle optionnel pour l'exécution du battement de cœur (`provider/model`).
- `includeReasoning` : lorsqu'activé, envoie également un message `Reasoning:` séparé (si disponible) (même format que `/reasoning on`).
- `session` : clé de session optionnelle pour l'exécution du battement de cœur.
  - `main` (par défaut) : session principale de l'agent.
  - Clé de session explicite (copiée depuis `openclaw sessions --json` ou [sessions CLI](/cli/sessions)).
  - Format de clé de session : voir [Session](/concepts/session) et [Groupes](/channels/groups).
- `target` :
  - `last` (par défaut) : envoie au dernier canal externe utilisé.
  - Canal explicite : `whatsapp` / `telegram` / `discord` / `googlechat` / `slack` / `msteams` / `signal` / `imessage`.
  - `none` : exécute le battement de cœur mais **n'envoie pas** vers l'extérieur.
- `to` : remplacement de destinataire optionnel (ID spécifique au canal, par ex. E.164 pour WhatsApp ou ID de chat Telegram).
- `prompt` : remplace le contenu de l'invite par défaut (ne fusionne pas).
- `ackMaxChars` : nombre maximum de caractères autorisés après `HEARTBEAT_OK` avant envoi.

## Comportement d'envoi

- Le battement de cœur s'exécute par défaut dans la session principale de l'agent (`agent:<id>:<mainKey>`), ou dans `global` lorsque `session.scope = "global"`. Définissez `session` pour remplacer par une session de canal spécifique (Discord/WhatsApp, etc.).
- `session` affecte uniquement le contexte d'exécution ; l'envoi est contrôlé par `target` et `to`.
- Pour envoyer à un canal/destinataire spécifique, définissez `target` + `to`. Lors de l'utilisation de `target: "last"`, l'envoi utilise le dernier canal externe de cette session.
- Si la file d'attente principale est occupée, le battement de cœur est ignoré et réessayé plus tard.
- Si `target` se résout en aucune cible externe, l'exécution se produit toujours mais aucun message sortant n'est envoyé.
- Les réponses de battement de cœur uniquement **ne maintiennent pas** la session active ; le dernier `updatedAt` est restauré, donc l'expiration d'inactivité fonctionne normalement.

## Contrôle de visibilité

Par défaut, les confirmations `HEARTBEAT_OK` sont supprimées, tandis que le contenu d'alerte est envoyé. Vous pouvez ajuster par canal ou par compte :

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false # Masquer HEARTBEAT_OK (par défaut)
      showAlerts: true # Afficher les messages d'alerte (par défaut)
      useIndicator: true # Émettre des événements d'indicateur (par défaut)
  telegram:
    heartbeat:
      showOk: true # Afficher les confirmations OK sur Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false # Supprimer l'envoi d'alertes pour ce compte
```

Priorité : compte unique → canal unique → valeurs par défaut du canal → valeurs par défaut intégrées.

### Fonction de chaque drapeau

- `showOk` : envoie la confirmation `HEARTBEAT_OK` lorsque le modèle retourne une réponse contenant uniquement OK.
- `showAlerts` : envoie le contenu d'alerte lorsque le modèle retourne une réponse non-OK.
- `useIndicator` : émet des événements d'indicateur pour l'interface utilisateur d'état.

Si **les trois** sont false, OpenClaw ignore complètement l'exécution du battement de cœur (n'appelle pas le modèle).

### Exemple canal unique vs compte unique

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false
      showAlerts: true
      useIndicator: true
  slack:
    heartbeat:
      showOk: true # Tous les comptes Slack
    accounts:
      ops:
        heartbeat:
          showAlerts: false # Supprimer les alertes uniquement pour le compte ops
  telegram:
    heartbeat:
      showOk: true
```

### Modèles courants

| Objectif                                    | Configuration                                                                                       |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Comportement par défaut (OK silencieux, alertes activées) | _( aucune configuration requise)_                                                                   |
| Complètement silencieux (pas de messages, pas d'indicateur) | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: false }`           |
| Indicateur uniquement (pas de messages)     | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: true }`            |
| Afficher OK sur un seul canal               | `channels.telegram.heartbeat: { showOk: true }`                                                     |

## HEARTBEAT.md (optionnel)

Si un fichier `HEARTBEAT.md` existe dans l'espace de travail, l'invite par défaut indique à l'agent de le lire. Pensez-y comme votre "liste de contrôle de battement de cœur" : petit, stable, peut être inclus en toute sécurité toutes les 30 minutes.

Si `HEARTBEAT.md` existe mais est en fait vide (uniquement des lignes vides et des titres markdown comme `# Heading`), OpenClaw ignore l'exécution du battement de cœur pour économiser les appels API. Si le fichier n'existe pas, le battement de cœur s'exécute toujours, le modèle décidant quoi faire.

Gardez-le petit (liste de contrôle courte ou rappels) pour éviter le gonflement des invites.

Exemple `HEARTBEAT.md` :

```md
# Heartbeat checklist

- Quick scan: anything urgent in inboxes?
- If it's daytime, do a lightweight check-in if nothing else is pending.
- If a task is blocked, write down _what is missing_ and ask Peter next time.
```

### L'agent peut-il mettre à jour HEARTBEAT.md ?

Oui — si vous le lui demandez.

`HEARTBEAT.md` est juste un fichier normal dans l'espace de travail de l'agent, vous pouvez donc dire à l'agent dans une conversation normale :

- "Mettez à jour `HEARTBEAT.md` pour ajouter une vér
