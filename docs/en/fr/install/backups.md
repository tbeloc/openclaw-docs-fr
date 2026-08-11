---
summary: "Sauvegarder l'état d'OpenClaw : archives, snapshots par base de données, planification, copies hors site et réplication continue"
read_when:
  - You want a backup routine for an OpenClaw install instead of a one-off archive
  - You want scheduled, offsite, or continuous backups without copying the whole database every time
  - You need to restore OpenClaw state from a backup
title: "Sauvegardes"
---

# Sauvegardes

OpenClaw conserve son état faisant autorité dans SQLite : une base de données de plan de contrôle global plus une base de données par agent, toutes situées dans le répertoire d'état (généralement `~/.openclaw`). Voir [Schémas de base de données](/fr/reference/database-schemas) pour la disposition exacte. Ce guide couvre la protection de cet état : archives ponctuelles, snapshots par base de données, planification, copies hors site et réplication continue pour les installations qui ne doivent pas réuploader des bases de données entières à chaque sauvegarde.

Ne copiez jamais les fichiers `.sqlite`, `-wal`, `-shm` ou `-journal` actifs comme sauvegarde. Les bases de données sont écrites pendant que la passerelle s'exécute, et les copies de fichiers bruts d'une base de données active peuvent être déchirées ou corrompues. Chaque chemin pris en charge ci-dessous capture l'état validé en toute sécurité.

<Warning>
  Les sauvegardes contiennent des profils d'authentification, des identifiants de canal et de fournisseur, l'historique des sessions et d'autres enregistrements sensibles. Stockez-les chiffrés, limitez la destination comme vous limitez le répertoire d'état actif et renouvelez les identifiants si vous soupçonnez qu'une sauvegarde a fui. Voir [Migration entre machines](/fr/install/migrating) pour les mêmes règles appliquées aux déplacements de machines.
</Warning>

## Choisir un chemin

- Ponctuel, tout, portable : `openclaw backup create` archive.
- Une base de données, compact et vérifié : `openclaw backup sqlite create`.
- Protection régulière : planifiez l'une ou l'autre commande et synchronisez la sortie hors site.
- Continu, incrémental, quelques secondes de perte de données : répliquez les bases de données avec Litestream.

## Archives complètes

```bash
openclaw backup create --output ~/Backups/openclaw --verify
```

Cela écrit un `.tar.gz` horodaté couvrant l'état, la configuration, les identifiants, les sessions et (par défaut) les espaces de travail, puis valide le manifeste et la charge utile de l'archive. Les bases de données SQLite à l'intérieur de l'archive sont capturées avec l'API de sauvegarde en ligne de SQLite et compactées, de sorte que l'archive est sûre à créer pendant que la passerelle s'exécute. [Sauvegarde CLI](/fr/cli/backup) documente chaque drapeau, les fichiers volatiles qui sont intentionnellement ignorés et les détails de vérification.

Les archives sont des copies complètes : chaque exécution réupload tout. Elles sont l'outil approprié avant une mise à jour, une réinitialisation, une désinstallation ou un déplacement de machine, et une routine quotidienne raisonnable pour les petites installations. Pour les grands espaces de travail ou les sauvegardes fréquentes, préférez les snapshots ou la réplication continue ci-dessous.

## Snapshots par base de données

```bash
openclaw backup sqlite create --global --repository ~/Backups/openclaw-sqlite
openclaw backup sqlite create --agent main --repository ~/Backups/openclaw-sqlite
```

Chaque exécution publie un répertoire de snapshot vérifié (`manifest.json` plus `database.sqlite`) dans le répertoire du référentiel. Les snapshots sont aspirés, de sorte que les vestiges de pages supprimées ne les gonflent pas, et chaque snapshot enregistre un SHA-256 que `openclaw backup sqlite verify` revérifie plus tard.

Les référentiels de snapshots sont des répertoires locaux. La planification, le téléchargement, la rétention et la restauration au démarrage sont intentionnellement laissés à l'opérateur ; les sections ci-dessous les couvrent.

## Planifier les sauvegardes

Utilisez le planificateur de votre plateforme. Un exemple cron nocturne qui snapshots la base de données du plan de contrôle et la base de données de l'agent `main` :

```bash
0 3 * * * openclaw backup sqlite create --global --repository "$HOME/Backups/openclaw-sqlite" --json >> "$HOME/Backups/openclaw-backup.log" 2>&1
5 3 * * * openclaw backup sqlite create --agent main --repository "$HOME/Backups/openclaw-sqlite" --json >> "$HOME/Backups/openclaw-backup.log" 2>&1
```

Sur macOS, une tâche `launchd` fonctionne de la même manière ; sur les serveurs provisionnés à partir des [guides d'hébergement](/fr/install), un minuteur systemd est le choix naturel. `--json` émet un résultat lisible par machine par exécution, de sorte que le journal double comme piste d'audit de sauvegarde. Élaguez les anciens répertoires de snapshots selon votre propre calendrier de rétention.

## Copier les sauvegardes hors site

Les archives et les référentiels de snapshots sont des fichiers simples, donc n'importe quel outil de synchronisation fonctionne. Un exemple `rclone` ciblant un bucket compatible S3 :

```bash
rclone sync ~/Backups/openclaw-sqlite remote:openclaw-backups/sqlite
```

Parce que chaque archive et snapshot est une copie complète, les synchronisations hors site réuploadent chaque nouvelle sauvegarde en intégralité. Les outils de sauvegarde dédupliquants tels que `restic` réduisent le stockage à la destination mais lisent toujours les snapshots complets en entrée. Lorsque la taille de téléchargement par sauvegarde est importante, utilisez plutôt la réplication continue.

## Réplication continue avec Litestream

[Litestream](https://litestream.io) est un démon de réplication open-source pour SQLite. Il s'exécute aux côtés de la passerelle sans modifications d'OpenClaw : il surveille le journal d'écriture anticipée de chaque base de données et diffuse les modifications incrémentielles vers le stockage d'objets, avec des snapshots périodiques pour que les restaurations restent rapides. Seules les pages modifiées quittent la machine, ce qui en fait l'outil approprié lorsque les sauvegardes ne doivent pas réuploader des bases de données entières.

Les bases de données d'OpenClaw s'exécutent en mode WAL, ce qui est l'une des exigences strictes de Litestream. Un `litestream.yml` minimal répliquant la base de données du plan de contrôle et une base de données d'agent vers un bucket compatible S3 :

```yaml
dbs:
  - path: /home/user/.openclaw/state/openclaw.sqlite
    replicas:
      - url: s3://openclaw-backups/state
  - path: /home/user/.openclaw/agents/main/agent/openclaw-agent.sqlite
    replicas:
      - url: s3://openclaw-backups/agents/main
```

Exécutez `litestream replicate` sous votre superviseur de processus, une entrée par base de données qui vous intéresse. Pour récupérer, restaurez vers un chemin frais et activez-le hors ligne :

```bash
litestream restore -o ./restored-openclaw.sqlite s3://openclaw-backups/state
```

Litestream réplique uniquement les octets de base de données. Les fichiers de configuration, les identifiants et les espaces de travail ont toujours besoin de l'un des chemins basés sur des fichiers ci-dessus, et les données répliquées sont aussi sensibles que les archives, donc appliquez les mêmes règles d'accès au bucket et de chiffrement.

## Restaurer

La restauration est délibérément explicite ; rien ne remplace une base de données active sur place :

1. Arrêtez la passerelle.
2. Pour les archives : extrayez dans un répertoire de staging et suivez le mappage source-à-archive `manifest.json` pour remettre les fichiers en place ; voir [Mise à jour](/fr/install/updating#rollback) pour le flux de travail de restauration.
3. Pour les snapshots : `openclaw backup sqlite restore <snapshot-directory> --target <new-database-path>` écrit une base de données re-vérifiée vers une cible fraîche. Déplacez-la en place pendant que la passerelle est arrêtée.
4. Pour Litestream : `litestream restore` écrit un fichier de base de données frais ; déplacez-le en place de la même manière.
5. Démarrez la passerelle et vérifiez `openclaw health` et `openclaw doctor`.

Après restauration sur une version OpenClaw différente, préflight la base de données d'abord avec `openclaw database preflight` ; voir [Schémas de base de données](/fr/reference/database-schemas#preflight-a-target-release).

## Connexes

- [Espace de travail d'agent](/fr/concepts/agent-workspace#git-backup-recommended-private) pour conserver les fichiers d'espace de travail dans un référentiel git privé
- [Référence CLI de sauvegarde](/fr/cli/backup)
- [Schémas de base de données](/fr/reference/database-schemas)
- [Migration entre machines](/fr/install/migrating)
- [Mise à jour](/fr/install/updating)
