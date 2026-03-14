---
summary: "Exécuter OpenClaw dans un conteneur Podman sans root"
read_when:
  - You want a containerized gateway with Podman instead of Docker
title: "Podman"
---

# Podman

Exécutez la passerelle OpenClaw dans un conteneur Podman **sans root**. Utilise la même image que Docker (construite à partir du [Dockerfile](https://github.com/openclaw/openclaw/blob/main/Dockerfile) du dépôt).

## Prérequis

- Podman (sans root)
- Sudo pour la configuration initiale (créer un utilisateur, construire l'image)

## Démarrage rapide

**1. Configuration initiale** (à partir de la racine du dépôt ; crée un utilisateur, construit l'image, installe le script de lancement) :

```bash
./setup-podman.sh
```

Cela crée également un fichier `~openclaw/.openclaw/openclaw.json` minimal (définit `gateway.mode="local"`) pour que la passerelle puisse démarrer sans exécuter l'assistant.

Par défaut, le conteneur n'est **pas** installé en tant que service systemd, vous le démarrez manuellement (voir ci-dessous). Pour une configuration de style production avec démarrage automatique et redémarrages, installez-le plutôt en tant que service utilisateur systemd Quadlet :

```bash
./setup-podman.sh --quadlet
```

(Ou définissez `OPENCLAW_PODMAN_QUADLET=1` ; utilisez `--container` pour installer uniquement le conteneur et le script de lancement.)

Variables d'environnement optionnelles au moment de la construction (à définir avant d'exécuter `setup-podman.sh`) :

- `OPENCLAW_DOCKER_APT_PACKAGES` — installer des paquets apt supplémentaires lors de la construction de l'image
- `OPENCLAW_EXTENSIONS` — pré-installer les dépendances d'extension (noms d'extension séparés par des espaces, par exemple `diagnostics-otel matrix`)

**2. Démarrer la passerelle** (manuel, pour un test rapide) :

```bash
./scripts/run-openclaw-podman.sh launch
```

**3. Assistant d'intégration** (par exemple pour ajouter des canaux ou des fournisseurs) :

```bash
./scripts/run-openclaw-podman.sh launch setup
```

Ouvrez ensuite `http://127.0.0.1:18789/` et utilisez le jeton de `~openclaw/.openclaw/.env` (ou la valeur imprimée par setup).

## Systemd (Quadlet, optionnel)

Si vous avez exécuté `./setup-podman.sh --quadlet` (ou `OPENCLAW_PODMAN_QUADLET=1`), une unité [Podman Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) est installée pour que la passerelle s'exécute en tant que service utilisateur systemd pour l'utilisateur openclaw. Le service est activé et démarré à la fin de la configuration.

- **Démarrer :** `sudo systemctl --machine openclaw@ --user start openclaw.service`
- **Arrêter :** `sudo systemctl --machine openclaw@ --user stop openclaw.service`
- **Statut :** `sudo systemctl --machine openclaw@ --user status openclaw.service`
- **Journaux :** `sudo journalctl --machine openclaw@ --user -u openclaw.service -f`

Le fichier quadlet se trouve à `~openclaw/.config/containers/systemd/openclaw.container`. Pour modifier les ports ou les variables d'environnement, modifiez ce fichier (ou le `.env` qu'il source), puis exécutez `sudo systemctl --machine openclaw@ --user daemon-reload` et redémarrez le service. Au démarrage, le service démarre automatiquement si lingering est activé pour openclaw (setup le fait quand loginctl est disponible).

Pour ajouter quadlet **après** une configuration initiale qui ne l'utilisait pas, réexécutez : `./setup-podman.sh --quadlet`.

## L'utilisateur openclaw (sans connexion)

`setup-podman.sh` crée un utilisateur système dédié `openclaw` :

- **Shell :** `nologin` — pas de connexion interactive ; réduit la surface d'attaque.
- **Accueil :** par exemple `/home/openclaw` — contient `~/.openclaw` (config, espace de travail) et le script de lancement `run-openclaw-podman.sh`.
- **Podman sans root :** L'utilisateur doit avoir une plage **subuid** et **subgid**. De nombreuses distributions les attribuent automatiquement lors de la création de l'utilisateur. Si setup affiche un avertissement, ajoutez des lignes à `/etc/subuid` et `/etc/subgid` :

  ```text
  openclaw:100000:65536
  ```

  Ensuite, démarrez la passerelle en tant que cet utilisateur (par exemple à partir de cron ou systemd) :

  ```bash
  sudo -u openclaw /home/openclaw/run-openclaw-podman.sh
  sudo -u openclaw /home/openclaw/run-openclaw-podman.sh setup
  ```

- **Config :** Seuls `openclaw` et root peuvent accéder à `/home/openclaw/.openclaw`. Pour modifier la config : utilisez l'interface de contrôle une fois que la passerelle est en cours d'exécution, ou `sudo -u openclaw $EDITOR /home/openclaw/.openclaw/openclaw.json`.

## Environnement et configuration

- **Jeton :** Stocké dans `~openclaw/.openclaw/.env` en tant que `OPENCLAW_GATEWAY_TOKEN`. `setup-podman.sh` et `run-openclaw-podman.sh` le génèrent s'il est manquant (utilise `openssl`, `python3`, ou `od`).
- **Optionnel :** Dans ce `.env`, vous pouvez définir les clés de fournisseur (par exemple `GROQ_API_KEY`, `OLLAMA_API_KEY`) et d'autres variables d'environnement OpenClaw.
- **Ports hôte :** Par défaut, le script mappe `18789` (passerelle) et `18790` (pont). Remplacez le mappage de port **hôte** avec `OPENCLAW_PODMAN_GATEWAY_HOST_PORT` et `OPENCLAW_PODMAN_BRIDGE_HOST_PORT` lors du lancement.
- **Liaison de passerelle :** Par défaut, `run-openclaw-podman.sh` démarre la passerelle avec `--bind loopback` pour un accès local sécurisé. Pour exposer sur le LAN, définissez `OPENCLAW_GATEWAY_BIND=lan` et configurez `gateway.controlUi.allowedOrigins` (ou activez explicitement le fallback host-header) dans `openclaw.json`.
- **Chemins :** La config hôte et l'espace de travail par défaut sont `~openclaw/.openclaw` et `~openclaw/.openclaw/workspace`. Remplacez les chemins hôte utilisés par le script de lancement avec `OPENCLAW_CONFIG_DIR` et `OPENCLAW_WORKSPACE_DIR`.

## Modèle de stockage

- **Données hôte persistantes :** `OPENCLAW_CONFIG_DIR` et `OPENCLAW_WORKSPACE_DIR` sont montés en bind dans le conteneur et conservent l'état sur l'hôte.
- **Tmpfs sandbox éphémère :** si vous activez `agents.defaults.sandbox`, les conteneurs sandbox d'outils montent `tmpfs` à `/tmp`, `/var/tmp`, et `/run`. Ces chemins sont soutenus par la mémoire et disparaissent avec le conteneur sandbox ; la configuration du conteneur Podman de haut niveau n'ajoute pas ses propres montages tmpfs.
- **Points chauds de croissance disque :** les chemins principaux à surveiller sont `media/`, `agents/<agentId>/sessions/sessions.json`, les fichiers JSONL de transcription, `cron/runs/*.jsonl`, et les journaux de fichiers roulants sous `/tmp/openclaw/` (ou votre `logging.file` configuré).

`setup-podman.sh` met maintenant en scène le tar d'image dans un répertoire temporaire privé et imprime le répertoire de base choisi lors de la configuration. Pour les exécutions non-root, il accepte `TMPDIR` uniquement quand cette base est sûre à utiliser ; sinon, il revient à `/var/tmp`, puis `/tmp`. Le tar sauvegardé reste propriétaire uniquement et est diffusé dans le `podman load` de l'utilisateur cible, donc les répertoires temporaires privés de l'appelant ne bloquent pas la configuration.

## Commandes utiles

- **Journaux :** Avec quadlet : `sudo journalctl --machine openclaw@ --user -u openclaw.service -f`. Avec script : `sudo -u openclaw podman logs -f openclaw`
- **Arrêter :** Avec quadlet : `sudo systemctl --machine openclaw@ --user stop openclaw.service`. Avec script : `sudo -u openclaw podman stop openclaw`
- **Redémarrer :** Avec quadlet : `sudo systemctl --machine openclaw@ --user start openclaw.service`. Avec script : réexécutez le script de lancement ou `podman start openclaw`
- **Supprimer le conteneur :** `sudo -u openclaw podman rm -f openclaw` — la config et l'espace de travail sur l'hôte sont conservés

## Dépannage

- **Permission refusée (EACCES) sur config ou auth-profiles :** Le conteneur utilise par défaut `--userns=keep-id` et s'exécute avec le même uid/gid que l'utilisateur hôte exécutant le script. Assurez-vous que votre `OPENCLAW_CONFIG_DIR` et `OPENCLAW_WORKSPACE_DIR` hôte sont possédés par cet utilisateur.
- **Démarrage de passerelle bloqué (manquant `gateway.mode=local`) :** Assurez-vous que `~openclaw/.openclaw/openclaw.json` existe et définit `gateway.mode="local"`. `setup-podman.sh` crée ce fichier s'il est manquant.
- **Podman sans root échoue pour l'utilisateur openclaw :** Vérifiez que `/etc/subuid` et `/etc/subgid` contiennent une ligne pour `openclaw` (par exemple `openclaw:100000:65536`). Ajoutez-la si elle est manquante et redémarrez.
- **Nom de conteneur en cours d'utilisation :** Le script de lancement utilise `podman run --replace`, donc le conteneur existant est remplacé quand vous redémarrez. Pour nettoyer manuellement : `podman rm -f openclaw`.
- **Script non trouvé lors de l'exécution en tant qu'openclaw :** Assurez-vous que `setup-podman.sh` a été exécuté pour que `run-openclaw-podman.sh` soit copié dans le répertoire personnel d'openclaw (par exemple `/home/openclaw/run-openclaw-podman.sh`).
- **Service Quadlet non trouvé ou échoue au démarrage :** Exécutez `sudo systemctl --machine openclaw@ --user daemon-reload` après avoir modifié le fichier `.container`. Quadlet nécessite cgroups v2 : `podman info --format '{{.Host.CgroupsVersion}}'` devrait afficher `2`.

## Optionnel : exécuter en tant que votre propre utilisateur

Pour exécuter la passerelle en tant qu'utilisateur normal (pas d'utilisateur openclaw dédié) : construisez l'image, créez `~/.openclaw/.env` avec `OPENCLAW_GATEWAY_TOKEN`, et exécutez le conteneur avec `--userns=keep-id` et des montages vers votre `~/.openclaw`. Le script de lancement est conçu pour le flux utilisateur openclaw ; pour une configuration mono-utilisateur, vous pouvez plutôt exécuter manuellement la commande `podman run` du script, en pointant la config et l'espace de travail vers votre répertoire personnel. Recommandé pour la plupart des utilisateurs : utilisez `setup-podman.sh` et exécutez en tant qu'utilisateur openclaw pour que la config et le processus soient isolés.
