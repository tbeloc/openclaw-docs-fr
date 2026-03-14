---
summary: "Accès au tableau de bord de la passerelle (Control UI) et authentification"
read_when:
  - Changing dashboard authentication or exposure modes
title: "Tableau de bord"
---

# Tableau de bord (Control UI)

Le tableau de bord de la passerelle est l'interface de contrôle du navigateur servie à `/` par défaut
(à remplacer avec `gateway.controlUi.basePath`).

Ouverture rapide (passerelle locale) :

- [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (ou [http://localhost:18789/](http://localhost:18789/))

Références clés :

- [Control UI](/web/control-ui) pour l'utilisation et les capacités de l'interface.
- [Tailscale](/gateway/tailscale) pour l'automatisation Serve/Funnel.
- [Surfaces web](/web) pour les modes de liaison et les notes de sécurité.

L'authentification est appliquée lors de la poignée de main WebSocket via `connect.params.auth`
(jeton ou mot de passe). Voir `gateway.auth` dans [Configuration de la passerelle](/gateway/configuration).

Note de sécurité : le Control UI est une **surface d'administration** (chat, config, approbations d'exécution).
Ne l'exposez pas publiquement. L'interface conserve les jetons d'URL du tableau de bord dans sessionStorage
pour la session actuelle de l'onglet du navigateur et l'URL de passerelle sélectionnée, et les supprime de l'URL après le chargement.
Préférez localhost, Tailscale Serve ou un tunnel SSH.

## Chemin rapide (recommandé)

- Après l'intégration, la CLI ouvre automatiquement le tableau de bord et affiche un lien propre (sans jeton).
- Rouvrez à tout moment : `openclaw dashboard` (copie le lien, ouvre le navigateur si possible, affiche l'indice SSH si sans interface graphique).
- Si l'interface demande une authentification, collez le jeton de `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`) dans les paramètres de Control UI.

## Principes de base des jetons (local vs distant)

- **Localhost** : ouvrez `http://127.0.0.1:18789/`.
- **Source du jeton** : `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`) ; `openclaw dashboard` peut le transmettre via le fragment d'URL pour un amorçage unique, et le Control UI le conserve dans sessionStorage pour la session actuelle de l'onglet du navigateur et l'URL de passerelle sélectionnée au lieu de localStorage.
- Si `gateway.auth.token` est géré par SecretRef, `openclaw dashboard` affiche/copie/ouvre une URL sans jeton par conception. Cela évite d'exposer les jetons gérés en externe dans les journaux du shell, l'historique du presse-papiers ou les arguments de lancement du navigateur.
- Si `gateway.auth.token` est configuré comme SecretRef et n'est pas résolu dans votre shell actuel, `openclaw dashboard` affiche toujours une URL sans jeton plus des conseils de configuration d'authentification exploitables.
- **Pas localhost** : utilisez Tailscale Serve (sans jeton pour Control UI/WebSocket si `gateway.auth.allowTailscale: true`, suppose un hôte de passerelle de confiance ; les API HTTP nécessitent toujours un jeton/mot de passe), une liaison tailnet avec un jeton ou un tunnel SSH. Voir [Surfaces web](/web).

## Si vous voyez « unauthorized » / 1008

- Assurez-vous que la passerelle est accessible (local : `openclaw status` ; distant : tunnel SSH `ssh -N -L 18789:127.0.0.1:18789 user@host` puis ouvrez `http://127.0.0.1:18789/`).
- Pour `AUTH_TOKEN_MISMATCH`, les clients peuvent effectuer une nouvelle tentative de confiance avec un jeton d'appareil mis en cache lorsque la passerelle retourne des indices de nouvelle tentative. Si l'authentification échoue toujours après cette nouvelle tentative, résolvez la dérive de jeton manuellement.
- Pour les étapes de réparation de la dérive de jeton, suivez [Liste de contrôle de récupération de dérive de jeton](/cli/devices#token-drift-recovery-checklist).
- Récupérez ou fournissez le jeton à partir de l'hôte de la passerelle :
  - Config en texte brut : `openclaw config get gateway.auth.token`
  - Config gérée par SecretRef : résolvez le fournisseur de secrets externe ou exportez `OPENCLAW_GATEWAY_TOKEN` dans ce shell, puis réexécutez `openclaw dashboard`
  - Aucun jeton configuré : `openclaw doctor --generate-gateway-token`
- Dans les paramètres du tableau de bord, collez le jeton dans le champ d'authentification, puis connectez-vous.
