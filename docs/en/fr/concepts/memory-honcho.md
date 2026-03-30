---
title: "Mémoire Honcho"
summary: "Mémoire multi-sessions native IA via le plugin Honcho"
read_when:
  - You want persistent memory that works across sessions and channels
  - You want AI-powered recall and user modeling
---

# Mémoire Honcho

[Honcho](https://honcho.dev) ajoute une mémoire native IA à OpenClaw. Il persiste
les conversations vers un service dédié et construit des modèles utilisateur et agent au fil du temps,
donnant à votre agent un contexte multi-sessions qui va au-delà des fichiers Markdown de l'espace de travail.

## Ce qu'il fournit

- **Mémoire multi-sessions** -- les conversations sont persistées après chaque tour, donc
  le contexte se maintient à travers les réinitialisations de session, la compaction et les changements de canal.
- **Modélisation utilisateur** -- Honcho maintient un profil pour chaque utilisateur (préférences,
  faits, style de communication) et pour l'agent (personnalité, comportements appris).
- **Recherche sémantique** -- recherche sur les observations des conversations passées, pas
  seulement la session actuelle.
- **Sensibilisation multi-agents** -- les agents parents suivent automatiquement les
  sous-agents générés, avec les parents ajoutés comme observateurs dans les sessions enfants.

## Outils disponibles

Honcho enregistre les outils que l'agent peut utiliser pendant la conversation :

**Récupération de données (rapide, sans appel LLM) :**

| Outil                       | Ce qu'il fait                                          |
| --------------------------- | ------------------------------------------------------ |
| `honcho_context`            | Représentation complète de l'utilisateur entre sessions |
| `honcho_search_conclusions` | Recherche sémantique sur les conclusions stockées      |
| `honcho_search_messages`    | Trouver des messages entre sessions (filtrer par expéditeur, date) |
| `honcho_session`            | Historique et résumé de la session actuelle            |

**Q&A (alimenté par LLM) :**

| Outil        | Ce qu'il fait                                                              |
| ------------ | ------------------------------------------------------------------------- |
| `honcho_ask` | Poser des questions sur l'utilisateur. `depth='quick'` pour les faits, `'thorough'` pour la synthèse |

## Démarrage rapide

Installez le plugin et exécutez la configuration :

```bash
openclaw plugins install @honcho-ai/openclaw-honcho
openclaw honcho setup
openclaw gateway --force
```

La commande setup vous demande vos identifiants API, écrit la configuration et
migre optionnellement les fichiers de mémoire d'espace de travail existants.

<Info>
Honcho peut s'exécuter entièrement localement (auto-hébergé) ou via l'API gérée à
`api.honcho.dev`. Aucune dépendance externe n'est requise pour l'option auto-hébergée.
</Info>

## Configuration

Les paramètres se trouvent sous `plugins.entries["openclaw-honcho"].config` :

```json5
{
  plugins: {
    entries: {
      "openclaw-honcho": {
        config: {
          apiKey: "your-api-key", // omit for self-hosted
          workspaceId: "openclaw", // memory isolation
          baseUrl: "https://api.honcho.dev",
        },
      },
    },
  },
}
```

Pour les instances auto-hébergées, pointez `baseUrl` vers votre serveur local (par exemple
`http://localhost:8000`) et omettez la clé API.

## Migration de la mémoire existante

Si vous avez des fichiers de mémoire d'espace de travail existants (`USER.md`, `MEMORY.md`,
`IDENTITY.md`, `memory/`, `canvas/`), `openclaw honcho setup` les détecte et
propose de les migrer.

<Info>
La migration est non-destructive -- les fichiers sont téléchargés vers Honcho. Les originaux ne sont
jamais supprimés ou déplacés.
</Info>

## Comment ça marche

Après chaque tour IA, la conversation est persistée vers Honcho. Les messages utilisateur et
agent sont observés, permettant à Honcho de construire et affiner ses modèles au fil du temps.

Pendant la conversation, les outils Honcho interrogent le service dans la phase `before_prompt_build`,
injectant le contexte pertinent avant que le modèle ne voie l'invite. Cela garantit
des limites de tour précises et un rappel pertinent.

## Honcho vs mémoire intégrée

|                   | Intégrée / QMD                | Honcho                              |
| ----------------- | ---------------------------- | ----------------------------------- |
| **Stockage**      | Fichiers Markdown d'espace de travail | Service dédié (local ou hébergé) |
| **Multi-sessions** | Via fichiers de mémoire      | Automatique, intégré                |
| **Modélisation utilisateur** | Manuel (écrire dans MEMORY.md) | Profils automatiques                |
| **Recherche**     | Vecteur + mot-clé (hybride)  | Sémantique sur observations         |
| **Multi-agents**  | Non suivi                    | Sensibilisation parent/enfant       |
| **Dépendances**   | Aucune (intégrée) ou binaire QMD | Installation du plugin              |

Honcho et le système de mémoire intégré peuvent fonctionner ensemble. Quand QMD est configuré,
des outils supplémentaires deviennent disponibles pour rechercher les fichiers Markdown locaux aux côtés de la mémoire multi-sessions de Honcho.

## Commandes CLI

```bash
openclaw honcho setup                        # Configure API key and migrate files
openclaw honcho status                       # Check connection status
openclaw honcho ask <question>               # Query Honcho about the user
openclaw honcho search <query> [-k N] [-d D] # Semantic search over memory
```

## Lectures complémentaires

- [Code source du plugin](https://github.com/plastic-labs/openclaw-honcho)
- [Documentation Honcho](https://docs.honcho.dev)
- [Guide d'intégration Honcho OpenClaw](https://docs.honcho.dev/v3/guides/integrations/openclaw)
- [Mémoire](/fr/concepts/memory) -- Aperçu de la mémoire OpenClaw
- [Moteurs de contexte](/fr/concepts/context-engine) -- comment fonctionnent les moteurs de contexte des plugins
