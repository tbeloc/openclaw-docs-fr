---
read_when:
  - Mise à jour du comportement de retry du fournisseur ou des valeurs par défaut
  - Débogage des erreurs d'envoi du fournisseur ou des limites de débit
summary: Stratégie de retry pour les appels de fournisseur sortants
title: Stratégie de retry
x-i18n:
  generated_at: "2026-02-01T20:23:37Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 55bb261ff567f46ce447be9c0ee0c5b5e6d2776287d7662762656c14108dd607
  source_path: concepts/retry.md
  workflow: 14
---

# Stratégie de retry

## Objectifs

- Réessayer par requête HTTP, et non par processus multi-étapes.
- Maintenir l'ordre en réessayant uniquement l'étape actuelle.
- Éviter l'exécution répétée d'opérations non idempotentes.

## Valeurs par défaut

- Nombre de tentatives : 3
- Délai maximum : 30000 millisecondes
- Gigue : 0,1 (10 %)
- Valeurs par défaut du fournisseur :
  - Telegram délai minimum : 400 millisecondes
  - Discord délai minimum : 500 millisecondes

## Comportement

### Discord

- Réessayer uniquement en cas d'erreur de limite de débit (HTTP 429).
- Utiliser `retry_after` de Discord si disponible, sinon utiliser le backoff exponentiel.

### Telegram

- Réessayer en cas d'erreur transitoire (429, timeout, connexion/réinitialisation/fermeture, temporairement indisponible).
- Utiliser `retry_after` si disponible, sinon utiliser le backoff exponentiel.
- Les erreurs d'analyse Markdown ne sont pas réessayées ; basculer vers du texte brut.

## Configuration

Définir la stratégie de retry par fournisseur dans `~/.openclaw/openclaw.json` :

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

## Remarques

- Le retry s'applique par requête (envoi de message, téléchargement de média, réaction emoji, sondage, autocollant).
- Les processus composés ne réessaient pas les étapes déjà complétées.
