---
summary: "Plan complet de modernisation d'application avec mises à jour des compétences en livraison frontend"
title: "Plan de modernisation d'application"
read_when:
  - Planning a broad OpenClaw application modernization pass
  - Updating frontend implementation standards for app or Control UI work
  - Turning a broad product quality review into phased engineering work
---

# Plan de modernisation d'application

## Objectif

Orienter l'application vers un produit plus propre, plus rapide et plus maintenable sans
casser les flux de travail actuels ni masquer les risques dans les refactorisations larges. Le travail doit
être livré en petites tranches examinables avec preuve pour chaque surface touchée.

## Principes

- Préserver l'architecture actuelle sauf si une limite cause démontrablement du churn,
  un coût de performance ou des bugs visibles pour l'utilisateur.
- Préférer le plus petit correctif correct pour chaque problème, puis répéter.
- Séparer les correctifs requis du polissage optionnel afin que les mainteneurs puissent livrer du travail de
  haute valeur sans attendre les décisions subjectives.
- Garder le comportement orienté plugin documenté et rétrocompatible.
- Vérifier le comportement livré, les contrats de dépendance et les tests avant de prétendre qu'une
  régression est corrigée.
- Améliorer d'abord le chemin utilisateur principal : onboarding, authentification, chat, configuration du fournisseur,
  gestion des plugins et diagnostics.

## Phase 1 : Audit de base

Inventorier l'application actuelle avant de la modifier.

- Identifier les principaux flux de travail utilisateur et les surfaces de code qui les possèdent.
- Lister les affordances mortes, les paramètres dupliqués, les états d'erreur peu clairs et les chemins de rendu coûteux.
- Capturer les commandes de validation actuelles pour chaque surface.
- Marquer les problèmes comme requis, recommandés ou optionnels.
- Documenter les blocages connus qui nécessitent un examen du propriétaire, en particulier les modifications d'API, de sécurité,
  de version et de contrat de plugin.

Définition de la fin :

- Une liste de problèmes avec références de fichiers à la racine du repo.
- Chaque problème a une sévérité, une surface propriétaire, un impact utilisateur attendu et un chemin de validation proposé.
- Aucun élément de nettoyage spéculatif n'est mélangé aux correctifs requis.

## Phase 2 : Nettoyage du produit et de l'UX

Prioriser les flux de travail visibles et supprimer la confusion.

- Resserrer la copie d'onboarding et les états vides autour de l'authentification du modèle, du statut de la passerelle
  et de la configuration des plugins.
- Supprimer ou désactiver les affordances mortes où aucune action n'est possible.
- Garder les actions importantes visibles sur les largeurs réactives au lieu de les masquer
  derrière des hypothèses de mise en page fragiles.
- Consolider le langage de statut répété afin que les erreurs aient une source unique de vérité.
- Ajouter une divulgation progressive pour les paramètres avancés tout en gardant la configuration de base rapide.

Validation recommandée :

- Chemin heureux manuel pour la configuration de première exécution et le démarrage de l'utilisateur existant.
- Tests ciblés pour toute logique de routage, de persistance de configuration ou de dérivation de statut.
- Captures d'écran du navigateur pour les surfaces réactives modifiées.

## Phase 3 : Resserrement de l'architecture frontend

Améliorer la maintenabilité sans une réécriture large.

- Déplacer les transformations d'état d'interface utilisateur répétées dans des assistants typés étroits.
- Garder les responsabilités de récupération de données, de persistance et de présentation séparées.
- Préférer les hooks, stores et modèles de composants existants aux nouvelles abstractions.
- Diviser les composants surdimensionnés uniquement lorsque cela réduit le couplage ou clarifie les tests.
- Éviter d'introduire un état global large pour les interactions de panneau local.

Garde-fous requis :

- Ne pas modifier le comportement public comme effet secondaire du fractionnement de fichiers.
- Garder le comportement d'accessibilité intact pour les menus, les dialogues, les onglets et la
  navigation au clavier.
- Vérifier que les états de chargement, vide, erreur et optimiste s'affichent toujours.

## Phase 4 : Performance et fiabilité

Cibler la douleur mesurée plutôt que l'optimisation théorique large.

- Mesurer les coûts de démarrage, de transition de route, de grande liste et de transcription de chat.
- Remplacer les données dérivées coûteuses répétées par des sélecteurs mémoïsés ou des assistants en cache
  où le profilage prouve la valeur.
- Réduire les analyses réseau ou système de fichiers évitables sur les chemins chauds.
- Garder un ordre déterministe pour les entrées de prompt, de registre, de fichier, de plugin et de réseau
  avant la construction de la charge utile du modèle.
- Ajouter des tests de régression légers pour les assistants chauds et les limites de contrat.

Définition de la fin :

- Chaque changement de performance enregistre la ligne de base, l'impact attendu, l'impact réel et
  l'écart restant.
- Aucun correctif de perf n'est livré uniquement sur l'intuition quand une mesure bon marché est disponible.

## Phase 5 : Durcissement du type, du contrat et du test

Augmenter la correction aux points limites sur lesquels les utilisateurs et les auteurs de plugins dépendent.

- Remplacer les chaînes d'exécution lâches par des unions discriminées ou des listes de code fermées.
- Valider les entrées externes avec les assistants de schéma existants ou zod.
- Ajouter des tests de contrat autour des manifestes de plugin, des catalogues de fournisseurs, des messages de protocole de passerelle
  et du comportement de migration de configuration.
- Garder les chemins de compatibilité dans les flux de docteur ou de réparation au lieu des migrations
  cachées au moment du démarrage.
- Éviter le couplage spécifique aux tests aux internes des plugins ; utiliser les façades SDK et les
  barils documentés.

Validation recommandée :

- `pnpm check:changed`
- Tests ciblés pour chaque limite modifiée.
- `pnpm build` quand les limites paresseuses, l'empaquetage ou les surfaces publiées changent.

## Phase 6 : Documentation et préparation à la version

Garder la documentation orientée utilisateur alignée avec le comportement.

- Mettre à jour les docs avec les changements de comportement, d'API, de configuration, d'onboarding ou de plugin.
- Ajouter des entrées de changelog uniquement pour les changements visibles pour l'utilisateur.
- Garder la terminologie des plugins orientée utilisateur ; utiliser les noms de packages internes uniquement où
  nécessaire pour les contributeurs.
- Confirmer que les instructions de version et d'installation correspondent toujours à la surface de commande actuelle.

Définition de la fin :

- Les docs pertinents sont mis à jour dans la même branche que les changements de comportement.
- Les docs générés ou les vérifications de dérive d'API passent quand touchés.
- La transmission nomme toute validation ignorée et pourquoi elle a été ignorée.

## Première tranche recommandée

Commencer par une passe Control UI et onboarding ciblée :

- Auditer la configuration de première exécution, la disponibilité de l'authentification du fournisseur, le statut de la passerelle et les surfaces de configuration des plugins.
- Supprimer les actions mortes et clarifier les états d'échec.
- Ajouter ou mettre à jour les tests ciblés pour la dérivation de statut et la persistance de configuration.
- Exécuter `pnpm check:changed`.

Cela donne une haute valeur utilisateur avec un risque d'architecture limité.

## Mise à jour des compétences frontend

Utilisez cette section pour mettre à jour le `SKILL.md` orienté frontend fourni avec la
tâche de modernisation. Si vous adoptez ce guide comme compétence OpenClaw locale du repo,
créez d'abord `.agents/skills/openclaw-frontend/SKILL.md`, gardez le frontmatter
qui appartient à cette compétence cible, puis ajoutez ou remplacez le guide du corps avec
le contenu suivant.

```markdown
# Normes de livraison frontend

Utilisez cette compétence lors de l'implémentation ou de l'examen du travail d'interface utilisateur React, Next.js,
webview de bureau ou d'application orienté utilisateur.

## Règles de fonctionnement

- Commencer par le flux de travail du produit existant et les conventions de code.
- Préférer le plus petit correctif correct qui améliore le chemin utilisateur actuel.
- Séparer les correctifs requis du polissage optionnel dans la transmission.
- Ne pas construire de pages marketing quand la demande concerne une surface d'application.
- Garder les actions visibles et utilisables sur les tailles de viewport supportées.
- Supprimer les affordances mortes au lieu de laisser des contrôles qui ne peuvent pas agir.
- Préserver les états de chargement, vide, erreur, succès et permission.
- Utiliser les composants de système de conception existants, les hooks, les stores et les icônes avant d'ajouter
  de nouvelles primitives.

## Liste de contrôle d'implémentation

1. Identifier la tâche utilisateur principale et le composant ou la route qui la possède.
2. Lire les modèles de composants locaux avant d'éditer.
3. Corriger la surface la plus étroite qui résout le problème.
4. Ajouter des contraintes réactives pour les contrôles de format fixe, les barres d'outils, les grilles et les
   compteurs afin que le texte et les états de survol ne puissent pas redimensionner la mise en page de manière inattendue.
5. Garder les responsabilités de chargement de données, de dérivation d'état et de rendu claires.
6. Ajouter des tests quand la logique, la persistance, le routage, les permissions ou les assistants partagés
   changent.
7. Vérifier le chemin heureux principal et le cas limite le plus pertinent.

## Portes de qualité visuelle

- Le texte doit tenir dans son conteneur sur mobile et bureau.
- Les barres d'outils peuvent s'enrouler, mais les contrôles doivent rester accessibles.
- Les boutons doivent utiliser des icônes familières quand l'icône est plus claire que le texte.
- Les cartes doivent être utilisées pour les éléments répétés, les modales et les outils encadrés, pas pour
  chaque section de page.
- Éviter les palettes de couleurs monotones et les arrière-plans décoratifs qui rivalisent avec
  le contenu opérationnel.
- Les surfaces de produit denses doivent optimiser pour l'analyse, la comparaison et l'utilisation
  répétée.

## Format de transmission

Rapporter :

- Ce qui a changé.
- Quel comportement utilisateur a changé.
- Validation requise qui a réussi.
- Toute validation ignorée et la raison concrète.
- Travail de suivi optionnel, clairement séparé des correctifs requis.
```
