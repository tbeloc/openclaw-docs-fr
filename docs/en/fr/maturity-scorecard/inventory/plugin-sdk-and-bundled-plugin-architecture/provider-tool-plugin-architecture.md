---
title: Plugins - Provider and Tool Plugins Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Provider and Tool Plugins Maturity Note

## Summary

Cette catégorie est Stable, avec des preuves actuelles étendues couvrant l'enregistrement des fournisseurs, l'authentification des fournisseurs et la propriété du catalogue de modèles, le chargement du runtime des fournisseurs de capacités, la génération de métadonnées des plugins d'outils, et les manifestes mixtes fournisseur-plus-outil. La couverture reste en dessous de Lovable car la preuve de runtime en direct et de bout en bout est représentative plutôt qu'exhaustive sur chaque famille de fournisseur groupée et le cycle de vie du plugin d'outil généré. La qualité est Stable car la documentation et le code source décrivent maintenant clairement une limite entre le manifeste froid et le runtime, mais les preuves d'archive montrent toujours des corrections actives et une prudence des mainteneurs autour des métadonnées d'authentification des fournisseurs, du routage personnalisé des fournisseurs, du durcissement des schémas, et de l'expansion de la surface du SDK.

## Category Scope

Cette catégorie couvre l'architecture des plugins de fournisseur et d'outil pour la surface Plugins :

- Création de plugins de fournisseur via `defineSingleProviderPluginEntry`, `api.registerProvider(...)`, méthodes d'authentification des fournisseurs, fournisseurs de catalogue de modèles, alias de fournisseurs, hooks de runtime, et normalisation de schéma détenue par le fournisseur.
- Contrats de capacité détenus par le fournisseur tels que la recherche web, la récupération web, la parole, la transcription en temps réel, la voix en temps réel, la compréhension des médias, la génération d'images, la génération de vidéos, la génération de musique, les embeddings, et les chemins de propriété de manifeste associés.
- Création de plugins d'outils via `defineToolPlugin`, génération de métadonnées statiques, métadonnées d'outils optionnelles, usines de runtime, génération de contrats de manifeste, et découverte d'outils sans charger le code de runtime du plugin.
- Formes de plugins mixtes fournisseur-et-outil où un plugin groupé détient des fournisseurs plus `contracts.tools`, comme Tavily et xAI.

Hors de portée : architecture des plugins de canal, distribution des plugins et préparation de la disponibilité des versions en tant que catégorie distincte, flux de publication ClawHub, et qualité spécifique aux fournisseurs au-delà des coutures d'architecture partagées fournisseur/outil.

## Features

- Provider plugins: Les plugins de fournisseur enregistrent les modèles et les capacités avec le runtime.
- Tool plugins: Les plugins d'outils enregistrent les outils découvrables et les métadonnées statiques sans propriété de runtime ambiguë.
- Model catalogs: Les catalogues de modèles des fournisseurs sont découvrables et fusionnent proprement dans les listes globales.
- Provider auth: La configuration d'authentification des fournisseurs et la gestion des secrets sont prises en charge.
- Web search and fetch: Les plugins de fournisseur ou d'outil peuvent exposer les capacités de recherche et de récupération web.
- Mixed plugins: Les plugins mixtes de fournisseur et d'outil sont pris en charge sans propriété ambiguë.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` a réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`.
- discrawl: `discrawl status --json` a réussi avec `generated_at=2026-05-30T00:38:20Z`, `state=current`, `summary=1487536 messages across 25831 channels`, `last_sync_at=2026-05-29T19:27:40Z`.

## Coverage Score

- Score: `Stable (84%)`
- Positive signals:
  - Les tests d'intégration du runtime couvrent la recherche de hooks de fournisseur, l'authentification de runtime préparée par le fournisseur, la résolution de fournisseur basée sur le catalogue et la configuration, et la réutilisation sûre du runtime dans `src/plugins/provider-runtime.test.ts`.
  - Les tests de runtime des fournisseurs de capacités couvrent la découverte de snapshot de métadonnées, le chargement de capacités externes activé, la capture de secours groupée, et la résolution de contrat de manifeste dans `src/plugins/capability-provider-runtime.test.ts` et `src/plugins/manifest-contract-runtime.test.ts`.
  - Les tests de runtime des fournisseurs de recherche web et de médias couvrent le chargement de fournisseurs groupés, la découverte de runtime délimitée, le comportement de liste blanche, l'exécution de fournisseur configuré, la détection automatique des identifiants, et les chemins de défaillance rapide des fournisseurs dans `src/plugins/web-search-providers.runtime.test.ts`, `src/web-search/runtime.test.ts`, et `src/video-generation/runtime.test.ts`.
  - Les tests d'intégration et e2e des hooks d'outils couvrent la mutation et le blocage avant l'appel d'outil ainsi que la dispatch et l'isolation après l'appel d'outil dans `src/agents/agent-tools.before-tool-call.integration.e2e.test.ts`, `src/agents/agent-tools.before-tool-call.e2e.test.ts`, et `src/plugins/wired-hooks-after-tool-call.e2e.test.ts`.
  - La couverture de fournisseur en direct existe pour les familles de fournisseurs groupées et les chemins de capacités dans `extensions/openai/openai.live.test.ts`, `extensions/openrouter/openrouter.live.test.ts`, `extensions/xai/xai.live.test.ts`, `extensions/xai/x-search.live.test.ts`, et `extensions/video-generation-providers.live.test.ts`.
- Negative signals:
  - La couverture est la plus forte pour le runtime des fournisseurs, la recherche web, les capacités de génération de médias, et la dispatch des hooks, mais pas pour chaque chemin d'intégration d'authentification de fournisseur groupé ou chaque variante de catalogue.
  - Les flux `defineToolPlugin` générés ont de bonnes preuves de création et de validation de manifeste, mais il y a toujours une preuve limitée de preuve complète d'installation-construction-inspection-exécution pour les packages de style tiers.
  - Les plugins mixtes fournisseur-plus-outil sont exercés via des suites de plugins spécifiques plutôt qu'une matrice de runtime à l'échelle de la catégorie.
- Integration gaps:
  - Ajouter une matrice de fumée inter-fournisseurs qui active chaque plugin de fournisseur groupé ou fournisseur-plus-outil, résout la propriété à partir des manifestes, et exécute un chemin de runtime inoffensif le cas échéant.
  - Ajouter une couverture de fumée en direct ou sauvegardée par relecture pour l'intégration d'authentification des fournisseurs plus la liste du catalogue de modèles sur plus de fournisseurs groupés, pas seulement les chemins OpenAI, OpenRouter, xAI et fournisseur de médias sélectionnés.
  - Ajouter un flux de package de plugin d'outil généré de bout en bout qui couvre l'échafaudage, la construction, la génération de métadonnées, l'inspection, l'activation, et l'exécution de runtime réelle.
  - Ajouter une couverture de régression de plugin mixte explicite qui maintient `contracts.tools`, la propriété des capacités, et l'alignement des métadonnées de runtime après l'installation et la mise à jour.

## Quality Score

- Score: `Stable (82%)`
- Gitcrawl reports:
  - `gitcrawl search openclaw/openclaw --query "provider plugin sdk tool web search" --json` a retourné le travail actuel sur la croissance des fournisseurs groupés et les réparations de routage, y compris #85158 (Parallel en tant que fournisseur `web_search` groupé), #77736 (correction de routage `web_search` personnalisé explicite), #86440 (plugin SerpApi avec fournisseur plus outils), #75218 (fournisseur `web_fetch` Tavily), et #87486 (retours bêta touchant les noms d'affichage des plugins, les surfaces de runtime paresseux, et les métadonnées du catalogue).
  - `gitcrawl search openclaw/openclaw --query "plugin sdk provider auth model catalog" --json` a retourné une pression de qualité continue autour des profils de réflexion des fournisseurs, du chargement du catalogue uniquement métadonnées, de l'intégration des fournisseurs, des en-têtes de catalogue, de la migration de résolution de runtime, du durcissement des schémas, de la réparation du refroidissement obsolète, de la migration OAuth, et de la consolidation de la surface du SDK (#84902, #75022, #84997, #78951, #77700, #87141, #87697, #82056, #80219).
- Discrawl reports:
  - La discussion actuelle des mainteneurs dit que les contrats d'API des plugins, le chargement des extensions, la dénomination des fournisseurs, l'authentification, le sandbox, et les plans de dépréciation sont tous des domaines de changement qui devraient recevoir un examen supplémentaire avant le durcissement.
  - Les notes d'examen des mainteneurs sur l'évolution du fournisseur d'embeddings appellent explicitement la coexistence des coutures de capacités héritées et plus récentes, ce qui est bon pour la compatibilité mais montre que cette architecture est toujours en transition.
  - La discussion des mainteneurs sur les métadonnées d'authentification xAI soutient que `providerAuthChoices` de manifeste froid et `auth` de fournisseur de runtime sont intentionnellement des contrats distincts, et avertit contre les échappatoires SDK ponctuelles telles que les modèles larges `extraAuth`.
  - Les messages de version récents décrivent une analyse plus rapide des plugins et des catalogues, des améliorations d'authentification des fournisseurs conscientes du profil, et de nouveaux plugins de fournisseur, ce qui est un signal opérationnel positif mais aussi une preuve d'agitation active.
- Good qualities:
  - La documentation et le code source actuels rendent la division manifeste froid versus runtime explicite : les métadonnées de manifeste alimentent la découverte et la validation, tandis que l'enregistrement de runtime détient le comportement réel du fournisseur et de l'outil.
  - `defineToolPlugin` maintient les métadonnées d'outil statiques et découvrables sans exécuter le code de runtime, et le chemin de commande de création préserve les métadonnées détenues par le manifeste tout en régénérant les contrats d'outils.
  - La documentation d'architecture, le guide des plugins de fournisseur, le guide des plugins d'outils, et l'inventaire généré donnent aux auteurs de plugins un chemin cohérent de la création à la propriété du runtime.
- Bad qualities:
  - Les preuves d'archive montrent toujours des réparations fréquentes dans le routage des fournisseurs, la gestion des profils d'authentification, les métadonnées du catalogue, les limites de flou de schéma, et le comportement du refroidissement.
  - Le retour d'archive des mainteneurs traite les contrats de sécurité des fournisseurs et les changements de surface du SDK comme des domaines d'examen à haut risque, ce qui maintient cette catégorie en dessous de Lovable.
  - L'architecture des fournisseurs et des outils reste suffisamment large pour que les nouveaux fournisseurs groupés ou les plugins mixtes puissent ajouter une pression à plusieurs coutures à la fois.
- Excluded from quality:
  - La couverture des tests unitaires, d'intégration, e2e et en direct a été utilisée uniquement comme entrées de couverture.
  - Les défaillances de validation de la surface de plugin partagée ont été traitées comme un bloqueur d'environnement local, pas comme une preuve de qualité du produit.

## Known Gaps

- Les flux d'intégration d'authentification des fournisseurs et de liste du catalogue ont toujours besoin d'une preuve de bout en bout plus large sur l'ensemble des fournisseurs groupés.
- Les plugins mixtes fournisseur-plus-outil ont besoin de vérifications de régression plus fortes à l'échelle de la catégorie afin que la propriété du manifeste, l'enregistrement du runtime, et les métadonnées des outils restent alignés ensemble.
- La surface du SDK public est toujours suffisamment grande pour que les mainteneurs suivent explicitement la consolidation des dettes d'export et de cycle de vie.
- L'empaquetage des plugins d'outils a une validation de contrat forte mais manque toujours de plus de preuves réelles d'installation tierce et de fumée de runtime.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-provider-plugins.md` documente les manifestes de fournisseur, l'authentification du fournisseur, les catalogues de modèles, les hooks d'exécution, les assistants de compatibilité fournisseur-outil, et `defineSingleProviderPluginEntry`.
- `/Users/kevinlin/code/openclaw/docs/plugins/tool-plugins.md` documente `defineToolPlugin`, les outils optionnels, les outils d'usine, la génération de métadonnées, et le flux d'authoring/build/validate.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture.md` documente le modèle de capacité, la division propriété manifest-versus-runtime, les formes de plugin, les snapshots de métadonnées, et la planification d'activation.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md` enregistre l'inventaire des plugins groupés et externes, y compris les surfaces de plugin fournisseur, fournisseur-plus-outil, et outil uniquement.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md` documente la migration héritée de clé de capacité dans `contracts`, ce qui importe pour les contrats de capacité possédés par le fournisseur.

## Source

- `/Users/kevinlin/code/openclaw/src/plugin-sdk/provider-entry.ts` implémente `defineSingleProviderPluginEntry`, la normalisation des variables d'environnement, le câblage de l'authentification du fournisseur, et la projection de catalogue en direct/statique.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/tool-plugin.ts` implémente `defineToolPlugin`, l'export de métadonnées statiques, la gestion des outils optionnels, et l'enregistrement des outils d'exécution.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/provider-tools.ts` implémente la normalisation du schéma d'outil de famille de fournisseur et les hooks d'inspection.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-runtime.ts` possède la résolution des hooks du fournisseur d'exécution, la gestion de l'authentification/profil du fournisseur, les superpositions de prompt, et le chargement du fournisseur d'exécution.
- `/Users/kevinlin/code/openclaw/src/plugins/capability-provider-runtime.ts` possède la découverte de contrat manifest et le chargement d'exécution pour les fournisseurs de capacité.
- `/Users/kevinlin/code/openclaw/src/plugins/manifest-contract-runtime.ts` résout la propriété du contrat manifest d'exécution soutenue par snapshot de métadonnées.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-authoring-command.ts` construit et valide les métadonnées du plugin d'outil générées.
- `/Users/kevinlin/code/openclaw/extensions/brave/openclaw.plugin.json`, `/Users/kevinlin/code/openclaw/extensions/tavily/openclaw.plugin.json`, et `/Users/kevinlin/code/openclaw/extensions/xai/openclaw.plugin.json` montrent les modèles actuels de propriété manifest fournisseur uniquement et fournisseur-plus-outil groupés.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/plugins/provider-runtime.test.ts` couvre la recherche de hook du fournisseur d'exécution, l'authentification d'exécution préparée, l'invalidation de mutation de configuration, et la résolution d'exécution sûre.
- `/Users/kevinlin/code/openclaw/src/plugins/capability-provider-runtime.test.ts` couvre la découverte de capacité snapshot manifest, la capture de secours groupée, les fournisseurs externes activés, et le chargement à froid des fournisseurs de capacité externes.
- `/Users/kevinlin/code/openclaw/src/plugins/manifest-contract-runtime.test.ts` couvre la résolution du contrat manifest d'exécution à partir des snapshots de métadonnées.
- `/Users/kevinlin/code/openclaw/src/plugins/web-search-providers.runtime.test.ts` et `/Users/kevinlin/code/openclaw/src/web-search/runtime.test.ts` couvrent le chargement du fournisseur de recherche web groupé, la découverte en mode setup, le chargement d'exécution scoped, l'exécution du fournisseur configuré, et les chemins fail-fast du fournisseur.
- `/Users/kevinlin/code/openclaw/src/video-generation/runtime.test.ts` couvre l'exécution du fournisseur actif, le comportement de secours, les gardes de schéma d'option de fournisseur, et la gestion de capacité spécifique au mode.
- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.before-tool-call.integration.e2e.test.ts`, `/Users/kevinlin/code/openclaw/src/agents/agent-tools.before-tool-call.e2e.test.ts`, et `/Users/kevinlin/code/openclaw/src/plugins/wired-hooks-after-tool-call.e2e.test.ts` couvrent le comportement des hooks before-tool-call et after-tool-call dans les flux d'exécution.
- `/Users/kevinlin/code/openclaw/extensions/openai/openai.live.test.ts`, `/Users/kevinlin/code/openclaw/extensions/openrouter/openrouter.live.test.ts`, `/Users/kevinlin/code/openclaw/extensions/xai/xai.live.test.ts`, `/Users/kevinlin/code/openclaw/extensions/xai/x-search.live.test.ts`, et `/Users/kevinlin/code/openclaw/extensions/video-generation-providers.live.test.ts` fournissent des preuves de fournisseur en direct pour les chemins de fournisseur groupé représentatifs.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugin-sdk/provider-entry.test.ts` couvre l'enregistrement du fournisseur, le câblage des variables d'environnement et de l'authentification, et les valeurs par défaut des métadonnées de l'assistant.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/tool-plugin.test.ts` couvre les résultats enveloppés, les outils optionnels, les usines d'exécution, les valeurs par défaut de configuration vide stricte, et l'export de métadonnées statiques.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/provider-tools.test.ts` couvre la normalisation du schéma de famille de fournisseur et le comportement d'inspection pour les schémas d'outil DeepSeek, Gemini, et OpenAI.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/provider-auth-runtime.test.ts` couvre la génération d'état OAuth, l'analyse de callback, et la gestion CORS de callback.
- `/Users/kevinlin/code/openclaw/src/cli/plugins-authoring-command.test.ts` couvre la génération de manifest à partir des métadonnées d'outil, les métadonnées d'outil optionnel, l'alignement d'entrée de package, et la validation de contrat obsolète.
- `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-tool-contracts.test.ts` couvre l'alignement entre la propriété `registerTool` d'exécution et `contracts.tools`.
- `/Users/kevinlin/code/openclaw/src/plugins/contracts/provider-family-plugin-tests.test.ts` couvre les limites de hook de famille de fournisseur groupée.

## Commandes de validation de surface

- `pnpm plugin-sdk:check-exports`: `bloqué` - tenté depuis `/Users/kevinlin/code/openclaw`, mais l'installation de dépendance locale a échoué avant la validation réelle sur les erreurs d'authentification de registre 403 pour `@microsoft/teams.cards` et `@microsoft/teams.api` avec `No authorization header was set for the request`; cette commande vérifierait les exports SDK publics générés par rapport à l'inventaire de point d'entrée coché.
- `pnpm plugin-sdk:api:check`: `bloqué` - tenté depuis `/Users/kevinlin/code/openclaw`, mais le même bloqueur d'installation de dépendance locale a empêché l'exécution; cette commande détecterait la dérive d'API publique dans la surface du Plugin SDK emballée.
- `pnpm plugin-sdk:surface:check`: `bloqué` - tenté depuis `/Users/kevinlin/code/openclaw`, mais le même bloqueur d'installation de dépendance locale a empêché l'exécution; cette commande appliquerait les budgets de taille de surface et les limites d'export obsolète pour le Plugin SDK public.
- `pnpm plugins:boundary-report:ci`: `bloqué` - tenté depuis `/Users/kevinlin/code/openclaw`, mais le même bloqueur d'installation de dépendance locale a empêché l'exécution; cette commande validerait les limites d'importation réservées, les sous-chemins non classifiés, et la dette de compatibilité due dans le code possédé par le plugin.
- `pnpm release:plugins:npm:check`: `bloqué` - tenté depuis `/Users/kevinlin/code/openclaw`, mais le même bloqueur d'installation de dépendance locale a empêché l'exécution; cette commande validerait les métadonnées npm du plugin publiable et la préparation à la publication.
- `pnpm release:plugins:clawhub:check`: `bloqué` - tenté depuis `/Users/kevinlin/code/openclaw`, mais le même bloqueur d'installation de dépendance locale a empêché l'exécution; cette commande validerait les métadonnées ClawHub du plugin publiable et la préparation à la publication.

## Requêtes Gitcrawl

Requête:

`gitcrawl search openclaw/openclaw --query "provider plugin sdk tool web search" --json`

Résultats:

- Retourné le travail ouvert sur la croissance du fournisseur groupé et la qualité du routage: #85158 (Parallel en tant que fournisseur `web_search` groupé), #77736 (correction explicite du routage du fournisseur `web_search` personnalisé), #86440 (plugin SerpApi avec fournisseur plus outils), #75218 (fournisseur Tavily `web_fetch`), #87486 (retours bêta touchant les noms d'affichage du plugin, les surfaces d'exécution paresseuses, et les métadonnées de catalogue), plus la pression d'extension adjacente de #86155 et #80388.

Requête:

`gitcrawl search openclaw/openclaw --query "plugin sdk provider auth model catalog" --json`

Résultats:

- Retourné les éléments de pression de qualité actuels autour des profils de réflexion du fournisseur, du chargement de catalogue métadonnées uniquement, de l'intégration du fournisseur, des en-têtes de catalogue, de la migration d'exécution préparée, du durcissement du schéma, de la réparation du délai d'attente obsolète, de la migration OAuth, et de la consolidation de surface SDK (#84902, #75022, #84997, #78951, #77700, #87141, #87697, #82056, #80219).

## Requêtes Discrawl

Requête:

`discrawl --json search "provider plugin sdk" --limit 10`

Résultats:

- Retourné la discussion actuelle du mainteneur qui traite les contrats d'API de plugin, la surface SDK, la sémantique de chargement d'extension, la dénomination du fournisseur, les limites d'authentification, et les plans de dépréciation comme des domaines nécessitant un examen supplémentaire avant le durcissement.
- Retourné une mise à jour récente du mainteneur qu'un changement de surface de plugin a ajouté des assistants partagés de flux de fournisseur réutilisables, ce qui est un signal positif pour la maintenance active mais confirme également l'expansion SDK en cours.
- Retourné la préoccupation du mainteneur qu'un changement proposé a ajouté un nouveau contrat de sécurité du fournisseur avec un détail de repro limité, ce qui est une preuve de qualité négative directe pour cette catégorie.

Requête:

`discrawl --json search "tool plugin provider auth model catalog" --limit 10`

Résultats:

- Retourné le commentaire du mainteneur que les `providerAuthChoices` manifest à froid et l'`auth` du fournisseur d'exécution sont intentionnellement des contrats séparés, et que préserver cette division importe pour l'intégration et la découverte.
- Retourné le commentaire du mainteneur que les coutures de fournisseur d'intégration héritées et plus récentes coexistent actuellement pour la compatibilité, ce qui est bon pour les plugins existants mais une preuve que la migration de capacité est toujours active.
- Retourné la messagerie de publication récente qui appelle la recherche de métadonnées d'authentification de plugin et de modèle plus rapide plus la couverture de plugin de fournisseur plus large, ce qui est un signal opérationnel positif pour cette catégorie.
