```markdown
---
read_when:
  - 开发 Zalo 功能或 webhooks
summary: Zalo bot 支持状态、功能和配置
title: Zalo
x-i18n:
  generated_at: "2026-02-03T07:44:44Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0311d932349f96412b712970b5d37329b91929bf3020536edf3ca0ff464373c0
  source_path: channels/zalo.md
  workflow: 15
---

# Zalo (Bot API)

Statut : Expérimental. Seuls les messages privés sont pris en charge ; les groupes seront bientôt disponibles selon la documentation Zalo.

## Plugin requis

Zalo est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

- Installation via CLI : `openclaw plugins install @openclaw/zalo`
- Ou sélectionnez **Zalo** lors de l'assistant de configuration et confirmez l'invite d'installation
- Détails : [Plugins](/tools/plugin)

## Configuration rapide (débutants)

1. Installez le plugin Zalo :
   - Extraction depuis la source : `openclaw plugins install ./extensions/zalo`
   - Depuis npm (si publié) : `openclaw plugins install @openclaw/zalo`
   - Ou sélectionnez **Zalo** lors de l'assistant et confirmez l'invite d'installation
2. Configurez le token :
   - Variable d'environnement : `ZALO_BOT_TOKEN=...`
   - Ou configuration : `channels.zalo.botToken: "..."`
3. Redémarrez la passerelle (ou terminez l'assistant).
4. L'accès aux messages privés est par défaut en mode d'appairage ; approuvez le code d'appairage lors du premier contact.

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

Zalo est une application de messagerie instantanée axée sur le marché vietnamien ; son Bot API permet à la passerelle d'exécuter un bot pour les conversations en tête-à-tête.
C'est idéal pour les scénarios de support ou de notification qui nécessitent un routage déterministe vers Zalo.

- Canal Zalo Bot API détenu par la passerelle.
- Routage déterministe : les réponses reviennent à Zalo ; le modèle ne choisit pas le canal.
- Les messages privés partagent la session principale de l'agent.
- Les groupes ne sont pas encore pris en charge (la documentation Zalo indique « à venir »).

## Configuration (chemin rapide)

### 1) Créer un token bot (plateforme Zalo Bot)

1. Allez à **https://bot.zaloplatforms.com** et connectez-vous.
2. Créez un nouveau bot et configurez ses paramètres.
3. Copiez le token bot (format : `12345689:abc-xyz`).

### 2) Configurer le token (variable d'environnement ou configuration)

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

Option variable d'environnement : `ZALO_BOT_TOKEN=...` (compte par défaut uniquement).

Support multi-comptes : utilisez la configuration `channels.zalo.accounts` pour les tokens par compte et le `name` optionnel.

3. Redémarrez la passerelle. Zalo démarre lorsque le token est analysé (variable d'environnement ou configuration).
4. L'accès aux messages privés est par défaut en mode d'appairage. Approuvez le code d'appairage lorsque le bot est contacté pour la première fois.

## Fonctionnement (comportement)

- Les messages entrants sont normalisés en enveloppes de canal partagées avec des espaces réservés pour les médias.
- Les réponses sont toujours routées vers le même chat Zalo.
- Utilise par défaut le long polling ; le mode webhook peut être activé via `channels.zalo.webhookUrl`.

## Limitations

- Le texte sortant est divisé en chunks de 2000 caractères (limite de l'API Zalo).
- Le téléchargement/chargement de médias est limité par `channels.zalo.mediaMaxMb` (par défaut 5).
- La diffusion en continu fonctionne mal en raison de la limite de 2000 caractères et est bloquée par défaut.

## Contrôle d'accès (messages privés)

### Accès aux messages privés

- Par défaut : `channels.zalo.dmPolicy = "pairing"`. Les expéditeurs inconnus reçoivent un code d'appairage ; les messages sont ignorés jusqu'à approbation (le code d'appairage expire après 1 heure).
- Approuvez via :
  - `openclaw pairing list zalo`
  - `openclaw pairing approve zalo <CODE>`
- L'appairage est le mécanisme d'échange de tokens par défaut. Détails : [Appairage](/channels/pairing)
- `channels.zalo.allowFrom` accepte les ID d'utilisateur numériques (pas de recherche de nom d'utilisateur).

## Long polling vs webhook

- Par défaut : long polling (pas d'URL publique requise).
- Mode webhook : définissez `channels.zalo.webhookUrl` et `channels.zalo.webhookSecret`.
  - Le secret webhook doit être de 8 à 256 caractères.
  - L'URL webhook doit utiliser HTTPS.
  - Zalo envoie les événements avec l'en-tête `X-Bot-Api-Secret-Token` pour la vérification.
  - La passerelle HTTP traite les requêtes webhook à `channels.zalo.webhookPath` (par défaut le chemin de l'URL webhook).

**Remarque :** Selon la documentation de l'API Zalo, getUpdates (polling) et webhook s'excluent mutuellement.

## Types de messages pris en charge

- **Messages texte** : entièrement pris en charge, divisés en chunks de 2000 caractères.
- **Messages image** : téléchargement et traitement des images entrantes ; envoi d'images via `sendPhoto`.
- **Autocollants** : documentés mais non entièrement traités (pas de réponse d'agent).
- **Types non pris en charge** : documentés (par exemple, messages d'utilisateurs protégés).

## Fonctionnalités

| Fonctionnalité      | Statut                              |
| ------------------- | ----------------------------------- |
| Messages privés     | ✅ Pris en charge                   |
| Groupes             | ❌ À venir (selon la documentation Zalo) |
| Médias (images)     | ✅ Pris en charge                   |
| Réactions emoji     | ❌ Non pris en charge               |
| Thèmes              | ❌ Non pris en charge               |
| Sondages            | ❌ Non pris en charge               |
| Commandes natives   | ❌ Non pris en charge               |
| Diffusion en continu | ⚠️ Bloquée (limite de 2000 caractères) |

## Cibles de livraison (CLI/cron)

- Utilisez l'ID de chat comme cible.
- Exemple : `openclaw message send --channel zalo --target 123456789 --message "hi"`.

## Dépannage

**Le bot ne répond pas :**

- Vérifiez que le token est valide : `openclaw channels status --probe`
- Vérifiez que l'expéditeur a été approuvé (appairage ou allowFrom)
- Vérifiez les journaux de la passerelle : `openclaw logs --follow`

**Le webhook ne reçoit pas d'événements :**

- Assurez-vous que l'URL webhook utilise HTTPS
- Vérifiez que le token secret est de 8 à 256 caractères
- Confirmez que le point de terminaison HTTP de la passerelle est accessible au chemin configuré
- Vérifiez que le polling getUpdates n'est pas en cours d'exécution (ils s'excluent mutuellement)

## Référence de configuration (Zalo)

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.zalo.enabled` : activer/désactiver le démarrage du canal.
- `channels.zalo.botToken` : token bot de la plateforme Zalo Bot.
- `channels.zalo.tokenFile` : lire le token depuis un chemin de fichier.
- `channels.zalo.dmPolicy` : `pairing | allowlist | open | disabled` (par défaut : pairing).
- `channels.zalo.allowFrom` : liste d'autorisation des messages privés (ID d'utilisateur). `open` nécessite `"*"`. L'assistant demande les ID numériques.
- `channels.zalo.mediaMaxMb` : limite de médias entrants/sortants (Mo, par défaut 5).
- `channels.zalo.webhookUrl` : activer le mode webhook (HTTPS requis).
- `channels.zalo.webhookSecret` : secret webhook (8-256 caractères).
- `channels.zalo.webhookPath` : chemin webhook sur le serveur HTTP de la passerelle.
- `channels.zalo.proxy` : URL proxy pour les requêtes API.

Options multi-comptes :

- `channels.zalo.accounts.<id>.botToken` : token par compte.
- `channels.zalo.accounts.<id>.tokenFile` : fichier token par compte.
- `channels.zalo.accounts.<id>.name` : nom d'affichage.
- `channels.zalo.accounts.<id>.enabled` : activer/désactiver le compte.
- `channels.zalo.accounts.<id>.dmPolicy` : politique de messages privés par compte.
- `channels.zalo.accounts.<id>.allowFrom` : liste d'autorisation par compte.
- `channels.zalo.accounts.<id>.webhookUrl` : URL webhook par compte.
- `channels.zalo.accounts.<id>.webhookSecret` : secret webhook par compte.
- `channels.zalo.accounts.<id>.webhookPath` : chemin webhook par compte.
- `channels.zalo.accounts.<id>.proxy` : URL proxy par compte.
```
