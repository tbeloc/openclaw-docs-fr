---
summary: "Commande de localisation pour les nœuds (location.get), modes de permission et comportement de premier plan Android"
read_when:
  - Adding location node support or permissions UI
  - Designing Android location permissions or foreground behavior
title: "Commande de localisation"
---

# Commande de localisation (nœuds)

## TL;DR

- `location.get` est une commande de nœud (via `node.invoke`).
- Désactivée par défaut.
- Les paramètres de l'application Android utilisent un sélecteur : Désactivé / Pendant l'utilisation.
- Bascule séparée : Localisation précise.

## Pourquoi un sélecteur (et non juste un commutateur)

Les permissions du système d'exploitation sont multi-niveaux. Nous pouvons exposer un sélecteur dans l'application, mais le système d'exploitation décide toujours de l'autorisation réelle.

- iOS/macOS peut exposer **Pendant l'utilisation** ou **Toujours** dans les invites système/Paramètres.
- L'application Android prend actuellement en charge uniquement la localisation au premier plan.
- La localisation précise est une autorisation séparée (iOS 14+ « Précis », Android « fine » vs « coarse »).

Le sélecteur dans l'interface utilisateur détermine notre mode demandé ; l'autorisation réelle se trouve dans les paramètres du système d'exploitation.

## Modèle de paramètres

Par appareil de nœud :

- `location.enabledMode`: `off | whileUsing`
- `location.preciseEnabled`: bool

Comportement de l'interface utilisateur :

- La sélection de `whileUsing` demande la permission de premier plan.
- Si le système d'exploitation refuse le niveau demandé, revenir au niveau autorisé le plus élevé et afficher le statut.

## Mappage des permissions (node.permissions)

Optionnel. Le nœud macOS signale `location` via la carte des permissions ; iOS/Android peuvent l'omettre.

## Commande : `location.get`

Appelée via `node.invoke`.

Paramètres (suggérés) :

```json
{
  "timeoutMs": 10000,
  "maxAgeMs": 15000,
  "desiredAccuracy": "coarse|balanced|precise"
}
```

Charge utile de réponse :

```json
{
  "lat": 48.20849,
  "lon": 16.37208,
  "accuracyMeters": 12.5,
  "altitudeMeters": 182.0,
  "speedMps": 0.0,
  "headingDeg": 270.0,
  "timestamp": "2026-01-03T12:34:56.000Z",
  "isPrecise": true,
  "source": "gps|wifi|cell|unknown"
}
```

Erreurs (codes stables) :

- `LOCATION_DISABLED`: le sélecteur est désactivé.
- `LOCATION_PERMISSION_REQUIRED`: permission manquante pour le mode demandé.
- `LOCATION_BACKGROUND_UNAVAILABLE`: l'application est en arrière-plan mais seul « Pendant l'utilisation » est autorisé.
- `LOCATION_TIMEOUT`: aucune correction à temps.
- `LOCATION_UNAVAILABLE`: défaillance du système / aucun fournisseur.

## Comportement en arrière-plan

- L'application Android refuse `location.get` en arrière-plan.
- Gardez OpenClaw ouvert lors de la demande de localisation sur Android.
- D'autres plates-formes de nœuds peuvent différer.

## Intégration modèle/outils

- Surface d'outil : l'outil `nodes` ajoute l'action `location_get` (nœud requis).
- CLI : `openclaw nodes location get --node <id>`.
- Directives d'agent : appelez uniquement lorsque l'utilisateur a activé la localisation et comprend la portée.

## Copie UX (suggérée)

- Désactivé : « Le partage de localisation est désactivé. »
- Pendant l'utilisation : « Uniquement lorsque OpenClaw est ouvert. »
- Précis : « Utiliser la localisation GPS précise. Désactivez pour partager une localisation approximative. »
