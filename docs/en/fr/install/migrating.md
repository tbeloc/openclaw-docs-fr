---
summary: "Déplacer (migrer) une installation OpenClaw d'une machine à une autre"
read_when:
  - You are moving OpenClaw to a new laptop/server
  - You want to preserve sessions, auth, and channel logins (WhatsApp, etc.)
title: "Guide de migration"
---

# Migration d'OpenClaw vers une nouvelle machine

Ce guide migre une passerelle OpenClaw d'une machine à une autre **sans refaire l'intégration initiale**.

La migration est simple conceptuellement :

- Copiez le **répertoire d'état** (`$OPENCLAW_STATE_DIR`, par défaut : `~/.openclaw/`) — cela inclut la configuration, l'authentification, les sessions et l'état des canaux.
- Copiez votre **espace de travail** (`~/.openclaw/workspace/` par défaut) — cela inclut vos fichiers d'agent (mémoire, invites, etc.).

Mais il y a des pièges courants autour des **profils**, des **permissions** et des **copies partielles**.

## Avant de commencer (ce que vous migrez)

### 1) Identifiez votre répertoire d'état

La plupart des installations utilisent la valeur par défaut :

- **Répertoire d'état :** `~/.openclaw/`

Mais il peut être différent si vous utilisez :

- `--profile <name>` (devient souvent `~/.openclaw-<profile>/`)
- `OPENCLAW_STATE_DIR=/some/path`

Si vous n'êtes pas sûr, exécutez sur l'**ancienne** machine :

```bash
openclaw status
```

Recherchez les mentions de `OPENCLAW_STATE_DIR` / profil dans la sortie. Si vous exécutez plusieurs passerelles, répétez pour chaque profil.

### 2) Identifiez votre espace de travail

Valeurs par défaut courantes :

- `~/.openclaw/workspace/` (espace de travail recommandé)
- un dossier personnalisé que vous avez créé

Votre espace de travail est l'endroit où vivent des fichiers comme `MEMORY.md`, `USER.md` et `memory/*.md`.

### 3) Comprenez ce que vous allez préserver

Si vous copiez **à la fois** le répertoire d'état et l'espace de travail, vous conservez :

- Configuration de la passerelle (`openclaw.json`)
- Profils d'authentification / clés API / jetons OAuth
- Historique des sessions + état de l'agent
- État des canaux (par exemple, connexion/session WhatsApp)
- Vos fichiers d'espace de travail (mémoire, notes de compétences, etc.)

Si vous copiez **uniquement** l'espace de travail (par exemple, via Git), vous ne préservez **pas** :

- les sessions
- les identifiants
- les connexions aux canaux

Ceux-ci se trouvent sous `$OPENCLAW_STATE_DIR`.

## Étapes de migration (recommandées)

### Étape 0 — Faire une sauvegarde (ancienne machine)

Sur l'**ancienne** machine, arrêtez d'abord la passerelle pour que les fichiers ne changent pas pendant la copie :

```bash
openclaw gateway stop
```

(Optionnel mais recommandé) archivez le répertoire d'état et l'espace de travail :

```bash
# Ajustez les chemins si vous utilisez un profil ou des emplacements personnalisés
cd ~
tar -czf openclaw-state.tgz .openclaw

tar -czf openclaw-workspace.tgz .openclaw/workspace
```

Si vous avez plusieurs profils/répertoires d'état (par exemple `~/.openclaw-main`, `~/.openclaw-work`), archivez chacun.

### Étape 1 — Installer OpenClaw sur la nouvelle machine

Sur la **nouvelle** machine, installez l'interface de ligne de commande (et Node si nécessaire) :

- Voir : [Install](/install)

À ce stade, il est OK si l'intégration initiale crée un `~/.openclaw/` frais — vous le remplacerez à l'étape suivante.

### Étape 2 — Copier le répertoire d'état + l'espace de travail vers la nouvelle machine

Copiez **les deux** :

- `$OPENCLAW_STATE_DIR` (par défaut `~/.openclaw/`)
- votre espace de travail (par défaut `~/.openclaw/workspace/`)

Approches courantes :

- `scp` les archives et extraire
- `rsync -a` sur SSH
- lecteur externe

Après la copie, assurez-vous que :

- Les répertoires cachés ont été inclus (par exemple `.openclaw/`)
- La propriété des fichiers est correcte pour l'utilisateur exécutant la passerelle

### Étape 3 — Exécuter Doctor (migrations + réparation de service)

Sur la **nouvelle** machine :

```bash
openclaw doctor
```

Doctor est la commande « sûre et ennuyeuse ». Elle répare les services, applique les migrations de configuration et avertit des incompatibilités.

Ensuite :

```bash
openclaw gateway restart
openclaw status
```

## Pièges courants (et comment les éviter)

### Piège : incompatibilité profil / répertoire d'état

Si vous avez exécuté l'ancienne passerelle avec un profil (ou `OPENCLAW_STATE_DIR`), et que la nouvelle passerelle en utilise un différent, vous verrez des symptômes comme :

- les modifications de configuration ne prennent pas effet
- les canaux manquent / déconnectés
- historique des sessions vide

Correction : exécutez la passerelle/service en utilisant le **même** profil/répertoire d'état que celui que vous avez migré, puis réexécutez :

```bash
openclaw doctor
```

### Piège : copier uniquement `openclaw.json`

`openclaw.json` ne suffit pas. De nombreux fournisseurs stockent l'état sous :

- `$OPENCLAW_STATE_DIR/credentials/`
- `$OPENCLAW_STATE_DIR/agents/<agentId>/...`

Migrez toujours le dossier `$OPENCLAW_STATE_DIR` entier.

### Piège : permissions / propriété

Si vous avez copié en tant que root ou changé d'utilisateurs, la passerelle peut ne pas pouvoir lire les identifiants/sessions.

Correction : assurez-vous que le répertoire d'état + l'espace de travail sont possédés par l'utilisateur exécutant la passerelle.

### Piège : migration entre modes distant/local

- Si votre interface utilisateur (WebUI/TUI) pointe vers une passerelle **distante**, l'hôte distant possède le magasin de sessions + l'espace de travail.
- La migration de votre ordinateur portable ne déplacera pas l'état de la passerelle distante.

Si vous êtes en mode distant, migrez l'**hôte de la passerelle**.

### Piège : secrets dans les sauvegardes

`$OPENCLAW_STATE_DIR` contient des secrets (clés API, jetons OAuth, identifiants WhatsApp). Traitez les sauvegardes comme des secrets de production :

- stockez chiffré
- évitez de partager sur des canaux non sécurisés
- renouvelez les clés si vous soupçonnez une exposition

## Liste de vérification de vérification

Sur la nouvelle machine, confirmez :

- `openclaw status` affiche la passerelle en cours d'exécution
- Vos canaux sont toujours connectés (par exemple, WhatsApp ne nécessite pas de réappairage)
- Le tableau de bord s'ouvre et affiche les sessions existantes
- Vos fichiers d'espace de travail (mémoire, configurations) sont présents

## Connexes

- [Doctor](/gateway/doctor)
- [Dépannage de la passerelle](/gateway/troubleshooting)
- [Où OpenClaw stocke-t-il ses données ?](/help/faq#where-does-openclaw-store-its-data)
