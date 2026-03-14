---
summary: "Support du canal WhatsApp, contrôles d'accès, comportement de livraison et opérations"
read_when:
  - Working on WhatsApp/web channel behavior or inbox routing
title: "WhatsApp"
---

# WhatsApp (Canal Web)

Statut : prêt pour la production via WhatsApp Web (Baileys). La passerelle possède la ou les sessions liées.

<CardGroup cols={3}>
  <Card title="Appairage" icon="link" href="/channels/pairing">
    La politique DM par défaut est l'appairage pour les expéditeurs inconnus.
  </Card>
  <Card title="Dépannage du canal" icon="wrench" href="/channels/troubleshooting">
    Diagnostics multi-canaux et guides de réparation.
  </Card>
  <Card title="Configuration de la passerelle" icon="settings" href="/gateway/configuration">
    Modèles et exemples de configuration de canal complets.
  </Card>
</CardGroup>

## Configuration rapide

<Steps>
  <Step title="Configurer la politique d'accès WhatsApp">

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      allowFrom: ["+15551234567"],
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
}
```

  </Step>

  <Step title="Lier WhatsApp (QR)">

```bash
openclaw channels login --channel whatsapp
```

    Pour un compte spécifique :

```bash
openclaw channels login --channel whatsapp --account work
```

  </Step>

  <Step title="Démarrer la passerelle">

```bash
openclaw gateway
```

  </Step>

  <Step title="Approuver la première demande d'appairage (si vous utilisez le mode appairage)">

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

    Les demandes d'appairage expirent après 1 heure. Les demandes en attente sont limitées à 3 par canal.

  </Step>
</Steps>

<Note>
OpenClaw recommande d'exécuter WhatsApp sur un numéro séparé si possible. (Le flux de métadonnées de canal et d'intégration est optimisé pour cette configuration, mais les configurations avec numéro personnel sont également prises en charge.)
</Note>

## Modèles de déploiement

<AccordionGroup>
  <Accordion title="Numéro dédié (recommandé)">
    C'est le mode opérationnel le plus propre :

    - identité WhatsApp séparée pour OpenClaw
    - listes de blocage DM et limites de routage plus claires
    - risque réduit de confusion d'auto-chat

    Modèle de politique minimal :

    ```json5
    {
      channels: {
        whatsapp: {
          dmPolicy: "allowlist",
          allowFrom: ["+15551234567"],
        },
      },
    }
    ```

  </Accordion>

  <Accordion title="Secours avec numéro personnel">
    L'intégration prend en charge le mode numéro personnel et écrit une base de référence conviviale pour l'auto-chat :

    - `dmPolicy: "allowlist"`
    - `allowFrom` inclut votre numéro personnel
    - `selfChatMode: true`

    À l'exécution, les protections d'auto-chat utilisent le numéro d'auto-liaison et `allowFrom`.

  </Accordion>

  <Accordion title="Portée du canal WhatsApp Web uniquement">
    Le canal de plateforme de messagerie est basé sur WhatsApp Web (`Baileys`) dans l'architecture actuelle du canal OpenClaw.

    Il n'y a pas de canal de messagerie WhatsApp Twilio séparé dans le registre de canal de chat intégré.

  </Accordion>
</AccordionGroup>

## Modèle d'exécution

- La passerelle possède le socket WhatsApp et la boucle de reconnexion.
- Les envois sortants nécessitent un écouteur WhatsApp actif pour le compte cible.
- Les chats de statut et de diffusion sont ignorés (`@status`, `@broadcast`).
- Les chats directs utilisent les règles de session DM (`session.dmScope` ; la valeur par défaut `main` réduit les DM à la session principale de l'agent).
- Les sessions de groupe sont isolées (`agent:<agentId>:whatsapp:group:<jid>`).

## Contrôle d'accès et activation

<Tabs>
  <Tab title="Politique DM">
    `channels.whatsapp.dmPolicy` contrôle l'accès au chat direct :

    - `pairing` (par défaut)
    - `allowlist`
    - `open` (nécessite que `allowFrom` inclue `"*"`)
    - `disabled`

    `allowFrom` accepte les numéros au format E.164 (normalisés en interne).

    Remplacement multi-compte : `channels.whatsapp.accounts.<id>.dmPolicy` (et `allowFrom`) ont priorité sur les valeurs par défaut au niveau du canal pour ce compte.

    Détails du comportement à l'exécution :

    - les appairages sont persistés dans le magasin de blocage du canal et fusionnés avec `allowFrom` configuré
    - si aucune liste de blocage n'est configurée, le numéro d'auto-liaison est autorisé par défaut
    - les DM sortants `fromMe` ne sont jamais appairés automatiquement

  </Tab>

  <Tab title="Politique de groupe + listes de blocage">
    L'accès au groupe a deux niveaux :

    1. **Liste de blocage d'adhésion au groupe** (`channels.whatsapp.groups`)
       - si `groups` est omis, tous les groupes sont éligibles
       - si `groups` est présent, il agit comme une liste de blocage de groupe (`"*"` autorisé)

    2. **Politique d'expéditeur de groupe** (`channels.whatsapp.groupPolicy` + `groupAllowFrom`)
       - `open` : liste de blocage d'expéditeur contournée
       - `allowlist` : l'expéditeur doit correspondre à `groupAllowFrom` (ou `*`)
       - `disabled` : bloquer tous les entrées de groupe

    Secours de liste de blocage d'expéditeur :

    - si `groupAllowFrom` n'est pas défini, l'exécution revient à `allowFrom` si disponible
    - les listes de blocage d'expéditeur sont évaluées avant l'activation de mention/réponse

    Remarque : si aucun bloc `channels.whatsapp` n'existe du tout, le secours de politique de groupe à l'exécution est `allowlist` (avec un journal d'avertissement), même si `channels.defaults.groupPolicy` est défini.

  </Tab>

  <Tab title="Mentions + /activation">
    Les réponses de groupe nécessitent une mention par défaut.

    La détection de mention inclut :

    - mentions explicites WhatsApp de l'identité du bot
    - modèles de regex de mention configurés (`agents.list[].groupChat.mentionPatterns`, secours `messages.groupChat.mentionPatterns`)
    - détection implicite de réponse au bot (l'expéditeur de la réponse correspond à l'identité du bot)

    Remarque de sécurité :

    - la citation/réponse satisfait uniquement le contrôle de mention ; elle n'accorde **pas** l'autorisation d'expéditeur
    - avec `groupPolicy: "allowlist"`, les expéditeurs non autorisés sont toujours bloqués même s'ils répondent au message d'un utilisateur autorisé

    Commande d'activation au niveau de la session :

    - `/activation mention`
    - `/activation always`

    `activation` met à jour l'état de la session (pas la configuration globale). Elle est contrôlée par le propriétaire.

  </Tab>
</Tabs>

## Comportement d'auto-chat et de numéro personnel

Lorsque le numéro d'auto-liaison est également présent dans `allowFrom`, les protections d'auto-chat WhatsApp s'activent :

- ignorer les accusés de lecture pour les tours d'auto-chat
- ignorer le comportement d'auto-déclenchement de mention-JID qui vous ferait vous mentionner vous-même
- si `messages.responsePrefix` n'est pas défini, les réponses d'auto-chat utilisent par défaut `[{identity.name}]` ou `[openclaw]`

## Normalisation des messages et contexte

<AccordionGroup>
  <Accordion title="Enveloppe entrante + contexte de réponse">
    Les messages WhatsApp entrants sont enveloppés dans l'enveloppe entrante partagée.

    Si une réponse citée existe, le contexte est ajouté sous cette forme :

    ```text
    [Replying to <sender> id:<stanzaId>]
    <quoted body or media placeholder>
    [/Replying]
    ```

    Les champs de métadonnées de réponse sont également remplis si disponibles (`ReplyToId`, `ReplyToBody`, `ReplyToSender`, JID/E.164 d'expéditeur).

  </Accordion>

  <Accordion title="Espaces réservés aux médias et extraction de localisation/contact">
    Les messages entrants contenant uniquement des médias sont normalisés avec des espaces réservés tels que :

    - `<media:image>`
    - `<media:video>`
    - `<media:audio>`
    - `<media:document>`
    - `<media:sticker>`

    Les charges utiles de localisation et de contact sont normalisées en contexte textuel avant le routage.

  </Accordion>

  <Accordion title="Injection d'historique de groupe en attente">
    Pour les groupes, les messages non traités peuvent être mis en mémoire tampon et injectés en tant que contexte lorsque le bot est finalement déclenché.

    - limite par défaut : `50`
    - config : `channels.whatsapp.historyLimit`
    - secours : `messages.groupChat.historyLimit`
    - `0` désactive

    Marqueurs d'injection :

    - `[Chat messages since your last reply - for context]`
    - `[Current message - respond to this]`

  </Accordion>

  <Accordion title="Accusés de lecture">
    Les accusés de lecture sont activés par défaut pour les messages WhatsApp entrants acceptés.

    Désactiver globalement :

    ```json5
    {
      channels: {
        whatsapp: {
          sendReadReceipts: false,
        },
      },
    }
    ```

    Remplacement par compte :

    ```json5
    {
      channels: {
        whatsapp: {
          accounts: {
            work: {
              sendReadReceipts: false,
            },
          },
        },
      },
    }
    ```

    Les tours d'auto-chat ignorent les accusés de lecture même lorsqu'ils sont activés globalement.

  </Accordion>
</AccordionGroup>

## Livraison, segmentation et médias

<AccordionGroup>
  <Accordion title="Segmentation de texte">
    - limite de segment par défaut : `channels.whatsapp.textChunkLimit = 4000`
    - `channels.whatsapp.chunkMode = "length" | "newline"`
    - le mode `newline` préfère les limites de paragraphe (lignes vides), puis revient à la segmentation sûre en longueur
  </Accordion>

  <Accordion title="Comportement des médias sortants">
    - prend en charge les charges utiles image, vidéo, audio (note vocale PTT) et document
    - `audio/ogg` est réécrit en `audio/ogg; codecs=opus` pour la compatibilité des notes vocales
    - la lecture GIF animée est prise en charge via `gifPlayback: true` sur les envois vidéo
    - les légendes sont appliquées au premier élément multimédia lors de l'envoi de charges utiles de réponse multi-médias
    - la source multimédia peut être HTTP(S), `file://` ou des chemins locaux
  </Accordion>

  <Accordion title="Limites de taille des médias et comportement de secours">
    - limite de sauvegarde des médias entrants : `channels.whatsapp.mediaMaxMb` (par défaut `50`)
    - limite d'envoi des médias sortants : `channels.whatsapp.mediaMaxMb` (par défaut `50`)
    - les remplacements par compte utilisent `channels.whatsapp.accounts.<accountId>.mediaMaxMb`
    - les images sont automatiquement optimisées (redimensionnement/balayage de qualité) pour s'adapter aux limites
    - en cas d'échec d'envoi de média, le secours du premier élément envoie un avertissement textuel au lieu de supprimer silencieusement la réponse
  </Accordion>
</AccordionGroup>

## Réactions d'accusé de réception

WhatsApp prend en charge les réactions d'accusé de réception immédiates à la réception entrante via `channels.whatsapp.ackReaction`.

```json5
{
  channels: {
    whatsapp: {
      ackReaction: {
        emoji: "👀",
        direct: true,
        group: "mentions", // always | mentions | never
      },
    },
  },
}
```

Remarques sur le comportement :

- envoyé immédiatement après l'acceptation entrante (pré-réponse)
- les échecs sont enregistrés mais ne bloquent pas la livraison normale des réponses
- le mode groupe `mentions` réagit sur les tours déclenchés par mention ; l'activation de groupe `always` agit comme un contournement pour cette vérification
- WhatsApp utilise `channels.whatsapp.ackReaction` (l'héritage `messages.ackReaction` n'est pas utilisé ici)

## Multi-compte et identifiants

<AccordionGroup>
  <Accordion title="Sélection de compte et valeurs par défaut">
    - les identifiants de compte proviennent de `channels.whatsapp.accounts`
    - sélection de compte par défaut : `default` si présent, sinon premier identifiant de compte configuré (trié)
    - les identifiants de compte sont normalisés en interne pour la recherche
  </Accordion>

  <Accordion title="Chemins d'identifiants et compatibilité héritée">
    - chemin d'authentification actuel : `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
    - fichier de sauvegarde : `creds.json.bak`
    - l'authentification par défaut héritée dans `~/.openclaw/credentials/` est toujours reconnue/migrée pour les flux de compte par défaut
  </Accordion>

  <Accordion title="Comportement de déconnexion">
    `openclaw channels logout --channel whatsapp [--account <id>]` efface l'état d'authentification WhatsApp pour
