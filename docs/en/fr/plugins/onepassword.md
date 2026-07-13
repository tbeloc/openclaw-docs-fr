---
summary: "Utilisez le plugin 1Password optionnel comme courtier de secrets d'agent audité"
read_when:
  - You want agents to request curated 1Password secrets
  - You need per-secret approval policy and audit history
  - You are configuring a 1Password service account for OpenClaw
title: "Courtier de secrets 1Password"
---

# Courtier de secrets 1Password

Le plugin `onepassword` fourni donne aux agents un outil contrôlé par politique pour
lire un ensemble organisé de champs 1Password. Il est désactivé par défaut et ne fait
rien jusqu'à ce que `plugins.entries.onepassword.config` soit présent.

C'est un outil d'agent, pas un fournisseur SecretRef. Il n'injecte pas de variables
d'environnement ni ne résout les secrets de configuration OpenClaw.

## Modèle de sécurité

- Authentification par compte de service uniquement. Le token reste dans un fichier
  d'identifiants local et n'est jamais accepté dans `openclaw.json`.
- Registre organisé uniquement. Les agents peuvent lister les slugs configurés, mais le
  plugin n'énumère jamais un coffre 1Password.
- Politique `auto`, `approve` ou `deny` par slug.
- Les approbations expirent. Une valeur en cache ne contourne jamais la politique actuelle.
- Chaque tentative d'accès est enregistrée dans l'état SQLite partagé d'OpenClaw. Les
  lignes d'audit incluent la raison fournie ; gardez les raisons non sensibles. Le courtier
  ne copie jamais une valeur récupérée ou le token de service dans une ligne d'audit.
- Après l'exécution de l'outil actuel, la persistance des transcriptions appartenant à
  OpenClaw remplace une valeur `get` réussie par des métadonnées rédactées.
- La valeur est visible par le modèle pour cette exécution. Si le modèle la copie dans un
  appel d'outil ultérieur ou une réponse, cet enregistrement séparé est en dehors du hook
  de persistance de ce plugin. Gardez les politiques étroites et ne demandez pas au modèle
  d'écho une valeur.
- Le plugin invoque `op` une fois par absence de cache. Il ne réessaie pas les limites de
  débit ou autres défaillances.

Donnez au compte de service un accès en lecture uniquement aux coffres et éléments
enregistrés dans la configuration du plugin.

## Avant de commencer

Vous avez besoin de :

- la CLI 1Password (`op`) installée sur l'hôte Gateway
- un compte de service 1Password avec accès aux éléments sélectionnés
- un fichier token de compte de service dédié

Activez le plugin fourni :

```bash
openclaw plugins enable onepassword
```

Créez le répertoire et le fichier de token sous le répertoire d'état OpenClaw :

```bash
mkdir -p ~/.openclaw/credentials/onepassword
chmod 700 ~/.openclaw/credentials/onepassword
printf '%s' "$OP_SERVICE_ACCOUNT_TOKEN" > \
  ~/.openclaw/credentials/onepassword/service-account-token
chmod 600 ~/.openclaw/credentials/onepassword/service-account-token
unset OP_SERVICE_ACCOUNT_TOKEN
```

Quand `OPENCLAW_STATE_DIR` est défini, remplacez `~/.openclaw` par ce répertoire.
Le plugin avertit une fois quand le fichier token est lisible ou inscriptible par le
groupe ou d'autres utilisateurs.

## Configurer les secrets enregistrés

Ajoutez la configuration du plugin à `openclaw.json` :

```jsonc
{
  "plugins": {
    "entries": {
      "onepassword": {
        "enabled": true,
        "config": {
          "vault": "Automation",
          "defaultPolicy": "approve",
          "cacheTtlSeconds": 300,
          "grantTtlHours": 720,
          "opTimeoutMs": 15000,
          "items": {
            "repository-token": {
              "item": "Repository automation token",
              "field": "credential",
              "policy": "approve",
              "description": "Token for repository automation",
            },
            "model-key": {
              "item": "Model provider key",
              "vault": "Agent credentials",
              "policy": "auto",
            },
          },
        },
      },
    },
  },
}
```

Les slugs utilisent des lettres minuscules, des chiffres et des tirets, commencent par une
lettre ou un chiffre, et contiennent au maximum 64 caractères. Un registre peut contenir
jusqu'à 32 slugs ; les descriptions peuvent contenir jusqu'à 200 caractères. `field`
accepte un libellé ou un ID de champ, ne doit pas contenir de virgule, et par défaut
`credential`. Un `vault` au niveau de l'élément remplace le coffre par défaut. `opBin`
peut définir un chemin absolu vers l'exécutable `op` ; sinon le plugin résout `op` à
partir de `PATH`. Les titres d'éléments ne doivent pas commencer par un tiret.

## Utiliser l'outil d'agent

Le nom de l'outil est `onepassword`.

Lister les slugs enregistrés :

```json
{ "action": "list" }
```

Le résultat contient uniquement le slug, la description, la politique et si une
approbation permanente est active. Il ne contient jamais une valeur secrète et ne
demande pas à 1Password.

Demander un secret :

```json
{
  "action": "get",
  "slug": "repository-token",
  "reason": "Authenticate the requested repository operation"
}
```

`reason` est obligatoire, doit être non vide, et est limité à 300 caractères. Un `get`
réussi retourne la valeur plus le slug configuré, le titre de l'élément et le libellé
du champ.

## Niveaux de politique et approbations

- `auto` : récupérer immédiatement et auditer la demande.
- `deny` : bloquer et auditer la demande.
- `approve` : utiliser une approbation permanente non expirée, ou demander à un humain
  d'autoriser une fois, toujours ou refuser.

Autoriser une fois autorise uniquement l'appel d'outil actuel. Autoriser toujours écrit
une approbation permanente pour cet agent et ce slug dans SQLite ; les autres agents
doivent recevoir leur propre approbation. OpenClaw n'offre autoriser toujours que quand
l'appelant a une identité d'agent concrète. L'approbation expire après `grantTtlHours`,
qui par défaut est 720 heures. Une approbation non résolue ou expirée refuse la demande ;
l'attente d'approbation maximale est 600 secondes. Le plugin conserve jusqu'à 1 024
approbations permanentes ; à cette limite, l'approbation la plus ancienne est évincée et
son agent doit approuver l'accès suivant.

Le cache en mémoire par défaut est 300 secondes et est limité par le registre de slugs
configuré. Définissez `cacheTtlSeconds` à `0` pour le désactiver. La politique est
évaluée avant chaque recherche en cache, et les accès au cache sont audités. Les
rechargements de configuration à l'exécution prennent effet à chaque limite de politique
et d'exécution ; désactiver le plugin ou supprimer, refuser ou rediriger un slug invalide
l'autorisation en attente et les valeurs en cache.

## Inspecter l'état et l'historique d'audit

Afficher la disponibilité et les comptages de registre :

```bash
openclaw onepassword status
```

Cela rapporte si le fichier token existe, si `op` a été résolu et son chemin, le nombre
d'éléments enregistrés et les comptages par politique. Il ne lit ni n'imprime jamais le
token ou les valeurs secrètes.

Afficher les 50 lignes d'audit les plus récentes :

```bash
openclaw onepassword audit
openclaw onepassword audit --limit 100
```

Les lignes sont les plus récentes en premier et affichent l'horodatage, l'agent, le slug,
le résultat et une raison tronquée. La raison est stockée telle que fournie ; le courtier
n'ajoute jamais la valeur récupérée au journal d'audit.

## Comportement de la CLI 1Password

Chaque absence de cache exécute `op item get` avec l'élément configuré, le coffre et le
sélecteur de champ exact, la sortie JSON, un délai d'attente limité et `--cache=false`.
L'enfant reçoit uniquement ce champ plutôt que l'élément complet. Seuls
`OP_SERVICE_ACCOUNT_TOKEN` et `HOME` sont présents dans l'environnement enfant.

Le plugin fait une tentative. Les erreurs `RATE_LIMITED` doivent être gérées en attendant
avant une demande d'agent ultérieure ; le plugin ne crée pas une boucle de réessai
automatique. D'autres codes d'erreur stables distinguent les tokens ou binaires manquants,
les éléments ou champs manquants, les défaillances d'authentification, les délais d'attente
et autres défaillances `op`.
