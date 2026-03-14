---
read_when:
  - 更改群组消息规则或提及设置时
summary: WhatsApp 群組訊息處理的行為和配置（mentionPatterns 在各平台間共享）
title: 群組消息
x-i18n:
  generated_at: "2026-02-03T10:05:00Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 181a72f12f5021af77c2e4c913120f711e0c0bc271d218d75cb6fe80dab675bb
  source_path: channels/group-messages.md
  workflow: 15
---

# Messages de groupe (canal WhatsApp Web)

Objectif : Garder Clawd dans les groupes WhatsApp, l'activer uniquement lorsqu'il est mentionné, et séparer ce fil de conversation de la session de messages privés personnels.

Remarque : `agents.list[].groupChat.mentionPatterns` est maintenant également utilisé par Telegram/Discord/Slack/iMessage ; cette documentation se concentre sur le comportement spécifique à WhatsApp. Pour les configurations multi-agents, définissez `agents.list[].groupChat.mentionPatterns` pour chaque agent (ou utilisez `messages.groupChat.mentionPatterns` comme secours global).

## Fonctionnalités implémentées (2025-12-03)

- Mode d'activation : `mention` (par défaut) ou `always`. `mention` nécessite d'être mentionné (via une véritable mention WhatsApp @ dans `mentionedJids`, des motifs d'expression régulière, ou le numéro E.164 du bot n'importe où dans le texte). `always` active l'agent à chaque message, mais il ne devrait répondre que s'il peut fournir une valeur significative ; sinon, retourner le jeton silencieux `NO_REPLY`. La valeur par défaut peut être définie dans la configuration (`channels.whatsapp.groups`) et peut être remplacée par groupe via `/activation`. Lorsque `channels.whatsapp.groups` est défini, il agit également comme liste blanche de groupes (contient `"*"` pour autoriser tous les groupes).
- Politique de groupe : `channels.whatsapp.groupPolicy` contrôle l'acceptation des messages de groupe (`open|disabled|allowlist`). `allowlist` utilise `channels.whatsapp.groupAllowFrom` (secours : `channels.whatsapp.allowFrom` explicite). Par défaut `allowlist` (bloqué jusqu'à ce que vous ajoutiez l'expéditeur).
- Sessions de groupe indépendantes : le format de clé de session est `agent:<agentId>:whatsapp:group:<jid>`, donc les commandes comme `/verbose on` ou `/think high` (envoyées comme message distinct) ne s'appliquent qu'à ce groupe ; l'état des messages privés n'est pas affecté. Les fils de groupe ignorent les battements de cœur.
- Injection de contexte : **uniquement les messages de groupe en attente** (50 par défaut), c'est-à-dire ceux qui n'ont *pas* déclenché une exécution, sont injectés avec le préfixe `[Chat messages since your last reply - for context]`, le message déclencheur étant sous `[Current message - respond to this]`. Les messages déjà dans la session ne sont pas réinjectés.
- Affichage de l'expéditeur : chaque lot de groupe se termine maintenant par `[from: Sender Name (+E164)]`, permettant à Pi de savoir qui parle.
- Messages éphémères/à affichage unique : nous dépaquettons ces messages avant d'extraire le texte/les mentions, donc les mentions qu'ils contiennent déclenchent toujours.
- Invite système de groupe : au premier tour de la session de groupe (et chaque fois que `/activation` change de mode), nous injectons une brève description dans l'invite système, comme `You are replying inside the WhatsApp group "<subject>". Group members: Alice (+44...), Bob (+43...), … Activation: trigger-only … Address the specific sender noted in the message context.` Si les métadonnées ne sont pas disponibles, nous informons toujours l'agent qu'il s'agit d'une conversation de groupe.

## Exemple de configuration (WhatsApp)

Ajoutez un bloc `groupChat` dans `~/.openclaw/openclaw.json` pour que les mentions de noms d'affichage fonctionnent correctement lorsque WhatsApp supprime le `@` visuel du corps du texte :

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

- Les expressions régulières ne sont pas sensibles à la casse ; elles couvrent les mentions de noms d'affichage comme `@openclaw`, ainsi que les numéros bruts avec ou sans `+`/espaces.
- Lorsque quelqu'un clique sur un contact, WhatsApp envoie toujours une mention canonique via `mentionedJids`, donc le secours numérique est rarement nécessaire, mais utile comme filet de sécurité.

### Commandes d'activation (propriétaire uniquement)

Utilisez les commandes de chat de groupe :

- `/activation mention`
- `/activation always`

Seul le numéro du propriétaire (de `channels.whatsapp.allowFrom`, ou le E.164 du bot lui-même si non défini) peut modifier ce paramètre. Envoyez `/status` comme message distinct dans le groupe pour voir le mode d'activation actuel.

## Mode d'emploi

1. Ajoutez votre compte WhatsApp (celui exécutant OpenClaw) au groupe.
2. Dites `@openclaw …` (ou incluez le numéro). Seuls les expéditeurs de la liste blanche peuvent déclencher, sauf si vous définissez `groupPolicy: "open"`.
3. L'invite de l'agent inclura le contexte de groupe récent plus une balise `[from: …]` à la fin, afin qu'il puisse répondre à la bonne personne.
4. Les instructions au niveau de la session (`/verbose on`, `/think high`, `/new` ou `/reset`, `/compact`) ne s'appliquent qu'à la session de ce groupe ; envoyez-les comme messages distincts pour qu'elles prennent effet. Votre session de messages privés reste indépendante.

## Test/Vérification

- Test de fumée manuel :
  - Envoyez une mention `@openclaw` dans le groupe, confirmez la réception d'une réponse citant le nom de l'expéditeur.
  - Envoyez une deuxième mention, vérifiez que le bloc d'historique est inclus, puis effacé au tour suivant.
- Vérifiez les journaux de la passerelle (exécutez avec `--verbose`) pour les entrées `inbound web message` montrant `from: <groupJid>` et le suffixe `[from: …]`.

## Problèmes connus

- Les groupes ignorent intentionnellement les battements de cœur pour éviter les diffusions bruyantes.
- La suppression d'écho utilise la chaîne de lot combinée ; si vous envoyez deux fois le même texte sans mention, seule la première recevra une réponse.
- Les entrées de stockage de session apparaîtront comme `agent:<agentId>:whatsapp:group:<jid>` dans le stockage de session (par défaut `~/.openclaw/agents/<agentId>/sessions/sessions.json`) ; une entrée manquante signifie simplement que ce groupe n'a pas encore déclenché d'exécution.
- Les indicateurs de saisie dans les groupes suivent `agents.defaults.typingMode` (par défaut : `message` lorsqu'il n'est pas mentionné).
