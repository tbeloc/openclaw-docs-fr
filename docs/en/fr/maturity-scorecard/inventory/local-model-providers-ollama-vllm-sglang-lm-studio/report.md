---
title: "Fournisseurs de modèles locaux : Rapport de maturité Ollama, vLLM, SGLang, LM Studio"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Rapport de maturité Ollama, vLLM, SGLang, LM Studio

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (77%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (77%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves archivées `local-model-providers-ollama-vllm-sglang-lm-studio` de `/Users/kevinlin/tmp/maturity/local-model-providers-ollama-vllm-sglang-lm-studio` dans le contrat d'inventaire process-version-3 actuel.

Les scores de catégorie Couverture et Qualité proviennent des lignes de score archivées soutenues par des preuves. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                                    | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration du fournisseur, cycle de vie et diagnostics](provider-selection-and-onboarding.md)          | ❌  | `Beta (74%)`   | `Beta (72%)`   | `Beta (74%)`   | Sélection du fournisseur, Intégration, configuration localService, Démarrage du processus et disponibilité, Baux de requête et arrêt inactif, Vérifications de santé et redémarrage, Recettes de fournisseur, État du fournisseur local, Sondes de disponibilité du backend, Erreurs de disponibilité du modèle, Diagnostics de disponibilité mémoire, Documentation de dépannage du fournisseur |
| [Plugins de fournisseur natif](ollama-native-provider.md)                                        | ❌  | `Beta (78%)`   | `Beta (78%)`   | `Beta (78%)`   | Configuration Ollama et extraction de modèles, Découverte de modèles, Streaming et vision, Intégrations Ollama, Support de recherche web, Configuration LM Studio, Découverte de modèles et authentification, Préchargement de modèles et chargement JIT, Compatibilité du streaming, Intégrations LM Studio                                                                                |
| [Compatibilité du runtime compatible OpenAI](request-stream-compatibility-and-tool-calling.md) | ❌  | `Beta (74%)`   | `Alpha (68%)`  | `Beta (74%)`   | Configuration du fournisseur groupé, Point de terminaison de découverte de modèles, Configuration non interactive, Contrôles de réflexion vLLM, Sémantique de chat et d'outils compatible OpenAI, Conseils de compatibilité SGLang, Compatibilité du flux de requête, Appel d'outils                                                                                        |
| [Mémoire locale et intégrations](local-embeddings-and-memory-provider-usage.md)                | ❌  | `Beta (76%)`   | `Alpha (68%)`  | `Beta (76%)`   | Sélection du fournisseur d'intégration, Disponibilité de la recherche mémoire, Remplacement du modèle memoryFlush, Recherche lexicale de secours, Conseils de non-concordance du fournisseur                                                                                                                                                                               |
| [Sécurité réseau et contrôles d'invite](safety-network-and-prompt-pressure-controls.md)        | ❌  | `Stable (82%)` | `Stable (82%)` | `Stable (82%)` | Réseau de sécurité, Contrôles de pression d'invite                                                                                                                                                                                                                                                                             |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de Couverture uniquement ; elles ne
  augmentent ni ne diminuent la Qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration du fournisseur, cycle de vie et diagnostics

Ancres de recherche : Sélection du fournisseur, Intégration, fournisseurs de modèles locaux : ollama, vllm, sglang, lm studio sélection et intégration du fournisseur, sélection et intégration du fournisseur, configuration localService, Démarrage du processus et disponibilité, Baux de requête et arrêt inactif, Vérifications de santé et redémarrage, Recettes de fournisseur, État du fournisseur local, Sondes de disponibilité du backend, Erreurs de disponibilité du modèle, Diagnostics de disponibilité de la mémoire, Documentation de dépannage du fournisseur.

Note de catégorie : [Configuration du fournisseur, cycle de vie et diagnostics](provider-selection-and-onboarding.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Sélection du fournisseur : Couvre la sélection du fournisseur sur le choix du fournisseur, `openclaw onboard`, contributions du sélecteur de modèle, configuration non interactive, et comportement associé de sélection et d'intégration du fournisseur.
- Intégration : Couvre l'intégration sur le choix du fournisseur, `openclaw onboard`, contributions du sélecteur de modèle, configuration non interactive, et comportement associé de sélection et d'intégration du fournisseur.
- Configuration localService : Couvre la configuration localService sur le contrat de configuration `localService`, démarrage du processus, sondes de disponibilité, comportement de bail/libération lors des requêtes du fournisseur, et comportement associé du cycle de vie et de la disponibilité du service local.
- Démarrage du processus et disponibilité : Couvre le démarrage du processus et la disponibilité sur le contrat de configuration `localService`, démarrage du processus, sondes de disponibilité, comportement de bail/libération lors des requêtes du fournisseur, et comportement associé du cycle de vie et de la disponibilité du service local.
- Baux de requête et arrêt inactif : Couvre les baux de requête et l'arrêt inactif sur le contrat de configuration `localService`, démarrage du processus, sondes de disponibilité, comportement de bail/libération lors des requêtes du fournisseur, et comportement associé du cycle de vie et de la disponibilité du service local.
- Vérifications de santé et redémarrage : Couvre les vérifications de santé et le redémarrage sur le contrat de configuration `localService`, démarrage du processus, sondes de disponibilité, comportement de bail/libération lors des requêtes du fournisseur, et comportement associé du cycle de vie et de la disponibilité du service local.
- Recettes de fournisseur : Couvre les recettes de fournisseur sur le contrat de configuration `localService`, démarrage du processus, sondes de disponibilité, comportement de bail/libération lors des requêtes du fournisseur, et comportement associé du cycle de vie et de la disponibilité du service local.
- État du fournisseur local : Couvre l'état du fournisseur local sur les commandes de diagnostic visibles par l'utilisateur, normalisation des erreurs HTTP du fournisseur, classification du modèle non trouvé, sondes directes du backend local, et comportement associé des diagnostics et du dépannage.
- Sondes de disponibilité du backend : Couvre les sondes de disponibilité du backend sur les commandes de diagnostic visibles par l'utilisateur, normalisation des erreurs HTTP du fournisseur, classification du modèle non trouvé, sondes directes du backend local, et comportement associé des diagnostics et du dépannage.
- Erreurs de disponibilité du modèle : Couvre les erreurs de disponibilité du modèle sur les commandes de diagnostic visibles par l'utilisateur, normalisation des erreurs HTTP du fournisseur, classification du modèle non trouvé, sondes directes du backend local, et comportement associé des diagnostics et du dépannage.
- Diagnostics de disponibilité de la mémoire : Couvre les diagnostics de disponibilité de la mémoire sur les commandes de diagnostic visibles par l'utilisateur, normalisation des erreurs HTTP du fournisseur, classification du modèle non trouvé, sondes directes du backend local, et comportement associé des diagnostics et du dépannage.
- Documentation de dépannage du fournisseur : Couvre la documentation de dépannage du fournisseur sur les commandes de diagnostic visibles par l'utilisateur, normalisation des erreurs HTTP du fournisseur, classification du modèle non trouvé, sondes directes du backend local, et comportement associé des diagnostics et du dépannage.

Docs principales :

- `docs/gateway/local-models.md`
- `docs/providers/lmstudio.md`
- `docs/providers/ollama.md`
- `docs/providers/vllm.md`
- `docs/gateway/local-model-services.md`
- `docs/gateway/config-agents.md`
- `docs/gateway/troubleshooting.md`
- `docs/gateway/doctor.md`

### 2. Plugins de fournisseur natifs

Ancres de recherche : Configuration d'Ollama et extraction de modèles, Découverte de modèles, Streaming et vision, Embeddings Ollama, Support de recherche web, Configuration de LM Studio, Découverte de modèles et authentification, Préchargement et chargement JIT des modèles, Compatibilité du streaming, Embeddings LM Studio.

Note de catégorie : [Plugins de fournisseur natifs](ollama-native-provider.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (78%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Configuration d'Ollama et extraction de modèles : Couvre la configuration d'Ollama et l'extraction de modèles sur la découverte native du chat/modèle Ollama, configuration cloud+local/local uniquement, marqueurs d'authentification locaux, extraction de modèles, et comportement associé du fournisseur natif ollama.
- Découverte de modèles : Couvre la découverte de modèles sur la découverte native du chat/modèle Ollama, configuration cloud+local/local uniquement, marqueurs d'authentification locaux, extraction de modèles, et comportement associé du fournisseur natif ollama.
- Streaming et vision : Couvre le streaming et la vision sur la découverte native du chat/modèle Ollama, configuration cloud+local/local uniquement, marqueurs d'authentification locaux, extraction de modèles, et comportement associé du fournisseur natif ollama.
- Embeddings Ollama : Couvre les embeddings Ollama sur la découverte native du chat/modèle Ollama, configuration cloud+local/local uniquement, marqueurs d'authentification locaux, extraction de modèles, et comportement associé du fournisseur natif ollama.
- Support de recherche web : Couvre le support de recherche web sur la découverte native du chat/modèle Ollama, configuration cloud+local/local uniquement, marqueurs d'authentification locaux, extraction de modèles, et comportement associé du fournisseur natif ollama.
- Configuration de LM Studio : Couvre la configuration de LM Studio sur le plugin du fournisseur LM Studio, docs `/providers/lmstudio`, découverte de modèles à partir des API LM Studio, comportement d'authentification pour les instances locales et authentifiées, comportement de préchargement/JIT, streaming compatible OpenAI, et embeddings de mémoire LM Studio.
- Découverte de modèles et authentification : Couvre la découverte de modèles et l'authentification sur le plugin du fournisseur LM Studio, docs `/providers/lmstudio`, découverte de modèles à partir des API LM Studio, comportement d'authentification pour les instances locales et authentifiées, comportement de préchargement/JIT, streaming compatible OpenAI, et embeddings de mémoire LM Studio.
- Préchargement et chargement JIT des modèles : Couvre le préchargement et le chargement JIT des modèles sur le plugin du fournisseur LM Studio, docs `/providers/lmstudio`, découverte de modèles à partir des API LM Studio, comportement d'authentification pour les instances locales et authentifiées, comportement de préchargement/JIT, streaming compatible OpenAI, et embeddings de mémoire LM Studio.
- Compatibilité du streaming : Couvre la compatibilité du streaming sur le plugin du fournisseur LM Studio, docs `/providers/lmstudio`, découverte de modèles à partir des API LM Studio, comportement d'authentification pour les instances locales et authentifiées, comportement de préchargement/JIT, streaming compatible OpenAI, et embeddings de mémoire LM Studio.
- Embeddings LM Studio : Couvre les embeddings LM Studio sur le plugin du fournisseur LM Studio, docs `/providers/lmstudio`, découverte de modèles à partir des API LM Studio, comportement d'authentification pour les instances locales et authentifiées, comportement de préchargement/JIT, streaming compatible OpenAI, et embeddings de mémoire LM Studio.

Docs principales :

- `docs/providers/ollama.md`
- `docs/providers/lmstudio.md`

### 3. Compatibilité du runtime compatible OpenAI

Ancres de recherche : Configuration du fournisseur fourni, découverte /v1/models, Configuration non interactive, Contrôles de réflexion vLLM, Sémantique du chat et des outils compatible OpenAI, Conseils de compatibilité SGLang, Compatibilité du flux de requête, Appel d'outils, fournisseurs de modèles locaux : ollama, vllm, sglang, lm studio compatibilité du flux de requête et appel d'outils, compatibilité du flux de requête et appel d'outils.

Note de catégorie : [Compatibilité du runtime compatible OpenAI](request-stream-compatibility-and-tool-calling.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Configuration du fournisseur fourni : Couvre la configuration du fournisseur fourni sur les plugins du fournisseur `vllm` et `sglang` fournis, docs, comportement par défaut env/URL de base, découverte `/v1/models`, et comportement associé des fournisseurs openai-compatible vllm et sglang.
- Point de terminaison de découverte de modèles : Couvre le point de terminaison de découverte de modèles sur les plugins du fournisseur `vllm` et `sglang` fournis, docs, comportement par défaut env/URL de base, découverte `/v1/models`, et comportement associé des fournisseurs openai-compatible vllm et sglang.
- Configuration non interactive : Couvre la configuration non interactive sur les plugins du fournisseur `vllm` et `sglang` fournis, docs, comportement par défaut env/URL de base, découverte `/v1/models`, et comportement associé des fournisseurs openai-compatible vllm et sglang.
- Contrôles de réflexion vLLM : Couvre les contrôles de réflexion vLLM sur les plugins du fournisseur `vllm` et `sglang` fournis, docs, comportement par défaut env/URL de base, découverte `/v1/models`, et comportement associé des fournisseurs openai-compatible vllm et sglang.
- Sémantique du chat et des outils compatible OpenAI : Couvre la sémantique du chat et des outils compatible OpenAI sur les plugins du fournisseur `vllm` et `sglang` fournis, docs, comportement par défaut env/URL de base, découverte `/v1/models`, et comportement associé des fournisseurs openai-compatible vllm et sglang.
- Conseils de compatibilité SGLang : Couvre les conseils de compatibilité SGLang sur les plugins du fournisseur `vllm` et `sglang` fournis, docs, comportement par défaut env/URL de base, découverte `/v1/models`, et comportement associé des fournisseurs openai-compatible vllm et sglang.
- Compatibilité du flux de requête : Couvre la compatibilité du flux de requête sur la mise en forme des requêtes de style chat et Responses, normalisation du streaming, compatibilité de l'appel d'outils, contrôles de raisonnement du modèle local, et comportement associé de la compatibilité du flux de requête et de l'appel d'outils.
- Appel d'outils : Couvre l'appel d'outils sur la mise en forme des requêtes de style chat et Responses, normalisation du streaming, compatibilité de l'appel d'outils, contrôles de raisonnement du modèle local, et comportement associé de la compatibilité du flux de requête et de l'appel d'outils.

Docs principales :

- `docs/providers/vllm.md`
- `docs/providers/sglang.md`
- `docs/gateway/local-models.md`
- `docs/providers/lmstudio.md`

### 4. Mémoire locale et embeddings

Ancres de recherche : Sélection du fournisseur d'embedding, Disponibilité de la recherche de mémoire, Remplacement du modèle memoryFlush, Recherche lexicale de secours, Conseils de non-concordance du fournisseur.

Note de catégorie : [Mémoire locale et embeddings](local-embeddings-and-memory-provider-usage.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Sélection du fournisseur d'embedding : Couvre la sélection du fournisseur d'embedding sur l'enregistrement du fournisseur d'embedding local pour Ollama et LM Studio, comportement d'embedding de l'hôte de mémoire, disponibilité de la recherche de mémoire, remplacements de modèle `memoryFlush` locaux, et comportement associé des embeddings locaux et de la mémoire.
- Disponibilité de la recherche de mémoire : Couvre la disponibilité de la recherche de mémoire sur l'enregistrement du fournisseur d'embedding local pour Ollama et LM Studio, comportement d'embedding de l'hôte de mémoire, disponibilité de la recherche de mémoire, remplacements de modèle `memoryFlush` locaux, et comportement associé des embeddings locaux et de la mémoire.
- Remplacement du modèle memoryFlush : Couvre le remplacement du modèle memoryFlush sur l'enregistrement du fournisseur d'embedding local pour Ollama et LM Studio, comportement d'embedding de l'hôte de mémoire, disponibilité de la recherche de mémoire, remplacements de modèle `memoryFlush` locaux, et comportement associé des embeddings locaux et de la mémoire.
- Recherche lexicale de secours : Couvre la recherche lexicale de secours sur l'enregistrement du fournisseur d'embedding local pour Ollama et LM Studio, comportement d'embedding de l'hôte de mémoire, disponibilité de la recherche de mémoire, remplacements de modèle `memoryFlush` locaux, et comportement associé des embeddings locaux et de la mémoire.
- Conseils de non-concordance du fournisseur : Couvre les conseils de non-concordance du fournisseur sur l'enregistrement du fournisseur d'embedding local pour Ollama et LM Studio, comportement d'embedding de l'hôte de mémoire, disponibilité de la recherche de mémoire, remplacements de modèle `memoryFlush` locaux, et comportement associé des embeddings locaux et de la mémoire.

Docs principales :

- `docs/concepts/memory.md`
- `docs/gateway/doctor.md`

### 5. Sécurité réseau et contrôles de requête

Ancres de recherche : Réseau de sécurité, Contrôles de pression de requête, fournisseurs de modèles locaux : ollama, vllm, sglang, lm studio réseau de sécurité et contrôles de pression de requête, réseau de sécurité et contrôles de pression de requête.

Note de catégorie : [Sécurité réseau et contrôles de requête](safety-network-and-prompt-pressure-controls.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Stable (82%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Réseau de sécurité : Couvre le réseau de sécurité sur la confiance du réseau privé et de l'origine exacte pour les URL de base du fournisseur local, protections SSRF pour la configuration auto-hébergée, assainissement des jetons spéciaux, comportement de requête allégée du modèle local, et comportement associé du réseau de sécurité et des contrôles de pression de requête.
- Contrôles de pression de requête : Couvre les contrôles de pression de requête sur la confiance du réseau privé et de l'origine exacte pour les URL de base du fournisseur local, protections SSRF pour la configuration auto-hébergée, assainissement des jetons spéciaux, comportement de requête allégée du modèle local, et comportement associé du réseau de sécurité et des contrôles de pression de requête.

Docs principales :

- `docs/gateway/security/index.md`
- `docs/gateway/config-tools.md`
- `docs/gateway/local-models.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/local-model-providers-ollama-vllm-sglang-lm-studio/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/local-model-providers-ollama-vllm-sglang-lm-studio`.
