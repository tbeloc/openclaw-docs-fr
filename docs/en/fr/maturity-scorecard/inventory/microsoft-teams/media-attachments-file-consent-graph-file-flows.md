---
title: "Microsoft Teams - Note de maturité des médias et du contenu enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Note de maturité des médias et du contenu enrichi

## Résumé

La gestion des médias et des fichiers dans Teams est large mais encore fragile. La documentation et le code source couvrent les pièces jointes en MP, les téléchargements Graph de canal/groupe, le consentement aux fichiers, les solutions de secours Bot Framework, les téléchargements SharePoint, la solution de secours OneDrive, et les listes blanches d'hôte/authentification. La couverture et la qualité restent Alpha car les preuves d'archive actuelles incluent des défaillances silencieuses de pièces jointes et un correctif de sécurité DNS-rebinding récent pour les récupérations de pièces jointes Teams.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Media and Rich Content`
- Fusionnée à partir de : `Media and Files`
- Report du score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Pièces jointes entrantes : Couvre les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Médias hébergés par Graph : Couvre les médias hébergés par Graph, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Consentement aux fichiers : Couvre le consentement aux fichiers, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Partage SharePoint et OneDrive : Couvre le partage SharePoint et OneDrive, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Sécurité de la récupération de médias : Couvre la sécurité de la récupération de médias, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.

## Fonctionnalités

- Pièces jointes entrantes : Couvre les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Médias hébergés par Graph : Couvre les médias hébergés par Graph, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Consentement aux fichiers : Couvre le consentement aux fichiers, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Partage SharePoint et OneDrive : Couvre le partage SharePoint et OneDrive, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.
- Sécurité de la récupération de médias : Couvre la sécurité de la récupération de médias, les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph, et le comportement de partage de médias et de fichiers associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (62%)`
- Signaux positifs : La source et les tests couvrent le téléchargement direct, la solution de secours Graph, la solution de secours Bot Framework, le consentement aux fichiers, les téléchargements en attente, les chemins d'envoi SharePoint/OneDrive, les listes blanches d'hôte, les redirections, et la journalisation des erreurs.
- Signaux négatifs : Aucun scénario de téléchargement/téléchargement de médias/fichiers Teams en direct n'a été trouvé ; la documentation indique que les médias de canal/groupe nécessitent le consentement administrateur Graph et la configuration SharePoint.
- Lacunes d'intégration : Preuve de locataire réelle manquante pour les images en ligne MP, les pièces jointes de fichiers MP, le contenu hébergé par canal, les liens de partage SharePoint, les rappels de consentement aux fichiers, et les états de permission refusée.

## Score de qualité

- Score : `Alpha (58%)`
- Rapports Gitcrawl : `msteams attachment DM file.download.info Graph shares` a retourné le problème ouvert `#67177` et la PR `#85845` pour le routage des partages Graph `file.download.info` ; la recherche large a retourné `#87567` épinglage DNS de récupération de pièce jointe Teams.
- Rapports Discrawl : `Teams attachment` a retourné `#87567` discussion de sécurité DNS-rebinding, `#67177` défaillances silencieuses de pièces jointes de fichiers MP, `#65329` abandons d'images/fichiers en ligne MP, et commentaires sur l'authentification plus stricte et le comportement de redirection.
- Bonnes qualités : L'implémentation a plusieurs chemins de secours, des listes blanches d'hôte/authentification, des récupérations protégées SSRF, la persistance des téléchargements en attente, et une documentation explicite pour les exigences Graph/SharePoint.
- Mauvaises qualités : Les médias Teams réels dépendent des permissions Graph, de la configuration SharePoint, des particularités Bot Framework, et de la gestion d'URL sensible à la sécurité, et l'archive a des régressions actives.
- Exclu de la qualité : Nombre de tests unitaires de pièces jointes, étendue de l'intégration, et absence de tests de médias en direct.

## Score de complétude

- Score : `Alpha (62%)`
- Instructions de surface : évaluées par rapport à `references/completeness/microsoft-teams.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les pièces jointes entrantes, les médias hébergés par Graph, le consentement aux fichiers, le partage SharePoint et OneDrive, la sécurité de la récupération de médias.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des scénarios en direct pour les images en ligne MP, les fichiers MP, les images de canal, les fichiers de canal, le comportement désactivé Graph, le téléchargement SharePoint, l'acceptation/refus du consentement aux fichiers, les blocages de redirection, et le comportement de transfert d'authentification.
- Ajouter des erreurs visibles par l'opérateur lorsque les espaces réservés de médias Teams ne peuvent pas être résolus.
- Ajouter un scénario de régression de sécurité pour les tentatives de redirection privée/interne.

## Preuves

### Documentation

- `docs/channels/msteams.md` documente l'état actuel des médias, la division de capacité RSC uniquement par rapport à Graph, les exigences de médias/historique activés par Graph, les limitations de pièces jointes, les listes blanches d'hôte, le consentement aux fichiers MP, la configuration de téléchargement SharePoint de groupe/canal, le comportement de partage, le comportement de secours, et le dépannage.

### Source

- `extensions/msteams/src/attachments/download.ts` télécharge les pièces jointes Teams avec la gestion de la politique d'hôte/authentification et des partages Graph.
- `extensions/msteams/src/attachments/graph.ts` télécharge les médias hébergés par Graph.
- `extensions/msteams/src/attachments/bot-framework.ts` gère les récupérations de pièces jointes MP Bot Framework.
- `extensions/msteams/src/monitor-handler/inbound-media.ts` décide du comportement de secours direct, Graph et Bot Framework.
- `extensions/msteams/src/file-consent.ts`, `extensions/msteams/src/file-consent-invoke.ts`, et `extensions/msteams/src/file-consent-helpers.ts` implémentent le consentement aux fichiers et la gestion des téléchargements en attente.
- `extensions/msteams/src/graph-upload.ts` gère le comportement de téléchargement OneDrive/SharePoint et de lien de partage.
- `extensions/msteams/src/send.ts` sélectionne l'image base64, le consentement aux fichiers, SharePoint, ou les chemins de fichiers sortants OneDrive.

### Tests d'intégration

- Aucune voie e2e de médias ou fichiers Teams en direct n'a été trouvée par `rg`.
- Les preuves d'archive incluent des rapports d'utilisateurs réels mais pas un artefact de scénario en direct enregistré.

### Tests unitaires

- `extensions/msteams/src/attachments.test.ts`, `attachments.graph.test.ts`, `attachments/bot-framework.test.ts`, `attachments/remote-media.test.ts`, et `attachments/shared.test.ts` couvrent les chemins de téléchargement de médias, les redirections, les listes blanches, le transfert d'authentification, et les partages Graph.
- `extensions/msteams/src/monitor-handler/inbound-media.test.ts` couvre les déclencheurs de secours et le routage.
- `extensions/msteams/src/file-consent-helpers.test.ts`, `file-consent.test.ts`, `pending-uploads.test.ts`, et `pending-uploads-fs.test.ts` couvrent le consentement et l'état des téléchargements en attente.
- `extensions/msteams/src/send.test.ts` couvre le comportement d'envoi de médias sortants.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "msteams Teams file consent attachment media Graph upload download" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams attachment DM file.download.info Graph shares" --json --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams Microsoft Teams" --json --limit 10`

Résultats :

- La recherche de problème ciblée a retourné `[]`.
- La requête de partages Graph a retourné `#85845` et le problème `#67177` pour les liens Teams `file.download.info`.
- La recherche large a retourné `#87567`, "Pin Microsoft Teams attachment fetch DNS".

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Teams attachment"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams Teams file consent attachment media Graph"`

Résultats :

- `Teams attachment` a retourné `#87567` discussion de sécurité DNS-rebinding, `#67177` défaillance silencieuse de pièce jointe MP, `#65329` abandon d'image/fichier en ligne, et notes sur la redirection plus stricte et le transfert d'autorisation.
- La requête ciblée `msteams Teams file consent attachment media Graph` n'a retourné aucune ligne.
