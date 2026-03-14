---
summary: "Statut et prochaines étapes pour découpler les écouteurs de passerelle Discord des tours d'agent longue durée avec un worker entrant spécifique à Discord"
owner: "openclaw"
status: "in_progress"
last_updated: "2026-03-05"
title: "Plan Discord Async Inbound Worker"
---

# Plan Discord Async Inbound Worker

## Objectif

Éliminer le délai d'expiration de l'écouteur Discord en tant que mode de défaillance visible par l'utilisateur en rendant les tours Discord entrants asynchrones :

1. L'écouteur de passerelle accepte et normalise rapidement les événements entrants.
2. Une file d'attente d'exécution Discord stocke les tâches sérialisées avec des clés basées sur la même limite de classement que nous utilisons aujourd'hui.
3. Un worker exécute le tour d'agent réel en dehors de la durée de vie de l'écouteur Carbon.
4. Les réponses sont livrées au canal ou au fil d'origine après la fin de l'exécution.

C'est la correction à long terme pour les exécutions Discord en file d'attente qui expirent à `channels.discord.eventQueue.listenerTimeout` alors que l'exécution de l'agent elle-même progresse toujours.

## Statut actuel

Ce plan est partiellement implémenté.

Déjà fait :

- Le délai d'expiration de l'écouteur Discord et le délai d'expiration de l'exécution Discord sont maintenant des paramètres distincts.
- Les tours Discord entrants acceptés sont mis en file d'attente dans `src/discord/monitor/inbound-worker.ts`.
- Le worker possède maintenant le tour longue durée au lieu de l'écouteur Carbon.
- Le classement existant par route est préservé par clé de file d'attente.
- La couverture de régression de délai d'expiration existe pour le chemin du worker Discord.

Ce que cela signifie en langage clair :

- le bogue de délai d'expiration en production est corrigé
- le tour longue durée ne meurt plus simplement parce que le budget de l'écouteur Discord expire
- l'architecture du worker n'est pas encore terminée

Ce qui manque encore :

- `DiscordInboundJob` est toujours seulement partiellement normalisé et porte toujours des références d'exécution en direct
- la sémantique des commandes (`stop`, `new`, `reset`, futurs contrôles de session) ne sont pas encore entièrement natives du worker
- l'observabilité du worker et le statut de l'opérateur sont toujours minimaux
- il n'y a toujours pas de durabilité de redémarrage

## Pourquoi cela existe

Le comportement actuel lie le tour d'agent complet à la durée de vie de l'écouteur :

- `src/discord/monitor/listeners.ts` applique la limite de délai d'expiration et la limite d'abandon.
- `src/discord/monitor/message-handler.ts` garde l'exécution en file d'attente à l'intérieur de cette limite.
- `src/discord/monitor/message-handler.process.ts` effectue le chargement des médias, le routage, la distribution, la saisie, la diffusion en continu des brouillons et la livraison de réponse finale en ligne.

Cette architecture a deux mauvaises propriétés :

- les tours longs mais sains peuvent être abandonnés par le chien de garde de l'écouteur
- les utilisateurs peuvent ne voir aucune réponse même si l'exécution en aval en aurait produit une

Augmenter le délai d'expiration aide mais ne change pas le mode de défaillance.

## Non-objectifs

- Ne pas redessiner les canaux non-Discord dans cette passe.
- Ne pas élargir cela en un framework de worker générique pour tous les canaux dans la première implémentation.
- Ne pas extraire une abstraction de worker entrant partagée entre canaux pour l'instant ; partager uniquement les primitives de bas niveau quand la duplication est évidente.
- Ne pas ajouter de récupération de crash durable dans la première passe sauf si nécessaire pour atterrir en toute sécurité.
- Ne pas modifier la sélection de route, la sémantique de liaison ou la politique ACP dans ce plan.

## Contraintes actuelles

Le chemin de traitement Discord actuel dépend toujours de certains objets d'exécution en direct qui ne devraient pas rester dans la charge utile de tâche à long terme :

- Carbon `Client`
- formes d'événement Discord brutes
- carte d'historique de guilde en mémoire
- rappels du gestionnaire de liaison de fil
- état de saisie et de diffusion en continu de brouillon en direct

Nous avons déjà déplacé l'exécution sur une file d'attente de worker, mais la limite de normalisation est toujours incomplète. En ce moment, le worker est « exécuter plus tard dans le même processus avec certains des mêmes objets en direct », pas une limite de tâche entièrement basée sur les données.

## Architecture cible

### 1. Étape d'écouteur

`DiscordMessageListener` reste le point d'entrée, mais son travail devient :

- exécuter les vérifications de préflight et de politique
- normaliser l'entrée acceptée en un `DiscordInboundJob` sérialisable
- mettre en file d'attente la tâche dans une file d'attente asynchrone par session ou par canal
- retourner immédiatement à Carbon une fois que la mise en file d'attente réussit

L'écouteur ne devrait plus posséder la durée de vie du tour LLM de bout en bout.

### 2. Charge utile de tâche normalisée

Introduire un descripteur de tâche sérialisable qui contient uniquement les données nécessaires pour exécuter le tour plus tard.

Forme minimale :

- identité de route
  - `agentId`
  - `sessionKey`
  - `accountId`
  - `channel`
- identité de livraison
  - ID du canal de destination
  - ID du message cible de réponse
  - ID du fil si présent
- identité de l'expéditeur
  - ID de l'expéditeur, étiquette, nom d'utilisateur, tag
- contexte du canal
  - ID de guilde
  - nom ou slug du canal
  - métadonnées du fil
  - invite système résolue si applicable
- corps du message normalisé
  - texte de base
  - texte du message effectif
  - descripteurs de pièces jointes ou références de médias résolues
- décisions de contrôle
  - résultat de l'exigence de mention
  - résultat de l'autorisation de commande
  - métadonnées de session liée ou d'agent si applicable

La charge utile de la tâche ne doit pas contenir d'objets Carbon en direct ou de fermetures mutables.

Statut de l'implémentation actuelle :

- partiellement fait
- `src/discord/monitor/inbound-job.ts` existe et définit la remise du worker
- la charge utile contient toujours le contexte d'exécution Discord en direct et devrait être réduite davantage

### 3. Étape du worker

Ajouter un runner de worker spécifique à Discord responsable de :

- reconstruire le contexte du tour à partir de `DiscordInboundJob`
- charger les médias et toutes métadonnées de canal supplémentaires nécessaires pour l'exécution
- distribuer le tour d'agent
- livrer les charges utiles de réponse finales
- mettre à jour le statut et les diagnostics

Emplacement recommandé :

- `src/discord/monitor/inbound-worker.ts`
- `src/discord/monitor/inbound-job.ts`

### 4. Modèle de classement

Le classement doit rester équivalent à aujourd'hui pour une limite de route donnée.

Clé recommandée :

- utiliser la même logique de clé de file d'attente que `resolveDiscordRunQueueKey(...)`

Cela préserve le comportement existant :

- une conversation d'agent liée ne s'entrelace pas avec elle-même
- différents canaux Discord peuvent toujours progresser indépendamment

### 5. Modèle de délai d'expiration

Après la transition, il y a deux classes de délai d'expiration distinctes :

- délai d'expiration de l'écouteur
  - couvre uniquement la normalisation et la mise en file d'attente
  - devrait être court
- délai d'expiration de l'exécution
  - optionnel, possédé par le worker, explicite et visible par l'utilisateur
  - ne devrait pas être hérité accidentellement des paramètres de l'écouteur Carbon

Cela supprime le couplage accidentel actuel entre « l'écouteur de passerelle Discord est resté actif » et « l'exécution de l'agent est saine ».

## Phases d'implémentation recommandées

### Phase 1 : limite de normalisation

- Statut : partiellement implémenté
- Fait :
  - extrait `buildDiscordInboundJob(...)`
  - ajouté des tests de remise du worker
- Restant :
  - rendre `DiscordInboundJob` données pures uniquement
  - déplacer les dépendances d'exécution en direct vers les services possédés par le worker au lieu de la charge utile par tâche
  - arrêter de reconstruire le contexte de processus en recousant les références d'écouteur en direct dans la tâche

### Phase 2 : file d'attente de worker en mémoire

- Statut : implémenté
- Fait :
  - ajouté `DiscordInboundWorkerQueue` avec clé par clé de file d'attente d'exécution résolue
  - l'écouteur met en file d'attente les tâches au lieu d'attendre directement `processDiscordMessage(...)`
  - le worker exécute les tâches en processus, en mémoire uniquement

C'est la première transition fonctionnelle.

### Phase 3 : division de processus

- Statut : non commencé
- Déplacer la propriété de la livraison, de la saisie et de la diffusion en continu de brouillon derrière des adaptateurs orientés worker.
- Remplacer l'utilisation directe du contexte de préflight en direct par la reconstruction du contexte du worker.
- Garder `processDiscordMessage(...)` temporairement comme façade si nécessaire, puis la diviser.

### Phase 4 : sémantique des commandes

- Statut : non commencé
  Assurez-vous que les commandes Discord natives se comportent toujours correctement quand le travail est en file d'attente :

- `stop`
- `new`
- `reset`
- toutes futures commandes de contrôle de session

La file d'attente du worker doit exposer suffisamment d'état d'exécution pour que les commandes ciblent le tour actif ou en file d'attente.

### Phase 5 : observabilité et UX de l'opérateur

- Statut : non commencé
- émettre la profondeur de la file d'attente et les compteurs de workers actifs dans le statut du moniteur
- enregistrer le temps de mise en file d'attente, le temps de démarrage, le temps de fin et la raison du délai d'expiration ou de l'annulation
- surfacer clairement les défaillances de délai d'expiration ou de livraison possédées par le worker dans les journaux

### Phase 6 : suivi optionnel de durabilité

- Statut : non commencé
  Seulement après que la version en mémoire soit stable :

- décider si les tâches Discord en file d'attente doivent survivre au redémarrage de la passerelle
- si oui, persister les descripteurs de tâche et les points de contrôle de livraison
- si non, documenter la limite explicite en mémoire

Cela devrait être un suivi séparé sauf si la récupération de redémarrage est requise pour atterrir.

## Impact sur les fichiers

Fichiers primaires actuels :

- `src/discord/monitor/listeners.ts`
- `src/discord/monitor/message-handler.ts`
- `src/discord/monitor/message-handler.preflight.ts`
- `src/discord/monitor/message-handler.process.ts`
- `src/discord/monitor/status.ts`

Fichiers de worker actuels :

- `src/discord/monitor/inbound-job.ts`
- `src/discord/monitor/inbound-worker.ts`
- `src/discord/monitor/inbound-job.test.ts`
- `src/discord/monitor/message-handler.queue.test.ts`

Points de contact probables suivants :

- `src/auto-reply/dispatch.ts`
- `src/discord/monitor/reply-delivery.ts`
- `src/discord/monitor/thread-bindings.ts`
- `src/discord/monitor/native-command.ts`

## Prochaine étape maintenant

La prochaine étape est de rendre la limite du worker réelle au lieu de partielle.

Faites ceci ensuite :

1. Déplacer les dépendances d'exécution en direct hors de `DiscordInboundJob`
2. Garder ces dépendances sur l'instance du worker Discord à la place
3. Réduire les tâches en file d'attente à des données pures spécifiques à Discord :
   - identité de route
   - cible de livraison
   - info de l'expéditeur
   - snapshot du message normalisé
   - décisions de contrôle et de liaison
4. Reconstruire le contexte d'exécution du worker à partir de ces données pures à l'intérieur du worker

En pratique, cela signifie :

- `client`
- `threadBindings`
- `guildHistories`
- `discordRestFetch`
- autres poignées mutables d'exécution uniquement

ne devraient plus vivre sur chaque tâche en file d'attente et devraient plutôt vivre sur le worker lui-même ou derrière des adaptateurs possédés par le worker.

Après que cela soit atterri, le suivi suivant devrait être le nettoyage de l'état des commandes pour `stop`, `new` et `reset`.

## Plan de test

Garder la couverture de repro de délai d'expiration existante dans :

- `src/discord/monitor/message-handler.queue.test.ts`

Ajouter de nouveaux tests pour :

1. l'écouteur retourne après la mise en file d'attente sans attendre le tour complet
2. le classement par route est préservé
3. différents canaux s'exécutent toujours en parallèle
4. les réponses sont livrées à la destination du message original
5. `stop` annule l'exécution active possédée par le worker
6. l'échec du worker produit des diagnostics visibles sans bloquer les tâches ultérieures
7. les canaux Discord liés à ACP routent toujours correctement sous l'exécution du worker

## Risques et atténuations

- Risque : la sémantique des commandes s'écarte du comportement synchrone actuel
  Atténuation : atterrir le câblage d'état des commandes dans la même transition, pas plus tard

- Risque : la livraison de réponse perd le contexte de fil ou de réponse à
  Atténuation : rendre l'identité de livraison de première classe dans `DiscordInboundJob`

- Risque : envois en double lors de tentatives ou redémarrages de file d'attente
  Atténuation : garder la première passe en mémoire uniquement, ou ajouter l'idempotence de livraison explicite avant la persistance

- Risque : `message-handler.process.ts` devient plus difficile à raisonner pendant la migration
  Atténuation : diviser en normalisation, exécution et aides de livraison avant ou pendant la transition du worker

## Critères d'acceptation

Le plan est complet quand :

1. Le délai d'expiration de l'écouteur Discord n'abandonne plus les tours longue durée sains.
2. La durée de vie de l'écouteur et la durée de vie du tour d'agent sont des concepts distincts dans le code.
3. Le classement existant par session est préservé.
4. Les canaux Discord liés à ACP fonctionnent via le même chemin du worker.
5. `stop` cible l'exécution possédée par le worker au lieu de l'ancienne pile d'appels possédée par l'écouteur.
6. Les défaillances de délai d'expiration et de livraison deviennent des résultats explicites du worker, pas des abandons silencieux de l'écouteur.

## Stratégie d'atterrissage restante

Terminez ceci dans les PR de suivi :

1. rendre `DiscordInboundJob` données pures uniquement et déplacer les références d'exécution en direct sur le worker
2. nettoyer la propriété de l'état des commandes pour `stop`, `new` et `reset`
3. ajouter l'observabilité du worker et le statut de l'opérateur
4. décider si la durabilité est nécessaire ou documenter explicitement la limite en mémoire

C'est toujours un suivi limité s'il est gardé Discord uniquement et si nous continuons à éviter une abstraction de worker entre canaux prématurée.
