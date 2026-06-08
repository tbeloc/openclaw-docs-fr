---
title: "Fournisseurs hébergés long-tail - Note de maturité des diagnostics de fournisseur et de réparation de secours"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs hébergés long-tail - Note de maturité des diagnostics de fournisseur et de réparation de secours

## Résumé

La fumée en direct, les diagnostics et la réparation de secours sont en Alpha. OpenClaw dispose de couches de test en direct utiles, de sondes d'authentification, de compartiments de statut de fournisseur et de comportement de secours, mais la preuve est opt-in, dépendante des identifiants et dispersée dans le modèle direct, la passerelle, les médias et les suites spécifiques aux fournisseurs.

## Portée de la catégorie

Cette note couvre la fumée en direct du fournisseur/modèle, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut, le comportement de secours du fournisseur, la gestion des modèles non trouvés, le diagnostic des délais d'expiration et les indices de réparation opérationnelle pour les fournisseurs hébergés long-tail.

Hors de portée : diagnostics de canal non-fournisseur, réparation du cycle de vie d'installation des plugins et runtimes de modèles locaux uniquement.

## Fonctionnalités

- Fumée directe du fournisseur : Couvre la fumée directe du fournisseur dans la fumée en direct du fournisseur/modèle direct, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement de diagnostic et de réparation de secours du fournisseur associé.
- Fumée en direct de la passerelle : Couvre la fumée en direct de la passerelle dans la fumée en direct du fournisseur/modèle direct, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement de diagnostic et de réparation de secours du fournisseur associé.
- Sondes de statut des modèles : Couvre les sondes de statut des modèles dans la fumée en direct du fournisseur/modèle direct, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement de diagnostic et de réparation de secours du fournisseur associé.
- Trace de secours et réparation : Couvre la trace de secours et la réparation dans la fumée en direct du fournisseur/modèle direct, la fumée du profil en direct de la passerelle, `models status --probe`, les compartiments d'authentification/statut et le comportement de diagnostic et de réparation de secours du fournisseur associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs :
  - Les docs en direct séparent la complétion du modèle direct de la fumée complète de la passerelle+agent.
  - La fumée en direct de la passerelle supporte les filtres de fournisseur, le mode fumée, le mode clé de profil, les sondes d'outils, les sondes d'image et les contrôles de délai d'expiration.
  - `models status --probe` documente les vraies sondes de fournisseur et les compartiments de statut.
  - Le harnais en direct des médias exécute les suites partagées d'image, de musique et de vidéo.
  - Des tests en direct spécifiques aux fournisseurs existent pour les fournisseurs de texte, de médias et d'audio hébergés sélectionnés.
- Signaux négatifs :
  - Les tests en direct sont opt-in et dépendent des clés, des comptes et de la disponibilité du fournisseur.
  - Les docs évitent explicitement une liste de modèles CI fixe.
  - Les preuves de secours et de diagnostic sont distribuées dans de nombreuses suites et rapports d'utilisateurs plutôt que dans une voie de sortie de fournisseur long-tail unique.

## Score de qualité

- Score : `Alpha (60%)`
- Bonnes qualités :
  - Les diagnostics distinguent l'échec du fournisseur/modèle direct de l'échec du pipeline passerelle+agent.
  - Les compartiments de sonde séparent les cas d'authentification, de limite de débit, de facturation, de délai d'expiration, de format, inconnu et sans modèle.
  - La configuration de fumée de la passerelle peut forcer le mode clé de profil et réduire les fournisseurs/modèles pour un débogage ciblé.
  - L'historique d'archive montre que les défaillances de secours, de délai d'expiration et d'authentification sont suffisamment visibles pour être diagnostiquées.
- Mauvaises qualités :
  - L'expérience de l'opérateur nécessite toujours de savoir quelle voie de diagnostic correspond à quelle famille de fournisseurs.
  - Le comportement de la chaîne de secours peut surprendre les utilisateurs lorsqu'un modèle sélectionné échoue et qu'un fournisseur de secours prend le relais.
  - La disponibilité du fournisseur peut échouer en raison de la disponibilité du modèle spécifique au compte, de mauvaises URL de base, d'authentification manquante, de quotas et de délais d'expiration en amont.
- Exclus de la qualité :
  - Les preuves unitaires, d'intégration et en direct ont été utilisées uniquement pour le score de couverture.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/long-tail-hosted-providers.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la fumée du fournisseur direct, la fumée en direct de la passerelle, les sondes de statut des modèles, la trace de secours et la réparation.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un manifeste de fumée de sortie de fournisseur hébergé unique avec un modèle ou une capacité curatée par famille de fournisseurs.
- Ajouter une UX de trace de secours qui affiche le modèle sélectionné, la première défaillance, le modèle de secours et si le secours était configuré par l'utilisateur ou automatique.
- Ajouter des diagnostics de fournisseur qui lient le compartiment d'authentification, le compartiment de modèle et la dernière preuve de fumée en direct.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:58` : la fumée du modèle en direct a deux couches, le modèle direct et la fumée de la passerelle.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:62` : le modèle direct indique si le fournisseur/modèle peut répondre avec la clé donnée.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:63` : la fumée de la passerelle prouve le pipeline complet passerelle+agent.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:94` : la fumée de la passerelle lance une passerelle en processus.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:98` : la fumée de la passerelle itère les modèles avec clés et affirme des réponses significatives, l'invocation d'outils, les sondes d'outils supplémentaires et les chemins de régression OpenAI.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:374` : les docs indiquent qu'il n'y a pas de liste de modèles CI fixe.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:573` : le harnais en direct des médias exécute les suites partagées d'image, de musique et de vidéo.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md:37` : `models status --probe` exécute des requêtes de fournisseur réelles.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md:138` : les compartiments de sonde incluent `ok`, `auth`, `rate_limit`, `billing`, `timeout`, `format`, `unknown` et `no_model`.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:66` : le test en direct de la passerelle supporte le secours ZAI et la précédence de la clé de profil.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:69` : le test en direct de la passerelle supporte le filtrage des fournisseurs via `OPENCLAW_LIVE_GATEWAY_PROVIDERS`.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:70` : le mode fumée de la passerelle en direct est contrôlé par `OPENCLAW_LIVE_GATEWAY_SMOKE`.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:75` : les sondes d'outils et d'images supplémentaires sont désactivées en mode fumée.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:120` : la suite en direct de la passerelle est contrôlée par `OPENCLAW_LIVE_GATEWAY`.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:3034` : la suite en direct de la passerelle exécute des invites significatives sur les modèles avec des clés disponibles.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:3039` : la suite en direct de la passerelle enregistre la sélection du fournisseur et charge la configuration avant de préparer les modèles.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:67` : le test en direct du modèle direct est `src/agents/models.profiles.live.test.ts`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:94` : le test en direct de la passerelle est `src/gateway/gateway-models.profiles.live.test.ts`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:467` : le test en direct d'image est `test/image-generation.runtime.live.test.ts`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:514` : le test en direct de musique est `extensions/music-generation-providers.live.test.ts`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:538` : le test en direct de vidéo est `extensions/video-generation-providers.live.test.ts`.
- `/Users/kevinlin/code/openclaw/extensions/deepseek/deepseek.live.test.ts:80` : le test en direct spécifique au fournisseur couvre le texte assistant DeepSeek.
- `/Users/kevinlin/code/openclaw/extensions/together/together.live.test.ts:47` : le test en direct spécifique au fournisseur couvre les modèles de catalogue Together.
- `/Users/kevinlin/code/openclaw/extensions/elevenlabs/elevenlabs.live.test.ts:27` : le test en direct spécifique au fournisseur couvre la parole ElevenLabs.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/model-selection.test.ts:933` : la couverture unitaire superpose les métadonnées du fournisseur configuré et les alias sur les entrées du catalogue.
- `/Users/kevinlin/code/openclaw/src/agents/model-selection.test.ts:1289` : la couverture unitaire applique les métadonnées du fournisseur et les alias aux entrées de liste d'autorisation synthétique.
- `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.test.ts:1751` : la couverture unitaire préserve les métadonnées du fournisseur de compréhension et de génération de médias.
- `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.test.ts:2142` : la couverture unitaire évite de promouvoir les champs de capacité de niveau supérieur hérités dans les contrats.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "provider fallback error timeout auth missing model"` a retourné #84384, #81213, #87744, #79380 et #86567.
- #81213 signale les délais d'expiration primaires OpenAI et le comportement de trace de secours incohérent, une préoccupation de diagnostic de secours adjacente.
- `gitcrawl --json search prs -R openclaw/openclaw "provider fallback error timeout auth missing model"` a retourné les PR incluant #84867, #62682, #44167, #81834, #86670 et #87141.
- #84867 est pertinent car il permet à un modèle commuté par l'utilisateur d'utiliser la chaîne de secours de l'agent.
- #62682 est pertinent car il distingue les abandons terminaux des défaillances réessayables.

### Requêtes Discrawl

- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "provider fallback error timeout auth missing model" --limit 5` a retourné les journaux de modèle non trouvé avec quota primaire dépassé, authentification manquante, fournisseur local inaccessible, troncature de contexte, délai d'expiration, tentatives épuisées et secours vers OpenAI Codex.
- La même recherche Discrawl a retourné une erreur de bot où tous les modèles ont échoué, y compris les délais d'expiration et l'authentification 401 sur `minimax-portal`.
- La même recherche Discrawl a retourné des conseils pour un utilisateur dont le modèle Kimi sélectionné a immédiatement basculé vers Cerebras/ZAI, y compris la vérification de `/model status` et des journaux pour 401/429/timeout/mauvaise URL de base.
