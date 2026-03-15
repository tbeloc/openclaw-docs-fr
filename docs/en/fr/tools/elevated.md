---
summary: "Mode exécution élevée et directives /elevated"
read_when:
  - Adjusting elevated mode defaults, allowlists, or slash command behavior
title: "Mode Exécution Élevée"
---

# Mode Exécution Élevée (directives /elevated)

## Ce qu'il fait

- `/elevated on` s'exécute sur l'hôte passerelle et conserve les approbations exec (identique à `/elevated ask`).
- `/elevated full` s'exécute sur l'hôte passerelle **et** approuve automatiquement exec (ignore les approbations exec).
- `/elevated ask` s'exécute sur l'hôte passerelle mais conserve les approbations exec (identique à `/elevated on`).
- `on`/`ask` ne forcent **pas** `exec.security=full` ; la politique de sécurité/demande configurée s'applique toujours.
- Ne change le comportement que lorsque l'agent est **en sandbox** (sinon exec s'exécute déjà sur l'hôte).
- Formes de directive : `/elevated on|off|ask|full`, `/elev on|off|ask|full`.
- Seuls `on|off|ask|full` sont acceptés ; tout autre chose retourne un indice et ne change pas l'état.

## Ce qu'il contrôle (et ce qu'il ne contrôle pas)

- **Portes de disponibilité** : `tools.elevated` est la ligne de base mondiale. `agents.list[].tools.elevated` peut restreindre davantage l'exécution élevée par agent (les deux doivent autoriser).
- **État par session** : `/elevated on|off|ask|full` définit le niveau d'exécution élevée pour la clé de session actuelle.
- **Directive en ligne** : `/elevated on|ask|full` à l'intérieur d'un message s'applique uniquement à ce message.
- **Groupes** : Dans les chats de groupe, les directives d'exécution élevée ne sont honorées que lorsque l'agent est mentionné. Les messages de commande uniquement qui contournent les exigences de mention sont traités comme mentionnés.
- **Exécution sur l'hôte** : l'exécution élevée force `exec` sur l'hôte passerelle ; `full` définit également `security=full`.
- **Approbations** : `full` ignore les approbations exec ; `on`/`ask` les honorent lorsque les règles d'allowlist/demande l'exigent.
- **Agents non sandboxés** : sans effet sur la localisation ; affecte uniquement le contrôle d'accès, la journalisation et le statut.
- **La politique d'outil s'applique toujours** : si `exec` est refusé par la politique d'outil, l'exécution élevée ne peut pas être utilisée.
- **Séparé de `/exec`** : `/exec` ajuste les valeurs par défaut par session pour les expéditeurs autorisés et ne nécessite pas l'exécution élevée.

## Ordre de résolution

1. Directive en ligne sur le message (s'applique uniquement à ce message).
2. Remplacement de session (défini en envoyant un message contenant uniquement la directive).
3. Valeur par défaut mondiale (`agents.defaults.elevatedDefault` dans la configuration).

## Définir une valeur par défaut de session

- Envoyez un message qui est **uniquement** la directive (espaces autorisés), par ex. `/elevated full`.
- Une réponse de confirmation est envoyée (`Elevated mode set to full...` / `Elevated mode disabled.`).
- Si l'accès à l'exécution élevée est désactivé ou si l'expéditeur ne figure pas sur la liste d'approbation autorisée, la directive répond avec une erreur exploitable et ne change pas l'état de la session.
- Envoyez `/elevated` (ou `/elevated:`) sans argument pour voir le niveau d'exécution élevée actuel.

## Disponibilité + allowlists

- Porte de fonctionnalité : `tools.elevated.enabled` (la valeur par défaut peut être désactivée via la configuration même si le code la supporte).
- Allowlist d'expéditeur : `tools.elevated.allowFrom` avec des allowlists par fournisseur (par ex. `discord`, `whatsapp`).
- Les entrées d'allowlist sans préfixe correspondent uniquement aux valeurs d'identité délimitées par l'expéditeur (`SenderId`, `SenderE164`, `From`) ; les champs de routage des destinataires ne sont jamais utilisés pour l'autorisation d'exécution élevée.
- Les métadonnées d'expéditeur mutables nécessitent des préfixes explicites :
  - `name:<value>` correspond à `SenderName`
  - `username:<value>` correspond à `SenderUsername`
  - `tag:<value>` correspond à `SenderTag`
  - `id:<value>`, `from:<value>`, `e164:<value>` sont disponibles pour le ciblage d'identité explicite
- Porte par agent : `agents.list[].tools.elevated.enabled` (optionnel ; peut uniquement restreindre davantage).
- Allowlist par agent : `agents.list[].tools.elevated.allowFrom` (optionnel ; lorsqu'elle est définie, l'expéditeur doit correspondre aux allowlists globales **et** par agent).
- Secours Discord : si `tools.elevated.allowFrom.discord` est omis, la liste `channels.discord.allowFrom` est utilisée comme secours (héritage : `channels.discord.dm.allowFrom`). Définissez `tools.elevated.allowFrom.discord` (même `[]`) pour remplacer. Les allowlists par agent n'utilisent **pas** le secours.
- Toutes les portes doivent être franchies ; sinon l'exécution élevée est traitée comme indisponible.

## Journalisation + statut

- Les appels exec d'exécution élevée sont journalisés au niveau info.
- Le statut de session inclut le mode d'exécution élevée (par ex. `elevated=ask`, `elevated=full`).
