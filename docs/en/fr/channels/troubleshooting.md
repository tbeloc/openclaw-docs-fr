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
| ------------------------------- | --------------------------------------------------- | ------------------------------------------------------------- |
| Connecté mais pas de réponses MP     | `openclaw pairing list whatsapp`                    | Approuver l'expéditeur ou changer la politique MP/liste blanche.           |
| Messages de groupe ignorés          | Vérifier `requireMention` + motifs de mention dans la config | Mentionner le bot ou assouplir la politique de mention pour ce groupe. |
| Déconnexions aléatoires/boucles de reconnexion | `openclaw channels status --probe` + logs           | Se reconnecter et vérifier que le répertoire des identifiants est sain.   |

Dépannage complet : [/channels/whatsapp#troubleshooting-quick](/fr/channels/whatsapp#troubleshooting-quick)

## Telegram

### Signatures de défaillance Telegram

| Symptôme                             | Vérification la plus rapide                                   | Correctif                                                                         |
| ----------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------- |
| `/start` mais pas de flux de réponse utilisable   | `openclaw pairing list telegram`                | Approuver l'appairage ou changer la politique MP.                        |
| Bot en ligne mais groupe silencieux   | Vérifier l'exigence de mention et le mode confidentialité du bot | Désactiver le mode confidentialité pour la visibilité du groupe ou mentionner le bot.                   |
| Échecs d'envoi avec erreurs réseau   | Inspecter les logs pour les échecs d'appels API Telegram     | Corriger le routage DNS/IPv6/proxy vers `api.telegram.org`.                           |
| `setMyCommands` rejeté au démarrage | Inspecter les logs pour `BOT_COMMANDS_TOO_MUCH`        | Réduire les commandes Telegram des plugins/compétences/personnalisées ou désactiver les menus natifs.       |
| Mise à niveau et liste blanche vous bloque   | `openclaw security audit` et listes blanches de config | Exécuter `openclaw doctor --fix` ou remplacer `@username` par des ID d'expéditeur numériques. |

Dépannage complet : [/channels/telegram#troubleshooting](/fr/channels/telegram#troubleshooting)

## Discord

### Signatures de défaillance Discord

| Symptôme                         | Vérification la plus rapide                       | Correctif                                                       |
| ------------------------------- | ----------------------------------- | --------------------------------------------------------- |
| Bot en ligne mais pas de réponses de guilde | `openclaw channels status --probe`  | Autoriser la guilde/le canal et vérifier l'intention du contenu du message.    |
| Messages de groupe ignorés          | Vérifier les logs pour les rejets de mention gating | Mentionner le bot ou définir `requireMention: false` pour la guilde/le canal. |
| Réponses MP manquantes              | `openclaw pairing list discord`     | Approuver l'appairage MP ou ajuster la politique MP.                   |

Dépannage complet : [/channels/discord#troubleshooting](/fr/channels/discord#troubleshooting)

## Slack

### Signatures de défaillance Slack

| Symptôme                                | Vérification la plus rapide                             | Correctif                                               |
| -------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| Mode socket connecté mais pas de réponses | `openclaw channels status --probe`        | Vérifier le jeton d'application + jeton de bot et les portées requises. |
| MPs bloqués                            | `openclaw pairing list slack`             | Approuver l'appairage ou assouplir la politique MP.               |
| Message de canal ignoré                | Vérifier `groupPolicy` et liste blanche de canal | Autoriser le canal ou changer la politique en `open`.     |

Dépannage complet : [/channels/slack#troubleshooting](/fr/channels/slack#troubleshooting)

## iMessage et BlueBubbles

### Signatures de défaillance iMessage et BlueBubbles

| Symptôme                          | Vérification la plus rapide                                                           | Correctif                                                   |
| -------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| Pas d'événements entrants                | Vérifier l'accessibilité du webhook/serveur et les permissions d'application                  | Corriger l'URL du webhook ou l'état du serveur BlueBubbles.          |
| Peut envoyer mais pas de réception sur macOS | Vérifier les permissions de confidentialité macOS pour l'automatisation Messages                 | Réaccorder les permissions TCC et redémarrer le processus de canal. |
| Expéditeur MP bloqué                | `openclaw pairing list imessage` ou `openclaw pairing list bluebubbles` | Approuver l'appairage ou mettre à jour la liste blanche.                  |

Dépannage complet :

- [/channels/imessage#troubleshooting-macos-privacy-and-security-tcc](/fr/channels/imessage#troubleshooting-macos-privacy-and-security-tcc)
- [/channels/bluebubbles#troubleshooting](/fr/channels/bluebubbles#troubleshooting)

## Signal

### Signatures de défaillance Signal

| Symptôme                         | Vérification la plus rapide                              | Correctif                                                      |
| ------------------------------- | ------------------------------------------ | -------------------------------------------------------- |
| Daemon accessible mais bot silencieux | `openclaw channels status --probe`         | Vérifier l'URL du daemon `signal-cli`/compte et le mode de réception. |
| MP bloqué                      | `openclaw pairing list signal`             | Approuver l'expéditeur ou ajuster la politique MP.                      |
| Les réponses de groupe ne se déclenchent pas    | Vérifier la liste blanche de groupe et les motifs de mention | Ajouter l'expéditeur/groupe ou assouplir le gating.                       |

Dépannage complet : [/channels/signal#troubleshooting](/fr/channels/signal#troubleshooting)

## Matrix

### Signatures de défaillance Matrix

| Symptôme                             | Vérification la plus rapide                                | Correctif                                             |
| ----------------------------------- | -------------------------------------------- | ----------------------------------------------- |
| Connecté mais ignore les messages de salle | `openclaw channels status --probe`           | Vérifier `groupPolicy` et liste blanche de salle.         |
| Les MPs ne sont pas traités                  | `openclaw pairing list matrix`               | Approuver l'expéditeur ou ajuster la politique MP.             |
| Les salles chiffrées échouent                | Vérifier le module crypto et les paramètres de chiffrement | Activer le support du chiffrement et rejoindre/synchroniser la salle. |

Dépannage complet : [/channels/matrix#troubleshooting](/fr/channels/matrix#troubleshooting)
