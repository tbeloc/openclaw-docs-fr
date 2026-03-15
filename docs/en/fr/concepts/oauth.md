---
summary: "OAuth dans OpenClaw : échange de jetons, stockage et modèles multi-comptes"
read_when:
  - You want to understand OpenClaw OAuth end-to-end
  - You hit token invalidation / logout issues
  - You want setup-token or OAuth auth flows
  - You want multiple accounts or profile routing
title: "OAuth"
---

# OAuth

OpenClaw supporte l'authentification par « subscription auth » via OAuth pour les fournisseurs qui l'offrent (notamment **OpenAI Codex (ChatGPT OAuth)**). Pour les abonnements Anthropic, utilisez le flux **setup-token**. L'utilisation d'abonnements Anthropic en dehors de Claude Code a été restreinte pour certains utilisateurs par le passé, traitez-la donc comme un risque de choix utilisateur et vérifiez vous-même la politique actuelle d'Anthropic. OpenAI Codex OAuth est explicitement supporté pour une utilisation dans des outils externes comme OpenClaw. Cette page explique :

Pour Anthropic en production, l'authentification par clé API est le chemin recommandé plus sûr par rapport à l'authentification par setup-token d'abonnement.

- comment fonctionne l'**échange de jetons** OAuth (PKCE)
- où les jetons sont **stockés** (et pourquoi)
- comment gérer les **comptes multiples** (profils + remplacements par session)

OpenClaw supporte également les **plugins de fournisseur** qui livrent leurs propres flux OAuth ou clé API. Exécutez-les via :

```bash
openclaw models auth login --provider <id>
```

## Le puits de jetons (pourquoi il existe)

Les fournisseurs OAuth émettent couramment un **nouveau jeton de rafraîchissement** lors des flux de connexion/rafraîchissement. Certains fournisseurs (ou clients OAuth) peuvent invalider les anciens jetons de rafraîchissement lorsqu'un nouveau est émis pour le même utilisateur/application.

Symptôme pratique :

- vous vous connectez via OpenClaw _et_ via Claude Code / Codex CLI → l'un d'eux se retrouve aléatoirement « déconnecté » plus tard

Pour réduire cela, OpenClaw traite `auth-profiles.json` comme un **puits de jetons** :

- le runtime lit les identifiants à partir d'**un seul endroit**
- nous pouvons conserver plusieurs profils et les router de manière déterministe

## Stockage (où vivent les jetons)

Les secrets sont stockés **par agent** :

- Profils d'authentification (OAuth + clés API + références de valeur optionnelles) : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- Fichier de compatibilité hérité : `~/.openclaw/agents/<agentId>/agent/auth.json`
  (les entrées statiques `api_key` sont supprimées lorsqu'elles sont détectées)

Fichier d'importation hérité uniquement (toujours supporté, mais pas le magasin principal) :

- `~/.openclaw/credentials/oauth.json` (importé dans `auth-profiles.json` à la première utilisation)

Tous les éléments ci-dessus respectent également `$OPENCLAW_STATE_DIR` (remplacement du répertoire d'état). Référence complète : [/gateway/configuration](/fr/gateway/configuration#auth-storage-oauth--api-keys)

Pour les références de secrets statiques et le comportement d'activation de snapshot d'exécution, voir [Gestion des secrets](/fr/gateway/secrets).

## Setup-token Anthropic (authentification par abonnement)

<Warning>
Le support du setup-token Anthropic est une compatibilité technique, pas une garantie de politique.
Anthropic a bloqué certaines utilisations d'abonnement en dehors de Claude Code par le passé.
Décidez vous-même si vous souhaitez utiliser l'authentification par abonnement et vérifiez les conditions actuelles d'Anthropic.
</Warning>

Exécutez `claude setup-token` sur n'importe quelle machine, puis collez-le dans OpenClaw :

```bash
openclaw models auth setup-token --provider anthropic
```

Si vous avez généré le jeton ailleurs, collez-le manuellement :

```bash
openclaw models auth paste-token --provider anthropic
```

Vérifiez :

```bash
openclaw models status
```

## Échange OAuth (comment fonctionne la connexion)

Les flux de connexion interactifs d'OpenClaw sont implémentés dans `@mariozechner/pi-ai` et intégrés aux assistants/commandes.

### Setup-token Anthropic

Forme du flux :

1. exécutez `claude setup-token`
2. collez le jeton dans OpenClaw
3. stockez comme profil d'authentification par jeton (pas de rafraîchissement)

Le chemin de l'assistant est `openclaw onboard` → choix d'authentification `setup-token` (Anthropic).

### OpenAI Codex (ChatGPT OAuth)

OpenAI Codex OAuth est explicitement supporté pour une utilisation en dehors de la CLI Codex, y compris les flux de travail OpenClaw.

Forme du flux (PKCE) :

1. générez le vérificateur/défi PKCE + `state` aléatoire
2. ouvrez `https://auth.openai.com/oauth/authorize?...`
3. essayez de capturer le rappel sur `http://127.0.0.1:1455/auth/callback`
4. si le rappel ne peut pas se lier (ou vous êtes à distance/sans interface), collez l'URL/code de redirection
5. échangez à `https://auth.openai.com/oauth/token`
6. extrayez `accountId` du jeton d'accès et stockez `{ access, refresh, expires, accountId }`

Le chemin de l'assistant est `openclaw onboard` → choix d'authentification `openai-codex`.

## Rafraîchissement + expiration

Les profils stockent un horodatage `expires`.

À l'exécution :

- si `expires` est dans le futur → utilisez le jeton d'accès stocké
- s'il a expiré → rafraîchissez (sous un verrou de fichier) et remplacez les identifiants stockés

Le flux de rafraîchissement est automatique ; vous n'avez généralement pas besoin de gérer les jetons manuellement.

## Comptes multiples (profils) + routage

Deux modèles :

### 1) Préféré : agents séparés

Si vous voulez que « personnel » et « travail » ne s'interagissent jamais, utilisez des agents isolés (sessions séparées + identifiants + espace de travail) :

```bash
openclaw agents add work
openclaw agents add personal
```

Ensuite, configurez l'authentification par agent (assistant) et routez les chats vers le bon agent.

### 2) Avancé : plusieurs profils dans un agent

`auth-profiles.json` supporte plusieurs ID de profil pour le même fournisseur.

Choisissez quel profil est utilisé :

- globalement via l'ordre de configuration (`auth.order`)
- par session via `/model ...@<profileId>`

Exemple (remplacement de session) :

- `/model Opus@anthropic:work`

Comment voir quels ID de profil existent :

- `openclaw channels list --json` (affiche `auth[]`)

Docs connexes :

- [/concepts/model-failover](/fr/concepts/model-failover) (règles de rotation + refroidissement)
- [/tools/slash-commands](/fr/tools/slash-commands) (surface de commande)
