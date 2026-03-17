---
summary: "Livre de recettes pour ajouter une nouvelle capacité partagée à OpenClaw"
read_when:
  - Adding a new core capability and plugin seam
  - Deciding whether code belongs in core, a vendor plugin, or a feature plugin
  - Wiring a new runtime helper for channels or tools
title: "Capability Cookbook"
---

# Livre de recettes des capacités

Utilisez ceci quand OpenClaw a besoin d'un nouveau domaine tel que la génération d'images, la génération de vidéos, ou un futur domaine de fonctionnalités soutenu par un fournisseur.

La règle :

- plugin = limite de propriété
- capability = contrat de base partagé

Cela signifie que vous ne devriez pas commencer par connecter directement un fournisseur à un canal ou un outil. Commencez par définir la capacité.

## Quand créer une capacité

Créez une nouvelle capacité quand tous ces éléments sont vrais :

1. plus d'un fournisseur pourrait plausiblement l'implémenter
2. les canaux, outils ou plugins de fonctionnalités devraient la consommer sans se soucier du fournisseur
3. le cœur doit posséder le comportement de secours, la politique, la configuration ou la livraison

Si le travail est spécifique au fournisseur et qu'aucun contrat partagé n'existe encore, arrêtez-vous et définissez d'abord le contrat.

## La séquence standard

1. Définissez le contrat de base typé.
2. Ajoutez l'enregistrement du plugin pour ce contrat.
3. Ajoutez un helper de runtime partagé.
4. Connectez un vrai plugin fournisseur comme preuve.
5. Déplacez les consommateurs de fonctionnalités/canaux sur le helper de runtime.
6. Ajoutez des tests de contrat.
7. Documentez le modèle de configuration et de propriété orienté opérateur.

## Où va quoi

Cœur :

- types de requête/réponse
- registre de fournisseur + résolution
- comportement de secours
- schéma de configuration et étiquettes/aide
- surface du helper de runtime

Plugin fournisseur :

- appels API du fournisseur
- gestion de l'authentification du fournisseur
- normalisation des requêtes spécifiques au fournisseur
- enregistrement de l'implémentation de la capacité

Plugin de fonctionnalité/canal :

- appelle `api.runtime.*` ou le helper `plugin-sdk/*-runtime` correspondant
- n'appelle jamais directement une implémentation de fournisseur

## Liste de contrôle des fichiers

Pour une nouvelle capacité, attendez-vous à toucher ces zones :

- `src/<capability>/types.ts`
- `src/<capability>/...registry/runtime.ts`
- `src/plugins/types.ts`
- `src/plugins/registry.ts`
- `src/plugins/captured-registration.ts`
- `src/plugins/contracts/registry.ts`
- `src/plugins/runtime/types-core.ts`
- `src/plugins/runtime/index.ts`
- `src/plugin-sdk/<capability>.ts`
- `src/plugin-sdk/<capability>-runtime.ts`
- une ou plusieurs `extensions/<vendor>/...`
- configuration/docs/tests

## Exemple : génération d'images

La génération d'images suit la forme standard :

1. le cœur définit `ImageGenerationProvider`
2. le cœur expose `registerImageGenerationProvider(...)`
3. le cœur expose `runtime.imageGeneration.generate(...)`
4. le plugin `openai` enregistre une implémentation soutenue par OpenAI
5. les futurs fournisseurs peuvent enregistrer le même contrat sans modifier les canaux/outils

La clé de configuration est séparée du routage d'analyse de vision :

- `agents.defaults.imageModel` = analyser les images
- `agents.defaults.imageGenerationModel` = générer les images

Gardez-les séparés pour que le secours et la politique restent explicites.

## Liste de contrôle de révision

Avant de livrer une nouvelle capacité, vérifiez :

- aucun canal/outil n'importe directement le code du fournisseur
- le helper de runtime est le chemin partagé
- au moins un test de contrat affirme la propriété groupée
- la documentation de configuration nomme la nouvelle clé de modèle/configuration
- la documentation du plugin explique la limite de propriété

Si une PR saute la couche de capacité et code en dur le comportement du fournisseur dans un canal/outil, renvoyez-la et définissez d'abord le contrat.
