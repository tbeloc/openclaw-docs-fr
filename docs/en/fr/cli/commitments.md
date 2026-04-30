---
summary: "Référence CLI pour `openclaw commitments` (inspecter et rejeter les suites inférées)"
read_when:
  - Vous souhaitez inspecter les engagements de suivi inférés
  - Vous souhaitez rejeter les vérifications en attente
  - Vous auditez ce que heartbeat peut livrer
title: "`openclaw commitments`"
---

Lister et gérer les engagements de suivi inférés.

Les engagements sont des mémoires de suivi à court terme créées à partir du
contexte de conversation, avec consentement explicite. Voir [Engagements inférés](/fr/concepts/commitments) pour le
guide conceptuel.

Sans sous-commande, `openclaw commitments` liste les engagements en attente.

## Utilisation

```bash
openclaw commitments [--all] [--agent <id>] [--status <status>] [--json]
openclaw commitments list [--all] [--agent <id>] [--status <status>] [--json]
openclaw commitments dismiss <id...> [--json]
```

## Options

- `--all`: afficher tous les statuts au lieu de seulement les engagements en attente.
- `--agent <id>`: filtrer par ID d'agent.
- `--status <status>`: filtrer par statut. Valeurs : `pending`, `sent`,
  `dismissed`, `snoozed`, ou `expired`.
- `--json`: sortie JSON lisible par machine.

## Exemples

Lister les engagements en attente :

```bash
openclaw commitments
```

Lister tous les engagements stockés :

```bash
openclaw commitments --all
```

Filtrer par agent :

```bash
openclaw commitments --agent main
```

Trouver les engagements reportés :

```bash
openclaw commitments --status snoozed
```

Rejeter un ou plusieurs engagements :

```bash
openclaw commitments dismiss cm_abc123 cm_def456
```

Exporter en JSON :

```bash
openclaw commitments --all --json
```

## Sortie

La sortie texte inclut :

- ID d'engagement
- statut
- type
- heure d'échéance la plus proche
- portée
- texte de vérification suggéré

La sortie JSON inclut également le chemin du magasin d'engagements et les enregistrements stockés complets.

## Voir aussi

- [Engagements inférés](/fr/concepts/commitments)
- [Aperçu de la mémoire](/fr/concepts/memory)
- [Heartbeat](/fr/gateway/heartbeat)
- [Tâches planifiées](/fr/automation/cron-jobs)
