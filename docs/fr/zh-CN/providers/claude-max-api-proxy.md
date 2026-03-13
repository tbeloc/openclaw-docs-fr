---
read_when:
  - Vous souhaitez utiliser votre abonnement Claude Max avec des outils compatibles OpenAI
  - Vous souhaitez un serveur API local encapsulant Claude Code CLI
  - Vous souhaitez économiser des frais en utilisant un abonnement plutôt qu'une clé API
summary: Utiliser votre abonnement Claude Max/Pro comme point de terminaison API compatible OpenAI
title: Proxy API Claude Max
x-i18n:
  generated_at: "2026-02-01T21:34:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 63b61096b96b720c6d0c317520852db65d72ca8279b3868f35e8387fe3b6ce41
  source_path: providers/claude-max-api-proxy.md
  workflow: 15
---

# Proxy API Claude Max

**claude-max-api-proxy** est un outil communautaire qui expose votre abonnement Claude Max/Pro comme point de terminaison API compatible OpenAI. Cela vous permet d'utiliser votre abonnement avec n'importe quel outil prenant en charge le format API OpenAI.

## Pourquoi l'utiliser ?

| Méthode         | Coût                                                  | Cas d'usage                          |
| --------------- | ----------------------------------------------------- | ------------------------------------ |
| API Anthropic   | Facturation à l'usage (Opus ~$15/M entrée, $75/M sortie) | Applications de production, trafic élevé |
| Abonnement Claude Max | $200 par mois forfaitaire                      | Utilisation personnelle, développement, usage illimité |

Si vous avez un abonnement Claude Max et souhaitez l'utiliser avec des outils compatibles OpenAI, ce proxy peut vous faire économiser considérablement.

## Fonctionnement

```
Votre application → claude-max-api-proxy → Claude Code CLI → Anthropic (via abonnement)
     (format OpenAI)              (conversion de format)           (utilise vos identifiants)
```

Le proxy :

1. Accepte les requêtes au format OpenAI sur `http://localhost:3456/v1/chat/completions`
2. Les convertit en commandes Claude Code CLI
3. Retourne les réponses au format OpenAI (avec support du streaming)

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
# Le serveur s'exécute sur http://localhost:3456
```

### Tests

```bash
# Vérification de santé
curl http://localhost:3456/health

# Lister les modèles
curl http://localhost:3456/v1/models

# Complétions de chat
curl http://localhost:3456/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Utilisation avec OpenClaw

Vous pouvez pointer OpenClaw vers ce proxy comme point de terminaison personnalisé compatible OpenAI :

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

| ID du modèle      | Modèle correspondant |
| ----------------- | ------------------- |
| `claude-opus-4`   | Claude Opus 4       |
| `claude-sonnet-4` | Claude Sonnet 4     |
| `claude-haiku-4`  | Claude Haiku 4      |

## Lancement automatique sur macOS

Créez un LaunchAgent pour exécuter automatiquement le proxy :

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

- **npm:** https://www.npmjs.com/package/claude-max-api-proxy
- **GitHub:** https://github.com/atalovesyou/claude-max-api-proxy
- **Issues:** https://github.com/atalovesyou/claude-max-api-proxy/issues

## Remarques

- Ceci est un **outil communautaire**, non officiellement supporté par Anthropic ou OpenClaw
- Nécessite un abonnement Claude Max/Pro valide et Claude Code CLI authentifié
- Le proxy s'exécute localement et n'envoie pas de données à des serveurs tiers
- Support complet des réponses en streaming

## Voir aussi

- [Fournisseur Anthropic](/providers/anthropic) - Intégration native d'OpenClaw avec Claude, utilisant setup-token ou clé API
- [Fournisseur OpenAI](/providers/openai) - Pour les abonnements OpenAI/Codex
