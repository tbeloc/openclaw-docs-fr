---
title: "Application compagnon Linux - Note de maturité des capacités de bureau"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon Linux - Note de maturité des capacités de bureau

## Résumé

Aucune permission d'application compagnon Linux prise en charge, modèle de stockage de secrets ou de sandbox n'existe dans la documentation ou le code source vérifiés. La documentation existante est solide pour TCC macOS et les approbations d'exécution génériques, tandis que les PR Linux ouvertes identifient l'examen de sécurité, l'identité TLS/appareil, la persistance des jetons et l'empaquetage comme non résolus.

## Portée de la catégorie

Inclus dans cette catégorie :

- Permissions de bureau Linux : permissions de bureau Linux pour les notifications, le microphone, l'écran, la caméra, l'accessibilité, les portails et les API d'environnement de bureau
- Stockage de secrets : stockage de secrets pour le jeton Gateway, l'identité de l'appareil, le jeton de socket d'approbation et les paramètres d'application
- Posture de sandbox/paquet : posture de sandbox/paquet pour Flatpak/Snap/AppImage ou paquets système
- Identité de nœud native Linux : identité de nœud native Linux et annonce de capacité
- Exécution de commandes hôte : exécution de commandes hôte via system.run et outils de bureau associés
- Outils de bureau : outils de bureau tels que l'écran, la caméra, les notifications, Canvas et l'exécution de commandes locales
- Talk natif Linux : Talk natif Linux, push-to-talk, activation vocale et transcription
- Capture de microphone : capture de microphone, capture d'écran/caméra, détection de contexte de bureau et flux de pièces jointes multimédias locales
- Permissions multimédias natives : permissions multimédias natives et comportement au premier plan/arrière-plan

## Fonctionnalités

- Permissions de bureau Linux : permissions de bureau Linux pour les notifications, le microphone, l'écran, la caméra, l'accessibilité, les portails et les API d'environnement de bureau
- Stockage de secrets : stockage de secrets pour le jeton Gateway, l'identité de l'appareil, le jeton de socket d'approbation et les paramètres d'application
- Posture de sandbox/paquet : posture de sandbox/paquet pour Flatpak/Snap/AppImage ou paquets système
- Identité de nœud native Linux : identité de nœud native Linux et annonce de capacité
- Exécution de commandes hôte : exécution de commandes hôte via system.run et outils de bureau associés
- Outils de bureau : outils de bureau tels que l'écran, la caméra, les notifications, Canvas et l'exécution de commandes locales
- Talk natif Linux : Talk natif Linux, push-to-talk, activation vocale et transcription
- Capture de microphone : capture de microphone, capture d'écran/caméra, détection de contexte de bureau et flux de pièces jointes multimédias locales
- Permissions multimédias natives : permissions multimédias natives et comportement au premier plan/arrière-plan

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (0%)`
- Signaux positifs : l'approbation d'exécution générique et la documentation de sécurité existent pour l'exécution hôte.
- Signaux négatifs : aucune invite de permission d'application Linux, intégration de stockage de secrets, modèle de portail, profil de sandbox ou manifeste de permission de paquet n'existe dans le code source actuel.
- Lacunes d'intégration : aucune preuve de permission compagnon Linux ou d'exécution de secrets n'existe.

## Score de qualité

- Score : `Expérimental (24%)`
- Rapports Gitcrawl : la requête de permission Linux/Secret Service/Wayland/X11 n'a retourné aucun résultat direct ; la PR ouverte #61576 signale l'examen de sécurité, l'identité de l'appareil, la vérification TLS et la persistance des jetons comme lacunes connues.
- Rapports Discrawl : la même requête de fonctionnalité n'a retourné aucune preuve de permission compagnon Linux directe.
- Bonnes qualités : la documentation actuelle évite de prétendre au support des permissions Linux et les PR ouvertes identifient ouvertement les préoccupations de sécurité.
- Mauvaises qualités : il n'existe pas de carte de permission Linux publique, de décision de magasin de secrets, de posture portail/sandbox, de modèle de compatibilité d'environnement de bureau ou de sémantique de secours sûre.
- Exclus de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Expérimental (0%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les permissions de bureau Linux, le stockage de secrets, la posture de sandbox/paquet, l'identité de nœud native Linux, l'exécution de commandes hôte, les outils de bureau, le Talk natif Linux, la capture de microphone et les permissions multimédias natives.
- Signaux négatifs : la note archivée a précédé le score de complétude du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Décider si les secrets Linux utilisent Secret Service, le stockage chiffré sauvegardé par fichier ou les références de configuration Gateway.
- Définir les invites de permission et les codes d'erreur pour les notifications, le micro, l'écran, la caméra et le contrôle de bureau.
- Définir les attentes de sécurité du sandbox/paquet avant les téléchargements officiels.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/permissions.md:11` : les octrois de permission macOS sont liés à la signature de code, à l'identifiant de bundle et au chemin.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md:16` : l'application macOS possède les invites Notifications, Accessibilité, Enregistrement d'écran, Microphone, Reconnaissance vocale et Automatisation.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md:11` : les approbations d'exécution sont une barrière de sécurité d'application compagnon / hôte de nœud pour l'exécution d'hôte réel.
- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:13` : les applications compagnon Linux natives sont prévues, sans modèle de permission Linux documenté.

### Source

- Aucun Secret Service Linux, portail XDG, permission Wayland/X11, manifeste Flatpak, confinement Snap ou code de sandbox d'application Linux n'existe dans le checkout actuel.
- `/Users/kevinlin/code/openclaw/src/infra/exec-approvals.ts` et les fichiers associés implémentent les approbations d'exécution hôte génériques, pas les permissions d'application de bureau Linux.

### Tests d'intégration

- Aucun test d'intégration de permission compagnon Linux, stockage de secrets, portail ou sandbox n'a été trouvé.
- Les tests de sécurité existants couvrent le comportement générique d'exécution/configuration et d'autres plates-formes d'application.

### Tests unitaires

- Aucun test unitaire de permission compagnon Linux ou de secrets n'a été trouvé.
- Les tests d'approbation d'exécution génériques sont adjacents, pas une preuve d'application Linux.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Linux companion permissions Secret Service portal Wayland X11" --mode keyword --limit 8 --json`
- `gitcrawl gh pr view 61576 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`
- `gitcrawl gh pr view 59859 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`

Résultats :

- La requête de fonctionnalité n'a retourné aucun résultat.
- La PR #61576 énumère l'examen de sécurité nécessaire pour la gestion de l'identité de l'appareil, le flux de vérification TLS et la persistance des jetons.
- La PR #59859 indique que le compagnon Linux introduit une nouvelle surface de bureau native avec contexte d'exécution local, état du service, connexions Gateway, édition de configuration et mutations de gestion ; elle reste ouverte.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux companion permissions Secret Service portal Wayland X11"`

Résultats :

- La requête de fonctionnalité n'a retourné aucun résultat direct.
- L'absence de rapports directs est neutre après les vérifications de fraîcheur, mais elle ne fournit aucun signal positif pour un modèle de permission Linux ou de secrets pris en charge.
