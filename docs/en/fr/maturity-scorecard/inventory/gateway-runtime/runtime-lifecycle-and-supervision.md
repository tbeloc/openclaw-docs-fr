---
version: 3
---

# Matrice des fonctionnalités WebSocket du runtime de passerelle - Cycle de vie de la passerelle

## Résumé

Le cycle de vie du runtime et la supervision sont implémentés dans le démarrage au premier plan `openclaw gateway`, les chemins d'installation/démarrage/arrêt/redémarrage/statut du service supervisé, les adaptateurs de service de plateforme, la planification du rechargement de configuration, le redémarrage sécurisé et l'isolation multi-passerelle. La couverture est **Oui** car le dépôt dispose de preuves réelles du flux Gateway/serveur pour le démarrage direct du serveur, deux instances de passerelle concurrentes, l'intégration d'installation du démon et le cycle de vie launchd de macOS. La faiblesse restante est une preuve de plateforme inégale : les flux Linux systemd et Windows Scheduled Task ont une couverture forte en termes de tests moqués/unitaires mais pas une couverture E2E supervisée en direct équivalente, et les modes de rechargement sont couverts principalement au niveau du gestionnaire/rechargeur plutôt que par un scénario complet de modification/redémarrage de passerelle en direct.

## Fonctionnalités

- Démarrage au premier plan : Démarrage au premier plan local via `openclaw gateway`.
- Installation du service : Installation du cycle de vie supervisé sur macOS, utilisateur Linux/systemd et planification native des tâches Windows.
- Redémarrage et arrêt : Comportement correct de `restart` et `stop` pour les installations supervisées.
- Statut du service : Comportement du statut pour les installations supervisées.
- Paramètres de liaison et de port : Précédence de liaison et de port entre les drapeaux CLI, les variables d'environnement, la configuration et les métadonnées du superviseur persistantes.
- Rechargement de configuration : Modes de rechargement de configuration : `off`, `hot`, `restart` et `hybrid`.
- Isolation multi-passerelle : Isolation multi-passerelle sur un hôte, y compris la séparation de la configuration/état/espace de travail.

## Fraîcheur de l'archive

- `gitcrawl doctor --json` : `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json` : `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : **86**

Étiquette : **Oui**

Signaux positifs :

- Le démarrage de la passerelle au premier plan est documenté et implémenté avec les options explicites `--port`, `--bind`, `--token`, `--auth`, `--tailscale`, `--force` et de journalisation dans `docs/gateway/index.md:25`, `docs/gateway/index.md:40`, `src/cli/gateway-cli/run-command.ts:10` et `src/cli/gateway-cli/run.ts:472`.
- La précédence de liaison et de port est documentée dans `docs/gateway/index.md:111` et implémentée par `resolveGatewayPort`, qui vérifie `OPENCLAW_GATEWAY_PORT`, la configuration, puis le port par défaut dans `src/config/paths.ts:262`.
- Le cycle de vie supervisé est implémenté via la distribution de plateforme pour LaunchAgent macOS, systemd utilisateur Linux et Scheduled Task Windows dans `src/daemon/service.ts:250`, avec les commandes de cycle de vie CLI câblées dans `src/cli/daemon-cli/register-service-commands.ts:56`.
- Le redémarrage, l'arrêt, le statut, le report de redémarrage sécurisé et la récupération non chargée ont une logique de cycle de vie centrale dans `src/cli/daemon-cli/lifecycle-core.ts:374`, `src/cli/daemon-cli/lifecycle-core.ts:464`, `src/cli/daemon-cli/lifecycle.ts:151` et `src/cli/daemon-cli/lifecycle.ts:275`.
- Les modes de rechargement de configuration sont documentés dans `docs/gateway/index.md:126` et `docs/gateway/configuration.md:550`, et implémentés par le rechargeur géré dans `src/gateway/server.impl.ts:1653`, `src/gateway/config-reload.ts:246` et les gestionnaires nécessitant un redémarrage dans `src/gateway/server-reload-handlers.ts:518`.
- L'isolation multi-passerelle est documentée avec des ports, une configuration, un état et des espaces de travail séparés dans `docs/gateway/index.md:152`, soutenue par les remplacements de configuration/état dans `src/config/paths.ts:60`, `src/config/paths.ts:154` et `src/config/paths.ts:193`.
- Des preuves réelles du flux Gateway/serveur existent : `test/gateway.multi.e2e.test.ts:27` démarre deux instances de passerelle et valide les crochets HTTP et l'appairage de nœud WebSocket par instance ; `src/gateway/server-network-runtime.e2e.test.ts:68` démarre un serveur réel avec une configuration/état temporaire et valide le comportement des requêtes ; `src/daemon/launchd.integration.e2e.test.ts:177` installe/redémarre/arrête/démarre un vrai LaunchAgent macOS.

Signaux négatifs :

- La supervision Linux systemd et Windows Scheduled Task sont représentées principalement par des tests unitaires/moqués, pas par des preuves E2E de gestionnaire de service en direct correspondant à la profondeur de launchd.
- Les modes de rechargement ont une couverture unitaire et de gestionnaire forte, mais aucune preuve d'intégration complète n'a été trouvée pour éditer la configuration via une passerelle réelle et observer le comportement `off`, `hot`, `restart` et `hybrid` de bout en bout.
- Les preuves d'archive montrent toujours une douleur opérationnelle orientée vers l'utilisateur autour de la remise de mise à jour de LaunchAgent, du comportement de mise à jour/redémarrage de systemd, des blocages de redémarrage/arrêt Windows, de la récupération de relais de crochet obsolète et de l'ambiguïté du rechargement à chaud.

Lacunes d'intégration :

- Aucun E2E en direct équivalent pour l'installation/démarrage/arrêt/redémarrage/statut de Linux `systemd --user` n'a été trouvé.
- Aucun E2E en direct équivalent pour l'installation/démarrage/arrêt/redémarrage/statut de Windows Scheduled Task n'a été trouvé.
- Aucun test de matrice de mode de rechargement complet en direct n'a été trouvé pour les éditions de configuration directes plus le comportement de redémarrage/application à chaud de la passerelle.

## Qualité

Score : **82**

Étiquette : **Élevée**

### Rapports gitcrawl

- La requête de problème ouvert `gitcrawl search issues "gateway restart lifecycle supervision" -R openclaw/openclaw --state open --json number,title,url,state --limit 10` a retourné 1 résultat : #74363, "Subagent runs can be falsely marked failed/lost after clean gateway close or pending wait".
- La requête de problème ouvert `gitcrawl search issues "gateway service launchd systemd schtasks install restart stop status" -R openclaw/openclaw --state open --json number,title,url,state --limit 10` a retourné 0 résultats.
- La requête de problème ouvert `gitcrawl search issues "gateway config reload hot restart hybrid" -R openclaw/openclaw --state open --json number,title,url,state --limit 10` a retourné 1 résultat : #43803, "[BUG] config.patch still sends SIGUSR1 for hot-reloadable paths (browser.profiles.\*), bypassing reload mode".
- La requête de problème ouvert `gitcrawl search issues "multiple gateways port config state workspace isolation" -R openclaw/openclaw --state open --json number,title,url,state --limit 10` a retourné 2 résultats : #71216, "Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`"; #64555, "[Bug]: WhatsApp credentials leak across `--profile` boundaries".
- La requête de problème fermé `gitcrawl search issues "gateway launchd restart handoff not loaded restart stop status" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10` a retourné #81894 et #85120 pour les défaillances de mise à jour/redémarrage de LaunchAgent macOS.
- La requête de problème fermé `gitcrawl search issues "gateway systemd service restart user unit linger XDG_RUNTIME_DIR" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10` a retourné #40275, #44417, #65184, #32635 et #36495 pour les régressions de statut/installation/redémarrage/détection de systemd.
- La requête de problème fermé `gitcrawl search issues "gateway schtasks Windows scheduled task restart stop port" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10` a retourné #69970, #52049, #72279, #52044 et #41047 pour les problèmes d'arrêt/redémarrage/contrôle de tâche planifiée Windows.
- La requête de problème fermé `gitcrawl search issues "gateway port precedence OPENCLAW_GATEWAY_PORT --port gateway.port service args" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10` a retourné 0 résultats.

### Rapports discrawl

- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway restart"` a retourné une discussion actuelle du responsable/utilisateur sur la récupération de relais de crochet natif obsolète nécessitant des sessions fraîches ou un redémarrage du serveur d'application Gateway/Codex, ainsi que des rapports de timeout VPS faible spécification et de lenteur de passerelle.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway service launchd"` a retourné des rapports de responsable/clawtributor sur v2026.5.12 laissant LaunchAgent macOS installé mais non chargé, les anciennes tâches launchd de mise à jour tuant les passerelles et la discussion PR autour du comportement `gateway stop` bootout.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway systemd"` a retourné des rapports sur les boucles de passerelle bêta sans réponse sur systemd, `openclaw update` arrêtant un service géré lors de l'échange d'installation global, la gestion des jetons systemd, les plans de redémarrage d'unité utilisateur systemd et les chutes de mémoire après un redémarrage propre de la passerelle.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway hot reload"` a retourné des rapports selon lesquels les modifications Discord/configuration peuvent se recharger à chaud, mais aussi des conseils du responsable selon lesquels certains paramètres nécessitent le prochain redémarrage/rechargement et la douleur de lecture de version autour du rechargement à chaud de la passerelle, du CPU, de la vivacité et des retombées de runtime-deps/plugin reload.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "multiple gateways"` a retourné le partage de documentation multi-passerelle, la discussion sur l'agent de sauvetage, les questions de topologie/cluster, les rapports d'exécution de plusieurs passerelles sur un hôte et le commentaire GitHub archivé sur les attentes d'isolation de répertoire d'état/profil.

### Bonnes qualités

- Les responsabilités du cycle de vie sont centralisées : les opérations du gestionnaire de service passent par `src/daemon/service.ts:250`, la politique de cycle de vie par `src/cli/daemon-cli/lifecycle-core.ts:374` et l'UX de commande par `src/cli/daemon-cli/register-service-commands.ts:56`.
- Le comportement du port et de la liaison a un assistant de configuration et un repli de métadonnées de commande de service, réduisant l'ambiguïté entre les démarrages au premier plan et supervisés (`src/config/paths.ts:262`, `src/cli/daemon-cli/lifecycle.ts:68`, `src/cli/daemon-cli/status.gather.ts:389`).
- La gestion du redémarrage est prudente : le redémarrage sécurisé supporte le report RPC, le drainage des exécutions actives, l'intention de force après expiration et le nettoyage des PID/écouteurs obsolètes (`src/cli/daemon-cli/lifecycle.ts:151`, `src/cli/gateway-cli/run-loop.ts:560`).
- Le rechargement de configuration échoue fermé sur les éditions directes invalides et sépare les modifications applicables à chaud des modifications nécessitant un redémarrage (`src/gateway/config-reload.ts:246`, `src/gateway/config-reload.ts:330`, `docs/gateway/configuration.md:547`).
- Le comportement du service spécifique à la plateforme est séparé en adaptateurs launchd, systemd et schtasks, gardant la construction de commande du système d'exploitation, l'analyse du statut et le comportement de récupération locaux à chaque limite de runtime.

### Mauvaises qualités

- Le comportement de l'opérateur multiplateforme est inégal car launchd, systemd et schtasks exposent des modes de défaillance et des chemins de récupération différents, ce qui rend les résultats de statut et de redémarrage plus difficiles à raisonner sur les systèmes d'exploitation.
- L'archive montre des régressions historiques répétées dans exactement cette famille : détection d'installation/statut de systemd, blocages d'arrêt/redémarrage Windows ou processus dupliqués et défaillances de remise de mise à jour de LaunchAgent.
- Le comportement de rechargement reste assez subtil pour que GitHub et Discord montrent une confusion ou des bogues autour du moment où le rechargement à chaud s'applique par rapport au moment où le redémarrage est requis.
- L'isolation multi-passerelle est documentée et implémentée autour des chemins, ports et espaces de travail par processus, mais les rapports de limite de profil/identifiant et les demandes de première classe `instances` montrent que les utilisateurs s'attendent à des affordances de topologie et de configuration plus fortes.

## Lacunes connues

- Contexte de capacité implémenté : démarrage au premier plan local, abstractions de service de plateforme, commandes de cycle de vie, redémarrage sécurisé, précédence port/liaison, modes de rechargement, isolation multi-passerelle, et couverture docs/dépannage de la passerelle sont tous présents dans les docs et sources cités.
- GitHub #71216 demande des ajouts de schéma de configuration incluant `instances`, suggérant une demande pour une configuration multi-passerelle/multi-instance plus de première classe.
- GitHub #64555 signale une fuite de credentials à travers les limites `--profile`, adjacente au contrat d'isolation multi-passerelle.
- Les recherches Discord `multiple gateways` montrent des utilisateurs posant des questions sur les agents de secours, les nœuds/passerelles multiples, le tunneling SSH vers plus d'une passerelle, et si plusieurs passerelles sont nécessaires.
- Les recherches Discord lifecycle montrent les responsables/utilisateurs ayant besoin d'une récupération plus claire pour les relais de hook obsolètes, la remise à jour automatique de LaunchAgent, la mise à jour/redémarrage systemd, et les attentes de rechargement/redémarrage à chaud.
- Aucune inadéquation directe source/docs n'a été trouvée pour le démarrage au premier plan cité, le cycle de vie du service, les modes de rechargement, ou la configuration multi-passerelle ; la demande `instances` est une lacune d'attente plutôt qu'un comportement documenté mais manquant dans les docs Gateway actuels.

## Preuves

### Docs

- `docs/gateway/index.md:25`: exemples de démarrage local au premier plan pour `openclaw gateway --port 18789`, `--verbose`, et `--force`.
- `docs/gateway/index.md:65`: le rechargement de config surveille le chemin de config actif et utilise par défaut `gateway.reload.mode="hybrid"`.
- `docs/gateway/index.md:71`: modèle d'exécution : un processus toujours actif, port multiplexé, loopback par défaut, authentification requise par défaut.
- `docs/gateway/index.md:111`: précédence port/bind et comportement des métadonnées du superviseur.
- `docs/gateway/index.md:126`: tableau des modes de rechargement pour `off`, `hot`, `restart`, et `hybrid`.
- `docs/gateway/index.md:152`: plusieurs passerelles sur un hôte nécessitent un port, une config, un état et un espace de travail isolés.
- `docs/gateway/configuration.md:534`: la passerelle surveille les modifications directes de config et rejette les modifications invalides/destructrices.
- `docs/gateway/configuration.md:550`: modes de rechargement et comportement de config applicable à chaud par rapport à celui nécessitant un redémarrage.
- `docs/cli/gateway.md:112`: variantes de redémarrage incluant redémarrage sûr, saut de report et force.
- `docs/cli/gateway.md:267`: sémantique de `gateway status`, `--probe`, et `--deep` pour les analyses launchd/systemd/schtasks.
- `docs/cli/gateway.md:496`: comportement d'installation/démarrage/arrêt/redémarrage du service et gestion des tokens/SecretRef.
- `docs/cli/daemon.md:13`: les commandes daemon héritées sont mappées aux commandes de service gateway sur launchd, systemd et schtasks.
- `docs/gateway/troubleshooting.md:424`: dépannage status/deep pour runtime arrêté, incompatibilité de config, conflits de port, services supplémentaires et métadonnées obsolètes.
- `docs/gateway/troubleshooting.md:547`: les modifications directes de config invalides conservent la config d'exécution active au lieu d'appliquer partiellement.

### Source

- `src/cli/gateway-cli/run-command.ts:10`: options de commande pour le démarrage local de la passerelle au premier plan.
- `src/cli/gateway-cli/run.ts:472`: chargement de config, analyse de port et sélection de port effectif.
- `src/cli/gateway-cli/run.ts:575`: validation de bind et nettoyage de PID obsolète en mode service.
- `src/cli/gateway-cli/run.ts:597`: `--force` tue les écouteurs existants et attend la capacité de liaison du port.
- `src/config/paths.ts:60`: remplacement de `OPENCLAW_STATE_DIR`.
- `src/config/paths.ts:154`: remplacement de config `OPENCLAW_CONFIG_PATH`.
- `src/config/paths.ts:262`: résolution du port de passerelle à partir de l'env, de la config, puis de la valeur par défaut.
- `src/daemon/service.ts:250`: registre de service macOS launchd, Linux systemd et Windows schtasks.
- `src/cli/daemon-cli/register-service-commands.ts:56`: enregistrement des commandes de cycle de vie du service.
- `src/cli/daemon-cli/install.ts:86`: l'installation résout le port de passerelle et bloque les configs de version future.
- `src/cli/daemon-cli/install.ts:220`: création du plan de service et installation.
- `src/cli/daemon-cli/lifecycle.ts:68`: résolution du port du cycle de vie à partir des args de commande de service, de l'env et de la config.
- `src/cli/daemon-cli/lifecycle.ts:151`: RPC de redémarrage sûr et gestion du report.
- `src/cli/daemon-cli/lifecycle.ts:253`: arrêt de secours pour le processus de passerelle non géré.
- `src/cli/daemon-cli/lifecycle.ts:275`: validation du redémarrage, récupération, gestion force/wait et contrôles de santé.
- `src/cli/daemon-cli/lifecycle-core.ts:374`: comportement d'arrêt principal.
- `src/cli/daemon-cli/lifecycle-core.ts:464`: comportement de redémarrage principal.
- `src/cli/daemon-cli/status.gather.ts:389`: résolution du port/probe de statut à partir des métadonnées de service et de la config.
- `src/gateway/server.impl.ts:1653`: le rechargeur de config géré démarre après que le serveur soit prêt.
- `src/gateway/config-reload.ts:86`: état du rechargeur de config géré et gestion du debounce.
- `src/gateway/config-reload.ts:246`: logique de décision du mode de rechargement.
- `src/gateway/config-reload.ts:330`: chemin d'application/promotion du snapshot en attente et gestion du snapshot invalide.
- `src/gateway/server-reload-handlers.ts:518`: les modifications de config nécessitant un redémarrage émettent une intention de redémarrage avec report de travail actif.
- `src/gateway/server-reload-handlers.ts:605`: les gestionnaires de rechargement gérés sont câblés uniquement pour l'état complet de la passerelle.
- `src/cli/gateway-cli/run-loop.ts:99`: la boucle d'exécution de la passerelle amorce le runtime du cycle de vie et gère le démarrage/redémarrage.
- `src/cli/gateway-cli/run-loop.ts:560`: le drain de redémarrage attend les tâches/exécutions actives ou abandonne de force en cas de timeout.

### Tests d'intégration

- `test/gateway.multi.e2e.test.ts:27`: démarre deux instances de passerelle et valide la livraison de hook HTTP par instance plus l'appairage de nœud WebSocket.
- `src/gateway/server-network-runtime.e2e.test.ts:68`: démarre un vrai serveur Gateway avec config/état temporaire et valide le comportement de requête directe.
- `src/cli/daemon-cli/install.integration.test.ts:39`: harnais d'intégration d'installation daemon avec home/state/config temporaire.
- `src/cli/daemon-cli/install.integration.test.ts:76`: l'installation échoue fermée quand le SecretRef de token requis n'est pas résolu.
- `src/cli/daemon-cli/install.integration.test.ts:110`: l'installation refuse les écritures de config de version future.
- `src/cli/daemon-cli/install.integration.test.ts:136`: l'installation génère automatiquement un token et ne l'intègre pas dans l'env du service.
- `src/daemon/launchd.integration.e2e.test.ts:177`: preuve réelle d'installation/redémarrage/KeepAlive/arrêt/démarrage/redémarrage du service launchd sur Darwin.

### Tests unitaires

- `src/gateway/config-reload.test.ts:507`: les paramètres de rechargement par défaut sont hybrid avec debounce de 300 ms.
- `src/gateway/config-reload.test.ts:688`: le rechargeur réessaie les snapshots manquants et recharge quand le fichier réapparaît.
- `src/gateway/config-reload.test.ts:934`: le rechargement à chaud rejeté ne promeut pas les modifications de config externes.
- `src/gateway/server-reload-handlers.test.ts:635`: les modifications de `gateway.port` nécessitant un redémarrage reportent pendant que le travail est actif.
- `src/gateway/server-reload-handlers.test.ts:722`: le timeout de report de redémarrage par défaut est de 300 secondes.
- `src/cli/gateway-cli/run-loop.test.ts:592`: l'intention de timeout de redémarrage saute un deuxième drain et abandonne les exécutions actives.
- `src/daemon/systemd.test.ts:153`: disponibilité de systemd et comportement de réparation de bus/secours.
- `src/daemon/systemd.test.ts:607`: comportement du chemin d'unité systemd spécifique au profil et personnalisé.
- `src/daemon/systemd.test.ts:780`: analyse de `EnvironmentFile` systemd et suivi de source.
- `src/daemon/schtasks.install.test.ts:85`: l'installation de tâche planifiée Windows cite/échappe les args/env de commande et les relit.
- `src/daemon/schtasks.install.test.ts:169`: l'installation de tâche planifiée Windows rejette les sauts de ligne dans les args/env/descriptions de commande.
- `src/daemon/schtasks.test.ts:75`: analyse du statut de tâche planifiée Windows pour en cours d'exécution/arrêté/inconnu.
- `src/daemon/schtasks.test.ts:140`: sélection du chemin de script de tâche Windows pour l'état par défaut/profil/personnalisé.
- `src/daemon/schtasks.stop.test.ts:110`: le nettoyage d'arrêt Windows tue les écouteurs de passerelle qui traînent et gère la suppression forcée.
- `src/cli/daemon-cli/status.gather.test.ts:428`: le statut deep réutilise l'environnement de commande de service et affiche les remises de redémarrage récentes.

### Requêtes gitcrawl

- `gitcrawl search issues "gateway restart lifecycle supervision" -R openclaw/openclaw --state open --json number,title,url,state --limit 10`
  - Résultat : `[{"number":74363,"state":"open","title":"Subagent runs can be falsely marked failed/lost after clean gateway close or pending wait","url":"https://github.com/openclaw/openclaw/issues/74363"}]`
- `gitcrawl search issues "gateway service launchd systemd schtasks install restart stop status" -R openclaw/openclaw --state open --json number,title,url,state --limit 10`
  - Résultat : `[]`
- `gitcrawl search issues "gateway config reload hot restart hybrid" -R openclaw/openclaw --state open --json number,title,url,state --limit 10`
  - Résultat : `[{"number":43803,"state":"open","title":"[BUG] config.patch still sends SIGUSR1 for hot-reloadable paths (browser.profiles.*), bypassing reload mode","url":"https://github.com/openclaw/openclaw/issues/43803"}]`
- `gitcrawl search issues "multiple gateways port config state workspace isolation" -R openclaw/openclaw --state open --json number,title,url,state --limit 10`
  - Résultat : #71216 problème ouvert « Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths` »; #64555 problème ouvert « [Bug]: WhatsApp credentials leak across `--profile` boundaries ».
- `gitcrawl search issues "gateway launchd restart handoff not loaded restart stop status" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10`
  - Résultat : #81894 problème fermé « v2026.5.12 agent-invoked self-update can leave macOS LaunchAgent unloaded or fail before package swap »; #85120 problème fermé « [Bug]: in-band `openclaw update` on macOS LaunchAgent can stop the gateway supervising it ».
- `gitcrawl search issues "gateway systemd service restart user unit linger XDG_RUNTIME_DIR" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10`
  - Résultat : #40275 problème fermé « [Bug]: openclaw gateway restart fails while user systemd service works via systemctl --user (service shown as disabled/stopped inconsistently) »; #44417 problème fermé « Bug: systemctl --user detection fails and hangs during `sudo -u` due to SUDO_USER fallback »; #65184 problème fermé « [Bug]: openclaw gateway install may fail with "Unit file openclaw-gateway.service does not exist" on migrated root + systemd --user installs »; #32635 problème fermé « Bug: gateway install fails on fresh Linux servers - execFileUtf8 clobbers systemctl stdout »; #36495 problème fermé « [Bug] Gateway install regression in 2026.3.2: `is-enabled` exit code `not-found` treated as "systemctl unavailable" ».
- `gitcrawl search issues "gateway schtasks Windows scheduled task restart stop port" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10`
  - Résultat : #69970 problème fermé « [Bug]: Windows auto-update restart script hangs indefinitely on `schtasks /End`, leaves zombie cmd.exe and flashing Terminal window »; #52049 problème fermé « Bug: gateway stop doesn't terminate node.exe process on Windows »; #72279 problème fermé « [Bug] [Windows] openclaw update still hangs with stuck findstr on 2026.4.24 - prior fixes (#57682, #44693, #27802, #41804) are incomplete »; #52044 problème fermé « Bug: gateway restart spawns duplicate processes on Windows (3 windows) »; #41047 problème fermé « [Bug]: OpenClaw Dashboard Control UI fails to send gateway token (token_missing) while gateway/runtime remain healthy ».
- `gitcrawl search issues "gateway port precedence OPENCLAW_GATEWAY_PORT --port gateway.port service args" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10`
  - Résultat : `[]`

### Requêtes discrawl

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway restart"`
  - Résultats :
    - `[maintainers] Molty, 2026-05-27T21:43:06Z`: la mise à jour des docs a dit que la solution de contournement `/new` est insuffisante si `Native hook relay unavailable` revient; redémarrer l'app-server Codex/OpenClaw Gateway.
    - `[users-helping-users] Rabid Neon, 2026-05-27T20:23:52Z`: `Native hook relay unavailable` récurrent après redémarrage; appairage gateway/native obsolète suspecté.
    - `[maintainers] 2026-05-27T18:13:58Z`: `Native hook relay unavailable` signifie config de hook retenue obsolète; la récupération est une nouvelle session ou redémarrage OpenClaw Gateway/Codex app-server.
    - `[maintainers] 2026-05-27T17:56:24Z`: même classe de relais de hook obsolète; la correction souhaitée est des IDs de relais stables par session et une réenregistrement à la reprise.
    - `[general] COOL, 2026-05-27T11:12:05Z`: passerelle marginalement plus lente, pas seulement un simple redémarrage de passerelle.
    - `[general] Peetiegonzalez, 2026-05-27T00:32:13Z`: timeout Codex intermittent bloqueur sur VPS bas de gamme.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway service launchd"`
  - Résultats :
    - `[clawtributors] BK, 2026-05-14T19:07:43Z`: la mise à jour automatique v2026.5.12 sur trois instances macOS LaunchAgent a laissé un paquet mis à jour avec LaunchAgent installé/non chargé et un toujours beta.8; la solution de contournement a utilisé SSH plus `gateway status --deep` et redémarrage.
    - `[clawtributors] BK, 2026-05-14T16:46:42Z`: le travail launchd `ai.openclaw.update.beta8` obsolète a tué à plusieurs reprises la passerelle; status/doctor n'a pas remarqué le travail de mise à jour frère.
    - `[clawtributors] Rizz, 2026-05-06T18:40:22Z`: PR #78412 corrige `gateway stop` bootout par défaut et kickstart inutile.
    - `[maintainers] Vincent K, 2026-04-30T09:28:42Z`: a demandé si la fonctionnalité aurait besoin de son propre agent launchd.
    - `[general] Yis, 2026-04-27T16:23:22Z`: la réinitialisation du cache de mise à niveau impliquait `gateway stop` et le comportement de launchd.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway systemd"`
  - Résultats :
    - `[clawtributors] Schwi, 2026-05-24T22:54:20Z`: boucle de passerelle 2026.5.24-beta.1 sans réponse sur systemd; la config de performance systemd a changé le comportement.
    - `[clawtributors] Schwi, 2026-05-24T19:39:55Z`: `openclaw update` a arrêté le service de passerelle géré, a échoué l'échange d'installation global, puis a redémarré le service systemd.
    - `[clawtributors] samzong, 2026-05-20T05:26:17Z`: PR #84408 a déplacé le token de passerelle node systemd hors des fichiers d'unité dans un fichier env mode-600.
    - `[clawtributors] JeffJHunter, 2026-05-18T20:31:23Z`: le plan de mise à jour a discuté du comportement d'arrêt/redémarrage de l'unité utilisateur systemd.
    - `[maintainers] brokemac79, 2026-05-18T20:18:53Z`: le redémarrage propre de la passerelle a considérablement réduit le RSS.
    - `[ct-helping] Julian Engel, 2026-05-09T07:01:24Z`: problème systemd pour l'utilisateur krill; la passerelle a fonctionné mais `gateway start` a échoué.
    - `[maintainers] 2026-05-05T20:07:35Z`: problème pressant listant le token de passerelle dans les unités daemon node Linux.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway hot reload"`
  - Résultats :
    - `[general] Pinched-Nerve, 2026-05-23T18:06:43Z`: les logs ont montré la détection du changement de config Discord, le redémarrage du canal et `config hot reload applied`.
    - `[maintainers] 2026-05-17T02:45:08Z`: le mainteneur a changé la config en direct mais a noté que l'effet peut attendre un redémarrage/rechargement s'il n'est pas rechargé à chaud.
    - `[general] 0xCyda, 2026-05-02T02:27:35Z`: la passerelle recharge à chaud la config des messages; redémarrage uniquement si la surveillance de fichier/rechargement est désactivé.
    - `[maintainers] 2026-05-01T16:15:25Z`: le mainteneur n'a pas redémarré la passerelle et a noté que les paramètres non-hot s'appliqueraient au prochain redémarrage/rechargement.
    - `[maintainers] Molty, 2026-05-01T00:12:06Z`: la lecture de version a listé le rechargement hot/CPU/liveness/event-loop delay et runtime-deps/plugin de la passerelle/fallout de boucle d'installation.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "multiple gateways"`
  - Résultats :
    - `[general] BK, 2026-05-15T00:37:18Z`: « Setup your rescue agent » avec lien docs `https://docs.openclaw.ai/gateway/multiple-gateways`.
    - `[users-helping-users] manjax, 2026-05-13T14:31:12Z`: a décrit une passerelle avec plusieurs nœuds et a demandé la flexibilité de passerelle multiple Kubernetes.
    - `[general] Hikaru, 2026-05-10T06:50:18Z`: a demandé pourquoi plusieurs passerelles sont nécessaires.
    - `[general] K, 2026-05-01T01:02:06Z`: exécution de plusieurs passerelles sur un hôte; a demandé si un tunnel SSH vers deux passerelles a causé des connexions perdues.
    - `[shell-society] disciplined, 2026-04-30T17:04:18Z`: a partagé le lien docs de passerelle multiple.
    - `[users-helping-users] Miky_The_Great, 2026-04-26T16:00:12Z`: voulait plusieurs agents/sous-agents; la solution impliquait deux passerelles et un bot Telegram séparé, que l'utilisateur voulait éviter.
