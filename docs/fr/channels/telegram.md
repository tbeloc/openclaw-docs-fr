---
summary: "Statut de support du bot Telegram, capacités et configuration"
read_when:
  - Working on Telegram features or webhooks
title: "Telegram"
---

# Telegram (Bot API)

Statut : prêt pour la production pour les DM de bot + groupes via grammY. Le long polling est le mode par défaut ; le mode webhook est optionnel.

<CardGroup cols={3}>
  <Card title="Pairing" icon="link" href="/channels/pairing">
    La politique DM par défaut pour Telegram est le pairing.
  </Card>
  <Card title="Channel troubleshooting" icon="wrench" href="/channels/troubleshooting">
    Diagnostics multi-canaux et playbooks de réparation.
  </Card>
  <Card title="Gateway configuration" icon="settings" href="/gateway/configuration">
    Modèles et exemples de configuration de canal complets.
  </Card>
</CardGroup>

## Configuration rapide

<Steps>
  <Step title="Créer le token du bot dans BotFather">
    Ouvrez Telegram et discutez avec **@BotFather** (confirmez que le handle est exactement `@BotFather`).

    Exécutez `/newbot`, suivez les invites et enregistrez le token.

  </Step>

  <Step title="Configurer le token et la politique DM">

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

    Fallback env : `TELEGRAM_BOT_TOKEN=...` (compte par défaut uniquement).
    Telegram n'utilise **pas** `openclaw channels login telegram` ; configurez le token dans config/env, puis démarrez la gateway.

  </Step>

  <Step title="Démarrer la gateway et approuver le premier DM">

```bash
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

    Les codes de pairing expirent après 1 heure.

  </Step>

  <Step title="Ajouter le bot à un groupe">
    Ajoutez le bot à votre groupe, puis définissez `channels.telegram.groups` et `groupPolicy` pour correspondre à votre modèle d'accès.
  </Step>
</Steps>

<Note>
L'ordre de résolution du token est conscient du compte. En pratique, les valeurs de config l'emportent sur le fallback env, et `TELEGRAM_BOT_TOKEN` s'applique uniquement au compte par défaut.
</Note>

## Paramètres côté Telegram

<AccordionGroup>
  <Accordion title="Mode de confidentialité et visibilité des groupes">
    Les bots Telegram sont par défaut en **Mode de confidentialité**, ce qui limite les messages de groupe qu'ils reçoivent.

    Si le bot doit voir tous les messages du groupe, soit :

    - désactiver le mode de confidentialité via `/setprivacy`, soit
    - faire du bot un administrateur du groupe.

    Lors du basculement du mode de confidentialité, supprimez et réajoutez le bot dans chaque groupe pour que Telegram applique la modification.

  </Accordion>

  <Accordion title="Permissions de groupe">
    Le statut d'administrateur est contrôlé dans les paramètres du groupe Telegram.

    Les bots administrateurs reçoivent tous les messages du groupe, ce qui est utile pour un comportement de groupe toujours actif.

  </Accordion>

  <Accordion title="Bascules BotFather utiles">

    - `/setjoingroups` pour autoriser/refuser les ajouts de groupe
    - `/setprivacy` pour le comportement de visibilité du groupe

  </Accordion>
</AccordionGroup>

## Contrôle d'accès et activation

<Tabs>
  <Tab title="Politique DM">
    `channels.telegram.dmPolicy` contrôle l'accès aux messages directs :

    - `pairing` (par défaut)
    - `allowlist` (nécessite au moins un ID d'expéditeur dans `allowFrom`)
    - `open` (nécessite que `allowFrom` inclue `"*"`)
    - `disabled`

    `channels.telegram.allowFrom` accepte les ID d'utilisateur Telegram numériques. Les préfixes `telegram:` / `tg:` sont acceptés et normalisés.
    `dmPolicy: "allowlist"` avec `allowFrom` vide bloque tous les DM et est rejeté par la validation de config.
    L'assistant d'intégration accepte l'entrée `@username` et la résout en ID numériques.
    Si vous avez mis à niveau et que votre config contient des entrées de liste blanche `@username`, exécutez `openclaw doctor --fix` pour les résoudre (meilleur effort ; nécessite un token de bot Telegram).
    Si vous aviez précédemment compté sur les fichiers de liste blanche du magasin de pairing, `openclaw doctor --fix` peut récupérer les entrées dans `channels.telegram.allowFrom` dans les flux de liste blanche (par exemple quand `dmPolicy: "allowlist"` n'a pas encore d'ID explicites).

    Pour les bots à propriétaire unique, préférez `dmPolicy: "allowlist"` avec des ID `allowFrom` numériques explicites pour garder la politique d'accès durable dans la config (au lieu de dépendre des approbations de pairing précédentes).

    ### Trouver votre ID d'utilisateur Telegram

    Plus sûr (pas de bot tiers) :

    1. Envoyez un DM à votre bot.
    2. Exécutez `openclaw logs --follow`.
    3. Lisez `from.id`.

    Méthode officielle de l'API Bot :

```bash
curl "https://api.telegram.org/bot<bot_token>/getUpdates"
```

    Méthode tierce (moins privée) : `@userinfobot` ou `@getidsbot`.

  </Tab>

  <Tab title="Politique de groupe et listes blanches">
    Deux contrôles s'appliquent ensemble :

    1. **Quels groupes sont autorisés** (`channels.telegram.groups`)
       - pas de config `groups` :
         - avec `groupPolicy: "open"` : n'importe quel groupe peut passer les vérifications d'ID de groupe
         - avec `groupPolicy: "allowlist"` (par défaut) : les groupes sont bloqués jusqu'à ce que vous ajoutiez des entrées `groups` (ou `"*"`)
       - `groups` configuré : agit comme liste blanche (ID explicites ou `"*"`)

    2. **Quels expéditeurs sont autorisés dans les groupes** (`channels.telegram.groupPolicy`)
       - `open`
       - `allowlist` (par défaut)
       - `disabled`

    `groupAllowFrom` est utilisé pour le filtrage des expéditeurs de groupe. S'il n'est pas défini, Telegram revient à `allowFrom`.
    Les entrées `groupAllowFrom` doivent être des ID d'utilisateur Telegram numériques (les préfixes `telegram:` / `tg:` sont normalisés).
    Ne mettez pas les ID de chat de groupe ou de supergroupe Telegram dans `groupAllowFrom`. Les ID de chat négatifs appartiennent à `channels.telegram.groups`.
    Les entrées non numériques sont ignorées pour l'autorisation de l'expéditeur.
    Limite de sécurité (`2026.2.25+`) : l'authentification de l'expéditeur du groupe n'hérite **pas** des approbations du magasin de pairing DM.
    Le pairing reste DM uniquement. Pour les groupes, définissez `groupAllowFrom` ou `allowFrom` par groupe/par sujet.
    Note d'exécution : si `channels.telegram` est complètement absent, l'exécution par défaut est `groupPolicy="allowlist"` fermé à moins que `channels.defaults.groupPolicy` soit explicitement défini.

    Exemple : autoriser n'importe quel membre dans un groupe spécifique :

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          groupPolicy: "open",
          requireMention: false,
        },
      },
    },
  },
}
```

    Exemple : autoriser uniquement des utilisateurs spécifiques dans un groupe spécifique :

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          requireMention: true,
          allowFrom: ["8734062810", "745123456"],
        },
      },
    },
  },
}
```

    <Warning>
      Erreur courante : `groupAllowFrom` n'est pas une liste blanche de groupe Telegram.

      - Mettez les ID de chat de groupe ou de supergroupe Telegram négatifs comme `-1001234567890` sous `channels.telegram.groups`.
      - Mettez les ID d'utilisateur Telegram comme `8734062810` sous `groupAllowFrom` quand vous voulez limiter les personnes à l'intérieur d'un groupe autorisé qui peuvent déclencher le bot.
      - Utilisez `groupAllowFrom: ["*"]` uniquement quand vous voulez que n'importe quel membre d'un groupe autorisé puisse parler au bot.
    </Warning>

  </Tab>

  <Tab title="Comportement de mention">
    Les réponses de groupe nécessitent une mention par défaut.

    La mention peut provenir de :

    - mention native `@botusername`, ou
    - modèles de mention dans :
      - `agents.list[].groupChat.mentionPatterns`
      - `messages.groupChat.mentionPatterns`

    Bascules de commande au niveau de la session :

    - `/activation always`
    - `/activation mention`

    Celles-ci mettent à jour l'état de la session uniquement. Utilisez la config pour la persistance.

    Exemple de config persistante :

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: false },
      },
    },
  },
}
```

    Obtenir l'ID du chat de groupe :

    - transférer un message de groupe à `@userinfobot` / `@getidsbot`
    - ou lire `chat.id` depuis `openclaw logs --follow`
    - ou inspecter l'API Bot `getUpdates`

  </Tab>
</Tabs>

## Comportement à l'exécution

- Telegram est détenu par le processus de la gateway.
- Le routage est déterministe : les réponses entrantes Telegram reviennent à Telegram (le modèle ne choisit pas les canaux).
- Les messages entrants se normalisent dans l'enveloppe de canal partagée avec les métadonnées de réponse et les espaces réservés de média.
- Les sessions de groupe sont isolées par ID de groupe. Les sujets du forum ajoutent `:topic:<threadId>` pour garder les sujets isolés.
- Les messages DM peuvent porter `message_thread_id` ; OpenClaw les achemine avec des clés de session conscientes des threads et préserve l'ID de thread pour les réponses.
- Le long polling utilise le runner grammY avec séquençage par chat/par thread. La concurrence du sink du runner global utilise `agents.defaults.maxConcurrent`.
- L'API Bot Telegram n'a pas de support de reçu de lecture (`sendReadReceipts` ne s'applique pas).

## Référence des fonctionnalités

<AccordionGroup>
  <Accordion title="Aperçu du flux en direct (éditions de messages)">
    OpenClaw peut diffuser les réponses partielles en temps réel :

    - chats directs : message d'aperçu + `editMessageText`
    - groupes/sujets : message d'aperçu + `editMessageText`

    Exigence :

    - `channels.telegram.streaming` est `off | partial | block | progress` (par défaut : `partial`)
    - `progress` mappe à `partial` sur Telegram (compat avec la dénomination multi-canaux)
    - les valeurs `streamMode` et `streaming` booléennes héritées sont mappées automatiquement

    Pour les réponses texte uniquement :

    - DM : OpenClaw garde le même message d'aperçu et effectue une édition finale en place (pas de deuxième message)
    - groupe/sujet : OpenClaw garde le même message d'aperçu et effectue une édition finale en place (pas de deuxième message)

    Pour les réponses complexes (par exemple les charges utiles de média), OpenClaw revient à la livraison finale normale puis nettoie le message d'aperçu.

    La diffusion d'aperçu est séparée de la diffusion de bloc. Quand la diffusion de bloc est explicitement activée pour Telegram, OpenClaw ignore le flux d'aperçu pour éviter la double diffusion.

    Si le transport de brouillon natif n'est pas disponible/rejeté, OpenClaw revient automatiquement à `sendMessage` + `editMessageText`.

    Flux de raisonnement spécifique à Telegram :

    - `/reasoning stream` envoie le raisonnement à l'aperçu en direct pendant la génération
    - la réponse finale est envoyée sans texte de raisonnement

  </Accordion>

  <Accordion title="Formatage et fallback HTML">
    Le texte sortant utilise Telegram `parse_mode: "HTML"`.

    - Le texte de style Markdown est rendu en HTML sûr pour Telegram.
    - Le HTML brut du modèle est échappé pour réduire les échecs d'analyse Telegram.
    - Si Telegram rejette le HTML analysé, OpenClaw réessaie en texte brut.

    Les aperçus de lien sont activés par défaut et peuvent être désactivés avec `channels.telegram.linkPreview: false`.

  </Accordion>

  <Accordion title="Commandes natives et commandes personnalisées">
    L'enregistrement du menu de commande Telegram est géré au démarrage avec `setMyCommands`.

    Valeurs par défaut des commandes natives :

    - `commands.native: "auto"` active les commandes natives pour Telegram

    Ajouter des entrées de menu de commande personnalisées :

```json5
{
  channels: {
    telegram: {
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
    },
  },
}
```

    Règles :

    - les noms sont normalisés (supprimez le `/` initial, minuscules)
    - modèle valide : `a-z`, `0-9`, `_`, longueur `1..32`
    - les commandes personnalisées ne peuvent pas remplacer les commandes natives
    - les conflits/doublons sont ignorés et enregistrés

    Notes :

    - les commandes personnalisées sont des entrées de menu uniquement ; elles n'implémentent pas automatiquement le comportement
    - les commandes de plugin/skill peuvent toujours fonctionner quand elles sont tapées même si elles ne sont
