---
title: "Rapport de maturité du chemin du fournisseur Anthropic"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du chemin du fournisseur Anthropic

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Stable (80%)`
- Qualité : `Beta (74%)`
- Complétude : `Stable (80%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `anthropic-provider-path` de `/Users/kevinlin/tmp/maturity/anthropic-provider-path` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                                     | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Authentification et récupération du fournisseur](auth-onboarding-and-credential-profile-health.md)               | ❌  | `Beta (78%)`   | `Beta (70%)`   | `Beta (78%)`   | Intégration des clés API, Réutilisation des identifiants Claude CLI, Authentification par jeton de configuration, Santé du profil d'authentification, État du modèle, Fenêtres d'utilisation, Rapports de refroidissement/profil, Récupération de contexte long, Conseils de secours                                     |
| [Sélection du modèle et de l'exécution](model-catalog-aliases-and-runtime-policy.md)                   | ❌  | `Stable (82%)` | `Alpha (68%)`  | `Stable (82%)` | Catalogue Claude groupé, Références anthropic canoniques, Compatibilité Claude CLI, Disponibilité du sélecteur de modèle, Métadonnées de capacité, Sélection de l'exécution, Continuité de session, Pont MCP/outil, Mappage du mode de permission, Prélude de secours |
| [Transport des requêtes et sémantique des tours](direct-anthropic-messages-transport-and-streaming.md) | ❌  | `Stable (82%)` | `Beta (72%)`   | `Stable (82%)` | Transport par clé API/OAuth, Charges utiles des messages, Décodage du streaming, Utilisation et raisons d'arrêt, Gestion des abandons/erreurs, Blocs d'utilisation d'outils, Relecture des résultats d'outils, Récupération JSON partielle, Réflexion native, Relecture de réflexion signée/masquée      |
| [Cache de prompt et contexte](prompt-caching-context-windows-and-request-knobs.md)              | ❌  | `Stable (82%)` | `Beta (76%)`   | `Stable (82%)` | Rétention du cache, Limite du cache du prompt système, Contexte 1M, Mode rapide/niveau de service, Diagnostics du cache                                                                                                                          |
| [Entrées médias](media-understanding-and-document-inputs.md)                                   | ❌  | `Beta (74%)`   | `Stable (82%)` | `Beta (74%)`   | Entrée d'image, Entrée de document PDF, Secours du modèle médias, Résultats d'outils d'image                                                                                                                                                     |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/exécution
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux d'exécution réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
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

### 1. Authentification du fournisseur et récupération

Ancres de recherche : Intégration de clé API, Réutilisation des identifiants Claude CLI, Authentification par jeton de configuration, Santé du profil d'authentification, État du modèle, Fenêtres d'utilisation, Signalement de refroidissement/profil, Récupération de contexte long, Conseils de secours.

Note de catégorie : [Authentification du fournisseur et récupération](auth-onboarding-and-credential-profile-health.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Intégration de clé API : Couvre l'intégration de clé API sur toute la surface des identifiants Anthropic avant qu'une demande de modèle ne soit effectuée : choix d'intégration, stockage de clé API, migration des identifiants Claude CLI, validation du jeton de configuration, et comportement connexe de configuration et de santé des identifiants.
- Réutilisation des identifiants Claude CLI : Couvre la réutilisation des identifiants Claude CLI sur toute la surface des identifiants Anthropic avant qu'une demande de modèle ne soit effectuée : choix d'intégration, stockage de clé API, migration des identifiants Claude CLI, validation du jeton de configuration, et comportement connexe de configuration et de santé des identifiants.
- Authentification par jeton de configuration : Couvre l'authentification par jeton de configuration sur toute la surface des identifiants Anthropic avant qu'une demande de modèle ne soit effectuée : choix d'intégration, stockage de clé API, migration des identifiants Claude CLI, validation du jeton de configuration, et comportement connexe de configuration et de santé des identifiants.
- Santé du profil d'authentification : Couvre la santé du profil d'authentification sur toute la surface des identifiants Anthropic avant qu'une demande de modèle ne soit effectuée : choix d'intégration, stockage de clé API, migration des identifiants Claude CLI, validation du jeton de configuration, et comportement connexe de configuration et de santé des identifiants.
- État du modèle : Couvre l'état du modèle sur les diagnostics d'opérateur et la récupération des défaillances du fournisseur Anthropic : sortie d'état, fenêtres d'utilisation, signalement de source de profil d'authentification, signalement de profil refroidi et désactivé, et comportement connexe de diagnostics et de récupération.
- Fenêtres d'utilisation : Couvre les fenêtres d'utilisation sur les diagnostics d'opérateur et la récupération des défaillances du fournisseur Anthropic : sortie d'état, fenêtres d'utilisation, signalement de source de profil d'authentification, signalement de profil refroidi et désactivé, et comportement connexe de diagnostics et de récupération.
- Signalement de refroidissement/profil : Couvre le signalement de refroidissement/profil sur les diagnostics d'opérateur et la récupération des défaillances du fournisseur Anthropic : sortie d'état, fenêtres d'utilisation, signalement de source de profil d'authentification, signalement de profil refroidi et désactivé, et comportement connexe de diagnostics et de récupération.
- Récupération de contexte long : Couvre la récupération de contexte long sur les diagnostics d'opérateur et la récupération des défaillances du fournisseur Anthropic : sortie d'état, fenêtres d'utilisation, signalement de source de profil d'authentification, signalement de profil refroidi et désactivé, et comportement connexe de diagnostics et de récupération.
- Conseils de secours : Couvre les conseils de secours sur les diagnostics d'opérateur et la récupération des défaillances du fournisseur Anthropic : sortie d'état, fenêtres d'utilisation, signalement de source de profil d'authentification, signalement de profil refroidi et désactivé, et comportement connexe de diagnostics et de récupération.

Docs principales :

- `docs/providers/anthropic.md`
- `docs/gateway/doctor.md`
- `docs/gateway/configuration-examples.md`
- `docs/gateway/troubleshooting.md`
- `docs/reference/prompt-caching.md`

### 2. Sélection du modèle et du runtime

Ancres de recherche : Catalogue Claude groupé, Références anthropic canoniques, Compatibilité Claude CLI, Disponibilité du sélecteur de modèle, Métadonnées de capacité, Sélection du runtime, Continuité de session, Pont MCP/outil, Mappage du mode de permission, Prélude de secours.

Note de catégorie : [Sélection du modèle et du runtime](model-catalog-aliases-and-runtime-policy.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Alpha (68%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Catalogue Claude groupé : Couvre le catalogue Claude groupé sur la couche de catalogue de modèles Anthropic et de politique : lignes de modèles groupés, alias de modèles, normalisation d'ID de modèle Claude actuelle et future, sélection de runtime-fournisseur, et comportement connexe de catalogue de modèles et de politique.
- Références anthropic canoniques : Couvre les références anthropic canoniques sur la couche de catalogue de modèles Anthropic et de politique : lignes de modèles groupés, alias de modèles, normalisation d'ID de modèle Claude actuelle et future, sélection de runtime-fournisseur, et comportement connexe de catalogue de modèles et de politique.
- Compatibilité Claude CLI : Couvre la compatibilité Claude CLI sur la couche de catalogue de modèles Anthropic et de politique : lignes de modèles groupés, alias de modèles, normalisation d'ID de modèle Claude actuelle et future, sélection de runtime-fournisseur, et comportement connexe de catalogue de modèles et de politique.
- Disponibilité du sélecteur de modèle : Couvre la disponibilité du sélecteur de modèle sur la couche de catalogue de modèles Anthropic et de politique : lignes de modèles groupés, alias de modèles, normalisation d'ID de modèle Claude actuelle et future, sélection de runtime-fournisseur, et comportement connexe de catalogue de modèles et de politique.
- Métadonnées de capacité : Couvre les métadonnées de capacité sur la couche de catalogue de modèles Anthropic et de politique : lignes de modèles groupés, alias de modèles, normalisation d'ID de modèle Claude actuelle et future, sélection de runtime-fournisseur, et comportement connexe de catalogue de modèles et de politique.
- Sélection du runtime : Couvre la sélection du runtime sur le chemin Claude CLI local d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, pont d'outil MCP, mode d'outil natif, et comportement connexe du backend claude cli.
- Continuité de session : Couvre la continuité de session sur le chemin Claude CLI local d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, pont d'outil MCP, mode d'outil natif, et comportement connexe du backend claude cli.
- Pont MCP/outil : Couvre le pont MCP/outil sur le chemin Claude CLI local d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, pont d'outil MCP, mode d'outil natif, et comportement connexe du backend claude cli.
- Mappage du mode de permission : Couvre le mappage du mode de permission sur le chemin Claude CLI local d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, pont d'outil MCP, mode d'outil natif, et comportement connexe du backend claude cli.
- Prélude de secours : Couvre le prélude de secours sur le chemin Claude CLI local d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, pont d'outil MCP, mode d'outil natif, et comportement connexe du backend claude cli.

Docs principales :

- `docs/providers/anthropic.md`
- `docs/gateway/config-agents.md`
- `docs/concepts/models.md`
- `docs/gateway/cli-backends.md`

### 3. Transport de demande et sémantique de tour

Ancres de recherche : Transport de clé API/OAuth, Charges utiles de messages, Décodage de flux, Raisons d'utilisation et d'arrêt, Gestion d'abandon/erreur, Blocs d'utilisation d'outil, Relecture de résultat d'outil, Récupération JSON partielle, Réflexion native, Relecture de réflexion signée/rédactée.

Note de catégorie : [Transport de demande et sémantique de tour](direct-anthropic-messages-transport-and-streaming.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Transport de clé API/OAuth : Couvre le transport de clé API/OAuth sur le comportement direct de demande et de flux Anthropic `api: "anthropic-messages"` : configuration du transport de clé API et OAuth, en-têtes bêta Anthropic, normalisation d'ID de modèle pour les hôtes directs, construction de charge utile, et comportement connexe de l'API anthropic directe.
- Charges utiles de messages : Couvre les charges utiles de messages sur le comportement direct de demande et de flux Anthropic `api: "anthropic-messages"` : configuration du transport de clé API et OAuth, en-têtes bêta Anthropic, normalisation d'ID de modèle pour les hôtes directs, construction de charge utile, et comportement connexe de l'API anthropic directe.
- Décodage de flux : Couvre le décodage de flux sur le comportement direct de demande et de flux Anthropic `api: "anthropic-messages"` : configuration du transport de clé API et OAuth, en-têtes bêta Anthropic, normalisation d'ID de modèle pour les hôtes directs, construction de charge utile, et comportement connexe de l'API anthropic directe.
- Raisons d'utilisation et d'arrêt : Couvre les raisons d'utilisation et d'arrêt sur le comportement direct de demande et de flux Anthropic `api: "anthropic-messages"` : configuration du transport de clé API et OAuth, en-têtes bêta Anthropic, normalisation d'ID de modèle pour les hôtes directs, construction de charge utile, et comportement connexe de l'API anthropic directe.
- Gestion d'abandon/erreur : Couvre la gestion d'abandon/erreur sur le comportement direct de demande et de flux Anthropic `api: "anthropic-messages"` : configuration du transport de clé API et OAuth, en-têtes bêta Anthropic, normalisation d'ID de modèle pour les hôtes directs, construction de charge utile, et comportement connexe de l'API anthropic directe.
- Blocs d'utilisation d'outil : Couvre les blocs d'utilisation d'outil sur la sémantique de tour spécifique à Anthropic à l'intérieur des exécutions d'agent : déclarations d'outil, conversion de bloc d'utilisation d'outil, conversion de résultat d'outil, normalisation d'ID d'appel d'outil, et comportement connexe des outils et de la réflexion.
- Relecture de résultat d'outil : Couvre la relecture de résultat d'outil sur la sémantique de tour spécifique à Anthropic à l'intérieur des exécutions d'agent : déclarations d'outil, conversion de bloc d'utilisation d'outil, conversion de résultat d'outil, normalisation d'ID d'appel d'outil, et comportement connexe des outils et de la réflexion.
- Récupération JSON partielle : Couvre la récupération JSON partielle sur la sémantique de tour spécifique à Anthropic à l'intérieur des exécutions d'agent : déclarations d'outil, conversion de bloc d'utilisation d'outil, conversion de résultat d'outil, normalisation d'ID d'appel d'outil, et comportement connexe des outils et de la réflexion.
- Réflexion native : Couvre la réflexion native sur la sémantique de tour spécifique à Anthropic à l'intérieur des exécutions d'agent : déclarations d'outil, conversion de bloc d'utilisation d'outil, conversion de résultat d'outil, normalisation d'ID d'appel d'outil, et comportement connexe des outils et de la réflexion.
- Relecture de réflexion signée/rédactée : Couvre la relecture de réflexion signée/rédactée sur la sémantique de tour spécifique à Anthropic à l'intérieur des exécutions d'agent : déclarations d'outil, conversion de bloc d'utilisation d'outil, conversion de résultat d'outil, normalisation d'ID d'appel d'outil, et comportement connexe des outils et de la réflexion.

Docs principales :

- `docs/providers/anthropic.md`
- `docs/reference/prompt-caching.md`
- `docs/gateway/troubleshooting.md`
- `docs/gateway/cli-backends.md`
- `docs/concepts/model-providers.md`

### 4. Cache de prompt et contexte

Ancres de recherche : Rétention du cache, Limite de cache de prompt système, Contexte de 1M, Mode rapide/niveau de service, Diagnostics du cache.

Note de catégorie : [Cache de prompt et contexte](prompt-caching-context-windows-and-request-knobs.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (76%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Rétention du cache : Couvre la rétention du cache sur les boutons de demande spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache de prompt, marqueurs de contrôle du cache, limite de cache de prompt système, dimensionnement du contexte de 1M, et comportement connexe du cache de prompt et du contexte.
- Limite de cache de prompt système : Couvre la limite de cache de prompt système sur les boutons de demande spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache de prompt, marqueurs de contrôle du cache, limite de cache de prompt système, dimensionnement du contexte de 1M, et comportement connexe du cache de prompt et du contexte.
- Contexte de 1M : Couvre le contexte de 1M sur les boutons de demande spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache de prompt, marqueurs de contrôle du cache, limite de cache de prompt système, dimensionnement du contexte de 1M, et comportement connexe du cache de prompt et du contexte.
- Mode rapide/niveau de service : Couvre le mode rapide/niveau de service sur les boutons de demande spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache de prompt, marqueurs de contrôle du cache, limite de cache de prompt système, dimensionnement du contexte de 1M, et comportement connexe du cache de prompt et du contexte.
- Diagnostics du cache : Couvre les diagnostics du cache sur les boutons de demande spécifiques à Anthropic en dehors du flux de contenu principal : rétention du cache de prompt, marqueurs de contrôle du cache, limite de cache de prompt système, dimensionnement du contexte de 1M, et comportement connexe du cache de prompt et du contexte.

Docs principales :

- `docs/providers/anthropic.md`
- `docs/reference/prompt-caching.md`
- `docs/gateway/troubleshooting.md`
- `docs/gateway/heartbeat.md`

### 5. Entrées médias

Ancres de recherche : Entrée d'image, Entrée de document PDF, Secours du modèle média, Résultats d'outil d'image.

Note de catégorie : [Entrées médias](media-understanding-and-document-inputs.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Stable (82%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Entrée d'image : Couvre l'entrée d'image sur la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées d'entrée de document PDF natif, sélection de modèle média par défaut, priorité automatique, et comportement connexe des entrées médias.
- Entrée de document PDF : Couvre l'entrée de document PDF sur la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées d'entrée de document PDF natif, sélection de modèle média par défaut, priorité automatique, et comportement connexe des entrées médias.
- Secours du modèle média : Couvre le secours du modèle média sur la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées d'entrée de document PDF natif, sélection de modèle média par défaut, priorité automatique, et comportement connexe des entrées médias.
- Résultats d'outil d'image : Couvre les résultats d'outil d'image sur la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées d'entrée de document PDF natif, sélection de modèle média par défaut, priorité automatique, et comportement connexe des entrées médias.

Docs principales :

- `docs/providers/anthropic.md`
- `docs/gateway/config-agents.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/anthropic-provider-path/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/anthropic-provider-path`.
