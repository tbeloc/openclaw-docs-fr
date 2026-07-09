---
summary: "Utilisez le plugin Vault fourni pour résoudre les SecretRefs depuis HashiCorp Vault"
read_when:
  - You want OpenClaw to read API keys from HashiCorp Vault
  - You are setting up SecretRefs on a local machine or server
  - You need to configure Vault-backed model provider credentials
title: "Vault SecretRefs"
---

# Vault SecretRefs

Le plugin Vault fourni permet à OpenClaw de résoudre les `exec` SecretRefs depuis
HashiCorp Vault au démarrage et au rechargement de la Gateway. OpenClaw stocke les
références Vault dans la config, conserve les valeurs résolues dans l'instantané
des secrets en mémoire, et n'écrit pas les clés API résolues dans `openclaw.json`.

Utilisez ceci quand vous exécutez déjà Vault ou que vous voulez que les clés des
fournisseurs de modèles vivent en dehors des fichiers de config OpenClaw. Pour le
modèle runtime SecretRef, voir [Gestion des secrets](/fr/gateway/secrets).

## Avant de commencer

Vous avez besoin de :

- OpenClaw avec le plugin `vault` fourni disponible
- un serveur Vault accessible
- une authentification Vault qui peut produire un jeton client avec accès en lecture
  aux chemins de secrets qu'OpenClaw doit résoudre
- l'environnement qui démarre la Gateway doit inclure `VAULT_ADDR` et soit
  `VAULT_TOKEN`, soit `OPENCLAW_VAULT_AUTH_METHOD=token_file` avec `VAULT_TOKEN_FILE`,
  ou une connexion JWT/Kubernetes configurée

Le résolveur communique avec Vault via HTTP depuis Node. La Gateway n'a pas besoin
de la CLI Vault pour résoudre les SecretRefs.

Activez le plugin fourni avant d'exécuter les commandes `openclaw vault` :

```bash
openclaw plugins enable vault
```

## Stocker une clé de fournisseur dans Vault

OpenClaw utilise par défaut KV v2 monté sur `secret`, correspondant aux exemples
du serveur de développement Vault. Pour un Vault de production, définissez
`OPENCLAW_VAULT_KV_MOUNT` sur votre chemin de montage KV réel avant de créer les
ids SecretRef. Avec les valeurs par défaut d'OpenClaw, cet id SecretRef :

```text
providers/openrouter/apiKey
```

lit ce champ Vault :

```text
secret/data/providers/openrouter -> apiKey
```

Une façon de le créer avec la CLI Vault est :

```bash
export OPENROUTER_API_KEY=<openrouter-api-key>
vault kv put secret/providers/openrouter apiKey="$OPENROUTER_API_KEY"
```

Utilisez un jeton client limité pour OpenClaw, pas un jeton root. Pour la mise en
page KV v2 par défaut, une politique minimale pour les clés des fournisseurs de
modèles ressemble à :

```hcl
path "secret/data/providers/*" {
  capabilities = ["read"]
}
```

## Rendre Vault visible à la Gateway

Pour une Gateway locale non conteneurisée, exportez les paramètres Vault dans le
même shell qui démarre OpenClaw. La méthode d'authentification par défaut lit un
jeton client Vault depuis `VAULT_TOKEN` :

```bash
export VAULT_ADDR=https://vault.example.com
export VAULT_TOKEN=<vault-client-token>
```

Si Vault Agent écrit un fichier de réserve de jeton, utilisez l'authentification
par fichier de jeton :

```bash
export VAULT_ADDR=https://vault.example.com
export OPENCLAW_VAULT_AUTH_METHOD=token_file
export VAULT_TOKEN_FILE=/vault/secrets/token
```

Pour un serveur Vault signé par une CA privée, installez soit cette CA dans le
magasin de confiance de l'hôte et activez la confiance système Node :

```bash
export NODE_USE_SYSTEM_CA=1
```

Ou fournissez un bundle PEM directement :

```bash
export NODE_EXTRA_CA_CERTS=/path/to/vault-ca.pem
```

Ces variables doivent être présentes au démarrage d'OpenClaw. Le plugin Vault les
transmet à son processus de résolution.

Pour l'authentification JWT non-interactive, utilisez un fichier JWT de charge de
travail et un rôle Vault de type `jwt` :

```bash
export VAULT_ADDR=https://vault.example.com
export OPENCLAW_VAULT_AUTH_METHOD=jwt
export OPENCLAW_VAULT_AUTH_MOUNT=jwt
export OPENCLAW_VAULT_AUTH_ROLE=openclaw
export OPENCLAW_VAULT_JWT_FILE=/var/run/secrets/tokens/vault
```

Le fichier JWT doit être un jeton de charge de travail projeté, comme un jeton de
compte de service Kubernetes avec une audience acceptée par le rôle Vault.
La connexion OIDC interactive par navigateur est utile pour les humains, mais le
runtime de la Gateway a besoin d'une connexion JWT non-interactive ou d'un fichier
de jeton.

Pour la méthode d'authentification Kubernetes de Vault, utilisez `kubernetes`. Ceci
est destiné aux Gateways s'exécutant en tant que Pods ; le montage par défaut est
`kubernetes`, et le fichier JWT par défaut est le chemin du jeton de compte de
service standard :

```bash
export VAULT_ADDR=https://vault.example.com
export OPENCLAW_VAULT_AUTH_METHOD=kubernetes
export OPENCLAW_VAULT_AUTH_ROLE=openclaw
```

Définissez `OPENCLAW_VAULT_AUTH_MOUNT` uniquement quand Vault a monté l'authentification
Kubernetes ailleurs que sur `auth/kubernetes`. Définissez `OPENCLAW_VAULT_JWT_FILE`
uniquement quand le jeton de compte de service est projeté sur un chemin personnalisé.

Paramètres optionnels :

```bash
export VAULT_NAMESPACE=<namespace-name>
export OPENCLAW_VAULT_KV_MOUNT=secret
export OPENCLAW_VAULT_KV_VERSION=2
```

Vérifiez ce que le shell actuel peut voir :

```bash
openclaw vault status
```

Quand plus d'un fournisseur de secrets soutenu par Vault est configuré, sélectionnez-en
un par alias :

```bash
openclaw vault status --provider-alias corp-vault
```

`openclaw vault status` n'imprime jamais `VAULT_TOKEN` ; il rapporte uniquement si
le jeton, le fichier de jeton et le fichier JWT sont définis.

<Warning>
Si la Gateway s'exécute en tant que service, LaunchAgent, unité systemd, tâche
planifiée ou conteneur, cet environnement runtime doit recevoir les mêmes variables
Vault. Définir des variables dans un shell interactif uniquement prouve ce shell,
pas la Gateway déjà en cours d'exécution.
</Warning>

## Générer et appliquer un plan SecretRef

Créez un plan qui mappe la clé API du fournisseur de modèles OpenRouter à Vault :

```bash
openclaw vault setup \
  --plan-out ./vault-secrets-plan.json \
  --openrouter-id providers/openrouter/apiKey
```

Appliquez et vérifiez le plan :

```bash
openclaw secrets apply --from ./vault-secrets-plan.json --dry-run --allow-exec
openclaw secrets apply --from ./vault-secrets-plan.json --allow-exec
openclaw secrets audit --check --allow-exec
openclaw secrets reload
```

Utilisez `--allow-exec` car le plugin Vault résout via un fournisseur SecretRef
exec géré par OpenClaw.

Si la Gateway n'est pas encore en cours d'exécution, démarrez-la normalement après
avoir appliqué le plan au lieu d'exécuter `openclaw secrets reload`.

## Configurer plus de clés de fournisseur

Raccourcis intégrés :

```bash
openclaw vault setup --openai-id providers/openai/apiKey
openclaw vault setup --anthropic-id providers/anthropic/apiKey
openclaw vault setup --openrouter-id providers/openrouter/apiKey
```

Plusieurs clés de fournisseur dans un plan :

```bash
openclaw vault setup \
  --plan-out ./vault-secrets-plan.json \
  --openai-id providers/openai/apiKey \
  --anthropic-id providers/anthropic/apiKey \
  --openrouter-id providers/openrouter/apiKey
```

Les fournisseurs fournis sans raccourcis, ou les fournisseurs OpenAI-compatibles et
les fournisseurs de modèles personnalisés déjà configurés, utilisent `--provider-key` :

```bash
openclaw vault setup \
  --plan-out ./vault-secrets-plan.json \
  --provider-key local-openai=providers/local-openai/apiKey \
  --provider-key groq=providers/groq/apiKey
```

Chaque `--provider-key <provider=id>` écrit un SecretRef dans
`models.providers.<provider>.apiKey`. Pour les fournisseurs personnalisés, il ne crée
pas les paramètres `baseUrl`, `api` ou `models` du fournisseur ; configurez-les d'abord.

Utilisez `--target <path=id>` pour tout chemin cible SecretRef connu :

```bash
openclaw vault setup \
  --target channels.telegram.botToken=channels/telegram/botToken \
  --target models.providers.openai.headers.x-api-key=providers/openai/proxyKey \
  --target auth-profiles:main:profiles.openai.key=providers/openai/apiKey
```

Les chemins cibles nus s'appliquent à `openclaw.json`. Utilisez
`auth-profiles:<agentId>:<path>` pour les cibles `auth-profiles.json` existantes.
Le chemin cible doit être une cible SecretRef OpenClaw enregistrée. La commande setup
ne crée pas de secrets nommés arbitraires dans OpenClaw ; Vault reste le magasin de
secrets, et OpenClaw stocke uniquement les SecretRefs sur les champs de config supportés.

## Format de l'id SecretRef

Les ids SecretRef Vault utilisent cette convention :

```text
<vault-secret-path>/<field>
```

Exemples :

| Id SecretRef                  | Lecture Vault KV v2 par défaut     | Champ retourné |
| ----------------------------- | ---------------------------------- | -------------- |
| `providers/openrouter/apiKey` | `secret/data/providers/openrouter` | `apiKey`       |
| `providers/openai/apiKey`     | `secret/data/providers/openai`     | `apiKey`       |
| `teams/agent-prod/openrouter` | `secret/data/teams/agent-prod`     | `openrouter`   |

Le champ Vault retourné doit être une chaîne.

Pour KV v1, définissez :

```bash
export OPENCLAW_VAULT_KV_VERSION=1
```

Ensuite `providers/openrouter/apiKey` lit :

```text
secret/providers/openrouter -> apiKey
```

## Ce qu'OpenClaw stocke

L'application d'un plan de configuration Vault stocke un fournisseur géré par plugin :

```json
{
  "source": "exec",
  "pluginIntegration": {
    "pluginId": "vault",
    "integrationId": "vault"
  }
}
```

Les champs de credentials pointent vers ce fournisseur :

```json
{ "source": "exec", "provider": "vault", "id": "providers/openrouter/apiKey" }
```

La valeur résolue vit uniquement dans l'instantané des secrets runtime actif.

## Conteneurs et déploiements gérés

Les Gateways conteneurisées utilisent toujours le même plugin et la même config
SecretRef. Le conteneur doit recevoir :

- `VAULT_ADDR`
- une source d'authentification :
  - `VAULT_TOKEN`
  - `OPENCLAW_VAULT_AUTH_METHOD=token_file` plus `VAULT_TOKEN_FILE`
  - `OPENCLAW_VAULT_AUTH_METHOD=jwt` plus `OPENCLAW_VAULT_AUTH_MOUNT`,
    `OPENCLAW_VAULT_AUTH_ROLE`, et `OPENCLAW_VAULT_JWT_FILE`
  - `OPENCLAW_VAULT_AUTH_METHOD=kubernetes` plus `OPENCLAW_VAULT_AUTH_ROLE` ; optionnellement
    remplacez `OPENCLAW_VAULT_AUTH_MOUNT` ou `OPENCLAW_VAULT_JWT_FILE`
- optionnel `VAULT_NAMESPACE`, `OPENCLAW_VAULT_KV_MOUNT`, et
  `OPENCLAW_VAULT_KV_VERSION`

Quand vous utilisez Kubernetes, préférez `OPENCLAW_VAULT_AUTH_METHOD=kubernetes`
quand Vault a l'authentification Kubernetes configurée pour le cluster. Utilisez
`OPENCLAW_VAULT_AUTH_METHOD=jwt` uniquement quand Vault est configuré pour traiter le cluster
comme un émetteur JWT/OIDC générique. L'une ou l'autre option est meilleure qu'un jeton
Vault de longue durée dans un Secret Kubernetes. Les déploiements de sidecar ou d'injecteur
Vault Agent peuvent utiliser `token_file` à la place.

Pour les configurations Vault multi-locataires, conservez le routage des locataires dans
la politique Vault et la config de déploiement. OpenClaw ne nécessite pas un montage, un
rôle ou un chemin fixe : chaque environnement Gateway peut définir ses propres
`OPENCLAW_VAULT_KV_MOUNT`, `OPENCLAW_VAULT_AUTH_ROLE`, et ids SecretRef. Si une Gateway
partagée doit résoudre différents utilisateurs Vault en même temps, utilisez des fournisseurs
exec configurés manuellement qui enveloppent des environnements d'authentification distincts,
ou divisez les locataires entre les environnements Gateway avec un env Vault séparé.

## Connexes

- [Gestion des secrets](/fr/gateway/secrets)
- [`openclaw secrets`](/fr/cli/secrets)
- [Inventaire des plugins](/fr/plugins/plugin-inventory)
