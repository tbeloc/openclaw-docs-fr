---
read_when:
  - Vous souhaitez réduire la croissance du contexte LLM causée par la sortie des outils
  - Vous ajustez agents.defaults.contextPruning
summary: Élagage de session : élagage des résultats d'outils pour réduire l'expansion du contexte
x-i18n:
  generated_at: "2026-02-03T07:46:35Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 9b0aa2d1abea7050ba848a2db038ccc3e6e2d83c6eb4e3843a2ead0ab847574a
  source_path: concepts/session-pruning.md
  workflow: 15
---

# Élagage de session

L'élagage de session élague les **anciens résultats d'outils** du contexte en mémoire avant chaque appel LLM. Il **ne réécrit pas** l'historique de session sur le disque (`*.jsonl`).

## Moment d'exécution

- Lorsque `mode: "cache-ttl"` est activé et que le dernier appel Anthropic pour cette session est antérieur à `ttl`.
- Affecte uniquement les messages envoyés au modèle pour cette requête.
- Fonctionne uniquement pour les appels API Anthropic (et les modèles Anthropic OpenRouter).
- Pour de meilleurs résultats, faites correspondre `ttl` avec le `cacheControlTtl` de votre modèle.
- Après l'élagage, la fenêtre TTL est réinitialisée, donc les requêtes suivantes conservent le cache jusqu'à ce que `ttl` expire à nouveau.

## Valeurs par défaut intelligentes (Anthropic)

- **Profils OAuth ou setup-token** : activez l'élagage `cache-ttl` et définissez le heartbeat sur `1h`.
- **Profils de clé API** : activez l'élagage `cache-ttl`, définissez le heartbeat sur `30m`, et définissez par défaut `cacheControlTtl` à `1h` pour les modèles Anthropic.
- Si vous avez explicitement défini l'une de ces valeurs, OpenClaw **ne les remplacera pas**.

## Améliorations (coût + comportement du cache)

- **Pourquoi élaguer :** Le cache de prompt Anthropic ne s'applique que dans la fenêtre TTL. Si une session est inactive au-delà du TTL, la requête suivante recache le prompt complet, sauf si vous l'élaguez d'abord.
- **Ce qui devient moins cher :** L'élagage réduit la taille **cacheWrite** de la première requête après l'expiration du TTL.
- **Pourquoi la réinitialisation du TTL est importante :** Une fois l'élagage exécuté, la fenêtre de cache est réinitialisée, donc les requêtes suivantes peuvent réutiliser le nouveau prompt en cache au lieu de recacher l'historique complet.
- **Ce qu'il ne fait pas :** L'élagage n'ajoute pas de tokens ou ne "double" pas les coûts ; il change simplement ce qui est mis en cache dans la première requête après ce TTL.

## Ce qui peut être élagué

- Uniquement les messages `toolResult`.
- Les messages utilisateur + assistant **ne sont jamais** modifiés.
- Les `keepLastAssistants` derniers messages d'assistant sont protégés ; les résultats d'outils après ce point de coupure ne sont pas élaguées.
- Si pas assez de messages d'assistant pour déterminer le point de coupure, l'élagage est ignoré.
- Les résultats d'outils contenant des **blocs d'image** sont ignorés (jamais élaguées/effacées).

## Estimation de la fenêtre de contexte

L'élagage utilise une fenêtre de contexte estimée (caractères ≈ tokens × 4). La fenêtre de base est résolue dans cet ordre :

1. Remplacement `models.providers.*.models[].contextWindow`.
2. `contextWindow` de définition de modèle (du registre de modèles).
3. Défaut `200000` tokens.

Si `agents.defaults.contextTokens` est défini, il sera traité comme une limite supérieure (minimum) pour la fenêtre résolue.

## Modes

### cache-ttl

- Exécute l'élagage uniquement si le dernier appel Anthropic est antérieur à `ttl` (par défaut `5m`).
- À l'exécution : même comportement d'élagage logiciel + effacement dur qu'avant.

## Élagage logiciel vs effacement dur

- **Élagage logiciel** : uniquement pour les résultats d'outils trop volumineux.
  - Conserve la tête + la queue, insère `...`, et ajoute un commentaire avec la taille d'origine.
  - Ignore les résultats contenant des blocs d'image.
- **Effacement dur** : remplace le résultat d'outil entier par `hardClear.placeholder`.

## Sélection d'outils

- `tools.allow` / `tools.deny` supportent le wildcard `*`.
- La négation a priorité.
- La correspondance est insensible à la casse.
- Liste d'autorisation vide => tous les outils sont autorisés.

## Interaction avec d'autres limites

- Les outils intégrés tronquent déjà leur propre sortie ; l'élagage de session est une couche supplémentaire qui empêche les chats de longue durée d'accumuler trop de sortie d'outils dans le contexte du modèle.
- La compaction est indépendante : la compaction résume et persiste, l'élagage est une opération temporaire par requête. Voir [/concepts/compaction](/concepts/compaction).

## Valeurs par défaut (lorsqu'activé)

- `ttl` : `"5m"`
- `keepLastAssistants` : `3`
- `softTrimRatio` : `0.3`
- `hardClearRatio` : `0.5`
- `minPrunableToolChars` : `50000`
- `softTrim` : `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }`
- `hardClear` : `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

## Exemples

Par défaut (désactivé) :

```json5
{
  agent: {
    contextPruning: { mode: "off" },
  },
}
```

Activer l'élagage sensible au TTL :

```json5
{
  agent: {
    contextPruning: { mode: "cache-ttl", ttl: "5m" },
  },
}
```

Limiter l'élagage à des outils spécifiques :

```json5
{
  agent: {
    contextPruning: {
      mode: "cache-ttl",
      tools: { allow: ["exec", "read"], deny: ["*image*"] },
    },
  },
}
```

Voir la référence de configuration : [Configuration de la passerelle](/gateway/configuration)
