---
summary: "Utilisation de l'outil exec, modes stdin et support TTY"
read_when:
  - Using or modifying the exec tool
  - Debugging stdin or TTY behavior
title: "Exec Tool"
---

# Outil Exec

Exécute des commandes shell dans l'espace de travail. Supporte l'exécution au premier plan et en arrière-plan via `process`.
Si `process` est désactivé, `exec` s'exécute de manière synchrone et ignore `yieldMs`/`background`.
Les sessions en arrière-plan sont limitées par agent ; `process` ne voit que les sessions du même agent.

## Paramètres

- `command` (requis)
- `workdir` (par défaut le répertoire courant)
- `env` (remplacements clé/valeur)
- `yieldMs` (par défaut 10000) : passer en arrière-plan automatiquement après le délai
- `background` (booléen) : passer en arrière-plan immédiatement
- `timeout` (secondes, par défaut 1800) : terminer à l'expiration
- `pty` (booléen) : exécuter dans un pseudo-terminal si disponible (CLIs TTY uniquement, agents de codage, interfaces de terminal)
- `host` (`sandbox | gateway | node`) : où exécuter
- `security` (`deny | allowlist | full`) : mode d'application pour `gateway`/`node`
- `ask` (`off | on-miss | always`) : invites d'approbation pour `gateway`/`node`
- `node` (chaîne) : id/nom du nœud pour `host=node`
- `elevated` (booléen) : demander le mode élevé (hôte gateway) ; `security=full` n'est forcé que lorsque elevated se résout en `full`

Notes :

- `host` est par défaut `sandbox`.
- `elevated` est ignoré lorsque le sandboxing est désactivé (exec s'exécute déjà sur l'hôte).
- Les approbations `gateway`/`node` sont contrôlées par `~/.openclaw/exec-approvals.json`.
- `node` nécessite un nœud appairé (application compagnon ou hôte de nœud sans interface).
- Si plusieurs nœuds sont disponibles, définissez `exec.node` ou `tools.exec.node` pour en sélectionner un.
- Sur les hôtes non-Windows, exec utilise `SHELL` s'il est défini ; si `SHELL` est `fish`, il préfère `bash` (ou `sh`)
  de `PATH` pour éviter les scripts incompatibles avec fish, puis revient à `SHELL` si aucun n'existe.
- Sur les hôtes Windows, exec préfère la découverte de PowerShell 7 (`pwsh`) (Program Files, ProgramW6432, puis PATH),
  puis revient à Windows PowerShell 5.1.
- L'exécution sur l'hôte (`gateway`/`node`) rejette `env.PATH` et les remplacements de chargeur (`LD_*`/`DYLD_*`) pour
  prévenir le détournement de binaires ou l'injection de code.
- OpenClaw définit `OPENCLAW_SHELL=exec` dans l'environnement de la commande générée (y compris l'exécution PTY et sandbox) afin que les règles shell/profil puissent détecter le contexte de l'outil exec.
- Important : le sandboxing est **désactivé par défaut**. Si le sandboxing est désactivé et que `host=sandbox` est explicitement
  configuré/demandé, exec échoue maintenant de manière sécurisée au lieu de s'exécuter silencieusement sur l'hôte gateway.
  Activez le sandboxing ou utilisez `host=gateway` avec les approbations.
- Les vérifications préalables de script (pour les erreurs de syntaxe shell Python/Node courantes) inspectent uniquement les fichiers à l'intérieur de la
  limite `workdir` effective. Si un chemin de script se résout en dehors de `workdir`, la vérification préalable est ignorée pour
  ce fichier.

## Configuration

- `tools.exec.notifyOnExit` (par défaut : true) : lorsque true, les sessions exec en arrière-plan mettent en file d'attente un événement système et demandent un heartbeat à la sortie.
- `tools.exec.approvalRunningNoticeMs` (par défaut : 10000) : émettre un seul avis "en cours d'exécution" lorsqu'un exec contrôlé par approbation s'exécute plus longtemps que cela (0 désactive).
- `tools.exec.host` (par défaut : `sandbox`)
- `tools.exec.security` (par défaut : `deny` pour sandbox, `allowlist` pour gateway + node si non défini)
- `tools.exec.ask` (par défaut : `on-miss`)
- `tools.exec.node` (par défaut : non défini)
- `tools.exec.pathPrepend` : liste de répertoires à ajouter au début de `PATH` pour les exécutions exec (gateway + sandbox uniquement).
- `tools.exec.safeBins` : binaires sûrs stdin uniquement qui peuvent s'exécuter sans entrées de liste d'autorisation explicites. Pour les détails du comportement, voir [Binaires sûrs](/fr/tools/exec-approvals#safe-bins-stdin-only).
- `tools.exec.safeBinTrustedDirs` : répertoires explicites supplémentaires approuvés pour les vérifications de chemin `safeBins`. Les entrées `PATH` ne sont jamais auto-approuvées. Les valeurs par défaut intégrées sont `/bin` et `/usr/bin`.
- `tools.exec.safeBinProfiles` : politique argv personnalisée optionnelle par binaire sûr (`minPositional`, `maxPositional`, `allowedValueFlags`, `deniedFlags`).

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

### Gestion de PATH

- `host=gateway` : fusionne votre `PATH` de shell de connexion dans l'environnement exec. Les remplacements `env.PATH` sont
  rejetés pour l'exécution sur l'hôte. Le daemon lui-même s'exécute toujours avec un `PATH` minimal :
  - macOS : `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`
  - Linux : `/usr/local/bin`, `/usr/bin`, `/bin`
- `host=sandbox` : exécute `sh -lc` (shell de connexion) à l'intérieur du conteneur, donc `/etc/profile` peut réinitialiser `PATH`.
  OpenClaw ajoute `env.PATH` au début après l'approvisionnement du profil via une variable env interne (pas d'interpolation shell) ;
  `tools.exec.pathPrepend` s'applique aussi ici.
- `host=node` : seuls les remplacements env non bloqués que vous transmettez sont envoyés au nœud. Les remplacements `env.PATH` sont
  rejetés pour l'exécution sur l'hôte et ignorés par les hôtes de nœud. Si vous avez besoin d'entrées PATH supplémentaires sur un nœud,
  configurez l'environnement du service hôte de nœud (systemd/launchd) ou installez les outils dans des emplacements standard.

Liaison de nœud par agent (utilisez l'index de la liste d'agents dans la configuration) :

```bash
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

Interface de contrôle : l'onglet Nœuds inclut un petit panneau "Liaison de nœud Exec" pour les mêmes paramètres.

## Remplacements de session (`/exec`)

Utilisez `/exec` pour définir les valeurs par défaut **par session** pour `host`, `security`, `ask` et `node`.
Envoyez `/exec` sans arguments pour afficher les valeurs actuelles.

Exemple :

```
/exec host=gateway security=allowlist ask=on-miss node=mac-1
```

## Modèle d'autorisation

`/exec` n'est honoré que pour les **expéditeurs autorisés** (listes d'autorisation de canal/appairage plus `commands.useAccessGroups`).
Il met à jour **l'état de session uniquement** et n'écrit pas la configuration. Pour désactiver complètement exec, refusez-le via la politique d'outil
(`tools.deny: ["exec"]` ou par agent). Les approbations d'hôte s'appliquent toujours sauf si vous définissez explicitement
`security=full` et `ask=off`.

## Approbations Exec (application compagnon / hôte de nœud)

Les agents en sandbox peuvent nécessiter une approbation par demande avant que `exec` s'exécute sur l'hôte gateway ou nœud.
Voir [Approbations Exec](/fr/tools/exec-approvals) pour la politique, la liste d'autorisation et le flux d'interface utilisateur.

Lorsque les approbations sont requises, l'outil exec retourne immédiatement avec
`status: "approval-pending"` et un id d'approbation. Une fois approuvé (ou refusé / expiré),
la Gateway émet des événements système (`Exec finished` / `Exec denied`). Si la commande est toujours
en cours d'exécution après `tools.exec.approvalRunningNoticeMs`, un seul avis `Exec running` est émis.

## Liste d'autorisation + binaires sûrs

L'application manuelle de la liste d'autorisation correspond **uniquement aux chemins binaires résolus** (pas de correspondances de nom de base). Lorsque
`security=allowlist`, les commandes shell sont auto-autorisées uniquement si chaque segment de pipeline est
autorisé ou un binaire sûr. Le chaînage (`;`, `&&`, `||`) et les redirections sont rejetés en
mode liste d'autorisation sauf si chaque segment de niveau supérieur satisfait la liste d'autorisation (y compris les binaires sûrs).
Les redirections restent non supportées.

`autoAllowSkills` est un chemin de commodité séparé dans les approbations exec. Ce n'est pas la même chose que
les entrées de liste d'autorisation de chemin manuel. Pour une confiance explicite stricte, gardez `autoAllowSkills` désactivé.

Utilisez les deux contrôles pour différents travaux :

- `tools.exec.safeBins` : petits filtres de flux stdin uniquement.
- `tools.exec.safeBinTrustedDirs` : répertoires supplémentaires explicitement approuvés pour les chemins exécutables de binaires sûrs.
- `tools.exec.safeBinProfiles` : politique argv explicite pour les binaires sûrs personnalisés.
- liste d'autorisation : confiance explicite pour les chemins exécutables.

Ne traitez pas `safeBins` comme une liste d'autorisation générique, et n'ajoutez pas de binaires interpréteur/runtime (par exemple `python3`, `node`, `ruby`, `bash`). Si vous en avez besoin, utilisez des entrées de liste d'autorisation explicites et gardez les invites d'approbation activées.
`openclaw security audit` avertit lorsque les entrées `safeBins` interpréteur/runtime manquent de profils explicites, et `openclaw doctor --fix` peut générer les entrées `safeBinProfiles` personnalisées manquantes.

Pour les détails complets de la politique et les exemples, voir [Approbations Exec](/fr/tools/exec-approvals#safe-bins-stdin-only) et [Binaires sûrs versus liste d'autorisation](/fr/tools/exec-approvals#safe-bins-versus-allowlist).

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

Soumettre (envoyer CR uniquement) :

```json
{ "tool": "process", "action": "submit", "sessionId": "<id>" }
```

Coller (encadré par défaut) :

```json
{ "tool": "process", "action": "paste", "sessionId": "<id>", "text": "line1\nline2\n" }
```

## apply_patch (expérimental)

`apply_patch` est un sous-outil de `exec` pour les éditions multi-fichiers structurées.
Activez-le explicitement :

```json5
{
  tools: {
    exec: {
      applyPatch: { enabled: true, workspaceOnly: true, allowModels: ["gpt-5.2"] },
    },
  },
}
```

Notes :

- Disponible uniquement pour les modèles OpenAI/OpenAI Codex.
- La politique d'outil s'applique toujours ; `allow: ["exec"]` autorise implicitement `apply_patch`.
- La configuration se trouve sous `tools.exec.applyPatch`.
- `tools.exec.applyPatch.workspaceOnly` est par défaut `true` (contenu dans l'espace de travail). Définissez-le à `false` uniquement si vous voulez intentionnellement que `apply_patch` écrive/supprime en dehors du répertoire de l'espace de travail.
