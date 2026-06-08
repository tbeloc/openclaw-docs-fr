---
title: "Telegram - Multi Account CLI Targets and Status Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Multi Account CLI Targets and Status Maturity Note

## Résumé

Le routage multi-compte Telegram, les cibles CLI, les pairs de répertoire et le statut sont un composant Beta. L'implémentation supporte la configuration de comptes nommés, la sélection de compte par défaut, les pairs de répertoire, l'analyse des cibles, les cibles de nom d'utilisateur/ID de chat/sujet de forum, l'envoi de messages/sondage CLI et les résumés de statut de canal. La qualité est limitée par les problèmes non résolus de résolution de jetons multi-compte, l'ambiguïté de la configuration de groupe locale au compte et les régressions de résumé de statut.

## Portée de la catégorie

- Configuration de compte nommé, sélection de compte par défaut, configuration de groupe locale au compte et portes d'action à portée de compte.
- Cibles CLI/outil de message : ID de chat numériques, noms d'utilisateur, cibles de sujet de forum `chat:topic`, ID de réponse, ID de fil, options de pin et de forçage de document.
- Adaptateurs de répertoire et pairs/groupes configurés pour les listes de cibles visibles par l'utilisateur.
- Statut de canal, `channels status --probe`, résumés de source de jeton, problèmes de vivacité et étiquettes d'exécution.
- Résolution de cible sortante, sondage, média et approbation à portée de compte.

## Fonctionnalités

- Configuration de compte nommé : Configuration de compte nommé, sélection de compte par défaut, configuration de groupe locale au compte
- Cibles CLI/outil de message : ID de chat numériques, noms d'utilisateur, sujet de forum
- Adaptateurs de répertoire : Adaptateurs de répertoire et pairs/groupes configurés pour les listes de cibles visibles par l'utilisateur
- Statut de canal : Statut de canal, channels status --probe, résumés de source de jeton, vivacité
- Sortante à portée de compte : Sortante à portée de compte, sondage, média et résolution de cible d'approbation

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  l'analyse des cibles, l'adaptateur sortant, la configuration du répertoire, la sélection de compte, la configuration de compte, le statut et le démarrage de la passerelle de canal ont des tests ciblés.
- Signaux négatifs :
  la preuve en direct utilise principalement un compte SUT et une cible de groupe ; elle n'exerce pas à plusieurs reprises les flottes multi-bot, la réécriture de cible de nom d'utilisateur, les listes de répertoire, la configuration de sujet locale au compte ou les permutations de sonde de statut.
- Lacunes d'intégration :
  ajouter une preuve en direct pour deux comptes Telegram, `defaultAccount` explicite, configuration de groupe locale au compte, réécriture de cible de nom d'utilisateur, cibles de sujet, sortie de statut/sonde et livraison d'approbation à portée de compte.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl :
  #61012, #64609, #63380, #70568, #82718, #79797, #79553 et #69529 montrent un risque récurrent de routage multi-compte, de statut et inter-fournisseur.
- Rapports Discrawl :
  la preuve de démarrage multi-compte en direct a bloqué la PR #80986, et les résumés des responsables ont listé le résolveur de jeton multi-compte Telegram et le routage de groupe comme des problèmes pressants.
- Bonnes qualités :
  la résolution de compte est centralisée, les avertissements de compte par défaut existent, les portes d'action sont conscientes du compte et l'analyse des cibles supporte les envois qualifiés par sujet.
- Mauvaises qualités :
  le comportement multi-compte reste difficile à raisonner quand le compte par défaut, les groupes locaux au compte, la réécriture de cible et les résumés de statut interagissent.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue de l'assurance qualité en direct et le nombre de tests n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les docs archivées, la source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration de compte nommé, les cibles CLI/outil de message, les adaptateurs de répertoire, le statut de canal, la sortante à portée de compte.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une fixture de preuve multi-compte en direct documentée avec des journaux de démarrage expurgés.
- Ajouter une sortie de statut qui rend le compte par défaut, la source de jeton, la configuration de groupe locale au compte et la résolution de cible de sujet inspectables en un seul endroit.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente la sélection de compte par défaut multi-compte, les cibles CLI, les cibles de sujet de forum, les sondages, les portes d'action et le dépannage de statut/sonde.
- `/Users/kevinlin/code/openclaw/docs/cli/channels.md` couvre les surfaces CLI de canal.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/accounts.ts` résout les ID de compte sélectionnés, le repli de compte par défaut, les sources de jeton et les portes d'action.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/account-selection.ts` et `/Users/kevinlin/code/openclaw/extensions/telegram/src/account-config.ts` possèdent la sélection de compte et le comportement de fusion de configuration.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/targets.ts` et `/Users/kevinlin/code/openclaw/extensions/telegram/src/outbound-params.ts` analysent les cibles de chat, nom d'utilisateur et sujet.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/directory-config.ts` liste les pairs et groupes configurés.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/status.ts`, `/Users/kevinlin/code/openclaw/extensions/telegram/src/status-issues.ts` et `/Users/kevinlin/code/openclaw/extensions/telegram/src/channel.ts` exposent le statut et l'état du cycle de vie de la passerelle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-rtt-config.mjs` configure les cibles de compte/groupe Telegram pour la preuve RTT en direct.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-live-docker.sh` exerce les chemins chauds liés à l'ajout de canal de package installé, au docteur et au statut.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/accounts.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/account-inspect.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/targets.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/outbound-params.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/directory-contract.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/status.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/channel.gateway.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/action-threading.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Telegram multi account" --json`

Résultats :

- #61012 problème ouvert : jeton de compte par défaut ignoré pour les messages sortants.
- #82718 PR ouverte : clarifier la configuration de groupe locale au compte.
- #64609 problème ouvert : systemPrompt de groupe/sujet ignoré en raison d'une résolution de configuration multi-compte incohérente.
- #63380 PR ouverte : permettre `agentId` dans la configuration de compte pour le routage multi-compte.
- #79553 problème ouvert : le magicien écrase les identifiants dans les plugins multi-compte.

Requête :

`gitcrawl search openclaw/openclaw --query "channelSummary telegram" --json`

Résultats :

- #79797 problème ouvert : `status --json` channelSummary est vide pour un canal Telegram configuré actif.
- #82600 PR ouverte : appliquer l'activation automatique du plugin lors du chargement du registre de plugin CLI.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram multi account"`

Résultats :

- `clawtributors`, 2026-05-12 : la PR #80986 a été bloquée sur la preuve de démarrage multi-compte Telegram en direct.
- `Vincent <> Molty - The Crustacean Kabal`, 2026-05-08 : le résumé du responsable a listé le résolveur de jeton multi-compte Telegram et le routage de groupe comme des problèmes pressants.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram status channelSummary"`

Résultats :

- `[openclaw] openclaw`, 2026-03-16 : les commentaires d'examen ont décrit les régressions de résumé de statut pour les configurations de canal uniquement env telles que `TELEGRAM_BOT_TOKEN`.
- `models anthropic not working`, 2026-02-17 : l'exemple de sortie de statut incluait un résumé de canal Telegram configuré avec la source de jeton.
