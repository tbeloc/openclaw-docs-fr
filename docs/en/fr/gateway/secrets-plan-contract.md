```markdown
---
summary: "Contrat pour les plans `secrets apply` : validation des cibles, correspondance des chemins et portée des cibles `auth-profiles.json`"
read_when:
  - Génération ou révision des plans `openclaw secrets apply`
  - Débogage des erreurs `Invalid plan target path`
  - Compréhension du comportement de validation des types de cibles et des chemins
title: "Contrat du plan Secrets Apply"
---

# Contrat du plan secrets apply

Cette page définit le contrat strict appliqué par `openclaw secrets apply`.

Si une cible ne correspond pas à ces règles, l'application échoue avant de modifier la configuration.

## Forme du fichier de plan

`openclaw secrets apply --from <plan.json>` attend un tableau `targets` de cibles de plan :

```json5
{
  version: 1,
  protocolVersion: 1,
  targets: [
    {
      type: "models.providers.apiKey",
      path: "models.providers.openai.apiKey",
      pathSegments: ["models", "providers", "openai", "apiKey"],
      providerId: "openai",
      ref: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
    },
    {
      type: "auth-profiles.api_key.key",
      path: "profiles.openai:default.key",
      pathSegments: ["profiles", "openai:default", "key"],
      agentId: "main",
      ref: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
    },
  ],
}
```

## Portée des cibles supportées

Les cibles de plan sont acceptées pour les chemins d'identifiants supportés dans :

- [SecretRef Credential Surface](/reference/secretref-credential-surface)

## Comportement du type de cible

Règle générale :

- `target.type` doit être reconnu et doit correspondre à la forme normalisée de `target.path`.

Les alias de compatibilité restent acceptés pour les plans existants :

- `models.providers.apiKey`
- `skills.entries.apiKey`
- `channels.googlechat.serviceAccount`

## Règles de validation des chemins

Chaque cible est validée avec tous les éléments suivants :

- `type` doit être un type de cible reconnu.
- `path` doit être un chemin en points non vide.
- `pathSegments` peut être omis. S'il est fourni, il doit se normaliser exactement au même chemin que `path`.
- Les segments interdits sont rejetés : `__proto__`, `prototype`, `constructor`.
- Le chemin normalisé doit correspondre à la forme de chemin enregistrée pour le type de cible.
- Si `providerId` ou `accountId` est défini, il doit correspondre à l'id encodé dans le chemin.
- Les cibles `auth-profiles.json` nécessitent `agentId`.
- Lors de la création d'un nouveau mappage `auth-profiles.json`, incluez `authProfileProvider`.

## Comportement en cas d'échec

Si une cible échoue la validation, l'application se termine avec une erreur comme :

```text
Invalid plan target path for models.providers.apiKey: models.providers.openai.baseUrl
```

Aucune écriture n'est validée pour un plan invalide.

## Notes sur la portée du runtime et de l'audit

- Les entrées `auth-profiles.json` en référence uniquement (`keyRef`/`tokenRef`) sont incluses dans la résolution du runtime et la couverture d'audit.
- `secrets apply` écrit les cibles `openclaw.json` supportées, les cibles `auth-profiles.json` supportées et les cibles de suppression optionnelles.

## Vérifications de l'opérateur

```bash
# Valider le plan sans écritures
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run

# Puis appliquer pour de vrai
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
```

Si l'application échoue avec un message de chemin de cible invalide, régénérez le plan avec `openclaw secrets configure` ou corrigez le chemin de la cible vers une forme supportée ci-dessus.

## Documentation connexe

- [Secrets Management](/gateway/secrets)
- [CLI `secrets`](/cli/secrets)
- [SecretRef Credential Surface](/reference/secretref-credential-surface)
- [Configuration Reference](/gateway/configuration-reference)
```
