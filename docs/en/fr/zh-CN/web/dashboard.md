---
read_when:
  - Modification de l'authentification du tableau de bord ou du mode d'exposition
summary: Accès et authentification du tableau de bord Gateway (UI de contrôle)
title: Tableau de bord
x-i18n:
  generated_at: "2026-02-03T10:13:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e6876d50e17d3dd741471ed78bef6ac175b2fdbdc1c45dd52d9d2bd013e17f31
  source_path: web/dashboard.md
  workflow: 15
---

# Tableau de bord (UI de contrôle)

Le tableau de bord Gateway est une UI de contrôle de navigateur fournie par défaut sur `/`
(à remplacer via `gateway.controlUi.basePath`).

Ouverture rapide (Gateway local) :

- http://127.0.0.1:18789/ (ou http://localhost:18789/)

Références clés :

- [UI de contrôle](/web/control-ui) pour connaître l'utilisation et les fonctionnalités de l'UI.
- [Tailscale](/gateway/tailscale) pour l'automatisation Serve/Funnel.
- [Interface Web](/web) pour les modes de liaison et les considérations de sécurité.

L'authentification est appliquée via `connect.params.auth` (token ou mot de passe) lors de la poignée de main WebSocket.
Voir `gateway.auth` dans [Configuration Gateway](/gateway/configuration).

Considérations de sécurité : l'UI de contrôle est une **interface d'administration** (chat, configuration, approbations d'exécution).
Ne l'exposez pas publiquement. L'UI stocke le token dans `localStorage` après le premier chargement.
Privilégiez localhost, Tailscale Serve ou les tunnels SSH.

## Chemin rapide (recommandé)

- Après l'assistant d'intégration, la CLI ouvre maintenant automatiquement le tableau de bord avec votre token et affiche le même lien avec token.
- Réouvrez à tout moment : `openclaw dashboard` (copie le lien, ouvre le navigateur si possible, affiche une invite SSH si environnement sans interface).
- Le token reste local (paramètre de requête uniquement) ; l'UI le supprime après le premier chargement et l'enregistre dans localStorage.

## Bases du token (local vs distant)

- **Localhost** : ouvrez `http://127.0.0.1:18789/`. Si vous voyez « unauthorized », exécutez `openclaw dashboard` et utilisez le lien avec token (`?token=...`).
- **Source du token** : `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`) ; l'UI l'enregistre après le premier chargement.
- **Non-localhost** : utilisez Tailscale Serve (pas de token requis si `gateway.auth.allowTailscale: true`), liaison tailnet avec token, ou tunnel SSH. Voir [Interface Web](/web).

## Si vous voyez « unauthorized » / 1008

- Exécutez `openclaw dashboard` pour obtenir un nouveau lien avec token.
- Assurez-vous que Gateway est accessible (local : `openclaw status` ; distant : tunnel SSH `ssh -N -L 18789:127.0.0.1:18789 user@host` puis ouvrez `http://127.0.0.1:18789/?token=...`).
- Dans les paramètres du tableau de bord, collez le même token que celui configuré dans `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
