---
summary: "Référence CLI pour `openclaw path` (inspecter et éditer les fichiers de l'espace de travail via le schéma d'adressage `oc://`)"
read_when:
  - You want to read or write a leaf inside a workspace file from the terminal
  - You're scripting against workspace state and want a stable, kind-agnostic addressing scheme
  - You're debugging a `oc://` path (validate the syntax, see what it resolves to)
title: "Path"
---

# `openclaw path`

Accès shell fourni par le plugin au substrat d'adressage `oc://` : un schéma de chemin unique dispatché par type pour inspecter et éditer les fichiers d'espace de travail adressables (markdown, jsonc, jsonl, yaml/yml/lobster). Les auto-hébergeurs, les auteurs de plugins et les extensions d'éditeur l'utilisent pour lire, trouver ou mettre à jour un emplacement précis sans développer des parseurs spécifiques à chaque fichier.

L'interface CLI reflète les verbes publics du substrat :

- `resolve` est concret et correspond à une seule correspondance.
- `find` est le verbe multi-correspondance pour les caractères génériques, les unions, les prédicats et l'expansion positionnelle.
- `set` n'accepte que les chemins concrets ou les marqueurs d'insertion ; les motifs avec caractères génériques sont rejetés avant l'écriture.

`path` est fourni par le plugin optionnel groupé `oc-path`. Activez-le avant la première utilisation :

```bash
openclaw plugins enable oc-path
```

## Pourquoi l'utiliser

L'état d'OpenClaw est réparti entre du markdown édité manuellement, de la configuration JSONC commentée, des journaux JSONL en ajout seul et des fichiers de workflow/spec YAML. Les scripts shell, les hooks et les agents ont souvent besoin d'une petite valeur de ces fichiers : une clé de frontmatter, un paramètre de plugin, un champ de journal, une étape YAML ou un élément de liste à puces sous une section nommée.

`openclaw path` donne à ces appelants une adresse stable au lieu d'un grep, d'une regex ou d'un parser unique pour chaque type de fichier. Le même chemin `oc://` peut être validé, résolu, recherché, exécuté en mode essai et écrit depuis le terminal, ce qui rend l'automatisation précise plus facile à examiner et plus sûre à rejouer. C'est particulièrement utile quand vous voulez mettre à jour une feuille tout en préservant les commentaires, les fins de ligne et le formatage environnant du reste du fichier.

Utilisez-le quand la chose que vous voulez a une adresse logique, mais la forme physique du fichier varie :

- Un hook veut lire un paramètre de JSONC commenté sans perdre les commentaires quand il réécrit la valeur.
- Un script de maintenance veut trouver chaque champ d'événement correspondant dans un journal JSONL sans charger le journal entier dans un parser personnalisé.
- Une extension d'éditeur veut accéder à une section markdown ou un élément de liste à puces par slug, puis afficher la ligne exacte qu'elle a résolue.
- Un agent veut exécuter en mode essai une petite édition d'espace de travail avant de l'appliquer, avec les octets modifiés visibles en révision.

Vous n'avez probablement pas besoin de `openclaw path` pour les éditions ordinaires de fichiers entiers, les migrations de configuration riches ou les écritures spécifiques à la mémoire. Celles-ci doivent utiliser la commande propriétaire ou le plugin. `path` est pour les petites opérations de fichier adressables où une commande terminal reproductible est plus claire qu'un autre parser sur mesure.

## Comment l'utiliser

Lire une valeur d'un fichier de configuration édité manuellement :

```bash
openclaw path resolve 'oc://config.jsonc/plugins/github/enabled'
```

Prévisualiser une écriture sans toucher au disque :

```bash
openclaw path set 'oc://config.jsonc/plugins/github/enabled' 'true' --dry-run
```

Trouver les enregistrements correspondants dans un journal JSONL en ajout seul :

```bash
openclaw path find 'oc://session.jsonl/[event=tool_call]/name'
```

Adresser une instruction en markdown par section et élément au lieu de par numéro de ligne :

```bash
openclaw path resolve 'oc://AGENTS.md/runtime-safety/openclaw-gateway'
```

Valider un chemin en CI ou dans un script de préflight avant que le script ne lise ou n'écrive :

```bash
openclaw path validate 'oc://AGENTS.md/tools/$last/risk'
```

Ces commandes sont destinées à être copiables dans des scripts shell. Utilisez `--json` quand un appelant a besoin d'une sortie structurée et `--human` quand une personne inspecte le résultat.

## Comment ça marche

`openclaw path` fait quatre choses :

1. Parse l'adresse `oc://` en emplacements : fichier, section, élément, champ et session optionnelle.
2. Choisit l'adaptateur de type de fichier à partir de l'extension cible (`.md`, `.jsonc`, `.jsonl`, `.yaml`, `.yml`, `.lobster` et alias connexes).
3. Résout les emplacements par rapport à l'AST de ce type de fichier : titres/éléments markdown, clés d'objet JSONC/index de tableau, enregistrements de ligne JSONL ou nœuds de map/séquence YAML.
4. Pour `set`, émet les octets édités via le même adaptateur pour que les parties non modifiées du fichier conservent leurs commentaires, fins de ligne et formatage environnant où le type le supporte.

`resolve` et `set` nécessitent une cible concrète. `find` est le verbe exploratoire : il développe les caractères génériques, les unions, les prédicats et les ordinaux dans les correspondances concrètes que vous pouvez inspecter avant d'en choisir une à écrire.

## Sous-commandes

| Sous-commande           | Objectif                                                                     |
| ----------------------- | ---------------------------------------------------------------------------- |
| `resolve <oc-path>`     | Affiche la correspondance concrète au chemin (ou « non trouvé »).            |
| `find <pattern>`        | Énumère les correspondances pour un chemin avec caractères génériques / union / prédicat. |
| `set <oc-path> <value>` | Écrit une feuille ou une cible d'insertion à un chemin concret. Supporte `--dry-run`. |
| `validate <oc-path>`    | Parse uniquement ; affiche la décomposition structurelle (fichier / section / élément / champ). |
| `emit <file>`           | Fait un aller-retour d'un fichier via `parseXxx` + `emitXxx` (diagnostic de fidélité d'octet). |

## Drapeaux globaux

| Drapeau         | Objectif                                                                   |
| --------------- | -------------------------------------------------------------------------- |
| `--cwd <dir>`   | Résout l'emplacement du fichier par rapport à ce répertoire (par défaut : `process.cwd()`). |
| `--file <path>` | Remplace le chemin résolu de l'emplacement du fichier (accès absolu).      |
| `--json`        | Force la sortie JSON (par défaut quand stdout n'est pas un TTY).           |
| `--human`       | Force la sortie humaine (par défaut quand stdout est un TTY).              |
| `--dry-run`     | (uniquement sur `set`) affiche les octets qui seraient écrits sans écrire. |
| `--diff`        | (avec `set --dry-run`) affiche un diff unifié au lieu des octets complets. |

## Syntaxe `oc://`

```
oc://FILE/SECTION/ITEM/FIELD?session=SCOPE
```

Règles d'emplacement : `field` nécessite `item`, et `item` nécessite `section`. Sur les quatre emplacements :

- **Segments entre guillemets** — `"a/b.c"` survit aux séparateurs `/` et `.`. Le contenu est littéral en octets ; `"` et `\` ne sont pas autorisés à l'intérieur des guillemets. L'emplacement du fichier est également sensible aux guillemets : `oc://"skills/email-drafter"/Tools/$last` traite `skills/email-drafter` comme un chemin de fichier unique.
- **Prédicats** — `[k=v]`, `[k!=v]`, `[k<v]`, `[k<=v]`, `[k>v]`, `[k>=v]`. Les opérations numériques nécessitent que les deux côtés se coercent en nombres finis.
- **Unions** — `{a,b,c}` correspond à l'une des alternatives.
- **Caractères génériques** — `*` (sous-segment unique) et `**` (zéro ou plus, récursif). `find` les accepte ; `resolve` et `set` les rejettent comme ambigus.
- **Positionnel** — `$first` / `$last` se résolvent au premier / dernier index ou clé déclarée.
- **Ordinal** — `#N` pour la Nième correspondance par ordre de document.
- **Marqueurs d'insertion** — `+`, `+key`, `+nnn` pour l'insertion avec clé / index (à utiliser avec `set`).
- **Portée de session** — `?session=cron-daily` etc. Orthogonal à l'imbrication d'emplacements. Les valeurs de session sont brutes, non décodées en pourcentage ; elles ne peuvent pas contenir de caractères de contrôle ou de délimiteurs de requête réservés (`?`, `&`, `%`).

Les caractères réservés (`?`, `&`, `%`) en dehors des segments entre guillemets, prédicats ou unions sont rejetés. Les caractères de contrôle (U+0000-U+001F, U+007F) sont rejetés partout, y compris dans la valeur de requête `session`.

`formatOcPath(parseOcPath(path)) === path` est garanti pour les chemins canoniques. Les paramètres de requête non canoniques sont ignorés sauf pour la première valeur `session=` non vide.

## Adressage par type de fichier

| Type              | Modèle d'adressage                                                                              |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| Markdown          | Sections H2 par slug, éléments de liste à puces par slug ou `#N`, frontmatter via `[frontmatter]`. |
| JSONC/JSON        | Clés d'objet et index de tableau ; les points divisent les sous-segments imbriqués sauf s'ils sont entre guillemets. |
| JSONL             | Adresses de ligne de haut niveau (`L1`, `L2`, `$first`, `$last`), puis descente de style JSONC à l'intérieur de la ligne. |
| YAML/YML/.lobster | Clés de map et index de séquence ; les commentaires et le style de flux sont gérés par l'API du document YAML. |

`resolve` retourne une correspondance structurée : `root`, `node`, `leaf` ou `insertion-point`, avec un numéro de ligne basé sur 1. Les valeurs de feuille sont surfacées en tant que texte plus un `leafType` pour que les auteurs de plugins puissent afficher des aperçus sans dépendre de la forme AST spécifique au type.

## Contrat de mutation

`set` écrit une cible concrète :

- Les valeurs de frontmatter markdown et les champs d'élément `- key: value` sont des feuilles de chaîne. Les insertions markdown ajoutent des sections, des clés de frontmatter ou des éléments de section et affichent une forme markdown canonique pour le fichier modifié.
- Les écritures de feuille JSONC coercent la valeur de chaîne au type de feuille existant (`string`, `number` fini, `true`/`false` ou `null`). Les insertions d'objet et de tableau JSONC analysent `<value>` en tant que JSON et utilisent le chemin d'édition `jsonc-parser` pour les écritures de feuille ordinaires, préservant les commentaires et le formatage environnant.
- Les écritures de feuille JSONL coercent comme JSONC à l'intérieur d'une ligne. Le remplacement de ligne entière et l'ajout analysent `<value>` en tant que JSON. Le JSONL rendu préserve la convention de fin de ligne LF/CRLF dominante du fichier.
- Les écritures de feuille YAML coercent au type scalaire existant (`string`, `number` fini, `true`/`false` ou `null`). Les insertions YAML utilisent l'API de document du paquet `yaml` groupé pour les mises à jour de map/séquence. Les documents YAML malformés avec des erreurs d'analyse sont refusés avant mutation avec `parse-error`.

Utilisez `--dry-run` avant les écritures visibles par l'utilisateur quand les octets exacts importent. Le substrat préserve la sortie identique en octets pour les aller-retours parse/emit, mais une mutation peut canonicaliser la région éditée ou le fichier selon le type. Ajoutez `--diff` quand vous voulez l'aperçu en tant que patch avant/après ciblé au lieu du fichier rendu complet.

## Exemples

```bash
# Valider un chemin (pas d'accès au système de fichiers)
openclaw path validate 'oc://AGENTS.md/Tools/$last/risk'

# Lire une feuille
openclaw path resolve 'oc://gateway.jsonc/version'

# Recherche avec caractères génériques
openclaw path find 'oc://session.jsonl/*/event' --file ./logs/session.jsonl

# Simulation d'écriture
openclaw path set 'oc://gateway.jsonc/version' '2.0' --dry-run

# Simulation d'écriture sous forme de diff unifié
openclaw path set 'oc://gateway.jsonc/version' '2.0' --dry-run --diff

# Appliquer l'écriture
openclaw path set 'oc://gateway.jsonc/version' '2.0'

# Round-trip avec fidélité au niveau des octets (diagnostic)
openclaw path emit ./AGENTS.md
```

Autres exemples de grammaire :

```bash
# Citer les clés contenant / ou .
openclaw path resolve 'oc://config.jsonc/agents.defaults.models/"anthropic/claude-opus-4-7"/alias'

# Recherche par prédicat sur les enfants JSONC
openclaw path find 'oc://config.jsonc/plugins/[enabled=true]/id'

# Insérer dans un tableau JSONC
openclaw path set 'oc://config.jsonc/items/+1' '{"id":"new","enabled":true}' --dry-run

# Insérer une clé d'objet JSONC
openclaw path set 'oc://config.jsonc/plugins/+github' '{"enabled":true}' --dry-run

# Ajouter un événement JSONL
openclaw path set 'oc://session.jsonl/+' '{"event":"checkpoint","ok":true}' --file ./logs/session.jsonl

# Résoudre la dernière ligne de valeur JSONL
openclaw path resolve 'oc://session.jsonl/$last/event' --file ./logs/session.jsonl

# Résoudre une étape de flux de travail YAML
openclaw path resolve 'oc://workflow.yaml/steps/0/id'

# Mettre à jour un scalaire YAML
openclaw path set 'oc://workflow.yaml/steps/$last/id' 'classify-renamed' --dry-run

# Adresser le frontmatter markdown
openclaw path resolve 'oc://AGENTS.md/[frontmatter]/name'

# Insérer un frontmatter markdown
openclaw path set 'oc://AGENTS.md/[frontmatter]/+description' 'Agent instructions' --dry-run

# Trouver les champs d'éléments markdown
openclaw path find 'oc://SKILL.md/Tools/*/send_email'

# Valider un chemin limité à la session
openclaw path validate 'oc://AGENTS.md/Tools/$last/risk?session=cron-daily'
```

## Recettes par type de fichier

Les mêmes cinq verbes fonctionnent sur tous les types ; le schéma d'adressage se dispatche selon l'extension du fichier. Les exemples ci-dessous utilisent les fixtures de la description de la PR.

### Markdown

```text
<!-- frontmatter.md -->
---
name: drafter
description: email drafting agent
tier: core
---
## Tools
- gh: GitHub CLI
- curl: HTTP client
- send_email: enabled
```

```bash
$ openclaw path resolve 'oc://x.md/[frontmatter]/tier' --file frontmatter.md --human
leaf @ L4: "core" (string)

$ openclaw path resolve 'oc://x.md/tools/gh/gh' --file frontmatter.md --human
leaf @ L9: "GitHub CLI" (string)

$ openclaw path find 'oc://x.md/tools/*' --file frontmatter.md --human
3 matches for oc://x.md/tools/*:
  oc://x.md/tools/gh           →  node @ L9 [md-item]
  oc://x.md/tools/curl         →  node @ L10 [md-item]
  oc://x.md/tools/send-email   →  node @ L11 [md-item]
```

Le prédicat `[frontmatter]` adresse le bloc frontmatter YAML ; `tools` correspond au titre `## Tools` via slug, et les feuilles d'éléments conservent leur forme slug même quand la source utilise des traits de soulignement (`send_email` → `send-email`).

### JSONC

```text
// config.jsonc
{
  "plugins": {
    "github": {"enabled": true, "role": "vcs"},
    "slack":  {"enabled": false, "role": "chat"}
  }
}
```

```bash
$ openclaw path resolve 'oc://config.jsonc/plugins/github/enabled' --file config.jsonc --human
leaf @ L4: "true" (boolean)

$ openclaw path set 'oc://config.jsonc/plugins/slack/enabled' 'true' --file config.jsonc --dry-run
--dry-run: would write 142 bytes to /…/config.jsonc
{
  "plugins": {
    "github": {"enabled": true, "role": "vcs"},
    "slack":  {"enabled": true, "role": "chat"}
  }
}
```

Les éditions JSONC passent par `jsonc-parser`, donc les commentaires et l'espacement survivent à un `set`. Exécutez avec `--dry-run` d'abord pour inspecter les octets avant de valider.

### JSONL

```text
{"event":"start","userId":"u1","ts":1}
{"event":"action","userId":"u1","ts":2}
{"event":"end","userId":"u1","ts":3}
```

```bash
$ openclaw path find 'oc://session.jsonl/[event=action]/userId' --file session.jsonl --human
1 match for oc://session.jsonl/[event=action]/userId:
  oc://session.jsonl/L2/userId  →  leaf @ L2: "u1" (string)

$ openclaw path resolve 'oc://session.jsonl/L2/ts' --file session.jsonl --human
leaf @ L2: "2" (number)
```

Chaque ligne est un enregistrement. Adressez par prédicat (`[event=action]`) quand vous ne connaissez pas le numéro de ligne, ou par le segment canonique `LN` quand vous le connaissez.

### YAML

```text
# workflow.yaml
name: inbox-triage
steps:
  - id: fetch
    command: gmail.search
  - id: classify
    command: openclaw.invoke
```

```bash
$ openclaw path resolve 'oc://workflow.yaml/steps/0/id' --file workflow.yaml --human
leaf @ L3: "fetch" (string)

$ openclaw path set 'oc://workflow.yaml/steps/$last/id' 'classify-renamed' --file workflow.yaml --dry-run
--dry-run: would write 99 bytes to /…/workflow.yaml
name: inbox-triage
steps:
  - id: fetch
    command: gmail.search
  - id: classify-renamed
    command: openclaw.invoke
```

YAML utilise l'API `Document` du paquet `yaml` plutôt qu'un parseur fait à la main, donc les round-trips parse/emit ordinaires préservent les commentaires et la forme de création tandis que les chemins résolus utilisent le même modèle map-key / sequence-index que JSONC. Le même adaptateur gère les fichiers `.yaml`, `.yml` et `.lobster`.

## Référence des sous-commandes

### `resolve <oc-path>`

Lire une feuille ou un nœud unique. Les caractères génériques sont rejetés — utilisez `find` pour ceux-ci.
Sort avec `0` en cas de correspondance, `1` en cas d'absence nette, `2` en cas d'erreur d'analyse ou de motif refusé.

```bash
openclaw path resolve 'oc://AGENTS.md/tools/gh/risk' --human
openclaw path resolve 'oc://gateway.jsonc/server/port' --json
```

### `find <pattern>`

Énumérer chaque correspondance pour un motif avec caractères génériques / prédicat / union. Sort avec `0` en cas d'au moins une correspondance, `1` en cas de zéro. Les caractères génériques d'emplacement de fichier sont rejetés avec `OC_PATH_FILE_WILDCARD_UNSUPPORTED` — passez un fichier concret (le globbing multi-fichiers est une fonctionnalité de suivi).

```bash
openclaw path find 'oc://AGENTS.md/tools/**/risk'
openclaw path find 'oc://session.jsonl/[event=action]/userId'
openclaw path find 'oc://config.jsonc/plugins/{github,slack}/enabled'
```

### `set <oc-path> <value>`

Écrire une feuille. Associez avec `--dry-run` pour prévisualiser les octets qui seraient écrits sans toucher au fichier. Ajoutez `--diff` pour un aperçu de diff unifié.
Sort avec `0` en cas d'écriture réussie, `1` si le substrat refuse (par exemple, une garde sentinelle activée), `2` en cas d'erreurs d'analyse.

```bash
openclaw path set 'oc://gateway.jsonc/version' '2.0' --dry-run
openclaw path set 'oc://gateway.jsonc/version' '2.0' --dry-run --diff
openclaw path set 'oc://gateway.jsonc/version' '2.0'
openclaw path set 'oc://AGENTS.md/Tools/+gh/risk' 'low'
```

Le marqueur d'insertion `+key` crée l'enfant nommé s'il n'existe pas déjà ; `+nnn` et `+` nu fonctionnent respectivement pour l'insertion indexée et l'ajout.

### `validate <oc-path>`

Vérification d'analyse uniquement. Pas d'accès au système de fichiers. Utile quand vous voulez confirmer qu'un chemin de modèle est bien formé avant de substituer des variables, ou quand vous voulez la décomposition structurelle pour le débogage :

```bash
$ openclaw path validate 'oc://AGENTS.md/tools/gh' --human
valid: oc://AGENTS.md/tools/gh
  file:    AGENTS.md
  section: tools
  item:    gh
```

Sort avec `0` quand valide, `1` quand invalide (avec un `code` et un `message` structurés), `2` en cas d'erreurs d'argument.

### `emit <file>`

Round-trip un fichier à travers le parseur et l'émetteur par type. La sortie devrait être identique au niveau des octets à l'entrée sur un fichier sain — la divergence indique un bug du parseur ou une garde sentinelle activée. Utile pour déboguer le comportement du substrat sur des entrées réelles.

```bash
openclaw path emit ./AGENTS.md
openclaw path emit ./gateway.jsonc --json
```

## Codes de sortie

| Code | Signification                                                                    |
| ---- | -------------------------------------------------------------------------- |
| `0`  | Succès. (`resolve` / `find` : au moins une correspondance. `set` : écriture réussie.) |
| `1`  | Pas de correspondance, ou `set` refusé par le substrat (pas d'erreur au niveau système).      |
| `2`  | Erreur d'argument ou d'analyse.                                                   |

## Mode de sortie

`openclaw path` est conscient du TTY : sortie lisible par l'homme sur un terminal, JSON quand stdout est redirigé ou canalisé. `--json` et `--human` remplacent la détection automatique.

## Notes

- `set` écrit les octets via le chemin d'émission du substrat, qui applique automatiquement la garde sentinelle de rédaction. Une feuille portant `__OPENCLAW_REDACTED__` (littéralement ou en tant que sous-chaîne) est refusée au moment de l'écriture.
- L'analyse JSONC et les éditions de feuilles utilisent la dépendance locale du plugin `jsonc-parser`, donc les commentaires et le formatage sont préservés sur les écritures de feuilles ordinaires au lieu de passer par un chemin d'analyse/re-rendu fait à la main.
- `path` ne connaît pas LKG. Si le fichier est suivi par LKG, l'appel observe suivant décide s'il faut promouvoir / récupérer. `set --batch` pour multi-set atomique via le cycle de vie de promotion/récupération LKG est prévu aux côtés du substrat de récupération LKG.

## Connexes

- [Référence CLI](/fr/cli)
