---
read_when:
  - Explorez les options de sélection de modèles futurs et les configurations d'authentification
summary: Exploration：configuration des modèles, profils d'authentification et comportement de secours
title: Exploration de la configuration des modèles
x-i18n:
  generated_at: "2026-02-01T20:25:05Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 48623233d80f874c0ae853b51f888599cf8b50ae6fbfe47f6d7b0216bae9500b
  source_path: experiments/proposals/model-config.md
  workflow: 14
---

# Configuration des modèles (Exploration)

Ce document enregistre les **concepts** pour la configuration future des modèles. Ce n'est pas une spécification de version officielle. Pour connaître le comportement actuel, veuillez consulter :

- [Modèles](/concepts/models)
- [Basculement de modèle](/concepts/model-failover)
- [OAuth + Profils](/concepts/oauth)

## Motivation

Les opérateurs souhaitent :

- Prendre en charge plusieurs profils d'authentification par fournisseur (personnel vs professionnel).
- Une sélection `/model` simple avec un comportement de secours prévisible.
- Une séparation claire entre les modèles de texte et les modèles d'image.

## Directions possibles (haut niveau)

- Garder la sélection de modèles simple : `provider/model` plus alias optionnel.
- Permettre aux fournisseurs d'avoir plusieurs profils d'authentification et de spécifier un ordre explicite.
- Utiliser une liste de secours globale pour que toutes les sessions basculent de manière cohérente.
- Remplacer le routage d'image uniquement lorsqu'il est explicitement configuré.

## Questions en attente de résolution

- La rotation des profils doit-elle être par fournisseur ou par modèle ?
- Comment l'interface utilisateur doit-elle présenter la sélection de profils pour les sessions ?
- Quel est le chemin de migration le plus sûr à partir des clés de configuration héritées ?
