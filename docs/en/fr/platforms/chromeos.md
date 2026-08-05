---
summary: "Exécutez la passerelle OpenClaw sur ChromeOS dans un conteneur Linux Crostini"
read_when:
  - Installing OpenClaw on a Chromebook or ChromeOS device
  - Debugging missing provider keys or a Gateway that is gone after a reboot
title: "ChromeOS"
---

ChromeOS exécute les logiciels Linux via **Crostini**, un conteneur Debian géré
que Google expose comme « environnement de développement Linux ». La passerelle
s'exécute à l'intérieur de ce conteneur exactement comme n'importe quelle autre
installation Linux, donc le [guide Linux](/fr/platforms/linux) s'applique
intégralement. Cette page couvre la configuration spécifique à ChromeOS et les
pièges qui diffèrent d'un hôte Linux ordinaire.

OpenClaw nécessite Node car son magasin d'état canonique utilise `node:sqlite`.
Bun peut installer les dépendances ou exécuter les scripts de package, mais il
ne peut pas exécuter l'interface de ligne de commande OpenClaw ou la passerelle.

## Activer le conteneur Linux

Activez Crostini avant d'installer quoi que ce soit :

1. Ouvrez les **Paramètres** de ChromeOS.
2. Allez à **À propos de ChromeOS** puis **Développeurs**.
3. À côté de **Environnement de développement Linux**, sélectionnez **Configurer**
   et suivez les invites. ChromeOS télécharge le conteneur Debian et ouvre un
   **Terminal**.

Exécutez chaque commande ci-dessous à l'intérieur de ce Terminal.

## Chemin rapide

1. Installez via le script d'installation (il installe une version Node
   supportée pour vous) :

   ```bash
   curl -fsSL https://openclaw.ai/install.sh | bash
   ```

2. Intégrez et installez le service :

   ```bash
   openclaw onboard --install-daemon
   ```

3. Confirmez que la passerelle est en cours d'exécution :

   ```bash
   openclaw gateway status
   ```

Les conseils complets du serveur se trouvent dans le [guide Linux](/fr/platforms/linux)
et le [runbook de la passerelle](/fr/gateway).

## Préférez l'installation native à Docker

Sur un Chromebook monoposte, utilisez l'installation npm native (le script
d'installation, ou un `npm i -g openclaw@latest` global) plutôt que
[Docker](/fr/install/docker).

Docker fonctionne dans Crostini, mais Docker dans Crostini ajoute des frictions :
si vous utilisez l'interface de ligne de commande Claude Code comme runtime de
modèle, elle doit être installée et connectée **à l'intérieur d'un répertoire
personnel de conteneur persistant**, ce qui est facile à perdre lors d'une
reconstruction de conteneur. L'installation native garde l'interface de ligne de
commande et sa connexion directement sur le système de fichiers Crostini, donc
une reconstruction d'image Docker ne peut pas l'effacer.

## Version de Node

La version de Node disponible dans un conteneur Crostini peut être inférieure au
minimum d'OpenClaw. OpenClaw nécessite Node 22.22.3+, Node 24.15+, ou Node 25.9+ ;
Node 26 est la version par défaut recommandée. Le script d'installation détecte
une version de Node manquante ou non supportée et provisionne automatiquement une
version supportée.

Si vous avez installé Node vous-même avant OpenClaw, mettez-le à jour **avant**
d'installer OpenClaw :

```bash
node -v
```

Consultez les [conseils d'installation de Node](/fr/install/node) pour les versions
supportées.

## Clés de fournisseur et variables d'environnement

La passerelle s'exécute en tant que **service utilisateur systemd**, donc un
`export VAR=...` dans un Terminal interactif n'est pas hérité par le service
déjà installé.

Mettez plutôt les clés de fournisseur dans `~/.openclaw/.env`, une par ligne :

```bash
DEEPSEEK_API_KEY=your-key-here
```

Ensuite, redémarrez pour que le service les récupère :

```bash
openclaw gateway restart
```

Consultez les [Variables d'environnement](/fr/help/environment) pour les règles
complètes de précédence et de source.

## Crostini n'est pas toujours actif

Ne traitez pas Crostini comme un hôte toujours actif. Après un redémarrage de
ChromeOS, ouvrez le **Terminal** une fois pour démarrer l'environnement Linux
avant de compter sur la passerelle.

Ensuite, vérifiez le service :

```bash
openclaw gateway status
```

## Connexes

- [Guide Linux](/fr/platforms/linux)
- [Aperçu de l'installation](/fr/install)
- [Conseils d'installation de Node](/fr/install/node)
- [Runbook de la passerelle](/fr/gateway)
- [Configuration de la passerelle](/fr/gateway/configuration)
- [Google : Configurer Linux sur votre Chromebook](https://support.google.com/chromebook/answer/9145439)
