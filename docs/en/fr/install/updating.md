```markdown
---
summary: "Mise à jour sécurisée d'OpenClaw (installation globale ou source), plus stratégie de restauration"
read_when:
  - Updating OpenClaw
  - Something breaks after an update
title: "Mise à jour"
---

# Mise à jour

OpenClaw évolue rapidement (pré "1.0"). Traitez les mises à jour comme une infrastructure : mise à jour → exécution des vérifications → redémarrage (ou utilisez `openclaw update`, qui redémarre) → vérification.

## Recommandé : réexécuter l'installateur du site web (mise à niveau sur place)

Le **chemin de mise à jour préféré** est de réexécuter l'installateur depuis le site web. Il
détecte les installations existantes, effectue une mise à niveau sur place et exécute `openclaw doctor` si
nécessaire.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Notes :

- Ajoutez `--no-onboard` si vous ne voulez pas que l'assistant d'intégration s'exécute à nouveau.
- Pour les **installations à partir de la source**, utilisez :

  ```bash
  curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-onboard
  ```

  L'installateur exécutera `git pull --rebase` **uniquement** si le dépôt est propre.

- Pour les **installations globales**, le script utilise `npm install -g openclaw@latest` en arrière-plan.
- Note héritée : `clawdbot` reste disponible comme shim de compatibilité.

## Avant de mettre à jour

- Sachez comment vous avez installé : **global** (npm/pnpm) vs **à partir de la source** (git clone).
- Sachez comment votre Gateway s'exécute : **terminal au premier plan** vs **service supervisé** (launchd/systemd).
- Prenez un instantané de votre personnalisation :
  - Config : `~/.openclaw/openclaw.json`
  - Identifiants : `~/.openclaw/credentials/`
  - Espace de travail : `~/.openclaw/workspace`

## Mise à jour (installation globale)

Installation globale (choisissez une) :

```bash
npm i -g openclaw@latest
```

```bash
pnpm add -g openclaw@latest
```

Nous **ne recommandons pas** Bun pour le runtime Gateway (bugs WhatsApp/Telegram).

Pour basculer les canaux de mise à jour (installations git + npm) :

```bash
openclaw update --channel beta
openclaw update --channel dev
openclaw update --channel stable
```

Utilisez `--tag <dist-tag|version>` pour une installation unique de tag/version.

Voir [Canaux de développement](/install/development-channels) pour la sémantique des canaux et les notes de version.

Note : sur les installations npm, la gateway enregistre un conseil de mise à jour au démarrage (vérifie le tag du canal actuel). Désactivez via `update.checkOnStart: false`.

### Mise à jour automatique du noyau (optionnel)

La mise à jour automatique est **désactivée par défaut** et est une fonctionnalité de Gateway principale (pas un plugin).

```json
{
  "update": {
    "channel": "stable",
    "auto": {
      "enabled": true,
      "stableDelayHours": 6,
      "stableJitterHours": 12,
      "betaCheckIntervalHours": 1
    }
  }
}
```

Comportement :

- `stable` : quand une nouvelle version est détectée, OpenClaw attend `stableDelayHours` puis applique une gigue déterministe par installation dans `stableJitterHours` (déploiement échelonné).
- `beta` : vérifie selon le cadence `betaCheckIntervalHours` (par défaut : toutes les heures) et applique quand une mise à jour est disponible.
- `dev` : pas d'application automatique ; utilisez `openclaw update` manuel.

Utilisez `openclaw update --dry-run` pour prévisualiser les actions de mise à jour avant d'activer l'automatisation.

Ensuite :

```bash
openclaw doctor
openclaw gateway restart
openclaw health
```

Notes :

- Si votre Gateway s'exécute en tant que service, `openclaw gateway restart` est préféré à l'arrêt des PID.
- Si vous êtes épinglé à une version spécifique, voir "Restauration / épinglage" ci-dessous.

## Mise à jour (`openclaw update`)

Pour les **installations à partir de la source** (git checkout), préférez :

```bash
openclaw update
```

Il exécute un flux de mise à jour relativement sûr :

- Nécessite un arbre de travail propre.
- Bascule vers le canal sélectionné (tag ou branche).
- Récupère + rebase par rapport à l'amont configuré (canal dev).
- Installe les dépendances, construit, construit l'interface utilisateur de contrôle et exécute `openclaw doctor`.
- Redémarre la gateway par défaut (utilisez `--no-restart` pour ignorer).

Si vous avez installé via **npm/pnpm** (pas de métadonnées git), `openclaw update` tentera de mettre à jour via votre gestionnaire de paquets. Si elle ne peut pas détecter l'installation, utilisez plutôt "Mise à jour (installation globale)".

## Mise à jour (Interface utilisateur de contrôle / RPC)

L'interface utilisateur de contrôle a **Mettre à jour et redémarrer** (RPC : `update.run`). Elle :

1. Exécute le même flux de mise à jour source que `openclaw update` (git checkout uniquement).
2. Écrit un sentinel de redémarrage avec un rapport structuré (queue stdout/stderr).
3. Redémarre la gateway et envoie un ping à la dernière session active avec le rapport.

Si le rebase échoue, la gateway abandonne et redémarre sans appliquer la mise à jour.

## Mise à jour (à partir de la source)

À partir du checkout du dépôt :

Préféré :

```bash
openclaw update
```

Manuel (équivalent-ish) :

```bash
git pull
pnpm install
pnpm build
pnpm ui:build # auto-installs UI deps on first run
openclaw doctor
openclaw health
```

Notes :

- `pnpm build` importe quand vous exécutez le binaire `openclaw` empaqueté ([`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs)) ou utilisez Node pour exécuter `dist/`.
- Si vous exécutez à partir d'un checkout de dépôt sans installation globale, utilisez `pnpm openclaw ...` pour les commandes CLI.
- Si vous exécutez directement à partir de TypeScript (`pnpm openclaw ...`), une reconstruction est généralement inutile, mais **les migrations de configuration s'appliquent toujours** → exécutez doctor.
- Basculer entre les installations globales et git est facile : installez l'autre variante, puis exécutez `openclaw doctor` pour que le point d'entrée du service gateway soit réécrit à l'installation actuelle.

## Toujours exécuter : `openclaw doctor`

Doctor est la commande "mise à jour sûre". C'est intentionnellement ennuyeux : réparer + migrer + avertir.

Note : si vous êtes sur une **installation source** (git checkout), `openclaw doctor` proposera d'exécuter d'abord `openclaw update`.

Les choses typiques qu'il fait :

- Migrer les clés de configuration dépréciées / emplacements de fichiers de configuration hérités.
- Auditer les politiques DM et avertir sur les paramètres "ouverts" risqués.
- Vérifier la santé de la Gateway et peut proposer un redémarrage.
- Détecter et migrer les services gateway plus anciens (launchd/systemd ; schtasks hérité) vers les services OpenClaw actuels.
- Sur Linux, assurer la persistance de l'utilisateur systemd (pour que la Gateway survive à la déconnexion).

Détails : [Doctor](/gateway/doctor)

## Démarrer / arrêter / redémarrer la Gateway

CLI (fonctionne quel que soit le système d'exploitation) :

```bash
openclaw gateway status
openclaw gateway stop
openclaw gateway restart
openclaw gateway --port 18789
openclaw logs --follow
```

Si vous êtes supervisé :

- macOS launchd (LaunchAgent fourni avec l'application) : `launchctl kickstart -k gui/$UID/ai.openclaw.gateway` (utilisez `ai.openclaw.<profile>` ; `com.openclaw.*` hérité fonctionne toujours)
- Service utilisateur Linux systemd : `systemctl --user restart openclaw-gateway[-<profile>].service`
- Windows (WSL2) : `systemctl --user restart openclaw-gateway[-<profile>].service`
  - `launchctl`/`systemctl` ne fonctionnent que si le service est installé ; sinon exécutez `openclaw gateway install`.

Runbook + étiquettes de service exactes : [Runbook Gateway](/gateway)

## Restauration / épinglage (quand quelque chose se casse)

### Épingler (installation globale)

Installez une version connue comme bonne (remplacez `<version>` par la dernière qui fonctionnait) :

```bash
npm i -g openclaw@<version>
```

```bash
pnpm add -g openclaw@<version>
```

Conseil : pour voir la version actuellement publiée, exécutez `npm view openclaw version`.

Ensuite redémarrez + réexécutez doctor :

```bash
openclaw doctor
openclaw gateway restart
```

### Épingler (source) par date

Choisissez un commit à partir d'une date (exemple : "état de main au 2026-01-01") :

```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
```

Ensuite réinstallez les dépendances + redémarrez :

```bash
pnpm install
pnpm build
openclaw gateway restart
```

Si vous voulez revenir à la dernière version plus tard :

```bash
git checkout main
git pull
```

## Si vous êtes bloqué

- Exécutez `openclaw doctor` à nouveau et lisez attentivement la sortie (elle vous dit souvent la correction).
- Vérifiez : [Dépannage](/gateway/troubleshooting)
- Demandez sur Discord : [https://discord.gg/clawd](https://discord.gg/clawd)
```
