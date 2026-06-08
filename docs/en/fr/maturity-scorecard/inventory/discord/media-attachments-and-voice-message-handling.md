---
title: "Discord - Note de maturité des médias et du contenu enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Note de maturité des médias et du contenu enrichi

## Résumé

La gestion des médias Discord est large et activement maintenue : les téléchargements de fichiers normaux, les blocs de fichiers de composants, les blocs de galerie multimédia, la division des légendes vidéo et les téléchargements de messages vocaux Discord ont tous des chemins source explicites et une couverture unitaire ciblée. La couverture est Beta car la preuve localisée est principalement des tests d'adaptateur/runtime plus des preuves de canal de version, et non une preuve de scénario Discord en direct répétée pour toutes les formes de médias. La qualité est Beta car les contrats source sont clairs et la posture de sécurité est raisonnable, mais l'historique d'archive montre toujours les régressions de livraison de médias comme une préoccupation active de version.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Médias et contenu enrichi`
- Fusionnée à partir de : `Livraison de messages et de médias`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Envois directs et de threads : Couvre les envois directs et de threads dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes.
- Division de texte et mode de réponse : Couvre la division de texte et le mode de réponse dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes.
- Brouillons et éditions de progression : Couvre les brouillons et éditions de progression dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes.
- Rendu des mentions et des intégrations : Couvre le rendu des mentions et des intégrations dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes.
- Nouvelle tentative REST et livraison finale : Couvre la nouvelle tentative REST et la livraison finale dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes.
- Téléchargements de fichiers : Téléchargements de fichiers sortants à partir d'URL et de chemins locaux, y compris les contraintes de livraison et le comportement de suivi.
- Blocs de fichiers de composants et galeries multimédia : Blocs de fichiers et de galeries multimédia de composants v2 pour la livraison de médias Discord.
- Suivi de légende vidéo : Gestion des légendes vidéo et livraison de suivi réservée aux médias dans les conversations Discord.
- Téléchargement de messages vocaux : Envois de messages vocaux Discord avec conversion OGG/Opus, génération de forme d'onde, métadonnées de durée et gestion d'URL de téléchargement.
- Contexte de pièce jointe entrante : Contexte de pièce jointe entrante mis à disposition pour les réponses Discord et les tours d'agent.
- Envois directs et de threads : Couvre les envois directs et de threads dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes
- Division de texte et mode de réponse : Couvre la division de texte et le mode de réponse dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes
- Brouillons et éditions de progression : Couvre les brouillons et éditions de progression dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes
- Rendu des mentions et des intégrations : Couvre le rendu des mentions et des intégrations dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes
- Nouvelle tentative REST et livraison finale : Couvre la nouvelle tentative REST et la livraison finale dans Cette note évalue le chemin de message sortant Discord : envois directs, réponses de threads, division de texte, suivi de médias et comportement de rendu et de livraison de messages sortants connexes
- Téléchargements de fichiers : Téléchargements de fichiers sortants à partir d'URL et de chemins locaux, y compris les contraintes de livraison et le comportement de suivi
- Blocs de fichiers de composants et galeries multimédia : Blocs de fichiers et de galeries multimédia de composants v2 pour la livraison de médias Discord
- Gestion des légendes vidéo et livraison de suivi réservée aux médias : Portée des preuves pour la gestion des légendes vidéo et la livraison de suivi réservée aux médias
- Envois de messages vocaux Discord avec conversion OGG/Opus : Couvre les envois de messages vocaux Discord avec conversion OGG/Opus, comportement de génération de forme d'onde.
- Comportement de débounce conscient des médias/pièces jointes entrantes : Portée des preuves pour le comportement de débounce conscient des médias/pièces jointes entrantes
- Conversations en temps réel dans les canaux vocaux : Couvre les conversations en temps réel dans les canaux vocaux, qui sont évaluées dans le comportement séparé.
- Livraison générale réservée au texte : Couvre la livraison générale réservée au texte, l'autorisation de rappel de composant et le comportement de canal.

## Fonctionnalités

- Médias et contenu enrichi : Portée des preuves pour les médias et le contenu enrichi.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs :
  - La documentation couvre les blocs de fichiers de composants, les références de pièces jointes, les blocs de galerie multimédia et le comportement de remplacement de nom de fichier.
  - La documentation couvre les contraintes des messages vocaux Discord : chemin de fichier local uniquement, pas de contenu textuel, conversion OGG/Opus, aperçu de forme d'onde et dépendance `ffmpeg`/`ffprobe`.
  - La source a un chemin de médias sortants partagé qui charge les médias via le SDK du plugin, résout les noms de fichiers, crée des charges utiles de fichiers Discord multipartites, préserve les cibles de réponse et envoie des blocs de texte de suivi après la première légende de média.
  - La source a un chemin dédié aux messages vocaux pour le rejet d'URL/protocole avant ffmpeg/ffprobe, normalisation OGG/Opus 48 kHz, génération de forme d'onde, négociation d'URL de téléchargement Discord, analyse des limites de débit et demandes de téléchargement protégées par SSRF.
  - Les tests unitaires couvrent les contraintes de conversion de messages vocaux, la nouvelle tentative de téléchargement vocal sur les limites de débit, le routage `audioAsVoice`, la préservation des réponses pour les envois vocaux, la division des légendes vidéo, le transfert d'accès aux médias de composants et la gestion des blocs de fichiers de composants.
- Signaux négatifs :
  - Les preuves Discord QA en direct localisées ne prouvent pas chaque forme de média de bout en bout par rapport à Discord réel : téléchargement de fichier normal, bloc de fichier de composant, galerie multimédia, limite de média volumineux, légende vidéo et téléchargement de message vocal.
  - Gitcrawl n'a pas retourné un cluster de problèmes ciblé pour les requêtes de médias Discord, mais les rapports de version Discrawl et de rattrapage des responsables appellent toujours les régressions de livraison de messages/médias une zone chaude.
  - La gestion des pièces jointes entrantes est présente pour le débounce et le contexte, mais la preuve localisée est au niveau source et des tests ciblés plutôt qu'une preuve en direct de pièce jointe entrante vers agent.
- Lacunes d'intégration :
  - Ajouter Discord QA en direct pour envoyer une image, un document, une vidéo avec légende, un bloc de fichier de composant, une galerie multimédia et un message vocal.
  - Ajouter un scénario de chemin d'échec Discord réel pour les médias surdimensionnés et les chemins de messages vocaux locaux invalides.
  - Ajouter une preuve en direct entrante que les fichiers joints et les médias de type message vocal entrent dans le contexte de l'agent avec la provenance et les limites de confidentialité attendues.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl :
  - `gitcrawl search issues 'discord media OR discord attachment OR discord voice message OR discord transcribe OR discord audio' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` a retourné le problème ouvert #40078, "Transcription de préflight silencieuse dans les canaux requireMention", qui est adjacent au comportement de préflight média/audio.
  - `gitcrawl search issues '"failed-silent media" OR "media replies" OR "voice message" OR "audioAsVoice" OR "Discord voice message"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` n'a retourné aucun problème ciblé.
  - `gitcrawl search issues '"Discord" "media" OR "Discord" "attachment" OR "Discord" "voice" OR "media reply" OR "failed-silent"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 40` n'a retourné aucun problème ciblé.
- Rapports Discrawl :
  - `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord voice message"` a retourné une discussion de version récente demandant aux testeurs d'exercer la voix Discord et mettant en avant les améliorations du sélecteur de voix/modèle Discord.
  - `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord media"` a retourné les notes de version pour 2026.5.26 indiquant que le polissage des canaux incluait les correctifs de groupe/médias WhatsApp et les correctifs de voix/sélecteur de modèle/légende/proxy Discord, plus les améliorations du pipeline de médias via Rastermill.
  - `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "failed silent media replies Discord"` a retourné une note de rattrapage du responsable indiquant que les régressions de livraison de messages/médias/génération en double restaient chaudes et mentionnaient spécifiquement les réponses de médias silencieuses échouées.
  - `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "discord attachment"` a retourné une discussion générale sur les pièces jointes/confidentialité et les notes de version qui regroupaient la fiabilité des canaux et le travail de provenance des médias.
- Bonnes qualités :
  - Le chargement des médias est centralisé via les assistants de médias du SDK du plugin, ce qui maintient l'accès aux chemins locaux et les limites d'octets en dehors des lectures de fichiers Discord ad hoc.
  - La conversion des messages vocaux rejette les entrées d'URL/protocole avant de transmettre les chemins à ffmpeg/ffprobe et met en scène la sortie ffmpeg via un assistant d'écriture sécurisé.
  - Le téléchargement de messages vocaux utilise des récupérations protégées par SSRF pour les URL de téléchargement de pièces jointes Discord et analyse les réponses de limite de débit dans la forme d'erreur de limite de débit Discord partagée.
  - La documentation est explicite sur les contraintes des messages vocaux Discord qui surprennent couramment les opérateurs : chemin local uniquement et pas de contenu textuel simultané.
  - Les pièces jointes de fichiers de composants utilisent le modèle de référence `attachment://` de Discord au lieu de deviner silencieusement quel fichier multimédia un composant doit rendre.
- Mauvaises qualités :
  - Les notes de version/archive récentes traitent toujours la livraison de médias comme une classe de régression chaude, donc l'implémentation n'est pas encore opérationnellement ennuyeuse.
  - Les messages vocaux dépendent de `ffmpeg` et `ffprobe` hôtes ; la documentation explique la dépendance, mais les modes d'échec des opérateurs restent plus fragiles que les envois de fichiers ordinaires.
  - La preuve en direct pour les médias de composants, les légendes vidéo et le téléchargement de messages vocaux n'est pas encore visible dans l'ensemble de scénarios Discord maintenu.
- Exclu de la qualité :
  - La présence ou l'absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent l'étendue de la taxonomie pour les médias et le contenu enrichi.
- Signaux négatifs : la note archivée antérieure à la version 3 du processus de score de complétude, ce score est donc initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Construire une matrice de scénarios médias Discord en direct maintenue couvrant les envois de fichiers, images, vidéos, fichiers de composants, galeries médias et messages vocaux.
- Ajouter une preuve de pièce jointe/média entrante pour le contexte du modèle et la provenance.
- Améliorer les diagnostics visibles par l'opérateur pour ffmpeg/ffprobe manquants et les sources de messages vocaux distants rejetées.
- Maintenir les régressions de livraison de médias visibles dans la preuve de scénario de version jusqu'à ce que le trafic d'archive cesse de les traiter comme critiques.

## Preuves

### Docs

- `docs/channels/discord.md:320` indique que les forums Discord et les canaux médias n'acceptent que les publications de threads et documentent les chemins de création de threads.
- `docs/channels/discord.md:347` répertorie les blocs de composants pris en charge, y compris `media-gallery` et `file`.
- `docs/channels/discord.md:359` documente les blocs de fichiers, les références `attachment://<filename>`, `media`/`path`/`filePath` et les remplacements de noms de fichiers.
- `docs/channels/discord.md:1501` documente les messages vocaux Discord, la conversion OGG/Opus, la génération de formes d'onde, l'entrée de chemin local uniquement, aucun contenu textuel et `asVoice=true`.
- `docs/channels/discord.md:1719` répertorie `mediaMaxMb` comme le plafond de téléchargement Discord sortant.

### Source

- `extensions/discord/src/send.shared.ts:375` charge les médias sortants avec `loadWebMedia` et les options d'accès aux médias du SDK.
- `extensions/discord/src/send.shared.ts:379` résout les noms de fichiers de téléchargement à partir du nom de fichier explicite, des métadonnées médias, de l'extension MIME ou d'une valeur par défaut.
- `extensions/discord/src/send.shared.ts:400` construit une demande de message Discord avec du texte, des composants, des intégrations, des drapeaux, une cible de réponse et une charge utile de fichier multipart.
- `extensions/discord/src/send.shared.ts:413` envoie le premier message média, puis envoie les chunks de texte non vides après la légende du média.
- `extensions/discord/src/voice-message.ts:200` rejette les entrées de messages vocaux URL/protocole avant ffmpeg/ffprobe.
- `extensions/discord/src/voice-message.ts:211` accélère les fichiers OGG uniquement lorsque ffprobe confirme Opus à 48 kHz.
- `extensions/discord/src/voice-message.ts:241` convertit les autres fichiers audio en OGG/Opus 48 kHz via une exécution ffmpeg bornée.
- `extensions/discord/src/voice-message.ts:270` calcule les métadonnées de durée et de forme d'onde.
- `extensions/discord/src/voice-message.ts:322` demande les URL de téléchargement de pièces jointes Discord pour les fichiers de messages vocaux.
- `extensions/discord/src/monitor/message-handler.ts:152` traite les messages entrants avec des pièces jointes ou des autocollants comme porteurs de médias pour les décisions de débounce.

### Tests d'intégration

- `extensions/qa-lab/src/mantis/discord-smoke.runtime.ts` définit un runtime de fumée Discord en direct, mais l'ensemble de scénarios situé est plus large et orienté canal/voix et ne prouve pas chaque forme de média dans ce composant.
- Aucun test en direct/e2e situé ne prouve les blocs de fichiers de composants, les téléchargements de galeries médias, le rejet de médias volumineux, la division de légende vidéo et le téléchargement de messages vocaux par rapport à Discord réel dans un scénario maintenu.

### Tests unitaires

- `extensions/discord/src/outbound-adapter.test.ts:310` couvre le routage `audioAsVoice` via l'assistant d'envoi vocal Discord plus les envois médias de suivi.
- `extensions/discord/src/outbound-adapter.test.ts:363` et `extensions/discord/src/outbound-adapter.test.ts:388` couvrent la préservation des réponses pour les charges utiles de messages vocaux.
- `extensions/discord/src/outbound-adapter.test.ts:413` couvre les légendes vidéo envoyées en tant que texte avant un suivi vidéo médias uniquement.
- `extensions/discord/src/send.components.test.ts:262` couvre le transfert d'accès aux médias vers le chemin d'envoi Discord classique.
- `extensions/discord/src/send.components.test.ts:373` couvre les blocs de fichiers spoiler restant sur le chemin du composant.
- `extensions/discord/src/voice-message.test.ts:75` couvre le rejet des entrées de messages vocaux URL/protocole.
- `extensions/discord/src/voice-message.test.ts:82` et `extensions/discord/src/voice-message.test.ts:105` couvrent le chemin rapide OGG/Opus et le comportement de réencodage 48 kHz.
- `extensions/discord/src/voice-message.test.ts:189` couvre le comportement de nouvelle tentative de téléchargement vocal lorsque le téléchargement CDN est limité en débit.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues 'discord media OR discord attachment OR discord voice message OR discord transcribe OR discord audio' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`

Résultats :

- Retourné ouvert #40078, « Silent preflight transcription in requireMention channels », une demande de préflight audio/média adjacente plutôt qu'une défaillance de média sortant directe.

Requête :

- `gitcrawl search issues '"failed-silent media" OR "media replies" OR "voice message" OR "audioAsVoice" OR "Discord voice message"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`

Résultats :

- Aucun problème ciblé retourné.

Requête :

- `gitcrawl search issues '"Discord" "media" OR "Discord" "attachment" OR "Discord" "voice" OR "media reply" OR "failed-silent"' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 40`

Résultats :

- Aucun problème ciblé retourné.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord voice message"`

Résultats :

- Retourné une discussion récente de version/testeur appelant Discord voice comme une fonctionnalité à exercer et décrivant les correctifs de voix/sélecteur de modèle.

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord media"`

Résultats :

- Retourné les notes de version 2026.5.26 décrivant les améliorations plus larges du pipeline médias et les correctifs de voix/sélecteur de modèle/légende/proxy Discord.

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "failed silent media replies Discord"`

Résultats :

- Retourné une note de rattrapage du mainteneur disant que les régressions de livraison de messages/médias/génération en double restaient critiques et mentionnant les réponses médias silencieuses échouées.

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "discord attachment"`

Résultats :

- Retourné une discussion sur les pièces jointes/confidentialité et les notes de version référençant le travail de provenance des médias/fiabilité des canaux.
