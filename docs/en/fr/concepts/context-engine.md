---
summary: "Context engine: pluggable context assembly, compaction, and subagent lifecycle"
read_when:
  - You want to understand how OpenClaw assembles model context
  - You are switching between the legacy engine and a plugin engine
  - You are building a context engine plugin
title: "Context Engine"
---

# Context Engine

Un **context engine** contrôle la façon dont OpenClaw construit le contexte du modèle pour chaque exécution.
Il décide quels messages inclure, comment résumer l'historique plus ancien et comment
gérer le contexte à travers les limites des sous-agents.

OpenClaw est livré avec un moteur `legacy` intégré. Les plugins peuvent enregistrer
des moteurs alternatifs qui remplacent l'ensemble du pipeline de contexte.

## Démarrage rapide

Vérifiez quel moteur est actif :

```bash
openclaw doctor
# ou inspectez directement la configuration :
cat ~/.openclaw/openclaw.json | jq '.plugins.slots.contextEngine'
```

### Installation d'un plugin de context engine

Les plugins de context engine s'installent comme n'importe quel autre plugin OpenClaw. Installez
d'abord, puis sélectionnez le moteur dans le slot :

```bash
# Installer depuis npm
openclaw plugins install @martian-engineering/lossless-claw

# Ou installer depuis un chemin local (pour le développement)
openclaw plugins install -l ./my-context-engine
```

Ensuite, activez le plugin et sélectionnez-le comme moteur actif dans votre configuration :

```json5
// openclaw.json
{
  plugins: {
    slots: {
      contextEngine: "lossless-claw", // doit correspondre à l'id du moteur enregistré du plugin
    },
    entries: {
      "lossless-claw": {
        enabled: true,
        // La configuration spécifique au plugin va ici (voir la documentation du plugin)
      },
    },
  },
}
```

Redémarrez la passerelle après l'installation et la configuration.

Pour revenir au moteur intégré, définissez `contextEngine` sur `"legacy"` (ou
supprimez la clé entièrement — `"legacy"` est la valeur par défaut).

## Fonctionnement

Chaque fois qu'OpenClaw exécute une invite de modèle, le context engine participe à
quatre points du cycle de vie :

1. **Ingest** — appelé quand un nouveau message est ajouté à la session. Le moteur
   peut stocker ou indexer le message dans son propre magasin de données.
2. **Assemble** — appelé avant chaque exécution du modèle. Le moteur retourne un ensemble ordonné
   de messages (et une `systemPromptAddition` optionnelle) qui s'inscrivent dans
   le budget de tokens.
3. **Compact** — appelé quand la fenêtre de contexte est pleine, ou quand l'utilisateur exécute
   `/compact`. Le moteur résume l'historique plus ancien pour libérer de l'espace.
4. **After turn** — appelé après la fin d'une exécution. Le moteur peut persister l'état,
   déclencher une compaction en arrière-plan, ou mettre à jour les index.

### Cycle de vie des sous-agents (optionnel)

OpenClaw appelle actuellement un hook de cycle de vie de sous-agent :

- **onSubagentEnded** — nettoyer quand une session de sous-agent se termine ou est balayée.

Le hook `prepareSubagentSpawn` fait partie de l'interface pour une utilisation future, mais
le runtime ne l'invoque pas encore.

### Ajout de prompt système

La méthode `assemble` peut retourner une chaîne `systemPromptAddition`. OpenClaw
la prépend au prompt système pour l'exécution. Cela permet aux moteurs d'injecter
des conseils de rappel dynamiques, des instructions de récupération, ou des indices
conscients du contexte sans nécessiter de fichiers d'espace de travail statiques.

## Le moteur legacy

Le moteur `legacy` intégré préserve le comportement original d'OpenClaw :

- **Ingest** : no-op (le gestionnaire de session gère la persistance des messages directement).
- **Assemble** : pass-through (le pipeline existant sanitize → validate → limit
  dans le runtime gère l'assemblage du contexte).
- **Compact** : délègue à la compaction de résumé intégrée, qui crée
  un résumé unique des messages plus anciens et conserve les messages récents intacts.
- **After turn** : no-op.

Le moteur legacy n'enregistre pas d'outils et ne fournit pas de `systemPromptAddition`.

Quand aucun `plugins.slots.contextEngine` n'est défini (ou qu'il est défini sur `"legacy"`), ce
moteur est utilisé automatiquement.

## Moteurs de plugin

Un plugin peut enregistrer un context engine en utilisant l'API du plugin :

```ts
export default function register(api) {
  api.registerContextEngine("my-engine", () => ({
    info: {
      id: "my-engine",
      name: "My Context Engine",
      ownsCompaction: true,
    },

    async ingest({ sessionId, message, isHeartbeat }) {
      // Stocker le message dans votre magasin de données
      return { ingested: true };
    },

    async assemble({ sessionId, messages, tokenBudget }) {
      // Retourner les messages qui s'inscrivent dans le budget
      return {
        messages: buildContext(messages, tokenBudget),
        estimatedTokens: countTokens(messages),
        systemPromptAddition: "Use lcm_grep to search history...",
      };
    },

    async compact({ sessionId, force }) {
      // Résumer le contexte plus ancien
      return { ok: true, compacted: true };
    },
  }));
}
```

Ensuite, activez-le dans la configuration :

```json5
{
  plugins: {
    slots: {
      contextEngine: "my-engine",
    },
    entries: {
      "my-engine": {
        enabled: true,
      },
    },
  },
}
```

### L'interface ContextEngine

Membres requis :

| Membre             | Type     | Objectif                                                  |
| ------------------ | -------- | -------------------------------------------------------- |
| `info`             | Propriété | Id du moteur, nom, version, et s'il possède la compaction |
| `ingest(params)`   | Méthode   | Stocker un seul message                                   |
| `assemble(params)` | Méthode   | Construire le contexte pour une exécution du modèle (retourne `AssembleResult`) |
| `compact(params)`  | Méthode   | Résumer/réduire le contexte                                 |

`assemble` retourne un `AssembleResult` avec :

- `messages` — les messages ordonnés à envoyer au modèle.
- `estimatedTokens` (requis, `number`) — l'estimation du moteur du nombre total de
  tokens dans le contexte assemblé. OpenClaw l'utilise pour les décisions de seuil de compaction
  et les rapports de diagnostic.
- `systemPromptAddition` (optionnel, `string`) — prépendé au prompt système.

Membres optionnels :

| Membre                         | Type   | Objectif                                                                                                         |
| ------------------------------ | ------ | --------------------------------------------------------------------------------------------------------------- |
| `bootstrap(params)`            | Méthode | Initialiser l'état du moteur pour une session. Appelé une fois quand le moteur voit une session pour la première fois (par exemple, importer l'historique). |
| `ingestBatch(params)`          | Méthode | Ingérer un tour complété en tant que lot. Appelé après une exécution, avec tous les messages de ce tour à la fois.     |
| `afterTurn(params)`            | Méthode | Travail du cycle de vie post-exécution (persister l'état, déclencher la compaction en arrière-plan).                                         |
| `prepareSubagentSpawn(params)` | Méthode | Configurer l'état partagé pour une session enfant.                                                                        |
| `onSubagentEnded(params)`      | Méthode | Nettoyer après la fin d'un sous-agent.                                                                                 |
| `dispose()`                    | Méthode | Libérer les ressources. Appelé lors de l'arrêt de la passerelle ou du rechargement du plugin — pas par session.                           |

### ownsCompaction

Quand `info.ownsCompaction` est `true`, le moteur gère son propre cycle de vie de compaction.
OpenClaw ne déclenchera pas la compaction automatique intégrée ; à la place, il
délègue entièrement à la méthode `compact()` du moteur. Le moteur peut aussi
exécuter la compaction de manière proactive dans `afterTurn()`.

Quand c'est `false` ou non défini, la logique de compaction automatique intégrée d'OpenClaw s'exécute
aux côtés du moteur.

## Référence de configuration

```json5
{
  plugins: {
    slots: {
      // Sélectionner le context engine actif. Défaut : "legacy".
      // Définir sur un id de plugin pour utiliser un moteur de plugin.
      contextEngine: "legacy",
    },
  },
}
```

Le slot est exclusif au moment de l'exécution — un seul context engine enregistré est
résolu pour une exécution ou une opération de compaction donnée. D'autres plugins
`kind: "context-engine"` activés peuvent toujours charger et exécuter leur code d'enregistrement ;
`plugins.slots.contextEngine` sélectionne uniquement quel id de moteur enregistré
OpenClaw résout quand il a besoin d'un context engine.

## Relation avec la compaction et la mémoire

- **Compaction** est une responsabilité du context engine. Le moteur legacy
  délègue à la résumé intégrée d'OpenClaw. Les moteurs de plugin peuvent implémenter
  n'importe quelle stratégie de compaction (résumés DAG, récupération vectorielle, etc.).
- **Plugins de mémoire** (`plugins.slots.memory`) sont séparés des context engines.
  Les plugins de mémoire fournissent la recherche/récupération ; les context engines contrôlent ce que
  le modèle voit. Ils peuvent travailler ensemble — un context engine pourrait utiliser les données
  du plugin de mémoire lors de l'assemblage.
- **Élagage de session** (suppression des anciens résultats d'outils en mémoire) s'exécute toujours
  quel que soit le context engine actif.

## Conseils

- Utilisez `openclaw doctor` pour vérifier que votre moteur se charge correctement.
- Si vous changez de moteur, les sessions existantes continuent avec leur historique actuel.
  Le nouveau moteur prend le relais pour les exécutions futures.
- Les erreurs du moteur sont enregistrées et surfacées dans les diagnostics. Si un moteur de plugin
  échoue à s'enregistrer ou que l'id du moteur sélectionné ne peut pas être résolu, OpenClaw
  ne revient pas automatiquement ; les exécutions échouent jusqu'à ce que vous corrigiez le plugin ou
  basculiez `plugins.slots.contextEngine` vers `"legacy"`.
- Pour le développement, utilisez `openclaw plugins install -l ./my-engine` pour lier
  un répertoire de plugin local sans copier.

Voir aussi : [Compaction](/fr/concepts/compaction), [Context](/fr/concepts/context),
[Plugins](/fr/tools/plugin), [Plugin manifest](/fr/plugins/manifest).
