---
title: "Plugins Agent Harness"
sidebarTitle: "Agent Harness"
summary: "Surface SDK expérimentale pour les plugins qui remplacent l'exécuteur d'agent intégré de bas niveau"
read_when:
  - You are changing the embedded agent runtime or harness registry
  - You are registering an agent harness from a bundled or trusted plugin
  - You need to understand how the Codex plugin relates to model providers
---

# Plugins Agent Harness

Un **agent harness** est l'exécuteur de bas niveau pour un tour d'agent OpenClaw préparé. Ce n'est pas un fournisseur de modèle, pas un canal, et pas un registre d'outils.

Utilisez cette surface uniquement pour les plugins natifs groupés ou de confiance. Le contrat est toujours expérimental car les types de paramètres reflètent intentionnellement l'exécuteur intégré actuel.

## Quand utiliser un harness

Enregistrez un agent harness quand une famille de modèles a son propre runtime de session natif et que le transport du fournisseur OpenClaw normal est la mauvaise abstraction.

Exemples :

- un serveur d'agent de codage natif qui possède les threads et la compaction
- une CLI locale ou un daemon qui doit diffuser les événements de plan/raisonnement/outil natifs
- un runtime de modèle qui a besoin de son propre id de reprise en plus de la transcription de session OpenClaw

Ne pas enregistrer un harness juste pour ajouter une nouvelle API LLM. Pour les API de modèle HTTP ou WebSocket normales, créez un [plugin fournisseur](/fr/plugins/sdk-provider-plugins).

## Ce que le cœur possède toujours

Avant qu'un harness soit sélectionné, OpenClaw a déjà résolu :

- le fournisseur et le modèle
- l'état d'authentification du runtime
- le niveau de réflexion et le budget de contexte
- le fichier de transcription/session OpenClaw
- l'espace de travail, le sandbox et la politique d'outils
- les rappels de réponse de canal et les rappels de diffusion
- la politique de secours du modèle et de commutation de modèle en direct

Cette séparation est intentionnelle. Un harness exécute une tentative préparée ; il ne choisit pas les fournisseurs, ne remplace pas la livraison de canal, et ne bascule pas silencieusement les modèles.

## Enregistrer un harness

**Import :** `openclaw/plugin-sdk/agent-harness`

```typescript
import type { AgentHarness } from "openclaw/plugin-sdk/agent-harness";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const myHarness: AgentHarness = {
  id: "my-harness",
  label: "My native agent harness",

  supports(ctx) {
    return ctx.provider === "my-provider"
      ? { supported: true, priority: 100 }
      : { supported: false };
  },

  async runAttempt(params) {
    // Start or resume your native thread.
    // Use params.prompt, params.tools, params.images, params.onPartialReply,
    // params.onAgentEvent, and the other prepared attempt fields.
    return await runMyNativeTurn(params);
  },
};

export default definePluginEntry({
  id: "my-native-agent",
  name: "My Native Agent",
  description: "Runs selected models through a native agent daemon.",
  register(api) {
    api.registerAgentHarness(myHarness);
  },
});
```

## Politique de sélection

OpenClaw choisit un harness après la résolution du fournisseur/modèle :

1. `OPENCLAW_AGENT_RUNTIME=<id>` force un harness enregistré avec cet id.
2. `OPENCLAW_AGENT_RUNTIME=pi` force le harness PI intégré.
3. `OPENCLAW_AGENT_RUNTIME=auto` demande aux harnesses enregistrés s'ils supportent le fournisseur/modèle résolu.
4. Si aucun harness enregistré ne correspond, OpenClaw utilise PI sauf si le secours PI est désactivé.

Les échecs de harness plugin forcés apparaissent comme des échecs d'exécution. En mode `auto`, OpenClaw peut revenir à PI quand le harness plugin sélectionné échoue avant qu'un tour ait produit des effets secondaires. Définissez `OPENCLAW_AGENT_HARNESS_FALLBACK=none` ou `embeddedHarness.fallback: "none"` pour que ce secours soit un échec dur à la place.

Le plugin Codex groupé enregistre `codex` comme son id de harness. Le cœur traite cela comme un id de harness plugin ordinaire ; les alias spécifiques à Codex appartiennent au plugin ou à la configuration de l'opérateur, pas au sélecteur de runtime partagé.

## Appairage fournisseur plus harness

La plupart des harnesses doivent également enregistrer un fournisseur. Le fournisseur rend les références de modèle, l'état d'authentification, les métadonnées de modèle, et la sélection `/model` visibles au reste d'OpenClaw. Le harness réclame alors ce fournisseur dans `supports(...)`.

Le plugin Codex groupé suit ce modèle :

- id du fournisseur : `codex`
- références de modèle utilisateur : `codex/gpt-5.4`, `codex/gpt-5.2`, ou un autre modèle retourné par le serveur d'application Codex
- id du harness : `codex`
- authentification : disponibilité du fournisseur synthétique, car le harness Codex possède la connexion/session Codex native
- requête du serveur d'application : OpenClaw envoie l'id de modèle nu à Codex et laisse le harness parler au protocole du serveur d'application natif

Le plugin Codex est additif. Les références `openai/gpt-*` simples restent des références du fournisseur OpenAI et continuent à utiliser le chemin du fournisseur OpenClaw normal. Sélectionnez `codex/gpt-*` quand vous voulez l'authentification gérée par Codex, la découverte de modèle Codex, les threads natifs, et l'exécution du serveur d'application Codex. `/model` peut basculer parmi les modèles Codex retournés par le serveur d'application Codex sans nécessiter les identifiants du fournisseur OpenAI.

Pour la configuration de l'opérateur, les exemples de préfixe de modèle, et les configurations Codex uniquement, voir [Codex Harness](/fr/plugins/codex-harness).

OpenClaw nécessite le serveur d'application Codex `0.118.0` ou plus récent. Le plugin Codex vérifie la poignée de main d'initialisation du serveur d'application et bloque les serveurs plus anciens ou sans version afin qu'OpenClaw ne s'exécute que sur la surface de protocole avec laquelle il a été testé.

## Désactiver le secours PI

Par défaut, OpenClaw exécute les agents intégrés avec `agents.defaults.embeddedHarness` défini sur `{ runtime: "auto", fallback: "pi" }`. En mode `auto`, les harnesses plugin enregistrés peuvent réclamer une paire fournisseur/modèle. Si aucun ne correspond, ou si un harness plugin sélectionné automatiquement échoue avant de produire une sortie, OpenClaw revient à PI.

Définissez `fallback: "none"` quand vous avez besoin de prouver qu'un harness plugin est le seul runtime en cours d'exercice. Cela désactive le secours PI automatique ; cela ne bloque pas un `runtime: "pi"` ou `OPENCLAW_AGENT_RUNTIME=pi` explicite.

Pour les exécutions intégrées Codex uniquement :

```json
{
  "agents": {
    "defaults": {
      "model": "codex/gpt-5.4",
      "embeddedHarness": {
        "runtime": "codex",
        "fallback": "none"
      }
    }
  }
}
```

Si vous voulez que tout harness plugin enregistré réclame les modèles correspondants mais ne voulez jamais qu'OpenClaw revienne silencieusement à PI, gardez `runtime: "auto"` et désactivez le secours :

```json
{
  "agents": {
    "defaults": {
      "embeddedHarness": {
        "runtime": "auto",
        "fallback": "none"
      }
    }
  }
}
```

Les remplacements par agent utilisent la même forme :

```json
{
  "agents": {
    "defaults": {
      "embeddedHarness": {
        "runtime": "auto",
        "fallback": "pi"
      }
    },
    "list": [
      {
        "id": "codex-only",
        "model": "codex/gpt-5.4",
        "embeddedHarness": {
          "runtime": "codex",
          "fallback": "none"
        }
      }
    ]
  }
}
```

`OPENCLAW_AGENT_RUNTIME` remplace toujours le runtime configuré. Utilisez `OPENCLAW_AGENT_HARNESS_FALLBACK=none` pour désactiver le secours PI depuis l'environnement.

```bash
OPENCLAW_AGENT_RUNTIME=codex \
OPENCLAW_AGENT_HARNESS_FALLBACK=none \
openclaw gateway run
```

Avec le secours désactivé, une session échoue tôt quand le harness demandé n'est pas enregistré, ne supporte pas le fournisseur/modèle résolu, ou échoue avant de produire des effets secondaires de tour. C'est intentionnel pour les déploiements Codex uniquement et pour les tests en direct qui doivent prouver que le chemin du serveur d'application Codex est réellement en cours d'utilisation.

Ce paramètre contrôle uniquement le harness d'agent intégré. Il ne désactive pas l'image, la vidéo, la musique, TTS, PDF, ou l'acheminement de modèle spécifique à d'autres fournisseurs.

## Sessions natives et miroir de transcription

Un harness peut conserver un id de session natif, un id de thread, ou un jeton de reprise côté daemon. Gardez cette liaison explicitement associée à la session OpenClaw, et continuez à refléter la sortie d'assistant/outil visible par l'utilisateur dans la transcription OpenClaw.

La transcription OpenClaw reste la couche de compatibilité pour :

- l'historique de session visible du canal
- la recherche et l'indexation de transcription
- le basculement vers le harness PI intégré sur un tour ultérieur
- le comportement générique `/new`, `/reset`, et suppression de session

Si votre harness stocke une liaison sidecar, implémentez `reset(...)` afin qu'OpenClaw puisse la nettoyer quand la session OpenClaw propriétaire est réinitialisée.

## Résultats d'outils et de médias

Le cœur construit la liste d'outils OpenClaw et la transmet dans la tentative préparée. Quand un harness exécute un appel d'outil dynamique, retournez le résultat de l'outil via la forme de résultat du harness au lieu d'envoyer vous-même les médias du canal.

Cela garde les sorties de texte, image, vidéo, musique, TTS, approbation, et outil de messagerie sur le même chemin de livraison que les exécutions soutenues par PI.

## Limitations actuelles

- Le chemin d'importation public est générique, mais certains alias de type tentative/résultat portent toujours des noms `Pi` pour la compatibilité.
- L'installation de harness tiers est expérimentale. Préférez les plugins fournisseur jusqu'à ce que vous ayez besoin d'un runtime de session natif.
- Le basculement de harness est supporté entre les tours. Ne basculez pas les harnesses au milieu d'un tour après que les outils natifs, approbations, texte d'assistant, ou envois de message aient commencé.

## Connexes

- [SDK Overview](/fr/plugins/sdk-overview)
- [Runtime Helpers](/fr/plugins/sdk-runtime)
- [Provider Plugins](/fr/plugins/sdk-provider-plugins)
- [Codex Harness](/fr/plugins/codex-harness)
- [Model Providers](/fr/concepts/model-providers)
