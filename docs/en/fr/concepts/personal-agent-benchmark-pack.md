---
summary: "Scénarios de canal qa local pour les vérifications de flux de travail d'assistant personnel préservant la confidentialité."
read_when:
  - Exécution de vérifications de fiabilité d'agent personnel local
  - Extension du catalogue de scénarios QA sauvegardé par le référentiel
  - Vérification du comportement diagnostique des rappels, réponses, mémoire, rédaction, suivi sécurisé des outils, statut des tâches et partage sécurisé
title: "Pack de référence d'agent personnel"
---

Le Pack de Référence d'Agent Personnel est un petit pack de scénarios QA sauvegardé par le référentiel pour les flux de travail d'assistant personnel local. Ce n'est pas un benchmark de modèle générique et il ne nécessite pas un nouveau runner. Le pack réutilise la pile QA privée décrite dans [Aperçu QA](/fr/concepts/qa-e2e-automation), le [canal QA](/fr/channels/qa-channel) synthétique, et le catalogue markdown `qa/scenarios` existant.

Le premier pack est intentionnellement étroit :

- faux rappels personnels via livraison cron locale
- faux routage de DM et de réponses de fil via `qa-channel`
- faux rappel de préférences à partir des fichiers mémoire temporaires de l'espace de travail QA
- faux contrôles de secret sans écho
- suivi sécurisé des outils sauvegardés par lecture après un tour de style approbation court
- comportement d'arrêt de refus d'approbation pour une demande de lecture locale sensible
- rapport de statut de tâche sauvegardé par preuve qui maintient les états en attente, bloqué et terminé séparés
- artefacts diagnostiques sécurisés pour le partage qui conservent un statut utile tout en omettant le contenu personnel brut

## Scénarios

Les métadonnées du pack lisibles par machine se trouvent dans
`extensions/qa-lab/src/scenario-packs.ts`. Exécutez le pack avec
`--pack personal-agent` :

```bash
OPENCLAW_ENABLE_PRIVATE_QA_CLI=1 pnpm openclaw qa suite \
  --provider-mode mock-openai \
  --pack personal-agent \
  --concurrency 1
```

`--pack` est additif avec les drapeaux `--scenario` répétés. Les scénarios explicites s'exécutent en premier, puis les scénarios du pack s'exécutent dans l'ordre `QA_PERSONAL_AGENT_SCENARIO_IDS` avec les doublons supprimés.

Le pack est conçu pour `qa-channel` avec `mock-openai` ou une autre voie de fournisseur QA locale. Il ne doit pas être pointé vers des services de chat en direct ou des comptes personnels réels.

## Modèle de Confidentialité

Les scénarios utilisent uniquement des utilisateurs fictifs, des préférences fictives, des secrets fictifs et l'espace de travail de passerelle QA temporaire créé par la suite. Ils ne doivent pas lire ou écrire la mémoire utilisateur OpenClaw réelle, les sessions, les identifiants, les agents de lancement, les configurations globales ou l'état de passerelle en direct.

Les artefacts restent sous le répertoire d'artefacts de la suite QA existante et doivent être traités comme une sortie de test. Les vérifications de rédaction utilisent des marqueurs fictifs afin que les défaillances soient sûres à inspecter et à signaler dans les problèmes.

## Extension du Pack

Ajoutez de nouveaux cas sous `qa/scenarios/personal/`, puis ajoutez l'identifiant du scénario à
`QA_PERSONAL_AGENT_SCENARIO_IDS`. Gardez chaque cas petit, local, déterministe dans
`mock-openai`, et concentré sur un comportement d'assistant personnel.

Bons candidats de suivi :

- vérifications d'export de trajectoire rédactée
- vérifications de flux de travail de plugin local uniquement

Évitez d'ajouter un nouveau runner, plugin, dépendance, transport en direct ou juge de modèle
jusqu'à ce que le catalogue de scénarios ait suffisamment de cas stables pour justifier cette surface.
