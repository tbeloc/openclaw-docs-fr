---
title: "ClawHub - Publishing Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - Publishing Maturity Note

## Résumé

La validation de la publication dispose de garde-fous sérieux : portée du propriétaire ClawHub, portée du package, portes de version, vérifications de propriété de package existant, provenance npm, format de version de publication, métadonnées publiables et champs de compatibilité des plugins externes. La couverture est Beta car les preuves de script et d'unité sont solides mais les preuves de publication en direct sont rares dans ce dépôt. La qualité est Beta car le modèle de validation est défendable, mais les preuves d'archive signalent les flux de publication/publication comme une lacune connue dans le renforcement de la chaîne d'approvisionnement et le câblage CI antérieur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Propriétaire de la publication du package ClawHub : règles de propriétaire et de portée de la publication du package ClawHub
- Validation de la publication du package détenu par OpenClaw pour ClawHub : validation de la publication du package détenu par OpenClaw pour ClawHub et npm
- Portes de bump de version : portes de bump de version pour les plugins publiables modifiés
- Provenance de publication de confiance npm : métadonnées de provenance de publication de confiance npm
- Contrat de package de plugin de code externe requis : contrat de package de plugin de code externe requis avant la publication

## Fonctionnalités

- Propriétaire de la publication du package ClawHub : règles de propriétaire et de portée de la publication du package ClawHub
- Validation de la publication du package détenu par OpenClaw pour ClawHub : validation de la publication du package détenu par OpenClaw pour ClawHub et npm
- Portes de bump de version : portes de bump de version pour les plugins publiables modifiés
- Provenance de publication de confiance npm : métadonnées de provenance de publication de confiance npm
- Contrat de package de plugin de code externe requis : contrat de package de plugin de code externe requis avant la publication
- Métadonnées du package de compétence : métadonnées prêtes pour la publication, limites de fichiers, versions et balises.
- Flux de publication de compétence : publication de compétence ClawHub à portée du propriétaire, validation, publication et examen.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : la documentation définit le comportement du propriétaire/portée/examen, les scripts de publication valident les métadonnées du package et les versions modifiées, et les tests couvrent les cas importants de plan de publication et de contrôle préalable à la publication.
- Signaux négatifs : la preuve d'archive GitHub note explicitement l'absence de npm en direct, de dist-tag, de publication ClawHub, de publication de publication et de preuve de Gateway de production dans un contexte de renforcement de la chaîne d'approvisionnement.
- Lacunes d'intégration : le dépôt OpenClaw ne prouve pas la boucle de publication, d'examen ClawHub, d'analyse, d'installation, de mise à jour et de restauration de bout en bout comme une seule porte.

## Score de qualité

- Score : `Beta (76%)`
- Bonnes qualités : la validation bloque les erreurs de métadonnées du package avant la publication, exige l'alignement du propriétaire, exige les métadonnées de compatibilité et exige les métadonnées du dépôt conviviales pour la provenance npm.
- Mauvaises qualités : la publication est divisée entre le comportement du serveur ClawHub, la CLI/documentation, les scripts de flux de travail GitHub, le comportement du registre npm et l'état de la branche de publication.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution ne sont comptabilisées que sous Couverture, pas Qualité.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le propriétaire de la publication du package ClawHub, la validation de la publication du package détenu par OpenClaw pour ClawHub, les portes de bump de version, la provenance de publication de confiance npm, le contrat de package de plugin de code externe requis, les métadonnées du package de compétence, le flux de publication de compétence.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve de publication en direct du changement de package via la publication cachée ClawHub, examen/vérification, installation et secours npm.
- Maintenir la mutabilité de la référence/extraction ClawHub et la propriété du jeton/des identifiants dans la liste de contrôle de publication jusqu'à ce que le flux soit entièrement déterministe.

## Preuves

### Documentation

- `docs/clawhub/publishing.md:11` : la publication ClawHub est à portée du propriétaire.
- `docs/clawhub/publishing.md:40` : la portée du package de plugin doit correspondre au propriétaire sélectionné.
- `docs/clawhub/publishing.md:56` : le flux de publication valide les métadonnées et masque les publications jusqu'à ce que l'examen et la vérification soient terminés.
- `docs/plugins/community.md:40` : ClawHub possède l'annonce en direct, l'historique des publications, l'état de l'analyse et les conseils d'installation.
- `docs/plugins/community.md:50` : la liste de contrôle de publication du plugin communautaire exige les métadonnées, le manifeste, la documentation de configuration et le propriétaire.

### Source

- `scripts/lib/plugin-clawhub-release.ts:101` : collecte les packages avec `publishToClawHub`.
- `scripts/lib/plugin-clawhub-release.ts:282` : exige des bumps de version lorsque les plugins publiables modifiés conservent la même version.
- `scripts/lib/plugin-clawhub-release.ts:353` : vérifie que les candidats à portée OpenClaw appartiennent à l'éditeur OpenClaw.
- `scripts/lib/plugin-clawhub-release.ts:406` : construit le plan de publication ClawHub.
- `scripts/lib/plugin-npm-release.ts:225` : valide les métadonnées du plugin publiable npm, l'URL de provenance, la portée du package, la spécification d'installation et le contrat de compatibilité.

### Tests d'intégration

- Aucune porte d'intégration de publication en direct, d'examen ClawHub, d'analyse, d'installation et de mise à jour n'a été trouvée.

### Tests unitaires

- `test/plugin-clawhub-release.test.ts:58` : exige le contrat de plugin externe ClawHub.
- `test/plugin-clawhub-release.test.ts:164` : exige un bump de version lorsqu'un plugin publiable change.
- `test/plugin-clawhub-release.test.ts:373` : exige que les candidats à la publication à portée OpenClaw appartiennent à l'éditeur OpenClaw.
- `test/plugin-clawhub-release.test.ts:417` : prévisualise la commande de publication via le contrôle préalable à la publication du test à sec de la CLI ClawHub.
- `test/plugin-npm-release.test.ts:158` : exige l'URL du dépôt GitHub de provenance npm.
- `test/plugin-npm-release.test.ts:183` : exige les métadonnées d'installation npm pour les plugins publiables.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "clawhub release plugin publish" --limit 5 --json`

Résultats :

- A retourné #81957, un fil de discussion sur le renforcement de la chaîne d'approvisionnement qui a supprimé la solution de secours du jeton ClawHub et a déclaré qu'aucune publication npm en direct, mutation de dist-tag npm, publication ClawHub, publication de publication ou exécution de Gateway de production n'a été effectuée.
- A retourné #71116, un problème de gouvernance des identifiants mentionnant les flux de travail de publication ClawHub et npm du plugin.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "ClawHub publish npm plugin release"`

Résultats :

- A retourné une note de PR du 2026-04-01 sur l'ajout d'un flux de travail de publication de plugin ClawHub, avec une mise en garde concernant les références de récupération ClawHub mutables, et une note du responsable du 2026-03-23 selon laquelle le flux e2e complet de publication/mise à jour ClawHub fonctionnait pendant les perturbations CI.
