---
title: "Slack - Channel Setup and Operations Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Channel Setup and Operations Maturity Note

## Résumé

La configuration de Slack a une surface d'implémentation large et actuelle : la documentation de production couvre Socket Mode et les manifestes HTTP, les types de jetons requis, les SecretRefs, l'env fallback, les lectures de jetons utilisateur et la précédence multi-compte. Le score reste Beta car la configuration réelle de l'espace de travail est toujours sensible à la portée et à la réinstallation, et les archives montrent une confusion répétée des opérateurs autour des portées manquantes, des échanges de types de jetons et de la promotion des valeurs par défaut multi-compte.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Channel Setup and Operations`
- Fusionnée à partir de : `Setup, Auth, and Runtime Health`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- App Install : Couvre App Install lors de l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/utilisateur/signing-secret et le comportement connexe d'installation d'app, d'authentification, de manifeste et de portées.
- Identifiants d'application Slack : Couvre les jetons bot/app/utilisateur, la gestion des signing-secret et la configuration des identifiants Slack pour l'authentification d'application.
- Manifest : Couvre Manifest lors de l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/utilisateur/signing-secret et le comportement connexe d'installation d'app, d'authentification, de manifeste et de portées.
- Portées : Couvre Portées lors de l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/utilisateur/signing-secret et le comportement connexe d'installation d'app, d'authentification, de manifeste et de portées.
- Diagnostics d'état du canal : Couvre `openclaw channels status --probe`, les snapshots de compte, les champs source/état du jeton, les diagnostics de capacité et de portée, et les conseils de réparation Slack.
- État du compte Slack : Couvre les snapshots de compte, les champs source/état du jeton, les résumés de capacité et la sortie d'état Slack.
- Réparation d'opérateur : Couvre Réparation d'opérateur dans `openclaw channels status --probe`, les snapshots de compte, les champs source/état du jeton, les diagnostics de capacité et de portée, et le comportement connexe de diagnostics, d'état et de réparation d'opérateur.
- Socket : Couvre Socket dans le démarrage/reconnexion/backoff de Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime.
- Transport HTTP : Couvre l'enregistrement de l'URL de requête HTTP, la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime HTTP Slack.
- Cycle de vie du runtime : Couvre Cycle de vie du runtime dans le démarrage/reconnexion/backoff de Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime.
- Socket : Couvre Socket dans le démarrage/reconnexion/backoff de Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime
- Transport HTTP : Couvre l'enregistrement de l'URL de requête HTTP, la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime HTTP Slack
- Cycle de vie du runtime : Couvre Cycle de vie du runtime dans le démarrage/reconnexion/backoff de Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime
- Diagnostics d'état du canal : Couvre `openclaw channels status --probe`, les snapshots de compte, les champs source/état du jeton, les diagnostics de capacité et de portée, et les conseils de réparation Slack
- État du compte Slack : Couvre les snapshots de compte, les champs source/état du jeton, les résumés de capacité et la sortie d'état Slack
- Réparation d'opérateur : Couvre Réparation d'opérateur dans `openclaw channels status --probe`, les snapshots de compte, les champs source/état du jeton, les diagnostics de capacité et de portée, et le comportement connexe de diagnostics, d'état et de réparation d'opérateur

## Fonctionnalités

- App Install : Couvre App Install lors de l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/utilisateur/signing-secret et le comportement connexe d'installation d'app, d'authentification, de manifeste et de portées.
- Identifiants d'application Slack : Couvre les jetons bot/app/utilisateur, la gestion des signing-secret et la configuration des identifiants Slack pour l'authentification d'application.
- Manifest : Couvre Manifest lors de l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/utilisateur/signing-secret et le comportement connexe d'installation d'app, d'authentification, de manifeste et de portées.
- Portées : Couvre Portées lors de l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/utilisateur/signing-secret et le comportement connexe d'installation d'app, d'authentification, de manifeste et de portées.
- Diagnostics d'état du canal : Couvre `openclaw channels status --probe`, les snapshots de compte, les champs source/état du jeton, les diagnostics de capacité et de portée, et les conseils de réparation Slack.
- État du compte Slack : Couvre les snapshots de compte, les champs source/état du jeton, les résumés de capacité et la sortie d'état Slack.
- Réparation d'opérateur : Couvre Réparation d'opérateur dans `openclaw channels status --probe`, les snapshots de compte, les champs source/état du jeton, les diagnostics de capacité et de portée, et le comportement connexe de diagnostics, d'état et de réparation d'opérateur.
- Socket : Couvre Socket dans le démarrage/reconnexion/backoff de Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime.
- Transport HTTP : Couvre l'enregistrement de l'URL de requête HTTP, la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime HTTP Slack.
- Cycle de vie du runtime : Couvre Cycle de vie du runtime dans le démarrage/reconnexion/backoff de Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, l'état/liveness et le comportement de démarrage/saut du runtime.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : La documentation de production et les tests de schéma de configuration couvrent Socket Mode, le mode HTTP, les signing secrets, la précédence de la source de jeton, les SecretRefs, les jetons utilisateur, la validation `dmPolicy="open"` et l'héritage de compte.
- Signaux négatifs : La voie Slack en direct valide un manifeste SUT plus étroit, pas le manifeste de production complet, le mode de lecture de jeton utilisateur, chaque fournisseur SecretRef ou l'intégration multi-compte complète.
- Lacunes d'intégration : Manquent les fiches de pointage d'installation/administration d'espace de travail en direct pour la réinstallation d'application après les changements de portée, les restrictions de politique d'espace de travail, les applications Slack multiples et le basculement de lecture/écriture de jeton utilisateur.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : `#62387` montre que la promotion multi-compte peut supprimer les valeurs par défaut partagées lorsque les clés de politique/identifiants de canal sont promues incorrectement.
- Rapports Discrawl : Les threads de support de configuration citent à plusieurs reprises les `im:write` manquants, les portées `*:read` manquantes, les échanges de jeton app/bot et les exigences de réinstallation d'application Slack après les changements de portée.
- Bonnes qualités : La source sépare les surfaces d'identifiants actifs par mode, suit la source/l'état des identifiants, supporte les SecretRefs et documente les manifestes recommandés/minimaux avec la justification de la portée.
- Mauvaises qualités : La configuration de Slack est toujours fragile pour l'opérateur car Slack n'accorde les portées qu'après la réinstallation, la surface du manifeste est longue et l'état du jeton/source est facile à mal lire entre les comptes par défaut et nommés.
- Exclu de la qualité : Nombre de tests unitaires, largeur de voie en direct et profondeur d'intégration.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour App Install, Slack app credentials, Manifest, Scopes, Channel status diagnostics, Slack account status, Operator Repair, Socket, HTTP transport, Runtime Lifecycle.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une fiche de pointage d'installation d'espace de travail en direct ou enregistrée qui commence à partir d'une application Slack propre, applique le manifeste, réinstalle après les changements de portée et vérifie l'état du jeton/source.
- Ajouter des exemples explicites du responsable pour migrer un compte Slack par défaut dans des comptes nommés sans perdre les clés de politique partagées.
- Ajouter des diagnostics orientés opérateur qui distinguent « portée présente dans le manifeste » de « portée accordée sur le jeton bot installé ».

## Preuves

### Docs

- `docs/channels/slack.md` documente l'installation, la configuration rapide, Socket Mode et les manifestes HTTP, la liste de contrôle des portées, le modèle de jeton, les exemples SecretRef et la configuration multi-compte.
- `docs/plugins/reference/slack.md` identifie le package `@openclaw/slack`, les routes d'installation et la surface du canal `slack`.
- `docs/gateway/secrets.md` est la référence SecretRef liée pour les identifiants Slack.

### Source

- `extensions/slack/openclaw.plugin.json` enregistre l'ID de plugin `slack`, les variables d'environnement du canal `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` et `SLACK_USER_TOKEN`.
- `extensions/slack/src/config-schema.ts` valide le jeton, le secret de signature HTTP, l'ajustement Socket Mode, le jeton utilisateur, `dmPolicy` et les champs au niveau du compte.
- `extensions/slack/src/accounts.ts` résout les comptes par défaut/nommés, la précédence des jetons config/env, `allowFrom`, les identifiants actifs spécifiques au mode, les actions, le streaming et les champs média.
- `extensions/slack/src/account-inspect.ts` rapporte la source/statut par identifiant, y compris le `signingSecretStatus` spécifique à HTTP.
- `extensions/slack/src/scopes.ts`, `extensions/slack/src/security.ts`, `extensions/slack/src/security-audit.ts` et `extensions/slack/src/doctor.ts` soutiennent les rapports de portée/sécurité/réparation.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` construit la configuration QA Slack avec des jetons de bot SUT/driver distincts et un jeton d'application SUT.
- `docs/concepts/qa-e2e-automation.md` documente la configuration de l'espace de travail QA Slack en direct avec des applications Slack Driver et SUT séparées.
- La couverture de la voie en direct est intentionnellement plus étroite que le manifeste de production et ne couvre pas toutes les branches de configuration/administration.

### Tests unitaires

- `extensions/slack/src/config-schema.test.ts` couvre la validation du secret de signature HTTP, les paramètres de ping/pong Socket Mode, les garde-fous `dmPolicy="open"` et les champs de jeton utilisateur.
- `extensions/slack/src/accounts.test.ts` couvre la précédence de la liste d'autorisation, l'héritage des comptes nommés, les défaillances SecretRef, l'activité des identifiants en mode HTTP et le repli env.
- `extensions/slack/src/channel.lazy-seams.test.ts`, `extensions/slack/src/scopes.test.ts`, `extensions/slack/src/security-audit.test.ts` et `extensions/slack/src/doctor.test.ts` couvrent les coutures de statut, portée, sécurité et docteur.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "Slack install app manifest scopes token multi-account" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "slack appToken botToken signingSecret" --json`

Résultats :

- La recherche de problème ciblée a retourné `[]`.
- La requête plus large a retourné `#62387`, "fix(channels): most channels missing namedAccountPromotionKeys - multi-account promotion strips shared defaults", avec les clés de politique et d'identifiant Slack appelées comme exemples.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack app manifest scopes token"`

Résultats :

- A retourné des fils de support sur le téléchargement/configuration d'images Slack, les portées manquantes, les vérifications de type de jeton, la réinstallation d'application après les modifications de portée OAuth, `auth.scopes`/`apps.permissions.info` `unknown_method` et les lacunes de manifeste d'intégration `im:write`.
