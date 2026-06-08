---
title: "Outils de génération d'images/vidéos/musique - Note de maturité de la génération vidéo"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Note de maturité de la génération vidéo

## Résumé

Le runtime vidéo partagé dispose d'un contrat de requête solide. Il supporte
les modes texte-vers-vidéo, image-vers-vidéo et vidéo-vers-vidéo ; les références d'image, vidéo et audio ;
la validation des rôles ; les limites de durée ; la normalisation du rapport d'aspect et de la résolution ; les contrôles d'audio généré et de filigrane ; les options de fournisseur typées ;
et l'omission de fournisseur lorsqu'un modèle ne peut pas accepter en toute sécurité le média demandé.

La couverture est Stable car la documentation et le code source couvrent le contrat de mode en détail,
avec validation du runtime et tests de contrat de capacité du fournisseur. La qualité est Beta
car le comportement de normalisation est prudent, mais l'expérience de l'opérateur peut toujours
être surprenante lorsque chaque fournisseur est omis en raison de contraintes de type de média ou d'option de fournisseur.

## Portée de la catégorie

Inclus dans cette catégorie :

- texte-vers-vidéo : Couvre texte-vers-vidéo dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- image-vers-vidéo : Couvre image-vers-vidéo dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- vidéo-vers-vidéo : Couvre vidéo-vers-vidéo dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- validation du rôle de référence : Couvre la validation du rôle de référence dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- références audio : Couvre les références audio dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- providerOptions typées : Couvre les providerOptions typées dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- tâches soutenues par une file d'attente : Couvre les tâches soutenues par une file d'attente dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- gestion de l'interrogation/délai d'expiration : Couvre la gestion de l'interrogation/délai d'expiration dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- téléchargement d'URL hébergée : Couvre le téléchargement d'URL hébergée dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- explications d'omission de fournisseur : Couvre les explications d'omission de fournisseur dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- métadonnées d'actif retournées : Couvre les métadonnées d'actif retournées dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.

## Fonctionnalités

- texte-vers-vidéo : Couvre texte-vers-vidéo dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- image-vers-vidéo : Couvre image-vers-vidéo dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- vidéo-vers-vidéo : Couvre vidéo-vers-vidéo dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- validation du rôle de référence : Couvre la validation du rôle de référence dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- références audio : Couvre les références audio dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- providerOptions typées : Couvre les providerOptions typées dans la normalisation des requêtes de génération vidéo avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et comportement des modes de génération vidéo associés.
- tâches soutenues par une file d'attente : Couvre les tâches soutenues par une file d'attente dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- gestion de l'interrogation/délai d'expiration : Couvre la gestion de l'interrogation/délai d'expiration dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- téléchargement d'URL hébergée : Couvre le téléchargement d'URL hébergée dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- explications d'omission de fournisseur : Couvre les explications d'omission de fournisseur dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.
- métadonnées d'actif retournées : Couvre les métadonnées d'actif retournées dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et fournisseurs vidéo associés et comportement d'interrogation.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La documentation décrit les modes, les références, la validation, la normalisation, les options de fournisseur et le comportement de secours ; le code source du runtime valide les options typées et ignore les candidats incompatibles.
- Signaux négatifs : Le contrat est suffisamment large pour que la couverture de chaque combinaison d'entrée de média, liste de rôles et option spécifique au fournisseur reste inégale.
- Lacunes d'intégration : Ajouter une matrice de bout en bout qui exerce texte uniquement, référence d'image, référence vidéo, référence audio, options de fournisseur typées invalides et explications d'omission de tous les fournisseurs.

## Score de qualité

- Score : `Beta (71%)`
- Rapports Gitcrawl : La recherche vidéo a retourné des problèmes où le modèle/config accepté a échoué plus tard au runtime et où la génération vidéo OpenRouter a échoué silencieusement.
- Rapports Discrawl : La recherche Discord a trouvé un échec de génération vidéo où plusieurs fournisseurs ont été omis car la requête incluait des entrées audio de référence non supportées.
- Bonnes qualités : Le runtime évite de supprimer silencieusement les entrées de référence incompatibles et enregistre les candidats omis avec les raisons.
- Mauvaises qualités : L'omission de fournisseur est correcte mais peut être opaque ; un utilisateur peut fournir une invite et des références plausibles mais ne recevoir aucune tentative de fournisseur réussie.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : les docs archivées, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour texte-vers-vidéo, image-vers-vidéo, vidéo-vers-vidéo, validation du rôle de référence, références audio, providerOptions typées, tâches soutenues par file d'attente, gestion de l'interrogation/délai d'expiration, téléchargement d'URL hébergée, explications d'omission de fournisseur, métadonnées d'actif retournées.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les raisons d'omission de fournisseur ont besoin d'une synthèse plus claire orientée vers l'utilisateur.
- Le support des références audio est particulièrement inégal entre les fournisseurs vidéo.
- Les options de fournisseur typées protègent les fournisseurs des mauvaises entrées, mais elles augmentent également le nombre de façons dont une requête peut échouer avant que la génération ne commence.

# Génération vidéo

## Modes

La génération vidéo supporte trois modes :

<Tabs>
  <Tab title="generate">
Génère une vidéo à partir d'une invite textuelle.
  </Tab>
  <Tab title="imageToVideo">
Génère une vidéo à partir d'une image de référence et d'une invite textuelle.
  </Tab>
  <Tab title="videoToVideo">
Génère une vidéo à partir d'une vidéo de référence et d'une invite textuelle.
  </Tab>
</Tabs>

## Capacités des fournisseurs

Chaque fournisseur de génération vidéo déclare les modes qu'il supporte et les paramètres optionnels disponibles pour chaque mode. Les capacités en direct sont documentées dans les [voies en direct](/fr/docs/tools/video-generation#live-lanes).

## Paramètres

### Paramètres de base

<Accordion title="prompt">
L'invite textuelle décrivant la vidéo à générer.

**Type :** `string`

**Requis :** Oui
</Accordion>

<Accordion title="mode">
Le mode de génération vidéo à utiliser.

**Type :** `"generate" | "imageToVideo" | "videoToVideo"`

**Requis :** Oui
</Accordion>

### Paramètres de référence

<Accordion title="referenceImage">
L'image de référence pour le mode `imageToVideo`.

**Type :** `string` (URL ou chemin de fichier)

**Requis :** Oui pour `imageToVideo`, Non pour les autres modes
</Accordion>

<Accordion title="referenceVideo">
La vidéo de référence pour le mode `videoToVideo`.

**Type :** `string` (URL ou chemin de fichier)

**Requis :** Oui pour `videoToVideo`, Non pour les autres modes
</Accordion>

<Accordion title="referenceAudio">
L'audio de référence pour synchroniser avec la vidéo générée.

**Type :** `string` (URL ou chemin de fichier)

**Requis :** Non
</Accordion>

<Accordion title="role">
Le rôle ou le personnage à utiliser dans la vidéo générée.

**Type :** `string`

**Requis :** Non
</Accordion>

### Contrôles de style

<Accordion title="style">
Le style visuel à appliquer à la vidéo générée.

**Type :** `string`

**Requis :** Non
</Accordion>

<Accordion title="duration">
La durée de la vidéo générée en secondes.

**Type :** `number`

**Requis :** Non

**Remarque :** Certains fournisseurs ont des limites de durée maximale qui seront appliquées.
</Accordion>

### Options avancées

<Accordion title="timeout">
Le délai d'attente en millisecondes pour la génération vidéo.

**Type :** `number`

**Requis :** Non

**Par défaut :** Délai d'attente par défaut du fournisseur
</Accordion>

<Accordion title="providerOptions">
Options spécifiques au fournisseur pour affiner le comportement de génération.

**Type :** `object`

**Requis :** Non

**Remarque :** Les options fournisseur sont validées par rapport au schéma du fournisseur sélectionné. Les options incompatibles avec le fournisseur ou le mode sélectionné seront ignorées.
</Accordion>

## Sélection du fournisseur

Le système de génération vidéo sélectionne automatiquement un fournisseur compatible en fonction de :

1. **Mode requis** : Le fournisseur doit supporter le mode spécifié (`generate`, `imageToVideo`, ou `videoToVideo`)
2. **Entrées de référence** : Le fournisseur doit supporter les entrées de référence fournies (image, vidéo, audio)
3. **Options du fournisseur** : Les options spécifiées doivent être compatibles avec le fournisseur
4. **Durée** : La durée demandée doit être dans les limites du fournisseur

Si plusieurs fournisseurs sont compatibles, le premier disponible sera utilisé. Si aucun fournisseur ne peut être trouvé, une erreur sera levée avec les détails des fournisseurs ignorés.

## Voies en direct

Les capacités en direct des fournisseurs de génération vidéo sont testées régulièrement. Consultez les résultats des tests pour voir quels fournisseurs et modes sont actuellement disponibles.

## Exemples

<Tabs>
  <Tab title="generate">
```javascript
const video = await client.video.generate({
  prompt: "Un chat dansant sur une plage au coucher du soleil",
  mode: "generate",
  duration: 5
});
```
  </Tab>
  <Tab title="imageToVideo">
```javascript
const video = await client.video.generate({
  prompt: "Le chat commence à danser",
  mode: "imageToVideo",
  referenceImage: "https://example.com/cat.jpg",
  duration: 5
});
```
  </Tab>
  <Tab title="videoToVideo">
```javascript
const video = await client.video.generate({
  prompt: "Rendre la vidéo plus dramatique avec des effets spéciaux",
  mode: "videoToVideo",
  referenceVideo: "https://example.com/video.mp4",
  duration: 5
});
```
  </Tab>
</Tabs>
