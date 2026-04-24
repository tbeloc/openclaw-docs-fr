---
summary: "Approbations exec avancées : safe bins, liaison d'interpréteur, transfert d'approbation, livraison native"
read_when:
  - Configuring safe bins or custom safe-bin profiles
  - Forwarding approvals to Slack/Discord/Telegram or other chat channels
  - Implementing a native approval client for a channel
title: "Approbations exec — avancé"
---

Sujets avancés d'approbation exec : le fast-path `safeBins`, la liaison d'interpréteur/runtime et le transfert d'approbation vers les canaux de chat (y compris la livraison native). Pour la politique de base et le flux d'approbation, voir [Approbations exec](/fr/tools/exec-approvals).

## Safe bins (stdin uniquement)

`tools.exec.safeBins` définit une petite liste de binaires **stdin uniquement** (par exemple `cut`) qui peuvent s'exécuter en mode liste blanche **sans** entrées de liste blanche explicites. Les safe bins rejettent les arguments de fichier positionnels et les tokens de type chemin, ils ne peuvent donc opérer que sur le flux entrant. Considérez ceci comme un fast-path étroit pour les filtres de flux, pas une liste de confiance générale.

<Warning>
Ne **pas** ajouter de binaires interpréteur ou runtime (par exemple `python3`, `node`, `ruby`, `bash`, `sh`, `zsh`) à `safeBins`. Si une commande peut évaluer du code, exécuter des sous-commandes ou lire des fichiers par conception, préférez les entrées de liste blanche explicites et gardez les invites d'approbation activées. Les safe bins personnalisés doivent définir un profil explicite dans `tools.exec.safeBinProfiles.<bin>`.
</Warning>

Safe bins par défaut :

[//]: # "SAFE_BIN_DEFAULTS:START"

`cut`, `uniq`, `head`, `tail`, `tr`, `wc`

[//]: # "SAFE_BIN_DEFAULTS:END"

`grep` et `sort` ne figurent pas dans la liste par défaut. Si vous optez pour cela, conservez des entrées de liste blanche explicites pour leurs flux non-stdin. Pour `grep` en mode safe-bin, fournissez le motif avec `-e`/`--regexp` ; la forme de motif positionnel est rejetée pour que les opérandes de fichier ne puissent pas être contrebandés comme des positionnels ambigus.

### Validation argv et drapeaux refusés

La validation est déterministe à partir de la forme argv uniquement (pas de vérifications d'existence du système de fichiers hôte), ce qui empêche le comportement d'oracle d'existence de fichier à partir des différences allow/deny. Les options orientées fichier sont refusées pour les safe bins par défaut ; les options longues sont validées fail-closed (les drapeaux inconnus et les abréviations ambigües sont rejetés).

Drapeaux refusés par profil safe-bin :

[//]: # "SAFE_BIN_DENIED_FLAGS:START"

- `grep`: `--dereference-recursive`, `--directories`, `--exclude-from`, `--file`, `--recursive`, `-R`, `-d`, `-f`, `-r`
- `jq`: `--argfile`, `--from-file`, `--library-path`, `--rawfile`, `--slurpfile`, `-L`, `-f`
- `sort`: `--compress-program`, `--files0-from`, `--output`, `--random-source`, `--temporary-directory`, `-T`, `-o`
- `wc`: `--files0-from`

[//]: # "SAFE_BIN_DENIED_FLAGS:END"

Les safe bins forcent également les tokens argv à être traités comme du **texte littéral** au moment de l'exécution (pas de globbing et pas d'expansion `$VARS`) pour les segments stdin uniquement, donc des motifs comme `*` ou `$HOME/...` ne peuvent pas être utilisés pour contrebander des lectures de fichier.

### Répertoires binaires de confiance

Les safe bins doivent se résoudre à partir de répertoires binaires de confiance (valeurs par défaut du système plus `tools.exec.safeBinTrustedDirs` optionnel). Les entrées `PATH` ne sont jamais auto-approuvées. Les répertoires de confiance par défaut sont intentionnellement minimaux : `/bin`, `/usr/bin`. Si votre exécutable safe-bin se trouve dans des chemins de gestionnaire de paquets/utilisateur (par exemple `/opt/homebrew/bin`, `/usr/local/bin`, `/opt/local/bin`, `/snap/bin`), ajoutez-les explicitement à `tools.exec.safeBinTrustedDirs`.

### Chaînage shell, wrappers et multiplexeurs

Le chaînage shell (`&&`, `||`, `;`) est autorisé lorsque chaque segment de niveau supérieur satisfait la liste blanche (y compris les safe bins ou l'auto-allow de compétence). Les redirections restent non supportées en mode liste blanche. La substitution de commande (`$()` / backticks) est rejetée lors de l'analyse de la liste blanche, y compris à l'intérieur des guillemets doubles ; utilisez des guillemets simples si vous avez besoin de texte littéral `$()`.

Sur les approbations d'application compagnon macOS, le texte shell brut contenant une syntaxe de contrôle ou d'expansion shell (`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) est traité comme un manque de liste blanche à moins que le binaire shell lui-même ne soit listé en blanc.

Pour les wrappers shell (`bash|sh|zsh ... -c/-lc`), les remplacements d'env limités à la requête sont réduits à une petite liste explicite (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`).

Pour les décisions `allow-always` en mode liste blanche, les wrappers de dispatch connus (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persistent le chemin exécutable interne au lieu du chemin wrapper. Les multiplexeurs shell (`busybox`, `toybox`) sont dépliés pour les applets shell (`sh`, `ash`, etc.) de la même manière. Si un wrapper ou multiplexeur ne peut pas être déplie en toute sécurité, aucune entrée de liste blanche n'est persistée automatiquement.

Si vous listez en blanc des interpréteurs comme `python3` ou `node`, préférez `tools.exec.strictInlineEval=true` pour que l'évaluation inline nécessite toujours une approbation explicite. En mode strict, `allow-always` peut toujours persister les invocations d'interpréteur/script bénignes, mais les transporteurs d'évaluation inline ne sont pas persistés automatiquement.

### Safe bins versus liste blanche

| Sujet            | `tools.exec.safeBins`                                  | Liste blanche (`exec-approvals.json`)                            |
| ---------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Objectif         | Auto-allow des filtres stdin étroits                   | Faire confiance explicitement à des exécutables spécifiques                        |
| Type de correspondance       | Nom exécutable + politique argv safe-bin                 | Motif glob de chemin exécutable résolu                        |
| Portée d'argument   | Restreint par profil safe-bin et règles de token littéral | Correspondance de chemin uniquement ; les arguments sont sinon votre responsabilité |
| Exemples typiques | `head`, `tail`, `tr`, `wc`                             | `jq`, `python3`, `node`, `ffmpeg`, CLIs personnalisés               |
| Meilleure utilisation         | Transformations de texte à faible risque dans les pipelines                  | Tout outil avec un comportement plus large ou des effets secondaires               |

Emplacement de configuration :

- `safeBins` provient de la config (`tools.exec.safeBins` ou par-agent `agents.list[].tools.exec.safeBins`).
- `safeBinTrustedDirs` provient de la config (`tools.exec.safeBinTrustedDirs` ou par-agent `agents.list[].tools.exec.safeBinTrustedDirs`).
- `safeBinProfiles` provient de la config (`tools.exec.safeBinProfiles` ou par-agent `agents.list[].tools.exec.safeBinProfiles`). Les clés de profil par-agent remplacent les clés globales.
- Les entrées de liste blanche se trouvent dans `~/.openclaw/exec-approvals.json` local à l'hôte sous `agents.<id>.allowlist` (ou via Control UI / `openclaw approvals allowlist ...`).
- `openclaw security audit` avertit avec `tools.exec.safe_bins_interpreter_unprofiled` lorsque des binaires interpréteur/runtime apparaissent dans `safeBins` sans profils explicites.
- `openclaw doctor --fix` peut générer des entrées `safeBinProfiles.<bin>` personnalisées manquantes comme `{}` (examinez et resserrez après). Les binaires interpréteur/runtime ne sont pas auto-générés.

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

Si vous optez explicitement pour `jq` dans `safeBins`, OpenClaw rejette toujours le builtin `env` en mode safe-bin pour que `jq -n env` ne puisse pas vider l'environnement du processus hôte sans un chemin de liste blanche explicite ou une invite d'approbation.

## Commandes interpréteur/runtime

Les exécutions interpréteur/runtime soutenues par approbation sont intentionnellement conservatrices :

- Le contexte exact argv/cwd/env est toujours lié.
- Les formes de script shell direct et de fichier runtime direct sont liées au mieux à un snapshot de fichier local concret.
- Les formes de wrapper de gestionnaire de paquets courant qui se résolvent toujours à un fichier local direct (par exemple `pnpm exec`, `pnpm node`, `npm exec`, `npx`) sont dépliées avant la liaison.
- Si OpenClaw ne peut pas identifier exactement un fichier local concret pour une commande interpréteur/runtime (par exemple les scripts de paquets, les formes eval, les chaînes de chargeur spécifiques au runtime ou les formes multi-fichiers ambigües), l'exécution soutenue par approbation est refusée au lieu de prétendre à une couverture sémantique qu'elle n'a pas.
- Pour ces flux de travail, préférez le sandboxing, une limite d'hôte séparée ou une liste blanche de confiance explicite/flux de travail complet où l'opérateur accepte la sémantique runtime plus large.

Lorsque les approbations sont requises, l'outil exec retourne immédiatement avec un id d'approbation. Utilisez cet id pour corréler les événements système ultérieurs (`Exec finished` / `Exec denied`). Si aucune décision n'arrive avant le délai d'expiration, la demande est traitée comme un délai d'expiration d'approbation et surfacée comme une raison de refus.

### Comportement de livraison de suivi

Après la fin d'une exec async approuvée, OpenClaw envoie un tour `agent` de suivi à la même session.

- Si une cible de livraison externe valide existe (canal livrable plus `to` cible), la livraison de suivi utilise ce canal.
- Dans les flux webchat uniquement ou session interne sans cible externe, la livraison de suivi reste session uniquement (`deliver: false`).
- Si un appelant demande explicitement une livraison externe stricte sans canal externe résolvable, la demande échoue avec `INVALID_REQUEST`.
- Si `bestEffortDeliver` est activé et qu'aucun canal externe ne peut être résolu, la livraison est rétrogradée à session uniquement au lieu d'échouer.

## Transfert des approbations vers les canaux de chat

Vous pouvez transférer les invites d'approbation exec vers n'importe quel canal de chat (y compris les canaux de plugins) et les approuver avec `/approve`. Cela utilise le pipeline de livraison sortante normal.

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

La commande `/approve` gère à la fois les approbations exec et les approbations de plugins. Si l'ID ne correspond pas à une approbation exec en attente, il vérifie automatiquement les approbations de plugins à la place.

### Transfert des approbations de plugins

Le transfert des approbations de plugins utilise le même pipeline de livraison que les approbations exec mais dispose de sa propre configuration indépendante sous `approvals.plugin`. L'activation ou la désactivation de l'une n'affecte pas l'autre.

```json5
{
  approvals: {
    plugin: {
      enabled: true,
      mode: "targets",
      agentFilter: ["main"],
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

La forme de la config est identique à `approvals.exec` : `enabled`, `mode`, `agentFilter`, `sessionFilter` et `targets` fonctionnent de la même manière.

Les canaux qui supportent les réponses interactives partagées affichent les mêmes boutons d'approbation pour les approbations exec et de plugins. Les canaux sans interface utilisateur interactive partagée reviennent à du texte brut avec les instructions `/approve`.

### Approbations dans le même chat sur n'importe quel canal

Lorsqu'une demande d'approbation exec ou de plugin provient d'une surface de chat livrable, le même chat peut maintenant l'approuver avec `/approve` par défaut. Cela s'applique aux canaux tels que Slack, Matrix et Microsoft Teams en plus des flux d'interface utilisateur Web et terminal existants.

Ce chemin de commande texte partagé utilise le modèle d'authentification normal du canal pour cette conversation. Si le chat d'origine peut déjà envoyer des commandes et recevoir des réponses, les demandes d'approbation n'ont plus besoin d'un adaptateur de livraison natif séparé pour rester en attente.

Discord et Telegram supportent également le `/approve` dans le même chat, mais ces canaux utilisent toujours leur liste d'approbateurs résolue pour l'autorisation même lorsque la livraison d'approbation native est désactivée.

Pour Telegram et les autres clients d'approbation natifs qui appellent la Gateway directement, ce fallback est intentionnellement limité aux défaillances « approbation non trouvée ». Un vrai refus ou une erreur d'approbation exec ne réessaie pas silencieusement en tant qu'approbation de plugin.

### Livraison d'approbation native

Certains canaux peuvent également agir en tant que clients d'approbation natifs. Les clients natifs ajoutent des DM d'approbateurs, un fanout de chat d'origine et une interface utilisateur d'approbation spécifique au canal en plus du flux `/approve` partagé dans le même chat.

Lorsque des cartes/boutons d'approbation natifs sont disponibles, cette interface utilisateur native est le chemin principal face à l'agent. L'agent ne doit pas non plus répéter une commande de chat `/approve` en texte brut en double à moins que le résultat de l'outil indique que les approbations de chat ne sont pas disponibles ou que l'approbation manuelle est le seul chemin restant.

Modèle générique :

- la politique exec de l'hôte décide toujours si l'approbation exec est requise
- `approvals.exec` contrôle le transfert des invites d'approbation vers d'autres destinations de chat
- `channels.<channel>.execApprovals` contrôle si ce canal agit en tant que client d'approbation natif

Les clients d'approbation natifs activent automatiquement la livraison prioritaire aux DM lorsque tous ces éléments sont vrais :

- le canal supporte la livraison d'approbation native
- les approbateurs peuvent être résolus à partir de `execApprovals.approvers` explicites ou des sources de fallback documentées de ce canal
- `channels.<channel>.execApprovals.enabled` n'est pas défini ou est `"auto"`

Définissez `enabled: false` pour désactiver explicitement un client d'approbation natif. Définissez `enabled: true` pour le forcer lorsque les approbateurs se résolvent. La livraison de chat d'origine publique reste explicite via `channels.<channel>.execApprovals.target`.

FAQ : [Pourquoi y a-t-il deux configs d'approbation exec pour les approbations de chat ?](/fr/help/faq#why-are-there-two-exec-approval-configs-for-chat-approvals)

- Discord : `channels.discord.execApprovals.*`
- Slack : `channels.slack.execApprovals.*`
- Telegram : `channels.telegram.execApprovals.*`

Ces clients d'approbation natifs ajoutent le routage des DM et le fanout de canal optionnel en plus du flux `/approve` partagé dans le même chat et des boutons d'approbation partagés.

Comportement partagé :

- Slack, Matrix, Microsoft Teams et les chats livrables similaires utilisent le modèle d'authentification normal du canal pour le `/approve` dans le même chat
- lorsqu'un client d'approbation natif s'active automatiquement, la cible de livraison native par défaut est les DM des approbateurs
- pour Discord et Telegram, seuls les approbateurs résolus peuvent approuver ou refuser
- les approbateurs Discord peuvent être explicites (`execApprovals.approvers`) ou déduits de `commands.ownerAllowFrom`
- les approbateurs Telegram peuvent être explicites (`execApprovals.approvers`) ou déduits de la config de propriétaire existante (`allowFrom`, plus `defaultTo` de message direct où supporté)
- les approbateurs Slack peuvent être explicites (`execApprovals.approvers`) ou déduits de `commands.ownerAllowFrom`
- les boutons natifs Slack préservent le type d'ID d'approbation, donc les IDs `plugin:` peuvent résoudre les approbations de plugins sans une deuxième couche de fallback locale à Slack
- le routage natif DM/canal Matrix et les raccourcis de réaction gèrent à la fois les approbations exec et de plugins ; l'autorisation de plugin provient toujours de `channels.matrix.dm.allowFrom`
- le demandeur n'a pas besoin d'être un approbateur
- le chat d'origine peut approuver directement avec `/approve` lorsque ce chat supporte déjà les commandes et les réponses
- les boutons d'approbation natifs Discord routent par type d'ID d'approbation : les IDs `plugin:` vont directement aux approbations de plugins, tout le reste va aux approbations exec
- les boutons d'approbation natifs Telegram suivent le même fallback exec-to-plugin limité que `/approve`
- lorsque la `target` native active la livraison de chat d'origine, les invites d'approbation incluent le texte de la commande
- les approbations exec en attente expirent après 30 minutes par défaut
- si aucune interface utilisateur d'opérateur ou client d'approbation configuré ne peut accepter la demande, l'invite revient à `askFallback`

Telegram utilise par défaut les DM des approbateurs (`target: "dm"`). Vous pouvez basculer vers `channel` ou `both` lorsque vous souhaitez que les invites d'approbation apparaissent également dans le chat/sujet Telegram d'origine. Pour les sujets de forum Telegram, OpenClaw préserve le sujet pour l'invite d'approbation et le suivi post-approbation.

Voir :

- [Discord](/fr/channels/discord)
- [Telegram](/fr/channels/telegram)

### Flux IPC macOS

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

Notes de sécurité :

- Mode de socket Unix `0600`, token stocké dans `exec-approvals.json`.
- Vérification de pair même UID.
- Challenge/response (nonce + token HMAC + hash de demande) + TTL court.

## Connexes

- [Approbations exec](/fr/tools/exec-approvals) — politique principale et flux d'approbation
- [Outil exec](/fr/tools/exec)
- [Mode élevé](/fr/tools/elevated)
- [Skills](/fr/tools/skills) — comportement d'auto-autorisation soutenu par les skills
