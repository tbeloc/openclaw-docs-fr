# Streaming + chunking

OpenClaw dispose de deux couches de streaming distinctes :

- **Block streaming (canaux) :** émettre des **blocs** complétés au fur et à mesure que l'assistant écrit. Ce sont des messages de canal normaux (pas des deltas de tokens).
- **Preview streaming (Telegram/Discord/Slack) :** mettre à jour un **message d'aperçu** temporaire pendant la génération.

Il n'y a **pas de vrai streaming de delta de tokens** vers les messages de canal aujourd'hui. Le preview streaming est basé sur les messages (envoi + éditions/ajouts).

## Block streaming (messages de canal)

Le block streaming envoie la sortie de l'assistant en chunks grossiers au fur et à mesure qu'elle devient disponible.

```
Model output
  └─ text_delta/events
       ├─ (blockStreamingBreak=text_end)
       │    └─ chunker emits blocks as buffer grows
       └─ (blockStreamingBreak=message_end)
            └─ chunker flushes at message_end
                   └─ channel send (block replies)
```

Légende :

- `text_delta/events` : événements de flux du modèle (peuvent être rares pour les modèles non-streaming).
- `chunker` : `EmbeddedBlockChunker` appliquant les limites min/max + préférence de rupture.
- `channel send` : messages sortants réels (réponses en blocs).

**Contrôles :**

- `agents.defaults.blockStreamingDefault` : `"on"`/`"off"` (par défaut off).
- Remplacements de canal : `*.blockStreaming` (et variantes par compte) pour forcer `"on"`/`"off"` par canal.
- `agents.defaults.blockStreamingBreak` : `"text_end"` ou `"message_end"`.
- `agents.defaults.blockStreamingChunk` : `{ minChars, maxChars, breakPreference? }`.
- `agents.defaults.blockStreamingCoalesce` : `{ minChars?, maxChars?, idleMs? }` (fusionner les blocs streamés avant envoi).
- Limite stricte du canal : `*.textChunkLimit` (ex. `channels.whatsapp.textChunkLimit`).
- Mode chunk du canal : `*.chunkMode` (`length` par défaut, `newline` divise sur les lignes vides (limites de paragraphes) avant chunking par longueur).
- Limite souple Discord : `channels.discord.maxLinesPerMessage` (par défaut 17) divise les réponses hautes pour éviter le clipping UI.

**Sémantique des limites :**

- `text_end` : streamer les blocs dès que le chunker émet ; flush à chaque `text_end`.
- `message_end` : attendre que le message de l'assistant se termine, puis flush la sortie mise en buffer.

`message_end` utilise toujours le chunker si le texte mis en buffer dépasse `maxChars`, il peut donc émettre plusieurs chunks à la fin.

## Algorithme de chunking (limites basse/haute)

Le chunking de blocs est implémenté par `EmbeddedBlockChunker` :

- **Limite basse :** ne pas émettre tant que le buffer < `minChars` (sauf si forcé).
- **Limite haute :** préférer les divisions avant `maxChars` ; si forcé, diviser à `maxChars`.
- **Préférence de rupture :** `paragraph` → `newline` → `sentence` → `whitespace` → rupture dure.
- **Clôtures de code :** ne jamais diviser à l'intérieur des clôtures ; quand forcé à `maxChars`, fermer + rouvrir la clôture pour garder le Markdown valide.

`maxChars` est limité au `textChunkLimit` du canal, vous ne pouvez donc pas dépasser les limites par canal.

## Coalescing (fusionner les blocs streamés)

Quand le block streaming est activé, OpenClaw peut **fusionner les chunks de blocs consécutifs**
avant de les envoyer. Cela réduit le "spam d'une seule ligne" tout en fournissant
une sortie progressive.

- Le coalescing attend des **lacunes d'inactivité** (`idleMs`) avant de flush.
- Les buffers sont limités par `maxChars` et vont flush s'ils le dépassent.
- `minChars` empêche les minuscules fragments d'être envoyés jusqu'à ce que suffisamment de texte s'accumule
  (le flush final envoie toujours le texte restant).
- Le joiner est dérivé de `blockStreamingChunk.breakPreference`
  (`paragraph` → `\n\n`, `newline` → `\n`, `sentence` → espace).
- Les remplacements de canal sont disponibles via `*.blockStreamingCoalesce` (y compris les configs par compte).
- Le `minChars` de coalescing par défaut est augmenté à 1500 pour Signal/Slack/Discord sauf s'il est remplacé.

## Rythme humain entre les blocs

Quand le block streaming est activé, vous pouvez ajouter une **pause aléatoire** entre
les réponses en blocs (après le premier bloc). Cela rend les réponses multi-bulles
plus naturelles.

- Config : `agents.defaults.humanDelay` (remplacer par agent via `agents.list[].humanDelay`).
- Modes : `off` (par défaut), `natural` (800–2500ms), `custom` (`minMs`/`maxMs`).
- S'applique uniquement aux **réponses en blocs**, pas aux réponses finales ou résumés d'outils.

## "Streamer les chunks ou tout"

Cela correspond à :

- **Streamer les chunks :** `blockStreamingDefault: "on"` + `blockStreamingBreak: "text_end"` (émettre au fur et à mesure). Les canaux non-Telegram ont également besoin de `*.blockStreaming: true`.
- **Streamer tout à la fin :** `blockStreamingBreak: "message_end"` (flush une fois, possiblement plusieurs chunks si très long).
- **Pas de block streaming :** `blockStreamingDefault: "off"` (réponse finale uniquement).

**Note de canal :** Le block streaming est **off sauf si**
`*.blockStreaming` est explicitement défini à `true`. Les canaux peuvent streamer un aperçu en direct
(`channels.<channel>.streaming`) sans réponses en blocs.

Rappel de localisation de config : les défauts `blockStreaming*` se trouvent sous
`agents.defaults`, pas la config racine.

## Modes de preview streaming

Clé canonique : `channels.<channel>.streaming`

Modes :

- `off` : désactiver le preview streaming.
- `partial` : aperçu unique qui est remplacé par le texte le plus récent.
- `block` : les mises à jour d'aperçu en étapes chunked/ajoutées.
- `progress` : aperçu de progression/statut pendant la génération, réponse finale à la fin.

### Mappage des canaux

| Canal    | `off` | `partial` | `block` | `progress`        |
| -------- | ----- | --------- | ------- | ----------------- |
| Telegram | ✅    | ✅        | ✅      | mappe à `partial` |
| Discord  | ✅    | ✅        | ✅      | mappe à `partial` |
| Slack    | ✅    | ✅        | ✅      | ✅                |

Slack uniquement :

- `channels.slack.nativeStreaming` bascule les appels API de streaming natif Slack quand `streaming=partial` (par défaut : `true`).

Migration de clé héritée :

- Telegram : `streamMode` + booléen `streaming` auto-migrent vers l'enum `streaming`.
- Discord : `streamMode` + booléen `streaming` auto-migrent vers l'enum `streaming`.
- Slack : `streamMode` auto-migre vers l'enum `streaming` ; booléen `streaming` auto-migre vers `nativeStreaming`.

### Comportement à l'exécution

Telegram :

- Utilise `sendMessage` + `editMessageText` pour les mises à jour d'aperçu dans les DMs et groupes/sujets.
- Le preview streaming est ignoré quand le block streaming Telegram est explicitement activé (pour éviter le double-streaming).
- `/reasoning stream` peut écrire le raisonnement à l'aperçu.

Discord :

- Utilise les messages d'aperçu send + edit.
- Le mode `block` utilise le chunking de brouillon (`draftChunk`).
- Le preview streaming est ignoré quand le block streaming Discord est explicitement activé.

Slack :

- `partial` peut utiliser le streaming natif Slack (`chat.startStream`/`append`/`stop`) quand disponible.
- `block` utilise les aperçus de brouillon de style ajout.
- `progress` utilise le texte d'aperçu de statut, puis la réponse finale.
