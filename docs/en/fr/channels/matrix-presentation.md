---
summary: "Métadonnées de présentation de message Matrix pour les clients compatibles OpenClaw"
read_when:
  - Building Matrix clients that render OpenClaw rich responses
  - Debugging com.openclaw.presentation event content
title: "Métadonnées de présentation Matrix"
---

OpenClaw peut joindre des métadonnées normalisées `MessagePresentation` aux événements Matrix `m.room.message` sortants sous `com.openclaw.presentation`.

Les clients Matrix standard continuent de rendre le texte brut `body`. Les clients compatibles OpenClaw peuvent lire les métadonnées structurées et rendre l'interface utilisateur native telle que les boutons, les sélecteurs, les lignes de contexte et les séparateurs.

## Contenu de l'événement

Les métadonnées sont stockées dans le contenu de l'événement Matrix :

```json
{
  "msgtype": "m.text",
  "body": "Select model\n\n- DeepSeek: /model deepseek/deepseek-chat",
  "com.openclaw.presentation": {
    "version": 1,
    "type": "message.presentation",
    "title": "Select model",
    "tone": "info",
    "blocks": [
      {
        "type": "select",
        "placeholder": "Choose model",
        "options": [
          {
            "label": "DeepSeek",
            "value": "/model deepseek/deepseek-chat"
          }
        ]
      }
    ]
  }
}
```

`version` est la version du schéma des métadonnées de présentation Matrix. `type` est un discriminateur stable pour les clients compatibles OpenClaw. Les clients doivent ignorer les valeurs `type` inconnues, les versions inconnues qu'ils ne peuvent pas interpréter en toute sécurité et les types de blocs inconnus.

## Comportement de secours

OpenClaw rend toujours un texte brut lisible et de secours dans `body`. Les métadonnées structurées sont additives et ne doivent pas être requises pour l'interopérabilité Matrix de base.

Les clients non pris en charge doivent continuer à afficher le texte de secours. Les clients compatibles OpenClaw peuvent préférer les métadonnées structurées pour l'affichage tout en préservant le texte de secours pour la copie, la recherche, les notifications et l'accessibilité.

## Blocs pris en charge

L'adaptateur sortant Matrix annonce la prise en charge de :

- `buttons`
- `select`
- `context`
- `divider`

Les clients doivent traiter ces blocs comme des indices de présentation au mieux. Les champs inconnus et les types de blocs inconnus doivent être ignorés plutôt que de causer l'échec du rendu du message complet.

## Interactions

Ces métadonnées n'ajoutent pas de sémantique de rappel Matrix. Les valeurs des boutons et des options de sélection sont des charges utiles d'interaction de secours, généralement des commandes slash ou des commandes texte. Un client Matrix qui souhaite prendre en charge l'interaction peut renvoyer la valeur sélectionnée à la salle en tant que message normal.

Par exemple, un bouton avec la valeur `/model deepseek/deepseek-chat` peut être géré en envoyant cette valeur en tant que message texte Matrix chiffré dans la même salle.

## Relation avec les métadonnées d'approbation

`com.openclaw.presentation` est destiné à la présentation générale des messages enrichis.

Les invites d'approbation utilisent les métadonnées dédiées `com.openclaw.approval` car les approbations portent un état sensible à la sécurité, des décisions et des détails exec/plugin. Si les deux clés de métadonnées sont présentes sur le même événement, les clients doivent préférer le rendu d'approbation dédié.

## Messages médias

Lorsqu'une réponse contient plusieurs URL de médias, OpenClaw envoie un événement Matrix par URL de média. Les métadonnées de présentation sont jointes uniquement au premier événement média afin que les clients aient une charge utile structurée stable et que les rendus en double soient évités.

Gardez les métadonnées de présentation compactes. Le texte volumineux visible par l'utilisateur doit rester dans `body` et utiliser le chemin de chunking de texte Matrix normal.
