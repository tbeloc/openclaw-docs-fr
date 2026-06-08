---
title: "Application compagnon macOS - Note de Maturité Canvas"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon macOS - Note de Maturité Canvas

## Résumé

Canvas est une fonctionnalité d'application macOS de première classe avec un panneau WKWebView, un schéma d'URL local personnalisé, la surveillance de fichiers, des snapshots, l'évaluation JavaScript, la navigation automatique de l'hôte Canvas Gateway, et les commandes A2UI v0.8. La couverture est Beta car Canvas dispose de chemins WKWebView et d'exécution A2UI concrets avec preuve de fumée de support, mais aucun scénario complet d'agent vers WKWebView n'a été trouvé. La qualité est Alpha car les preuves d'archive montrent des régressions récentes de visibilité A2UI, de liste d'autorisation et de livraison de charge utile.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Ouverture/fermeture/navigation/évaluation/snapshot du panneau Canvas : comportement du panneau Canvas, statut et vérification visible par l'opérateur.
- Schéma d'URL personnalisé local : schéma d'URL personnalisé local et service de fichiers racine de session
- Navigation automatique de l'hôte A2UI : navigation automatique de l'hôte A2UI, push/reset et pont d'action
- Paramètre d'activation/désactivation de Canvas : paramètre d'activation/désactivation de Canvas et comportement de la commande de nœud

## Fonctionnalités

- Ouverture/fermeture/navigation/évaluation/snapshot du panneau Canvas : comportement du panneau Canvas, statut et vérification visible par l'opérateur.
- Schéma d'URL personnalisé local : schéma d'URL personnalisé local et service de fichiers racine de session
- Navigation automatique de l'hôte A2UI : navigation automatique de l'hôte A2UI, push/reset et pont d'action
- Paramètre d'activation/désactivation de Canvas : paramètre d'activation/désactivation de Canvas et comportement de la commande de nœud

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (74%)`
- Signaux positifs : Les docs et sources couvrent les racines de fichiers Canvas, le schéma personnalisé, le comportement du panneau, l'API d'agent, les commandes A2UI, les liens profonds et la sécurité. Les tests unitaires/fumée couvrent les charges utiles IPC, la sécurité du schéma, la fumée de fenêtre, l'actualisation de l'URL de l'hôte A2UI et la gestion des erreurs/taille de snapshot.
- Signaux négatifs : La couverture ne prouve pas un `canvas.a2ui.push` complet de Gateway vers nœud atteignant le moteur de rendu WKWebView dans une application en cours d'exécution. Le support A2UI est explicitement v0.8 et exclut `createSurface` v0.9.
- Lacunes d'intégration : Besoin d'un scénario d'application réel qui invoque `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`, `canvas.a2ui.push` et le rappel du pont d'action via l'invocation de nœud Gateway.

## Score de Qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : Les résultats incluent le problème #81159 où `canvas.a2ui.push` retourne ok mais la charge utile n'atteint jamais WKWebView, le problème #86707 où le nœud macOS déclare les commandes `canvas.*` que la liste d'autorisation Gateway bloque, la PR #62021 pour la réécriture de l'hôte A2UI avec caractères génériques vers loopback, et la PR #86729 pour ajouter les commandes canvas macOS à la liste d'autorisation de plateforme.
- Rapports Discrawl : L'archive inclut #75039 comme correctif à reporter pour le contenu Canvas A2UI macOS étant effacé par rechargement redondant, #62609 fermeture pour l'échec de l'hôte A2UI loopback/Tailscale Serve, et #66983 demande de support de nœud canvas web.
- Bonnes qualités : Canvas bloque la traversée de répertoires, utilise un schéma personnalisé pour le contenu local, contrôle Canvas avec un paramètre, ferme les identifiants d'action A2UI et actualise la capacité de l'hôte A2UI.
- Mauvaises qualités : La fonctionnalité dépend des URL d'hôte canvas Gateway, des listes d'autorisation de plateforme de nœud, du timing de chargement WKWebView, du comportement du schéma personnalisé et de la compatibilité de version A2UI ; les résultats récents de l'archive sont directement visibles par l'utilisateur.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la Qualité.

## Score de Complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'ouverture/fermeture/navigation/évaluation/snapshot du panneau Canvas, le schéma d'URL personnalisé local, la navigation automatique de l'hôte A2UI, le paramètre d'activation/désactivation de Canvas.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Besoin de preuve A2UI push en direct de Gateway via le nœud macOS dans WKWebView.
- Besoin de parité de liste d'autorisation de plateforme et de déclaration de commande de nœud pour rester couvert dans la fumée de version.
- Besoin de docs pour la compatibilité A2UI v0.8/v0.9 et les modes d'échec attendus.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/canvas.md` documente le stockage Canvas, le schéma d'URL personnalisé, le comportement du panneau, l'API d'agent, les commandes A2UI v0.8, les liens profonds et les notes de sécurité.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` répertorie les commandes Canvas comme capacités du nœud macOS.
- `/Users/kevinlin/code/openclaw/docs/web/webchat.md` est lié par les surfaces visuelles/chat partagées mais n'est pas le doc Canvas principal.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/CanvasManager.swift` crée/réutilise les panneaux, navigue automatiquement vers A2UI, suit l'URL de l'hôte canvas Gateway et actualise le statut de débogage.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/CanvasWindowController.swift` crée WKWebView, gestionnaire de schéma personnalisé, observateur de fichiers, pont d'action A2UI et comportement du panneau/fenêtre.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/CanvasSchemeHandler.swift` sert le contenu racine de session et bloque les échappements.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/NodeMode/MacNodeRuntime.swift` distribue les commandes de nœud `canvas.*` et `canvas.a2ui.*`.

### Tests d'intégration

- Aucun scénario complet d'invocation de nœud Gateway vers Canvas WKWebView en direct n'a été trouvé.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/CanvasWindowSmokeTests.swift` ouvre et ferme le contrôleur de fenêtre natif, mais ne prouve pas la livraison Gateway.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/CanvasIPCTests.swift` couvre les allers-retours Canvas IPC codables.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/CanvasFileWatcherTests.swift` couvre le comportement de l'observateur de fichiers.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/MacNodeRuntimeTests.swift` couvre l'actualisation de l'URL de l'hôte A2UI.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/LowCoverageHelperTests.swift` couvre le service de fichiers de schéma personnalisé et le blocage d'échappement de lien symbolique.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS canvas A2UI node" --json`

Résultats :

- Problème #81159 `canvas.a2ui.push / canvas.a2ui.pushJSONL retourne ok mais la charge utile n'atteint jamais le moteur de rendu WKWebView`.
- Problème #86707 `les commandes canvas.* déclarées par le nœud macOS sont bloquées par la liste d'autorisation de plateforme gateway`.
- PR #62021 `fix(macos): réécrire l'hôte A2UI avec caractères génériques vers loopback`.
- PR #86729 `fix(gateway): ajouter les commandes canvas à la liste d'autorisation de plateforme macOS`.
- Le problème #83958 inclut la liste des commandes de nœud d'application macOS et le comportement de délai d'expiration.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS canvas A2UI"`

Résultats :

- 2026-04-30 la liste de report du responsable marque #75039 `fix(macos): garder le contenu canvas A2UI visible` comme devant être reporté.
- 2026-04-25 le miroir GitHub ferme #62609 après l'accès canvas/A2UI limité aux capacités.
- 2026-04-15 le miroir GitHub ouvre #66983 demandant un support plus large du nœud canvas web.
