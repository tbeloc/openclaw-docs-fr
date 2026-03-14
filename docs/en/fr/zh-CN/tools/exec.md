---
read_when:
  - Utilisation ou modification de l'outil exec
  - Débogage du comportement stdin ou TTY
summary: Utilisation de l'outil Exec, modes stdin et support TTY
title: Outil Exec
x-i18n:
  generated_at: "2026-02-03T09:26:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3b32238dd8dce93d4f24100eaa521ce9f8485eff6d8498e2680ce9ed6045d25f
  source_path: tools/exec.md
  workflow: 15
---

# Outil Exec

Exécute des commandes shell dans l'espace de travail. Supporte l'exécution au premier plan et en arrière-plan via `process`.
Si `process` est désactivé, `exec` s'exécutera de manière synchrone et ignorera `yieldMs`/`background`.
Les sessions en arrière-plan sont isolées par agent ; `process` ne peut voir que les sessions du même agent.

## Paramètres

- `command` (obligatoire)
- `workdir` (par défaut : répertoire courant)
- `env` (surcharges clé-valeur)
- `yieldMs` (par défaut 10000) : passe automatiquement en arrière-plan après ce délai
- `background` (booléen) : passe immédiatement en arrière-plan
- `timeout` (secondes, par défaut 1800) : termine après expiration
- `pty` (booléen) : exécute avec pseudo-terminal si disponible (CLI TTY uniquement, agents de programmation, UI terminal)
- `host` (`sandbox | gateway | node`) : lieu d'exécution
- `security` (`deny | allowlist | full`) : politique d'exécution pour `gateway`/`node`
- `ask` (`off | on-miss | always`) : invite d'approbation pour `gateway`/`node`
- `node` (chaîne) : id/nom du nœud quand `host=node`
- `elevated` (booléen) : demande le mode élevé (hôte gateway) ; force `security=full` uniquement si elevated se résout en `full`

Remarques :

- `host` est par défaut `sandbox`.
- `elevated` est ignoré quand l'isolation du bac à sable est désactivée (exec s'exécute déjà sur l'hôte).
- Les approbations `gateway`/`node` sont contrôlées par `~/.openclaw/exec-approvals.json`.
- `node` nécessite un nœud appairé (application compagnon ou hôte nœud sans interface).
- S'il y a plusieurs nœuds disponibles, définissez `exec.node` ou `tools.exec.node` pour en sélectionner un.
- Sur les hôtes non-Windows, exec utilise le `SHELL` défini ; si `SHELL` est `fish`, il préfère sélectionner `bash` (ou `sh`) depuis `PATH` pour éviter les scripts incompatibles avec fish, avec repli sur `SHELL` si aucun n'existe.
- L'exécution sur hôte (`gateway`/`node`) rejette les surcharges `env.PATH` et chargeur (`LD_*`/`DYLD_*`) pour prévenir le détournement de binaires ou l'injection de code.
- Important : l'isolation du bac à sable est **désactivée par défaut**. Si l'isolation du bac à sable est désactivée, `host=sandbox` s'exécutera directement sur l'hôte Gateway (sans conteneur) et **ne nécessite pas d'approbation**. Pour une approbation, exécutez avec `host=gateway` et configurez les approbations exec (ou activez l'isolation du bac à sable).

## Configuration

- `tools.exec.notifyOnExit` (par défaut : true) : quand true, les sessions exec en arrière-plan mettent en file d'attente un événement système à la sortie et demandent un battement de cœur.
- `tools.exec.approvalRunningNoticeMs` (par défaut : 10000) : émet une notification unique "en cours d'exécution" quand un exec nécessitant approbation s'exécute plus longtemps que cette valeur (0 pour désactiver).
- `tools.exec.host` (par défaut : `sandbox`)
- `tools.exec.security` (par défaut : `deny` pour sandbox, `allowlist` quand gateway + node ne sont pas définis)
- `tools.exec.ask` (par défaut : `on-miss`)
- `tools.exec.node` (par défaut : non défini)
- `tools.exec.pathPrepend` : liste de répertoires à ajouter au début de `PATH` lors de l'exécution d'exec.
- `tools.exec.safeBins` : binaires sûrs stdin uniquement, exécutables sans entrée de liste blanche explicite.

Exemple :

```json5
{
  tools: {
    exec: {
      pathPrepend: ["~/bin", "/opt/oss/bin"],
    },
  },
}
```

### Traitement de PATH

- `host=gateway` : fusionne votre `PATH` de shell de connexion dans l'environnement exec. Les surcharges `env.PATH` sont rejetées lors de l'exécution sur hôte. Le démon lui-même s'exécute toujours avec un `PATH` minimal :
  - macOS : `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`
  - Linux : `/usr/local/bin`, `/usr/bin`, `/bin`
- `host=sandbox` : exécute `sh -lc` (shell de connexion) dans le conteneur, donc `/etc/profile` peut réinitialiser `PATH`. OpenClaw ajoute `env.PATH` au début via une variable d'environnement interne après le chargement du profil (sans interpolation shell) ; `tools.exec.pathPrepend` s'applique aussi ici.
- `host=node` : seules vos surcharges env non bloquées sont envoyées au nœud. Les surcharges `env.PATH` sont rejetées lors de l'exécution sur hôte. Les hôtes nœud sans interface n'acceptent que si `PATH` est ajouté au début du PATH du nœud hôte (remplacement non autorisé). Les nœuds macOS rejettent complètement les surcharges `PATH`.

Lier des nœuds par agent (utiliser l'index de liste d'agents dans la configuration) :

```bash
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

Contrôle UI : l'onglet Nodes contient un petit panneau "Exec Node Binding" pour le même paramètre.

## Surcharges de session (`/exec`)

Utilisez `/exec` pour définir les valeurs par défaut **par session** pour `host`, `security`, `ask` et `node`.
Envoyez `/exec` sans paramètres pour afficher les valeurs actuelles.

Exemple :

```
/exec host=gateway security=allowlist ask=on-miss node=mac-1
```

## Modèle d'autorisation

`/exec` n'est effectif que pour les **expéditeurs autorisés** (liste blanche de canal/appairage plus `commands.useAccessGroups`).
Il met à jour uniquement l'**état de session**, n'écrit pas dans la configuration. Pour désactiver complètement exec, rejetez-le via la politique d'outils (`tools.deny: ["exec"]` ou par configuration d'agent). L'approbation d'hôte s'applique toujours sauf si vous définissez explicitement `security=full` et `ask=off`.

## Approbations Exec (application compagnon/hôte nœud)

Les agents avec isolation de bac à sable peuvent exiger une approbation par requête avant que `exec` s'exécute sur Gateway ou un hôte nœud.
Consultez [Approbations Exec](/tools/exec-approvals) pour les politiques, listes blanches et flux UI.

Quand une approbation est requise, l'outil exec retourne immédiatement `status: "approval-pending"` et un id d'approbation. Une fois approuvé (ou rejeté/expiré), Gateway émet un événement système (`Exec finished` / `Exec denied`). Si la commande s'exécute toujours après `tools.exec.approvalRunningNoticeMs`, une notification unique `Exec running` est émise.

## Liste blanche + binaires sûrs

L'exécution en liste blanche correspond uniquement aux **chemins binaires résolus** (pas aux noms de base). Quand `security=allowlist`, les commandes shell ne sont automatiquement autorisées que si chaque segment de pipeline est en liste blanche ou est un binaire sûr. En mode liste blanche, les commandes chaînées (`;`, `&&`, `||`) et les redirections sont rejetées.

## Exemples

Premier plan :

```json
{ "tool": "exec", "command": "ls -la" }
```

Arrière-plan + sondage :

```json
{"tool":"exec","command":"npm run build","yieldMs":1000}
{"tool":"process","action":"poll","sessionId":"<id>"}
```

Envoyer des touches (style tmux) :

```json
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Enter"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["C-c"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Up","Up","Enter"]}
```

Soumettre (envoie uniquement CR) :

```json
{ "tool": "process", "action": "submit", "sessionId": "<id>" }
```

Coller (parenthèses par défaut) :

```json
{ "tool": "process", "action": "paste", "sessionId": "<id>", "text": "line1\nline2\n" }
```

## apply_patch (expérimental)

`apply_patch` est un sous-outil d'`exec` pour les éditions multi-fichiers structurées.
Doit être explicitement activé :

```json5
{
  tools: {
    exec: {
      applyPatch: { enabled: true, allowModels: ["gpt-5.2"] },
    },
  },
}
```

Remarques :

- Applicable uniquement aux modèles OpenAI/OpenAI Codex.
- La politique d'outils s'applique toujours ; `allow: ["exec"]` autorise implicitement `apply_patch`.
- La configuration se trouve sous `tools.exec.applyPatch`.
