---
title: "Compréhension des médias et génération de médias - Note de maturité de livraison de synthèse vocale"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de livraison de synthèse vocale

## Résumé

La synthèse vocale dispose de l'une des surfaces de fournisseur les plus largement documentées dans le domaine des médias : de nombreux fournisseurs de synthèse vocale, comportement des notes vocales par canal, commandes `/tts`, directives, modes automatiques, personas, intégration Talk et méthodes Gateway. La qualité est inférieure à stable car les problèmes archivés montrent un routage des notes vocales spécifique au canal, une instabilité du mode final et des problèmes de compatibilité audio.

## Portée de la catégorie

Inclus dans cette catégorie :

- TTS : Couvre la synthèse vocale sur l'agent/outil `tts` et les méthodes Gateway, `messages.tts`, registre des fournisseurs, directives et comportement de livraison audio vocal sortant associé.
- Livraison audio vocal sortant : Couvre la livraison audio vocal sortant sur l'agent/outil `tts` et les méthodes Gateway, `messages.tts`, registre des fournisseurs, directives et comportement de livraison audio vocal sortant associé.

## Fonctionnalités

- TTS : Couvre la synthèse vocale sur l'agent/outil `tts` et les méthodes Gateway, `messages.tts`, registre des fournisseurs, directives et comportement de livraison audio vocal sortant associé.
- Livraison audio vocal sortant : Couvre la livraison audio vocal sortant sur l'agent/outil `tts` et les méthodes Gateway, `messages.tts`, registre des fournisseurs, directives et comportement de livraison audio vocal sortant associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : La documentation couvre la configuration des fournisseurs, les modes automatiques, l'utilisation explicite des outils, les directives, le comportement des notes vocales par canal, l'interaction Talk et les matrices des fournisseurs. La source contient la configuration/statut TTS, les directives, le registre des fournisseurs, les fournisseurs de synthèse vocale, l'intégration des messages sortants, les méthodes RPC Gateway et les déclarations de capacité des canaux.
- Signaux négatifs : Le comportement natif des notes vocales diffère par canal et format de sortie du fournisseur, donc un chemin générique ne prouve pas tous les scénarios utilisateur.
- Lacunes d'intégration : La livraison des notes vocales entre canaux nécessite une preuve récurrente du scénario car Feishu, Telegram, WhatsApp, Matrix, Discord voice, Talk et webchat affichent tous différemment.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : #85632 montre l'envoi d'agent cron isolé envoyant de l'audio brut au lieu d'une note vocale ; #80317/#83227 couvrent la compatibilité vocale MP3 OpenAI pour Telegram ; #84791 couvre le routage des notes vocales Telegram ; #83511/#83988 couvrent l'instabilité texte/audio du mode final ; #42539 et #73210 demandent des modes de livraison vocale uniquement/séparée ; #68770 couvre les journaux de succès manquants pour les médias Telegram.
- Rapports Discrawl : Les enregistrements d'archives Freshbits et OpenClaw mentionnent les correctifs de notes vocales Google Opus, la clarification de la documentation des notes vocales WhatsApp, le correctif de livraison runtime Feishu et la confusion des utilisateurs entre la voix TTS et les modèles de voix en temps réel.
- Bonnes qualités : TTS est explicite par défaut, supporte les modes automatiques/étiquetés, normalise les capacités de livraison vocale fournisseur/canal et dispose de méthodes Gateway status/convert/provider/persona.
- Mauvaises qualités : La livraison des notes vocales est sensible à la forme de charge utile spécifique au canal, au format de sortie du fournisseur, à la sémantique d'affichage du mode final et au fait que le chemin soit commande, modèle final, outil de message, cron, Talk ou voix de canal.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux runtime.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour TTS, Livraison audio vocal sortant.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le routage des notes vocales a toujours des cas limites spécifiques au canal.
- Le comportement du texte visible du mode final plus l'audio retardé a nécessité des correctifs récents.
- L'observabilité de l'opérateur pour les réponses TTS portant des médias est inégale selon le canal.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/tts.md` documente les fournisseurs, la configuration, les modes automatiques, l'utilisation des outils, les directives, les personas, le basculement des fournisseurs et la relation Talk.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` documente TTS comme sortie média synchrone et distingue les modes Talk/temps réel.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md`, `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md`, `/Users/kevinlin/code/openclaw/docs/channels/telegram.md`, `/Users/kevinlin/code/openclaw/docs/channels/feishu.md` et `/Users/kevinlin/code/openclaw/docs/channels/qqbot.md` documentent le comportement TTS/notes vocales spécifique au canal.

### Source

- `/Users/kevinlin/code/openclaw/src/tts/tts.ts`
- `/Users/kevinlin/code/openclaw/src/tts/tts-config.ts`
- `/Users/kevinlin/code/openclaw/src/tts/status-config.ts`
- `/Users/kevinlin/code/openclaw/src/tts/directives.ts`
- `/Users/kevinlin/code/openclaw/src/tts/openai-compatible-speech-provider.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/tts-tool.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/tts.ts`
- `/Users/kevinlin/code/openclaw/src/infra/outbound/message-action-tts.ts`
- `/Users/kevinlin/code/openclaw/src/channels/plugins/tts-capabilities.ts`
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/tts-runtime.ts`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/dispatch-acp-tts.runtime.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat.directive-tags.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.test.ts`
- `/Users/kevinlin/code/openclaw/src/infra/outbound/message-action-runner.core-send.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/tools/tts-tool.test.ts`
- `/Users/kevinlin/code/openclaw/src/tts/status-config.test.ts`
- `/Users/kevinlin/code/openclaw/src/tts/directives.test.ts`
- `/Users/kevinlin/code/openclaw/src/tts/tts-config.test.ts`
- `/Users/kevinlin/code/openclaw/src/tts/openai-compatible-speech-provider.test.ts`
- `/Users/kevinlin/code/openclaw/src/channels/plugins/tts-capabilities.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/tts.test.ts`

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "tts voice note" --json
```

Résultats :

- A retourné #85632 propagation de notes vocales d'agent cron isolé, #80317/#83227 compatibilité vocale MP3 OpenAI, #83988/#83511 instabilité du mode final, #84791 routage des notes vocales Telegram, #42539 mode texte/voix séparé, #74722 réponses vocales conscientes de la langue, #68770 journalisation du succès des médias et #73210 mode de livraison vocale uniquement.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "tts voice note" --limit 5
```

Résultats :

- A retourné des entrées Freshbits mentionnant le correctif TTS de notes vocales Google Opus, les remplacements de voix par agent et la documentation des notes vocales WhatsApp.
- A retourné un commentaire d'archive OpenClaw pour #71920 indiquant que la livraison des notes vocales TTS Feishu a été corrigée après que le TTS de streaming de bloc ait ignoré la normalisation des médias sécurisés avant la distribution.
- A retourné une question utilisateur distinguant la voix TTS des modèles de voix en temps réel, montrant la confusion de l'opérateur/utilisateur sur les surfaces de synthèse vocale.
