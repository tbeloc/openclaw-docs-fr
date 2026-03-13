---
read_when:
  - 添加位置节点支持或权限 UI
  - 设计后台位置 + 推送流程
summary: 节点的位置命令（location.get）、权限模式和后台行为
title: 位置命令
x-i18n:
  generated_at: "2026-02-03T07:50:59Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 23124096256384d2b28157352b072309c61c970a20e009aac5ce4a8250dc3764
  source_path: nodes/location-command.md
  workflow: 15
---

# Commande de localisation (nœud)

## Aperçu rapide

- `location.get` est une commande de nœud (via `node.invoke`).
- Désactivée par défaut.
- Configuration via sélecteur : Désactivé / Lors de l'utilisation / Toujours.
- Commutateur séparé : Localisation précise.

## Pourquoi un sélecteur (et non juste un commutateur)

Les permissions du système d'exploitation sont multi-niveaux. Nous pouvons exposer un sélecteur dans l'application, mais le système d'exploitation décide de l'autorisation réelle.

- iOS/macOS : L'utilisateur peut choisir **Lors de l'utilisation** ou **Toujours** dans l'invite système/les paramètres. L'application peut demander une mise à niveau, mais le système d'exploitation peut exiger d'accéder aux paramètres.
- Android : La localisation en arrière-plan est une permission distincte ; sur Android 10+, elle nécessite généralement un flux de paramètres.
- La localisation précise est une autorisation distincte (iOS 14+ "Précis", Android "Fin" vs "Approximatif").

Le sélecteur dans l'interface utilisateur détermine le mode que nous demandons ; l'autorisation réelle réside dans les paramètres du système d'exploitation.

## Modèle de configuration

Par appareil de nœud :

- `location.enabledMode` : `off | whileUsing | always`
- `location.preciseEnabled` : bool

Comportement de l'interface utilisateur :

- Sélectionner `whileUsing` demande la permission au premier plan.
- Sélectionner `always` assure d'abord `whileUsing`, puis demande l'arrière-plan (ou guide l'utilisateur vers les paramètres si nécessaire).
- Si le système d'exploitation refuse le niveau demandé, revenir au niveau le plus élevé accordé et afficher le statut.

## Mappage des permissions (node.permissions)

Optionnel. Les nœuds macOS signalent `location` via le mappage des permissions ; iOS/Android peuvent l'omettre.

## Commande : `location.get`

Appelée via `node.invoke`.

Paramètres (recommandés) :

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

- `LOCATION_DISABLED` : Le sélecteur est désactivé.
- `LOCATION_PERMISSION_REQUIRED` : Permission manquante pour le mode demandé.
- `LOCATION_BACKGROUND_UNAVAILABLE` : L'application est en arrière-plan mais seule l'utilisation est autorisée.
- `LOCATION_TIMEOUT` : Pas de localisation dans le délai imparti.
- `LOCATION_UNAVAILABLE` : Défaillance système / aucun fournisseur.

## Comportement en arrière-plan (futur)

Objectif : Le modèle peut demander la localisation lorsque le nœud est en arrière-plan, mais uniquement si :

- L'utilisateur a sélectionné **Toujours**.
- Le système d'exploitation a accordé la permission de localisation en arrière-plan.
- L'application est autorisée à s'exécuter en arrière-plan pour obtenir la localisation (mode arrière-plan iOS / service au premier plan Android ou permission spéciale).

Flux de déclenchement par notification (futur) :

1. La passerelle envoie une notification au nœud (notification silencieuse ou données FCM).
2. Le nœud se réveille brièvement et demande la localisation à l'appareil.
3. Le nœud transmet la charge utile à la passerelle.

Remarques :

- iOS : Nécessite la permission Toujours + mode localisation en arrière-plan. Les notifications silencieuses peuvent être limitées ; les défaillances intermittentes sont attendues.
- Android : La localisation en arrière-plan peut nécessiter un service au premier plan ; sinon, les refus sont attendus.

## Intégration modèle/ensemble d'outils

- Interface d'outils : L'outil `nodes` ajoute l'opération `location_get` (nécessite un nœud).
- CLI : `openclaw nodes location get --node <id>`.
- Guide d'agent : Appeler uniquement si l'utilisateur a activé la localisation et comprend la portée.

## Texte UX (recommandé)

- Désactivé : "Le partage de localisation est désactivé."
- Lors de l'utilisation : "Uniquement lorsque OpenClaw est ouvert."
- Toujours : "Autoriser la localisation en arrière-plan. Nécessite les permissions système."
- Précis : "Utiliser la localisation GPS précise. Désactiver pour partager une localisation approximative."
