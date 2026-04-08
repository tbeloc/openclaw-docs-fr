---
summary: "memory-wiki: coffre-fort de connaissances compilées avec provenance, réclamations, tableaux de bord et mode pont"
read_when:
  - You want persistent knowledge beyond plain MEMORY.md notes
  - You are configuring the bundled memory-wiki plugin
  - You want to understand wiki_search, wiki_get, or bridge mode
title: "Memory Wiki"
---

# Memory Wiki

`memory-wiki` est un plugin fourni qui transforme la mémoire durable en un
coffre-fort de connaissances compilées.

Il ne remplace **pas** le plugin de mémoire active. Le plugin de mémoire active
conserve toujours la récupération, la promotion, l'indexation et la rêverie.
`memory-wiki` se place à côté et compile les connaissances durables en un wiki
navigable avec des pages déterministes, des réclamations structurées, la
provenance, les tableaux de bord et les digests lisibles par machine.

Utilisez-le quand vous voulez que la mémoire se comporte davantage comme une
couche de connaissances maintenue et moins comme un tas de fichiers Markdown.

## Ce qu'il ajoute

- Un coffre-fort wiki dédié avec disposition de page déterministe
- Métadonnées structurées de réclamation et de preuve, pas seulement de la prose
- Provenance au niveau de la page, confiance, contradictions et questions ouvertes
- Digests compilés pour les consommateurs d'agent/runtime
- Outils de recherche/obtention/application/lint natifs du wiki
- Mode pont optionnel qui importe les artefacts publics du plugin de mémoire active
- Mode de rendu compatible Obsidian optionnel et intégration CLI

## Comment il s'intègre avec la mémoire

Pensez à la division comme ceci :

| Couche                                                   | Possède                                                                                       |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Plugin de mémoire active (`memory-core`, QMD, Honcho, etc.) | Récupération, recherche sémantique, promotion, rêverie, runtime de mémoire                               |
| `memory-wiki`                                           | Pages wiki compilées, synthèses riches en provenance, tableaux de bord, recherche/obtention/application spécifiques au wiki |

Si le plugin de mémoire active expose des artefacts de rappel partagés, OpenClaw
peut rechercher les deux couches en un seul passage avec `memory_search corpus=all`.

Quand vous avez besoin d'un classement spécifique au wiki, de provenance ou d'un
accès direct à la page, utilisez plutôt les outils natifs du wiki.

## Modes de coffre-fort

`memory-wiki` supporte trois modes de coffre-fort :

### `isolated`

Coffre-fort propre, sources propres, aucune dépendance sur `memory-core`.

Utilisez ceci quand vous voulez que le wiki soit son propre magasin de
connaissances organisé.

### `bridge`

Lit les artefacts de mémoire publique et les événements de mémoire du plugin de
mémoire active via les coutures publiques du SDK du plugin.

Utilisez ceci quand vous voulez que le wiki compile et organise les artefacts
exportés du plugin de mémoire sans accéder aux internes privés du plugin.

Le mode pont peut indexer :

- artefacts de mémoire exportés
- rapports de rêverie
- notes quotidiennes
- fichiers racine de mémoire
- journaux d'événements de mémoire

### `unsafe-local`

Échappatoire explicite de même machine pour les chemins privés locaux.

Ce mode est intentionnellement expérimental et non portable. Utilisez-le
uniquement quand vous comprenez la limite de confiance et que vous avez
spécifiquement besoin d'un accès au système de fichiers local que le mode pont
ne peut pas fournir.

## Disposition du coffre-fort

Le plugin initialise un coffre-fort comme ceci :

```text
<vault>/
  AGENTS.md
  WIKI.md
  index.md
  inbox.md
  entities/
  concepts/
  syntheses/
  sources/
  reports/
  _attachments/
  _views/
  .openclaw-wiki/
```

Le contenu géré reste à l'intérieur des blocs générés. Les blocs de notes
humaines sont préservés.

Les principaux groupes de pages sont :

- `sources/` pour le matériel brut importé et les pages soutenues par pont
- `entities/` pour les choses durables, les personnes, les systèmes, les projets et les objets
- `concepts/` pour les idées, les abstractions, les modèles et les politiques
- `syntheses/` pour les résumés compilés et les rollups maintenus
- `reports/` pour les tableaux de bord générés

## Réclamations et preuves structurées

Les pages peuvent porter des métadonnées `claims` structurées, pas seulement du
texte libre.

Chaque réclamation peut inclure :

- `id`
- `text`
- `status`
- `confidence`
- `evidence[]`
- `updatedAt`

Les entrées de preuve peuvent inclure :

- `sourceId`
- `path`
- `lines`
- `weight`
- `note`
- `updatedAt`

C'est ce qui fait que le wiki agit davantage comme une couche de croyance qu'un
simple tas de notes passif. Les réclamations peuvent être suivies, notées,
contestées et résolues en remontant aux sources.

## Pipeline de compilation

L'étape de compilation lit les pages du wiki, normalise les résumés et émet des
artefacts stables orientés machine sous :

- `.openclaw-wiki/cache/agent-digest.json`
- `.openclaw-wiki/cache/claims.jsonl`

Ces digests existent pour que les agents et le code runtime n'aient pas à
scraper les pages Markdown.

La sortie compilée alimente également :

- indexation wiki de première passe pour les flux de recherche/obtention
- recherche d'ID de réclamation en retour aux pages propriétaires
- suppléments de prompt compacts
- génération de rapport/tableau de bord

## Tableaux de bord et rapports de santé

Quand `render.createDashboards` est activé, la compilation maintient les
tableaux de bord sous `reports/`.

Les rapports intégrés incluent :

- `reports/open-questions.md`
- `reports/contradictions.md`
- `reports/low-confidence.md`
- `reports/claim-health.md`
- `reports/stale-pages.md`

Ces rapports suivent des choses comme :

- grappes de notes de contradiction
- grappes de réclamations concurrentes
- réclamations manquant de preuves structurées
- pages et réclamations à faible confiance
- pages obsolètes ou de fraîcheur inconnue
- pages avec des questions non résolues

## Recherche et récupération

`memory-wiki` supporte deux backends de recherche :

- `shared`: utiliser le flux de recherche de mémoire partagée quand disponible
- `local`: rechercher le wiki localement

Il supporte également trois corpus :

- `wiki`
- `memory`
- `all`

Comportement important :

- `wiki_search` et `wiki_get` utilisent les digests compilés comme première passe quand possible
- les IDs de réclamation peuvent se résoudre en retour à la page propriétaire
- les réclamations contestées/obsolètes/fraîches influencent le classement
- les étiquettes de provenance peuvent survivre dans les résultats

Règle pratique :

- utilisez `memory_search corpus=all` pour un large passage de rappel
- utilisez `wiki_search` + `wiki_get` quand vous vous souciez du classement spécifique au wiki,
  de la provenance ou de la structure de croyance au niveau de la page

## Outils d'agent

Le plugin enregistre ces outils :

- `wiki_status`
- `wiki_search`
- `wiki_get`
- `wiki_apply`
- `wiki_lint`

Ce qu'ils font :

- `wiki_status`: mode de coffre-fort actuel, santé, disponibilité CLI Obsidian
- `wiki_search`: rechercher les pages du wiki et, quand configuré, les corpus de mémoire partagée
- `wiki_get`: lire une page du wiki par id/chemin ou revenir au corpus de mémoire partagée
- `wiki_apply`: mutations de synthèse/métadonnées étroites sans chirurgie de page libre
- `wiki_lint`: vérifications structurelles, lacunes de provenance, contradictions, questions ouvertes

Le plugin enregistre également un supplément de corpus de mémoire non exclusif, donc
`memory_search` et `memory_get` partagés peuvent atteindre le wiki quand le plugin de
mémoire active supporte la sélection de corpus.

## Comportement du prompt et du contexte

Quand `context.includeCompiledDigestPrompt` est activé, les sections de prompt de
mémoire ajoutent un snapshot compilé compact de `agent-digest.json`.

Ce snapshot est intentionnellement petit et à haut signal :

- pages principales uniquement
- réclamations principales uniquement
- nombre de contradictions
- nombre de questions
- qualificateurs de confiance/fraîcheur

C'est opt-in car cela change la forme du prompt et est principalement utile pour
les moteurs de contexte ou l'assemblage de prompt hérité qui consomment
explicitement les suppléments de mémoire.

## Configuration

Mettez la configuration sous `plugins.entries.memory-wiki.config`:

```json5
{
  plugins: {
    entries: {
      "memory-wiki": {
        enabled: true,
        config: {
          vaultMode: "isolated",
          vault: {
            path: "~/.openclaw/wiki/main",
            renderMode: "obsidian",
          },
          obsidian: {
            enabled: true,
            useOfficialCli: true,
            vaultName: "OpenClaw Wiki",
            openAfterWrites: false,
          },
          bridge: {
            enabled: false,
            readMemoryArtifacts: true,
            indexDreamReports: true,
            indexDailyNotes: true,
            indexMemoryRoot: true,
            followMemoryEvents: true,
          },
          ingest: {
            autoCompile: true,
            maxConcurrentJobs: 1,
            allowUrlIngest: true,
          },
          search: {
            backend: "shared",
            corpus: "wiki",
          },
          context: {
            includeCompiledDigestPrompt: false,
          },
          render: {
            preserveHumanBlocks: true,
            createBacklinks: true,
            createDashboards: true,
          },
        },
      },
    },
  },
}
```

Bascules clés :

- `vaultMode`: `isolated`, `bridge`, `unsafe-local`
- `vault.renderMode`: `native` ou `obsidian`
- `bridge.readMemoryArtifacts`: importer les artefacts publics du plugin de mémoire active
- `bridge.followMemoryEvents`: inclure les journaux d'événements en mode pont
- `search.backend`: `shared` ou `local`
- `search.corpus`: `wiki`, `memory`, ou `all`
- `context.includeCompiledDigestPrompt`: ajouter un snapshot de digest compact aux sections de prompt de mémoire
- `render.createBacklinks`: générer des blocs connexes déterministes
- `render.createDashboards`: générer des pages de tableau de bord

## CLI

`memory-wiki` expose également une surface CLI de haut niveau :

```bash
openclaw wiki status
openclaw wiki doctor
openclaw wiki init
openclaw wiki ingest ./notes/alpha.md
openclaw wiki compile
openclaw wiki lint
openclaw wiki search "alpha"
openclaw wiki get entity.alpha
openclaw wiki apply synthesis "Alpha Summary" --body "..." --source-id source.alpha
openclaw wiki bridge import
openclaw wiki obsidian status
```

Voir [CLI: wiki](/fr/cli/wiki) pour la référence complète des commandes.

## Support Obsidian

Quand `vault.renderMode` est `obsidian`, le plugin écrit du Markdown compatible
Obsidian et peut optionnellement utiliser le CLI officiel `obsidian`.

Les flux de travail supportés incluent :

- sondage de statut
- recherche de coffre-fort
- ouverture d'une page
- invocation d'une commande Obsidian
- saut à la note quotidienne

C'est optionnel. Le wiki fonctionne toujours en mode natif sans Obsidian.

## Flux de travail recommandé

1. Gardez votre plugin de mémoire active pour la récupération/promotion/rêverie.
2. Activez `memory-wiki`.
3. Commencez avec le mode `isolated` sauf si vous voulez explicitement le mode pont.
4. Utilisez `wiki_search` / `wiki_get` quand la provenance importe.
5. Utilisez `wiki_apply` pour les synthèses étroites ou les mises à jour de métadonnées.
6. Exécutez `wiki_lint` après des changements significatifs.
7. Activez les tableaux de bord si vous voulez la visibilité obsolète/contradiction.

## Docs connexes

- [Memory Overview](/fr/concepts/memory)
- [CLI: memory](/fr/cli/memory)
- [CLI: wiki](/fr/cli/wiki)
- [Plugin SDK overview](/fr/plugins/sdk-overview)
