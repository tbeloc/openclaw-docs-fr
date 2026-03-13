---
read_when:
  - Vous souhaitez utiliser des modèles Amazon Bedrock dans OpenClaw
  - Vous devez configurer les identifiants AWS/région pour les appels de modèle
summary: Utiliser les modèles Amazon Bedrock (API Converse) dans OpenClaw
title: Amazon Bedrock
x-i18n:
  generated_at: "2026-02-03T10:04:01Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 318f1048451a1910b70522e2f7f9dfc87084de26d9e3938a29d372eed32244a8
  source_path: providers/bedrock.md
  workflow: 15
---

# Amazon Bedrock

OpenClaw peut utiliser les modèles **Amazon Bedrock** via le fournisseur de streaming **Bedrock Converse** de pi‑ai. L'authentification Bedrock utilise la **chaîne de credentials par défaut du SDK AWS**, et non une clé API.

## Fonctionnalités supportées par pi‑ai

- Fournisseur : `amazon-bedrock`
- API : `bedrock-converse-stream`
- Authentification : Identifiants AWS (variables d'environnement, configuration partagée ou rôle d'instance)
- Région : `AWS_REGION` ou `AWS_DEFAULT_REGION` (par défaut : `us-east-1`)

## Découverte automatique des modèles

Si des identifiants AWS sont détectés, OpenClaw peut découvrir automatiquement les modèles Bedrock qui supportent le **streaming** et la **sortie texte**. La découverte utilise `bedrock:ListFoundationModels` et est mise en cache (par défaut : 1 heure).

Les options de configuration se trouvent sous `models.bedrockDiscovery` :

```json5
{
  models: {
    bedrockDiscovery: {
      enabled: true,
      region: "us-east-1",
      providerFilter: ["anthropic", "amazon"],
      refreshInterval: 3600,
      defaultContextWindow: 32000,
      defaultMaxTokens: 4096,
    },
  },
}
```

Remarques :

- `enabled` est par défaut `true` si des identifiants AWS sont présents.
- `region` est par défaut `AWS_REGION` ou `AWS_DEFAULT_REGION`, puis `us-east-1`.
- `providerFilter` correspond aux noms de fournisseurs Bedrock (par exemple `anthropic`).
- `refreshInterval` est en secondes ; définissez à `0` pour désactiver la mise en cache.
- `defaultContextWindow` (par défaut : `32000`) et `defaultMaxTokens` (par défaut : `4096`) sont utilisés pour les modèles découverts (vous pouvez remplacer ces valeurs si vous connaissez les limites du modèle).

## Configuration (manuelle)

1. Assurez-vous que les identifiants AWS sont disponibles sur l'**hôte Gateway** :

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
# Optionnel :
export AWS_SESSION_TOKEN="..."
export AWS_PROFILE="your-profile"
# Optionnel (clé API Bedrock/jeton Bearer) :
export AWS_BEARER_TOKEN_BEDROCK="..."
```

2. Ajoutez le fournisseur Bedrock et les modèles à votre configuration (pas besoin de `apiKey`) :

```json5
{
  models: {
    providers: {
      "amazon-bedrock": {
        baseUrl: "https://bedrock-runtime.us-east-1.amazonaws.com",
        api: "bedrock-converse-stream",
        auth: "aws-sdk",
        models: [
          {
            id: "anthropic.claude-opus-4-5-20251101-v1:0",
            name: "Claude Opus 4.5 (Bedrock)",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "amazon-bedrock/anthropic.claude-opus-4-5-20251101-v1:0" },
    },
  },
}
```

## Rôle d'instance EC2

Lors de l'exécution d'OpenClaw sur une instance EC2 avec un rôle IAM attaché, le SDK AWS utilise automatiquement le service de métadonnées d'instance (IMDS) pour l'authentification. Cependant, la détection des identifiants d'OpenClaw ne vérifie actuellement que les variables d'environnement, pas les identifiants IMDS.

**Solution de contournement :** Définissez `AWS_PROFILE=default` pour indiquer que les identifiants AWS sont disponibles. L'authentification réelle utilise toujours le rôle d'instance via IMDS.

```bash
# Ajoutez à ~/.bashrc ou votre fichier de configuration shell
export AWS_PROFILE=default
export AWS_REGION=us-east-1
```

**Permissions IAM requises** pour le rôle d'instance EC2 :

- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`
- `bedrock:ListFoundationModels` (pour la découverte automatique)

Ou attachez la politique gérée `AmazonBedrockFullAccess`.

**Configuration rapide :**

```bash
# 1. Créer le rôle IAM et le profil d'instance
aws iam create-role --role-name EC2-Bedrock-Access \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy --role-name EC2-Bedrock-Access \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam create-instance-profile --instance-profile-name EC2-Bedrock-Access
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-Bedrock-Access \
  --role-name EC2-Bedrock-Access

# 2. Attacher à votre instance EC2
aws ec2 associate-iam-instance-profile \
  --instance-id i-xxxxx \
  --iam-instance-profile Name=EC2-Bedrock-Access

# 3. Activer la découverte sur l'instance EC2
openclaw config set models.bedrockDiscovery.enabled true
openclaw config set models.bedrockDiscovery.region us-east-1

# 4. Définir les variables d'environnement requises pour la solution de contournement
echo 'export AWS_PROFILE=default' >> ~/.bashrc
echo 'export AWS_REGION=us-east-1' >> ~/.bashrc
source ~/.bashrc

# 5. Vérifier que les modèles ont été découverts
openclaw models list
```

## Remarques

- Bedrock nécessite que l'**accès aux modèles** soit activé dans votre compte/région AWS.
- La découverte automatique nécessite la permission `bedrock:ListFoundationModels`.
- Si vous utilisez un profil de configuration, définissez `AWS_PROFILE` sur l'hôte Gateway.
- OpenClaw récupère les identifiants dans cet ordre : `AWS_BEARER_TOKEN_BEDROCK`, puis `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`, puis `AWS_PROFILE`, puis la chaîne par défaut du SDK AWS.
- Le support du raisonnement dépend du modèle ; consultez la fiche du modèle Bedrock pour les fonctionnalités actuelles.
- Si vous préférez un processus de clé gérée, vous pouvez également placer un proxy compatible OpenAI devant Bedrock et le configurer comme fournisseur OpenAI.
