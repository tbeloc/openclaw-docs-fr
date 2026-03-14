---
read_when:
  - Vous avez besoin d'explications détaillées sur la boucle ou les événements du cycle de vie de l'agent
summary: Cycle de vie de la boucle d'agent, flux et sémantique d'attente
title: Boucle d'agent
x-i18n:
  generated_at: "2026-02-03T10:05:11Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0775b96eb3451e137297661a1095eaefb2bafeebb5f78123174a46290e18b014
  source_path: concepts/agent-loop.md
  workflow: 15
---

# Boucle d'agent (OpenClaw)

La boucle d'agent est une exécution complète et « réelle » de l'agent : réception → assemblage du contexte → inférence du modèle → exécution d'outils → réponse en flux → persistance. C'est le chemin faisant autorité pour transformer les messages en actions et réponses finales, tout en maintenant la cohérence de l'état de la session.

Dans OpenClaw, la boucle est une exécution sérialisée unique par session qui émet des événements de cycle de vie et de flux pendant que le modèle réfléchit, appelle des outils et diffuse la sortie. Cette documentation explique comment cette boucle réelle est connectée de bout en bout.

## Points d'entrée

- RPC Gateway : `agent` et `agent.wait`.
- CLI : commande `agent`.

## Fonctionnement (haut niveau)

1. L'RPC `agent` valide les paramètres, analyse la session (sessionKey/sessionId), persiste les métadonnées de session et retourne immédiatement `{ runId, acceptedAt }`.
2. `agentCommand` exécute l'agent :
   - Analyse les valeurs par défaut du modèle + mode réflexion/détaillé
   - Charge l'instantané Skills
   - Appelle `runEmbeddedPiAgent` (runtime pi-agent-core)
   - Émet un événement **fin de cycle de vie/erreur** si la boucle intégrée ne l'a pas fait
3. `runEmbeddedPiAgent` :
   - Sérialise les exécutions par session + file d'attente globale
   - Analyse le modèle + profil d'authentification et construit une session pi
   - S'abonne aux événements pi et diffuse les deltas assistant/outil
   - Applique le délai d'expiration -> abandonne l'exécution en cas de dépassement
   - Retourne la charge utile + métadonnées d'utilisation
4. `subscribeEmbeddedPiSession` relie les événements pi-agent-core au flux OpenClaw `agent` :
   - Événements d'outils => `stream: "tool"`
   - Deltas assistant => `stream: "assistant"`
   - Événements de cycle de vie => `stream: "lifecycle"` (`phase: "start" | "end" | "error"`)
5. `agent.wait` utilise `waitForAgentJob` :
   - Attend la **fin de cycle de vie/erreur** pour `runId`
   - Retourne `{ status: ok|error|timeout, startedAt, endedAt, error? }`

## File d'attente + Concurrence

- Les exécutions sont sérialisées par clé de session (canal de session), optionnellement via un canal global.
- Cela empêche les courses d'outils/session et maintient la cohérence de l'historique de session.
- Les canaux de messages peuvent optionnellement mettre en file d'attente le mode (collect/steer/followup) pour alimenter ce système de canaux. Voir [File d'attente de commandes](/concepts/queue).

## Préparation de session + Espace de travail

- Analyse et crée l'espace de travail ; les exécutions isolées en sandbox peuvent être redirigées vers la racine de l'espace de travail sandbox.
- Charge les Skills (ou réutilise à partir d'un instantané) et les injecte dans l'environnement et le prompt.
- Analyse les fichiers de bootstrap/contexte et les injecte dans le rapport de prompt système.
- Acquiert le verrou d'écriture de session ; ouvre et prépare `SessionManager` avant la diffusion.

## Assemblage de prompt + Prompt système

- Le prompt système est construit à partir du prompt de base d'OpenClaw, du prompt Skills, du contexte de bootstrap et des remplacements par exécution.
- Applique les limites spécifiques au modèle et la compression des jetons de réserve.
- Voir [Prompt système](/concepts/system-prompt) pour ce que le modèle voit.

## Points d'accroche (où intercepter)

OpenClaw dispose de deux systèmes d'accroche :

- **Accroche interne** (Accroche Gateway) : scripts pilotés par événements pour les commandes et événements de cycle de vie.
- **Accroche de plugin** : points d'extension dans le cycle de vie agent/outil et le pipeline Gateway.

### Accroche interne (Accroche Gateway)

- **`agent:bootstrap`** : s'exécute lors de la construction du fichier de bootstrap avant la finalisation du prompt système. Utilisé pour ajouter/supprimer des fichiers de contexte de bootstrap.
- **Accroche de commande** : `/new`, `/reset`, `/stop` et autres événements de commande (voir documentation des accroche).

Voir [Accroche](/automation/hooks) pour la configuration et les exemples.

### Accroche de plugin (Cycle de vie agent + Gateway)

Celles-ci s'exécutent dans la boucle d'agent ou le pipeline Gateway :

- **`before_agent_start`** : injecte le contexte ou remplace le prompt système avant le démarrage de l'exécution.
- **`agent_end`** : inspecte la liste des messages finaux et les métadonnées d'exécution après la fin.
- **`before_compaction` / `after_compaction`** : observe ou annote les cycles de compression.
- **`before_tool_call` / `after_tool_call`** : intercepte les paramètres/résultats d'outils.
- **`tool_result_persist`** : transforme les résultats d'outils de manière synchrone avant qu'ils ne soient écrits dans le journal de session.
- **`message_received` / `message_sending` / `message_sent`** : accroche de messages entrants + sortants.
- **`session_start` / `session_end`** : limites du cycle de vie de session.
- **`gateway_start` / `gateway_stop`** : événements du cycle de vie Gateway.

Voir [Plugin](/tools/plugin#plugin-hooks) pour l'API d'accroche et les détails d'enregistrement.

## Diffusion + Réponses partielles

- Les deltas assistant sont diffusés à partir de pi-agent-core et émis comme événements `assistant`.
- La diffusion en chunks peut émettre des réponses partielles à `text_end` ou `message_end`.
- La diffusion de raisonnement peut être émise comme un flux séparé ou comme une réponse en chunks.
- Voir [Diffusion](/concepts/streaming) pour le comportement des chunks et des réponses en chunks.

## Exécution d'outils + Outils de message

- Les événements de début/mise à jour/fin d'outil sont émis sur le flux `tool`.
- Les résultats d'outils sont nettoyés pour la taille et les charges utiles d'image avant enregistrement/émission.
- Les envois d'outils de message sont suivis pour supprimer les confirmations d'assistant en double.

## Mise en forme de réponse + Suppression

- La charge utile finale est assemblée à partir de :
  - Texte assistant (et raisonnement optionnel)
  - Résumé d'outil en ligne (quand mode détaillé + autorisé)
  - Texte d'erreur assistant en cas d'erreur du modèle
- `NO_REPLY` est traité comme un jeton silencieux, filtré de la charge utile sortante.
- Les doublons d'outils de message sont supprimés de la liste de charge utile finale.
- Si aucune charge utile rendable ne reste et que l'outil a échoué, émet une réponse d'erreur d'outil de secours (sauf si un outil de message a déjà envoyé une réponse visible par l'utilisateur).

## Compression + Nouvelle tentative

- La compression automatique émet un événement de flux `compaction`, qui peut déclencher une nouvelle tentative.
- Lors d'une nouvelle tentative, le tampon mémoire et les résumés d'outils sont réinitialisés pour éviter la sortie en double.
- Voir [Compression](/concepts/compaction) pour le pipeline de compression.

## Flux d'événements (actuel)

- `lifecycle` : émis par `subscribeEmbeddedPiSession` (et comme secours de `agentCommand`)
- `assistant` : deltas diffusés à partir de pi-agent-core
- `tool` : événements d'outils diffusés à partir de pi-agent-core

## Traitement des canaux de chat

- Les deltas assistant sont mis en tampon dans les messages de chat `delta`.
- Émet le chat `final` à la **fin de cycle de vie/erreur**.

## Délai d'expiration

- `agent.wait` par défaut : 30 secondes (attente uniquement). Le paramètre `timeoutMs` peut remplacer.
- Temps d'exécution de l'agent : `agents.defaults.timeoutSeconds` par défaut 600 secondes ; appliqué dans le minuteur d'abandon de `runEmbeddedPiAgent`.

## Cas de fin anticipée possible

- Délai d'expiration de l'agent (abandon)
- AbortSignal (annulation)
- Déconnexion Gateway ou délai d'expiration RPC
- Délai d'expiration `agent.wait` (attente uniquement, n'arrête pas l'agent)
