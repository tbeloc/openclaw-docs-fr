---
summary: "Où OpenClaw charge les variables d'environnement et l'ordre de précédence"
read_when:
  - You need to know which env vars are loaded, and in what order
  - You are debugging missing API keys in the Gateway
  - You are documenting provider auth or deployment environments
title: "Variables d'environnement"
---

# Variables d'environnement

OpenClaw récupère les variables d'environnement à partir de plusieurs sources. La règle est **ne jamais remplacer les valeurs existantes**.

## Précédence (la plus haute → la plus basse)

1. **Environnement du processus** (ce que le processus Gateway a déjà du shell/daemon parent).
2. **`.env` dans le répertoire de travail actuel** (dotenv par défaut ; ne remplace pas).
3. **`.env` global** à `~/.openclaw/.env` (alias `$OPENCLAW_STATE_DIR/.env` ; ne remplace pas).
4. **Bloc `env` de la configuration** dans `~/.openclaw/openclaw.json` (appliqué uniquement s'il manque).
5. **Import de shell de connexion optionnel** (`env.shellEnv.enabled` ou `OPENCLAW_LOAD_SHELL_ENV=1`), appliqué uniquement pour les clés attendues manquantes.

Si le fichier de configuration est complètement absent, l'étape 4 est ignorée ; l'import de shell s'exécute toujours s'il est activé.

## Bloc `env` de la configuration

Deux façons équivalentes de définir des variables d'environnement en ligne (les deux ne remplacent pas) :

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

## Import de shell env

`env.shellEnv` exécute votre shell de connexion et importe uniquement les clés attendues **manquantes** :

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Équivalents de variables d'environnement :

- `OPENCLAW_LOAD_SHELL_ENV=1`
- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

## Variables d'environnement injectées au runtime

OpenClaw injecte également des marqueurs de contexte dans les processus enfants générés :

- `OPENCLAW_SHELL=exec` : défini pour les commandes exécutées via l'outil `exec`.
- `OPENCLAW_SHELL=acp` : défini pour les générations de processus du backend runtime ACP (par exemple `acpx`).
- `OPENCLAW_SHELL=acp-client` : défini pour `openclaw acp client` lorsqu'il génère le processus du pont ACP.
- `OPENCLAW_SHELL=tui-local` : défini pour les commandes shell `!` TUI locales.

Ce sont des marqueurs de runtime (pas une configuration utilisateur requise). Ils peuvent être utilisés dans la logique shell/profile pour appliquer des règles spécifiques au contexte.

## Variables d'environnement de l'interface utilisateur

- `OPENCLAW_THEME=light` : force la palette TUI claire lorsque votre terminal a un fond clair.
- `OPENCLAW_THEME=dark` : force la palette TUI sombre.
- `COLORFGBG` : si votre terminal l'exporte, OpenClaw utilise l'indice de couleur de fond pour choisir automatiquement la palette TUI.

## Substitution de variables d'environnement dans la configuration

Vous pouvez référencer les variables d'environnement directement dans les valeurs de chaîne de configuration en utilisant la syntaxe `${VAR_NAME}` :

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
}
```

Voir [Configuration : Substitution de variables d'environnement](/gateway/configuration#env-var-substitution-in-config) pour plus de détails.

## Références secrètes vs chaînes `${ENV}`

OpenClaw supporte deux modèles pilotés par env :

- Substitution de chaîne `${VAR}` dans les valeurs de configuration.
- Objets SecretRef (`{ source: "env", provider: "default", id: "VAR" }`) pour les champs qui supportent les références de secrets.

Les deux se résolvent à partir de l'env du processus au moment de l'activation. Les détails de SecretRef sont documentés dans [Gestion des secrets](/gateway/secrets).

## Variables d'environnement liées aux chemins

| Variable               | Objectif                                                                                                                                                                          |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OPENCLAW_HOME`        | Remplacer le répertoire personnel utilisé pour toute la résolution de chemin interne (`~/.openclaw/`, répertoires d'agents, sessions, identifiants). Utile lors de l'exécution d'OpenClaw en tant qu'utilisateur de service dédié. |
| `OPENCLAW_STATE_DIR`   | Remplacer le répertoire d'état (par défaut `~/.openclaw`).                                                                                                                            |
| `OPENCLAW_CONFIG_PATH` | Remplacer le chemin du fichier de configuration (par défaut `~/.openclaw/openclaw.json`).                                                                                                                             |

## Journalisation

| Variable             | Objectif                                                                                                                                                                                      |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OPENCLAW_LOG_LEVEL` | Remplacer le niveau de journalisation pour le fichier et la console (par exemple `debug`, `trace`). Prend la priorité sur `logging.level` et `logging.consoleLevel` dans la configuration. Les valeurs invalides sont ignorées avec un avertissement. |

### `OPENCLAW_HOME`

Lorsqu'elle est définie, `OPENCLAW_HOME` remplace le répertoire personnel du système (`$HOME` / `os.homedir()`) pour toute la résolution de chemin interne. Cela permet une isolation complète du système de fichiers pour les comptes de service sans interface.

**Précédence :** `OPENCLAW_HOME` > `$HOME` > `USERPROFILE` > `os.homedir()`

**Exemple** (macOS LaunchDaemon) :

```xml
<key>EnvironmentVariables</key>
<dict>
  <key>OPENCLAW_HOME</key>
  <string>/Users/kira</string>
</dict>
```

`OPENCLAW_HOME` peut également être défini sur un chemin tilde (par exemple `~/svc`), qui est développé en utilisant `$HOME` avant utilisation.

## Connexes

- [Configuration de la passerelle](/gateway/configuration)
- [FAQ : variables d'environnement et chargement .env](/help/faq#env-vars-and-env-loading)
- [Aperçu des modèles](/concepts/models)
