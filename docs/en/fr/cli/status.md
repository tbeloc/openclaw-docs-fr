---
summary: "Référence CLI pour `openclaw status` (diagnostiques, sondes, instantanés d'utilisation)"
read_when:
  - Vous voulez un diagnostic rapide de la santé des canaux + destinataires de sessions récentes
  - Vous voulez un statut « all » collable pour le débogage
title: "status"
---

# `openclaw status`

Diagnostiques pour les canaux + sessions.

```bash
openclaw status
openclaw status --all
openclaw status --deep
openclaw status --usage
```

Notes :

- `--deep` exécute des sondes en direct (WhatsApp Web + Telegram + Discord + Google Chat + Slack + Signal).
- La sortie inclut les magasins de sessions par agent lorsque plusieurs agents sont configurés.
- L'aperçu inclut l'état d'installation/exécution du service Gateway + nœud hôte lorsqu'il est disponible.
- L'aperçu inclut le canal de mise à jour + SHA git (pour les checkouts source).
- Les informations de mise à jour s'affichent dans l'aperçu ; si une mise à jour est disponible, le statut affiche un conseil pour exécuter `openclaw update` (voir [Mise à jour](/install/updating)).
- Les surfaces de statut en lecture seule (`status`, `status --json`, `status --all`) résolvent les SecretRefs supportés pour leurs chemins de configuration ciblés lorsque c'est possible.
- Si une SecretRef de canal supportée est configurée mais indisponible dans le chemin de commande actuel, le statut reste en lecture seule et rapporte une sortie dégradée au lieu de planter. La sortie humaine affiche des avertissements tels que « token configuré indisponible dans ce chemin de commande », et la sortie JSON inclut `secretDiagnostics`.
