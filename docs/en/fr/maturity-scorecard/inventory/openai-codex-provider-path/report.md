---
title: "Rapport de maturité du chemin du fournisseur OpenAI / Codex"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du chemin du fournisseur OpenAI / Codex

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Beta (78%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (78%)`
- Fonctionnalités LTS : `3/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `openai-codex-provider-path` depuis `/Users/kevinlin/tmp/maturity/openai-codex-provider-path` dans le contrat d'inventaire actuel de la version 3 du processus.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                                   | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                   |
| ------------------------------------------------------------------------------------------ | --- | -------------- | ------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| [Modèle et authentification](canonical-openai-model-routing-and-catalog.md)                            | ✅  | `Beta (78%)`   | `Alpha (66%)` | `Beta (78%)`   | Routage canonique des modèles OpenAI, Catalogue, Profils OAuth Codex, Utilisation des abonnements, Diagnostics du docteur, Réparation de l'opérateur |
| [Compatibilité des réponses et des outils](codex-responses-transport-and-payload-compatibility.md) | ✅  | `Beta (76%)`   | `Beta (70%)`  | `Beta (76%)`   | Transport des réponses Codex, Compatibilité des charges utiles, Contexte des outils, Compatibilité des capacités                               |
| [Harnais Codex natif](native-codex-app-server-harness-and-thread-lifecycle.md)            | ✅  | `Stable (82%)` | `Beta (72%)`  | `Stable (82%)` | Harnais du serveur d'applications Codex natif, Cycle de vie des threads                                                                      |
| [Entrée image et multimodale](image-generation-editing-and-multimodal-input.md)             | ❌  | `Stable (80%)` | `Beta (72%)`  | `Stable (80%)` | Édition de génération d'images, Entrée multimodale                                                                             |
| [Voix et audio en temps réel](realtime-voice-transcription-and-speech.md)                     | ❌  | `Beta (72%)`   | `Alpha (68%)` | `Beta (72%)`   | Transcription vocale en temps réel, Parole                                                                                   |

## Barème de notation

- Couverture :
  notation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves du flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et du flux runtime réel sont des entrées de couverture uniquement ; ils ne
  n'augmentent ni ne diminuent la qualité.
- Complétude :
  notation de l'étiquette de maturité pour la façon dont la catégorie fournit complètement l'ensemble des
  capacités spécifiques à la surface. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Modèle et authentification

Ancres de recherche : Routage canonique des modèles OpenAI, Catalogue, openai / codex provider path canonical openai model routing and catalog, canonical openai model routing and catalog, Profils OAuth Codex, Utilisation des abonnements, openai / codex provider path codex oauth profiles and subscription usage, codex oauth profiles and subscription usage, Diagnostics du docteur, Réparation de l'opérateur, openai / codex provider path doctor diagnostics and operator repair, doctor diagnostics and operator repair.

Note de catégorie : [Modèle et authentification](canonical-openai-model-routing-and-catalog.md)

Décisions de notation :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Routage canonique des modèles OpenAI : Couvre le routage canonique des modèles OpenAI dans le contrat de route de modèle orienté utilisateur/opérateur : références canoniques `openai/gpt-*`, références de modèles hérités `openai-codex/*`, lignes du catalogue de modèles, limites de contexte et comportement canonique de routage et catalogue des modèles OpenAI associé.
- Catalogue : Couvre le catalogue dans le contrat de route de modèle orienté utilisateur/opérateur : références canoniques `openai/gpt-*`, références de modèles hérités `openai-codex/*`, lignes du catalogue de modèles, limites de contexte et comportement canonique de routage et catalogue des modèles OpenAI associé.
- Profils OAuth Codex : Couvre les profils OAuth Codex dans les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation de l'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.
- Utilisation des abonnements : Couvre l'utilisation des abonnements dans les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation de l'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.
- Diagnostics du docteur : Couvre les diagnostics du docteur dans la réparation et le diagnostic orientés opérateur pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles runtime, sidecars de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.
- Réparation de l'opérateur : Couvre la réparation de l'opérateur dans la réparation et le diagnostic orientés opérateur pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles runtime, sidecars de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.

Documentation principale :

- `docs/providers/openai.md`
- `docs/plugins/codex-harness.md`
- `docs/concepts/models.md`
- `docs/concepts/oauth.md`
- `docs/plugins/codex-harness-reference.md`
- `docs/automation/auth-monitoring.md`

### 2. Compatibilité des réponses et des outils

Ancres de recherche : Transport des réponses Codex, Compatibilité des charges utiles, openai / codex provider path codex responses transport and payload compatibility, codex responses transport and payload compatibility, Contexte des outils, Compatibilité des capacités, openai / codex provider path tool context and capability compatibility, tool context and capability compatibility.

Note de catégorie : [Compatibilité des réponses et des outils](codex-responses-transport-and-payload-compatibility.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ✅

Fonctionnalités :

- Transport des réponses Codex : Couvre le transport des réponses Codex dans le chemin de requête/streaming du fournisseur de bas niveau pour `openai-codex-responses` et le code de conversion des réponses OpenAI partagé utilisé par les routes de compatibilité OpenAI directe et Codex-auth.
- Compatibilité des charges utiles : Couvre la compatibilité des charges utiles dans le chemin de requête/streaming du fournisseur de bas niveau pour `openai-codex-responses` et le code de conversion des réponses OpenAI partagé utilisé par les routes de compatibilité OpenAI directe et Codex-auth.
- Contexte des outils : Couvre le contexte des outils dans les outils orientés fournisseur, l'injection de contexte, les entrées multimédias, la propriété des outils natifs par rapport aux clients, la compatibilité des réponses OpenAI et la façon dont les modèles OpenAI/Codex reçoivent le contexte runtime OpenClaw.
- Compatibilité des capacités : Couvre la compatibilité des capacités dans les outils orientés fournisseur, l'injection de contexte, les entrées multimédias, la propriété des outils natifs par rapport aux clients, la compatibilité des réponses OpenAI et la façon dont les modèles OpenAI/Codex reçoivent le contexte runtime OpenClaw.

Documentation principale :

- `docs/providers/openai.md`
- `docs/gateway/openresponses-http-api.md`
- `docs/gateway/openai-http-api.md`
- `docs/plugins/codex-native-plugins.md`

### 3. Harnais Codex natif

Ancres de recherche : Harnais du serveur d'applications Codex natif, Cycle de vie des threads, openai / codex provider path native codex app-server harness and thread lifecycle, native codex app-server harness and thread lifecycle.

Note de catégorie : [Harnais Codex natif](native-codex-app-server-harness-and-thread-lifecycle.md)

Décisions de notation :

- Couverture : `Stable (82%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Harnais du serveur d'applications Codex natif : Couvre le harnais du serveur d'applications Codex natif dans le chemin runtime du serveur d'applications Codex natif utilisé par les tours d'agent OpenAI lorsque le harnais Codex possède l'identité du thread, la boucle de modèle natif, la compaction, les outils natifs et les contrôles du serveur d'applications natif.
- Cycle de vie des threads : Couvre le cycle de vie des threads dans le chemin runtime du serveur d'applications Codex natif utilisé par les tours d'agent OpenAI lorsque le harnais Codex possède l'identité du thread, la boucle de modèle natif, la compaction, les outils natifs et les contrôles du serveur d'applications natif.

Documentation principale :

- `docs/plugins/codex-harness.md`
- `docs/plugins/codex-harness-runtime.md`
- `docs/plugins/codex-harness-reference.md`
- `docs/plugins/codex-native-plugins.md`

### 4. Entrée image et multimodale

Ancres de recherche : Édition de génération d'images, Entrée multimodale, openai / codex provider path image generation editing and multimodal input, image generation editing and multimodal input.

Note de catégorie : [Entrée image et multimodale](image-generation-editing-and-multimodal-input.md)

Décisions de notation :

- Couverture : `Stable (80%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (80%)`
- LTS : ❌

Fonctionnalités :

- Édition de génération d'images : Couvre l'édition de génération d'images dans la génération et l'édition d'images OpenAI, le backend d'images OAuth Codex, le routage de fond transparent, les points de terminaison d'images Azure/OpenAI privées et le comportement associé de génération d'images et d'entrée multimodale.
- Entrée multimodale : Couvre l'entrée multimodale dans la génération et l'édition d'images OpenAI, le backend d'images OAuth Codex, le routage de fond transparent, les points de terminaison d'images Azure/OpenAI privées et le comportement associé de génération d'images et d'entrée multimodale.

Documentation principale :

- `docs/providers/openai.md`
- `docs/tools/image-generation.md`
- `docs/nodes/images.md`

### 5. Voix et audio en temps réel

Ancres de recherche : Transcription vocale en temps réel, Parole, openai / codex provider path realtime voice transcription and speech, realtime voice transcription and speech.

Note de catégorie : [Voix et audio en temps réel](realtime-voice-transcription-and-speech.md)

Décisions de notation :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Transcription vocale en temps réel : Couvre la transcription vocale en temps réel dans la synthèse vocale OpenAI, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, le navigateur Talk/WebRTC, les ponts WebSocket backend, la frappe de secret client soutenue par OAuth, les déploiements Azure Realtime et le comportement de contrôle vocal.
- Parole : Couvre la parole dans la synthèse vocale OpenAI, la transcription vocale par lot, la transcription en temps réel, la voix en temps réel, le navigateur Talk/WebRTC, les ponts WebSocket backend, la frappe de secret client soutenue par OAuth, les déploiements Azure Realtime et le comportement de contrôle vocal.

Documentation principale :

- `docs/providers/openai.md`
- `docs/channels/discord.md`
- `docs/plugins/voice-call.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/openai-codex-provider-path/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/openai-codex-provider-path`.
