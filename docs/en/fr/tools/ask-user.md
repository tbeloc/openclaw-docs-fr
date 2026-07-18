---
summary: "Comment ask_user met en pause un tour d'agent pour une décision humaine structurée"
read_when:
  - Vous voulez qu'un agent pose à l'utilisateur une question structurée
  - Vous répondez ou déboguez une invite ask_user
  - Vous avez besoin du schéma ask_user, du délai d'expiration ou du comportement du canal
title: "Demander à l'utilisateur"
---

`ask_user` permet à l'agent de poser à l'humain une à trois questions structurées et
d'attendre les réponses. C'est pour les décisions qui appartiennent véritablement à l'utilisateur,
et non pour les confirmations de routine ou les informations que l'agent peut dériver de la demande,
du code ou d'une valeur par défaut raisonnable.

L'outil n'est disponible que dans la session principale. Les sous-agents et autres
exécutions non primaires ne le reçoivent pas.

## Répondre à une question

Vous pouvez répondre à partir de n'importe quelle surface de conversation prise en charge :

- L'interface utilisateur Control du web affiche une carte de question unifiée.
- Telegram, Discord et Slack affichent des boutons natifs pour une invite à choix unique
  et question unique.
- Une réponse en texte brut fonctionne sur n'importe quel canal. Répondez avec un numéro, une étiquette d'option,
  ou votre propre réponse.

OpenClaw active toujours une réponse **Autre** en texte libre. L'agent ne doit pas ajouter une
option `Autre` à la liste d'options créée.

Les invites qui ne peuvent pas utiliser de boutons natifs, y compris les invites multi-questions et
multi-sélection, se dégradent en texte lisible. L'interface utilisateur Control conserve la carte
structurée complète.

## Délai d'expiration et pas de réponse

Le délai d'expiration par défaut est de 900 secondes. `timeoutSeconds` est limité à la plage
30 à 3600 secondes.

Si la question expire ou est annulée avant l'arrivée d'une réponse, l'outil
retourne `status: "no_answer"`. L'agent continue alors avec son meilleur jugement.
Une exécution d'agent abandonnée annule sa question Gateway en attente.

## Schéma de l'outil

```ts
{
  questions: Array<{
    id: string; // clé de réponse unique en snake_case
    header: string; // étiquette courte ; tronquée à 12 caractères
    question: string; // une phrase
    options: Array<{
      label: string;
      description?: string;
    }>; // 2-4 options
    multiSelect?: boolean;
  }>; // 1-3 questions
  timeoutSeconds?: number; // entier ; par défaut 900, limité à 30-3600
}
```

Avec `multiSelect: true`, l'utilisateur peut choisir plusieurs options. Les valeurs de réponse
sont retournées sous forme de tableau pour chaque question.

Exemple de résultat répondu :

```json
{
  "status": "answered",
  "answers": {
    "answers": {
      "deploy_target": {
        "answers": ["Staging (Recommended)"]
      }
    }
  }
}
```

## Orientation du modèle

Le contrat face au modèle indique à l'agent de :

- poser des questions uniquement lorsqu'il est bloqué sur une décision véritablement détenue par l'utilisateur ;
- préférer une question et ne pas en utiliser plus de trois ;
- mettre l'option recommandée en premier et suffixer son étiquette avec `(Recommended)` ;
- omettre une option `Autre` créée car le texte libre est ajouté automatiquement ;
- continuer avec le meilleur jugement après `no_answer`.

L'agent ne doit pas utiliser `ask_user` pour demander s'il peut procéder ou pour confirmer
son propre plan.
