---
read_when:
  - 为 OpenClaw 设置 Zalo Personal
  - 调试 Zalo Personal 登录或消息流程
summary: 通过 zca-cli（QR 登录）支持 Zalo 个人账户、功能和配置
title: Zalo Personal
x-i18n:
  generated_at: "2026-02-03T07:44:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2a249728d556e5cc52274627bdaf390fa10e815afa04f4497feb57a2a0cb9261
  source_path: channels/zalouser.md
  workflow: 15
---

# Zalo Personnel (non officiel)

Statut : Expérimental. Cette intégration automatise les **comptes Zalo personnels** via `zca-cli`.

> **Avertissement :** Il s'agit d'une intégration non officielle qui peut entraîner la suspension/fermeture de votre compte. Utilisation à vos risques et périls.

## Plugin requis

Zalo Personnel est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

- Installation via CLI : `openclaw plugins install @openclaw/zalouser`
- Ou installation depuis la source : `openclaw plugins install ./extensions/zalouser`
- Détails : [Plugins](/tools/plugin)

## Prérequis : zca-cli

Le serveur Gateway doit avoir le binaire `zca` disponible dans `PATH`.

- Vérification : `zca --version`
- S'il est manquant, installez zca-cli (voir `extensions/zalouser/README.md` ou la documentation en amont de zca-cli).

## Configuration rapide (débutants)

1. Installez le plugin (voir ci-dessus).
2. Connectez-vous (QR, sur la machine Gateway) :
   - `openclaw channels login --channel zalouser`
   - Scannez le code QR dans le terminal avec votre application mobile Zalo.
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

4. Redémarrez Gateway (ou terminez l'assistant de configuration).
5. L'accès aux messages privés est par défaut en mode appairage ; approuvez le code d'appairage au premier contact.

## Qu'est-ce que c'est

- Utilise `zca listen` pour recevoir les messages entrants.
- Utilise `zca msg ...` pour envoyer des réponses (texte/média/liens).
- Conçu pour les scénarios d'utilisation de "compte personnel", utile quand l'API Zalo Bot n'est pas disponible.

## Nommage

L'ID du canal est `zalouser` pour clarifier qu'il s'agit d'automatiser un **compte utilisateur Zalo personnel** (non officiel). Nous réservons `zalo` pour une possible intégration officielle future avec l'API Zalo.

## Trouver des ID (répertoire)

Utilisez la CLI du répertoire pour découvrir les contacts/groupes et leurs ID :

```bash
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

## Limitations

- Les textes sortants sont fragmentés à environ 2000 caractères (limitation du client Zalo).
- La diffusion en continu est bloquée par défaut.

## Contrôle d'accès (messages privés)

`channels.zalouser.dmPolicy` supporte : `pairing | allowlist | open | disabled` (par défaut : `pairing`).
`channels.zalouser.allowFrom` accepte les ID ou noms d'utilisateurs. L'assistant résout les noms en ID via `zca friend find` quand disponible.

Approuvez via :

- `openclaw pairing list zalouser`
- `openclaw pairing approve zalouser <code>`

## Accès aux groupes (optionnel)

- Par défaut : `channels.zalouser.groupPolicy = "open"` (groupes autorisés). Utilisez `channels.defaults.groupPolicy` pour remplacer la valeur par défaut si non définie.
- Restreindre à une liste blanche :
  - `channels.zalouser.groupPolicy = "allowlist"`
  - `channels.zalouser.groups` (clés : ID ou noms de groupes)
- Bloquer tous les groupes : `channels.zalouser.groupPolicy = "disabled"`.
- L'assistant de configuration peut demander une liste blanche de groupes.
- Au démarrage, OpenClaw résout les noms de groupes/utilisateurs dans la liste blanche en ID et enregistre les mappages ; les entrées non résolues restent inchangées.

Exemple :

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

## Comptes multiples

Les comptes sont mappés aux fichiers de configuration zca. Exemple :

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

## Dépannage

**`zca` introuvable :**

- Installez zca-cli et assurez-vous qu'il se trouve dans `PATH` du processus Gateway.

**La connexion ne persiste pas :**

- `openclaw channels status --probe`
- Reconnectez-vous : `openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`
