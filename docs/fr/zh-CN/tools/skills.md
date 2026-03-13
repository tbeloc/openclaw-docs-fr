---
read_when:
  - Ajouter ou modifier des Skills
  - Modifier les règles de gating ou de chargement des Skills
summary: Skills : hébergement dans l'espace de travail, règles de gating et connexion aux variables de configuration/environnement
title: Skills
x-i18n:
  generated_at: "2026-02-03T10:12:27Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 54685da5885600b367ccdad6342497199fcb168ce33f8cdc00391d993f3bab7e
  source_path: tools/skills.md
  workflow: 15
---

# Skills (OpenClaw)

OpenClaw utilise des dossiers Skills **compatibles avec [AgentSkills](https://agentskills.io)** pour enseigner aux agents comment utiliser les outils. Chaque Skill est un répertoire contenant un `SKILL.md` avec un frontmatter YAML et des instructions. OpenClaw charge les **Skills intégrés** ainsi que les remplacements locaux optionnels, et les filtre au chargement en fonction de l'environnement, de la configuration et de l'existence des fichiers binaires.

## Emplacements et priorités

Les Skills sont chargés à partir de **trois** emplacements :

1. **Skills intégrés** : distribués avec le package d'installation (package npm ou OpenClaw.app)
2. **Skills hébergés/locaux** : `~/.openclaw/skills`
3. **Skills de l'espace de travail** : `<workspace>/skills`

En cas de conflit de noms de Skills, la priorité est :

`<workspace>/skills` (la plus élevée) → `~/.openclaw/skills` → Skills intégrés (la plus basse)

De plus, vous pouvez configurer des dossiers Skills supplémentaires via `skills.load.extraDirs` dans `~/.openclaw/openclaw.json` (priorité la plus basse).

## Skills mono-agent vs partagés

Dans une configuration **multi-agents**, chaque agent dispose de son propre espace de travail. Cela signifie :

- Les **Skills mono-agent** se trouvent dans `<workspace>/skills` et ne sont utilisés que par cet agent.
- Les **Skills partagés** se trouvent dans `~/.openclaw/skills` (hébergés/locaux) et sont visibles pour **tous les agents** sur la même machine.
- Si vous souhaitez que plusieurs agents utilisent un package Skills commun, vous pouvez également ajouter un **dossier partagé** via `skills.load.extraDirs` (priorité la plus basse).

Si le même nom de Skill existe à plusieurs emplacements, les règles de priorité habituelles s'appliquent : l'espace de travail en premier, puis hébergé/local, puis intégré.

## Plugins + Skills

Les plugins peuvent publier leurs propres Skills en listant un répertoire `skills` (chemin relatif à la racine du plugin) dans `openclaw.plugin.json`. Les Skills des plugins sont chargés lorsque le plugin est activé et participent aux règles de priorité normales des Skills. Vous pouvez les gater via `metadata.openclaw.requires.config` sur l'entrée de configuration du plugin. Voir [Plugins](/tools/plugin) pour la découverte/configuration, et [Outils](/tools) pour les interfaces d'outils enseignées par ces Skills.

## ClawHub (installation + synchronisation)

ClawHub est le registre public des Skills pour OpenClaw. Parcourez https://clawhub.com. Utilisez-le pour découvrir, installer, mettre à jour et sauvegarder les Skills. Guide complet : [ClawHub](/tools/clawhub).

Flux courants :

- Installer des Skills dans votre espace de travail :
  - `clawhub install <skill-slug>`
- Mettre à jour tous les Skills installés :
  - `clawhub update --all`
- Synchroniser (scanner + publier les mises à jour) :
  - `clawhub sync --all`

Par défaut, `clawhub` installe dans `./skills` sous le répertoire de travail actuel (ou revient à l'espace de travail OpenClaw configuré). OpenClaw le reconnaît comme `<workspace>/skills` à la session suivante.

## Considérations de sécurité

- Traitez les Skills tiers comme du **code non approuvé**. Lisez-les avant de les activer.
- Pour les entrées non approuvées et les outils à haut risque, privilégiez l'exécution en isolation de bac à sable. Voir [Bac à sable](/gateway/sandboxing).
- `skills.entries.*.env` et `skills.entries.*.apiKey` injectent des secrets dans le processus **hôte** pour cette exécution d'agent (pas dans le bac à sable). Gardez les secrets hors des invites et des journaux.
- Pour un modèle de menace plus large et une liste de contrôle, voir [Sécurité](/gateway/security).

## Format (AgentSkills + compatible Pi)

`SKILL.md` doit contenir au minimum :

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
---
```

Remarques :

- Nous suivons la disposition/intention de la spécification AgentSkills.
- Le parseur utilisé par les agents intégrés ne supporte que les clés frontmatter **sur une seule ligne**.
- `metadata` doit être un **objet JSON sur une seule ligne**.
- Utilisez `{baseDir}` dans les instructions pour référencer le chemin du dossier Skills.
- Clés frontmatter optionnelles :
  - `homepage` — URL affichée comme « Website » dans l'interface macOS Skills (également supportée via `metadata.openclaw.homepage`).
  - `user-invocable` — `true|false` (par défaut : `true`). Quand `true`, le Skill est exposé comme commande slash utilisateur.
  - `disable-model-invocation` — `true|false` (par défaut : `false`). Quand `true`, le Skill est exclu de l'invite du modèle (toujours utilisable via invocation utilisateur).
  - `command-dispatch` — `tool` (optionnel). Quand défini à `tool`, la commande slash contourne le modèle et se dispatche directement à l'outil.
  - `command-tool` — Nom de l'outil à invoquer quand `command-dispatch: tool` est défini.
  - `command-arg-mode` — `raw` (par défaut). Pour le dispatch d'outil, transmet la chaîne d'arguments bruts à l'outil (pas d'analyse de base).

    L'outil est invoqué avec les paramètres suivants :
    `{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`.

## Gating (filtrage au chargement)

OpenClaw utilise `metadata` (JSON sur une seule ligne) pour **filtrer les Skills au chargement** :

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
      },
  }
---
```

Champs sous `metadata.openclaw` :

- `always: true` — Inclure toujours ce Skill (ignorer les autres gatings).
- `emoji` — Emoji optionnel utilisé par l'interface macOS Skills.
- `homepage` — URL optionnelle affichée comme « Website » dans l'interface macOS Skills.
- `os` — Liste optionnelle de plateformes (`darwin`, `linux`, `win32`). Si défini, ce Skill n'est admissible que sur ces systèmes d'exploitation.
- `requires.bins` — Liste ; chacun doit exister dans `PATH`.
- `requires.anyBins` — Liste ; au moins un doit exister dans `PATH`.
- `requires.env` — Liste ; les variables d'environnement doivent exister **ou** être fournies dans la configuration.
- `requires.config` — Liste de chemins `openclaw.json` qui doivent être des valeurs vraies.
- `primaryEnv` — Nom de la variable d'environnement associée à `skills.entries.<name>.apiKey`.
- `install` — Tableau optionnel de spécifications d'installateur utilisées par l'interface macOS Skills (brew/node/go/uv/download).

Remarques sur le bac à sable :

- `requires.bins` est vérifié sur l'**hôte** au chargement du Skill.
- Si l'agent est en bac à sable, le fichier binaire doit également exister **à l'intérieur du conteneur**. Installez-le via `agents.defaults.sandbox.docker.setupCommand` (ou une image personnalisée). `setupCommand` s'exécute une fois après la création du conteneur. L'installation de packages nécessite également une sortie réseau, un système de fichiers racine inscriptible et l'utilisateur root dans le bac à sable. Exemple : le Skill `summarize` (`skills/summarize/SKILL.md`) nécessite le CLI `summarize` dans le conteneur du bac à sable pour s'exécuter.

Exemple d'installateur :

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

Remarques :

- Si plusieurs installateurs sont listés, la Gateway choisit **une seule** option préférée (brew si disponible, sinon node).
- Si tous les installateurs sont `download`, OpenClaw liste chaque entrée pour que vous puissiez voir les artefacts disponibles.
- Les spécifications d'installateur peuvent inclure `os: ["darwin"|"linux"|"win32"]` pour filtrer les options par plateforme.
- L'installation Node suit `skills.install.nodeManager` dans `openclaw.json` (par défaut : npm ; options : npm/pnpm/yarn/bun). Cela affecte uniquement l'**installation des Skills** ; le runtime de la Gateway doit toujours être Node (Bun n'est pas recommandé pour WhatsApp/Telegram).
- Installation Go : si `go` est manquant et `brew` est disponible, la Gateway installe d'abord Go via Homebrew et définit `GOBIN` sur le `bin` de Homebrew si possible.
- Installation Download : `url` (obligatoire), `archive` (`tar.gz` | `tar.bz2` | `zip`), `extract` (par défaut : détection automatique si archive), `stripComponents`, `targetDir` (par défaut : `~/.openclaw/tools/<skillKey>`).

S'il n'y a pas de `metadata.openclaw`, le Skill est toujours admissible (sauf s'il est désactivé dans la configuration ou bloqué par `skills.allowBundled` pour les Skills intégrés).

## Remplacements de configuration (`~/.openclaw/openclaw.json`)

Les Skills intégrés/hébergés peuvent être basculés et fournir des valeurs de variables d'environnement :

```json5
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
        config: {
          endpoint: "https://example.invalid",
          model: "nano-pro",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

Remarque : si le nom du Skill contient des tirets, mettez la clé entre guillemets (JSON5 permet les clés entre guillemets).

Les clés de configuration correspondent par défaut au **nom du Skill**. Si le Skill définit `metadata.openclaw.skillKey`, utilisez cette clé sous `skills.entries`.

Règles :

- `enabled: false` désactive le Skill, même s'il est intégré/installé.
- `env` : injecté **uniquement si** la variable n'est pas déjà définie dans le processus.
- `apiKey` : champ de commodité pour les Skills déclarant `metadata.openclaw.primaryEnv`.
- `config` : conteneur optionnel pour les champs personnalisés d'un seul Skill ; les clés personnalisées doivent aller ici.
- `allowBundled` : liste blanche optionnelle **uniquement pour les Skills intégrés**. Si défini, seuls les Skills intégrés de la liste sont admissibles (les Skills hébergés/espace de travail ne sont pas affectés).

## Injection de variables d'environnement (à chaque exécution d'agent)

Quand une exécution d'agent commence, OpenClaw :

1. Lit les métadonnées des Skills.
2. Applique tout `skills.entries.<key>.env` ou `skills.entries.<key>.apiKey` à `process.env`.
3. Construit l'invite système avec les Skills **admissibles**.
4. Restaure l'environnement d'origine après la fin de l'exécution.

Ceci est **limité à la portée de l'exécution de l'agent**, pas l'environnement shell global.

## Snapshot de session (performance)

OpenClaw prend un snapshot des Skills admissibles **au début de la session** et réutilise cette liste dans les tours suivants de la même session. Les modifications apportées aux Skills ou à la configuration prennent effet dans la session suivante.

Les Skills peuvent également être actualisés au cours d'une session lorsque le moniteur de Skills est activé ou qu'un nouveau nœud distant admissible apparaît (voir ci-dessous). Considérez cela comme un **rechargement à chaud** : la liste actualisée est récupérée au prochain tour d'agent.

## Nœuds macOS distants (Gateway Linux)

Si la Gateway s'exécute sur Linux mais est connectée à un **nœud macOS permettant `system.run`** (paramètre de sécurité Exec approval non défini à `deny`), OpenClaw peut considérer les Skills macOS uniquement comme admissibles quand le fichier binaire requis existe sur ce nœud. L'agent doit exécuter ces Skills via l'outil `nodes` (généralement `nodes.run`).

Cela dépend du nœud signalant son support de commandes et de la détection de fichiers binaires via `system.run`. Si le nœud macOS se déconnecte ultérieurement, les Skills restent visibles ; l'invocation peut échouer jusqu'à la reconnexion du nœud.

## Moniteur de Skills (actualisation automatique)

Par défaut, OpenClaw surveille les dossiers Skills et met à jour le snapshot des Skills qu
