```markdown
---
summary: "Statut du support des bots Zalo, capacités et configuration"
read_when:
  - Working on Zalo features or webhooks
title: "Zalo"
---

# Zalo (Bot API)

Statut : expérimental. Les messages directs sont supportés ; la gestion des groupes est disponible avec des contrôles de politique de groupe explicites.

## Plugin requis

Zalo est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

- Installer via CLI : `openclaw plugins install @openclaw/zalo`
- Ou sélectionner **Zalo** lors de l'intégration et confirmer l'invite d'installation
- Détails : [Plugins](/tools/plugin)

## Configuration rapide (débutant)

1. Installer le plugin Zalo :
   - À partir d'une source locale : `openclaw plugins install ./extensions/zalo`
   - À partir de npm (si publié) : `openclaw plugins install @openclaw/zalo`
   - Ou sélectionner **Zalo** lors de l'intégration et confirmer l'invite d'installation
2. Définir le token :
   - Env : `ZALO_BOT_TOKEN=...`
   - Ou config : `channels.zalo.botToken: "..."`.
3. Redémarrer la passerelle (ou terminer l'intégration).
4. L'accès aux messages directs est l'appairage par défaut ; approuver le code d'appairage au premier contact.

Configuration minimale :

```json5
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

## Qu'est-ce que c'est

Zalo est une application de messagerie centrée sur le Vietnam ; son Bot API permet à la passerelle d'exécuter un bot pour les conversations 1:1.
C'est un bon choix pour le support ou les notifications où vous souhaitez un routage déterministe vers Zalo.

- Un canal Bot API Zalo appartenant à la passerelle.
- Routage déterministe : les réponses reviennent à Zalo ; le modèle ne choisit jamais les canaux.
- Les messages directs partagent la session principale de l'agent.
- Les groupes sont supportés avec des contrôles de politique (`groupPolicy` + `groupAllowFrom`) et par défaut un comportement de liste blanche fermée.

## Configuration (chemin rapide)

### 1) Créer un token de bot (Plateforme Bot Zalo)

1. Aller à [https://bot.zaloplatforms.com](https://bot.zaloplatforms.com) et se connecter.
2. Créer un nouveau bot et configurer ses paramètres.
3. Copier le token du bot (format : `12345689:abc-xyz`).

### 2) Configurer le token (env ou config)

Exemple :

```json5
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

Option env : `ZALO_BOT_TOKEN=...` (fonctionne pour le compte par défaut uniquement).

Support multi-compte : utiliser `channels.zalo.accounts` avec des tokens par compte et un `name` optionnel.

3. Redémarrer la passerelle. Zalo démarre quand un token est résolu (env ou config).
4. L'accès aux messages directs par défaut est l'appairage. Approuver le code quand le bot est contacté pour la première fois.

## Comment ça marche (comportement)

- Les messages entrants sont normalisés dans l'enveloppe de canal partagée avec des espaces réservés pour les médias.
- Les réponses sont toujours routées vers le même chat Zalo.
- Long-polling par défaut ; mode webhook disponible avec `channels.zalo.webhookUrl`.

## Limites

- Le texte sortant est divisé en chunks de 2000 caractères (limite de l'API Zalo).
- Les téléchargements/uploads de médias sont limités par `channels.zalo.mediaMaxMb` (par défaut 5).
- Le streaming est bloqué par défaut en raison de la limite de 2000 caractères qui rend le streaming moins utile.

## Contrôle d'accès (Messages directs)

### Accès aux messages directs

- Par défaut : `channels.zalo.dmPolicy = "pairing"`. Les expéditeurs inconnus reçoivent un code d'appairage ; les messages sont ignorés jusqu'à approbation (les codes expirent après 1 heure).
- Approuver via :
  - `openclaw pairing list zalo`
  - `openclaw pairing approve zalo <CODE>`
- L'appairage est l'échange de token par défaut. Détails : [Pairing](/channels/pairing)
- `channels.zalo.allowFrom` accepte les IDs d'utilisateur numériques (aucune recherche de nom d'utilisateur disponible).

## Contrôle d'accès (Groupes)

- `channels.zalo.groupPolicy` contrôle la gestion des messages entrants de groupe : `open | allowlist | disabled`.
- Le comportement par défaut est fermé : `allowlist`.
- `channels.zalo.groupAllowFrom` restreint les IDs d'expéditeur qui peuvent déclencher le bot dans les groupes.
- Si `groupAllowFrom` n'est pas défini, Zalo revient à `allowFrom` pour les vérifications d'expéditeur.
- `groupPolicy: "disabled"` bloque tous les messages de groupe.
- `groupPolicy: "open"` permet à tout membre du groupe (gated par mention).
- Note d'exécution : si `channels.zalo` est complètement absent, l'exécution revient toujours à `groupPolicy="allowlist"` pour la sécurité.

## Long-polling vs webhook

- Par défaut : long-polling (aucune URL publique requise).
- Mode webhook : définir `channels.zalo.webhookUrl` et `channels.zalo.webhookSecret`.
  - Le secret webhook doit être de 8-256 caractères.
  - L'URL webhook doit utiliser HTTPS.
  - Zalo envoie les événements avec l'en-tête `X-Bot-Api-Secret-Token` pour la vérification.
  - La passerelle HTTP gère les requêtes webhook à `channels.zalo.webhookPath` (par défaut le chemin de l'URL webhook).
  - Les requêtes doivent utiliser `Content-Type: application/json` (ou les types de médias `+json`).
  - Les événements en doublon (`event_name + message_id`) sont ignorés pour une courte fenêtre de relecture.
  - Le trafic en rafales est limité par chemin/source et peut retourner HTTP 429.

**Note :** getUpdates (polling) et webhook s'excluent mutuellement selon la documentation de l'API Zalo.

## Types de messages supportés

- **Messages texte** : Support complet avec chunking de 2000 caractères.
- **Messages image** : Télécharger et traiter les images entrantes ; envoyer des images via `sendPhoto`.
- **Stickers** : Enregistrés mais pas entièrement traités (pas de réponse d'agent).
- **Types non supportés** : Enregistrés (par exemple, messages d'utilisateurs protégés).

## Capacités

| Fonctionnalité      | Statut                                                   |
| ------------------- | -------------------------------------------------------- |
| Messages directs    | ✅ Supporté                                              |
| Groupes             | ⚠️ Supporté avec contrôles de politique (liste blanche par défaut) |
| Médias (images)     | ✅ Supporté                                              |
| Réactions           | ❌ Non supporté                                          |
| Threads             | ❌ Non supporté                                          |
| Sondages            | ❌ Non supporté                                          |
| Commandes natives   | ❌ Non supporté                                          |
| Streaming           | ⚠️ Bloqué (limite de 2000 caractères)                    |

## Cibles de livraison (CLI/cron)

- Utiliser un ID de chat comme cible.
- Exemple : `openclaw message send --channel zalo --target 123456789 --message "hi"`.

## Dépannage

**Le bot ne répond pas :**

- Vérifier que le token est valide : `openclaw channels status --probe`
- Vérifier que l'expéditeur est approuvé (appairage ou allowFrom)
- Vérifier les logs de la passerelle : `openclaw logs --follow`

**Le webhook ne reçoit pas les événements :**

- S'assurer que l'URL webhook utilise HTTPS
- Vérifier que le token secret est de 8-256 caractères
- Confirmer que le point de terminaison HTTP de la passerelle est accessible sur le chemin configuré
- Vérifier que le polling getUpdates n'est pas en cours d'exécution (ils s'excluent mutuellement)

## Référence de configuration (Zalo)

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.zalo.enabled`: activer/désactiver le démarrage du canal.
- `channels.zalo.botToken`: token du bot depuis la plateforme Bot Zalo.
- `channels.zalo.tokenFile`: lire le token depuis un chemin de fichier régulier. Les liens symboliques sont rejetés.
- `channels.zalo.dmPolicy`: `pairing | allowlist | open | disabled` (par défaut : pairing).
- `channels.zalo.allowFrom`: liste blanche des messages directs (IDs d'utilisateur). `open` nécessite `"*"`. L'assistant demandera les IDs numériques.
- `channels.zalo.groupPolicy`: `open | allowlist | disabled` (par défaut : allowlist).
- `channels.zalo.groupAllowFrom`: liste blanche des expéditeurs de groupe (IDs d'utilisateur). Revient à `allowFrom` quand non défini.
- `channels.zalo.mediaMaxMb`: limite des médias entrants/sortants (MB, par défaut 5).
- `channels.zalo.webhookUrl`: activer le mode webhook (HTTPS requis).
- `channels.zalo.webhookSecret`: secret webhook (8-256 caractères).
- `channels.zalo.webhookPath`: chemin webhook sur le serveur HTTP de la passerelle.
- `channels.zalo.proxy`: URL proxy pour les requêtes API.

Options multi-compte :

- `channels.zalo.accounts.<id>.botToken`: token par compte.
- `channels.zalo.accounts.<id>.tokenFile`: fichier token régulier par compte. Les liens symboliques sont rejetés.
- `channels.zalo.accounts.<id>.name`: nom d'affichage.
- `channels.zalo.accounts.<id>.enabled`: activer/désactiver le compte.
- `channels.zalo.accounts.<id>.dmPolicy`: politique des messages directs par compte.
- `channels.zalo.accounts.<id>.allowFrom`: liste blanche par compte.
- `channels.zalo.accounts.<id>.groupPolicy`: politique de groupe par compte.
- `channels.zalo.accounts.<id>.groupAllowFrom`: liste blanche des expéditeurs de groupe par compte.
- `channels.zalo.accounts.<id>.webhookUrl`: URL webhook par compte.
- `channels.zalo.accounts.<id>.webhookSecret`: secret webhook par compte.
- `channels.zalo.accounts.<id>.webhookPath`: chemin webhook par compte.
- `channels.zalo.accounts.<id>.proxy`: URL proxy par compte.
```
