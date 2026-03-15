---
summary: "Exploration: model config, auth profiles, and fallback behavior"
read_when:
  - Exploring future model selection + auth profile ideas
title: "Model Config Exploration"
---

# Model Config (Exploration)

Ce document capture les **idées** pour la configuration future des modèles. Ce n'est pas une spécification de livraison. Pour le comportement actuel, voir :

- [Models](/concepts/models)
- [Model failover](/concepts/model-failover)
- [OAuth + profiles](/concepts/oauth)

## Motivation

Les opérateurs veulent :

- Plusieurs profils d'authentification par fournisseur (personnel vs professionnel).
- Sélection simple `/model` avec des fallbacks prévisibles.
- Séparation claire entre les modèles de texte et les modèles compatibles avec les images.

## Direction possible (haut niveau)

- Garder la sélection de modèle simple : `provider/model` avec des alias optionnels.
- Permettre aux fournisseurs d'avoir plusieurs profils d'authentification, avec un ordre explicite.
- Utiliser une liste de fallback globale pour que toutes les sessions basculent de manière cohérente.
- Ne remplacer le routage des images que lorsqu'il est explicitement configuré.

## Questions ouvertes

- La rotation de profil doit-elle être par fournisseur ou par modèle ?
- Comment l'interface utilisateur doit-elle afficher la sélection de profil pour une session ?
- Quel est le chemin de migration le plus sûr à partir des clés de configuration héritées ?
