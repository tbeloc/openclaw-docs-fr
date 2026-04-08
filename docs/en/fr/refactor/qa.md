# Refactorisation QA

Statut : migration fondationnelle déployée.

## Objectif

Migrer OpenClaw QA d'un modèle de définition fragmentée vers une source unique de vérité :

- métadonnées de scénario
- invites envoyées au modèle
- configuration et nettoyage
- logique du harnais
- assertions et critères de succès
- artefacts et indices de rapport

L'état final souhaité est un harnais QA générique qui charge des fichiers de définition de scénario puissants au lieu de coder en dur la plupart des comportements en TypeScript.

## État actuel

La source de vérité principale réside maintenant dans `qa/scenarios.md`.

Implémenté :

- `qa/scenarios.md`
  - pack QA canonique
  - identité de l'opérateur
  - mission de lancement
  - métadonnées de scénario
  - liaisons de gestionnaire
- `extensions/qa-lab/src/scenario-catalog.ts`
  - analyseur de pack markdown + validation zod
- `extensions/qa-lab/src/qa-agent-bootstrap.ts`
  - rendu du plan à partir du pack markdown
- `extensions/qa-lab/src/qa-agent-workspace.ts`
  - génère des fichiers de compatibilité plus `QA_SCENARIOS.md`
- `extensions/qa-lab/src/suite.ts`
  - sélectionne les scénarios exécutables via les liaisons de gestionnaire définies en markdown
- Protocole de bus QA + UI
  - pièces jointes génériques en ligne pour le rendu d'image/vidéo/audio/fichier

Surfaces de fractionnement restantes :

- `extensions/qa-lab/src/suite.ts`
  - possède toujours la plupart de la logique de gestionnaire personnalisé exécutable
- `extensions/qa-lab/src/report.ts`
  - dérive toujours la structure du rapport des sorties d'exécution

Le fractionnement de la source de vérité est donc corrigé, mais l'exécution est toujours principalement basée sur le gestionnaire plutôt que pleinement déclarative.

## À quoi ressemble la véritable surface de scénario

La lecture de la suite actuelle montre quelques classes de scénario distinctes.

### Interaction simple

- ligne de base du canal
- ligne de base DM
- suivi en fil de discussion
- changement de modèle
- suivi d'approbation
- réaction/édition/suppression

### Mutation de configuration et d'exécution

- désactivation de compétence de correctif de configuration
- redémarrage d'application de configuration wake-up
- basculement de capacité de redémarrage de configuration
- vérification de dérive d'inventaire d'exécution

### Assertions de système de fichiers et de référentiel

- rapport de découverte source/docs
- construire Lobster Invaders
- recherche d'artefact d'image générée

### Orchestration de la mémoire

- rappel de mémoire
- outils de mémoire dans le contexte du canal
- secours en cas d'échec de mémoire
- classement de la mémoire de session
- isolation de la mémoire de fil de discussion
- balayage de rêve de mémoire

### Intégration d'outils et de plugins

- appel d'outils de plugin MCP
- visibilité des compétences
- installation à chaud de compétences
- génération d'image native
- aller-retour d'image
- compréhension d'image à partir de pièce jointe

### Multi-tour et multi-acteur

- remise de sous-agent
- synthèse de fanout de sous-agent
- flux de style de récupération de redémarrage

Ces catégories sont importantes car elles pilotent les exigences du DSL. Une liste plate d'invite + texte attendu ne suffit pas.

## Direction

### Source unique de vérité

Utilisez `qa/scenarios.md` comme source de vérité créée.

Le pack doit rester :

- lisible par l'homme en révision
- analysable par machine
- assez riche pour piloter :
  - exécution de suite
  - amorçage de l'espace de travail QA
  - métadonnées de l'interface utilisateur QA Lab
  - invites de docs/découverte
  - génération de rapport

### Format de création préféré

Utilisez markdown comme format de niveau supérieur, avec YAML structuré à l'intérieur.

Forme recommandée :

- préambule YAML
  - id
  - titre
  - surface
  - balises
  - références docs
  - références de code
  - remplacements de modèle/fournisseur
  - conditions préalables
- sections en prose
  - objectif
  - notes
  - conseils de débogage
- blocs YAML clôturés
  - configuration
  - étapes
  - assertions
  - nettoyage

Cela donne :

- meilleure lisibilité PR que JSON géant
- contexte plus riche que YAML pur
- analyse stricte et validation zod

JSON brut n'est acceptable que comme forme intermédiaire générée.

## Forme de fichier de scénario proposée

Exemple :

````md
---
id: image-generation-roundtrip
title: Image generation roundtrip
surface: image
tags: [media, image, roundtrip]
models:
  primary: openai/gpt-5.4
requires:
  tools: [image_generate]
  plugins: [openai, qa-channel]
docsRefs:
  - docs/help/testing.md
  - docs/concepts/model-providers.md
codeRefs:
  - extensions/qa-lab/src/suite.ts
  - src/gateway/chat-attachments.ts
---

# Objective

Verify generated media is reattached on the follow-up turn.

# Setup

```yaml scenario.setup
- action: config.patch
  patch:
    agents:
      defaults:
        imageGenerationModel:
          primary: openai/gpt-image-1
- action: session.create
  key: agent:qa:image-roundtrip
```
````

# Steps

```yaml scenario.steps
- action: agent.send
  session: agent:qa:image-roundtrip
  message: |
    Image generation check: generate a QA lighthouse image and summarize it in one short sentence.
- action: artifact.capture
  kind: generated-image
  promptSnippet: Image generation check
  saveAs: lighthouseImage
- action: agent.send
  session: agent:qa:image-roundtrip
  message: |
    Roundtrip image inspection check: describe the generated lighthouse attachment in one short sentence.
  attachments:
    - fromArtifact: lighthouseImage
```

# Expect

```yaml scenario.expect
- assert: outbound.textIncludes
  value: lighthouse
- assert: requestLog.matches
  where:
    promptIncludes: Roundtrip image inspection check
  imageInputCountGte: 1
- assert: artifact.exists
  ref: lighthouseImage
```

````

## Capacités du runner que le DSL doit couvrir

En fonction de la suite actuelle, le runner générique a besoin de plus que l'exécution d'invite.

### Actions d'environnement et de configuration

- `bus.reset`
- `gateway.waitHealthy`
- `channel.waitReady`
- `session.create`
- `thread.create`
- `workspace.writeSkill`

### Actions de tour d'agent

- `agent.send`
- `agent.wait`
- `bus.injectInbound`
- `bus.injectOutbound`

### Actions de configuration et d'exécution

- `config.get`
- `config.patch`
- `config.apply`
- `gateway.restart`
- `tools.effective`
- `skills.status`

### Actions de fichier et d'artefact

- `file.write`
- `file.read`
- `file.delete`
- `file.touchTime`
- `artifact.captureGeneratedImage`
- `artifact.capturePath`

### Actions de mémoire et de cron

- `memory.indexForce`
- `memory.searchCli`
- `doctor.memory.status`
- `cron.list`
- `cron.run`
- `cron.waitCompletion`
- `sessionTranscript.write`

### Actions MCP

- `mcp.callTool`

### Assertions

- `outbound.textIncludes`
- `outbound.inThread`
- `outbound.notInRoot`
- `tool.called`
- `tool.notPresent`
- `skill.visible`
- `skill.disabled`
- `file.contains`
- `memory.contains`
- `requestLog.matches`
- `sessionStore.matches`
- `cron.managedPresent`
- `artifact.exists`

## Variables et références d'artefact

Le DSL doit supporter les sorties enregistrées et les références ultérieures.

Exemples de la suite actuelle :

- créer un fil de discussion, puis réutiliser `threadId`
- créer une session, puis réutiliser `sessionKey`
- générer une image, puis joindre le fichier au tour suivant
- générer une chaîne de marqueur de réveil, puis affirmer qu'elle apparaît plus tard

Capacités nécessaires :

- `saveAs`
- `${vars.name}`
- `${artifacts.name}`
- références typées pour les chemins, les clés de session, les identifiants de fil de discussion, les marqueurs, les sorties d'outils

Sans support de variable, le harnais continuera à fuir la logique de scénario dans TypeScript.

## Ce qui devrait rester comme échappatoires

Un runner pleinement pur déclaratif n'est pas réaliste en phase 1.

Certains scénarios sont intrinsèquement lourds en orchestration :

- balayage de rêve de mémoire
- redémarrage de wake-up d'application de configuration
- basculement de capacité de redémarrage de configuration
- résolution d'artefact d'image générée par horodatage/chemin
- évaluation du rapport de découverte

Ceux-ci doivent utiliser des gestionnaires personnalisés explicites pour l'instant.

Règle recommandée :

- 85-90% déclaratif
- étapes `customHandler` explicites pour le reste difficile
- gestionnaires personnalisés nommés et documentés uniquement
- pas de code en ligne anonyme dans le fichier de scénario

Cela garde le moteur générique propre tout en permettant les progrès.

## Changement d'architecture

### Actuel

Le markdown de scénario est déjà la source de vérité pour :

- exécution de suite
- fichiers d'amorçage de l'espace de travail
- catalogue de scénarios de l'interface utilisateur QA Lab
- métadonnées de rapport
- invites de découverte

Compatibilité générée :

- l'espace de travail amorcé inclut toujours `QA_KICKOFF_TASK.md`
- l'espace de travail amorcé inclut toujours `QA_SCENARIO_PLAN.md`
- l'espace de travail amorcé inclut maintenant aussi `QA_SCENARIOS.md`

## Plan de refactorisation

### Phase 1 : chargeur et schéma

Fait.

- ajouté `qa/scenarios.md`
- ajouté analyseur pour le contenu YAML markdown nommé pack
- validé avec zod
- consommateurs commutés vers le pack analysé
- supprimé `qa/seed-scenarios.json` et `qa/QA_KICKOFF_TASK.md` au niveau du référentiel

### Phase 2 : moteur générique

- diviser `extensions/qa-lab/src/suite.ts` en :
  - chargeur
  - moteur
  - registre d'action
  - registre d'assertion
  - gestionnaires personnalisés
- garder les fonctions d'aide existantes comme opérations du moteur

Livrable :

- le moteur exécute des scénarios déclaratifs simples

Commencez par les scénarios qui sont principalement invite + attendre + affirmer :

- suivi en fil de discussion
- compréhension d'image à partir de pièce jointe
- visibilité et invocation des compétences
- ligne de base du canal

Livrable :

- premiers vrais scénarios définis en markdown expédiés via le moteur générique

### Phase 4 : migrer les scénarios moyens

- aller-retour de génération d'image
- outils de mémoire dans le contexte du canal
- classement de la mémoire de session
- remise de sous-agent
- synthèse de fanout de sous-agent

Livrable :

- variables, artefacts, assertions d'outils, assertions de journal de requête prouvées

### Phase 5 : garder les scénarios difficiles sur les gestionnaires personnalisés

- balayage de rêve de mémoire
- redémarrage de wake-up d'application de configuration
- basculement de capacité de redémarrage de configuration
- dérive d'inventaire d'exécution

Livrable :

- même format de création, mais avec des blocs d'étape personnalisée explicites où nécessaire

### Phase 6 : supprimer la carte de scénario codée en dur

Une fois la couverture du pack suffisamment bonne :

- supprimer la plupart des branches spécifiques au scénario TypeScript de `extensions/qa-lab/src/suite.ts`

## Support Slack faux / média riche

Le bus QA actuel est d'abord du texte.

Fichiers pertinents :

- `extensions/qa-channel/src/protocol.ts`
- `extensions/qa-lab/src/bus-state.ts`
- `extensions/qa-lab/src/bus-queries.ts`
- `extensions/qa-lab/src/bus-server.ts`
- `extensions/qa-lab/web/src/ui-render.ts`

Aujourd'hui, le bus QA supporte :

- texte
- réactions
- fils de discussion

Il ne modélise pas encore les pièces jointes multimédias en ligne.

### Contrat de transport nécessaire

Ajouter un modèle de pièce jointe de bus QA générique :

```ts
type QaBusAttachment = {
  id: string;
  kind: "image" | "video" | "audio" | "file";
  mimeType: string;
  fileName?: string;
  inline?: boolean;
  url?: string;
  contentBase64?: string;
  width?: number;
  height?: number;
  durationMs?: number;
  altText?: string;
  transcript?: string;
};
````

Puis ajouter `attachments?: QaBusAttachment[]` à :

- `QaBusMessage`
- `QaBusInboundMessageInput`
- `QaBusOutboundMessageInput`

### Pourquoi générique d'abord

Ne construisez pas un modèle multimédia réservé à Slack.

Au lieu de cela :

- un modèle de transport QA générique
- plusieurs rendus au-dessus
  - chat QA Lab actuel
  - futur faux web Slack
  - toute autre vue de transport faux

Cela évite la logique dupliquée et permet aux scénarios multimédias de rester agnostiques au transport.

### Travail d'interface utilisateur nécessaire

Mettez à jour l'interface utilisateur QA pour afficher :

- aperçu d'image en ligne
- lecteur audio en ligne
- lecteur vidéo en ligne
- puce de pièce jointe de fichier

L'interface utilisateur actuelle peut déjà afficher les fils de discussion et les réactions, donc le rendu des pièces jointes doit se superposer au même modèle de carte de message.

### Travail de scénario activé par le transport multimédia

Une fois que les pièces jointes circulent via le bus QA, nous pouvons ajouter des scénarios de faux chat plus riches :

- réponse d'image en ligne dans le faux Slack
- compréhension de pièce jointe audio
- compréhension de pièce jointe vidéo
- classement de pièce jointe mixte
- réponse de fil de discussion avec média conservé

## Recommandation

Le prochain bloc d'implémentation devrait être :

1. ajouter chargeur de scénario markdown + schéma zod
2. générer le catalogue actuel à partir de markdown
3. migrer d'abord quelques scénarios simples
4. ajouter le support de pièce jointe de bus QA générique
5. afficher l'image en ligne dans l'interface utilisateur QA
6. puis développer vers l'audio et la vidéo

C'est le plus petit chemin qui prouve les deux objectifs :

- QA générique défini en markdown
- surfaces de messagerie fausses plus riches

## Questions ouvertes

- si les fichiers de scénario doivent autoriser les modèles d'invite markdown intégrés avec interpolation de variable
- si la configuration/nettoyage doit être des sections nommées ou simplement des listes d'action ordonnées
- si les références d'artefact doivent être fortement typées dans le schéma ou basées sur des chaînes
- si les gestionnaires personnalisés doivent vivre dans un registre ou des registres par surface
- si le fichier de compatibilité JSON généré doit rester archivé pendant la migration
