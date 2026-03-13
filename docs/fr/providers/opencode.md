---
summary: "Utilisez les catalogues OpenCode Zen et Go avec OpenClaw"
read_when:
  - Vous voulez accéder aux modèles hébergés par OpenCode
  - Vous voulez choisir entre les catalogues Zen et Go
title: "OpenCode"
---

# OpenCode

OpenCode expose deux catalogues hébergés dans OpenClaw :

- `opencode/...` pour le catalogue **Zen**
- `opencode-go/...` pour le catalogue **Go**

Les deux catalogues utilisent la même clé API OpenCode. OpenClaw maintient les identifiants de fournisseur d'exécution séparés pour que le routage en amont par modèle reste correct, mais l'intégration et la documentation les traitent comme une seule configuration OpenCode.

## Configuration CLI

### Catalogue Zen

```bash
openclaw onboard --auth-choice opencode-zen
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

### Catalogue Go

```bash
openclaw onboard --auth-choice opencode-go
openclaw onboard --opencode-go-api-key "$OPENCODE_API_KEY"
```

## Extrait de configuration

```json5
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

## Catalogues

### Zen

- Fournisseur d'exécution : `opencode`
- Modèles d'exemple : `opencode/claude-opus-4-6`, `opencode/gpt-5.2`, `opencode/gemini-3-pro`
- À utiliser quand vous voulez le proxy multi-modèle OpenCode organisé

### Go

- Fournisseur d'exécution : `opencode-go`
- Modèles d'exemple : `opencode-go/kimi-k2.5`, `opencode-go/glm-5`, `opencode-go/minimax-m2.5`
- À utiliser quand vous voulez la gamme Kimi/GLM/MiniMax hébergée par OpenCode

## Remarques

- `OPENCODE_ZEN_API_KEY` est également supportée.
- L'entrée d'une clé OpenCode lors de l'intégration stocke les identifiants pour les deux fournisseurs d'exécution.
- Vous vous connectez à OpenCode, ajoutez les détails de facturation et copiez votre clé API.
- La facturation et la disponibilité des catalogues sont gérées depuis le tableau de bord OpenCode.
