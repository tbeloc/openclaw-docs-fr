---
summary: "Support des comptes personnels Zalo via zca-js natif (connexion QR), capacités et configuration"
read_when:
  - Configuration de Zalo Personal pour OpenClaw
  - Débogage de la connexion Zalo Personal ou du flux de messages
title: "Zalo Personal"
---

# Zalo Personal (non officiel)

Statut : expérimental. Cette intégration automatise un **compte Zalo personnel** via `zca-js` natif à l'intérieur d'OpenClaw.

> **Avertissement :** Ceci est une intégration non officielle et peut entraîner la suspension/interdiction du compte. À utiliser à vos risques et périls.

## Plugin requis

Zalo Personal est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

- Installer via CLI : `openclaw plugins install @openclaw/zalouser`
- Ou à partir d'une extraction source : `openclaw plugins install ./extensions/zalouser`
- Détails : [Plugins](/fr/tools/plugin)

Aucun binaire CLI `zca`/`openzca` externe n'est requis.

## Configuration rapide (débutant)

1. Installez le plugin (voir ci-dessus).
2. Connectez-vous (QR, sur la machine Gateway) :
   - `openclaw channels login --channel zalouser`
   - Scannez le code QR avec l'application mobile Zalo.
3. Activez le canal :

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

4. Redémarrez la Gateway (ou terminez l'intégration).
5. L'accès aux DM par défaut est l'appairage ; approuvez le code d'appairage au premier contact.

## Ce que c'est

- S'exécute entièrement en processus via `zca-js`.
- Utilise des écouteurs d'événements natifs pour recevoir les messages entrants.
- Envoie les réponses directement via l'API JS (texte/média/lien).
- Conçu pour les cas d'usage de « compte personnel » où l'API Zalo Bot n'est pas disponible.

## Nommage

L'ID du canal est `zalouser` pour clarifier que ceci automatise un **compte utilisateur Zalo personnel** (non officiel). Nous réservons `zalo` pour une intégration potentielle future avec l'API Zalo officielle.

## Recherche d'IDs (répertoire)

Utilisez le CLI du répertoire pour découvrir les pairs/groupes et leurs IDs :

```bash
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

## Limites

- Le texte sortant est divisé en ~2000 caractères (limites du client Zalo).
- La diffusion en continu est bloquée par défaut.

## Contrôle d'accès (DMs)

`channels.zalouser.dmPolicy` supporte : `pairing | allowlist | open | disabled` (par défaut : `pairing`).

`channels.zalouser.allowFrom` accepte les IDs ou noms d'utilisateurs. Lors de l'intégration, les noms sont résolus en IDs à l'aide de la recherche de contacts en processus du plugin.

Approuvez via :

- `openclaw pairing list zalouser`
- `openclaw pairing approve zalouser <code>`

## Accès aux groupes (optionnel)

- Par défaut : `channels.zalouser.groupPolicy = "open"` (groupes autorisés). Utilisez `channels.defaults.groupPolicy` pour remplacer la valeur par défaut si elle n'est pas définie.
- Restreindre à une liste blanche avec :
  - `channels.zalouser.groupPolicy = "allowlist"`
  - `channels.zalouser.groups` (les clés doivent être des IDs de groupe stables ; les noms sont résolus en IDs au démarrage si possible)
  - `channels.zalouser.groupAllowFrom` (contrôle quels expéditeurs dans les groupes autorisés peuvent déclencher le bot)
- Bloquer tous les groupes : `channels.zalouser.groupPolicy = "disabled"`.
- L'assistant de configuration peut demander des listes blanches de groupes.
- Au démarrage, OpenClaw résout les noms de groupe/utilisateur dans les listes blanches en IDs et enregistre le mappage.
- La correspondance de la liste blanche de groupes est basée sur l'ID uniquement par défaut. Les noms non résolus sont ignorés pour l'authentification sauf si `channels.zalouser.dangerouslyAllowNameMatching: true` est activé.
- `channels.zalouser.dangerouslyAllowNameMatching: true` est un mode de compatibilité de secours qui réactive la correspondance de noms de groupe mutables.
- Si `groupAllowFrom` n'est pas défini, l'exécution revient à `allowFrom` pour les vérifications d'expéditeur de groupe.
- Les vérifications d'expéditeur s'appliquent aux messages de groupe normaux et aux commandes de contrôle (par exemple `/new`, `/reset`).

Exemple :

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["1471383327500481391"],
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

### Gating de mention de groupe

- `channels.zalouser.groups.<group>.requireMention` contrôle si les réponses de groupe nécessitent une mention.
- Ordre de résolution : ID/nom de groupe exact -> slug de groupe normalisé -> `*` -> par défaut (`true`).
- Ceci s'applique à la fois aux groupes de liste blanche et au mode groupe ouvert.
- Les commandes de contrôle autorisées (par exemple `/new`) peuvent contourner le gating de mention.
- Lorsqu'un message de groupe est ignoré parce qu'une mention est requise, OpenClaw le stocke comme historique de groupe en attente et l'inclut au prochain message de groupe traité.
- La limite d'historique de groupe par défaut est `messages.groupChat.historyLimit` (secours `50`). Vous pouvez remplacer par compte avec `channels.zalouser.historyLimit`.

Exemple :

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "*": { allow: true, requireMention: true },
        "Work Chat": { allow: true, requireMention: false },
      },
    },
  },
}
```

## Multi-compte

Les comptes correspondent à des profils `zalouser` dans l'état d'OpenClaw. Exemple :

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      defaultAccount: "default",
      accounts: {
        work: { enabled: true, profile: "work" },
      },
    },
  },
}
```

## Saisie, réactions et accusés de réception de livraison

- OpenClaw envoie un événement de saisie avant de dispatcher une réponse (meilleur effort).
- L'action de réaction de message `react` est supportée pour `zalouser` dans les actions de canal.
  - Utilisez `remove: true` pour supprimer un emoji de réaction spécifique d'un message.
  - Sémantique des réactions : [Réactions](/fr/tools/reactions)
- Pour les messages entrants qui incluent les métadonnées d'événement, OpenClaw envoie les accusés de réception livrés + vus (meilleur effort).

## Dépannage

**La connexion ne persiste pas :**

- `openclaw channels status --probe`
- Se reconnecter : `openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`

**Le nom de la liste blanche/groupe n'a pas été résolu :**

- Utilisez des IDs numériques dans `allowFrom`/`groupAllowFrom`/`groups`, ou des noms d'ami/groupe exacts.

**Mise à niveau à partir de l'ancienne configuration basée sur CLI :**

- Supprimez toute hypothèse de processus `zca` externe ancien.
- Le canal s'exécute maintenant entièrement dans OpenClaw sans binaires CLI externes.
