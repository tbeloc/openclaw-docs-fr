---
summary: "Comportement et configuration pour la gestion des messages de groupe WhatsApp (mentionPatterns sont partagés entre les surfaces)"
read_when:
  - Changing group message rules or mentions
title: "Messages de groupe"
---

# Messages de groupe (canal WhatsApp web)

Objectif : permettre à Clawd de rester dans les groupes WhatsApp, de se réveiller uniquement quand il est mentionné, et de garder ce fil de discussion séparé de la session DM personnelle.

Remarque : `agents.list[].groupChat.mentionPatterns` est maintenant utilisé par Telegram/Discord/Slack/iMessage également ; cette documentation se concentre sur le comportement spécifique à WhatsApp. Pour les configurations multi-agents, définissez `agents.list[].groupChat.mentionPatterns` par agent (ou utilisez `messages.groupChat.mentionPatterns` comme fallback global).

## Ce qui est implémenté (2025-12-03)

- Modes d'activation : `mention` (par défaut) ou `always`. `mention` nécessite une mention (vraies @-mentions WhatsApp via `mentionedJids`, motifs regex, ou le numéro E.164 du bot n'importe où dans le texte). `always` réveille l'agent à chaque message mais il ne devrait répondre que quand il peut ajouter une valeur significative ; sinon il retourne le token silencieux `NO_REPLY`. Les valeurs par défaut peuvent être définies dans la config (`channels.whatsapp.groups`) et remplacées par groupe via `/activation`. Quand `channels.whatsapp.groups` est défini, il agit aussi comme une liste blanche de groupes (incluez `"*"` pour autoriser tous).
- Politique de groupe : `channels.whatsapp.groupPolicy` contrôle si les messages de groupe sont acceptés (`open|disabled|allowlist`). `allowlist` utilise `channels.whatsapp.groupAllowFrom` (fallback : `channels.whatsapp.allowFrom` explicite). La valeur par défaut est `allowlist` (bloqué jusqu'à ce que vous ajoutiez des expéditeurs).
- Sessions par groupe : les clés de session ressemblent à `agent:<agentId>:whatsapp:group:<jid>` donc les commandes telles que `/verbose on` ou `/think high` (envoyées comme messages autonomes) sont limitées à ce groupe ; l'état DM personnel reste inchangé. Les battements de cœur sont ignorés pour les fils de groupe.
- Injection de contexte : messages de groupe **en attente uniquement** (50 par défaut) qui n'ont _pas_ déclenché une exécution sont préfixés sous `[Chat messages since your last reply - for context]`, avec la ligne déclenchante sous `[Current message - respond to this]`. Les messages déjà dans la session ne sont pas réinjectés.
- Surfaçage de l'expéditeur : chaque lot de groupe se termine maintenant par `[from: Sender Name (+E164)]` pour que Pi sache qui parle.
- Éphémère/vue une fois : nous les dépaquettons avant d'extraire le texte/mentions, donc les mentions à l'intérieur les déclenchent toujours.
- Invite système de groupe : au premier tour d'une session de groupe (et chaque fois que `/activation` change le mode) nous injectons un court texte dans l'invite système comme `You are replying inside the WhatsApp group "<subject>". Group members: Alice (+44...), Bob (+43...), … Activation: trigger-only … Address the specific sender noted in the message context.` Si les métadonnées ne sont pas disponibles, nous disons quand même à l'agent que c'est un chat de groupe.

## Exemple de configuration (WhatsApp)

Ajoutez un bloc `groupChat` à `~/.openclaw/openclaw.json` pour que les mentions par nom d'affichage fonctionnent même quand WhatsApp supprime le `@` visuel dans le corps du texte :

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          historyLimit: 50,
          mentionPatterns: ["@?openclaw", "\\+?15555550123"],
        },
      },
    ],
  },
}
```

Remarques :

- Les regex sont insensibles à la casse ; elles couvrent une mention par nom d'affichage comme `@openclaw` et le numéro brut avec ou sans `+`/espaces.
- WhatsApp envoie toujours les mentions canoniques via `mentionedJids` quand quelqu'un appuie sur le contact, donc le fallback numérique est rarement nécessaire mais c'est un filet de sécurité utile.

### Commande d'activation (propriétaire uniquement)

Utilisez la commande de chat de groupe :

- `/activation mention`
- `/activation always`

Seul le numéro propriétaire (de `channels.whatsapp.allowFrom`, ou le numéro E.164 du bot quand non défini) peut changer cela. Envoyez `/status` comme message autonome dans le groupe pour voir le mode d'activation actuel.

## Comment utiliser

1. Ajoutez votre compte WhatsApp (celui exécutant OpenClaw) au groupe.
2. Dites `@openclaw …` (ou incluez le numéro). Seuls les expéditeurs en liste blanche peuvent le déclencher sauf si vous définissez `groupPolicy: "open"`.
3. L'invite de l'agent inclura le contexte récent du groupe plus le marqueur `[from: …]` final pour qu'il puisse adresser la bonne personne.
4. Les directives au niveau de la session (`/verbose on`, `/think high`, `/new` ou `/reset`, `/compact`) s'appliquent uniquement à la session de ce groupe ; envoyez-les comme messages autonomes pour qu'ils s'enregistrent. Votre session DM personnelle reste indépendante.

## Test / vérification

- Fumée manuelle :
  - Envoyez une mention `@openclaw` dans le groupe et confirmez une réponse qui référence le nom de l'expéditeur.
  - Envoyez une deuxième mention et vérifiez que le bloc d'historique est inclus puis effacé au tour suivant.
- Vérifiez les journaux de passerelle (exécutez avec `--verbose`) pour voir les entrées `inbound web message` montrant `from: <groupJid>` et le suffixe `[from: …]`.

## Considérations connues

- Les battements de cœur sont intentionnellement ignorés pour les groupes pour éviter les diffusions bruyantes.
- La suppression d'écho utilise la chaîne de lot combinée ; si vous envoyez du texte identique deux fois sans mentions, seul le premier obtiendra une réponse.
- Les entrées du magasin de session apparaîtront comme `agent:<agentId>:whatsapp:group:<jid>` dans le magasin de session (`~/.openclaw/agents/<agentId>/sessions/sessions.json` par défaut) ; une entrée manquante signifie simplement que le groupe n'a pas encore déclenché une exécution.
- Les indicateurs de saisie dans les groupes suivent `agents.defaults.typingMode` (par défaut : `message` quand non mentionné).
