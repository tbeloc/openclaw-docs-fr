---
summary: "Comment OpenClaw construit le contexte des invites et rapporte l'utilisation des tokens + les coûts"
read_when:
  - Explaining token usage, costs, or context windows
  - Debugging context growth or compaction behavior
title: "Utilisation des tokens et coûts"
---

# Utilisation des tokens et coûts

OpenClaw suit les **tokens**, pas les caractères. Les tokens sont spécifiques au modèle, mais la plupart des modèles de style OpenAI font en moyenne ~4 caractères par token pour le texte anglais.

## Comment l'invite système est construite

OpenClaw assemble sa propre invite système à chaque exécution. Elle inclut :

- Liste des outils + descriptions courtes
- Liste des compétences (métadonnées uniquement ; les instructions sont chargées à la demande avec `read`)
- Instructions d'auto-mise à jour
- Fichiers d'espace de travail + bootstrap (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` quand nouveaux, plus `MEMORY.md` quand présents ou `memory.md` comme alternative en minuscules). Les fichiers volumineux sont tronqués par `agents.defaults.bootstrapMaxChars` (par défaut : 20000), et l'injection bootstrap totale est limitée par `agents.defaults.bootstrapTotalMaxChars` (par défaut : 150000). Les fichiers `memory/*.md` sont à la demande via les outils de mémoire et ne sont pas auto-injectés.
- Heure (UTC + fuseau horaire de l'utilisateur)
- Balises de réponse + comportement de battement cardiaque
- Métadonnées d'exécution (hôte/OS/modèle/réflexion)

Voir la ventilation complète dans [Invite système](/fr/concepts/system-prompt).

## Ce qui compte dans la fenêtre de contexte

Tout ce que le modèle reçoit compte vers la limite de contexte :

- Invite système (toutes les sections listées ci-dessus)
- Historique de conversation (messages utilisateur + assistant)
- Appels d'outils et résultats d'outils
- Pièces jointes/transcriptions (images, audio, fichiers)
- Résumés de compaction et artefacts d'élagage
- Wrappers de fournisseur ou en-têtes de sécurité (non visibles, mais toujours comptés)

Pour les images, OpenClaw réduit les charges utiles d'image de transcription/outil avant les appels de fournisseur.
Utilisez `agents.defaults.imageMaxDimensionPx` (par défaut : `1200`) pour ajuster ceci :

- Les valeurs plus basses réduisent généralement l'utilisation des tokens de vision et la taille de la charge utile.
- Les valeurs plus élevées préservent plus de détails visuels pour les captures d'écran OCR/UI-lourdes.

Pour une ventilation pratique (par fichier injecté, outils, compétences et taille d'invite système), utilisez `/context list` ou `/context detail`. Voir [Contexte](/fr/concepts/context).

## Comment voir l'utilisation actuelle des tokens

Utilisez ceux-ci dans le chat :

- `/status` → **carte de statut riche en emoji** avec le modèle de session, l'utilisation du contexte,
  les tokens d'entrée/sortie de la dernière réponse, et le **coût estimé** (clé API uniquement).
- `/usage off|tokens|full` → ajoute un **pied de page d'utilisation par réponse** à chaque réponse.
  - Persiste par session (stocké comme `responseUsage`).
  - L'authentification OAuth **masque le coût** (tokens uniquement).
- `/usage cost` → affiche un résumé de coût local à partir des journaux de session OpenClaw.

Autres surfaces :

- **TUI/Web TUI :** `/status` + `/usage` sont supportés.
- **CLI :** `openclaw status --usage` et `openclaw channels list` affichent
  les fenêtres de quota du fournisseur (pas les coûts par réponse).

## Estimation des coûts (quand affichée)

Les coûts sont estimés à partir de votre configuration de tarification du modèle :

```
models.providers.<provider>.models[].cost
```

Ce sont des **USD par 1M tokens** pour `input`, `output`, `cacheRead` et
`cacheWrite`. Si la tarification est manquante, OpenClaw affiche les tokens uniquement. Les tokens OAuth ne montrent jamais le coût en dollars.

## Impact de la TTL du cache et de l'élagage

La mise en cache des invites du fournisseur s'applique uniquement dans la fenêtre TTL du cache. OpenClaw peut éventuellement exécuter **l'élagage cache-ttl** : il élague la session une fois que la TTL du cache a expiré, puis réinitialise la fenêtre du cache afin que les demandes ultérieures puissent réutiliser le contexte fraîchement mis en cache au lieu de re-mettre en cache l'historique complet. Cela maintient les coûts d'écriture du cache plus bas quand une session devient inactive au-delà de la TTL.

Configurez-le dans [Configuration de la passerelle](/fr/gateway/configuration) et consultez les détails du comportement dans [Élagage de session](/fr/concepts/session-pruning).

Le battement cardiaque peut garder le cache **chaud** sur les lacunes d'inactivité. Si votre TTL du cache de modèle est `1h`, définir l'intervalle de battement cardiaque juste en dessous (par exemple, `55m`) peut éviter la re-mise en cache de l'invite complète, réduisant les coûts d'écriture du cache.

Dans les configurations multi-agents, vous pouvez conserver une configuration de modèle partagée et ajuster le comportement du cache par agent avec `agents.list[].params.cacheRetention`.

Pour un guide complet knob-by-knob, voir [Mise en cache des invites](/fr/reference/prompt-caching).

Pour la tarification de l'API Anthropic, les lectures du cache sont considérablement moins chères que les tokens d'entrée, tandis que les écritures du cache sont facturées à un multiplicateur plus élevé. Consultez la tarification de la mise en cache des invites d'Anthropic pour les tarifs les plus récents et les multiplicateurs TTL :
[https://docs.anthropic.com/docs/build-with-claude/prompt-caching](https://docs.anthropic.com/docs/build-with-claude/prompt-caching)

### Exemple : garder le cache 1h chaud avec battement cardiaque

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
    heartbeat:
      every: "55m"
```

### Exemple : trafic mixte avec stratégie de cache par agent

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long" # baseline par défaut pour la plupart des agents
  list:
    - id: "research"
      default: true
      heartbeat:
        every: "55m" # garder le cache long chaud pour les sessions approfondies
    - id: "alerts"
      params:
        cacheRetention: "none" # éviter les écritures du cache pour les notifications en rafales
```

`agents.list[].params` fusionne au-dessus des `params` du modèle sélectionné, vous pouvez donc
remplacer uniquement `cacheRetention` et hériter des autres valeurs par défaut du modèle inchangées.

### Exemple : activer l'en-tête bêta du contexte 1M d'Anthropic

La fenêtre de contexte 1M d'Anthropic est actuellement en bêta fermée. OpenClaw peut injecter la
valeur `anthropic-beta` requise quand vous activez `context1m` sur les modèles Opus
ou Sonnet supportés.

```yaml
agents:
  defaults:
    models:
      "anthropic/claude-opus-4-6":
        params:
          context1m: true
```

Cela correspond à l'en-tête bêta `context-1m-2025-08-07` d'Anthropic.

Cela s'applique uniquement quand `context1m: true` est défini sur cette entrée de modèle.

Exigence : les identifiants doivent être éligibles pour l'utilisation du contexte long (facturation par clé API,
ou abonnement avec utilisation supplémentaire activée). Sinon, Anthropic répond avec
`HTTP 429: rate_limit_error: Extra usage is required for long context requests`.

Si vous authentifiez Anthropic avec des tokens OAuth/abonnement (`sk-ant-oat-*`),
OpenClaw ignore l'en-tête bêta `context-1m-*` car Anthropic rejette actuellement
cette combinaison avec HTTP 401.

## Conseils pour réduire la pression des tokens

- Utilisez `/compact` pour résumer les sessions longues.
- Réduisez les grandes sorties d'outils dans vos flux de travail.
- Abaissez `agents.defaults.imageMaxDimensionPx` pour les sessions lourdes en captures d'écran.
- Gardez les descriptions de compétences courtes (la liste des compétences est injectée dans l'invite).
- Préférez les modèles plus petits pour le travail verbeux et exploratoire.

Voir [Compétences](/fr/tools/skills) pour la formule exacte de surcharge de liste de compétences.
