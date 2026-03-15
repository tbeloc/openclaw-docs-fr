---
summary: "Plan: isoler browser act:evaluate de la file d'attente Playwright en utilisant CDP, avec des délais de bout en bout et une résolution de référence plus sûre"
read_when:
  - Travail sur les problèmes de timeout, d'abandon ou de blocage de file d'attente de `act:evaluate`
  - Planification de l'isolation basée sur CDP pour l'exécution d'evaluate
owner: "openclaw"
status: "draft"
last_updated: "2026-02-10"
title: "Plan de refactorisation CDP pour Browser Evaluate"
---

# Plan de refactorisation CDP pour Browser Evaluate

## Contexte

`act:evaluate` exécute du JavaScript fourni par l'utilisateur dans la page. Actuellement, il s'exécute via Playwright
(`page.evaluate` ou `locator.evaluate`). Playwright sérialise les commandes CDP par page, donc une
évaluation bloquée ou longue peut bloquer la file d'attente des commandes de la page et rendre chaque action ultérieure
sur cet onglet "bloquée".

La PR #13498 ajoute un filet de sécurité pragmatique (évaluation bornée, propagation d'abandon et récupération
au mieux). Ce document décrit un refactorisation plus large qui rend `act:evaluate` intrinsèquement
isolé de Playwright afin qu'une évaluation bloquée ne puisse pas coincer les opérations Playwright normales.

## Objectifs

- `act:evaluate` ne peut pas bloquer définitivement les actions de navigateur ultérieures sur le même onglet.
- Les délais d'expiration sont une source unique de vérité de bout en bout afin qu'un appelant puisse compter sur un budget.
- L'abandon et le délai d'expiration sont traités de la même manière dans la distribution HTTP et en processus.
- Le ciblage d'éléments pour evaluate est pris en charge sans tout basculer de Playwright.
- Maintenir la compatibilité rétroactive pour les appelants et les charges utiles existants.

## Non-objectifs

- Remplacer toutes les actions de navigateur (clic, saisie, attente, etc.) par des implémentations CDP.
- Supprimer le filet de sécurité existant introduit dans la PR #13498 (il reste un repli utile).
- Introduire de nouvelles capacités non sûres au-delà de la porte `browser.evaluateEnabled` existante.
- Ajouter l'isolation de processus (processus worker/thread) pour evaluate. Si nous voyons toujours des états
  bloqués difficiles à récupérer après ce refactorisation, c'est une idée de suivi.

## Architecture actuelle (Pourquoi elle se bloque)

À haut niveau :

- Les appelants envoient `act:evaluate` au service de contrôle du navigateur.
- Le gestionnaire de route appelle Playwright pour exécuter le JavaScript.
- Playwright sérialise les commandes de page, donc une évaluation qui ne se termine jamais bloque la file d'attente.
- Une file d'attente bloquée signifie que les opérations clic/saisie/attente ultérieures sur l'onglet peuvent sembler se bloquer.

## Architecture proposée

### 1. Propagation des délais

Introduire un concept de budget unique et en dériver tout :

- L'appelant définit `timeoutMs` (ou une deadline dans le futur).
- Le délai d'expiration de la requête externe, la logique du gestionnaire de route et le budget d'exécution à l'intérieur de la page
  utilisent tous le même budget, avec une petite marge de manœuvre si nécessaire pour les frais généraux de sérialisation.
- L'abandon est propagé comme un `AbortSignal` partout afin que l'annulation soit cohérente.

Direction de mise en œuvre :

- Ajouter un petit assistant (par exemple `createBudget({ timeoutMs, signal })`) qui retourne :
  - `signal` : le AbortSignal lié
  - `deadlineAtMs` : deadline absolue
  - `remainingMs()` : budget restant pour les opérations enfants
- Utiliser cet assistant dans :
  - `src/browser/client-fetch.ts` (distribution HTTP et en processus)
  - `src/node-host/runner.ts` (chemin proxy)
  - implémentations d'actions de navigateur (Playwright et CDP)

### 2. Moteur Evaluate séparé (Chemin CDP)

Ajouter une implémentation d'évaluation basée sur CDP qui ne partage pas la file d'attente des commandes par page de Playwright. La propriété clé
est que le transport d'évaluation est une connexion WebSocket séparée et une session CDP séparée attachée à la cible.

Direction de mise en œuvre :

- Nouveau module, par exemple `src/browser/cdp-evaluate.ts`, qui :
  - Se connecte au point de terminaison CDP configuré (socket au niveau du navigateur).
  - Utilise `Target.attachToTarget({ targetId, flatten: true })` pour obtenir un `sessionId`.
  - Exécute soit :
    - `Runtime.evaluate` pour l'évaluation au niveau de la page, soit
    - `DOM.resolveNode` plus `Runtime.callFunctionOn` pour l'évaluation d'élément.
  - En cas de délai d'expiration ou d'abandon :
    - Envoie `Runtime.terminateExecution` au mieux pour la session.
    - Ferme le WebSocket et retourne une erreur claire.

Remarques :

- Cela exécute toujours du JavaScript dans la page, donc la terminaison peut avoir des effets secondaires. Le gain
  est qu'il ne coince pas la file d'attente Playwright, et il est annulable au niveau du transport en tuant la session CDP.

### 3. Récit de référence (Ciblage d'éléments sans réécriture complète)

La partie difficile est le ciblage d'éléments. CDP a besoin d'une poignée DOM ou d'un `backendDOMNodeId`, tandis que
aujourd'hui la plupart des actions de navigateur utilisent des localisateurs Playwright basés sur des références de snapshots.

Approche recommandée : conserver les références existantes, mais joindre un id CDP résolvable optionnel.

#### 3.1 Étendre les informations de référence stockées

Étendre les métadonnées de référence de rôle stockées pour inclure optionnellement un id CDP :

- Aujourd'hui : `{ role, name, nth }`
- Proposé : `{ role, name, nth, backendDOMNodeId?: number }`

Cela garde toutes les actions basées sur Playwright existantes fonctionnelles et permet à l'évaluation CDP d'accepter
la même valeur `ref` quand le `backendDOMNodeId` est disponible.

#### 3.2 Remplir backendDOMNodeId au moment du snapshot

Lors de la production d'un snapshot de rôle :

1. Générer la carte de référence de rôle existante comme aujourd'hui (rôle, nom, nth).
2. Récupérer l'arborescence AX via CDP (`Accessibility.getFullAXTree`) et calculer une carte parallèle de
   `(role, name, nth) -> backendDOMNodeId` en utilisant les mêmes règles de gestion des doublons.
3. Fusionner l'id dans les informations de référence stockées pour l'onglet actuel.

Si le mappage échoue pour une référence, laisser `backendDOMNodeId` indéfini. Cela rend la fonctionnalité
au mieux et sûre à déployer.

#### 3.3 Comportement d'Evaluate avec Ref

Dans `act:evaluate` :

- Si `ref` est présent et a `backendDOMNodeId`, exécuter l'évaluation d'élément via CDP.
- Si `ref` est présent mais n'a pas `backendDOMNodeId`, revenir au chemin Playwright (avec
  le filet de sécurité).

Échappatoire optionnel :

- Étendre la forme de la requête pour accepter `backendDOMNodeId` directement pour les appelants avancés (et
  pour le débogage), tout en gardant `ref` comme interface principale.

### 4. Garder un chemin de récupération en dernier recours

Même avec l'évaluation CDP, il y a d'autres façons de coincer un onglet ou une connexion. Garder les
mécanismes de récupération existants (terminer l'exécution + déconnecter Playwright) comme dernier recours pour :

- les appelants hérités
- les environnements où l'attachement CDP est bloqué
- les cas limites Playwright inattendus

## Plan de mise en œuvre (Itération unique)

### Livrables

- Un moteur d'évaluation CDP qui s'exécute en dehors de la file d'attente des commandes par page de Playwright.
- Un budget de timeout/abandon de bout en bout unique utilisé de manière cohérente par les appelants et les gestionnaires.
- Métadonnées de référence qui peuvent optionnellement porter `backendDOMNodeId` pour l'évaluation d'élément.
- `act:evaluate` préfère le moteur CDP quand possible et revient à Playwright quand ce n'est pas le cas.
- Tests qui prouvent qu'une évaluation bloquée ne coince pas les actions ultérieures.
- Journaux/métriques qui rendent les défaillances et les replis visibles.

### Liste de contrôle de mise en œuvre

1. Ajouter un assistant "budget" partagé pour lier `timeoutMs` + `AbortSignal` en amont dans :
   - un `AbortSignal` unique
   - une deadline absolue
   - un assistant `remainingMs()` pour les opérations en aval
2. Mettre à jour tous les chemins d'appelant pour utiliser cet assistant afin que `timeoutMs` signifie la même chose partout :
   - `src/browser/client-fetch.ts` (distribution HTTP et en processus)
   - `src/node-host/runner.ts` (chemin proxy de nœud)
   - Wrappers CLI qui appellent `/act` (ajouter `--timeout-ms` à `browser evaluate`)
3. Implémenter `src/browser/cdp-evaluate.ts` :
   - se connecter au socket CDP au niveau du navigateur
   - `Target.attachToTarget` pour obtenir un `sessionId`
   - exécuter `Runtime.evaluate` pour l'évaluation de page
   - exécuter `DOM.resolveNode` + `Runtime.callFunctionOn` pour l'évaluation d'élément
   - en cas de timeout/abandon : au mieux `Runtime.terminateExecution` puis fermer le socket
4. Étendre les métadonnées de référence de rôle stockées pour inclure optionnellement `backendDOMNodeId` :
   - garder le comportement `{ role, name, nth }` existant pour les actions Playwright
   - ajouter `backendDOMNodeId?: number` pour le ciblage d'élément CDP
5. Remplir `backendDOMNodeId` lors de la création du snapshot (au mieux) :
   - récupérer l'arborescence AX via CDP (`Accessibility.getFullAXTree`)
   - calculer `(role, name, nth) -> backendDOMNodeId` et fusionner dans la carte de référence stockée
   - si le mappage est ambigu ou manquant, laisser l'id indéfini
6. Mettre à jour le routage `act:evaluate` :
   - si pas de `ref` : toujours utiliser l'évaluation CDP
   - si `ref` se résout en `backendDOMNodeId` : utiliser l'évaluation d'élément CDP
   - sinon : revenir à l'évaluation Playwright (toujours bornée et annulable)
7. Garder le chemin de récupération "en dernier recours" existant comme repli, pas le chemin par défaut.
8. Ajouter des tests :
   - l'évaluation bloquée intentionnelle expire dans le budget et le clic/saisie suivant réussit
   - l'abandon annule l'évaluation (déconnexion du client ou timeout) et déverrouille les actions ultérieures
   - les défaillances de mappage reviennent proprement à Playwright
9. Ajouter l'observabilité :
   - durée d'évaluation et compteurs de timeout
   - utilisation de terminateExecution
   - taux de repli (CDP -> Playwright) et raisons

### Critères d'acceptation

- Une `act:evaluate` intentionnellement suspendue retourne dans le budget de l'appelant et ne coince pas l'onglet
  pour les actions ultérieures.
- `timeoutMs` se comporte de manière cohérente dans les appels CLI, outil d'agent, proxy de nœud et en processus.
- Si `ref` peut être mappé à `backendDOMNodeId`, l'évaluation d'élément utilise CDP ; sinon le
  chemin de repli est toujours borné et récupérable.

## Plan de test

- Tests unitaires :
  - logique de correspondance `(role, name, nth)` entre les références de rôle et les nœuds d'arborescence AX.
  - comportement de l'assistant budget (marge de manœuvre, mathématiques du temps restant).
- Tests d'intégration :
  - le timeout d'évaluation CDP retourne dans le budget et ne bloque pas l'action suivante.
  - l'abandon annule l'évaluation et déclenche la terminaison au mieux.
- Tests de contrat :
  - Assurer que `BrowserActRequest` et `BrowserActResponse` restent compatibles.

## Risques et atténuations

- Le mappage est imparfait :
  - Atténuation : mappage au mieux, repli à l'évaluation Playwright et ajout d'outils de débogage.
- `Runtime.terminateExecution` a des effets secondaires :
  - Atténuation : utiliser uniquement en cas de timeout/abandon et documenter le comportement dans les erreurs.
- Surcharge supplémentaire :
  - Atténuation : récupérer l'arborescence AX uniquement quand les snapshots sont demandés, mettre en cache par cible et garder
    la session CDP de courte durée.
- Limitations du relais d'extension :
  - Atténuation : utiliser les API d'attachement au niveau du navigateur quand les sockets par page ne sont pas disponibles et
    garder le chemin Playwright actuel comme repli.

## Questions ouvertes

- Le nouveau moteur doit-il être configurable comme `playwright`, `cdp` ou `auto` ?
- Voulons-nous exposer un nouveau format "nodeRef" pour les utilisateurs avancés, ou garder `ref` uniquement ?
- Comment les snapshots de cadre et les snapshots délimités par sélecteur doivent-ils participer au mappage AX ?
