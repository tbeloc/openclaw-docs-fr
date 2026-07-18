---
summary: "Emplacements de la base de données SQLite OpenClaw, versions de schéma, vérifications d'intégrité et récupération de rétrogradation"
read_when:
  - Diagnosing a newer database schema error
  - Checking database compatibility before an update or downgrade
  - Recovering a database for an older OpenClaw release
title: "Schémas de base de données"
---

OpenClaw stocke l'état du plan de contrôle dans une base de données SQLite globale et les données des agents dans une base de données SQLite par agent. Les migrations de schéma s'exécutent vers l'avant lorsqu'une base de données s'ouvre. Les versions plus anciennes d'OpenClaw refusent les bases de données écrites par un schéma plus récent.

## Disposition de la base de données

| Portée                | Chemin par défaut                                          | Contenu                                                                                              |
| -------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Plan de contrôle global | `~/.openclaw/state/openclaw.sqlite`                        | État de configuration partagée, registres, approbations, état des plugins et historique de vérification             |
| Plan de données par agent | `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite` | Sessions, transcriptions, index de mémoire, état d'authentification, état de conversation et état d'exécution limité à l'agent |

Quelques fonctionnalités à haut volume ou spécifiques au cycle de vie utilisent des magasins SQLite dédiés, notamment le registre des tâches et les données de trajectoire.

## Contrat de versioning

Chaque base de données enregistre son schéma à deux endroits :

- `PRAGMA user_version` est la version du schéma SQLite.
- La ligne `schema_meta` primaire enregistre `role`, `agent_id`, `schema_version` et `app_version`. `app_version` est la version d'OpenClaw qui a écrit en dernier les métadonnées du schéma.

OpenClaw applique des migrations avant uniquement lorsqu'il ouvre une base de données plus ancienne prise en charge. Il refuse une base de données dont `user_version` est plus récente que la version en cours d'exécution et signale une erreur `newer schema version`. La passerelle vérifie toutes les bases de données enregistrées avant le démarrage. `openclaw update` refuse également un package ou une cible source dont le support de schéma déclaré est plus ancien qu'une base de données sur disque. Les packages cibles publiés avant l'ajout des métadonnées de schéma ne peuvent pas être préfligés.

L'installation manuelle d'OpenClaw via npm contourne la protection du programme de mise à jour. Les vérifications d'ouverture de base de données refusent toujours une version incompatible.

## Historique du schéma d'agent

| Version | Modification                                                                                                                                                                                                                                                         | Première version                                   |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| 1       | Magasin initial par agent ([#88349](https://github.com/openclaw/openclaw/pull/88349))                                                                                                                                                                            | `v2026.5.30-beta.1`, stable jusqu'à `v2026.7.1` |
| 2       | Identité de l'index de mémoire ([#104449](https://github.com/openclaw/openclaw/pull/104449))                                                                                                                                                                            | `v2026.7.2-beta.1`                              |
| 4       | Sessions et transcriptions déplacées dans SQLite ([#98236](https://github.com/openclaw/openclaw/pull/98236))                                                                                                                                                         | `v2026.7.2-beta.1`                              |
| 5-6     | Fraîcheur du terminal et cycle de vie de l'état ([#104859](https://github.com/openclaw/openclaw/pull/104859))                                                                                                                                                           | `v2026.7.2-beta.1`                              |
| 7       | Projection d'état du cycle de vie par entrée ([#106151](https://github.com/openclaw/openclaw/pull/106151))                                                                                                                                                            | `v2026.7.2-beta.1`                              |
| 8       | Provenance de session par transcription ([#106766](https://github.com/openclaw/openclaw/pull/106766))                                                                                                                                                                | `v2026.7.2-beta.2`                              |
| 9       | Tables `STRICT` ([#108663](https://github.com/openclaw/openclaw/pull/108663))                                                                                                                                                                                  | `v2026.7.2-beta.2`                              |
| 10      | Chemins de transcription active matérialisés ([#108851](https://github.com/openclaw/openclaw/pull/108851))                                                                                                                                                             | Non publié                                      |
| 11      | Baux, livraison durable, adresses de conversation et résultats de battement cardiaque ([#109636](https://github.com/openclaw/openclaw/pull/109636), [#95838](https://github.com/openclaw/openclaw/pull/95838), [#109999](https://github.com/openclaw/openclaw/pull/109999)) | Non publié                                      |

La version 3 était une étape de développement non expédiée intégrée à la version 4.

## Historique du schéma d'état

| Version | Modification                                                                                                   | Première version       |
| ------- | -------------------------------------------------------------------------------------------------------- | ------------------- |
| 1       | Base de données d'état partagée initiale                                                                            | `v2026.5.30-beta.1` |
| 2       | Événements d'audit de message métadonnées uniquement ([#103903](https://github.com/openclaw/openclaw/pull/103903))         | `v2026.7.2-beta.1`  |
| 3       | Tables `STRICT` et durcissement contre la dérive de schéma ([#108663](https://github.com/openclaw/openclaw/pull/108663)) | `v2026.7.2-beta.2`  |
| 4       | La provenance de surveillance de session remplace les lignes sentinelles codées                                                  | Non publié          |

## Vérifications d'intégrité

| Quand                                        | Vérification                                                           |
| ------------------------------------------- | --------------------------------------------------------------- |
| À chaque ouverture                                  | Valider la table `schema_meta` et la ligne de métadonnées primaire       |
| Avant une migration en attente                  | Exécuter une analyse complète d'intégrité, de clé étrangère, de rôle, de schéma et d'index |
| Vérificateur d'arrière-plan de la passerelle                 | Exécuter l'analyse complète environ une fois par jour et enregistrer les résultats           |
| Docteur, vérification de sauvegarde et compaction | Exécuter l'analyse complète avant d'accepter ou de réécrire la base de données    |

Le préflight de la passerelle lit uniquement les en-têtes de schéma. Le vérificateur d'arrière-plan possède l'analyse complète plus lente pour les bases de données qui ne nécessitent pas de migration.
Les décisions de mise en quarantaine vivent dans un magasin `openclaw-quarantine.sqlite` dédié, de sorte qu'elles survivent aux dommages aux bases de données en quarantaine. La table `database_verifications` globale reste l'historique de vérification.

## Dépannage

### Pourquoi vous ne pouvez pas revenir après la mise à jour vers 2026.7.2

Chaque version jusqu'à `v2026.7.1` utilisait le schéma d'agent 1 et le schéma d'état 1. La série de versions 2026.7.2 (à partir de `v2026.7.2-beta.1`) migre vos bases de données vers l'avant au premier démarrage. Cette migration est unidirectionnelle : les données sont réécrites dans le nouveau schéma, et l'installation d'une version plus ancienne d'OpenClaw par la suite ne l'annule pas. La version plus ancienne refuse de démarrer avec une erreur `newer schema version` qui nomme la version qui possède la base de données.

La rétrogradation du binaire ne rétrograde jamais les données. Si vous devez exécuter une version antérieure à 2026.7.2 après la mise à jour, vous avez trois options :

1. Restaurer une sauvegarde effectuée avant la mise à jour. [Créez et vérifiez les sauvegardes](/fr/cli/backup) avant les mises à jour majeures.
2. Exécutez la version plus ancienne par rapport à un répertoire d'état séparé (`OPENCLAW_STATE_DIR`). Il démarre à zéro ; vos données migrées restent intactes pour quand vous reviendrez à la version plus récente.
3. Suivez la procédure de rétrogradation manuelle ci-dessous. Elle n'est pas prise en charge et risque une perte de données sans une sauvegarde vérifiée.

Depuis 2026.7.2, `openclaw update` refuse d'installer une version qui ne peut pas ouvrir vos bases de données actuelles, de sorte que le programme de mise à jour ne vous mettra pas dans cette situation. L'installation manuelle d'une version plus ancienne via npm contourne cette protection ; les bases de données refusent toujours le binaire ancien, mais seulement après son installation.

### La passerelle refuse de démarrer avec une erreur de version de schéma plus récente

Une version plus récente d'OpenClaw a écrit vos bases de données, et la version en cours d'exécution est plus ancienne. L'erreur et le journal de démarrage de la passerelle nomment la version qui possède la base de données (`app_version`). Installez cette version ou une version plus récente, ou utilisez l'une des options ci-dessus. Ne modifiez pas la base de données pour supprimer l'erreur.

### Une base de données est mise en quarantaine après l'échec de la vérification d'intégrité

Le vérificateur d'arrière-plan a prouvé que le fichier est corrompu, et chaque ouverture échoue maintenant rapidement au lieu de relancer l'analyse. Restaurez la base de données à partir d'une sauvegarde ou réparez-la, puis exécutez `openclaw doctor --fix` pour effacer l'enregistrement de quarantaine. Le docteur signale une erreur explicite si l'enregistrement de quarantaine lui-même ne peut pas être effacé ; réexécutez-le jusqu'à ce qu'il signale un état propre.

## Les rétrogradations ne sont pas prises en charge

Les rétrogradations manuelles de schéma sont destinées aux agents et aux opérateurs qui acceptent le risque. [Créez et vérifiez une sauvegarde](/fr/cli/backup) avant de modifier une base de données. Arrêtez la passerelle et tous les processus qui peuvent ouvrir la base de données.

La procédure générale est :

1. Lisez le schéma et les migrations de la version cible.
2. Dans une transaction, supprimez chaque table, index, déclencheur et colonne introduits après la version cible.
3. Définissez `PRAGMA user_version` et `schema_meta.schema_version` sur la version cible.
4. Exécutez la vérification complète de la base de données de la version cible avant de démarrer la passerelle.

### Exemple : schéma d'agent 11 à 9

Le schéma 10 a ajouté la projection de transcription active. Le schéma 11 a ajouté les baux, la livraison durable, l'état de l'adresse de conversation et les résultats du battement cardiaque. La coordination QMD utilise des lignes dans `state_leases` ; il n'y a pas de table QMD séparée à conserver.

Exécutez le SQL équivalent par rapport à chaque base de données par agent affectée après inspection du schéma exact qui l'a écrite :

```sql
BEGIN IMMEDIATE;

DROP TABLE IF EXISTS heartbeat_outcomes;
DROP TABLE IF EXISTS conversation_deliveries;
DROP TABLE IF EXISTS state_leases;
DROP TABLE IF EXISTS session_transcript_active_events;

ALTER TABLE session_transcript_index_state DROP COLUMN active_event_count;
ALTER TABLE session_transcript_index_state DROP COLUMN active_message_count;
ALTER TABLE conversations DROP COLUMN delivery_target;

PRAGMA user_version = 9;
UPDATE schema_meta
SET schema_version = 9,
    updated_at = unixepoch('now') * 1000
WHERE meta_key = 'primary';

COMMIT;
```

Cela supprime l'état des versions 10-11, y compris les opérations de livraison en vol, les baux, les résultats du battement cardiaque et la projection de transcription active dérivée. Une rétrogradation ratée signifie restaurer à partir de la sauvegarde vérifiée.
