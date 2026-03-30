---
title: "Moteur de mémoire QMD"
summary: "Sidecar de recherche local avec BM25, vecteurs, reclassement et expansion de requêtes"
read_when:
  - You want to set up QMD as your memory backend
  - You want advanced memory features like reranking or extra indexed paths
---

# Moteur de mémoire QMD

[QMD](https://github.com/tobi/qmd) est un sidecar de recherche local-first qui s'exécute
aux côtés d'OpenClaw. Il combine la recherche BM25, la recherche vectorielle et le reclassement dans un seul
binaire, et peut indexer du contenu au-delà de vos fichiers de mémoire d'espace de travail.

## Ce qu'il ajoute par rapport à la version intégrée

- **Reclassement et expansion de requêtes** pour un meilleur rappel.
- **Indexer des répertoires supplémentaires** -- docs de projet, notes d'équipe, n'importe quoi sur le disque.
- **Indexer les transcriptions de session** -- rappeler les conversations antérieures.
- **Entièrement local** -- s'exécute via Bun + node-llama-cpp, télécharge automatiquement les modèles GGUF.
- **Basculement automatique** -- si QMD n'est pas disponible, OpenClaw bascule vers le
  moteur intégré de manière transparente.

## Mise en route

### Prérequis

- Installer QMD : `bun install -g https://github.com/tobi/qmd`
- Build SQLite qui permet les extensions (`brew install sqlite` sur macOS).
- QMD doit être sur le `PATH` de la passerelle.
- macOS et Linux fonctionnent directement. Windows est mieux supporté via WSL2.

### Activer

```json5
{
  memory: {
    backend: "qmd",
  },
}
```

OpenClaw crée un répertoire d'accueil QMD autonome sous
`~/.openclaw/agents/<agentId>/qmd/` et gère le cycle de vie du sidecar
automatiquement -- les collections, les mises à jour et les exécutions d'embedding sont gérées pour vous.

## Comment fonctionne le sidecar

- OpenClaw crée des collections à partir de vos fichiers de mémoire d'espace de travail et de tout
  `memory.qmd.paths` configuré, puis exécute `qmd update` + `qmd embed` au démarrage
  et périodiquement (par défaut toutes les 5 minutes).
- L'exécution de démarrage s'effectue en arrière-plan afin que le démarrage du chat ne soit pas bloqué.
- Les recherches utilisent le `searchMode` configuré (par défaut : `search` ; supporte aussi
  `vsearch` et `query`). Si un mode échoue, OpenClaw réessaie avec `qmd query`.
- Si QMD échoue complètement, OpenClaw bascule vers le moteur SQLite intégré.

<Info>
La première recherche peut être lente -- QMD télécharge automatiquement les modèles GGUF (~2 GB) pour
le reclassement et l'expansion de requêtes lors de la première exécution de `qmd query`.
</Info>

## Indexer des chemins supplémentaires

Pointez QMD vers des répertoires supplémentaires pour les rendre consultables :

```json5
{
  memory: {
    backend: "qmd",
    qmd: {
      paths: [{ name: "docs", path: "~/notes", pattern: "**/*.md" }],
    },
  },
}
```

Les extraits des chemins supplémentaires apparaissent comme `qmd/<collection>/<relative-path>` dans
les résultats de recherche. `memory_get` comprend ce préfixe et lit à partir de la racine de collection correcte.

## Indexer les transcriptions de session

Activez l'indexation de session pour rappeler les conversations antérieures :

```json5
{
  memory: {
    backend: "qmd",
    qmd: {
      sessions: { enabled: true },
    },
  },
}
```

Les transcriptions sont exportées sous forme de tours User/Assistant assainis dans une collection QMD dédiée sous `~/.openclaw/agents/<id>/qmd/sessions/`.

## Portée de la recherche

Par défaut, les résultats de recherche QMD ne sont affichés que dans les sessions DM (pas dans les groupes ou
les canaux). Configurez `memory.qmd.scope` pour changer cela :

```json5
{
  memory: {
    qmd: {
      scope: {
        default: "deny",
        rules: [{ action: "allow", match: { chatType: "direct" } }],
      },
    },
  },
}
```

Lorsque la portée refuse une recherche, OpenClaw enregistre un avertissement avec le canal dérivé et
le type de chat afin que les résultats vides soient plus faciles à déboguer.

## Citations

Lorsque `memory.citations` est `auto` ou `on`, les extraits de recherche incluent un
pied de page `Source: <path#line>`. Définissez `memory.citations = "off"` pour omettre le pied de page
tout en transmettant le chemin à l'agent en interne.

## Quand l'utiliser

Choisissez QMD quand vous avez besoin de :

- Reclassement pour des résultats de meilleure qualité.
- Rechercher des docs de projet ou des notes en dehors de l'espace de travail.
- Rappeler les conversations de session passées.
- Recherche entièrement locale sans clés API.

Pour les configurations plus simples, le [moteur intégré](/fr/concepts/memory-builtin) fonctionne bien
sans dépendances supplémentaires.

## Dépannage

**QMD introuvable ?** Assurez-vous que le binaire est sur le `PATH` de la passerelle. Si OpenClaw
s'exécute en tant que service, créez un lien symbolique :
`sudo ln -s ~/.bun/bin/qmd /usr/local/bin/qmd`.

**Première recherche très lente ?** QMD télécharge les modèles GGUF à la première utilisation. Préchauffez
avec `qmd query "test"` en utilisant les mêmes répertoires XDG qu'OpenClaw.

**La recherche expire ?** Augmentez `memory.qmd.limits.timeoutMs` (par défaut : 4000ms).
Définissez à `120000` pour le matériel plus lent.

**Résultats vides dans les chats de groupe ?** Vérifiez `memory.qmd.scope` -- la valeur par défaut
n'autorise que les sessions DM.

## Configuration

Pour la surface de configuration complète (`memory.qmd.*`), les modes de recherche, les intervalles de mise à jour,
les règles de portée et tous les autres paramètres, consultez la
[Référence de configuration de la mémoire](/fr/reference/memory-config).
