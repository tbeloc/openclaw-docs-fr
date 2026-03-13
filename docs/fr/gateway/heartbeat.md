---
summary: "Messages de sondage de battement de cœur et règles de notification"
read_when:
  - Adjusting heartbeat cadence or messaging
  - Deciding between heartbeat and cron for scheduled tasks
title: "Heartbeat"
---

# Heartbeat (Gateway)

> **Heartbeat vs Cron?** Voir [Cron vs Heartbeat](/automation/cron-vs-heartbeat) pour des conseils sur quand utiliser chacun.

Heartbeat exécute des **tours d'agent périodiques** dans la session principale afin que le modèle puisse
signaler tout ce qui nécessite une attention sans vous spammer.

Dépannage: [/automation/troubleshooting](/automation/troubleshooting)

## Démarrage rapide (débutant)

1. Laissez les battements de cœur activés (la valeur par défaut est `30m`, ou `1h` pour Anthropic OAuth/setup-token) ou définissez votre propre cadence.
2. Créez une petite liste de contrôle `HEARTBEAT.md` dans l'espace de travail de l'agent (facultatif mais recommandé).
3. Décidez où les messages de battement de cœur doivent aller (`target: "none"` est la valeur par défaut; définissez `target: "last"` pour acheminer vers le dernier contact).
4. Facultatif: activez la livraison du raisonnement du battement de cœur pour la transparence.
5. Facultatif: utilisez un contexte d'amorçage léger si les exécutions de battement de cœur n'ont besoin que de `HEARTBEAT.md`.
6. Facultatif: limitez les battements de cœur aux heures actives (heure locale).

Exemple de configuration:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // livraison explicite au dernier contact (la valeur par défaut est "none")
        directPolicy: "allow", // par défaut: autoriser les cibles directes/DM; définissez "block" pour supprimer
        lightContext: true, // facultatif: injecter uniquement HEARTBEAT.md à partir des fichiers d'amorçage
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // facultatif: envoyer également un message `Reasoning:` séparé
      },
    },
  },
}
```

## Valeurs par défaut

- Intervalle: `30m` (ou `1h` quand Anthropic OAuth/setup-token est le mode d'authentification détecté). Définissez `agents.defaults.heartbeat.every` ou par agent `agents.list[].heartbeat.every`; utilisez `0m` pour désactiver.
- Corps du message (configurable via `agents.defaults.heartbeat.prompt`):
  `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`
- Le message de battement de cœur est envoyé **textuellement** comme message utilisateur. Le message système
  inclut une section "Heartbeat" et l'exécution est marquée en interne.
- Les heures actives (`heartbeat.activeHours`) sont vérifiées dans le fuseau horaire configuré.
  En dehors de la fenêtre, les battements de cœur sont ignorés jusqu'au prochain tick à l'intérieur de la fenêtre.

## À quoi sert le message de battement de cœur

Le message par défaut est intentionnellement large:

- **Tâches de fond**: "Consider outstanding tasks" incite l'agent à examiner
  les suites (boîte de réception, calendrier, rappels, travail en attente) et à signaler tout ce qui est urgent.
- **Vérification humaine**: "Checkup sometimes on your human during day time" incite à
  un message occasionnel léger "anything you need?", mais évite le spam nocturne
  en utilisant votre fuseau horaire local configuré (voir [/concepts/timezone](/concepts/timezone)).

Si vous voulez qu'un battement de cœur fasse quelque chose de très spécifique (par exemple "check Gmail PubSub
stats" ou "verify gateway health"), définissez `agents.defaults.heartbeat.prompt` (ou
`agents.list[].heartbeat.prompt`) sur un corps personnalisé (envoyé textuellement).

## Contrat de réponse

- Si rien ne nécessite une attention, répondez avec **`HEARTBEAT_OK`**.
- Pendant les exécutions de battement de cœur, OpenClaw traite `HEARTBEAT_OK` comme un accusé de réception quand il apparaît
  au **début ou à la fin** de la réponse. Le jeton est supprimé et la réponse est
  abandonnée si le contenu restant est **≤ `ackMaxChars`** (par défaut: 300).
- Si `HEARTBEAT_OK` apparaît au **milieu** d'une réponse, il n'est pas traité
  spécialement.
- Pour les alertes, **ne pas** inclure `HEARTBEAT_OK`; retournez uniquement le texte d'alerte.

En dehors des battements de cœur, un `HEARTBEAT_OK` égaré au début/à la fin d'un message est supprimé
et enregistré; un message qui est uniquement `HEARTBEAT_OK` est abandonné.

## Configuration

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // par défaut: 30m (0m désactive)
        model: "anthropic/claude-opus-4-6",
        includeReasoning: false, // par défaut: false (livrer un message `Reasoning:` séparé quand disponible)
        lightContext: false, // par défaut: false; true garde uniquement HEARTBEAT.md à partir des fichiers d'amorçage de l'espace de travail
        target: "last", // par défaut: none | options: last | none | <channel id> (core ou plugin, par exemple "bluebubbles")
        to: "+15551234567", // remplacement facultatif spécifique au canal
        accountId: "ops-bot", // id de canal multi-compte facultatif
        prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        ackMaxChars: 300, // max de caractères autorisés après HEARTBEAT_OK
      },
    },
  },
}
```

### Portée et précédence

- `agents.defaults.heartbeat` définit le comportement global du battement de cœur.
- `agents.list[].heartbeat` fusionne par-dessus; si un agent a un bloc `heartbeat`, **seuls ces agents** exécutent les battements de cœur.
- `channels.defaults.heartbeat` définit les valeurs par défaut de visibilité pour tous les canaux.
- `channels.<channel>.heartbeat` remplace les valeurs par défaut du canal.
- `channels.<channel>.accounts.<id>.heartbeat` (canaux multi-compte) remplace les paramètres par canal.

### Battements de cœur par agent

Si une entrée `agents.list[]` inclut un bloc `heartbeat`, **seuls ces agents**
exécutent les battements de cœur. Le bloc par agent fusionne par-dessus `agents.defaults.heartbeat`
(vous pouvez donc définir les valeurs par défaut partagées une fois et les remplacer par agent).

Exemple: deux agents, seul le deuxième agent exécute les battements de cœur.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // livraison explicite au dernier contact (la valeur par défaut est "none")
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

### Exemple d'heures actives

Limitez les battements de cœur aux heures de bureau dans un fuseau horaire spécifique:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // livraison explicite au dernier contact (la valeur par défaut est "none")
        activeHours: {
          start: "09:00",
          end: "22:00",
          timezone: "America/New_York", // facultatif; utilise votre userTimezone s'il est défini, sinon tz hôte
        },
      },
    },
  },
}
```

En dehors de cette fenêtre (avant 9h ou après 22h Eastern), les battements de cœur sont ignorés. Le prochain tick programmé à l'intérieur de la fenêtre s'exécutera normalement.

### Configuration 24/7

Si vous voulez que les battements de cœur s'exécutent toute la journée, utilisez l'un de ces modèles:

- Omettez `activeHours` entièrement (pas de restriction de fenêtre de temps; c'est le comportement par défaut).
- Définissez une fenêtre pleine journée: `activeHours: { start: "00:00", end: "24:00" }`.

Ne définissez pas la même heure `start` et `end` (par exemple `08:00` à `08:00`).
Ceci est traité comme une fenêtre de largeur zéro, donc les battements de cœur sont toujours ignorés.

### Exemple multi-compte

Utilisez `accountId` pour cibler un compte spécifique sur les canaux multi-compte comme Telegram:

```json5
{
  agents: {
    list: [
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "telegram",
          to: "12345678:topic:42", // facultatif: acheminer vers un sujet/fil spécifique
          accountId: "ops-bot",
        },
      },
    ],
  },
  channels: {
    telegram: {
      accounts: {
        "ops-bot": { botToken: "YOUR_TELEGRAM_BOT_TOKEN" },
      },
    },
  },
}
```

### Notes sur les champs

- `every`: intervalle de battement de cœur (chaîne de durée; unité par défaut = minutes).
- `model`: remplacement de modèle facultatif pour les exécutions de battement de cœur (`provider/model`).
- `includeReasoning`: quand activé, livrer également le message `Reasoning:` séparé quand disponible (même forme que `/reasoning on`).
- `lightContext`: quand true, les exécutions de battement de cœur utilisent un contexte d'amorçage léger et gardent uniquement `HEARTBEAT.md` à partir des fichiers d'amorçage de l'espace de travail.
- `session`: clé de session facultative pour les exécutions de battement de cœur.
  - `main` (par défaut): session principale de l'agent.
  - Clé de session explicite (copier depuis `openclaw sessions --json` ou le [CLI sessions](/cli/sessions)).
  - Formats de clé de session: voir [Sessions](/concepts/session) et [Groups](/channels/groups).
- `target`:
  - `last`: livrer au dernier canal externe utilisé.
  - canal explicite: `whatsapp` / `telegram` / `discord` / `googlechat` / `slack` / `msteams` / `signal` / `imessage`.
  - `none` (par défaut): exécuter le battement de cœur mais **ne pas livrer** en externe.
- `directPolicy`: contrôle le comportement de livraison directe/DM:
  - `allow` (par défaut): autoriser la livraison de battement de cœur direct/DM.
  - `block`: supprimer la livraison directe/DM (`reason=dm-blocked`).
- `to`: remplacement de destinataire facultatif (id spécifique au canal, par exemple E.164 pour WhatsApp ou un id de chat Telegram). Pour les sujets/fils Telegram, utilisez `<chatId>:topic:<messageThreadId>`.
- `accountId`: id de compte facultatif pour les canaux multi-compte. Quand `target: "last"`, l'id de compte s'applique au dernier canal résolu s'il supporte les comptes; sinon il est ignoré. Si l'id de compte ne correspond pas à un compte configuré pour le canal résolu, la livraison est ignorée.
- `prompt`: remplace le corps du message par défaut (non fusionné).
- `ackMaxChars`: max de caractères autorisés après `HEARTBEAT_OK` avant livraison.
- `suppressToolErrorWarnings`: quand true, supprime les charges utiles d'avertissement d'erreur d'outil pendant les exécutions de battement de cœur.
- `activeHours`: limite les exécutions de battement de cœur à une fenêtre de temps. Objet avec `start` (HH:MM, inclusif; utilisez `00:00` pour le début du jour), `end` (HH:MM exclusif; `24:00` autorisé pour la fin du jour), et `timezone` facultatif.
  - Omis ou `"user"`: utilise votre `agents.defaults.userTimezone` s'il est défini, sinon revient au fuseau horaire du système hôte.
  - `"local"`: utilise toujours le fuseau horaire du système hôte.
  - N'importe quel identifiant IANA (par exemple `America/New_York`): utilisé directement; s'il est invalide, revient au comportement `"user"` ci-dessus.
  - `start` et `end` ne doivent pas être égaux pour une fenêtre active; les valeurs égales sont traitées comme une largeur zéro (toujours en dehors de la fenêtre).
  - En dehors de la fenêtre active, les battements de cœur sont ignorés jusqu'au prochain tick à l'intérieur de la fenêtre.

## Comportement de livraison

- Les battements de cœur s'exécutent dans la session principale de l'agent par défaut (`agent:<id>:<mainKey>`),
  ou `global` quand `session.scope = "global"`. Définissez `session` pour remplacer par une
  session de canal spécifique (Discord/WhatsApp/etc.).
- `session` affecte uniquement le contexte d'exécution; la livraison est contrôlée par `target` et `to`.
- Pour livrer à un canal/destinataire spécifique, définissez `target` + `to`. Avec
  `target: "last"`, la livraison utilise le dernier canal externe pour cette session.
