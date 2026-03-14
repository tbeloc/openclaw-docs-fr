---
summary: "Analyse de la localisation des canaux entrants (Telegram + WhatsApp) et champs de contexte"
read_when:
  - Adding or modifying channel location parsing
  - Using location context fields in agent prompts or tools
title: "Analyse de la localisation des canaux"
---

# Analyse de la localisation des canaux

OpenClaw normalise les localisations partagées depuis les canaux de chat en :

- texte lisible ajouté au corps du message entrant, et
- champs structurés dans la charge utile du contexte de réponse automatique.

Actuellement supportés :

- **Telegram** (épingles de localisation + lieux + localisations en direct)
- **WhatsApp** (locationMessage + liveLocationMessage)
- **Matrix** (`m.location` avec `geo_uri`)

## Formatage du texte

Les localisations sont rendues sous forme de lignes conviviales sans crochets :

- Épingle :
  - `📍 48.858844, 2.294351 ±12m`
- Lieu nommé :
  - `📍 Eiffel Tower — Champ de Mars, Paris (48.858844, 2.294351 ±12m)`
- Partage en direct :
  - `🛰 Live location: 48.858844, 2.294351 ±12m`

Si le canal inclut une légende/commentaire, il est ajouté à la ligne suivante :

```
📍 48.858844, 2.294351 ±12m
Meet here
```

## Champs de contexte

Quand une localisation est présente, ces champs sont ajoutés à `ctx` :

- `LocationLat` (nombre)
- `LocationLon` (nombre)
- `LocationAccuracy` (nombre, mètres ; optionnel)
- `LocationName` (chaîne de caractères ; optionnel)
- `LocationAddress` (chaîne de caractères ; optionnel)
- `LocationSource` (`pin | place | live`)
- `LocationIsLive` (booléen)

## Notes par canal

- **Telegram** : les lieux sont mappés à `LocationName/LocationAddress` ; les localisations en direct utilisent `live_period`.
- **WhatsApp** : `locationMessage.comment` et `liveLocationMessage.caption` sont ajoutés comme ligne de légende.
- **Matrix** : `geo_uri` est analysé comme une épingle de localisation ; l'altitude est ignorée et `LocationIsLive` est toujours faux.
