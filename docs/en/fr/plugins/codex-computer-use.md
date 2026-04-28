---
summary: "Configurez Codex Computer Use pour les agents OpenClaw en mode Codex"
title: "Codex Computer Use"
read_when:
  - You want Codex-mode OpenClaw agents to use Codex Computer Use
  - You are configuring computerUse for the bundled Codex plugin
  - You are troubleshooting /codex computer-use status or install
---

Computer Use est un plugin MCP natif de Codex pour le contrôle local du bureau. OpenClaw ne fournit pas l'application de bureau, n'exécute pas les actions du bureau lui-même et ne contourne pas les permissions de Codex. Le plugin `codex` fourni prépare uniquement le serveur d'application Codex : il active la prise en charge des plugins Codex, trouve ou installe le plugin Codex Computer Use configuré, vérifie que le serveur MCP `computer-use` est disponible, puis laisse Codex gérer les appels d'outils MCP natifs pendant les tours en mode Codex.

Utilisez cette page lorsque OpenClaw utilise déjà le harnais Codex natif. Pour la configuration du runtime elle-même, consultez [Codex harness](/fr/plugins/codex-harness).

## Configuration rapide

Définissez `plugins.entries.codex.config.computerUse` lorsque les tours en mode Codex doivent avoir Computer Use disponible avant le démarrage d'un thread :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          computerUse: {
            autoInstall: true,
          },
        },
      },
    },
  },
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
      agentRuntime: {
        id: "codex",
        fallback: "none",
      },
    },
  },
}
```

Avec cette configuration, OpenClaw vérifie le serveur d'application Codex avant chaque tour en mode Codex. Si Computer Use est manquant mais que le serveur d'application Codex a déjà découvert une marketplace installable, OpenClaw demande au serveur d'application Codex d'installer ou de réactiver le plugin et de recharger les serveurs MCP. Sur macOS, lorsqu'aucune marketplace correspondante n'est enregistrée et que le bundle d'application Codex standard existe, OpenClaw essaie également d'enregistrer la marketplace Codex fournie à partir de `/Applications/Codex.app/Contents/Resources/plugins/openai-bundled` avant d'échouer. Si la configuration ne peut toujours pas rendre le serveur MCP disponible, le tour échoue avant le démarrage du thread.

Les sessions existantes conservent leur runtime et leur liaison de thread Codex. Après avoir modifié `agentRuntime` ou la configuration de Computer Use, utilisez `/new` ou `/reset` dans le chat affecté avant de tester.

## Commandes

Utilisez les commandes `/codex computer-use` à partir de n'importe quelle surface de chat où la surface de commande du plugin `codex` est disponible. Ce sont des commandes de chat/runtime OpenClaw, pas des sous-commandes CLI `openclaw codex ...` :

```text
/codex computer-use status
/codex computer-use install
/codex computer-use install --source <marketplace-source>
/codex computer-use install --marketplace-path <path>
/codex computer-use install --marketplace <name>
```

`status` est en lecture seule. Il n'ajoute pas de sources de marketplace, n'installe pas de plugins et n'active pas la prise en charge des plugins Codex.

`install` active la prise en charge des plugins du serveur d'application Codex, ajoute éventuellement une source de marketplace configurée, installe ou réactive le plugin configuré via le serveur d'application Codex, recharge les serveurs MCP et vérifie que le serveur MCP expose les outils.

## Choix de marketplace

OpenClaw utilise la même API de serveur d'application que Codex expose. Les champs de marketplace choisissent où Codex doit trouver `computer-use`.

| Champ                | Utiliser quand                                                        | Support d'installation                                          |
| -------------------- | --------------------------------------------------------------- | -------------------------------------------------------- |
| Aucun champ de marketplace | Vous voulez que le serveur d'application Codex utilise les marketplaces qu'il connaît déjà. | Oui, lorsque le serveur d'application retourne une marketplace locale.        |
| `marketplaceSource`  | Vous avez une source de marketplace Codex que le serveur d'application peut ajouter.         | Oui, pour `/codex computer-use install` explicite.         |
| `marketplacePath`    | Vous connaissez déjà le chemin du fichier de marketplace local sur l'hôte.   | Oui, pour l'installation explicite et l'auto-installation au démarrage du tour.   |
| `marketplaceName`    | Vous voulez sélectionner une marketplace déjà enregistrée par nom.  | Oui uniquement lorsque la marketplace sélectionnée a un chemin local. |

Les nouveaux répertoires Codex peuvent avoir besoin d'un court moment pour initialiser leurs marketplaces officielles. Pendant l'installation, OpenClaw interroge `plugin/list` pendant jusqu'à `marketplaceDiscoveryTimeoutMs` millisecondes. La valeur par défaut est 60 secondes.

Si plusieurs marketplaces connues contiennent Computer Use, OpenClaw préfère `openai-bundled`, puis `openai-curated`, puis `local`. Les correspondances ambiguës inconnues échouent fermées et vous demandent de définir `marketplaceName` ou `marketplacePath`.

## Marketplace fournie macOS

Les récentes versions de Codex Desktop fournissent Computer Use ici :

```text
/Applications/Codex.app/Contents/Resources/plugins/openai-bundled/plugins/computer-use
```

Lorsque `computerUse.autoInstall` est true et qu'aucune marketplace contenant `computer-use` n'est enregistrée, OpenClaw essaie d'ajouter automatiquement la racine de la marketplace fournie standard :

```text
/Applications/Codex.app/Contents/Resources/plugins/openai-bundled
```

Vous pouvez également l'enregistrer explicitement à partir d'un shell avec Codex :

```bash
codex plugin marketplace add /Applications/Codex.app/Contents/Resources/plugins/openai-bundled
```

Si vous utilisez un chemin d'application Codex non standard, définissez `computerUse.marketplacePath` sur un chemin de fichier de marketplace local ou exécutez `/codex computer-use install --source <marketplace-source>` une fois.

## Limite du catalogue distant

Le serveur d'application Codex peut lister et lire les entrées de catalogue distantes uniquement, mais il ne supporte pas actuellement `plugin/install` distant. Cela signifie que `marketplaceName` peut sélectionner une marketplace distante uniquement pour les vérifications de statut, mais les installations et réactivations ont toujours besoin d'une marketplace locale via `marketplaceSource` ou `marketplacePath`.

Si le statut indique que le plugin est disponible dans une marketplace Codex distante mais que l'installation distante n'est pas supportée, exécutez l'installation avec une source ou un chemin local :

```text
/codex computer-use install --source <marketplace-source>
/codex computer-use install --marketplace-path <path>
```

## Référence de configuration

| Champ                           | Défaut        | Signification                                                                        |
| ------------------------------- | -------------- | ------------------------------------------------------------------------------ |
| `enabled`                       | inféré       | Exiger Computer Use. Par défaut true lorsqu'un autre champ Computer Use est défini. |
| `autoInstall`                   | false          | Installer ou réactiver à partir des marketplaces déjà découvertes au démarrage du tour.       |
| `marketplaceDiscoveryTimeoutMs` | 60000          | Combien de temps l'installation attend la découverte de marketplace du serveur d'application Codex.             |
| `marketplaceSource`             | non défini          | Chaîne source passée à `marketplace/add` du serveur d'application Codex.                    |
| `marketplacePath`               | non défini          | Chemin du fichier de marketplace Codex local contenant le plugin.                       |
| `marketplaceName`               | non défini          | Nom de la marketplace Codex enregistrée à sélectionner.                                   |
| `pluginName`                    | `computer-use` | Nom du plugin de marketplace Codex.                                                 |
| `mcpServerName`                 | `computer-use` | Nom du serveur MCP exposé par le plugin installé.                               |

L'auto-installation au démarrage du tour refuse intentionnellement les valeurs `marketplaceSource` configurées. Ajouter une nouvelle source est une opération de configuration explicite, donc utilisez `/codex computer-use install --source <marketplace-source>` une fois, puis laissez `autoInstall` gérer les futures réactivations à partir des marketplaces locales découvertes. L'auto-installation au démarrage du tour peut utiliser un `marketplacePath` configuré, car c'est déjà un chemin local sur l'hôte.

## Ce qu'OpenClaw vérifie

OpenClaw rapporte une raison de configuration stable en interne et formate le statut visible pour l'utilisateur pour le chat :

| Raison                       | Signification                                                | Étape suivante                                     |
| ---------------------------- | ------------------------------------------------------ | --------------------------------------------- |
| `disabled`                   | `computerUse.enabled` s'est résolu à false.               | Définissez `enabled` ou un autre champ Computer Use.  |
| `marketplace_missing`        | Aucune marketplace correspondante n'était disponible.                 | Configurez la source, le chemin ou le nom de la marketplace.  |
| `plugin_not_installed`       | La marketplace existe, mais le plugin n'est pas installé.   | Exécutez l'installation ou activez `autoInstall`.          |
| `plugin_disabled`            | Le plugin est installé mais désactivé dans la configuration Codex.      | Exécutez l'installation pour le réactiver.                  |
| `remote_install_unsupported` | La marketplace sélectionnée est distante uniquement.                   | Utilisez `marketplaceSource` ou `marketplacePath`. |
| `mcp_missing`                | Le plugin est activé, mais le serveur MCP est indisponible.  | Vérifiez Codex Computer Use et les permissions du système d'exploitation.  |
| `ready`                      | Le plugin et les outils MCP sont disponibles.                    | Démarrez le tour en mode Codex.                    |
| `check_failed`               | Une demande du serveur d'application Codex a échoué lors de la vérification du statut. | Vérifiez la connectivité et les journaux du serveur d'application.       |
| `auto_install_blocked`       | La configuration au démarrage du tour devrait ajouter une nouvelle source.       | Exécutez d'abord l'installation explicite.                   |

La sortie du chat inclut l'état du plugin, l'état du serveur MCP, la marketplace, les outils lorsqu'ils sont disponibles, et le message spécifique pour l'étape de configuration défaillante.

## Permissions macOS

Computer Use est spécifique à macOS. Le serveur MCP détenu par Codex peut avoir besoin de permissions du système d'exploitation local avant de pouvoir inspecter ou contrôler les applications. Si OpenClaw dit que Computer Use est installé mais que le serveur MCP est indisponible, vérifiez d'abord la configuration de Computer Use côté Codex :

- Le serveur d'application Codex s'exécute sur le même hôte où le contrôle du bureau doit se produire.
- Le plugin Computer Use est activé dans la configuration Codex.
- Le serveur MCP `computer-use` apparaît dans le statut MCP du serveur d'application Codex.
- macOS a accordé les permissions requises pour l'application de contrôle du bureau.
- La session d'hôte actuelle peut accéder au bureau en cours de contrôle.

OpenClaw échoue intentionnellement fermé lorsque `computerUse.enabled` est true. Un tour en mode Codex ne doit pas procéder silencieusement sans les outils de bureau natifs que la configuration exigeait.

## Dépannage

**Le statut indique non installé.** Exécutez `/codex computer-use install`. Si la marketplace n'est pas découverte, passez `--source` ou `--marketplace-path`.

**Le statut indique installé mais désactivé.** Exécutez `/codex computer-use install` à nouveau. L'installation du serveur d'application Codex réécrit la configuration du plugin en activé.

**Le statut indique que l'installation distante n'est pas supportée.** Utilisez une source de marketplace locale ou un chemin. Les entrées de catalogue distantes uniquement peuvent être inspectées mais pas installées via l'API du serveur d'application actuelle.

**Le statut indique que le serveur MCP est indisponible.** Réexécutez l'installation une fois pour que les serveurs MCP se rechargent. S'il reste indisponible, corrigez l'application Codex Computer Use, le statut MCP du serveur d'application Codex ou les permissions macOS.

**Le statut ou une sonde expire sur `computer-use.list_apps`.** Le plugin et le serveur MCP sont présents, mais le pont Computer Use local n'a pas répondu. Quittez ou redémarrez Codex Computer Use, relancez Codex Desktop si nécessaire, puis réessayez dans une nouvelle session OpenClaw.

**Un outil Computer Use indique `Native hook relay unavailable`.** Le hook d'outil natif Codex a atteint OpenClaw avec un enregistrement de relais obsolète ou manquant. Démarrez une nouvelle session OpenClaw avec `/new` ou `/reset`. Si cela continue de se produire, redémarrez la passerelle pour que les anciens threads du serveur d'application et les enregistrements de hook soient supprimés, puis réessayez.

**L'auto-installation au démarrage du tour refuse une source.** C'est intentionnel. Ajoutez d'abord la source avec `/codex computer-use install --source <marketplace-source>` explicite, puis l'auto-installation au démarrage du tour peut utiliser la marketplace locale découverte.
