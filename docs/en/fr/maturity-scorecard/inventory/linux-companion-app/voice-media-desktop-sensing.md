---
title: "Application compagnon Linux - Note de maturité pour la voix, les médias et la détection de bureau toujours active"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon Linux - Note de maturité pour la voix, les médias et la détection de bureau toujours active

## Résumé

OpenClaw prend en charge la conversation native et la capture de médias sur macOS/iOS/Android et la conversation via navigateur à travers la passerelle, mais Linux n'a pas d'application compagnon native prise en charge pour le microphone, l'écran, la caméra, l'activation vocale ou la détection de bureau toujours active. Les threads d'assistance archivés orientent explicitement les utilisateurs Linux vers des scripts de surveillance ou d'autres ponts pour ces flux.

## Portée des catégories

- Conversation native Linux, appui sur bouton pour parler, activation vocale et transcription.
- Capture de microphone, capture d'écran/caméra, détection de contexte de bureau et flux de pièces jointes multimédias locales.
- Permissions multimédias natives et comportement au premier plan/arrière-plan.
- Surfaces adjacentes hors de portée : conversation par navigateur, conversation native Android/iOS/macOS, chemin texte/chat Linux Gateway.

## Fonctionnalités

- Conversation native Linux : Conversation native Linux, appui sur bouton pour parler, activation vocale et transcription
- Capture de microphone : Capture de microphone, capture d'écran/caméra, détection de contexte de bureau et flux de pièces jointes multimédias locales
- Permissions multimédias natives : Permissions multimédias natives et comportement au premier plan/arrière-plan

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (0%)`
- Signaux positifs : Les contrats de conversation et de médias existent sur d'autres plates-formes d'applications natives et surfaces de navigateur.
- Signaux négatifs : aucune source de capture de médias, voix, activation, écran, caméra ou détection toujours active d'application native Linux n'existe dans la version actuelle.
- Lacunes d'intégration : aucune preuve de voix/médias/détection d'application native Linux n'existe.

## Score de qualité

- Score : `Expérimental (20%)`
- Rapports Gitcrawl : Les requêtes de compagnon voix/mic/écran Linux n'ont retourné aucun résultat direct.
- Rapports Discrawl : les conseils d'assistance pour l'utilisation d'un assistant de bureau Linux indiquent qu'aucune application compagnon OpenClaw native n'existe pour la détection de bureau toujours active complète et recommandent des scripts de surveillance pour la capture de mic/écran.
- Bonnes qualités : la documentation évite de promettre un comportement voix/médias natif Linux et la documentation d'application existante rend les plates-formes prises en charge explicites.
- Mauvaises qualités : il n'existe pas de modèle de permission Linux, contrat de capture de médias, politique au premier plan/arrière-plan, conception de boucle d'activation ou UX de paramètres natifs.
- Exclus de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Expérimental (0%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la conversation native Linux, la capture de microphone, les permissions multimédias natives.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Définir si la capture de médias native Linux est dans la portée de la première version de l'application.
- Décider des API d'environnement de bureau pour l'accès à l'écran/mic/caméra et l'activation vocale.
- Documenter les modèles de secours pour les utilisateurs qui ont besoin de détection Linux toujours active avant qu'une application native n'existe.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:9` : la conversation native nomme actuellement macOS/iOS/Android, plus la conversation par navigateur.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:126` : le comportement de l'interface utilisateur macOS et Android est documenté ; aucune interface utilisateur de conversation native Linux n'est documentée.
- `/Users/kevinlin/code/openclaw/docs/nodes/camera.md:9` : la capture de caméra est prise en charge pour les nœuds d'application iOS, Android et macOS.
- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:13` : les applications compagnon Linux sont prévues.

### Source

- Aucune conversation native Linux, capture de médias, microphone, capture d'écran ou source de caméra n'existe sous `apps/`.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/TalkModeRuntime.swift`, `/Users/kevinlin/code/openclaw/apps/ios/Sources/Voice`, et `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/voice` sont des implémentations de voix natives adjacentes prises en charge, pas Linux.

### Tests d'intégration

- Aucun test d'intégration voix/médias/détection native Linux n'a été trouvé.
- Les tests E2E de voix Android existants et les tests de voix native Apple/mobile sont adjacents, pas une preuve d'application Linux.

### Tests unitaires

- Aucun test unitaire voix/médias natif Linux n'a été trouvé.
- Les tests de conversation/médias existants ciblent macOS, iOS, Android, OpenClawKit partagé et le code Gateway/navigateur.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Linux companion voice wake microphone screen capture" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "Linux no native companion app mic screen watcher scripts" --mode keyword --limit 8 --json`

Résultats :

- Les deux requêtes gitcrawl spécifiques aux fonctionnalités n'ont retourné aucun résultat.
- L'absence de résultats gitcrawl est neutre après les vérifications de fraîcheur, mais elle ne fournit aucun signal positif pour le comportement voix/médias natif Linux pris en charge.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux companion voice wake microphone screen capture"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux no native companion app mic screen watcher scripts"`

Résultats :

- La requête voix/activation/mic/écran n'a retourné aucun résultat direct.
- La requête scripts de surveillance a retourné un thread d'assistance du 10 avril pour Arch/Hyprland expliquant que parce que Linux n'a pas encore d'application compagnon OpenClaw native, l'utilisateur devrait utiliser des scripts de surveillance locaux pour la capture d'écran et de mic et faire un pont via OpenClaw/Discord.
