---
title: Processus de fiche de maturité
version: 3
---

# Processus de fiche de maturité

Ce répertoire est une racine d'artefact maintenue par la compétence locale `claw-score`
définie dans le fichier `SKILL.md` externe `claw-score`.

La compétence possède la politique de notation, le flux de travail de notation, la validation, la forme d'artefact,
et les attentes du moteur de rendu. Ce README est le contrat de répertoire orienté utilisateur
et l'aperçu du processus.

La disposition de la fiche de maturité de haut niveau est possédée par le modèle de compétence
`.agents/skills/claw-score/references/maturity-scorecard-template.md`, puis
rendu dans [maturity-scorecard.md](maturity-scorecard.md).

Opérationnellement, la compétence sépare trois flux de travail : maintenance de la taxonomie, calcul des scores,
et auto-maintenance de la compétence. Les instructions détaillées de l'agent
pour ceux-ci se trouvent dans les fichiers de référence de la compétence, pas dans ce README.

## Fichiers sources

- `taxonomy.yaml` est la source de vérité pour les surfaces, les niveaux de maturité,
  les identifiants de surface, les définitions de catégories, les valeurs `human_lts_override` de catégorie,
  les listes de lecture `docs` de catégorie, les `completeness_instructions` de surface, et
  la provenance `last_score_run` pour les surfaces actives dans le dépôt.
- `/Users/kevinlin/tmp/maturity/taxonomy.yaml` stocke la taxonomie archivée pour
  les autres surfaces qui sont temporairement hors du champ d'application actif du dépôt.
- `<artifact-root>/<surface>/scores.yaml` est la source de score par surface pour
  Coverage, Quality, Completeness, et l'identité de ligne (`name` et
  `category_note`). Le moteur de rendu joint les métadonnées de catégorie possédées par la taxonomie à partir de
  `taxonomy.yaml`. Les chemins d'artefact actifs sont dérivés par convention de nommage à partir
  de l'identifiant de surface de la taxonomie : `inventory/<surface-id>/report.md`,
  `inventory/<surface-id>/scores.yaml`, et `inventory/<surface-id>/<category-note>`.
  Les surfaces archivées historiques se trouvent à `/Users/kevinlin/tmp/maturity` et sont
  intentionnellement ignorées par les flux de travail normaux de rendu et de synchronisation `claw-score`.
- [maturity-scorecard.md](maturity-scorecard.md), [taxonomy.md](taxonomy.md),
  [taxonomy-outline.md](taxonomy-outline.md), et
  `<artifact-root>/<surface>/report.md` sont des artefacts Markdown rendus. Ne pas
  modifier manuellement leurs tableaux générés.

## Disposition du répertoire

```text
docs/kevinslin/maturity-scorecard/
├── README.md
├── taxonomy.md
├── taxonomy-outline.md
├── maturity-scorecard.md
└── inventory/
    ├── gateway-runtime/
    │   ├── report.md
    │   ├── <category>.md
    │   └── scores.yaml
    └── plugin-sdk-and-bundled-plugin-architecture/
        ├── report.md
        ├── <category>.md
        └── scores.yaml
```

Interprétez ces fichiers comme suit :

- `README.md` : aperçu du processus orienté utilisateur et contrat d'artefact.
- `taxonomy.md` : référence de taxonomie rendue générée à partir du YAML de taxonomie possédé par la compétence.
- `taxonomy-outline.md` : aperçu de surface rendu groupé par famille, généré
  à partir du YAML de taxonomie possédé par la compétence.
- [maturity-scorecard.md](maturity-scorecard.md) : fiche de maturité de haut niveau rendue générée à partir de la
  taxonomie possédée par la compétence.
- `inventory/` : racine d'artefact canonique pour le travail actif de fiche de maturité.
- `/Users/kevinlin/tmp/maturity` : emplacement d'archive pour les arbres d'artefacts historiques
  et le fichier de taxonomie archivé. Traitez-le comme hors du champ d'application sauf si
  vous restaurez explicitement le travail archivé.
- `<artifact-root>/<surface>/scores.yaml` : source de score par surface générée ou
  actualisée par la compétence.
- `<artifact-root>/<surface>/report.md` : rapport de surface rendu.
- `<artifact-root>/<surface>/<category>.md` : note de preuve par catégorie.

## Concepts

- `taxonomy` : le fichier YAML possédé par la compétence qui définit le modèle de maturité de haut niveau,
  l'inventaire de surface, les métadonnées de catégorie par surface, et l'état `last_score_run`.
- `scorecard` : l'aperçu Markdown de haut niveau rendu généré à partir de la
  taxonomie. Son tableau généré inclut les colonnes Coverage, Quality,
  Completeness, et LTS par surface dérivées de `scores.yaml` plus
  les métadonnées de taxonomie `human_lts_override`.
- `taxonomy doc` : la vue de référence Markdown rendue de la taxonomie,
  incluant l'inventaire de surface et les catégories par surface.
- `taxonomy outline` : l'aperçu Markdown rendu des surfaces actives groupées
  par famille.
- `surface` : une zone de produit ou de plateforme notée à partir de la taxonomie.
- `surface slug` : l'identifiant stable convivial pour le système de fichiers utilisé pour
  le répertoire d'inventaire d'une surface et les noms de fichiers.
- `artifact root` : le répertoire parent par surface sélectionné dans la convention de nommage de taxonomie.
  Le travail actif utilise actuellement `inventory/<surface-id>/` ;
  les surfaces archivées sont marquées dans la taxonomie avec `archived: true`.
- `category` : une partie importante orientée utilisateur ou opérateur d'une surface
  qui obtient sa propre note de preuve et ligne dans le YAML de score par surface. Une
  catégorie doit représenter une zone de capacité qu'un utilisateur peut réellement utiliser, pas
  un compartiment d'implémentation interne.
- `category note` : l'artefact de preuve Markdown par catégorie
  `<artifact-root>/<surface>/<category>.md`. Les notes incluent une section
  `## Features` dérivée de la taxonomie qui reflète la liste de fonctionnalités de catégorie à partir de
  `taxonomy.yaml`.
- `scores.yaml` : la source de score par surface canonique
  `<artifact-root>/<surface>/scores.yaml` ; elle stocke Coverage, Quality,
  Completeness, et l'identité de ligne, tandis que la taxonomie possède les fonctionnalités, les docs, les ancres de recherche,
  `human_lts_override`, et les `completeness_instructions` au niveau de la surface.
- `LTS.md` : tranche LTS initiale organisée manuellement. Ses lignes d'état doivent rester
  synchronisées avec les valeurs `human_lts_override` de la taxonomie et les cellules LTS de la matrice de rapport
  par surface rendue en exécutant
  `.agents/skills/claw-score/scripts/validate_lts_sync.py`.
- `completeness_instructions` : métadonnées de surface possédées par la taxonomie pointant vers un
  fichier de rubrique relatif à la compétence sous `.agents/skills/claw-score/` qui explique
  comment noter Completeness pour cette surface.
- `features` : métadonnées de catégorie possédées par la taxonomie stockées en tant qu'objets avec `name`
  et `description`. Gardez `name` court et scannable ; mettez l'explication plus complète
  dans `description`. Une fonctionnalité doit être une capacité invocable par l'utilisateur
  pour cette surface/catégorie, pas une étape de poignée de main ou autre
  détail d'implémentation uniquement.
- `docs` : métadonnées de catégorie possédées par la taxonomie listant les URL de doc relatives au dépôt qui
  couvrent le mieux la catégorie. Gardez ceci comme une courte liste de lecture principale, pas
  un vidage de preuve complet. Lors de la maintenance de la taxonomie, cette liste doit être choisie
  en scannant le corpus de docs OpenClaw pour la catégorie et en sélectionnant les
  pages canoniques qu'un examinateur doit ouvrir en premier.
- `surface report` : le rapport de surface Markdown rendu
  `<artifact-root>/<surface>/report.md`.

Les noms d'affichage de catégorie doivent être des noms de capacité courts et orientés opérateur.
Préférez moins de catégories plus grossières, fusionnez les concepts connexes qui partagent des docs et
des flux de travail opérateur, et gardez l'ancienne terminologie ou la terminologie lourde d'implémentation dans
`search_anchors`, les descriptions de fonctionnalités, ou les preuves plutôt que dans le nom d'affichage.

## Versioning

Les artefacts de fiche de maturité Markdown utilisent `version` en frontmatter pour le processus de notation
qui a produit ce document.

Lors d'une véritable rescore, le rapport de surface et les notes de catégorie doivent avoir
la frontmatter `version` égale à la `process_version` active de `scores.yaml`.

Les sources YAML utilisent :

- `version` : version de schéma pour la forme de fichier. Cela commence à `1`.
- `process_version` : version du processus de notation. Les exécutions de notation actuelles utilisent `3`.

Ne mettez pas à jour en masse la `last_score_run.process_version` par surface existante ou
la `process_version` de `scores.yaml` pour les modifications de rendu uniquement, de taxonomie uniquement, ou mécaniques de doc.
Mettez à jour la provenance de notation d'une surface lorsque cette surface est réellement
rescore avec des preuves actualisées.

## LTS

LTS est généré, pas noté par les agents de catégorie.

Le moteur de rendu marque une catégorie comme LTS lorsque l'une des conditions est vraie :

- `quality > 80 and coverage > 90`
- la catégorie de taxonomie correspondante définit `human_lts_override: true`

Gardez `human_lts_override` dans `taxonomy.yaml`. Ne l'écrivez pas dans
`scores.yaml`.

## Régénération

Utilisez les scripts de compétence à partir de la racine du dépôt :

```bash
python3 .agents/skills/claw-score/scripts/sync_taxonomy_categories.py \
  --taxonomy .agents/skills/claw-score/taxonomy.yaml \
  --scorecard-root docs/kevinslin/maturity-scorecard

python3 .agents/skills/claw-score/scripts/sync_scores_yaml.py \
  --taxonomy .agents/skills/claw-score/taxonomy.yaml \
  --scorecard-root docs/kevinslin/maturity-scorecard

python3 .agents/skills/claw-score/scripts/render_taxonomy_from_taxonomy.py \
  --taxonomy .agents/skills/claw-score/taxonomy.yaml \
  --taxonomy-doc docs/kevinslin/maturity-scorecard/taxonomy.md \
  --taxonomy-outline-doc docs/kevinslin/maturity-scorecard/taxonomy-outline.md

python3 .agents/skills/claw-score/scripts/render_scorecard_from_taxonomy.py \
  --taxonomy .agents/skills/claw-score/taxonomy.yaml \
  --scorecard docs/kevinslin/maturity-scorecard/maturity-scorecard.md
```

Utilisez le mode `--check` de chaque commande avant la remise lors de la vérification des artefacts.

Si les moteurs de rendu de la compétence, les scripts de synchronisation, ou les modèles changent, réexécutez les commandes
pertinentes ci-dessus et mettez à jour ce README dans le même changement lorsque le contrat d'artefact,
la terminologie, ou les conseils de régénération changent.

## Règles d'édition

- Pour la notation, la rescore, les audits, les modifications de taxonomie, la régénération de rapport, ou
  les modifications de forme de sortie, utilisez `claw-score`.
- Lors de la mise à jour de la compétence `claw-score` elle-même, mettez à jour les fichiers sources pertinents
  sous `.agents/skills/claw-score/` et gardez ce README aligné avec
  tout changement de contrat d'artefact, de terminologie, ou de régénération.
- Ne modifiez pas manuellement les tableaux générés ou les inventaires dans `taxonomy.md` ou
  `taxonomy-outline.md` ; réaffichez-les via les scripts de compétence.
- Ne modifiez pas manuellement les tableaux de score générés dans `maturity-scorecard.md` ou
  `<artifact-root>/<surface>/report.md` ; réaffichez-les via les scripts de compétence.
  Cela inclut les listes de fonctionnalités du rapport, qui sont rendues à partir de
  la taxonomie.
- Ne modifiez pas manuellement les sections `## Features` dérivées de la taxonomie dans les notes de catégorie ;
  mettez à jour `taxonomy.yaml` et réaffichez le rapport de surface propriétaire à la place.
- Gardez les instructions de l'agent dans le fichier `SKILL.md` externe `claw-score`, pas dans ce
  répertoire.
