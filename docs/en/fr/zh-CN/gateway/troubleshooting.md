---
read_when:
  - Enquêter sur les problèmes d'exécution ou les pannes
summary: Guide de dépannage rapide pour les problèmes courants d'OpenClaw
title: Dépannage
x-i18n:
  generated_at: "2026-02-03T10:09:42Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a07bb06f0b5ef56872578aaff6ac83adb740e2f1d23e3eed86934b51f62a877e
  source_path: gateway/troubleshooting.md
  workflow: 15
---

# Dépannage 🔧

Lorsque OpenClaw se comporte de manière inattendue, voici comment le corriger.

Si vous voulez simplement classer rapidement un problème, consultez d'abord les [premières soixante secondes](/help/faq#first-60-seconds-if-somethings-broken) pour les problèmes courants. Cette page approfondit les pannes d'exécution et les diagnostics.

Raccourcis spécifiques aux fournisseurs : [/channels/troubleshooting](/channels/troubleshooting)

## État et diagnostic

Commandes de classification rapide (dans l'ordre) :

| Commande                           | Ce qu'elle vous dit                                                                                                                                                 | Quand l'utiliser                                    |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `openclaw status`                  | Résumé local : OS + mises à jour, accessibilité/mode Gateway, services, agents/sessions, état de configuration des fournisseurs                                     | Première vérification, aperçu rapide                |
| `openclaw status --all`            | Diagnostic local complet (lecture seule, collable, relativement sûr) incluant la fin des journaux                                                                  | Lorsque vous devez partager un rapport de débogage  |
| `openclaw status --deep`           | Exécute les vérifications de santé Gateway (y compris les sondes de fournisseurs ; nécessite une Gateway accessible)                                              | Quand « configuré » ne signifie pas « fonctionne »  |
| `openclaw gateway probe`           | Découverte Gateway + accessibilité (cibles locales + distantes)                                                                                                     | Quand vous soupçonnez une mauvaise sonde Gateway   |
| `openclaw channels status --probe` | Interroge l'état des canaux auprès de la Gateway en cours d'exécution (et sonde optionnellement)                                                                  | Quand Gateway est accessible mais les canaux ne le sont pas |
| `openclaw gateway status`          | État du superviseur (launchd/systemd/schtasks), PID/sortie d'exécution, dernière erreur Gateway                                                                   | Quand le service « semble chargé » mais ne s'exécute pas |
| `openclaw logs --follow`           | Journaux en temps réel (meilleur signal pour les problèmes d'exécution)                                                                                            | Quand vous avez besoin de la cause réelle de la panne |

**Partage de sortie :** Préférez `openclaw status --all` (il masque les jetons). Si vous collez `openclaw status`, envisagez de définir d'abord `OPENCLAW_SHOW_SECRETS=0` (aperçu des jetons).

Voir aussi : [Vérification de santé](/gateway/health) et [Journalisation](/logging).

## Problèmes courants

### Aucune clé API trouvée pour le fournisseur « anthropic »

Cela signifie que **le magasin d'authentification de l'agent est vide** ou que les identifiants Anthropic manquent.
L'authentification est **indépendante par agent**, donc les nouveaux agents n'héritent pas des clés de l'agent principal.

Options de correction :

- Réexécutez l'assistant et sélectionnez **Anthropic** pour cet agent.
- Ou collez le setup-token sur **l'hôte Gateway** :
  ```bash
  openclaw models auth setup-token --provider anthropic
  ```
- Ou copiez `auth-profiles.json` du répertoire de l'agent principal vers le répertoire du nouvel agent.

Vérification :

```bash
openclaw models status
```

### Échec de l'actualisation du jeton OAuth (abonnement Anthropic Claude)

Cela signifie que le jeton OAuth Anthropic stocké a expiré et l'actualisation a échoué.
Si vous utilisez un abonnement Claude (sans clé API), la correction la plus fiable est de
passer à **Claude Code setup-token** et de coller sur **l'hôte Gateway**.

**Recommandé (setup-token) :**

```bash
# Exécutez sur l'hôte Gateway (collez le setup-token)
openclaw models auth setup-token --provider anthropic
openclaw models status
```

Si vous avez généré le jeton ailleurs :

```bash
openclaw models auth paste-token --provider anthropic
openclaw models status
```

Plus de détails : [Anthropic](/providers/anthropic) et [OAuth](/concepts/oauth).

### Control UI échoue sur HTTP (« device identity required » / « connect failed »)

Si vous ouvrez le tableau de bord sur HTTP pur (par exemple `http://<lan-ip>:18789/` ou
`http://<tailscale-ip>:18789/`), le navigateur s'exécute dans un **contexte non sécurisé**,
ce qui bloque WebCrypto et empêche la génération d'identité d'appareil.

**Correction :**

- Préférez HTTPS via [Tailscale Serve](/gateway/tailscale).
- Ou ouvrez localement sur l'hôte Gateway : `http://127.0.0.1:18789/`.
- Si vous devez utiliser HTTP, activez `gateway.controlUi.allowInsecureAuth: true` et
  utilisez le jeton Gateway (jeton uniquement ; pas d'identité d'appareil/appairage). Voir
  [Control UI](/web/control-ui#insecure-http).

### Échec de l'analyse des secrets CI

Cela signifie que `detect-secrets` a trouvé de nouveaux candidats qui ne sont pas encore dans la ligne de base.
Suivez [Analyse des secrets](/gateway/security#secret-scanning-detect-secrets).

### Service installé mais ne s'exécute pas

Si le service Gateway est installé mais le processus se termine immédiatement, le service
peut afficher « chargé » mais ne s'exécute pas réellement.

**Vérification :**

```bash
openclaw gateway status
openclaw doctor
```

Doctor/service affichera l'état d'exécution (PID/dernière sortie) et les conseils de journalisation.

**Journaux :**

- Préféré : `openclaw logs --follow`
- Journaux de fichier (toujours) : `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (ou votre `logging.file` configuré)
- macOS LaunchAgent (si installé) : `$OPENCLAW_STATE_DIR/logs/gateway.log` et `gateway.err.log`
- Linux systemd (si installé) : `journalctl --user -u openclaw-gateway[-<profile>].service -n 200 --no-pager`
- Windows : `schtasks /Query /TN "OpenClaw Gateway (<profile>)" /V /FO LIST`

**Activation de plus de journalisation :**

- Augmentez la verbosité du journal de fichier (JSONL persistant) :
  ```json
  { "logging": { "level": "debug" } }
  ```
- Augmentez la verbosité de la console (sortie TTY uniquement) :
  ```json
  { "logging": { "consoleLevel": "debug", "consoleStyle": "pretty" } }
  ```
- Conseil rapide : `--verbose` affecte uniquement la sortie **console**. Le journal de fichier est toujours contrôlé par `logging.level`.

Voir [/logging](/logging) pour un aperçu complet du format, de la configuration et de l'accès.

### « Gateway start blocked: set gateway.mode=local »

Cela signifie que la configuration existe mais `gateway.mode` n'est pas défini (ou n'est pas `local`), donc
Gateway refuse de démarrer.

**Correction (recommandée) :**

- Exécutez l'assistant et définissez le mode d'exécution Gateway sur **Local** :
  ```bash
  openclaw configure
  ```
- Ou définissez directement :
  ```bash
  openclaw config set gateway.mode local
  ```

**Si vous avez l'intention d'exécuter une Gateway distante :**

- Définissez l'URL distante et conservez `gateway.mode=remote` :
  ```bash
  openclaw config set gateway.mode remote
  openclaw config set gateway.remote.url "wss://gateway.example.com"
  ```

**Utilisation temporaire/développement uniquement :** Passez `--allow-unconfigured` pour démarrer Gateway sans
`gateway.mode=local`.

**Pas encore de fichier de configuration ?** Exécutez `openclaw setup` pour créer la configuration initiale, puis réexécutez
Gateway.

### Environnement de service (PATH + exécution)

Le service Gateway s'exécute avec un **PATH minimal** pour éviter les interférences du shell/gestionnaire :

- macOS : `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`
- Linux : `/usr/local/bin`, `/usr/bin`, `/bin`

Cela exclut intentionnellement les gestionnaires de versions (nvm/fnm/volta/asdf) et les
gestionnaires de paquets (pnpm/npm), car le service ne charge pas votre initialisation shell. Les variables
d'exécution comme `DISPLAY` doivent aller dans `~/.openclaw/.env` (chargé tôt par Gateway).
Les exécutions `Exec` sur `host=gateway` fusionneront votre `PATH` de shell de connexion dans l'environnement d'exécution, donc
les outils manquants signifient généralement que votre initialisation shell ne les exporte pas (ou définissez
`tools.exec.pathPrepend`). Voir [/tools/exec](/tools/exec).

Les canaux WhatsApp + Telegram nécessitent **Node** ; Bun n'est pas supporté. Si votre
service a été installé avec Bun ou un chemin Node géré par version, exécutez `openclaw doctor`
pour migrer vers une installation Node système.

### Skill manquant de clé API dans le bac à sable

**Symptôme :** Skill fonctionne sur l'hôte mais échoue dans le bac à sable en raison d'une clé API manquante.

**Cause :** L'exécution du bac à sable s'exécute dans Docker, **ne** hérite **pas** de `process.env` de l'hôte.

**Correction :**

- Définissez `agents.defaults.sandbox.docker.env` (ou `agents.list[].sandbox.docker.env` par agent)
- Ou intégrez les clés dans votre image de bac à sable personnalisée
- Puis exécutez `openclaw sandbox recreate --agent <id>` (ou `--all`)

### Service en cours d'exécution mais port non écouté

Si le service rapporte **en cours d'exécution** mais qu'aucun port Gateway n'écoute,
Gateway peut refuser de se lier.

**Ce que « en cours d'exécution » signifie ici**

- `Runtime: running` signifie que votre superviseur (launchd/systemd/schtasks) pense que le processus est vivant.
- `RPC probe` signifie que la CLI peut réellement se connecter au WebSocket Gateway et appeler `status`.
- Faites toujours confiance à `Probe target:` + `Config (service):` comme ligne d'information « qu'avons-nous réellement essayé ? ».

**Vérification :**

- `gateway.mode` doit être `local` pour exécuter `openclaw gateway` et le service.
- Si vous avez défini `gateway.mode=remote`, la **CLI par défaut** utilise l'URL distante. Le service peut toujours s'exécuter localement, mais votre CLI peut sonder le mauvais endroit. Utilisez `openclaw gateway status` pour voir le port que le service résout + la cible de sonde (ou passez `--url`).
- `openclaw gateway status` et `openclaw doctor` affichent la **dernière erreur Gateway** dans les journaux lorsque le service semble s'exécuter mais que le port est fermé.
- Les liaisons non-loopback locales (`lan`/`tailnet`/`custom`, ou `auto` quand loopback n'est pas disponible) nécessitent l'authentification :
  `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
- `gateway.remote.token` est uniquement pour les appels CLI distants ; il **n'** active **pas** l'authentification locale.
- `gateway.token` est ignoré ; utilisez `gateway.auth.token`.

**Si `openclaw gateway status` affiche une non-concordance de configuration**

- `Config (cli): ...` et `Config (service): ...` devraient généralement correspondre.
- S'ils ne correspondent pas, vous éditez presque certainement une configuration tandis que le service en exécute une autre.
- Correction : Réexécutez `openclaw gateway install --force` à partir du même `--profile` / `OPENCLAW_STATE_DIR` que celui que vous souhaitez que le service utilise.

**Si `openclaw gateway status` rapporte un problème de configuration de service**

- La configuration du superviseur (launchd/systemd/schtasks) manque les valeurs par défaut actuelles.
- Correction : Exécutez `openclaw doctor` pour la mettre à jour (ou `openclaw gateway install --force` pour la réécrire complètement).

**Si `Last gateway error:` mentionne « refusing to bind … without auth »**

- Vous avez défini `gateway.bind` en mode non-loopback local (`lan`/`tailnet`/`custom`, ou `auto` quand loopback n'est pas disponible) mais n'avez pas configuré l'authentification.
- Correction : Définissez `gateway.auth.mode` + `gateway.auth.token` (ou exportez `OPENCLAW_GATEWAY_TOKEN`) et redémarrez le service.

**Si `openclaw gateway status` affiche `bind=tailnet` mais n'a pas trouvé l'interface tailnet**

- Gateway tente de se lier à l'IP Tailscale (100.64.0.0/10) mais n'a pas été détectée sur l'hôte.
- Correction : Démarrez Tailscale sur cette machine (ou changez `gateway.bind` en `loopback`/`lan`).

**Si `Probe note:` dit que la sonde utilise loopback**

- Pour `bind=lan` c'est attendu : Gateway écoute `0.0.0.0` (toutes les interfaces), loopback devrait toujours se connecter localement.
- Pour les clients distants, utilisez l'IP LAN réelle (pas
