---
summary: "Liste de contrôle de planification et d'audit pour déplacer Canvas hors du cœur et dans un plugin expérimental fourni."
read_when:
  - Déplacement de la propriété Canvas host, tools, commands, docs ou protocol
  - Audit pour vérifier si Canvas est toujours détenu par le cœur
  - Préparation ou révision de la PR du plugin Canvas expérimental
title: "Refactorisation du plugin Canvas"
---

# Refactorisation du plugin Canvas

Canvas est peu utilisé et expérimental. Traitez-le comme un plugin fourni, pas comme une fonctionnalité principale. Le cœur peut conserver la plomberie générique de passerelle, nœud, HTTP, authentification, configuration et client natif, mais le comportement spécifique à Canvas doit se trouver sous `extensions/canvas`.

## Objectif

Transférer la propriété de Canvas à `extensions/canvas` tout en préservant le comportement actuel des nœuds appairés :

- l'outil `canvas` orienté agent est enregistré par le plugin Canvas
- Les commandes de nœud Canvas ne sont autorisées que lorsque le plugin Canvas les enregistre
- Les fichiers host/source A2UI résident sous le plugin Canvas
- La matérialisation des documents Canvas réside sous le plugin Canvas
- L'implémentation de la commande CLI réside sous le plugin Canvas, ou délègue via un barrel runtime détenu par le plugin
- Les docs et l'inventaire des plugins décrivent Canvas comme expérimental et soutenu par un plugin

## Non-objectifs

- Ne pas redessiner l'interface utilisateur Canvas de l'application native dans cette refactorisation.
- Ne pas supprimer le support du protocole/client Canvas de iOS, Android ou macOS sauf si une décision produit distincte indique que Canvas doit être supprimé.
- Ne pas construire un large cadre de service de plugin uniquement pour Canvas sauf si au moins un autre plugin fourni a besoin de la même jointure.

## État actuel de la branche

Terminé :

- Ajout du package de plugin fourni dans `extensions/canvas`.
- Ajout de `extensions/canvas/openclaw.plugin.json`.
- Déplacement de l'outil agent `canvas` de `src/agents/tools/canvas-tool.ts` vers `extensions/canvas/src/tool.ts`.
- Suppression de l'enregistrement principal de `createCanvasTool` de `src/agents/openclaw-tools.ts`.
- Déplacement de l'implémentation Canvas host de `src/canvas-host` vers `extensions/canvas/src/host`.
- Conservation de `extensions/canvas/runtime-api.ts` comme barrel de compatibilité détenu par le plugin pour les tests, l'empaquetage et les assistants Canvas publics externes.
- Déplacement de la matérialisation des documents Canvas de `src/gateway/canvas-documents.ts` vers `extensions/canvas/src/documents.ts`.
- Déplacement de l'implémentation CLI Canvas et des assistants JSONL A2UI dans `extensions/canvas/src/cli.ts`.
- Déplacement des assistants URL host Canvas et capacité délimitée dans `extensions/canvas/src`.
- Déplacement des valeurs par défaut des commandes de nœud Canvas hors des listes principales codées en dur et dans les `nodeInvokePolicies` du plugin.
- Ajout de la configuration Canvas host détenue par le plugin à `plugins.entries.canvas.config.host`.
- Déplacement de la diffusion HTTP Canvas et A2UI derrière l'enregistrement de route HTTP du plugin Canvas.
- Ajout de la distribution générique de mise à niveau WebSocket du plugin pour les routes HTTP détenues par le plugin.
- Remplacement de l'authentification de capacité de nœud et d'URL host de passerelle spécifique à Canvas par une surface de plugin hébergée générique et des assistants de capacité de nœud.
- Ajout de résolveurs de médias hébergés détenus par le plugin afin que les URL de documents Canvas se résolvent via le plugin Canvas au lieu que le cœur importe les éléments internes des documents Canvas.
- Ajout de `api.registerNodeCliFeature(...)` afin que Canvas puisse déclarer `openclaw nodes canvas` comme une fonctionnalité de nœud détenue par le plugin sans épeler manuellement le chemin de la commande parent.
- Suppression des importations de production `src/**` de `extensions/canvas/runtime-api.js`.
- Déplacement de la source du bundle A2UI de `apps/shared/OpenClawKit/Tools/CanvasA2UI` vers `extensions/canvas/src/host/a2ui-app`.
- Déplacement de l'implémentation de build/copie A2UI sous `extensions/canvas/scripts` et remplacement du câblage de build racine par des crochets d'actifs de plugin fourni génériques.
- Suppression de l'alias de configuration de niveau supérieur hérité `canvasHost`.
- Conservation de la migration du docteur Canvas afin que `openclaw doctor --fix` réécrive les anciennes configurations `canvasHost` en `plugins.entries.canvas.config.host`.
- Suppression de la compatibilité du protocole Canvas de l'ancien agent derrière la version 4 du protocole de passerelle. Les clients natifs et les passerelles utilisent désormais uniquement `pluginSurfaceUrls.canvas` plus `node.pluginSurface.refresh` ; le chemin dépréciée `canvasHostUrl`, `canvasCapability` et `node.canvas.capability.refresh` n'est intentionnellement pas pris en charge dans cette refactorisation expérimentale.
- Mise à jour de l'inventaire des plugins générés pour inclure Canvas.
- Ajout de docs de référence de plugin à `docs/plugins/reference/canvas.md`.

Surfaces Canvas détenues par le cœur restantes connues :

- Les gestionnaires Canvas de l'application native sous `apps/` consomment toujours intentionnellement la surface du plugin Canvas
- Les gestionnaires de protocole/client Canvas de l'application native sous `apps/`
- La sortie d'artefact publiée utilise toujours `dist/canvas-host/a2ui` pour la recherche de runtime rétrocompatible, mais l'étape de copie est désormais détenue par le plugin

## Forme cible

`extensions/canvas` doit posséder :

- manifeste de plugin et métadonnées de package
- enregistrement d'outil agent
- politique de commande d'invocation de nœud
- runtime Canvas host et A2UI
- source du bundle Canvas A2UI et scripts de build/copie d'actifs
- création de documents Canvas et résolution d'actifs
- implémentation CLI Canvas
- page docs Canvas et entrée d'inventaire de plugin

Le cœur doit posséder uniquement les jointures génériques :

- découverte et enregistrement de plugin
- registre d'outil agent générique
- registre de politique d'invocation de nœud générique
- distribution générique de mise à niveau HTTP/authentification et WebSocket de passerelle
- résolution générique d'URL de surface de plugin hébergée
- enregistrement générique de résolveur de médias hébergés
- transport générique de capacité de nœud
- plomberie de configuration générique
- découverte générique de crochet d'actifs de plugin fourni

Les applications natives peuvent conserver les gestionnaires de commandes Canvas en tant que clients du protocole. Elles ne sont pas propriétaires du runtime du plugin.

## Étapes de migration

1. Traitez `plugins.entries.canvas.config.host` comme la surface de configuration détenue par le plugin.
2. Mettez à jour les docs afin que Canvas soit décrit comme un plugin fourni expérimental.
3. Exécutez les tests Canvas ciblés, les vérifications d'inventaire de plugin, les vérifications d'API du SDK de plugin et les portes de build/type affectées par les limites de runtime.

## Liste de contrôle d'audit

Avant de déclarer la refactorisation terminée :

- `rg "src/canvas-host|../canvas-host"` ne retourne aucune importation de source active.
- `rg "canvas-tool|createCanvasTool" src` ne trouve aucune implémentation d'outil Canvas détenue par le cœur.
- `rg "canvas.present|canvas.snapshot|canvas.a2ui" src/gateway` ne trouve aucune valeur par défaut de liste d'autorisation codée en dur en dehors des tests de politique de plugin générique.
- `rg "extensions/canvas/runtime-api" src --glob '!**/*.test.ts'` est vide.
- `rg "canvas-documents" src` est vide.
- `rg "registerNodesCanvasCommands|nodes-canvas" src` est vide ; le plugin Canvas enregistre `openclaw nodes canvas` via les métadonnées CLI du plugin imbriqué.
- `rg "createCanvasHostHandler|handleA2uiHttpRequest" src/gateway` ne retourne aucune propriété de runtime de passerelle.
- `rg "apps/shared/OpenClawKit/Tools/CanvasA2UI|canvas-a2ui-copy|extensions/canvas/src/host/a2ui" scripts .github package.json` ne trouve que des wrappers de compatibilité ou des chemins détenus par le plugin.
- `pnpm plugins:inventory:check` réussit.
- `pnpm plugin-sdk:api:check` réussit, ou les lignes de base d'API générées sont intentionnellement mises à jour et examinées.
- Les tests Canvas ciblés réussissent.
- Les tests des voies modifiées réussissent pour les chemins host/A2UI Canvas.
- Le corps de la PR dit explicitement que Canvas est expérimental et soutenu par un plugin.

## Commandes de vérification

Utilisez les vérifications locales ciblées lors de l'itération :

```sh
pnpm test extensions/canvas/src/host/server.test.ts extensions/canvas/src/host/server.state-dir.test.ts extensions/canvas/src/host/file-resolver.test.ts
pnpm test src/gateway/server.plugin-node-capability-auth.test.ts src/gateway/server-import-boundary.test.ts
pnpm test extensions/canvas/src/config-migration.test.ts src/commands/doctor-legacy-config.migrations.test.ts
pnpm test test/scripts/changed-lanes.test.ts test/scripts/build-all.test.ts extensions/canvas/scripts/bundle-a2ui.test.ts test/scripts/bundled-plugin-assets.test.ts extensions/canvas/scripts/copy-a2ui.test.ts src/infra/run-node.test.ts
pnpm tsgo:extensions
pnpm plugins:inventory:check
pnpm plugin-sdk:api:check
```

Exécutez `pnpm build` avant de pousser si le barrel runtime, l'importation lazy, l'empaquetage ou les surfaces de plugin publiées changent.
