# Gestion des secrets

OpenClaw prend en charge les SecretRefs additifs afin que les identifiants pris en charge n'aient pas besoin d'être stockés en clair dans la configuration.

Le texte en clair fonctionne toujours. Les SecretRefs sont optionnels par identifiant.

## Objectifs et modèle d'exécution

Les secrets sont résolus dans un instantané d'exécution en mémoire.

- La résolution est rapide lors de l'activation, pas paresseuse sur les chemins de requête.
- Le démarrage échoue rapidement lorsqu'une SecretRef effectivement active ne peut pas être résolue.
- Le rechargement utilise un échange atomique : succès complet ou conservation du dernier instantané connu valide.
- Les requêtes d'exécution lisent uniquement à partir de l'instantané actif en mémoire.
- Les chemins de livraison sortante lisent également à partir de cet instantané actif (par exemple, la livraison de réponse/fil Discord et les envois d'action Telegram) ; ils ne résolvent pas les SecretRefs à chaque envoi.

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
  En mode automatique (fournisseur non défini), les clés sont consultées par ordre de priorité pour la détection automatique du fournisseur jusqu'à ce qu'une soit résolue.
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
- Chemin de réutilisation de démarrage rapide : lorsque `gateway.auth.token` est déjà une SecretRef, l'intégration la résout avant l'amorçage de sonde/tableau de bord (pour les références `env`, `file` et `exec`) en utilisant la même porte de défaillance rapide.

Si la validation échoue, l'intégration affiche l'erreur et vous permet de réessayer.

## Contrat SecretRef

Utilisez une seule forme d'objet partout :

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
- `mode: "json"` attend une charge utile d'objet JSON et résout `id` comme pointeur.
- `mode: "singleValue"` attend l'id de référence `"value"` et retourne le contenu du fichier.
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

- [Surface d'identifiant SecretRef](/reference/secretref-credential-surface)

Les identifiants créés à l'exécution ou rotatifs et le matériel d'actualisation OAuth sont intentionnellement exclus de la résolution SecretRef en lecture seule.

## Comportement requis et priorité

- Champ sans référence : inchangé.
- Champ avec une référence : requis sur les surfaces actives lors de l'activation.
- Si le texte en clair et la référence sont présents, la référence a priorité sur les chemins de priorité pris en charge.

Signaux d'avertissement et d'audit :

- `SECRETS_REF_OVERRIDES_PLAINTEXT` (avertissement d'exécution)
- `REF_SHADOWED` (constatation d'audit lorsque les identifiants `auth-profiles.json` ont priorité sur les références `openclaw.json`)

Comportement de compatibilité Google Chat :

- `serviceAccountRef` a priorité sur le texte en clair `serviceAccount`.
- La valeur en clair est ignorée lorsque la référence sœur est définie.

## Déclencheurs d'activation

L'activation des secrets s'exécute sur :

- Démarrage (vérification préalable plus activation finale)
- Chemin d'application à chaud du rechargement de configuration
- Chemin de vérification de redémarrage du rechargement de configuration
- Rechargement manuel via `secrets.reload`

Contrat d'activation :

- Le succès échange l'instantané de manière atomique.
- L'échec au démarrage interrompt le démarrage de la passerelle.
- L'échec du rechargement d'exécution conserve le dernier instantané connu valide.
- Fournir un jeton de canal explicite par appel à un appel d'outil/assistant sortant ne déclenche pas l'activation de SecretRef ; les points d'activation restent le démarrage, le rechargement et le `secrets.reload` explicite.

## Signaux dégradés et récupérés

Lorsque l'activation au moment du rechargement échoue après un état sain, OpenClaw entre dans un état de secrets dégradé.

Codes d'événement système et de journal à usage unique :

- `SECRETS_RELOADER_DEGRADED`
- `SECRETS_RELOADER_RECOVERED`

Comportement :

- Dégradé : l'exécution conserve le dernier instantané connu valide.
- Récupéré : émis une fois après la prochaine activation réussie.
- Les défaillances répétées alors que déjà dégradées enregistrent des avertissements mais ne spamment pas les événements.
- L'échec rapide au démarrage n'émet pas d'événements dégradés car l'exécution n'est jamais devenue active.

## Résolution du chemin de commande

Les chemins de commande peuvent opter pour la résolution de SecretRef supportée via RPC de snapshot de passerelle.

Il y a deux grands comportements :

- Les chemins de commande stricts (par exemple les chemins de mémoire distante `openclaw memory` et `openclaw qr --remote`) lisent à partir du snapshot actif et échouent rapidement lorsqu'une SecretRef requise est indisponible.
- Les chemins de commande en lecture seule (par exemple `openclaw status`, `openclaw status --all`, `openclaw channels status`, `openclaw channels resolve`, et les flux de réparation doctor/config en lecture seule) préfèrent également le snapshot actif, mais se dégradent au lieu d'abandonner lorsqu'une SecretRef ciblée est indisponible dans ce chemin de commande.

Comportement en lecture seule :

- Lorsque la passerelle est en cours d'exécution, ces commandes lisent d'abord à partir du snapshot actif.
- Si la résolution de la passerelle est incomplète ou si la passerelle est indisponible, elles tentent un repli local ciblé pour la surface de commande spécifique.
- Si une SecretRef ciblée est toujours indisponible, la commande continue avec une sortie dégradée en lecture seule et des diagnostics explicites tels que « configuré mais indisponible dans ce chemin de commande ».
- Ce comportement dégradé est local à la commande uniquement. Il n'affaiblit pas le démarrage du runtime, le rechargement ou les chemins d'envoi/authentification.

Autres notes :

- L'actualisation du snapshot après la rotation des secrets du backend est gérée par `openclaw secrets reload`.
- Méthode RPC de passerelle utilisée par ces chemins de commande : `secrets.resolve`.

## Flux d'audit et de configuration

Flux d'opérateur par défaut :

```bash
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets audit --check
```

### `secrets audit`

Les résultats incluent :

- valeurs en texte brut au repos (`openclaw.json`, `auth-profiles.json`, `.env`, et `agents/*/agent/models.json` généré)
- résidus de en-têtes de fournisseur sensibles en texte brut dans les entrées `models.json` générées
- références non résolues
- ombrage de précédence (`auth-profiles.json` prenant priorité sur les références `openclaw.json`)
- résidus hérités (`auth.json`, rappels OAuth)

Note sur les résidus d'en-têtes :

- La détection de résidus d'en-têtes sensibles est basée sur l'heuristique de nom (noms et fragments d'en-têtes d'authentification/identifiants courants tels que `authorization`, `x-api-key`, `token`, `secret`, `password`, et `credential`).

### `secrets configure`

Assistant interactif qui :

- configure d'abord `secrets.providers` (`env`/`file`/`exec`, ajouter/modifier/supprimer)
- vous permet de sélectionner les champs porteurs de secrets supportés dans `openclaw.json` plus `auth-profiles.json` pour une portée d'agent
- peut créer un nouveau mappage `auth-profiles.json` directement dans le sélecteur de cible
- capture les détails de SecretRef (`source`, `provider`, `id`)
- exécute la résolution préalable
- peut s'appliquer immédiatement

Modes utiles :

- `openclaw secrets configure --providers-only`
- `openclaw secrets configure --skip-provider-setup`
- `openclaw secrets configure --agent <id>`

Valeurs par défaut de `configure` apply :

- nettoyer les identifiants statiques correspondants de `auth-profiles.json` pour les fournisseurs ciblés
- nettoyer les entrées `api_key` statiques héritées de `auth.json`
- nettoyer les lignes de secrets connues correspondantes de `<config-dir>/.env`

### `secrets apply`

Appliquer un plan enregistré :

```bash
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
```

Pour les détails du contrat de cible/chemin strict et les règles de rejet exactes, voir :

- [Contrat du plan Secrets Apply](/gateway/secrets-plan-contract)

## Politique de sécurité unidirectionnelle

OpenClaw n'écrit intentionnellement pas de sauvegardes de restauration contenant des valeurs de secrets en texte brut historiques.

Modèle de sécurité :

- la vérification préalable doit réussir avant le mode d'écriture
- l'activation du runtime est validée avant la validation
- apply met à jour les fichiers en utilisant le remplacement de fichier atomique et la restauration au mieux de nos efforts en cas d'échec

## Notes de compatibilité d'authentification héritée

Pour les identifiants statiques, le runtime ne dépend plus du stockage d'authentification hérité en texte brut.

- La source d'identifiants du runtime est le snapshot en mémoire résolu.
- Les entrées `api_key` statiques héritées sont nettoyées lorsqu'elles sont découvertes.
- Le comportement de compatibilité lié à OAuth reste séparé.

## Note sur l'interface Web

Certaines unions SecretInput sont plus faciles à configurer en mode éditeur brut qu'en mode formulaire.

## Documents connexes

- Commandes CLI : [secrets](/cli/secrets)
- Détails du contrat du plan : [Contrat du plan Secrets Apply](/gateway/secrets-plan-contract)
- Surface d'identifiants : [Surface d'identifiants SecretRef](/reference/secretref-credential-surface)
- Configuration de l'authentification : [Authentification](/gateway/authentication)
- Posture de sécurité : [Sécurité](/gateway/security)
- Précédence des variables d'environnement : [Variables d'environnement](/help/environment)
