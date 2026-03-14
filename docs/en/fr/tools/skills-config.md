---
summary: "Schéma de configuration des compétences et exemples"
read_when:
  - Adding or modifying skills config
  - Adjusting bundled allowlist or install behavior
title: "Configuration des compétences"
---

# Configuration des compétences

Toute la configuration liée aux compétences se trouve sous `skills` dans `~/.openclaw/openclaw.json`.

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
      nodeManager: "npm", // npm | pnpm | yarn | bun (Gateway runtime still Node; bun not recommended)
    },
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
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

- `allowBundled` : liste d'autorisation optionnelle pour les compétences **intégrées** uniquement. Lorsqu'elle est définie, seules les compétences intégrées de la liste sont éligibles (les compétences gérées/workspace ne sont pas affectées).
- `load.extraDirs` : répertoires de compétences supplémentaires à analyser (priorité la plus basse).
- `load.watch` : surveiller les dossiers de compétences et actualiser l'instantané des compétences (par défaut : true).
- `load.watchDebounceMs` : délai d'attente pour les événements du moniteur de compétences en millisecondes (par défaut : 250).
- `install.preferBrew` : préférer les installateurs brew lorsqu'ils sont disponibles (par défaut : true).
- `install.nodeManager` : préférence d'installateur node (`npm` | `pnpm` | `yarn` | `bun`, par défaut : npm).
  Cela affecte uniquement les **installations de compétences** ; le runtime Gateway doit toujours être Node
  (Bun non recommandé pour WhatsApp/Telegram).
- `entries.<skillKey>` : remplacements par compétence.

Champs par compétence :

- `enabled` : définir à `false` pour désactiver une compétence même si elle est intégrée/installée.
- `env` : variables d'environnement injectées pour l'exécution de l'agent (uniquement si elles ne sont pas déjà définies).
- `apiKey` : commodité optionnelle pour les compétences qui déclarent une variable d'environnement principale.
  Supporte une chaîne en texte brut ou un objet SecretRef (`{ source, provider, id }`).

## Remarques

- Les clés sous `entries` correspondent au nom de la compétence par défaut. Si une compétence définit
  `metadata.openclaw.skillKey`, utilisez cette clé à la place.
- Les modifications apportées aux compétences sont prises en compte au prochain tour de l'agent lorsque le moniteur est activé.

### Compétences en sandbox + variables d'environnement

Lorsqu'une session est **en sandbox**, les processus de compétences s'exécutent à l'intérieur de Docker. Le sandbox
n'hérite **pas** du `process.env` de l'hôte.

Utilisez l'une des options suivantes :

- `agents.defaults.sandbox.docker.env` (ou `agents.list[].sandbox.docker.env` par agent)
- intégrer l'env dans votre image de sandbox personnalisée

Les champs `env` et `skills.entries.<skill>.env/apiKey` globaux s'appliquent uniquement aux exécutions **hôte**.
