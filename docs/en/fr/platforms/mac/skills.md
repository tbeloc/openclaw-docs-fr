---
summary: "Interface des paramètres Skills macOS et statut soutenu par la passerelle"
read_when:
  - Updating the macOS Skills settings UI
  - Changing skills gating or install behavior
title: "Skills"
---

# Skills (macOS)

L'application macOS expose les skills OpenClaw via la passerelle ; elle n'analyse pas les skills localement.

## Source de données

- `skills.status` (passerelle) retourne tous les skills ainsi que l'éligibilité et les exigences manquantes
  (y compris les blocages de liste blanche pour les skills groupés).
- Les exigences sont dérivées de `metadata.openclaw.requires` dans chaque `SKILL.md`.

## Actions d'installation

- `metadata.openclaw.install` définit les options d'installation (brew/node/go/uv).
- L'application appelle `skills.install` pour exécuter les installateurs sur l'hôte de la passerelle.
- La passerelle expose un seul installateur préféré lorsque plusieurs sont fournis
  (brew si disponible, sinon gestionnaire de nœuds de `skills.install`, npm par défaut).

## Clés Env/API

- L'application stocke les clés dans `~/.openclaw/openclaw.json` sous `skills.entries.<skillKey>`.
- `skills.update` corrige `enabled`, `apiKey`, et `env`.

## Mode distant

- Les mises à jour d'installation et de configuration se produisent sur l'hôte de la passerelle (pas sur le Mac local).
