---
read_when:
  - Diagnostiquer la rotation des profils d'authentification, les temps de refroidissement ou le comportement de secours du modèle
  - Mettre à jour les règles de basculement des profils d'authentification ou des modèles
summary: Comment OpenClaw fait tourner les profils d'authentification et bascule entre les modèles
title: Basculement du modèle
x-i18n:
  generated_at: "2026-02-03T07:46:17Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: eab7c0633824d941cf0d6ce4294f0bc8747fbba2ce93650e9643eca327cd04a9
  source_path: concepts/model-failover.md
  workflow: 15
---

# Basculement du modèle

OpenClaw gère les défaillances en deux étapes :

1. **Rotation des profils d'authentification** au sein du fournisseur actuel.
2. **Secours du modèle** vers le modèle suivant dans `agents.defaults.model.fallbacks`.

Ce document explique les règles d'exécution et les données qui les sous-tendent.

## Stockage d'authentification (clés + OAuth)

OpenClaw utilise des **profils d'authentification** pour les clés API et les jetons OAuth.

- Les clés sont stockées dans `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (hérité : `~/.openclaw/agent/auth-profiles.json`).
- La configuration `auth.profiles` / `auth.order` est **utilisée uniquement pour les métadonnées et le routage** (sans clés).
- L'héritage importe uniquement les fichiers OAuth : `~/.openclaw/credentials/oauth.json` (importés dans `auth-profiles.json` à la première utilisation).

Pour plus de détails : [/concepts/oauth](/concepts/oauth)

Types de credentials :

- `type: "api_key"` → `{ provider, key }`
- `type: "oauth"` → `{ provider, access, refresh, expires, email? }` (certains fournisseurs ont aussi `projectId`/`enterpriseUrl`)

## ID de profil

Les connexions OAuth créent des profils distincts afin que plusieurs comptes puissent coexister.

- Par défaut : `provider:default` quand aucun email n'est disponible.
- OAuth avec email : `provider:<email>` (par exemple `google-antigravity:user@gmail.com`).

Les profils sont stockés sous `profiles` dans `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`.

## Ordre de rotation

Quand un fournisseur a plusieurs profils, OpenClaw en choisit un selon cet ordre :

1. **Configuration explicite** : `auth.order[provider]` (si défini).
2. **Profils configurés** : `auth.profiles` filtrés par fournisseur.
3. **Profils stockés** : entrées pour ce fournisseur dans `auth-profiles.json`.

Si aucun ordre explicite n'est configuré, OpenClaw utilise l'ordre de rotation :

- **Clé primaire :** type de profil (**OAuth avant les clés API**).
- **Clé secondaire :** `usageStats.lastUsed` (le plus ancien de chaque type en priorité).
- **Les profils en refroidissement/désactivés** sont déplacés à la fin, triés par heure d'expiration la plus proche.

### Adhérence de session (cache-friendly)

OpenClaw **fixe le profil d'authentification sélectionné pour chaque session** pour maintenir le cache du fournisseur chaud. Il **ne fait pas** de rotation à chaque requête. Le profil fixé est réutilisé jusqu'à :

- La session est réinitialisée (`/new` / `/reset`)
- La compression est terminée (le compteur de compression s'incrémente)
- Le profil est en refroidissement/désactivé

La sélection manuelle via `/model …@<profileId>` définit un **remplacement utilisateur** pour cette session, qui ne sera pas automatiquement roté jusqu'au début d'une nouvelle session.

Les profils fixés automatiquement (sélectionnés par le routeur de session) sont considérés comme des **préférences** : ils sont essayés en priorité, mais OpenClaw peut basculer vers un autre profil en cas de limite de débit/timeout. Les profils fixés par l'utilisateur sont verrouillés sur ce profil ; s'ils échouent et qu'un secours de modèle est configuré, OpenClaw passe au modèle suivant plutôt que de changer de profil.

### Pourquoi OAuth peut sembler "manquant"

Si vous avez à la fois un profil OAuth et un profil de clé API pour le même fournisseur, la rotation peut les basculer entre les messages à moins qu'ils ne soient fixés. Pour forcer un seul profil :

- Utilisez `auth.order[provider] = ["provider:profileId"]` pour fixer, ou
- Utilisez un remplacement par session via `/model …` et spécifiez un remplacement de profil (quand votre UI/interface de chat le supporte).

## Temps de refroidissement

Quand un profil échoue en raison d'erreurs d'authentification/limite de débit (ou de timeouts qui ressemblent à une limite de débit), OpenClaw le marque comme en refroidissement et passe au profil suivant. Les erreurs de format/requête invalide (par exemple, l'échec de la validation de l'ID d'appel d'outil Cloud Code Assist) sont considérées comme dignes d'un basculement, utilisant le même temps de refroidissement.

Le temps de refroidissement utilise un backoff exponentiel :

- 1 minute
- 5 minutes
- 25 minutes
- 1 heure (limite)

L'état est stocké sous `usageStats` dans `auth-profiles.json` :

```json
{
  "usageStats": {
    "provider:profile": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

## Désactivation de facturation

Les échecs de facturation/crédit (par exemple "insufficient credits"/"credit balance too low") sont considérés comme dignes d'un basculement, mais ils ne sont généralement pas temporaires. Au lieu d'utiliser un court temps de refroidissement, OpenClaw marque le profil comme **désactivé** (utilisant un temps de backoff plus long) et bascule vers le profil/fournisseur suivant.

L'état est stocké dans `auth-profiles.json` :

```json
{
  "usageStats": {
    "provider:profile": {
      "disabledUntil": 1736178000000,
      "disabledReason": "billing"
    }
  }
}
```

Valeurs par défaut :

- Le backoff de facturation commence à **5 heures**, doublant à chaque échec de facturation, avec une limite de **24 heures**.
- Si un profil n'a pas échoué dans les **24 heures**, le compteur de backoff est réinitialisé (configurable).

## Secours du modèle

Si tous les profils d'un fournisseur échouent, OpenClaw passe au modèle suivant dans `agents.defaults.model.fallbacks`. Cela s'applique aux échecs d'authentification, aux limites de débit et aux timeouts après épuisement de la rotation des profils (les autres erreurs ne font pas avancer le secours).

Quand une exécution commence avec un remplacement de modèle (hook ou CLI), le secours se termine toujours à `agents.defaults.model.primary` après avoir essayé tous les secours configurés.

## Configuration associée

Consultez [Configuration de la passerelle](/gateway/configuration) pour :

- `auth.profiles` / `auth.order`
- `auth.cooldowns.billingBackoffHours` / `auth.cooldowns.billingBackoffHoursByProvider`
- `auth.cooldowns.billingMaxHours` / `auth.cooldowns.failureWindowHours`
- `agents.defaults.model.primary` / `agents.defaults.model.fallbacks`
- Routage `agents.defaults.imageModel`

Consultez [Modèles](/concepts/models) pour un aperçu plus large de la sélection et du secours des modèles.
