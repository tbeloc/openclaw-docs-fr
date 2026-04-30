---
summary: "Proposition de conception pour un SDK public OpenClaw pour les exécutions d'agents, les sessions, les tâches, les artefacts et les environnements gérés"
title: "Conception du SDK OpenClaw"
read_when:
  - You are designing or implementing a public OpenClaw app SDK
  - You are comparing OpenClaw agent APIs with Cursor, Claude Agent SDK, OpenAI Agents, Google ADK, OpenCode, Codex, or ACP
  - You need to decide whether a feature belongs in the public app SDK, plugin SDK, Gateway protocol, ACP backend, or managed environment layer
---

Cette page est une proposition de conception pour un futur **SDK public OpenClaw**. Elle est
distincte du [SDK plugin](/fr/plugins/sdk-overview) existant.

Le SDK plugin est destiné au code qui s'exécute à l'intérieur d'OpenClaw et étend les fournisseurs,
les canaux, les outils, les hooks et les runtimes de confiance. Le SDK app devrait être destiné aux
applications externes, scripts, tableaux de bord, tâches CI, extensions IDE et
systèmes d'automatisation qui souhaitent exécuter et observer les agents OpenClaw via une API
publique stable.

## Statut

Architecture en brouillon.

Ce document capture la direction de conception issue d'un examen comparatif de ces
surfaces de SDK d'agent et de runtime :

| Projet             | Leçon utile                                                                                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cursor SDK cookbook | Meilleure API produit de haut niveau : `Agent`, `Run`, runtimes locaux et cloud, streaming, annulation, découverte de modèles, dépôts, artefacts et flux de pull request cloud.    |
| Claude Agent SDK    | Client de session bidirectionnel fort, support d'interruption et de direction, modes de permission, hooks, outils personnalisés, magasins de session et transcriptions reprises.                        |
| OpenAI Agents SDK   | Concepts de flux de travail forts : transferts, garde-fous, approbations humaines, traçage, état d'exécution, objets de résultat en streaming et reprise après interruptions.                             |
| Google ADK          | Architecture interne forte : runner, service de session, service de mémoire, service d'artefact, service de credential, plugins, actions d'événement et confirmations d'outils longue durée.  |
| OpenCode            | Forme client/serveur forte : client API généré, REST plus SSE, sessions, espaces de travail, worktrees, permissions, questions, fichiers, VCS, PTY, outils, agents, compétences et MCP. |
| Codex               | Limite de runtime local forte : approbations, sandboxing, politique réseau, serveurs d'exécution locaux et distants, événements de protocole structurés et sessions app-server conscientes des threads.     |
| ACP et acpx        | Couche d'interopérabilité forte pour les harnais de codage externes avec sessions nommées, files d'attente de prompts, annulation coopérative et adaptateurs de runtime.                            |

La recommandation est de construire une façade publique simple de type Cursor au-dessus d'un
client Gateway généré de style OpenCode, tout en gardant les concepts de Claude, OpenAI Agents,
ADK, Codex et ACP comme références de conception interne où ils conviennent.

## Objectifs

- Donner aux développeurs d'applications une petite API de haut niveau pour exécuter les agents OpenClaw.
- Garder OpenClaw local-first comme runtime par défaut.
- Faire des environnements cloud ou gérés un fournisseur d'environnement additif, pas une
  API d'agent différente.
- Préserver les limites existantes d'OpenClaw : Gateway possède le protocole public, le SDK plugin possède les extensions en processus, ACP possède l'interopérabilité des harnais externes.
- Supporter `stream`, `wait`, `cancel`, `resume`, `fork`, les artefacts, les approbations et
  les tâches de fond comme opérations de première classe.
- Exposer les événements normalisés stables tout en préservant les événements bruts natifs du runtime pour
  les consommateurs avancés.
- Rendre explicites les permissions du SDK, le transfert de secrets, les approbations, le sandboxing et les
  environnements distants.
- Garder le contrat public assez petit pour être documenté, testé, versionné et
  généré.

## Non-objectifs

- Ne pas exposer `openclaw/plugin-sdk/*` comme le SDK app.
- Ne pas faire d'ACP le seul modèle de runtime.
- Ne pas exiger un service cloud avant que le SDK soit utile.
- Ne pas cloner exactement les APIs de Cursor, Claude, OpenAI, ADK, OpenCode, Codex ou ACP.
- Ne pas exposer les charges utiles d'événement `any` non bornées comme seul contrat public.
- Ne pas promettre l'isolation de sandbox ou réseau pour un harnais externe à moins que
  l'environnement sélectionné puisse réellement l'appliquer.
- Ne pas faire dépendre les auteurs de plugins des objets du SDK app à l'intérieur du code de runtime du plugin.

## Ajustement actuel d'OpenClaw

OpenClaw a déjà la plupart du substrat :

| Surface existante                                    | Ce qu'elle contribue                                                                                                        |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [Boucle d'agent](/fr/concepts/agent-loop)                  | Cycle de vie d'exécution `agent` et `agent.wait`, streaming, timeout et sérialisation de session.                                     |
| [Runtimes d'agent](/fr/concepts/agent-runtimes)          | Séparation des fournisseurs, modèles, runtimes et canaux.                                                                          |
| [Agents ACP](/fr/tools/acp-agents)                     | Sessions de harnais externes pour Claude Code, Cursor, Gemini CLI, OpenCode, ACP Codex explicite et outils similaires.            |
| [Tâches de fond](/fr/automation/tasks)                   | Registre d'activité détaché pour ACP, sous-agents, cron, opérations CLI et tâches de médias asynchrones.                                   |
| [Sous-agents](/fr/tools/subagents)                      | Exécutions d'agents de fond isolées, contexte forké optionnel, livraison aux sessions du demandeur.                              |
| [Plugins de harnais d'agent](/fr/plugins/sdk-agent-harness) | Enregistrement de runtime natif de confiance pour les harnais intégrés tels que Codex.                                                  |
| Schémas du protocole Gateway                            | Définitions de méthode et d'événement typées actuelles pour les paramètres d'agent, les sessions, les abonnements, les abandons, la compaction et les points de contrôle. |

L'écart n'est pas l'exécution d'agent. L'écart est une façade publique stable et conviviale sur
ces éléments.

## Modèle de base

Le SDK app devrait utiliser un petit ensemble de noms durables.

| Nom          | Signification                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `OpenClaw`    | Point d'entrée du client. Possède la découverte Gateway, l'authentification, l'accès client de bas niveau et les usines d'espace de noms.                        |
| `Agent`       | Acteur configuré. Porte l'id d'agent, le modèle par défaut, le runtime par défaut, la politique d'outils par défaut et les aides orientées app.           |
| `Session`     | Transcript durable, routage, espace de travail, contexte et liaison de runtime.                                                      |
| `Run`         | Un tour ou une tâche soumis. Diffuse les événements, attend le résultat, annule et expose les artefacts.                              |
| `Task`        | Entrée du registre d'activité détachée ou de fond. Couvre les sous-agents, les spawns ACP, les tâches cron, les exécutions CLI et les tâches asynchrones.           |
| `Artifact`    | Fichiers, patches, diffs, médias, logs, trajectoires, pull requests, captures d'écran et bundles générés.                       |
| `Environment` | Où l'exécution s'effectue : Gateway local, espace de travail local, hôte node, harnais ACP, runner géré ou futur espace de travail cloud. |
| `ToolSpace`   | La surface d'outils effective : outils OpenClaw, serveurs MCP, outils de canal, outils app, règles d'approbation et métadonnées d'outils.      |
| `Approval`    | Décision humaine ou politique demandée par une exécution, un outil, un environnement ou un harnais.                                |

Ces noms correspondent proprement aux concepts existants d'OpenClaw mais évitent de fuir
les noms spécifiques à l'implémentation tels que les internes du runner PI, l'enregistrement du harnais plugin ou
les détails de l'adaptateur ACP.

## Forme du produit

Le SDK de haut niveau devrait ressembler à ceci :

```typescript
import { OpenClaw } from "@openclaw/sdk";

const oc = new OpenClaw({ gateway: "auto" });
const agent = await oc.agents.get("main");

const run = await agent.run({
  input: "Review this pull request and suggest the smallest safe fix.",
  model: "openai/gpt-5.5",
});

for await (const event of run.events()) {
  if (event.type === "assistant.delta") {
    process.stdout.write(event.text);
  }
}

const result = await run.wait();
console.log(result.status);
```

La même application devrait pouvoir utiliser une session durable :

```typescript
const session = await oc.sessions.create({
  agentId: "main",
  label: "release-review",
});

const run = await session.send("Prepare release notes from the current diff.");
await run.wait();
```

Note d'implémentation actuelle : `@openclaw/sdk` commence par la surface soutenue par Gateway qui existe aujourd'hui. Les références de modèle qualifiées par fournisseur telles que
`openai/gpt-5.5` sont divisées en `provider` Gateway et les remplacements `model`.
Les sélections par exécution de `workspace`, `runtime`, `environment` et `approvals` sont
toujours des cibles de conception ; le client lève une exception quand les appelants les définissent pour que les demandes ne s'exécutent pas
silencieusement avec les valeurs par défaut. Les aides Task, artifact, environment et invocation d'outils génériques sont également
échafaudées comme forme d'API future et lèvent des erreurs explicites non supportées jusqu'à ce que les RPC Gateway existent pour eux.

Et la même API devrait pouvoir utiliser un harnais ACP externe :

```typescript
const run = await oc.runs.create({
  input: "Deep review this repository and return only high-risk findings.",
  workspace: { cwd: process.cwd() },
  runtime: { type: "acp", harness: "claude" },
  mode: "task",
});
```

Les environnements gérés ne devraient pas changer l'API de haut niveau :

```typescript
const run = await agent.run({
  input: "Run the full changed gate and summarize failures.",
  workspace: { repo: "openclaw/openclaw", ref: "main" },
  runtime: {
    type: "managed",
    provider: "testbox",
    timeoutMinutes: 90,
  },
});
```

## Sélection du runtime

Le SDK app devrait exposer la sélection du runtime comme une union normalisée :

```typescript
type RuntimeSelection =
  | "auto"
  | { type: "embedded"; id: "pi" | "codex" | string }
  | { type: "cli"; id: "claude-cli" | string }
  | { type: "acp"; harness: "claude" | "cursor" | "gemini" | "opencode" | string }
  | { type: "managed"; provider: "local" | "node" | "testbox" | "cloud" | string };
```

Règles :

- `auto` suit les règles de sélection de runtime d'OpenClaw.
- `embedded` cible les harnais en processus de confiance enregistrés via le SDK plugin,
  tels que `pi` ou `codex`.
- `cli` cible l'exécution du backend CLI détenu par OpenClaw où disponible.
- `acp` cible les harnais externes via ACP/acpx.
- `managed` cible un fournisseur d'environnement et peut toujours exécuter un runtime
  embedded, CLI ou ACP à l'intérieur de cet environnement.

L'objet de sélection du runtime devrait être descriptif. Ce ne devrait pas être l'endroit
où la gestion des secrets, la politique de sandbox ou le provisionnement de l'espace de travail se cachent.

## Modèle d'environnement

L'environnement est le substrat d'exécution. Il doit être explicite car les exécutions CLI locales, les harnais externes, les hôtes de nœuds et les espaces de travail cloud ont des propriétés de sécurité et de cycle de vie différentes.

```typescript
type EnvironmentSelection =
  | { type: "local"; cwd?: string }
  | { type: "gateway"; url?: string; cwd?: string }
  | { type: "node"; nodeId: string; cwd?: string }
  | { type: "managed"; provider: string; repo?: string; ref?: string }
  | { type: "ephemeral"; provider: string; repo?: string; ref?: string };
```

L'environnement possède :

- la préparation du checkout ou de l'espace de travail
- l'accès aux processus et fichiers
- l'application du sandbox et de la sécurité réseau
- les variables d'environnement et les références de secrets
- les journaux, traces et artefacts
- le nettoyage et la rétention
- la disponibilité du runtime

Cette séparation rend les agents gérés une extension naturelle du SDK. Un agent géré est une exécution normale dans un environnement géré, pas un fork de produit spécial.

Les contrats détaillés des espaces de noms, événements, résultats, approbations, artefacts, sécurité, packages et fournisseurs d'environnement se trouvent dans [Conception de l'API OpenClaw SDK](/fr/reference/openclaw-sdk-api-design).

## Plan du cookbook

Le SDK doit être livré avec un cookbook, pas seulement de la documentation de référence.

Exemples recommandés :

| Exemple                      | Montre                                                                                        |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| Démarrage rapide             | Créer un client, exécuter un agent, diffuser la sortie, attendre le résultat.                |
| Agent CLI de codage          | Espace de travail local, sélecteur de modèle, annulation, approbations, sortie JSON.         |
| Tableau de bord d'agent      | Sessions, exécutions, tâches en arrière-plan, artefacts, relecture d'événements, filtres de statut. |
| Générateur d'applications    | L'agent modifie un espace de travail tandis qu'un serveur d'aperçu s'exécute à côté.         |
| Examinateur de demande de tirage | Exécuter contre une référence de référentiel, collecter les commentaires de diff et les artefacts. |
| Console d'approbation        | S'abonner aux approbations et y répondre à partir d'une interface utilisateur.                |
| Exécuteur de harnais ACP     | Exécuter Claude Code, Cursor, Gemini CLI ou OpenCode via ACP en utilisant la même API `Run`. |
| Fournisseur d'environnement géré | Fournisseur minimal qui prépare un espace de travail, diffuse les événements, enregistre les artefacts et nettoie. |
| Pont Slack ou Discord        | L'application externe reçoit les événements et publie les résumés de progression sans devenir un plugin de canal. |
| Recherche multi-agents       | Générer des exécutions parallèles, collecter les artefacts et synthétiser un rapport final. |

Les exemples du cookbook doivent d'abord utiliser l'API de haut niveau. Les exemples de client généré de bas niveau appartiennent à une section avancée.

## Implémentation par phases

### Phase 0 : RFC et vocabulaire

- Convenir des noms et des noms publics.
- Décider des noms de packages.
- Définir la première taxonomie d'événements.
- Marquer le SDK de plugin actuel comme intentionnellement séparé dans la documentation.

### Phase 1 : Client généré de bas niveau

- Générer un client TypeScript à partir des schémas de protocole Gateway.
- Couvrir d'abord `agent`, `agent.wait`, sessions, abonnements, abandons et tâches.
- Ajouter des tests de fumée pour que les méthodes générées correspondent aux noms de méthodes Gateway et aux formes de schéma.
- Publier en tant que package expérimental ou interne.

### Phase 2 : API d'exécution de haut niveau

- Ajouter `OpenClaw`, `Agent`, `Session` et `Run`.
- Supporter `run.events()`, `run.wait()` et `run.cancel()`.
- Supporter la découverte locale de Gateway et les URL Gateway explicites.
- Supporter les sessions durables et l'envoi de session.

### Phase 3 : Projection d'événement normalisée

- Ajouter la projection d'événement normalisée côté Gateway à côté des événements bruts existants.
- Préserver les événements de runtime bruts où la politique le permet.
- Ajouter les curseurs de relecture et le comportement de reconnexion.
- Mapper les événements PI, Codex, ACP et tâche dans la taxonomie stable.

### Phase 4 : Artefacts et approbations

- Ajouter l'énumération et le téléchargement d'artefacts.
- Ajouter les assistants d'abonnement et de réponse d'approbation.
- Ajouter les assistants d'abonnement et de réponse aux questions.
- Ajouter la console d'approbation du cookbook.

### Phase 5 : Fournisseurs d'environnement

- Introduire les contrats des fournisseurs d'environnement local, nœud et géré.
- Commencer par un environnement qui existe déjà opérationnellement.
- Ajouter la préparation de l'espace de travail, les journaux, les artefacts, le délai d'expiration, le nettoyage et la rétention.

### Phase 6 : Flux de travail de style cloud

- Ajouter les exécutions orientées référentiel et branche.
- Ajouter les artefacts de demande de tirage.
- Ajouter les tableaux d'exécution groupés par référentiel, branche, statut et assignataire.
- Ajouter les sessions gérées longue durée et la politique de rétention.

## Choix de conception à copier

Copiez ces idées :

- De Cursor : `Agent` plus `Run`, symétrie locale et cloud, découverte de modèle, artefacts et intégration guidée par cookbook.
- Du SDK Claude Agent : clients bidirectionnels, interruption, permissions, hooks, outils personnalisés, magasins de sessions et sémantique de reprise.
- Des agents OpenAI : transferts, garde-fous, approbation humaine reprise, traçage et objets de résultat diffusés structurés.
- De Google ADK : services derrière le runner, actions d'événement, mémoire, artefacts, services de credentials et interception de plugins autour du cycle de vie d'exécution.
- D'OpenCode : client de protocole généré, REST plus SSE, sessions, espaces de travail, questions, permissions, fichiers, VCS, PTY, MCP, agents et compétences.
- De Codex : sandbox explicite, approbation, réseau, exécution locale et distante et limites de thread serveur d'application.
- D'ACP et acpx : interopérabilité de harnais externe basée sur adaptateur et files d'attente de prompt nommées.

## Choix de conception à éviter

Évitez ces pièges :

- Un SDK public qui est juste un vidage mince des internals de Gateway.
- Un SDK public qui importe les sous-chemins du SDK de plugin.
- Un SDK public où les événements ne sont que `stream` plus `data`.
- Une API cloud-first qui rend OpenClaw local comme un mode hérité.
- La sélection du runtime cachée dans les préfixes d'ID de modèle.
- Le transfert de secrets caché dans les cartes d'environnement.
- Les options spécifiques à ACP au niveau supérieur de chaque exécution.
- Les drapeaux de sandbox qui ne peuvent pas être appliqués par le runtime choisi.
- Un objet SDK qui essaie d'être plugin de fournisseur, plugin de canal, client d'application et runner géré à la fois.

## Questions ouvertes

- Le package initial doit-il vivre dans ce référentiel ou dans un référentiel SDK séparé ?
- Le client généré de bas niveau doit-il être publié publiquement avant que le wrapper de haut niveau se stabilise ?
- Quel est le premier mécanisme d'authentification d'application pris en charge : token local, token administrateur, flux d'appareil OAuth ou enregistrement d'application signé ?
- Combien d'historique de messages de session le SDK doit-il exposer par défaut ?
- Les environnements gérés doivent-ils être configurés uniquement dans la configuration de Gateway, ou les appelants du SDK peuvent-ils les demander directement avec des tokens limités ?
- Quelles règles de rétention s'appliquent aux artefacts générés par les exécutions locales ?
- Quelles charges utiles d'événement nécessitent une rédaction avant la livraison à l'application ?
- `Run` doit-il couvrir les tours de chat normaux et les tâches détachées, ou le travail en arrière-plan détaché doit-il toujours retourner un wrapper `Task` avec un `Run` imbriqué ?

## Documents connexes

- [Boucle d'agent](/fr/concepts/agent-loop)
- [Runtimes d'agent](/fr/concepts/agent-runtimes)
- [Session](/fr/concepts/session)
- [Sous-agents](/fr/tools/subagents)
- [Tâches en arrière-plan](/fr/automation/tasks)
- [Agents ACP](/fr/tools/acp-agents)
- [Plugins de harnais d'agent](/fr/plugins/sdk-agent-harness)
- [Aperçu du SDK de plugin](/fr/plugins/sdk-overview)
