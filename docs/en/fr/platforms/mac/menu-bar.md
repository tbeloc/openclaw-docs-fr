---
summary: "Logique d'état de la barre de menu et ce qui est affiché aux utilisateurs"
read_when:
  - Tweaking mac menu UI or status logic
title: "Barre de menu"
---

# Logique d'état de la barre de menu

## Ce qui est affiché

- Nous affichons l'état actuel du travail de l'agent dans l'icône de la barre de menu et dans la première ligne d'état du menu.
- L'état de santé est masqué pendant que le travail est actif ; il réapparaît quand toutes les sessions sont inactives.
- Le bloc « Nodes » du menu liste **uniquement les appareils** (nœuds appairés via `node.list`), pas les entrées client/présence.
- Une section « Usage » apparaît sous Context quand des snapshots d'utilisation du fournisseur sont disponibles.

## Modèle d'état

- Sessions : les événements arrivent avec `runId` (par exécution) plus `sessionKey` dans la charge utile. La session « principale » est la clé `main` ; en son absence, nous revenons à la session la plus récemment mise à jour.
- Priorité : main gagne toujours. Si main est actif, son état est affiché immédiatement. Si main est inactif, la session non-main la plus récemment active est affichée. Nous ne basculons pas en cours d'activité ; nous ne changeons que quand la session actuelle devient inactive ou que main devient actif.
- Types d'activité :
  - `job` : exécution de commande de haut niveau (`state: started|streaming|done|error`).
  - `tool` : `phase: start|result` avec `toolName` et `meta/args`.

## Énumération IconState (Swift)

- `idle`
- `workingMain(ActivityKind)`
- `workingOther(ActivityKind)`
- `overridden(ActivityKind)` (débogage override)

### ActivityKind → glyphe

- `exec` → 💻
- `read` → 📄
- `write` → ✍️
- `edit` → 📝
- `attach` → 📎
- défaut → 🛠️

### Mappage visuel

- `idle` : créature normale.
- `workingMain` : badge avec glyphe, teinte complète, animation de jambe « working ».
- `workingOther` : badge avec glyphe, teinte atténuée, pas de scurry.
- `overridden` : utilise le glyphe/la teinte choisis indépendamment de l'activité.

## Texte de la ligne d'état (menu)

- Pendant que le travail est actif : `<Session role> · <activity label>`
  - Exemples : `Main · exec: pnpm test`, `Other · read: apps/macos/Sources/OpenClaw/AppState.swift`.
- Quand inactif : revient au résumé de santé.

## Ingestion d'événements

- Source : événements `agent` du canal de contrôle (`ControlChannel.handleAgentEvent`).
- Champs analysés :
  - `stream: "job"` avec `data.state` pour start/stop.
  - `stream: "tool"` avec `data.phase`, `name`, `meta`/`args` optionnel.
- Étiquettes :
  - `exec` : première ligne de `args.command`.
  - `read`/`write` : chemin raccourci.
  - `edit` : chemin plus type de changement déduit de `meta`/comptages de diff.
  - fallback : nom de l'outil.

## Override de débogage

- Paramètres ▸ Débogage ▸ sélecteur « Icon override » :
  - `System (auto)` (défaut)
  - `Working: main` (par type d'outil)
  - `Working: other` (par type d'outil)
  - `Idle`
- Stocké via `@AppStorage("iconOverride")` ; mappé à `IconState.overridden`.

## Liste de contrôle de test

- Déclencher un job de session principale : vérifier que l'icône bascule immédiatement et que la ligne d'état affiche l'étiquette principale.
- Déclencher un job de session non-principale pendant que main est inactif : l'icône/l'état affiche non-principal ; reste stable jusqu'à ce qu'il se termine.
- Démarrer main pendant que other est actif : l'icône bascule à main instantanément.
- Rafales d'outils rapides : s'assurer que le badge ne scintille pas (TTL grace sur les résultats d'outils).
- La ligne de santé réapparaît une fois que toutes les sessions sont inactives.
