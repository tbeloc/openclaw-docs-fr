---
summary: "Déplacer l'état local de Claude Code et Claude Desktop dans OpenClaw avec un aperçu d'importation"
read_when:
  - You are coming from Claude Code or Claude Desktop and want to keep instructions, MCP servers, and skills
  - You need to understand what OpenClaw imports automatically and what stays archive-only
title: "Migration depuis Claude"
---

OpenClaw importe l'état local de Claude via le fournisseur de migration Claude fourni. Le fournisseur affiche un aperçu de chaque élément avant de modifier l'état, masque les secrets dans les plans et rapports, et crée une sauvegarde vérifiée avant l'application.

<Note>
Les importations d'intégration nécessitent une installation OpenClaw récente. Si vous avez déjà un état OpenClaw local, réinitialisez d'abord la configuration, les identifiants, les sessions et l'espace de travail, ou utilisez `openclaw migrate` directement avec `--overwrite` après avoir examiné le plan.
</Note>

## Deux façons d'importer

<Tabs>
  <Tab title="Assistant d'intégration">
    L'assistant propose Claude lorsqu'il détecte un état local de Claude.

    ```bash
    openclaw onboard --flow import
    ```

    Ou pointez vers une source spécifique :

    ```bash
    openclaw onboard --import-from claude --import-source ~/.claude
    ```

  </Tab>
  <Tab title="CLI">
    Utilisez `openclaw migrate` pour les exécutions scriptées ou répétables. Voir [`openclaw migrate`](/fr/cli/migrate) pour la référence complète.

    ```bash
    openclaw migrate claude --dry-run
    openclaw migrate apply claude --yes
    ```

    Ajoutez `--from <path>` pour importer un répertoire personnel Claude Code ou une racine de projet spécifique.

  </Tab>
</Tabs>

## Ce qui est importé

<AccordionGroup>
  <Accordion title="Instructions et mémoire">
    - Le contenu du projet `CLAUDE.md` et `.claude/CLAUDE.md` est copié ou ajouté à l'espace de travail de l'agent OpenClaw `AGENTS.md`.
    - Le contenu utilisateur `~/.claude/CLAUDE.md` est ajouté à l'espace de travail `USER.md`.
  </Accordion>
  <Accordion title="Serveurs MCP">
    Les définitions de serveur MCP sont importées à partir du projet `.mcp.json`, de Claude Code `~/.claude.json`, et de Claude Desktop `claude_desktop_config.json` lorsqu'ils sont présents.
  </Accordion>
  <Accordion title="Compétences et commandes">
    - Les compétences Claude avec un fichier `SKILL.md` sont copiées dans le répertoire des compétences de l'espace de travail OpenClaw.
    - Les fichiers Markdown de commande Claude sous `.claude/commands/` ou `~/.claude/commands/` sont convertis en compétences OpenClaw avec `disable-model-invocation: true`.
  </Accordion>
</AccordionGroup>

## Ce qui reste en archive uniquement

Le fournisseur copie ces éléments dans le rapport de migration pour examen manuel, mais ne les charge **pas** dans la configuration OpenClaw active :

- Crochets Claude
- Permissions Claude et listes d'outils larges
- Valeurs par défaut d'environnement Claude
- `CLAUDE.local.md`
- `.claude/rules/`
- Sous-agents Claude sous `.claude/agents/` ou `~/.claude/agents/`
- Caches Claude Code, plans et répertoires d'historique de projet
- Extensions Claude Desktop et identifiants stockés par le système d'exploitation

OpenClaw refuse d'exécuter automatiquement les crochets, de faire confiance aux listes d'autorisation de permissions, ou de décoder l'état opaque des identifiants OAuth et Desktop. Déplacez ce dont vous avez besoin manuellement après avoir examiné l'archive.

## Sélection de la source

Sans `--from`, OpenClaw inspecte le répertoire personnel Claude Code par défaut à `~/.claude`, le fichier d'état `~/.claude.json` de Claude Code échantillonné, et la configuration MCP Claude Desktop sur macOS.

Lorsque `--from` pointe vers une racine de projet, OpenClaw importe uniquement les fichiers Claude de ce projet tels que `CLAUDE.md`, `.claude/settings.json`, `.claude/commands/`, `.claude/skills/`, et `.mcp.json`. Il ne lit pas votre répertoire personnel Claude global lors d'une importation de racine de projet.

## Flux recommandé

<Steps>
  <Step title="Afficher un aperçu du plan">
    ```bash
    openclaw migrate claude --dry-run
    ```

    Le plan énumère tout ce qui va changer, y compris les conflits, les éléments ignorés et les valeurs sensibles masquées dans les champs `env` ou `headers` MCP imbriqués.

  </Step>
  <Step title="Appliquer avec sauvegarde">
    ```bash
    openclaw migrate apply claude --yes
    ```

    OpenClaw crée et vérifie une sauvegarde avant l'application.

  </Step>
  <Step title="Exécuter doctor">
    ```bash
    openclaw doctor
    ```

    [Doctor](/fr/gateway/doctor) vérifie les problèmes de configuration ou d'état après l'importation.

  </Step>
  <Step title="Redémarrer et vérifier">
    ```bash
    openclaw gateway restart
    openclaw status
    ```

    Confirmez que la passerelle est saine et que vos instructions importées, serveurs MCP et compétences sont chargés.

  </Step>
</Steps>

## Gestion des conflits

L'application refuse de continuer lorsque le plan signale des conflits (un fichier ou une valeur de configuration existe déjà à la cible).

<Warning>
Réexécutez avec `--overwrite` uniquement lorsque le remplacement de la cible existante est intentionnel. Les fournisseurs peuvent toujours écrire des sauvegardes au niveau des éléments pour les fichiers remplacés dans le répertoire du rapport de migration.
</Warning>

Pour une installation OpenClaw récente, les conflits sont inhabituels. Ils apparaissent généralement lorsque vous réexécutez l'importation sur une configuration qui a déjà des modifications utilisateur.

## Sortie JSON pour l'automatisation

```bash
openclaw migrate claude --dry-run --json
openclaw migrate apply claude --json --yes
```

Avec `--json` et sans `--yes`, apply affiche le plan et ne modifie pas l'état. C'est le mode le plus sûr pour CI et les scripts partagés.

## Dépannage

<AccordionGroup>
  <Accordion title="L'état Claude se trouve en dehors de ~/.claude">
    Passez `--from /actual/path` (CLI) ou `--import-source /actual/path` (intégration).
  </Accordion>
  <Accordion title="L'intégration refuse d'importer sur une configuration existante">
    Les importations d'intégration nécessitent une installation récente. Soit réinitialisez l'état et réintégrez, soit utilisez `openclaw migrate apply claude` directement, qui supporte `--overwrite` et le contrôle explicite de la sauvegarde.
  </Accordion>
  <Accordion title="Les serveurs MCP de Claude Desktop n'ont pas été importés">
    Claude Desktop lit `claude_desktop_config.json` à partir d'un chemin spécifique à la plateforme. Pointez `--from` vers le répertoire de ce fichier si OpenClaw ne l'a pas détecté automatiquement.
  </Accordion>
  <Accordion title="Les commandes Claude sont devenues des compétences avec invocation de modèle désactivée">
    Par conception. Les commandes Claude sont déclenchées par l'utilisateur, donc OpenClaw les importe en tant que compétences avec `disable-model-invocation: true`. Modifiez le frontmatter de chaque compétence si vous souhaitez que l'agent les invoque automatiquement.
  </Accordion>
</AccordionGroup>

## Connexes

- [`openclaw migrate`](/fr/cli/migrate): référence CLI complète, contrat de plugin et formes JSON.
- [Guide de migration](/fr/install/migrating): tous les chemins de migration.
- [Migration depuis Hermes](/fr/install/migrating-hermes): l'autre chemin d'importation entre systèmes.
- [Intégration](/fr/cli/onboard): flux d'assistant et drapeaux non interactifs.
- [Doctor](/fr/gateway/doctor): vérification de santé post-migration.
- [Espace de travail de l'agent](/fr/concepts/agent-workspace): où vivent `AGENTS.md`, `USER.md` et les compétences.
