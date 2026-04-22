---
title: "Présentation des messages"
summary: "Cartes de messages sémantiques, boutons, sélecteurs, texte de secours et indices de livraison pour les plugins de canal"
read_when:
  - Adding or modifying message card, button, or select rendering
  - Building a channel plugin that supports rich outbound messages
  - Changing message tool presentation or delivery capabilities
  - Debugging provider-specific card/block/component rendering regressions
---

# Présentation des messages

La présentation des messages est le contrat partagé d'OpenClaw pour l'interface utilisateur de chat enrichie en sortie.
Elle permet aux agents, commandes CLI, flux d'approbation et plugins de décrire l'intention du message
une seule fois, tandis que chaque plugin de canal rend la meilleure forme native qu'il peut.

Utilisez la présentation pour l'interface utilisateur des messages portables :

- sections de texte
- petit texte de contexte/pied de page
- séparateurs
- boutons
- menus de sélection
- titre et ton de la carte

N'ajoutez pas de nouveaux champs natifs du fournisseur tels que Discord `components`, Slack
`blocks`, Telegram `buttons`, Teams `card`, ou Feishu `card` à l'outil de message partagé. Ceux-ci
sont des sorties de rendu détenues par le plugin de canal.

## Contrat

Les auteurs de plugins importent le contrat public à partir de :

```ts
import type {
  MessagePresentation,
  ReplyPayloadDelivery,
} from "openclaw/plugin-sdk/interactive-runtime";
```

Forme :

```ts
type MessagePresentation = {
  title?: string;
  tone?: "neutral" | "info" | "success" | "warning" | "danger";
  blocks: MessagePresentationBlock[];
};

type MessagePresentationBlock =
  | { type: "text"; text: string }
  | { type: "context"; text: string }
  | { type: "divider" }
  | { type: "buttons"; buttons: MessagePresentationButton[] }
  | { type: "select"; placeholder?: string; options: MessagePresentationOption[] };

type MessagePresentationButton = {
  label: string;
  value?: string;
  url?: string;
  style?: "primary" | "secondary" | "success" | "danger";
};

type MessagePresentationOption = {
  label: string;
  value: string;
};

type ReplyPayloadDelivery = {
  pin?:
    | boolean
    | {
        enabled: boolean;
        notify?: boolean;
        required?: boolean;
      };
};
```

Sémantique des boutons :

- `value` est une valeur d'action d'application acheminée via le chemin d'interaction existant du canal lorsque le canal supporte les contrôles cliquables.
- `url` est un bouton de lien. Il peut exister sans `value`.
- `label` est obligatoire et est également utilisé dans le texte de secours.
- `style` est consultatif. Les rendus doivent mapper les styles non supportés à une valeur par défaut sûre, pas échouer l'envoi.

Sémantique de sélection :

- `options[].value` est la valeur d'application sélectionnée.
- `placeholder` est consultatif et peut être ignoré par les canaux sans support de sélection natif.
- Si un canal ne supporte pas les sélections, le texte de secours liste les étiquettes.

## Exemples de producteur

Carte simple :

```json
{
  "title": "Deploy approval",
  "tone": "warning",
  "blocks": [
    { "type": "text", "text": "Canary is ready to promote." },
    { "type": "context", "text": "Build 1234, staging passed." },
    {
      "type": "buttons",
      "buttons": [
        { "label": "Approve", "value": "deploy:approve", "style": "success" },
        { "label": "Decline", "value": "deploy:decline", "style": "danger" }
      ]
    }
  ]
}
```

Bouton de lien URL uniquement :

```json
{
  "blocks": [
    { "type": "text", "text": "Release notes are ready." },
    {
      "type": "buttons",
      "buttons": [{ "label": "Open notes", "url": "https://example.com/release" }]
    }
  ]
}
```

Menu de sélection :

```json
{
  "title": "Choose environment",
  "blocks": [
    {
      "type": "select",
      "placeholder": "Environment",
      "options": [
        { "label": "Canary", "value": "env:canary" },
        { "label": "Production", "value": "env:prod" }
      ]
    }
  ]
}
```

Envoi CLI :

```bash
openclaw message send --channel slack \
  --target channel:C123 \
  --message "Deploy approval" \
  --presentation '{"title":"Deploy approval","tone":"warning","blocks":[{"type":"text","text":"Canary is ready."},{"type":"buttons","buttons":[{"label":"Approve","value":"deploy:approve","style":"success"},{"label":"Decline","value":"deploy:decline","style":"danger"}]}]}'
```

Livraison épinglée :

```bash
openclaw message send --channel telegram \
  --target -1001234567890 \
  --message "Topic opened" \
  --pin
```

Livraison épinglée avec JSON explicite :

```json
{
  "pin": {
    "enabled": true,
    "notify": true,
    "required": false
  }
}
```

## Contrat de rendu

Les plugins de canal déclarent le support de rendu sur leur adaptateur sortant :

```ts
const adapter: ChannelOutboundAdapter = {
  deliveryMode: "direct",
  presentationCapabilities: {
    supported: true,
    buttons: true,
    selects: true,
    context: true,
    divider: true,
  },
  deliveryCapabilities: {
    pin: true,
  },
  renderPresentation({ payload, presentation, ctx }) {
    return renderNativePayload(payload, presentation, ctx);
  },
  async pinDeliveredMessage({ target, messageId, pin }) {
    await pinNativeMessage(target, messageId, { notify: pin.notify === true });
  },
};
```

Les champs de capacité sont intentionnellement des booléens simples. Ils décrivent ce que le
rendu peut rendre interactif, pas chaque limite de plateforme native. Les rendus possèdent toujours
les limites spécifiques à la plateforme telles que le nombre maximum de boutons, le nombre de blocs et
la taille de la carte.

## Flux de rendu principal

Lorsqu'une `ReplyPayload` ou une action de message inclut `presentation`, le cœur :

1. Normalise la charge utile de présentation.
2. Résout l'adaptateur sortant du canal cible.
3. Lit `presentationCapabilities`.
4. Appelle `renderPresentation` lorsque l'adaptateur peut rendre la charge utile.
5. Revient au texte conservateur lorsque l'adaptateur est absent ou ne peut pas rendre.
6. Envoie la charge utile résultante via le chemin de livraison de canal normal.
7. Applique les métadonnées de livraison telles que `delivery.pin` après le premier message envoyé avec succès.

Le cœur possède le comportement de secours afin que les producteurs puissent rester agnostiques du canal. Les
plugins de canal possèdent le rendu natif et la gestion des interactions.

## Règles de dégradation

La présentation doit être sûre à envoyer sur les canaux limités.

Le texte de secours inclut :

- `title` comme première ligne
- blocs `text` comme paragraphes normaux
- blocs `context` comme lignes de contexte compactes
- blocs `divider` comme séparateur visuel
- étiquettes de bouton, y compris les URL pour les boutons de lien
- étiquettes d'option de sélection

Les contrôles natifs non supportés doivent se dégrader plutôt que d'échouer l'envoi entier.
Exemples :

- Telegram avec les boutons en ligne désactivés envoie le texte de secours.
- Un canal sans support de sélection liste les options de sélection en tant que texte.
- Un bouton URL uniquement devient soit un bouton de lien natif, soit une ligne d'URL de secours.
- Les défaillances d'épinglage optionnel ne font pas échouer le message livré.

L'exception principale est `delivery.pin.required: true` ; si l'épinglage est demandé comme
requis et le canal ne peut pas épingler le message envoyé, la livraison signale un échec.

## Mappage des fournisseurs

Rendus groupés actuels :

| Canal           | Cible de rendu natif                | Notes
