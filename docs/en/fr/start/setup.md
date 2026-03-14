---
summary: "Configuration avancée et flux de travail de développement pour OpenClaw"
read_when:
  - Configuration d'une nouvelle machine
  - Vous voulez la "dernière version" sans casser votre configuration personnelle
title: "Configuration"
---

# Configuration

<Note>
Si vous configurez pour la première fois, commencez par [Démarrage](/start/getting-started).
Pour plus de détails sur l'assistant, voir [Assistant d'intégration](/start/wizard).
</Note>

Dernière mise à jour : 2026-01-01

## TL;DR

- **La personnalisation se fait en dehors du repo :** `~/.openclaw/workspace` (espace de travail) + `~/.openclaw/openclaw.json` (config).
- **Flux de travail stable :** installez l'app macOS ; laissez-la exécuter la Gateway intégrée.
- **Flux de travail à la pointe :** exécutez la Gateway vous-même via `pnpm gateway:watch`, puis laissez l'app macOS se connecter en mode Local.

## Prérequis (à partir des sources)

- Node `>=22`
- `pnpm`
- Docker (optionnel ; uniquement pour la configuration conteneurisée/e2e — voir [Docker](/install/docker))

## Stratégie de personnalisation (pour que les mises à jour ne posent pas problème)

Si vous voulez "100% personnalisé pour moi" _et_ des mises à jour faciles, gardez votre personnalisation dans :

- **Config :** `~/.openclaw/openclaw.json` (JSON/JSON5-ish)
- **Espace de travail :** `~/.openclaw/workspace` (compétences, invites, mémoires ; faites-en un repo git privé)

Amorçage unique :

```bash
openclaw setup
```

Depuis l'intérieur de ce repo, utilisez l'entrée CLI locale :

```bash
openclaw setup
```

Si vous n'avez pas encore d'installation globale, exécutez-la via `pnpm openclaw setup`.

## Exécuter la Gateway à partir de ce repo

Après `pnpm build`, vous pouvez exécuter directement la CLI empaquetée :

```bash
node openclaw.mjs gateway --port 18789 --verbose
```

## Flux de travail stable (app macOS en premier)

1. Installez et lancez **OpenClaw.app** (barre de menu).
2. Complétez la liste de contrôle d'intégration/permissions (invites TCC).
3. Assurez-vous que la Gateway est **Local** et en cours d'exécution (l'app la gère).
4. Liez les surfaces (exemple : WhatsApp) :

```bash
openclaw channels login
```

5. Vérification de santé :

```bash
openclaw health
```

Si l'intégration n'est pas disponible dans votre build :

- Exécutez `openclaw setup`, puis `openclaw channels login`, puis démarrez la Gateway manuellement (`openclaw gateway`).

## Flux de travail à la pointe (Gateway dans un terminal)

Objectif : travailler sur la Gateway TypeScript, obtenir le rechargement à chaud, garder l'interface macOS attachée.

### 0) (Optionnel) Exécutez aussi l'app macOS à partir des sources

Si vous voulez aussi l'app macOS à la pointe :

```bash
./scripts/restart-mac.sh
```

### 1) Démarrez la Gateway de développement

```bash
pnpm install
pnpm gateway:watch
```

`gateway:watch` exécute la gateway en mode watch et recharge lors des changements TypeScript.

### 2) Pointez l'app macOS vers votre Gateway en cours d'exécution

Dans **OpenClaw.app** :

- Mode de connexion : **Local**
  L'app se connectera à la gateway en cours d'exécution sur le port configuré.

### 3) Vérifiez

- Le statut de la Gateway dans l'app devrait afficher **"Using existing gateway …"**
- Ou via CLI :

```bash
openclaw health
```

### Pièges courants

- **Mauvais port :** La Gateway WS par défaut est `ws://127.0.0.1:18789` ; gardez l'app et la CLI sur le même port.
- **Où l'état est stocké :**
  - Identifiants : `~/.openclaw/credentials/`
  - Sessions : `~/.openclaw/agents/<agentId>/sessions/`
  - Logs : `/tmp/openclaw/`

## Carte de stockage des identifiants

Utilisez ceci lors du débogage de l'authentification ou pour décider ce qu'il faut sauvegarder :

- **WhatsApp** : `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- **Jeton bot Telegram** : config/env ou `channels.telegram.tokenFile` (fichier régulier uniquement ; les symlinks sont rejetés)
- **Jeton bot Discord** : config/env ou SecretRef (fournisseurs env/file/exec)
- **Jetons Slack** : config/env (`channels.slack.*`)
- **Listes blanches d'appairage** :
  - `~/.openclaw/credentials/<channel>-allowFrom.json` (compte par défaut)
  - `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json` (comptes non-défaut)
- **Profils d'authentification du modèle** : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **Charge utile de secrets sauvegardée sur fichier (optionnel)** : `~/.openclaw/secrets.json`
- **Import OAuth hérité** : `~/.openclaw/credentials/oauth.json`
  Plus de détails : [Sécurité](/gateway/security#credential-storage-map).

## Mise à jour (sans casser votre configuration)

- Gardez `~/.openclaw/workspace` et `~/.openclaw/` comme "vos affaires" ; ne mettez pas d'invites/config personnelles dans le repo `openclaw`.
- Mise à jour des sources : `git pull` + `pnpm install` (quand le lockfile a changé) + continuez à utiliser `pnpm gateway:watch`.

## Linux (service utilisateur systemd)

Les installations Linux utilisent un service utilisateur **user** systemd. Par défaut, systemd arrête les services utilisateur à la déconnexion/inactivité, ce qui tue la Gateway. L'intégration tente d'activer la persistance pour vous (peut demander sudo). Si c'est toujours désactivé, exécutez :

```bash
sudo loginctl enable-linger $USER
```

Pour les serveurs toujours actifs ou multi-utilisateurs, envisagez un service **système** au lieu d'un service utilisateur (pas besoin de persistance). Voir [Runbook Gateway](/gateway) pour les notes systemd.

## Documentation connexe

- [Runbook Gateway](/gateway) (drapeaux, supervision, ports)
- [Configuration Gateway](/gateway/configuration) (schéma de config + exemples)
- [Discord](/channels/discord) et [Telegram](/channels/telegram) (balises de réponse + paramètres replyToMode)
- [Configuration de l'assistant OpenClaw](/start/openclaw)
- [App macOS](/platforms/macos) (cycle de vie de la gateway)
