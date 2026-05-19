---
summary: "Mantis est le système de vérification visuelle de bout en bout pour reproduire les bugs OpenClaw sur les transports en direct, capturer les preuves avant et après, et joindre les artefacts aux PR."
title: "Mantis"
read_when:
  - Building or running live visual QA for OpenClaw bugs
  - Adding before and after verification for a pull request
  - Adding Discord, Slack, WhatsApp, or other live transport scenarios
  - Debugging QA runs that need screenshots, browser automation, or VNC access
---

Mantis est le système de vérification de bout en bout d'OpenClaw pour les bugs qui nécessitent un vrai runtime, un vrai transport, et une preuve visible. Il exécute un scénario par rapport à une référence connue comme défectueuse, capture des preuves, exécute le même scénario par rapport à une référence candidate, et publie la comparaison en tant qu'artefacts qu'un responsable peut inspecter à partir d'une PR ou d'une commande locale.

Mantis commence avec Discord car Discord nous offre une première voie de grande valeur : authentification bot réelle, vrais canaux de guilde, réactions, threads, commandes natives, et une interface de navigateur où les humains peuvent visuellement confirmer ce que le transport a montré.

## Objectifs

- Reproduire un bug à partir d'un problème ou d'une PR GitHub avec la même forme de transport que les utilisateurs voient.
- Capturer un artefact **avant** sur la référence de base avant d'appliquer le correctif.
- Capturer un artefact **après** sur la référence candidate après l'application du correctif.
- Utiliser un oracle déterministe chaque fois que possible, comme une lecture de réaction Discord REST ou une vérification de transcription de canal.
- Capturer des captures d'écran quand le bug a une surface d'interface utilisateur visible.
- Exécuter localement à partir d'une CLI contrôlée par un agent et à distance à partir de GitHub.
- Préserver suffisamment d'état machine pour un sauvetage VNC quand la connexion, l'automatisation du navigateur, ou l'authentification du fournisseur se bloque.
- Publier un statut concis sur un canal Discord d'opérateur quand l'exécution est bloquée, a besoin d'aide VNC manuelle, ou se termine.

## Non-objectifs

- Mantis n'est pas un remplacement pour les tests unitaires. Une exécution Mantis devrait généralement devenir un test de régression plus petit après que le correctif soit compris.
- Mantis n'est pas la porte CI rapide normale. Il est plus lent, utilise des identifiants en direct, et est réservé aux bugs où l'environnement en direct est important.
- Mantis ne devrait pas nécessiter un humain pour un fonctionnement normal. VNC manuel est un chemin de sauvetage, pas le chemin heureux.
- Mantis ne stocke pas les secrets bruts dans les artefacts, les journaux, les captures d'écran, les rapports Markdown, ou les commentaires PR.

## Propriété

Mantis vit dans la pile QA d'OpenClaw.

- OpenClaw possède le runtime du scénario, les adaptateurs de transport, le schéma de preuves, et la CLI locale sous `pnpm openclaw qa mantis`.
- QA Lab possède les pièces du harnais de transport en direct, les aides de capture de navigateur, et les rédacteurs d'artefacts.
- Crabbox possède les machines Linux préchauffées quand une VM distante est nécessaire.
- GitHub Actions possède le point d'entrée du workflow distant et la rétention des artefacts.
- ClawSweeper possède le routage des commentaires GitHub : analyse des commandes du responsable, dispatch du workflow, et publication du commentaire PR final.
- Les agents OpenClaw pilotent Mantis via Codex quand un scénario a besoin de configuration agentique, de débogage, ou de rapports d'état bloqué.

Cette limite garde la connaissance du transport dans OpenClaw, la planification des machines dans Crabbox, et la colle du workflow du responsable dans ClawSweeper.

## Forme de la commande

La première commande locale vérifie le bot Discord, la guilde, le canal, l'envoi de message,
l'envoi de réaction et le chemin d'artefact :

```bash
pnpm openclaw qa mantis discord-smoke \
  --output-dir .artifacts/qa-e2e/mantis/discord-smoke
```

Le runner local avant et après accepte cette forme :

```bash
pnpm openclaw qa mantis run \
  --transport discord \
  --scenario discord-status-reactions-tool-only \
  --baseline origin/main \
  --candidate HEAD \
  --output-dir .artifacts/qa-e2e/mantis/local-discord-status-reactions
```

Le runner crée des worktrees détachés de base de référence et de candidat sous le répertoire de sortie,
installe les dépendances, construit chaque ref, exécute le scénario avec
`--allow-failures`, puis écrit `baseline/`, `candidate/`, `comparison.json`,
et `mantis-report.md`. Pour le premier scénario Discord, une vérification réussie
signifie que le statut de base de référence est `fail` et le statut du candidat est `pass`.

La deuxième sonde Discord avant/après cible les pièces jointes de fil :

```bash
pnpm openclaw qa mantis run \
  --transport discord \
  --scenario discord-thread-reply-filepath-attachment \
  --baseline <bug-ref> \
  --candidate <fix-ref> \
  --output-dir .artifacts/qa-e2e/mantis/local-discord-thread-attachment
```

Ce scénario publie un message parent avec le bot pilote, crée un vrai fil Discord,
appelle l'action `message.thread-reply` d'OpenClaw avec un
`filePath` local au dépôt, puis interroge le fil pour la réponse SUT et le nom de fichier de la pièce jointe. La capture d'écran de base de référence montre la réponse sans pièce jointe ; la capture d'écran du candidat
montre la pièce jointe `mantis-thread-report.md` attendue.

La première primitive VM/navigateur est le smoke desktop :

```bash
pnpm openclaw qa mantis desktop-browser-smoke \
  --output-dir .artifacts/qa-e2e/mantis/desktop-browser
```

Il loue ou réutilise une machine de bureau Crabbox, démarre un navigateur visible dans la
session VNC, capture le bureau, récupère les artefacts vers le
répertoire de sortie local, et écrit la commande de reconnexion dans le rapport. La commande utilise par défaut le fournisseur Hetzner car c'est le premier fournisseur avec une couverture desktop/VNC fonctionnelle dans la voie Mantis. Remplacez-le avec `--provider`, `--crabbox-bin`, ou
`OPENCLAW_MANTIS_CRABBOX_PROVIDER` lors de l'exécution contre une autre flotte Crabbox.

Drapeaux de smoke desktop utiles :

- `--lease-id <cbx_...>` ou `OPENCLAW_MANTIS_CRABBOX_LEASE_ID` réutilise un bureau préchauffé.
- `--browser-url <url>` change la page ouverte dans le navigateur visible.
- `--html-file <path>` rend un artefact HTML local au dépôt dans le navigateur visible. Mantis l'utilise pour capturer la chronologie de réaction de statut Discord générée via un vrai bureau Crabbox.
- `--browser-profile-dir <remote-path>` réutilise un répertoire user-data-dir Chrome distant pour qu'un bureau Mantis persistant puisse rester connecté entre les exécutions. Utilisez ceci pour le profil de visualiseur Discord Web de longue durée.
- `--browser-profile-archive-env <name>` restaure une archive `.tgz` user-data-dir Chrome en base64 à partir de la variable d'environnement nommée avant de lancer le navigateur. Utilisez ceci pour les témoins connectés comme Discord Web. La variable d'environnement par défaut est `OPENCLAW_MANTIS_BROWSER_PROFILE_TGZ_B64`.
- `--video-duration <seconds>` contrôle la durée de capture MP4. Utilisez une durée plus longue pour les applications web connectées lentes qui ont besoin de temps pour se stabiliser.
- `--keep-lease` ou `OPENCLAW_MANTIS_KEEP_VM=1` garde un bail nouvellement créé et réussi ouvert pour l'inspection VNC. Les exécutions échouées gardent le bail par défaut quand un a été créé pour qu'un opérateur puisse se reconnecter.
- `--class`, `--idle-timeout`, et `--ttl` ajustent la taille de la machine et la durée de vie du bail.

Pour les preuves Discord Web, Mantis utilise un compte de visualiseur dédié au lieu d'un
jeton de bot. Le scénario API Discord en direct reste l'oracle : il crée le vrai
fil, envoie le `thread-reply` SUT, et vérifie la pièce jointe via Discord
REST. Quand `OPENCLAW_QA_DISCORD_CAPTURE_UI_METADATA=1` est défini, le scénario écrit aussi
un artefact URL Discord Web. Quand `OPENCLAW_QA_DISCORD_KEEP_THREADS=1` est
défini, il laisse ce fil disponible assez longtemps pour qu'un navigateur connecté l'ouvre
et l'enregistre.

Le workflow GitHub ouvre l'URL du fil candidat dans Discord Web, capture une
capture d'écran, enregistre un MP4, et génère un aperçu GIF réduit quand les outils
médias Crabbox sont disponibles. Préférez un chemin de profil de visualiseur persistant configuré
via `MANTIS_DISCORD_VIEWER_CHROME_PROFILE_DIR`, car les archives de profil Chrome complètes
peuvent dépasser la limite de taille des secrets GitHub. Pour les petits/profils bootstrap,
le workflow peut aussi restaurer une archive `.tgz` en base64 à partir de
`MANTIS_DISCORD_VIEWER_CHROME_PROFILE_TGZ_B64`. Si aucune source de profil n'est
configurée, le workflow publie toujours les captures d'écran de pièce jointe déterministes baseline/candidate
et enregistre un avis que le témoin Discord Web connecté a été ignoré.

La première primitive de transport desktop complète est le smoke desktop Slack :

```bash
pnpm openclaw qa mantis slack-desktop-smoke \
  --output-dir .artifacts/qa-e2e/mantis/slack-desktop \
  --gateway-setup \
  --scenario slack-canary \
  --keep-lease
```

Il loue ou réutilise une machine de bureau Crabbox, synchronise le checkout actuel dans
la VM, exécute `pnpm openclaw qa slack` à l'intérieur de cette VM, ouvre Slack Web dans le navigateur VNC,
capture le bureau visible, et copie à la fois les artefacts QA Slack et
la capture d'écran VNC vers le répertoire de sortie local. C'est la première
forme Mantis où la passerelle OpenClaw SUT et le navigateur vivent tous les deux à l'intérieur de la
même VM desktop Linux.

Avec `--gateway-setup`, la commande prépare un accueil OpenClaw jetable persistant à
`$HOME/.openclaw-mantis/slack-openclaw`, corrige la configuration Slack Socket Mode
pour le canal sélectionné, démarre `openclaw gateway run` sur le port
`38973`, et garde Chrome en cours d'exécution dans la session VNC. C'est le mode
"laisse-moi un bureau Linux avec Slack et une griffe en cours d'exécution" ; la voie QA Slack bot-to-bot
reste la valeur par défaut quand `--gateway-setup` est omis.

Entrées requises pour `--credential-source env` :

- `OPENCLAW_QA_SLACK_CHANNEL_ID`
- `OPENCLAW_QA_SLACK_DRIVER_BOT_TOKEN`
- `OPENCLAW_QA_SLACK_SUT_BOT_TOKEN`
- `OPENCLAW_QA_SLACK_SUT_APP_TOKEN`
- `OPENCLAW_LIVE_OPENAI_KEY` pour la voie du modèle distant. Si seulement
  `OPENAI_API_KEY` est défini localement, Mantis le mappe à `OPENCLAW_LIVE_OPENAI_KEY`
  avant d'invoquer Crabbox pour que le transfert d'env `OPENCLAW_*` de Crabbox puisse le
  porter dans la VM.

Avec `--gateway-setup --credential-source convex`, Mantis loue les identifiants SUT Slack
du pool partagé avant de créer la VM et transfère l'id de canal loué, le jeton d'application Socket Mode,
et le jeton de bot comme l'env d'exécution `OPENCLAW_MANTIS_SLACK_*` à l'intérieur du bureau. Cela garde
les workflows GitHub minces : ils n'ont besoin que du secret du courtier Convex, pas des jetons de bot ou d'application Slack bruts.

Drapeaux Slack desktop utiles :

- `--lease-id <cbx_...>` réexécute contre une machine où un opérateur s'est déjà connecté à Slack Web via VNC.
- `--gateway-setup` démarre une passerelle Slack OpenClaw persistante dans la VM au lieu de seulement exécuter la voie QA bot-to-bot.
- `--keep-lease` garde la VM de passerelle ouverte pour l'inspection VNC après le succès ; `--no-keep-lease` l'arrête après la collecte des artefacts.
- `--slack-url <url>` ouvre une URL Slack Web spécifique. Sans cela, Mantis dérive `https://app.slack.com/client/<team>/<channel>` à partir de Slack `auth.test` quand le jeton de bot SUT est disponible.
- `--slack-channel-id <id>` contrôle la liste d'autorisation de canal Slack utilisée par la configuration de passerelle.
- `OPENCLAW_MANTIS_SLACK_BROWSER_PROFILE_DIR` contrôle le profil Chrome persistant à l'intérieur de la VM. La valeur par défaut est `$HOME/.config/openclaw-mantis/slack-chrome-profile`, donc une connexion Slack Web manuelle survit aux réexécutions sur le même bail.
- `--credential-source convex --credential-role ci` utilise le pool d'identifiants partagé au lieu des jetons d'env Slack directs.
- `--provider-mode`, `--model`, `--alt-model`, et `--fast` passent à la voie Slack en direct.

Le workflow smoke GitHub est `Mantis Discord Smoke`. Le workflow GitHub avant et après
pour le premier vrai scénario est `Mantis Discord Status Reactions`. Il
accepte :

- `baseline_ref` : la ref attendue pour reproduire le comportement queued-only.
- `candidate_ref` : la ref attendue pour montrer `queued -> thinking -> done`.

Il vérifie la ref du harnais de workflow, construit des worktrees baseline et candidate séparés,
exécute `discord-status-reactions-tool-only` contre chaque worktree, et
télécharge `baseline/`, `candidate/`, `comparison.json`, et `mantis-report.md` comme
artefacts Actions. Il rend aussi la chronologie HTML de chaque voie dans un navigateur de bureau Crabbox
et publie ces captures d'écran VNC à côté des PNG de chronologie déterministes dans le commentaire PR. Le même commentaire PR intègre des aperçus GIF légers réduits en mouvement générés par `crabbox media preview`, des liens vers les clips MP4 réduits en mouvement correspondants, et garde les fichiers MP4 de bureau complets pour l'inspection approfondie. Les captures d'écran restent en ligne pour un examen rapide. Le workflow construit la CLI Crabbox à partir de
`openclaw/crabbox` main pour pouvoir utiliser les drapeaux de bail desktop/navigateur actuels
avant la prochaine version binaire Crabbox.

`Mantis Scenario` est le point d'entrée manuel générique. Il prend un `scenario_id`,
`candidate_ref`, `baseline_ref` optionnel, et `pr_number` optionnel, puis
distribue le workflow détenu par le scénario. Le wrapper est intentionnellement mince :
les workflows de scénario possèdent toujours leur configuration de transport, identifiants, classe VM,
oracle attendu, et manifeste d'artefact.

`Mantis Slack Desktop Smoke` est le premier workflow VM Slack. Il vérifie la
ref candidate de confiance dans un worktree séparé, loue un bureau Linux Crabbox,
exécute `pnpm openclaw qa mantis slack-desktop-smoke --gateway-setup` contre ce
candidat, ouvre Slack Web dans le navigateur VNC, enregistre le bureau, génère un
aperçu réduit en mouvement avec `crabbox media preview`, télécharge le répertoire d'artefact complet, et
publie optionnellement le commentaire de preuve en ligne sur la PR cible.
Il utilise par défaut AWS pour le bail du bureau et expose une entrée de fournisseur manuel pour que
les opérateurs puissent basculer vers Hetzner quand la capacité AWS est lente ou indisponible. Utilisez
cette voie quand vous voulez "un bureau Linux avec Slack et une griffe en cours d'exécution" au lieu de
seulement une transcription Slack bot-to-bot.

`Mantis Telegram Live` enveloppe la voie QA Telegram en direct existante dans le même
pipeline de preuve PR. Il vérifie la ref candidate de confiance dans un worktree séparé,
exécute `pnpm openclaw qa telegram --credential-source convex
--credential-role ci`, écrit un manifeste `mantis-evidence.json` à partir du
résumé QA Telegram et de l'artefact de message observé, rend la chronologie HTML rédactée via un navigateur de bureau Crabbox,
génère un GIF réduit en mouvement avec `crabbox media preview`, et publie le commentaire de preuve PR en ligne quand un
numéro PR est disponible. Cette voie est plutôt transcription-visuelle que preuve Telegram Web connectée :
l'API Bot Telegram donne une preuve de message en direct stable, mais l'état de connexion Telegram Web n'est pas
requis pour l'automatisation Mantis normale.

`Mantis Telegram Desktop Proof` est le wrapper natif Telegram Desktop avant/après agentique.
Un mainteneur peut le déclencher à partir d'un commentaire PR avec
`@openclaw-mantis telegram desktop proof`, à partir de l'interface utilisateur Actions avec des instructions en texte libre, ou via le distributeur générique `Mantis Scenario`. Le workflow
remet la PR, la ref baseline, la ref candidate, et les instructions du mainteneur à Codex.
L'agent lit la PR, décide quel comportement visible Telegram prouve le
changement, exécute la voie de preuve Telegram Desktop Crabbox utilisateur réel pour baseline et
candidat, itère jusqu'à ce que les GIF natifs soient utiles, écrit des artefacts `motionPreview` appairés
dans `mantis-evidence.json`, télécharge le bundle, et
publie un tableau de preuve PR à 2 colonnes quand un numéro PR est disponible.

Pour la configuration Telegram desktop avec intervention humaine, utilisez le générateur de scénario :

```bash
pnpm openclaw qa mantis telegram-desktop-builder \
  --credential-source convex \
  --credential-role maintainer \
  --keep-lease
```

Le générateur loue ou réutilise un bureau Crabbox, installe le binaire natif Linux
Telegram Desktop, restaure optionnellement une archive de session utilisateur, configure
OpenClaw avec le jeton de bot SUT Telegram loué, démarre `openclaw gateway run`
sur le port `38974`, publie un message de disponibilité du bot pilote au groupe privé loué,
puis capture une capture d'écran et un MP4 du bureau VNC visible. Un jeton de bot ne connecte jamais
Telegram Desktop ; il configure seulement OpenClaw. Le visualiseur de bureau est une session utilisateur Telegram
séparée restaurée à partir de
`--telegram-profile-archive-env <name>` ou créée manuellement via VNC et gardée
vivante avec `--keep-lease`.

Drapeaux du générateur Telegram desktop utiles :

- `--lease-id <cbx_...>` réexécute contre une VM où un opérateur s'est déjà connecté à Telegram Desktop.
- `--telegram-profile-archive-env <name>` lit une archive de profil Telegram Desktop `.tgz` en base64 à partir de cette variable d'env et la restaure avant le lancement.
- `--telegram-profile-dir <remote-path>` contrôle le répertoire de profil Telegram Desktop distant. La valeur par défaut est `$HOME/.local/share/TelegramDesktop`.
- `--no-gateway-setup` installe et ouvre Telegram Desktop sans configurer OpenClaw.
- `--credential-source convex --credential-role ci` utilise le courtier d'identifiants partagé au lieu des jetons d'env Telegram directs.

Chaque scénario publié sur PR écrit `mantis-evidence.json` à côté de son rapport.
Ce schéma est la transmission entre le code de scénario et les commentaires GitHub :

```json
{
  "schemaVersion": 1,
  "id": "discord-status-reactions",
  "title": "Mantis Discord Status Reactions QA",
  "summary": "Résumé supérieur lisible par l'homme pour le commentaire PR.",
  "scenario": "discord-status-reactions-tool-only",
  "comparison": {
    "baseline": { "sha": "...", "status": "fail", "expected": "queued-only" },
    "candidate": { "sha": "...", "status": "pass", "expected": "queued -> thinking -> done" },
    "pass": true
  },
  "artifacts": [
    {
      "kind": "timeline",
      "lane": "baseline",
      "label": "Baseline queued-only",
      "path": "baseline/timeline.png",
      "targetPath": "baseline.png",
      "alt": "Chronologie Discord de base de référence",
      "width": 420
    }
  ]
}
```

Les valeurs `path` d'artefact sont relatives au répertoire du manifeste. Les valeurs `targetPath`
sont des chemins relatifs sous le préfixe d'artefact Mantis R2/S3 configuré. L'éditeur
rejette la traversée de chemin et ignore les entrées marquées `"required": false`
quand les aperçus ou vidéos optionnels ne sont pas disponibles.

Types d'artefacts supportés :

- `timeline` : capture d'écran de scénario déterministe, généralement avant/après.
- `desktopScreenshot` : capture d'écran de bureau VNC/navigateur.
- `motionPreview` : GIF animé en ligne généré à partir de l'enregistrement de bureau.
- `motionClip` : MP4 réduit en mouvement qui supprime l'introduction et la queue statiques.
- `fullVideo` : enregistrement MP4 complet pour l'inspection approfondie.
- `metadata` : accompagnement JSON/log.
- `report` : rapport Markdown.

L'éditeur réutilisable est `scripts/mantis/publish-pr-evidence.mjs`. Les workflows
l'appellent avec le manifeste, la PR cible, la racine cible d'artefact, le marqueur de commentaire,
l'URL d'artefact Actions, l'URL d'exécution, et la source de la demande. Il télécharge les artefacts déclarés
vers le bucket Mantis R2/S3 configuré, construit un commentaire PR résumé en premier avec
des images/aperçus en ligne et des vidéos liées, puis met à jour le commentaire de marqueur existant
ou en crée un. Les workflows publient vers `openclaw-crabbox-artifacts`
avec des URL publiques sous `https://artifacts.openclaw.ai`. Ils fournissent le bucket,
la région, et les valeurs d'URL publique directement. L'éditeur réutilisable nécessite :

- `MANTIS_ARTIFACT_R2_ACCESS_KEY_ID`
- `MANTIS_ARTIFACT_R2_SECRET_ACCESS_KEY`
- `MANTIS_ARTIFACT_R2_BUCKET`
- `MANTIS_ARTIFACT_R2_ENDPOINT`
- `MANTIS_ARTIFACT_R2_REGION`
- `MANTIS_ARTIFACT_R2_PUBLIC_BASE_URL`

Vous pouvez aussi déclencher l'exécution des réactions de statut directement à partir d'un commentaire PR :

```text
@openclaw-mantis discord status reactions
```

Le déclencheur de commentaire est intentionnellement étroit. Il s'exécute seulement sur les
commentaires de demande de tirage des utilisateurs ayant un accès en écriture, maintenance ou administrateur, et il reconnaît seulement
les demandes de réaction de statut Discord. Par défaut, il utilise la ref baseline connue comme mauvaise
et le SHA de tête PR actuel comme candidat. Les mainteneurs peuvent remplacer l'une ou l'autre
ref :

```text
@openclaw-mantis discord status reactions baseline=origin/main candidate=HEAD
```

Le QA Telegram en direct peut aussi être déclenché à partir d'un commentaire PR :

```text
@openclaw-mantis telegram
@openclaw-mantis telegram scenario=telegram-status-command
@openclaw-mantis telegram scenarios=telegram-status-command,telegram-mentioned-message-reply
```

Par défaut, il utilise le SHA de tête PR actuel comme candidat et exécute
`telegram-status-command`. Les mainteneurs peuvent remplacer `candidate=...`,
`provider=aws|hetzner`, et `lease=<cbx_...>` quand ils ont besoin d'une ref spécifique ou d'un
bureau Crabbox préchauffé.

Exemples de commande ClawSweeper :

```text
@clawsweeper mantis discord discord-status-reactions-tool-only
@clawsweeper verify e2e discord
```

La première commande est explicite et centrée sur le scénario. La deuxième peut plus tard
mapper une PR ou un problème aux scénarios Mantis recommandés à partir des étiquettes, fichiers modifiés, et
résultats d'examen ClawSweeper.

## Cycle de vie d'une exécution

1. Acquérir les identifiants.
2. Allouer ou réutiliser une VM.
3. Préparer le profil de bureau/navigateur lorsque le scénario nécessite des preuves d'interface utilisateur.
4. Préparer un checkout propre pour la référence de base.
5. Installer les dépendances et construire uniquement ce dont le scénario a besoin.
6. Démarrer une passerelle OpenClaw enfant avec un répertoire d'état isolé.
7. Configurer le transport en direct, le fournisseur, le modèle et le profil de navigateur.
8. Exécuter le scénario et capturer les preuves de base.
9. Arrêter la passerelle et conserver les journaux.
10. Préparer la référence candidate dans la même VM.
11. Exécuter le même scénario et capturer les preuves candidates.
12. Comparer les résultats de l'oracle et les preuves visuelles.
13. Écrire les artefacts Markdown, JSON, journaux, captures d'écran et traces optionnels.
14. Télécharger les artefacts GitHub Actions.
15. Publier un message de statut concis sur PR ou Discord.

Le scénario doit pouvoir échouer de deux manières différentes :

- **Bug reproduit** : la base a échoué de la manière attendue.
- **Échec du harnais** : la configuration de l'environnement, les identifiants, l'API Discord, le navigateur ou le fournisseur ont échoué avant que l'oracle du bug soit significatif.

Le rapport final doit séparer ces cas afin que les responsables ne confondent pas un environnement instable avec le comportement du produit.

## MVP Discord

Le premier scénario doit cibler les réactions de statut Discord dans les canaux de guilde où le mode de livraison de réponse source est `message_tool_only`.

Pourquoi c'est une bonne graine Mantis :

- C'est visible dans Discord sous forme de réactions sur le message déclencheur.
- Il a un oracle REST fort grâce à l'état de réaction des messages Discord.
- Il exerce une véritable passerelle OpenClaw, l'authentification du bot Discord, la distribution de messages, le mode de livraison de réponse source, l'état de réaction de statut et le cycle de vie du tour du modèle.
- C'est assez étroit pour garder la première implémentation honnête.

Forme de scénario attendue :

```yaml
id: discord-status-reactions-tool-only
transport: discord
baseline:
  expect:
    reproduced: true
candidate:
  expect:
    fixed: true
config:
  messages:
    ackReaction: "👀"
    ackReactionScope: "group-mentions"
    groupChat:
      visibleReplies: "message_tool"
    statusReactions:
      enabled: true
      timing:
        debounceMs: 0
discord:
  requireMention: true
  notifyChannel: operator-notify
evidence:
  rest:
    messageReactions: true
  browser:
    screenshotMessageRow: true
```

Les preuves de base doivent montrer la réaction d'accusé de réception en attente mais aucune transition de cycle de vie en mode tool-only. Les preuves candidates doivent montrer les réactions de statut du cycle de vie s'exécutant lorsque `messages.statusReactions.enabled` est explicitement vrai.

La première tranche exécutable est le scénario QA Discord en direct opt-in :

```bash
pnpm openclaw qa discord \
  --scenario discord-status-reactions-tool-only \
  --provider-mode live-frontier \
  --model openai/gpt-5.4 \
  --alt-model openai/gpt-5.4 \
  --fast \
  --output-dir .artifacts/qa-e2e/mantis/discord-status-reactions-candidate
```

Il configure le SUT avec la gestion de guilde toujours activée, `visibleReplies: "message_tool"`, `ackReaction: "👀"` et les réactions de statut explicites. L'oracle interroge le vrai message déclencheur Discord et s'attend à la séquence observée `👀 -> 🤔 -> 👍`. Les artefacts incluent `discord-qa-reaction-timelines.json`, `discord-status-reactions-tool-only-timeline.html` et `discord-status-reactions-tool-only-timeline.png`.

## Pièces QA existantes

Mantis doit s'appuyer sur la pile QA privée existante au lieu de commencer de zéro :

- `pnpm openclaw qa discord` exécute déjà une voie Discord en direct avec les bots pilote et SUT.
- Le runner de transport en direct écrit déjà les rapports et les artefacts de messages observés sous `.artifacts/qa-e2e/`.
- Les baux de credentials Convex fournissent déjà un accès exclusif aux credentials de transport en direct partagés.
- Le service de contrôle du navigateur supporte déjà les captures d'écran, les snapshots, les profils gérés sans interface et les profils CDP distants.
- QA Lab a déjà une interface de débogage et un bus pour les tests de forme transport.

La première implémentation de Mantis peut être un runner avant/après mince sur ces pièces, plus une couche de preuves visuelles.

## Modèle de preuves

Chaque exécution écrit un répertoire d'artefacts stable :

```text
.artifacts/qa-e2e/mantis/<run-id>/
  mantis-report.md
  mantis-summary.json
  baseline/
    summary.json
    discord-message.json
    screenshot-message-row.png
    gateway-debug/
  candidate/
    summary.json
    discord-message.json
    screenshot-message-row.png
    gateway-debug/
  comparison.json
  run.log
```

`mantis-summary.json` doit être la source de vérité lisible par machine. Le rapport Markdown est pour les commentaires PR et l'examen humain.

Le résumé doit inclure :

- les références et SHA testés
- l'ID de transport et de scénario
- le fournisseur de machine et l'ID de machine ou l'ID de bail
- la source de credentials sans valeurs secrètes
- le résultat de base
- le résultat candidat
- si le bug a été reproduit sur la base
- si le candidat l'a corrigé
- les chemins d'artefacts
- les problèmes de configuration ou de nettoyage assainis

Les captures d'écran sont des preuves, pas des secrets. Elles nécessitent toujours une discipline de rédaction : les noms de canaux privés, les noms d'utilisateurs ou le contenu des messages peuvent apparaître. Pour les PR publiques, préférez les liens d'artefacts GitHub Actions aux images intégrées jusqu'à ce que l'histoire de la rédaction soit plus solide.

## Navigateur et VNC

La voie du navigateur a deux modes :

- **Automatisation sans interface** : par défaut pour CI. Chrome s'exécute avec CDP activé, et Playwright ou le contrôle du navigateur OpenClaw capture les captures d'écran.
- **Secours VNC** : activé sur la même VM lorsque la connexion, l'authentification multifacteur, l'anti-automatisation Discord ou le débogage visuel nécessite un humain.

Le profil de navigateur observateur Discord doit être assez persistant pour éviter de se connecter à chaque exécution, mais isolé de l'état du navigateur personnel. Un profil appartient au pool de machines Mantis, pas à un ordinateur portable de développeur.

Lorsque Mantis se bloque, il publie un message de statut Discord avec :

- l'ID d'exécution
- l'ID du scénario
- le fournisseur de machine
- le répertoire d'artefacts
- les instructions de connexion VNC ou noVNC si disponibles
- un texte de blocage court

Le premier déploiement privé peut publier ces messages sur le canal opérateur existant et passer à un canal Mantis dédié plus tard.

## Machines

Mantis doit préférer AWS via Crabbox pour la première implémentation distante. Crabbox nous donne des machines préchauffées, le suivi des baux, l'hydratation, les journaux, les résultats et le nettoyage. Si la capacité AWS est trop lente ou indisponible, ajoutez un fournisseur Hetzner derrière la même interface de machine.

Exigences minimales de VM :

- Linux avec une installation de Chrome ou Chromium capable de bureau
- Accès CDP pour l'automatisation du navigateur
- VNC ou noVNC pour le secours
- Node 22 et pnpm
- Checkout OpenClaw et cache de dépendances
- Cache du navigateur Playwright Chromium lorsque Playwright est utilisé
- Suffisamment de CPU et de mémoire pour une passerelle OpenClaw, un navigateur et une exécution de modèle
- Accès sortant à Discord, GitHub, les fournisseurs de modèles et le courtier de credentials

La VM ne doit pas conserver les secrets bruts de longue durée en dehors des magasins de credentials ou de profils de navigateur attendus.

## Secrets

Les secrets vivent dans les secrets de l'organisation ou du référentiel GitHub pour les exécutions distantes, et dans un fichier secret contrôlé par l'opérateur local pour les exécutions locales.

Noms de secrets recommandés :

- `OPENCLAW_QA_DISCORD_MANTIS_BOT_TOKEN`
- `OPENCLAW_QA_DISCORD_DRIVER_BOT_TOKEN`
- `OPENCLAW_QA_DISCORD_SUT_BOT_TOKEN`
- `OPENCLAW_QA_DISCORD_GUILD_ID`
- `OPENCLAW_QA_DISCORD_CHANNEL_ID`
- `OPENCLAW_QA_DISCORD_NOTIFY_CHANNEL_ID`
- `OPENCLAW_QA_REDACT_PUBLIC_METADATA=1` pour les téléchargements d'artefacts GitHub publics
- `OPENCLAW_QA_CONVEX_SITE_URL`
- `OPENCLAW_QA_CONVEX_SECRET_CI`
- `OPENCLAW_QA_MANTIS_CRABBOX_COORDINATOR`
- `OPENCLAW_QA_MANTIS_CRABBOX_COORDINATOR_TOKEN`

À long terme, le pool de credentials Convex doit rester la source normale pour les credentials de transport en direct. Les secrets GitHub amorçent le courtier et les voies de secours. Le flux de travail des réactions de statut Discord Mantis remapppe les secrets Crabbox Mantis aux variables d'environnement `CRABBOX_COORDINATOR` et `CRABBOX_COORDINATOR_TOKEN` que l'interface de ligne de commande Crabbox attend. Les noms de secrets GitHub simples `CRABBOX_*` restent acceptés comme compatibilité rétroactive.

Le runner Mantis ne doit jamais imprimer :

- Les jetons de bot Discord
- Les clés API du fournisseur
- Les cookies du navigateur
- Le contenu du profil d'authentification
- Les mots de passe VNC
- Les charges utiles de credentials brutes

Les téléchargements d'artefacts publics doivent également rédiger les métadonnées cibles Discord telles que les ID de bot, de guilde, de canal et de message. Le flux de travail de fumée GitHub active `OPENCLAW_QA_REDACT_PUBLIC_METADATA=1` pour cette raison.

Si un jeton est accidentellement collé dans un problème, une PR, un chat ou un journal, faites-le tourner après que le nouveau secret ait été stocké.

## Artefacts GitHub et commentaires PR

Les flux de travail Mantis doivent télécharger le bundle de preuves complet en tant qu'artefact Actions de courte durée. Lorsque le flux de travail est exécuté pour un rapport de bug ou une PR de correction, il doit également publier des médias réduits en ligne vers le bucket Mantis R2/S3 configuré et upsert un commentaire sur ce bug ou cette PR de correction avec des captures d'écran avant/après intégrées. Ne publiez pas la preuve principale uniquement sur une PR d'automatisation QA générique. Les journaux bruts, les messages observés et autres preuves volumineuses restent dans l'artefact Actions.

Les flux de travail de production doivent publier ces commentaires avec l'application GitHub Mantis, pas avec `github-actions[bot]`. Stockez l'ID de l'application et la clé privée en tant que secrets GitHub Actions `MANTIS_GITHUB_APP_ID` et `MANTIS_GITHUB_APP_PRIVATE_KEY`. Le flux de travail utilise un marqueur caché comme clé upsert, met à jour ce commentaire lorsque le jeton peut le modifier et crée un nouveau commentaire appartenant à Mantis lorsqu'un marqueur bot plus ancien ne peut pas être modifié.

Le commentaire PR doit être court et visuel :

```md
Mantis Discord Status Reactions QA

Résumé : Mantis a réexécuté le bug de réaction de statut Discord signalé par rapport à la base connue mauvaise et à la correction candidate. La base a reproduit le bug, tandis que le candidat a montré la séquence attendue en attente -> réflexion -> terminé.

- Scénario : `discord-status-reactions-tool-only`
- Exécution : <lien d'exécution du flux de travail>
- Artefact : <lien d'artefact>
- Base : `<statut>` à `<sha>`
- Candidat : `<statut>` à `<sha>`

| Base                | Candidat            |
| ------------------- | ------------------- |
| <capture d'écran>   | <capture d'écran>   |
```

Lorsque l'exécution échoue parce que le harnais a échoué, le commentaire doit le dire au lieu d'impliquer que le candidat a échoué.

## Notes de déploiement privé

Un déploiement privé peut déjà avoir une application Discord Mantis. Réutilisez cette application au lieu de créer une autre application lorsqu'elle a les bonnes permissions de bot et peut être tournée en toute sécurité.

Définissez le canal de notification opérateur initial via les secrets ou la configuration de déploiement. Il peut d'abord pointer vers un canal de responsable ou d'opérations existant, puis passer à un canal Mantis dédié une fois qu'il existe.

Ne mettez pas les ID de guilde, les ID de canal, les jetons de bot, les cookies du navigateur ou les mots de passe VNC dans ce document. Stockez-les dans les secrets GitHub, le courtier de credentials ou le magasin de secrets local de l'opérateur.

## Ajouter un scénario

Un scénario Mantis doit déclarer :

- l'ID et le titre
- le transport
- les credentials requis
- la politique de référence de base
- la politique de référence candidate
- le correctif de configuration OpenClaw
- les étapes de configuration
- le stimulus
- l'oracle de base attendu
- l'oracle candidat attendu
- les cibles de capture visuelles
- le budget de délai d'attente
- les étapes de nettoyage

Les scénarios doivent préférer les oracles petits et typés :

- L'état de réaction Discord pour les bugs de réaction
- Les références de messages Discord pour les bugs de threading
- L'état de l'API de thread ts et de réaction Slack pour les bugs Slack
- Les ID de messages et en-têtes d'e-mail pour les bugs d'e-mail
- Les captures d'écran du navigateur lorsque l'interface utilisateur est le seul observable fiable

Les vérifications de vision doivent être additives. Si une API de plateforme peut prouver le bug, utilisez l'API comme oracle de réussite/échec et gardez les captures d'écran pour la confiance humaine.

## Expansion du fournisseur

Après Discord, le même runner peut ajouter :

- Slack : réactions, threads, mentions d'application, modales, téléchargements de fichiers.
- E-mail : authentification Gmail et threading de messages utilisant `gog` où les connecteurs ne suffisent pas.
- WhatsApp : connexion par code QR, réidentification, livraison de messages, médias, réactions.
- Telegram : gating de mention de groupe, commandes, réactions où disponibles.
- Matrix : salons chiffrés, relations de thread ou de réponse, reprise de redémarrage.

Chaque transport doit avoir un scénario de fumée bon marché et un ou plusieurs scénarios de classe de bug. Les scénarios visuels coûteux doivent rester opt-in.

## Questions ouvertes

- Quel bot Discord devrait être le pilote et lequel devrait être le SUT, lorsque
  le bot Mantis existant est réutilisé ?
- La connexion du navigateur observateur devrait-elle utiliser un compte Discord humain, un compte de test,
  ou seulement des preuves REST lisibles par les bots pour la première phase ?
- Combien de temps GitHub devrait-il conserver les artefacts Mantis pour les PR ?
- Quand ClawSweeper devrait-il recommander automatiquement Mantis au lieu d'attendre une
  commande du mainteneur ?
- Les captures d'écran devraient-elles être masquées ou recadrées avant le téléchargement pour les PR publiques ?
