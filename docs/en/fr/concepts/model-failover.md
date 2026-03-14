---
summary: "Comment OpenClaw fait tourner les profils d'authentification et bascule entre les modèles"
read_when:
  - Diagnosing auth profile rotation, cooldowns, or model fallback behavior
  - Updating failover rules for auth profiles or models
title: "Basculement de modèle"
---

# Basculement de modèle

OpenClaw gère les défaillances en deux étapes :

1. **Rotation des profils d'authentification** au sein du fournisseur actuel.
2. **Basculement de modèle** vers le modèle suivant dans `agents.defaults.model.fallbacks`.

Ce document explique les règles d'exécution et les données qui les soutiennent.

## Stockage d'authentification (clés + OAuth)

OpenClaw utilise des **profils d'authentification** pour les clés API et les jetons OAuth.

- Les secrets se trouvent dans `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (hérité : `~/.openclaw/agent/auth-profiles.json`).
- La configuration `auth.profiles` / `auth.order` est **métadonnées + routage uniquement** (pas de secrets).
- Fichier OAuth d'importation hérité : `~/.openclaw/credentials/oauth.json` (importé dans `auth-profiles.json` à la première utilisation).

Plus de détails : [/concepts/oauth](/concepts/oauth)

Types d'identifiants :

- `type: "api_key"` → `{ provider, key }`
- `type: "oauth"` → `{ provider, access, refresh, expires, email? }` (+ `projectId`/`enterpriseUrl` pour certains fournisseurs)

## ID de profil

Les connexions OAuth créent des profils distincts pour que plusieurs comptes puissent coexister.

- Par défaut : `provider:default` quand aucun email n'est disponible.
- OAuth avec email : `provider:<email>` (par exemple `google-antigravity:user@gmail.com`).

Les profils se trouvent dans `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` sous `profiles`.

## Ordre de rotation

Quand un fournisseur a plusieurs profils, OpenClaw choisit un ordre comme ceci :

1. **Configuration explicite** : `auth.order[provider]` (si défini).
2. **Profils configurés** : `auth.profiles` filtrés par fournisseur.
3. **Profils stockés** : entrées dans `auth-profiles.json` pour le fournisseur.

Si aucun ordre explicite n'est configuré, OpenClaw utilise un ordre round-robin :

- **Clé primaire :** type de profil (**OAuth avant les clés API**).
- **Clé secondaire :** `usageStats.lastUsed` (le plus ancien en premier, dans chaque type).
- **Les profils en cooldown/désactivés** sont déplacés à la fin, ordonnés par expiration la plus proche.

### Adhérence de session (cache-friendly)

OpenClaw **épingle le profil d'authentification choisi par session** pour garder les caches du fournisseur chauds.
Il ne fait **pas** de rotation à chaque requête. Le profil épinglé est réutilisé jusqu'à :

- la réinitialisation de la session (`/new` / `/reset`)
- la fin d'une compaction (le compteur de compaction s'incrémente)
- le profil est en cooldown/désactivé

La sélection manuelle via `/model …@<profileId>` définit un **remplacement utilisateur** pour cette session
et n'est pas auto-rotaté jusqu'au démarrage d'une nouvelle session.

Les profils auto-épinglés (sélectionnés par le routeur de session) sont traités comme une **préférence** :
ils sont essayés en premier, mais OpenClaw peut faire tourner vers un autre profil en cas de limites de débit/timeouts.
Les profils épinglés par l'utilisateur restent verrouillés sur ce profil ; s'il échoue et que les basculements de modèle
sont configurés, OpenClaw passe au modèle suivant au lieu de changer de profils.

### Pourquoi OAuth peut sembler "perdu"

Si vous avez à la fois un profil OAuth et un profil de clé API pour le même fournisseur, le round-robin peut basculer entre eux à travers les messages sauf s'il est épinglé. Pour forcer un seul profil :

- Épinglez avec `auth.order[provider] = ["provider:profileId"]`, ou
- Utilisez un remplacement par session via `/model …` avec un remplacement de profil (si supporté par votre UI/surface de chat).

## Cooldowns

Quand un profil échoue en raison d'erreurs d'authentification/limite de débit (ou un timeout qui ressemble
à une limitation de débit), OpenClaw le marque en cooldown et passe au profil suivant.
Les erreurs de format/requête invalide (par exemple les échecs de validation d'ID d'appel d'outil Cloud Code Assist) sont traitées comme dignes de basculement et utilisent les mêmes cooldowns.
Les erreurs de raison d'arrêt compatibles avec OpenAI comme `Unhandled stop reason: error`,
`stop reason: error`, et `reason: error` sont classées comme signaux de timeout/basculement.

Les cooldowns utilisent une augmentation exponentielle :

- 1 minute
- 5 minutes
- 25 minutes
- 1 heure (plafond)

L'état est stocké dans `auth-profiles.json` sous `usageStats` :

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

## Désactivations de facturation

Les défaillances de facturation/crédit (par exemple "crédits insuffisants" / "solde de crédit trop bas") sont traitées comme dignes de basculement, mais elles ne sont généralement pas transitoires. Au lieu d'un court cooldown, OpenClaw marque le profil comme **désactivé** (avec un backoff plus long) et fait tourner vers le profil/fournisseur suivant.

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

- Le backoff de facturation commence à **5 heures**, double par défaillance de facturation, et plafonne à **24 heures**.
- Les compteurs de backoff se réinitialisent si le profil n'a pas échoué pendant **24 heures** (configurable).

## Basculement de modèle

Si tous les profils d'un fournisseur échouent, OpenClaw passe au modèle suivant dans
`agents.defaults.model.fallbacks`. Cela s'applique aux défaillances d'authentification, aux limites de débit, et aux
timeouts qui ont épuisé la rotation des profils (les autres erreurs ne font pas avancer le basculement).

Quand une exécution démarre avec un remplacement de modèle (hooks ou CLI), les basculements se terminent toujours à
`agents.defaults.model.primary` après avoir essayé les basculements configurés.

## Configuration associée

Voir [Configuration de la passerelle](/gateway/configuration) pour :

- `auth.profiles` / `auth.order`
- `auth.cooldowns.billingBackoffHours` / `auth.cooldowns.billingBackoffHoursByProvider`
- `auth.cooldowns.billingMaxHours` / `auth.cooldowns.failureWindowHours`
- `agents.defaults.model.primary` / `agents.defaults.model.fallbacks`
- routage `agents.defaults.imageModel`

Voir [Modèles](/concepts/models) pour l'aperçu plus large de la sélection et du basculement de modèle.
