# Sémantique des identifiants d'authentification

Ce document définit la sémantique canonique d'éligibilité des identifiants et de résolution utilisée dans :

- `resolveAuthProfileOrder`
- `resolveApiKeyForProfile`
- `models status --probe`
- `doctor-auth`

L'objectif est de maintenir l'alignement entre le comportement au moment de la sélection et le comportement à l'exécution.

## Codes de raison stables

- `ok`
- `missing_credential`
- `invalid_expires`
- `expired`
- `unresolved_ref`

## Identifiants de jeton

Les identifiants de jeton (`type: "token"`) supportent `token` inline et/ou `tokenRef`.

### Règles d'éligibilité

1. Un profil de jeton est inéligible quand `token` et `tokenRef` sont tous deux absents.
2. `expires` est optionnel.
3. Si `expires` est présent, il doit être un nombre fini supérieur à `0`.
4. Si `expires` est invalide (`NaN`, `0`, négatif, non-fini, ou type incorrect), le profil est inéligible avec `invalid_expires`.
5. Si `expires` est dans le passé, le profil est inéligible avec `expired`.
6. `tokenRef` ne contourne pas la validation de `expires`.

### Règles de résolution

1. La sémantique du résolveur correspond à la sémantique d'éligibilité pour `expires`.
2. Pour les profils éligibles, le matériel de jeton peut être résolu à partir de la valeur inline ou de `tokenRef`.
3. Les références non résolubles produisent `unresolved_ref` dans la sortie de `models status --probe`.

## Messagerie compatible avec l'héritage

Pour la compatibilité des scripts, les erreurs de sonde conservent cette première ligne inchangée :

`Auth profile credentials are missing or expired.`

Les détails conviviaux et les codes de raison stables peuvent être ajoutés sur les lignes suivantes.
