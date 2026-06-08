---
title: "Application compagne Windows native - Note de maturité des sessions de chat"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Windows native - Note de maturité des sessions de chat

## Résumé

Les utilisateurs Windows ont bénéficié de chemins d'accès supportés via l'interface de contrôle du navigateur/WebChat et CLI chat, mais la branche principale actuelle ne fournit pas de client de chat compagne Windows natif. Les recherches d'une WebChat compagne Windows n'ont pas trouvé de preuves pertinentes dans les archives. Ce composant est effectivement non implémenté pour la surface sélectionnée.

## Portée de la catégorie

Inclus dans cette catégorie :

- Fenêtre de chat Windows native : Fenêtre de chat Windows native, transcription, compositeur, sélecteur de session, contrôles de modèle/réflexion, actions d'abandon/suivi, gestion de la reconnexion et rendu des outils
- Transport de chat Gateway : Transport de chat Gateway et contrôle de session depuis l'application Windows native.

## Fonctionnalités

- Fenêtre de chat Windows native : Fenêtre de chat Windows native, transcription, compositeur, sélecteur de session, contrôles de modèle/réflexion, actions d'abandon/suivi, gestion de la reconnexion et rendu des outils
- Transport de chat Gateway : Transport de chat Gateway et contrôle de session depuis l'application Windows native.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (0%)`
- Signaux positifs : des surfaces Gateway chat et WebChat navigateur réutilisables existent en dehors de ce composant.
- Signaux négatifs : aucune fenêtre de chat Windows native, transport, interface utilisateur de session, état d'application ou validation de chat spécifique à l'application n'existe.
- Lacunes d'intégration : aucun cycle de vie de chat d'application Windows ne peut être lancé, envoyé, reconnecté ou validé.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Expérimental (25%)`
- Rapports Gitcrawl : la requête spécifique à la fonctionnalité `Windows companion chat WebChat` n'a retourné aucun résultat.
- Rapports Discrawl : la requête spécifique à la fonctionnalité `Windows companion chat WebChat` n'a retourné aucun message.
- Bonnes qualités : la documentation actuelle ne prétend pas qu'une application de chat Windows native existe ; les utilisateurs sont dirigés vers les chemins Gateway et tableau de bord supportés.
- Mauvaises qualités : il n'existe pas de contrat UX d'application, d'implémentation, de conception de continuité de session ou de comportement de rendu natif pour Windows.
- Exclus de la qualité : les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer la qualité.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'exhaustivité

- Score : `Expérimental (0%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la fenêtre de chat Windows native, le transport de chat Gateway.
- Signaux négatifs : la note archivée a précédé le scoring d'exhaustivité de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune source ou documentation de client de chat Windows native.
- Aucun sélecteur de session, contrôles de modèle ou contrat de rendu de transcription native.
- Aucun comportement hors ligne/reconnexion spécifique à l'application ou redémarrage de Gateway.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md` dirige les utilisateurs vers les chemins du runbook Gateway et de l'interface de contrôle, pas une interface utilisateur de chat d'application native.
- `/Users/kevinlin/code/openclaw/docs/web/webchat.md` et `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` couvrent les surfaces du navigateur, pas le support d'application native Windows.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-chat.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat.ts` fournissent les primitives de chat Gateway.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawChatUI/` fournit l'interface utilisateur de chat partagée Swift pour les surfaces d'application Apple.
- Aucune source de chat d'application Windows n'a été trouvée.

### Tests d'intégration

- Des tests de chat Gateway existent, mais aucun test d'intégration de chat d'application Windows native n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/server.chat.gateway-server-chat.test.ts`
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Tests/OpenClawKitTests/ChatViewModelTests.swift`
- Aucun test unitaire de chat Windows native n'a été trouvé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows companion chat WebChat" --json`

Résultats :

- Aucun résultat.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows companion chat WebChat"`

Résultats :

- Aucun message.
