---
summary: "Compétences : gérées vs workspace, règles de gating et câblage config/env"
read_when:
  - Adding or modifying skills
  - Changing skill gating or load rules
title: "Compétences"
---

# Compétences (OpenClaw)

OpenClaw utilise des dossiers de compétences **[AgentSkills](https://agentskills.io)-compatibles** pour enseigner à l'agent comment utiliser les outils. Chaque compétence est un répertoire contenant un `SKILL.md` avec un frontmatter YAML et des instructions. OpenClaw charge les **compétences intégrées** plus les remplacements locaux optionnels, et les filtre au moment du chargement en fonction de l'environnement, de la configuration et de la présence binaire.

## Emplacements et précédence

Les compétences sont chargées à partir de **trois** endroits :

1. **Compétences intégrées** : livrées avec l'installation (package npm ou OpenClaw.app)
2. **Compétences gérées/locales** : `~/.openclaw/skills`
3. **Compétences workspace** : `<workspace>/skills`

En cas de conflit de nom de compétence, la précédence est :

`<workspace>/skills` (la plus élevée) → `~/.openclaw/skills` → compétences intégrées (la plus basse)

De plus, vous pouvez configurer des dossiers de compétences supplémentaires (précédence la plus basse) via
`skills.load.extraDirs` dans `~/.openclaw/openclaw.json`.

## Compétences par agent vs compétences partagées

Dans les configurations **multi-agents**, chaque agent a son propre workspace. Cela signifie :

- Les **compétences par agent** se trouvent dans `<workspace>/skills` pour cet agent uniquement.
- Les **compétences partagées** se trouvent dans `~/.openclaw/skills` (gérées/locales) et sont visibles
  pour **tous les agents** sur la même machine.
- Les **dossiers partagés** peuvent également être ajoutés via `skills.load.extraDirs` (précédence la plus basse) si vous souhaitez un pack de compétences commun utilisé par plusieurs agents.

Si le même nom de compétence existe à plus d'un endroit, la précédence habituelle
s'applique : workspace gagne, puis gérée/locale, puis intégrée.

## Plugins + compétences

Les plugins peuvent livrer leurs propres compétences en listant les répertoires `skills` dans
`openclaw.plugin.json` (chemins relatifs à la racine du plugin). Les compétences des plugins se chargent
lorsque le plugin est activé et participent aux règles de précédence des compétences normales.
Vous pouvez les gater via `metadata.openclaw.requires.config` sur l'entrée de configuration du plugin. Voir [Plugins](/tools/plugin) pour la découverte/configuration et [Outils](/tools) pour la
surface d'outils que ces compétences enseignent.

## ClawHub (installation + synchronisation)

ClawHub est le registre public des compétences pour OpenClaw. Parcourez à
[https://clawhub.com](https://clawhub.com). Utilisez-le pour découvrir, installer, mettre à jour et sauvegarder les compétences.
Guide complet : [ClawHub](/tools/clawhub).

Flux courants :

- Installer une compétence dans votre workspace :
  - `clawhub install <skill-slug>`
- Mettre à jour toutes les compétences installées :
  - `clawhub update --all`
- Synchroniser (scanner + publier les mises à jour) :
  - `clawhub sync --all`

Par défaut, `clawhub` installe dans `./skills` sous votre répertoire de travail actuel
(ou revient au workspace OpenClaw configuré). OpenClaw le récupère
comme `<workspace>/skills` à la session suivante.

## Notes de sécurité

- Traitez les compétences tierces comme du **code non approuvé**. Lisez-les avant de les activer.
- Préférez les exécutions en sandbox pour les entrées non approuvées et les outils risqués. Voir [Sandboxing](/gateway/sandboxing).
- La découverte des compétences du workspace et des répertoires supplémentaires n'accepte que les racines de compétences et les fichiers `SKILL.md` dont le realpath résolu reste à l'intérieur de la racine configurée.
- `skills.entries.*.env` et `skills.entries.*.apiKey` injectent des secrets dans le **processus hôte**
  pour ce tour d'agent (pas le sandbox). Gardez les secrets hors des prompts et des logs.
- Pour un modèle de menace plus large et des listes de contrôle, voir [Sécurité](/gateway/security).

## Format (AgentSkills + compatible Pi)

`SKILL.md` doit inclure au minimum :

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
---
```

Notes :

- Nous suivons la spécification AgentSkills pour la mise en page/intention.
- L'analyseur utilisé par l'agent intégré ne supporte que les clés frontmatter **sur une seule ligne**.
- `metadata` doit être un **objet JSON sur une seule ligne**.
- Utilisez `{baseDir}` dans les instructions pour référencer le chemin du dossier de compétence.
- Clés frontmatter optionnelles :
  - `homepage` — URL affichée comme « Site Web » dans l'interface des compétences macOS (également supportée via `metadata.openclaw.homepage`).
  - `user-invocable` — `true|false` (par défaut : `true`). Quand `true`, la compétence est exposée comme une commande slash utilisateur.
  - `disable-model-invocation` — `true|false` (par défaut : `false`). Quand `true`, la compétence est exclue du prompt du modèle (toujours disponible via invocation utilisateur).
  - `command-dispatch` — `tool` (optionnel). Quand défini à `tool`, la commande slash contourne le modèle et se dispatche directement à un outil.
  - `command-tool` — nom de l'outil à invoquer quand `command-dispatch: tool` est défini.
  - `command-arg-mode` — `raw` (par défaut). Pour le dispatch d'outil, transfère la chaîne d'arguments bruts à l'outil (pas d'analyse core).

    L'outil est invoqué avec les paramètres :
    `{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`.

## Gating (filtres au moment du chargement)

OpenClaw **filtre les compétences au moment du chargement** en utilisant `metadata` (JSON sur une seule ligne) :

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

- `always: true` — toujours inclure la compétence (ignorer les autres gates).
- `emoji` — emoji optionnel utilisé par l'interface des compétences macOS.
- `homepage` — URL optionnelle affichée comme « Site Web » dans l'interface des compétences macOS.
- `os` — liste optionnelle de plateformes (`darwin`, `linux`, `win32`). Si défini, la compétence n'est éligible que sur ces systèmes d'exploitation.
- `requires.bins` — liste ; chacun doit exister sur `PATH`.
- `requires.anyBins` — liste ; au moins un doit exister sur `PATH`.
- `requires.env` — liste ; la variable d'environnement doit exister **ou** être fournie dans la configuration.
- `requires.config` — liste de chemins `openclaw.json` qui doivent être truthy.
- `primaryEnv` — nom de la variable d'environnement associée à `skills.entries.<name>.apiKey`.
- `install` — tableau optionnel de spécifications d'installateur utilisées par l'interface des compétences macOS (brew/node/go/uv/download).

Note sur le sandboxing :

- `requires.bins` est vérifié sur l'**hôte** au moment du chargement de la compétence.
- Si un agent est en sandbox, le binaire doit également exister **à l'intérieur du conteneur**.
  Installez-le via `agents.defaults.sandbox.docker.setupCommand` (ou une image personnalisée).
  `setupCommand` s'exécute une fois après la création du conteneur.
  Les installations de packages nécessitent également une sortie réseau, un système de fichiers racine inscriptible et un utilisateur root dans le sandbox.
  Exemple : la compétence `summarize` (`skills/summarize/SKILL.md`) a besoin du CLI `summarize`
  dans le conteneur sandbox pour s'y exécuter.

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

Notes :

- Si plusieurs installateurs sont listés, la gateway choisit une **seule** option préférée (brew quand disponible, sinon node).
- Si tous les installateurs sont `download`, OpenClaw liste chaque entrée pour que vous puissiez voir les artefacts disponibles.
- Les spécifications d'installateur peuvent inclure `os: ["darwin"|"linux"|"win32"]` pour filtrer les options par plateforme.
- Les installations Node respectent `skills.install.nodeManager` dans `openclaw.json` (par défaut : npm ; options : npm/pnpm/yarn/bun).
  Cela affecte uniquement les **installations de compétences** ; le runtime de la Gateway doit toujours être Node
  (Bun n'est pas recommandé pour WhatsApp/Telegram).
- Installations Go : si `go` est manquant et `brew` est disponible, la gateway installe Go via Homebrew d'abord et définit `GOBIN` sur le `bin` de Homebrew quand possible.
- Installations Download : `url` (requis), `archive` (`tar.gz` | `tar.bz2` | `zip`), `extract` (par défaut : auto quand archive détectée), `stripComponents`, `targetDir` (par défaut : `~/.openclaw/tools/<skillKey>`).

Si aucun `metadata.openclaw` n'est présent, la compétence est toujours éligible (sauf si
désactivée dans la configuration ou bloquée par `skills.allowBundled` pour les compétences intégrées).

## Remplacements de configuration (`~/.openclaw/openclaw.json`)

Les compétences intégrées/gérées peuvent être basculées et fournies avec des valeurs d'environnement :

```json5
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
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

Note : si le nom de la compétence contient des tirets, citez la clé (JSON5 permet les clés citées).

Les clés de configuration correspondent au **nom de la compétence** par défaut. Si une compétence définit
`metadata.openclaw.skillKey`, utilisez cette clé sous `skills.entries`.

Règles :

- `enabled: false` désactive la compétence même si elle est intégrée/installée.
- `env` : injecté **seulement si** la variable n'est pas déjà définie dans le processus.
- `apiKey` : commodité pour les compétences qui déclarent `metadata.openclaw.primaryEnv`.
  Supporte une chaîne en texte brut ou un objet SecretRef (`{ source, provider, id }`).
- `config` : sac optionnel pour les champs personnalisés par compétence ; les clés personnalisées doivent vivre ici.
- `allowBundled` : liste d'autorisation optionnelle pour les compétences **intégrées** uniquement. Si défini, seules
  les compétences intégrées dans la liste sont éligibles (les compétences gérées/workspace ne sont pas affectées).

## Injection d'environnement (par exécution d'agent)

Quand une exécution d'agent démarre, OpenClaw :

1. Lit les métadonnées de compétence.
2. Applique tout `skills.entries.<key>.env` ou `skills.entries.<key>.apiKey` à
   `process.env`.
3. Construit le prompt système avec les compétences **éligibles**.
4. Restaure l'environnement d'origine après la fin de l'exécution.

Ceci est **limité à l'exécution de l'agent**, pas un environnement shell global.

## Snapshot de session (performance)

OpenClaw prend un snapshot des compétences éligibles **quand une session démarre** et réutilise cette liste pour les tours suivants dans la même session. Les modifications des compétences ou de la configuration prennent effet à la prochaine nouvelle session.

Les compétences peuvent également s'actualiser en milieu de session quand le watcher de compétences est activé ou quand un nouveau nœud distant éligible apparaît (voir ci-dessous). Pensez à cela comme un **hot reload** : la liste actualisée est récupérée au prochain tour d'agent.

## Nœuds macOS distants (gateway Linux)

Si la Gateway s'exécute sur Linux mais qu'un **nœud macOS** est connecté **avec `system.run` autorisé** (les approbations de sécurité Exec ne sont pas définies sur `deny`), OpenClaw peut traiter les compétences macOS uniquement comme éligibles quand les binaires requis sont présents sur ce nœud. L'agent doit exécuter ces compétences via l'outil `nodes` (généralement `nodes.run`).

Cela dépend du nœud signalant son support de commande et d'une sonde bin via `system.run`. Si le nœud macOS se déconnecte plus tard, les compétences restent visibles ; les invocations peuvent échouer jusqu'à ce que le nœud se reconnecte.

## Watcher de compétences (actualisation automatique)

Par défaut, OpenClaw surveille les dossiers de compétences et met à jour le snapshot de compétences quand les fichiers `SKILL.md` changent. Configurez ceci sous `skills.load` :

```json5
{
  skills: {
    load: {
      watch: true,
      watchDebounceMs: 250,
    },
  },
}
```

## Impact sur les tokens (liste de compétences)

Quand les compétences sont éligibles, OpenClaw injecte une liste XML compacte des compétences disponibles dans le prompt système (via `formatSkillsForPrompt` dans `pi-coding-agent`). Le coût est déterministe :

- **Surcharge de base (seulement quand ≥1 compétence) :** 195 caractères.
- **Par compétence :** 97 caractères + la longueur des valeurs `<name>`, `<description>` et `<location>` échappées en XML.

Formule (caractères) :

```
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

Notes :

- L'échappement XML développe `& < > " '` en entités (`&amp;`, `&lt;`, etc.), augmentant la longueur.
- Les comptages de tokens varient selon le tokenizer du modèle. Une estimation approximative de style OpenAI est ~4 caractères/token, donc **97 caractères ≈ 24 tokens** par compétence plus vos longueurs de champs réelles.

## Cycle de vie des compétences gérées

OpenClaw est livré avec un ensemble de base de compétences en tant que **compétences groupées** dans le cadre de l'installation (package npm ou OpenClaw.app). `~/.openclaw/skills` existe pour les remplacements locaux (par exemple, épingler/corriger une compétence sans modifier la copie groupée). Les compétences de l'espace de travail sont détenues par l'utilisateur et remplacent les deux en cas de conflits de noms.

## Référence de configuration

Voir [Configuration des compétences](/tools/skills-config) pour le schéma de configuration complet.

## Vous cherchez plus de compétences ?

Parcourez [https://clawhub.com](https://clawhub.com).

---
