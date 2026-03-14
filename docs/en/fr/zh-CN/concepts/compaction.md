---
read_when:
  - Vous voulez comprendre la compression automatique et /compact
  - Vous déboguez des problèmes de sessions longues qui touchent la limite de contexte
summary: Fenêtre de contexte + compression : comment OpenClaw maintient les sessions dans les limites du modèle
title: Compression
x-i18n:
  generated_at: "2026-02-01T20:22:17Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e1d6791f2902044b5798ebf9320a7d055d37211eff4be03caa35d7e328ae803c
  source_path: concepts/compaction.md
  workflow: 14
---

# Fenêtre de contexte et compression

Chaque modèle dispose d'une **fenêtre de contexte** (nombre maximum de tokens visibles). Les conversations longues accumulent des messages et des résultats d'outils ; une fois que l'espace de la fenêtre devient limité, OpenClaw **compresse** l'historique antérieur pour rester dans les limites.

## Qu'est-ce que la compression

La compression **résume les conversations antérieures** en une seule entrée de résumé compact, tout en conservant les messages récents inchangés. Le résumé est stocké dans l'historique de la session, donc les requêtes suivantes utilisent :

- Le résumé compressé
- Les messages récents après le point de compression

La compression est **persistante** dans l'historique JSONL de la session.

## Configuration

Pour les paramètres `agents.defaults.compaction`, consultez [Configuration et modes de compression](/concepts/compaction).

## Compression automatique (activée par défaut)

Lorsqu'une session approche ou dépasse la fenêtre de contexte du modèle, OpenClaw déclenche une compression automatique et peut réessayer la requête d'origine avec le contexte compressé.

Vous verrez :

- `🧹 Auto-compaction complete` en mode verbeux
- `/status` affiche `🧹 Compactions: <count>`

Avant la compression, OpenClaw peut exécuter un cycle de **vidage de mémoire silencieux** pour écrire les notes persistantes sur le disque. Pour plus de détails et la configuration, consultez [Mémoire](/concepts/memory).

## Compression manuelle

Utilisez `/compact` (optionnellement avec une instruction) pour forcer une compression :

```
/compact Focus on decisions and open questions
```

## Source de la fenêtre de contexte

La fenêtre de contexte varie selon le modèle. OpenClaw utilise les définitions de modèle du répertoire des fournisseurs configurés pour déterminer la limite.

## Compression et élagage

- **Compression** : résume et **persiste** dans JSONL.
- **Élagage de session** : coupe uniquement les anciens **résultats d'outils**, **en mémoire** par requête.

Pour plus de détails sur l'élagage, consultez [/concepts/session-pruning](/concepts/session-pruning).

## Conseils

- Utilisez `/compact` lorsque la session semble obsolète ou que le contexte est encombré.
- Les grandes sorties d'outils sont tronquées ; l'élagage peut réduire davantage l'accumulation de résultats d'outils.
- Si vous avez besoin d'un nouveau départ, `/new` ou `/reset` lance un nouvel ID de session.
