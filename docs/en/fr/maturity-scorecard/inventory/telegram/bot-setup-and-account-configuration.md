---
title: "Telegram - Note de Maturité de Configuration et Opérations de Canal"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Note de Maturité de Configuration et Opérations de Canal

## Résumé

La configuration de Telegram est un composant solide de Beta à Stable. La documentation publique couvre BotFather,
le placement des jetons, l'alternative env, la précédence des jetons conscients du compte, le comportement de l'assistant de configuration,
et les diagnostics de démarrage. Le principal frein à la maturité est la variance des opérateurs : les fichiers de jetons, les SecretRefs,
les valeurs par défaut multi-comptes, et les résumés de statut apparaissent toujours dans les rapports d'archives récents.

## Normalisation

Catégorie active après la normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Configuration et Opérations de Canal`
- Fusionnée à partir de : `Configuration et Comptes`, `Cycle de Vie d'Exécution`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Création de jeton BotFather : Création de jeton BotFather et premier démarrage de passerelle
- TELEGRAM_BOT_TOKEN : TELEGRAM_BOT_TOKEN, botToken, tokenFile, et jeton limité au compte
- Capture de credentials de l'assistant de configuration : Capture de credentials de l'assistant de configuration, invites de liste blanche, et valeurs par défaut de politique DM
- Startup getMe : Startup getMe, cache d'info-bot, limitation de compte, et valeur par défaut multi-compte
- Surfaçage Doctor/status : Surfaçage Doctor/status pour jetons invalides, valeurs par défaut manquantes, et lecture seule
- Configuration de compte nommé : Configuration de compte nommé, sélection de compte par défaut, groupe local au compte
- Cibles CLI/message-tool : IDs de chat numériques, noms d'utilisateur, forum-topic
- Adaptateurs de répertoire : Adaptateurs de répertoire et pairs/groupes configurés pour les listes de cibles visibles par l'utilisateur
- Statut du canal : Statut du canal, channels status --probe, résumés de source de jeton, vivacité
- Sortie limitée au compte : Sortie limitée au compte, sondage, média, et résolution de cible d'approbation
- Démarrage du runner de long polling : Démarrage du runner de long polling, protection contre les sondeurs dupliqués, décalages de mise à jour, et cycle de vie du compte
- Démarrage du listener webhook : Démarrage du listener webhook, validation secrète, dispatch d'événement asynchrone, et local
- Reconnexion : Reconnexion, erreurs réseau récupérables, getUpdates bloqué, pinces de délai d'attente, et gestion de la récupération.
- Redémarrage : Redémarrage et comportement de récupération après rotation de jeton, abandons de processus, et rechargements de compte.
- Configuration de compte nommé : Couvre Configuration de compte nommé, sélection de compte par défaut, comportement de groupe local au compte.
- Adaptateurs de répertoire et pairs/groupes configurés pour : Couvre Adaptateurs de répertoire et pairs/groupes configurés pour le comportement des listes de cibles visibles par l'utilisateur.
- Statut du canal : Couvre Statut du canal, `channels status --probe`, résumés de source de jeton, comportement de vivacité.
- Sortie limitée au compte : Couvre Sortie limitée au compte, sondage, média, et comportement de résolution de cible d'approbation.
- Démarrage du runner de long polling : Démarrage du runner de long polling, protection contre les sondeurs dupliqués, décalages de mise à jour, et cycle de vie du compte
- Reconnexion : Reconnexion, erreurs réseau récupérables, getUpdates bloqué, pinces de délai d'attente, et gestion de la récupération
- Redémarrage : Redémarrage et comportement de récupération après rotation de jeton, abandons de processus, et rechargements de compte

## Fonctionnalités

- Création de jeton BotFather : Création de jeton BotFather et premier démarrage de passerelle
- TELEGRAM_BOT_TOKEN : TELEGRAM_BOT_TOKEN, botToken, tokenFile, et jeton limité au compte
- Capture de credentials de l'assistant de configuration : Capture de credentials de l'assistant de configuration, invites de liste blanche, et valeurs par défaut de politique DM
- Startup getMe : Startup getMe, cache d'info-bot, limitation de compte, et valeur par défaut multi-compte
- Surfaçage Doctor/status : Surfaçage Doctor/status pour jetons invalides, valeurs par défaut manquantes, et lecture seule
- Configuration de compte nommé : Configuration de compte nommé, sélection de compte par défaut, groupe local au compte
- Cibles CLI/message-tool : IDs de chat numériques, noms d'utilisateur, forum-topic
- Adaptateurs de répertoire : Adaptateurs de répertoire et pairs/groupes configurés pour les listes de cibles visibles par l'utilisateur
- Statut du canal : Statut du canal, channels status --probe, résumés de source de jeton, vivacité
- Sortie limitée au compte : Sortie limitée au compte, sondage, média, et résolution de cible d'approbation

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs :
  la configuration, le schéma de config, la résolution de compte, le statut, le doctor, et le package Telegram
  Les flux Docker ont tous des ancres source et test.
- Signaux négatifs :
  la preuve du package en direct se concentre sur l'installation, l'intégration, le doctor, et les chemins de réponse de groupe ;
  elle n'exerce pas chaque forme de credential ou chaque branche d'héritage multi-compte.
- Lacunes d'intégration :
  preuve en direct récurrente manquante pour les SecretRefs de fichier de jeton, la config de groupe local au compte,
  et les invites de migration de compte par défaut sur les hôtes frais et mis à niveau.

## Score de Qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl :
  les rapports multi-compte et SecretRef maintiennent ceci en dessous de Stable : #61012, #62985,
  #74832, #74833, et #82718.
- Rapports Discrawl :
  le trafic d'aide de configuration inclut la confusion d'intégration BotFather/jeton et les demandes
  de preuve de démarrage multi-compte en direct.
- Bonnes qualités :
  la résolution de jeton est consciente du compte, les jetons invalides échouent avant le sondage, l'invalidation du cache d'info-bot est explicite,
  et l'assistant de configuration écrit des listes blanches numériques.
- Mauvaises qualités :
  les opérateurs peuvent toujours confondre la sélection de compte par défaut, les lectures de statut SecretRef,
  les IDs de groupe par rapport aux IDs d'utilisateur, et les configurations env uniquement.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue de l'AQ en direct, et le nombre de tests n'ont pas été
  utilisés comme entrées de Qualité.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les docs archivées, la source, le test, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la création de jeton BotFather, TELEGRAM_BOT_TOKEN, Capture de credentials de l'assistant de configuration, Startup getMe, Surfaçage Doctor/status, Configuration de compte nommé, Cibles CLI/message-tool, Adaptateurs de répertoire, Statut du canal, Sortie limitée au compte.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuve et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une preuve de scorecard de version pour le fichier de jeton, SecretRef, env uniquement par défaut, et
  les configurations de compte nommé multi-compte.
- Rendre les avertissements de compte par défaut et la config de groupe local au compte plus faciles à inspecter
  dans `openclaw channels status`.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente la création de jeton BotFather,
  l'alternative env, la résolution de jeton consciente du compte, les diagnostics de jeton invalide, et les conseils de compte par défaut multi-compte.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md` est la référence de configuration Telegram liée.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/setup-surface.ts`
  implémente la capture de credential et de liste blanche de l'assistant de configuration.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/accounts.ts` résout
  les IDs de compte, l'alternative de compte par défaut, les portes d'action, et les sources de jeton.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/channel.ts` câble le cache d'info-bot,
  les sondes de démarrage, l'adaptateur de configuration, le statut, le doctor, et le démarrage du moniteur.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/token.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-info-cache.ts`
  gèrent le comportement du cache de jeton et d'identité de bot.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-live-docker.sh`
  installe le package, exécute l'intégration, ajoute Telegram, et exécute les chemins doctor.
- `/Users/kevinlin/code/openclaw/test/scripts/npm-telegram-live.test.ts`
  affirme le harnais Docker Telegram du package installé, les alias de credential,
  les commandes bornées, et les étapes doctor/intégration.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-rtt-config.mjs`
  construit une config de groupe Telegram en direct avec des jetons de bot, des listes blanches de groupe, et
  des paramètres de groupe gérés par mention.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/accounts.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/token.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/config-schema.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/setup-surface.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/channel.gateway.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/doctor.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Telegram SecretRef" --json`

Résultats :

- #52130 issue ouverte : redémarrage tempête de `telegram.retry.jitter` type mismatch
  plus SecretRef doctor trompeur pour jeton Telegram.
- #74832 issue ouverte : `openclaw status` échoue sur Telegram file SecretRef lors de la
  résolution des métadonnées de liste blanche.
- #74833 PR ouverte : éviter de résoudre les secrets pour les accesseurs de statut.

Requête :

`gitcrawl search openclaw/openclaw --query "Telegram multi account" --json`

Résultats :

- #61012 issue ouverte : le routage multi-bot Telegram ignore le jeton de compte par défaut
  pour les messages sortants.
- #82718 PR ouverte : les docs clarifient la config de groupe local au compte.
- #64609 issue ouverte : groupe/topic `systemPrompt` ignoré dans la config multi-compte
  en raison de la résolution de config incohérente.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram bot token setup"`

Résultats :

- `users-helping-users`, 2026-04-26 : l'utilisateur de configuration pour la première fois a décrit la création d'un
  jeton BotFather et son entrée lors de la configuration OpenClaw.
- `users-helping-users`, 2026-05-12 : le rapport VPS a dit qu'un jeton Telegram bot frais
  a fonctionné brièvement, puis le sondage a cessé de répondre.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram multi account"`

Résultats :

- `clawtributors`, 2026-05-12 : la preuve de démarrage multi-compte Telegram a été
  appelée comme le bloqueur pour PR #80986.
- `Vincent <> Molty - The Crustacean Kabal`, 2026-05-08 : le balayage de version/régression
  a listé le résolveur de jeton multi-compte Telegram parmi les problèmes pressants.
