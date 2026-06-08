---
title: "Android app - Mobile Chat Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Android app - Mobile Chat Maturity Note

## Résumé

L'application Android dispose d'une surface de chat mobile substantielle : sélection de session, historique, envois optimistes, texte d'assistant en streaming, affichage des appels d'outils en attente, pièces jointes d'images, contrôles de réflexion, rendu markdown et support des benchmarks de chat en ligne. La couverture atteint Beta car l'implémentation s'étend sur les RPC de chat Gateway et la preuve d'interface utilisateur en ligne, bien qu'aucun scénario de chat installé complet sur Play n'ait été trouvé. La qualité reste Alpha car les preuves d'archive actives incluent des problèmes d'examen de copie/réponse de chat et la source actuelle dépend toujours de chemins d'interface utilisateur mobile en évolution rapide.

## Portée de la catégorie

Inclus dans cette catégorie :

- Onglet Chat : Onglet Chat, liste/filtrage de session, compositeur, pièces jointes d'images, analyse/rendu de messages, statut du modèle/fournisseur adjacent au chat et intégration RPC de chat Gateway

## Fonctionnalités

- Onglet Chat : Onglet Chat, liste/filtrage de session, compositeur, pièces jointes d'images, analyse/rendu de messages, statut du modèle/fournisseur adjacent au chat et intégration RPC de chat Gateway

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`
- Signaux positifs : La documentation décrit `chat.history`, `chat.send`, `chat.subscribe`, la sélection de session, la normalisation d'affichage et les mises à jour push au mieux. La source implémente l'amorçage d'historique, le changement de session, les messages optimistes, le texte d'assistant en streaming, les appels d'outils en attente, l'abandon/actualisation, les pièces jointes et le rendu markdown. Le benchmark en ligne vérifie explicitement l'état connecté et le compositeur de chat en direct.
- Signaux négatifs : Les preuves sont plus fortes pour les tranches source/unité/benchmark d'interface utilisateur que pour un chemin de chat installé sur Play de bout en bout via installation, appairage, envoi, streaming, arrière-plan, reconnexion et reprise.
- Lacunes d'intégration : Besoin d'assurance qualité récurrente du chat mobile qui envoie du texte et des images, change de session, diffuse une réponse utilisant des outils, met l'application en arrière-plan/la rouvre et vérifie la parité d'historique avec un autre client.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : `Android message copy text selection chat screen` a trouvé le problème #57754 et la PR #59603 pour la copie de message et la sélection de texte du chat. L'enregistrement d'examen de la PR a signalé les citations de réponse, le contexte de réponse avec pièce jointe uniquement, les actions de texte vide et la sémantique d'envoi de réponse.
- Rapports Discrawl : La recherche a trouvé des commentaires d'examen du miroir GitHub sur la PR #59603 qui identifient les problèmes visibles par l'utilisateur autour des citations multiligne, des messages contenant uniquement des images, des charges utiles de copie/partage vides et de l'état d'interface utilisateur de réponse locale uniquement.
- Bonnes qualités : La logique de chat suit les ID d'exécution en attente, normalise les sessions, supprime le texte bruyant de contrôle de modèle/appel d'outil de l'historique, prend en charge les pièces jointes d'images avec gestion de la taille et sépare la santé/les erreurs visibles de l'activation d'envoi du compositeur.
- Mauvaises qualités : Le comportement de réponse/copie a eu plusieurs régressions subtiles visibles par l'utilisateur, l'interface utilisateur du chat mobile est toujours en cours de reconstruction active et la continuité de session entre les changements de réseau/mise en arrière-plan manque d'un résultat de runbook publié spécifique à Android.
- Exclu de la qualité : La couverture de test et la preuve de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/android-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'onglet Chat.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un smoke test de parité de chat mobile par rapport à WebChat/TUI pour l'historique, le streaming, les sessions, les pièces jointes et l'abandon.
- Confirmer le comportement de réponse/copie/sélection de texte après les conclusions d'examen de la PR #59603.
- Rendre explicite la reconnexion et l'état de reprise de session dans les diagnostics de chat Android.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` documente l'historique de l'onglet Chat via `chat.history`, l'envoi via `chat.send`, le `chat.subscribe` au mieux, la sélection de session et le comportement de normalisation d'affichage.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` indique que la reconstruction inclut une interface utilisateur de chat restylisée, le support du streaming et les notifications push pour les mises à jour de statut gateway/chat.

### Source

- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/chat/ChatController.kt` implémente le chargement/changement de session, la santé, les envois optimistes, les exécutions en attente, le texte d'assistant en streaming, l'état des appels d'outils, l'historique et le `chat.send` Gateway.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/chat/ChatScreen.kt` compose l'en-tête de chat, les avis, la liste des messages, les pièces jointes, le raccourci vocal, le niveau de réflexion, l'actualisation/abandon et le chemin d'envoi.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/chat/ChatComposer.kt` implémente les contrôles du compositeur, le sélecteur de réflexion, la bande de pièces jointes, l'actualisation, l'abandon et l'activation d'envoi.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/chat/ChatMarkdown.kt` rend les blocs markdown, le code, les tableaux, les listes de tâches, les liens, les images et les conteneurs de sélection.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/SessionsScreen.kt` rend les filtres de session récente/en direct, le tri et les lignes de session active.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/apps/android/scripts/perf-online-benchmark.sh` vérifie que l'application atteint un état connecté visible et que le compositeur de chat en direct est présent, puis exécute des benchmarks de changement de session de chat ou de défilement.
- Aucun e2e de chat Android complet via une réponse Gateway réelle et une vérification de parité d'historique avec un autre client n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/chat/ChatControllerMessageIdentityTest.kt`, `ChatControllerSessionPolicyTest.kt` et `ChatMessageContentParsingTest.kt` couvrent le comportement du modèle/contrôleur de chat.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/ui/chat/ChatComposerDraftTest.kt`, `ChatImageCodecTest.kt`, `ChatMarkdownTest.kt`, `ChatSheetContentTest.kt` et `SessionFiltersTest.kt` couvrent les aides d'interface utilisateur de chat.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Android message copy text selection chat screen" --json`

Résultats :

- Problème #57754 `Android: Add message copy and text selection to chat screen`.
- PR #59603 `feat(android): Add message copy and text selection to chat screen`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android chat screen message copy"`

Résultats :

- 2026-04-03 Commentaires d'examen du miroir GitHub sur la PR #59603 ont signalé le formatage des citations multiligne, le contexte de réponse avec pièce jointe uniquement, les actions de copie/partage vides pour les messages contenant uniquement des images et l'absence de cible de réponse dans le chemin d'envoi sortant.
