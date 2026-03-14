---
description: Runtime de workflow typé pour OpenClaw — pipelines composables avec portes d'approbation.
read_when:
  - Vous voulez des workflows multi-étapes déterministes avec approbations explicites
  - Vous avez besoin de reprendre des workflows sans réexécuter les étapes antérieures
summary: Runtime de workflow typé pour OpenClaw, supportant les portes d'approbation récupérables.
title: Lobster
x-i18n:
  generated_at: "2026-02-03T10:11:30Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ff84e65f4be162ad98f16ddf0882f23b3198f05b4d9e8dc03d07e9b2bf0fd5ad
  source_path: tools/lobster.md
  workflow: 15
---

# Lobster

Lobster est un shell de workflow qui permet à OpenClaw d'exécuter des séquences d'outils multi-étapes en tant qu'opération unique déterministe, avec des points de contrôle d'approbation explicites.

## Points forts

Votre assistant peut construire des outils qui se gèrent eux-mêmes. Demandez un workflow, et 30 minutes plus tard vous avez une CLI et un pipeline qui s'exécute en un seul appel. Lobster est la pièce manquante : pipelines déterministes, approbations explicites et état récupérable.

## Pourquoi

Aujourd'hui, les workflows complexes nécessitent plusieurs allers-retours d'appels d'outils. Chaque appel consomme des tokens, et le LLM doit orchestrer chaque étape. Lobster déplace cette orchestration dans un runtime typé :

- **Un appel au lieu de plusieurs** : OpenClaw exécute une seule invocation d'outil Lobster et obtient un résultat structuré.
- **Approbation intégrée** : Les effets secondaires (envoyer des emails, publier des commentaires) mettent le workflow en pause jusqu'à approbation explicite.
- **Récupérable** : Un workflow en pause retourne un token ; approuvez et reprenez sans réexécuter tout.

## Pourquoi un DSL plutôt qu'un programme ordinaire ?

Lobster est intentionnellement petit. L'objectif n'est pas « un nouveau langage », mais une spécification de pipeline prévisible et conviviale pour l'IA, avec approbation et tokens de récupération de première classe.

- **Approbation/récupération intégrées** : Un programme ordinaire peut inviter un humain, mais il ne peut pas *mettre en pause et reprendre* avec un token persistant, sauf si vous inventez vous-même ce runtime.
- **Déterminisme + auditabilité** : Les pipelines sont des données, donc ils sont faciles à enregistrer, comparer, rejouer et examiner.
- **Surface restreinte pour l'IA** : Une syntaxe minuscule + pipelines JSON réduisent les chemins de code « créatifs », rendant la validation pratiquement réalisable.
- **Politiques de sécurité intégrées** : Les timeouts, les limites de sortie, les vérifications de sandbox et les listes blanches sont appliqués par le runtime, pas par chaque script.
- **Toujours programmable** : Chaque étape peut appeler n'importe quel CLI ou script. Si vous voulez du JS/TS, générez des fichiers `.lobster` à partir du code.

## Comment ça marche

OpenClaw démarre le CLI `lobster` local en **mode outil** et analyse les enveloppes JSON depuis stdout.
Si le pipeline se met en pause en attente d'approbation, l'outil retourne un `resumeToken` pour que vous puissiez continuer plus tard.

## Modèle : petite CLI + pipeline JSON + approbation

Construisez de petites commandes qui produisent du JSON, puis chaînez-les en un seul appel Lobster. (Les noms de commandes ci-dessous sont des exemples — remplacez-les par les vôtres.)

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

L'IA déclenche le workflow ; Lobster exécute les étapes. Les portes d'approbation rendent les effets secondaires explicites et auditables.

Exemple : mapper les éléments d'entrée aux appels d'outils :

```bash
gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

## Étapes LLM en JSON pur (llm-task)

Pour les workflows qui nécessitent des **étapes LLM structurées**, activez l'outil de plugin optionnel
`llm-task` et appelez-le depuis Lobster. Cela maintient le workflow
déterministe tout en vous permettant d'utiliser le modèle pour la classification/résumé/brouillon.

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

Utilisez-le dans le pipeline :

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
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

Voir [LLM Task](/tools/llm-task) pour plus de détails et d'options de configuration.

## Fichiers de workflow (.lobster)

Lobster peut exécuter des fichiers de workflow YAML/JSON contenant les champs `name`, `args`, `steps`, `env`, `condition` et `approval`. Dans un appel d'outil OpenClaw, définissez `pipeline` sur le chemin du fichier.

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

- `stdin: $step.stdout` et `stdin: $step.json` transmettent la sortie de l'étape précédente.
- `condition` (ou `when`) peut contrôler les étapes en fonction de `$step.approved`.

## Installer Lobster

Installez le CLI Lobster sur le **même hôte** que celui exécutant la passerelle OpenClaw (voir [dépôt Lobster](https://github.com/openclaw/lobster)), et assurez-vous que `lobster` est dans `PATH`.
Si vous voulez utiliser un emplacement binaire personnalisé, passez un chemin **absolu** `lobsterPath` dans l'appel d'outil.

## Activer l'outil

Lobster est un outil de plugin **optionnel** (désactivé par défaut).

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

Évitez `tools.allow: ["lobster"]` sauf si vous avez l'intention de fonctionner en mode liste blanche restrictive.

Note : la liste blanche est volontaire pour les plugins optionnels. Si votre liste blanche contient uniquement
des outils de plugin (comme `lobster`), OpenClaw maintient les outils principaux activés. Pour restreindre les outils
principaux, incluez également les outils ou groupes principaux que vous souhaitez dans la liste blanche.

## Exemple : triage d'emails

Sans Lobster :

```
Utilisateur : « Vérifiez mes emails et rédigez des réponses »
→ openclaw invoque gmail.list
→ LLM résume
→ Utilisateur : « Rédigez des réponses pour #2 et #5 »
→ LLM rédige
→ Utilisateur : « Envoyer #2 »
→ openclaw invoque gmail.send
(répété chaque jour, sans se souvenir de ce qui a été trié)
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

L'utilisateur approuve → Reprendre :

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

Un workflow. Déterministe. Sûr.

## Paramètres d'outil

### `run`

Exécutez un pipeline en mode outil.

```json
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "/path/to/workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

Exécutez un fichier de workflow avec des paramètres :

```json
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

### `resume`

Continuez un workflow en pause après approbation.

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### Entrées optionnelles

- `lobsterPath` : chemin absolu vers le binaire Lobster (omettez pour utiliser `PATH`).
- `cwd` : répertoire de travail du pipeline (par défaut : répertoire de travail du processus actuel).
- `timeoutMs` : terminez si le sous-processus dépasse cette durée (par défaut : 20000).
- `maxStdoutBytes` : terminez le sous-processus si stdout dépasse cette taille (par défaut : 512000).
- `argsJson` : chaîne JSON à passer à `lobster run --args-json` (fichiers de workflow uniquement).

## Enveloppe de sortie

Lobster retourne une enveloppe JSON avec l'un des trois états :

- `ok` → Complété avec succès
- `needs_approval` → En pause ; nécessite `requiresApproval.resumeToken` pour reprendre
- `cancelled` → Explicitement rejeté ou annulé

L'outil affiche l'enveloppe à la fois dans `content` (JSON formaté) et `details` (objet brut).

## Approbation

S'il existe `requiresApproval`, vérifiez l'invite et décidez :

- `approve: true` → Reprenez et continuez les effets secondaires
- `approve: false` → Annulez et terminez le workflow

Utilisez `approve --preview-from-stdin --limit N` pour joindre un aperçu JSON à la demande d'approbation, sans code de liaison jq/heredoc personnalisé. Les tokens de reprise sont maintenant compacts : Lobster stocke l'état de récupération du workflow sous son répertoire d'état et retourne une petite clé de token.

## OpenProse

OpenProse fonctionne bien avec Lobster : utilisez `/prose` pour orchestrer la préparation multi-agents, puis exécutez un pipeline Lobster pour l'approbation déterministe. Si un programme Prose a besoin de Lobster, autorisez l'outil `lobster` aux sous-agents via `tools.subagents.tools`. Voir [OpenProse](/prose).

## Sécurité

- **Sous-processus locaux uniquement** — Le plugin lui-même n'effectue pas d'appels réseau.
- **Pas de clés** — Lobster ne gère pas OAuth ; il appelle les outils OpenClaw qui gèrent OAuth.
- **Conscient du sandbox** — Désactivé lorsque le contexte d'outil est en isolation sandbox.
- **Renforcé** — Si spécifié, `lobsterPath` doit être un chemin absolu ; les timeouts et les limites de sortie sont appliqués.

## Dépannage

- **`lobster subprocess timed out`** → Augmentez `timeoutMs`, ou divisez les longs pipelines.
- **`lobster output exceeded maxStdoutBytes`** → Augmentez `maxStdoutBytes` ou réduisez la taille de la sortie.
- **`lobster returned invalid JSON`** → Assurez-vous que le pipeline s'exécute en mode outil et n'imprime que du JSON.
- **`lobster failed (code …)`** → Exécutez le même pipeline dans le terminal pour vérifier stderr.

## En savoir plus

- [Plugins](/tools/plugin)
- [Développement d'outils de plugin](/plugins/agent-tools)

## Étude de cas : workflows communautaires

Un exemple public : une CLI « deuxième cerveau » + pipeline Lobster qui gère trois dépôts Markdown (personnel, partenaire, partagé). La CLI produit du JSON pour les statistiques, les listes de boîte de réception et les analyses d'obsolescence ; Lobster chaîne ces commandes en workflows comme `weekly-review`, `inbox-triage`, `memory-consolidation` et `shared-task-sync`, chacun avec une porte d'approbation. L'
