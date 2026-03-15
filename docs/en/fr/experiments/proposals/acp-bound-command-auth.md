---
summary: "Proposition : modèle d'autorisation de commande à long terme pour les conversations liées à ACP"
read_when:
  - Designing native command auth behavior in Telegram/Discord ACP-bound channels/topics
title: "Autorisation de commande liée à ACP (Proposition)"
---

# Autorisation de commande liée à ACP (Proposition)

Statut : Proposé, **pas encore implémenté**.

Ce document décrit un modèle d'autorisation à long terme pour les commandes natives dans les conversations liées à ACP. Il s'agit d'une proposition d'expérience et ne remplace pas le comportement actuel en production.

Pour le comportement implémenté, consultez le code source et les tests dans :

- `src/telegram/bot-native-commands.ts`
- `src/discord/monitor/native-command.ts`
- `src/auto-reply/reply/commands-core.ts`

## Problème

Aujourd'hui, nous avons des vérifications spécifiques aux commandes (par exemple `/new` et `/reset`) qui doivent fonctionner dans les canaux/sujets liés à ACP même lorsque les listes blanches sont vides. Cela résout la douleur UX immédiate, mais les exceptions basées sur le nom de la commande ne s'adaptent pas bien.

## Forme à long terme

Déplacer l'autorisation des commandes de la logique du gestionnaire ad-hoc vers les métadonnées de commande plus un évaluateur de politique partagé.

### 1) Ajouter les métadonnées de politique d'authentification aux définitions de commande

Chaque définition de commande doit déclarer une politique d'authentification. Exemple de forme :

```ts
type CommandAuthPolicy =
  | { mode: "owner_or_allowlist" } // default, current strict behavior
  | { mode: "bound_acp_or_owner_or_allowlist" } // allow in explicitly bound ACP conversations
  | { mode: "owner_only" };
```

`/new` et `/reset` utiliseraient `bound_acp_or_owner_or_allowlist`.
La plupart des autres commandes resteraient `owner_or_allowlist`.

### 2) Partager un évaluateur sur tous les canaux

Introduire un assistant qui évalue l'authentification de la commande en utilisant :

- les métadonnées de politique de commande
- l'état d'autorisation de l'expéditeur
- l'état de liaison de conversation résolu

Les gestionnaires natifs Telegram et Discord doivent appeler le même assistant pour éviter la dérive de comportement.

### 3) Utiliser la correspondance de liaison comme limite de contournement

Lorsque la politique permet le contournement ACP lié, autoriser uniquement si une correspondance de liaison configurée a été résolue pour la conversation actuelle (pas seulement parce que la clé de session actuelle ressemble à ACP).

Cela maintient la limite explicite et minimise l'élargissement accidentel.

## Pourquoi c'est mieux

- S'adapte aux commandes futures sans ajouter plus de conditions basées sur le nom de la commande.
- Maintient le comportement cohérent sur les canaux.
- Préserve le modèle de sécurité actuel en exigeant une correspondance de liaison explicite.
- Garde les listes blanches comme renforcement optionnel au lieu d'une exigence universelle.

## Plan de déploiement (futur)

1. Ajouter le champ de politique d'authentification de commande aux types de registre de commande et aux données de commande.
2. Implémenter l'évaluateur partagé et migrer les gestionnaires natifs Telegram + Discord.
3. Déplacer `/new` et `/reset` vers une politique basée sur les métadonnées.
4. Ajouter des tests par mode de politique et surface de canal.

## Non-objectifs

- Cette proposition ne modifie pas le comportement du cycle de vie de la session ACP.
- Cette proposition ne nécessite pas de listes blanches pour toutes les commandes liées à ACP.
- Cette proposition ne modifie pas la sémantique de liaison d'itinéraire existante.

## Remarque

Cette proposition est intentionnellement additive et ne supprime ni ne remplace les documents d'expériences existants.
