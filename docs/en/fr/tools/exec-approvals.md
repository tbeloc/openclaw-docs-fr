---
summary: "Approbations exec, listes blanches et invites d'échappement sandbox"
read_when:
  - Configuring exec approvals or allowlists
  - Implementing exec approval UX in the macOS app
  - Reviewing sandbox escape prompts and implications
title: "Approbations Exec"
---

# Approbations exec

Les approbations exec sont la **garde-fou de l'application compagne / hôte nœud** permettant à un agent en sandbox d'exécuter
des commandes sur un vrai hôte (`gateway` ou `node`). Pensez-y comme un verrouillage de sécurité :
les commandes ne sont autorisées que lorsque la politique + la liste blanche + (optionnellement) l'approbation utilisateur sont d'accord.
Les approbations exec s'ajoutent à la politique d'outils et au contrôle d'élévation (sauf si elevated est défini sur `full`, ce qui ignore les approbations).
La politique effective est la **plus stricte** entre `tools.exec.*` et les valeurs par défaut des approbations ; si un champ d'approbations est omis, la valeur `tools.exec` est utilisée.

Si l'interface utilisateur de l'application compagne n'est **pas disponible**, toute demande nécessitant une invite est
résolue par le **fallback ask** (par défaut : refuser).

## Où cela s'applique

Les approbations exec sont appliquées localement sur l'hôte d'exécution :

- **hôte gateway** → processus `openclaw` sur la machine gateway
- **hôte node** → node runner (application compagne macOS ou hôte node headless)

Note sur le modèle de confiance :

- Les appelants authentifiés par Gateway sont des opérateurs de confiance pour ce Gateway.
- Les nœuds appairés étendent cette capacité d'opérateur de confiance à l'hôte nœud.
- Les approbations exec réduisent le risque d'exécution accidentelle, mais ne constituent pas une limite d'authentification par utilisateur.
- Les exécutions approuvées sur nœud-hôte lient le contexte d'exécution canonique : cwd canonique, argv exact, liaison env
  le cas échéant, et chemin exécutable épinglé le cas échéant.
- Pour les scripts shell et les invocations directes d'interpréteur/fichier runtime, OpenClaw essaie également de lier
  un opérande de fichier local concret. Si ce fichier lié change après approbation mais avant exécution,
  l'exécution est refusée au lieu d'exécuter du contenu modifié.
- Cette liaison de fichier est intentionnellement au mieux, pas un modèle sémantique complet de chaque
  chemin de chargeur d'interpréteur/runtime. Si le mode approbation ne peut pas identifier exactement un fichier local concret à lier, il refuse de créer une exécution soutenue par approbation au lieu de prétendre une couverture complète.

Division macOS :

- **service hôte nœud** transfère `system.run` à l'**application macOS** via IPC local.
- **application macOS** applique les approbations + exécute la commande dans le contexte UI.

## Paramètres et stockage

Les approbations vivent dans un fichier JSON local sur l'hôte d'exécution :

`~/.openclaw/exec-approvals.json`

Schéma d'exemple :

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

- **deny**: bloquer toutes les demandes d'exec hôte.
- **allowlist**: autoriser uniquement les commandes en liste blanche.
- **full**: autoriser tout (équivalent à elevated).

### Ask (`exec.ask`)

- **off**: ne jamais inviter.
- **on-miss**: inviter uniquement lorsque la liste blanche ne correspond pas.
- **always**: inviter à chaque commande.

### Ask fallback (`askFallback`)

Si une invite est requise mais qu'aucune interface utilisateur n'est accessible, le fallback décide :

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
- **last used** timestamp
- **last used command**
- **last resolved path**

## Auto-allow skill CLIs

Lorsque **Auto-allow skill CLIs** est activé, les exécutables référencés par les compétences connues
sont traités comme en liste blanche sur les nœuds (nœud macOS ou hôte nœud headless). Cela utilise
`skills.bins` sur l'appel RPC Gateway pour récupérer la liste des bins de compétences. Désactivez ceci si vous voulez des listes blanches manuelles strictes.

Notes de confiance importantes :

- C'est une **liste blanche de commodité implicite**, séparée des entrées de liste blanche de chemin manuel.
- Elle est destinée aux environnements d'opérateurs de confiance où Gateway et nœud sont dans la même limite de confiance.
- Si vous avez besoin d'une confiance explicite stricte, gardez `autoAllowSkills: false` et utilisez uniquement les entrées de liste blanche de chemin manuel.

## Bins sûrs (stdin uniquement)

`tools.exec.safeBins` définit une petite liste de binaires **stdin uniquement** (par exemple `jq`)
qui peuvent s'exécuter en mode liste blanche **sans** entrées de liste blanche explicites. Les bins sûrs rejettent
les arguments de fichier positionnels et les jetons de type chemin, ils ne peuvent donc fonctionner que sur le flux entrant.
Traitez ceci comme un chemin rapide étroit pour les filtres de flux, pas une liste de confiance générale.
Ne **pas** ajouter d'interpréteur ou de binaires runtime (par exemple `python3`, `node`, `ruby`, `bash`, `sh`, `zsh`) à `safeBins`.
Si une commande peut évaluer du code, exécuter des sous-commandes ou lire des fichiers par conception, préférez les entrées de liste blanche explicites et gardez les invites d'approbation activées.
Les bins sûrs personnalisés doivent définir un profil explicite dans `tools.exec.safeBinProfiles.<bin>`.
La validation est déterministe à partir de la forme argv uniquement (pas de vérifications d'existence du système de fichiers hôte), ce qui
empêche le comportement d'oracle d'existence de fichier à partir des différences allow/deny.
Les options orientées fichier sont refusées pour les bins sûrs par défaut (par exemple `sort -o`, `sort --output`,
`sort --files0-from`, `sort --compress-program`, `sort --random-source`,
`sort --temporary-directory`/`-T`, `wc --files0-from`, `jq -f/--from-file`,
`grep -f/--file`).
Les bins sûrs appliquent également une politique de drapeau explicite par binaire pour les options qui cassent le comportement stdin uniquement (par exemple `sort -o/--output/--compress-program` et les drapeaux récursifs grep).
Les options longues sont validées fail-closed en mode safe-bin : les drapeaux inconnus et les
abréviations ambiguës sont rejetés.
Drapeaux refusés par profil safe-bin :

[//]: # "SAFE_BIN_DENIED_FLAGS:START"

- `grep`: `--dereference-recursive`, `--directories`, `--exclude-from`, `--file`, `--recursive`, `-R`, `-d`, `-f`, `-r`
- `jq`: `--argfile`, `--from-file`, `--library-path`, `--rawfile`, `--slurpfile`, `-L`, `-f`
- `sort`: `--compress-program`, `--files0-from`, `--output`, `--random-source`, `--temporary-directory`, `-T`, `-o`
- `wc`: `--files0-from`

[//]: # "SAFE_BIN_DENIED_FLAGS:END"

Les bins sûrs forcent également les jetons argv à être traités comme du **texte littéral** au moment de l'exécution (pas de globbing
et pas d'expansion `$VARS`) pour les segments stdin uniquement, donc les motifs comme `*` ou `$HOME/...` ne peuvent pas être
utilisés pour contrebander des lectures de fichier.
Les bins sûrs doivent également se résoudre à partir de répertoires binaires de confiance (valeurs par défaut système plus
`tools.exec.safeBinTrustedDirs` optionnel). Les entrées `PATH` ne sont jamais auto-approuvées.
Les répertoires safe-bin de confiance par défaut sont intentionnellement minimaux : `/bin`, `/usr/bin`.
Si votre exécutable safe-bin se trouve dans des chemins de gestionnaire de paquets/utilisateur (par exemple
`/opt/homebrew/bin`, `/usr/local/bin`, `/opt/local/bin`, `/snap/bin`), ajoutez-les explicitement
à `tools.exec.safeBinTrustedDirs`.
Le chaînage shell et les redirections ne sont pas auto-autorisés en mode liste blanche.

Le chaînage shell (`&&`, `||`, `;`) est autorisé lorsque chaque segment de niveau supérieur satisfait la liste blanche
(y compris les bins sûrs ou l'auto-allow de compétences). Les redirections restent non supportées en mode liste blanche.
La substitution de commande (`$()` / backticks) est rejetée lors de l'analyse de la liste blanche, y compris à l'intérieur
des guillemets doubles ; utilisez des guillemets simples si vous avez besoin de texte littéral `$()`.
Sur les approbations de l'application compagne macOS, le texte shell brut contenant le contrôle shell ou la syntaxe d'expansion
(`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) est traité comme une absence de liste blanche sauf si
le binaire shell lui-même est en liste blanche.
Pour les wrappers shell (`bash|sh|zsh ... -c/-lc`), les remplacements env de portée de demande sont réduits à une
petite liste explicite (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`).
Pour les décisions allow-always en mode liste blanche, les wrappers de dispatch connus
(`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persistent les chemins exécutables internes au lieu des chemins wrapper.
Les multiplexeurs shell (`busybox`, `toybox`) sont également dépliés pour les applets shell (`sh`, `ash`,
etc.) donc les exécutables internes sont persistés au lieu des binaires multiplexeur. Si un wrapper ou
un multiplexeur ne peut pas être dépilé en toute sécurité, aucune entrée de liste blanche n'est persistée automatiquement.

Bins sûrs par défaut : `jq`, `cut`, `uniq`, `head`, `tail`, `tr`, `wc`.

`grep` et `sort` ne sont pas dans la liste par défaut. Si vous optez pour, gardez des entrées de liste blanche explicites pour
leurs flux de travail non-stdin.
Pour `grep` en mode safe-bin, fournissez le motif avec `-e`/`--regexp` ; la forme de motif positionnelle est
rejetée donc les opérandes de fichier ne peuvent pas être contrebandés comme positionnels ambigus.

### Bins sûrs versus liste blanche

| Sujet            | `tools.exec.safeBins`                                  | Liste blanche (`exec-approvals.json`)                            |
| ---------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Objectif         | Auto-allow narrow stdin filters                        | Faire confiance explicitement à des exécutables spécifiques                        |
| Type de correspondance       | Nom exécutable + politique argv safe-bin                 | Motif glob de chemin exécutable résolu                        |
| Portée d'argument   | Restreint par profil safe-bin et règles de jetons littéraux | Correspondance de chemin uniquement ; les arguments sont sinon votre responsabilité |
| Exemples typiques | `jq`, `head`, `tail`, `wc`                             | `python3`, `node`, `ffmpeg`, CLIs personnalisés                     |
| Meilleure utilisation         | Transformations de texte à faible risque dans les pipelines                  | Tout outil avec un comportement plus large ou des effets secondaires               |

Emplacement de configuration :

- `safeBins` provient de la config (`tools.exec.safeBins` ou par agent `agents.list[].tools.exec.safeBins`).
- `safeBinTrustedDirs` provient de la config (`tools.exec.safeBinTrustedDirs` ou par agent `agents.list[].tools.exec.safeBinTrustedDirs`).
- `safeBinProfiles` provient de la config (`tools.exec.safeBinProfiles` ou par agent `agents.list[].tools.exec.safeBinProfiles`). Les clés de profil par agent remplacent les clés globales.
- les entrées de liste blanche vivent dans `~/.openclaw/exec-approvals.json` local à l'hôte sous `agents.<id>.allowlist` (ou via Control UI / `openclaw approvals allowlist ...`).
- `openclaw security audit` avertit avec `tools.exec.safe_bins_interpreter_unprofiled` lorsque les binaires interpréteur/runtime apparaissent dans `safeBins` sans profils explicites.
- `openclaw doctor --fix` peut échafauder les entrées `safeBinProfiles.<bin>` personnalisées manquantes comme `{}` (examinez et resserrez après). Les binaires interpréteur/runtime ne sont pas auto-échafaudés.

Exemple de profil personnalisé :

```json5
{
  tools: {
    exec: {
      safeBins: ["jq", "myfilter"],
      safeBinProfiles: {
        myfilter: {
          minPositional: 0,
          maxPositional: 0,
          allowedValueFlags: ["-n", "--limit"],
          deniedFlags: ["-f", "--file", "-c", "--command"],
        },
      },
    },
  },
}
```

## Édition de l'interface de contrôle

Utilisez la carte **Control UI → Nodes → Exec approvals** pour modifier les valeurs par défaut, les remplacements par agent et les listes d'autorisation. Sélectionnez une portée (Defaults ou un agent), ajustez la politique, ajoutez/supprimez des modèles de liste d'autorisation, puis cliquez sur **Save**. L'interface affiche les métadonnées **last used** par modèle pour que vous puissiez garder la liste organisée.

Le sélecteur de cible choisit **Gateway** (approbations locales) ou un **Node**. Les nœuds doivent annoncer `system.execApprovals.get/set` (application macOS ou hôte de nœud sans interface). Si un nœud n'annonce pas encore les approbations d'exécution, modifiez directement son fichier local `~/.openclaw/exec-approvals.json`.

CLI : `openclaw approvals` prend en charge l'édition de gateway ou de nœud (voir [Approvals CLI](/cli/approvals)).

## Flux d'approbation

Lorsqu'une invite est requise, la gateway diffuse `exec.approval.requested` aux clients opérateurs.
L'interface Control UI et l'application macOS la résolvent via `exec.approval.resolve`, puis la gateway transfère la demande approuvée à l'hôte du nœud.

Pour `host=node`, les demandes d'approbation incluent une charge utile `systemRunPlan` canonique. La gateway utilise ce plan comme commande faisant autorité/cwd/contexte de session lors du transfert des demandes `system.run` approuvées.

## Commandes d'interpréteur/runtime

Les exécutions d'interpréteur/runtime soutenues par approbation sont intentionnellement conservatrices :

- Le contexte exact argv/cwd/env est toujours lié.
- Les formes de script shell direct et de fichier runtime direct sont liées au mieux à un snapshot de fichier local concret.
- Les formes courantes de wrapper de gestionnaire de paquets qui se résolvent toujours en un fichier local direct (par exemple `pnpm exec`, `pnpm node`, `npm exec`, `npx`) sont dépliées avant la liaison.
- Si OpenClaw ne peut pas identifier exactement un fichier local concret pour une commande d'interpréteur/runtime (par exemple les scripts de paquets, les formes eval, les chaînes de chargeurs spécifiques au runtime ou les formes multi-fichiers ambiguës), l'exécution soutenue par approbation est refusée au lieu de prétendre à une couverture sémantique qu'elle n'a pas.
- Pour ces flux de travail, préférez le sandboxing, une limite d'hôte séparé ou une liste d'autorisation explicite de confiance/flux de travail complet où l'opérateur accepte la sémantique runtime plus large.

Lorsque les approbations sont requises, l'outil exec retourne immédiatement avec un identifiant d'approbation. Utilisez cet identifiant pour corréler les événements système ultérieurs (`Exec finished` / `Exec denied`). Si aucune décision n'arrive avant le délai d'expiration, la demande est traitée comme un délai d'approbation et présentée comme une raison de refus.

La boîte de dialogue de confirmation inclut :

- commande + arguments
- cwd
- identifiant d'agent
- chemin d'exécutable résolu
- métadonnées d'hôte + politique

Actions :

- **Allow once** → exécuter maintenant
- **Always allow** → ajouter à la liste d'autorisation + exécuter
- **Deny** → bloquer

## Transfert d'approbation vers les canaux de chat

Vous pouvez transférer les invites d'approbation d'exécution vers n'importe quel canal de chat (y compris les canaux de plugin) et les approuver avec `/approve`. Cela utilise le pipeline de livraison sortante normal.

Config :

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring or regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

Répondre dans le chat :

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

### Clients d'approbation de chat intégrés

Discord et Telegram peuvent également agir en tant que clients d'approbation d'exécution explicites avec une configuration spécifique au canal.

- Discord : `channels.discord.execApprovals.*`
- Telegram : `channels.telegram.execApprovals.*`

Ces clients sont optionnels. Si un canal n'a pas les approbations d'exécution activées, OpenClaw ne traite pas ce canal comme une surface d'approbation simplement parce que la conversation s'y est déroulée.

Comportement partagé :

- seuls les approbateurs configurés peuvent approuver ou refuser
- le demandeur n'a pas besoin d'être un approbateur
- lorsque la livraison de canal est activée, les invites d'approbation incluent le texte de la commande
- si aucune interface opérateur ou client d'approbation configuré ne peut accepter la demande, l'invite revient à `askFallback`

Telegram utilise par défaut les DM d'approbateur (`target: "dm"`). Vous pouvez basculer vers `channel` ou `both` lorsque vous souhaitez que les invites d'approbation apparaissent également dans le chat/sujet Telegram d'origine. Pour les sujets du forum Telegram, OpenClaw préserve le sujet pour l'invite d'approbation et le suivi post-approbation.

Voir :

- [Discord](/channels/discord#exec-approvals-in-discord)
- [Telegram](/channels/telegram#exec-approvals-in-telegram)

### Flux IPC macOS

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

Notes de sécurité :

- Mode de socket Unix `0600`, token stocké dans `exec-approvals.json`.
- Vérification de pair UID identique.
- Challenge/response (nonce + token HMAC + hash de demande) + TTL court.

## Événements système

Le cycle de vie Exec est présenté sous forme de messages système :

- `Exec running` (uniquement si la commande dépasse le seuil de notification d'exécution)
- `Exec finished`
- `Exec denied`

Ceux-ci sont publiés dans la session de l'agent après que le nœud signale l'événement.
Les approbations d'exécution gateway-host émettent les mêmes événements de cycle de vie lorsque la commande se termine (et éventuellement lorsqu'elle s'exécute plus longtemps que le seuil).
Les exécutions contrôlées par approbation réutilisent l'identifiant d'approbation comme `runId` dans ces messages pour une corrélation facile.

## Implications

- **full** est puissant ; préférez les listes d'autorisation si possible.
- **ask** vous tient informé tout en permettant des approbations rapides.
- Les listes d'autorisation par agent empêchent les approbations d'un agent de fuir vers d'autres.
- Les approbations ne s'appliquent qu'aux demandes d'exécution d'hôte des **expéditeurs autorisés**. Les expéditeurs non autorisés ne peuvent pas émettre `/exec`.
- `/exec security=full` est une commodité au niveau de la session pour les opérateurs autorisés et ignore intentionnellement les approbations.
  Pour bloquer complètement l'exécution d'hôte, définissez la sécurité des approbations sur `deny` ou refusez l'outil `exec` via la politique d'outil.

Connexes :

- [Exec tool](/tools/exec)
- [Elevated mode](/tools/elevated)
- [Skills](/tools/skills)
