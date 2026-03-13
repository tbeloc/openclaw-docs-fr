```markdown
---
description: Track outbound session mirroring refactor notes, decisions, tests, and open items.
title: Refactorisation de la mise en miroir de session sortante (Issue #1520)
x-i18n:
  generated_at: "2026-02-03T07:53:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b88a72f36f7b6d8a71fde9d014c0a87e9a8b8b0d449b67119cf3b6f414fa2b81
  source_path: refactor/outbound-session-mirroring.md
  workflow: 15
---

# Refactorisation de la mise en miroir de session sortante (Issue #1520)

## Statut

- En cours.
- Le routage des canaux principaux + plugins a été mis à jour pour supporter la mise en miroir sortante.
- L'envoi par passerelle dérive maintenant la session cible lors de l'omission de sessionKey.

## Contexte

Les envois sortants sont mis en miroir vers la session d'agent *actuelle* (clé de session d'outil) plutôt que vers la session du canal cible. Le routage entrant utilise les clés de session canal/pair, donc les réponses sortantes se retrouvent dans la mauvaise session, et les cibles de premier contact manquent généralement d'entrée de session.

## Objectifs

- Mettre en miroir les messages sortants vers la clé de session du canal cible.
- Créer des entrées de session pour les envois sortants en cas d'absence.
- Maintenir l'alignement de la portée des fils/sujets avec la clé de session entrante.
- Couvrir les canaux principaux plus les extensions intégrées.

## Résumé de l'implémentation

- Nouveaux assistants de routage de session sortante :
  - `src/infra/outbound/outbound-session.ts`
  - `resolveOutboundSessionRoute` construit la sessionKey cible en utilisant `buildAgentSessionKey` (dmScope + identityLinks).
  - `ensureOutboundSessionEntry` écrit un `MsgContext` minimal via `recordSessionMetaFromInbound`.
- `runMessageAction` (envoi) dérive la sessionKey cible et la transmet à `executeSendAction` pour la mise en miroir.
- `message-tool` ne met plus en miroir directement ; il résout uniquement agentId à partir de la clé de session actuelle.
- Le chemin d'envoi des plugins utilise la sessionKey dérivée pour la mise en miroir via `appendAssistantMessageToSessionTranscript`.
- L'envoi par passerelle dérive la clé de session cible en cas d'absence (agent par défaut) et assure l'entrée de session.

## Gestion des fils/sujets

- Slack : replyTo/threadId -> `resolveThreadSessionKeys` (suffixe).
- Discord : threadId/replyTo -> `resolveThreadSessionKeys`, `useSuffix=false` pour correspondre à l'entrant (l'id du canal de fil est déjà une session à portée).
- Telegram : l'id du sujet est mappé à `chatId:topic:<id>` via `buildTelegramGroupPeerId`.

## Extensions couvertes

- Matrix, MS Teams, Mattermost, BlueBubbles, Nextcloud Talk, Zalo, Zalo Personal, Nostr, Tlon.
- Notes :
  - Les cibles Mattermost suppriment maintenant `@` du routage de clé de session de message privé.
  - Zalo Personal utilise le type de pair de message privé pour les cibles 1:1 (utilise le groupe uniquement si `group:` est présent).
  - Les cibles de groupe BlueBubbles suppriment le préfixe `chat_*` pour correspondre à la clé de session entrante.
  - La mise en miroir automatique des fils Slack correspond à l'id du canal sans tenir compte de la casse.
  - L'envoi par passerelle convertit la clé de session fournie en minuscules avant la mise en miroir.

## Décisions

- **Dérivation de session d'envoi par passerelle** : si `sessionKey` est fourni, l'utiliser. S'il est omis, dériver sessionKey à partir de la cible + agent par défaut et mettre en miroir là-bas.
- **Création d'entrée de session** : toujours utiliser `recordSessionMetaFromInbound`, avec Provider/From/To/ChatType/AccountId/Originating* alignés sur le format entrant.
- **Normalisation de cible** : le routage sortant utilise la cible analysée (après `resolveChannelTarget`) quand disponible.
- **Casse de clé de session** : normaliser les clés de session en minuscules lors de l'écriture et de la migration.

## Tests ajoutés/mis à jour

- `src/infra/outbound/outbound-session.test.ts`
  - Clés de session de fil Slack.
  - Clés de session de sujet Telegram.
  - dmScope identityLinks avec Discord.
- `src/agents/tools/message-tool.test.ts`
  - Dérivation d'agentId à partir de la clé de session (sans passer sessionKey).
- `src/gateway/server-methods/send.test.ts`
  - Dérivation de clé de session et création d'entrée de session en cas d'omission.

## Éléments en attente / Suivi ultérieur

- Le plugin d'appels vocaux utilise une clé de session personnalisée `voice:<phone>`. La mise en correspondance sortante n'est pas normalisée ici ; si message-tool doit supporter l'envoi d'appels vocaux, ajoutez un mappage explicite.
- Confirmez s'il existe des plugins externes utilisant des formats `From/To` non standard en dehors de l'ensemble intégré.

## Fichiers impliqués

- `src/infra/outbound/outbound-session.ts`
- `src/infra/outbound/outbound-send-service.ts`
- `src/infra/outbound/message-action-runner.ts`
- `src/agents/tools/message-tool.ts`
- `src/gateway/server-methods/send.ts`
- Tests :
  - `src/infra/outbound/outbound-session.test.ts`
  - `src/agents/tools/message-tool.test.ts`
  - `src/gateway/server-methods/send.test.ts`
```
