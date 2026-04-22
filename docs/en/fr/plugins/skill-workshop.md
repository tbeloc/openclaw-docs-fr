---
title: "Plugin Skill Workshop"
summary: "Capture expérimental de procédures réutilisables en tant que compétences d'espace de travail avec révision, approbation, mise en quarantaine et actualisation de compétences à chaud"
read_when:
  - You want agents to turn corrections or reusable procedures into workspace skills
  - You are configuring procedural skill memory
  - You are debugging skill_workshop tool behavior
  - You are deciding whether to enable automatic skill creation
---

# Plugin Skill Workshop

Skill Workshop est **expérimental**. Il est désactivé par défaut, ses heuristiques de capture et ses invites de révision peuvent changer entre les versions, et les écritures automatiques ne doivent être utilisées que dans les espaces de travail de confiance après avoir d'abord examiné la sortie en mode en attente.

Skill Workshop est la mémoire procédurale pour les compétences d'espace de travail. Il permet à un agent de transformer des flux de travail réutilisables, des corrections utilisateur, des correctifs difficiles à obtenir et des pièges récurrents en fichiers `SKILL.md` sous :

```text
<workspace>/skills/<skill-name>/SKILL.md
```

Ceci est différent de la mémoire à long terme :

- **Mémoire** stocke les faits, les préférences, les entités et le contexte passé.
- **Compétences** stockent les procédures réutilisables que l'agent doit suivre pour les tâches futures.
- **Skill Workshop** est le pont entre un tour utile et une compétence d'espace de travail durable, avec des contrôles de sécurité et une approbation optionnelle.

Skill Workshop est utile lorsque l'agent apprend une procédure telle que :

- comment valider les ressources GIF animées provenant de sources externes
- comment remplacer les ressources de capture d'écran et vérifier les dimensions
- comment exécuter un scénario d'assurance qualité spécifique au référentiel
- comment déboguer une défaillance de fournisseur récurrente
- comment réparer une note de flux de travail local obsolète

Il n'est pas destiné à :

- des faits comme « l'utilisateur aime le bleu »
- une large mémoire autobiographique
- l'archivage brut de transcriptions
- les secrets, les identifiants ou le texte d'invite caché
- les instructions ponctuelles qui ne se répéteront pas

## État par défaut

Le plugin fourni est **expérimental** et **désactivé par défaut** sauf s'il est explicitement activé dans `plugins.entries.skill-workshop`.

Le manifeste du plugin ne définit pas `enabledByDefault: true`. La valeur par défaut `enabled: true` à l'intérieur du schéma de configuration du plugin s'applique uniquement après que l'entrée du plugin ait déjà été sélectionnée et chargée.

Expérimental signifie :

- le plugin est suffisamment supporté pour les tests d'opt-in et le dogfooding
- le stockage des propositions, les seuils de révision et les heuristiques de capture peuvent évoluer
- l'approbation en attente est le mode de démarrage recommandé
- l'application automatique est pour les configurations personnelles/d'espace de travail de confiance, pas pour les environnements partagés ou hostiles avec beaucoup d'entrées

## Activer

Configuration minimale sûre :

```json5
{
  plugins: {
    entries: {
      "skill-workshop": {
        enabled: true,
        config: {
          autoCapture: true,
          approvalPolicy: "pending",
          reviewMode: "hybrid",
        },
      },
    },
  },
}
```

Avec cette configuration :

- l'outil `skill_workshop` est disponible
- les corrections réutilisables explicites sont mises en file d'attente en tant que propositions en attente
- les passages du révérificateur basés sur les seuils peuvent proposer des mises à jour de compétences
- aucun fichier de compétence n'est écrit jusqu'à ce qu'une proposition en attente soit appliquée

Utilisez les écritures automatiques uniquement dans les espaces de travail de confiance :

```json5
{
  plugins: {
    entries: {
      "skill-workshop": {
        enabled: true,
        config: {
          autoCapture: true,
          approvalPolicy: "auto",
          reviewMode: "hybrid",
        },
      },
    },
  },
}
```

`approvalPolicy: "auto"` utilise toujours le même scanner et le même chemin de quarantaine. Il n'applique pas les propositions avec des résultats critiques.

## Configuration

| Clé                  | Par défaut  | Plage / valeurs                             | Signification                                                        |
| -------------------- | ----------- | ------------------------------------------- | -------------------------------------------------------------------- |
| `enabled`            | `true`      | booléen                                     | Active le plugin après le chargement de l'entrée du plugin.           |
| `autoCapture`        | `true`      | booléen                                     | Active la capture/révision post-tour sur les tours d'agent réussis.   |
| `approvalPolicy`     | `"pending"` | `"pending"`, `"auto"`                       | Met en file d'attente les propositions ou écrit les propositions sûres automatiquement. |
| `reviewMode`         | `"hybrid"`  | `"off"`, `"heuristic"`, `"llm"`, `"hybrid"` | Choisit la capture de correction explicite, le révérificateur LLM, les deux ou aucun. |
| `reviewInterval`     | `15`        | `1..200`                                    | Exécute le révérificateur après ce nombre de tours réussis.           |
| `reviewMinToolCalls` | `8`         | `1..500`                                    | Exécute le révérificateur après ce nombre d'appels d'outils observés. |
| `reviewTimeoutMs`    | `45000`     | `5000..180000`                              | Délai d'expiration pour l'exécution du révérificateur intégré.        |
| `maxPending`         | `50`        | `1..200`                                    | Nombre maximum de propositions en attente/en quarantaine conservées par espace de travail. |
| `maxSkillBytes`      | `40000`     | `1024..200000`                              | Taille maximale du fichier de compétence/support généré.             |

Profils recommandés :

```json5
// Conservateur : utilisation explicite d'outils uniquement, pas de capture automatique.
{
  autoCapture: false,
  approvalPolicy: "pending",
  reviewMode: "off",
}
```

```json5
// Révision d'abord : capture automatiquement, mais exige l'approbation.
{
  autoCapture: true,
  approvalPolicy: "pending",
  reviewMode: "hybrid",
}
```

```json5
// Automatisation de confiance : écrit immédiatement les propositions sûres.
{
  autoCapture: true,
  approvalPolicy: "auto",
  reviewMode: "hybrid",
}
```

```json5
// Faible coût : pas d'appel LLM du révérificateur, uniquement les phrases de correction explicites.
{
  autoCapture: true,
  approvalPolicy: "pending",
  reviewMode: "heuristic",
}
```

## Chemins de capture

Skill Workshop a trois chemins de capture.

### Suggestions d'outils

Le modèle peut appeler `skill_workshop` directement lorsqu'il voit une procédure réutilisable ou lorsque l'utilisateur lui demande de sauvegarder/mettre à jour une compétence.

C'est le chemin le plus explicite et fonctionne même avec `autoCapture: false`.

### Capture heuristique

Lorsque `autoCapture` est activé et `reviewMode` est `heuristic` ou `hybrid`, le plugin analyse les tours réussis pour les phrases de correction utilisateur explicites :

- `next time`
- `from now on`
- `remember to`
- `make sure to`
- `always ... use/check/verify/record/save/prefer`
- `prefer ... when/for/instead/use`
- `when asked`

L'heuristique crée une proposition à partir de la dernière instruction utilisateur correspondante. Il utilise des indices de sujet pour choisir les noms de compétences pour les flux de travail courants :

- tâches GIF animées -> `animated-gif-workflow`
- tâches de capture d'écran ou d'actifs -> `screenshot-asset-workflow`
- tâches d'assurance qualité ou de scénario -> `qa-scenario-workflow`
- tâches GitHub PR -> `github-pr-workflow`
- secours -> `learned-workflows`

La capture heuristique est intentionnellement étroite. C'est pour les corrections claires et les notes de processus répétables, pas pour la résumé général de transcription.

### Révérificateur LLM

Lorsque `autoCapture` est activé et `reviewMode` est `llm` ou `hybrid`, le plugin exécute un révérificateur intégré compact après que les seuils soient atteints.

Le révérificateur reçoit :

- le texte de transcription récent, limité aux 12 000 derniers caractères
- jusqu'à 12 compétences d'espace de travail existantes
- jusqu'à 2 000 caractères de chaque compétence existante
- instructions JSON uniquement

Le révérificateur n'a pas d'outils :

- `disableTools: true`
- `toolsAllow: []`
- `disableMessageTool: true`

Il peut retourner :

```json
{ "action": "none" }
```

ou une proposition de compétence :

```json
{
  "action": "create",
  "skillName": "media-asset-qa",
  "title": "Media Asset QA",
  "reason": "Reusable animated media acceptance workflow",
  "description": "Validate externally sourced animated media before product use.",
  "body": "## Workflow\n\n- Verify true animation.\n- Record attribution.\n- Store a local approved copy.\n- Verify in product UI before final reply."
}
```

Il peut également ajouter à une compétence existante :

```json
{
  "action": "append",
  "skillName": "qa-scenario-workflow",
  "title": "QA Scenario Workflow",
  "reason": "Animated media QA needs reusable checks",
  "description": "QA scenario workflow.",
  "section": "Workflow",
  "body": "- For animated GIF tasks, verify frame count and attribution before passing."
}
```

Ou remplacer le texte exact dans une compétence existante :

```json
{
  "action": "replace",
  "skillName": "screenshot-asset-workflow",
  "title": "Screenshot Asset Workflow",
  "reason": "Old validation missed image optimization",
  "oldText": "- Replace the screenshot asset.",
  "newText": "- Replace the screenshot asset, preserve dimensions, optimize the PNG, and run the relevant validation gate."
}
```

Préférez `append` ou `replace` lorsqu'une compétence pertinente existe déjà. Utilisez `create` uniquement lorsqu'aucune compétence existante ne convient.

## Cycle de vie de la proposition

Chaque mise à jour générée devient une proposition avec :

- `id`
- `createdAt`
- `updatedAt`
- `workspaceDir`
- `agentId` optionnel
- `sessionId` optionnel
- `skillName`
- `title`
- `reason`
- `source` : `tool`, `agent_end` ou `reviewer`
- `status`
- `change`
- `scanFindings` optionnel
- `quarantineReason` optionnel

Statuts de proposition :

- `pending` - en attente d'approbation
- `applied` - écrit dans `<workspace>/skills`
- `rejected` - rejeté par l'opérateur/modèle
- `quarantined` - bloqué par les résultats critiques du scanner

L'état est stocké par espace de travail sous le répertoire d'état de la passerelle :

```text
<stateDir>/skill-workshop/<workspace-hash>.json
```

Les propositions en attente et en quarantaine sont dédupliquées par nom de compétence et charge utile de modification. Le magasin conserve les propositions en attente/en quarantaine les plus récentes jusqu'à `maxPending`.

## Référence des outils

Le plugin enregistre un outil d'agent :

```text
skill_workshop
```

### `status`

Compter les propositions par état pour l'espace de travail actif.

```json
{ "action": "status" }
```

Forme du résultat :

```json
{
  "workspaceDir": "/path/to/workspace",
  "pending": 1,
  "quarantined": 0,
  "applied": 3,
  "rejected": 0
}
```

### `list_pending`

Lister les propositions en attente.

```json
{ "action": "list_pending" }
```

Pour lister un autre état :

```json
{ "action": "list_pending", "status": "applied" }
```

Valeurs `status` valides :

- `pending`
- `applied`
- `rejected`
- `quarantined`

### `list_quarantine`

Lister les propositions en quarantaine.

```json
{ "action": "list_quarantine" }
```

Utilisez ceci quand la capture automatique semble ne rien faire et que les journaux mentionnent
`skill-workshop: quarantined <skill>`.

### `inspect`

Récupérer une proposition par id.

```json
{
  "action": "inspect",
  "id": "proposal-id"
}
```

### `suggest`

Créer une proposition. Avec `approvalPolicy: "pending"`, cela met en file d'attente par défaut.

```json
{
  "action": "suggest",
  "skillName": "animated-gif-workflow",
  "title": "Animated GIF Workflow",
  "reason": "User established reusable GIF validation rules.",
  "description": "Validate animated GIF assets before using them.",
  "body": "## Workflow\n\n- Verify the URL resolves to image/gif.\n- Confirm it has multiple frames.\n- Record attribution and license.\n- Avoid hotlinking when a local asset is needed."
}
```

Forcer une écriture sûre :

```json
{
  "action": "suggest",
  "apply": true,
  "skillName": "animated-gif-workflow",
  "description": "Validate animated GIF assets before using them.",
  "body": "## Workflow\n\n- Verify true animation.\n- Record attribution."
}
```

Forcer en attente même dans `approvalPolicy: "auto"` :

```json
{
  "action": "suggest",
  "apply": false,
  "skillName": "screenshot-asset-workflow",
  "description": "Screenshot replacement workflow.",
  "body": "## Workflow\n\n- Verify dimensions.\n- Optimize the PNG.\n- Run the relevant gate."
}
```

Ajouter à une section :

```json
{
  "action": "suggest",
  "skillName": "qa-scenario-workflow",
  "section": "Workflow",
  "description": "QA scenario workflow.",
  "body": "- For media QA, verify generated assets render and pass final assertions."
}
```

Remplacer du texte exact :

```json
{
  "action": "suggest",
  "skillName": "github-pr-workflow",
  "oldText": "- Check the PR.",
  "newText": "- Check unresolved review threads, CI status, linked issues, and changed files before deciding."
}
```

### `apply`

Appliquer une proposition en attente.

```json
{
  "action": "apply",
  "id": "proposal-id"
}
```

`apply` refuse les propositions en quarantaine :

```text
quarantined proposal cannot be applied
```

### `reject`

Marquer une proposition comme rejetée.

```json
{
  "action": "reject",
  "id": "proposal-id"
}
```

### `write_support_file`

Écrire un fichier de support dans un répertoire de compétence existant ou proposé.

Répertoires de support de niveau supérieur autorisés :

- `references/`
- `templates/`
- `scripts/`
- `assets/`

Exemple :

```json
{
  "action": "write_support_file",
  "skillName": "release-workflow",
  "relativePath": "references/checklist.md",
  "body": "# Release Checklist\n\n- Run release docs.\n- Verify changelog.\n"
}
```

Les fichiers de support sont limités à l'espace de travail, vérifiés par chemin, limités en octets par
`maxSkillBytes`, analysés et écrits de manière atomique.

## Écritures de compétences

Skill Workshop écrit uniquement sous :

```text
<workspace>/skills/<normalized-skill-name>/
```

Les noms de compétences sont normalisés :

- minuscules
- les exécutions non `[a-z0-9_-]` deviennent `-`
- les caractères non alphanumériques de début/fin sont supprimés
- la longueur maximale est de 80 caractères
- le nom final doit correspondre à `[a-z0-9][a-z0-9_-]{1,79}`

Pour `create` :

- si la compétence n'existe pas, Skill Workshop écrit un nouveau `SKILL.md`
- si elle existe déjà, Skill Workshop ajoute le corps à `## Workflow`

Pour `append` :

- si la compétence existe, Skill Workshop ajoute à la section demandée
- si elle n'existe pas, Skill Workshop crée une compétence minimale puis ajoute

Pour `replace` :

- la compétence doit déjà exister
- `oldText` doit être présent exactement
- seule la première correspondance exacte est remplacée

Toutes les écritures sont atomiques et actualisent immédiatement l'instantané des compétences en mémoire, de sorte que
la compétence nouvelle ou mise à jour peut devenir visible sans redémarrage de Gateway.

## Modèle de sécurité

Skill Workshop dispose d'un scanner de sécurité sur le contenu généré `SKILL.md` et les fichiers de support.

Les résultats critiques mettent les propositions en quarantaine :

| ID de règle                            | Bloque le contenu qui...                                                |
| -------------------------------------- | ----------------------------------------------------------------------- |
| `prompt-injection-ignore-instructions` | dit à l'agent d'ignorer les instructions antérieures/supérieures         |
| `prompt-injection-system`              | référence les invites système, les messages de développeur ou les instructions cachées |
| `prompt-injection-tool`                | encourage le contournement de la permission/approbation des outils       |
| `shell-pipe-to-shell`                  | inclut `curl`/`wget` canalisé dans `sh`, `bash` ou `zsh`                |
| `secret-exfiltration`                  | semble envoyer des données env/process env sur le réseau                 |

Les résultats d'avertissement sont conservés mais ne bloquent pas par eux-mêmes :

| ID de règle          | Avertit sur...                           |
| -------------------- | ---------------------------------------- |
| `destructive-delete` | commandes `rm -rf` de style large        |
| `unsafe-permissions` | utilisation de permissions `chmod 777`   |

Propositions en quarantaine :

- conservent `scanFindings`
- conservent `quarantineReason`
- apparaissent dans `list_quarantine`
- ne peuvent pas être appliquées via `apply`

Pour récupérer d'une proposition en quarantaine, créez une nouvelle proposition sûre avec le contenu non sûr supprimé. Ne modifiez pas le JSON du magasin à la main.

## Guidance d'invite

Lorsqu'elle est activée, Skill Workshop injecte une courte section d'invite qui dit à l'agent d'utiliser `skill_workshop` pour la mémoire procédurale durable.

La guidance met l'accent sur :

- les procédures, pas les faits/préférences
- les corrections de l'utilisateur
- les procédures réussies non évidentes
- les pièges récurrents
- la réparation des compétences obsolètes/minces/incorrectes via append/replace
- l'enregistrement de la procédure réutilisable après de longues boucles d'outils ou des corrections difficiles
- le texte de compétence impératif court
- pas de vidages de transcription

Le texte du mode d'écriture change avec `approvalPolicy` :

- mode en attente : mettre en file d'attente les suggestions ; appliquer uniquement après approbation explicite
- mode auto : appliquer les mises à jour de compétences d'espace de travail sûres quand clairement réutilisables

## Coûts et comportement à l'exécution

La capture heuristique n'appelle pas un modèle.

L'examen LLM utilise une exécution intégrée sur le modèle d'agent actif/par défaut. Il est basé sur un seuil, donc il ne s'exécute pas à chaque tour par défaut.

L'examinateur :

- utilise le même contexte de fournisseur/modèle configuré quand disponible
- revient aux valeurs par défaut de l'agent d'exécution
- a `reviewTimeoutMs`
- utilise un contexte d'amorçage léger
- n'a pas d'outils
- n'écrit rien directement
- ne peut émettre qu'une proposition qui passe par le scanner normal et le chemin d'approbation/quarantaine

Si l'examinateur échoue, expire ou retourne un JSON invalide, le plugin enregistre un message d'avertissement/débogage et ignore ce passage d'examen.

## Modèles d'exploitation

Utilisez Skill Workshop quand l'utilisateur dit :

- « la prochaine fois, fais X »
- « à partir de maintenant, préfère Y »
- « assure-toi de vérifier Z »
- « enregistre ceci comme un flux de travail »
- « cela a pris du temps ; souviens-toi du processus »
- « mets à jour la compétence locale pour ceci »

Bon texte de compétence :

```markdown
## Workflow

- Verify the GIF URL resolves to `image/gif`.
- Confirm the file has multiple frames.
- Record source URL, license, and attribution.
- Store a local copy when the asset will ship with the product.
- Verify the local asset renders in the target UI before final reply.
```

Mauvais texte de compétence :

```markdown
The user asked about a GIF and I searched two websites. Then one was blocked by
Cloudflare. The final answer said to check attribution.
```

Raisons pour lesquelles la mauvaise version ne devrait pas être enregistrée :

- en forme de transcription
- pas impératif
- inclut des détails bruyants ponctuels
- ne dit pas au prochain agent quoi faire

## Débogage

Vérifier si le plugin est chargé :

```bash
openclaw plugins list --enabled
```

Vérifier les nombres de propositions à partir d'un contexte d'agent/outil :

```json
{ "action": "status" }
```

Inspecter les propositions en attente :

```json
{ "action": "list_pending" }
```

Inspecter les propositions en quarantaine :

```json
{ "action": "list_quarantine" }
```

Symptômes courants :

| Symptôme                              | Cause probable                                                                      | Vérifier                                                                 |
| ------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| L'outil n'est pas disponible          | L'entrée du plugin n'est pas activée                                                | `plugins.entries.skill-workshop.enabled` et `openclaw plugins list`      |
| Aucune proposition automatique n'apparaît | `autoCapture: false`, `reviewMode: "off"` ou les seuils ne sont pas atteints       | Config, statut de la proposition, journaux Gateway                       |
| La capture heuristique n'a pas fonctionné | La formulation de l'utilisateur ne correspondait pas aux modèles de correction      | Utilisez `skill_workshop.suggest` explicite ou activez l'examinateur LLM |
| L'examinateur n'a pas créé de proposition | L'examinateur a retourné `none`, un JSON invalide ou a expiré                      | Journaux Gateway, `reviewTimeoutMs`, seuils                              |
| La proposition n'est pas appliquée   | `approvalPolicy: "pending"`                                                         | `list_pending`, puis `apply`                                             |
| La proposition a disparu de en attente | Proposition dupliquée réutilisée, élagage max en attente ou appliquée/rejetée/mise en quarantaine | `status`, `list_pending` avec filtres de statut, `list_quarantine`       |
| Le fichier de compétence existe mais le modèle le manque | L'instantané de compétence n'est pas actualisé ou le gating de compétence l'exclut | Statut `openclaw skills` et éligibilité de compétence d'espace de travail |

Journaux pertinents :

- `skill-workshop: queued <skill>`
- `skill-workshop: applied <skill>`
- `skill-workshop: quarantined <skill>`
- `skill-workshop: heuristic capture skipped: ...`
- `skill-workshop: reviewer skipped: ...`
- `skill-workshop: reviewer found no update`

## Scénarios QA

Scénarios QA sauvegardés par repo :

- `qa/scenarios/plugins/skill-workshop-animated-gif-autocreate.md`
- `qa/scenarios/plugins/skill-workshop-pending-approval.md`
- `qa/scenarios/plugins/skill-workshop-reviewer-autonomous.md`

Exécuter la couverture déterministe :

```bash
pnpm openclaw qa suite \
  --scenario skill-workshop-animated-gif-autocreate \
  --scenario skill-workshop-pending-approval \
  --concurrency 1
```

Exécuter la couverture de l'examinateur :

```bash
pnpm openclaw qa suite \
  --scenario skill-workshop-reviewer-autonomous \
  --concurrency 1
```

Le scénario de l'examinateur est intentionnellement séparé car il active `reviewMode: "llm"` et exerce le passage d'examinateur intégré.

## Quand ne pas activer l'application automatique

Évitez `approvalPolicy: "auto"` quand :

- l'espace de travail contient des procédures sensibles
- l'agent travaille sur une entrée non fiable
- les compétences sont partagées dans une large équipe
- vous êtes toujours en train d'affiner les invites ou les règles du scanner
- le modèle traite fréquemment du contenu web/email hostile

Utilisez d'abord le mode en attente. Passez au mode auto uniquement après avoir examiné le type de compétences que l'agent propose dans cet espace de travail.

## Docs connexes

- [Skills](/fr/tools/skills)
- [Plugins](/fr/tools/plugin)
- [Testing](/fr/reference/test)
