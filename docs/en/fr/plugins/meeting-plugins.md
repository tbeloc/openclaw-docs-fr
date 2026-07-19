---
summary: "Choisissez et configurez la participation à des réunions Google Meet, Microsoft Teams ou Zoom"
read_when:
  - You want an OpenClaw agent to join a video meeting
  - You are choosing between the Google Meet, Microsoft Teams meetings, and Zoom meetings plugins
  - You need the shared Chrome, BlackHole, SoX, or meeting-mode setup
title: "Plugins de réunion"
---

OpenClaw dispose de plugins distincts pour Google Meet, les réunions Microsoft Teams et Zoom. Les trois peuvent se joindre via Chrome, utilisent les mêmes modes de participation et exécutent Chrome soit sur l'hôte Gateway, soit sur un nœud appairé. Leurs URL de plateforme, leur modèle d'installation et leurs capacités supplémentaires diffèrent.

Ces plugins participent à des réunions. Ils sont distincts des canaux de messagerie tels que le [canal Microsoft Teams](/fr/channels/msteams) et du [plugin d'appel vocal](/fr/plugins/voice-call).

## Choisir un plugin

| Plateforme      | Plugin                                      | Liens de réunion acceptés                                                                                   | Installation                             | Chemins de participation                                 | Capacités spécifiques à la plateforme                                                                       |
| --------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Google Meet     | [`google-meet`](/fr/plugins/google-meet)       | `meet.google.com/...`                                                                                       | Installer depuis npm ou ClawHub, puis activer | Chrome local, Chrome sur un nœud appairé, ou numérotation Twilio | Peut créer des réunions via l'API Meet ou un navigateur connecté ; peut lire les artefacts Meet pris en charge avec OAuth |
| Microsoft Teams | [`teams-meetings`](/fr/plugins/teams-meetings) | Liens professionnels sous `teams.microsoft.com/l/meetup-join/...` et liens grand public sous `teams.live.com/meet/...` | Inclus ; l'activer                      | Chrome local ou Chrome sur un nœud appairé                  | Participation en tant qu'invité pour les réunions professionnelles et grand public                                                                     |
| Zoom            | [`zoom-meetings`](/fr/plugins/zoom-meetings)   | `zoom.us/j/...` et sous-domaines de compte tels que `example.zoom.us/j/...`                                      | Inclus ; l'activer                      | Chrome local ou Chrome sur un nœud appairé                  | Participation en tant qu'invité via l'application Web Zoom                                                                           |

Choisissez Google Meet lorsque vous avez besoin de création de réunion, d'artefacts API Google ou d'un chemin téléphonique Twilio. Choisissez Teams ou Zoom pour une participation directe en tant qu'invité du navigateur sur ces plateformes. Les plugins Teams et Zoom ne créent pas de réunions, ne composent pas de numéro, n'appellent pas l'API du fournisseur et n'enregistrent pas les réunions.

## Choisir un mode

Les trois plugins partagent les mêmes modes :

| Mode         | Comportement                                                                                              | Exigences audio                                      |
| ------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `agent`      | La transcription en temps réel va à l'agent OpenClaw configuré ; la synthèse vocale OpenClaw régulière parle la réponse.  | Le retour audio Chrome nécessite le pont BlackHole et SoX. |
| `bidi`       | Un modèle de voix en temps réel écoute et répond directement.                                                  | Le retour audio Chrome nécessite le pont BlackHole et SoX. |
| `transcribe` | Se joint en observation uniquement et expose une transcription de sous-titres en direct limitée lorsque la plateforme fournit des sous-titres. | Aucun pont de retour audio BlackHole ou SoX.                   |

Utilisez `transcribe` lorsque l'agent n'a besoin que du texte de la réunion. Utilisez `agent` pour le raisonnement et les outils OpenClaw normaux. Utilisez `bidi` lorsque la voix directe à faible latence est plus importante que le routage de chaque tour via l'agent régulier.

Les transcriptions de sous-titres sont des données d'exécution limitées à la session, pas des enregistrements de réunion durables. La disponibilité des sous-titres dépend toujours de la plateforme de réunion, du compte, de la langue et de la politique de l'hôte. Consultez le guide de la plateforme pour ses limites de transcription et ses champs de statut.

## Préparer Chrome et l'audio

Chrome peut s'exécuter sur l'hôte Gateway ou sur un nœud appairé. Un nœud Chrome distant doit autoriser `browser.proxy` plus la commande de plateforme :

| Plugin          | Commande de nœud           |
| --------------- | ---------------------- |
| Google Meet     | `googlemeet.chrome`    |
| Microsoft Teams | `teamsmeetings.chrome` |
| Zoom            | `zoommeetings.chrome`  |

Pour le mode `agent` ou `bidi` via Chrome, exécutez Chrome sur macOS et installez les dépendances audio partagées sur le même hôte :

```bash
brew install blackhole-2ch sox
sudo reboot
system_profiler SPAudioDataType | grep -i BlackHole
command -v sox
```

L'hôte Gateway possède toujours l'agent OpenClaw et les identifiants du modèle lorsque Chrome s'exécute sur un nœud appairé. Configurez un fournisseur de transcription en temps réel et OpenClaw TTS pour le mode `agent`, ou un fournisseur de voix en temps réel pour le mode `bidi`. Les guides de plateforme contiennent les options de fournisseur et de commande audio.

## Activer le plugin

Installez Google Meet avant de l'activer. Les réunions Teams et Zoom sont incluses avec OpenClaw et ne nécessitent que d'être activées :

```bash
# Google Meet uniquement
openclaw plugins install npm:@openclaw/google-meet

# Activez uniquement les plugins de réunion que vous utilisez
openclaw plugins enable google-meet
openclaw plugins enable teams-meetings
openclaw plugins enable zoom-meetings
```

Redémarrez la Gateway si votre chemin de gestion des plugins ne la redémarre pas automatiquement. Ensuite, exécutez la vérification de configuration de la plateforme avant de vous joindre.

## Vérifier et se joindre

| Plateforme      | Vérification de configuration                    | Commande de participation                                                                  |
| --------------- | ------------------------------ | ----------------------------------------------------------------------------- |
| Google Meet     | `openclaw googlemeet setup`    | `openclaw googlemeet join 'https://meet.google.com/abc-defg-hij'`             |
| Microsoft Teams | `openclaw teamsmeetings setup` | `openclaw teamsmeetings join 'https://teams.microsoft.com/l/meetup-join/...'` |
| Zoom            | `openclaw zoommeetings setup`  | `openclaw zoommeetings join 'https://zoom.us/j/1234567890'`                   |

Traitez toute vérification de configuration échouée comme un bloqueur pour ce transport et ce mode. Pour un test de fumée en observation uniquement, sélectionnez le mode `transcribe` et confirmez que le rapport de statut indique une session en appel avant de vous attendre à du texte de sous-titres.

## Gérer les invites de politique de plateforme

L'automatisation du navigateur gère les contrôles normaux de nom d'invité, de caméra et de microphone avant la participation, de participation, en appel et de départ. Elle ne contourne pas la politique de la plateforme ou de l'organisateur.

- Google Meet peut nécessiter une connexion Google, une admission de l'hôte ou une décision de permission du navigateur.
- Microsoft Teams peut nécessiter une connexion au locataire, une vérification d'e-mail ou une admission de l'organisateur.
- Zoom peut nécessiter une authentification, une vérification d'e-mail, un code d'accès, la réalisation d'un CAPTCHA ou une admission de l'hôte ; un compte peut également désactiver la participation via le navigateur.

Lorsqu'un résultat de participation ou de statut signale `manualActionRequired`, complétez l'étape signalée dans le même profil Chrome OpenClaw avant de réessayer. L'ouverture répétée de nouveaux onglets ne résout pas un compte, un locataire, un problème de salle d'attente ou une barrière CAPTCHA.

Rejoignez uniquement les réunions où l'opérateur est autorisé à ajouter un agent. Informez les participants lorsque la politique locale ou les règles de consentement exigent la divulgation de la participation automatisée, de la transcription ou de la synthèse vocale.

## Conversation vocale Discord

[Les canaux vocaux Discord](/fr/channels/discord#voice-channels) fournissent une conversation en temps réel native et audio uniquement sans automatisation de réunion de navigateur. OpenClaw peut se joindre à un canal vocal, écouter, router les tours via un agent OpenClaw ou un modèle de voix en temps réel, et parler les réponses. Il n'envoie ni ne reçoit de vidéo de caméra ou de partage d'écran, même lorsque les gens utilisent la vidéo dans le même canal Discord, donc Discord voice est une surface de conversation en direct connexe plutôt qu'un quatrième plugin de réunion de navigateur.

## Guides de plateforme

- [Plugin Google Meet](/fr/plugins/google-meet)
- [Plugin réunions Microsoft Teams](/fr/plugins/teams-meetings)
- [Plugin réunions Zoom](/fr/plugins/zoom-meetings)
- [Gérer les plugins](/fr/plugins/manage-plugins)
- [Contrôle du navigateur](/fr/tools/browser)
