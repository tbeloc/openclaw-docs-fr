---
summary: "Gestion des secrets : contrat SecretRef, comportement des snapshots d'exécution et scrubbing sécurisé unidirectionnel"
read_when:
  - Configuring SecretRefs for provider credentials and `auth-profiles.json` refs
  - Operating secrets reload, audit, configure, and apply safely in production
  - Understanding startup fail-fast, inactive-surface filtering, and last-known-good behavior
title: "Gestion des secrets"
---

# Gestion des secrets

OpenClaw prend en charge les SecretRefs additifs afin que les identifiants pris en charge n'aient pas besoin d'être stockés en clair dans la configuration.

Le texte en clair fonctionne toujours. Les SecretRefs sont optionnels par identifiant.

## Objectifs et modèle d'exécution

Les secrets sont résolus dans un snapshot d'exécution en mémoire.

- La résolution est rapide lors de l'activation, pas paresseuse sur les chemins de requête.
- Le démarrage échoue rapidement lorsqu'une SecretRef effectivement active ne peut pas être résolue.
- Le rechargement utilise un échange atomique : succès complet ou conservation du dernier snapshot connu.
- Les requêtes d'exécution lisent uniquement à partir du snapshot en mémoire actif.
- Les chemins de livraison sortants lisent également à partir de ce snapshot actif (par exemple, la livraison de réponse/thread Discord et les envois d'action Telegram) ; ils ne résolvent pas les SecretRefs à chaque envoi.

Cela maintient les pannes du fournisseur de secrets en dehors des chemins de requête actifs.

## Filtrage de surface active

Les SecretRefs sont validées uniquement sur les surfaces effectivement actives.

- Surfaces activées : les références non résolues bloquent le démarrage/rechargement.
- Surfaces inactives : les références non résolues ne bloquent pas le démarrage/rechargement.
- Les références inactives émettent des diagnostics non fatals avec le code `SECRETS_REF_IGNORED_INACTIVE_SURFACE`.

Exemples de surfaces inactives :

- Entrées de canal/compte désactivées.
- Identifiants de canal de niveau supérieur qu'aucun compte activé n'hérite.
- Surfaces d'outil/fonctionnalité désactivées.
- Clés spécifiques au fournisseur de recherche Web qui ne sont pas sélectionnées par `tools.web.search.provider`.
  En mode automatique (fournisseur non défini), les clés sont consultées par précédence pour la détection automatique du fournisseur jusqu'à ce qu'une soit résolue.
  Après la sélection, les clés de fournisseur non sélectionnées sont traitées comme inactives jusqu'à la sélection.
- Les SecretRefs `gateway.remote.token` / `gateway.remote.password` sont actifs si l'une de ces conditions est vraie :
  - `gateway.mode=remote`
  - `gateway.remote.url` est configuré
  - `gateway.tailscale.mode` est `serve` ou `funnel`
  - En mode local sans ces surfaces distantes :
    - `gateway.remote.token` est actif lorsque l'authentification par jeton peut gagner et qu'aucun jeton env/auth n'est configuré.
    - `gateway.remote.password` est actif uniquement lorsque l'authentification par mot de passe peut gagner et qu'aucun mot de passe env/auth n'est configuré.
- La SecretRef `gateway.auth.token` est inactive pour la résolution d'authentification au démarrage lorsque `OPENCLAW_GATEWAY_TOKEN` (ou `CLAWDBOT_GATEWAY_TOKEN`) est défini, car l'entrée de jeton env gagne pour ce runtime.

## Diagnostics de surface d'authentification de passerelle

Lorsqu'une SecretRef est configurée sur `gateway.auth.token`, `gateway.auth.password`,
`gateway.remote.token` ou `gateway.remote.password`, le démarrage/rechargement de la passerelle enregistre
l'état de la surface explicitement :

- `active` : la SecretRef fait partie de la surface d'authentification effective et doit être résolue.
- `inactive` : la SecretRef est ignorée pour ce runtime car une autre surface d'authentification gagne, ou
  car l'authentification distante est désactivée/non active.

Ces entrées sont enregistrées avec `SECRETS_GATEWAY_AUTH_SURFACE` et incluent la raison utilisée par la
politique de surface active, afin que vous puissiez voir pourquoi un identifiant a été traité comme actif ou inactif.

## Vérification préalable de référence d'intégration

Lorsque l'intégration s'exécute en mode interactif et que vous choisissez le stockage SecretRef, OpenClaw exécute la validation préalable avant l'enregistrement :

- Références env : valide le nom de la variable env et confirme qu'une valeur non vide est visible lors de l'intégration.
- Références de fournisseur (`file` ou `exec`) : valide la sélection du fournisseur, résout `id` et vérifie le type de valeur résolue.
- Chemin de réutilisation de démarrage rapide : lorsque `gateway.auth.token` est déjà une SecretRef, l'intégration la résout avant l'amorçage de sonde/tableau de bord (pour les références `env`, `file` et `exec`) en utilisant la même porte fail-fast.

Si la validation échoue, l'intégration affiche l'erreur et vous permet de réessayer.

## Contrat SecretRef

Utilisez une forme d'objet identique partout :

```json5
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

### `source: "env"`

```json5
{ source: "env", provider: "default", id: "OPENAI_API_KEY" }
```

Validation :

- `provider` doit correspondre à `^[a-z][a-z0-9_-]{0,63}$`
- `id` doit correspondre à `^[A-Z][A-Z0-9_]{0,127}$`

### `source: "file"`

```json5
{ source: "file", provider: "filemain", id: "/providers/openai/apiKey" }
```

Validation :

- `provider` doit correspondre à `^[a-z][a-z0-9_-]{0,63}$`
- `id` doit être un pointeur JSON absolu (`/...`)
- Échappement RFC6901 dans les segments : `~` => `~0`, `/` => `~1`

### `source: "exec"`

```json5
{ source: "exec", provider: "vault", id: "providers/openai/apiKey" }
```

Validation :

- `provider` doit correspondre à `^[a-z][a-z0-9_-]{0,63}$`
- `id` doit correspondre à `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$`
- `id` ne doit pas contenir `.` ou `..` comme segments de chemin délimités par des barres obliques (par exemple `a/../b` est rejeté)

## Configuration du fournisseur

Définissez les fournisseurs sous `secrets.providers` :

```json5
{
  secrets: {
    providers: {
      default: { source: "env" },
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json", // or "singleValue"
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        args: ["--profile", "prod"],
        passEnv: ["PATH", "VAULT_ADDR"],
        jsonOnly: true,
      },
    },
    defaults: {
      env: "default",
      file: "filemain",
      exec: "vault",
    },
    resolution: {
      maxProviderConcurrency: 4,
      maxRefsPerProvider: 512,
      maxBatchBytes: 262144,
    },
  },
}
```

### Fournisseur Env

- Liste d'autorisation optionnelle via `allowlist`.
- Les valeurs env manquantes/vides échouent la résolution.

### Fournisseur File

- Lit le fichier local à partir de `path`.
- `mode: "json"` s'attend à une charge utile d'objet JSON et résout `id` comme pointeur.
- `mode: "singleValue"` s'attend à l'id de référence `"value"` et retourne le contenu du fichier.
- Le chemin doit passer les vérifications de propriété/permission.
- Note d'échec fermé Windows : si la vérification ACL n'est pas disponible pour un chemin, la résolution échoue. Pour les chemins de confiance uniquement, définissez `allowInsecurePath: true` sur ce fournisseur pour contourner les vérifications de sécurité du chemin.

### Fournisseur Exec

- Exécute le chemin binaire absolu configuré, pas de shell.
- Par défaut, `command` doit pointer vers un fichier régulier (pas un lien symbolique).
- Définissez `allowSymlinkCommand: true` pour autoriser les chemins de commande de lien symbolique (par exemple, les shims Homebrew). OpenClaw valide le chemin cible résolu.
- Associez `allowSymlinkCommand` avec `trustedDirs` pour les chemins du gestionnaire de paquets (par exemple `["/opt/homebrew"]`).
- Prend en charge le délai d'expiration, le délai d'expiration sans sortie, les limites d'octets de sortie, la liste d'autorisation env et les répertoires de confiance.
- Note d'échec fermé Windows : si la vérification ACL n'est pas disponible pour le chemin de commande, la résolution échoue. Pour les chemins de confiance uniquement, définissez `allowInsecurePath: true` sur ce fournisseur pour contourner les vérifications de sécurité du chemin.

Charge utile de requête (stdin) :

```json
{ "protocolVersion": 1, "provider": "vault", "ids": ["providers/openai/apiKey"] }
```

Charge utile de réponse (stdout) :

```jsonc
{ "protocolVersion": 1, "values": { "providers/openai/apiKey": "<openai-api-key>" } } // pragma: allowlist secret
```

Erreurs optionnelles par id :

```json
{
  "protocolVersion": 1,
  "values": {},
  "errors": { "providers/openai/apiKey": { "message": "not found" } }
}
```

## Exemples d'intégration Exec

### 1Password CLI

```json5
{
  secrets: {
    providers: {
      onepassword_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/op",
        allowSymlinkCommand: true, // required for Homebrew symlinked binaries
        trustedDirs: ["/opt/homebrew"],
        args: ["read", "op://Personal/OpenClaw QA API Key/password"],
        passEnv: ["HOME"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "onepassword_openai", id: "value" },
      },
    },
  },
}
```

### HashiCorp Vault CLI

```json5
{
  secrets: {
    providers: {
      vault_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/vault",
        allowSymlinkCommand: true, // required for Homebrew symlinked binaries
        trustedDirs: ["/opt/homebrew"],
        args: ["kv", "get", "-field=OPENAI_API_KEY", "secret/openclaw"],
        passEnv: ["VAULT_ADDR", "VAULT_TOKEN"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "vault_openai", id: "value" },
      },
    },
  },
}
```

### `sops`

```json5
{
  secrets: {
    providers: {
      sops_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/sops",
        allowSymlinkCommand: true, // required for Homebrew symlinked binaries
        trustedDirs: ["/opt/homebrew"],
        args: ["-d", "--extract", '["providers"]["openai"]["apiKey"]', "/path/to/secrets.enc.json"],
        passEnv: ["SOPS_AGE_KEY_FILE"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "sops_openai", id: "value" },
      },
    },
  },
}
```

## Surface d'identifiant prise en charge

Les identifiants pris en charge et non pris en charge canoniques sont répertoriés dans :

- [SecretRef Credential Surface](/reference/secretref-credential-surface)

Les identifiants frappés à l'exécution ou rotatifs et le matériel d'actualisation OAuth sont intentionnellement exclus de la résolution SecretRef en lecture seule.

## Comportement requis et précédence

- Champ sans référence : inchangé.
- Champ avec une référence : requis sur les surfaces actives lors de l'activation.
- Si le texte en clair et la référence sont présents, la référence prend la précédence sur les chemins de précédence pris en charge.

Signaux d'avertissement et d'audit :

- `SECRETS_REF_OVERRIDES_PLAINTEXT` (avertissement d'exécution)
- `REF_SHADOWED` (constatation d'audit lorsque les identifiants `auth-profiles.json` prennent la précédence sur les références `openclaw.json`)

Comportement de compatibilité Google Chat :

- `serviceAccountRef` prend la précédence sur le texte en clair `serviceAccount`.
- La valeur en clair est ignorée lorsque la référence sœur est définie.

## Déclencheurs d'activation

L'activation secrète s'exécute sur :

- Démarrage (vérification préalable plus activation finale)
- Chemin d'application à chaud de rechargement de configuration
- Che
