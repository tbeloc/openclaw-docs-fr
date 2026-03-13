---
read_when:
  - Vous voulez un repli fiable lorsqu'un fournisseur d'API échoue
  - Vous exécutez Claude Code CLI ou un autre CLI d'IA local et souhaitez les réutiliser
  - Vous avez besoin d'un chemin pur texte sans outils, mais avec support des conversations et des images
summary: Backend CLI : repli en texte pur via CLI d'IA local
title: Backend CLI
x-i18n:
  generated_at: "2026-02-03T07:47:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 56a96e83b16a4f6443cbf4a9da7a660c41a5b178af5e13f35352c9d72e1b08dd
  source_path: gateway/cli-backends.md
  workflow: 15
---

# Backend CLI (Runtime de repli)

Lorsqu'un fournisseur d'API est en panne, limité en débit ou temporairement défaillant, OpenClaw peut exécuter un **CLI d'IA local** comme **repli en texte pur**. C'est un design intentionnellement conservateur :

- **Les outils sont désactivés** (pas d'appels d'outils).
- **Entrée texte → Sortie texte** (fiable).
- **Support des conversations** (donc les tours suivants restent cohérents).
- Si le CLI accepte les chemins d'images, **les images peuvent être transmises**.

C'est conçu comme un **filet de sécurité** et non comme un chemin principal. Utilisez-le quand vous voulez une réponse textuelle "qui fonctionne toujours" sans dépendre d'une API externe.

## Démarrage rapide convivial

Vous pouvez utiliser Claude Code CLI **sans aucune configuration** (OpenClaw inclut des valeurs par défaut intégrées) :

```bash
openclaw agent --message "hi" --model claude-cli/opus-4.5
```

Codex CLI fonctionne également prêt à l'emploi :

```bash
openclaw agent --message "hi" --model codex-cli/gpt-5.2-codex
```

Si votre Gateway s'exécute sous launchd/systemd et que votre PATH est minimaliste, ajoutez simplement le chemin de la commande :

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
      },
    },
  },
}
```

C'est tout. Pas de clés, pas de configuration d'authentification supplémentaire, sauf le CLI lui-même.

## Utilisation comme repli

Ajoutez le backend CLI à votre liste de repli, afin qu'il ne s'exécute que si le modèle principal échoue :

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-5",
        fallbacks: ["claude-cli/opus-4.5"],
      },
      models: {
        "anthropic/claude-opus-4-5": { alias: "Opus" },
        "claude-cli/opus-4.5": {},
      },
    },
  },
}
```

Points importants :

- Si vous utilisez `agents.defaults.models` (liste d'autorisation), vous devez inclure `claude-cli/...`.
- Si le fournisseur principal échoue (authentification, limitation de débit, délai d'expiration), OpenClaw essaiera ensuite le backend CLI.

## Aperçu de la configuration

Tous les backends CLI se trouvent à :

```
agents.defaults.cliBackends
```

Chaque entrée est indexée par **ID de fournisseur** (par exemple `claude-cli`, `my-cli`). L'ID de fournisseur devient la partie gauche de votre référence de modèle :

```
<provider>/<model>
```

### Exemple de configuration

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          input: "arg",
          modelArg: "--model",
          modelAliases: {
            "claude-opus-4-5": "opus",
            "claude-sonnet-4-5": "sonnet",
          },
          sessionArg: "--session",
          sessionMode: "existing",
          sessionIdFields: ["session_id", "conversation_id"],
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
          serialize: true,
        },
      },
    },
  },
}
```

## Fonctionnement

1. **Sélection du backend** basée sur le préfixe du fournisseur (`claude-cli/...`).
2. **Construction du message système** en utilisant le même message OpenClaw + contexte de l'espace de travail.
3. **Exécution du CLI** avec l'ID de session (s'il est supporté), pour maintenir l'historique cohérent.
4. **Analyse de la sortie** (JSON ou texte pur) et retour du texte final.
5. **Persistance de l'ID de session** par backend, afin que les demandes suivantes réutilisent la même session CLI.

## Conversations

- Si le CLI supporte les conversations, définissez `sessionArg` (par exemple `--session-id`) ou `sessionArgs` (avec l'espace réservé `{sessionId}`) quand l'ID doit être inséré dans plusieurs drapeaux.
- Si le CLI utilise une **sous-commande de reprise** avec des drapeaux différents, définissez `resumeArgs` (remplace `args` lors de la reprise) ainsi que `resumeOutput` optionnel (pour la reprise non-JSON).
- `sessionMode` :
  - `always` : envoie toujours l'ID de session (utilise un nouvel UUID s'il n'est pas stocké).
  - `existing` : envoie uniquement si un ID de session a été stocké précédemment.
  - `none` : n'envoie jamais l'ID de session.

## Images (transmission)

Si votre CLI accepte les chemins d'images, définissez `imageArg` :

```json5
imageArg: "--image",
imageMode: "repeat"
```

OpenClaw écrira les images base64 dans des fichiers temporaires. Si `imageArg` est défini, ces chemins sont transmis comme arguments CLI. S'il manque `imageArg`, OpenClaw ajoutera les chemins de fichiers au message (injection de chemin), ce qui est suffisant pour les CLI qui chargent automatiquement les fichiers locaux à partir de chemins purs (comportement de Claude Code CLI).

## Entrée / Sortie

- `output: "json"` (par défaut) tente d'analyser JSON et d'extraire le texte + l'ID de session.
- `output: "jsonl"` analyse un flux JSONL (Codex CLI `--json`) et extrait le dernier message d'agent ainsi que `thread_id` s'il existe.
- `output: "text"` traite stdout comme la réponse finale.

Modes d'entrée :

- `input: "arg"` (par défaut) transmet le message comme dernier argument CLI.
- `input: "stdin"` envoie le message via stdin.
- Si le message est long et que `maxPromptArgChars` est défini, stdin est utilisé.

## Valeurs par défaut (intégrées)

OpenClaw inclut des valeurs par défaut pour `claude-cli` :

- `command: "claude"`
- `args: ["-p", "--output-format", "json", "--dangerously-skip-permissions"]`
- `resumeArgs: ["-p", "--output-format", "json", "--dangerously-skip-permissions", "--resume", "{sessionId}"]`
- `modelArg: "--model"`
- `systemPromptArg: "--append-system-prompt"`
- `sessionArg: "--session-id"`
- `systemPromptWhen: "first"`
- `sessionMode: "always"`

OpenClaw inclut également des valeurs par défaut pour `codex-cli` :

- `command: "codex"`
- `args: ["exec","--json","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
- `resumeArgs: ["exec","resume","{sessionId}","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
- `output: "jsonl"`
- `resumeOutput: "text"`
- `modelArg: "--model"`
- `imageArg: "--image"`
- `sessionMode: "existing"`

Remplacez uniquement si nécessaire (courant : chemin absolu `command`).

## Limitations

- **Pas d'outils OpenClaw** (les backends CLI ne reçoivent jamais d'appels d'outils). Certains CLI peuvent toujours exécuter leurs propres outils d'agent.
- **Pas de streaming** (la sortie CLI est collectée puis retournée).
- **Sortie structurée** dépend du format JSON du CLI.
- **Sessions Codex CLI** reprises via sortie texte (pas de JSONL), ce qui est moins structuré que l'exécution `--json` initiale. Les sessions OpenClaw fonctionnent toujours normalement.

## Dépannage

- **CLI introuvable** : définissez `command` sur le chemin complet.
- **Nom de modèle incorrect** : utilisez `modelAliases` pour mapper `provider/model` au modèle CLI.
- **Pas de continuité de conversation** : assurez-vous que `sessionArg` est défini et que `sessionMode` n'est pas `none` (Codex CLI ne peut actuellement pas reprendre avec sortie JSON).
- **Images ignorées** : définissez `imageArg` (et vérifiez que le CLI supporte les chemins de fichiers).
