---
title: "Agent Runtime Maturity Report"
version: 3
last_refreshed: 2026-05-31
last_refreshed_by: codex
---

# Agent Runtime Maturity Report

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Coverage: `Stable (80%)`
- Quality: `Alpha (69%)`
- Completeness: `Stable (80%)`
- LTS Features: `6/9`

## Résumé

Ce rapport promeut les preuves de maturité archivées `agent-runtime-and-provider-execution` de `/Users/kevinlin/tmp/maturity/agent-runtime-and-provider-execution` dans le contrat d'inventaire process-version-3 actuel.

Les scores de catégorie Coverage et Quality proviennent des lignes de score soutenues par les preuves archivées. Completeness est initialisé à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis joint avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                              | LTS | Coverage       | Quality       | Completeness   | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Agent Turn Execution](agent-turn-orchestration-and-runtime-lifecycle.md)             | ✅  | `Stable (82%)` | `Beta (74%)`  | `Stable (82%)` | Démarrage du tour et choix du runtime, Coordination de session et d'exécution, Abandon et résultats terminaux                                                                                                                                                                                |
| [External Runtimes and Subagents](cli-harnesses-external-runtimes-and-subagents.md)   | ❌  | `Beta (78%)`   | `Alpha (66%)` | `Beta (78%)`   | Sélection du harnais externe, Alias de runtime CLI, Tours de sous-agent, Récupération du runtime                                                                                                                                                                                          |
| [Hosted Provider Execution](hosted-provider-adapters-and-payload-compatibility.md)    | ✅  | `Beta (76%)`   | `Beta (70%)`  | `Beta (76%)`   | Tours de fournisseur hébergé, Options de modèle spécifiques au fournisseur, Utilisation d'outils hébergés, Contrôles de raisonnement et de cache, Streaming hébergé et réponses                                                                                                             |
| [Local and Self-hosted Providers](local-and-self-hosted-provider-execution.md)        | ❌  | `Beta (70%)`   | `Alpha (60%)` | `Beta (70%)`   | Profils de fournisseur local, Drapeaux de capacité d'outil, Délais d'attente et fenêtres de contexte, Vérifications de fumée locales, Gestion des défaillances locales                                                                                                                      |
| [Model and Runtime Selection](model-selection-provider-routing-and-runtime-policy.md) | ✅  | `Stable (84%)` | `Beta (72%)`  | `Stable (84%)` | Sélection de référence de modèle, Remplacements de fournisseur et de runtime, Paramètres de réflexion et de contexte, Récupération de route invalide                                                                                                                                       |
| [Provider Auth](provider-auth-profiles-and-credential-health.md)                      | ✅  | `Stable (80%)` | `Alpha (66%)` | `Stable (80%)` | Configuration de connexion et de clé API, Sélection du profil d'authentification, Vérifications de santé des identifiants, Basculement d'authentification, Récupération de secours du fournisseur, Récupération de limite de débit et de capacité, Conseils sur clé manquante et OAuth, Récupération de redémarrage et de route obsolète, Diagnostics de fournisseur structurés, Propagation des identifiants de sous-agent |
| [Streaming and Progress](streaming-progress-and-preview-visibility.md)                | ❌  | `Stable (84%)` | `Beta (70%)`  | `Stable (84%)` | Réponses en streaming, Visibilité de la progression                                                                                                                                                                                                                                        |
| [Tool Calls and Response Handling](streaming-tool-call-and-response-normalization.md) | ✅  | `Stable (80%)` | `Alpha (66%)` | `Stable (80%)` | Gestion des appels d'outil, Rapports d'utilisation et de réponse, Récupération des défaillances                                                                                                                                                                                           |
| [Tool Execution Controls](tool-execution-approvals-and-sandbox-policy.md)             | ✅  | `Stable (86%)` | `Beta (74%)`  | `Stable (86%)` | Règles de disponibilité des outils, Comportement d'exécution en sandbox, Flux d'approbation, Exécution élevée, Contrôles de sécurité des outils, Accès aux outils délégués                                                                                                                 |

## Rubrique de notation

- Coverage:
  évaluation du libellé de maturité pour l'intégration, e2e, live, ou les preuves
  de flux de serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Quality:
  évaluation du libellé de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et de flux de runtime réel sont des entrées de Coverage
  uniquement ; elles ne relèvent ni n'abaissent la Quality.
- Completeness:
  évaluation du libellé de maturité pour la façon dont la catégorie livre l'ensemble
  de capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS:
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées:
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  libellé de maturité supérieur.
- Lacunes majeures de qualité/complétude:
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Exécution des tours d'agent

Ancres de recherche : forme RPC d'agent et flux d'événements, runAgentTurnWithFallback, délai d'attente d'agent et résultats terminaux.

Note de catégorie : [Agent Turn Execution](agent-turn-orchestration-and-runtime-lifecycle.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (74%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Démarrage du tour et choix du runtime : Démarrage d'un tour d'agent et choix entre l'exécution du runtime de passerelle ou intégré.
- Coordination de session et d'exécution : Établissement des identifiants de session et d'exécution, verrous de file d'attente et coordination d'exécution associée.
- Abandon et résultats terminaux : Respect des abandons, délai d'exécution du travail du fournisseur/modèle et émission de résultats terminaux.

Documentation principale :

- `docs/concepts/agent-loop.md`
- `docs/cli/agent.md`
- `docs/concepts/agent-runtimes.md`

### 2. Runtimes externes et sous-agents

Ancres de recherche : runtimes d'agent, tours de sous-agent, alias de runtime CLI.

Note de catégorie : [External Runtimes and Subagents](cli-harnesses-external-runtimes-and-subagents.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Sélection de harnais externe : Choix du serveur d'application Codex, ACP et autres harnais de runtime externes.
- Alias de runtime CLI : Alias de runtime et chemins d'exécution basés sur CLI tels que Claude CLI et Gemini CLI.
- Tours de sous-agent : Génération, livraison et annonce du travail de sous-agent en dehors du chemin intégré par défaut.
- Récupération du runtime : Nettoyage, délai d'expiration et comportement de vivacité pour les runtimes externes et les sous-agents.

Documentation principale :

- `docs/concepts/agent-runtimes.md`
- `docs/providers/anthropic.md`
- `docs/providers/google.md`
- `docs/tools/subagents.md`

### 3. Exécution du fournisseur hébergé

Ancres de recherche : tours de fournisseur hébergé, options de modèle spécifiques au fournisseur, normalisation des réponses en streaming.

Note de catégorie : [Hosted Provider Execution](hosted-provider-adapters-and-payload-compatibility.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ✅

Fonctionnalités :

- Tours de fournisseur hébergé : Exécution de tours d'agent contre des fournisseurs hébergés tels que OpenAI, Anthropic et Google.
- Options de modèle spécifiques au fournisseur : Paramètres de modèle spécifiques au fournisseur et paramètres de demande de runtime exposés aux utilisateurs ou opérateurs.
- Utilisation d'outils hébergés : Comportement d'utilisation d'outils lorsque le runtime actif est un fournisseur hébergé.
- Contrôles de raisonnement et de cache : Contrôles spécifiques au fournisseur pour le raisonnement, la réflexion et le cache lors de l'exécution hébergée.
- Streaming hébergé et réponses : Comportement de streaming et de réponse visible par l'opérateur tandis que les adaptateurs hébergés normalisent les différences de charge utile.

Documentation principale :

- `docs/providers/openai.md`
- `docs/providers/anthropic.md`
- `docs/providers/google.md`
- `docs/concepts/models.md`

### 4. Fournisseurs locaux et auto-hébergés

Ancres de recherche : profils de fournisseur local Ollama, serveurs locaux compatibles OpenAI, vérifications de fumée locales.

Note de catégorie : [Local and Self-hosted Providers](local-and-self-hosted-provider-execution.md)

Décisions de score :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (60%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Profils de fournisseur local : Configuration du profil de modèle local pour Ollama et serveurs locaux compatibles OpenAI.
- Drapeaux de capacité d'outil : Drapeaux de capacité de fournisseur local et comportement pour l'utilisation d'outils.
- Délais d'expiration et fenêtres de contexte : Configuration du délai d'expiration et de la fenêtre de contexte du fournisseur local.
- Vérifications de fumée locales : Vérifications de fumée d'image et de modèle locales visibles par les opérateurs.
- Gestion des défaillances locales : Gestion des défaillances visible par l'opérateur pour les fournisseurs locaux et auto-hébergés.

Documentation principale :

- `docs/providers/ollama.md`
- `docs/concepts/models.md`
- `docs/cli/agent.md`

### 5. Sélection du modèle et du runtime

Ancres de recherche : sélection de référence de modèle, remplacements de runtime, paramètres de réflexion et de contexte.

Note de catégorie : [Model and Runtime Selection](model-selection-provider-routing-and-runtime-policy.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (84%)`
- LTS : ✅

Fonctionnalités :

- Sélection de référence de modèle : Sélection de la référence de modèle pour un tour d'agent à partir des valeurs par défaut de l'utilisateur ou configurées.
- Remplacements de fournisseur et de runtime : Gestion de la sélection du fournisseur et des remplacements de runtime pour un tour.
- Paramètres de réflexion et de contexte : Résolution des paramètres de réflexion et de contexte dans le cadre de la sélection du modèle.
- Récupération de route invalide : Préservation ou effacement de l'état de route invalide lorsque les sélections dérivent ou échouent.

Documentation principale :

- `docs/concepts/models.md`
- `docs/cli/models.md`
- `docs/providers/openai.md`
- `docs/concepts/agent-runtimes.md`

### 6. Authentification du fournisseur

Ancres de recherche : configuration de connexion et de clé API, sélection du profil d'authentification, récupération de secours du fournisseur.

Note de catégorie : [Provider Auth](provider-auth-profiles-and-credential-health.md)

Décisions de score :

- Couverture : `Stable (80%)`
- Qualité : `Alpha (66%)`
- Complétude : `Stable (80%)`
- LTS : ✅

Fonctionnalités :

- Configuration de connexion et de clé API : Flux de connexion, OAuth et collage de clé pour l'accès au fournisseur.
- Sélection du profil d'authentification : Sélection et validation des profils d'authentification du fournisseur.
- Vérifications de l'intégrité des identifiants : Vérifications de l'intégrité des identifiants et signaux de réparation associés du docteur et du statut.
- Basculement d'authentification : Comportement de secours d'authentification du même fournisseur et entre profils.
- Récupération de secours du fournisseur : Comportement de secours du fournisseur et du profil d'authentification en cas d'échec de l'exécution.
- Récupération des limites de débit et de capacité : Chemins de récupération pour les défaillances de quota, de capacité et de limite de débit.
- Orientation sur les clés manquantes et OAuth : Orientation de l'opérateur pour les clés manquantes, l'état OAuth expiré et les défaillances d'authentification associées.
- Récupération de redémarrage et de route obsolète : Récupération de l'état de route obsolète, exigences de redémarrage et dérive de fournisseur associée.
- Diagnostics structurés du fournisseur : Erreurs et diagnostics structurés du fournisseur livrés dans les journaux ou les réponses d'agent.
- Propagation des identifiants du sous-agent : Propagation des identifiants du fournisseur dans les flux de sous-agent et de runtime délégué.

Documentation principale :

- `docs/concepts/models.md`
- `docs/cli/agent.md`
- `docs/cli/models.md`
- `docs/providers/openai.md`
- `docs/providers/anthropic.md`
- `docs/providers/google.md`
- `docs/tools/subagents.md`

### 7. Streaming et progression

Ancres de recherche : réponses en streaming, visibilité de la progression, livraison d'événements.

Note de catégorie : [Streaming and Progress](streaming-progress-and-preview-visibility.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Beta (70%)`
- Complétude : `Stable (84%)`
- LTS : ❌

Fonctionnalités :

- Réponses en streaming : Mises à jour de bloc en streaming et sortie d'assistant partielle avant la livraison finale.
- Visibilité de la progression : Événements d'aperçu de progression et mises à jour du cycle de vie des éléments surfacés lors de l'exécution.

Documentation principale :

- `docs/concepts/streaming.md`
- `docs/concepts/agent-loop.md`

### 8. Appels d'outils et gestion des réponses

Ancres de recherche : gestion des appels d'outils, rapports d'utilisation, récupération des défaillances.

Note de catégorie : [Tool Calls and Response Handling](streaming-tool-call-and-response-normalization.md)

Décisions de score :

- Couverture : `Stable (80%)`
- Qualité : `Alpha (66%)`
- Complétude : `Stable (80%)`
- LTS : ✅

Fonctionnalités :

- Gestion des appels d'outils : Comportement fiable des appels d'outils entre les fournisseurs, y compris les différences de charge utile malformées ou spécifiques au fournisseur.
- Rapports d'utilisation et de réponse : Identifiants de réponse et comptabilité d'utilisation normalisés dans le comportement du runtime visible par l'opérateur.
- Récupération des défaillances : Finalisation du flux de défaillance et nettoyage lorsque la sortie du fournisseur est malformée ou incomplète.

Documentation principale :

- `docs/concepts/agent-loop.md`
- `docs/providers/ollama.md`

### 9. Contrôles d'exécution des outils

Ancres de recherche : règles de disponibilité des outils, comportement d'exécution en bac à sable, flux d'approbation.

Note de catégorie : [Tool Execution Controls](tool-execution-approvals-and-sandbox-policy.md)

Décisions de score :

- Couverture : `Stable (86%)`
- Qualité : `Beta (74%)`
- Complétude : `Stable (86%)`
- LTS : ✅

Fonctionnalités :

- Règles de disponibilité des outils : Quels outils sont disponibles lors d'un tour après la résolution de la politique et la suppression basée sur le fournisseur.
- Comportement d'exécution en bac à sable : Comportement d'exécution, racines de bac à sable et contraintes d'espace de travail visibles par les opérateurs.
- Flux d'approbation : Portes d'approbation de l'opérateur pour l'exécution des outils.
- Exécution élevée : Règles d'exécution d'hôte élevée et contrôles associés.
- Contrôles de sécurité des outils : Crochets avant appel d'outil et garde-fous associés qui façonnent le comportement des outils visible par l'opérateur.
- Accès aux outils délégués : Politique d'outils héritée ou réduite pour les sous-agents et l'exécution déléguée.

Documentation principale :

- `docs/gateway/sandbox-vs-tool-policy-vs-elevated.md`
- `docs/concepts/agent-loop.md`
- `docs/tools/subagents.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base de référence d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/agent-runtime-and-provider-execution/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/agent-runtime-and-provider-execution`.
