```markdown
---
summary: "Support iMessage hérité via imsg (JSON-RPC sur stdio). Les nouvelles configurations doivent utiliser BlueBubbles."
read_when:
  - Setting up iMessage support
  - Debugging iMessage send/receive
title: "iMessage"
---

# iMessage (hérité : imsg)

<Warning>
Pour les nouveaux déploiements iMessage, utilisez <a href="/channels/bluebubbles">BlueBubbles</a>.

L'intégration `imsg` est héritée et peut être supprimée dans une version future.
</Warning>

Statut : intégration CLI externe héritée. La passerelle lance `imsg rpc` et communique via JSON-RPC sur stdio (pas de démon/port séparé).

<CardGroup cols={3}>
  <Card title="BlueBubbles (recommandé)" icon="message-circle" href="/channels/bluebubbles">
    Chemin iMessage préféré pour les nouvelles configurations.
  </Card>
  <Card title="Appairage" icon="link" href="/channels/pairing">
    Les DM iMessage utilisent par défaut le mode appairage.
  </Card>
  <Card title="Référence de configuration" icon="settings" href="/gateway/configuration-reference#imessage">
    Référence complète des champs iMessage.
  </Card>
</CardGroup>

## Configuration rapide

<Tabs>
  <Tab title="Mac local (chemin rapide)">
    <Steps>
      <Step title="Installer et vérifier imsg">

```bash
brew install steipete/tap/imsg
imsg rpc --help
```

      </Step>

      <Step title="Configurer OpenClaw">

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/usr/local/bin/imsg",
      dbPath: "/Users/<you>/Library/Messages/chat.db",
    },
  },
}
```

      </Step>

      <Step title="Démarrer la passerelle">

```bash
openclaw gateway
```

      </Step>

      <Step title="Approuver le premier appairage DM (dmPolicy par défaut)">

```bash
openclaw pairing list imessage
openclaw pairing approve imessage <CODE>
```

        Les demandes d'appairage expirent après 1 heure.
      </Step>
    </Steps>

  </Tab>

  <Tab title="Mac distant via SSH">
    OpenClaw ne nécessite qu'un `cliPath` compatible stdio, vous pouvez donc pointer `cliPath` vers un script wrapper qui se connecte en SSH à un Mac distant et exécute `imsg`.

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

    Configuration recommandée quand les pièces jointes sont activées :

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "user@gateway-host", // utilisé pour les récupérations de pièces jointes SCP
      includeAttachments: true,
      // Optionnel : remplacer les racines de pièces jointes autorisées.
      // Les valeurs par défaut incluent /Users/*/Library/Messages/Attachments
      attachmentRoots: ["/Users/*/Library/Messages/Attachments"],
      remoteAttachmentRoots: ["/Users/*/Library/Messages/Attachments"],
    },
  },
}
```

    Si `remoteHost` n'est pas défini, OpenClaw tente de le détecter automatiquement en analysant le script wrapper SSH.
    `remoteHost` doit être `host` ou `user@host` (sans espaces ni options SSH).
    OpenClaw utilise la vérification stricte des clés d'hôte pour SCP, donc la clé d'hôte relais doit déjà exister dans `~/.ssh/known_hosts`.
    Les chemins de pièces jointes sont validés par rapport aux racines autorisées (`attachmentRoots` / `remoteAttachmentRoots`).

  </Tab>
</Tabs>

## Exigences et permissions (macOS)

- Messages doit être connecté sur le Mac exécutant `imsg`.
- L'accès complet au disque est requis pour le contexte de processus exécutant OpenClaw/`imsg` (accès à la base de données Messages).
- La permission d'automatisation est requise pour envoyer des messages via Messages.app.

<Tip>
Les permissions sont accordées par contexte de processus. Si la passerelle s'exécute sans interface (LaunchAgent/SSH), exécutez une commande interactive unique dans ce même contexte pour déclencher les invites :

```bash
imsg chats --limit 1
# ou
imsg send <handle> "test"
```

</Tip>

## Contrôle d'accès et routage

<Tabs>
  <Tab title="Politique DM">
    `channels.imessage.dmPolicy` contrôle les messages directs :

    - `pairing` (par défaut)
    - `allowlist`
    - `open` (nécessite que `allowFrom` inclue `"*"`)
    - `disabled`

    Champ liste blanche : `channels.imessage.allowFrom`.

    Les entrées de liste blanche peuvent être des handles ou des cibles de chat (`chat_id:*`, `chat_guid:*`, `chat_identifier:*`).

  </Tab>

  <Tab title="Politique de groupe + mentions">
    `channels.imessage.groupPolicy` contrôle la gestion des groupes :

    - `allowlist` (par défaut quand configuré)
    - `open`
    - `disabled`

    Liste blanche des expéditeurs de groupe : `channels.imessage.groupAllowFrom`.

    Secours à l'exécution : si `groupAllowFrom` n'est pas défini, les vérifications des expéditeurs de groupe iMessage se replient sur `allowFrom` quand disponible.
    Note à l'exécution : si `channels.imessage` est complètement absent, le runtime se replie sur `groupPolicy="allowlist"` et enregistre un avertissement (même si `channels.defaults.groupPolicy` est défini).

    Gating des mentions pour les groupes :

    - iMessage n'a pas de métadonnées de mention natives
    - la détection des mentions utilise des motifs regex (`agents.list[].groupChat.mentionPatterns`, secours `messages.groupChat.mentionPatterns`)
    - sans motifs configurés, le gating des mentions ne peut pas être appliqué

    Les commandes de contrôle des expéditeurs autorisés peuvent contourner le gating des mentions dans les groupes.

  </Tab>

  <Tab title="Sessions et réponses déterministes">
    - Les DM utilisent le routage direct ; les groupes utilisent le routage de groupe.
    - Avec le `session.dmScope=main` par défaut, les DM iMessage s'effondrent dans la session principale de l'agent.
    - Les sessions de groupe sont isolées (`agent:<agentId>:imessage:group:<chat_id>`).
    - Les réponses sont routées vers iMessage en utilisant les métadonnées de canal/cible d'origine.

    Comportement de thread de type groupe :

    Certains threads iMessage multi-participants peuvent arriver avec `is_group=false`.
    Si ce `chat_id` est explicitement configuré sous `channels.imessage.groups`, OpenClaw le traite comme du trafic de groupe (gating de groupe + isolation de session de groupe).

  </Tab>
</Tabs>

## Modèles de déploiement

<AccordionGroup>
  <Accordion title="Utilisateur macOS bot dédié (identité iMessage séparée)">
    Utilisez un Apple ID dédié et un utilisateur macOS afin que le trafic bot soit isolé de votre profil Messages personnel.

    Flux typique :

    1. Créer/se connecter à un utilisateur macOS dédié.
    2. Se connecter à Messages avec l'Apple ID bot dans cet utilisateur.
    3. Installer `imsg` dans cet utilisateur.
    4. Créer un wrapper SSH pour qu'OpenClaw puisse exécuter `imsg` dans ce contexte utilisateur.
    5. Pointer `channels.imessage.accounts.<id>.cliPath` et `.dbPath` vers ce profil utilisateur.

    La première exécution peut nécessiter des approbations GUI (Automatisation + Accès complet au disque) dans cette session utilisateur bot.

  </Accordion>

  <Accordion title="Mac distant via Tailscale (exemple)">
    Topologie courante :

    - la passerelle s'exécute sur Linux/VM
    - iMessage + `imsg` s'exécute sur un Mac dans votre tailnet
    - le wrapper `cliPath` utilise SSH pour exécuter `imsg`
    - `remoteHost` active les récupérations de pièces jointes SCP

    Exemple :

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "bot@mac-mini.tailnet-1234.ts.net",
      includeAttachments: true,
      dbPath: "/Users/bot/Library/Messages/chat.db",
    },
  },
}
```

```bash
#!/usr/bin/env bash
exec ssh -T bot@mac-mini.tailnet-1234.ts.net imsg "$@"
```

    Utilisez des clés SSH pour que SSH et SCP soient non-interactifs.
    Assurez-vous que la clé d'hôte est approuvée en premier (par exemple `ssh bot@mac-mini.tailnet-1234.ts.net`) pour que `known_hosts` soit rempli.

  </Accordion>

  <Accordion title="Modèle multi-compte">
    iMessage supporte la configuration par compte sous `channels.imessage.accounts`.

    Chaque compte peut remplacer des champs tels que `cliPath`, `dbPath`, `allowFrom`, `groupPolicy`, `mediaMaxMb`, les paramètres d'historique et les listes blanches de racines de pièces jointes.

  </Accordion>
</AccordionGroup>

## Médias, chunking et cibles de livraison

<AccordionGroup>
  <Accordion title="Pièces jointes et médias">
    - l'ingestion des pièces jointes entrantes est optionnelle : `channels.imessage.includeAttachments`
    - les chemins de pièces jointes distantes peuvent être récupérés via SCP quand `remoteHost` est défini
    - les chemins de pièces jointes doivent correspondre aux racines autorisées :
      - `channels.imessage.attachmentRoots` (local)
      - `channels.imessage.remoteAttachmentRoots` (mode SCP distant)
      - motif de racine par défaut : `/Users/*/Library/Messages/Attachments`
    - SCP utilise la vérification stricte des clés d'hôte (`StrictHostKeyChecking=yes`)
    - la taille des médias sortants utilise `channels.imessage.mediaMaxMb` (16 MB par défaut)
  </Accordion>

  <Accordion title="Chunking sortant">
    - limite de chunk de texte : `channels.imessage.textChunkLimit` (4000 par défaut)
    - mode chunk : `channels.imessage.chunkMode`
      - `length` (par défaut)
      - `newline` (division par paragraphe en premier)
  </Accordion>

  <Accordion title="Formats d'adressage">
    Cibles explicites préférées :

    - `chat_id:123` (recommandé pour le routage stable)
    - `chat_guid:...`
    - `chat_identifier:...`

    Les cibles de handle sont également supportées :

    - `imessage:+1555...`
    - `sms:+1555...`
    - `user@example.com`

```bash
imsg chats --limit 20
```

  </Accordion>
</AccordionGroup>

## Écritures de configuration

iMessage permet les écritures de configuration initiées par le canal par défaut (pour `/config set|unset` quand `commands.config: true`).

Désactiver :

```json5
{
  channels: {
    imessage: {
      configWrites: false,
    },
  },
}
```

## Dépannage

<AccordionGroup>
  <Accordion title="imsg introuvable ou RPC non supporté">
    Validez le binaire et le support RPC :

```bash
imsg rpc --help
openclaw channels status --probe
```

    Si la sonde signale RPC non supporté, mettez à jour `imsg`.

  </Accordion>

  <Accordion title="Les DM sont ignorés">
    Vérifiez :

    - `channels.imessage.dmPolicy`
    - `channels.imessage.allowFrom`
    - approbations d'appairage (`openclaw pairing list imessage`)

  </Accordion>

  <Accordion title="Les messages de groupe sont ignorés">
    Vérifiez :

    - `channels.imessage.groupPolicy`
    - `channels.imessage.groupAllowFrom`
    - comportement de liste blanche `channels.imessage.groups`
    - configuration du motif de mention (`agents.list[].groupChat.mentionPatterns`)

  </Accordion>

  <Accordion title="Les pièces jointes distantes échouent">
    Vérifiez :

    - `channels.imessage.remoteHost`
    - `channels.imessage.remoteAttachmentRoots`
    - authentification SSH/SCP depuis l'hôte de la passerelle
    - la clé d'hôte existe dans `~/.ssh/known_hosts` sur l'hôte de la passerelle
    - la lisibilité du chemin distant sur le Mac exécutant Messages

  </Accordion>

  <Accordion title="Les invites de permission macOS ont été manquées">
    Réexécutez dans un terminal GUI interactif dans le même contexte utilisateur/session et approuvez les invites :

```bash
imsg chats --limit 1
imsg send <handle> "test"
```

    Confirmez que l'accès complet au disque + l'automatisation sont accordés pour le contexte de processus qui exécute OpenClaw/`imsg`.

  </Accordion>
</AccordionGroup>

## Pointeurs de référence de configuration

- [Référence de configuration - iMessage](/gateway/configuration-reference#imessage)
- [Configuration de la passerelle](/gateway/configuration)
- [Appairage](/channels/pairing)
- [BlueBubbles](/channels/bluebubbles)
```
