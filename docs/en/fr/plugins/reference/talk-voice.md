---
summary: "Gérer la sélection de voix Talk (lister/définir)."
read_when:
  - You are installing, configuring, or auditing the talk-voice plugin
title: "Plugin Talk Voice"
---

# Plugin Talk Voice

Gérer la sélection de voix Talk (lister/définir).

## Distribution

- Package: `openclaw`
- Install route: included in OpenClaw

## Surface

commands: `/voice`

<!-- openclaw-plugin-reference:manual-start -->

## Configurer une voix Talk depuis le chat

Définissez `talk.provider` et configurez l'entrée `talk.providers.<provider>` correspondante avant d'utiliser la commande. Le fournisseur actif doit supporter l'énumération des voix.

- `/voice status` affiche le fournisseur actif et l'ID de voix défini pour ce fournisseur. Le champ de clé API n'est qu'une valeur de configuration masquée ou non définie ; il ne prouve pas que des identifiants utilisables sont disponibles.
- `/voice list [limit]` énumère les voix du fournisseur actif. La limite par défaut est 12 et le maximum est 50.
- `/voice set <voiceId|name>` résout une voix par ID exact, nom exact ou nom partiel, puis l'enregistre dans `talk.providers.<activeProvider>.voiceId`.

Discord enregistre la commande native en tant que `/talkvoice` ; ses sous-commandes et arguments sont identiques. Status et list sont en lecture seule. La définition d'une voix nécessite un propriétaire sur un canal de message ou la portée `operator.admin` pour un client Gateway.

Les échecs sont retournés visiblement dans le chat. La configuration Talk manquante identifie les clés requises ; les erreurs de recherche de fournisseur incluent l'erreur du fournisseur ; les voix inconnues suggèrent d'énumérer les voix disponibles ; et les écritures non autorisées indiquent la permission requise.

<!-- openclaw-plugin-reference:manual-end -->
