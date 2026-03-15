---
summary: "Utilisez le catalogue OpenCode Go avec la configuration OpenCode partagée"
read_when:
  - Vous voulez le catalogue OpenCode Go
  - Vous avez besoin des références du modèle runtime pour les modèles hébergés sur Go
title: "OpenCode Go"
---

# OpenCode Go

OpenCode Go est le catalogue Go dans [OpenCode](/fr/providers/opencode).
Il utilise la même `OPENCODE_API_KEY` que le catalogue Zen, mais conserve l'ID du
fournisseur runtime `opencode-go` pour que le routage en amont par modèle reste correct.

## Modèles supportés

- `opencode-go/kimi-k2.5`
- `opencode-go/glm-5`
- `opencode-go/minimax-m2.5`

## Configuration CLI

```bash
openclaw onboard --auth-choice opencode-go
# ou non-interactif
openclaw onboard --opencode-go-api-key "$OPENCODE_API_KEY"
```

## Extrait de configuration

```json5
{
  env: { OPENCODE_API_KEY: "YOUR_API_KEY_HERE" }, // pragma: allowlist secret
  agents: { defaults: { model: { primary: "opencode-go/kimi-k2.5" } } },
}
```

## Comportement du routage

OpenClaw gère automatiquement le routage par modèle lorsque la référence du modèle utilise `opencode-go/...`.

## Notes

- Utilisez [OpenCode](/fr/providers/opencode) pour l'intégration partagée et l'aperçu du catalogue.
- Les références runtime restent explicites : `opencode/...` pour Zen, `opencode-go/...` pour Go.
