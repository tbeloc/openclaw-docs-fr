---
title: "Outils de génération d'images/vidéos/musique - Note de maturité de la génération musicale"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Note de maturité de la génération musicale

## Résumé

La génération musicale dispose d'un runtime partagé, de documentation, d'enregistrements de fournisseurs et d'échafaudage de fournisseurs en direct, mais c'est la partie la plus nouvelle et la moins éprouvée de la surface. L'outil supporte la génération basée sur des invites uniquement, les paroles, le mode instrumental, la durée, le format, le mode d'édition d'images où les fournisseurs le déclarent, les basculements de fournisseurs et la mise en forme des actifs audio.

La couverture est Beta car la documentation et le code source couvrent le contrat prévu et des tests en direct existent pour les fournisseurs représentatifs. La qualité est Alpha car les archives montrent des problèmes d'interrogation/routage MiniMax, la musique OpenRouter ne s'expédiant pas dans une fenêtre de rapport, la troncature de la valeur des paroles et les problèmes de découverte différée de `music_generate`.

## Portée de la catégorie

Inclus dans cette catégorie :

- entrée d'invite et de paroles : Couvre l'entrée d'invite et de paroles dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- mode instrumental : Couvre le mode instrumental dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- contrôles de durée/format : Couvre les contrôles de durée/format dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- voies d'édition avec référence d'image : Couvre les voies d'édition avec référence d'image dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- sorties audio générées : Couvre les sorties audio générées dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- basculement de fournisseur : Couvre le basculement de fournisseur dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.

## Fonctionnalités

- entrée d'invite et de paroles : Couvre l'entrée d'invite et de paroles dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- mode instrumental : Couvre le mode instrumental dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- contrôles de durée/format : Couvre les contrôles de durée/format dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- voies d'édition avec référence d'image : Couvre les voies d'édition avec référence d'image dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- sorties audio générées : Couvre les sorties audio générées dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.
- basculement de fournisseur : Couvre le basculement de fournisseur dans `music_generate`, les entrées d'invite et de paroles, le mode instrumental, la durée et le comportement de génération musicale associé.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : La documentation explique l'outil, les paramètres, la liste des fournisseurs, la validation, le comportement asynchrone et les commandes de test en direct ; le code source dispose d'un runtime partagé et de gestion des actifs audio ; les tests en direct couvrent la génération et les voies d'édition déclarées.
- Signaux négatifs : L'ensemble des fournisseurs est plus petit et plus nouveau que celui des images/vidéos, le support d'édition est spécifique au fournisseur et la preuve en direct dépend davantage des identifiants.
- Lacunes d'intégration : Ajouter un scénario de passerelle/canal pour `music_generate` qui vérifie la découverte d'outil, la livraison des pièces jointes audio générées et le comportement du statut du fournisseur.

## Score de qualité

- Score : `Alpha (61%)`
- Rapports Gitcrawl : Les recherches musicales ont retourné #84506 sur l'interrogation asynchrone de génération musicale MiniMax, #79535 où la vidéo OpenRouter a échoué et la musique n'avait pas été expédiée, #82678 où la chaîne `none` a tronqué les appels d'outils et les réponses de l'assistant lorsqu'elle était utilisée comme paroles, et #84764 demandant des réponses de génération musicale en continu.
- Rapports Discrawl : La recherche Discord a trouvé une discussion sur les outils médias différés où `music_generate` n'était pas assez découvrable à partir du contexte source prévisualisé.
- Bonnes qualités : Le runtime musical partage la résolution des candidats fournisseurs et la mise en forme des actifs générés avec le reste de la surface médias.
- Mauvaises qualités : Le comportement du fournisseur et la découverte restent incertains, et la gestion des paramètres de paroles/instrumental a produit des cas limites visibles par l'utilisateur.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : les archives de documentation, code source, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'entrée d'invite et de paroles, le mode instrumental, les contrôles de durée/format, les voies d'édition avec référence d'image, les sorties audio générées, le basculement de fournisseur.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'étendue des fournisseurs musicaux et la preuve opérationnelle sont en retard par rapport aux images et vidéos.
- L'interrogation asynchrone MiniMax et le comportement de la musique OpenRouter présentent un risque d'archive récent.
- La découverte de `music_generate` via les outils différés a besoin de meilleures affordances visibles par l'utilisateur.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:11` décrit la capacité de génération musicale partagée.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:96` répertorie les fournisseurs pris en charge et la matrice de capacités.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:119` documente les actions `list` et `status`.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:138` documente les paramètres de l'outil.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:170` documente la validation, la normalisation et les délais d'expiration.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:223` documente la sélection de modèle, les basculements et la détection automatique.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:257` documente les notes du fournisseur.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md:331` documente la couverture des tests en direct et `pnpm test:live:media music`.

### Code source

- `/Users/kevinlin/code/openclaw/src/music-generation/runtime.ts:30` répertorie les fournisseurs de génération musicale du runtime.
- `/Users/kevinlin/code/openclaw/src/music-generation/runtime.ts:37` résout les candidats fournisseurs musicaux et la messagerie sans modèle.
- `/Users/kevinlin/code/openclaw/src/music-generation/runtime.ts:84` applique la normalisation des remplacements et invoque les fournisseurs.
- `/Users/kevinlin/code/openclaw/src/music-generation/runtime.ts:126` enregistre les tentatives de fournisseur et la gestion des défaillances.
- `/Users/kevinlin/code/openclaw/src/music-generation/provider-assets.ts:50` extrait les candidats de fichiers musicaux.
- `/Users/kevinlin/code/openclaw/src/music-generation/provider-assets.ts:64` construit les actifs musicaux générés à partir de données base64.
- `/Users/kevinlin/code/openclaw/src/music-generation/provider-assets.ts:78` télécharge les actifs musicaux générés.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts:194` enregistre la génération musicale OpenRouter.
- `/Users/kevinlin/code/openclaw/extensions/fal/index.ts:13` enregistre la génération musicale fal.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/music-generation-providers.live.test.ts:53` déclare les cas de fournisseur en direct pour fal, Google, MiniMax et OpenRouter.
- `/Users/kevinlin/code/openclaw/extensions/music-generation-providers.live.test.ts:170` configure l'authentification en direct.
- `/Users/kevinlin/code/openclaw/extensions/music-generation-providers.live.test.ts:226` affirme le MIME audio généré et les tampons.
- `/Users/kevinlin/code/openclaw/extensions/music-generation-providers.live.test.ts:260` affirme le mode d'édition avec entrée d'image où déclaré.
- `/Users/kevinlin/code/openclaw/scripts/test-live-media.ts:31` inclut les listes de fournisseurs de la suite musicale en direct.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts:22` répertorie les fournisseurs musicaux groupés attendus.
- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts:54` vérifie les manifestes des fournisseurs musicaux groupés.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-announce-delivery.test.ts:2289` couvre les messages directs d'achèvement musical nécessitant l'outil de message.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "music generation" --json`

Résultats :

- Retourné #84506 sur l'interrogation asynchrone MiniMax, #79535 sur le statut vidéo/musique OpenRouter, #82678 sur les paroles `none` tronquant les appels d'outils/réponses, #84764 sur la génération musicale en continu et #78852 sur la réutilisation de la disponibilité des outils médias.

Requête : `gitcrawl search openclaw/openclaw --query "music generation Lyria MiniMax fal OpenRouter" --json`

Résultats :

- Aucun résultat direct pour la phrase exacte.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "music_generate"`

Résultats :

- Trouvé une discussion du responsable sur la découverte différée de l'outil `music_generate` et le comportement de l'aperçu source.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "music generation Lyria MiniMax fal OpenRouter"`

Résultats :

- Aucun résultat direct pour la phrase exacte.
