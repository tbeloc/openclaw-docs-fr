---
read_when:
  - Vous modifiez la façon dont les horodatages sont affichés au modèle ou à l'utilisateur
  - Vous déboguez des problèmes de format d'heure dans les messages ou les sorties de prompt système
summary: Gestion des dates et heures dans les enveloppes, prompts, outils et connecteurs
title: Dates et heures
x-i18n:
  generated_at: "2026-02-01T20:24:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 753af5946a006215d6af2467fa478f3abb42b1dff027cf85d5dc4c7ba4b58d39
  source_path: date-time.md
  workflow: 14
---

# Dates et heures

OpenClaw utilise par défaut **l'heure locale de l'hôte comme horodatage de transport** et **utilise uniquement le fuseau horaire de l'utilisateur dans le prompt système**.
Les horodatages des fournisseurs sont conservés, de sorte que les outils conservent leur sémantique native (l'heure actuelle peut être obtenue via `session_status`).

## Enveloppe de message (heure locale par défaut)

Les messages entrants sont accompagnés d'un horodatage (précision à la minute) :

```
[Provider ... 2026-01-05 16:26 PST] message text
```

Cet horodatage d'enveloppe est **par défaut l'heure locale de l'hôte**, indépendamment du fuseau horaire du fournisseur.

Vous pouvez remplacer ce comportement :

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
- `envelopeTimezone: "local"` utilise le fuseau horaire de l'hôte.
- `envelopeTimezone: "user"` utilise `agents.defaults.userTimezone` (revient au fuseau horaire de l'hôte).
- Utilisez un fuseau horaire IANA explicite (par exemple `"America/Chicago"`) pour spécifier un fuseau horaire fixe.
- `envelopeTimestamp: "off"` supprime l'horodatage absolu de l'en-tête d'enveloppe.
- `envelopeElapsed: "off"` supprime le suffixe de temps écoulé (style `+2m`).

### Exemples

**Heure locale (par défaut) :**

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

## Prompt système : date et heure actuelles

Si le fuseau horaire de l'utilisateur est connu, le prompt système contient une section **date et heure actuelles** dédiée, contenant uniquement le **fuseau horaire** (sans format d'horloge/heure), pour maintenir la stabilité du cache du prompt :

```
Time zone: America/Chicago
```

Lorsque l'agent a besoin d'obtenir l'heure actuelle, utilisez l'outil `session_status` ; la ligne d'horodatage est incluse dans la carte d'état.

## Lignes d'événements système (heure locale par défaut)

Les événements système en file d'attente insérés dans le contexte de l'agent sont préfixés par un horodatage, utilisant la même sélection de fuseau horaire que l'enveloppe de message (par défaut : heure locale de l'hôte).

```
System: [2026-01-12 12:19:17 PST] Model switched.
```

### Configuration du fuseau horaire et du format de l'utilisateur

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

- `userTimezone` définit le **fuseau horaire local de l'utilisateur** dans le contexte du prompt.
- `timeFormat` contrôle le **format d'affichage 12 heures/24 heures** dans le prompt. `auto` suit les préférences du système d'exploitation.

## Détection du format d'heure (auto)

Lorsque `timeFormat: "auto"`, OpenClaw vérifie les préférences du système d'exploitation (macOS/Windows) et revient au format régional. La valeur détectée est **mise en cache par processus** pour éviter les appels système répétés.

## Charge utile des outils + connecteurs (heure native du fournisseur + champs normalisés)

Les outils de canal retournent **les horodatages natifs du fournisseur** et ajoutent des champs normalisés pour la cohérence :

- `timestampMs` : millisecondes depuis l'époque (UTC)
- `timestampUtc` : chaîne ISO 8601 UTC

Les champs natifs du fournisseur sont conservés, aucune donnée n'est perdue.

- Slack : chaîne de type époque de l'API
- Discord : horodatage ISO UTC
- Telegram/WhatsApp : horodatages numériques/ISO spécifiques au fournisseur

Si vous avez besoin de l'heure locale, effectuez la conversion en aval avec un fuseau horaire connu.

## Documentation connexe

- [Prompt système](/concepts/system-prompt)
- [Fuseau horaire](/concepts/timezone)
- [Messages](/concepts/messages)
