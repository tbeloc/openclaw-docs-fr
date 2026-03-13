---
summary: "Backends CLI : secours textuel via des CLI IA locales"
read_when:
  - You want a reliable fallback when API providers fail
  - You are running Claude Code CLI or other local AI CLIs and want to reuse them
  - You need a text-only, tool-free path that still supports sessions and images
title: "Backends CLI"
---

# Backends CLI (runtime de secours)

OpenClaw peut exécuter des **CLI IA locales** comme **secours textuel** quand les fournisseurs d'API sont indisponibles,
limités en débit, ou se comportent mal temporairement. C'est intentionnellement conservateur :

- **Les outils sont désactivés** (pas d'appels d'outils).
- **Texte en → texte out** (fiable).
- **Les sessions sont supportées** (donc les tours de suivi restent cohérents).
- **Les images peuvent être transmises** si la CLI accepte les chemins d'images.

C'est conçu comme un **filet de sécurité** plutôt qu'un chemin principal. Utilisez-le quand vous
voulez des réponses textuelles « qui fonctionnent toujours » sans dépendre d'API externes.

## Guide de démarrage rapide pour débutants

Vous pouvez utiliser Claude Code CLI **sans aucune configuration** (OpenClaw inclut une valeur par défaut intégrée) :

```bash
openclaw agent --message "hi" --model claude-cli/opus-4.6
```

Codex CLI fonctionne aussi directement :

```bash
openclaw agent --message "hi" --model codex-cli/gpt-5.4
```

Si votre passerelle s'exécute sous launchd/systemd et que PATH est minimal, ajoutez simplement le
chemin de la commande :

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

C'est tout. Pas de clés, pas de configuration d'authentification supplémentaire au-delà de la CLI elle-même.

## L'utiliser comme secours

Ajoutez un backend CLI à votre liste de secours pour qu'il ne s'exécute que quand les modèles principaux échouent :

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["claude-cli/opus-4.6", "claude-cli/opus-4.5"],
      },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "claude-cli/opus-4.6": {},
        "claude-cli/opus-4.5": {},
      },
    },
  },
}
```

Notes :

- Si vous utilisez `agents.defaults.models` (liste blanche), vous devez inclure `claude-cli/...`.
- Si le fournisseur principal échoue (authentification, limites de débit, délais d'expiration), OpenClaw
  essaiera ensuite le backend CLI.

## Aperçu de la configuration

Tous les backends CLI se trouvent sous :

```
agents.defaults.cliBackends
```

Chaque entrée est indexée par un **identifiant de fournisseur** (par ex. `claude-cli`, `my-cli`).
L'identifiant du fournisseur devient le côté gauche de votre référence de modèle :

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
            "claude-opus-4-6": "opus",
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

## Comment ça marche

1. **Sélectionne un backend** basé sur le préfixe du fournisseur (`claude-cli/...`).
2. **Construit une invite système** en utilisant le même prompt OpenClaw + contexte de l'espace de travail.
3. **Exécute la CLI** avec un identifiant de session (si supporté) pour que l'historique reste cohérent.
4. **Analyse la sortie** (JSON ou texte brut) et retourne le texte final.
5. **Persiste les identifiants de session** par backend, donc les suites réutilisent la même session CLI.

## Sessions

- Si la CLI supporte les sessions, définissez `sessionArg` (par ex. `--session-id`) ou
  `sessionArgs` (placeholder `{sessionId}`) quand l'ID doit être inséré
  dans plusieurs drapeaux.
- Si la CLI utilise une **sous-commande de reprise** avec des drapeaux différents, définissez
  `resumeArgs` (remplace `args` lors de la reprise) et optionnellement `resumeOutput`
  (pour les reprises non-JSON).
- `sessionMode`:
  - `always`: toujours envoyer un identifiant de session (nouvel UUID si aucun stocké).
  - `existing`: envoyer un identifiant de session seulement s'il a été stocké avant.
  - `none`: ne jamais envoyer d'identifiant de session.

## Images (transmission directe)

Si votre CLI accepte les chemins d'images, définissez `imageArg` :

```json5
imageArg: "--image",
imageMode: "repeat"
```

OpenClaw écrira les images base64 dans des fichiers temporaires. Si `imageArg` est défini, ces
chemins sont passés comme arguments CLI. Si `imageArg` est manquant, OpenClaw ajoute les
chemins de fichiers à l'invite (injection de chemin), ce qui suffit pour les CLI qui chargent automatiquement
les fichiers locaux à partir de chemins simples (comportement de Claude Code CLI).

## Entrées / sorties

- `output: "json"` (par défaut) essaie d'analyser JSON et d'extraire le texte + identifiant de session.
- `output: "jsonl"` analyse les flux JSONL (Codex CLI `--json`) et extrait le
  dernier message d'agent plus `thread_id` quand présent.
- `output: "text"` traite stdout comme la réponse finale.

Modes d'entrée :

- `input: "arg"` (par défaut) passe l'invite comme dernier argument CLI.
- `input: "stdin"` envoie l'invite via stdin.
- Si l'invite est très longue et `maxPromptArgChars` est défini, stdin est utilisé.

## Valeurs par défaut (intégrées)

OpenClaw inclut une valeur par défaut pour `claude-cli` :

- `command: "claude"`
- `args: ["-p", "--output-format", "json", "--permission-mode", "bypassPermissions"]`
- `resumeArgs: ["-p", "--output-format", "json", "--permission-mode", "bypassPermissions", "--resume", "{sessionId}"]`
- `modelArg: "--model"`
- `systemPromptArg: "--append-system-prompt"`
- `sessionArg: "--session-id"`
- `systemPromptWhen: "first"`
- `sessionMode: "always"`

OpenClaw inclut aussi une valeur par défaut pour `codex-cli` :

- `command: "codex"`
- `args: ["exec","--json","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
- `resumeArgs: ["exec","resume","{sessionId}","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
- `output: "jsonl"`
- `resumeOutput: "text"`
- `modelArg: "--model"`
- `imageArg: "--image"`
- `sessionMode: "existing"`

Remplacez seulement si nécessaire (courant : chemin absolu `command`).

## Limitations

- **Pas d'outils OpenClaw** (le backend CLI ne reçoit jamais d'appels d'outils). Certaines CLI
  peuvent toujours exécuter leur propre outillage d'agent.
- **Pas de streaming** (la sortie CLI est collectée puis retournée).
- **Les sorties structurées** dépendent du format JSON de la CLI.
- **Les sessions Codex CLI** reprennent via sortie texte (pas de JSONL), ce qui est moins
  structuré que l'exécution initiale `--json`. Les sessions OpenClaw fonctionnent toujours
  normalement.

## Dépannage

- **CLI non trouvée** : définissez `command` sur un chemin complet.
- **Nom de modèle incorrect** : utilisez `modelAliases` pour mapper `provider/model` → modèle CLI.
- **Pas de continuité de session** : assurez-vous que `sessionArg` est défini et `sessionMode` n'est pas
  `none` (Codex CLI ne peut actuellement pas reprendre avec sortie JSON).
- **Images ignorées** : définissez `imageArg` (et vérifiez que la CLI supporte les chemins de fichiers).
