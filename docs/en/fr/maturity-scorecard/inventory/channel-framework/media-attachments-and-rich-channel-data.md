---
title: "Cadre de canal - Note de maturité des pièces jointes multimédias et des données de canal enrichies"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Cadre de canal - Note de maturité des pièces jointes multimédias et des données de canal enrichies

## Résumé

Les médias, les pièces jointes et les données de canal enrichies partagent un cadre commun, mais la maturité est inégale entre les fournisseurs. Le code principal normalise les médias entrants, construit les charges utiles multimédias, résout les racines multimédias entrantes, prend en charge les adaptateurs sortants directs texte/média et expose le contexte de localisation ; la documentation des fournisseurs documente les capacités multimédias, les téléchargements de fichiers, les charges utiles enrichies, les réactions, les sondages, la localisation et les notes vocales.

La limite de maturité est la variance des fournisseurs et les modes de défaillance. Certains canaux offrent un support riche, tandis que les preuves d'archive montrent des problèmes récents autour des directives multimédias sortantes, des délais d'expiration de téléchargement multimédias LINE, des notes vocales Matrix avant les portes de mention et la compatibilité de téléchargement de fichiers spécifique au canal.

## Portée de la catégorie

Inclus dans cette catégorie :

- Normalisation des médias entrants : Normalisation des médias entrants, persistance des pièces jointes et contexte des médias historiques
- Envois directs texte/média sortants : Envois directs texte/média sortants et support d'adaptateur de charge utile enrichie
- channelData spécifique au fournisseur : channelData spécifique au fournisseur, réponses rapides, localisations, sondages, réactions et gestion des notes vocales
- Racines multimédias : Racines multimédias et sécurité des chemins de fichiers pour le stockage entrant du canal

## Fonctionnalités

- Normalisation des médias entrants : Normalisation des médias entrants, persistance des pièces jointes et contexte des médias historiques
- Envois directs texte/média sortants : Envois directs texte/média sortants et support d'adaptateur de charge utile enrichie
- channelData spécifique au fournisseur : channelData spécifique au fournisseur, réponses rapides, localisations, sondages, réactions et gestion des notes vocales
- Racines multimédias : Racines multimédias et sécurité des chemins de fichiers pour le stockage entrant du canal

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs :
  - La documentation des fournisseurs couvre les médias et les données enrichies pour LINE, Signal, Google Chat, Matrix, Discord et autres canaux (`docs/channels/line.md:160`, `docs/channels/line.md:165`, `docs/channels/line.md:216`, `docs/channels/signal.md:233`, `docs/channels/signal.md:275`, `docs/channels/googlechat.md:217`, `docs/channels/matrix.md:10`, `docs/channels/discord.md:1503`).
  - La source partagée couvre la normalisation des médias entrants, la construction de charges utiles multimédias, les racines entrantes, les envois directs texte/média sortants, le formatage de localisation et la dérivation de capacité de livraison.
  - La couverture unitaire existe pour les médias entrants, les adaptateurs sortants directs texte/média, les capacités de message, les reçus de pont sortants et les assistants de localisation.
- Signaux négatifs :
  - Il n'existe pas de document de contrat multicanal unique qui indique aux opérateurs quels canaux prennent en charge les téléchargements entrants, les téléchargements sortants, les cartes enrichies, les réactions, les sondages et les localisations.
  - Les preuves d'archive montrent des régressions et des délais d'expiration spécifiques au fournisseur.
  - Les preuves d'intégration sont présentes mais pas assez larges pour prouver le comportement des médias sur tous les canaux enrichis.
- Lacunes d'intégration :
  - Aucune matrice multicanal complète n'a été trouvée pour les cas de téléchargement de fichiers entrants, de téléchargement sortant, de localisation, de réaction, de sondage et de note vocale.
  - Les contraintes de sécurité multimédias sont implémentées dans la source/documentation des fournisseurs, mais les preuves en direct ne sont pas uniformes.

## Score de qualité

- Score : `Beta (70%)`
- Justification de la qualité :
  - Les abstractions principales sont appropriément conservatrices : les médias sont normalisés avant le contexte de l'agent, les racines locales/distantes sont résolues de manière centralisée et les adaptateurs multimédias directs appliquent les limites d'octets et la gestion des résultats.
  - La documentation des fournisseurs appelle les contraintes de sécurité telles que les exigences HTTPS publiques et le rejet de réseau loopback/privé pour les médias sortants LINE.
  - Le support de charge utile enrichie est explicite via `channelData` spécifique au canal, ce qui évite de forcer tous les fournisseurs dans une forme de plus petit dénominateur commun.
- Principaux risques de qualité :
  - Le contrat visible par l'utilisateur est fragmenté par fournisseur.
  - Les fonctionnalités de données enrichies dépendent fortement de l'implémentation spécifique à l'adaptateur et des limites de l'API du fournisseur.
  - Les défaillances multimédias peuvent être tardives et spécifiques au fournisseur, ce qui les rend plus difficiles à diagnostiquer à partir du statut du canal commun.
- La notation de qualité exclut la quantité de tests ; les tests sont enregistrés uniquement comme preuves de couverture.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/channel-framework.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la normalisation des médias entrants, les envois directs texte/média sortants, le channelData spécifique au fournisseur, les racines multimédias.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une matrice de support générée pour les médias entrants, les médias sortants, les pièces jointes, les réactions, les sondages, les localisations et les cartes enrichies par canal.
- Ajouter la conformité en direct/média pour les chemins représentatifs de téléchargement entrant, de téléchargement sortant, de rejet de fichier surdimensionné et d'envoi de charge utile enrichie.
- Afficher les raisons de défaillance multimédias sous une forme diagnostique commune entre les adaptateurs.

## Preuves

### Docs

- `docs/channels/line.md:14` à `docs/channels/line.md:15` documente les messages directs LINE, les chats de groupe, les médias, les localisations, les messages Flex, les messages de modèle, les réponses rapides, les réactions et les threads.
- `docs/channels/line.md:160` à `docs/channels/line.md:167` documente les limites de téléchargement multimédias, la persistance du magasin multimédia partagé et les messages enrichis `channelData.line`.
- `docs/channels/line.md:216` à `docs/channels/line.md:226` documente les images sortantes, les vidéos, l'audio, la validation d'URL et le comportement de secours.
- `docs/channels/signal.md:233` à `docs/channels/signal.md:240` documente les envois Signal, les réceptions, les pièces jointes, les indicateurs de saisie, les reçus de lecture/visualisation, les réactions, les groupes, le texte stylisé et les limites d'octets multimédias.
- `docs/channels/signal.md:275` à `docs/channels/signal.md:307` documente les pièces jointes de notes vocales, les limites multimédias, la saisie/lecture des reçus et les outils de réaction.
- `docs/channels/googlechat.md:217` à `docs/channels/googlechat.md:219` documente les actions de message pour l'envoi/téléchargement de fichier et les téléchargements de pièces jointes via l'API Chat.
- `docs/channels/matrix.md:10` documente le support Matrix pour les DM, les salles, les threads, les médias, les réactions, les sondages, la localisation et E2EE.
- `docs/channels/matrix.md:231` à `docs/channels/matrix.md:277` documente les réponses multimédias, les charges utiles d'approbation et le comportement des miniatures d'images chiffrées.
- `docs/channels/discord.md:1503` à `docs/channels/discord.md:1510` documente les exigences de fichier de message vocal Discord et l'exemple d'outil de message sortant.

### Source

- `src/channels/inbound-event/media.ts:39` à `src/channels/inbound-event/media.ts:92` normalise les médias entrants, les médias historiques et les charges utiles multimédias.
- `src/channels/plugins/media-payload.ts:15` à `src/channels/plugins/media-payload.ts:33` construit des charges utiles multimédias partagées pour les plugins.
- `src/channels/plugins/outbound/direct-text-media.ts:36` à `src/channels/plugins/outbound/direct-text-media.ts:157` implémente les adaptateurs sortants directs texte/média avec résolution de limite d'octets et gestion d'envoi.
- `src/channels/location.ts:1` à `src/channels/location.ts:71` définit les types de localisation, le formatage de texte et l'extraction de contexte.
- `src/media/channel-inbound-roots.ts:20` à `src/media/channel-inbound-roots.ts:109` résout l'API de contrat multimédia, les racines entrantes locales et les racines distantes.
- `src/channels/message/capabilities.ts:29` à `src/channels/message/capabilities.ts:56` dérive les exigences de livraison finale durables à partir des charges utiles et des extras natifs du canal.
- `src/channels/message/outbound-bridge.ts:108` à `src/channels/message/outbound-bridge.ts:195` enveloppe le comportement de charge utile enrichie, de sondage et de reçu des gestionnaires sortants.

### Tests d'intégration

- `scripts/e2e/mcp-channels-docker-client.ts:311` exerce le comportement en forme de pièce jointe dans le harnais de canal MCP.
- `scripts/e2e/npm-onboard-channel-agent-docker.sh:184` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:201` prouve que l'agent de canal se tourne après la configuration pour les canaux courants, mais pas une matrice multimédia enrichie.
- Aucune matrice multimédia en direct pour tous les canaux n'a été trouvée dans cette passe d'audit.

### Tests unitaires

- `src/channels/inbound-event/media.test.ts` couvre la normalisation des médias entrants et le comportement de charge utile historique/média.
- `src/channels/plugins/outbound/direct-text-media.test.ts` couvre le comportement de l'adaptateur sortant direct texte/média.
- `src/channels/location.test.ts` couvre le formatage de localisation et les assistants de contexte.
- `src/media/channel-inbound-roots.fast-path.test.ts` couvre les chemins rapides de résolution des racines multimédias entrantes.
- `src/channels/message/outbound-bridge.test.ts:108` à `src/channels/message/outbound-bridge.test.ts:195` couvre l'enveloppe de charge utile enrichie et de reçu de sondage.
- `src/channels/message/capabilities.test.ts:12` à `src/channels/message/capabilities.test.ts:43` couvre les exigences de livraison dépendantes de la charge utile et les extras natifs du canal.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "channel media attachments rich channelData location" --json --limit 8`

Résultats :

- N'a retourné aucun résultat, ce qui est neutre après les vérifications de fraîcheur pour la requête exacte multicanal.

Requête : `gitcrawl search openclaw/openclaw --query "WhatsApp media attachment download channel" --json --limit 8`

Résultats :

- A retourné des résultats PR/problème incluant les notes vocales Matrix avant la porte de mention (#78069), la directive MEDIA sortante en texte brut au lieu d'un bloc de contenu (#83584) et le délai d'expiration de téléchargement multimédia LINE entrant (#86873).

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channel media attachments rich channelData location" --limit 8`

Résultats :

- A retourné null, ce qui est neutre après les vérifications de fraîcheur pour cette requête exacte.

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "WhatsApp media attachment download channel" --limit 8`

Résultats :

- A trouvé une discussion sur le format de sortie Microsoft TTS pour la compatibilité des messages vocaux.
- A trouvé la discussion PR #52801 autour des téléchargements de préflight multimédias à vue unique consommant des URL.
- A trouvé une discussion utilisateur selon laquelle `/hooks/agent` ne pouvait pas télécharger un fichier directement tandis que les adaptateurs de canal gèrent les médias entrants, soutenant le besoin de contrats multimédias appartenant à l'adaptateur.
