---
title: "Chemin du fournisseur OpenAI / Codex - Note de maturité du modèle et de l'authentification"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenAI / Codex - Note de maturité du modèle et de l'authentification

## Résumé

Le routage des modèles canoniques est l'une des parties les mieux couvertes de la surface. La documentation sépare explicitement `openai`, `openai-codex`, le plugin `codex`, la politique d'exécution du fournisseur/modèle et les contrôles `/codex`. La source dispose de fonctions d'assistance dédiées pour la sélection par défaut du runtime Codex, la détection des références héritées, la synthèse dynamique du catalogue OpenAI et Codex, les métadonnées de contexte, la réparation des modèles compatibles avec les images et la réparation des routes du docteur. La qualité reste en version bêta car les preuves d'archive montrent que les utilisateurs rencontrent toujours un état de route `openai-codex/*` obsolète et confondent les noms de fournisseur, d'exécution et d'authentification après les mises à jour.

## Portée de la catégorie

Inclus dans cette catégorie :

- Routage canonique des modèles OpenAI : couvre le routage canonique des modèles OpenAI sur le contrat de route exposé aux utilisateurs/opérateurs : références canoniques `openai/gpt-*`, références de modèles héritées `openai-codex/*`, lignes du catalogue de modèles, limites de contexte et comportement de routage et de catalogue des modèles OpenAI canoniques associés.
- Catalogue : couvre le catalogue sur le contrat de route exposé aux utilisateurs/opérateurs : références canoniques `openai/gpt-*`, références de modèles héritées `openai-codex/*`, lignes du catalogue de modèles, limites de contexte et comportement de routage et de catalogue des modèles OpenAI canoniques associés.
- Profils OAuth Codex : couvre les profils OAuth Codex sur les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation de l'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.
- Utilisation de l'abonnement : couvre l'utilisation de l'abonnement sur les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation de l'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.
- Diagnostics du docteur : couvre les diagnostics du docteur sur la réparation et le diagnostic exposés aux opérateurs pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles d'exécution, barres latérales de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.
- Réparation de l'opérateur : couvre la réparation de l'opérateur sur la réparation et le diagnostic exposés aux opérateurs pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles d'exécution, barres latérales de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.

## Fonctionnalités

- Routage canonique des modèles OpenAI : couvre le routage canonique des modèles OpenAI sur le contrat de route exposé aux utilisateurs/opérateurs : références canoniques `openai/gpt-*`, références de modèles héritées `openai-codex/*`, lignes du catalogue de modèles, limites de contexte et comportement de routage et de catalogue des modèles OpenAI canoniques associés.
- Catalogue : couvre le catalogue sur le contrat de route exposé aux utilisateurs/opérateurs : références canoniques `openai/gpt-*`, références de modèles héritées `openai-codex/*`, lignes du catalogue de modèles, limites de contexte et comportement de routage et de catalogue des modèles OpenAI canoniques associés.
- Profils OAuth Codex : couvre les profils OAuth Codex sur les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation de l'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.
- Utilisation de l'abonnement : couvre l'utilisation de l'abonnement sur les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation de l'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.
- Diagnostics du docteur : couvre les diagnostics du docteur sur la réparation et le diagnostic exposés aux opérateurs pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles d'exécution, barres latérales de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.
- Réparation de l'opérateur : couvre la réparation de l'opérateur sur la réparation et le diagnostic exposés aux opérateurs pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles d'exécution, barres latérales de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : la documentation explique la carte de nommage et le tableau de route ; la source dispose de fonctions d'assistance dédiées pour la route/les valeurs par défaut et des plugins de fournisseur ; les tests unitaires et e2e couvrent l'énumération des modèles, la réparation des routes et le comportement de compatibilité.
- Signaux négatifs : la preuve complète de la voie de publication pour chaque combinaison de catalogue et de migration de route OpenAI/Codex n'est pas visible dans une seule fiche d'évaluation standard.
- Lacunes d'intégration : la survie de la mise à niveau pour les épingles de session obsolètes et les références héritées est toujours prouvée par des tests dispersés du docteur/runtime plus un suivi d'archive plutôt qu'une seule preuve de publication.

## Score de qualité

- Score : `Bêta (70%)`
- Rapports Gitcrawl : les problèmes ouverts #87436, #80628, #84637, #87650, #84200, #84038, #83223 et #84252 impliquent tous une confusion de route OpenAI/Codex, d'exécution, de verbosité de texte ou de docteur/statut.
- Rapports Discrawl : la discussion Discord du 2026-05-17 décrit `openai/gpt-5.5` atteignant incorrectement les réponses OpenAI directes en raison d'épingles de fournisseur/exécution/authentification obsolètes ; un fil de discussion du 2026-04-14 distingue l'utilisation du harnais `openai-codex/*` de `codex/*`.
- Bonnes qualités : la source encode la division fournisseur/exécution au lieu de s'appuyer sur des commentaires de chaîne ; la documentation donne des commandes de récupération concrètes.
- Mauvaises qualités : le nommage est toujours facile à mal lire et l'état de session obsolète peut remplacer la configuration actuelle.
- Exclu de la qualité : la présence d'unité, d'intégration, d'e2e et de test en direct a été utilisée uniquement comme preuve de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le routage canonique des modèles OpenAI, le catalogue, les profils OAuth Codex, l'utilisation de l'abonnement, les diagnostics du docteur, la réparation de l'opérateur.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La réparation des routes a besoin d'une preuve de publication plus forte sur l'état de session persistant, les épingles de profil d'authentification et les épingles d'exécution.
- La sortie de l'opérateur devrait rendre les différences `openai/*`, `openai-codex/*` et `codex/*` difficiles à manquer.
- Le score dépend du comportement actuel du catalogue du fournisseur, qui change fréquemment.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente la réparation canonique `openai/*`, héritée `openai-codex/*`, la carte de nommage, les résumés de route, les plafonds de contexte GPT-5.5 et la récupération du catalogue.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness.md` documente les références de modèle `openai/gpt-*` recommandées, la sélection d'exécution, la vérification `/status` et la distinction par rapport à ACP/acpx.
- `/Users/kevinlin/code/openclaw/docs/concepts/models.md` documente la séparation modèle/fournisseur/exécution utilisée par ce chemin.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/openai-codex-routing.ts` implémente la détection du fournisseur OpenAI, la valeur par défaut de l'URL de base officielle au runtime Codex, la sélection du fournisseur d'authentification et la normalisation de la route/fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/openai/openai-provider.ts` synthétise les lignes GPT OpenAI modernes, les fenêtres de contexte, l'entrée multimédia et les métadonnées de transport des réponses.
- `/Users/kevinlin/code/openclaw/extensions/openai/openai-codex-provider.ts` normalise les champs de transport Codex, synthétise les lignes de modèle Codex, restaure la capacité d'entrée d'image et expose le comportement d'utilisation/authentification de Codex.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/codex-route-warnings.ts` détecte et répare la configuration héritée `openai-codex/*` et l'état de route d'exécution/session obsolète.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` exerce le comportement de la liste des modèles, les lignes du catalogue du fournisseur, la visibilité de l'authentification et le rapport d'échec du catalogue.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.run-embedded-agent.auth-profile-rotation.e2e.test.ts` couvre le comportement de secours du modèle/fournisseur et la rotation du profil d'authentification dans les exécutions intégrées.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-codex-harness.live.test.ts` contient des sondes de routage du harnais Codex en direct optionnelles.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/model-runtime-policy.ts` est couvert par les tests de politique d'exécution adjacents pour la sélection d'exécution du modèle/fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/openai/openai-provider.test.ts` et `extensions/openai/openai-codex-provider.test.ts` couvrent la normalisation du fournisseur et le comportement du modèle Codex.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/codex-route-warnings.test.ts` couvre la réparation du docteur de l'état de route Codex hérité.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "openai gpt-5.5 codex runtime openai/gpt openai-codex route doctor"`

Résultats :

- A retourné les problèmes ouverts #87436, #80628, #84637, #87650, #84200, #84038, #83223, #84252, #81213 et #87168, y compris la récréation de route obsolète, la dérive de route protégée, la confusion d'exécution/modèle Codex et les échecs de récupération du docteur/statut.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "openai-codex doctor route auth profile Codex harness"`

Résultats :

- A retourné la PR #81700, `fix(auth): drop stale Codex OAuth routing`, plus les travaux de fournisseur-exécution adjacents.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "openai gpt-5.5 codex runtime openai/gpt openai-codex route doctor"`

Résultats :

- A retourné une discussion de mainteneur du 2026-05-17 décrivant l'état de route persistant obsolète et la sélection des réponses OpenAI directes pour `openai/gpt-5.5`, plus les notes du 2026-05-10 et 2026-05-09 autour de la PR #80017 et l'authentification par clé API OpenAI directe atteignant toujours la configuration OAuth uniquement.

Requête : `discrawl search --limit 10 "codex app-server harness thread compact /codex status native codex"`

Résultats :

- A retourné une discussion du 2026-04-14 distinguant `openai-codex/*` comme le chemin du fournisseur OAuth Codex de `codex/*` comme le harnais natif du serveur d'application, y compris l'utilisation et les compromis de compaction.
