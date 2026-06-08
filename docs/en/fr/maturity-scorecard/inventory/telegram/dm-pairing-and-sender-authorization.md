---
title: "Telegram - Note de Maturité d'Accès et d'Identité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Note de Maturité d'Accès et d'Identité

## Résumé

L'appairage DM Telegram et l'autorisation de l'expéditeur sont suffisamment matures pour une utilisation régulière.
La documentation sépare explicitement l'appairage DM de l'autorisation de groupe, les ID d'expéditeur numériques sont mis en avant, et le code d'exécution utilise des assistants d'accès partagés plus la normalisation spécifique à Telegram. Cela reste en Beta sur la Qualité car la confusion des opérateurs autour des ID de propriétaire, des attentes d'appairage de groupe et des paramètres par défaut de liste blanche est toujours visible.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Access and Identity`
- Fusionnée à partir de : `Access and Conversation Routing`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Modes dmPolicy : appairage, liste blanche, ouvert et désactivé
- Approbation du code d'appairage : Approbation du code d'appairage, bootstrap du premier propriétaire et commands.ownerAllowFrom
- Normalisation de l'ID utilisateur Telegram numérique avec les préfixes telegram: et tg:
- allowFrom : allowFrom, groupAllowFrom, groupes d'accès et limites DM-versus-groupe
- DM non autorisé : DM non autorisé, groupe, commande, rappel et gestion des réactions
- Listes blanches de groupe : Listes blanches de groupe, groupPolicy, groupAllowFrom et gating par mention
- ID de chat négatif de supergroupe : ID de chat négatif de supergroupe et héritage de configuration de groupe/sujet
- Clés de session de sujet de forum : Clés de session de sujet de forum, message_thread_id, comportement du sujet Général et routage de sujet.
- Routage de sujet ACP : Liaison de sujet ACP et /acp spawn --thread
- Construction de clé de session : Construction de clé de session, correspondance de route de conversation et cible de réponse

## Fonctionnalités

- Modes dmPolicy : appairage, liste blanche, ouvert et désactivé
- Approbation du code d'appairage : Approbation du code d'appairage, bootstrap du premier propriétaire et commands.ownerAllowFrom
- Normalisation de l'ID utilisateur Telegram numérique avec les préfixes telegram: et tg:
- allowFrom : allowFrom, groupAllowFrom, groupes d'accès et limites DM-versus-groupe
- DM non autorisé : DM non autorisé, groupe, commande, rappel et gestion des réactions
- Listes blanches de groupe : Listes blanches de groupe, groupPolicy, groupAllowFrom et gating par mention
- ID de chat négatif de supergroupe : ID de chat négatif de supergroupe et héritage de configuration de groupe/sujet
- Clés de session de sujet de forum : Clés de session de sujet de forum, message_thread_id, comportement du sujet Général et routage de sujet.
- Routage de sujet ACP : Liaison de sujet ACP et /acp spawn --thread
- Construction de clé de session : Construction de clé de session, correspondance de route de conversation et cible de réponse

## Fraîcheur de l'Archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (80%)`
- Signaux positifs :
  L'accès DM, l'accès au groupe, l'autorisation de commande, la normalisation de l'expéditeur et la configuration du premier propriétaire ont une source et des tests ciblés.
- Signaux négatifs :
  La preuve en direct est centrée sur les scénarios de mention de groupe et de commande ; elle ne prouve pas à plusieurs reprises chaque appairage, bootstrap du premier propriétaire, groupe d'accès et branche de bot ouvert.
- Lacunes d'intégration :
  ajouter une preuve de version pour le premier appairage DM, le bootstrap du premier propriétaire, le DM en liste blanche uniquement, le mode bot ouvert public et les flux d'expéditeur non autorisé échoués.

## Score de Qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl :
  #7679, #84447, #81876, #11489, #41058 et #79111 montrent une demande continue pour des paramètres par défaut plus sûrs, des limites de débit, une UX d'appairage de groupe et des messages d'appairage plus clairs.
- Rapports Discrawl :
  la discussion du responsable pointe vers une refonte plus large de l'entrée de canal, et les commentaires du miroir Discord appellent toujours l'appairage de groupe Telegram comme une demande ouverte.
- Bonnes qualités :
  la documentation appelle la limite exacte d'autorisation DM versus groupe, l'exécution normalise les ID d'expéditeur et l'authentification de l'expéditeur de groupe n'hérite intentionnellement pas des approbations du magasin d'appairage DM.
- Mauvaises qualités :
  l'appairage reste facile à généraliser à outrance comme « autorisé partout », et l'intégration de groupe manque d'un flux d'approbation de notification de propriétaire.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue de l'assurance qualité en direct et le nombre de tests n'ont pas été utilisés comme entrées de Qualité.

## Score de Complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les modes dmPolicy, l'approbation du code d'appairage, la normalisation de l'ID utilisateur Telegram numérique avec telegram, allowFrom, DM non autorisé, les listes blanches de groupe, les ID de chat négatif de supergroupe, les clés de session de sujet de forum, le routage de sujet ACP, la construction de clé de session.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un flux d'appairage de groupe ou de notification de propriétaire si la direction du produit souhaite l'intégration de groupe sans modifications de configuration manuelle.
- Ajouter des diagnostics plus clairs lorsqu'un utilisateur est appairé pour DM mais bloqué dans un groupe.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente la politique DM, les ID utilisateur numériques, le bootstrap du propriétaire uniquement et la division d'autorisation DM/groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/pairing.md` est la référence d'appairage liée.
- `/Users/kevinlin/code/openclaw/docs/channels/access-groups.md` documente le comportement du groupe d'accès réutilisable.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.ts` évalue l'accès DM, l'accès au groupe, l'autorisation de commande et les faits d'accès avant la distribution.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/dm-access.ts` applique la politique DM Telegram.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-access.ts` et `/Users/kevinlin/code/openclaw/extensions/telegram/src/allow-from.ts` gèrent l'accès de l'expéditeur de groupe et la normalisation des ID.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/access-groups.ts` développe les entrées du groupe d'accès.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/setup-core.ts` fournit l'aide à la configuration et l'analyse de l'ID Telegram.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/telegram/telegram-live.runtime.ts` inclut le gating par mention, l'autorisation de commande et d'autres scénarios en direct de gating de commande de bot.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-rtt-config.mjs` écrit `groupPolicy`, `groupAllowFrom`, les ID de groupe et la configuration de groupe gated par mention pour le harnais RTT en direct.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/dm-access.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-access.base-access.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-policy.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.group-auth.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.session-meta.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-message-context.reactions.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Telegram pairing allowlist" --json`

Résultats :

- #7679 problème ouvert : Telegram devrait utiliser par défaut le mode liste blanche avec l'ID du propriétaire.
- #84447 problème ouvert : limite de débit DM entrant par expéditeur pour les politiques d'appairage/liste blanche de canal.
- #81876 problème ouvert : basculer automatiquement les paramètres par défaut DM de canal en liste blanche du propriétaire après le bootstrap du premier propriétaire.
- #11489 problème ouvert : flux d'appairage de groupe avec notification de propriétaire et mode lecture seule pour les groupes non configurés.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram allowlist pairing"`

Résultats :

- `maintainers`, 2026-05-07 : note de refonte d'entrée de canal listée politique DM, politique de groupe, `allowFrom`, `groupAllowFrom`, groupes d'accès et appairage comme politique dupliquée à consolider.
- `[openclaw] openclaw`, 2026-04-26 : le problème #41753 a été fermé après que les DM Telegram utilisant `dmPolicy: "pairing"` et `allowFrom` aient été couverts par l'autorisation de l'ID d'expéditeur numérique.
- `[openclaw] openclaw`, 2026-04-26 : le problème #11489 est resté ouvert car l'appairage de groupe reste absent.
