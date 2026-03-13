---
read_when:
  - Vous devez effectuer des modifications structurées sur plusieurs fichiers
  - Vous souhaitez enregistrer ou déboguer des modifications basées sur des correctifs
summary: Appliquer des correctifs multi-fichiers à l'aide de l'outil apply_patch
title: Outil apply_patch
x-i18n:
  generated_at: "2026-02-01T21:39:24Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8cec2b4ee3afa9105fc3dd1bc28a338917df129afc634ac83620a3347c46bcec
  source_path: tools/apply-patch.md
  workflow: 15
---

# Outil apply_patch

Appliquez des modifications de fichiers à l'aide d'un format de correctif structuré. Ceci est idéal pour les modifications
multi-fichiers ou multi-segments, dans les scénarios où un seul appel `edit` serait fragile.

L'outil accepte une chaîne `input` contenant une ou plusieurs opérations de fichier :

```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

## Paramètres

- `input` (obligatoire) : contenu complet du correctif, incluant `*** Begin Patch` et `*** End Patch`.

## Instructions

- Les chemins sont résolus par rapport à la racine de l'espace de travail.
- Utilisez `*** Move to:` dans les segments `*** Update File:` pour renommer des fichiers.
- Utilisez le marqueur `*** End of File` si nécessaire pour les insertions uniquement à la fin du fichier.
- Fonctionnalité expérimentale, désactivée par défaut. Activez via `tools.exec.applyPatch.enabled`.
- Limité à OpenAI (y compris OpenAI Codex). Restriction optionnelle par modèle via
  `tools.exec.applyPatch.allowModels`.
- Configuration uniquement sous `tools.exec`.

## Exemple

```json
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```
