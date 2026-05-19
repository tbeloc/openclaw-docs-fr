---
summary: "Exemples rapides pour lister, installer, mettre à jour, inspecter et désinstaller les plugins OpenClaw"
read_when:
  - You want quick plugin list, install, update, inspect, or uninstall examples
  - You want to choose a plugin install source
  - You want the right reference for publishing plugin packages
title: "Gérer les plugins"
sidebarTitle: "Gérer les plugins"
doc-schema-version: 1
---

Utilisez cette page pour les commandes courantes de gestion des plugins. Pour le contrat de commande exhaustif, les drapeaux, les règles de sélection de source et les cas limites, consultez [`openclaw plugins`](/fr/cli/plugins).

La plupart des flux d'installation sont :

1. trouver un paquet
2. l'installer à partir de ClawHub, npm, git ou un chemin local
3. laisser la Gateway gérée redémarrer automatiquement, ou la redémarrer manuellement si elle n'est pas gérée
4. vérifier les enregistrements d'exécution du plugin

## Lister et rechercher des plugins

```bash
openclaw plugins list
openclaw plugins list --enabled
openclaw plugins list --verbose
openclaw plugins list --json
openclaw plugins search "calendar"
```

Utilisez `--json` pour les scripts :

```bash
openclaw plugins list --json \
  | jq '.plugins[] | {id, enabled, format, source, dependencyStatus}'
```

`plugins list` est une vérification d'inventaire à froid. Elle affiche ce qu'OpenClaw peut découvrir à partir de la configuration, des manifestes et du registre de plugins ; elle ne prouve pas qu'une Gateway déjà en cours d'exécution a importé le runtime du plugin. La sortie JSON inclut les diagnostics du registre et le `dependencyStatus` statique de chaque plugin lorsque le paquet du plugin déclare `dependencies` ou `optionalDependencies`.

`plugins search` interroge ClawHub pour les paquets de plugins installables et affiche des conseils d'installation tels que `openclaw plugins install clawhub:<package>`.

## Installer des plugins

```bash
# Rechercher des paquets de plugins sur ClawHub.
openclaw plugins search "calendar"

# Installer à partir de ClawHub.
openclaw plugins install clawhub:<package>
openclaw plugins install clawhub:<package>@1.2.3
openclaw plugins install clawhub:<package>@beta

# Installer à partir de npm.
openclaw plugins install npm:<package>
openclaw plugins install npm:@scope/openclaw-plugin@1.2.3
openclaw plugins install npm:@openclaw/codex

# Installer à partir d'un artefact npm pack local.
openclaw plugins install npm-pack:<path.tgz>

# Installer à partir de git ou d'une extraction de développement local.
openclaw plugins install git:github.com/acme/openclaw-plugin@v1.0.0
openclaw plugins install ./my-plugin
openclaw plugins install --link ./my-plugin
```

Les spécifications de paquets nus s'installent à partir de npm lors de la transition de lancement. Utilisez `clawhub:`, `npm:`, `git:` ou `npm-pack:` lorsque vous avez besoin d'une sélection de source déterministe. Si le nom nu correspond à un id de plugin officiel, OpenClaw peut installer l'entrée du catalogue directement.

Utilisez `--force` uniquement lorsque vous souhaitez intentionnellement remplacer une cible d'installation existante. Pour les mises à jour de routine des installations npm, ClawHub ou hook-pack suivies, utilisez `openclaw plugins update`.

## Redémarrer et inspecter

Après l'installation, la mise à jour ou la désinstallation du code du plugin, une Gateway gérée en cours d'exécution avec le rechargement de configuration activé redémarre automatiquement. Si la Gateway n'est pas gérée ou si le rechargement est désactivé, redémarrez-la vous-même avant de vérifier les surfaces d'exécution en direct :

```bash
openclaw gateway restart
openclaw plugins inspect <plugin-id> --runtime --json
```

Utilisez `inspect --runtime` lorsque vous avez besoin de la preuve que le plugin a enregistré les surfaces d'exécution telles que les outils, les hooks, les services, les méthodes Gateway, les routes HTTP ou les commandes CLI appartenant au plugin. Les vérifications simples `inspect` et `list` sont des vérifications froides des manifestes, de la configuration et du registre.

## Mettre à jour les plugins

```bash
openclaw plugins update <plugin-id>
openclaw plugins update <npm-package-or-spec>
openclaw plugins update --all
openclaw plugins update <plugin-id> --dry-run
```

Lorsque vous transmettez un id de plugin, OpenClaw réutilise la spécification d'installation suivie. Les dist-tags stockés tels que `@beta` et les versions exactes épinglées continuent à être utilisés lors des exécutions ultérieures de `update <plugin-id>`.

Pour les installations npm, vous pouvez transmettre une spécification de paquet explicite pour changer l'enregistrement suivi :

```bash
openclaw plugins update @scope/openclaw-plugin@beta
openclaw plugins update @scope/openclaw-plugin
```

La deuxième commande ramène un plugin à la ligne de version par défaut du registre lorsqu'il était précédemment épinglé à une version exacte ou à une balise.

Lorsque `openclaw update` s'exécute sur le canal bêta, les enregistrements de plugins peuvent préférer les versions `@beta` correspondantes. Pour les règles exactes de secours et d'épinglage, consultez [`openclaw plugins`](/fr/cli/plugins#update).

## Désinstaller les plugins

```bash
openclaw plugins uninstall <plugin-id> --dry-run
openclaw plugins uninstall <plugin-id>
openclaw plugins uninstall <plugin-id> --keep-files
```

La désinstallation supprime l'entrée de configuration du plugin, l'enregistrement d'index du plugin persistant, les entrées de liste d'autorisation/refus et les chemins de charge liés le cas échéant. Les répertoires d'installation gérés sont supprimés sauf si vous transmettez `--keep-files`. Une Gateway gérée en cours d'exécution redémarre automatiquement lorsque la désinstallation modifie la source du plugin.

En mode Nix (`OPENCLAW_NIX_MODE=1`), les commandes d'installation, de mise à jour, de désinstallation, d'activation et de désactivation des plugins sont désactivées. Gérez ces choix dans la source Nix pour l'installation à la place.

## Choisir une source

| Source      | Utiliser quand                                                                                    | Exemple                                                        |
| ----------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| ClawHub     | Vous voulez la découverte native OpenClaw, les résumés de scan, les versions et les conseils     | `openclaw plugins install clawhub:<package>`                   |
| npmjs.com   | Vous expédiez déjà des paquets JavaScript ou avez besoin de dist-tags npm/registre privé         | `openclaw plugins install npm:@acme/openclaw-plugin`           |
| git         | Vous voulez une branche, une balise ou un commit d'un référentiel                                 | `openclaw plugins install git:github.com/<owner>/<repo>@<ref>` |
| chemin local | Vous développez ou testez un plugin sur la même machine                                          | `openclaw plugins install --link ./my-plugin`                  |
| npm pack    | Vous prouvez un artefact de paquet local via la sémantique d'installation npm                    | `openclaw plugins install npm-pack:<path.tgz>`                 |
| marketplace | Vous installez un plugin de marketplace compatible avec Claude                                   | `openclaw plugins install <plugin> --marketplace <source>`     |

## Publier des plugins

ClawHub est la surface de découverte publique principale pour les plugins OpenClaw. Publiez-y lorsque vous voulez que les utilisateurs trouvent les métadonnées du plugin, l'historique des versions, les résultats du scan du registre et les conseils d'installation avant d'installer.

```bash
npm i -g clawhub
clawhub login
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
clawhub package publish your-org/your-plugin@v1.0.0
```

Les plugins npm natifs doivent inclure un manifeste de plugin et des métadonnées de paquet avant la publication :

```json package.json
{
  "name": "@acme/openclaw-plugin",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

```bash
npm publish --access public
openclaw plugins install npm:@acme/openclaw-plugin
openclaw plugins install npm:@acme/openclaw-plugin@beta
openclaw plugins install npm:@acme/openclaw-plugin@1.0.0
```

Utilisez ces pages pour le contrat de publication complet au lieu de traiter cette page comme la référence de publication :

- [Publication ClawHub](/fr/clawhub/publishing) explique les propriétaires, les portées, les versions, l'examen, la validation des paquets et le transfert de paquets.
- [Construire des plugins](/fr/plugins/building-plugins) montre la forme du paquet de plugin et le flux de première publication.
- [Manifeste du plugin](/fr/plugins/manifest) définit les champs du manifeste de plugin natif.

Si le même paquet est disponible sur ClawHub et npm, utilisez le préfixe explicite `clawhub:` ou `npm:` lorsque vous avez besoin de forcer une source.

## Connexes

- [Plugins](/fr/tools/plugin) - installer, configurer, redémarrer et dépanner
- [`openclaw plugins`](/fr/cli/plugins) - référence CLI complète
- [Plugins communautaires](/fr/plugins/community) - découverte publique et publication ClawHub
- [ClawHub](/fr/clawhub/cli) - opérations CLI du registre
- [Construire des plugins](/fr/plugins/building-plugins) - créer un paquet de plugin
- [Manifeste du plugin](/fr/plugins/manifest) - manifeste et métadonnées du paquet
