---
read_when:
  - 添加或修改 Skills 配置
  - 调整内置白名单或安装行为
summary: Skills 配置 schema 和示例
title: Skills 配置
x-i18n:
  generated_at: "2026-02-03T10:10:59Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e265c93da7856887c11abd92b379349181549e1a02164184d61a8d1f6b2feed5
  source_path: tools/skills-config.md
  workflow: 15
---

# Configuration des Skills

Toutes les configurations liées aux Skills se trouvent sous `skills` dans `~/.openclaw/openclaw.json`.

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun（Gateway 网关运行时仍为 Node；不推荐 bun）
    },
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

## Champs

- `allowBundled` : Liste blanche optionnelle réservée aux Skills **intégrés** uniquement. Une fois définie, seuls les Skills intégrés de la liste sont éligibles (les Skills hébergés/d'espace de travail ne sont pas affectés).
- `load.extraDirs` : Répertoires de Skills supplémentaires à analyser (priorité la plus basse).
- `load.watch` : Surveille les dossiers de Skills et actualise les snapshots de Skills (par défaut : true).
- `load.watchDebounceMs` : Délai de débounce pour les événements du moniteur de Skills (en millisecondes) (par défaut : 250).
- `install.preferBrew` : Préfère l'installateur brew lorsqu'il est disponible (par défaut : true).
- `install.nodeManager` : Préférence du gestionnaire de nœuds (`npm` | `pnpm` | `yarn` | `bun`, par défaut : npm). Cela affecte uniquement l'**installation des Skills** ; le runtime Gateway doit rester Node (Bun n'est pas recommandé pour WhatsApp/Telegram).
- `entries.<skillKey>` : Remplacements de Skills individuels.

Champs de Skills individuels :

- `enabled` : Définissez à `false` pour désactiver un Skills, même s'il est intégré/installé.
- `env` : Variables d'environnement injectées pour l'exécution de l'agent (uniquement si elles ne sont pas déjà définies).
- `apiKey` : Champ de commodité optionnel pour déclarer la variable d'environnement principale des Skills.

## Remarques

- Les clés sous `entries` sont mappées par défaut aux noms de Skills. Si le Skills définit `metadata.openclaw.skillKey`, cette clé est utilisée à la place.
- Lorsque le moniteur est activé, les modifications des Skills sont récupérées au prochain tour de l'agent.

### Skills isolés en sandbox + variables d'environnement

Lorsqu'une session est en état **sandbox isolé**, le processus Skills s'exécute dans Docker. Le sandbox **n'hérite pas** de `process.env` de la machine hôte.

Utilisez l'une des méthodes suivantes :

- `agents.defaults.sandbox.docker.env` (ou `agents.list[].sandbox.docker.env` pour un agent unique)
- Intégrez les variables d'environnement dans votre image de sandbox personnalisée

Les champs globaux `env` et `skills.entries.<skill>.env/apiKey` s'appliquent uniquement à l'exécution sur la **machine hôte**.
