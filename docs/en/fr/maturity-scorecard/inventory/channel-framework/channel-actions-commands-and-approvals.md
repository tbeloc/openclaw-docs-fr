---
title: "Cadre de canal - Note de maturité des commandes, actions de canal et approbations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Cadre de canal - Note de maturité des commandes, actions de canal et approbations

## Résumé

Les actions de canal, les commandes et les approbations sont implémentées mais encore en maturation. Le cadre dispose d'une autorisation de commande partagée, d'un ciblage de session de commande native, de capacités de plugin d'approbation, d'une distribution d'action de message, d'une découverte d'API d'outil de message, d'invites d'approbation natives au canal et de documents de fournisseur pour les réactions, les commandes slash, les boutons d'action et les clients d'approbation natifs.

La limite de maturité est la variance des capacités du fournisseur et l'UX sensible à la sécurité. Les preuves d'archive montrent un travail actif autour des approbations médiatisées par canal, des invites d'approbation natives, des composants Discord, des boutons en ligne Telegram, des cartes Feishu et du contexte d'approbation long format.

## Portée de la catégorie

Inclus dans cette catégorie :

- Commandes natives au canal : Commandes natives au canal et portes d'autorisation de commande
- Cible de session de commande native : Résolution de cible de session de commande native
- Actions de message : Actions de message, distribution d'action et vérifications du demandeur de confiance
- Découverte d'API d'outil de message : Découverte d'API d'outil de message pour les actions de canal
- Invites d'approbation natives au canal : Invites d'approbation natives au canal et routage d'approbation plugin/exec

## Fonctionnalités

- Commandes natives au canal : Commandes natives au canal et portes d'autorisation de commande
- Cible de session de commande native : Résolution de cible de session de commande native
- Actions de message : Actions de message, distribution d'action et vérifications du demandeur de confiance
- Découverte d'API d'outil de message : Découverte d'API d'outil de message pour les actions de canal
- Invites d'approbation natives au canal : Invites d'approbation natives au canal et routage d'approbation plugin/exec

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs :
  - Les documents couvrent le comportement des commandes slash natives, les composants de message Discord, les actions de réaction, les actions de téléchargement Google Chat, les approbations Signal/Matrix et les paramètres de commande/action spécifiques au fournisseur (`docs/channels/groups.md:106`, `docs/channels/discord.md:353`, `docs/channels/discord.md:1079`, `docs/channels/discord.md:1117`, `docs/channels/googlechat.md:216`, `docs/channels/signal.md:309`, `docs/channels/matrix.md:237`, `docs/channels/matrix.md:678`).
  - La source dispose de portes de commande partagées, de cibles de session de commande natives, de plomberie de capacité d'approbation, de distribution d'action de message, de découverte d'API d'outil de message et de détection de capacité d'invite d'approbation native.
  - La couverture unitaire existe pour les portes de commande, les cibles de session de commande natives, les approbations, les actions de message, la sécurité des actions de message et le comportement de l'API d'outil de message.
- Signaux négatifs :
  - Le support des capacités du fournisseur varie considérablement : tous les canaux n'ont pas de commandes natives, de boutons, de cartes, de réactions ou d'affordances d'invite d'approbation native.
  - L'UX d'approbation est sensible à la sécurité et le travail d'archive actif montre des raffinements en cours.
  - La preuve de couverture en direct est plus mince que la preuve source/unitaire pour les composants de canal natifs et les flux d'approbation.
- Lacunes d'intégration :
  - Aucune matrice de conformité d'action/approbation en direct pour tous les canaux n'a été trouvée.
  - Les chemins d'interface utilisateur natifs du fournisseur tels que les composants Discord, les boutons Telegram, les cartes Feishu, les événements d'approbation Matrix et les réactions Signal nécessitent une preuve en direct plus solide entre les canaux.

## Score de qualité

- Score : `Beta (72%)`
- Justification de la qualité :
  - L'autorisation de commande est explicitement contrôlée et peut utiliser des groupes d'accès.
  - La résolution de cible de commande native évite la dérive accidentelle de session en résolvant les cibles liées et routées.
  - La distribution d'action de message inclut des vérifications du demandeur de confiance, ce qui est important pour la sécurité de l'interface utilisateur du canal interactif.
  - La détection d'invite d'approbation native est basée sur les capacités plutôt que supposée pour chaque canal.
- Principaux risques de qualité :
  - Les affordances natives du fournisseur ont des modèles d'expiration, de permission, d'interaction et d'identité différents.
  - Les résultats d'archive montrent un travail actif sur le contexte d'approbation, les métadonnées et le support d'action spécifique au canal.
  - Les opérateurs ont besoin de documents plus clairs sur les canaux qui supportent quelles fonctionnalités d'action/approbation natives.
- Le score de qualité exclut la quantité de tests ; les tests sont enregistrés uniquement comme preuve de couverture.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/channel-framework.md`.
- Signaux positifs : les preuves d'archive, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les commandes natives au canal, la cible de session de commande native, les actions de message, la découverte d'API d'outil de message, les invites d'approbation natives au canal.
- Signaux négatifs : la note d'archive a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connus utilisés pour le score de couverture d'archive.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une matrice de support pour les commandes natives, les réactions, les boutons/composants/cartes, les actions de téléchargement, les approbations natives, les réactions d'approbation et les commandes slash de secours par canal.
- Ajouter la conformité en direct pour l'approbation autoriser/refuser, les rappels d'action obsolète, les tentatives d'action non autorisées et l'approbation de commande de secours.
- Exposer le statut de capacité d'action/approbation via `channels status`.

## Preuves

### Documents

- `docs/channels/groups.md:106` documente que les commandes slash natives contournent les réponses visibles uniquement pour les outils de message et répondent toujours visiblement.
- `docs/channels/discord.md:353` à `docs/channels/discord.md:355` documente les utilisateurs autorisés des boutons Discord et le TTL de rappel de composant.
- `docs/channels/discord.md:1079` à `docs/channels/discord.md:1101` documente les approbations exec natives Discord.
- `docs/channels/discord.md:1117` à `docs/channels/discord.md:1143` documente les capacités d'action de message Discord et les composants.
- `docs/channels/googlechat.md:216` à `docs/channels/googlechat.md:218` documente les réactions, `send`, `upload-file` et les indicateurs de saisie.
- `docs/channels/signal.md:286` à `docs/channels/signal.md:322` documente les réactions Signal et les réactions d'approbation.
- `docs/channels/matrix.md:237` à `docs/channels/matrix.md:239` documente le contenu d'invite d'approbation native Matrix ; `docs/channels/matrix.md:678` à `docs/channels/matrix.md:700` documente le routage d'approbation exec Matrix, les approbateurs, les raccourcis de réaction et les commandes slash de secours.
- `docs/channels/discord.md:1713` à `docs/channels/discord.md:1720` énumère les groupes de fonctionnalités de commande, streaming, média, retry et action config.

### Source

- `src/channels/command-gating.ts:8` à `src/channels/command-gating.ts:66` implémente les portes de commande et de contrôle-commande.
- `src/channels/native-command-session-targets.ts:12` à `src/channels/native-command-session-targets.ts:22` résout les cibles de session de commande native.
- `src/channels/plugins/approvals.ts:4` à `src/channels/plugins/approvals.ts:31` définit les formes de capacité d'approbation et d'adaptateur.
- `src/channels/plugins/message-action-dispatch.ts:5` à `src/channels/plugins/message-action-dispatch.ts:31` implémente les vérifications du demandeur de confiance et la distribution.
- `src/channels/plugins/message-tool-api.ts:16` à `src/channels/plugins/message-tool-api.ts:52` charge et décrit la découverte d'outil de message groupé.
- `src/channels/plugins/native-approval-prompt.ts:5` à `src/channels/plugins/native-approval-prompt.ts:43` vérifie les canaux d'approbation native connus et les capacités d'exécution.
- `src/channels/message/capabilities.ts:29` à `src/channels/message/capabilities.ts:56` dérive les exigences de livraison finales à partir des extras natifs du canal.

### Tests d'intégration

- `scripts/e2e/mcp-channels-docker-client.ts:254` à `scripts/e2e/mcp-channels-docker-client.ts:311` exerce la conversation de canal et le comportement en forme d'action de canal via le harnais Docker.
- `scripts/e2e/npm-onboard-channel-agent-docker.sh:184` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:201` vérifie les tours d'agent de base après la configuration du canal pour les canaux courants.
- Aucune suite de conformité d'action/approbation native en direct pour tous les canaux n'a été trouvée.

### Tests unitaires

- `src/channels/command-gating.test.ts:8` à `src/channels/command-gating.test.ts:99` couvre l'autorisation de commande et les portes de contrôle-commande.
- `src/channels/native-command-session-targets.test.ts:4` à `src/channels/native-command-session-targets.test.ts:34` couvre les cibles liées, les cibles routées et les clés de session en minuscules.
- `src/channels/plugins/approvals.test.ts` couvre le comportement de capacité/adaptateur d'approbation.
- `src/channels/plugins/message-actions.test.ts` couvre le comportement de distribution d'action de message.
- `src/channels/plugins/message-actions.security.test.ts` couvre la sécurité du demandeur d'action de message.
- `src/channels/plugins/message-tool-api.test.ts` couvre la découverte d'outil de message et le comportement de description.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "channel command approval native action" --json --limit 8`

Résultats :

- Problème retourné #85954 pour les invites d'approbation de corps attribué iMessage.
- Problème retourné #87486 pour les commentaires de métadonnées d'action d'approbation.
- Problème retourné #81864 pour les approbations de plugin en langage naturel.
- Problème retourné #81901 pour le contexte long format dans les approbations de plugin Telegram/Slack/Discord.
- Problème retourné #78308 pour les approbations MCP médiatisées par canal.
- Problème retourné #79832 pour les actions de carte Feishu non supportées.
- Problème retourné #81135 pour les boutons en ligne Telegram dans les invites de groupe.
- PR retournée #78813 pour les composants Discord `SendParams`.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channel command approval native action" --limit 8`

Résultats :

- Trouvé une note de version mentionnant le durcissement d'entrée d'exécution non sécurisé et le nettoyage de livraison de canal.
- Trouvé une discussion de mainteneur énumérant un ensemble de tests de contrat solide, incluant un cas de canal WeCom avec politique de groupe/DM, listes blanches de commande, livraison de média/fichier et un cas de pont de serveur d'application Codex pour le comportement de pont interactif Discord/Telegram.
