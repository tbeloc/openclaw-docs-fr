---
summary: "Proxy communautaire pour exposer les identifiants d'abonnement Claude en tant que point de terminaison compatible OpenAI"
read_when:
  - You want to use Claude Max subscription with OpenAI-compatible tools
  - You want a local API server that wraps Claude Code CLI
  - You want to evaluate subscription-based vs API-key-based Anthropic access
title: "Claude Max API Proxy"
---

# Claude Max API Proxy

**claude-max-api-proxy** est un outil communautaire qui expose votre abonnement Claude Max/Pro en tant que point de terminaison API compatible OpenAI. Cela vous permet d'utiliser votre abonnement avec n'importe quel outil qui supporte le format API OpenAI.

<Warning>
Ce chemin est uniquement pour la compatibilité technique. Anthropic a bloqué certains
usages d'abonnement en dehors de Claude Code par le passé. Vous devez décider par
vous-même si vous souhaitez l'utiliser et vérifier les conditions actuelles d'Anthropic
avant de vous y fier.
</Warning>

## Pourquoi l'utiliser ?

| Approche                | Coût                                                | Idéal pour                                 |
| ----------------------- | --------------------------------------------------- | ------------------------------------------ |
| API Anthropic           | Paiement à l'usage (~15 $/M entrée, 75 $/M sortie pour Opus) | Applications en production, volume élevé               |
| Abonnement Claude Max | 200 $/mois forfaitaire                                     | Usage personnel, développement, usage illimité |

Si vous avez un abonnement Claude Max et souhaitez l'utiliser avec des outils compatibles OpenAI, ce proxy peut réduire les coûts pour certains flux de travail. Les clés API restent le chemin politique plus clair pour l'usage en production.

## Comment ça marche

```
Votre App → claude-max-api-proxy → Claude Code CLI → Anthropic (via abonnement)
     (format OpenAI)              (convertit le format)      (utilise votre connexion)
```

Le proxy :

1. Accepte les requêtes au format OpenAI à `http://localhost:3456/v1/chat/completions`
2. Les convertit en commandes Claude Code CLI
3. Retourne les réponses au format OpenAI (streaming supporté)

## Installation

```bash
# Nécessite Node.js 20+ et Claude Code CLI
npm install -g claude-max-api-proxy

# Vérifiez que Claude CLI est authentifié
claude --version
```

## Utilisation

### Démarrer le serveur

```bash
claude-max-api
# Le serveur s'exécute à http://localhost:3456
```

### Le tester

```bash
# Vérification de santé
curl http://localhost:3456/health

# Lister les modèles
curl http://localhost:3456/v1/models

# Complétion de chat
curl http://localhost:3456/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Avec OpenClaw

Vous pouvez pointer OpenClaw vers le proxy en tant que point de terminaison personnalisé compatible OpenAI :

```json5
{
  env: {
    OPENAI_API_KEY: "not-needed",
    OPENAI_BASE_URL: "http://localhost:3456/v1",
  },
  agents: {
    defaults: {
      model: { primary: "openai/claude-opus-4" },
    },
  },
}
```

## Modèles disponibles

| ID du modèle      | Correspond à    |
| ----------------- | --------------- |
| `claude-opus-4`   | Claude Opus 4   |
| `claude-sonnet-4` | Claude Sonnet 4 |
| `claude-haiku-4`  | Claude Haiku 4  |

## Démarrage automatique sur macOS

Créez un LaunchAgent pour exécuter le proxy automatiquement :

```bash
cat > ~/Library/LaunchAgents/com.claude-max-api.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.claude-max-api</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/node</string>
    <string>/usr/local/lib/node_modules/claude-max-api-proxy/dist/server/standalone.js</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/opt/homebrew/bin:~/.local/bin:/usr/bin:/bin</string>
  </dict>
</dict>
</plist>
EOF

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claude-max-api.plist
```

## Liens

- **npm:** [https://www.npmjs.com/package/claude-max-api-proxy](https://www.npmjs.com/package/claude-max-api-proxy)
- **GitHub:** [https://github.com/atalovesyou/claude-max-api-proxy](https://github.com/atalovesyou/claude-max-api-proxy)
- **Problèmes:** [https://github.com/atalovesyou/claude-max-api-proxy/issues](https://github.com/atalovesyou/claude-max-api-proxy/issues)

## Notes

- Ceci est un **outil communautaire**, non officiellement supporté par Anthropic ou OpenClaw
- Nécessite un abonnement Claude Max/Pro actif avec Claude Code CLI authentifié
- Le proxy s'exécute localement et n'envoie pas de données à des serveurs tiers
- Les réponses en streaming sont entièrement supportées

## Voir aussi

- [Fournisseur Anthropic](/providers/anthropic) - Intégration native OpenClaw avec Claude setup-token ou clés API
- [Fournisseur OpenAI](/providers/openai) - Pour les abonnements OpenAI/Codex
