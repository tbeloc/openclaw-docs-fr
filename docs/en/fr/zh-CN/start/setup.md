---
read_when:
  - Configurer une nouvelle machine
  - Vous voulez « le dernier et le meilleur » sans casser vos paramètres personnels
summary: Guide de configuration : Gardez vos paramètres OpenClaw personnalisés tout en restant à jour
title: Configuration
x-i18n:
  generated_at: "2026-02-03T07:54:27Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b7f4bd657d0df4feb5035c9f5ee727f9c67b991e9cedfc7768f99d010553fa01
  source_path: start/setup.md
  workflow: 15
---

# Configuration

Dernière mise à jour : 2026-01-01

## Trop long ; pas lu

- **Les paramètres personnalisés vivent en dehors du dépôt :** `~/.openclaw/workspace` (espace de travail) + `~/.openclaw/openclaw.json` (configuration).
- **Flux de travail stable :** Installez l'application macOS ; laissez-la exécuter la passerelle intégrée.
- **Flux de travail de pointe :** Exécutez vous-même la passerelle via `pnpm gateway:watch`, puis laissez l'application macOS se connecter en mode local.

## Prérequis (à partir de la source)

- Node `>=22`
- `pnpm`
- Docker (optionnel ; uniquement pour les configurations conteneurisées/e2e — voir [Docker](/install/docker))

## Stratégie de personnalisation (pour que les mises à jour ne causent pas de problèmes)

Si vous voulez « 100% personnalisé pour moi » *et* facile à mettre à jour, conservez vos personnalisations dans :

- **Configuration :** `~/.openclaw/openclaw.json` (format JSON/JSON5)
- **Espace de travail :** `~/.openclaw/workspace` (Skills, invites, mémoire ; rendez-le un dépôt git privé)

Amorcer une fois :

```bash
openclaw setup
```

À l'intérieur de ce dépôt, utilisez l'entrée CLI locale :

```bash
openclaw setup
```

Si vous ne l'avez pas installé globalement, exécutez-le via `pnpm openclaw setup`.

## Flux de travail stable (application macOS en premier)

1. Installez et lancez **OpenClaw.app** (barre de menu).
2. Complétez l'assistant de configuration/liste de contrôle des autorisations (invites TCC).
3. Assurez-vous que la passerelle est **locale** et en cours d'exécution (l'application la gère).
4. Canaux de liaison (exemple : WhatsApp) :

```bash
openclaw channels login
```

5. Vérification d'intégrité :

```bash
openclaw health
```

Si votre version compilée n'a pas d'assistant de configuration :

- Exécutez `openclaw setup`, puis `openclaw channels login`, puis démarrez manuellement la passerelle (`openclaw gateway`).

## Flux de travail de pointe (exécuter la passerelle dans le terminal)

Objectif : Développer la passerelle TypeScript, obtenir le rechargement à chaud, garder l'interface utilisateur de l'application macOS connectée.

### 0) (Optionnel) Exécutez également l'application macOS à partir de la source

Si vous voulez aussi garder l'application macOS de pointe :

```bash
./scripts/restart-mac.sh
```

### 1) Démarrer la passerelle de développement

```bash
pnpm install
pnpm gateway:watch
```

`gateway:watch` exécute la passerelle en mode surveillance et recharge lorsque TypeScript change.

### 2) Pointez l'application macOS vers votre passerelle en cours d'exécution

Dans **OpenClaw.app** :

- Mode de connexion : **Local**
  L'application se connectera à la passerelle en cours d'exécution sur le port configuré.

### 3) Vérifier

- L'état de la passerelle dans l'application devrait afficher **« Using existing gateway … »**
- Ou via CLI :

```bash
openclaw health
```

### Pièges courants

- **Erreur de port :** La passerelle WS par défaut est `ws://127.0.0.1:18789` ; gardez l'application + CLI sur le même port.
- **Emplacements de stockage d'état :**
  - Identifiants : `~/.openclaw/credentials/`
  - Sessions : `~/.openclaw/agents/<agentId>/sessions/`
  - Journaux : `/tmp/openclaw/`

## Mappage du stockage des identifiants

Utilisez ce mappage lors du débogage de l'authentification ou de la décision de ce qu'il faut sauvegarder :

- **WhatsApp** : `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- **Jeton bot Telegram** : Configuration/variables d'environnement ou `channels.telegram.tokenFile`
- **Jeton bot Discord** : Configuration/variables d'environnement (fichier de jeton non encore supporté)
- **Jetons Slack** : Configuration/variables d'environnement (`channels.slack.*`)
- **Liste blanche d'appairage** : `~/.openclaw/credentials/<channel>-allowFrom.json`
- **Profils d'authentification du modèle** : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **Importation OAuth héritée** : `~/.openclaw/credentials/oauth.json`
  Plus de détails : [Sécurité](/gateway/security#credential-storage-map).

## Mise à jour (sans casser vos paramètres)

- Gardez `~/.openclaw/workspace` et `~/.openclaw/` comme « vos affaires » ; ne mettez pas d'invites/configurations personnelles dans le dépôt `openclaw`.
- Mettez à jour la source : `git pull` + `pnpm install` (lorsque le fichier de verrouillage change) + continuez à utiliser `pnpm gateway:watch`.

## Linux (service utilisateur systemd)

L'installation Linux utilise un service utilisateur systemd. Par défaut, systemd arrête les services utilisateur à la déconnexion/inactivité, ce qui termine la passerelle. L'assistant de configuration tentera d'activer lingering pour vous (peut demander sudo). S'il s'arrête toujours, exécutez :

```bash
sudo loginctl enable-linger $USER
```

Pour les serveurs résidents ou multi-utilisateurs, envisagez d'utiliser un service **système** au lieu d'un service utilisateur (pas besoin de lingering). Voir [Manuel de la passerelle](/gateway) pour les instructions systemd.

## Documentation connexe

- [Manuel de la passerelle](/gateway) (drapeaux, supervision, ports)
- [Configuration de la passerelle](/gateway/configuration) (schémas de configuration + exemples)
- [Discord](/channels/discord) et [Telegram](/channels/telegram) (balises de réponse + paramètres replyToMode)
- [Configuration de l'assistant OpenClaw](/start/openclaw)
- [Application macOS](/platforms/macos) (cycle de vie de la passerelle)
