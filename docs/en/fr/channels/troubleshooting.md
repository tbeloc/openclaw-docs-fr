```markdown
---
summary: "Dépannage rapide au niveau du canal avec signatures de défaillance par canal et correctifs"
read_when:
  - Channel transport says connected but replies fail
  - You need channel specific checks before deep provider docs
title: "Dépannage des canaux"
---

# Dépannage des canaux

Utilisez cette page lorsqu'un canal se connecte mais que le comportement est incorrect.

## Échelle de commandes

Exécutez-les dans cet ordre d'abord :

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Ligne de base saine :

- `Runtime: running`
- `RPC probe: ok`
- La sonde de canal affiche connecté/prêt

## WhatsApp

### Signatures de défaillance WhatsApp

| Symptôme                         | Vérification la plus rapide                         | Correctif                                                     |
| ------------------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| Connecté mais pas de réponses MP     | `openclaw pairing list whatsapp`                    | Approuvez l'expéditeur ou changez la politique MP/liste blanche.           |
| Messages de groupe ignorés          | Vérifiez `requireMention` + modèles de mention dans la config | Mentionnez le bot ou assouplissez la politique de mention pour ce groupe. |
| Déconnexion aléatoire/boucles de reconnexion | `openclaw channels status --probe` + logs           | Reconnectez-vous et vérifiez que le répertoire des identifiants est sain.   |

Dépannage complet : [/channels/whatsapp#troubleshooting-quick](/channels/whatsapp#troubleshooting-quick)

## Telegram

### Signatures de défaillance Telegram

| Symptôme                             | Vérification la plus rapide                                   | Correctif                                                                         |
| ----------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------- |
| `/start` mais pas de flux de réponse utilisable   | `openclaw pairing list telegram`                | Approuvez l'appairage ou changez la politique MP.                        |
| Bot en ligne mais le groupe reste silencieux   | Vérifiez l'exigence de mention et le mode confidentialité du bot | Désactivez le mode confidentialité pour la visibilité du groupe ou mentionnez le bot.                   |
| Échecs d'envoi avec erreurs réseau   | Inspectez les logs pour les échecs d'appels API Telegram     | Corrigez le routage DNS/IPv6/proxy vers `api.telegram.org`.                           |
| `setMyCommands` rejeté au démarrage | Inspectez les logs pour `BOT_COMMANDS_TOO_MUCH`        | Réduisez les commandes Telegram des plugins/compétences/personnalisées ou désactivez les menus natifs.       |
| Mise à niveau et liste blanche vous bloque   | `openclaw security audit` et listes blanches de config | Exécutez `openclaw doctor --fix` ou remplacez `@username` par des ID d'expéditeur numériques. |

Dépannage complet : [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting)

## Discord

### Signatures de défaillance Discord

| Symptôme                         | Vérification la plus rapide                       | Correctif                                                       |
| ------------------------------- | ----------------------------------- | --------------------------------------------------------- |
| Bot en ligne mais pas de réponses de guilde | `openclaw channels status --probe`  | Autorisez la guilde/le canal et vérifiez l'intention de contenu du message.    |
| Messages de groupe ignorés          | Vérifiez les logs pour les rejets de gating de mention | Mentionnez le bot ou définissez `requireMention: false` pour la guilde/le canal. |
| Réponses MP manquantes              | `openclaw pairing list discord`     | Approuvez l'appairage MP ou ajustez la politique MP.                   |

Dépannage complet : [/channels/discord#troubleshooting](/channels/discord#troubleshooting)

## Slack

### Signatures de défaillance Slack

| Symptôme                                | Vérification la plus rapide                             | Correctif                                               |
| -------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| Mode socket connecté mais pas de réponses | `openclaw channels status --probe`        | Vérifiez le jeton d'application + jeton de bot et les portées requises. |
| MPs bloqués                            | `openclaw pairing list slack`             | Approuvez l'appairage ou assouplissez la politique MP.               |
| Message de canal ignoré                | Vérifiez `groupPolicy` et la liste blanche du canal | Autorisez le canal ou changez la politique en `open`.     |

Dépannage complet : [/channels/slack#troubleshooting](/channels/slack#troubleshooting)

## iMessage et BlueBubbles

### Signatures de défaillance iMessage et BlueBubbles

| Symptôme                          | Vérification la plus rapide                                                           | Correctif                                                   |
| -------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| Pas d'événements entrants                | Vérifiez l'accessibilité du webhook/serveur et les permissions d'application                  | Corrigez l'URL du webhook ou l'état du serveur BlueBubbles.          |
| Peut envoyer mais pas de réception sur macOS | Vérifiez les permissions de confidentialité macOS pour l'automatisation Messages                 | Réaccordez les permissions TCC et redémarrez le processus du canal. |
| Expéditeur MP bloqué                | `openclaw pairing list imessage` ou `openclaw pairing list bluebubbles` | Approuvez l'appairage ou mettez à jour la liste blanche.                  |

Dépannage complet :

- [/channels/imessage#troubleshooting-macos-privacy-and-security-tcc](/channels/imessage#troubleshooting-macos-privacy-and-security-tcc)
- [/channels/bluebubbles#troubleshooting](/channels/bluebubbles#troubleshooting)

## Signal

### Signatures de défaillance Signal

| Symptôme                         | Vérification la plus rapide                              | Correctif                                                      |
| ------------------------------- | ------------------------------------------ | -------------------------------------------------------- |
| Démon accessible mais bot silencieux | `openclaw channels status --probe`         | Vérifiez l'URL du démon `signal-cli`/le compte et le mode de réception. |
| MP bloqué                      | `openclaw pairing list signal`             | Approuvez l'expéditeur ou ajustez la politique MP.                      |
| Les réponses de groupe ne se déclenchent pas    | Vérifiez la liste blanche du groupe et les modèles de mention | Ajoutez l'expéditeur/le groupe ou assouplissez le gating.                       |

Dépannage complet : [/channels/signal#troubleshooting](/channels/signal#troubleshooting)

## Matrix

### Signatures de défaillance Matrix

| Symptôme                             | Vérification la plus rapide                                | Correctif                                             |
| ----------------------------------- | -------------------------------------------- | ----------------------------------------------- |
| Connecté mais ignore les messages de salle | `openclaw channels status --probe`           | Vérifiez `groupPolicy` et la liste blanche de salle.         |
| Les MPs ne sont pas traités                  | `openclaw pairing list matrix`               | Approuvez l'expéditeur ou ajustez la politique MP.             |
| Les salles chiffrées échouent                | Vérifiez le module crypto et les paramètres de chiffrement | Activez le support du chiffrement et rejoignez/synchronisez la salle. |

Dépannage complet : [/channels/matrix#troubleshooting](/channels/matrix#troubleshooting)
```
