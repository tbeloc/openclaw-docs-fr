---
summary: "Mode élevé et directives /elevated"
read_when:
  - Ajustement des paramètres par défaut du mode élevé, des listes blanches ou du comportement des commandes slash
title: "Mode Élevé"
---

# Mode Élevé (directives /elevated)

## Ce qu'il fait

- `/elevated on` s'exécute sur l'hôte de passerelle et conserve les approbations exec (identique à `/elevated ask`).
- `/elevated full` s'exécute sur l'hôte de passerelle **et** approuve automatiquement exec (ignore les approbations exec).
- `/elevated ask` s'exécute sur l'hôte de passerelle mais conserve les approbations exec (identique à `/elevated on`).
- `on`/`ask` ne forcent **pas** `exec.security=full` ; la politique de sécurité/demande configurée s'applique toujours.
- Ne change le comportement que lorsque l'agent est **en sandbox** (sinon exec s'exécute déjà sur l'hôte).
- Formes de directive : `/elevated on|off|ask|full`, `/elev on|off|ask|full`.
- Seuls `on|off|ask|full` sont acceptés ; tout autre chose retourne un indice et ne change pas l'état.

## Ce qu'il contrôle (et ce qu'il ne contrôle pas)

- **Portes de disponibilité** : `tools.elevated` est la ligne de base mondiale. `agents.list[].tools.elevated` peut restreindre davantage le mode élevé par agent (les deux doivent l'autoriser).
- **État par session** : `/elevated on|off|ask|full` définit le niveau élevé pour la clé de session actuelle.
- **Directive en ligne** : `/elevated on|ask|full` à l'intérieur d'un message s'applique uniquement à ce message.
- **Groupes** : Dans les chats de groupe, les directives élevées ne sont honorées que lorsque l'agent est mentionné. Les messages de commande uniquement qui contournent les exigences de mention sont traités comme mentionnés.
- **Exécution sur l'hôte** : elevated force `exec` sur l'hôte de passerelle ; `full` définit également `security=full`.
- **Approbations** : `full` ignore les approbations exec ; `on`/`ask` les honorent lorsque les règles de liste blanche/demande l'exigent.
- **Agents non sandboxés** : sans effet sur la localisation ; affecte uniquement le contrôle d'accès, la journalisation et le statut.
- **La politique d'outil s'applique toujours** : si `exec` est refusé par la politique d'outil, elevated ne peut pas être utilisé.
- **Séparé de `/exec`** : `/exec` ajuste les paramètres par défaut par session pour les expéditeurs autorisés et ne nécessite pas elevated.

## Ordre de résolution

1. Directive en ligne sur le message (s'applique uniquement à ce message).
2. Remplacement de session (défini en envoyant un message contenant uniquement la directive).
3. Paramètre par défaut mondial (`agents.defaults.elevatedDefault` dans la configuration).

## Définir un paramètre par défaut de session

- Envoyez un message qui est **uniquement** la directive (espaces blancs autorisés), par ex. `/elevated full`.
- Une réponse de confirmation est envoyée (`Elevated mode set to full...` / `Elevated mode disabled.`).
- Si l'accès élevé est désactivé ou l'expéditeur n'est pas sur la liste blanche approuvée, la directive répond avec une erreur exploitable et ne change pas l'état de la session.
- Envoyez `/elevated` (ou `/elevated:`) sans argument pour voir le niveau élevé actuel.

## Disponibilité + listes blanches

- Porte de fonctionnalité : `tools.elevated.enabled` (la valeur par défaut peut être désactivée via la configuration même si le code la supporte).
- Liste blanche d'expéditeurs : `tools.elevated.allowFrom` avec des listes blanches par fournisseur (par ex. `discord`, `whatsapp`).
- Les entrées de liste blanche sans préfixe correspondent uniquement aux valeurs d'identité délimitées par l'expéditeur (`SenderId`, `SenderE164`, `From`) ; les champs de routage des destinataires ne sont jamais utilisés pour l'autorisation élevée.
- Les métadonnées d'expéditeur mutables nécessitent des préfixes explicites :
  - `name:<value>` correspond à `SenderName`
  - `username:<value>` correspond à `SenderUsername`
  - `tag:<value>` correspond à `SenderTag`
  - `id:<value>`, `from:<value>`, `e164:<value>` sont disponibles pour le ciblage d'identité explicite
- Porte par agent : `agents.list[].tools.elevated.enabled` (optionnel ; peut uniquement restreindre davantage).
- Liste blanche par agent : `agents.list[].tools.elevated.allowFrom` (optionnel ; lorsqu'elle est définie, l'expéditeur doit correspondre aux listes blanches globales **et** par agent).
- Secours Discord : si `tools.elevated.allowFrom.discord` est omis, la liste `channels.discord.allowFrom` est utilisée comme secours (héritage : `channels.discord.dm.allowFrom`). Définissez `tools.elevated.allowFrom.discord` (même `[]`) pour remplacer. Les listes blanches par agent n'utilisent **pas** le secours.
- Toutes les portes doivent passer ; sinon elevated est traité comme indisponible.

## Journalisation + statut

- Les appels exec élevés sont journalisés au niveau info.
- Le statut de session inclut le mode élevé (par ex. `elevated=ask`, `elevated=full`).
