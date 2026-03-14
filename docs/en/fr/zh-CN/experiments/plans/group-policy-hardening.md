---
read_when:
  - 查看历史 Telegram 允许列表更改
summary: Telegram 允许列表加固：前缀 + 空白规范化
title: Telegram 允许列表加固
x-i18n:
  generated_at: "2026-02-03T07:47:16Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a2eca5fcc85376948cfe1b6044f1a8bc69c7f0eb94d1ceafedc1e507ba544162
  source_path: experiments/plans/group-policy-hardening.md
  workflow: 15
---

# Renforcement de la liste d'autorisation Telegram

**Date** : 2026-01-05  
**Statut** : Terminé  
**PR** : #216

## Résumé

La liste d'autorisation Telegram accepte désormais les préfixes `telegram:` et `tg:` sans distinction de casse et tolère les espaces inutiles. Cela rend la vérification de la liste d'autorisation entrante cohérente avec la normalisation de l'envoi sortant.

## Modifications

- Les préfixes `telegram:` et `tg:` sont traités de manière équivalente (insensible à la casse).
- Les entrées de la liste d'autorisation sont supprimées ; les entrées vides sont ignorées.

## Exemples

Tous les formulaires suivants sont acceptés pour le même ID :

- `telegram:123456`
- `TG:123456`
- `tg:123456`

## Pourquoi c'est important

Copier/coller à partir de journaux ou d'ID de chat inclut généralement le préfixe et les espaces. La normalisation évite les faux négatifs lors de la décision de répondre dans les messages privés ou les groupes.

## Documentation connexe

- [Groupes de discussion](/channels/groups)
- [Fournisseur Telegram](/channels/telegram)
