---
read_when:
  - Vous migrez OpenClaw vers un nouvel ordinateur portable/serveur
  - Vous souhaitez conserver les sessions, l'authentification et les connexions aux canaux (WhatsApp, etc.)
summary: Migrer une installation OpenClaw d'une machine à une autre
title: Guide de migration
x-i18n:
  generated_at: "2026-02-03T07:49:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 604d862c4bf86e7924d09028db8cc2514ca6f1d64ebe8bb7d1e2dde57ef70caa
  source_path: install/migrating.md
  workflow: 15
---

# Migrer OpenClaw vers une nouvelle machine

Ce guide migre la passerelle OpenClaw Gateway d'une machine à une autre, **sans refaire l'onboarding**.

La migration est conceptuellement simple :

- Copiez le **répertoire d'état** (`$OPENCLAW_STATE_DIR`, par défaut : `~/.openclaw/`) — cela inclut la configuration, l'authentification, les sessions et l'état des canaux.
- Copiez votre **espace de travail** (par défaut `~/.openclaw/workspace/`) — cela inclut vos fichiers d'agent (mémoire, invites, etc.).

Mais il y a des pièges courants avec les **fichiers de configuration**, les **permissions** et les **copies partielles**.

## Avant de commencer (qu'allez-vous migrer)

### 1) Identifiez votre répertoire d'état

La plupart des installations utilisent la valeur par défaut :

- **Répertoire d'état :** `~/.openclaw/`

Mais cela peut être différent si vous utilisez :

- `--profile <name>` (devient généralement `~/.openclaw-<profile>/`)
- `OPENCLAW_STATE_DIR=/some/path`

Si vous n'êtes pas sûr, exécutez sur l'**ancienne** machine :

```bash
openclaw status
```

Recherchez les mentions de `OPENCLAW_STATE_DIR` / profil dans la sortie. Si vous exécutez plusieurs passerelles Gateway, répétez cette opération pour chaque profil.

### 2) Identifiez votre espace de travail

Valeurs par défaut courantes :

- `~/.openclaw/workspace/` (espace de travail recommandé)
- Un dossier personnalisé que vous avez créé

Votre espace de travail est l'endroit où se trouvent les fichiers comme `MEMORY.md`, `USER.md` et `memory/*.md`.

### 3) Comprenez ce que vous allez conserver

Si vous copiez **les deux** — répertoire d'état et espace de travail, vous conserverez :

- Configuration de la passerelle Gateway (`openclaw.json`)
- Fichiers d'authentification / clés API / jetons OAuth
- Historique des sessions + état de l'agent
- État des canaux (par exemple, connexion/sessions WhatsApp)
- Vos fichiers d'espace de travail (mémoire, notes Skills, etc.)

Si vous copiez **uniquement** l'espace de travail (par exemple via Git), vous **ne conserverez pas** :

- Les sessions
- Les identifiants
- Les connexions aux canaux

Ceux-ci sont stockés sous `$OPENCLAW_STATE_DIR`.

## Étapes de migration (recommandées)

### Étape 0 — Sauvegarde (ancienne machine)

Sur l'**ancienne** machine, arrêtez d'abord la passerelle Gateway pour que les fichiers ne changent pas pendant la copie :

```bash
openclaw gateway stop
```

(Optionnel mais recommandé) Archivez le répertoire d'état et l'espace de travail :

```bash
# Ajustez les chemins si vous utilisez des profils ou des emplacements personnalisés
cd ~
tar -czf openclaw-state.tgz .openclaw

tar -czf openclaw-workspace.tgz .openclaw/workspace
```

Si vous avez plusieurs profils/répertoires d'état (par exemple `~/.openclaw-main`, `~/.openclaw-work`), archivez chacun séparément.

### Étape 1 — Installez OpenClaw sur la nouvelle machine

Sur la **nouvelle** machine, installez la CLI (et Node si nécessaire) :

- Voir : [Installation](/install)

À ce stade, il n'y a pas de problème si l'onboarding crée un nouveau `~/.openclaw/` — vous le remplacerez à l'étape suivante.

### Étape 2 — Copiez le répertoire d'état + l'espace de travail vers la nouvelle machine

Copiez **les deux** :

- `$OPENCLAW_STATE_DIR` (par défaut `~/.openclaw/`)
- Votre espace de travail (par défaut `~/.openclaw/workspace/`)

Méthodes courantes :

- `scp` les archives et décompressez-les
- `rsync -a` via SSH
- Lecteur externe

Après la copie, assurez-vous que :

- Les répertoires cachés sont inclus (par exemple `.openclaw/`)
- La propriété des fichiers est correcte pour l'utilisateur exécutant la passerelle Gateway

### Étape 3 — Exécutez Doctor (migration + correction des services)

Sur la **nouvelle** machine :

```bash
openclaw doctor
```

Doctor est une commande « sûre et fiable ». Elle corrige les services, applique les migrations de configuration et avertit des problèmes de non-concordance.

Ensuite :

```bash
openclaw gateway restart
openclaw status
```

## Pièges courants (et comment les éviter)

### Piège : profil/répertoire d'état non concordant

Si vous avez utilisé un profil sur l'ancienne passerelle Gateway (ou `OPENCLAW_STATE_DIR`), et que la nouvelle passerelle utilise un profil différent, vous verrez des symptômes comme :

- Les modifications de configuration ne prennent pas effet
- Les canaux sont perdus/déconnectés
- L'historique des sessions est vide

Correction : exécutez la passerelle Gateway/service avec le **même** profil/répertoire d'état que celui que vous avez migré, puis réexécutez :

```bash
openclaw doctor
```

### Piège : copier uniquement `openclaw.json`

`openclaw.json` seul ne suffit pas. De nombreux fournisseurs stockent l'état dans :

- `$OPENCLAW_STATE_DIR/credentials/`
- `$OPENCLAW_STATE_DIR/agents/<agentId>/...`

Migrez toujours le dossier `$OPENCLAW_STATE_DIR` entier.

### Piège : permissions/propriété

Si vous avez copié en tant que root ou changé d'utilisateur, la passerelle Gateway peut ne pas pouvoir lire les identifiants/sessions.

Correction : assurez-vous que le répertoire d'état + l'espace de travail sont possédés par l'utilisateur exécutant la passerelle Gateway.

### Piège : migration entre modes distant/local

- Si votre interface utilisateur (WebUI/TUI) pointe vers une passerelle Gateway **distante**, l'hôte distant possède le stockage des sessions + l'espace de travail.
- Migrer votre ordinateur portable ne déplacera pas l'état de la passerelle Gateway distante.

Si vous êtes en mode distant, migrez l'**hôte de la passerelle Gateway**.

### Piège : clés dans les sauvegardes

`$OPENCLAW_STATE_DIR` contient des clés (clés API, jetons OAuth, identifiants WhatsApp). Traitez les sauvegardes comme des clés de production :

- Stockez-les chiffrées
- Évitez de les partager via des canaux non sécurisés
- Si une fuite est suspectée, renouvelez les clés

## Liste de contrôle de vérification

Sur la nouvelle machine, confirmez que :

- `openclaw status` affiche que la passerelle Gateway est en cours d'exécution
- Vos canaux sont toujours connectés (par exemple, WhatsApp n'a pas besoin d'être réappairé)
- Le tableau de bord s'ouvre et affiche les sessions existantes
- Vos fichiers d'espace de travail (mémoire, configuration) existent

## Contenu connexe

- [Doctor](/gateway/doctor)
- [Dépannage de la passerelle Gateway](/gateway/troubleshooting)
- [Où OpenClaw stocke-t-il ses données ?](/help/faq#where-does-openclaw-store-its-data)
