---
title: Plan de refactorisation de la présentation des canaux
summary: Découpler la présentation sémantique des messages des renderers natifs de l'interface utilisateur des canaux.
read_when:
  - Refactorisation de l'interface utilisateur des messages de canal, des charges utiles interactives ou des renderers natifs des canaux
  - Modification des capacités des outils de message, des indices de livraison ou des marqueurs inter-contextes
  - Débogage de l'importation Discord Carbon ou de la paresse d'exécution du plugin de canal
---

# Plan de refactorisation de la présentation des canaux

## Statut

Implémenté pour l'agent partagé, l'interface de ligne de commande, la capacité du plugin et les surfaces de livraison sortante :

- `ReplyPayload.presentation` porte l'interface utilisateur sémantique du message.
- `ReplyPayload.delivery.pin` porte les demandes d'épinglage des messages envoyés.
- Les actions de message partagées exposent `presentation`, `delivery` et `pin` au lieu des `components`, `blocks`, `buttons` ou `card` natifs du fournisseur.
- Le cœur rend ou dégénère automatiquement la présentation via les capacités sortantes déclarées par le plugin.
- Les renderers Discord, Slack, Telegram, Mattermost, MS Teams et Feishu consomment le contrat générique.
- Le code du plan de contrôle du canal Discord n'importe plus les conteneurs d'interface utilisateur soutenus par Carbon.

La documentation canonique se trouve maintenant dans [Message Presentation](/fr/plugins/message-presentation).
Conservez ce plan comme contexte d'implémentation historique ; mettez à jour le guide canonique
pour les modifications du contrat, du renderer ou du comportement de secours.

## Problème

L'interface utilisateur du canal est actuellement divisée entre plusieurs surfaces incompatibles :

- Le cœur possède un hook de renderer inter-contextes en forme de Discord via `buildCrossContextComponents`.
- Discord `channel.ts` peut importer l'interface utilisateur native Carbon via `DiscordUiContainer`, ce qui tire les dépendances d'interface utilisateur d'exécution dans le plan de contrôle du plugin de canal.
- L'agent et l'interface de ligne de commande exposent des échappatoires de charge utile native tels que Discord `components`, Slack `blocks`, Telegram ou Mattermost `buttons`, et Teams ou Feishu `card`.
- `ReplyPayload.channelData` porte à la fois des indices de transport et des enveloppes d'interface utilisateur native.
- Le modèle générique `interactive` existe, mais il est plus étroit que les mises en page plus riches déjà utilisées par Discord, Slack, Teams, Feishu, LINE, Telegram et Mattermost.

Cela rend le cœur conscient des formes d'interface utilisateur native, affaiblit la paresse d'exécution du plugin et donne aux agents trop de façons spécifiques au fournisseur d'exprimer la même intention de message.

## Objectifs

- Le cœur décide la meilleure présentation sémantique d'un message à partir des capacités déclarées.
- Les extensions déclarent les capacités et rendent la présentation sémantique dans les charges utiles de transport native.
- L'interface utilisateur du contrôle Web reste séparée de l'interface utilisateur native du chat.
- Les charges utiles de canal native ne sont pas exposées via la surface de message de l'agent partagé ou de l'interface de ligne de commande.
- Les fonctionnalités de présentation non prises en charge se dégénèrent automatiquement à la meilleure représentation textuelle.
- Le comportement de livraison tel que l'épinglage d'un message envoyé est une métadonnée de livraison générique, pas une présentation.

## Non-objectifs

- Aucun shim de compatibilité rétroactive pour `buildCrossContextComponents`.
- Aucune échappatoire native publique pour `components`, `blocks`, `buttons` ou `card`.
- Aucune importation de cœur de bibliothèques d'interface utilisateur natives des canaux.
- Aucune couture SDK spécifique au fournisseur pour les canaux groupés.

## Modèle cible

Ajouter un champ `presentation` appartenant au cœur à `ReplyPayload`.

```ts
type MessagePresentationTone = "neutral" | "info" | "success" | "warning" | "danger";

type MessagePresentation = {
  tone?: MessagePresentationTone;
  title?: string;
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
```

`interactive` devient un sous-ensemble de `presentation` lors de la migration :

- Le bloc de texte `interactive` correspond à `presentation.blocks[].type = "text"`.
- Le bloc de boutons `interactive` correspond à `presentation.blocks[].type = "buttons"`.
- Le bloc de sélection `interactive` correspond à `presentation.blocks[].type = "select"`.

Les schémas d'agent et d'interface de ligne de commande externes utilisent maintenant `presentation` ; `interactive` reste un helper d'analyse/rendu hérité interne pour les producteurs de réponses existants.

## Métadonnées de livraison

Ajouter un champ `delivery` appartenant au cœur pour le comportement d'envoi qui n'est pas une interface utilisateur.

```ts
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

Sémantique :

- `delivery.pin = true` signifie épingler le premier message livré avec succès.
- `notify` est par défaut `false`.
- `required` est par défaut `false` ; les canaux non pris en charge ou l'épinglage échoué se dégénèrent automatiquement en continuant la livraison.
- Les actions manuelles `pin`, `unpin` et `list-pins` restent pour les messages existants.

La liaison de rubrique ACP Telegram actuelle doit passer de `channelData.telegram.pin = true` à `delivery.pin = true`.

## Contrat de capacité d'exécution

Ajouter des hooks de rendu de présentation et de livraison à l'adaptateur sortant d'exécution, pas au plugin de canal du plan de contrôle.

```ts
type ChannelPresentationCapabilities = {
  supported: boolean;
  buttons?: boolean;
  selects?: boolean;
  context?: boolean;
  divider?: boolean;
  tones?: MessagePresentationTone[];
};

type ChannelDeliveryCapabilities = {
  pinSentMessage?: boolean;
};

type ChannelOutboundAdapter = {
  presentationCapabilities?: ChannelPresentationCapabilities;

  renderPresentation?: (params: {
    payload: ReplyPayload;
    presentation: MessagePresentation;
    ctx: ChannelOutboundSendContext;
  }) => ReplyPayload | null;

  deliveryCapabilities?: ChannelDeliveryCapabilities;

  pinDeliveredMessage?: (params: {
    cfg: OpenClawConfig;
    accountId?: string | null;
    to: string;
    threadId?: string | number | null;
    messageId: string;
    notify: boolean;
  }) => Promise<void>;
};
```

Comportement du cœur :

- Résoudre le canal cible et l'adaptateur d'exécution.
- Demander les capacités de présentation.
- Dégrader les blocs non pris en charge avant le rendu.
- Appeler `renderPresentation`.
- Si aucun renderer n'existe, convertir la présentation en secours textuel.
- Après un envoi réussi, appeler `pinDeliveredMessage` quand `delivery.pin` est demandé et pris en charge.

## Mappage des canaux

Discord :

- Rendre `presentation` aux composants v2 et aux conteneurs Carbon dans les modules d'exécution uniquement.
- Conserver les helpers de couleur d'accent dans les modules légers.
- Supprimer les importations `DiscordUiContainer` du code du plan de contrôle du plugin de canal.

Slack :

- Rendre `presentation` à Block Kit.
- Supprimer l'entrée `blocks` de l'agent et de l'interface de ligne de commande.

Telegram :

- Rendre le texte, le contexte et les diviseurs sous forme de texte.
- Rendre les actions et la sélection en tant que claviers en ligne lorsqu'ils sont configurés et autorisés pour la surface cible.
- Utiliser le secours textuel lorsque les boutons en ligne sont désactivés.
- Déplacer l'épinglage de rubrique ACP vers `delivery.pin`.

Mattermost :

- Rendre les actions en tant que boutons interactifs où configurés.
- Rendre les autres blocs en tant que secours textuel.

MS Teams :

- Rendre `presentation` aux cartes adaptatives.
- Conserver les actions manuelles d'épinglage/dépinglage/liste des épingles.
- Implémenter éventuellement `pinDeliveredMessage` si le support Graph est fiable pour la conversation cible.

Feishu :

- Rendre `presentation` aux cartes interactives.
- Conserver les actions manuelles d'épinglage/dépinglage/liste des épingles.
- Implémenter éventuellement `pinDeliveredMessage` pour l'épinglage des messages envoyés si le comportement de l'API est fiable.

LINE :

- Rendre `presentation` aux messages Flex ou modèles où possible.
- Revenir au texte pour les blocs non pris en charge.
- Supprimer les charges utiles d'interface utilisateur LINE de `channelData`.

Canaux simples ou limités :

- Convertir la présentation en texte avec un formatage conservateur.

## Étapes de refactorisation

1. Réappliquer le correctif de version Discord qui divise `ui-colors.ts` de l'interface utilisateur soutenus par Carbon et supprime `DiscordUiContainer` de `extensions/discord/src/channel.ts`.
2. Ajouter `presentation` et `delivery` à `ReplyPayload`, normalisation de charge utile sortante, résumés de livraison et charges utiles de hook.
3. Ajouter le schéma `MessagePresentation` et les helpers d'analyse dans un sous-chemin SDK/exécution étroit.
4. Remplacer les capacités de message `buttons`, `cards`, `components` et `blocks` par les capacités de présentation sémantique.
5. Ajouter des hooks d'adaptateur sortant d'exécution pour le rendu de présentation et l'épinglage de livraison.
6. Remplacer la construction de composants inter-contextes par `buildCrossContextPresentation`.
7. Supprimer `src/infra/outbound/channel-adapters.ts` et supprimer `buildCrossContextComponents` des types de plugin de canal.
8. Modifier `maybeApplyCrossContextMarker` pour attacher `presentation` au lieu de paramètres natifs.
9. Mettre à jour les chemins d'envoi de dispatch du plugin pour consommer uniquement la présentation sémantique et les métadonnées de livraison.
10. Supprimer les paramètres de charge utile native de l'agent et de l'interface de ligne de commande : `components`, `blocks`, `buttons` et `card`.
11. Supprimer les helpers SDK qui créent des schémas d'outils de message natifs, en les remplaçant par des helpers de schéma de présentation.
12. Supprimer les enveloppes d'interface utilisateur/native de `channelData` ; conserver uniquement les métadonnées de transport jusqu'à ce que chaque champ restant soit examiné.
13. Migrer les renderers Discord, Slack, Telegram, Mattermost, MS Teams, Feishu et LINE.
14. Mettre à jour la documentation pour le CLI de message, les pages de canal, le SDK du plugin et le livre de recettes des capacités.
15. Exécuter le profilage de fanout d'importation pour Discord et les points d'entrée de canal affectés.

Les étapes 1-11 et 13-14 sont implémentées dans cette refactorisation pour l'agent partagé, l'interface de ligne de commande, la capacité du plugin et les contrats d'adaptateur sortant. L'étape 12 reste une passe de nettoyage interne plus approfondie pour les enveloppes de transport `channelData` privées du fournisseur. L'étape 15 reste une validation de suivi si nous voulons des chiffres de fanout d'importation quantifiés au-delà de la porte de type/test.

## Tests

Ajouter ou mettre à jour :

- Tests de normalisation de présentation.
- Tests de dégénérescence automatique de présentation pour les blocs non pris en charge.
- Tests de marqueur inter-contextes pour le dispatch du plugin et les chemins de livraison du cœur.
- Tests de matrice de rendu de canal pour Discord, Slack, Telegram, Mattermost, MS Teams, Feishu, LINE et secours textuel.
- Tests de schéma d'outil de message prouvant que les champs natifs sont partis.
- Tests d'interface de ligne de commande prouvant que les drapeaux natifs sont partis.
- Régression de paresse d'importation du point d'entrée Discord couvrant Carbon.
- Tests d'épinglage de livraison couvrant Telegram et le secours générique.

## Questions ouvertes

- `delivery.pin` doit-il être implémenté pour Discord, Slack, MS Teams et Feishu lors du premier passage, ou seulement Telegram en premier ?
- `delivery` devrait-il éventuellement absorber les champs existants tels que `replyToId`, `replyToCurrent`, `silent` et `audioAsVoice`, ou rester concentré sur les comportements post-envoi ?
- La présentation devrait-elle prendre en charge les images ou les références de fichiers directement, ou les médias devraient-ils rester séparés de la mise en page de l'interface utilisateur pour l'instant ?
