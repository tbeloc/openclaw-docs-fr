---
title: "Application compagne macOS - Note de maturité du statut du menu et du tableau de bord"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne macOS - Note de maturité du statut du menu et du tableau de bord

## Résumé

La surface de la barre de menu est un shell d'opérateur complet pour les bascules, les résumés de santé, l'état du nœud/appairage, l'utilisation, WebChat, Canvas, Talk, les paramètres, les actions de débogage et les raccourcis du dock. La couverture est Beta car le shell de menu est large et rendu sur plusieurs modes de connexion en couverture de fumée, mais il n'existe pas de scénario de statut de menu en direct complet qui pilote le travail de l'agent, l'état du nœud, la santé et les actions du tableau de bord ensemble. La qualité est Beta avec un risque visible provenant des rapports d'archive concernant les icônes en double, le scintillement des identifiants et les blocages du chat natif.

## Portée de la catégorie

- Statut de la barre de menu, menu d'action, état de l'icône de statut, menu du dock, raccourcis du tableau de bord/chat/canvas/talk.
- Ingestion de l'état d'activité et comportement de la ligne de statut.
- Hors de portée : éléments internes du tableau de bord de l'interface utilisateur de contrôle du navigateur.

## Fonctionnalités

- Statut de la barre de menu : Statut de la barre de menu, menu d'action, état de l'icône de statut, menu du dock, raccourcis du tableau de bord/chat/canvas/talk
- Ingestion de l'état d'activité : Ingestion de l'état d'activité et comportement de la ligne de statut

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`
- Signaux positifs : La documentation spécifie le comportement de la ligne de statut et de l'icône. La source rend les bascules de menu et les raccourcis en modes local, distant et non configuré. Les tests de fumée construisent le contenu du menu et les raccourcis du dock.
- Signaux négatifs : La couverture ne prouve pas l'ingestion réelle des événements d'agent, les transitions de santé, les invites d'appairage, les instantanés d'utilisation et les actions du tableau de bord/WebChat/Canvas dans une application en cours d'exécution.
- Lacunes d'intégration : Absence d'un scénario d'application macOS en direct qui pilote un travail de session principale, un travail non-principal, une dégradation de la santé, une approbation d'appairage, l'ouverture de WebChat, l'ouverture de Canvas et l'ouverture du tableau de bord à partir du menu.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : Les résultats de requête incluent la PR #82739 pour les icônes de barre de menu en double, le problème #85352 pour le scintillement de la porte des identifiants à l'ouverture du menu et le problème #71586 pour le blocage de l'interface utilisateur du chat de l'application compagne lors de l'utilisation du menu de la barre de statut.
- Rapports Discrawl : La recherche Discord pour `macOS menu bar` a surtout surfacé des discussions adjacentes sur les applications de barre de menu, pas un cluster de support OpenClaw à haut volume.
- Bonnes qualités : La source du menu garde les contrôles communs près de l'élément de statut, masque la santé pendant que le travail est actif, sépare les appareils des entrées de présence et expose les actions de débogage derrière un volet de débogage.
- Mauvaises qualités : Les rapports d'archive montrent que des régressions du shell de menu/application natif se sont produites, et la correction du statut dépend de plusieurs magasins asynchrones se mettant à jour ensemble.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le statut de la barre de menu, l'ingestion de l'état d'activité.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin d'un scénario de statut/icône déterministe pour les événements d'agent, la santé, l'appairage des nœuds et les instantanés d'utilisation.
- Besoin d'une orientation d'opérateur plus claire lorsque le menu affiche un état dégradé mais le tableau de bord, WebChat ou le service de nœud ne sont pas d'accord.
- Besoin de preuve de régression récurrente pour les éléments de statut en double et le scintillement de la porte des identifiants.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/menu-bar.md` définit l'état de travail visible du menu, le sous-menu de contexte, la ligne d'utilisation, la priorité de statut, l'ingestion d'événements et la liste de contrôle de test.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/icon.md` décrit le comportement de l'icône de travail/inactivité et le remplacement de débogage.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` répertorie les notifications natives et le statut de la barre de menu comme des fonctionnalités d'application de première classe.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/MenuContentView.swift` rend l'état de connexion, la santé, l'état du nœud, les invites d'appairage, les bascules navigateur/caméra/exec/canvas/voix, les actions du tableau de bord/chat/canvas/talk, les paramètres, les actions de débogage et la fermeture.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/IconState.swift` mappe les états de travail principal/autre aux symboles de badge et à l'état de travail.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/AppNavigationActions.swift` achemine les actions du menu vers le tableau de bord, le chat et Canvas.

### Tests d'intégration

- Aucun scénario d'intégration de statut de menu d'application en direct dédié n'a été trouvé.
- `/Users/kevinlin/code/openclaw/test/scripts/package-mac-app.test.ts` couvre uniquement le comportement du script de package pertinent pour les artefacts de lancement d'application.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/MenuContentSmokeTests.swift` construit le contenu du menu en états local, distant, non configuré, débogage/canvas et vérifie les raccourcis du menu du dock.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/CritterIconRendererTests.swift` et `MasterDiscoveryMenuSmokeTests.swift` couvrent les surfaces d'interface utilisateur adjacentes d'icône/découverte.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS menu bar" --json`

Résultats :

- PR #82739 `fix(macos): prevent duplicate menu bar icons`.
- Problème #85352 `macOS menu bar app flashes credentials gate on open`.
- Problème #71586 `macOS companion app chat UI hangs when dragging scrollbar thumb up and down`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS menu bar"`

Résultats :

- La recherche a surtout retourné des discussions adjacentes sur les applications de barre de menu, pas un cluster de support OpenClaw direct.
- Aucun cluster de confusion d'opérateur de statut de menu à haut volume direct n'est apparu dans les cinq premiers résultats.
