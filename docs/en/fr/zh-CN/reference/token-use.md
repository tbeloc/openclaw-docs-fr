---
read_when:
  - 解释 token 使用量、成本或上下文窗口时
  - 调试上下文增长或压缩行为时
summary: OpenClaw 如何构建提示上下文并报告 token 使用量 + 成本
title: Token 使用与成本
x-i18n:
  generated_at: "2026-02-03T07:54:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: aee417119851db9e36890487517ed9602d214849e412127e7f534ebec5c9e105
  source_path: reference/token-use.md
  workflow: 15
---

# Utilisation des tokens et coûts

OpenClaw suit les **tokens**, et non les caractères. Les tokens sont spécifiques au modèle, mais la plupart
des modèles de style OpenAI représentent environ 4 caractères pour 1 token en texte anglais.

## Comment le système de prompt est construit

OpenClaw assemble son propre système de prompt à chaque exécution. Il comprend :

- Liste des outils + descriptions brèves
- Liste des Skills (métadonnées uniquement ; les instructions sont chargées à la demande via `read`)
- Instructions d'auto-mise à jour
- Fichiers d'espace de travail + guidage (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` (lors de la création)). Les fichiers volumineux sont tronqués par `agents.defaults.bootstrapMaxChars` (par défaut : 20000).
- Heure (UTC + fuseau horaire de l'utilisateur)
- Balises de réponse + comportement de heartbeat
- Métadonnées d'exécution (hôte/système d'exploitation/modèle/réflexion)

Pour une décomposition complète, voir [Système de prompt](/concepts/system-prompt).

## Ce qui compte dans la fenêtre de contexte

Tout ce que le modèle reçoit compte dans la limite de contexte :

- Système de prompt (toutes les parties listées ci-dessus)
- Historique de conversation (messages utilisateur + assistant)
- Appels d'outils et résultats d'outils
- Pièces jointes/transcriptions (images, audio, fichiers)
- Résumés compressés et artefacts d'élagage
- Encapsulation du fournisseur ou en-têtes de sécurité (invisibles, mais toujours comptabilisés)

Pour une décomposition réelle (taille de chaque fichier injecté, outil, Skill et système de prompt), utilisez `/context list` ou `/context detail`. Voir [Contexte](/concepts/context).

## Comment voir l'utilisation actuelle des tokens

Dans le chat, utilisez :

- `/status` → **Carte de statut riche en emoji** avec modèle de session, utilisation du contexte,
  tokens d'entrée/sortie de la dernière réponse et **coût estimé** (clé API uniquement).
- `/usage off|tokens|full` → Ajoute un **pied de page d'utilisation par réponse** après chaque réponse.
  - Persistant par session (stocké comme `responseUsage`).
  - L'authentification OAuth **masque les coûts** (tokens uniquement).
- `/usage cost` → Affiche un résumé des coûts locaux à partir des journaux de session OpenClaw.

Autres interfaces :

- **TUI/Web TUI :** Support pour `/status` + `/usage`.
- **CLI :** `openclaw status --usage` et `openclaw channels list` affichent
  la fenêtre de quota du fournisseur (pas le coût par réponse).

## Estimation des coûts (quand affichée)

Les coûts sont estimés à partir de votre configuration de tarification du modèle :

```
models.providers.<provider>.models[].cost
```

Ce sont les **dollars par 1M tokens** pour `input`, `output`, `cacheRead` et
`cacheWrite`. Si la tarification est manquante, OpenClaw affiche uniquement les tokens. Les tokens OAuth
n'affichent jamais les coûts en dollars.

## Impact du TTL du cache et de l'élagage

Le cache de prompt du fournisseur ne s'applique que dans la fenêtre TTL du cache. OpenClaw peut
exécuter sélectivement un **élagage TTL du cache** : il élague la session après l'expiration du TTL du cache,
puis réinitialise la fenêtre du cache afin que les demandes ultérieures puissent réutiliser
le contexte nouvellement mis en cache au lieu de remettre en cache l'historique complet. Cela peut
réduire les coûts d'écriture du cache lorsque la session est inactive au-delà du TTL.

Configurez-le dans [Configuration de la passerelle](/gateway/configuration) et consultez les détails du comportement dans
[Élagage de session](/concepts/session-pruning).

Le heartbeat peut garder le cache **chaud** pendant les intervalles d'inactivité. Si votre TTL du cache de modèle
est `1h`, définir l'intervalle de heartbeat légèrement en dessous (par exemple `55m`) peut éviter
la remise en cache du prompt complet, réduisant ainsi les coûts d'écriture du cache.

Pour la tarification de l'API Anthropic, les lectures du cache sont beaucoup moins chères que les tokens d'entrée,
tandis que les écritures du cache sont facturées à un taux plus élevé. Consultez la tarification du cache de prompt d'Anthropic pour les tarifs et multiplicateurs TTL les plus récents :
https://docs.anthropic.com/docs/build-with-claude/prompt-caching

### Exemple : garder un cache de 1 heure chaud avec heartbeat

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-5"
    models:
      "anthropic/claude-opus-4-5":
        params:
          cacheRetention: "long"
    heartbeat:
      every: "55m"
```

## Conseils pour réduire la pression des tokens

- Utilisez `/compact` pour résumer les longues sessions.
- Élaguez les grandes sorties d'outils dans votre flux de travail.
- Gardez les descriptions des Skills courtes (la liste des Skills est injectée dans le prompt).
- Pour les travaux exploratoires longs, privilégiez les modèles plus petits.

Pour la formule exacte de surcharge de la liste des Skills, voir [Skills](/tools/skills).
