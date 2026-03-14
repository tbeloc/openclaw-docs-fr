```markdown
---
read_when:
  - 更新 OpenClaw
  - 更新后出现问题
summary: 安全更新 OpenClaw（全局安装或源码），以及回滚策略
title: 更新
x-i18n:
  generated_at: "2026-02-03T07:50:25Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 38cccac0839f0f22403b6508cd94ba1b401133ffc1d92d4f7640b8d04e082317
  source_path: install/updating.md
  workflow: 15
---

# Mise à jour

OpenClaw évolue rapidement (pas encore à la version "1.0"). Considérez les mises à jour comme une infrastructure de publication : mise à jour → exécution des vérifications → redémarrage (ou utilisation de `openclaw update` qui redémarre) → vérification.

## Recommandé : réexécuter le programme d'installation du site (mise à niveau sur place)

Le chemin de mise à jour **préféré** est de réexécuter le programme d'installation sur le site. Il détecte l'installation existante, effectue une mise à niveau sur place et exécute `openclaw doctor` si nécessaire.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Notes :

- Si vous ne souhaitez pas réexécuter l'assistant d'intégration, ajoutez `--no-onboard`.
- Pour les **installations à partir du code source**, utilisez :
  ```bash
  curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-onboard
  ```
  Le programme d'installation exécutera `git pull --rebase` **uniquement** si le référentiel est propre.
- Pour les **installations globales**, le script utilise en arrière-plan `npm install -g openclaw@latest`.
- Notes héritées : `clawdbot` peut toujours être utilisé comme shim de compatibilité.

## Avant la mise à jour

- Connaître votre méthode d'installation : **globale** (npm/pnpm) ou **source** (git clone).
- Connaître votre mode d'exécution de la passerelle : **terminal au premier plan** ou **service géré** (launchd/systemd).
- Créer un instantané de vos personnalisations :
  - Configuration : `~/.openclaw/openclaw.json`
  - Identifiants : `~/.openclaw/credentials/`
  - Espace de travail : `~/.openclaw/workspace`

## Mise à jour (installation globale)

Installation globale (choisissez l'une des deux) :

```bash
npm i -g openclaw@latest
```

```bash
pnpm add -g openclaw@latest
```

Nous **ne recommandons pas** d'utiliser Bun pour l'exécution de la passerelle (bugs avec WhatsApp/Telegram).

Basculer les canaux de mise à jour (installation git + npm) :

```bash
openclaw update --channel beta
openclaw update --channel dev
openclaw update --channel stable
```

Utilisez `--tag <dist-tag|version>` pour une installation unique d'une balise/version spécifique.

Pour la sémantique des canaux et les notes de publication, consultez [Canaux de développement](/install/development-channels).

Remarque : lors d'une installation npm, la passerelle enregistre une notification de mise à jour au démarrage (vérification de la balise du canal actuel). Désactivez avec `update.checkOnStart: false`.

Ensuite :

```bash
openclaw doctor
openclaw gateway restart
openclaw health
```

Notes :

- Si votre passerelle s'exécute en tant que service, `openclaw gateway restart` est préférable à tuer le PID.
- Si vous êtes épinglé à une version spécifique, consultez "Restauration/Épinglage" ci-dessous.

## Mise à jour (`openclaw update`)

Pour les **installations à partir du code source** (git checkout), préféré :

```bash
openclaw update
```

Il exécute un processus de mise à jour relativement sûr :

- Nécessite un arbre de travail propre.
- Bascule vers le canal sélectionné (balise ou branche).
- Récupère et rebase vers l'amont configuré (canal dev).
- Installe les dépendances, construit, construit l'interface utilisateur de contrôle et exécute `openclaw doctor`.
- Redémarre la passerelle par défaut (utilisez `--no-restart` pour ignorer).

Si vous avez installé via **npm/pnpm** (sans métadonnées git), `openclaw update` tentera de mettre à jour via votre gestionnaire de paquets. Si l'installation ne peut pas être détectée, utilisez plutôt "Mise à jour (installation globale)".

## Mise à jour (interface utilisateur de contrôle / RPC)

L'interface utilisateur de contrôle a **Mettre à jour et redémarrer** (RPC : `update.run`). Elle :

1. Exécute le même processus de mise à jour du code source que `openclaw update` (git checkout uniquement).
2. Écrit une sentinelle de redémarrage avec un rapport structuré (queue stdout/stderr).
3. Redémarre la passerelle et envoie un ping du rapport à la dernière session active.

Si le rebase échoue, la passerelle s'arrête et redémarre sans appliquer la mise à jour.

## Mise à jour (à partir du code source)

À partir du checkout du référentiel :

Préféré :

```bash
openclaw update
```

Manuel (à peu près équivalent) :

```bash
git pull
pnpm install
pnpm build
pnpm ui:build # Installe automatiquement les dépendances de l'interface utilisateur à la première exécution
openclaw doctor
openclaw health
```

Notes :

- `pnpm build` est important lorsque vous exécutez le binaire `openclaw` empaqueté ([`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs)) ou utilisez Node pour exécuter `dist/`.
- Si vous exécutez à partir du checkout du référentiel sans installation globale, les commandes CLI utilisent `pnpm openclaw ...`.
- Si vous exécutez directement à partir de TypeScript (`pnpm openclaw ...`), la reconstruction n'est généralement pas nécessaire, mais **les migrations de configuration s'appliquent toujours** → exécutez doctor.
- Basculer entre les installations globales et git est facile : installez l'autre méthode, puis exécutez `openclaw doctor` pour que le point d'entrée du service de passerelle soit réécrit pour l'installation actuelle.

## Toujours exécuter : `openclaw doctor`

Doctor est la commande "mise à jour sécurisée". Elle est intentionnellement ennuyeuse : corrections + migrations + avertissements.

Remarque : si vous êtes une **installation à partir du code source** (git checkout), `openclaw doctor` suggère d'exécuter d'abord `openclaw update`.

Ce qu'elle fait généralement :

- Migre les clés de configuration dépréciées/emplacements de fichiers de configuration hérités.
- Audite les politiques de messages privés et avertit sur les paramètres "ouverts" risqués.
- Vérifie la santé de la passerelle, peut proposer un redémarrage.
- Détecte et migre les services de passerelle hérités (launchd/systemd ; ancien schtasks) vers le service OpenClaw actuel.
- Sur Linux, assure la persistance de l'utilisateur systemd (afin que la passerelle survive après la déconnexion).

Détails : [Doctor](/gateway/doctor)

## Démarrer/arrêter/redémarrer la passerelle

CLI (fonctionne sur tous les systèmes d'exploitation) :

```bash
openclaw gateway status
openclaw gateway stop
openclaw gateway restart
openclaw gateway --port 18789
openclaw logs --follow
```

Si vous utilisez un service géré :

- macOS launchd (LaunchAgent fourni avec l'application) : `launchctl kickstart -k gui/$UID/bot.molt.gateway` (utilisez `bot.molt.<profile>` ; ancien `com.openclaw.*` fonctionne toujours)
- Service utilisateur Linux systemd : `systemctl --user restart openclaw-gateway[-<profile>].service`
- Windows (WSL2) : `systemctl --user restart openclaw-gateway[-<profile>].service`
  - `launchctl`/`systemctl` ne fonctionnent que si le service est installé ; sinon, exécutez `openclaw gateway install`.

Manuel d'exécution + étiquettes de service exactes : [Manuel de la passerelle](/gateway)

## Restauration/Épinglage (en cas de problème)

### Épinglage (installation globale)

Installez une version connue comme bonne (remplacez `<version>` par la dernière version disponible) :

```bash
npm i -g openclaw@<version>
```

```bash
pnpm add -g openclaw@<version>
```

Conseil : pour voir les versions actuellement publiées, exécutez `npm view openclaw version`.

Puis redémarrez et réexécutez doctor :

```bash
openclaw doctor
openclaw gateway restart
```

### Épinglage par date (source)

Sélectionnez un commit à une certaine date (exemple : "état de main au 2026-01-01") :

```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
```

Puis réinstallez les dépendances et redémarrez :

```bash
pnpm install
pnpm build
openclaw gateway restart
```

Si vous souhaitez revenir à la dernière version par la suite :

```bash
git checkout main
git pull
```

## Si vous êtes bloqué

- Réexécutez `openclaw doctor` et lisez attentivement la sortie (elle vous dit généralement comment corriger).
- Consultez : [Dépannage](/gateway/troubleshooting)
- Posez une question sur Discord : https://discord.gg/clawd
```
