---
summary: "Agent runtime (embedded pi-mono), workspace contract, and session bootstrap"
read_when:
  - Changing agent runtime, workspace bootstrap, or session behavior
title: "Agent Runtime"
---

# Agent Runtime 🤖

OpenClaw exécute un seul agent runtime embarqué dérivé de **pi-mono**.

## Workspace (requis)

OpenClaw utilise un seul répertoire workspace d'agent (`agents.defaults.workspace`) comme **seul** répertoire de travail (`cwd`) de l'agent pour les outils et le contexte.

Recommandé : utilisez `openclaw setup` pour créer `~/.openclaw/openclaw.json` s'il manque et initialiser les fichiers du workspace.

Disposition complète du workspace + guide de sauvegarde : [Agent workspace](/concepts/agent-workspace)

Si `agents.defaults.sandbox` est activé, les sessions non-main peuvent le remplacer par
des workspaces par session sous `agents.defaults.sandbox.workspaceRoot` (voir
[Gateway configuration](/gateway/configuration)).

## Fichiers de bootstrap (injectés)

À l'intérieur de `agents.defaults.workspace`, OpenClaw s'attend à ces fichiers modifiables par l'utilisateur :

- `AGENTS.md` — instructions d'exploitation + « mémoire »
- `SOUL.md` — persona, limites, ton
- `TOOLS.md` — notes d'outils maintenues par l'utilisateur (par ex. `imsg`, `sag`, conventions)
- `BOOTSTRAP.md` — rituel unique au premier lancement (supprimé après achèvement)
- `IDENTITY.md` — nom/vibe/emoji de l'agent
- `USER.md` — profil utilisateur + adresse préférée

Au premier tour d'une nouvelle session, OpenClaw injecte le contenu de ces fichiers directement dans le contexte de l'agent.

Les fichiers vides sont ignorés. Les fichiers volumineux sont réduits et tronqués avec un marqueur pour que les prompts restent légers (lisez le fichier pour le contenu complet).

Si un fichier manque, OpenClaw injecte une seule ligne de marqueur « fichier manquant » (et `openclaw setup` créera un modèle par défaut sûr).

`BOOTSTRAP.md` n'est créé que pour un **workspace tout neuf** (aucun autre fichier de bootstrap présent). Si vous le supprimez après avoir complété le rituel, il ne devrait pas être recréé lors des redémarrages ultérieurs.

Pour désactiver entièrement la création de fichiers de bootstrap (pour les workspaces pré-ensemencés), définissez :

```json5
{ agent: { skipBootstrap: true } }
```

## Outils intégrés

Les outils principaux (read/exec/edit/write et outils système connexes) sont toujours disponibles,
sous réserve de la politique d'outils. `apply_patch` est optionnel et contrôlé par
`tools.exec.applyPatch`. `TOOLS.md` ne contrôle **pas** quels outils existent ; c'est
une orientation sur la façon dont _vous_ voulez les utiliser.

## Compétences

OpenClaw charge les compétences à partir de trois emplacements (le workspace gagne en cas de conflit de nom) :

- Groupées (livrées avec l'installation)
- Gérées/locales : `~/.openclaw/skills`
- Workspace : `<workspace>/skills`

Les compétences peuvent être contrôlées par config/env (voir `skills` dans [Gateway configuration](/gateway/configuration)).

## Intégration pi-mono

OpenClaw réutilise des parties de la base de code pi-mono (modèles/outils), mais **la gestion des sessions, la découverte et le câblage des outils sont la propriété d'OpenClaw**.

- Pas de runtime agent pi-coding.
- Aucun paramètre `~/.pi/agent` ou `<workspace>/.pi` n'est consulté.

## Sessions

Les transcriptions de session sont stockées en JSONL à :

- `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

L'ID de session est stable et choisi par OpenClaw.
Les dossiers de session Pi/Tau hérités ne sont **pas** lus.

## Direction pendant le streaming

Quand le mode de file d'attente est `steer`, les messages entrants sont injectés dans l'exécution actuelle.
La file d'attente est vérifiée **après chaque appel d'outil** ; si un message en file d'attente est présent,
les appels d'outils restants du message assistant actuel sont ignorés (résultats d'outils d'erreur avec « Ignoré en raison d'un message utilisateur en file d'attente. »), puis le message utilisateur en file d'attente
est injecté avant la prochaine réponse de l'assistant.

Quand le mode de file d'attente est `followup` ou `collect`, les messages entrants sont maintenus jusqu'à la
fin du tour actuel, puis un nouveau tour d'agent commence avec les charges utiles en file d'attente. Voir
[Queue](/concepts/queue) pour le comportement du mode + debounce/cap.

Le streaming de bloc envoie les blocs assistant terminés dès qu'ils se terminent ; il est
**désactivé par défaut** (`agents.defaults.blockStreamingDefault: "off"`).
Ajustez la limite via `agents.defaults.blockStreamingBreak` (`text_end` vs `message_end` ; par défaut text_end).
Contrôlez le chunking de bloc logiciel avec `agents.defaults.blockStreamingChunk` (par défaut
800–1200 caractères ; préfère les sauts de paragraphe, puis les sauts de ligne ; les phrases en dernier).
Fusionnez les chunks streamés avec `agents.defaults.blockStreamingCoalesce` pour réduire
le spam d'une seule ligne (fusion basée sur l'inactivité avant l'envoi). Les canaux non-Telegram nécessitent
un `*.blockStreaming: true` explicite pour activer les réponses de bloc.
Les résumés d'outils détaillés sont émis au démarrage de l'outil (pas de debounce) ; l'interface utilisateur de contrôle
streame la sortie d'outil via les événements d'agent quand disponible.
Plus de détails : [Streaming + chunking](/concepts/streaming).

## Références de modèle

Les références de modèle dans la config (par exemple `agents.defaults.model` et `agents.defaults.models`) sont analysées en divisant sur le **premier** `/`.

- Utilisez `provider/model` lors de la configuration des modèles.
- Si l'ID du modèle lui-même contient `/` (style OpenRouter), incluez le préfixe du fournisseur (exemple : `openrouter/moonshotai/kimi-k2`).
- Si vous omettez le fournisseur, OpenClaw traite l'entrée comme un alias ou un modèle pour le **fournisseur par défaut** (ne fonctionne que s'il n'y a pas de `/` dans l'ID du modèle).

## Configuration (minimale)

Au minimum, définissez :

- `agents.defaults.workspace`
- `channels.whatsapp.allowFrom` (fortement recommandé)

---

_Suivant : [Group Chats](/channels/group-messages)_ 🦞
