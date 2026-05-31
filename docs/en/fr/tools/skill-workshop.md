---
summary: "Créer et mettre à jour les compétences de l'espace de travail via l'examen de Skill Workshop"
read_when:
  - You want the agent to create or update a skill from chat
  - You need to review, apply, reject, or quarantine a generated skill draft
  - You are configuring Skill Workshop approval, autonomy, storage, or limits
title: "Skill Workshop"
sidebarTitle: "Skill Workshop"
---

Skill Workshop est le chemin gouverné d'OpenClaw pour créer et mettre à jour les
compétences de l'espace de travail.

Les agents et les opérateurs n'écrivent pas directement les fichiers `SKILL.md`
actifs via ce chemin. Ils créent d'abord une **proposition**. Une proposition est
un brouillon en attente contenant le contenu de compétence proposé, la liaison
cible, l'état du scanner, les hashes, les métadonnées des fichiers de support et
les métadonnées de restauration. Elle ne devient une compétence active que
lorsqu'elle est appliquée.

Skill Workshop écrit uniquement les compétences de l'espace de travail. Il ne
modifie pas les compétences groupées, de plugin, ClawHub, extra-root, gérées,
d'agent personnel ou système.

## Fonctionnement

- **Proposition d'abord :** le contenu de compétence généré est stocké sous
  `PROPOSAL.md`, pas `SKILL.md`.
- **L'application est la seule écriture active :** créer, mettre à jour et
  réviser ne modifient pas les compétences actives.
- **Portée de l'espace de travail :** les créations ciblent la racine `skills/`
  de l'espace de travail. Les mises à jour sont autorisées uniquement pour les
  compétences d'espace de travail inscriptibles.
- **Pas de remplacement :** la création échoue si la compétence cible existe
  déjà.
- **Lié au hash :** les propositions de mise à jour se lient au hash cible
  actuel et deviennent obsolètes si la compétence active change avant
  l'application.
- **Gated par scanner :** l'application réexécute l'analyse avant d'écrire.
- **Récupérable :** l'application écrit les métadonnées de restauration avant de
  modifier les fichiers actifs.
- **Surfaces cohérentes :** le chat, la CLI et la passerelle appellent tous le
  même service Skill Workshop.

## Cycle de vie

```text
create/update -> pending
revise        -> pending
apply         -> applied
reject        -> rejected
quarantine    -> quarantined
target change -> stale
```

Seules les propositions `pending` peuvent être révisées, appliquées, rejetées ou
mises en quarantaine.

## Chat

Demandez à l'agent la compétence que vous souhaitez. L'agent appelle
`skill_workshop` et retourne un identifiant de proposition.

Créer :

```text
Make a skill called morning-catchup that runs my Monday inbox routine.
```

Mettre à jour une compétence d'espace de travail existante :

```text
Update trip-planning to also check seat maps before booking.
```

Itérer sur une proposition en attente :

```text
Show me the morning-catchup proposal.
Revise it to also flag anything marked urgent.
Apply the morning-catchup proposal.
```

Par défaut, les actions `apply`, `reject` et `quarantine` initiées par l'agent
affichent une invite d'approbation avant leur exécution. Définissez
`skills.workshop.approvalPolicy` sur `"auto"` pour ignorer l'invite dans les
environnements de confiance.

## CLI

Créer une nouvelle proposition de compétence :

```bash
openclaw skills workshop propose-create \
  --name morning-catchup \
  --description "Daily inbox catch-up: triage, archive, surface, draft, plan" \
  --proposal ./PROPOSAL.md
```

Créer une proposition de mise à jour pour une compétence d'espace de travail
existante :

```bash
openclaw skills workshop propose-update trip-planning --proposal ./PROPOSAL.md
```

Lister et inspecter :

```bash
openclaw skills workshop list
openclaw skills workshop inspect <proposal-id>
```

Réviser avant approbation :

```bash
openclaw skills workshop revise <proposal-id> --proposal ./PROPOSAL.md
```

Clôturer la proposition :

```bash
openclaw skills workshop apply <proposal-id>
openclaw skills workshop reject <proposal-id> --reason "Duplicate"
openclaw skills workshop quarantine <proposal-id> --reason "Needs security review"
```

## Contenu de la proposition

En attente, la proposition est stockée sous `PROPOSAL.md` avec les métadonnées
spécifiques à la proposition :

```markdown
---
name: "morning-catchup"
description: "Daily inbox catch-up: triage, archive, surface, draft, plan"
status: proposal
version: "v1"
date: "2026-05-30T00:00:00.000Z"
---
```

À l'application, Skill Workshop écrit le `SKILL.md` actif et supprime les champs
spécifiques à la proposition : `status`, `version` de proposition et `date` de
proposition.

## Fichiers de support

Utilisez `--proposal-dir` lorsque la compétence proposée a besoin de fichiers
à côté de `PROPOSAL.md` :

```bash
openclaw skills workshop propose-create \
  --name weekly-update \
  --description "Friday wrap-up: stats, highlights, next week's top three" \
  --proposal-dir ./weekly-update-proposal
```

Le répertoire doit contenir `PROPOSAL.md`. Les fichiers de support doivent être
sous :

- `assets/`
- `examples/`
- `references/`
- `scripts/`
- `templates/`

Skill Workshop analyse, hache et stocke les fichiers de support avec la
proposition. Ils sont écrits à côté du `SKILL.md` actif uniquement à
l'application.

Les chemins de fichiers de support rejetés incluent les chemins absolus, les
segments de chemin cachés, la traversée de répertoires, les chemins
chevauchants, les fichiers exécutables des répertoires de proposition, le texte
non-UTF-8 et les fichiers en dehors des dossiers de support standard.

## Outil d'agent

Le modèle utilise `skill_workshop` :

```text
action: create | update | revise | list | inspect | apply | reject | quarantine
```

Les agents doivent utiliser `skill_workshop` pour le travail de compétence
généré. Ils ne doivent pas créer ou modifier les fichiers de proposition via
`write`, `edit`, `exec`, les commandes shell ou les opérations directes du
système de fichiers.

## Approbation et autonomie

```json5
{
  skills: {
    workshop: {
      autonomous: {
        enabled: false,
      },
      approvalPolicy: "pending",
      maxPending: 50,
      maxSkillBytes: 40000,
    },
  },
}
```

- `autonomous.enabled` : permet à OpenClaw de créer des propositions en attente
  à partir de signaux de conversation durables après des tours réussis. Par
  défaut : `false`.
- `approvalPolicy: "pending"` : nécessite une invite d'approbation avant les
  actions `apply`, `reject` ou `quarantine` initiées par l'agent.
- `approvalPolicy: "auto"` : ignore cette invite. L'agent doit toujours appeler
  l'action.
- `maxPending` : limite les propositions en attente et en quarantaine par espace
  de travail.
- `maxSkillBytes` : limite la taille du corps de la proposition. Par défaut :
  `40000`.

Les descriptions de proposition sont toujours limitées à 160 octets.

## Méthodes de passerelle

```text
skills.proposals.list
skills.proposals.inspect
skills.proposals.create
skills.proposals.update
skills.proposals.revise
skills.proposals.apply
skills.proposals.reject
skills.proposals.quarantine
```

Les méthodes en lecture seule nécessitent `operator.read`. Les méthodes de
mutation nécessitent `operator.admin`.

## Stockage

```text
<OPENCLAW_STATE_DIR>/skill-workshop/
  proposals.json
  proposals/<proposal-id>/
    proposal.json
    PROPOSAL.md
    rollback.json
    assets/
    examples/
    references/
    scripts/
    templates/
```

Répertoire d'état par défaut : `~/.openclaw`.

- `proposal.json` : enregistrement de proposition canonique.
- `proposals.json` : index de listage rapide, reconstructible à partir des
  dossiers de proposition.
- `PROPOSAL.md` : proposition de compétence en attente.
- `rollback.json` : métadonnées de récupération écrites avant que l'application
  ne modifie les fichiers actifs.

## Limites

- Description : 160 octets.
- Corps de la proposition : `skills.workshop.maxSkillBytes` (par défaut 40 000).
- Fichiers de support : 64 par proposition.
- Taille du fichier de support : 256 Ko chacun, 2 Mo au total.
- Propositions en attente et en quarantaine : `skills.workshop.maxPending` par
  espace de travail (par défaut 50).

## Dépannage

| Problème                                       | Résolution                                                                                                      |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `Skill proposal description is too large`      | Raccourcissez `description` à 160 octets ou moins.                                                              |
| `Skill proposal content is too large`          | Raccourcissez le corps de la proposition ou augmentez `skills.workshop.maxSkillBytes`.                          |
| `Target skill changed after proposal creation` | Révisez la proposition par rapport à la cible actuelle, ou créez une nouvelle proposition.                      |
| `Proposal scan failed`                         | Inspectez les résultats du scanner, puis révisez ou mettez en quarantaine la proposition.                       |
| `Support file paths must be under one of...`   | Déplacez les fichiers de support sous `assets/`, `examples/`, `references/`, `scripts/` ou `templates/`.       |
| La proposition ne s'affiche pas dans la liste  | Vérifiez l'espace de travail `--agent` sélectionné et `OPENCLAW_STATE_DIR`.                                     |

## Connexes

- [Skills](/fr/tools/skills) pour l'ordre de chargement, la précédence et la
  visibilité
- [Creating skills](/fr/tools/creating-skills) pour les bases de `SKILL.md`
  écrites à la main
- [Skills config](/fr/tools/skills-config) pour le schéma complet
  `skills.workshop`
- [Skills CLI](/fr/cli/skills) pour les commandes `openclaw skills`
