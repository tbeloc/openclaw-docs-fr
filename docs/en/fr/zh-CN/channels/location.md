---
read_when:
  - Ajouter ou modifier l'analyse de localisation des canaux
  - Utiliser les champs de contexte de localisation dans les invites d'agent ou les outils
summary: Analyse de localisation des canaux entrants (Telegram + WhatsApp) et champs de contexte
title: Analyse de localisation des canaux
x-i18n:
  generated_at: "2026-02-01T19:21:46Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 5602ef105c3da7e47497bfed8fc343dd8d7f3c019ff7e423a08b25092c5a1837
  source_path: channels/location.md
  workflow: 14
---

# Analyse de localisation des canaux

OpenClaw normalise les localisations partagées dans les canaux de chat en :

- Texte lisible attaché au corps du message entrant, et
- Champs structurés dans la charge utile du contexte de réponse automatique.

Actuellement supporté :

- **Telegram** (épingles de localisation + lieux + localisation en direct)
- **WhatsApp** (locationMessage + liveLocationMessage)
- **Matrix** (`m.location` avec `geo_uri`)

## Format texte

Les localisations sont présentées dans un format de ligne convivial, sans parenthèses :

- Épingle :
  - `📍 48.858844, 2.294351 ±12m`
- Lieu nommé :
  - `📍 Eiffel Tower — Champ de Mars, Paris (48.858844, 2.294351 ±12m)`
- Partage en direct :
  - `🛰 Live location: 48.858844, 2.294351 ±12m`

Si le canal contient un titre/commentaire, il est attaché à la ligne suivante :

```
📍 48.858844, 2.294351 ±12m
Meet here
```

## Champs de contexte

Lorsqu'une localisation est présente, les champs suivants sont ajoutés à `ctx` :

- `LocationLat` (nombre)
- `LocationLon` (nombre)
- `LocationAccuracy` (nombre, mètres ; optionnel)
- `LocationName` (chaîne ; optionnel)
- `LocationAddress` (chaîne ; optionnel)
- `LocationSource` (`pin | place | live`)
- `LocationIsLive` (booléen)

## Notes spécifiques aux canaux

- **Telegram** : Les lieux sont mappés à `LocationName/LocationAddress` ; la localisation en direct utilise `live_period`.
- **WhatsApp** : `locationMessage.comment` et `liveLocationMessage.caption` sont attachés comme ligne de titre.
- **Matrix** : `geo_uri` est analysé comme une localisation d'épingle ; l'altitude est ignorée, `LocationIsLive` est toujours false.
