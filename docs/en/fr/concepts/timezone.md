---
summary: "Gestion des fuseaux horaires pour les agents, enveloppes et invites"
read_when:
  - Vous devez comprendre comment les horodatages sont normalisés pour le modèle
  - Configuration du fuseau horaire utilisateur pour les invites système
title: "Fuseaux horaires"
---

# Fuseaux horaires

OpenClaw normalise les horodatages afin que le modèle voie une **heure de référence unique**.

## Enveloppes de messages (locales par défaut)

Les messages entrants sont enveloppés comme suit :

```
[Provider ... 2026-01-05 16:26 PST] message text
```

L'horodatage dans l'enveloppe est **local à l'hôte par défaut**, avec une précision à la minute.

Vous pouvez le remplacer par :

```json5
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | fuseau horaire IANA
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

- `envelopeTimezone: "utc"` utilise UTC.
- `envelopeTimezone: "user"` utilise `agents.defaults.userTimezone` (revient au fuseau horaire de l'hôte).
- Utilisez un fuseau horaire IANA explicite (par exemple, `"Europe/Vienna"`) pour un décalage fixe.
- `envelopeTimestamp: "off"` supprime les horodatages absolus des en-têtes d'enveloppe.
- `envelopeElapsed: "off"` supprime les suffixes de temps écoulé (style `+2m`).

### Exemples

**Local (par défaut) :**

```
[Signal Alice +1555 2026-01-18 00:19 PST] hello
```

**Fuseau horaire fixe :**

```
[Signal Alice +1555 2026-01-18 06:19 GMT+1] hello
```

**Temps écoulé :**

```
[Signal Alice +1555 +2m 2026-01-18T05:19Z] follow-up
```

## Charges utiles d'outils (données brutes du fournisseur + champs normalisés)

Les appels d'outils (`channels.discord.readMessages`, `channels.slack.readMessages`, etc.) retournent des **horodatages bruts du fournisseur**.
Nous joignons également des champs normalisés pour la cohérence :

- `timestampMs` (millisecondes d'époque UTC)
- `timestampUtc` (chaîne ISO 8601 UTC)

Les champs bruts du fournisseur sont conservés.

## Fuseau horaire utilisateur pour l'invite système

Définissez `agents.defaults.userTimezone` pour indiquer au modèle le fuseau horaire local de l'utilisateur. S'il n'est
pas défini, OpenClaw résout le **fuseau horaire de l'hôte à l'exécution** (sans écriture de configuration).

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

L'invite système inclut :

- Section `Current Date & Time` avec l'heure locale et le fuseau horaire
- `Time format: 12-hour` ou `24-hour`

Vous pouvez contrôler le format de l'invite avec `agents.defaults.timeFormat` (`auto` | `12` | `24`).

Consultez [Date & Time](/date-time) pour le comportement complet et des exemples.
