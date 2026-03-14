---
summary: "Référence CLI pour `openclaw plugins` (lister, installer, désinstaller, activer/désactiver, doctor)"
read_when:
  - Vous souhaitez installer ou gérer des plugins Gateway in-process
  - Vous souhaitez déboguer les échecs de chargement de plugins
title: "plugins"
---

# `openclaw plugins`

Gérer les plugins/extensions Gateway (chargés in-process).

Connexes :

- Système de plugins : [Plugins](/tools/plugin)
- Manifeste de plugin + schéma : [Manifeste de plugin](/plugins/manifest)
- Durcissement de la sécurité : [Sécurité](/gateway/security)

## Commandes

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins uninstall <id>
openclaw plugins doctor
openclaw plugins update <id>
openclaw plugins update --all
```

Les plugins fournis avec OpenClaw sont désactivés au démarrage. Utilisez `plugins enable` pour
les activer.

Tous les plugins doivent inclure un fichier `openclaw.plugin.json` avec un schéma JSON intégré
(`configSchema`, même s'il est vide). Les manifestes ou schémas manquants/invalides empêchent
le plugin de se charger et font échouer la validation de la configuration.

### Installer

```bash
openclaw plugins install <path-or-spec>
openclaw plugins install <npm-spec> --pin
```

Note de sécurité : traitez les installations de plugins comme l'exécution de code. Préférez les versions épinglées.

Les spécifications npm sont **registry-only** (nom du package + version **exacte** optionnelle ou
**dist-tag**). Les spécifications Git/URL/fichier et les plages semver sont rejetées. Les installations de dépendances
s'exécutent avec `--ignore-scripts` pour des raisons de sécurité.

Les spécifications nues et `@latest` restent sur la piste stable. Si npm résout l'une ou l'autre
en préversion, OpenClaw s'arrête et vous demande d'accepter explicitement avec une
balise de préversion telle que `@beta`/`@rc` ou une version de préversion exacte telle que
`@1.2.3-beta.4`.

Si une spécification d'installation nue correspond à un id de plugin fourni (par exemple `diffs`), OpenClaw
installe le plugin fourni directement. Pour installer un package npm avec le même
nom, utilisez une spécification explicitement délimitée (par exemple `@scope/diffs`).

Archives supportées : `.zip`, `.tgz`, `.tar.gz`, `.tar`.

Utilisez `--link` pour éviter de copier un répertoire local (ajoute à `plugins.load.paths`) :

```bash
openclaw plugins install -l ./my-plugin
```

Utilisez `--pin` sur les installations npm pour enregistrer la spécification exacte résolue (`name@version`) dans
`plugins.installs` tout en conservant le comportement par défaut non épinglé.

### Désinstaller

```bash
openclaw plugins uninstall <id>
openclaw plugins uninstall <id> --dry-run
openclaw plugins uninstall <id> --keep-files
```

`uninstall` supprime les enregistrements de plugins de `plugins.entries`, `plugins.installs`,
la liste d'autorisation des plugins et les entrées `plugins.load.paths` liées le cas échéant.
Pour les plugins de mémoire actifs, l'emplacement de mémoire est réinitialisé à `memory-core`.

Par défaut, uninstall supprime également le répertoire d'installation du plugin sous la racine des extensions du répertoire d'état actif
(`$OPENCLAW_STATE_DIR/extensions/<id>`). Utilisez
`--keep-files` pour conserver les fichiers sur le disque.

`--keep-config` est supporté comme alias déprécié pour `--keep-files`.

### Mettre à jour

```bash
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins update <id> --dry-run
```

Les mises à jour s'appliquent uniquement aux plugins installés à partir de npm (suivis dans `plugins.installs`).

Lorsqu'un hash d'intégrité stocké existe et que le hash d'artefact récupéré change,
OpenClaw affiche un avertissement et demande une confirmation avant de continuer. Utilisez
le `--yes` global pour contourner les invites dans les exécutions CI/non-interactives.
