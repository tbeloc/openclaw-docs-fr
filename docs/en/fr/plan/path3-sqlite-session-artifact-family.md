---
summary: "Plan Path 3 pour archiver tous les artefacts de transcription SQLite appartenant à une session"
read_when:
  - You are implementing clawdbot-d63.2 / clawdbot-04b
  - You are touching SQLite session retention, reset, delete, or agent-deletion archival
  - You need to distinguish SQLite-era artifact families from legacy JSONL sidecars
title: "Famille d'artefacts de session SQLite Path 3"
---

# Famille d'artefacts de session SQLite Path 3

Cette note définit le périmètre de `clawdbot-d63.2` tandis que `clawdbot-d63.1` possède l'assistant de réinitialisation/suppression/archivage qui chevauche dans `src/config/sessions/session-accessor.sqlite.ts`.
Le fichier d'implémentation était instable lors de cette passe, donc cet artefact enregistre le contrat exact et les points de patch sans entrer en concurrence avec le worker frère.

## Famille faisant autorité

Après le basculement SQLite, les transcriptions de session actives sont des lignes SQLite. La famille d'archivage d'une session est :

- Les lignes `transcript_events`, `transcript_event_identities` et `sessions` pour le `sessionId` actuel de l'entrée.
- Le même ensemble de lignes de transcription SQLite pour chaque `sessionId` référencé par `entry.compactionCheckpoints[*].preCompaction.sessionId`.
- Le même ensemble de lignes de transcription SQLite pour chaque `sessionId` référencé par `entry.compactionCheckpoints[*].postCompaction.sessionId`.
- Le même ensemble de lignes de transcription SQLite pour chaque `sessionId` dans `entry.usageFamilySessionIds`.

Archivez uniquement les lignes qui ne sont plus référencées par aucune ligne `session_entries` restante ou par aucune métadonnée de compaction ou de famille d'utilisation d'entrée restante. Cela préserve l'état de branche/restauration de point de contrôle et de cumul d'utilisation jusqu'à ce que la dernière référence active disparaisse.

## Artefacts non-famille après le basculement

Les variantes de fichier de transcription de sujet générées et les sidecars de trajectoire ne sont pas un état d'exécution SQLite actif. Ce sont des artefacts de fichier hérités :

- Les variantes de sujet telles que `<sessionId>-topic-<thread>.jsonl` n'existent que pour le format de transcription sauvegardé sur fichier. SQLite utilise l'identifiant de session canonique plus les métadonnées `session_routes`/livraison d'entrée au lieu de fichiers JSONL par sujet.
- Les sidecars de trajectoire tels que `.trajectory.jsonl` et `.trajectory-path.json` sont nommés à partir de chemins réels `sessionFile` JSONL. Les valeurs SQLite `sessionFile` sont des marqueurs `sqlite:<agentId>:<sessionId>:<storePath>` et ne nomment pas de fichiers sidecar.
- Les lecteurs de niveau archive doivent continuer à lire les fichiers JSONL archivés hérités, mais la rétention d'exécution ne doit pas analyser les répertoires de sessions actives ou rouvrir les fichiers de transcription JSONL pour les sessions SQLite.

L'importation Doctor reste le propriétaire de la migration pour les fichiers JSONL primaires hérités et leurs sidecars de trajectoire adjacents. La rétention SQLite d'exécution ne doit pas ajouter un second importateur ou un repli de fichier.

## Points de patch

Étendez l'assistant d'archivage SQLite introduit par `clawdbot-d63.1` plutôt que d'ajouter un chemin parallèle.

1. Ajoutez un collecteur local près de `deleteSqliteSessionStateIfUnreferenced` :
   - `collectSqliteSessionArtifactFamily(entry: SessionEntry): Set<string>`
   - Incluez `entry.sessionId`, les identifiants de session pré/post de point de contrôle et `usageFamilySessionIds`.
   - Filtrez les chaînes vides et dédupliquez de manière déterministe.

2. Ajoutez un collecteur de référence pour le magasin post-suppression :
   - `readReferencedSqliteSessionArtifactFamilyIds(database): Set<string>`
   - Itérez les `session_entries` actuelles, analysez chaque `entry_json` et collectez les mêmes identifiants de famille de chaque entrée survivante.

3. Modifiez les appelants de réinitialisation/suppression/maintenance qui archivaient actuellement un `sessionId` supprimé pour passer la famille complète de l'entrée supprimée.

4. Pour chaque identifiant de famille, archivez les lignes de transcription SQLite avec la raison de l'appelant (`reset` ou `deleted`), puis supprimez la ligne `sessions` uniquement lorsque l'identifiant de famille est absent de l'ensemble de référence post-suppression.

5. Gardez la suppression d'événement de transcription centralisée via le chemin de nettoyage de ligne de session SQLite existant. N'ajoutez pas de lectures JSONL actives.

## Tests ciblés

Ajoutez des tests SQLite uniquement à `src/config/sessions/session-accessor.conformance.test.ts` ou au test de cycle de vie frère après le commit de `clawdbot-d63.1` :

- La suppression d'une entrée avec une transcription pré-compaction archive à la fois la session actuelle et la session pré-compaction, puis supprime les deux ensembles de lignes SQLite.
- La suppression d'une des deux entrées qui partagent une pré-session de compaction n'archive rien pour la pré-session partagée jusqu'à ce que la dernière entrée de référence soit supprimée.
- La suppression d'une entrée avec `usageFamilySessionIds` archive les lignes de transcription SQLite prédécesseur lorsqu'aucune autre entrée ne référence cette famille d'utilisation.
- Une clé de session en forme de sujet avec un marqueur SQLite ne provoque aucune lecture JSONL de sujet générée ou recherche de sidecar.

La preuve ciblée doit utiliser :

```bash
node scripts/run-vitest.mjs src/config/sessions/session-accessor.conformance.test.ts
```

Si les tests finaux se trouvent dans `store.session-lifecycle-mutation.test.ts`, exécutez ce fichier explicitement avec le même wrapper. Les portes `pnpm` larges doivent rester sur Crabbox/Testbox pour ce worktree Codex.
