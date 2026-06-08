---
title: "Slack - Media and Rich Content Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Media and Rich Content Maturity Note

## Summary

La prise en charge des médias Slack comprend les téléchargements de fichiers privés entrants, les espaces réservés de fichiers, les écritures de magasin de médias, l'héritage des pièces jointes de racine de thread, la gestion multi-pièces jointes, `download-file`, les téléchargements sortants, les limites de téléchargement et la transmission image/vision. C'est la couverture Slack la plus faible car la voie d'assurance qualité Slack en direct n'exerce actuellement pas les fichiers/médias, et les preuves d'archive montrent des défaillances répétées des pièces jointes, des bogues d'authentification de téléchargement, des bogues de réhydratation des médias de thread et une confusion silencieuse de la livraison des médias.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Media and Rich Content`
- Fusionnée à partir de : `Message Delivery and Media`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Livraison sortante : Couvre la livraison sortante sur `message.send` livraison texte/bloc, réponses de thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Streaming : Couvre le streaming sur `message.send` livraison texte/bloc, réponses de thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Réactions : Couvre les réactions sur `message.send` livraison texte/bloc, réponses de thread, `replyBroadcast`, chunking et comportement de livraison sortante, streaming et réactions associés.
- Médias : Couvre les médias sur les fichiers Slack entrants, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Pièces jointes : Couvre les pièces jointes sur les fichiers Slack entrants, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Fichiers : Couvre les fichiers sur les fichiers Slack entrants, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.
- Vision : Couvre la vision sur les fichiers Slack entrants, téléchargement/authentification d'URL privée, limites de taille de médias, contexte de médias de démarreur de thread et comportement de médias, pièces jointes, fichiers et vision associés.

## Fonctionnalités

- Media and Rich Content : Portée des preuves pour Media and Rich Content.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs : Les tests unitaires/runtime couvrent la résolution des médias Slack entrants, l'authentification download-file, le routage upload-file, les vérifications de portée, les limites de médias, les métadonnées non-image et la gestion des médias de racine de thread.
- Signaux négatifs : La voie en direct Slack standard omet les médias, le téléchargement/téléchargement de fichiers, les multi-pièces jointes, PDF, vision image, rejet de surdimensionné et les scénarios d'héritage de médias de thread racine.
- Lacunes d'intégration : Ajouter des cas de médias en direct pour image, PDF, plusieurs fichiers, URL privées expirées, fichiers surdimensionnés, héritage de médias de thread racine, téléchargement sortant avec `thread_ts` et `download-file` via variantes user-token/bot-token.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : `#63905`, `#62792`, `#60335`, `#60353`, `#83165`, `#63588`, `#41657` et `#53932` montrent des problèmes actifs et récurrents de médias/téléchargement/thread.
- Rapports Discrawl : Les recherches de médias Slack spécifiques aux fonctionnalités n'ont retourné aucun message d'archive Discord récent ciblé, tandis que les discussions plus larges en miroir GitHub montrent la confusion de téléchargement/téléchargement de fichiers Slack et de configuration de portée manquante.
- Bonnes qualités : L'implémentation limite les téléchargements, continue le traitement quand une pièce jointe échoue, expose les ID de fichiers pour `download-file` et sépare les pièces jointes image des métadonnées de fichier/PDF générique.
- Mauvaises qualités : Les modes de défaillance des médias sont visibles par l'utilisateur et difficiles à diagnostiquer, les médias de démarreur de thread ont régressé auparavant, et les preuves en direct traînent le nombre de combinaisons de fichiers et de médias que les utilisateurs essaient réellement.
- Exclu de la qualité : Nombre de tests unitaires, largeur de voie en direct et profondeur d'intégration.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Media and Rich Content.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une voie de médias Slack en direct ou des scénarios optionnels pour les fichiers/PDF/images entrants, les multi-pièces jointes, le téléchargement sortant et `download-file`.
- Ajouter une copie plus claire orientée utilisateur quand le téléchargement d'URL privée Slack échoue ou qu'un seul espace réservé atteint l'agent.
- Ajouter une preuve de porte de version pour l'héritage de médias de thread racine et « ne pas réattacher les médias parents à chaque réponse ».

## Preuves

### Docs

- `docs/channels/slack.md` documente les pièces jointes entrantes, les fichiers texte/sortants, les cibles de livraison, la référence vision des pièces jointes, les types de médias pris en charge, l'héritage des pièces jointes de racine de thread, le comportement multi-pièces jointes, les limites de taille, les défaillances de téléchargement et les limites connues.
- `docs/channels/slack.md` lie la compréhension des médias et les références des outils PDF pour la gestion en aval.

### Source

- `extensions/slack/src/monitor/media.ts` gère la résolution des médias Slack entrants.
- `extensions/slack/src/file-reference.ts`, `extensions/slack/src/actions.ts` et `extensions/slack/src/send.ts` prennent en charge les références de fichiers, download-file et les téléchargements sortants.
- `extensions/slack/src/monitor/message-handler/prepare.ts` sélectionne les médias directs ou les médias de démarreur de thread et ajoute le contexte des médias aux tours.
- `extensions/slack/src/limits.ts` et `extensions/slack/src/media-types.ts` prennent en charge les limites de charge utile et la gestion des types.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` n'a pas de scénario de médias standard.
- `docs/concepts/qa-e2e-automation.md` indique que le manifeste QA SUT omet les portées/événements de réaction ; la liste des scénarios documentés manque également de couverture de médias.

### Tests unitaires

- `extensions/slack/src/monitor/media.test.ts`, `monitor/monitor.media.test.ts`, `media.runtime.ts` et `actions.download-file.test.ts` couvrent la résolution des médias et le comportement de téléchargement.
- `extensions/slack/src/action-runtime.test.ts` couvre `downloadFile`, `uploadFile`, le comportement media-before-blocks, l'autorisation de téléchargement de fichiers, les lectures user-token et le rejet de diffusion de réponse pour les téléchargements.
- `extensions/slack/src/send.upload.test.ts` et `outbound-payload.test.ts` couvrent le comportement de charge utile de téléchargement.
- `src/auto-reply/reply/get-reply-run.media-only.test.ts` couvre le contexte de réponse Slack media-only via le runtime de réponse partagée.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "slack media" --json`

Résultats :

- Retourné `#63905` les pièces jointes entrantes échouent dans le bac à sable du conteneur, `#62792` correction d'accès aux fichiers Slack, `#60335` les réponses de thread réattachent les médias parents, `#60353` ne jamais hydrater les médias de démarreur de thread pour les réponses de thread, `#83165` les exécutions longues semblent silencieuses quand la livraison des médias échoue partiellement, `#53932` préoccupation d'optimisation d'image, `#63588` authentification de téléchargement Slack et `#41657` demande de fonctionnalité de métadonnées de pièce jointe.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack media attachment download-file"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack file upload download auth missing_scope"`

Résultats :

- Les deux recherches spécifiques aux fonctionnalités n'ont retourné aucun message ciblé dans l'archive Discord.
- Les recherches de configuration associées ont retourné une discussion de support/téléchargement d'image Slack sur `files:read`, `files:write`, réinstallation de portée bot-token et diagnostic de portée manquante.
