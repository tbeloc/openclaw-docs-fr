---
last_updated: "2026-01-05"
owner: openclaw
status: complete
summary: Renforcer le traitement des entrées de cron.add, aligner le schéma, améliorer l'interface utilisateur cron/outils d'agent
title: Renforcement de Cron Add
x-i18n:
  generated_at: "2026-02-03T07:47:26Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d7e469674bd9435b846757ea0d5dc8f174eaa8533917fc013b1ef4f82859496d
  source_path: experiments/plans/cron-add-hardening.md
  workflow: 15
---

# Renforcement de Cron Add & Alignement du Schéma

## Contexte

Les journaux récents de la passerelle Gateway montrent des échecs répétés de `cron.add` avec des paramètres invalides (absence de `sessionTarget`, `wakeMode`, `payload`, et `schedule` mal formaté). Cela indique qu'au moins un client (probablement le chemin d'appel de l'outil d'agent) envoie des charges utiles de tâche encapsulées ou partiellement spécifiées. De plus, il existe une dérive entre l'énumération du fournisseur cron en TypeScript, le schéma Gateway, les drapeaux CLI et les types de formulaire UI, ainsi qu'une inadéquation UI pour `cron.status` (attendant `jobCount` alors que Gateway retourne `jobs`).

## Objectifs

- Arrêter les déchets INVALID_REQUEST de `cron.add` en normalisant les charges utiles encapsulées courantes et en déduisant le champ `kind` manquant.
- Aligner la liste des fournisseurs cron entre le schéma Gateway, les types cron, la documentation CLI et les formulaires UI.
- Rendre le schéma de l'outil cron d'agent explicite afin que l'LLM génère des charges utiles de tâche correctes.
- Corriger l'affichage du comptage des tâches d'état cron de l'interface utilisateur Control.
- Ajouter des tests pour couvrir la normalisation et le comportement des outils.

## Non-objectifs

- Modifier la sémantique de planification cron ou le comportement d'exécution des tâches.
- Ajouter de nouveaux types de planification ou d'analyse d'expressions cron.
- Apporter de grands changements à l'interface utilisateur/UX cron au-delà des corrections de champs nécessaires.

## Résultats (écarts actuels)

- Le `CronPayloadSchema` dans Gateway exclut `signal` + `imessage`, tandis que les types TS les incluent.
- CronStatus de l'interface utilisateur Control attend `jobCount`, mais Gateway retourne `jobs`.
- Le schéma de l'outil cron d'agent permet un objet `job` arbitraire, entraînant des entrées mal formatées.
- Gateway valide strictement `cron.add` sans normalisation, donc les charges utiles encapsulées échouent.

## Changements

- `cron.add` et `cron.update` normalisent désormais les formes encapsulées courantes et déduisent le champ `kind` manquant.
- Le schéma de l'outil cron d'agent correspond au schéma Gateway, réduisant les charges utiles invalides.
- L'énumération des fournisseurs est alignée entre Gateway, CLI, UI et le sélecteur macOS.
- L'interface utilisateur Control utilise le champ de comptage `jobs` de Gateway pour afficher l'état.

## Comportement actuel

- **Normalisation :** Les charges utiles encapsulées `data`/`job` sont déballées ; `schedule.kind` et `payload.kind` sont déduits en toute sécurité.
- **Valeurs par défaut :** Des valeurs par défaut sûres sont appliquées à `wakeMode` et `sessionTarget` lorsqu'ils sont manquants.
- **Fournisseurs :** Discord/Slack/Signal/iMessage s'affichent désormais de manière cohérente dans CLI/UI.

Voir [Tâches Cron](/automation/cron-jobs) pour les formes normalisées et les exemples.

## Validation

- Observer si les erreurs INVALID_REQUEST de `cron.add` diminuent dans les journaux Gateway.
- Confirmer que l'état cron de l'interface utilisateur Control affiche le comptage des tâches après actualisation.

## Travail de suivi optionnel

- Test de fumée manuel de l'interface utilisateur Control : ajouter une tâche cron pour chaque fournisseur + vérifier le comptage des tâches d'état.

## Questions ouvertes

- `cron.add` devrait-il accepter un `state` explicite du client (actuellement interdit par le schéma) ?
- Devrions-nous autoriser `webchat` comme fournisseur de livraison explicite (actuellement filtré dans l'analyse de livraison) ?
