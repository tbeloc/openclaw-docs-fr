---
title: "Rapport de maturité des outils de recherche Web"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité des outils de recherche Web

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (79%)`
- Qualité : `Beta (76%)`
- Complétude : `Beta (79%)`
- Fonctionnalités LTS : `0/4`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `web-search-tools` de `/Users/kevinlin/tmp/maturity/web-search-tools` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                            | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Fournisseurs de recherche](bundled-structured-search-providers.md)                          | ❌  | `Beta (76%)`   | `Beta (72%)`   | `Beta (76%)`   | Fournisseurs soutenus par API, Fournisseurs sans clé et auto-hébergés, Comparaison et détection automatique des fournisseurs, Filtres et extraction spécifiques au fournisseur, Normalisation des résultats, web_search natif OpenAI, web_search natif Codex, Grounding Gemini, Grounding web Grok, Recherche web Kimi, Citations natives du fournisseur, Routage des modèles et filtres, webSearchProviders, registerWebSearchProvider, webFetchProviders, registerWebFetchProvider, chargement d'artefacts publics, résolution à l'exécution, tests de contrat |
| [Configuration et diagnostics](operator-setup-provider-selection-and-credential-repair.md) | ❌  | `Beta (74%)`   | `Beta (70%)`   | `Beta (74%)`   | Identifiants du fournisseur, Sélection du fournisseur par défaut, Réparation des identifiants, Vérifications d'état, Erreurs de quota, Contrôles de cache, Diagnostics du fournisseur, Nouvelle tentative et basculement, Réparation de l'opérateur                                                                                                                                                                                                                                                                                                             |
| [Sécurité réseau](network-safety-ssrf-redirects-and-untrusted-content.md)            | ❌  | `Stable (84%)` | `Stable (84%)` | `Stable (84%)` | Sécurité réseau, SSRF, Redirections, Contenu non approuvé                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| [Disponibilité et récupération des outils](tool-exposure-policy-and-runtime-tool-wiring.md)      | ❌  | `Stable (82%)` | `Stable (80%)` | `Stable (82%)` | Exposition web_search, Exposition web_fetch, Exposition x_search, Politique group:web, Diagnostics d'état désactivé, Gating fournisseur/modèle, Récupération d'URL, Extraction HTML, Extraction PDF/texte, Troncature sécurisée, Remise de citation de contenu                                                                                                                                                                                                                                                             |

## Barème de notation

- Couverture :
  Évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/exécution
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  Évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux d'exécution réel sont des entrées de couverture
  uniquement ; elles ne relèvent ni n'abaissent la qualité.
- Complétude :
  Évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifique à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Fournisseurs de recherche

Ancres de recherche : Fournisseurs soutenus par API, Fournisseurs sans clé et auto-hébergés, Comparaison de fournisseurs et détection automatique, Filtres et extraction spécifiques au fournisseur, Normalisation des résultats, web_search natif OpenAI, web_search natif Codex, Grounding Gemini, Grounding web Grok, Recherche web Kimi, Citations natives du fournisseur, Routage des modèles et filtres, webSearchProviders, registerWebSearchProvider, webFetchProviders, registerWebFetchProvider, chargement d'artefacts publics, résolution à l'exécution, tests de contrat.

Note de catégorie : [Fournisseurs de recherche](bundled-structured-search-providers.md)

Décisions de score :

- Couverture : `Bêta (76%)`
- Qualité : `Bêta (72%)`
- Complétude : `Bêta (76%)`
- LTS : ❌

Fonctionnalités :

- Fournisseurs soutenus par API : Couvre le routage des fournisseurs soutenus par API, la mise en forme des requêtes, le streaming et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Fournisseurs sans clé et auto-hébergés : Couvre le routage des fournisseurs sans clé et auto-hébergés, la mise en forme des requêtes, le streaming et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Comparaison de fournisseurs et détection automatique : Couvre le routage de la comparaison de fournisseurs et de la détection automatique, la mise en forme des requêtes, le streaming et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Filtres et extraction spécifiques au fournisseur : Couvre le routage des filtres et de l'extraction spécifiques au fournisseur, la mise en forme des requêtes, le streaming et la normalisation des réponses pour les fournisseurs de recherche structurée.
- Normalisation des résultats : Couvre le routage de la normalisation des résultats, la mise en forme des requêtes, le streaming et la normalisation des réponses pour les fournisseurs de recherche structurée.
- web_search natif OpenAI : Couvre le routage de web_search natif OpenAI, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- web_search natif Codex : Couvre le routage de web_search natif Codex, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Grounding Gemini : Couvre le routage du grounding Gemini, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Grounding web Grok : Couvre le routage du grounding web Grok, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Recherche web Kimi : Couvre le routage de la recherche web Kimi, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Citations natives du fournisseur : Couvre le routage des citations natives du fournisseur, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- Routage des modèles et filtres : Couvre le routage des modèles et filtres, la liaison de session, l'historique et le contexte de conversation pour la recherche ancrée native du fournisseur.
- webSearchProviders : Définit la configuration de webSearchProviders, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les contrats de plugin de fournisseur web.
- registerWebSearchProvider : Définit la configuration de registerWebSearchProvider, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les contrats de plugin de fournisseur web.
- webFetchProviders : Définit la configuration de webFetchProviders, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les contrats de plugin de fournisseur web.
- registerWebFetchProvider : Définit la configuration de registerWebFetchProvider, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les contrats de plugin de fournisseur web.
- Chargement d'artefacts publics : Définit la configuration du chargement d'artefacts publics, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les contrats de plugin de fournisseur web.
- Résolution à l'exécution : Définit la configuration de la résolution à l'exécution, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les contrats de plugin de fournisseur web.
- Tests de contrat : Définit la configuration des tests de contrat, les identifiants, la configuration et le comportement de vérification de l'opérateur pour les contrats de plugin de fournisseur web.

Documentation principale :

- `docs/tools/web.md`
- `docs/tools/brave-search.md`
- `docs/tools/tavily.md`
- `docs/tools/exa-search.md`
- `docs/tools/firecrawl.md`
- `docs/tools/perplexity-search.md`
- `docs/tools/duckduckgo-search.md`
- `docs/tools/searxng-search.md`
- `docs/tools/gemini-search.md`
- `docs/tools/grok-search.md`
- `docs/tools/kimi-search.md`
- `docs/tools/minimax-search.md`
- `docs/tools/ollama-search.md`
- `docs/plugins/sdk-subpaths.md`
- `docs/plugins/sdk-overview.md`
- `docs/plugins/manifest.md`

### 2. Configuration et diagnostics

Ancres de recherche : Identifiants du fournisseur, Sélection du fournisseur par défaut, Réparation des identifiants, Vérifications d'état, Erreurs de quota, Contrôles de cache, Diagnostics du fournisseur, Nouvelle tentative et basculement, Réparation de l'opérateur.

Note de catégorie : [Configuration et diagnostics](operator-setup-provider-selection-and-credential-repair.md)

Décisions de score :

- Couverture : `Bêta (74%)`
- Qualité : `Bêta (70%)`
- Complétude : `Bêta (74%)`
- LTS : ❌

Fonctionnalités :

- Identifiants du fournisseur : Définit la configuration des identifiants du fournisseur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la réparation de configuration et d'identifiants.
- Sélection du fournisseur par défaut : Définit la configuration de la sélection du fournisseur par défaut, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la réparation de configuration et d'identifiants.
- Réparation des identifiants : Définit la configuration de la réparation des identifiants, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la réparation de configuration et d'identifiants.
- Vérifications d'état : Définit la configuration des vérifications d'état, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la réparation de configuration et d'identifiants.
- Erreurs de quota : Couvre l'état des erreurs de quota, les diagnostics, la gestion des défaillances et la réparation de l'opérateur pour la fiabilité et les diagnostics du fournisseur.
- Contrôles de cache : Couvre l'état des contrôles de cache, les diagnostics, la gestion des défaillances et la réparation de l'opérateur pour la fiabilité et les diagnostics du fournisseur.
- Diagnostics du fournisseur : Couvre l'état des diagnostics du fournisseur, les diagnostics, la gestion des défaillances et la réparation de l'opérateur pour la fiabilité et les diagnostics du fournisseur.
- Nouvelle tentative et basculement : Couvre l'état de la nouvelle tentative et du basculement, les diagnostics, la gestion des défaillances et la réparation de l'opérateur pour la fiabilité et les diagnostics du fournisseur.
- Réparation de l'opérateur : Couvre l'état de la réparation de l'opérateur, les diagnostics, la gestion des défaillances et la réparation de l'opérateur pour la fiabilité et les diagnostics du fournisseur.

Documentation principale :

- `docs/tools/web.md`
- `docs/tools/web-fetch.md`
- `docs/help/faq.md`
- `docs/reference/api-usage-costs.md`
- `docs/tools/brave-search.md`
- `docs/tools/perplexity-search.md`
- `docs/tools/tavily.md`
- `docs/tools/firecrawl.md`

### 3. Sécurité réseau

Ancres de recherche : Sécurité réseau, SSRF, Redirections, Contenu non approuvé, sécurité réseau des outils de recherche web, ssrf, redirections et contenu non approuvé, sécurité réseau, ssrf, redirections et contenu non approuvé.

Note de catégorie : [Sécurité réseau](network-safety-ssrf-redirects-and-untrusted-content.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Stable (84%)`
- Complétude : `Stable (84%)`
- LTS : ❌

Fonctionnalités :

- Sécurité réseau : Définit l'autorisation de sécurité réseau, la confiance, les limites de sécurité et les contrôles de l'opérateur pour la sécurité réseau, Ssrf, les redirections et le contenu non approuvé.
- SSRF : Définit l'autorisation SSRF, la confiance, les limites de sécurité et les contrôles de l'opérateur pour la sécurité réseau, Ssrf, les redirections et le contenu non approuvé.
- Redirections : Définit l'autorisation des redirections, la confiance, les limites de sécurité et les contrôles de l'opérateur pour la sécurité réseau, Ssrf, les redirections et le contenu non approuvé.
- Contenu non approuvé : Définit l'autorisation du contenu non approuvé, la confiance, les limites de sécurité et les contrôles de l'opérateur pour la sécurité réseau, Ssrf, les redirections et le contenu non approuvé.

Documentation principale :

- `docs/tools/web.md`
- `docs/tools/web-fetch.md`
- `docs/tools/firecrawl.md`
- `docs/tools/searxng-search.md`

### 4. Disponibilité des outils et récupération

Ancres de recherche : exposition web_search, exposition web_fetch, exposition x_search, politique group:web, diagnostics d'état désactivé, gating fournisseur/modèle, récupération d'URL, extraction HTML, extraction PDF/texte, Troncature sécurisée, Remise de citation de contenu.

Note de catégorie : [Disponibilité des outils et récupération](tool-exposure-policy-and-runtime-tool-wiring.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Stable (80%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Exposition web_search : Définit la configuration de l'exposition web_search, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité et la politique des outils.
- Exposition web_fetch : Définit la configuration de l'exposition web_fetch, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité et la politique des outils.
- Exposition x_search : Définit la configuration de l'exposition x_search, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité et la politique des outils.
- Politique group:web : Définit la configuration de la politique group:web, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité et la politique des outils.
- Diagnostics d'état désactivé : Définit la configuration des diagnostics d'état désactivé, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité et la politique des outils.
- Gating fournisseur/modèle : Définit la configuration du gating fournisseur/modèle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la disponibilité et la politique des outils.
- Récupération d'URL : Couvre l'invocation de l'outil de récupération d'URL, l'exécution de l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Extraction HTML : Couvre l'invocation de l'outil d'extraction HTML, l'exécution de l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Extraction PDF/texte : Couvre l'invocation de l'outil d'extraction PDF/texte, l'exécution de l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Troncature sécurisée : Couvre l'invocation de l'outil de troncature sécurisée, l'exécution de l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.
- Remise de citation de contenu : Couvre l'invocation de l'outil de remise de citation de contenu, l'exécution de l'hôte, la politique de bac à sable et la gestion des artefacts pour la récupération web et l'extraction de contenu.

Documentation principale :

- `docs/gateway/config-tools.md`
- `docs/tools/web-fetch.md`
- `docs/tools/web.md`
- `docs/help/faq.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/web-search-tools/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/web-search-tools`.
