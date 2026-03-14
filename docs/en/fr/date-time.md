---
summary: "Gestion de la date et de l'heure dans les enveloppes, les invites, les outils et les connecteurs"
read_when:
  - You are changing how timestamps are shown to the model or users
  - You are debugging time formatting in messages or system prompt output
title: "Date et heure"
---

# Date et heure

OpenClaw utilise par défaut **l'heure locale de l'hôte pour les horodatages de transport** et **le fuseau horaire de l'utilisateur uniquement dans l'invite système**.
Les horodatages des fournisseurs sont conservés afin que les outils conservent leur sémantique native (l'heure actuelle est disponible via `session_status`).

## Enveloppes de messages (locale par défaut)

Les messages entrants sont enveloppés avec un horodatage (précision à la minute) :

```
[Provider ... 2026-01-05 16:26 PST] message text
```

Cet horodatage d'enveloppe est **local à l'hôte par défaut**, quel que soit le fuseau horaire du fournisseur.

Vous pouvez remplacer ce comportement :

```json5
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

- `envelopeTimezone: "utc"` utilise UTC.
- `envelopeTimezone: "local"` utilise le fuseau horaire de l'hôte.
- `envelopeTimezone: "user"` utilise `agents.defaults.userTimezone` (revient au fuseau horaire de l'hôte).
- Utilisez un fuseau horaire IANA explicite (par exemple, `"America/Chicago"`) pour une zone fixe.
- `envelopeTimestamp: "off"` supprime les horodatages absolus des en-têtes d'enveloppe.
- `envelopeElapsed: "off"` supprime les suffixes de temps écoulé (le style `+2m`).

### Exemples

**Local (par défaut) :**

```
[WhatsApp +1555 2026-01-18 00:19 PST] hello
```

**Fuseau horaire de l'utilisateur :**

```
[WhatsApp +1555 2026-01-18 00:19 CST] hello
```

**Temps écoulé activé :**

```
[WhatsApp +1555 +30s 2026-01-18T05:19Z] follow-up
```

## Invite système : Date et heure actuelles

Si le fuseau horaire de l'utilisateur est connu, l'invite système inclut une section dédiée
**Date et heure actuelles** avec **le fuseau horaire uniquement** (pas de format d'horloge/heure)
pour maintenir la stabilité de la mise en cache des invites :

```
Time zone: America/Chicago
```

Lorsque l'agent a besoin de l'heure actuelle, utilisez l'outil `session_status` ; la carte de statut
inclut une ligne d'horodatage.

## Lignes d'événements système (locale par défaut)

Les événements système en file d'attente insérés dans le contexte de l'agent sont préfixés avec un horodatage utilisant
la même sélection de fuseau horaire que les enveloppes de messages (par défaut : local à l'hôte).

```
System: [2026-01-12 12:19:17 PST] Model switched.
```

### Configurer le fuseau horaire de l'utilisateur + le format

```json5
{
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
      timeFormat: "auto", // auto | 12 | 24
    },
  },
}
```

- `userTimezone` définit le **fuseau horaire local de l'utilisateur** pour le contexte d'invite.
- `timeFormat` contrôle l'affichage **12h/24h** dans l'invite. `auto` suit les préférences du système d'exploitation.

## Détection du format d'heure (auto)

Lorsque `timeFormat: "auto"`, OpenClaw inspecte la préférence du système d'exploitation (macOS/Windows)
et revient au formatage des paramètres régionaux. La valeur détectée est **mise en cache par processus**
pour éviter les appels système répétés.

## Charges utiles d'outils + connecteurs (heure brute du fournisseur + champs normalisés)

Les outils de canal retournent **les horodatages natifs du fournisseur** et ajoutent des champs normalisés pour la cohérence :

- `timestampMs` : millisecondes d'époque (UTC)
- `timestampUtc` : chaîne ISO 8601 UTC

Les champs bruts du fournisseur sont conservés afin que rien ne soit perdu.

- Slack : chaînes de type époque de l'API
- Discord : horodatages ISO UTC
- Telegram/WhatsApp : horodatages numériques/ISO spécifiques au fournisseur

Si vous avez besoin de l'heure locale, convertissez-la en aval en utilisant le fuseau horaire connu.

## Documents connexes

- [System Prompt](/concepts/system-prompt)
- [Timezones](/concepts/timezone)
- [Messages](/concepts/messages)
