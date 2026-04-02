---
summary: "Couche d'orchestration de flux TaskFlow au-dessus des tâches de fond"
read_when:
  - Vous voulez comprendre comment TaskFlow se rapporte aux tâches de fond
  - Vous rencontrez TaskFlow ou des flux openclaw dans les notes de version ou la documentation
  - Vous voulez inspecter ou gérer l'état durable du flux
title: "TaskFlow"
---

# TaskFlow

TaskFlow est le substrat d'orchestration de flux qui se situe au-dessus des [tâches de fond](/fr/automation/tasks). Il gère les flux multi-étapes durables avec leur propre état, suivi des révisions et sémantique de synchronisation, tandis que les tâches individuelles restent l'unité de travail détaché.

## Modes de synchronisation

TaskFlow supporte deux modes de synchronisation :

- **Géré** — TaskFlow possède le cycle de vie de bout en bout, créant et pilotant les tâches à mesure que les étapes du flux progressent.
- **Miroir** — TaskFlow observe les tâches créées en externe et maintient l'état du flux en synchronisation sans prendre possession de la création de tâches.

## État durable et suivi des révisions

Chaque flux persiste son propre état et suit les révisions afin que la progression survive aux redémarrages de la passerelle. Le suivi des révisions permet la détection de conflits lorsque plusieurs sources tentent d'avancer le même flux.

## Commandes CLI

```bash
# Lister les flux actifs et récents
openclaw flows list

# Afficher les détails d'un flux spécifique
openclaw flows show <lookup>

# Annuler un flux en cours d'exécution
openclaw flows cancel <lookup>
```

- `openclaw flows list` — affiche les flux suivis avec le statut et le mode de synchronisation
- `openclaw flows show <lookup>` — inspecter un flux par identifiant de flux ou clé de recherche
- `openclaw flows cancel <lookup>` — annuler un flux en cours d'exécution et ses tâches actives

## Comment les flux se rapportent aux tâches

Les flux coordonnent les tâches, ils ne les remplacent pas. Un seul flux peut piloter plusieurs tâches de fond au cours de sa durée de vie. Utilisez `openclaw tasks` pour inspecter les enregistrements de tâches individuels et `openclaw flows` pour inspecter le flux orchestrant.

## Connexes

- [Tâches de fond](/fr/automation/tasks) — le registre de travail détaché que les flux coordonnent
- [CLI : flows](/fr/cli/flows) — référence de commande CLI pour `openclaw flows`
- [Aperçu de l'automatisation](/fr/automation) — tous les mécanismes d'automatisation en un coup d'œil
- [Tâches Cron](/fr/automation/cron-jobs) — tâches planifiées qui peuvent alimenter les flux
