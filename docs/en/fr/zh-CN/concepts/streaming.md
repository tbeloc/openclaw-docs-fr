---
read_when:
  - Expliquer comment la diffusion en continu ou le chunking fonctionne sur les canaux
  - Modifier le comportement de chunking en continu ou de chunking de canal
  - Déboguer les réponses de chunks répétées/anticipées ou la diffusion de brouillons
summary: Comportement de diffusion en continu + chunking (réponses de chunks, diffusion de brouillons, limites)
title: Diffusion en continu et chunking
x-i18n:
  generated_at: "2026-02-03T10:05:41Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f014eb1898c4351b1d6b812223226d91324701e3e809cd0f3faf6679841bc353
  source_path: concepts/streaming.md
  workflow: 15
---

# Diffusion en continu et chunking

OpenClaw dispose de deux couches de « diffusion en continu » indépendantes :

- **Diffusion en continu par chunks (canaux) :** Émet des **chunks** terminés au fur et à mesure que l'assistant écrit. Ce sont des messages de canal ordinaires (pas des incréments de tokens).
- **Diffusion de type token (Telegram uniquement) :** Met à jour les **bulles de brouillon** avec du texte partiel lors de la génération ; le message final est envoyé à la fin.

Il n'y a actuellement **pas de véritable diffusion en continu de tokens** vers les messages de canal externes. La diffusion de brouillon Telegram est la seule interface de diffusion en continu partielle.

## Diffusion en continu par chunks (messages de canal)

La diffusion en continu par chunks envoie des chunks à granularité grossière au fur et à mesure que la sortie de l'assistant devient disponible.

```
Sortie du modèle
  └─ text_delta/events
       ├─ (blockStreamingBreak=text_end)
       │    └─ Le chunker émet des chunks au fur et à mesure que le buffer grandit
       └─ (blockStreamingBreak=message_end)
            └─ Le chunker vide le buffer à message_end
                   └─ Envoi du canal (réponse de chunk)
```

Légende :

- `text_delta/events` : Événements de flux du modèle (peut être clairsemé pour les modèles non-streaming).
- `chunker` : `EmbeddedBlockChunker` appliquant les limites min/max + préférences de rupture.
- `channel send` : Message sortant réel (réponse de chunk).

**Éléments de contrôle :**

- `agents.defaults.blockStreamingDefault` : `"on"`/`"off"` (désactivé par défaut).
- Surcharge de canal : `*.blockStreaming` (et variantes par compte) peut forcer `"on"`/`"off"` par canal.
- `agents.defaults.blockStreamingBreak` : `"text_end"` ou `"message_end"`.
- `agents.defaults.blockStreamingChunk` : `{ minChars, maxChars, breakPreference? }`.
- `agents.defaults.blockStreamingCoalesce` : `{ minChars?, maxChars?, idleMs? }` (fusionne les chunks en continu avant envoi).
- Limite matérielle du canal : `*.textChunkLimit` (par ex. `channels.whatsapp.textChunkLimit`).
- Mode de chunking du canal : `*.chunkMode` (par défaut `length`, `newline` divise par lignes vides (limites de paragraphes) avant chunking par longueur).
- Limite logicielle Discord : `channels.discord.maxLinesPerMessage` (par défaut 17) divise les réponses plus hautes pour éviter la coupure de l'interface utilisateur.

**Sémantique des limites :**

- `text_end` : Le chunker émet immédiatement les chunks en continu ; vide à chaque `text_end`.
- `message_end` : Attend que le message de l'assistant soit terminé, puis vide la sortie mise en buffer.

Si le texte mis en buffer dépasse `maxChars`, `message_end` utilise toujours le chunker, donc peut émettre plusieurs chunks à la fin.

## Algorithme de chunking (limites basse/haute)

Le chunking des blocs est implémenté par `EmbeddedBlockChunker` :

- **Limite basse :** N'émet pas tant que le buffer < `minChars` (sauf si forcé).
- **Limite haute :** Préfère diviser avant `maxChars` ; si forcé, divise à `maxChars`.
- **Préférence de rupture :** `paragraph` → `newline` → `sentence` → `whitespace` → rupture matérielle.
- **Clôtures de code :** Ne divise jamais à l'intérieur des clôtures ; lors d'une division forcée à `maxChars`, ferme + rouvre les clôtures pour garder le Markdown valide.

`maxChars` est limité par le `textChunkLimit` du canal, donc vous ne pouvez pas dépasser la limite par canal.

## Coalescence (fusion des chunks en continu)

Lorsque la diffusion en continu par chunks est activée, OpenClaw peut **fusionner les chunks de chunks consécutifs** avant envoi. Cela réduit le « spam d'une seule ligne » tout en fournissant toujours une sortie progressive.

- La coalescence vide après un **écart d'inactivité** (`idleMs`).
- Le buffer est limité par `maxChars`, vide au dépassement.
- `minChars` empêche les minuscules fragments d'être envoyés jusqu'à ce que suffisamment de texte s'accumule (le vidage final envoie toujours le texte restant).
- Le connecteur est dérivé de `blockStreamingChunk.breakPreference` (`paragraph` → `\n\n`, `newline` → `\n`, `sentence` → espace).
- Les surcharges de canal sont disponibles via `*.blockStreamingCoalesce` (y compris la configuration par compte).
- Sauf surcharge, la coalescence par défaut `minChars` pour Signal/Slack/Discord est augmentée à 1500.

## Rythme quasi-humain entre les chunks

Lorsque la diffusion en continu par chunks est activée, vous pouvez ajouter des **pauses aléatoires** entre les réponses de chunks (après le premier chunk). Cela rend les réponses multi-bulles plus naturelles.

- Configuration : `agents.defaults.humanDelay` (surcharge par agent via `agents.list[].humanDelay`).
- Modes : `off` (par défaut), `natural` (800–2500ms), `custom` (`minMs`/`maxMs`).
- S'applique uniquement aux **réponses de chunks**, pas aux réponses finales ou résumés d'outils.

## « Diffuser les chunks ou tout à la fin »

Cela correspond à :

- **Diffuser les chunks :** `blockStreamingDefault: "on"` + `blockStreamingBreak: "text_end"` (émet au fur et à mesure de la génération). Les canaux non-Telegram nécessitent également `*.blockStreaming: true`.
- **Diffuser tout à la fin :** `blockStreamingBreak: "message_end"` (vide une fois, peut être plusieurs chunks si long).
- **Pas de diffusion en continu par chunks :** `blockStreamingDefault: "off"` (réponse finale uniquement).

**Remarque sur les canaux :** Pour les canaux non-Telegram, la diffusion en continu par chunks est **désactivée par défaut**, sauf si `*.blockStreaming` est explicitement défini à `true`. Telegram peut diffuser des brouillons sans réponses de chunks (`channels.telegram.streamMode`).

Rappel d'emplacement de configuration : Les valeurs par défaut de `blockStreaming*` se trouvent sous `agents.defaults`, pas à la racine de la configuration.

## Diffusion de brouillon Telegram (type token)

Telegram est le seul canal supportant la diffusion de brouillon :

- Utilise l'API Bot `sendMessageDraft` dans les **chats privés avec sujet**.
- `channels.telegram.streamMode: "partial" | "block" | "off"`.
  - `partial` : Met à jour le brouillon avec le dernier texte en continu.
  - `block` : Met à jour le brouillon par chunks (mêmes règles de chunker).
  - `off` : Pas de diffusion de brouillon.
- Configuration de chunking de brouillon (uniquement pour `streamMode: "block"`) : `channels.telegram.draftChunk` (par défaut : `minChars: 200`, `maxChars: 800`).
- La diffusion de brouillon est séparée de la diffusion en continu par chunks ; les réponses de chunks sont désactivées par défaut, activées uniquement sur les canaux non-Telegram via `*.blockStreaming: true`.
- La réponse finale est toujours un message ordinaire.
- `/reasoning stream` écrit le raisonnement dans la bulle de brouillon (Telegram uniquement).

Lorsque la diffusion de brouillon est active, OpenClaw désactive la diffusion en continu par chunks pour cette réponse pour éviter une double diffusion.

```
Telegram (chat privé + sujet)
  └─ sendMessageDraft (bulle de brouillon)
       ├─ streamMode=partial → Met à jour le dernier texte
       └─ streamMode=block   → Le chunker met à jour le brouillon
  └─ Réponse finale → Message ordinaire
```

Légende :

- `sendMessageDraft` : Bulle de brouillon Telegram (pas un vrai message).
- `final reply` : Message Telegram ordinaire envoyé.
