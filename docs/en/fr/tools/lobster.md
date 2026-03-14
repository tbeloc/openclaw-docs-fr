---
title: Lobster
summary: "Runtime de workflow typé pour OpenClaw avec des portes d'approbation reprises."
description: Runtime de workflow typé pour OpenClaw — pipelines composables avec des portes d'approbation.
read_when:
  - You want deterministic multi-step workflows with explicit approvals
  - You need to resume a workflow without re-running earlier steps
---

# Lobster

Lobster est un shell de workflow qui permet à OpenClaw d'exécuter des séquences d'outils multi-étapes comme une seule opération déterministe avec des points de contrôle d'approbation explicites.

## Hook

Votre assistant peut construire les outils qui le gèrent lui-même. Demandez un workflow, et 30 minutes plus tard vous avez une CLI plus des pipelines qui s'exécutent en un seul appel. Lobster est la pièce manquante : pipelines déterministes, approbations explicites et état repris.

## Pourquoi

Aujourd'hui, les workflows complexes nécessitent de nombreux appels d'outils aller-retour. Chaque appel coûte des tokens, et le LLM doit orchestrer chaque étape. Lobster déplace cette orchestration dans un runtime typé :

- **Un appel au lieu de plusieurs** : OpenClaw exécute un appel d'outil Lobster et obtient un résultat structuré.
- **Approbations intégrées** : Les effets secondaires (envoyer un email, poster un commentaire) arrêtent le workflow jusqu'à approbation explicite.
- **Repris** : Les workflows arrêtés retournent un token ; approuvez et reprenez sans tout réexécuter.

## Pourquoi un DSL au lieu de programmes simples ?

Lobster est intentionnellement petit. L'objectif n'est pas « un nouveau langage », c'est une spécification de pipeline prévisible et conviviale pour l'IA avec des approbations et des tokens de reprise de première classe.

- **Approuver/reprendre est intégré** : Un programme normal peut inviter un humain, mais il ne peut pas _mettre en pause et reprendre_ avec un token durable sans que vous inventiez ce runtime vous-même.
- **Déterminisme + auditabilité** : Les pipelines sont des données, donc ils sont faciles à enregistrer, comparer, rejouer et examiner.
- **Surface contrainte pour l'IA** : Une petite grammaire + tuyauterie JSON réduit les chemins de code « créatifs » et rend la validation réaliste.
- **Politique de sécurité intégrée** : Les délais d'expiration, les limites de sortie, les vérifications de sandbox et les listes blanches sont appliqués par le runtime, pas par chaque script.
- **Toujours programmable** : Chaque étape peut appeler n'importe quel CLI ou script. Si vous voulez JS/TS, générez des fichiers `.lobster` à partir du code.

## Comment ça marche

OpenClaw lance la CLI `lobster` locale en **mode outil** et analyse une enveloppe JSON à partir de stdout.
Si le pipeline s'arrête pour approbation, l'outil retourne un `resumeToken` pour que vous puissiez continuer plus tard.

## Modèle : petite CLI + tuyauterie JSON + approbations

Construisez de petites commandes qui parlent JSON, puis enchaînez-les en un seul appel Lobster. (Les noms de commandes d'exemple ci-dessous — remplacez par les vôtres.)

```bash
inbox list --json
inbox categorize --json
inbox apply --json
```

```json
{
  "action": "run",
  "pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",
  "timeoutMs": 30000
}
```

Si le pipeline demande une approbation, reprenez avec le token :

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

L'IA déclenche le workflow ; Lobster exécute les étapes. Les portes d'approbation gardent les effets secondaires explicites et auditables.

Exemple : mapper les éléments d'entrée en appels d'outils :

```bash
gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

## Étapes LLM JSON uniquement (llm-task)

Pour les workflows qui ont besoin d'une **étape LLM structurée**, activez l'outil de plugin optionnel
`llm-task` et appelez-le depuis Lobster. Cela garde le workflow
déterministe tout en vous permettant de classer/résumer/rédiger avec un modèle.

Activez l'outil :

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

Utilisez-le dans un pipeline :

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "thinking": "low",
  "input": { "subject": "Hello", "body": "Can you help?" },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

Voir [LLM Task](/tools/llm-task) pour les détails et les options de configuration.

## Fichiers de workflow (.lobster)

Lobster peut exécuter des fichiers de workflow YAML/JSON avec les champs `name`, `args`, `steps`, `env`, `condition` et `approval`. Dans les appels d'outils OpenClaw, définissez `pipeline` sur le chemin du fichier.

```yaml
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

Notes :

- `stdin: $step.stdout` et `stdin: $step.json` passent la sortie d'une étape antérieure.
- `condition` (ou `when`) peut gater les étapes sur `$step.approved`.

## Installer Lobster

Installez la CLI Lobster sur le **même hôte** qui exécute la Gateway OpenClaw (voir le [dépôt Lobster](https://github.com/openclaw/lobster)), et assurez-vous que `lobster` est sur `PATH`.

## Activer l'outil

Lobster est un outil de plugin **optionnel** (non activé par défaut).

Recommandé (additif, sûr) :

```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

Ou par agent :

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["lobster"]
        }
      }
    ]
  }
}
```

Évitez d'utiliser `tools.allow: ["lobster"]` sauf si vous avez l'intention d'exécuter en mode liste blanche restrictive.

Note : les listes blanches sont opt-in pour les plugins optionnels. Si votre liste blanche ne nomme que des outils de plugin (comme `lobster`), OpenClaw garde les outils principaux activés. Pour restreindre les outils principaux, incluez également les outils ou groupes principaux que vous voulez dans la liste blanche.

## Exemple : Triage des emails

Sans Lobster :

```
User: "Check my email and draft replies"
→ openclaw calls gmail.list
→ LLM summarizes
→ User: "draft replies to #2 and #5"
→ LLM drafts
→ User: "send #2"
→ openclaw calls gmail.send
(repeat daily, no memory of what was triaged)
```

Avec Lobster :

```json
{
  "action": "run",
  "pipeline": "email.triage --limit 20",
  "timeoutMs": 30000
}
```

Retourne une enveloppe JSON (tronquée) :

```json
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

L'utilisateur approuve → reprend :

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

Un workflow. Déterministe. Sûr.

## Paramètres de l'outil

### `run`

Exécutez un pipeline en mode outil.

```json
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

Exécutez un fichier de workflow avec des arguments :

```json
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

### `resume`

Continuez un workflow arrêté après approbation.

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### Entrées optionnelles

- `cwd` : Répertoire de travail relatif pour le pipeline (doit rester dans le répertoire de travail du processus actuel).
- `timeoutMs` : Tuez le sous-processus s'il dépasse cette durée (par défaut : 20000).
- `maxStdoutBytes` : Tuez le sous-processus si stdout dépasse cette taille (par défaut : 512000).
- `argsJson` : Chaîne JSON passée à `lobster run --args-json` (fichiers de workflow uniquement).

## Enveloppe de sortie

Lobster retourne une enveloppe JSON avec l'un des trois statuts :

- `ok` → terminé avec succès
- `needs_approval` → en pause ; `requiresApproval.resumeToken` est requis pour reprendre
- `cancelled` → explicitement refusé ou annulé

L'outil affiche l'enveloppe à la fois dans `content` (JSON joli) et `details` (objet brut).

## Approbations

Si `requiresApproval` est présent, inspectez l'invite et décidez :

- `approve: true` → reprendre et continuer les effets secondaires
- `approve: false` → annuler et finaliser le workflow

Utilisez `approve --preview-from-stdin --limit N` pour joindre un aperçu JSON aux demandes d'approbation sans colle jq/heredoc personnalisée. Les tokens de reprise sont maintenant compacts : Lobster stocke l'état de reprise du workflow sous son répertoire d'état et retourne une petite clé de token.

## OpenProse

OpenProse s'associe bien avec Lobster : utilisez `/prose` pour orchestrer la préparation multi-agents, puis exécutez un pipeline Lobster pour les approbations déterministes. Si un programme Prose a besoin de Lobster, autorisez l'outil `lobster` pour les sous-agents via `tools.subagents.tools`. Voir [OpenProse](/prose).

## Sécurité

- **Sous-processus local uniquement** — pas d'appels réseau du plugin lui-même.
- **Pas de secrets** — Lobster ne gère pas OAuth ; il appelle les outils OpenClaw qui le font.
- **Conscient du sandbox** — désactivé lorsque le contexte de l'outil est en sandbox.
- **Renforcé** — nom d'exécutable fixe (`lobster`) sur `PATH` ; délais d'expiration et limites de sortie appliqués.

## Dépannage

- **`lobster subprocess timed out`** → augmentez `timeoutMs`, ou divisez un long pipeline.
- **`lobster output exceeded maxStdoutBytes`** → augmentez `maxStdoutBytes` ou réduisez la taille de la sortie.
- **`lobster returned invalid JSON`** → assurez-vous que le pipeline s'exécute en mode outil et n'imprime que du JSON.
- **`lobster failed (code …)`** → exécutez le même pipeline dans un terminal pour inspecter stderr.

## En savoir plus

- [Plugins](/tools/plugin)
- [Création d'outils de plugin](/plugins/agent-tools)

## Étude de cas : workflows communautaires

Un exemple public : une CLI « second cerveau » + des pipelines Lobster qui gèrent trois coffres Markdown (personnel, partenaire, partagé). La CLI émet du JSON pour les statistiques, les listes de boîte de réception et les analyses obsolètes ; Lobster enchaîne ces commandes dans des workflows comme `weekly-review`, `inbox-triage`, `memory-consolidation` et `shared-task-sync`, chacun avec des portes d'approbation. L'IA gère le jugement (catégorisation) lorsqu'elle est disponible et revient à des règles déterministes sinon.

- Thread : [https://x.com/plattenschieber/status/2014508656335770033](https://x.com/plattenschieber/status/2014508656335770033)
- Repo : [https://github.com/bloomedai/brain-cli](https://github.com/bloomedai/brain-cli)
