---
summary: "Plugin `oc-path` fourni : fournit la CLI `openclaw path` pour le schéma d'adressage de fichiers d'espace de travail `oc://`"
read_when:
  - You want to inspect or edit a single leaf inside a workspace file from the terminal
  - You are scripting against workspace state and need a stable, kind-agnostic addressing scheme
  - You are deciding whether to enable the optional `oc-path` plugin on a self-hosted Gateway
title: "Plugin OC Path"
---

Le plugin `oc-path` fourni ajoute la CLI [`openclaw path`](/fr/cli/path) pour le
schéma d'adressage de fichiers d'espace de travail `oc://`. Il est fourni dans le dépôt OpenClaw sous
`extensions/oc-path/` mais est optionnel — l'installation/la compilation le laisse dormant jusqu'à ce que vous
l'activiez.

Les adresses `oc://` pointent vers une seule feuille (ou un ensemble de feuilles avec caractères génériques) à l'intérieur
d'un fichier d'espace de travail. Le plugin comprend quatre types de fichiers aujourd'hui :

- **markdown** (`.md`, `.mdx`) : frontmatter, sections, éléments, champs
- **jsonc** (`.jsonc`, `.json5`, `.json`) : commentaires et formatage préservés
- **jsonl** (`.jsonl`, `.ndjson`) : enregistrements orientés ligne
- **yaml** (`.yaml`, `.yml`, `.lobster`) : nœuds map/sequence/scalar via l'API
  du document YAML

Les auto-hébergeurs et les extensions d'éditeur utilisent la CLI pour lire ou écrire une seule feuille
sans écrire de script directement contre le SDK ; les agents et les hooks la traitent comme un
substrat déterministe afin que les allers-retours avec fidélité d'octet et la garde
sentinelle de rédaction s'appliquent uniformément entre les types.

## Pourquoi l'activer

Activez `oc-path` quand vous voulez que les scripts, les hooks ou l'outillage d'agent local pointent
vers une partie précise de l'état de l'espace de travail sans inventer un analyseur pour chaque
forme de fichier. Une seule adresse `oc://` peut nommer une clé de frontmatter markdown, un
élément de section, une feuille de config JSONC, un champ d'événement JSONL, ou une étape de workflow YAML.

C'est important pour les flux de travail des mainteneurs où le changement doit être petit,
auditable et reproductible : inspectez une valeur, trouvez les enregistrements correspondants, faites un essai d'écriture,
puis appliquez uniquement cette feuille tout en laissant les commentaires, les fins de ligne et
le formatage à proximité intacts. Garder ceci comme un plugin optionnel donne aux utilisateurs avancés le
substrat d'adressage sans mettre les dépendances d'analyseur ou la surface CLI dans
le noyau pour les installations qui n'en ont jamais besoin.

Raisons courantes de l'activer :

- **Automatisation locale** : les scripts shell peuvent résoudre ou mettre à jour une valeur d'espace de travail
  avec `openclaw path … --json` au lieu de porter du code d'analyse markdown, JSONC,
  JSONL et YAML séparé.
- **Édits visibles par l'agent** : un agent peut afficher un diff d'essai pour une
  feuille adressée avant d'écrire, ce qui est plus facile à examiner qu'une réécriture de fichier libre.
- **Intégrations d'éditeur** : un éditeur peut mapper `oc://AGENTS.md/tools/gh` au
  nœud markdown exact et au numéro de ligne sans deviner à partir du texte du titre.
- **Diagnostics** : `emit` fait un aller-retour d'un fichier via l'analyseur et l'émetteur, afin que
  vous puissiez vérifier si un type de fichier est stable en octets avant de compter sur des
  édits automatisés.

Exemples concrets :

```bash
# Le plugin GitHub est-il activé dans cette config ?
openclaw path resolve 'oc://config.jsonc/plugins/github/enabled' --json

# Quels noms d'appels d'outils apparaissent dans ce journal de session ?
openclaw path find 'oc://session.jsonl/[event=tool_call]/name' --json

# Quels octets cette minuscule édition de config écrirait-elle ?
openclaw path set 'oc://config.jsonc/plugins/github/enabled' 'true' --dry-run
```

Le plugin n'est intentionnellement pas propriétaire de la sémantique de haut niveau. Les
plugins de mémoire possèdent toujours les écritures de mémoire, les commandes de config possèdent toujours la
gestion complète de la config, et la logique LKG possède toujours la restauration/promotion. `oc-path` est la
couche étroite d'adressage et d'opération de fichier préservant les octets que ces outils de haut niveau
peuvent construire autour.

## Où il s'exécute

Le plugin s'exécute **en processus à l'intérieur de la CLI `openclaw`** sur l'hôte où vous
invoquez la commande. Il n'a pas besoin d'une Gateway en cours d'exécution et n'ouvre aucun
socket réseau — chaque verbe est une transformation pure sur un fichier que vous pointez.

Les métadonnées du plugin se trouvent dans `extensions/oc-path/openclaw.plugin.json` :

```json
{
  "id": "oc-path",
  "name": "OC Path",
  "activation": {
    "onStartup": false,
    "onCommands": ["path"]
  },
  "commandAliases": [{ "name": "path", "kind": "cli" }]
}
```

`onStartup: false` garde le plugin hors du chemin chaud de la Gateway. `onCommands:
["path"]` dit à la CLI de charger le plugin paresseusement la première fois que vous exécutez
`openclaw path …`, afin que les installations qui n'utilisent jamais le verbe ne paient aucun coût.

## Activer

```bash
openclaw plugins enable oc-path
```

Redémarrez la Gateway (si vous en exécutez une) afin que l'instantané du manifeste reprenne le nouvel
état. Les invocations `openclaw path` simples fonctionnent immédiatement sur le même hôte —
la CLI charge le plugin à la demande.

Désactivez avec :

```bash
openclaw plugins disable oc-path
```

## Dépendances

Toutes les dépendances d'analyseur sont locales au plugin — activer `oc-path` ne tire pas
de nouveaux packages dans le runtime principal :

| Dépendance     | Objectif                                                                |
| -------------- | ---------------------------------------------------------------------- |
| `commander`    | Câblage de sous-commande pour `resolve`, `find`, `set`, `validate`, `emit`.    |
| `jsonc-parser` | Analyse JSONC + édits de feuille avec commentaires et virgules finales conservés.       |
| `markdown-it`  | Tokenization Markdown pour le modèle section / élément / champ.            |
| `yaml`         | Analyse YAML `Document` / émission / édition avec commentaires et style de flux conservés. |

JSONL reste fait à la main — l'analyse orientée ligne est plus simple que n'importe quelle
dépendance, et l'analyse JSONC par ligne passe déjà par `jsonc-parser`.

## Ce qu'il fournit

| Surface                        | Fourni par                                             |
| ------------------------------ | ------------------------------------------------------- |
| CLI `openclaw path`            | `extensions/oc-path/cli-registration.ts`                |
| Analyseur / formateur `oc://`     | `extensions/oc-path/src/oc-path/oc-path.ts`             |
| Analyse / émission / édition par type   | `extensions/oc-path/src/oc-path/{md,jsonc,jsonl,yaml}`  |
| Résolution / recherche / définition universelle | `extensions/oc-path/src/oc-path/{resolve,find,edit}.ts` |
| Garde sentinelle de rédaction       | `extensions/oc-path/src/oc-path/sentinel.ts`            |

La CLI est la seule surface publique aujourd'hui. Les verbes de substrat sont privés au
plugin ; les consommateurs utilisent la CLI (ou construisent leur propre plugin contre le SDK).

## Relation avec d'autres plugins

- **`memory-*`** : les écritures de mémoire passent par les plugins de mémoire, pas `oc-path`.
  `oc-path` est un substrat de fichier générique ; les plugins de mémoire superposent leur propre
  sémantique par-dessus.
- **LKG** : `path` ne connaît pas la restauration de config Last-Known-Good. Si un
  fichier est suivi par LKG, l'appel `observe` suivant décide s'il faut promouvoir ou
  récupérer ; `set --batch` pour la multi-définition atomique via le cycle de vie de promotion/récupération LKG est prévu
  aux côtés du substrat de récupération LKG.

## Sécurité

`set` écrit des octets bruts via le chemin d'émission du substrat, qui applique la
garde sentinelle de rédaction automatiquement. Une feuille portant
`__OPENCLAW_REDACTED__` (littéralement ou en tant que sous-chaîne) est refusée au moment de l'écriture
avec `OC_EMIT_SENTINEL`. La CLI nettoie également le sentinelle littéral de toute
sortie humaine ou JSON qu'elle imprime, le remplaçant par `[REDACTED]` afin que les
captures de terminal et les pipelines ne fuient jamais le marqueur.

## Connexes

- [Référence CLI `openclaw path`](/fr/cli/path)
- [Gérer les plugins](/fr/plugins/manage-plugins)
- [Construire des plugins](/fr/plugins/building-plugins)
