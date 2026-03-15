---
summary: "Guide de dépannage approfondi pour la passerelle, les canaux, l'automatisation, les nœuds et le navigateur"
read_when:
  - Le hub de dépannage vous a dirigé ici pour un diagnostic plus approfondi
  - Vous avez besoin de sections de runbook stables basées sur les symptômes avec des commandes exactes
title: "Dépannage"
---

# Dépannage de la passerelle

Cette page est le runbook approfondi.
Commencez par [/help/troubleshooting](/help/troubleshooting) si vous voulez d'abord le flux de triage rapide.

## Échelle de commandes

Exécutez celles-ci en premier, dans cet ordre :

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Signaux de santé attendus :

- `openclaw gateway status` affiche `Runtime: running` et `RPC probe: ok`.
- `openclaw doctor` ne signale aucun problème de configuration/service bloquant.
- `openclaw channels status --probe` affiche les canaux connectés/prêts.

## Anthropic 429 utilisation supplémentaire requise pour le contexte long

Utilisez ceci quand les journaux/erreurs incluent :
`HTTP 429: rate_limit_error: Extra usage is required for long context requests`.

```bash
openclaw logs --follow
openclaw models status
openclaw config get agents.defaults.models
```

Recherchez :

- Le modèle Anthropic Opus/Sonnet sélectionné a `params.context1m: true`.
- Les identifiants Anthropic actuels ne sont pas éligibles pour l'utilisation du contexte long.
- Les demandes échouent uniquement sur les sessions longues/exécutions de modèle qui nécessitent le chemin bêta 1M.

Options de correction :

1. Désactivez `context1m` pour ce modèle pour revenir à la fenêtre de contexte normale.
2. Utilisez une clé API Anthropic avec facturation, ou activez Anthropic Extra Usage sur le compte d'abonnement.
3. Configurez des modèles de secours pour que les exécutions continuent quand les demandes de contexte long Anthropic sont rejetées.

Connexes :

- [/providers/anthropic](/providers/anthropic)
- [/reference/token-use](/reference/token-use)
- [/help/faq#why-am-i-seeing-http-429-ratelimiterror-from-anthropic](/help/faq#why-am-i-seeing-http-429-ratelimiterror-from-anthropic)

## Pas de réponses

Si les canaux sont actifs mais rien ne répond, vérifiez le routage et la politique avant de reconnecter quoi que ce soit.

```bash
openclaw status
openclaw channels status --probe
openclaw pairing list --channel <channel> [--account <id>]
openclaw config get channels
openclaw logs --follow
```

Recherchez :

- Appairage en attente pour les expéditeurs de DM.
- Gating de mention de groupe (`requireMention`, `mentionPatterns`).
- Incompatibilités de liste blanche de canal/groupe.

Signatures courantes :

- `drop guild message (mention required` → message de groupe ignoré jusqu'à mention.
- `pairing request` → l'expéditeur a besoin d'approbation.
- `blocked` / `allowlist` → l'expéditeur/canal a été filtré par la politique.

Connexes :

- [/channels/troubleshooting](/channels/troubleshooting)
- [/channels/pairing](/channels/pairing)
- [/channels/groups](/channels/groups)

## Connectivité de l'interface utilisateur de contrôle du tableau de bord

Quand l'interface utilisateur du tableau de bord/contrôle ne se connecte pas, validez l'URL, le mode d'authentification et les hypothèses de contexte sécurisé.

```bash
openclaw gateway status
openclaw status
openclaw logs --follow
openclaw doctor
openclaw gateway status --json
```

Recherchez :

- URL de sonde et URL de tableau de bord correctes.
- Incompatibilité du mode d'authentification/jeton entre le client et la passerelle.
- Utilisation HTTP où l'identité de l'appareil est requise.

Signatures courantes :

- `device identity required` → contexte non sécurisé ou authentification d'appareil manquante.
- `device nonce required` / `device nonce mismatch` → le client ne complète pas le flux d'authentification d'appareil basé sur le défi (`connect.challenge` + `device.nonce`).
- `device signature invalid` / `device signature expired` → le client a signé la mauvaise charge utile (ou horodatage obsolète) pour la poignée de main actuelle.
- `AUTH_TOKEN_MISMATCH` avec `canRetryWithDeviceToken=true` → le client peut faire une nouvelle tentative de confiance avec le jeton d'appareil en cache.
- `unauthorized` répété après cette nouvelle tentative → dérive du jeton partagé/jeton d'appareil ; actualisez la configuration du jeton et réapprouvez/faites pivoter le jeton d'appareil si nécessaire.
- `gateway connect failed:` → cible d'hôte/port/URL incorrecte.

### Carte rapide des codes de détail d'authentification

Utilisez `error.details.code` de la réponse `connect` échouée pour choisir l'action suivante :

| Code de détail               | Signification                                                | Action recommandée                                                                                                                                                   |
| ---------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AUTH_TOKEN_MISSING`         | Le client n'a pas envoyé de jeton partagé requis.            | Collez/définissez le jeton dans le client et réessayez. Pour les chemins du tableau de bord : `openclaw config get gateway.auth.token` puis collez dans les paramètres de l'interface utilisateur de contrôle.                          |
| `AUTH_TOKEN_MISMATCH`        | Le jeton partagé ne correspondait pas au jeton d'authentification de la passerelle.           | Si `canRetryWithDeviceToken=true`, autorisez une nouvelle tentative de confiance. Si cela échoue toujours, exécutez la [liste de contrôle de récupération de dérive de jeton](/cli/devices#token-drift-recovery-checklist). |
| `AUTH_DEVICE_TOKEN_MISMATCH` | Le jeton d'appareil en cache est obsolète ou révoqué.             | Faites pivoter/réapprouvez le jeton d'appareil en utilisant [CLI des appareils](/cli/devices), puis reconnectez-vous.                                                                                    |
| `PAIRING_REQUIRED`           | L'identité de l'appareil est connue mais non approuvée pour ce rôle. | Approuvez la demande en attente : `openclaw devices list` puis `openclaw devices approve <requestId>`.                                                                        |

Vérification de la migration de l'authentification d'appareil v2 :

```bash
openclaw --version
openclaw doctor
openclaw gateway status
```

Si les journaux affichent des erreurs de nonce/signature, mettez à jour le client de connexion et vérifiez qu'il :

1. attend `connect.challenge`
2. signe la charge utile liée au défi
3. envoie `connect.params.device.nonce` avec le même nonce de défi

Connexes :

- [/web/control-ui](/web/control-ui)
- [/gateway/authentication](/gateway/authentication)
- [/gateway/remote](/gateway/remote)
- [/cli/devices](/cli/devices)

## Service de passerelle non exécuté

Utilisez ceci quand le service est installé mais que le processus ne reste pas actif.

```bash
openclaw gateway status
openclaw status
openclaw logs --follow
openclaw doctor
openclaw gateway status --deep
```

Recherchez :

- `Runtime: stopped` avec des indices de sortie.
- Incompatibilité de configuration de service (`Config (cli)` vs `Config (service)`).
- Conflits de port/écouteur.

Signatures courantes :

- `Gateway start blocked: set gateway.mode=local` → le mode de passerelle local n'est pas activé. Correction : définissez `gateway.mode="local"` dans votre configuration (ou exécutez `openclaw configure`). Si vous exécutez OpenClaw via Podman en utilisant l'utilisateur dédié `openclaw`, la configuration se trouve à `~openclaw/.openclaw/openclaw.json`.
- `refusing to bind gateway ... without auth` → liaison non-loopback sans jeton/mot de passe.
- `another gateway instance is already listening` / `EADDRINUSE` → conflit de port.

Connexes :

- [/gateway/background-process](/gateway/background-process)
- [/gateway/configuration](/gateway/configuration)
- [/gateway/doctor](/gateway/doctor)

## Messages connectés au canal ne circulant pas

Si l'état du canal est connecté mais que le flux de messages est mort, concentrez-vous sur la politique, les permissions et les règles de livraison spécifiques au canal.

```bash
openclaw channels status --probe
openclaw pairing list --channel <channel> [--account <id>]
openclaw status --deep
openclaw logs --follow
openclaw config get channels
```

Recherchez :

- Politique DM (`pairing`, `allowlist`, `open`, `disabled`).
- Liste blanche de groupe et exigences de mention.
- Permissions/scopes d'API de canal manquants.

Signatures courantes :

- `mention required` → message ignoré par la politique de mention de groupe.
- `pairing` / traces d'approbation en attente → l'expéditeur n'est pas approuvé.
- `missing_scope`, `not_in_channel`, `Forbidden`, `401/403` → problème d'authentification/permissions du canal.

Connexes :

- [/channels/troubleshooting](/channels/troubleshooting)
- [/channels/whatsapp](/channels/whatsapp)
- [/channels/telegram](/channels/telegram)
- [/channels/discord](/channels/discord)

## Livraison cron et heartbeat

Si cron ou heartbeat ne s'est pas exécuté ou n'a pas livré, vérifiez d'abord l'état du planificateur, puis la cible de livraison.

```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw system heartbeat last
openclaw logs --follow
```

Recherchez :

- Cron activé et prochain réveil présent.
- Statut de l'historique d'exécution du travail (`ok`, `skipped`, `error`).
- Raisons du saut de heartbeat (`quiet-hours`, `requests-in-flight`, `alerts-disabled`).

Signatures courantes :

- `cron: scheduler disabled; jobs will not run automatically` → cron désactivé.
- `cron: timer tick failed` → l'horloge du planificateur a échoué ; vérifiez les erreurs de fichier/journal/runtime.
- `heartbeat skipped` avec `reason=quiet-hours` → en dehors de la fenêtre d'heures actives.
- `heartbeat: unknown accountId` → ID de compte invalide pour la cible de livraison du heartbeat.
- `heartbeat skipped` avec `reason=dm-blocked` → la cible du heartbeat s'est résolu en une destination de style DM tandis que `agents.defaults.heartbeat.directPolicy` (ou remplacement par agent) est défini sur `block`.

Connexes :

- [/automation/troubleshooting](/automation/troubleshooting)
- [/automation/cron-jobs](/automation/cron-jobs)
- [/gateway/heartbeat](/gateway/heartbeat)

## L'outil de nœud appairé échoue

Si un nœud est appairé mais que les outils échouent, isolez l'état de premier plan, de permission et d'approbation.

```bash
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
openclaw logs --follow
openclaw status
```

Recherchez :

- Nœud en ligne avec les capacités attendues.
- Octrois de permission du système d'exploitation pour la caméra/micro/localisation/écran.
- État des approbations exec et de la liste blanche.

Signatures courantes :

- `NODE_BACKGROUND_UNAVAILABLE` → l'application de nœud doit être au premier plan.
- `*_PERMISSION_REQUIRED` / `LOCATION_PERMISSION_REQUIRED` → permission du système d'exploitation manquante.
- `SYSTEM_RUN_DENIED: approval required` → approbation exec en attente.
- `SYSTEM_RUN_DENIED: allowlist miss` → commande bloquée par la liste blanche.

Connexes :

- [/nodes/troubleshooting](/nodes/troubleshooting)
- [/nodes/index](/nodes/index)
- [/tools/exec-approvals](/tools/exec-approvals)

## L'outil de navigateur échoue

Utilisez ceci quand les actions de l'outil de navigateur échouent même si la passerelle elle-même est saine.

```bash
openclaw browser status
openclaw browser start --browser-profile openclaw
openclaw browser profiles
openclaw logs --follow
openclaw doctor
```

Recherchez :

- Chemin d'exécutable de navigateur valide.
- Accessibilité du profil CDP.
- Attachement de l'onglet de relais d'extension (si un profil de relais d'extension est configuré).

Signatures courantes :

- `Failed to start Chrome CDP on port` → le processus du navigateur n'a pas pu se lancer.
- `browser.executablePath not found` → le chemin configuré est invalide.
- `Chrome extension relay is running, but no tab is connected` → relais d'extension non attaché.
- `Browser attachOnly is enabled ... not reachable` → le profil attach-only n'a pas de cible accessible.

Connexes :

- [/tools/browser-linux-troubleshooting](/tools/browser-linux-troubleshooting)
- [/tools/chrome-extension](/tools/chrome-extension)
- [/tools/browser](/tools/browser)

## Si vous avez effectué une mise à niveau et quelque chose s'est soudainement cassé

La plupart des pannes post-mise à niveau sont dues à une dérive de configuration ou à des valeurs par défaut plus strictes qui sont maintenant appliquées.

### 1) Le comportement de remplacement d'authentification et d'URL a changé

```bash
openclaw gateway status
openclaw config get gateway.mode
openclaw config get gateway.remote.url
openclaw config get gateway.auth.mode
```

Ce qu'il faut vérifier :

- Si `gateway.mode=remote`, les appels CLI peuvent cibler le serveur distant alors que votre service local fonctionne correctement.
- Les appels explicites `--url` ne reviennent pas aux identifiants stockés.

Signatures courantes :

- `gateway connect failed:` → mauvaise cible d'URL.
- `unauthorized` → point de terminaison accessible mais authentification incorrecte.

### 2) Les garde-fous de liaison et d'authentification sont plus stricts

```bash
openclaw config get gateway.bind
openclaw config get gateway.auth.token
openclaw gateway status
openclaw logs --follow
```

Ce qu'il faut vérifier :

- Les liaisons non-loopback (`lan`, `tailnet`, `custom`) nécessitent une authentification configurée.
- Les anciennes clés comme `gateway.token` ne remplacent pas `gateway.auth.token`.

Signatures courantes :

- `refusing to bind gateway ... without auth` → incompatibilité liaison+authentification.
- `RPC probe: failed` alors que le runtime est en cours d'exécution → gateway active mais inaccessible avec l'authentification/URL actuelle.

### 3) L'état d'appairage et d'identité de l'appareil a changé

```bash
openclaw devices list
openclaw pairing list --channel <channel> [--account <id>]
openclaw logs --follow
openclaw doctor
```

Ce qu'il faut vérifier :

- Approbations d'appareils en attente pour le tableau de bord/nœuds.
- Approbations d'appairage DM en attente après des modifications de politique ou d'identité.

Signatures courantes :

- `device identity required` → authentification de l'appareil non satisfaite.
- `pairing required` → l'expéditeur/l'appareil doit être approuvé.

Si la configuration du service et le runtime ne sont toujours pas d'accord après les vérifications, réinstallez les métadonnées du service à partir du même répertoire de profil/état :

```bash
openclaw gateway install --force
openclaw gateway restart
```

Connexes :

- [/gateway/pairing](/gateway/pairing)
- [/gateway/authentication](/gateway/authentication)
- [/gateway/background-process](/gateway/background-process)
