---
summary: "Référence CLI pour `openclaw migrate` (importer l'état d'un autre système d'agent)"
read_when:
  - You want to migrate from Hermes or another agent system into OpenClaw
  - You are adding a plugin-owned migration provider
title: "Migrate"
---

# `openclaw migrate`

Importez l'état d'un autre système d'agent via un fournisseur de migration détenu par un plugin. Les fournisseurs groupés couvrent [Claude](/fr/install/migrating-claude) et [Hermes](/fr/install/migrating-hermes) ; les plugins tiers peuvent enregistrer des fournisseurs supplémentaires.

<Tip>
Pour les procédures pas à pas destinées aux utilisateurs, consultez [Migration depuis Claude](/fr/install/migrating-claude) et [Migration depuis Hermes](/fr/install/migrating-hermes). Le [hub de migration](/fr/install/migrating) répertorie tous les chemins.
</Tip>

## Commandes

```bash
openclaw migrate list
openclaw migrate claude --dry-run
openclaw migrate hermes --dry-run
openclaw migrate hermes
openclaw migrate apply claude --yes
openclaw migrate apply hermes --yes
openclaw migrate apply hermes --include-secrets --yes
openclaw onboard --flow import
openclaw onboard --import-from claude --import-source ~/.claude
openclaw onboard --import-from hermes --import-source ~/.hermes
```

<ParamField path="<provider>" type="string">
  Nom d'un fournisseur de migration enregistré, par exemple `hermes`. Exécutez `openclaw migrate list` pour voir les fournisseurs installés.
</ParamField>
<ParamField path="--dry-run" type="boolean">
  Construisez le plan et quittez sans modifier l'état.
</ParamField>
<ParamField path="--from <path>" type="string">
  Remplacez le répertoire d'état source. Hermes utilise par défaut `~/.hermes`.
</ParamField>
<ParamField path="--include-secrets" type="boolean">
  Importez les identifiants pris en charge. Désactivé par défaut.
</ParamField>
<ParamField path="--overwrite" type="boolean">
  Autorisez apply à remplacer les cibles existantes lorsque le plan signale des conflits.
</ParamField>
<ParamField path="--yes" type="boolean">
  Ignorez l'invite de confirmation. Requis en mode non interactif.
</ParamField>
<ParamField path="--no-backup" type="boolean">
  Ignorez la sauvegarde avant apply. Nécessite `--force` lorsque l'état OpenClaw local existe.
</ParamField>
<ParamField path="--force" type="boolean">
  Requis avec `--no-backup` lorsque apply refuserait autrement de sauter la sauvegarde.
</ParamField>
<ParamField path="--json" type="boolean">
  Imprimez le plan ou le résultat apply en JSON. Avec `--json` et sans `--yes`, apply imprime le plan et ne modifie pas l'état.
</ParamField>

## Modèle de sécurité

`openclaw migrate` est d'abord un aperçu.

<AccordionGroup>
  <Accordion title="Aperçu avant apply">
    Le fournisseur retourne un plan détaillé avant tout changement, y compris les conflits, les éléments ignorés et les éléments sensibles. Les plans JSON, la sortie apply et les rapports de migration masquent les clés imbriquées ressemblant à des secrets telles que les clés API, les jetons, les en-têtes d'autorisation, les cookies et les mots de passe.

    `openclaw migrate apply <provider>` affiche un aperçu du plan et demande une confirmation avant de modifier l'état, sauf si `--yes` est défini. En mode non interactif, apply nécessite `--yes`.

  </Accordion>
  <Accordion title="Sauvegardes">
    Apply crée et vérifie une sauvegarde OpenClaw avant d'appliquer la migration. Si aucun état OpenClaw local n'existe encore, l'étape de sauvegarde est ignorée et la migration peut continuer. Pour ignorer une sauvegarde lorsque l'état existe, passez à la fois `--no-backup` et `--force`.
  </Accordion>
  <Accordion title="Conflits">
    Apply refuse de continuer lorsque le plan a des conflits. Examinez le plan, puis réexécutez avec `--overwrite` si le remplacement des cibles existantes est intentionnel. Les fournisseurs peuvent toujours écrire des sauvegardes au niveau des éléments pour les fichiers remplacés dans le répertoire du rapport de migration.
  </Accordion>
  <Accordion title="Secrets">
    Les secrets ne sont jamais importés par défaut. Utilisez `--include-secrets` pour importer les identifiants pris en charge.
  </Accordion>
</AccordionGroup>

## Fournisseur Claude

Le fournisseur Claude groupé détecte l'état Claude Code à `~/.claude` par défaut. Utilisez `--from <path>` pour importer un répertoire personnel Claude Code spécifique ou une racine de projet.

<Tip>
Pour une procédure pas à pas destinée aux utilisateurs, consultez [Migration depuis Claude](/fr/install/migrating-claude).
</Tip>

### Ce que Claude importe

- Projet `CLAUDE.md` et `.claude/CLAUDE.md` dans l'espace de travail de l'agent OpenClaw.
- Utilisateur `~/.claude/CLAUDE.md` ajouté à l'espace de travail `USER.md`.
- Définitions du serveur MCP à partir du projet `.mcp.json`, Claude Code `~/.claude.json` et Claude Desktop `claude_desktop_config.json`.
- Répertoires de compétences Claude qui incluent `SKILL.md`.
- Fichiers Markdown de commande Claude convertis en compétences OpenClaw avec invocation manuelle uniquement.

### État d'archive et d'examen manuel

Les hooks Claude, les permissions, les valeurs par défaut de l'environnement, la mémoire locale, les règles délimitées par le chemin, les sous-agents, les caches, les plans et l'historique du projet sont préservés dans le rapport de migration ou signalés comme éléments d'examen manuel. OpenClaw n'exécute pas les hooks, ne copie pas les listes blanches larges et n'importe pas automatiquement l'état des identifiants OAuth/Desktop.

## Fournisseur Hermes

Le fournisseur Hermes groupé détecte l'état à `~/.hermes` par défaut. Utilisez `--from <path>` lorsque Hermes se trouve ailleurs.

### Ce que Hermes importe

- Configuration du modèle par défaut à partir de `config.yaml`.
- Fournisseurs de modèles configurés et points de terminaison personnalisés compatibles OpenAI à partir de `providers` et `custom_providers`.
- Définitions du serveur MCP à partir de `mcp_servers` ou `mcp.servers`.
- `SOUL.md` et `AGENTS.md` dans l'espace de travail de l'agent OpenClaw.
- `memories/MEMORY.md` et `memories/USER.md` ajoutés aux fichiers de mémoire de l'espace de travail.
- Valeurs par défaut de la configuration de la mémoire pour la mémoire de fichier OpenClaw, plus les éléments d'archive ou d'examen manuel pour les fournisseurs de mémoire externes tels que Honcho.
- Compétences qui incluent un fichier `SKILL.md` sous `skills/<name>/`.
- Valeurs de configuration par compétence à partir de `skills.config`.
- Clés API prises en charge à partir de `.env`, uniquement avec `--include-secrets`.

### Clés `.env` prises en charge

`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`, `XAI_API_KEY`, `MISTRAL_API_KEY`, `DEEPSEEK_API_KEY`.

### État archivé uniquement

L'état Hermes qu'OpenClaw ne peut pas interpréter en toute sécurité est copié dans le rapport de migration pour examen manuel, mais il n'est pas chargé dans la configuration ou les identifiants OpenClaw actifs. Cela préserve l'état opaque ou non sécurisé sans prétendre qu'OpenClaw peut l'exécuter ou le faire confiance automatiquement :

- `plugins/`
- `sessions/`
- `logs/`
- `cron/`
- `mcp-tokens/`
- `auth.json`
- `state.db`

### Après application

```bash
openclaw doctor
```

## Contrat de plugin

Les sources de migration sont des plugins. Un plugin déclare ses identifiants de fournisseur dans `openclaw.plugin.json` :

```json
{
  "contracts": {
    "migrationProviders": ["hermes"]
  }
}
```

À l'exécution, le plugin appelle `api.registerMigrationProvider(...)`. Le fournisseur implémente `detect`, `plan` et `apply`. Core possède l'orchestration CLI, la politique de sauvegarde, les invites, la sortie JSON et la vérification préalable des conflits. Core transmet le plan examiné dans `apply(ctx, plan)`, et les fournisseurs ne peuvent reconstruire le plan que lorsque cet argument est absent pour la compatibilité.

Les plugins de fournisseur peuvent utiliser `openclaw/plugin-sdk/migration` pour la construction d'éléments et les comptages de résumé, plus `openclaw/plugin-sdk/migration-runtime` pour les copies de fichiers conscientes des conflits, les copies de rapports archivés uniquement et les rapports de migration.

## Intégration d'intégration

L'intégration peut offrir une migration lorsqu'un fournisseur détecte une source connue. À la fois `openclaw onboard --flow import` et `openclaw setup --wizard --import-from hermes` utilisent le même fournisseur de migration de plugin et affichent toujours un aperçu avant application.

<Note>
Les importations d'intégration nécessitent une configuration OpenClaw nouvelle. Réinitialisez d'abord la configuration, les identifiants, les sessions et l'espace de travail si vous avez déjà un état local. Les importations de sauvegarde-plus-remplacement ou de fusion sont contrôlées par des fonctionnalités pour les configurations existantes.
</Note>

## Connexes

- [Migration depuis Hermes](/fr/install/migrating-hermes) : procédure pas à pas destinée aux utilisateurs.
- [Migration depuis Claude](/fr/install/migrating-claude) : procédure pas à pas destinée aux utilisateurs.
- [Migration](/fr/install/migrating) : déplacer OpenClaw vers une nouvelle machine.
- [Doctor](/fr/gateway/doctor) : vérification de santé après application d'une migration.
- [Plugins](/fr/tools/plugin) : installation et enregistrement des plugins.
