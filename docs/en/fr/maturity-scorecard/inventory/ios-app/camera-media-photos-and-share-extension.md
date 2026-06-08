---
title: "iOS app - Media and Sharing Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Media and Sharing Maturity Note

## Résumé

Le support des médias iOS est implémenté sur la capture/clip caméra, les lectures de photothèque, l'enregistrement d'écran, le bounding de charge utile locale, et une Share Extension qui transfère du texte, des URL et des pièces jointes vers la Gateway appairée en tant que `agent.request`. La couverture est Expérimentale car il n'existe actuellement aucun test de fumée public/TestFlight prouvant la persistance end-to-end de la caméra, des photos, du partage et des transcriptions. La qualité est mi-Expérimentale car les limites de charge utile et les erreurs de permission sont explicites, tandis que les enregistrements d'archive montrent que les métadonnées de médias et les régressions de pièces jointes volumineuses affectent toujours les chemins mobiles/partage.

## Portée de la catégorie

Inclus dans cette catégorie :

- Liste/snap/clip caméra : Liste/snap/clip caméra, charges utiles d'image la plus récente de la photothèque, enregistrement d'écran en tant que média, flux de brouillon/envoi de Share Extension, extraction de pièces jointes, paramètres de relais de gateway pour le partage, et limites de charge utile de médias mobiles

## Fonctionnalités

- Liste/snap/clip caméra : Liste/snap/clip caméra, charges utiles d'image la plus récente de la photothèque, enregistrement d'écran en tant que média, flux de brouillon/envoi de Share Extension, extraction de pièces jointes, paramètres de relais de gateway pour le partage, et limites de charge utile de médias mobiles

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimentale (42%)`
- Signaux positifs : Le script e2e du nœud iOS manuel peut invoquer `photos.latest`, `camera.snap`, et `screen.record` contre un nœud connecté ; les tests unitaires de l'application et Swift partagés couvrent les limites de paramètres et le comportement de lien profond de partage.
- Signaux négatifs : Aucune fiche de score de médias automatisée sur appareil réel n'a été trouvée pour les permissions de caméra, la sélection d'appareil avant/arrière, l'audio de clip, les limites de photothèque, la livraison de pièces jointes de Share Extension, la persistance des métadonnées de transcription, et les modes d'échec au premier plan/arrière-plan.
- Lacunes d'intégration : Besoin d'un test de fumée TestFlight ou sur appareil réel actuel qui capture les artefacts de caméra/photo/écran/partage et vérifie qu'ils apparaissent dans la transcription Gateway avec les métadonnées intactes.

## Score de qualité

- Score : `Expérimentale (45%)`
- Rapports Gitcrawl : `iOS share extension media metadata` a trouvé le problème #60339 pour les métadonnées offloadedRefs perdues dans les transcriptions iOS share/node et PR #86936 pour persister les métadonnées de médias dans les transcriptions `agent.request`. `iOS app` a également trouvé PR #73711 pour les miniatures de pièces jointes iOS de style photos-picker.
- Rapports Discrawl : `iOS camera photos share extension media` n'a retourné aucun résultat. Les résultats plus larges `iOS app` et `iOS node commands foreground background unavailable` mentionnent les exigences de premier plan de caméra et les limites d'aperçu interne/TestFlight.
- Bonnes qualités : Les paramètres par défaut de sortie de caméra sont bornés, les réponses de photothèque restent sous les budgets de charge utile WebSocket de Gateway, Share Extension enregistre les événements de statut, réessaie l'ID client hérité en cas de non-concordance de protocole, et utilise une configuration Gateway appairée plutôt qu'un téléchargement non authentifié.
- Mauvaises qualités : Le chemin des médias repose toujours sur les charges utiles base64 pour plusieurs commandes, les commandes au premier plan uniquement sont faciles à invoquer depuis le mauvais état, et les enregistrements d'archive récents montrent que la préservation des métadonnées de transcription était toujours en cours de réparation.
- Exclu de la qualité : Les tests unitaires et le script d'invocation de médias manuel n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Expérimentale (42%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la liste/snap/clip caméra.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un test de fumée de médias couvrant le snap caméra, le clip caméra avec et sans audio, la récupération de photothèque, le transfert d'image de Share Extension, et la rétention des métadonnées de transcription.
- Déplacer les flux de médias volumineux vers des handles durables où les budgets de charge utile base64 sont trop serrés.
- Exposer une récupération in-app plus claire pour les défaillances de permission de caméra/photo et les erreurs au premier plan uniquement.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` répertorie la caméra, l'écran, les photos, et les limites de premier plan/arrière-plan.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` répertorie le snap/clip caméra, l'enregistrement d'écran, les photos, et le transfert de lien profond de Share Extension comme fonctionnalités concrètes actuelles.
- `/Users/kevinlin/code/openclaw/docs/nodes/camera.md` documente la famille de commandes caméra inter-nœuds.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Camera/CameraController.swift` implémente la capture de photo et de clip avec permissions, sélection d'appareil, transcodage JPEG, et export MP4.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Media/PhotoLibraryService.swift` implémente `photos.latest` avec budgets de charge utile et réduction d'échelle JPEG.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Screen/ScreenRecordService.swift` enregistre les charges utiles vidéo d'écran.
- `/Users/kevinlin/code/openclaw/apps/ios/ShareExtension/ShareViewController.swift` prépare un brouillon de partage et envoie `agent.request` via une session de nœud Gateway appairée.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/dev/ios-node-e2e.ts` inclut `photos.latest` et les invocations optionnelles dangereuses `camera.snap` et `screen.record`.
- Aucun artefact e2e de médias et Share Extension automatisé sur appareil réel n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/CameraControllerClampTests.swift`, `CameraControllerErrorTests.swift`, et `ScreenRecordServiceTests.swift` couvrent les limites de paramètres et les erreurs.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/ShareToAgentDeepLinkTests.swift` couvre l'encodage de message de partage et de route.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Tests/OpenClawKitTests/ChatImageProcessorTests.swift` couvre les aides de traitement d'image partagées.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iOS share extension media metadata" --json`

Résultats :

- Problème #60339 `[Bug]: bug(gateway): offloadedRefs metadata lost in transcript for iOS share/node path`.
- PR #86936 `fix(gateway): persist media metadata in agent.request transcripts`.

Contexte de requête supplémentaire :

- `gitcrawl search openclaw/openclaw --query "iOS app" --json` a trouvé PR #73711 pour les miniatures de pièces jointes iOS de style photos-picker.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS camera photos share extension media"`

Résultats :

- Aucun résultat.

Contexte de requête supplémentaire :

- `discrawl search --mode fts --limit 5 "iOS node commands foreground background unavailable"` a trouvé des conseils de support indiquant que les commandes de caméra et d'écran nécessitent que l'application iOS soit au premier plan.
