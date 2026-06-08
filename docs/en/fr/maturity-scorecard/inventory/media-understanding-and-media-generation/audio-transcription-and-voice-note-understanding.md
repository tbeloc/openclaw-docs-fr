---
title: "Compréhension des médias et génération de médias - Note de maturité de la transcription audio et de la compréhension des notes vocales"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de la transcription audio et de la compréhension des notes vocales

## Résumé

La compréhension audio est une fonctionnalité documentée et largement implémentée : les notes vocales entrantes peuvent être transcrites, l'analyse des commandes peut utiliser les transcriptions, des solutions de secours pour les fournisseurs et l'interface de ligne de commande existent, et les groupes contrôlés par mention peuvent vérifier les notes vocales en amont. La qualité est maintenue en dessous du stable en raison de problèmes récurrents d'authentification, de sortie de progression, de liste des fournisseurs et de comportement des transcriptions dans les archives.

## Portée de la catégorie

Cette catégorie couvre la compréhension des médias audio/STT par lot, les solutions de secours locales de l'interface de ligne de commande, la transcription par fournisseur, la vérification préalable des notes vocales avant les portes de mention, l'insertion de transcriptions dans `Body`/`Transcript`, le comportement d'écho-transcription, le support des proxies et la sélection des pièces jointes audio. La parole en direct/temps réel est hors de portée sauf si la documentation indique explicitement qu'elle n'utilise pas ce chemin par lot.

## Fonctionnalités

- Sélection des pièces jointes audio : Couvre la sélection des pièces jointes audio dans la compréhension des médias audio/STT par lot, les solutions de secours locales de l'interface de ligne de commande, la transcription par fournisseur, la vérification préalable des notes vocales avant les portes de mention et le comportement associé de la transcription audio et de la compréhension des notes vocales.
- Fournisseur STT par lot et solution de secours de l'interface de ligne de commande : Couvre le fournisseur STT par lot et la solution de secours de l'interface de ligne de commande dans la compréhension des médias audio/STT par lot, les solutions de secours locales de l'interface de ligne de commande, la transcription par fournisseur, la vérification préalable des notes vocales avant les portes de mention et le comportement associé de la transcription audio et de la compréhension des notes vocales.
- Vérification préalable des mentions de notes vocales : Couvre la vérification préalable des mentions de notes vocales dans la compréhension des médias audio/STT par lot, les solutions de secours locales de l'interface de ligne de commande, la transcription par fournisseur, la vérification préalable des notes vocales avant les portes de mention et le comportement associé de la transcription audio et de la compréhension des notes vocales.
- Insertion et écho de transcription : Couvre l'insertion et l'écho de transcription dans la compréhension des médias audio/STT par lot, les solutions de secours locales de l'interface de ligne de commande, la transcription par fournisseur, la vérification préalable des notes vocales avant les portes de mention et le comportement associé de la transcription audio et de la compréhension des notes vocales.
- Gestion des proxies audio et des limites : Couvre la gestion des proxies audio et des limites dans la compréhension des médias audio/STT par lot, les solutions de secours locales de l'interface de ligne de commande, la transcription par fournisseur, la vérification préalable des notes vocales avant les portes de mention et le comportement associé de la transcription audio et de la compréhension des notes vocales.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La documentation couvre la configuration, les valeurs par défaut, l'ordre des fournisseurs, les solutions de secours de l'interface de ligne de commande, le comportement de vérification préalable des mentions, les options d'écho de transcription, les limites de taille, la gestion des proxies et le comportement en cas d'échec. La source dispose d'un exécuteur dédié, d'une vérification préalable audio, d'un chemin audio compatible avec les fournisseurs et d'une intégration d'analyse des commandes.
- Signaux négatifs : La preuve d'intégration est forte pour les chemins de réponse et de canal, mais pas uniforme dans toutes les combinaisons de fournisseurs et de canaux.
- Lacunes d'intégration : Des analyses en direct spécifiques aux fournisseurs existent via des fichiers d'assistance, mais les cartes de pointage de version récurrentes pour tous les fournisseurs STT et tous les canaux de notes vocales ne sont pas évidentes à partir de la documentation enregistrée.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : Les enregistrements d'archives ouvertes incluent le support natif de la compréhension audio/vidéo (#78797), les correctifs de points de terminaison audio compatibles OpenAI privés (#73817), le support des segments de transcription diarisés (#81721), la suppression de la transcription de progression de Whisper local (#87393/#87384), le démarrage du fournisseur audio enthousiaste lors de la liste (#85368) et les défaillances de clé API STT sans authentification/locale (#74644).
- Rapports Discrawl : Les commentaires d'archives enregistrent les lacunes de remplissage de notes vocales minuscules/silencieuses, les correctifs de transcription de livraison directe et les défaillances de compréhension des médias devenant visibles en tant qu'avertissement/statut plutôt que supprimées.
- Bonnes qualités : La conception est explicitement au mieux, conserve les pièces jointes d'origine, a une gestion déterministe des tailles/audio minuscule, utilise la résolution d'authentification standard et peut vérifier les notes vocales de groupe avant les portes de mention.
- Mauvaises qualités : Le comportement du chemin audio reste sensible à la forme d'authentification du fournisseur, aux conventions stdout de l'interface de ligne de commande, à la disponibilité des binaires locaux et à la question de savoir si la transcription s'exécute en tant que vérification préalable, livraison directe, ACP ou traitement normal des réponses.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les archives, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la sélection des pièces jointes audio, le fournisseur STT par lot et la solution de secours de l'interface de ligne de commande, la vérification préalable des mentions de notes vocales, l'insertion et l'écho de transcription, la gestion des proxies audio et des limites.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'analyse de la sortie de transcription de l'interface de ligne de commande semble toujours assez fragile pour produire des correctifs récents.
- Les fournisseurs sans authentification/locaux et les points de terminaison privés explicites ont nécessité des correctifs de suivi.
- La documentation orientée opérateur est large, mais une histoire concise de santé/runbook pour la compréhension audio échouée est distribuée dans la documentation et la sortie de statut plutôt que centralisée.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/nodes/audio.md` documente la compréhension des médias audio, l'ordre de secours du fournisseur et de l'interface de ligne de commande, l'analyse des commandes, l'écho de transcription, le support des proxies, la détection des mentions et les limites.
- `/Users/kevinlin/code/openclaw/docs/nodes/media-understanding.md` documente la configuration partagée `tools.media.audio`, les entrées de fournisseur, les entrées de l'interface de ligne de commande, la politique de pièces jointes, les plafonds de taille, la concurrence, la portée et la sortie de statut.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` mappe les fournisseurs STT et explique la réutilisation des transcriptions de vérification préalable par la compréhension partagée des médias.
- La documentation des canaux incluant `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md`, `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` et `/Users/kevinlin/code/openclaw/docs/channels/discord.md` décrit le comportement de transcription des notes vocales.

### Source

- `/Users/kevinlin/code/openclaw/src/media-understanding/audio-transcription-runner.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/openai-compatible-audio.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/audio-preflight.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.entries.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/apply.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/echo-transcript.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/audio-tags.ts`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/dispatch-acp-tts.runtime.ts` et `/Users/kevinlin/code/openclaw/src/auto-reply/reply/dispatch-acp-media.runtime.ts` couvrent les surfaces de dispatch d'exécution autour des médias et de la parole.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner.media-paths.test.ts` et `/Users/kevinlin/code/openclaw/src/auto-reply/reply/get-reply-run.media-only.test.ts` couvrent le comportement du chemin média de la réponse.
- `/Users/kevinlin/code/openclaw/src/scripts/test-live-media.test.ts` fournit la couverture du point d'entrée du test de médias en direct.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/media-understanding/openai-compatible-audio.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.auto-audio.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.cli-audio.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.deepgram.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.skip-tiny-audio.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/audio-preflight.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/apply.echo-transcript.test.ts`

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "audio transcription media understanding" --json
```

Résultats :

- Threads pertinents retournés : #78797 compréhension native audio/vidéo, #73817 points de terminaison de transcription audio compatibles OpenAI privés, #81721 segments de transcription JSON diarisés, #87393/#87384 suppression de la transcription de progression de Whisper, #85368 évitement du démarrage de la liste des fournisseurs, #74644 défaillance de clé API STT locale/sans authentification, #78069 notes vocales avant la porte de mention.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "audio transcription media understanding" --limit 5
```

Résultats :

- Commentaires d'archives retournés notant les lacunes de remplissage de notes vocales silencieuses sur #49131, ajout d'AssemblyAI en tant que plugin fourni sur #71740, confirmation de la transcription audio de livraison directe sur #65978, confirmation que les raisons d'échec de la compréhension des médias sont surfacées dans la sortie d'avertissement/statut sur #60421 et conservation des chemins image/vidéo tout en supprimant uniquement les pièces jointes audio transcrites sur #56541.
