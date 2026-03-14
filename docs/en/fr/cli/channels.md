# `openclaw channels`

Gérer les comptes de canaux de chat et leur statut d'exécution sur la passerelle.

Documentations connexes :

- Guides des canaux : [Channels](/channels/index)
- Configuration de la passerelle : [Configuration](/gateway/configuration)

## Commandes courantes

```bash
openclaw channels list
openclaw channels status
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels logs --channel all
```

## Ajouter / supprimer des comptes

```bash
openclaw channels add --channel telegram --token <bot-token>
openclaw channels remove --channel telegram --delete
```

Conseil : `openclaw channels add --help` affiche les drapeaux spécifiques à chaque canal (token, app token, chemins signal-cli, etc).

Lorsque vous exécutez `openclaw channels add` sans drapeaux, l'assistant interactif peut vous demander :

- les identifiants de compte par canal sélectionné
- les noms d'affichage optionnels pour ces comptes
- `Lier les comptes de canal configurés aux agents maintenant ?`

Si vous confirmez la liaison maintenant, l'assistant vous demande quel agent doit posséder chaque compte de canal configuré et écrit les liaisons de routage limitées au compte.

Vous pouvez également gérer les mêmes règles de routage ultérieurement avec `openclaw agents bindings`, `openclaw agents bind` et `openclaw agents unbind` (voir [agents](/cli/agents)).

Lorsque vous ajoutez un compte non-défaut à un canal qui utilise toujours des paramètres de niveau supérieur à compte unique (pas encore d'entrées `channels.<channel>.accounts`), OpenClaw déplace les valeurs de niveau supérieur à compte unique limitées au compte dans `channels.<channel>.accounts.default`, puis écrit le nouveau compte. Cela préserve le comportement du compte d'origine tout en passant à la forme multi-compte.

Le comportement de routage reste cohérent :

- Les liaisons existantes limitées au canal (pas de `accountId`) continuent à correspondre au compte par défaut.
- `channels add` ne crée pas automatiquement ou ne réécrit pas les liaisons en mode non-interactif.
- La configuration interactive peut éventuellement ajouter des liaisons limitées au compte.

Si votre configuration était déjà dans un état mixte (comptes nommés présents, `default` manquant, et valeurs de niveau supérieur à compte unique toujours définies), exécutez `openclaw doctor --fix` pour déplacer les valeurs limitées au compte dans `accounts.default`.

## Connexion / déconnexion (interactif)

```bash
openclaw channels login --channel whatsapp
openclaw channels logout --channel whatsapp
```

## Dépannage

- Exécutez `openclaw status --deep` pour une sonde large.
- Utilisez `openclaw doctor` pour des corrections guidées.
- `openclaw channels list` affiche `Claude: HTTP 403 ... user:profile` → l'instantané d'utilisation a besoin de la portée `user:profile`. Utilisez `--no-usage`, ou fournissez une clé de session claude.ai (`CLAUDE_WEB_SESSION_KEY` / `CLAUDE_WEB_COOKIE`), ou réauthentifiez-vous via Claude Code CLI.
- `openclaw channels status` revient à des résumés limités à la configuration lorsque la passerelle est inaccessible. Si une credential de canal supportée est configurée via SecretRef mais indisponible dans le chemin de commande actuel, elle signale ce compte comme configuré avec des notes dégradées au lieu de l'afficher comme non configuré.

## Sonde de capacités

Récupérez les indices de capacité du fournisseur (intentions/portées le cas échéant) plus le support des fonctionnalités statiques :

```bash
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
```

Remarques :

- `--channel` est optionnel ; omettez-le pour lister chaque canal (y compris les extensions).
- `--target` accepte `channel:<id>` ou un identifiant de canal numérique brut et s'applique uniquement à Discord.
- Les sondes sont spécifiques au fournisseur : intentions Discord + permissions de canal optionnelles ; portées bot + utilisateur Slack ; drapeaux bot Telegram + webhook ; version du démon Signal ; token d'application MS Teams + rôles/portées Graph (annotés le cas échéant). Les canaux sans sondes signalent `Probe: unavailable`.

## Résoudre les noms en identifiants

Résolvez les noms de canal/utilisateur en identifiants à l'aide du répertoire du fournisseur :

```bash
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels resolve --channel discord "My Server/#support" "@someone"
openclaw channels resolve --channel matrix "Project Room"
```

Remarques :

- Utilisez `--kind user|group|auto` pour forcer le type de cible.
- La résolution préfère les correspondances actives lorsque plusieurs entrées partagent le même nom.
- `channels resolve` est en lecture seule. Si un compte sélectionné est configuré via SecretRef mais que cette credential est indisponible dans le chemin de commande actuel, la commande retourne des résultats non résolus dégradés avec des notes au lieu d'abandonner l'exécution entière.
