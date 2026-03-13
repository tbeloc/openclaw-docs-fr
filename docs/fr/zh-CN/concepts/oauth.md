# OAuth

OpenClaw prend en charge l'authentification par abonnement via OAuth pour les fournisseurs qui proposent cette fonctionnalité (en particulier **OpenAI Codex (ChatGPT OAuth)**). Pour les abonnements Anthropic, utilisez le flux **setup-token**. Cette page explique :

- Comment fonctionne l'**échange de jetons** OAuth (PKCE)
- Où les jetons sont **stockés** (et pourquoi)
- Comment gérer les **comptes multiples** (profils + remplacement par session)

OpenClaw prend également en charge les **plugins de fournisseur**, qui incluent leurs propres flux OAuth ou de clé API. Exécutez-les avec :

```bash
openclaw models auth login --provider <id>
```

## Point de convergence des jetons (pourquoi c'est nécessaire)

Les fournisseurs OAuth émettent généralement des **nouveaux jetons de rafraîchissement** lors des flux de connexion/rafraîchissement. Certains fournisseurs (ou clients OAuth) peuvent invalider les anciens jetons de rafraîchissement lors de l'émission de nouveaux jetons pour le même utilisateur/application.

Symptômes observés :

- Vous vous connectez via OpenClaw _et_ Claude Code / Codex CLI → l'un des deux se "déconnecte" aléatoirement plus tard

Pour atténuer cela, OpenClaw traite `auth-profiles.json` comme un **point de convergence des jetons** :

- Le runtime lit les identifiants de **même endroit**
- Nous pouvons maintenir plusieurs profils et les router de manière déterministe

## Stockage (où les jetons sont stockés)

Les clés sont stockées **par agent** :

- Profils d'authentification (OAuth + clés API) : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- Cache runtime (géré automatiquement ; ne pas modifier) : `~/.openclaw/agents/<agentId>/agent/auth.json`

Fichiers hérités à usage d'importation uniquement (toujours supportés, mais pas le stockage principal) :

- `~/.openclaw/credentials/oauth.json` (importé dans `auth-profiles.json` à la première utilisation)

Tous les chemins ci-dessus respectent également `$OPENCLAW_STATE_DIR` (remplacement du répertoire d'état). Référence complète : [/gateway/configuration](/gateway/configuration#auth-storage-oauth--api-keys)

## Anthropic setup-token (authentification par abonnement)

Exécutez `claude setup-token` sur n'importe quelle machine, puis collez-le dans OpenClaw :

```bash
openclaw models auth setup-token --provider anthropic
```

Si vous avez généré le jeton ailleurs, vous pouvez le coller manuellement :

```bash
openclaw models auth paste-token --provider anthropic
```

Vérification :

```bash
openclaw models status
```

## Échange OAuth (fonctionnement de la connexion)

Le flux de connexion interactif d'OpenClaw est implémenté dans `@mariozechner/pi-ai` et intégré aux assistants/commandes.

### Anthropic (Claude Pro/Max) setup-token

Résumé du flux :

1. Exécutez `claude setup-token`
2. Collez le jeton dans OpenClaw
3. Stocké en tant que profil d'authentification par jeton (pas de rafraîchissement)

Le chemin de l'assistant est `openclaw onboard` → choix d'authentification `setup-token` (Anthropic).

### OpenAI Codex (ChatGPT OAuth)

Résumé du flux (PKCE) :

1. Générez un vérificateur/défi PKCE + `state` aléatoire
2. Ouvrez `https://auth.openai.com/oauth/authorize?...`
3. Tentez de capturer le rappel à `http://127.0.0.1:1455/auth/callback`
4. Si le rappel ne peut pas être lié (ou vous êtes dans un environnement distant/sans interface), collez manuellement l'URL/code de redirection
5. Échangez à `https://auth.openai.com/oauth/token`
6. Extrayez `accountId` du jeton d'accès et stockez `{ access, refresh, expires, accountId }`

Le chemin de l'assistant est `openclaw onboard` → choix d'authentification `openai-codex`.

## Rafraîchissement + Expiration

Le profil stocke l'horodatage `expires`.

À l'exécution :

- Si `expires` est dans le futur → utilisez le jeton d'accès stocké
- S'il a expiré → rafraîchissez (sous verrou de fichier) et remplacez les identifiants stockés

Le processus de rafraîchissement est automatique ; vous n'avez généralement pas besoin de gérer manuellement les jetons.

## Comptes multiples (profils) + Routage

Deux modes :

### 1) Recommandé : Agents indépendants

Si vous souhaitez que "personnel" et "professionnel" ne se croisent jamais, utilisez des agents isolés (sessions indépendantes + identifiants + espaces de travail) :

```bash
openclaw agents add work
openclaw agents add personal
```

Configurez ensuite l'authentification par agent (assistant) et routez les conversations vers le bon agent.

### 2) Avancé : Plusieurs profils dans un seul agent

`auth-profiles.json` prend en charge plusieurs ID de profils pour le même fournisseur.

Choisissez quel profil utiliser :

- Globalement via l'ordre de configuration (`auth.order`)
- Par session via `/model ...@<profileId>`

Exemple (remplacement par session) :

- `/model Opus@anthropic:work`

Comment voir quels ID de profils existent :

- `openclaw channels list --json` (affiche `auth[]`)

Documentation connexe :

- [/concepts/model-failover](/concepts/model-failover) (rotation + règles de refroidissement)
- [/tools/slash-commands](/tools/slash-commands) (interface de commande)
