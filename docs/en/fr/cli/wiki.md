---
summary: "Référence CLI pour `openclaw wiki` (statut du coffre memory-wiki, recherche, compilation, lint, application, pont, et assistants Obsidian)"
read_when:
  - You want to use the memory-wiki CLI
  - You are documenting or changing `openclaw wiki`
title: "wiki"
---

# `openclaw wiki`

Inspectez et maintenez le coffre `memory-wiki`.

Fourni par le plugin `memory-wiki` fourni.

Liens connexes :

- [Plugin Memory Wiki](/fr/plugins/memory-wiki)
- [Aperçu de la mémoire](/fr/concepts/memory)
- [CLI : memory](/fr/cli/memory)

## À quoi ça sert

Utilisez `openclaw wiki` quand vous voulez un coffre de connaissances compilé avec :

- recherche native wiki et lectures de pages
- synthèses riches en provenance
- rapports de contradiction et de fraîcheur
- importations de pont depuis le plugin de mémoire actif
- assistants CLI Obsidian optionnels

## Commandes courantes

```bash
openclaw wiki status
openclaw wiki doctor
openclaw wiki init
openclaw wiki ingest ./notes/alpha.md
openclaw wiki compile
openclaw wiki lint
openclaw wiki search "alpha"
openclaw wiki get entity.alpha --from 1 --lines 80

openclaw wiki apply synthesis "Alpha Summary" \
  --body "Short synthesis body" \
  --source-id source.alpha

openclaw wiki apply metadata entity.alpha \
  --source-id source.alpha \
  --status review \
  --question "Still active?"

openclaw wiki bridge import
openclaw wiki unsafe-local import

openclaw wiki obsidian status
openclaw wiki obsidian search "alpha"
openclaw wiki obsidian open syntheses/alpha-summary.md
openclaw wiki obsidian command workspace:quick-switcher
openclaw wiki obsidian daily
```

## Commandes

### `wiki status`

Inspectez le mode actuel du coffre, la santé et la disponibilité de l'CLI Obsidian.

Utilisez ceci en premier quand vous n'êtes pas sûr que le coffre soit initialisé, que le
mode pont soit sain, ou que l'intégration Obsidian soit disponible.

### `wiki doctor`

Exécutez les vérifications de santé du wiki et surfacez les problèmes de configuration ou de coffre.

Les problèmes typiques incluent :

- mode pont activé sans artefacts de mémoire publique
- disposition de coffre invalide ou manquante
- CLI Obsidian externe manquant quand le mode Obsidian est attendu

### `wiki init`

Créez la disposition du coffre wiki et les pages de démarrage.

Cela initialise la structure racine, y compris les index de haut niveau et les répertoires
de cache.

### `wiki ingest <path-or-url>`

Importez du contenu dans la couche source du wiki.

Notes :

- L'ingestion d'URL est contrôlée par `ingest.allowUrlIngest`
- les pages source importées conservent la provenance dans le frontmatter
- la compilation automatique peut s'exécuter après l'ingestion quand elle est activée

### `wiki compile`

Reconstruisez les index, les blocs connexes, les tableaux de bord et les digests compilés.

Cela écrit des artefacts stables orientés machine sous :

- `.openclaw-wiki/cache/agent-digest.json`
- `.openclaw-wiki/cache/claims.jsonl`

Si `render.createDashboards` est activé, la compilation actualise également les pages de rapport.

### `wiki lint`

Lintez le coffre et signalez :

- les problèmes structurels
- les lacunes de provenance
- les contradictions
- les questions ouvertes
- les pages/réclamations à faible confiance
- les pages/réclamations obsolètes

Exécutez ceci après des mises à jour wiki significatives.

### `wiki search <query>`

Recherchez du contenu wiki.

Le comportement dépend de la configuration :

- `search.backend` : `shared` ou `local`
- `search.corpus` : `wiki`, `memory`, ou `all`

Utilisez `wiki search` quand vous voulez un classement spécifique au wiki ou des détails de provenance.
Pour un large passage de rappel partagé, préférez `openclaw memory search` quand le
plugin de mémoire actif expose la recherche partagée.

### `wiki get <lookup>`

Lisez une page wiki par id ou chemin relatif.

Exemples :

```bash
openclaw wiki get entity.alpha
openclaw wiki get syntheses/alpha-summary.md --from 1 --lines 80
```

### `wiki apply`

Appliquez des mutations étroites sans chirurgie de page en forme libre.

Les flux supportés incluent :

- créer/mettre à jour une page de synthèse
- mettre à jour les métadonnées de page
- attacher des ids de source
- ajouter des questions
- ajouter des contradictions
- mettre à jour la confiance/le statut
- écrire des réclamations structurées

Cette commande existe pour que le wiki puisse évoluer en toute sécurité sans édition manuelle
de blocs gérés.

### `wiki bridge import`

Importez les artefacts de mémoire publique du plugin de mémoire actif dans les pages source
soutenues par pont.

Utilisez ceci en mode `bridge` quand vous voulez que les derniers artefacts de mémoire exportés
soient tirés dans le coffre wiki.

### `wiki unsafe-local import`

Importez à partir de chemins locaux explicitement configurés en mode `unsafe-local`.

C'est intentionnellement expérimental et local à la même machine uniquement.

### `wiki obsidian ...`

Commandes d'assistant Obsidian pour les coffres fonctionnant en mode compatible Obsidian.

Sous-commandes :

- `status`
- `search`
- `open`
- `command`
- `daily`

Celles-ci nécessitent l'CLI officiel `obsidian` sur `PATH` quand
`obsidian.useOfficialCli` est activé.

## Conseils d'utilisation pratique

- Utilisez `wiki search` + `wiki get` quand la provenance et l'identité de page importent.
- Utilisez `wiki apply` au lieu d'éditer manuellement les sections générées gérées.
- Utilisez `wiki lint` avant de faire confiance au contenu contradictoire ou à faible confiance.
- Utilisez `wiki compile` après les importations en masse ou les changements de source quand vous voulez des
  tableaux de bord frais et des digests compilés immédiatement.
- Utilisez `wiki bridge import` quand le mode pont dépend des artefacts de mémoire nouvellement exportés.

## Liens de configuration

Le comportement de `openclaw wiki` est façonné par :

- `plugins.entries.memory-wiki.config.vaultMode`
- `plugins.entries.memory-wiki.config.search.backend`
- `plugins.entries.memory-wiki.config.search.corpus`
- `plugins.entries.memory-wiki.config.bridge.*`
- `plugins.entries.memory-wiki.config.obsidian.*`
- `plugins.entries.memory-wiki.config.render.*`
- `plugins.entries.memory-wiki.config.context.includeCompiledDigestPrompt`

Voir [Plugin Memory Wiki](/fr/plugins/memory-wiki) pour le modèle de configuration complet.
