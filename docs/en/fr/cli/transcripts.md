---
summary: "Référence CLI pour `openclaw transcripts` (lister, afficher et localiser les transcriptions stockées)"
read_when:
  - You want to read stored transcript summaries from the terminal
  - You need the path to a transcripts markdown summary
  - You are debugging the core transcripts storage layout
title: "Transcripts CLI"
---

# `openclaw transcripts`

Inspectez les transcriptions écrites par l'outil `transcripts` principal d'OpenClaw. Cette CLI est en lecture seule ; la capture, l'importation et la synthèse sont gérées par l'outil agent et les sources de démarrage automatique configurées.

Utilisez la CLI lorsque vous souhaitez trouver les notes d'hier, ouvrir le fichier Markdown dans un éditeur, transmettre une transcription à un autre outil ou déboguer où une session s'est retrouvée sur le disque. Elle ne démarre ni n'arrête la capture.

Les artefacts se trouvent dans le répertoire d'état d'OpenClaw :

```text
$OPENCLAW_STATE_DIR/transcripts/YYYY-MM-DD/<session>/
  metadata.json
  transcript.jsonl
  summary.json
  summary.md
```

Le répertoire d'état par défaut est `~/.openclaw` ; définissez `OPENCLAW_STATE_DIR` pour en utiliser un différent. Le répertoire de date provient de l'heure de début de la session, et le répertoire de session est un segment de système de fichiers sécurisé dérivé de l'identifiant de session.

## Commandes

```bash
openclaw transcripts list
openclaw transcripts show <session>
openclaw transcripts show YYYY-MM-DD/<session>
openclaw transcripts path <session>
openclaw transcripts path YYYY-MM-DD/<session>
openclaw transcripts path <session> --dir
openclaw transcripts path <session> --metadata
openclaw transcripts path <session> --transcript
openclaw transcripts list --json
openclaw transcripts show <session> --json
openclaw transcripts path <session> --json
```

- `list` : lister les sessions stockées, le sélecteur qualifié par date, l'heure de début, le titre et le chemin `summary.md`.
- `show <session>` : afficher le `summary.md` stocké.
- `path <session>` : afficher le chemin `summary.md`.
- `path <session> --dir` : afficher le répertoire de session.
- `path <session> --metadata` : afficher `metadata.json`.
- `path <session> --transcript` : afficher `transcript.jsonl`.
- `--json` : afficher la sortie lisible par machine.

Lorsqu'un identifiant de session humain se répète sur plusieurs jours, utilisez le sélecteur qualifié par date de `list`, par exemple `openclaw transcripts show 2026-05-22/standup`.
Les identifiants de session par défaut incluent un horodatage et un suffixe aléatoire ; configurez les identifiants de session fixes uniquement lorsqu'ils sont uniques dans la journée.

## Sortie

`list` affiche une session par ligne :

```text
2026-05-22/standup  2026-05-22T09:00:00.000Z  Weekly standup  /Users/alex/.openclaw/transcripts/2026-05-22/standup/summary.md
```

La sortie est séparée par des tabulations. Les colonnes sont le sélecteur, l'heure de début, le titre et le chemin du résumé. Le sélecteur est la valeur la plus sûre à repasser à `show` ou `path`.

`list --json` affiche les objets avec :

- `sessionId`
- `selector`
- `date`
- `title`
- `startedAt`
- `stoppedAt`
- `source`
- `path`
- `summaryPath`
- `hasSummary`

`show --json` retourne les métadonnées de session stockées, le sélecteur, le répertoire de session, le chemin du résumé et le texte Markdown du résumé. `path --json` retourne le chemin sélectionné et si ce fichier existe.

## Plusieurs réunions par jour

Les transcriptions regroupent les sessions par date, puis par identifiant de session. Dix réunions en un jour deviennent dix dossiers frères :

```text
~/.openclaw/transcripts/2026-05-22/
  transcript-2026-05-22T09-00-00-000Z-a1b2c3d4/
  transcript-2026-05-22T10-30-00-000Z-b2c3d4e5/
  standup/
```

Utilisez les identifiants générés par défaut pour la plupart des automatisations. Utilisez un identifiant fixe tel que `standup` uniquement lorsque le même identifiant ne sera pas utilisé deux fois le même jour.

## Résumés manquants

Les sessions en direct écrivent `summary.md` lorsque la session s'arrête. Les transcriptions importées écrivent `summary.md` immédiatement après l'importation. Une session peut toujours apparaître dans `list` sans résumé lorsque la capture est active, qu'un fournisseur a échoué lors de l'arrêt, ou que les métadonnées ont été écrites avant l'arrivée d'énoncés.

Utilisez `path <session> --transcript` pour inspecter la transcription en ajout seul, et utilisez l'action `summarize` de l'outil `transcripts` pour régénérer le résumé Markdown.

## Configuration

La capture de transcription est optionnelle car les sources en direct peuvent rejoindre et enregistrer l'audio de réunion. Activez l'outil avec `transcripts.enabled` au niveau supérieur :

```json
{
  "transcripts": {
    "enabled": true,
    "maxUtterances": 2000
  }
}
```

Configurez les sources de démarrage automatique avec `transcripts.autoStart` dans `openclaw.json`.
Chaque entrée est activée par sa présence ; omettez une entrée pour désactiver cette source.

```json
{
  "transcripts": {
    "enabled": true,
    "autoStart": [
      {
        "providerId": "discord-voice",
        "guildId": "1234567890",
        "channelId": "2345678901"
      },
      {
        "providerId": "slack-huddle",
        "accountId": "workspace",
        "channelId": "C123"
      }
    ]
  }
}
```
