---
title: Plugins - Canvas Plugin Maturity Note
version: 3
last_refreshed: 2026-06-04
last_refreshed_by: codex
---

# Plugins - Canvas Plugin Maturity Note

## Résumé

Canvas est mieux présenté comme un plugin groupé expérimental qui possède un ensemble de capacités connexes : routes Canvas/A2UI hébergées, l'outil agent `canvas`, commandes de nœud, intégrations Control UI, matérialisation de documents hébergés, snapshots et transport A2UI. La couverture est `Beta` car le dépôt dispose de sources concrètes et de documentation pour la famille de fonctionnalités, mais les preuves restent au niveau des entrées de plugin et des composants plutôt qu'une promesse de support de version complète. La qualité est `Alpha` car la fonctionnalité est explicitement expérimentale et dépend de plusieurs chemins d'hôte, de nœud et d'intégration qui restent alignés.

## Portée de la catégorie

- Cette catégorie couvre le plugin Canvas groupé en tant que famille de fonctionnalités, pas un comportement unique et étroit.
- Cette catégorie couvre les routes Canvas/A2UI Gateway hébergées, l'outil `canvas` orienté agent, les commandes `canvas.*` de nœud, les intégrations Control UI, les URL de documents hébergés, les snapshots et le transport A2UI.
- Hors de portée : les détails d'implémentation Canvas spécifiques à l'application native pour les nœuds macOS, iOS, Android ou Windows. Ceux-ci restent évalués dans les surfaces de plateforme pertinentes.

## Fonctionnalités

- Surfaces Canvas et A2UI hébergées : le plugin Canvas enregistre les routes HTTP et WebSocket Gateway authentifiées pour les documents Canvas hébergés et les surfaces d'exécution A2UI.
- Outil canvas agent : le plugin Canvas enregistre l'outil `canvas` orienté agent pour présenter, masquer, naviguer, évaluer, capturer des snapshots et contrôler A2UI.
- Commandes Canvas de nœud : le plugin Canvas possède la politique d'invocation de nœud pour les commandes `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot` et `canvas.a2ui.*`.
- Intégrations Control UI : la sortie de l'assistant peut intégrer les URL de documents Canvas hébergés dans les sessions Control UI et WebChat.
- Documents Canvas : le plugin Canvas matérialise les fichiers de documents hébergés et les URL `/__openclaw__/canvas/documents/...`.
- Transport A2UI et snapshots : le plugin Canvas regroupe le push A2UI, la réinitialisation et le transport JSONL avec la capture de snapshots et l'état Canvas rendu par nœud.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - `extensions/canvas/index.ts:45` définit Canvas comme une entrée de plugin groupé, et `docs/refactor/canvas.md:12` présente Canvas comme un plugin groupé expérimental plutôt qu'une fonctionnalité réservée à la plateforme.
  - `extensions/canvas/index.ts:82` enregistre les surfaces HTTP Canvas/A2UI hébergées, et `docs/gateway/configuration-reference.md:812` documente la surface de configuration Canvas/A2UI hébergée.
  - `extensions/canvas/index.ts:128` enregistre l'outil `canvas` orienté agent.
  - `extensions/canvas/index.ts:9` définit les commandes de nœud incluant `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot` et `canvas.a2ui.*`.
  - `src/agents/system-prompt.ts:428` documente les intégrations Control UI pour les documents Canvas hébergés.
  - `extensions/canvas/src/documents.ts:132` matérialise les URL d'entrée de document Canvas sous `/__openclaw__/canvas/documents/...`.
- Signaux négatifs :
  - La preuve la plus claire est l'alignement des sources et de la documentation. Cette note n'enregistre pas un test de fumée complet Gateway-plus-nœud-plus-intégration pour Canvas.
  - Canvas est toujours décrit comme expérimental, donc la catégorie ne doit pas être traitée comme un noyau de support LTS.
- Lacunes d'intégration :
  - Ajouter un test de fumée qui démarre la Gateway, charge le plugin Canvas groupé, sert une URL de document hébergée, l'intègre dans Control UI, invoque une commande de nœud appariée et vérifie les allers-retours snapshot/A2UI.

## Score de qualité

- Score : `Alpha (66%)`
- Bonnes qualités :
  - La propriété est concentrée dans une entrée de plugin unique au lieu d'être dispersée sur des surfaces de plateforme non liées.
  - Le plugin regroupe les routes d'hôte, l'enregistrement d'outils, les commandes de nœud, les URL de documents et le transport A2UI sous un espace de noms Canvas cohérent.
  - La documentation Gateway expose les opérateurs de limite URL/configuration que les opérateurs doivent comprendre pour raisonner sur le routage Canvas.
- Mauvaises qualités :
  - Le plugin reste expérimental et traverse plusieurs limites opérationnelles : authentification HTTP Gateway, disponibilité/premier plan du nœud, sortie d'intégration d'assistant, actifs de documents hébergés et transport de messages A2UI.
  - La préparation des applications spécifiques à la plateforme et la disponibilité des commandes de nœud affectent toujours si Canvas réussit en pratique, même si la propriété du plugin est claire.
  - Il n'existe pas d'artefact de support récurrent spécifique à la catégorie montrant que tous les sous-éléments fonctionnent ensemble.
- Exclus de la qualité :
  - La présence de sources et les tests augmentent uniquement la couverture ; ils ne relèvent pas par eux-mêmes la qualité.

## Score de complétude

- Score : `Beta (74%)`
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les surfaces Canvas et A2UI hébergées, l'outil canvas agent, les commandes Canvas de nœud, les intégrations Control UI, les documents Canvas, le transport A2UI et les snapshots.
- Signaux négatifs : la catégorie manque d'une limite de support utilisateur durcie et d'un artefact de validation récurrent pour toute la famille.
- Lacunes de complétude :
  - Documenter la matrice de sous-fonctionnalités Canvas supportées dans la page de référence Canvas publique.
  - Ajouter des conseils d'échec orientés opérateur pour la configuration d'hôte, la disponibilité des nœuds, l'accessibilité des URL de documents et les erreurs de transport A2UI.
