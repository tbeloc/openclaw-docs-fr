---
title: "Google (Gemini)"
summary: "Configuration de Google Gemini (clé API + OAuth, génération d'images, compréhension multimédia, recherche web)"
read_when:
  - Vous souhaitez utiliser les modèles Google Gemini avec OpenClaw
  - Vous avez besoin de la clé API ou du flux d'authentification OAuth
---

# Google (Gemini)

Le plugin Google fournit l'accès aux modèles Gemini via Google AI Studio, ainsi que
la génération d'images, la compréhension multimédia (image/audio/vidéo) et la recherche web via
Gemini Grounding.

- Fournisseur : `google`
- Authentification : `GEMINI_API_KEY` ou `GOOGLE_API_KEY`
- API : Google Gemini API
- Fournisseur alternatif : `google-gemini-cli` (OAuth)

## Démarrage rapide

1. Définissez la clé API :

```bash
openclaw onboard --auth-choice google-api-key
```

2. Définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "google/gemini-3.1-pro-preview" },
    },
  },
}
```

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice google-api-key \
  --gemini-api-key "$GEMINI_API_KEY"
```

## OAuth (Gemini CLI)

Un fournisseur alternatif `google-gemini-cli` utilise OAuth PKCE au lieu d'une clé API.
Il s'agit d'une intégration non officielle ; certains utilisateurs signalent des
restrictions de compte. À utiliser à vos risques et périls.

Variables d'environnement :

- `OPENCLAW_GEMINI_OAUTH_CLIENT_ID`
- `OPENCLAW_GEMINI_OAUTH_CLIENT_SECRET`

(Ou les variantes `GEMINI_CLI_*`.)

## Capacités

| Capacité               | Supportée         |
| ---------------------- | ----------------- |
| Complétions de chat    | Oui               |
| Génération d'images    | Oui               |
| Compréhension d'images | Oui               |
| Transcription audio    | Oui               |
| Compréhension vidéo    | Oui               |
| Recherche web (Grounding) | Oui            |
| Réflexion/raisonnement | Oui (Gemini 3.1+) |

## Note sur l'environnement

Si la Gateway s'exécute en tant que daemon (launchd/systemd), assurez-vous que `GEMINI_API_KEY`
est disponible pour ce processus (par exemple, dans `~/.openclaw/.env` ou via
`env.shellEnv`).
