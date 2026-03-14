---
read_when:
  - Vous souhaitez accéder aux modèles via OpenCode Zen
  - Vous souhaitez une liste de modèles sélectionnés adaptée à la programmation
summary: Utiliser OpenCode Zen (modèles sélectionnés) dans OpenClaw
title: OpenCode Zen
x-i18n:
  generated_at: "2026-02-01T21:35:16Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1390f9803a3cac48cb40694dd69267e3ddccd203a4ce8babda3198b926b5f6a3
  source_path: providers/opencode.md
  workflow: 15
---

# OpenCode Zen

OpenCode Zen est un ensemble de **modèles sélectionnés** recommandés par l'équipe OpenCode, conçus pour les agents de programmation. Il s'agit d'un chemin d'accès aux modèles hébergés optionnel, utilisant une clé API et le fournisseur `opencode`. Zen est actuellement en phase bêta.

## Configuration CLI

```bash
openclaw onboard --auth-choice opencode-zen
# ou non-interactif
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

## Extrait de configuration

```json5
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-5" } } },
}
```

## Remarques

- `OPENCODE_ZEN_API_KEY` est également supporté.
- Vous devez vous connecter à Zen, ajouter les informations de facturation, puis copier votre clé API.
- OpenCode Zen est facturé à la demande ; consultez la console OpenCode pour plus de détails.
