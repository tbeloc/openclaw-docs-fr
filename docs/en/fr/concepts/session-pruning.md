---
title: "Élagage de session"
summary: "Élagage de session : réduction des résultats d'outils pour limiter l'encombrement du contexte"
read_when:
  - You want to reduce LLM context growth from tool outputs
  - You are tuning agents.defaults.contextPruning
---

# Élagage de session

L'élagage de session supprime les **anciens résultats d'outils** du contexte en mémoire juste avant chaque appel LLM. Il ne réécrit **pas** l'historique de session sur disque (`*.jsonl`).

## Quand il s'exécute

- Quand `mode: "cache-ttl"` est activé et que le dernier appel Anthropic pour la session est plus ancien que `ttl`.
- Affecte uniquement les messages envoyés au modèle pour cette requête.
- Actif uniquement pour les appels API Anthropic (et les modèles Anthropic OpenRouter).
- Pour de meilleurs résultats, alignez `ttl` sur votre politique `cacheRetention` du modèle (`short` = 5m, `long` = 1h).
- Après un élagage, la fenêtre TTL se réinitialise pour que les requêtes suivantes conservent le cache jusqu'à l'expiration de `ttl`.

## Valeurs par défaut intelligentes (Anthropic)

- **Profils OAuth ou setup-token** : activez l'élagage `cache-ttl` et définissez le heartbeat sur `1h`.
- **Profils de clé API** : activez l'élagage `cache-ttl`, définissez le heartbeat sur `30m`, et `cacheRetention: "short"` par défaut sur les modèles Anthropic.
- Si vous définissez explicitement l'une de ces valeurs, OpenClaw ne les remplace **pas**.

## Ce que cela améliore (coût + comportement du cache)

- **Pourquoi élaguer :** La mise en cache des invites Anthropic ne s'applique que dans le TTL. Si une session devient inactive au-delà du TTL, la requête suivante rémet en cache l'invite complète sauf si vous la réduisez d'abord.
- **Ce qui devient moins cher :** l'élagage réduit la taille de **cacheWrite** pour cette première requête après l'expiration du TTL.
- **Pourquoi la réinitialisation du TTL est importante :** une fois l'élagage exécuté, la fenêtre de cache se réinitialise, les requêtes suivantes peuvent réutiliser l'invite fraîchement mise en cache au lieu de rémettre en cache l'historique complet.
- **Ce qu'il ne fait pas :** l'élagage n'ajoute pas de tokens ou ne "double" pas les coûts ; il change uniquement ce qui est mis en cache lors de cette première requête post-TTL.

## Ce qui peut être élagué

- Uniquement les messages `toolResult`.
- Les messages utilisateur + assistant ne sont **jamais** modifiés.
- Les `keepLastAssistants` derniers messages d'assistant sont protégés ; les résultats d'outils après ce seuil ne sont pas élaguées.
- S'il n'y a pas assez de messages d'assistant pour établir le seuil, l'élagage est ignoré.
- Les résultats d'outils contenant des **blocs d'image** sont ignorés (jamais réduits/effacés).

## Estimation de la fenêtre de contexte

L'élagage utilise une fenêtre de contexte estimée (caractères ≈ tokens × 4). La fenêtre de base est résolue dans cet ordre :

1. Remplacement `models.providers.*.models[].contextWindow`.
2. Définition du modèle `contextWindow` (du registre des modèles).
3. Défaut `200000` tokens.

Si `agents.defaults.contextTokens` est défini, il est traité comme un plafond (min) sur la fenêtre résolue.

## Mode

### cache-ttl

- L'élagage s'exécute uniquement si le dernier appel Anthropic est plus ancien que `ttl` (par défaut `5m`).
- Quand il s'exécute : même comportement de réduction progressive + effacement complet qu'avant.

## Élagage progressif vs complet

- **Réduction progressive** : uniquement pour les résultats d'outils surdimensionnés.
  - Conserve le début + la fin, insère `...`, et ajoute une note avec la taille d'origine.
  - Ignore les résultats avec des blocs d'image.
- **Effacement complet** : remplace le résultat d'outil entier par `hardClear.placeholder`.

## Sélection d'outils

- `tools.allow` / `tools.deny` supportent les caractères génériques `*`.
- Deny l'emporte.
- La correspondance est insensible à la casse.
- Liste allow vide => tous les outils autorisés.

## Interaction avec d'autres limites

- Les outils intégrés tronquent déjà leur propre sortie ; l'élagage de session est une couche supplémentaire qui empêche les chats de longue durée d'accumuler trop de sortie d'outils dans le contexte du modèle.
- La compaction est séparée : la compaction résume et persiste, l'élagage est transitoire par requête. Voir [/concepts/compaction](/fr/concepts/compaction).

## Valeurs par défaut (quand activé)

- `ttl`: `"5m"`
- `keepLastAssistants`: `3`
- `softTrimRatio`: `0.3`
- `hardClearRatio`: `0.5`
- `minPrunableToolChars`: `50000`
- `softTrim`: `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }`
- `hardClear`: `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

## Exemples

Par défaut (désactivé) :

```json5
{
  agents: { defaults: { contextPruning: { mode: "off" } } },
}
```

Activer l'élagage conscient du TTL :

```json5
{
  agents: { defaults: { contextPruning: { mode: "cache-ttl", ttl: "5m" } } },
}
```

Restreindre l'élagage à des outils spécifiques :

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl",
        tools: { allow: ["exec", "read"], deny: ["*image*"] },
      },
    },
  },
}
```

Voir la référence de configuration : [Gateway Configuration](/fr/gateway/configuration)
