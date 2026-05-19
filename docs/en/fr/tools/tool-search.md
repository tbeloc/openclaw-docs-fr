---
summary: "Recherche d'outils : compacter les grands catalogues d'outils PI derrière une recherche, une description et un appel"
title: "Recherche d'outils"
read_when:
  - You want PI agents to use a large tool catalog without adding every tool schema to the prompt
  - You want OpenClaw tools, MCP tools, and client tools exposed through one compact PI surface
  - You are implementing or debugging tool discovery for PI runs
---

Tool Search est une fonctionnalité expérimentale d'agent OpenClaw PI. Elle offre aux agents PI un moyen compact de découvrir et d'appeler de grands catalogues d'outils. Elle est utile lorsque l'exécution dispose de nombreux outils disponibles mais que le modèle n'aura probablement besoin que de quelques-uns d'entre eux.

Cette page documente OpenClaw PI Tool Search. Il ne s'agit pas de la recherche d'outils native de Codex ou de la surface dynamic-tools. Le mode code natif de Codex, la recherche d'outils, les outils dynamiques différés et les appels d'outils imbriqués sont des surfaces de harnais Codex stables et ne dépendent pas de `tools.toolSearch`.

Lorsqu'elle est activée pour PI, le modèle reçoit par défaut un outil `tool_search_code`. Cet outil exécute un court corps JavaScript dans un sous-processus Node isolé avec un pont `openclaw.tools` :

```js
const hits = await openclaw.tools.search("create a GitHub issue");
const tool = await openclaw.tools.describe(hits[0].id);
return await openclaw.tools.call(tool.id, {
  title: "Crash on startup",
  body: "Steps to reproduce...",
});
```

Le catalogue peut inclure des outils OpenClaw, des outils de plugin, des outils MCP et des outils fournis par le client. Le modèle ne voit pas chaque schéma complet à l'avance. Au lieu de cela, il recherche des descripteurs compacts, décrit un outil sélectionné lorsqu'il a besoin du schéma exact, et appelle cet outil via OpenClaw.

Les exécutions du harnais Codex ne reçoivent pas ces contrôles expérimentaux OpenClaw Tool Search. OpenClaw transmet les capacités du produit à Codex en tant qu'outils dynamiques, et Codex possède le mode code natif stable, la recherche d'outils native, les outils dynamiques différés et les appels d'outils imbriqués.

## Comment un tour s'exécute

Au moment de la planification, le moteur d'exécution intégré PI construit le catalogue effectif pour l'exécution :

1. Résoudre la politique d'outils active pour l'agent, le profil, le bac à sable et la session.
2. Lister les outils OpenClaw et de plugin éligibles.
3. Lister les outils MCP éligibles via le runtime MCP de la session.
4. Ajouter les outils clients éligibles fournis pour l'exécution actuelle.
5. Indexer les descripteurs compacts pour la recherche.
6. Exposer soit le pont de code PI, soit les outils de secours structurés au modèle.

Au moment de l'exécution, chaque appel d'outil réel revient à OpenClaw. Le runtime Node isolé ne contient pas les implémentations de plugin, les objets clients MCP ou les secrets. `openclaw.tools.call(...)` traverse le pont dans la Gateway, où la politique normale, l'approbation, les hooks, la journalisation et la gestion des résultats s'appliquent toujours.

## Modes

`tools.toolSearch` a deux modes orientés vers le modèle :

- `code` : expose `tool_search_code`, le pont JavaScript compact par défaut.
- `tools` : expose `tool_search`, `tool_describe` et `tool_call` en tant qu'outils structurés simples pour les fournisseurs qui ne doivent pas recevoir de code.

Les deux modes utilisent le même catalogue et le même chemin d'exécution. La seule différence est la forme que le modèle voit. Si le runtime actuel ne peut pas lancer le processus enfant du mode code Node isolé, le mode `code` par défaut revient à `tools` avant la compaction du catalogue.

Les deux modes sont expérimentaux. Préférez l'exposition directe des outils pour les petits catalogues d'outils PI, et préférez les surfaces stables natives de Codex pour les exécutions du harnais Codex.

Il n'y a pas de configuration de sélection de source séparée. Lorsque Tool Search est activé, le catalogue inclut les outils OpenClaw, MCP et clients éligibles après le filtrage normal de la politique.

## Pourquoi cela existe

Les grands catalogues sont utiles mais coûteux. Envoyer chaque schéma d'outil au modèle rend la requête plus grande, ralentit la planification et augmente la sélection accidentelle d'outils.

Tool Search change la forme :

- outils directs : le modèle voit chaque schéma sélectionné avant le premier token
- Mode code Tool Search : le modèle voit un outil de code compact et un contrat API court
- Mode outils Tool Search : le modèle voit trois outils de secours structurés compacts
- pendant le tour : le modèle charge uniquement les schémas d'outils dont il a réellement besoin

L'exposition directe des outils est toujours le bon défaut pour les petits catalogues. Tool Search est meilleur lorsqu'une exécution peut voir de nombreux outils, en particulier à partir de serveurs MCP ou d'outils d'application fournis par le client.

## API

`openclaw.tools.search(query, options?)`

Recherche le catalogue effectif pour l'exécution actuelle. Les résultats sont compacts et sûrs à remettre dans le contexte d'invite.

```js
const hits = await openclaw.tools.search("calendar event", { limit: 5 });
```

`openclaw.tools.describe(id)`

Charge les métadonnées complètes pour un résultat de recherche, y compris le schéma d'entrée exact.

```js
const calendarCreate = await openclaw.tools.describe("mcp:calendar:create_event");
```

`openclaw.tools.call(id, args)`

Appelle un outil sélectionné via OpenClaw.

```js
await openclaw.tools.call(calendarCreate.id, {
  summary: "Planning",
  start: "2026-05-09T14:00:00Z",
});
```

Le mode de secours structuré expose les mêmes opérations que les outils :

- `tool_search`
- `tool_describe`
- `tool_call`

## Limite du runtime

Le pont de code s'exécute dans un sous-processus Node de courte durée. Le sous-processus démarre avec le mode de permission Node activé, un environnement vide, aucune subvention de système de fichiers ou de réseau, et aucune subvention de processus enfant ou de worker. OpenClaw applique un délai d'expiration du temps mur du processus parent et tue le sous-processus en cas de dépassement du délai, y compris après les continuations asynchrones.

Le runtime expose uniquement :

- `console.log`, `console.warn` et `console.error`
- `openclaw.tools.search`
- `openclaw.tools.describe`
- `openclaw.tools.call`

Le comportement normal d'OpenClaw s'applique toujours aux appels finaux :

- politiques d'autorisation et de refus des outils
- restrictions d'outils par agent et par bac à sable
- gating réservé au propriétaire
- hooks d'approbation
- hooks de plugin `before_tool_call`
- identité de session, journaux et télémétrie

## Configuration

Activez Tool Search pour les exécutions PI avec le pont de code par défaut :

```bash
openclaw config set tools.toolSearch true
```

JSON équivalent :

```json5
{
  tools: {
    toolSearch: true,
  },
}
```

Utilisez plutôt les outils de secours structurés pour les exécutions PI :

```json5
{
  tools: {
    toolSearch: {
      mode: "tools",
    },
  },
}
```

Ajustez le délai d'expiration du mode code et les limites des résultats de recherche :

```json5
{
  tools: {
    toolSearch: {
      mode: "code",
      codeTimeoutMs: 10000,
      searchDefaultLimit: 8,
      maxSearchLimit: 20,
    },
  },
}
```

Désactivez-le :

```json5
{
  tools: {
    toolSearch: false,
  },
}
```

## Invite et télémétrie

Tool Search enregistre suffisamment de télémétrie pour la comparer avec l'exposition directe des outils :

- total des octets d'outils et d'invite sérialisés envoyés au harnais
- taille du catalogue et répartition des sources
- comptages de recherche, description et appel
- appels d'outils finaux exécutés via OpenClaw
- identifiants et sources d'outils sélectionnés

Les journaux de session doivent permettre de répondre à :

- combien de schémas d'outils le modèle a vu à l'avance
- combien d'opérations de recherche et de description il a effectuées
- quel outil final a été appelé
- si le résultat provenait d'OpenClaw, MCP ou d'un outil client

## Validation E2E

Le moteur E2E de la gateway prouve les deux chemins avec le harnais PI :

```bash
node --import tsx scripts/tool-search-gateway-e2e.ts
```

Il crée un faux plugin temporaire avec un grand catalogue d'outils, démarre le fournisseur OpenAI simulé, démarre une Gateway une fois en mode direct et une fois avec Tool Search activé, puis compare les charges utiles des requêtes du fournisseur et les journaux de session.

La régression prouve :

1. Le mode direct peut appeler l'outil du faux plugin.
2. Tool Search peut appeler le même outil du faux plugin.
3. Le mode direct expose les schémas d'outils du faux plugin directement au fournisseur.
4. Tool Search expose uniquement le pont compact.
5. La charge utile de la requête Tool Search est plus petite pour le grand faux catalogue.
6. Les journaux de session affichent les comptages d'appels d'outils attendus et la télémétrie d'appels pontés.

## Comportement en cas d'échec

Tool Search devrait échouer de manière fermée :

- si un outil n'est pas dans la politique effective, la recherche ne devrait pas le retourner
- si un outil sélectionné devient indisponible, `tool_call` devrait échouer
- si la politique ou l'approbation bloque l'exécution, le résultat de l'appel devrait signaler ce blocage au lieu de le contourner
- si le pont de code ne peut pas créer un runtime isolé, utilisez `mode: "tools"` ou désactivez Tool Search pour ce déploiement

## Connexes

- [Tools and plugins](/fr/tools)
- [Multi-agent sandbox and tools](/fr/tools/multi-agent-sandbox-tools)
- [Exec tool](/fr/tools/exec)
- [ACP agents setup](/fr/tools/acp-agents-setup)
- [Building plugins](/fr/plugins/building-plugins)
