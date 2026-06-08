---
title: "Application compagnon macOS - Note de maturité des permissions, confidentialité et Tcc"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon macOS - Note de maturité des permissions, confidentialité et Tcc

## Résumé

L'application dispose d'un modèle de permission clair : l'application signée possède les invites TCC et signale l'état des permissions aux agents. Elle couvre les notifications, l'accessibilité, l'enregistrement d'écran, le microphone, la reconnaissance vocale, l'automatisation/AppleScript, la caméra et la localisation. La couverture est Alpha car l'état des permissions et les chemins des paramètres sont implémentés, mais aucune matrice TCC d'invite en direct n'a été trouvée. La qualité est Alpha car la source et la documentation sont réfléchies, mais les preuves d'archive montrent que les incompatibilités de portée TCC, de contexte launchd et de liste blanche de plateforme restent des risques récurrents.

## Portée des catégories

- Demandes de permission, interrogation d'état, interface utilisateur des paramètres et annonce de permission de nœud.
- Persistance TCC, exigences de signature et conseils de permission sécurisée appartenant à l'application.
- Hors de portée : bogues du système d'exploitation en amont et modèles de permission non-macOS.

## Fonctionnalités

- Demandes de permission : demandes de permission, interrogation d'état, interface utilisateur des paramètres et annonce de permission de nœud
- Persistance TCC : persistance TCC, exigences de signature et conseils de permission sécurisée appartenant à l'application

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs : la documentation explique la persistance TCC et la récupération. La source implémente des vérifications de permission interactives et non interactives pour toutes les capacités majeures et expose une page de paramètres avec comportement d'actualisation/nouvelle tentative. Les tests interrogent l'état de permission non interactif et le rendu des paramètres.
- Signaux négatifs : aucun scénario TCC d'invite d'application signée en direct n'a été trouvé. Les tests ne prouvent pas les invites réelles d'accessibilité, d'enregistrement d'écran, de parole, de microphone, de caméra, de localisation, d'automatisation et de notification sur les identités d'application propres/reconstruites.
- Lacunes d'intégration : besoin d'une matrice de permission d'application signée sur la première installation, la reconstruction, le changement de chemin d'application, le mode distant, le service de nœud et le contexte de processus LaunchAgent.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : les résultats incluent le problème #69799 concernant un binaire Node dédié/fourni pour la portée des permissions TCC, le problème #78049 concernant Gateway géré par launchd accédant aux dossiers protégés par TCC, le problème #57169 concernant le nœud macOS annonçant la capacité d'écran tandis que le runtime bloque `screen.record` et le problème #79289 concernant la permission d'automatisation attribuée au wrapper SSH.
- Rapports Discrawl : l'archive Discord inclut la discussion #69799 confirmant que TCC s'étend au chemin binaire et la fermeture #69561 indiquant que le modèle TCC appartenant à l'application est plus sûr. Elle inclut également la note SRE #71848 reliant launchd, la session Aqua, la pression mémoire et le blocage TCC du processus spawn.
- Bonnes qualités : la documentation avertit fortement contre l'octroi de l'accessibilité à un runtime `node` générique, la source garde les invites dans l'application et les permissions sont annoncées aux agents via la carte de permission de nœud.
- Mauvaises qualités : le comportement des permissions dépend de l'identité de signature, du chemin du bundle, du contexte du processus, de l'origine LaunchAgent/SSH et des listes blanches de commandes de plateforme. Les utilisateurs peuvent toujours rencontrer une incompatibilité « permission accordée mais commande bloquée ».
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les demandes de permission et la persistance TCC.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin de preuve TCC d'invite en direct pour toutes les capacités annoncées de l'application empaquetée.
- Besoin d'un chemin d'opérateur qui distingue la permission du système d'exploitation manquante du déni de liste blanche Gateway/plateforme.
- Besoin de preuve de version que les octrois de permission survivent aux reconstructions signées, aux mises à jour et aux hypothèses de stabilité du chemin d'application.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/permissions.md` documente les exigences de persistance TCC, l'identité d'application signée, le risque d'accessibilité pour le Node générique, la liste de contrôle de récupération et les permissions de fichiers/dossiers.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` indique que l'application possède les invites TCC et expose les outils macOS uniquement tout en signalant une carte de permission.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/signing.md` lie la signature et l'identité de bundle fixe à la persistance des permissions.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/peekaboo.md` documente l'automatisation de l'interface utilisateur consciente des permissions via le bundle d'application.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/PermissionManager.swift` implémente l'assurance/statut de permission pour les notifications, AppleScript, l'accessibilité, l'enregistrement d'écran, le microphone, la reconnaissance vocale, la caméra et la localisation.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/PermissionsSettings.swift` rend le résumé, les boutons de demande par capacité, le comportement d'actualisation et le redémarrage d'intégration.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/NodeMode/MacNodeModeCoordinator.swift` construit la carte `permissions` du nœud à partir de `PermissionManager.status()`.

### Tests d'intégration

- Aucune matrice de permission TCC complète en direct n'a été trouvée.
- Les tests de script d'empaquetage/signature vérifient l'hygiène du script liée à la signature mais n'exercent pas les invites de permission macOS.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/PermissionManagerTests.swift` couvre le comportement du helper de permission non interactif et la forme de requête d'état.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/PermissionManagerLocationTests.swift` couvre le comportement du helper d'autorisation de localisation.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/SettingsViewSmokeTests.swift` rend `PermissionsSettings`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS TCC" --json`

Résultats :

- Problème #69799 `Livrer un binaire Node dédié/fourni pour que les permissions TCC macOS soient limitées à OpenClaw uniquement`.
- Problème #78049 `Gateway géré par launchd macOS ne peut pas accéder de manière fiable aux dossiers protégés par TCC via les outils CLI`.
- Problème #57169 `Le nœud macOS annonce la capacité d'écran mais le runtime bloque screen.record via la liste blanche de plateforme`.
- Problème #79289 `Le modèle iMessage remote-SSH peut échouer lorsque macOS attribue la permission d'automatisation à sshd-keygen-wrapper`.

Requête :

`gitcrawl search openclaw/openclaw --query "screen.record macOS node permissions" --json`

Résultats :

- Le problème #57169 et le problème sœur #86707 montrent les capacités de nœud macOS annoncées bloquées par la liste blanche de plateforme.
- Le problème #83958 signale le flottement du nœud d'application macOS et les délais d'expiration d'invocation de Gateway.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS permissions TCC"`

Résultats :

- Le commentaire du miroir GitHub du 2026-04-25 sur #69561 indique que main actuel documente le modèle de permission TCC plus sûr appartenant à l'application.
- Le commentaire du miroir GitHub du 2026-04-22 sur #69799 indique que la portée TCC au binaire Node est un vrai problème de sécurité.
- Le miroir SRE du 2026-04-26 sur #71848 lie l'échec de launchd aux problèmes de contexte de processus TCC/Aqua/session.
