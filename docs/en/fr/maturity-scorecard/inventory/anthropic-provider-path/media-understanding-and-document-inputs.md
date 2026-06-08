---
title: "Chemin du fournisseur Anthropic - Note de maturité des entrées médias"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Anthropic - Note de maturité des entrées médias

## Résumé

Le support des médias Anthropic est une partie plus petite et clairement délimitée du chemin du fournisseur. La documentation indique que le plugin Anthropic fourni enregistre la compréhension des images et des PDF, la source enregistre la capacité d'image avec les métadonnées natives d'entrée de document PDF, et les métadonnées du modèle normalisent les lignes Claude compatibles avec les images. La couverture est Beta car la source et la documentation sont claires mais la preuve de scénario média Anthropic en direct est plus mince que la preuve de transport texte/outil. La qualité est Stable car la surface est petite, directement mappée aux capacités du fournisseur, et la recherche d'archive n'a pas trouvé de rapports utilisateur spécifiques aux fonctionnalités après les vérifications de fraîcheur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Entrée d'image : Couvre l'entrée d'image dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.
- Entrée de document PDF : Couvre l'entrée de document PDF dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.
- Secours du modèle média : Couvre le secours du modèle média dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.
- Résultats d'outil d'image : Couvre les résultats d'outil d'image dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.

## Fonctionnalités

- Entrée d'image : Couvre l'entrée d'image dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.
- Entrée de document PDF : Couvre l'entrée de document PDF dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.
- Secours du modèle média : Couvre le secours du modèle média dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.
- Résultats d'outil d'image : Couvre les résultats d'outil d'image dans la compréhension des médias Anthropic dans le cadre du chemin du fournisseur : support d'entrée d'image, métadonnées natives d'entrée de document PDF, sélection de modèle média par défaut, auto-priorité, et comportement d'entrées médias connexes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : La documentation décrit la compréhension des images et des PDF ; le manifeste et la source du fournisseur enregistrent les métadonnées médias ; le transport direct convertit les blocs d'image ; les tests couvrent les métadonnées médias d'image et la conversion de charge utile de résultat d'outil d'image.
- Signaux négatifs : L'audit n'a pas trouvé d'artefact de scénario image/PDF Anthropic en direct dédié ou de résultat de fumée média par version.
- Lacunes d'intégration : Le support média est couvert davantage par l'enregistrement du fournisseur et les tests de charge utile que par les exécutions médias de bout en bout.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : La requête de problème GitHub spécifique à la fonctionnalité n'a retourné aucun rapport média Anthropic direct après les vérifications de fraîcheur.
- Rapports Discrawl : La requête Discord spécifique à la fonctionnalité n'a retourné aucun rapport média Anthropic direct après les vérifications de fraîcheur.
- Bonnes qualités : La capacité est petite, déclarative et alignée avec les métadonnées du modèle Claude moderne ; la source conserve les valeurs par défaut du modèle média et les métadonnées natives d'entrée de document dans une surface détenue par un seul plugin.
- Mauvaises qualités : La documentation dit compréhension des images et des PDF, tandis que la liste des capacités du fournisseur est `["image"]` plus `nativeDocumentInputs: ["pdf"]` séparé ; cette division peut nécessiter une formulation prudente à mesure que la documentation évolue.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ceux-ci sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/anthropic-provider-path.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'entrée d'image, l'entrée de document PDF, le secours du modèle média, les résultats d'outil d'image.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune preuve en direct dédiée d'image/PDF Anthropic n'a été trouvée dans cet audit.
- Le support PDF est représenté comme métadonnées natives d'entrée de document plutôt que comme un identifiant de capacité séparé.
- La génération de médias est hors de portée ; ce composant est la compréhension des médias uniquement.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente « Compréhension des médias (image et PDF) », modèle par défaut `claude-opus-4-7`, images d'entrée/documents PDF pris en charge, et routage automatique via le fournisseur de compréhension des médias Anthropic.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md` documente le comportement de redimensionnement d'image pour Claude Opus 4.7 et d'autres modèles de vision.

### Source

- `/Users/kevinlin/code/openclaw/extensions/anthropic/openclaw.plugin.json` déclare les métadonnées du fournisseur de compréhension des médias pour Anthropic avec la capacité `image`, le modèle d'image par défaut `claude-opus-4-7`, la priorité automatique `20`, et l'entrée de document natif `pdf`.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/media-understanding-provider.ts` enregistre `anthropicMediaUnderstandingProvider` avec les capacités d'image, les modèles par défaut, la priorité automatique, les entrées de documents natifs, et les assistants `describeImage`/`describeImages`.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/register.runtime.ts` normalise les modèles Claude modernes pour inclure l'entrée d'image et le dimensionnement d'entrée média spécifique au modèle.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.ts` convertit les blocs d'image utilisateur et les blocs de résultat d'outil d'image en contenu d'image Anthropic.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.ts` effectue la conversion d'image et de résultat d'outil côté transport pour les charges utiles Anthropic Messages.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` inclut le câblage du profil Anthropic en direct mais ne prouve pas en soi les scénarios image/PDF.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/anthropic/index.test.ts` couvre la normalisation obsolète de ligne de vision Claude moderne texte uniquement et la fusion de métadonnées médias pour `claude-opus-4-7`.
- `/Users/kevinlin/code/openclaw/src/agents/anthropic-transport-stream.test.ts` couvre la conversion de résultat d'outil d'image et la forme de charge utile d'image.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/model.provider-runtime.test-support.ts` définit les préfixes de modèle de vision Anthropic utilisés dans le support de test d'exécution du fournisseur.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic media image PDF Claude"`

Résultats :

- N'a retourné aucun résultat direct pour les rapports média/image/PDF Anthropic.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "Anthropic media understanding image PDF Claude"`

Résultats :

- N'a retourné aucun résultat direct pour les rapports média/image/PDF Anthropic.
