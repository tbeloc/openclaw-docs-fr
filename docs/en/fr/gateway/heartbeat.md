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
        target: "last", // explicit delivery to last contact (default is "none")
        directPolicy: "allow", // default: allow direct/DM targets; set "block" to suppress
        lightContext: true, // optional: only inject HEARTBEAT.md from bootstrap files
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // optional: send separate `Reasoning:` message too
      },
    },
  },
}
```

## Valeurs par défaut

- Intervalle: `30m` (ou `1h` lorsque Anthropic OAuth/setup-token est le mode d'authentification détecté). Définissez `agents.defaults.heartbeat.every` ou par agent `agents.list[].heartbeat.every`; utilisez `0m` pour désactiver.
- Corps du message (configurable via `agents.defaults.heartbeat.prompt`):
  `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`
- Le message de battement de cœur est envoyé **textuellement** comme message utilisateur. Le message système
  inclut une section "Heartbeat" et l'exécution est marquée en interne.
- Les heures actives (`heartbeat.activeHours`) sont vérifiées dans le fuseau horaire configuré.
  En dehors de la fenêtre, les battements de cœur sont ignorés jusqu'au prochain tick à l'intérieur de la fenêtre.

## À quoi sert le message de battement de cœur

Le message par défaut est intentionnellement large:

- **Tâches de fond**: "Consider outstanding tasks" pousse l'agent à examiner
  les suites (boîte de réception, calendrier, rappels, travail en attente) et signaler tout ce qui est urgent.
- **Vérification humaine**: "Checkup sometimes on your human during day time" pousse un
  message occasionnel léger "anything you need?", mais évite le spam nocturne
  en utilisant votre fuseau horaire local configuré (voir [/concepts/timezone](/concepts/timezone)).

Si vous voulez qu'un battement de cœur fasse quelque chose de très spécifique (par exemple "check Gmail PubSub
stats" ou "verify gateway health"), définissez `agents.defaults.heartbeat.prompt` (ou
`agents.list[].heartbeat.prompt`) sur un corps personnalisé (envoyé textuellement).

## Contrat de réponse

- Si rien ne nécessite une attention, répondez avec **`HEARTBEAT_OK`**.
- Pendant les exécutions de battement de cœur, OpenClaw traite `HEARTBEAT_OK` comme un accusé de réception lorsqu'il apparaît
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
        every: "30m", // default: 30m (0m disables)
        model: "anthropic/claude-opus-4-6",
        includeReasoning: false, // default: false (deliver separate Reasoning: message when available)
        lightContext: false, // default: false; true keeps only HEARTBEAT.md from workspace bootstrap files
        target: "last", // default: none | options: last | none | <channel id> (core or plugin, e.g. "bluebubbles")
        to: "+15551234567", // optional channel-specific override
        accountId: "ops-bot", // optional multi-account channel id
        prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        ackMaxChars: 300, // max chars allowed after HEARTBEAT_OK
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
- `channels.<channel>.accounts.<id>.heartbeat` (canaux multi-comptes) remplace les paramètres par canal.

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
        target: "last", // explicit delivery to last contact (default is "none")
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
        target: "last", // explicit delivery to last contact (default is "none")
        activeHours: {
          start: "09:00",
          end: "22:00",
          timezone: "America/New_York", // optional; uses your userTimezone if set, otherwise host tz
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

Utilisez `accountId` pour cibler un compte spécifique sur les canaux multi-comptes comme Telegram:

```json5
{
  agents: {
    list: [
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "telegram",
          to: "12345678:topic:42", // optional: route to a specific topic/thread
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
- `model`: remplacement de modèle optionnel pour les exécutions de battement de cœur (`provider/model`).
- `includeReasoning`: lorsqu'activé, livrez également le message `Reasoning:` séparé lorsqu'il est disponible (même forme que `/reasoning on`).
- `lightContext`: lorsque true, les exécutions de battement de cœur utilisent un contexte d'amorçage léger et conservent uniquement `HEARTBEAT.md` à partir des fichiers d'amorçage de l'espace de travail.
- `session`: clé de session optionnelle pour les exécutions de battement de cœur.
  - `main` (par défaut): session principale de l'agent.
  - Clé de session explicite (copiée à partir de `openclaw sessions --json` ou de la [CLI sessions](/cli/sessions)).
  - Formats de clé de session: voir [Sessions](/concepts/session) et [Groups](/channels/groups).
- `target`:
  - `last`: livrer au dernier canal externe utilisé.
  - canal explicite: `whatsapp` / `telegram` / `discord` / `googlechat` / `slack` / `msteams` / `signal` / `imessage`.
  - `none` (par défaut): exécutez le battement de cœur mais **ne livrez pas** en externe.
- `directPolicy`: contrôle le comportement de livraison direct/DM:
  - `allow` (par défaut): autoriser la livraison de battement de cœur direct/DM.
  - `block`: supprimer la livraison direct/DM (`reason=dm-blocked`).
- `to`: remplacement de destinataire optionnel (identifiant spécifique au canal, par exemple E.164 pour WhatsApp ou un identifiant de chat Telegram). Pour les sujets/threads Telegram, utilisez `<chatId>:topic:<messageThreadId>`.
- `accountId`: identifiant de compte optionnel pour les canaux multi-comptes. Lorsque `target: "last"`, l'identifiant de compte s'applique au dernier canal résolu s'il prend en charge les comptes; sinon il est ignoré. Si l'identifiant de compte ne correspond pas à un compte configuré pour le canal résolu, la livraison est ignorée.
- `prompt`: remplace le corps du message par défaut (non fusionné).
- `ackMaxChars`: nombre maximum de caractères autorisés après `HEARTBEAT_OK` avant la livraison.
- `suppressToolErrorWarnings`: lorsque true, supprime les charges utiles d'avertissement d'erreur d'outil pendant les exécutions de battement de cœur.
- `activeHours`: limite les exécutions de battement de cœur à une fenêtre de temps. Objet avec `start` (HH:MM, inclusif; utilisez `00:00` pour le début du jour), `end` (HH:MM exclusif; `24:00` autorisé pour la fin du jour), et `timezone` optionnel.
  - Omis ou `"user"`: utilise votre `agents.defaults.userTimezone` s'il est défini, sinon revient au fuseau horaire du système hôte.
  - `"local"`: utilise toujours le fuseau horaire du système hôte.
  - Tout identifiant IANA (par exemple `America/New_York`): utilisé directement; s'il est invalide, revient au comportement `"user"` ci-dessus.
  - `start` et `end` ne doivent pas être égaux pour une fenêtre active; les valeurs égales sont traitées comme une largeur zéro (toujours en dehors de la fenêtre).
  - En dehors de la fenêtre active, les battements de cœur sont ignorés jusqu'au prochain tick à l'intérieur de la fenêtre.

## Comportement de livraison

- Les battements de cœur s'exécutent dans la session principale de l'agent par défaut (`agent:<id>:<mainKey>`),
  ou `global` lorsque `session.scope = "global"`. Définissez `session` pour remplacer par une
  session de canal spécifique (Discord/WhatsApp/etc.).
- `session` affecte uniquement le contexte d'exécution; la livraison est contrôlée par `target` et `to`.
- Pour livrer à un canal/destinataire spécifique, définissez `target` + `to`. Avec
  `target: "last"`, la livraison utilise le dernier canal externe pour cette session.
- Les livraisons de battement de cœur autorisent les cibles direct/DM par défaut. Définissez `directPolicy: "block"` pour supprimer les envois de cible directe tout en exécutant le tour de battement de cœur.
- Si la file d'attente principale est occupée, le battement de cœur est ignoré et réessayé plus tard.
- Si `target` ne se résout à aucune destination externe, l'exécution se produit toujours mais aucun
  message sortant n'est envoyé.
- Les réponses uniquement de battement de cœur **ne** maintiennent pas la session active; le dernier `updatedAt`
  est restauré afin que l'expiration d'inactivité se comporte normalement.

## Contrôles de visibilité

Par défaut, les accusés de réception `HEARTBEAT_OK` sont supprimés tandis que le
contenu des alertes est livré. Vous pouvez ajuster cela par canal ou par compte :

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false # Masquer HEARTBEAT_OK (par défaut)
      showAlerts: true # Afficher les messages d'alerte (par défaut)
      useIndicator: true # Émettre des événements indicateurs (par défaut)
  telegram:
    heartbeat:
      showOk: true # Afficher les accusés de réception OK sur Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false # Supprimer la livraison des alertes pour ce compte
```

Précédence : par compte → par canal → paramètres par défaut du canal → paramètres par défaut intégrés.

### Ce que fait chaque drapeau

- `showOk` : envoie un accusé de réception `HEARTBEAT_OK` quand le modèle retourne une réponse OK uniquement.
- `showAlerts` : envoie le contenu de l'alerte quand le modèle retourne une réponse non-OK.
- `useIndicator` : émet des événements indicateurs pour les surfaces de statut de l'interface utilisateur.

Si **les trois** sont faux, OpenClaw ignore complètement l'exécution du heartbeat (aucun appel au modèle).

### Exemples par canal vs par compte

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false
      showAlerts: true
      useIndicator: true
  slack:
    heartbeat:
      showOk: true # tous les comptes Slack
    accounts:
      ops:
        heartbeat:
          showAlerts: false # supprimer les alertes pour le compte ops uniquement
  telegram:
    heartbeat:
      showOk: true
```

### Modèles courants

| Objectif                                      | Configuration                                                                            |
| --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Comportement par défaut (OK silencieux, alertes activées) | _(aucune configuration nécessaire)_                                                      |
| Complètement silencieux (pas de messages, pas d'indicateur) | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: false }` |
| Indicateur uniquement (pas de messages)       | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: true }`  |
| OK dans un seul canal                         | `channels.telegram.heartbeat: { showOk: true }`                                          |

## HEARTBEAT.md (optionnel)

Si un fichier `HEARTBEAT.md` existe dans l'espace de travail, l'invite par défaut
indique à l'agent de le lire. Pensez-y comme votre « liste de contrôle du heartbeat » :
petite, stable et sûre à inclure toutes les 30 minutes.

Si `HEARTBEAT.md` existe mais est effectivement vide (uniquement des lignes vides et des
en-têtes markdown comme `# Heading`), OpenClaw ignore l'exécution du heartbeat pour
économiser les appels API. Si le fichier est manquant, le heartbeat s'exécute quand même
et le modèle décide quoi faire.

Gardez-le minuscule (courte liste de contrôle ou rappels) pour éviter le surpoids de l'invite.

Exemple `HEARTBEAT.md` :

```md
# Liste de contrôle du heartbeat

- Scan rapide : quelque chose d'urgent dans les boîtes de réception ?
- Si c'est la journée, faire un contrôle léger si rien d'autre n'est en attente.
- Si une tâche est bloquée, noter _ce qui manque_ et demander à Peter la prochaine fois.
```

### L'agent peut-il mettre à jour HEARTBEAT.md ?

Oui — si vous le lui demandez.

`HEARTBEAT.md` est juste un fichier normal dans l'espace de travail de l'agent, vous pouvez donc
dire à l'agent (dans un chat normal) quelque chose comme :

- « Mettez à jour `HEARTBEAT.md` pour ajouter une vérification quotidienne du calendrier. »
- « Réécrivez `HEARTBEAT.md` pour qu'il soit plus court et axé sur les suivis de boîte de réception. »

Si vous voulez que cela se produise de manière proactive, vous pouvez également inclure une ligne
explicite dans votre invite de heartbeat comme : « Si la liste de contrôle devient obsolète, mettez
à jour `HEARTBEAT.md` avec une meilleure. »

Note de sécurité : ne mettez pas de secrets (clés API, numéros de téléphone, jetons privés) dans
`HEARTBEAT.md` — cela devient partie du contexte de l'invite.

## Réveil manuel (à la demande)

Vous pouvez mettre en file d'attente un événement système et déclencher un heartbeat immédiat avec :

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

Si plusieurs agents ont `heartbeat` configuré, un réveil manuel exécute immédiatement chacun de ces
heartbeats d'agent.

Utilisez `--mode next-heartbeat` pour attendre le prochain tick programmé.

## Livraison du raisonnement (optionnel)

Par défaut, les heartbeats livrent uniquement la charge utile « réponse » finale.

Si vous voulez de la transparence, activez :

- `agents.defaults.heartbeat.includeReasoning: true`

Lorsqu'activé, les heartbeats livreront également un message séparé préfixé
`Reasoning:` (même forme que `/reasoning on`). Cela peut être utile quand l'agent
gère plusieurs sessions/codex et que vous voulez voir pourquoi il a décidé de vous
contacter — mais cela peut aussi révéler plus de détails internes que vous ne le
souhaitez. Préférez le garder désactivé dans les chats de groupe.

## Sensibilisation aux coûts

Les heartbeats exécutent des tours d'agent complets. Les intervalles plus courts consomment plus de jetons.
Gardez `HEARTBEAT.md` petit et envisagez un `model` moins cher ou `target: "none"` si vous
voulez uniquement des mises à jour d'état interne.
