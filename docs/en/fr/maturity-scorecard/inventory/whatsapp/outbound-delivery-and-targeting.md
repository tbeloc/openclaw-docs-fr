---
title: "WhatsApp - Note de Maturité de la Livraison et du Ciblage Sortants"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Note de Maturité de la Livraison et du Ciblage Sortants

## Résumé

La livraison et le ciblage sortants WhatsApp sont en Bêta. Le chemin principal documenté est large et soutenu par des sources, avec des vérifications d'écouteur actif, une normalisation des cibles, un chunking, des réponses citées, des accusés de livraison, des sondages, des réactions et un gating de chemin d'action. Il reste en dessous de Stable car la livraison dépend toujours d'un écouteur WhatsApp Web/Baileys actif et la recherche d'archive n'a pas ajouté de signal de champ actuel pour ce composant exact.

## Portée de la Catégorie

- Envois de texte sortants, livraison par outil de message, cibles explicites DM/groupe/infolettre, chunking, citation de réponse native, sondages, réactions, chemin d'action de fichier de téléchargement et comportement d'échec d'écouteur actif.
- Accusés de réception acceptés par le fournisseur et identifiants de livraison durables.
- Hors de portée : politique d'accès entrant, qualité de charge utile multimédia au-delà du routage sortant et sémantique de décision d'approbation native.

## Fonctionnalités

- Envois de texte sortants : Envois de texte sortants, livraison par outil de message, cibles explicites DM/groupe/infolettre
- Accusés de réception acceptés par le fournisseur : Accusés de réception acceptés par le fournisseur et identifiants de livraison durables

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Bêta (76%)`
- Signaux positifs : les tests de contrat couvrent le chunking sortant et les preuves de texte/replyTo durable-final ; les tests de style runtime exercent la livraison de moniteur, les drains de livraison en attente, les réponses chunked, la propagation de citation et l'autorisation de cible/action.
- Signaux négatifs : Gitcrawl et Discrawl n'ont pas surfacé de preuves de champ en direct actuel pour le chunking sortant, la citation, les cibles explicites ou les actions.
- Lacunes d'intégration : aucune preuve de livraison Baileys en direct actuelle ne couvre les chemins d'action DM, JID de groupe, JID d'infolettre, réponse citée, réaction, sondage et fichier de téléchargement en tant que matrice unique.

## Score de Qualité

- Score : `Bêta (78%)`
- Rapports Gitcrawl : `whatsapp outbound send target chunk quote newsletter` n'a retourné aucun résultat.
- Rapports Discrawl : `whatsapp outbound send target chunk quote newsletter` a retourné `null`.
- Bonnes qualités : la source échoue rapidement sans écouteur actif, normalise les cibles E.164/groupe/infolettre, préserve l'acceptation du fournisseur dans les accusés de réception, supporte les envois/réactions conscients du LID, assainit le texte visible et réessaye les échecs sortants réessayables.
- Mauvaises qualités : `@openclaw/whatsapp` dépend de Baileys `7.0.0-rc13`, la volatilité de la session WhatsApp Web reste une préoccupation de l'opérateur, les docs sous-estiment le chemin d'action `upload-file` complet et les charges utiles structurées uniquement sans texte/média sont explicitement rejetées.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et de flux runtime réel n'a pas augmenté ni diminué ce score de Qualité.

## Score de Complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les envois de texte sortants et les accusés de réception acceptés par le fournisseur.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une preuve en direct pour les envois DM, JID de groupe, JID d'infolettre, réponse citée, sondage, réaction et fichier de téléchargement.
- Améliorer les docs pour la surface d'action sortante complète, en particulier upload-file.
- Garder visible la sémantique acceptée par le fournisseur par rapport à livrée par le fournisseur dans le dépannage de l'opérateur.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:155` documente la portée WhatsApp Web/Baileys, la socket détenue par Gateway, l'exigence d'écouteur actif, les envois de groupe et les cibles d'infolettre.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:421` documente les limites de chunk de texte et `chunkMode`.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:455` documente les modes de citation de réponse native.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:584` documente les actions et les gates.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:669` documente le dépannage de l'écouteur actif et accepté par le fournisseur.

### Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/send.ts:47` nécessite un écouteur actif pour les envois sortants.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/send.ts:77` normalise le texte, résout les médias, utilise l'écouteur Baileys et enregistre les cibles de réaction d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/normalize-target.ts:70` normalise les cibles DM, groupe et infolettre.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/resolve-outbound-target.ts:17` résout les cibles sortantes conscientes de allowFrom.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-base.ts:144` déclare la livraison gateway, le chunking de 4000 caractères, le texte/replyTo durable, les sondages et la recherche de citation.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/send-api.ts:68` construit les charges utiles Baileys pour les options citées, les mentions, les accusés de livraison, les sondages et les réactions.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/package.json:10` épingle Baileys comme dépendance de transport sortant.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-payload.contract.test.ts:33` couvre les contrats de charge utile sortante et le chunking de 4000 caractères.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/outbound-payload.contract.test.ts:71` couvre les preuves de texte et replyTo durable-final.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.web-auto-reply.connection-and-logging.e2e.test.ts:269` couvre le drain de livraison en attente lors de la connexion.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.web-auto-reply.connection-and-logging.e2e.test.ts:939` couvre le traitement du moniteur des messages entrants directs dans la résolution de réponse.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/resolve-outbound-target.test.ts:103` couvre les cibles de groupe/infolettre et le comportement de allowFrom.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/deliver-reply.test.ts:245` couvre les réponses de texte chunked et les accusés de réception.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/deliver-reply.test.ts:363` couvre le threading de citation sur chaque chunk de texte.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/channel-react-action.test.ts:106` couvre l'autorisation d'action de fichier de téléchargement et le chemin d'envoi.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/action-runtime.test.ts:55` couvre l'ajout/suppression de réaction, le gating et le routage de compte.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/send-api.test.ts:408` couvre les sondages, les réactions, les envois non acceptés par le fournisseur, les envois d'infolettre et les JID distants cités.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp outbound send target chunk quote newsletter" --json`

Résultats :

- N'a retourné aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "WhatsApp outbound send target chunk quote reaction active listener Baileys" --json`

Résultats :

- N'a retourné aucun résultat.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp outbound send target chunk quote newsletter" --limit 5`

Résultats :

- A retourné `null`.

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "WhatsApp outbound send target chunk quote reaction active listener" --limit 5`

Résultats :

- A retourné `null`.
