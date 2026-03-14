```markdown
---
summary: "Espace de travail de l'agent : localisation, disposition et stratégie de sauvegarde"
read_when:
  - You need to explain the agent workspace or its file layout
  - You want to back up or migrate an agent workspace
title: "Agent Workspace"
---

# Espace de travail de l'agent

L'espace de travail est la maison de l'agent. C'est le seul répertoire de travail utilisé pour
les outils de fichiers et pour le contexte de l'espace de travail. Gardez-le privé et traitez-le comme une mémoire.

C'est distinct de `~/.openclaw/`, qui stocke la configuration, les identifiants et les
sessions.

**Important :** l'espace de travail est le **cwd par défaut**, pas un bac à sable strict. Les outils
résolvent les chemins relatifs par rapport à l'espace de travail, mais les chemins absolus peuvent toujours atteindre
ailleurs sur l'hôte sauf si le bac à sable est activé. Si vous avez besoin d'isolation, utilisez
[`agents.defaults.sandbox`](/gateway/sandboxing) (et/ou la configuration de bac à sable par agent).
Lorsque le bac à sable est activé et que `workspaceAccess` n'est pas `"rw"`, les outils fonctionnent
à l'intérieur d'un espace de travail en bac à sable sous `~/.openclaw/sandboxes`, pas votre espace de travail hôte.

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

`openclaw onboard`, `openclaw configure`, ou `openclaw setup` créeront l'
espace de travail et ensemenceront les fichiers d'amorçage s'ils manquent.
Les copies d'amorçage du bac à sable n'acceptent que les fichiers réguliers dans l'espace de travail ; les
alias de lien symbolique/lien physique qui se résolvent en dehors de l'espace de travail source sont ignorés.

Si vous gérez déjà vous-même les fichiers de l'espace de travail, vous pouvez désactiver la création de fichiers d'amorçage :

```json5
{ agent: { skipBootstrap: true } }
```

## Dossiers d'espace de travail supplémentaires

Les installations plus anciennes peuvent avoir créé `~/openclaw`. Garder plusieurs répertoires d'espace de travail
peut causer une dérive confuse de l'authentification ou de l'état, car un seul
espace de travail est actif à la fois.

**Recommandation :** conservez un seul espace de travail actif. Si vous n'utilisez plus les
dossiers supplémentaires, archivez-les ou déplacez-les à la Corbeille (par exemple `trash ~/openclaw`).
Si vous conservez intentionnellement plusieurs espaces de travail, assurez-vous que
`agents.defaults.workspace` pointe vers celui qui est actif.

`openclaw doctor` avertit lorsqu'il détecte des répertoires d'espace de travail supplémentaires.

## Carte des fichiers de l'espace de travail (ce que signifie chaque fichier)

Ce sont les fichiers standard qu'OpenClaw s'attend à trouver dans l'espace de travail :

- `AGENTS.md`
  - Instructions d'exploitation pour l'agent et comment il doit utiliser la mémoire.
  - Chargé au début de chaque session.
  - Bon endroit pour les règles, les priorités et les détails « comment se comporter ».

- `SOUL.md`
  - Persona, ton et limites.
  - Chargé à chaque session.

- `USER.md`
  - Qui est l'utilisateur et comment l'adresser.
  - Chargé à chaque session.

- `IDENTITY.md`
  - Le nom, l'ambiance et l'emoji de l'agent.
  - Créé/mis à jour lors du rituel d'amorçage.

- `TOOLS.md`
  - Notes sur vos outils locaux et conventions.
  - Ne contrôle pas la disponibilité des outils ; c'est seulement un guide.

- `HEARTBEAT.md`
  - Liste de contrôle optionnelle minuscule pour les exécutions de battement cardiaque.
  - Gardez-la courte pour éviter la consommation de jetons.

- `BOOT.md`
  - Liste de contrôle de démarrage optionnelle exécutée au redémarrage de la passerelle lorsque les crochets internes sont activés.
  - Gardez-la courte ; utilisez l'outil de message pour les envois sortants.

- `BOOTSTRAP.md`
  - Rituel de première exécution unique.
  - Créé uniquement pour un espace de travail tout neuf.
  - Supprimez-le après la fin du rituel.

- `memory/YYYY-MM-DD.md`
  - Journal de mémoire quotidien (un fichier par jour).
  - Recommandé de lire aujourd'hui + hier au démarrage de la session.

- `MEMORY.md` (optionnel)
  - Mémoire à long terme organisée.
  - Charger uniquement dans la session principale et privée (pas les contextes partagés/groupe).

Voir [Mémoire](/concepts/memory) pour le flux de travail et le vidage automatique de la mémoire.

- `skills/` (optionnel)
  - Compétences spécifiques à l'espace de travail.
  - Remplace les compétences gérées/groupées en cas de collision de noms.

- `canvas/` (optionnel)
  - Fichiers UI Canvas pour les affichages de nœuds (par exemple `canvas/index.html`).

Si un fichier d'amorçage manque, OpenClaw injecte un marqueur « fichier manquant » dans
la session et continue. Les fichiers d'amorçage volumineux sont tronqués lors de l'injection ;
ajustez les limites avec `agents.defaults.bootstrapMaxChars` (par défaut : 20000) et
`agents.defaults.bootstrapTotalMaxChars` (par défaut : 150000).
`openclaw setup` peut recréer les valeurs par défaut manquantes sans écraser les fichiers existants.

## Ce qui N'EST PAS dans l'espace de travail

Ceux-ci se trouvent sous `~/.openclaw/` et ne doivent PAS être validés dans le référentiel de l'espace de travail :

- `~/.openclaw/openclaw.json` (configuration)
- `~/.openclaw/credentials/` (jetons OAuth, clés API)
- `~/.openclaw/agents/<agentId>/sessions/` (transcriptions de session + métadonnées)
- `~/.openclaw/skills/` (compétences gérées)

Si vous devez migrer des sessions ou une configuration, copiez-les séparément et gardez-les
en dehors du contrôle de version.

## Sauvegarde Git (recommandée, privée)

Traitez l'espace de travail comme une mémoire privée. Mettez-le dans un référentiel git **privé** afin qu'il soit
sauvegardé et récupérable.

Exécutez ces étapes sur la machine où la passerelle s'exécute (c'est là que se trouve l'
espace de travail).

### 1) Initialiser le référentiel

Si git est installé, les espaces de travail tout neufs sont initialisés automatiquement. Si cet
espace de travail n'est pas déjà un référentiel, exécutez :

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

### 2) Ajouter une télécommande privée (options conviviales pour les débutants)

Option A : Interface Web GitHub

1. Créez un nouveau référentiel **privé** sur GitHub.
2. Ne l'initialisez pas avec un README (évite les conflits de fusion).
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

Option C : Interface Web GitLab

1. Créez un nouveau référentiel **privé** sur GitLab.
2. Ne l'initialisez pas avec un README (évite les conflits de fusion).
3. Copiez l'URL de la télécommande HTTPS.
4. Ajoutez la télécommande et poussez :

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

### 3) Mises à jour en cours

```bash
git status
git add .
git commit -m "Update memory"
git push
```

## Ne validez pas les secrets

Même dans un référentiel privé, évitez de stocker des secrets dans l'espace de travail :

- Clés API, jetons OAuth, mots de passe ou identifiants privés.
- Tout ce qui se trouve sous `~/.openclaw/`.
- Vidages bruts de chats ou pièces jointes sensibles.

Si vous devez stocker des références sensibles, utilisez des espaces réservés et gardez le vrai
secret ailleurs (gestionnaire de mots de passe, variables d'environnement, ou `~/.openclaw/`).

Starter `.gitignore` suggéré :

```gitignore
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Déplacer l'espace de travail vers une nouvelle machine

1. Clonez le référentiel vers le chemin souhaité (par défaut `~/.openclaw/workspace`).
2. Définissez `agents.defaults.workspace` sur ce chemin dans `~/.openclaw/openclaw.json`.
3. Exécutez `openclaw setup --workspace <path>` pour ensemencer les fichiers manquants.
4. Si vous avez besoin de sessions, copiez `~/.openclaw/agents/<agentId>/sessions/` de l'
   ancienne machine séparément.

## Notes avancées

- Le routage multi-agent peut utiliser différents espaces de travail par agent. Voir
  [Routage des canaux](/channels/channel-routing) pour la configuration du routage.
- Si `agents.defaults.sandbox` est activé, les sessions non principales peuvent utiliser des espaces de travail en bac à sable par session sous `agents.defaults.sandbox.workspaceRoot`.
```
