---
summary: "Guide de contribution pour ajouter une nouvelle capacité partagée au système de plugins OpenClaw"
read_when:
  - Adding a new core capability and plugin registration surface
  - Deciding whether code belongs in core, a vendor plugin, or a feature plugin
  - Wiring a new runtime helper for channels or tools
title: "Ajouter des capacités (guide de contribution)"
sidebarTitle: "Ajouter des capacités"
---

<Info>
  Ceci est un **guide de contribution** pour les développeurs du noyau OpenClaw. Si vous
  construisez un plugin externe, consultez plutôt [Construire des plugins](/fr/plugins/building-plugins). Pour la référence d'architecture approfondie (modèle de capacité, propriété,
  pipeline de chargement, assistants d'exécution), consultez [Internals des plugins](/fr/plugins/architecture).
</Info>

Utilisez ceci quand OpenClaw a besoin d'un nouveau domaine partagé tel que la génération d'images, la génération de vidéos, ou un futur domaine de fonctionnalités soutenu par un fournisseur.

La règle :

- **plugin** = limite de propriété
- **capacité** = contrat de noyau partagé

Ne commencez pas en connectant directement un fournisseur à un canal ou un outil. Commencez par définir la capacité.

## Quand créer une capacité

Créez une nouvelle capacité quand **tous** ces éléments sont vrais :

1. Plus d'un fournisseur pourrait plausiblement l'implémenter.
2. Les canaux, outils ou plugins de fonctionnalités devraient la consommer sans se soucier du fournisseur.
3. Le noyau doit posséder le comportement de secours, la politique, la configuration ou la livraison.

Si le travail est spécifique au fournisseur et qu'aucun contrat partagé n'existe encore, arrêtez-vous et définissez d'abord le contrat.

## La séquence standard

1. Définissez le contrat de noyau typé.
2. Ajoutez l'enregistrement du plugin pour ce contrat.
3. Ajoutez un assistant d'exécution partagé.
4. Connectez un vrai plugin de fournisseur comme preuve.
5. Déplacez les consommateurs de fonctionnalités/canaux sur l'assistant d'exécution.
6. Ajoutez des tests de contrat.
7. Documentez le modèle de configuration et de propriété face à l'opérateur.

## Où va quoi

**Noyau :**

- Types de requête/réponse.
- Registre de fournisseur + résolution.
- Comportement de secours.
- Schéma de configuration avec métadonnées de documentation `title` / `description` propagées sur les nœuds d'objet imbriqué, de caractère générique, d'élément de tableau et de composition.
- Surface d'assistant d'exécution.

**Plugin de fournisseur :**

- Appels d'API du fournisseur.
- Gestion de l'authentification du fournisseur.
- Normalisation des requêtes spécifiques au fournisseur.
- Enregistrement de l'implémentation de la capacité.

**Plugin de fonctionnalité/canal :**

- Appelle `api.runtime.*` ou l'assistant correspondant `plugin-sdk/*-runtime`.
- N'appelle jamais directement une implémentation de fournisseur.

## Coutures de fournisseur et de harnais

Utilisez les **crochets de fournisseur** quand le comportement appartient au contrat de fournisseur de modèle plutôt qu'à la boucle d'agent générique. Les exemples incluent les paramètres de requête spécifiques au fournisseur après la sélection du transport, la préférence de profil d'authentification, les superpositions d'invite et le routage de secours de suivi après le basculement du modèle/profil.

Utilisez les **crochets de harnais d'agent** quand le comportement appartient à l'exécution qui exécute un tour. Les harnais peuvent classer les résultats de tentative réussis mais inutilisables tels que les réponses vides, réservées au raisonnement ou réservées à la planification afin que la politique de secours du modèle externe puisse prendre la décision de réessai.

Gardez les deux coutures étroites :

- Le noyau possède la politique de réessai/secours.
- Les plugins de fournisseur possèdent les indices de requête/authentification/routage spécifiques au fournisseur.
- Les plugins de harnais possèdent la classification de tentative spécifique à l'exécution.
- Les plugins tiers retournent des indices, pas des mutations directes de l'état du noyau.

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
- Un ou plusieurs packages de plugins groupés.
- Configuration, documentation, tests.

## Exemple travaillé : génération d'images

La génération d'images suit la forme standard :

1. Le noyau définit `ImageGenerationProvider`.
2. Le noyau expose `registerImageGenerationProvider(...)`.
3. Le noyau expose `runtime.imageGeneration.generate(...)`.
4. Les plugins `openai`, `google`, `fal` et `minimax` enregistrent les implémentations soutenues par le fournisseur.
5. Les futurs fournisseurs enregistrent le même contrat sans modifier les canaux/outils.

La clé de configuration est intentionnellement séparée du routage d'analyse de vision :

- `agents.defaults.imageModel` analyse les images.
- `agents.defaults.imageGenerationModel` génère les images.

Gardez-les séparés afin que le secours et la politique restent explicites.

## Liste de contrôle d'examen

Avant de livrer une nouvelle capacité, vérifiez :

- Aucun canal/outil n'importe directement le code du fournisseur.
- L'assistant d'exécution est le chemin partagé.
- Au moins un test de contrat affirme la propriété groupée.
- Les documents de configuration nomment la nouvelle clé de modèle/configuration.
- Les documents de plugin expliquent la limite de propriété.

Si une PR ignore la couche de capacité et code en dur le comportement du fournisseur dans un canal/outil, renvoyez-la et définissez d'abord le contrat.

## Connexes

- [Internals des plugins](/fr/plugins/architecture) — modèle de capacité, propriété, pipeline de chargement, assistants d'exécution.
- [Construire des plugins](/fr/plugins/building-plugins) — tutoriel du premier plugin.
- [Aperçu du SDK](/fr/plugins/sdk-overview) — carte d'importation et référence de l'API d'enregistrement.
- [Créer des compétences](/fr/tools/creating-skills) — surface de contribution compagnon.
