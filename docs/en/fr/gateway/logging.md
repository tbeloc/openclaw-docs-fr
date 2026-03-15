---
summary: "Surfaces de journalisation, journaux de fichiers, styles de journaux WS et formatage de console"
read_when:
  - Changing logging output or formats
  - Debugging CLI or gateway output
title: "Journalisation"
---

# Journalisation

Pour un aperçu destiné aux utilisateurs (CLI + Control UI + config), voir [/logging](/fr/logging).

OpenClaw dispose de deux « surfaces » de journalisation :

- **Sortie console** (ce que vous voyez dans le terminal / Debug UI).
- **Journaux de fichiers** (JSON lines) écrits par le logger de la passerelle.

## Logger basé sur fichier

- Le fichier journal roulant par défaut se trouve sous `/tmp/openclaw/` (un fichier par jour) : `openclaw-YYYY-MM-DD.log`
  - La date utilise le fuseau horaire local de l'hôte de la passerelle.
- Le chemin du fichier journal et le niveau peuvent être configurés via `~/.openclaw/openclaw.json` :
  - `logging.file`
  - `logging.level`

Le format du fichier est un objet JSON par ligne.

L'onglet Logs de la Control UI suit ce fichier via la passerelle (`logs.tail`).
La CLI peut faire de même :

```bash
openclaw logs --follow
```

**Verbose vs. niveaux de journalisation**

- Les **journaux de fichiers** sont contrôlés exclusivement par `logging.level`.
- `--verbose` affecte uniquement la **verbosité de la console** (et le style de journalisation WS) ; il n'élève **pas**
  le niveau de journalisation des fichiers.
- Pour capturer les détails verbose uniquement dans les journaux de fichiers, définissez `logging.level` sur `debug` ou
  `trace`.

## Capture de console

La CLI capture `console.log/info/warn/error/debug/trace` et les écrit dans les journaux de fichiers,
tout en les imprimant sur stdout/stderr.

Vous pouvez ajuster la verbosité de la console indépendamment via :

- `logging.consoleLevel` (par défaut `info`)
- `logging.consoleStyle` (`pretty` | `compact` | `json`)

## Rédaction du résumé des outils

Les résumés d'outils verbose (par ex. `🛠️ Exec: ...`) peuvent masquer les jetons sensibles avant qu'ils ne frappent le
flux de console. Ceci est **outils uniquement** et ne modifie pas les journaux de fichiers.

- `logging.redactSensitive` : `off` | `tools` (par défaut : `tools`)
- `logging.redactPatterns` : tableau de chaînes regex (remplace les valeurs par défaut)
  - Utilisez des chaînes regex brutes (auto `gi`), ou `/pattern/flags` si vous avez besoin de drapeaux personnalisés.
  - Les correspondances sont masquées en conservant les 6 premiers + 4 derniers caractères (longueur >= 18), sinon `***`.
  - Les valeurs par défaut couvrent les attributions de clés courantes, les drapeaux CLI, les champs JSON, les en-têtes bearer, les blocs PEM et les préfixes de jetons populaires.

## Journaux WebSocket de la passerelle

La passerelle imprime les journaux du protocole WebSocket en deux modes :

- **Mode normal (sans `--verbose`)** : seuls les résultats RPC « intéressants » sont imprimés :
  - erreurs (`ok=false`)
  - appels lents (seuil par défaut : `>= 50ms`)
  - erreurs d'analyse
- **Mode verbose (`--verbose`)** : imprime tout le trafic de requête/réponse WS.

### Style de journalisation WS

`openclaw gateway` supporte un commutateur de style par passerelle :

- `--ws-log auto` (par défaut) : le mode normal est optimisé ; le mode verbose utilise une sortie compacte
- `--ws-log compact` : sortie compacte (requête/réponse appairées) en mode verbose
- `--ws-log full` : sortie complète par frame en mode verbose
- `--compact` : alias pour `--ws-log compact`

Exemples :

```bash
# optimisé (erreurs/lent uniquement)
openclaw gateway

# afficher tout le trafic WS (appairé)
openclaw gateway --verbose --ws-log compact

# afficher tout le trafic WS (métadonnées complètes)
openclaw gateway --verbose --ws-log full
```

## Formatage de console (journalisation des sous-systèmes)

Le formateur de console est **conscient du TTY** et imprime des lignes cohérentes et préfixées.
Les loggers de sous-systèmes gardent la sortie groupée et analysable.

Comportement :

- **Préfixes de sous-systèmes** sur chaque ligne (par ex. `[gateway]`, `[canvas]`, `[tailscale]`)
- **Couleurs de sous-systèmes** (stables par sous-système) plus coloration de niveau
- **Couleur lorsque la sortie est un TTY ou que l'environnement ressemble à un terminal riche** (`TERM`/`COLORTERM`/`TERM_PROGRAM`), respecte `NO_COLOR`
- **Préfixes de sous-systèmes raccourcis** : supprime `gateway/` + `channels/` au début, conserve les 2 derniers segments (par ex. `whatsapp/outbound`)
- **Sous-loggers par sous-système** (préfixe automatique + champ structuré `{ subsystem }`)
- **`logRaw()`** pour la sortie QR/UX (pas de préfixe, pas de formatage)
- **Styles de console** (par ex. `pretty | compact | json`)
- **Niveau de journalisation de console** séparé du niveau de journalisation de fichier (le fichier conserve tous les détails lorsque `logging.level` est défini sur `debug`/`trace`)
- **Les corps de messages WhatsApp** sont journalisés à `debug` (utilisez `--verbose` pour les voir)

Cela maintient les journaux de fichiers existants stables tout en rendant la sortie interactive analysable.
