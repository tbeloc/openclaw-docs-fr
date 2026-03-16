---
summary: "Guide de format de bundle unifié pour les bundles Codex, Claude et Cursor dans OpenClaw"
read_when:
  - Vous souhaitez installer ou déboguer un bundle compatible Codex, Claude ou Cursor
  - Vous devez comprendre comment OpenClaw mappe le contenu du bundle dans les fonctionnalités natives
  - Vous documentez la compatibilité des bundles ou les limites de support actuelles
title: "Plugin Bundles"
---

# Plugin bundles

OpenClaw supporte une classe partagée de paquets de plugins externes : les **bundle plugins**.

Aujourd'hui, cela signifie trois écosystèmes étroitement liés :

- Bundles Codex
- Bundles Claude
- Bundles Cursor

OpenClaw les affiche tous comme `Format: bundle` dans `openclaw plugins list`.
La sortie détaillée et `openclaw plugins info <id>` affichent également le sous-type
(`codex`, `claude`, ou `cursor`).

Connexes :

- Aperçu du système de plugins : [Plugins](/fr/tools/plugin)
- Flux CLI install/list : [plugins](/fr/cli/plugins)
- Schéma de manifeste natif : [Plugin manifest](/fr/plugins/manifest)

## Qu'est-ce qu'un bundle

Un bundle est un **paquet de contenu/métadonnées**, pas un plugin OpenClaw natif en processus.

Aujourd'hui, OpenClaw **n'exécute pas** le code runtime du bundle en processus. Au lieu de cela,
il détecte les fichiers de bundle connus, lit les métadonnées, et mappe le contenu de bundle supporté
dans les surfaces OpenClaw natives telles que les skills, les hook packs, la config MCP,
et les paramètres Pi intégrés.

C'est la limite de confiance principale :

- plugin OpenClaw natif : le module runtime s'exécute en processus
- bundle : paquet de métadonnées/contenu, avec mappage de fonctionnalités sélectif

## Modèle de bundle partagé

Les bundles Codex, Claude et Cursor sont suffisamment similaires pour qu'OpenClaw les traite
comme un modèle normalisé.

Idée partagée :

- un petit fichier manifeste, ou une disposition de répertoire par défaut
- une ou plusieurs racines de contenu telles que `skills/` ou `commands/`
- métadonnées optionnelles d'outil/runtime telles que MCP, hooks, agents, ou LSP
- installer en tant que répertoire ou archive, puis activer dans la liste de plugins normale

Comportement OpenClaw commun :

- détecter le sous-type du bundle
- le normaliser en un enregistrement de bundle interne
- mapper les parties supportées dans les fonctionnalités OpenClaw natives
- signaler les parties non supportées comme des capacités détectées mais non câblées

En pratique, la plupart des utilisateurs n'ont pas besoin de penser d'abord au format spécifique au fournisseur. La question la plus utile est : quelles surfaces de bundle OpenClaw mappe aujourd'hui ?

## Ordre de détection

OpenClaw préfère les dispositions de plugins/paquets OpenClaw natifs avant le traitement des bundles.

Effet pratique :

- `openclaw.plugin.json` l'emporte sur la détection de bundle
- les installations de paquets avec `package.json` valide + `openclaw.extensions` utilisent le
  chemin d'installation natif
- si un répertoire contient à la fois des métadonnées natives et de bundle, OpenClaw le traite
  comme natif en premier

Cela évite d'installer partiellement un paquet au format double en tant que bundle et de le
charger plus tard en tant que plugin natif.

## Ce qui fonctionne aujourd'hui

OpenClaw normalise les métadonnées du bundle en un enregistrement de bundle interne, puis mappe
les surfaces supportées dans le comportement natif existant.

### Supporté maintenant

#### Contenu de skill

- les racines de skill du bundle se chargent comme des racines de skill OpenClaw normales
- les racines `commands` de Claude sont traitées comme des racines de skill supplémentaires
- les racines `.cursor/commands` de Cursor sont traitées comme des racines de skill supplémentaires

Cela signifie que les fichiers de commande markdown Claude fonctionnent via le chargeur de skill OpenClaw normal. Les commandes markdown Cursor fonctionnent via le même chemin.

#### Hook packs

- les racines de hook du bundle fonctionnent **uniquement** lorsqu'elles utilisent la disposition
  normale du hook-pack OpenClaw. Aujourd'hui, c'est principalement le cas compatible Codex :
  - `HOOK.md`
  - `handler.ts` ou `handler.js`

#### MCP pour les backends CLI

- les bundles activés peuvent contribuer à la config du serveur MCP
- le câblage runtime actuel est utilisé par le backend `claude-cli`
- OpenClaw fusionne la config MCP du bundle dans le fichier `--mcp-config` du backend

#### Paramètres Pi intégrés

- `settings.json` de Claude est importé comme paramètres Pi intégrés par défaut lorsque le
  bundle est activé
- OpenClaw assainit les clés de remplacement de shell avant de les appliquer

Clés assainies :

- `shellPath`
- `shellCommandPrefix`

### Détecté mais non exécuté

Ces surfaces sont détectées, affichées dans les capacités du bundle, et peuvent apparaître dans
la sortie de diagnostics/info, mais OpenClaw ne les exécute pas encore :

- `agents` de Claude
- `hooks.json` automation de Claude
- `lspServers` de Claude
- `outputStyles` de Claude
- `.cursor/agents` de Cursor
- `.cursor/hooks.json` de Cursor
- `.cursor/rules` de Cursor
- `mcpServers` de Cursor en dehors des chemins runtime actuellement mappés
- métadonnées inline/app de Codex au-delà du rapport de capacité

## Rapport de capacité

`openclaw plugins info <id>` affiche les capacités du bundle à partir de l'enregistrement
de bundle normalisé.

Les capacités supportées sont chargées silencieusement. Les capacités non supportées produisent
un avertissement tel que :

```text
bundle capability detected but not wired into OpenClaw yet: agents
```

Exceptions actuelles :

- `commands` de Claude est considéré comme supporté car il mappe aux skills
- `settings` de Claude est considéré comme supporté car il mappe aux paramètres Pi intégrés
- `commands` de Cursor est considéré comme supporté car il mappe aux skills
- MCP du bundle est considéré comme supporté où OpenClaw l'importe réellement
- `hooks` de Codex est considéré comme supporté uniquement pour les dispositions de hook-pack OpenClaw

## Différences de format

Les formats sont proches, mais pas identiques octet par octet. Ce sont les différences pratiques
qui importent dans OpenClaw.

### Codex

Marqueurs typiques :

- `.codex-plugin/plugin.json`
- `skills/` optionnel
- `hooks/` optionnel
- `.mcp.json` optionnel
- `.app.json` optionnel

Les bundles Codex s'adaptent mieux à OpenClaw lorsqu'ils utilisent des racines de skill et
des répertoires de hook-pack de style OpenClaw.

### Claude

OpenClaw supporte les deux :

- bundles Claude basés sur manifeste : `.claude-plugin/plugin.json`
- bundles Claude sans manifeste qui utilisent la disposition Claude par défaut

Marqueurs de disposition Claude par défaut qu'OpenClaw reconnaît :

- `skills/`
- `commands/`
- `agents/`
- `hooks/hooks.json`
- `.mcp.json`
- `.lsp.json`
- `settings.json`

Notes spécifiques à Claude :

- `commands/` est traité comme du contenu de skill
- `settings.json` est importé dans les paramètres Pi intégrés
- `hooks/hooks.json` est détecté, mais non exécuté comme automation Claude

### Cursor

Marqueurs typiques :

- `.cursor-plugin/plugin.json`
- `skills/` optionnel
- `.cursor/commands/` optionnel
- `.cursor/agents/` optionnel
- `.cursor/rules/` optionnel
- `.cursor/hooks.json` optionnel
- `.mcp.json` optionnel

Notes spécifiques à Cursor :

- `.cursor/commands/` est traité comme du contenu de skill
- `.cursor/rules/`, `.cursor/agents/`, et `.cursor/hooks.json` sont
  détection uniquement aujourd'hui

## Chemins personnalisés Claude

Les manifestes de bundle Claude peuvent déclarer des chemins de composant personnalisés. OpenClaw traite
ces chemins comme **additifs**, non remplaçants des valeurs par défaut.

Clés de chemin personnalisé actuellement reconnues :

- `skills`
- `commands`
- `agents`
- `hooks`
- `mcpServers`
- `lspServers`
- `outputStyles`

Exemples :

- `commands/` par défaut plus manifeste `commands: "extra-commands"` =>
  OpenClaw scanne les deux
- `skills/` par défaut plus manifeste `skills: ["team-skills"]` =>
  OpenClaw scanne les deux

## Modèle de sécurité

Le support des bundles est intentionnellement plus étroit que le support des plugins natifs.

Comportement actuel :

- la découverte de bundle lit les fichiers à l'intérieur de la racine du plugin avec des vérifications de limite
- les chemins de skills et de hook-pack doivent rester à l'intérieur de la racine du plugin
- les fichiers de paramètres du bundle sont lus avec les mêmes vérifications de limite
- OpenClaw n'exécute pas de code runtime de bundle arbitraire en processus

Cela rend le support des bundles plus sûr par défaut que les modules de plugins natifs, mais vous
devriez toujours traiter les bundles tiers comme du contenu de confiance pour les fonctionnalités
qu'ils exposent.

## Exemples d'installation

```bash
openclaw plugins install ./my-codex-bundle
openclaw plugins install ./my-claude-bundle
openclaw plugins install ./my-cursor-bundle
openclaw plugins install ./my-bundle.tgz
openclaw plugins info my-bundle
```

Si le répertoire est un plugin/paquet OpenClaw natif, le chemin d'installation natif l'emporte toujours.

## Dépannage

### Le bundle est détecté mais les capacités ne s'exécutent pas

Vérifiez `openclaw plugins info <id>`.

Si la capacité est listée mais OpenClaw dit qu'elle n'est pas encore câblée, c'est une
vraie limite de produit, pas une installation cassée.

### Les fichiers de commande Claude n'apparaissent pas

Assurez-vous que le bundle est activé et que les fichiers markdown sont à l'intérieur d'une
racine `commands` ou `skills` détectée.

### Les paramètres Claude ne s'appliquent pas

Le support actuel est limité aux paramètres Pi intégrés de `settings.json`.
OpenClaw ne traite pas les paramètres du bundle comme des correctifs de config OpenClaw bruts.

### Les hooks Claude ne s'exécutent pas

`hooks/hooks.json` est uniquement détecté aujourd'hui.

Si vous avez besoin de hooks de bundle exécutables aujourd'hui, utilisez la disposition
normale du hook-pack OpenClaw via une racine de hook Codex supportée ou livrez un plugin
OpenClaw natif.
