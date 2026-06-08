---
title: "Telegram - Note de maturité des contrôles natifs et approbations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Note de maturité des contrôles natifs et approbations

## Résumé

Les boutons en ligne Telegram, les approbations exec et les actions de message sont importants et
utilisables, mais toujours en Beta. Le composant dispose de docs claires, de portes d'action, de
gestion des rappels, de boutons d'approbation en ligne, de contexte d'exécution d'approbation natif et d'actions d'outil de message pour envoyer/réagir/supprimer/modifier/autocollant/sujet/sondage. La qualité reste
limitée par les préoccupations concernant les rappels actifs, les approbations en double, la modification de médias, la gestion des actions et les opérateurs sensibles à la sécurité.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Contrôles natifs et approbations`
- Fusionnée à partir de : `Commandes et contrôles interactifs`
- Report du score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Rendu du clavier en ligne : rendu du clavier en ligne, gestion des requêtes de rappel, boutons URL Mini App et rappels d'approbation.
- Approbations exec en MP : approbations exec en MP, canaux, sujets ou les deux ; résolution des approbateurs ; plugin
- Actions de message : envoyer, sondage, réagir, supprimer, modifier, autocollant et actions de recherche d'autocollant.
- Découverte de capacité d'action : découverte de capacité d'action, configuration de gating, portes d'action à portée de compte et vérifications de confiance du demandeur.
- Synchronisation de démarrage setMyCommands natif : synchronisation de démarrage setMyCommands natif, commandes personnalisées, alias natifs, plugin
- Normalisation du nom/description de commande : normalisation du nom/description de commande, réduction du budget de menu, doublon
- Commandes intégrées : commandes intégrées telles que /help, /commands, /whoami, /status et interface utilisateur de commande associée.
- Autorisation de commande en MP : autorisation de commande en MP, groupes et commandes adressées à d'autres bots
- Boutons de modèle : boutons de modèle et assistants d'interface utilisateur de commande
- Synchronisation de démarrage `setMyCommands` natif : couvre la synchronisation de démarrage `setMyCommands` natif, les commandes personnalisées, les alias natifs et le comportement du plugin.
- Normalisation du nom/description de commande : couvre la normalisation du nom/description de commande, la réduction du budget de menu et le comportement en doublon.
- Commandes intégrées telles que `/help` : couvre le comportement des commandes intégrées telles que `/help`, `/commands`, `/whoami`, `/status`.
- Autorisation de commande en MP : couvre le comportement de l'autorisation de commande en MP, dans les groupes et les commandes adressées à d'autres bots.
- Boutons de modèle et assistants d'interface utilisateur de commande : portée de preuve pour les boutons de modèle et les assistants d'interface utilisateur de commande.

## Fonctionnalités

- Rendu du clavier en ligne : rendu du clavier en ligne, gestion des requêtes de rappel, boutons URL Mini App et rappels d'approbation.
- Approbations exec en MP : approbations exec en MP, canaux, sujets ou les deux ; résolution des approbateurs ; plugin
- Actions de message : envoyer, sondage, réagir, supprimer, modifier, autocollant et actions de recherche d'autocollant.
- Découverte de capacité d'action : découverte de capacité d'action, configuration de gating, portes d'action à portée de compte et vérifications de confiance du demandeur.
- Synchronisation de démarrage setMyCommands natif : synchronisation de démarrage setMyCommands natif, commandes personnalisées, alias natifs, plugin
- Normalisation du nom/description de commande : normalisation du nom/description de commande, réduction du budget de menu, doublon
- Commandes intégrées : commandes intégrées telles que /help, /commands, /whoami, /status et interface utilisateur de commande associée.
- Autorisation de commande en MP : autorisation de commande en MP, groupes et commandes adressées à d'autres bots
- Boutons de modèle : boutons de modèle et assistants d'interface utilisateur de commande

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs :
  les boutons en ligne, les types de boutons, les rappels d'approbation, les approbations exec, l'exécution d'action, les actions de message et le threading d'action ont des tests ciblés et des ancres source.
- Signaux négatifs :
  les enregistrements de preuve en direct enregistrent les métadonnées des boutons en ligne mais n'exercent pas complètement les clics d'approbation natifs, les combinaisons de gating d'action, les modifications de médias ou les actions de sujet.
- Lacunes d'intégration :
  ajouter une preuve en direct pour les cibles d'approbation MP/canal/les deux, les clics de rappel non autorisés, les accusés de réception de rappel en ligne, les actions de sujet et les actions de modification de message multimédia.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl :
  #64715, #76622, #76975, #74176, #70568, #75749, #86161 et #86176 montrent des travaux actifs
  ou ouverts autour des claviers, de l'accusé de réception de rappel, des approbations, de la livraison en double et des modifications de médias.
- Rapports Discrawl :
  la discussion de sécurité du responsable traite l'accès aux outils, le contexte d'invite et les
  approbations comme une zone de conception à rayon d'explosion élevé ; les notes de version appellent les approbations de rôle d'appareil non-administrateur et les réponses d'action Telegram durables.
- Bonnes qualités :
  les portes d'action sont conscientes du compte, la portée du bouton en ligne est configurable,
  les boutons d'approbation sont acheminés via le contexte d'exécution natif et les actions de message exposent des capacités explicites.
- Mauvaises qualités :
  le comportement d'approbation et d'action est sensible à la sécurité, les rappels peuvent être opaques pour les
  utilisateurs et la livraison en double/secours apparaît toujours dans l'historique d'archive.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue de l'assurance qualité en direct et le nombre de tests n'ont pas été
  utilisés comme entrées de qualité.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le rendu du clavier en ligne, les approbations exec en MP, les actions de message, la découverte de capacité d'action, la synchronisation de démarrage setMyCommands natif, la normalisation du nom/description de commande, les commandes intégrées, l'autorisation de commande en MP et les boutons de modèle.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuve` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario d'approbation natif en direct avec preuve de clic en ligne et comportement de clic expiré.
- Ajouter une matrice de support d'action Telegram générée couvrant les portes par défaut et les remplacements de compte.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente les boutons en ligne, les boutons Mini App, les actions de message, les portes d'action, le threading de réponse et les approbations exec.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md` est la référence des approbations exec liée.
- `/Users/kevinlin/code/openclaw/docs/tools/reactions.md` est liée pour la sémantique de suppression de réaction.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/inline-buttons.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/button-types.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/inline-keyboard.ts`
  implémentent la capacité et le rendu des boutons en ligne.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/approval-native.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/approval-handler.runtime.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/exec-approvals.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/exec-approval-forwarding.ts`
  implémentent l'acheminement des approbations et la gestion des approbations natifs.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/channel-actions.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/action-runtime.ts`
  implémentent la découverte et l'exécution des actions de message.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/action-threading.ts`
  résout les cibles d'action conscientes du thread.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/telegram/telegram-live.runtime.ts`
  capture les étiquettes de bouton en ligne et les types de médias dans les artefacts de message observés.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-live-runner.ts`
  exécute les scénarios en direct Telegram installés par paquet qui peuvent inclure des extensions d'action/approbation opt-in.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/inline-buttons.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/button-types.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/approval-native.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/approval-handler.runtime.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/exec-approvals.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/exec-approval-resolver.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/channel-actions.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/action-runtime.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/action-threading.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "inline keyboard" --json`

Résultats :

- #64715 problème ouvert : ajouter le support du clavier de réponse natif à la
  surface d'envoi de message/agent.
- #74176 PR ouvert : support des boutons URL Mini App.
- #76975 PR ouvert : autoriser le texte d'accusé de réception de rappel.
- #76622 problème ouvert : `answerCallbackQuery` appelé sans texte.
- #86161 problème ouvert et #86176 PR ouvert : comportement de modification de message multimédia.

Requête :

`gitcrawl search openclaw/openclaw --query "Telegram exec approvals" --json`

Résultats :

- #70568 PR ouvert : portée des approbations exec ambiguës à un compte.
- #61051 PR ouvert : flux d'acheminement du terminal administrateur Telegram.
- #75749 problème ouvert : messages en double d'approbation du plugin sur Telegram.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram inline button"`

Résultats :

- `clawtributors`, 2026-05-13 : la liste PR incluait le support du bouton web_app dans le
  clavier en ligne.
- `[openclaw] openclaw`, 2026-04-25 : le problème #63282 a été fermé après confirmation du
  support des requêtes de rappel.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram approval"`

Résultats :

- `releases`, 2026-05-28 : les notes de version ont appelé les approbations de rôle d'appareil non-administrateur et les réponses d'action Telegram durables.
- `maintainer-security-ops`, 2026-05-27 : la discussion a traité l'accès aux outils et le
  contexte d'invite comme une architecture sensible à la sécurité adjacente aux approbations.
