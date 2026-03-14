---
read_when:
  - Vous devez expliquer l'espace de travail de l'agent ou sa disposition de fichiers
  - Vous souhaitez sauvegarder ou migrer l'espace de travail de l'agent
summary: Espace de travail de l'agent : localisation, disposition et stratégies de sauvegarde
title: Espace de travail de l'agent
x-i18n:
  generated_at: "2026-02-03T07:45:49Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 84c550fd89b5f2474aeae586795485fd29d36effbb462f13342b31540fc18b82
  source_path: concepts/agent-workspace.md
  workflow: 15
---

# Espace de travail de l'agent

L'espace de travail est la maison de l'agent. C'est le répertoire de travail unique utilisé par les outils de fichiers et le contexte de l'espace de travail. Gardez-le privé et considérez-le comme une mémoire.

Ceci est séparé de `~/.openclaw/`, qui stocke la configuration, les identifiants et les sessions.

**Important :** L'espace de travail est le **répertoire de travail par défaut**, et non un bac à sable strict. Les outils résolvent les chemins relatifs par rapport à l'espace de travail, mais les chemins absolus peuvent toujours accéder à d'autres emplacements sur l'hôte, sauf si l'isolation du bac à sable est activée. Si vous avez besoin d'une isolation, utilisez
[`agents.defaults.sandbox`](/gateway/sandboxing) (et/ou la configuration du bac à sable par agent).
Lorsque l'isolation du bac à sable est activée et que `workspaceAccess` n'est pas `"rw"`, les outils fonctionnent dans l'espace de travail du bac à sable sous `~/.openclaw/sandboxes`, plutôt que dans votre espace de travail hôte.

## Localisation par défaut

- Par défaut : `~/.openclaw/workspace`
- Si `OPENCLAW_PROFILE` est défini et n'est pas `"default"`, la valeur par défaut devient
  `~/.openclaw/workspace-<profile>`.
- Remplacez dans `~/.openclaw/openclaw.json` :

```json5
{
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

`openclaw onboard`, `openclaw configure` ou `openclaw setup` créeront l'espace de travail et rempliront les fichiers d'amorçage s'ils manquent.

Si vous gérez déjà les fichiers de l'espace de travail vous-même, vous pouvez désactiver la création de fichiers d'amorçage :

```json5
{ agent: { skipBootstrap: true } }
```

## Dossiers d'espace de travail supplémentaires

Les installations héritées peuvent avoir créé `~/openclaw`. Conserver plusieurs répertoires d'espace de travail peut entraîner une authentification confuse ou une dérive d'état, car un seul espace de travail est actif à la fois.

**Recommandation :** Conservez un seul espace de travail actif. Si vous n'utilisez plus les dossiers supplémentaires, archivez-les ou déplacez-les à la corbeille (par exemple `trash ~/openclaw`).
Si vous souhaitez intentionnellement conserver plusieurs espaces de travail, assurez-vous que `agents.defaults.workspace` pointe vers celui qui est actif.

`openclaw doctor` émettra un avertissement lors de la détection de répertoires d'espace de travail supplémentaires.

## Mappage des fichiers de l'espace de travail (signification de chaque fichier)

Ce sont les fichiers standard qu'OpenClaw s'attend à trouver dans l'espace de travail :

- `AGENTS.md`
  - Guide opérationnel de l'agent et comment il doit utiliser la mémoire.
  - Chargé au début de chaque session.
  - Idéal pour placer les règles, les priorités et les détails du « comment se comporter ».

- `SOUL.md`
  - Personnalité, ton et limites.
  - Chargé à chaque session.

- `USER.md`
  - Qui est l'utilisateur et comment l'appeler.
  - Chargé à chaque session.

- `IDENTITY.md`
  - Nom, style et émojis de l'agent.
  - Créé/mis à jour lors de la cérémonie d'amorçage.

- `TOOLS.md`
  - Notes sur vos outils locaux et conventions.
  - Ne contrôle pas la disponibilité des outils ; à titre informatif uniquement.

- `HEARTBEAT.md`
  - Liste de contrôle optionnelle du battement cardiaque pour exécuter de petites vérifications.
  - Gardez-la courte pour éviter la consommation de tokens.

- `BOOT.md`
  - Liste de contrôle de démarrage optionnelle exécutée lors du redémarrage de la passerelle Gateway lorsque les hooks internes sont activés.
  - Gardez-la courte ; utilisez l'outil message pour les envois sortants.

- `BOOTSTRAP.md`
  - Cérémonie de première exécution unique.
  - Créé uniquement pour les espaces de travail tout neufs.
  - Supprimez-le une fois la cérémonie terminée.

- `memory/YYYY-MM-DD.md`
  - Journal de mémoire quotidien (un fichier par jour).
  - Il est recommandé de lire aujourd'hui + hier au début de la session.

- `MEMORY.md` (optionnel)
  - Mémoire à long terme sélectionnée.
  - Chargé uniquement dans les sessions privées principales (pas dans les contextes partagés/groupes).

Voir [Mémoire](/concepts/memory) pour les flux de travail et l'actualisation automatique de la mémoire.

- `skills/` (optionnel)
  - Skills spécifiques à l'espace de travail.
  - Remplace les Skills gérés/fournis en cas de conflit de noms.

- `canvas/` (optionnel)
  - Fichiers Canvas UI pour l'affichage des nœuds (par exemple `canvas/index.html`).

Si des fichiers d'amorçage manquent, OpenClaw injectera un marqueur « fichier manquant » dans la session et continuera. Les fichiers d'amorçage volumineux sont tronqués lors de l'injection ; ajustez la limite avec `agents.defaults.bootstrapMaxChars` (par défaut : 20000).
`openclaw setup` peut recréer les valeurs par défaut manquantes sans remplacer les fichiers existants.

## Ce qui n'est pas inclus dans l'espace de travail

Ceux-ci se trouvent sous `~/.openclaw/` et ne doivent pas être validés dans le référentiel de l'espace de travail :

- `~/.openclaw/openclaw.json` (configuration)
- `~/.openclaw/credentials/` (tokens OAuth, clés API)
- `~/.openclaw/agents/<agentId>/sessions/` (enregistrements de session + métadonnées)
- `~/.openclaw/skills/` (Skills gérés)

Si vous devez migrer des sessions ou une configuration, copiez-les séparément et excluez-les du contrôle de version.

## Sauvegarde Git (recommandée, privée)

Considérez l'espace de travail comme une mémoire privée. Placez-le dans un référentiel git **privé** pour la sauvegarde et la restauration.

Exécutez ces étapes sur la machine exécutant la passerelle Gateway (c'est là que se trouve l'espace de travail).

### 1) Initialiser le référentiel

Si git est installé, un espace de travail tout neuf sera initialisé automatiquement. Si cet espace de travail n'est pas encore un référentiel, exécutez :

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

### 2) Ajouter une télécommande privée (option conviviale pour les débutants)

Option A : Interface web GitHub

1. Créez un nouveau référentiel **privé** sur GitHub.
2. Ne l'initialisez pas avec un README (évitez les conflits de fusion).
3. Copiez l'URL de la télécommande HTTPS.
4. Ajoutez la télécommande et poussez :

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

Option B : GitHub CLI (`gh`)

```bash
gh auth login
gh repo create openclaw-workspace --private --source . --remote origin --push
```

Option C : Interface web GitLab

1. Créez un nouveau référentiel **privé** sur GitLab.
2. Ne l'initialisez pas avec un README (évitez les conflits de fusion).
3. Copiez l'URL de la télécommande HTTPS.
4. Ajoutez la télécommande et poussez :

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

### 3) Mises à jour continues

```bash
git status
git add .
git commit -m "Update memory"
git push
```

## Ne validez pas les clés

Même dans les référentiels privés, évitez de stocker les clés dans l'espace de travail :

- Clés API, tokens OAuth, mots de passe ou identifiants privés.
- Tout ce qui se trouve sous `~/.openclaw/`.
- Vidages bruts de conversations ou pièces jointes sensibles.

Si vous devez stocker des références sensibles, utilisez des espaces réservés et conservez les vraies clés ailleurs (gestionnaire de mots de passe, variables d'environnement ou `~/.openclaw/`).

Configuration `.gitignore` recommandée pour commencer :

```gitignore
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Migrer l'espace de travail vers une nouvelle machine

1. Clonez le référentiel vers le chemin souhaité (par défaut `~/.openclaw/workspace`).
2. Définissez `agents.defaults.workspace` sur ce chemin dans `~/.openclaw/openclaw.json`.
3. Exécutez `openclaw setup --workspace <path>` pour remplir les fichiers manquants.
4. Si vous avez besoin de sessions, copiez séparément `~/.openclaw/agents/<agentId>/sessions/` de l'ancienne machine.

## Remarques avancées

- L'acheminement multi-agents peut utiliser des espaces de travail différents pour chaque agent. Voir
  [Acheminement des canaux](/channels/channel-routing) pour la configuration de l'acheminement.
- Si `agents.defaults.sandbox` est activé, les sessions non principales peuvent utiliser des espaces de travail de bac à sable par session sous `agents.defaults.sandbox.workspaceRoot`.
