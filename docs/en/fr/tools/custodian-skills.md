---
title: "Compétences Custodian"
sidebarTitle: "Compétences Custodian"
summary: "Compétences opérationnelles versionnées par version qui seul l'agent Custodian configuré peut découvrir et utiliser."
read_when:
  - Configuring or extending the Custodian agent
  - Reviewing agent-only skill loading
  - Planning operational skill coverage
---

Les compétences Custodian sont des playbooks opérationnels versionnés par version fournis avec OpenClaw. Ils se trouvent sous `custodian-skills/` dans le package et se chargent au niveau de précédence des compétences groupées, mais uniquement pour l'agent résolu par `agents.defaults.systemAgent.agentId`.

Lorsque ce paramètre est absent, OpenClaw utilise le fallback d'agent système existant : l'agent unique configuré, ou le `main` hérité quand aucun roster d'agent explicite n'existe. Si plusieurs agents sont configurés et qu'aucun agent système n'est sélectionné, aucun agent ne reçoit la bibliothèque. Pour tous les autres agents, les compétences Custodian sont absentes de la découverte, des snapshots, des catalogues de commandes slash, de la synchronisation sandbox et de l'invite de compétences orientée modèle.

Les contrôles de compétences normaux s'appliquent toujours. `skills.entries.<name>.enabled: false` désactive une compétence Custodian individuelle, et les listes blanches de compétences d'agent peuvent réduire l'ensemble final. Voir [Configuration des compétences](/fr/tools/skills-config).

## Contrat de flux de travail

Chaque compétence Custodian fournie utilise les mêmes cinq sections dans cet ordre :

1. **Gather** lit la configuration actuelle expurgée et sonde l'état en direct.
2. **Mutate** utilise des écritures validées non interactives — `openclaw config set` / `openclaw config patch` à partir d'un shell de confiance, ou les actions d'outil Custodian en session où la politique le permet — jamais une édition directe de fichier.
3. **Repair** exécute `openclaw doctor` et sépare le diagnostic de toute réparation approuvée.
4. **Prove** exerce un résultat end-to-end en direct.
5. **Report** enregistre ce qui a changé, ce qui a été observé et ce qui reste.

Tous les playbooks à cinq sections gardent les valeurs secrètes hors des invites, des journaux et des fichiers. Les identifiants utilisent SecretRefs ou des magasins d'identifiants. Un flux de travail ne revendique jamais le succès sans son résultat Prove ; il signale le bloqueur exact quand la preuve en direct est indisponible.

## Première vague

| Compétence           | Résultat                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `configure-channel`  | Configurer et envoyer un message de test confirmé via une famille de canaux telle que Discord, Slack, Telegram ou WhatsApp.               |
| `add-model-provider` | Configurer l'accès au fournisseur API-key ou subscription/OAuth et exécuter une inférence Gateway en direct.                              |
| `diagnose-gateway`   | Effectuer un triage Gateway, config, SecretRef, channel-auth, log et port en lecture seule.                                               |
| `cloud-image-bake`   | Cuire une image Cloud Worker, la prouver avec une dispatch chronométrée et retirer en toute sécurité le snapshot remplacé.                |

## Catalogue de feuille de route

Le catalogue suivant documente les niveaux ultérieurs prévus. Ces noms sont des entrées de feuille de route, pas des compétences groupées ou des promesses de comportement actuel.

### Niveau 2 : opérations courantes

- `configure-search`: configurer et prouver en direct un fournisseur de recherche.
- `create-agent`: créer un agent, vérifier son espace de travail et prouver un tour.
- `manage-plugin`: installer, configurer, vérifier ou supprimer un plugin approuvé.
- `rotate-credential`: faire tourner une compétence supportée via son magasin propriétaire et prouver le consommateur.
- `upgrade-openclaw`: préparer une mise à niveau, exécuter des contrôles de santé et vérifier la disponibilité de restauration.

### Niveau 3 : opérations avancées

- `fleet-rollout`: déployer une configuration ou une version vérifiée sur les Gateways gérés.
- `incident-response`: collecter des preuves expurgées, contenir un incident et vérifier la récupération.
- `migrate-gateway`: déplacer une Gateway tout en préservant les contrats d'état et d'identité explicites.
- `release-validation`: exécuter le package de piste de version, installer et prouver le comportement en direct.
- `restore-backup`: restaurer dans une cible isolée, valider l'état et basculer délibérément.

## Ajouter une compétence d'opérateur

Placez les ajouts locaux dans l'espace de travail de l'agent Custodian configuré, pas dans le répertoire du package détenu par la version :

```text
<custodian-workspace>/skills/<skill-name>/SKILL.md
```

Les compétences d'espace de travail ont déjà une précédence plus élevée que le niveau groupé et sont limitées à l'espace de travail de cet agent. Suivez le même contrat Gather → Mutate → Repair → Prove → Report, gardez la description courte et démarrez une nouvelle session après avoir modifié la compétence. Voir [Créer des compétences](/fr/tools/creating-skills) pour le format complet.

## Connexes

- [Compétences](/fr/tools/skills)
- [Configuration des compétences](/fr/tools/skills-config)
- [Cloud Workers](/fr/gateway/cloud-workers)
- [Dépannage Gateway](/fr/gateway/troubleshooting)
