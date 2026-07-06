---
summary: "Exécutez des tâches d'agent dans des checkouts git isolés avec snapshots automatiques et nettoyage"
read_when:
  - Vous voulez une branche isolée et un checkout pour une tâche d'agent
  - Vous configurez des cartes Workboard avec des espaces de travail worktree
  - Vous devez restaurer ou nettoyer un worktree géré par OpenClaw
title: "Worktrees gérés"
---

Les worktrees gérés donnent à une tâche d'agent sa propre branche git et son propre checkout sans placer de répertoires temporaires à l'intérieur du référentiel source. OpenClaw les crée dans son répertoire d'état, les enregistre dans la base de données d'état partagée, et crée des snapshots de leurs contenus suivis et non ignorés avant suppression.

## Disposition et noms

Chaque worktree se trouve à :

```text
<openclaw-state-dir>/worktrees/<repo-fingerprint>/<name>
```

L'empreinte du référentiel est les 16 premiers caractères hexadécimaux d'un hash SHA-256 sur le répertoire git commun canonique et l'URL d'origine. Un nom fourni doit correspondre à `[a-z0-9][a-z0-9-]{0,63}`. Sans nom, OpenClaw génère `wt-` suivi de huit caractères hexadécimaux aléatoires.

OpenClaw crée la branche `openclaw/<name>` à la ref de base demandée. Sans ref de base, il récupère `origin`, utilise la branche par défaut distante si disponible, et revient à `HEAD` local lorsque le référentiel est hors ligne ou n'a pas de distant utilisable.

## Provisionner les fichiers ignorés

Ajoutez `.worktreeinclude` à la racine du référentiel source pour copier les fichiers ignorés et non suivis sélectionnés dans un nouveau worktree. Le fichier utilise la syntaxe de motif gitignore, un motif par ligne, avec des commentaires `#` :

```gitignore
.env.local
fixtures/generated/**
```

Seuls les fichiers signalés par git comme à la fois ignorés et non suivis sont éligibles. Les fichiers suivis sont déjà présents via git et ne sont jamais copiés par cette étape. OpenClaw ne remplace pas les fichiers de destination ni ne suit les répertoires liés par symlink, et il préserve les modes de fichier copiés.

## Exécuter la configuration du référentiel

Si `.openclaw/worktree-setup.sh` existe dans le référentiel source et est exécutable, OpenClaw l'exécute avec le nouveau worktree comme répertoire courant. Le script reçoit :

```text
OPENCLAW_SOURCE_TREE_PATH=<source checkout>
OPENCLAW_WORKTREE_PATH=<managed worktree>
```

Une sortie non nulle abandonne la création et supprime le nouveau worktree et la branche. C'est un contrat local au référentiel ; il n'y a pas de clé de configuration OpenClaw pour cela.

## Worktrees de session

Démarrez une discussion isolée à partir de l'espace de travail git de l'agent actif avec **Nouvelle discussion dans worktree** : utilisez l'action Nouvelle discussion secondaire dans la barre latérale de l'interface de contrôle, le menu des actions de discussion sur iOS, ou l'action de débordement à côté de Nouvelle discussion sur Android. L'action n'est disponible que pour un agent soutenu par git où le client a cette capacité ; les clients qui ne peuvent pas le prévoler affichent l'erreur de passerelle à la place.

Le worktree géré résultant est détenu par la session, et chaque exécution d'agent dans cette session utilise son checkout. Lorsque l'espace de travail est un sous-répertoire du référentiel, le worktree est ancré à la racine du référentiel et la session s'exécute à partir du sous-répertoire correspondant à l'intérieur. La création de worktree de session utilise la portée `operator.write` de la méthode, mais l'étape `.openclaw/worktree-setup.sh` s'exécute uniquement pour les appelants `operator.admin` car elle exécute du code de référentiel ; le provisionnement `.worktreeinclude` s'applique toujours à chaque appelant. La suppression de la session supprime le worktree uniquement lorsque cela est sans perte. Les worktrees sales ou les branches avec des commits non poussés restent disponibles ; le nettoyage horaire crée des snapshots des worktrees de session après 7 jours d'inactivité, en traitant l'activité de session récente comme une activité de worktree. Les worktrees supprimés restent restaurables à partir de leurs snapshots comme décrit ci-dessous.

## Snapshots, nettoyage et restauration

La suppression crée d'abord un commit synthétique contenant les fichiers suivis et non ignorés non suivis, et l'épingle à `refs/openclaw/snapshots/<id>`. Les fichiers ignorés par git sont exclus de la base de données d'objets du référentiel ; les fichiers sélectionnés par `.worktreeinclude` sont copiés à nouveau lors de la restauration. Si la création du snapshot échoue, la suppression s'arrête. Une suppression forcée explicite peut continuer sans snapshot.

OpenClaw applique ces règles de nettoyage :

- À la fin de l'exécution, il supprime un worktree uniquement lorsque `git status --porcelain` est vide et `git log HEAD --not --remotes --oneline` ne trouve aucun commit non poussé. Sinon, il libère uniquement le verrou d'activité.
- Le nettoyage horaire crée des snapshots et supprime les worktrees inactifs appartenant à Workboard et à la session pendant plus de 7 jours, même s'ils sont sales. Les worktrees manuels ne sont jamais supprimés automatiquement.
- Les enregistrements de snapshot restent restaurables pendant 30 jours. Le nettoyage supprime ensuite la ref de snapshot et la ligne de registre.
- Un verrou de processus OpenClaw actif et tout verrou de worktree git étranger ou non reconnu protègent un worktree de la collecte des ordures.

La restauration recrée `openclaw/<name>` au commit pré-snapshot d'origine, puis reconstruit les différences de snapshot en tant que modifications non indexées et fichiers non suivis. Cela garde le commit de snapshot synthétique hors de l'historique des branches. La ref de snapshot reste enregistrée comme provenance.

## CLI

```bash
openclaw worktrees list [--json]
openclaw worktrees create <repo-root> [--name <name>] [--base-ref <ref>] [--json]
openclaw worktrees remove <id> [--force] [--json]
openclaw worktrees restore <id> [--json]
openclaw worktrees gc [--json]
```

La page **Worktrees** de l'interface de contrôle fournit les mêmes actions de liste, suppression, restauration et nettoyage.

## Méthodes de passerelle

| Méthode             | Objectif                                              |
| ------------------- | ----------------------------------------------------- |
| `worktrees.list`    | Lister les enregistrements de worktree actifs et restaurables. |
| `worktrees.create`  | Créer ou réutiliser un worktree géré nommé.           |
| `worktrees.remove`  | Créer un snapshot et supprimer un worktree.           |
| `worktrees.restore` | Restaurer un worktree supprimé à partir de son snapshot. |
| `worktrees.gc`      | Exécuter le nettoyage d'inactivité, d'orphelin et de rétention maintenant. |

`worktrees.list` nécessite `operator.read`. Les méthodes mutantes nécessitent `operator.admin`.

## Espaces de travail Workboard

Le plugin Workboard fourni [](/fr/plugins/workboard) peut matérialiser un espace de travail de carte en tant que worktree géré :

```json
{
  "kind": "worktree",
  "path": "/absolute/path/to/source-checkout",
  "branch": "main"
}
```

`path` identifie le checkout git source. `branch` est optionnel et devient la ref de base. Lorsque la dispatch démarre le worker de la carte, Workboard crée ou réutilise `wb-<card-id>`, exécute le sous-agent avec le checkout géré comme répertoire de travail, et écrit le chemin et la branche résolus dans la carte. La matérialisation déclenchée par la passerelle nécessite `operator.admin`. À la fin de l'exécution, Workboard supprime le checkout uniquement lorsqu'il est manifestement sans perte ; le travail sale ou les commits non poussés restent disponibles.

Les agents intégrés en sandbox rejettent actuellement un répertoire de travail de tâche en dehors de leur espace de travail d'agent configuré. Utilisez un agent cible non sandboxé pour les cartes de worktree géré Workboard jusqu'à ce que le runtime sandbox supporte un montage de checkout additif.
