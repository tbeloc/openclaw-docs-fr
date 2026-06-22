---
summary: "Support des agents externes Raft via le pont de réveil Raft CLI"
read_when:
  - You want to connect OpenClaw to a Raft workspace
  - You are configuring a Raft External Agent
  - You are debugging Raft wake delivery
title: "Raft"
sidebarTitle: "Raft"
---

Le support Raft connecte un agent OpenClaw à un agent externe Raft via la CLI Raft locale. Raft envoie des indices de réveil authentifiés à la passerelle. L'agent utilise ensuite la CLI Raft pour vérifier et envoyer des messages.

## Installation

Raft est un plugin externe officiel. Installez-le sur l'hôte de la passerelle :

```bash
openclaw plugins install @openclaw/raft
openclaw gateway restart
```

Détails : [Plugins](/fr/tools/plugin)

## Prérequis

- Un espace de travail Raft avec un agent externe.
- La CLI Raft installée sur le même hôte que la passerelle OpenClaw.
- Un profil CLI Raft déjà connecté et associé à cet agent externe.

Le plugin ne stocke pas les identifiants Raft. La CLI Raft conserve cette authentification dans son propre profil.

## Configuration

Définissez le profil dans la configuration :

```json5
{
  channels: {
    raft: {
      enabled: true,
      profile: "openclaw",
    },
  },
}
```

Pour le compte par défaut, vous pouvez plutôt définir `RAFT_PROFILE` dans l'environnement de la passerelle :

```bash
RAFT_PROFILE=openclaw
```

Utilisez un compte nommé quand une passerelle se connecte à plus d'un agent externe Raft :

```json5
{
  channels: {
    raft: {
      accounts: {
        support: {
          profile: "support-agent",
        },
        engineering: {
          profile: "engineering-agent",
        },
      },
    },
  },
}
```

Le flux de configuration interactif enregistre le même profil :

```bash
openclaw channels setup raft
```

## Fonctionnement

Quand la passerelle démarre, le plugin :

1. Ouvre un point de terminaison de réveil HTTP en boucle locale sur un port éphémère.
2. Démarre `raft --profile <profile> agent bridge` avec ce point de terminaison et un jeton par processus.
3. Accepte uniquement les indices de réveil authentifiés et sans contenu avec une identité de relecture du pont local.
4. Nécessite l'un de `eventId`, `attemptId`, `messageId`, `delivery_id`, `wake_id`, ou `id`.
5. Déduplique les livraisons de réveil récemment réessayées par ID d'événement du pont, y compris entre les redémarrages de la passerelle.
6. Retourne une session d'exécution stable pour le pont actuel et un lot de vidage d'activité vide pour le protocole CLI Raft.
7. Démarre un tour d'agent OpenClaw sérialisé pour chaque réveil accepté.

Le pont possède les tentatives de livraison Raft et les reconnexions. Le tour OpenClaw reçoit uniquement un avis de réveil, pas une copie du corps du message Raft. Il utilise la CLI pour lire les messages en attente et envoyer sa réponse :

```bash
raft --profile openclaw message check
raft --profile openclaw message send
```

<Note>
Raft n'est pas un transport de message push normal. OpenClaw n'envoie pas automatiquement le texte final du modèle via le pont, donc l'agent doit utiliser la CLI Raft après traitement d'un réveil.
</Note>

## Vérification

Vérifiez qu'OpenClaw peut trouver la CLI et a un profil configuré :

```bash
openclaw channels status --probe
openclaw plugins inspect raft --runtime --json
```

Ensuite, envoyez un message à l'agent externe Raft. Le journal de la passerelle devrait afficher le démarrage du pont Raft, suivi d'un réveil entrant. L'agent devrait utiliser le profil Raft configuré pour vérifier ses messages en attente.

## Dépannage

<AccordionGroup>
  <Accordion title="La CLI Raft est manquante">
    Installez la CLI Raft sur l'hôte de la passerelle et rendez `raft` disponible sur le `PATH` du service. Vérifiez-le avec `raft --help`, puis redémarrez la passerelle.
  </Accordion>
  <Accordion title="Le pont se ferme immédiatement">
    Vérifiez que le profil configuré est connecté et appartient à l'agent externe Raft prévu. Exécutez `raft --profile <profile> agent bridge` directement pour voir le diagnostic de la CLI.
  </Accordion>
  <Accordion title="Un réveil arrive mais aucune réponse Raft n'est envoyée">
    C'est attendu quand l'agent n'invoque pas la CLI Raft. Le pont de réveil ne porte pas les corps de messages ou les réponses finales automatiques. Vérifiez la politique d'outils de l'agent et assurez-vous qu'il peut exécuter `raft --profile <profile> message check` et `message send`.
  </Accordion>
</AccordionGroup>

## Références

- [Raft](https://raft.build/)
- [Documentation Raft](https://docs.raft.build/welcome/)
- [Intégration Raft Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/raft)
