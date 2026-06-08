---
title: "Compréhension des médias et génération de médias - Note de maturité d'accès et d'admission des médias"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité d'accès et d'admission des médias

## Résumé

OpenClaw dispose d'une couche d'admission de médias partagée substantielle couvrant l'admission URL/base64, la détection MIME, les plafonds de taille, la récupération gardée, la politique de racine locale, le stockage de médias entrants, la distribution d'extraction PDF et le transfert de médias de canal. La posture de sécurité fondamentale est plus solide que ne le suggère le score de maturité orienté utilisateur : les récupérations distantes utilisent l'épinglage DNS gardé par SSRF et les contrôles de redirection, les lectures locales sont gardées par racine, le magasin de médias utilise des ID délimités et des écritures bornées, et l'extraction PDF/document est acheminée via des extracteurs de plugin avec des limites de page/pixel.

Le composant n'est pas encore stable car la preuve d'exécution est inégale sur toute la surface d'admission. Les scénarios QA prouvent que les pièces jointes d'image et la boucle d'image générée passent par un flux de style passerelle réel, et les tests de canal couvrent des chemins importants Telegram, WhatsApp, Slack, Teams et agent-runner, mais il n'existe pas de suite d'intégration unique qui exerce toutes les classes d'admission significatives ensemble : récupération d'URL distante, racines de chemin local, hydratation `media://inbound`, PDF/documents, assistants QR/image/audio/vidéo et mise en scène sandbox. L'enregistrement d'archive montre également une confusion répétée de l'opérateur et de l'utilisateur autour de la livraison de chemin de médias local, de la résolution `media://inbound`, des espaces réservés de document de canal et de l'accès du navigateur/outil aux médias entrants gérés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Références de médias locaux et distants : Couvre les références de médias locaux et distants dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Détection MIME et de type : Couvre la détection MIME et de type dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Plafonds de taille et lectures bornées : Couvre les plafonds de taille et les lectures bornées dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Récupération distante sécurisée : Couvre la récupération distante sécurisée dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Politique de racine locale : Couvre la politique de racine locale dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Magasin de médias entrants : Couvre le magasin de médias entrants dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Distribution d'extraction PDF/document : Couvre la distribution d'extraction PDF/document dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Classification des assistants QR et médias : Couvre la classification des assistants QR et médias dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.

## Fonctionnalités

- Références de médias locaux et distants : Couvre les références de médias locaux et distants dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Détection MIME et de type : Couvre la détection MIME et de type dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Plafonds de taille et lectures bornées : Couvre les plafonds de taille et les lectures bornées dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Récupération distante sécurisée : Couvre la récupération distante sécurisée dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Politique de racine locale : Couvre la politique de racine locale dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Magasin de médias entrants : Couvre le magasin de médias entrants dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Distribution d'extraction PDF/document : Couvre la distribution d'extraction PDF/document dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.
- Classification des assistants QR et médias : Couvre la classification des assistants QR et médias dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S) et le comportement d'admission, de stockage et d'accès sécurisé des fichiers médias associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs :
  - Les scénarios QA couvrent les flux de médias d'agent/exécution réels pour la livraison de pièces jointes d'image, la création d'artefacts d'image générée native et la réattachement d'image générée via le chemin de vision.
  - Les tests d'exécution/e2e de canal et d'agent-runner couvrent les comportements clés d'admission de médias : téléchargements de médias Telegram et groupes de médias, enregistrements entrants WhatsApp et `mediaMaxMb`, routage de secours de pièce jointe Teams, gestion de fichier protégé Slack, hydratation `media://` entrant, mise en scène sandbox et normalisation de chemin `MEDIA:` final.
  - Les tests unitaires sont larges sur les limites de récupération distante, la sécurité du chemin du magasin, la détection MIME, la politique de racine locale, les modèles de chemin entrant, la distribution d'extracteur PDF et les limites de lecture de réponse.
- Signaux négatifs :
  - La couverture est fragmentée par sous-système. Il n'existe pas de voie d'intégration unique prouvant le chemin local, la récupération d'URL, le magasin de médias, la mise en scène sandbox, l'extraction de document/PDF et la classification image/audio/vidéo et le transfert de fournisseur ensemble.
  - L'admission PDF/document a principalement des tests de distribution d'extracteur au niveau unitaire et spécifiques au canal, pas un scénario d'intégration clair équivalent aux flux de compréhension d'image et de génération d'image.
  - La récupération sécurisée et la politique de racine locale sont bien testées au niveau unitaire, mais moins de tests exercent ces politiques exactes via des chemins de passerelle/canal visibles par l'utilisateur.
- Lacunes d'intégration :
  - Ajouter un scénario de matrice d'admission de médias d'intégration qui soumet des références locales, distantes, `media://inbound`, PDF, image, audio et vidéo via le même point d'entrée d'exécution et affirme le stockage, MIME, le plafond de taille, la politique de racine et les résultats de transfert de fournisseur.
  - Ajouter une preuve d'exécution réelle explicite pour l'extraction PDF/document à partir de médias de canal entrants et des chemins `input_file` compatibles OpenAI.
  - Ajouter des scénarios de régression pour les modes de défaillance récurrents d'archive : accès `media://inbound` depuis le navigateur/outils, hydratation de document/autocollant Telegram et réponses finales de canal qui rendent les directives `MEDIA:` sous forme de texte.

## Score de Qualité

- Score : `Bêta (76%)`
- Rapports Gitcrawl :
  - Plusieurs rapports ouverts pertinents indiquent une instabilité vécue autour de la résolution des références médias et du transfert de canal : `#87203` (la résolution du chemin `media://inbound` échoue pour l'espace de travail personnalisé), `#83544` (le téléchargement du navigateur ne peut pas accéder aux médias entrants gérés), `#83065` (les médias entrants Signal ne sont pas résolubles par les outils intégrés), `#83748` (les autocollants Telegram ne sont pas hydratés), `#55917` (les documents Telegram deviennent des espaces réservés), `#85401` (la ligne `MEDIA:` PDF/document WhatsApp est rendue en tant que texte), `#67915` (les pièces jointes de l'assistant local en dehors des dossiers autorisés), et `#67031` (les limites de taille d'image codées en dur ne sont pas configurables dans les couches de désinfection).
  - Les RP pertinents montrent un renforcement actif mais aussi du changement : `#83660` limite médias entrants du téléchargement du navigateur, `#87219` références de lecture des médias entrants, `#74231` indices d'erreur racine locale, `#79268` limites de confiance des directives médias, `#77279` déduplications des notes médias entrants, et corrections de la liste blanche des médias locaux à l'hôte.
- Rapports Discrawl :
  - Les résultats Discord du responsable mentionnent le RP `#83660` nécessitant toujours une décision sur la limite `browser.upload` des médias entrants, le travail de plafond des médias entrants Feishu dans `#81044`, les notes de version appelant les racines des pièces jointes locales iMessage et le comportement des médias WhatsApp, et les rapports des utilisateurs selon lesquels les fichiers TTS/médias ont été générés localement mais non livrés via Discord.
  - Discord a également mis en évidence des commentaires antérieurs sur les pièces jointes du modèle texte uniquement WebChat étant déchargées en tant que `media://inbound/*`, le nettoyage de la réhydratation d'image obsolète, et la restauration de la liste blanche MIME de lecture d'hôte.
- Bonnes qualités :
  - La posture de sécurité est délibérée : les récupérations distantes passent par `fetchWithSsrFGuard`, les hôtes privés/internes bloqués sont enregistrés, les réponses DNS sont épinglées et vérifiées, les redirections sont limitées, les en-têtes sensibles inter-origines sont supprimés, et les URL de fichiers Slack sont limitées aux noms d'hôte HTTPS contrôlés par Slack.
  - Les contrôles de taille et de flux sont systématiquement présents : vérifications de la longueur du contenu, limites d'octets de flux, délais d'inactivité, plafonds médias par défaut, canal `mediaMaxMb`, limites de pages/pixels PDF, et extraits de texte limités.
  - L'accès local est limité à la racine plutôt qu'ad hoc : les médias entrants gérés sont traités spécialement, les racines du système de fichiers rejettent les racines larges ou invalides, le mode réservé à l'espace de travail arrête l'élargissement opportuniste, et les copies de mise en scène du bac à sable ne copient que les chemins entrants autorisés dans un répertoire de médias limité.
  - La gestion MIME est robuste contre l'usurpation d'identité courante : le reniflement d'octets bat les types d'images déclarés suspects, les conteneurs ZIP génériques ne deviennent pas de fausses images, les formats Office sont résolus à partir de la structure OOXML ou des extensions de confiance, et les secours CAF/audio couvrent la réalité des notes vocales du canal.
  - Le magasin de médias a des primitives de portée et de nettoyage claires : noms de fichiers désinfectés, sous-répertoires sûrs, ID relatifs à la racine, écritures atomiques via frères temporaires, vérifications de fichiers réguliers, lectures limitées, et support de suppression pour le nettoyage d'analyse abandonnée.
- Mauvaises qualités :
  - La clarté de l'opérateur reste inégale. Les erreurs de racine de médias locaux, l'accessibilité des médias entrants gérés, et les espaces réservés de médias spécifiques au canal ont généré des rapports de bogues et des RP répétés, ce qui signifie que le contrat d'implémentation est plus fort que l'explication orientée vers l'opérateur.
  - La surface d'admission a de nombreux points d'entrée parallèles avec des valeurs par défaut légèrement différentes : OpenAI-compatible `input_image`/`input_file`, téléchargements entrants du canal, chargements de médias sortants/locaux, téléchargement du navigateur, références d'invite d'agent, mise en scène du bac à sable, et artefacts d'outils de génération de médias. Cela augmente le risque de dérive.
  - Certains comportements attendus sont toujours dépendants du canal : documents/autocollants Telegram, références `media://` Signal, réponses PDF/document WhatsApp, URL protégées Slack, téléchargements Teams Graph/Bot Framework, et téléchargements entrants gérés par navigateur nécessitent chacun des correctifs spécifiques ou des exceptions documentées.
  - L'historique d'archive montre des réparations de limite de confiance après coup, y compris le renforcement des directives `MEDIA:` textuelles brutes et le nettoyage de réhydratation des références médias obsolètes.
- Exclu de la qualité :
  - La profondeur de vérification unitaire, d'intégration, e2e, en direct et en temps d'exécution réel n'a pas été utilisée pour augmenter ou diminuer ce score de qualité.

## Score de Complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour les références médias locales et distantes, la détection MIME et de type, les plafonds de taille et les lectures limitées, la récupération distante sûre, la politique de racine locale, le magasin de médias entrants, la distribution d'extraction PDF/document, la classification des assistants QR et médias.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucun harnais de composant de bout en bout unifié ne couvre tous les modes d'admission significatifs et les couches de politique ensemble.
- L'extraction PDF/document est présente mais non prouvée par un large flux visible par l'utilisateur dans le canal, la passerelle, le magasin de médias, l'extracteur, et le transfert de modèle.
- Les médias entrants gérés restent une limite d'intégration récurrente pour le navigateur/les outils/les espaces de travail personnalisés.
- La livraison des chemins de médias locaux et la messagerie d'erreur créent toujours une confusion de l'opérateur malgré les améliorations de la politique de racine.
- L'hydratation des médias du canal reste inégale pour les documents, les autocollants, les messages transférés/multi-images, et les réponses finales de type document.
- Les contrôles de limite de taille existent à plusieurs endroits, mais les rapports d'archive indiquent que les plafonds et la configurabilité sont difficiles à raisonner dans les couches de désinfection et les valeurs par défaut du canal.

## Preuves

### Docs

- `docs/kevinslin/maturity-scorecard/maturity-scorecard.md` évalue la surface plus large `Media understanding and media generation` comme `M2 Alpha` avec variance de fournisseur notée, limites de fichiers et risque de parité nœud/application.
- `docs/gateway/security/secure-file-operations.md` documente la posture fs-safe d'OpenClaw : opérations limitées à la racine, remplacement atomique, limites d'octets, rejet des liens symboliques/liens physiques si nécessaire, et conseils aux plugins pour éviter le `fs` brut pour les chemins non fiables.
- `docs/tools/image-generation.md` documente la livraison de médias générés via `image_generate`, la transmission d'images générées via l'outil de message, les avertissements SSRF des points de terminaison locaux/privés, et les chemins/URL d'images de référence pour le mode édition.
- `docs/cli/qr.md` documente la génération de codes QR comme assistant média de code de configuration et note la gestion des jetons/mots de passe et la sécurité des URL distantes.
- `docs/channels/line.md` documente les médias entrants sauvegardés sous `~/.openclaw/media/inbound/`, un plafond par défaut `channels.line.mediaMaxMb`, les exigences HTTPS publiques pour les médias sortants, et le rejet des cibles de boucle locale/lien local/réseau privé.
- `docs/channels/whatsapp.md`, `docs/channels/signal.md`, `docs/channels/telegram.md`, `docs/channels/slack.md`, `docs/channels/msteams.md`, `docs/channels/googlechat.md`, et les documents de canaux adjacents documentent les plafonds de médias spécifiques aux canaux, la gestion des pièces jointes entrantes, et les avertissements concernant les médias distants.
- `src/config/schema.help.ts` documente les contrôles d'URL d'image compatibles OpenAI (`allowUrl`, `urlAllowlist`, `allowedMimes`, `maxBytes`, redirections, délai d'expiration), les paramètres de niveau supérieur `media.preserveFilenames` / `media.ttlHours`, les plafonds d'image/vidéo pour la compréhension des médias, et les valeurs par défaut du modèle PDF/taille max/pages.

### Source

- `src/media/input-files.ts` implémente les sources base64/URL `input_image` et `input_file`, les listes blanches MIME par défaut, les limites d'octets/caractères/redirections/délai d'expiration/PDF, la récupération d'URL gardée, le rejet d'images usurpées, la normalisation HEIC, l'écrêtage de texte, et la distribution d'extraction PDF.
- `src/media/fetch.ts` implémente la récupération/sauvegarde de médias distants partagée avec récupération gardée SSRF, politique de nouvelle tentative, limites de longueur de contenu et de streaming, délai d'inactivité, détail d'erreur réduit, noms de fichiers conscients des redirections, et transmission de médias sauvegardés.
- `src/infra/net/fetch-guard.ts` et `src/infra/net/ssrf.ts` implémentent la récupération gardée HTTP(S) uniquement, les abandons de délai d'expiration, les vérifications de boucle/nombre de redirections, l'élimination des en-têtes cross-origin, le DNS épinglé, les listes blanches de noms d'hôtes, les adresses localhost/internes/privées/à usage spécial bloquées, et les modes de proxy de confiance.
- `src/media/store.ts` implémente le magasin de médias sous le répertoire de médias configuré, validation sûre du sous-répertoire/ID, gestion du nom de fichier d'origine assaini, écritures atomiques, écritures de flux et de tampon limitées, extensions dérivées de MIME, sauvegarde sûre des sources distantes/locales, `resolveMediaBufferPath`, `readMediaBuffer`, et `deleteMediaBuffer`.
- `src/media/media-reference.ts` implémente la normalisation `MEDIA:`, l'analyse `media://inbound/<id>`, la réécriture du chemin du bac à sable, l'endiguement du chemin des médias entrants, et la conversion des références entrantes en chemins physiques.
- `src/media/local-roots.ts`, `src/media/local-media-access.ts`, et `src/media/inbound-path-policy.ts` implémentent les racines de médias par défaut, les racines délimitées par agent, l'expansion optionnelle des racines à partir de sources locales concrètes, les contraintes d'espace de travail uniquement, les exceptions entrantes gérées, le rejet des chemins réseau Windows, et les modèles de racine entrante avec caractères génériques.
- `src/media/mime.ts`, `src/media/sniff-mime-from-base64.ts`, et `src/media/constants.ts` implémentent la normalisation MIME, le reniflage de type de fichier avec préfixes limités, les mappages d'extension pour les types image/audio/vidéo/PDF/Office/archive/texte, la solution de secours CAF, la gestion des conteneurs génériques, la classification des types, et les octets max par type.
- `src/media/pdf-extract.ts` et `src/media/document-extractors.runtime.ts` acheminent l'extraction PDF via les extracteurs de documents enregistrés avec des limites de page/pixel/texte et des erreurs désactivées claires.
- `src/media/web-media.ts` charge les références de médias locales, distantes, hébergées par plugin et entrantes, applique les portes de racine locale, les restrictions optionnelles de capacité de lecture d'hôte, la détection du type de média, l'optimisation/compression d'image, et les listes blanches MIME de document/média.
- `src/channels/inbound-event/media.ts` normalise les faits de médias de canal et les tableaux `MediaPath` / `MediaUrl` / `MediaType` hérités tout en préservant l'alignement chemin/URL mixte.
- `src/auto-reply/reply/stage-sandbox-media.ts` prépare les médias entrants autorisés dans le bac à sable ou les racines de cache distant en utilisant la copie fs-safe, les limites d'octets maximales, les vérifications de racine entrante, et la réécriture de chemin.
- `extensions/whatsapp/src/inbound/media.ts`, `extensions/slack/src/monitor/media.ts`, `extensions/telegram/src/telegram-media.runtime.ts`, `extensions/msteams/src/monitor-handler/inbound-media.ts`, et les fichiers de canal associés adaptent les téléchargements de pièces jointes spécifiques au fournisseur dans le magasin de médias partagé et le modèle de chemin d'exécution.

### Tests d'intégration

- `qa/scenarios/media/image-understanding-attachment.md` exécute un flux où un PNG joint atteint le chemin de vision du fournisseur et est affirmé via `imageInputCount`.
- `qa/scenarios/media/native-image-generation.md` vérifie que `image_generate` apparaît lorsqu'il est configuré, s'exécute et produit un chemin d'artefact de média sauvegardé.
- `qa/scenarios/media/image-generation-roundtrip.md` vérifie qu'une image générée est sauvegardée en tant que média, lue à partir du disque, réattachée au tour suivant, et reçue par le chemin de vision.
- `extensions/telegram/src/bot.media.downloads-media-file-path-no-file-download.e2e.test.ts` couvre les téléchargements de médias entrants Telegram, les groupes de médias, la préférence de récupération par proxy, la gestion des chemins de fichiers, et le comportement de médias de canal associé.
- `extensions/telegram/src/bot.media.stickers-and-fragments.e2e.test.ts` couvre la gestion des médias d'autocollants et de fragments Telegram.
- `extensions/whatsapp/src/inbound.media.test.ts` couvre les sauvegardes d'images/documents entrants, les médias cités, la préservation des extensions, et la propagation de `mediaMaxMb`.
- `extensions/msteams/src/monitor-handler/inbound-media.test.ts` couvre l'acheminement de secours Graph/Bot Framework Teams et la journalisation diagnostique.
- `src/auto-reply/reply/agent-runner.media-paths.test.ts` couvre la normalisation finale de la réponse `MEDIA:`, le comportement du cache de médias partagé, les médias entrants actuels transmis en tant qu'images natives, et le comportement de secours pour les médias partiels.
- `src/agents/embedded-agent-runner/run/images.test.ts` couvre l'hydratation `media://` entrante gérée, les médias entrants préparés en bac à sable, le blocage d'espace de travail uniquement, l'ordre des pièces jointes, et la gestion des références stales/locales dans le coureur d'agent.
- `src/gateway/control-ui-assistant-media.e2e.test.ts`, `src/cli/program.nodes-media.e2e.test.ts`, `test/image-generation.runtime.live.test.ts`, et `test/image-generation.infer-cli.live.test.ts` fournissent des preuves d'exécution/en direct supplémentaires pour les chemins de livraison et de génération de médias adjacents.

### Tests unitaires

- `src/media/fetch.test.ts` couvre le rejet de longueur de contenu et de streaming maxBytes, les limites de flux par défaut, le blocage d'IP privée, les erreurs de jetons réduits, le délai d'inactivité, le comportement de nouvelle tentative, et le comportement de sauvegarde/lecture de médias distants.
- `src/media/store.test.ts` et `src/media/store.redirect.test.ts` couvrent les extensions de médias sauvegardés, l'assainissement du nom de fichier d'origine, les lectures de source sûres, le nettoyage sans espace, la gestion des redirections, l'élimination des en-têtes cross-origin, la rétention des en-têtes same-origin, et les modes de fichier.
- `src/media/local-media-access.test.ts`, `src/media/local-roots.test.ts`, et `src/media/inbound-path-policy.test.ts` couvrent les exceptions entrantes gérées, le rejet des entrées imbriquées, le rejet des frères de l'espace de travail, les racines délimitées, la politique d'expansion des racines, le comportement de schéma distant de passage, les racines entrantes avec caractères génériques, et la validation des racines.
- `src/media/input-files.fetch-guard.test.ts` couvre l'admission d'images/fichiers base64 et URL, la conversion HEIC, le rejet de MIME usurpé, le comportement URL désactivé, l'annulation de longueur de contenu/flux, l'application MIME autorisée, et les paramètres de garde URL.
- `src/media/mime.test.ts` et `src/media/sniff-mime-from-base64.test.ts` couvrent la gestion Office/ZIP/conteneur générique, l'usurpation d'en-tête/extension d'image, les mappages HTML/XML/CSS, la détection audio et CAF, le mappage d'extension, et les préfixes de reniflage limités.
- `src/media/read-response-with-limit.test.ts` et `src/media/read-byte-stream-with-limit.test.ts` couvrent les lectures de flux limitées, les erreurs de débordement, les extraits de texte, et l'annulation du délai d'inactivité.
- `src/media/pdf-extract.test.ts` et `src/media/document-extractors.runtime.test.ts` couvrent la distribution d'extracteur de documents, les mots de passe PDF, les erreurs d'extracteur désactivé, la correspondance MIME, et l'agrégation d'erreurs d'extracteur.
- `src/media/web-media.test.ts` couvre le chargement de médias locaux/hébergés, l'application de racine locale, la politique d'optimisation/compression d'image, le comportement de liste blanche MIME de lecture d'hôte, et le rejet de médias locaux non sûrs.
- `src/channels/inbound-event/media.test.ts` couvre la normalisation des faits de médias chemin/URL/type de contenu et les tableaux de charge utile de médias hérités.
- `src/auto-reply/reply/stage-sandbox-media.runtime.ts` et les tests associés couvrent la préparation de médias en bac à sable, les vérifications de racine entrante, la réécriture de chemin préparé, et le comportement de dépassement.
- Les tests unitaires de canal sous `extensions/slack`, `extensions/whatsapp`, `extensions/msteams`, `extensions/telegram`, `extensions/qqbot`, et `extensions/line` couvrent les plafonds de médias spécifiques aux canaux, les téléchargements de pièces jointes, les solutions de secours MIME, le consentement/téléchargement de fichiers, la gestion des sources de médias sortants, et le comportement des assistants de médias.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "media file intake storage secure access" --json
```

Résultats :

- Aucun résultat.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "media attachment MIME sniff size cap SSRF local roots" --json
```

Résultats :

- Aucun résultat.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "media://inbound media store attachment file access" --json
```

Résultats :

- Aucun résultat.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "PDF document extraction media intake" --json
```

Résultats :

- Aucun résultat.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "local media path" --json
```

Résultats :

- `#77702` problème ouvert : Les directives `MEDIA:` Telegram avec chemins d'images locales sont envoyées en tant que texte au lieu de pièces jointes.
- `#85401` problème ouvert : La directive `MEDIA:` de réponse finale WhatsApp peut s'afficher en tant que texte brut pour les pièces jointes PDF/document.
- `#67915` problème ouvert : les pièces jointes d'assistant local s'affichent comme indisponibles/en dehors des dossiers autorisés malgré la configuration du serveur.
- `#74231` PR ouvert : ajoute les racines configurées aux indices d'erreur path-not-allowed.
- `#79268` PR ouvert : renforce les limites de confiance des directives de médias.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "input_image" --json
```

Résultats :

- `#86878` problème ouvert : la sortie stdout de codex-app-server fuit dans la base64 `input_image` et casse les appels API suivants.
- `#67031` problème ouvert : les limites de taille d'image sont codées en dur et non configurables dans les couches d'assainissement.
- `#80418` PR ouvert : la mention du chemin de parité du SDK OpenAI inclut la forme de test `input_image` et `input_file`.
- `#75727` PR ouvert : le chemin de rendu de médias en ligne inclut le comportement du bloc de contenu `input_image`.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "inbound media" --json
```

Résultats :

- `#83660` PR ouvert : permet le téléchargement du navigateur à partir du répertoire de médias entrants.
- `#87219` PR ouvert et `#87203` problème ouvert : résout les références de lecture de médias entrants et corrige les défaillances de résolution de chemin `media://inbound` pour les espaces de travail personnalisés.
- `#83544` problème ouvert : le téléchargement du navigateur ne peut pas accéder aux fichiers du média entrant géré.
- `#83065` problème ouvert : Les médias entrants Signal s'affichent en tant qu'URI `media://` non résolubles par les outils intégrés.
- `#83748` problème ouvert : Les autocollants entrants Telegram ne sont pas hydratés en tant que médias lisibles par l'agent.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "mediaMaxMb attachment" --json
```

Résultats :

- `#55917` problème ouvert : Les documents Telegram arrivent parfois uniquement en tant que `<media:document>` au lieu d'une véritable pièce jointe.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "media file intake storage secure access" --limit 5
```

Résultats :

- Aucun résultat.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "local media path" --limit 5
```

Résultats :

- Les notes de version du 2026-05-27 mentionnent les racines de pièces jointes locales iMessage, le comportement de groupe/média WhatsApp, et l'enveloppe de texte de fichier récupéré comme durcie ou plus stable.
- Le rapport du contributeur du 2026-05-18 décrit un cas TTS Discord où un vrai fichier Opus local a été produit mais n'a pas été remis à Discord en tant que média, indiquant une confusion du pont de livraison.
- Le rapport du responsable du 2026-05-26 mentionne les corrections de messagerie dans les chemins iMessage, WhatsApp, Mattermost, QQ Bot et Telegram.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "inbound media" --limit 5
```

Résultats :

- La demande du responsable du 2026-05-19 pour la PR `#83660` demande un examen de la limite `browser.upload` des médias entrants et si elle ou `#83572` devrait être canonique.
- La note de la PR `#81521` du 2026-05-13 décrit une correction de limite de confiance des métadonnées entrantes pour les métadonnées de canal circulant dans les invites visibles.
- La note de la PR `#81044` du 2026-05-12 indique que les téléchargements de médias entrants Feishu ont été plafonnés pour fermer un écart de risque de mémoire de fichier surdimensionné.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "media://inbound" --limit 5
```

Résultats :

- Le commentaire du problème du 2026-04-26 indique que l'atténuation des pièces jointes WebChat/Gateway texte uniquement décharge les images en tant que références `media://inbound/*` au lieu de les rejeter.
- Les commentaires du problème du 2026-04-26 pour la réhydratation d'images stales indiquent que les anciennes références `[media attached: ...]`, `[Image: source: ...]`, et `media://inbound/...` nues sont supprimées du contexte de relecture élagué.
- Le commentaire d'examen du 2026-04-26 indique que la préservation des pièces jointes pour les chemins de modèle texte uniquement en déchargeant vers `media://inbound/*` n'est pas la même que d'honorer la sémantique de remplacement d'entrée de modèle explicite.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "PDF document attachment media" --limit 5
```

Résultats :

- Le commentaire d'examen du 2026-04-10 indique que `src/media/web-media.ts` a restauré la liste blanche MIME de lecture d'hôte afin que les envois sortants locaux d'hôte soient limités aux types MIME image/audio/vidéo plus PDF et document Office au lieu de fichiers texte brut arbitraires.
- Les notes de problème et de PR du 2026-04-08 décrivent les envois de médias PDF/document WhatsApp qui ont signalé le succès tout en livrant du texte uniquement, et une correction acheminant les envois de médias vers `sendMedia` au lieu de `sendText`.
- La note de la PR du 2026-03-27 indique que les pièces jointes de document Telegram étaient mal identifiées par un espace réservé générique, ce qui a amené les agents à répondre comme si aucun PDF n'avait été reçu.
