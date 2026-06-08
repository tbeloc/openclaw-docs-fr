---
title: "Rapport de Maturité ClawHub"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité ClawHub

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Beta (72%)`
- Qualité : `Beta (73%)`
- Complétude : `Beta (72%)`
- Fonctionnalités LTS : `0/4`

## Résumé

Ce rapport promeut les preuves de maturité archivées `clawhub-and-external-plugin-distribution` de `/Users/kevinlin/tmp/maturity/clawhub-and-external-plugin-distribution` dans le contrat d'inventaire process-version-3 actuel.

Les scores de catégorie Couverture et Qualité proviennent des lignes de score soutenues par les preuves archivées. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                        | LTS | Couverture    | Qualité      | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------- | --- | ------------- | ------------ | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Publication](clawhub-and-npm-publishing-release-validation.md)                  | ❌  | `Beta (72%)`  | `Beta (76%)` | `Beta (72%)`  | Propriétaire de publication de paquet ClawHub, Validation de version de paquet détenu par OpenClaw pour ClawHub, Portes de bump de version, Provenance de publication de confiance npm, Contrat de paquet de plugin de code externe requis, Métadonnées de paquet de compétence, Flux de publication de compétence                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Découverte du Catalogue](clawhub-discovery-catalog-metadata-and-package-lookup.md)   | ❌  | `Alpha (66%)` | `Beta (72%)` | `Alpha (66%)` | Recherche de plugins openclaw en tant que ClawHub, Métadonnées des résultats de recherche, Distinction entre recherche de plugin, Échec de recherche de catalogue, Recherche de catalogue de compétence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Compatibilité et Confiance](compatibility-gates-and-official-external-catalog.md) | ❌  | `Beta (76%)`  | `Beta (74%)` | `Beta (76%)`  | openclaw.compat.pluginApi, Validation de compatibilité de paquet ClawHub, Secours de compatibilité npm vers le plus récent, Comportement du catalogue de plugin externe officiel, Documentation de compatibilité, Modèle de confiance de l'opérateur pour l'installation, Archive ClawHub, Dérive d'intégrité npm, Analyseur de code dangereux intégré, Comportement de révision/version cachée de publication ClawHub en amont, Sécurité de l'archive de compétence, Signaux d'audit de compétence                                                                                                                                                                                                                                                        |
| [Cycle de Vie et Santé du Plugin](plugin-lifecycle-and-health.md)                   | ❌  | `Beta (76%)`  | `Beta (71%)` | `Beta (76%)`  | Préfixes source, Comportement de paquet nu lors du lancement, Versions épinglées explicites, Enregistrements d'installation gérés qui préservent la source, Codex, Local, Liste Marketplace, Fonctionnalités mappées prises en charge, Sécurité du chemin de marketplace distant, Mise à jour par identifiant de plugin, Sémantique de réinstallation par rapport à la mise à jour, Rétrogradation, Nettoyage de config/index/policy/file de désinstallation, Exigences de redémarrage/rechargement de passerelle après, Projet npm géré par plugin, Installations de candidat à la version locale npm-pack, Propriété des dépendances entre paquets de plugin, Reliaison des dépendances homologues, Nettoyage racine des dépendances héritées, Liste des plugins, Index de plugin local, Dépannage de la configuration obsolète, Vérification d'exécution après passerelle, Installations de compétence ClawHub, Chemin d'installation de téléchargement de compétence, Installateurs de dépendance de compétence |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, live, ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et de flux runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement
  l'ensemble de capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Publication

Ancres de recherche : publication clawhub validation de version, publication clawhub et npm validation de version, format SKILL.md, métadonnées d'exécution, flux de version, contenu de compétence.

Note de catégorie : [Publication](clawhub-and-npm-publishing-release-validation.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Beta (76%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Propriétaire de publication de paquet ClawHub : Propriétaire de publication de paquet ClawHub et règles de portée
- Validation de version pour paquet détenu par OpenClaw pour ClawHub : Validation de version pour paquet détenu par OpenClaw pour ClawHub et npm
- Portes de changement de version : Portes de changement de version pour les plugins publiables modifiés
- Provenance de publication de confiance npm : Métadonnées de provenance de publication de confiance npm
- Contrat de paquet de plugin de code externe requis : Contrat de paquet de plugin de code externe requis avant la publication
- Métadonnées de paquet de compétence : Métadonnées prêtes pour la publication, limites de fichiers, versions et balises.
- Flux de publication de compétence : Publication de compétence ClawHub avec portée propriétaire, validation, version et examen.

Docs principaux :

- `docs/clawhub/publishing.md`
- `docs/clawhub/skill-format.md`
- `docs/tools/creating-skills.md`
- `docs/plugins/community.md`

### 2. Découverte du catalogue

Ancres de recherche : découverte clawhub, métadonnées du catalogue et recherche de paquet, compétences openclaw, installation et synchronisation ClawHub.

Note de catégorie : [Découverte du catalogue](clawhub-discovery-catalog-metadata-and-package-lookup.md)

Décisions de score :

- Couverture : `Alpha (66%)`
- Qualité : `Beta (72%)`
- Complétude : `Alpha (66%)`
- LTS : ❌

Fonctionnalités :

- Recherche de plugins openclaw en tant que ClawHub : Recherche de plugins openclaw en tant que commande de recherche de plugin ClawHub
- Métadonnées de résultat de recherche : nom de paquet, famille, canal, version, résumé et
- Distinction entre recherche de plugin : Distinction entre recherche de plugin et recherche de compétence
- Échec de recherche de catalogue : Échec de recherche de catalogue et comportement de résultat vide
- Recherche de catalogue de compétence : Rechercher, lister, inspecter et installer des compétences suivies par ClawHub à partir de l'interface de ligne de commande.

Docs principaux :

- `docs/tools/plugin.md`
- `docs/cli/plugins.md`
- `docs/cli/skills.md`
- `docs/tools/skills.md`
- `docs/plugins/community.md`

### 3. Compatibilité et confiance

Ancres de recherche : portes de compatibilité clawhub et catalogue externe officiel, portes de compatibilité et catalogue externe officiel, confiance de plugin externe clawhub, intégrité et approbations d'installation, confiance de plugin externe, intégrité et approbations d'installation, traiter les compétences tierces comme du code non fiable, skills.install.allowUploadedArchives, audits de sécurité ClawHub, compétences dynamiques.

Note de catégorie : [Compatibilité et confiance](compatibility-gates-and-official-external-catalog.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- openclaw.compat.pluginApi : openclaw.compat.pluginApi, métadonnées de construction et minimums d'hôte/passerelle
- Validation de compatibilité de paquet ClawHub : Portée de preuve pour la validation de compatibilité de paquet ClawHub.
- Secours de compatibilité npm à la version stable la plus récente : Secours de compatibilité npm à la version stable la plus récente compatible
- Comportement du catalogue de plugins externes officiel : Comportement du catalogue de plugins externes officiel et migration de regroupé à externe
- Docs de compatibilité : Docs de compatibilité et registre de dépréciation
- Modèle de confiance d'opérateur pour l'installation : Modèle de confiance d'opérateur pour l'installation et l'activation de code externe
- Archive ClawHub : Vérification de l'archive ClawHub et du résumé ClawPack
- Dérive d'intégrité npm : Dérive d'intégrité npm et vérifications d'installation gérées
- Analyseur de code dangereux intégré : Analyseur de code dangereux intégré et sémantique de remplacement d'urgence
- Comportement de révision/version cachée de publication ClawHub en tant que signal en amont : Comportement de révision/version cachée de publication ClawHub en tant que signal de confiance en amont
- Sécurité de l'archive de compétence : Les archives de compétence téléchargées sont contrôlées et réutilisent les protections d'extraction.
- Signaux d'audit de compétence : L'état d'audit ClawHub, le risque, les résultats et les métadonnées de confiance s'appliquent aux paquets de compétence.

Docs principaux :

- `docs/tools/plugin.md`
- `docs/cli/plugins.md`
- `docs/plugins/compatibility.md`
- `docs/plugins/plugin-inventory.md`
- `docs/clawhub/publishing.md`
- `docs/clawhub/security-audits.md`
- `docs/tools/skills.md`
- `docs/tools/skills-config.md`

### 4. Cycle de vie et santé du plugin

Ancres de recherche : sélection de source de plugin clawhub et résolution de spécification d'installation, sélection de source de plugin et résolution de spécification d'installation, support d'importation de paquet compatible et marché clawhub, support d'importation de paquet compatible et marché, cycle de vie de mise à jour, restauration, désinstallation et rechargement de passerelle clawhub, mise à jour, restauration, désinstallation et rechargement de passerelle, résolution de dépendance clawhub, racines d'installation gérées et métadonnées de paquet, résolution de dépendance, racines d'installation gérées et métadonnées de paquet, inventaire d'opérateur clawhub, inspection, diagnostic et dépannage, inventaire d'opérateur, inspection, diagnostic et dépannage, skills.upload.begin, skills.install, skills.update, contenu de compétence.

Note de catégorie : [Cycle de vie et santé du plugin](plugin-lifecycle-and-health.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Préfixes de source : Préfixes de source et résolution abrégée pour clawhub:, npm:,
- Comportement de paquet nu lors du basculement de lancement : Comportement de paquet nu lors du basculement de lancement
- Versions épinglées explicites : Versions épinglées explicites, balises de préversion et comportement de secours stable
- Enregistrements d'installation gérés qui préservent la source : Enregistrements d'installation gérés qui préservent les métadonnées de source pour mise à jour/désinstallation
- Détection de paquet compatible Codex, Claude et Cursor : Détection de paquet compatible Codex, Claude et Cursor
- Chemins locaux, d'archive et de marché : Chemins locaux, d'archive et de marché
- Liste de marché : Liste de marché, raccourci et flux d'installation
- Fonctionnalités mappées prises en charge : Fonctionnalités mappées prises en charge et capacités détectées mais non exécutées
- Sécurité du chemin de marché distant : Sécurité du chemin de marché distant et gardes de téléchargement d'archive
- Mise à jour par id de plugin : Mise à jour par id de plugin, spécification npm, spécification ClawHub, canal bêta et marché
- Sémantique de réinstallation par rapport à mise à jour : Portée de preuve pour la sémantique de réinstallation par rapport à mise à jour.
- Rétrogradation : Rétrogradation et sélecteurs épinglés
- Nettoyage de config/index/politique/fichier de désinstallation : Portée de preuve pour le nettoyage de config/index/politique/fichier de désinstallation.
- Exigences de redémarrage/rechargement de passerelle après : Exigences de redémarrage/rechargement de passerelle après installation/mise à jour/désinstallation
- Racines de projet npm gérées par plugin : Racines de projet npm gérées par plugin
- Installations de candidat à la version locale npm-pack : Installations de candidat à la version locale npm-pack via sémantique npm
- Propriété de dépendance entre paquets de plugin : Propriété de dépendance entre paquets de plugin et OpenClaw
- Reliaison de dépendance pair : Reliaison de dépendance pair pour openclaw/plugin-sdk/\*
- Nettoyage de racine de dépendance héritée : Nettoyage de racine de dépendance héritée et réparation de diagnostic
- Liste de plugins : Liste de plugins, inspection de plugins, inspection d'exécution, diagnostic de plugins et
- Index de plugin local : Index de plugin local et état de registre froid persistant
- Dépannage de config obsolète : Dépannage de config obsolète, chemins bloqués, dépendances, plugins manquants,
- Vérification d'exécution après redémarrage de passerelle : Vérification d'exécution après redémarrage de passerelle
- Installations de compétence ClawHub : Installer et mettre à jour les compétences d'espace de travail ou globales suivies par ClawHub.
- Chemin d'installation de téléchargement de compétence : Téléchargement d'archive privée de confiance et installation via les API de téléchargement de compétence.
- Installateurs de dépendance de compétence : Installateurs Brew, Node, Go, uv ou téléchargement déclarés pour les paquets de compétence.

Docs principaux :

- `docs/tools/plugin.md`
- `docs/cli/plugins.md`
- `docs/cli/skills.md`
- `docs/tools/skills.md`
- `docs/gateway/protocol.md`
- `docs/plugins/bundles.md`
- `docs/plugins/dependency-resolution.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, les docs et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/clawhub-and-external-plugin-distribution/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuve archivée :
  `/Users/kevinlin/tmp/maturity/clawhub-and-external-plugin-distribution`.
