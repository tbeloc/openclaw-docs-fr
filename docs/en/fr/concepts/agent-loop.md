---
summary: "Cycle de vie de la boucle d'agent, flux et sémantique d'attente"
read_when:
  - You need an exact walkthrough of the agent loop or lifecycle events
title: "Agent Loop"
---

# Agent Loop (OpenClaw)

Une boucle agentive est l'exécution complète « réelle » d'un agent : intake → assemblage du contexte → inférence du modèle →
exécution d'outils → réponses en flux → persistance. C'est le chemin faisant autorité qui transforme un message
en actions et une réponse finale, tout en maintenant la cohérence de l'état de session.

Dans OpenClaw, une boucle est une exécution unique et sérialisée par session qui émet des événements de cycle de vie et de flux
au fur et à mesure que le modèle réfléchit, appelle des outils et diffuse la sortie. Ce document explique comment cette boucle authentique est
câblée de bout en bout.

## Points d'entrée

- Gateway RPC : `agent` et `agent.wait`.
- CLI : commande `agent`.

## Fonctionnement (haut niveau)

1. `agent` RPC valide les paramètres, résout la session (sessionKey/sessionId), persiste les métadonnées de session, retourne `{ runId, acceptedAt }` immédiatement.
2. `agentCommand` exécute l'agent :
   - résout les valeurs par défaut du modèle + thinking/verbose
   - charge l'instantané des compétences
   - appelle `runEmbeddedPiAgent` (runtime pi-agent-core)
   - émet **lifecycle end/error** si la boucle intégrée n'en émet pas une
3. `runEmbeddedPiAgent` :
   - sérialise les exécutions via des files d'attente par session + globales
   - résout le modèle + le profil d'authentification et construit la session pi
   - s'abonne aux événements pi et diffuse les deltas assistant/outil
   - applique le timeout -> abandonne l'exécution si dépassé
   - retourne les charges utiles + métadonnées d'utilisation
4. `subscribeEmbeddedPiSession` relie les événements pi-agent-core au flux `agent` OpenClaw :
   - événements d'outils => `stream: "tool"`
   - deltas assistant => `stream: "assistant"`
   - événements de cycle de vie => `stream: "lifecycle"` (`phase: "start" | "end" | "error"`)
5. `agent.wait` utilise `waitForAgentJob` :
   - attend **lifecycle end/error** pour `runId`
   - retourne `{ status: ok|error|timeout, startedAt, endedAt, error? }`

## Mise en file d'attente + concurrence

- Les exécutions sont sérialisées par clé de session (voie de session) et optionnellement via une voie globale.
- Cela prévient les courses d'outils/session et maintient la cohérence de l'historique de session.
- Les canaux de messagerie peuvent choisir des modes de file d'attente (collect/steer/followup) qui alimentent ce système de voies.
  Voir [Command Queue](/concepts/queue).

## Préparation de session + workspace

- Le workspace est résolu et créé ; les exécutions en sandbox peuvent rediriger vers une racine de workspace en sandbox.
- Les compétences sont chargées (ou réutilisées à partir d'un instantané) et injectées dans l'env et le prompt.
- Les fichiers bootstrap/contexte sont résolus et injectés dans le rapport de prompt système.
- Un verrou d'écriture de session est acquis ; `SessionManager` est ouvert et préparé avant la diffusion.

## Assemblage du prompt + prompt système

- Le prompt système est construit à partir du prompt de base OpenClaw, du prompt de compétences, du contexte bootstrap et des remplacements par exécution.
- Les limites spécifiques au modèle et les tokens de réserve de compaction sont appliqués.
- Voir [System prompt](/concepts/system-prompt) pour ce que le modèle voit.

## Points d'accrochage (où vous pouvez intercepter)

OpenClaw dispose de deux systèmes de hooks :

- **Hooks internes** (Gateway hooks) : scripts pilotés par événements pour les commandes et les événements de cycle de vie.
- **Plugin hooks** : points d'extension à l'intérieur du cycle de vie agent/outil et du pipeline gateway.

### Hooks internes (Gateway hooks)

- **`agent:bootstrap`** : s'exécute lors de la construction des fichiers bootstrap avant que le prompt système soit finalisé.
  Utilisez ceci pour ajouter/supprimer des fichiers de contexte bootstrap.
- **Command hooks** : `/new`, `/reset`, `/stop` et autres événements de commande (voir doc Hooks).

Voir [Hooks](/automation/hooks) pour la configuration et les exemples.

### Plugin hooks (cycle de vie agent + gateway)

Ceux-ci s'exécutent à l'intérieur de la boucle d'agent ou du pipeline gateway :

- **`before_model_resolve`** : s'exécute pré-session (pas de `messages`) pour remplacer de manière déterministe le fournisseur/modèle avant la résolution du modèle.
- **`before_prompt_build`** : s'exécute après le chargement de la session (avec `messages`) pour injecter `prependContext`, `systemPrompt`, `prependSystemContext` ou `appendSystemContext` avant la soumission du prompt. Utilisez `prependContext` pour le texte dynamique par tour et les champs de contexte système pour les conseils stables qui doivent se situer dans l'espace du prompt système.
- **`before_agent_start`** : hook de compatibilité hérité qui peut s'exécuter dans l'une ou l'autre phase ; préférez les hooks explicites ci-dessus.
- **`agent_end`** : inspectez la liste de messages finale et les métadonnées d'exécution après la fin.
- **`before_compaction` / `after_compaction`** : observez ou annotez les cycles de compaction.
- **`before_tool_call` / `after_tool_call`** : interceptez les paramètres/résultats d'outils.
- **`tool_result_persist`** : transformez de manière synchrone les résultats d'outils avant qu'ils ne soient écrits dans la transcription de session.
- **`message_received` / `message_sending` / `message_sent`** : hooks de messages entrants + sortants.
- **`session_start` / `session_end`** : limites du cycle de vie de la session.
- **`gateway_start` / `gateway_stop`** : événements du cycle de vie du gateway.

Voir [Plugins](/tools/plugin#plugin-hooks) pour l'API de hook et les détails d'enregistrement.

## Diffusion + réponses partielles

- Les deltas assistant sont diffusés à partir de pi-agent-core et émis en tant qu'événements `assistant`.
- La diffusion de bloc peut émettre des réponses partielles soit sur `text_end` soit sur `message_end`.
- La diffusion de raisonnement peut être émise en tant que flux séparé ou en tant que réponses de bloc.
- Voir [Streaming](/concepts/streaming) pour le comportement de chunking et de réponse de bloc.

## Exécution d'outils + outils de messagerie

- Les événements de démarrage/mise à jour/fin d'outil sont émis sur le flux `tool`.
- Les résultats d'outils sont assainis pour la taille et les charges utiles d'image avant la journalisation/émission.
- L'envoi d'outils de messagerie est suivi pour supprimer les confirmations d'assistant en double.

## Mise en forme des réponses + suppression

- Les charges utiles finales sont assemblées à partir de :
  - texte assistant (et raisonnement optionnel)
  - résumés d'outils en ligne (quand verbose + autorisé)
  - texte d'erreur assistant quand le modèle erreur
- `NO_REPLY` est traité comme un token silencieux et filtré des charges utiles sortantes.
- Les doublons d'outils de messagerie sont supprimés de la liste de charges utiles finale.
- Si aucune charge utile rendable ne reste et qu'un outil a erreur, une réponse d'erreur d'outil de secours est émise
  (sauf si un outil de messagerie a déjà envoyé une réponse visible par l'utilisateur).

## Compaction + tentatives

- La compaction automatique émet des événements de flux `compaction` et peut déclencher une tentative.
- En cas de tentative, les tampons en mémoire et les résumés d'outils sont réinitialisés pour éviter la sortie en double.
- Voir [Compaction](/concepts/compaction) pour le pipeline de compaction.

## Flux d'événements (aujourd'hui)

- `lifecycle` : émis par `subscribeEmbeddedPiSession` (et en secours par `agentCommand`)
- `assistant` : deltas diffusés à partir de pi-agent-core
- `tool` : événements d'outils diffusés à partir de pi-agent-core

## Gestion des canaux de chat

- Les deltas assistant sont mis en mémoire tampon dans les messages de chat `delta`.
- Un chat `final` est émis sur **lifecycle end/error**.

## Timeouts

- `agent.wait` par défaut : 30s (juste l'attente). Le paramètre `timeoutMs` remplace.
- Runtime d'agent : `agents.defaults.timeoutSeconds` par défaut 600s ; appliqué dans le minuteur d'abandon `runEmbeddedPiAgent`.

## Où les choses peuvent se terminer tôt

- Timeout d'agent (abandon)
- AbortSignal (annulation)
- Déconnexion du gateway ou timeout RPC
- Timeout `agent.wait` (attente uniquement, n'arrête pas l'agent)
