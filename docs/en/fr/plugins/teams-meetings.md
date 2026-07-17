---
summary: "Plugin réunions Microsoft Teams : rejoindre des réunions professionnelles ou grand public en tant qu'invité navigateur Chrome"
read_when:
  - You want an OpenClaw agent to join a Microsoft Teams meeting
  - You are configuring Chrome, BlackHole, or SoX for Teams meeting talk-back
title: "Plugin réunions Microsoft Teams"
---

Le plugin `teams-meetings` rejoint les liens Microsoft Teams en tant qu'invité dans le profil Chrome OpenClaw. Il accepte les liens professionnels sous `teams.microsoft.com/l/meetup-join/...` et les liens grand public sous `teams.live.com/meet/...`. Il ne crée pas de réunions, ne compose pas de numéro, n'appelle pas Microsoft Graph et n'enregistre pas les réunions.

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
      "teams-meetings": {
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
openclaw teamsmeetings setup
openclaw teamsmeetings join 'https://teams.microsoft.com/l/meetup-join/...'
```

Utilisez `chromeNode.node` pour exécuter Chrome, BlackHole et SoX sur un nœud macOS appairé. Le nœud doit autoriser `teamsmeetings.chrome` et `browser.proxy`.

## Modes

| Mode         | Comportement                                                                    |
| ------------ | --------------------------------------------------------------------------- |
| `agent`      | La transcription en temps réel consulte l'agent OpenClaw configuré ; les réponses TTS. |
| `bidi`       | Un modèle vocal en temps réel écoute et répond directement.                       |
| `transcribe` | Rejoindre en observation uniquement. Les instantanés de sous-titres sont actuellement vides.                      |

Le scraping des sous-titres est désactivé par défaut. Les sélecteurs DOM des sous-titres en direct de Teams doivent être validés sur les locataires professionnels et grand public en direct avant que le plugin puisse promettre la capture de transcription.

## Limites de jointure en tant qu'invité

L'adaptateur de navigateur rejette l'interstitiel d'application, remplit le nom d'invité, éteint la caméra, configure le microphone pour le mode sélectionné et clique sur le bouton de jointure. L'état en appel utilise le contrôle de raccrochage ; les états de salle d'attente, de connexion au locataire et de permission d'appareil retournent des raisons d'action manuelle explicites.

La politique du locataire Teams peut exiger une connexion, une vérification d'e-mail ou l'admission de l'organisateur. Complétez cette étape dans le profil Chrome OpenClaw, puis réessayez le statut ou la parole. Le plugin ne contourne pas la politique du locataire.

Tous les sélecteurs dans la page sont au mieux des efforts en attente de validation en direct. Les modifications de l'interface utilisateur de Teams professionnelle et grand public peuvent nécessiter des mises à jour de sélecteur. Validez ces flux avant utilisation sans surveillance : interstitiel d'application, entrée de nom d'invité, bascules de microphone/caméra de préjointure, jointure, admission en salle d'attente, connexion au locataire/vérification d'e-mail, permissions multimédias, détection en appel, routage de sortie BlackHole, confirmation de départ et comportement de réunion grand public.

## Surface d'outil et de passerelle

L'outil d'agent `teams_meetings` supporte `join`, `leave`, `status`, `transcript` et `speak`. Les méthodes de passerelle utilisent le préfixe `teamsmeetings.*`. La commande de nœud est `teamsmeetings.chrome`.
