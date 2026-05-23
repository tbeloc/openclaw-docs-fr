---
summary: "Plugin Meeting Notes : capturer les transcriptions des appels vocaux Discord et des sources de réunion importées, puis rédiger des résumés"
read_when:
  - You want OpenClaw to take meeting notes
  - You are wiring Discord voice, Google Meet, Slack huddles, or another meeting source into notes
  - You need the meeting_notes tool contract
title: "Plugin Meeting Notes"
---

Le plugin Meeting Notes est la couche de notes générique pour les appels en direct et les transcriptions de réunions importées. Il gère le stockage des transcriptions, le rendu des résumés et l'outil `meeting_notes`. Les plugins de canal gèrent la capture, l'authentification et les jointures de réunion spécifiques à la plateforme.

Utilisez cette page lorsque vous souhaitez qu'OpenClaw capture les notes vocales Discord dès aujourd'hui, lorsque vous souhaitez importer une transcription d'un autre système de réunion, ou lorsque vous créez un fournisseur de source Google Meet, Slack huddle, Zoom ou propriétaire du calendrier.

## Modèle de source

Les sources de réunion enregistrent `meetingNotesSourceProviders` via le SDK du plugin. Le premier fournisseur en direct est `discord-voice` ; le fournisseur intégré `manual-transcript` importe les transcriptions post-réunion.

- `live-audio` : la source rejoint ou écoute un appel et diffuse les énoncés finaux.
- `live-caption` : la source lit les sous-titres d'une surface de navigateur ou de réunion.
- `posthoc-transcript` : la source importe un artefact de transcription ou de notes après la réunion.
- `recording-stt` : la source transcrit un enregistrement avant d'importer les énoncés.

Cela maintient Discord, Google Meet, Slack huddles et les futures surfaces de réunion en dehors du moteur de notes. Chaque source fournit des énoncés étiquetés par orateur ; Meeting Notes écrit les artefacts et le résumé.

## Installation et activation

Meeting Notes est un plugin de source externe dans ce référentiel. Il ne fait pas partie du package npm OpenClaw principal et ne devient disponible que lorsque le plugin est installé en tant que plugin ou chargé à partir d'une extraction de source contenant `extensions/meeting-notes`.

Une fois le plugin chargé, il est activé par défaut sauf si l'un de ces paramètres le bloque :

- `plugins.enabled: false` désactive tous les plugins.
- `plugins.deny` contient `meeting-notes`.
- `plugins.allow` est défini et ne contient pas `meeting-notes`.
- `plugins.entries.meeting-notes.enabled: false` désactive cette entrée de plugin.
- `plugins.entries.meeting-notes.config.enabled: false` garde le plugin chargé mais désactive l'outil `meeting_notes` et le service de démarrage automatique.

Le fichier de configuration utilisateur normal est `~/.openclaw/openclaw.json`. La section `plugins` contrôle le chargement des plugins, et l'objet imbriqué `entries.<pluginId>.config` est transmis à ce plugin en tant que configuration spécifique au plugin. Un bloc `config: { ... }` séparé sous `meeting-notes` est attendu ; c'est ainsi que les plugins reçoivent leurs propres options sans ajouter de clés de configuration principale.

Utilisez cette forme lorsque votre configuration a une liste d'autorisation de plugins :

```json5
{
  plugins: {
    allow: ["discord", "meeting-notes"],
    entries: {
      "meeting-notes": {
        enabled: true,
        config: {
          enabled: true,
          maxUtterances: 2000,
          autoStart: [],
        },
      },
    },
  },
}
```

Exécutez une vérification de configuration après modification :

```bash
openclaw config validate
```

Le rechargement à chaud de la configuration de la passerelle applique les modifications de la liste d'autorisation des plugins et des entrées de plugin. Redémarrez la passerelle si vous modifiez également le plugin source lui-même, installez de nouveaux fichiers de plugin ou modifiez les identifiants Discord voice.

## Configuration

Meeting Notes a trois champs de configuration de plugin :

- `enabled` : `true` par défaut. Définissez `false` pour laisser le plugin installé mais désactiver l'outil et le service de démarrage automatique.
- `maxUtterances` : `2000` par défaut. La génération de résumé lit uniquement les N énoncés les plus récents de `transcript.jsonl` ; les valeurs valides sont limitées à `1` à `10000`.
- `autoStart` : vide par défaut. Chaque entrée démarre une source de notes en direct lorsque la passerelle démarre ou recharge le plugin.

Une entrée `autoStart` accepte :

- `providerId` : obligatoire. Utilisez `discord-voice` pour Discord voice.
- `enabled` : optionnel, par défaut `true`. Définissez `false` pour conserver une entrée sans la démarrer.
- `sessionId` : optionnel. S'il est omis, OpenClaw génère un identifiant horodaté.
- `title` : titre lisible optionnel pour les résumés et la sortie CLI.
- `accountId` : identifiant de compte de source optionnel lorsque plusieurs comptes existent.
- `guildId` : identifiant de guilde Discord spécifique au fournisseur.
- `channelId` : identifiant de canal vocal Discord spécifique au fournisseur.
- `meetingUrl` : URL de réunion spécifique au fournisseur pour les sources de navigateur ou de calendrier.

Utilisez `autoStart` lorsqu'OpenClaw doit commencer la capture de notes automatiquement au démarrage de la passerelle :

```json5
{
  plugins: {
    entries: {
      "meeting-notes": {
        config: {
          autoStart: [
            {
              providerId: "discord-voice",
              guildId: "123",
              channelId: "456",
              title: "Weekly planning",
            },
          ],
        },
      },
    },
  },
}
```

Le démarrage automatique réessaie les défaillances de démarrage jusqu'à 12 fois avec un délai de cinq secondes. Cela permet au service de notes d'attendre que les plugins de canal tels que Discord terminent l'initialisation. Les sessions qui ont été démarrées par démarrage automatique sont arrêtées et résumées lorsque le service de plugin s'arrête correctement.

La capture vocale Discord nécessite toujours la configuration et les autorisations Discord voice normales. Voir [Discord voice](/fr/channels/discord#voice-mode).

## Discord voice

Discord est la première source en direct. Le plugin Discord gère la connexion vocale, la détection du locuteur, le décodage audio et la transcription. Meeting Notes reçoit les énoncés finaux étiquetés par orateur et les persiste.

Pour la capture en direct Discord :

- Activez et configurez d'abord le plugin Discord.
- Configurez le mode vocal Discord pour qu'OpenClaw puisse rejoindre le canal vocal cible.
- Utilisez `providerId: "discord-voice"`.
- Fournissez `guildId` et `channelId`.
- Ajoutez `accountId` uniquement lorsque vous exécutez plus d'un compte Discord.

Le modèle de transcription n'est pas choisi par Meeting Notes. En mode vocal Discord `stt-tts`, STT utilise `tools.media.audio` ; `voice.model` contrôle le modèle de réponse de l'agent, pas la transcription. En modes vocaux en temps réel, la transcription suit le fournisseur et le modèle en temps réel configurés. Voir [Discord voice](/fr/channels/discord#voice-mode) pour les boutons actuels du modèle et du fournisseur vocal Discord.

## Google Meet, Slack huddles et autres sources

Meeting Notes est intentionnellement neutre par rapport à la source. Google Meet, Slack huddles, Zoom, enregistrements de calendrier ou capture de sous-titres de navigateur doivent être des fournisseurs de source séparés qui s'enregistrent auprès du SDK du plugin.

Choix de source recommandés :

- Support de navigateur/sous-titres en direct Google Meet : implémentez un fournisseur `live-caption` qui accepte `meetingUrl` et émet les énoncés de sous-titres finaux.
- Enregistrements Google Meet ou transcriptions téléchargées : implémentez `posthoc-transcript` ou utilisez `manual-transcript` jusqu'à ce qu'un fournisseur existe.
- Slack huddles aujourd'hui : importez les notes ou les artefacts de transcription post-huddle. Slack n'expose pas une API audio huddle en direct générale pour les bots.
- Slack huddles plus tard : gardez le fournisseur de source propriétaire de Slack responsable de l'authentification Slack, de la recherche d'artefacts et de la normalisation des transcriptions.

Le moteur de notes ne doit pas contenir de jointures de plateforme, d'automatisation de navigateur, d'interrogation d'API Slack ou de logique vocale Discord. Ceux-ci appartiennent au plugin source propriétaire.

## Outil

Utilisez `meeting_notes` avec une `action` :

- `status` : lister les fournisseurs enregistrés et les sessions actives.
- `start` : démarrer une session de notes en direct.
- `stop` : arrêter une session en direct et écrire `summary.md`.
- `import` : importer une transcription et écrire `summary.md`.
- `summarize` : régénérer un résumé pour une session existante.

Les notes en direct Discord nécessitent `providerId: "discord-voice"`, plus `guildId` et `channelId`. `accountId` est optionnel lorsqu'un seul compte Discord est actif.

```json
{
  "action": "start",
  "providerId": "discord-voice",
  "guildId": "123",
  "channelId": "456",
  "title": "Weekly planning"
}
```

Arrêtez par identifiant de session :

```json
{
  "action": "stop",
  "sessionId": "meeting-2026-05-22T10-00-00-000Z-a1b2c3d4"
}
```

Importer une transcription :

```json
{
  "action": "import",
  "providerId": "manual-transcript",
  "title": "Design review",
  "transcript": "Alex: We decided to ship the Discord source first.\nSam: Action item: add Slack huddle import later."
}
```

`manual-transcript` divise le texte de transcription brut en énoncés. Utilisez-le pour les notes Google Meet copiées, les résumés Slack huddle, les transcriptions de calendrier ou toute source qui a déjà produit du texte.

## Disposition du stockage

Les artefacts sont stockés dans le répertoire d'état OpenClaw :

```text
$OPENCLAW_STATE_DIR/meeting-notes/YYYY-MM-DD/<session>/
  metadata.json
  transcript.jsonl
  summary.json
  summary.md
```

Si `OPENCLAW_STATE_DIR` n'est pas défini, le répertoire d'état par défaut est `~/.openclaw`. Une installation locale normale écrit donc les notes sous `~/.openclaw/meeting-notes/...`.

Chaque fichier a un travail :

- `metadata.json` : identifiant de session, fournisseur de source, titre, heure de début, heure d'arrêt et métadonnées du fournisseur.
- `transcript.jsonl` : énoncés de locuteur en ajout uniquement. Chaque ligne est un objet JSON avec le texte de l'énoncé et l'identifiant de session.
- `summary.json` : données de résumé structurées utilisées par les outils.
- `summary.md` : notes lisibles par l'homme pour les terminaux, les éditeurs et les flux de travail de documents.

Le répertoire de date provient de l'heure de début de la session, donc plusieurs réunions par jour restent groupées. Si un identifiant de session humain se répète sur plusieurs jours, utilisez le sélecteur qualifié par date de `openclaw meeting-notes list`, tel que `2026-05-22/standup`.

Par défaut, OpenClaw génère des identifiants de session horodatés :

```text
meeting-2026-05-22T10-00-00-000Z-a1b2c3d4
```

Cela signifie que dix réunions le même jour deviennent dix répertoires frères :

```text
~/.openclaw/meeting-notes/2026-05-22/
  meeting-2026-05-22T09-00-00-000Z-a1b2c3d4/
  meeting-2026-05-22T10-30-00-000Z-b2c3d4e5/
  meeting-2026-05-22T13-00-00-000Z-c3d4e5f6/
```

Configurez `sessionId` uniquement lorsque cet identifiant est unique pour la journée. Les identifiants humains tels que `standup` conviennent à une réunion récurrente par jour. Si le même identifiant apparaît sur plusieurs jours, utilisez le sélecteur qualifié par date dans la CLI.

## Accès CLI

Utilisez la CLI en lecture seule pour trouver ou imprimer les résumés stockés :

```bash
openclaw meeting-notes list
openclaw meeting-notes show <session>
openclaw meeting-notes path <session>
openclaw meeting-notes path <session> --transcript
```

Voir [Meeting Notes CLI](/fr/cli/meeting-notes) pour la référence complète des commandes.

## Réunions longues

Pour les réunions longues, les énoncés sont ajoutés à `transcript.jsonl` à mesure qu'ils arrivent. La génération de résumé lit une fenêtre délimitée contrôlée par `plugins.entries.meeting-notes.config.maxUtterances` (par défaut : `2000`) afin qu'un appel de plusieurs heures ne nécessite pas une mémoire de résumé illimitée.

Cela signifie que la transcription peut continuer à croître sur le disque, tandis que la résumé reste délimitée. Augmentez `maxUtterances` lorsque vous avez besoin de plus d'une réunion de plusieurs heures dans le résumé généré. Diminuez-le lorsque les résumés sont trop lents ou trop volumineux.

Les résumés actuels sont générés lorsqu'une session s'arrête, après une importation, ou lorsque l'action `summarize` s'exécute. Ils ne sont pas continuellement réécrits pour chaque énoncé.

## Dépannage

### `meeting_notes` est manquant

Vérifiez que le plugin est installé ou chargé à partir de la source, et que le chargement du plugin ne l'exclut pas :

```bash
openclaw config validate
openclaw meeting-notes list
```

Si `plugins.allow` est défini, il doit inclure `meeting-notes`. Si `plugins.deny` contient `meeting-notes`, supprimez-le.

### L'auto-démarrage ne rejoint pas Discord

Confirmez que l'entrée `autoStart` utilise `providerId: "discord-voice"` et inclut à la fois `guildId` et `channelId`. Si vous exécutez plusieurs comptes Discord, incluez `accountId`. Vérifiez également que la voix Discord fonctionne en dehors de Meeting Notes en rejoignant le même canal vocal via les commandes vocales Discord.

### Le résumé est manquant

Les sessions en direct écrivent `summary.md` lors de l'arrêt. Arrêtez la session avec l'action `meeting_notes` `stop`, puis inspectez-la :

```bash
openclaw meeting-notes list
openclaw meeting-notes path <session>
```

Utilisez l'action `meeting_notes` `summarize` pour régénérer `summary.md` pour une session stockée existante.

### Le sélecteur est ambigu

Si vous avez réutilisé un identifiant de session humaine tel que `standup`, utilisez le sélecteur qualifié par la date affiché par `openclaw meeting-notes list` :

```bash
openclaw meeting-notes show 2026-05-22/standup
```

## Connexes

- [Meeting Notes CLI](/fr/cli/meeting-notes)
- [Voix Discord](/fr/channels/discord#voice-mode)
- [Gestion des plugins](/fr/tools/plugin)
- [Architecture des plugins](/fr/plugins/architecture)
