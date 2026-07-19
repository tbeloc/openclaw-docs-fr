---
summary: "Plugin Zoom meetings : rejoindre des réunions en tant qu'invité du navigateur Chrome"
read_when:
  - You want an OpenClaw agent to join a Zoom meeting
  - You are configuring Chrome, BlackHole, or SoX for Zoom meeting talk-back
title: "Plugin Zoom meetings"
---

Le plugin `zoom-meetings` rejoint les liens de réunion Zoom en tant qu'invité via l'application Web Zoom dans le profil Chrome OpenClaw. Il accepte les liens de réunion sous `zoom.us/j/...` et les sous-domaines de compte tels que `example.zoom.us/j/...`. Il ne crée pas de réunions, ne compose pas de numéro, n'utilise pas le SDK Zoom Meeting et n'enregistre pas les réunions.

## Configuration

La fonction de rétroaction utilise les mêmes prérequis audio locaux que le [plugin Google Meet](/fr/plugins/google-meet) : macOS, le périphérique audio virtuel `BlackHole 2ch` et SoX.

```bash
brew install blackhole-2ch sox
sudo reboot
system_profiler SPAudioDataType | grep -i BlackHole
command -v sox
```

Activez le plugin, puis vérifiez la configuration :

```json5
{
  plugins: {
    entries: {
      "zoom-meetings": {
        enabled: true,
        config: {
          defaultMode: "agent",
          chrome: { guestName: "OpenClaw Agent" },
        },
      },
    },
  },
}
```

```bash
openclaw zoommeetings setup
openclaw zoommeetings join 'https://zoom.us/j/1234567890'
```

Utilisez `chromeNode.node` pour exécuter Chrome, BlackHole et SoX sur un nœud macOS appairé. Le nœud doit autoriser `zoommeetings.chrome` et `browser.proxy`.

## Modes

| Mode         | Comportement                                                                    |
| ------------ | --------------------------------------------------------------------------- |
| `agent`      | La transcription en temps réel consulte l'agent OpenClaw configuré ; les réponses TTS. |
| `bidi`       | Un modèle vocal en temps réel écoute et répond directement.                       |
| `transcribe` | Rejoindre en observation uniquement avec des instantanés de transcription de sous-titres en direct.                   |

Le mode Transcribe active les sous-titres en direct Zoom après l'admission et capture l'affichage des sous-titres délimité. L'action `transcript` retourne le tampon de sous-titres pour la session de réunion OpenClaw active.

## Limites de participation des invités

L'adaptateur de navigateur choisit **Rejoindre depuis le navigateur**, remplit le nom de l'invité, désactive la caméra, configure le microphone pour le mode sélectionné et clique sur **Rejoindre**. L'application Web Zoom s'exécute sous `app.zoom.us` ; le plugin accorde à cette origine les autorisations de microphone et de sélection de haut-parleur avant la navigation. L'état en appel utilise le contrôle Quitter de Zoom. Les états du hall d'attente, de connexion, de code d'accès, de CAPTCHA et d'autorisation d'appareil retournent des raisons d'action manuelle explicites.

La politique de l'hôte Zoom et du compte peut désactiver la participation via navigateur, exiger une authentification ou une vérification par e-mail, afficher un CAPTCHA ou exiger l'admission de l'hôte. Complétez cette étape dans le profil Chrome OpenClaw, puis réessayez le statut ou la parole. Le plugin ne contourne pas la politique Zoom.

L'application Web Zoom a été validée en direct avec une réunion de test officielle Zoom pour l'interstitiel de l'application, l'entrée du nom d'invité iframe, les contrôles de microphone et de caméra avant la réunion, la participation, les autorisations multimédias du navigateur et de macOS, la détection en appel, l'activation des sous-titres en direct et la détection de fin d'hôte. Les états du hall d'attente et d'authentification dépendent de la politique de l'hôte et conservent des solutions de secours textuelles lorsqu'aucun identifiant DOM stable n'est disponible.

## Surface d'outil et de passerelle

L'outil d'agent `zoom_meetings` supporte `join`, `leave`, `status`, `transcript` et `speak`. Les méthodes de passerelle utilisent le préfixe `zoommeetings.*`. La commande de nœud est `zoommeetings.chrome`.

## Connexes

- [Aperçu des plugins de réunion](/fr/plugins/meeting-plugins)
