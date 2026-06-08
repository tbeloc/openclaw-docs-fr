---
title: "Rapport de maturité des fournisseurs hébergés long-tail"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité des fournisseurs hébergés long-tail

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (60%)`
- Complétude : `Alpha (64%)`
- Fonctionnalités LTS : `0/3`

## Résumé

Ce rapport promeut les preuves de maturité archivées `long-tail-hosted-providers` de `/Users/kevinlin/tmp/maturity/long-tail-hosted-providers` dans le contrat d'inventaire actuel de la version-3 du processus.

Les scores de couverture et de qualité de la catégorie proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                            | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Fournisseurs LLM hébergés](openai-compatible-hosted-text-adapters.md)   | ❌  | `Alpha (58%)` | `Alpha (56%)` | `Alpha (58%)` | Configuration Bedrock, Routage Gateway/proxy, Accès hébergé Copilot/OpenCode, Diagnostics de capacité proxy, Complétude de texte hébergée, Compatibilité des appels d'outils et du streaming, Résolution du catalogue de modèles, Mise en forme des requêtes spécifiques au fournisseur, Configuration du fournisseur régional, Routage régional et plan, Smoke test régional en direct, Diagnostics des prérequis de compte |
| [Fournisseurs de médias hébergés](hosted-media-generation-providers.md)      | ❌  | `Beta (70%)`  | `Alpha (64%)` | `Beta (70%)`  | Fournisseurs de génération d'images, Fournisseurs de génération vidéo, Fournisseurs de génération musicale, Couverture des modes médias, Fournisseurs de synthèse vocale, Fournisseurs de reconnaissance vocale, Fournisseurs de transcription en temps réel, Diagnostics des formats audio                                                                                                                 |
| [Opérations du fournisseur](setup-auth-profiles-and-credential-health.md) | ❌  | `Alpha (64%)` | `Alpha (60%)` | `Alpha (64%)` | Répertoire des fournisseurs, Catalogue d'installation des fournisseurs, Métadonnées du catalogue de modèles, Vérifications de parité du catalogue, Descripteurs de configuration du fournisseur, Profils d'authentification et alias, Sondes de santé des identifiants, Rotation et récupération des clés, Smoke test direct du fournisseur, Smoke test Gateway en direct, Sondes d'état des modèles, Trace de secours et réparation                                     |

## Barème de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct, ou les preuves de flux
  serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests
  unitaires, d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; elles ne relèvent ni n'abaissent la qualité.
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
  texte de preuves uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Fournisseurs LLM hébergés

Ancres de recherche : Configuration de Bedrock, Routage de passerelle/proxy, Accès hébergé Copilot/OpenCode, Diagnostics de capacité proxy, Complétion de texte hébergée, Compatibilité des appels d'outils et du streaming, Résolution du catalogue de modèles, Mise en forme des requêtes spécifiques au fournisseur, Configuration du fournisseur régional, Routage régional et plan, Smoke test régional en direct, Diagnostics des prérequis de compte.

Note de catégorie : [Fournisseurs LLM hébergés](openai-compatible-hosted-text-adapters.md)

Décisions de score :

- Couverture : `Alpha (58%)`
- Qualité : `Alpha (56%)`
- Complétude : `Alpha (58%)`
- LTS : ❌

Fonctionnalités :

- Configuration de Bedrock : Couvre la configuration de Bedrock sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway, et le comportement des fournisseurs cloud et passerelle associés.
- Routage de passerelle/proxy : Couvre le routage de passerelle/proxy sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway, et le comportement des fournisseurs cloud et passerelle associés.
- Accès hébergé Copilot/OpenCode : Couvre l'accès hébergé Copilot/OpenCode sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway, et le comportement des fournisseurs cloud et passerelle associés.
- Diagnostics de capacité proxy : Couvre les diagnostics de capacité proxy sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway, et le comportement des fournisseurs cloud et passerelle associés.
- Complétion de texte hébergée : Couvre la complétion de texte hébergée sur les fournisseurs de texte hébergés qui utilisent principalement des routes compatibles OpenAI ou des variantes proches : DeepSeek, Groq, Mistral, Together, et le comportement des fournisseurs de texte hébergés compatibles openai associés.
- Compatibilité des appels d'outils et du streaming : Couvre la compatibilité des appels d'outils et du streaming sur les fournisseurs de texte hébergés qui utilisent principalement des routes compatibles OpenAI ou des variantes proches : DeepSeek, Groq, Mistral, Together, et le comportement des fournisseurs de texte hébergés compatibles openai associés.
- Résolution du catalogue de modèles : Couvre la résolution du catalogue de modèles sur les fournisseurs de texte hébergés qui utilisent principalement des routes compatibles OpenAI ou des variantes proches : DeepSeek, Groq, Mistral, Together, et le comportement des fournisseurs de texte hébergés compatibles openai associés.
- Mise en forme des requêtes spécifiques au fournisseur : Couvre la mise en forme des requêtes spécifiques au fournisseur sur les fournisseurs de texte hébergés qui utilisent principalement des routes compatibles OpenAI ou des variantes proches : DeepSeek, Groq, Mistral, Together, et le comportement des fournisseurs de texte hébergés compatibles openai associés.
- Configuration du fournisseur régional : Couvre la configuration du fournisseur régional sur Qwen, Alibaba, Tencent, Qianfan, et le comportement des fournisseurs llm hébergés régionaux associés.
- Routage régional et plan : Couvre le routage régional et plan sur Qwen, Alibaba, Tencent, Qianfan, et le comportement des fournisseurs llm hébergés régionaux associés.
- Smoke test régional en direct : Couvre le smoke test régional en direct sur Qwen, Alibaba, Tencent, Qianfan, et le comportement des fournisseurs llm hébergés régionaux associés.
- Diagnostics des prérequis de compte : Couvre les diagnostics des prérequis de compte sur Qwen, Alibaba, Tencent, Qianfan, et le comportement des fournisseurs llm hébergés régionaux associés.

Documentation principale :

- `docs/providers/index.md`
- `docs/concepts/model-providers.md`
- `docs/help/testing-live.md`
- `docs/cli/onboard.md`

### 2. Fournisseurs de médias hébergés

Ancres de recherche : Fournisseurs de génération d'images, Fournisseurs de génération de vidéos, Fournisseurs de génération de musique, Couverture du mode média, Fournisseurs de synthèse vocale, Fournisseurs de reconnaissance vocale, Fournisseurs de transcription en temps réel, Diagnostics de format audio.

Note de catégorie : [Fournisseurs de médias hébergés](hosted-media-generation-providers.md)

Décisions de score :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (64%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Fournisseurs de génération d'images : Couvre les fournisseurs de génération d'images sur les chemins de fournisseurs de génération d'images, vidéos et musique hébergés, y compris DeepInfra, et le comportement des fournisseurs de génération de médias hébergés associés.
- Fournisseurs de génération de vidéos : Couvre les fournisseurs de génération de vidéos sur les chemins de fournisseurs de génération d'images, vidéos et musique hébergés, y compris DeepInfra, et le comportement des fournisseurs de génération de médias hébergés associés.
- Fournisseurs de génération de musique : Couvre les fournisseurs de génération de musique sur les chemins de fournisseurs de génération d'images, vidéos et musique hébergés, y compris DeepInfra, et le comportement des fournisseurs de génération de médias hébergés associés.
- Couverture du mode média : Couvre la couverture du mode média sur les chemins de fournisseurs de génération d'images, vidéos et musique hébergés, y compris DeepInfra, et le comportement des fournisseurs de génération de médias hébergés associés.
- Fournisseurs de synthèse vocale : Couvre les fournisseurs de synthèse vocale sur les chemins de synthèse vocale, reconnaissance vocale, transcription en temps réel, audio téléphonique, et le comportement des fournisseurs de parole, transcription et audio hébergés associés.
- Fournisseurs de reconnaissance vocale : Couvre les fournisseurs de reconnaissance vocale sur les chemins de synthèse vocale, reconnaissance vocale, transcription en temps réel, audio téléphonique, et le comportement des fournisseurs de parole, transcription et audio hébergés associés.
- Fournisseurs de transcription en temps réel : Couvre les fournisseurs de transcription en temps réel sur les chemins de synthèse vocale, reconnaissance vocale, transcription en temps réel, audio téléphonique, et le comportement des fournisseurs de parole, transcription et audio hébergés associés.
- Diagnostics de format audio : Couvre les diagnostics de format audio sur les chemins de synthèse vocale, reconnaissance vocale, transcription en temps réel, audio téléphonique, et le comportement des fournisseurs de parole, transcription et audio hébergés associés.

Documentation principale :

- `docs/plugins/manifest.md`
- `docs/help/testing-live.md`
- `docs/providers/index.md`

### 3. Opérations de fournisseur

Ancres de recherche : Répertoire des fournisseurs, Catalogue d'installation des fournisseurs, Métadonnées du catalogue de modèles, Vérifications de parité du catalogue, Descripteurs de configuration du fournisseur, Profils d'authentification et alias, Sondes de santé des identifiants, Rotation et récupération des clés, Smoke test direct du fournisseur, Smoke test en direct de la passerelle, Sondes d'état des modèles, Trace de secours et réparation.

Note de catégorie : [Opérations de fournisseur](setup-auth-profiles-and-credential-health.md)

Décisions de score :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (60%)`
- Complétude : `Alpha (64%)`
- LTS : ❌

Fonctionnalités :

- Répertoire des fournisseurs : Couvre le répertoire des fournisseurs sur le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des fournisseurs de modèles, les métadonnées des fournisseurs de manifeste, et le comportement de découverte et catalogue de fournisseurs associé.
- Catalogue d'installation des fournisseurs : Couvre le catalogue d'installation des fournisseurs sur le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des fournisseurs de modèles, les métadonnées des fournisseurs de manifeste, et le comportement de découverte et catalogue de fournisseurs associé.
- Métadonnées du catalogue de modèles : Couvre les métadonnées du catalogue de modèles sur le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des fournisseurs de modèles, les métadonnées des fournisseurs de manifeste, et le comportement de découverte et catalogue de fournisseurs associé.
- Vérifications de parité du catalogue : Couvre les vérifications de parité du catalogue sur le répertoire public des fournisseurs, les liens de documentation des fournisseurs, les tableaux de vue d'ensemble des fournisseurs de modèles, les métadonnées des fournisseurs de manifeste, et le comportement de découverte et catalogue de fournisseurs associé.
- Descripteurs de configuration du fournisseur : Couvre les descripteurs de configuration du fournisseur sur les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification, et le comportement de configuration et santé des identifiants associé.
- Profils d'authentification et alias : Couvre les profils d'authentification et alias sur les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification, et le comportement de configuration et santé des identifiants associé.
- Sondes de santé des identifiants : Couvre les sondes de santé des identifiants sur les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification, et le comportement de configuration et santé des identifiants associé.
- Rotation et récupération des clés : Couvre la rotation et récupération des clés sur les descripteurs de configuration du fournisseur, les choix d'authentification du fournisseur, les métadonnées des variables d'environnement d'authentification, les alias d'authentification, et le comportement de configuration et santé des identifiants associé.
- Smoke test direct du fournisseur : Couvre le smoke test direct du fournisseur sur le smoke test direct du fournisseur/modèle en direct, le smoke test du profil de passerelle en direct, `models status --probe`, les buckets d'authentification/état, et le comportement de diagnostics de fournisseur et réparation de secours associé.
- Smoke test en direct de la passerelle : Couvre le smoke test en direct de la passerelle sur le smoke test direct du fournisseur/modèle en direct, le smoke test du profil de passerelle en direct, `models status --probe`, les buckets d'authentification/état, et le comportement de diagnostics de fournisseur et réparation de secours associé.
- Sondes d'état des modèles : Couvre les sondes d'état des modèles sur le smoke test direct du fournisseur/modèle en direct, le smoke test du profil de passerelle en direct, `models status --probe`, les buckets d'authentification/état, et le comportement de diagnostics de fournisseur et réparation de secours associé.
- Trace de secours et réparation : Couvre la trace de secours et réparation sur le smoke test direct du fournisseur/modèle en direct, le smoke test du profil de passerelle en direct, `models status --probe`, les buckets d'authentification/état, et le comportement de diagnostics de fournisseur et réparation de secours associé.

Documentation principale :

- `docs/providers/index.md`
- `docs/concepts/model-providers.md`
- `docs/plugins/manifest.md`
- `docs/help/testing-live.md`
- `docs/cli/models.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/long-tail-hosted-providers/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/long-tail-hosted-providers`.
