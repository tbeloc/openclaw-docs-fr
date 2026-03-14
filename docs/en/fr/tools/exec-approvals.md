---
summary: "Approbations exec, listes blanches et invites d'échappement sandbox"
read_when:
  - Configuring exec approvals or allowlists
  - Implementing exec approval UX in the macOS app
  - Reviewing sandbox escape prompts and implications
title: "Approbations Exec"
---

# Approbations exec

Les approbations exec sont le **garde-fou de l'application compagne / hôte nœud** permettant à un agent en sandbox d'exécuter
des commandes sur un vrai hôte (`gateway` ou `node`). Pensez-y comme un verrouillage de sécurité :
les commandes ne sont autorisées que lorsque la politique + la liste blanche + (optionnellement) l'approbation utilisateur sont d'accord.
Les approbations exec s'ajoutent **en plus** à la politique d'outils et au contrôle d'accès élevé (sauf si elevated est défini à `full`, ce qui ignore les approbations).
La politique effective est la **plus stricte** entre `tools.exec.*` et les valeurs par défaut des approbations ; si un champ d'approbations est omis, la valeur `tools.exec` est utilisée.

Si l'interface utilisateur de l'application compagne n'est **pas disponible**, toute demande nécessitant une invite est
résolue par le **secours ask** (par défaut : refuser).

## Où cela s'applique

Les approbations exec sont appliquées localement sur l'hôte d'exécution :

- **hôte gateway** → processus `openclaw` sur la machine gateway
- **hôte node** → node runner (application compagne macOS ou hôte node sans interface)

Note sur le modèle de confiance :

- Les appelants authentifiés par Gateway sont des opérateurs de confiance pour ce Gateway.
- Les nœuds appairés étendent cette capacité d'opérateur de confiance à l'hôte nœud.
- Les approbations exec réduisent le risque d'exécution accidentelle, mais ne constituent pas une limite d'authentification par utilisateur.
- Les exécutions approuvées sur nœud-hôte lient le contexte d'exécution canonique : cwd canonique, argv exact, liaison env
  le cas échéant, et chemin exécutable épinglé le cas échéant.
- Pour les scripts shell et les invocations directes de fichiers interpréteur/runtime, OpenClaw essaie également de lier
  un opérande de fichier local concret. Si ce fichier lié change après approbation mais avant exécution,
  l'exécution est refusée au lieu d'exécuter du contenu modifié.
- Cette liaison de fichier est intentionnellement au mieux, pas un modèle sémantique complet de chaque
  chemin de chargeur interpréteur/runtime. Si le mode approbation ne peut pas identifier exactement un fichier local concret à lier, il refuse de créer une exécution soutenue par approbation au lieu de prétendre à une couverture complète.

Division macOS :

- **service nœud hôte** transfère `system.run` à l'**application macOS** via IPC local.
- **application macOS** applique les approbations + exécute la commande dans le contexte UI.

## Paramètres et stockage

Les approbations vivent dans un fichier JSON local sur l'hôte d'exécution :

`~/.openclaw/exec-approvals.json`

Exemple de schéma :

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

## Boutons de politique

### Sécurité (`exec.security`)

- **deny**: bloquer toutes les demandes d'exécution hôte.
- **allowlist**: autoriser uniquement les commandes de la liste blanche.
- **full**: autoriser tout (équivalent à elevated).

### Ask (`exec.ask`)

- **off**: ne jamais inviter.
- **on-miss**: inviter uniquement lorsque la liste blanche ne correspond pas.
- **always**: inviter à chaque commande.

### Secours ask (`askFallback`)

Si une invite est requise mais qu'aucune interface utilisateur n'est accessible, le secours décide :

- **deny**: bloquer.
- **allowlist**: autoriser uniquement si la liste blanche correspond.
- **full**: autoriser.

## Liste blanche (par agent)

Les listes blanches sont **par agent**. Si plusieurs agents existent, basculez l'agent que vous
modifiez dans l'application macOS. Les motifs sont des **correspondances glob insensibles à la casse**.
Les motifs doivent se résoudre en **chemins binaires** (les entrées basename uniquement sont ignorées).
Les entrées héritées `agents.default` sont migrées vers `agents.main` au chargement.

Exemples :

- `~/Projects/**/bin/peekaboo`
- `~/.local/bin/*`
- `/opt/homebrew/bin/rg`

Chaque entrée de liste blanche suit :

- **id** UUID stable utilisé pour l'identité UI (optionnel)
- **last used** horodatage
- **last used command** dernière commande utilisée
- **last resolved path** dernier chemin résolu

## Auto-allow skill CLIs

Lorsque **Auto-allow skill CLIs** est activé, les exécutables référencés par les compétences connues
sont traités comme étant sur liste blanche sur les nœuds (nœud macOS ou hôte nœud sans interface). Cela utilise
`skills.bins` via l'appel RPC Gateway pour récupérer la liste des bins de compétences. Désactivez ceci si vous voulez des listes blanches strictement manuelles.

Notes importantes sur la confiance :

- C'est une **liste blanche de commodité implicite**, séparée des entrées de liste blanche de chemin manuel.
- Elle est destinée aux environnements d'opérateurs de confiance où Gateway et nœud sont dans la même limite de confiance.
- Si vous exigez une confiance explicite stricte, gardez `autoAllowSkills: false` et utilisez uniquement les entrées de liste blanche de chemin manuel.

## Bins sûrs (stdin uniquement)

`tools.exec.safeBins` définit une petite liste de **stdin uniquement** binaires (par exemple `jq`)
qui peuvent s'exécuter en mode liste blanche **sans** entrées de liste blanche explicites. Les bins sûrs rejettent
les arguments de fichier positionnels et les jetons de type chemin, ils ne peuvent donc fonctionner que sur le flux entrant.
Traitez ceci comme un chemin rapide étroit pour les filtres de flux, pas une liste de confiance générale.
Ne **pas** ajouter les binaires interpréteur ou runtime (par exemple `python3`, `node`, `ruby`, `bash`, `sh`, `zsh`) à `safeBins`.
Si une commande peut évaluer du code, exécuter des sous-commandes ou lire des fichiers par conception, préférez les entrées de liste blanche explicites et gardez les invites d'approbation activées.
Les bins sûrs personnalisés doivent définir un profil explicite dans `tools.exec.safeBinProfiles.<bin>`.
La validation est déterministe à partir de la forme argv uniquement (pas de vérifications d'existence du système de fichiers hôte), ce qui
empêche le comportement d'oracle d'existence de fichier à partir des différences allow/deny.
Les options orientées fichier sont refusées pour les bins sûrs par défaut (par exemple `sort -o`, `sort --output`,
`sort --files0-from`, `sort --compress-program`, `sort --random-source`,
`sort --temporary-directory`/`-T`, `wc --files0-from`, `jq -f/--from-file`,
`grep -f/--file`).
Les bins sûrs appliquent également une politique de drapeau explicite par binaire pour les options qui cassent le comportement stdin uniquement (par exemple `sort -o/--output/--compress-program` et les drapeaux récursifs grep).
Les options longues sont validées en échec fermé en mode bin sûr : les drapeaux inconnus et les
abréviations ambiguës sont rejetés.
Drapeaux refusés par profil bin sûr :

<!-- SAFE_BIN_DENIED_FLAGS:START -->

- `grep`: `--dereference-recursive`, `--directories`, `--exclude-from`, `--file`, `--recursive`, `-R`, `-d`, `-f`, `-r`
- `jq`: `--argfile`, `--from-file`, `--library-path`, `--rawfile`, `--slurpfile`, `-L`, `-f`
- `sort`: `--compress-program`, `--files0-from`, `--output`, `--random-source`, `--temporary-directory`, `-T`, `-o`
- `wc`: `--files0-from`
<!-- SAFE_BIN_DENIED_FLAGS:END -->

Les bins sûrs forcent également les jetons argv à être traités comme du **texte littéral** au moment de l'exécution (pas de globbing
et pas d'expansion `$VARS`) pour les segments stdin uniquement, donc les motifs comme `*` ou `$HOME/...` ne peuvent pas être
utilisés pour contrebander des lectures de fichier.
Les bins sûrs doivent également se résoudre à partir de répertoires binaires de confiance (valeurs par défaut système plus
`tools.exec.safeBinTrustedDirs` optionnel). Les entrées `PATH` ne sont jamais auto-approuvées.
Les répertoires de bins sûrs de confiance par défaut sont intentionnellement minimaux : `/bin`, `/usr/bin`.
Si votre exécutable bin sûr se trouve dans des chemins de gestionnaire de paquets/utilisateur (par exemple
`/opt/homebrew/bin`, `/usr/local/bin`, `/opt/local/bin`, `/snap/bin`), ajoutez-les explicitement
à `tools.exec.safeBinTrustedDirs`.
Le chaînage shell et les redirections ne sont pas auto-autorisés en mode liste blanche.

Le chaînage shell (`&&`, `||`, `;`) est autorisé lorsque chaque segment de niveau supérieur satisfait la liste blanche
(y compris les bins sûrs ou l'auto-allow de compétences). Les redirections restent non supportées en mode liste blanche.
La substitution de commande (`$()` / backticks) est rejetée lors de l'analyse de la liste blanche, y compris à l'intérieur
des guillemets doubles ; utilisez des guillemets simples si vous avez besoin de texte littéral `$()`.
Sur les approbations de l'application compagne macOS, le texte shell brut contenant le contrôle shell ou la syntaxe d'expansion
(`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) est traité comme un manque de liste blanche sauf si
le binaire shell lui-même est sur liste blanche.
Pour les wrappers shell (`bash|sh|zsh ... -c/-lc`), les remplacements env au niveau de la demande sont réduits à une
petite liste explicite (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`).
Pour les décisions allow-always en mode liste blanche, les wrappers de dispatch connus
(`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persistent les chemins exécutables internes au lieu des chemins wrapper.
Les multiplexeurs shell (`busybox`, `toybox`) sont également dépliés pour les applets shell (`sh`, `ash`,
etc.) donc les exécutables internes sont persistés au lieu des binaires multiplexeur. Si un wrapper ou
un multiplexeur ne peut pas être déplie en toute sécurité, aucune entrée de liste blanche n'est persistée automatiquement.

Bins sûrs par défaut : `jq`, `cut`, `uniq`, `head`, `tail`, `tr`, `wc`.

`grep` et `sort` ne sont pas dans la liste par défaut. Si vous optez pour, gardez les entrées de liste blanche explicites pour
leurs flux de travail non-stdin.
Pour `grep` en mode bin sûr, fournissez le motif avec `-e`/`--regexp` ; la forme de motif positionnelle est
rejetée donc les opérandes de fichier ne peuvent pas être contrebandés comme positionnels ambigus.

### Bins sûrs versus liste blanche

| Sujet            | `tools.exec.safeBins`                                  | Liste blanche (`exec-approvals.json`)                            |
| ---------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Objectif         | Auto-allow filtres stdin étroits                       | Faire confiance explicitement à des exécutables spécifiques                        |
| Type de correspondance       | Nom exécutable + politique argv bin sûr                 | Motif glob de chemin exécutable résolu                        |
| Portée d'argument   | Restreint par profil bin sûr et règles de jetons littéraux | Correspondance de chemin uniquement ; les arguments sont sinon votre responsabilité |
| Exemples typiques | `jq`, `head`, `tail`, `wc`                             | `python3`, `node`, `ffmpeg`, CLIs personnalisés                     |
| Meilleure utilisation         | Transformations de texte à faible risque dans les pipelines                  | N'importe quel outil avec un comportement plus large ou des effets secondaires               |

Emplacement de configuration :

- `safeBins` provient de la config (`tools.exec.safeBins` ou par agent `agents.list[].tools.exec.safeBins`).
- `safeBinTrustedDirs` provient de la config (`tools.exec.safeBinTrustedDirs` ou par agent `agents.list[].tools.exec.safeBinTrustedDirs`).
- `safeBinProfiles` provient de la config (`tools.exec.safeBinProfiles` ou par agent `agents.list[].tools.exec.safeBinProfiles`). Les clés de profil par agent remplacent les clés globales.
- les entrées de liste blanche vivent dans `~/.openclaw/exec-approvals.json` local à l'hôte sous `agents.<id>.allowlist` (ou via Control UI / `openclaw approvals allowlist ...`).
