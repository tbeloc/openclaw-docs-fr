---
summary: "Politique de retry pour les appels de fournisseurs sortants"
read_when:
  - Updating provider retry behavior or defaults
  - Debugging provider send errors or rate limits
title: "Politique de Retry"
---

# Politique de retry

## Objectifs

- Retry par requête HTTP, et non par flux multi-étapes.
- Préserver l'ordre en effectuant un retry uniquement de l'étape actuelle.
- Éviter de dupliquer les opérations non-idempotentes.

## Valeurs par défaut

- Tentatives : 3
- Délai maximum : 30000 ms
- Jitter : 0.1 (10 pour cent)
- Valeurs par défaut du fournisseur :
  - Délai minimum Telegram : 400 ms
  - Délai minimum Discord : 500 ms

## Comportement

### Discord

- Effectue un retry uniquement sur les erreurs de limite de débit (HTTP 429).
- Utilise `retry_after` de Discord si disponible, sinon backoff exponentiel.

### Telegram

- Effectue un retry sur les erreurs transitoires (429, timeout, connect/reset/closed, temporarily unavailable).
- Utilise `retry_after` si disponible, sinon backoff exponentiel.
- Les erreurs d'analyse Markdown ne sont pas retentées ; elles reviennent au texte brut.

## Configuration

Définissez la politique de retry par fournisseur dans `~/.openclaw/openclaw.json` :

```json5
{
  channels: {
    telegram: {
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
    discord: {
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

## Notes

- Les retries s'appliquent par requête (envoi de message, téléchargement de média, réaction, sondage, autocollant).
- Les flux composites ne retentent pas les étapes complétées.
