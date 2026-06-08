---
title: "ClawHub - Compatibility and Trust Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - Compatibility and Trust Maturity Note

## Résumé

La compatibilité est réelle mais encore en maturation. ClawHub, npm et les métadonnées de paquets externes comportent tous des portes de version d'API de plugin et d'hôte, et les plugins externes officiels peuvent être préférés aux copies intégrées lors de la migration. La surface est en Beta car les vérifications de compatibilité sont implémentées sur plusieurs chemins, mais les preuves d'archive montrent un travail actif pour aligner les installations directes de paquets avec la même sémantique de compatibilité ClawHub et pour maintenir les replis de catalogue officiels prévisibles.

## Portée de la catégorie

Inclus dans cette catégorie :

- openclaw.compat.pluginApi : openclaw.compat.pluginApi, métadonnées de construction et minimums d'hôte/passerelle
- Validation de compatibilité des paquets ClawHub : Portée des preuves pour la validation de compatibilité des paquets ClawHub.
- Repli de compatibilité npm vers la version la plus récente : Repli de compatibilité npm vers la version stable la plus récente compatible
- Comportement du catalogue officiel de plugins externes : Comportement du catalogue officiel de plugins externes et migration intégrée vers externe
- Docs de compatibilité : Docs de compatibilité et registre d'obsolescence
- Modèle de confiance de l'opérateur pour l'installation : Modèle de confiance de l'opérateur pour l'installation et l'activation de code externe
- Archive ClawHub : Archive ClawHub et vérification du résumé ClawPack
- Dérive d'intégrité npm : Dérive d'intégrité npm et vérifications d'installation gérées
- Analyseur de code dangereux intégré : Analyseur de code dangereux intégré et sémantique de remplacement d'urgence
- Comportement d'examen de publication/version cachée ClawHub en amont : Comportement d'examen de publication/version cachée ClawHub en amont comme signal de confiance

## Fonctionnalités

- openclaw.compat.pluginApi : openclaw.compat.pluginApi, métadonnées de construction et minimums d'hôte/passerelle
- Validation de compatibilité des paquets ClawHub : Portée des preuves pour la validation de compatibilité des paquets ClawHub.
- Repli de compatibilité npm vers la version la plus récente : Repli de compatibilité npm vers la version stable la plus récente compatible
- Comportement du catalogue officiel de plugins externes : Comportement du catalogue officiel de plugins externes et migration intégrée vers externe
- Docs de compatibilité : Docs de compatibilité et registre d'obsolescence
- Modèle de confiance de l'opérateur pour l'installation : Modèle de confiance de l'opérateur pour l'installation et l'activation de code externe
- Archive ClawHub : Archive ClawHub et vérification du résumé ClawPack
- Dérive d'intégrité npm : Dérive d'intégrité npm et vérifications d'installation gérées
- Analyseur de code dangereux intégré : Analyseur de code dangereux intégré et sémantique de remplacement d'urgence
- Comportement d'examen de publication/version cachée ClawHub en amont : Comportement d'examen de publication/version cachée ClawHub en amont comme signal de confiance
- Sécurité de l'archive de compétences : Les archives de compétences téléchargées sont contrôlées et réutilisent les protections d'extraction.
- Signaux d'audit de compétences : L'état d'audit ClawHub, le risque, les résultats et les métadonnées de confiance s'appliquent aux paquets de compétences.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : les docs et sources couvrent les plages d'API de plugin, les versions minimales de passerelle, la validation du contrat de paquet, le repli de version compatible npm et la migration officielle de plugins externes.
- Signaux négatifs : les preuves d'archive GitHub montrent un écart de compatibilité récent dans les installations directes de paquets, et il n'existe pas de matrice unique en direct pour la compatibilité ClawHub, npm et repli intégré.
- Lacunes d'intégration : la source du catalogue officiel, le repli et les vérifications de compatibilité nécessitent une porte d'installation de paquet sur les lignes de paquet stable, bêta, exact et incompatible.

## Score de qualité

- Score : `Beta (74%)`
- Bonnes qualités : les défaillances de compatibilité sont explicites et exploitables, les champs de contrat de paquet externe sont normalisés, et le repli npm recherche les versions stables plus anciennes au lieu d'installer aveuglément une version la plus récente incompatible.
- Mauvaises qualités : la politique de compatibilité est divisée entre les métadonnées ClawHub, les métadonnées package.json, les métadonnées npm et la propriété du catalogue officiel, créant un risque de dérive.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et flux d'exécution ne sont comptabilisées que sous Couverture, pas Qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour openclaw.compat.pluginApi, validation de compatibilité des paquets ClawHub, repli de compatibilité npm vers la version la plus récente, comportement du catalogue officiel de plugins externes, docs de compatibilité, modèle de confiance de l'opérateur pour l'installation, archive ClawHub, dérive d'intégrité npm, analyseur de code dangereux intégré, comportement d'examen de publication/version cachée ClawHub en amont, sécurité de l'archive de compétences, signaux d'audit de compétences.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Consolider le comportement de compatibilité d'installation directe npm/paquet avec le comportement de compatibilité ClawHub.
- Publier un petit ensemble de fixtures de compatibilité pour les cas d'API de plugin plus ancien, même étage bêta, plus récent, minimum d'hôte plus récent et métadonnées manquantes.

## Preuves

### Docs

- `docs/tools/plugin.md:139` : les installations npm se replient sur la version stable compatible la plus récente lorsque la version la plus récente nécessite un hôte plus récent.
- `docs/cli/plugins.md:180` : repli de compatibilité d'installation npm et comportement strict exact/tag.
- `docs/plugins/compatibility.md:15` : le registre de compatibilité suit le code stable, l'état, le propriétaire, les dates, le remplacement, les docs et les tests.
- `docs/plugins/plugin-inventory.md:141` : l'inventaire officiel des paquets externes répertorie les plugins distribués npm/ClawHub.

### Source

- `packages/plugin-package-contract/src/index.ts:20` : les paquets de plugins de code externe nécessitent `openclaw.compat.pluginApi` et `openclaw.build.openclawVersion`.
- `packages/plugin-package-contract/src/index.ts:46` : normalise les métadonnées de compatibilité de l'API de plugin, du minimum de passerelle, de la construction et du SDK.
- `src/plugins/install.ts:145` : valide la compatibilité de l'API de plugin du paquet.
- `src/plugins/install.ts:170` : valide la compatibilité du minimum d'hôte du paquet.
- `src/plugins/clawhub.ts:963` : rejette la famille de paquets ClawHub incompatible, le canal, l'API de plugin et les minimums de passerelle.

### Tests d'intégration

- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:41` : le chemin d'installation d'installation de paquet exerce les paquets de fixtures npm compatibles.
- Aucune matrice de compatibilité du catalogue officiel ClawHub/npm en direct n'a été trouvée.

### Tests unitaires

- `src/plugins/clawhub.test.ts:807` : installe lorsque ClawHub annonce une plage d'API de plugin générique.
- `src/plugins/clawhub.test.ts:832` : accepte un runtime de correction CalVer qui satisfait la plage d'API de plugin de base.
- `src/plugins/clawhub.test.ts:858` : accepte un runtime bêta sur le même étage d'API de plugin.
- `src/plugins/clawhub.test.ts:884` : rejette la compatibilité de runtime invalide cachée par une plage d'API de plugin générique.
- `test/plugin-npm-release.test.ts:207` : nécessite le contrat de compatibilité du paquet de plugin externe pour la publication npm.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "plugin compatibility ClawHub npm release" --limit 5 --json`

Résultats :

- A retourné #87477, qui aligne les installations directes de paquets avec les vérifications de compatibilité de l'API de plugin ClawHub.
- A retourné #81957, qui note qu'aucune publication npm en direct, mutation npm dist-tag, publication ClawHub, publication de version ou exécution de passerelle de production n'a été vérifiée dans ce contexte de durcissement de la chaîne d'approvisionnement.
- A retourné #75186, qui note que l'installation/mise à jour/désinstallation npm/ClawHub en direct n'a pas été vérifiée pour les RPC de gestion de plugins.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "plugin compatibility ClawHub npm release"`

Résultats :

- A retourné une discussion de mainteneur du 2026-05-07 sur l'inadéquation de propriété ClawHub/plugin et la propriété du manifeste de registre, plus des notes bêta du 2026-05-05 mentionnant les commutateurs de source npm/ClawHub et la réparation officielle de plugins externalisée.
