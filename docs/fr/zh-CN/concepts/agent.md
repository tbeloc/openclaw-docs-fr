---
read_when:
  - Lors de la modification du runtime de l'agent, de la guidance de l'espace de travail ou du comportement de session
summary: Runtime de l'agent (pi-mono embarqué), contrat d'espace de travail et guidance de session
title: Runtime de l'agent
x-i18n:
  generated_at: "2026-02-03T10:04:53Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 04b4e0bc6345d2afd9a93186e5d7a02a393ec97da2244e531703cb6a1c182325
  source_path: concepts/agent.md
  workflow: 15
---

# Runtime de l'agent 🤖

OpenClaw exécute un runtime d'agent embarqué dérivé de **pi-mono**.

## Espace de travail (obligatoire)

OpenClaw utilise un répertoire d'espace de travail d'agent unique (`agents.defaults.workspace`) comme répertoire de travail **unique** (`cwd`) de l'agent pour les outils et le contexte.

Recommandation : utilisez `openclaw setup` pour créer `~/.openclaw/openclaw.json` en cas d'absence et initialiser les fichiers d'espace de travail.

Disposition complète de l'espace de travail + guide de sauvegarde : [Espace de travail de l'agent](/concepts/agent-workspace)

Si `agents.defaults.sandbox` est activé, les sessions non principales peuvent remplacer ce paramètre en utilisant des espaces de travail isolés par session sous `agents.defaults.sandbox.workspaceRoot` (voir [Configuration de la passerelle](/gateway/configuration)).

## Fichiers de guidance (injection)

Dans `agents.defaults.workspace`, OpenClaw s'attend aux fichiers suivants modifiables par l'utilisateur :

- `AGENTS.md` — Instructions opérationnelles + « mémoire »
- `SOUL.md` — Personnalité, limites, ton
- `TOOLS.md` — Descriptions d'outils maintenues par l'utilisateur (par ex. `imsg`, `sag`, conventions)
- `BOOTSTRAP.md` — Rituel unique de première exécution (à supprimer après achèvement)
- `IDENTITY.md` — Nom/style/expressions de l'agent
- `USER.md` — Profil utilisateur + préférences d'appellation

Au premier tour d'une nouvelle session, OpenClaw injecte directement le contenu de ces fichiers dans le contexte de l'agent.

Les fichiers vides sont ignorés. Les fichiers volumineux sont élagués et tronqués avec des marqueurs pour maintenir le prompt concis (lisez le fichier pour le contenu complet).

Si un fichier est manquant, OpenClaw injecte un marqueur « fichier manquant » d'une ligne (`openclaw setup` créera des modèles par défaut sécurisés).

`BOOTSTRAP.md` n'est créé que pour un **espace de travail tout neuf** (aucun autre fichier de guidance n'existe). Si vous le supprimez après avoir complété le rituel, les redémarrages ultérieurs ne devraient pas le recréer.

Pour désactiver complètement la création de fichiers de guidance (pour les espaces de travail préconfigurés), définissez :

```json5
{ agent: { skipBootstrap: true } }
```

## Outils intégrés

Les outils principaux (read/exec/edit/write et outils système connexes) sont toujours disponibles, soumis à la politique d'outils. `apply_patch` est optionnel, contrôlé par `tools.exec.applyPatch`. `TOOLS.md` ne contrôle **pas** quels outils existent ; il s'agit de conseils sur la *façon dont* vous souhaitez les utiliser.

## Skills

OpenClaw charge les Skills à partir de trois emplacements (l'espace de travail a priorité en cas de conflit de noms) :

- Intégrés (fournis avec l'installation)
- Hébergés/locaux : `~/.openclaw/skills`
- Espace de travail : `<workspace>/skills`

Les Skills peuvent être contrôlés via la configuration/variables d'environnement (voir `skills` dans [Configuration de la passerelle](/gateway/configuration)).

## Intégration pi-mono

OpenClaw réutilise des portions de la base de code pi-mono (modèles/outils), mais **la gestion des sessions, la découverte d'appareils et la connexion d'outils sont gérées par OpenClaw**.

- Pas de runtime d'agent pi-coding.
- Ne lit pas les paramètres `~/.pi/agent` ou `<workspace>/.pi`.

## Sessions

Les enregistrements de session sont stockés au format JSONL dans :

- `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

L'ID de session est stable, choisi par OpenClaw.
Ne lit **pas** les anciens dossiers de sessions Pi/Tau.

## Guidance en streaming

Lorsque le mode de file d'attente est `steer`, les messages entrants sont injectés dans l'exécution actuelle.
La file d'attente est vérifiée **après chaque appel d'outil** ; s'il existe des messages en attente, les appels d'outils restants du message d'assistant actuel sont ignorés (les résultats d'outils affichent l'erreur « Skipped due to queued user message. »), puis le message utilisateur en attente est injecté avant la réponse d'assistant suivante.

Lorsque le mode de file d'attente est `followup` ou `collect`, les messages entrants sont conservés jusqu'à la fin du tour actuel, puis un nouveau tour d'agent commence avec la charge en attente. Voir [File d'attente](/concepts/queue) pour les modes + comportement de débounce/limite.

Le streaming par bloc est envoyé immédiatement après la fin d'un bloc d'assistant ; par défaut **désactivé** (`agents.defaults.blockStreamingDefault: "off"`).
Ajustez les limites via `agents.defaults.blockStreamingBreak` (`text_end` vs `message_end` ; par défaut text_end).
Utilisez `agents.defaults.blockStreamingChunk` pour contrôler le chunking de bloc logiciel (par défaut 800–1200 caractères ; priorité aux séparateurs de paragraphes, puis sauts de ligne ; enfin phrases).
Utilisez `agents.defaults.blockStreamingCoalesce` pour fusionner les blocs en streaming afin de réduire le spam d'une seule ligne (fusion basée sur l'inactivité avant envoi). Les canaux non-Telegram nécessitent un paramètre explicite `*.blockStreaming: true` pour activer les réponses par bloc.
Un résumé d'outil détaillé est émis au lancement de l'outil (sans débounce) ; l'interface de contrôle diffuse la sortie d'outil via le flux d'événements d'agent lorsqu'elle est disponible.
Plus de détails : [Streaming + Chunking](/concepts/streaming).

## Référence de modèle

Les références de modèle dans la configuration (par ex. `agents.defaults.model` et `agents.defaults.models`) sont résolues en divisant au **premier** `/`.

- Utilisez `provider/model` lors de la configuration d'un modèle.
- Si l'ID de modèle lui-même contient `/` (style OpenRouter), incluez le préfixe du fournisseur (par ex. : `openrouter/moonshotai/kimi-k2`).
- Si le fournisseur est omis, OpenClaw traite l'entrée comme un alias ou un modèle du **fournisseur par défaut** (valide uniquement si l'ID de modèle ne contient pas `/`).

## Configuration (minimale)

Au minimum, vous devez définir :

- `agents.defaults.workspace`
- `channels.whatsapp.allowFrom` (fortement recommandé)

---

_Suivant : [Messages de groupe](/channels/group-messages)_ 🦞
