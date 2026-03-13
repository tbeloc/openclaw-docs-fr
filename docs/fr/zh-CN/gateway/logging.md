---
read_when:
  - Modification de la sortie ou du format des journaux
  - Débogage de la sortie CLI ou Gateway
summary: Interface de sortie des journaux, journaux de fichiers, styles de journaux WS et formatage de la console
title: Journalisation
x-i18n:
  generated_at: "2026-02-03T07:48:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: efb8eda5e77e3809369a8ff569fac110323a86b3945797093f20e9bc98f39b2e
  source_path: gateway/logging.md
  workflow: 15
---

# Journalisation

Pour un aperçu orienté utilisateur (CLI + Control UI + configuration), consultez [/logging](/logging).

OpenClaw dispose de deux « interfaces » de journalisation :

- **Sortie console** (ce que vous voyez dans le terminal / Debug UI).
- **Journaux de fichiers** (lignes JSON) écrits par le logger Gateway.

## Logger basé sur les fichiers

- Les fichiers journaux rotatifs par défaut se trouvent sous `/tmp/openclaw/` (un fichier par jour) : `openclaw-YYYY-MM-DD.log`
  - La date utilise le fuseau horaire local de l'hôte Gateway.
- Le chemin du fichier journal et le niveau peuvent être configurés via `~/.openclaw/openclaw.json` :
  - `logging.file`
  - `logging.level`

Le format du fichier est un objet JSON par ligne.

L'onglet Logs de Control UI suit ce fichier via Gateway (`logs.tail`). Le CLI peut également le faire :

```bash
openclaw logs --follow
```

**Verbose vs niveau de journalisation**

- **Les journaux de fichiers** sont entièrement contrôlés par `logging.level`.
- `--verbose` affecte uniquement la **verbosité de la console** (et le style des journaux WS) ; il **n'augmente pas** le niveau de journalisation des fichiers.
- Pour capturer les détails verbose uniquement dans les journaux de fichiers, définissez `logging.level` sur `debug` ou `trace`.

## Capture de console

Le CLI capture `console.log/info/warn/error/debug/trace` et les écrit dans les journaux de fichiers, tout en les imprimant toujours sur stdout/stderr.

Vous pouvez ajuster indépendamment la verbosité de la console :

- `logging.consoleLevel` (par défaut `info`)
- `logging.consoleStyle` (`pretty` | `compact` | `json`)

## Rédaction des résumés d'outils

Les résumés d'outils détaillés (par exemple `🛠️ Exec: ...`) peuvent masquer les jetons sensibles avant d'entrer dans le flux de console. Ceci est **limité aux outils** et ne modifie pas les journaux de fichiers.

- `logging.redactSensitive` : `off` | `tools` (par défaut : `tools`)
- `logging.redactPatterns` : tableau de chaînes d'expressions régulières (remplace les valeurs par défaut)
  - Utilisez des chaînes regex brutes (automatiquement `gi`), ou `/pattern/flags` si vous avez besoin de drapeaux personnalisés.
  - Les correspondances sont masquées en conservant les 6 premiers + 4 derniers caractères (longueur >= 18), sinon `***`.
  - Les valeurs par défaut couvrent les assignations de clés courantes, les drapeaux CLI, les champs JSON, les en-têtes bearer, les blocs PEM et les préfixes de jetons populaires.

## Journaux WebSocket Gateway

Gateway imprime les journaux du protocole WebSocket en deux modes :

- **Mode normal (sans `--verbose`)** : imprime uniquement les résultats RPC « intéressants » :
  - Erreurs (`ok=false`)
  - Appels lents (seuil par défaut : `>= 50ms`)
  - Erreurs d'analyse
- **Mode verbose (`--verbose`)** : imprime tout le trafic des requêtes/réponses WS.

### Style des journaux WS

`openclaw gateway` supporte le changement de style par Gateway :

- `--ws-log auto` (par défaut) : le mode normal est optimisé ; le mode verbose utilise une sortie compacte
- `--ws-log compact` : utilise une sortie compacte en mode verbose (requêtes/réponses appairées)
- `--ws-log full` : utilise une sortie complète par trame en mode verbose
- `--compact` : alias pour `--ws-log compact`

Exemples :

```bash
# Optimisé (erreurs/appels lents uniquement)
openclaw gateway

# Affiche tout le trafic WS (appairé)
openclaw gateway --verbose --ws-log compact

# Affiche tout le trafic WS (métadonnées complètes)
openclaw gateway --verbose --ws-log full
```

## Formatage de la console (journaux des sous-systèmes)

Le formateur de console est **conscient du TTY** et imprime des lignes avec préfixes cohérents. Les loggers des sous-systèmes maintiennent la sortie groupée et facile à scanner.

Comportement :

- Chaque ligne a un **préfixe de sous-système** (par exemple `[gateway]`, `[canvas]`, `[tailscale]`)
- **Couleurs de sous-système** (stables par sous-système) plus coloration du niveau
- **Coloration lorsque la sortie est un TTY ou que l'environnement ressemble à un terminal riche** (`TERM`/`COLORTERM`/`TERM_PROGRAM`), en respectant `NO_COLOR`
- **Préfixes de sous-système raccourcis** : supprime les `gateway/` + `channels/` de début, conserve les 2 derniers segments (par exemple `whatsapp/outbound`)
- **Loggers enfants par sous-système** (préfixe automatique + champ structuré `{ subsystem }`)
- **`logRaw()`** pour la sortie QR/UX (sans préfixe, sans formatage)
- **Style de console** (par exemple `pretty | compact | json`)
- **Niveau de journalisation de la console** séparé du niveau de journalisation des fichiers (lorsque `logging.level` est défini sur `debug`/`trace`, le fichier conserve les détails complets)
- **Corps des messages WhatsApp** enregistrés au niveau `debug` (utilisez `--verbose` pour les voir)

Cela maintient la stabilité des journaux de fichiers existants tout en rendant la sortie interactive facile à scanner.
