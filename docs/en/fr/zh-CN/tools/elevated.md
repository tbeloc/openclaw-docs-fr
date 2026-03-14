---
read_when:
  - 调整提升模式默认值、允许列表或斜杠命令行为
summary: 提升的 exec 模式和 /elevated 指令
title: Mode élevé
x-i18n:
  generated_at: "2026-02-03T07:55:23Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 83767a01609304026d145feb0aa0b0533e8cf8b16cd200f724d9e3e8cf2920c3
  source_path: tools/elevated.md
  workflow: 15
---

# Mode élevé (directive `/elevated`)

## Description des fonctionnalités

- `/elevated on` s'exécute sur l'hôte Gateway et conserve l'approbation exec (identique à `/elevated ask`).
- `/elevated full` s'exécute sur l'hôte Gateway **et** approuve automatiquement exec (ignore l'approbation exec).
- `/elevated ask` s'exécute sur l'hôte Gateway mais conserve l'approbation exec (identique à `/elevated on`).
- `on`/`ask` **ne force pas** `exec.security=full` ; la politique de sécurité/demande configurée s'applique toujours.
- Modifie le comportement uniquement si l'agent est **en sandbox** (sinon exec s'exécute déjà sur l'hôte).
- Formes de directive : `/ elevated on|off|ask|full`, `/elev on|off|ask|full`.
- Accepte uniquement `on|off|ask|full` ; tout autre contenu retourne une invite et ne change pas l'état.

## Ce qu'il contrôle (et ce qu'il ne contrôle pas)

- **Contrôle d'accès** : `tools.elevated` est la ligne de base mondiale. `agents.list[].tools.elevated` peut restreindre davantage l'élévation par agent (les deux doivent autoriser).
- **État par session** : `/elevated on|off|ask|full` définit le niveau d'élévation pour la clé de session actuelle.
- **Directives en ligne** : `/elevated on|ask|full` dans un message s'applique uniquement à ce message.
- **Groupes** : dans les chats de groupe, les directives d'élévation ne sont respectées que si l'agent est mentionné. Les messages de commande pure qui contournent l'exigence de mention sont traités comme mentionnés.
- **Exécution sur l'hôte** : elevated force `exec` vers l'hôte Gateway ; `full` définit également `security=full`.
- **Approbation** : `full` ignore l'approbation exec ; `on`/`ask` respectent l'approbation si les règles de liste blanche/demande l'exigent.
- **Agents non en sandbox** : n'affecte pas l'emplacement ; affecte uniquement le contrôle d'accès, la journalisation et l'état.
- **Les politiques d'outils s'appliquent toujours** : si `exec` est rejeté par une politique d'outils, elevated ne peut pas être utilisé.
- **Séparé de `/exec`** : `/exec` ajuste les valeurs par défaut par session pour les expéditeurs autorisés, ne nécessite pas elevated.

## Ordre de résolution

1. Directives en ligne sur le message (s'appliquent uniquement à ce message).
2. Remplacement de session (défini en envoyant un message contenant uniquement la directive).
3. Valeurs par défaut globales (`agents.defaults.elevatedDefault` dans la configuration).

## Définir les valeurs par défaut de session

- Envoyez un message contenant **uniquement** la directive (les espaces blancs sont autorisés), par exemple `/elevated full`.
- Envoyez une réponse de confirmation (`Elevated mode set to full...` / `Elevated mode disabled.`).
- Si l'accès elevated est désactivé ou si l'expéditeur ne figure pas dans la liste blanche d'approbation, la directive répond avec une erreur exploitable et ne change pas l'état de la session.
- Envoyez `/elevated` sans paramètres (ou `/elevated:`) pour voir le niveau d'élévation actuel.

## Disponibilité + Liste blanche

- Contrôle de fonctionnalité : `tools.elevated.enabled` (peut être désactivé par défaut via la configuration même si le code le supporte).
- Liste blanche d'expéditeurs : `tools.elevated.allowFrom`, avec des listes blanches par fournisseur (par exemple `discord`, `whatsapp`).
- Contrôle par agent : `agents.list[].tools.elevated.enabled` (optionnel ; peut uniquement restreindre davantage).
- Liste blanche par agent : `agents.list[].tools.elevated.allowFrom` (optionnel ; lorsqu'elle est définie, l'expéditeur doit correspondre à la fois à la liste blanche globale + par agent).
- Secours Discord : si `tools.elevated.allowFrom.discord` est omis, la liste `channels.discord.dm.allowFrom` est utilisée comme secours. Définissez `tools.elevated.allowFrom.discord` (même si c'est `[]`) pour remplacer. La liste blanche par agent **n'utilise pas** de secours.
- Tous les contrôles d'accès doivent réussir ; sinon, elevated est considéré comme indisponible.

## Journalisation + État

- Les appels exec élevés sont enregistrés au niveau info.
- L'état de session inclut le mode élevé (par exemple `elevated=ask`, `elevated=full`).
