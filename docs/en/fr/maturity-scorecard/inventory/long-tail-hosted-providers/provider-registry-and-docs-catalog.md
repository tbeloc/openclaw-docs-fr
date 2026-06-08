---
title: "Fournisseurs hébergés long-tail - Note de maturité du catalogue de fournisseurs et de la découverte"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs hébergés long-tail - Note de maturité du catalogue de fournisseurs et de la découverte

## Résumé

Le registre de fournisseurs et le catalogue de docs sont en Alpha. Le répertoire de fournisseurs est large et la plomberie du catalogue d'installation de manifeste/fournisseur est réelle, mais le catalogue reste partiellement maintenu manuellement et dispersé sur plusieurs sources de vérité.

## Portée de la catégorie

Cette note couvre le répertoire de fournisseurs public, les liens de docs de fournisseurs, les tableaux d'aperçu des fournisseurs de modèles, les métadonnées de fournisseurs de manifeste, les métadonnées du catalogue de modèles, les entrées officielles du catalogue de fournisseurs externes, les lignes d'aperçu de l'index des fournisseurs, et le comportement de recherche/catalogue d'installation.

Hors de portée : les fournisseurs locaux uniquement, les fiches d'évaluation des fournisseurs de première partie lorsqu'elles sont évaluées séparément, et le comportement d'exécution des fournisseurs après qu'un fournisseur a déjà été sélectionné.

## Fonctionnalités

- Répertoire de fournisseurs : Couvre le répertoire de fournisseurs dans le répertoire de fournisseurs public, les liens de docs de fournisseurs, les tableaux d'aperçu des fournisseurs de modèles, les métadonnées de fournisseurs de manifeste, et le comportement associé du catalogue et de la découverte des fournisseurs.
- Catalogue d'installation de fournisseurs : Couvre le catalogue d'installation de fournisseurs dans le répertoire de fournisseurs public, les liens de docs de fournisseurs, les tableaux d'aperçu des fournisseurs de modèles, les métadonnées de fournisseurs de manifeste, et le comportement associé du catalogue et de la découverte des fournisseurs.
- Métadonnées du catalogue de modèles : Couvre les métadonnées du catalogue de modèles dans le répertoire de fournisseurs public, les liens de docs de fournisseurs, les tableaux d'aperçu des fournisseurs de modèles, les métadonnées de fournisseurs de manifeste, et le comportement associé du catalogue et de la découverte des fournisseurs.
- Vérifications de parité du catalogue : Couvre les vérifications de parité du catalogue dans le répertoire de fournisseurs public, les liens de docs de fournisseurs, les tableaux d'aperçu des fournisseurs de modèles, les métadonnées de fournisseurs de manifeste, et le comportement associé du catalogue et de la découverte des fournisseurs.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs :
  - `docs/providers/index.md` répertorie des dizaines de docs de fournisseurs hébergés, des aperçus de génération partagés, et des fournisseurs de transcription.
  - `docs/concepts/model-providers.md` explique le comportement des fournisseurs appartenant aux plugins et contient un tableau de fournisseurs groupés avec les identifiants de fournisseurs long-tail, les variables d'env d'authentification, et les modèles d'exemple.
  - `docs/plugins/manifest.md` documente les `providers` appartenant au manifeste, `providerCatalogEntry`, `modelCatalog`, les métadonnées d'authentification/env/configuration du fournisseur, les contrats, et les métadonnées de génération.
  - La source fusionne le manifeste, le catalogue officiel externe des fournisseurs, et les métadonnées d'installation de l'index des fournisseurs dans les choix d'installation des fournisseurs.
  - Les tests unitaires et de flux de commande couvrent les métadonnées d'installation des fournisseurs, la découverte des fournisseurs par secours, la source de chemin du catalogue des fournisseurs de manifeste par secours, et les lignes du catalogue des fournisseurs `models list`.
- Signaux négatifs :
  - La preuve du catalogue n'est pas générée de bout en bout à partir d'une seule source de métadonnées de fournisseur faisant autorité.
  - La passe d'assistance a trouvé des pages de fournisseurs non liées à partir de la liste principale de docs de fournisseurs : `deepinfra`, `inworld`, et `pixverse`.
  - `OPENCLAW_PROVIDER_INDEX` est délibérément un petit secours d'aperçu avec seulement les entrées Moonshot et DeepSeek dans la source actuelle.
  - Les tests en direct prouvent les chemins de fournisseurs sélectionnés, mais pas la parité docs/catalogue public pour toute la queue de fournisseurs hébergés.

## Score de qualité

- Score : `Alpha (61%)`
- Bonnes qualités :
  - Les métadonnées du manifeste gardent les docs des fournisseurs, les catalogues de modèles, les descripteurs de configuration, les métadonnées d'authentification, les contrats, et les métadonnées de génération facilement inspectables avant que l'exécution ne se charge.
  - La résolution du catalogue d'installation a une fusion explicite et un dédoublonnage entre les manifestes installés, les entrées officielles externes, et les lignes d'aperçu de l'index des fournisseurs.
  - Les docs disent clairement aux utilisateurs que les plugins de fournisseurs possèdent les catalogues, la cartographie des variables d'env d'authentification, la normalisation des demandes, la classification des basculements, l'actualisation OAuth, la déclaration d'utilisation, et les profils de raisonnement.
- Mauvaises qualités :
  - Les métadonnées sont fragmentées entre les manifestes, `scripts/lib/official-external-provider-catalog.json`, `OPENCLAW_PROVIDER_INDEX`, les modules de catalogue d'exécution spécifiques aux fournisseurs, et les docs maintenues manuellement.
  - La dérive docs/catalogue public est déjà observable dans cet audit.
  - L'historique des archives montre une confusion récurrente concernant l'identité des fournisseurs, le préfixe, le modèle obsolète, l'authentification, et l'enregistrement des fournisseurs de médias.
- Exclus de la qualité :
  - Les preuves unitaires, d'intégration et en direct ont été utilisées uniquement pour le score de couverture.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/long-tail-hosted-providers.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le répertoire de fournisseurs, le catalogue d'installation des fournisseurs, les métadonnées du catalogue de modèles, les vérifications de parité du catalogue.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une vérification de parité du répertoire de fournisseurs qui compare les liens de docs, les manifestes groupés, les entrées officielles du catalogue de fournisseurs externes, et les fichiers de docs de fournisseurs.
- Ajouter un artefact d'inventaire de fournisseurs généré pour les fournisseurs hébergés long-tail.
- Suivre la dérive du catalogue des fournisseurs comme une vérification explicite de fraîcheur de la fiche d'évaluation.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/index.md:25` : la liste publique de docs de fournisseurs commence par Alibaba, Bedrock, Bedrock Mantle, Anthropic, Arcee, Azure Speech, BytePlus, Cerebras, Chutes, Cloudflare AI Gateway, ComfyUI, DeepSeek, ElevenLabs, fal, Fireworks, GitHub Copilot, Google, Gradium, Groq, Hugging Face, Kilo, LiteLLM, MiniMax, Mistral, Moonshot, NVIDIA, OpenCode, OpenRouter, Qianfan, Qwen, Runway, SenseAudio, StepFun, Synthetic, Tencent, Together, Venice, Vercel AI Gateway, Volcengine, Vydra, xAI, Xiaomi, et Z.AI.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:80` : les pages d'aperçu partagées de génération d'images, de musique et de vidéo sont liées à partir du répertoire de fournisseurs.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:87` : les fournisseurs de transcription incluent Deepgram, ElevenLabs, Mistral, OpenAI, SenseAudio, et xAI.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:51` : la logique spécifique aux fournisseurs réside dans les plugins ; les plugins possèdent l'intégration, les catalogues, la cartographie des variables d'env d'authentification, la normalisation des demandes, la classification des basculements, l'actualisation OAuth, la déclaration d'utilisation, et les profils de raisonnement.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:291` : le tableau « Autres plugins de fournisseurs groupés » répertorie de nombreux fournisseurs long-tail, identifiants, variables d'env d'authentification, et modèles d'exemple.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:151` : les champs de niveau supérieur du manifeste incluent `providers`, `providerCatalogEntry`, `modelCatalog`, les points de terminaison des fournisseurs, les métadonnées de demande des fournisseurs, les variables d'env d'authentification des fournisseurs, les choix d'authentification des fournisseurs, la configuration, les contrats, et les métadonnées de génération.

### Source

- `/Users/kevinlin/code/openclaw/scripts/lib/official-external-provider-catalog.json:1` : le catalogue officiel externe des fournisseurs contient actuellement cinq entrées, notamment Bedrock, Bedrock Mantle, Anthropic Vertex, Codex, et PixVerse.
- `/Users/kevinlin/code/openclaw/src/model-catalog/provider-index/openclaw-provider-index.ts:3` : `OPENCLAW_PROVIDER_INDEX` est une métadonnée d'aperçu de secours ; les manifestes des plugins installés restent faisant autorité.
- `/Users/kevinlin/code/openclaw/src/model-catalog/provider-index/openclaw-provider-index.ts:12` : les entrées de fournisseurs d'aperçu actuelles sont Moonshot et DeepSeek.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-install-catalog.ts:213` : les entrées de l'index des fournisseurs sont construites uniquement pour les plugins de fournisseurs non installés avec des choix d'authentification.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-install-catalog.ts:278` : les entrées du catalogue officiel externe des fournisseurs sont normalisées dans les choix du catalogue d'installation des fournisseurs.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-install-catalog.ts:342` : le catalogue d'installation final des fournisseurs retourne les entrées du manifeste, les entrées externes officielles, et les entrées de l'index des fournisseurs triées ensemble.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts:572` : la couverture du flux de commande vérifie les lignes du catalogue des fournisseurs `models list --all` et l'exclusion du mode local.
- `/Users/kevinlin/code/openclaw/src/commands/models/list.list-command.forward-compat.test.ts:381` : les tests de compatibilité avant couvrent le manifeste, l'index des fournisseurs, le catalogue de fournisseurs statique, les chemins configurés/soutenus par l'authentification, et les chemins de liste filtrés par fournisseur.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:58` : les docs de fumée du modèle en direct divisent la preuve directe du fournisseur/modèle de la fumée Gateway+agent.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:372` : les docs de matrice de modèle en direct disent explicitement qu'il n'y a pas de liste de modèles CI fixe.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/provider-install-catalog.test.ts:559` : la couverture unitaire vérifie les métadonnées officielles d'installation du catalogue externe des fournisseurs.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-discovery.runtime.test.ts:160` : la couverture unitaire vérifie les entrées de découverte statique et le secours borné.
- `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.test.ts:1415` : la couverture unitaire vérifie la source de chemin du catalogue des fournisseurs de manifeste par secours et le renforcement des limites racine.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "long-tail hosted providers provider metadata"` a retourné `[]`.
- `gitcrawl --json search prs -R openclaw/openclaw "provider metadata model catalog"` a retourné les RP de métadonnées/catalogue de fournisseurs incluant #84581, #84902, #84997, #84566, #75022, #85345, #67579, #83292, #69729, #86670, et #43493.
- La requête d'assistance `models list provider catalog` a trouvé un historique large de catalogue dynamique et de catalogue obsolète, incluant #10687, #74481, #74986, #81216, et #87746.
- La requête d'assistance `NVIDIA provider catalog model prefix` a trouvé #81525, un risque de non-concordance préfixe/catalogue de fournisseur.

### Requêtes Discrawl

- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "long-tail hosted provider metadata" --limit 5` a retourné `null`.
- La requête d'assistance `DeepInfra provider catalog` a retourné l'historique de publication/révision concernant la découverte sans authentification, le secours de préservation d'ordre, la récupération en direct dupliquée, et la navigation du catalogue consciente des identifiants.
- La requête d'assistance `Chutes provider catalog` a retourné l'historique de révision concernant les résultats partiels du chemin rapide, l'authentification synthétique causant des appels de catalogue en direct, les identifiants contenant des barres obliques, la découverte des plugins, et la précédence de l'authentification.
- La requête d'assistance `Venice provider catalog OpenClaw` a retourné l'historique de dérive de liste d'autorisation/découverte de modèle obsolète et de non-concordance du catalogue de support d'outils.
