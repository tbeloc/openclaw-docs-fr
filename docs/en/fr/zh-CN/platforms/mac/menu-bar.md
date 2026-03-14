---
read_when:
  - Ajuster l'interface utilisateur ou la logique d'état du menu Mac
summary: Logique d'état de la barre de menu et contenu affiché à l'utilisateur
title: Barre de menu
x-i18n:
  generated_at: "2026-02-01T21:33:00Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8eb73c0e671a76aae4ebb653c65147610bf3e6d3c9c0943d150e292e7761d16d
  source_path: platforms/mac/menu-bar.md
  workflow: 15
---

# Logique d'état de la barre de menu

## Contenu affiché

- Nous affichons l'état de travail actuel de l'agent dans l'icône de la barre de menu et dans la ligne d'état de la première ligne du menu.
- La ligne de santé est masquée lorsque le travail est actif ; elle réapparaît lorsque toutes les sessions sont inactives.
- Le bloc « Nœuds » dans le menu ne liste que les **appareils** (nœuds appairés via `node.list`), excluant les entrées de client/statut en ligne.
- La section « Utilisation » s'affiche sous le contexte lorsqu'un instantané d'utilisation du fournisseur est disponible.

## Modèle d'état

- Sessions : les événements portent `runId` (par exécution) et `sessionKey` dans la charge utile. La clé de la session « main » est `main` ; en cas d'absence, basculer vers la session la plus récemment mise à jour.
- Priorité : main a toujours la priorité. Si main est actif, afficher immédiatement son état. Si main est inactif, afficher la session non-main la plus récemment active. Ne pas basculer d'avant en arrière pendant une activité ; basculer uniquement lorsque la session actuelle devient inactive ou que main devient actif.
- Types d'activité :
  - `job` : exécution de commande de haut niveau (`state: started|streaming|done|error`).
  - `tool` : `phase: start|result`, contenant `toolName` et `meta/args`.

## Énumération IconState (Swift)

- `idle`
- `workingMain(ActivityKind)`
- `workingOther(ActivityKind)`
- `overridden(ActivityKind)` (remplacement de débogage)

### ActivityKind → symbole d'icône

- `exec` → 💻
- `read` → 📄
- `write` → ✍️
- `edit` → 📝
- `attach` → 📎
- Par défaut → 🛠️

### Mappage visuel

- `idle` : icône d'animal normal.
- `workingMain` : badge avec symbole d'icône, teinte complète, animation de jambes « travaillant ».
- `workingOther` : badge avec symbole d'icône, teinte douce, pas d'animation de course rapide.
- `overridden` : utiliser le symbole d'icône/la teinte sélectionnés, quel que soit l'état de l'activité.

## Texte de la ligne d'état (menu)

- Lorsque le travail est actif : `<rôle de session> · <étiquette d'activité>`
  - Exemples : `Main · exec: pnpm test`, `Other · read: apps/macos/Sources/OpenClaw/AppState.swift`.
- Lorsque inactif : revenir à l'affichage du résumé de santé.

## Réception d'événements

- Source : événements du canal de contrôle `agent` (`ControlChannel.handleAgentEvent`).
- Champs analysés :
  - `stream: "job"`, contenant `data.state` pour démarrage/arrêt.
  - `stream: "tool"`, contenant `data.phase`, `name`, optionnellement `meta`/`args`.
- Étiquettes :
  - `exec` : première ligne de `args.command`.
  - `read`/`write` : chemin raccourci.
  - `edit` : chemin plus type de modification déduit du comptage `meta`/diff.
  - Secours : nom de l'outil.

## Remplacement de débogage

- Paramètres ▸ Débogage ▸ sélecteur « Remplacement d'icône » :
  - `Système (automatique)` (par défaut)
  - `Travail : main` (par type d'outil)
  - `Travail : other` (par type d'outil)
  - `Inactif`
- Stocké via `@AppStorage("iconOverride")` ; mappé à `IconState.overridden`.

## Liste de contrôle de test

- Déclencher une tâche de session main : vérifier que l'icône bascule immédiatement et que la ligne d'état affiche l'étiquette main.
- Déclencher une tâche de session non-main lorsque main est inactif : l'icône/l'état affiche non-main ; rester stable jusqu'à la fin.
- Démarrer main pendant que other est actif : l'icône bascule immédiatement vers main.
- Appels d'outils en succession rapide : s'assurer que le badge ne clignote pas (période de grâce TTL pour les résultats d'outils).
- Après que toutes les sessions soient inactives, la ligne de santé réapparaît.
