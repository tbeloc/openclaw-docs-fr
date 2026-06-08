---
title: "Android app - Media Capture Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Android app - Media Capture Maturity Note

## Résumé

La capture de médias Android inclut la capture de photos et de clips CameraX, le redimensionnement des charges utiles d'images, les retours visuels de la caméra HUD, WebView Canvas/A2UI, l'accès à la photothèque dans la variante tierce, et les vérifications de capacité en direct pour les commandes caméra/canvas. La couverture est Alpha car l'implémentation est réelle mais au premier plan uniquement et la documentation de la caméra Android n'est pas entièrement alignée avec l'ensemble des commandes source. La qualité est Alpha car les permissions, les limites de charge utile, la disponibilité de WebView, les restrictions de la variante Play et l'état au premier plan rendent le chemin de l'opérateur fragile.

## Portée de la catégorie

Inclus dans cette catégorie :

- Caméra et capture de médias : énumération de caméra, capture, photo, écran et comportement de capture de médias.

## Fonctionnalités

- Caméra et capture de médias : énumération de caméra, capture, photo, écran et comportement de capture de médias.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (66%)`
- Signaux positifs : la documentation Android couvre les commandes Canvas et caméra au premier plan ; la source implémente la capture de photos/clips CameraX, l'invite de permission, les garde-fous de charge utile, les actions A2UI/WebView et l'accès à la photothèque où la variante le permet. La suite de capacité en direct profile `camera.list`, `camera.snap`, `camera.clip`, `canvas.*` et `canvas.a2ui.*`.
- Signaux négatifs : les tests de capacité en direct sont préconditions sur une application appairée, au premier plan et déverrouillée, et nécessitent l'onglet Écran pour Canvas/A2UI. La documentation des commandes de caméra partagées ne liste que `camera.list` Android dans la section Android même si la source et la documentation de plateforme exposent snap/clip.
- Lacunes d'intégration : besoin d'une véritable fiche de notation de médias Android qui maintient l'application au premier plan, accorde les permissions caméra/micro/photo, invoque photo avant/arrière, clip court avec/sans audio, Canvas navigate/eval/snapshot, et enregistre le comportement d'échec en arrière-plan.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : `camera.snap Android` a trouvé le problème #87058 où le nœud Android s'est connecté mais a annoncé zéro commandes ; l'extrait note que `camera.snap`, `camera.clip` et `canvas.*` sont des commandes à haut risque contrôlées. `photos.latest Android` n'a retourné aucun résultat direct.
- Rapports Discrawl : la recherche a trouvé des messages d'assistance de janvier décrivant la caméra snap/clip Android, Canvas, la mise en veille vocale et l'enregistrement d'écran comme des capacités de nœud prises en charge, et avertissant que les nœuds sont souvent hors ligne ou dépendants du premier plan.
- Bonnes qualités : les commandes de caméra demandent les permissions d'exécution, limitent la durée du clip, limitent la taille de la charge utile, recompressent les JPEG sous les limites API, affichent l'état HUD de la caméra et séparent la variante Play de l'accès à la photothèque tierce.
- Mauvaises qualités : les commandes de médias sont au premier plan uniquement, WebView/A2UI dépend de la disponibilité de l'onglet Écran et de la disponibilité de l'hôte canvas Gateway, et la variante Play supprime les permissions de photothèque. L'alignement source/docs est imparfait pour les détails des commandes de caméra Android.
- Exclu de la qualité : la couverture des tests et la preuve du flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (66%)`
- Instructions de surface : évaluées par rapport à `references/completeness/android-app.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la caméra et la capture de médias.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aligner la documentation des commandes Android `/nodes/camera` avec la source et la documentation de plateforme pour `camera.snap` et `camera.clip`.
- Ajouter un runbook de mode d'échec de médias au premier plan/arrière-plan avec les messages d'opérateur exacts.
- Décider si `photos.latest` est pris en charge uniquement pour les builds tiers ou devrait avoir un remplacement compatible Play.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` documente l'hôte Canvas, `canvas.eval`, `canvas.snapshot`, `canvas.navigate`, les commandes A2UI et les commandes de caméra au premier plan uniquement `camera.snap` et `camera.clip`.
- `/Users/kevinlin/code/openclaw/docs/nodes/camera.md` documente les paramètres de caméra Android, les permissions, l'exigence au premier plan et `camera.list` ; sa liste de commandes Android est plus étroite que la page source et plateforme.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` documente les exigences de l'onglet Écran pour les tests d'intégration A2UI et indique que les builds Play suppriment l'accès à la photothèque.

### Source

- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/CameraCaptureManager.kt` implémente l'énumération des appareils CameraX, la capture de photos, l'enregistrement de clips, les demandes de permission, la rotation EXIF, la mise à l'échelle JPEG et les limites de charge utile.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/CameraHandler.kt` gère `camera.list`, `camera.snap`, `camera.clip`, l'état HUD, la journalisation de débogage, les limites de taille de clip et les charges utiles base64.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/PhotosHandler.kt` implémente `photos.latest` avec vérifications de permission, requête d'image la plus récente, redimensionnement et limites de budget base64.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/CanvasScreen.kt` implémente le Canvas WebView, les paramètres de navigation sécurisée, le pont A2UI WebMessage, le cycle de vie de visibilité et la gestion du processus de rendu.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/InvokeDispatcher.kt` applique l'exigence au premier plan pour les commandes de caméra et canvas.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/android-node.capabilities.live.test.ts` inclut des profils pour `camera.list`, `camera.snap`, `camera.clip`, `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot` et les commandes A2UI push/reset.
- `/Users/kevinlin/code/openclaw/apps/android/scripts/perf-online-benchmark.sh` vérifie la disponibilité de WebView de l'onglet Écran avant d'exécuter le benchmark d'écran.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/node/CameraHandlerTest.kt`, `JpegSizeLimiterTest.kt`, `PhotosHandlerTest.kt`, `CanvasControllerSnapshotParamsTest.kt`, `CanvasActionTrustTest.kt` et `CanvasA2UIActionBridgeTest.kt` couvrent les aides de médias et canvas.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/node/InvokeDispatcherTest.kt` couvre le comportement de dispatch de commande.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "camera.snap Android" --json`

Résultats :

- Problème #87058 `Android node connects but advertises zero commands ...` ; l'extrait note `camera.snap`, `camera.clip` et `canvas.*` comme commandes à haut risque correctement contrôlées.

Requête :

`gitcrawl search openclaw/openclaw --query "photos.latest Android" --json`

Résultats :

- Aucun résultat direct.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android camera snap screen canvas"`

Résultats :

- Les messages d'assistance du 2026-01-03 décrivent les nœuds Android comme des appareils compagnons appairés qui peuvent exposer la caméra snap/clip, Canvas, l'enregistrement d'écran et les surfaces audio/TTS, tout en notant que la disponibilité réelle dépend de la connectivité du nœud.
