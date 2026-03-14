---
read_when:
  - Besoin de comprendre comment les horodatages sont normalisés pour le modèle
  - Configuration du fuseau horaire utilisateur pour les invites système
summary: Gestion des fuseaux horaires pour les agents, enveloppes et invites
title: Fuseau horaire
x-i18n:
  generated_at: "2026-02-01T20:24:13Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 9ee809c96897db1126c7efcaa5bf48a63cdcb2092abd4b3205af224ebd882766
  source_path: concepts/timezone.md
  workflow: 14
---

# Fuseau horaire

OpenClaw normalise les horodatages pour que le modèle voie **une seule heure de référence**.

## Enveloppe de message (fuseau horaire local par défaut)

Les messages entrants sont encapsulés dans l'enveloppe suivante :

```
[Provider ... 2026-01-05 16:26 PST] message text
```

L'horodatage dans l'enveloppe est **par défaut l'heure locale de l'hôte**, précis à la minute.

Vous pouvez le remplacer avec la configuration suivante :

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
- `envelopeTimezone: "user"` utilise `agents.defaults.userTimezone` (repli sur le fuseau horaire de l'hôte).
- Utilisez un fuseau horaire IANA explicite (par exemple `"Europe/Vienna"`) pour définir un décalage fixe.
- `envelopeTimestamp: "off"` supprime l'horodatage absolu de l'en-tête d'enveloppe.
- `envelopeElapsed: "off"` supprime le suffixe de temps écoulé (style `+2m`).

### Exemples

**Heure locale (par défaut) :**

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

## Charge utile d'outil (données brutes du fournisseur + champs normalisés)

Les appels d'outil (`channels.discord.readMessages`, `channels.slack.readMessages`, etc.) retournent **les horodatages bruts du fournisseur**. Nous ajoutons également des champs normalisés pour assurer la cohérence :

- `timestampMs` (millisecondes depuis l'époque UTC)
- `timestampUtc` (chaîne UTC ISO 8601)

Les champs bruts du fournisseur restent inchangés.

## Fuseau horaire utilisateur dans l'invite système

Définissez `agents.defaults.userTimezone` pour indiquer au modèle le fuseau horaire local de l'utilisateur. S'il n'est pas défini, OpenClaw **analyse le fuseau horaire de l'hôte** au moment de l'exécution (sans nécessiter d'écriture dans la configuration).

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

L'invite système contient :

- Une section `Current Date & Time` affichant l'heure locale et le fuseau horaire
- `Time format: 12-hour` ou `24-hour`

Vous pouvez contrôler le format de l'invite via `agents.defaults.timeFormat` (`auto` | `12` | `24`).

Pour plus de détails, consultez le comportement complet et les exemples dans [Date et heure](/date-time).
