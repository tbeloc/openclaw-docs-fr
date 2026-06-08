---
title: CLI - Note de maturité de la gestion du service Gateway
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# CLI - Note de maturité de la gestion du service Gateway

## Résumé

L'interface CLI expose une large surface de passerelle gérée pour l'exécution, l'installation, le statut,
le démarrage, l'arrêt, le redémarrage, le redémarrage sécurisé et les conseils de réparation de service sur launchd,
systemd et Windows Scheduled Tasks. La couverture est forte car les adaptateurs de commande et
de plateforme sont larges et il existe une preuve réelle d'intégration launchd ; la qualité
est matériellement inférieure car le cycle de vie du service reste un point de douleur récurrent pour les opérateurs, en particulier sur systemd Linux et les redémarrages entre versions.

## Portée de la catégorie

Cette catégorie couvre les exécutions de passerelle au premier plan et l'installation et le contrôle du cycle de vie de la passerelle supervisée. Elle ne couvre pas les choix d'intégration de haut niveau ni le flux de diagnostic qui répare la dérive de service après coup.

## Fonctionnalités

- Exécutions de passerelle au premier plan : Les opérateurs peuvent exécuter la passerelle directement depuis l'interface CLI pour le développement local ou la récupération ad hoc.
- Installation et contrôle du service : L'interface CLI documente les flux d'installation, de statut, de démarrage, d'arrêt, de redémarrage et d'exécution pour les services de passerelle gérés.
- Câblage d'authentification du service : L'installation du service de passerelle documente comment les jetons d'authentification et autres valeurs sensibles sont traités.
- Récupération de dérive et de réinstallation : Les opérateurs reçoivent des conseils explicites pour réparer ou réinstaller un service de passerelle géré cassé.
- Vérifications de santé du service : Les flux de service de passerelle orientent les opérateurs vers les vérifications de santé et de dépannage à l'exécution après l'installation ou le redémarrage.

## Fraîcheur de l'archive

- gitcrawl: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`, `api_supported=false`, `github_token_present=false`.
- discrawl: `generated_at=2026-05-30T01:10:41Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Score de couverture

- Score : `Stable (88%)`
- Signaux positifs :
  - `docs/cli/gateway.md`, `docs/gateway/troubleshooting.md` et `docs/install/updating.md` documentent les flux d'exécution, d'installation, de redémarrage, d'arrêt, de statut et de récupération supervisée.
  - L'implémentation de la commande de cycle de vie s'étend sur `src/cli/gateway-cli/run.ts`, `src/cli/gateway-cli/run-loop.ts`, `src/cli/daemon-cli/shared.ts` et les adaptateurs de plateforme sous `src/daemon/`.
  - Des implémentations de service spécifiques à la plateforme existent pour launchd, systemd et schtasks dans `src/daemon/launchd.ts`, `src/daemon/systemd.ts` et `src/daemon/schtasks.ts`.
  - Une preuve d'intégration réelle existe dans `src/daemon/launchd.integration.e2e.test.ts`.
- Signaux négatifs :
  - La preuve multiplateforme est inégale, avec launchd macOS mieux couvert que les flux systemd ou Windows en direct.
  - Le cycle de vie du service reste sensible à la remise de redémarrage, aux unités obsolètes et au comportement du wrapper/processus.
- Lacunes d'intégration :
  - Aucune suite d'intégration systemd en direct ou Windows scheduled-task équivalente correspondant à la profondeur de launchd n'a été trouvée.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl search issues "gateway install restart status start stop" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné des problèmes ouverts incluant `#81410 Gateway lifecycle commands target stale SUDO_USER scope from root shell instead of root systemd user service`, `#83360 auto-update can never succeed under systemd`, `#83354 helper commands can silently resurrect stopped user-level units`, `#79375 stale user-level systemd unit dueling services` et `#79534 Gateway wrapper child survives SIGTERM and blocks systemd restarts`.
- Rapports Discrawl :
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "gateway install restart status stop"` a retourné l'accent du test bêta 2026.5.16 appelant le redémarrage géré et les avertissements de wrapper obsolète, plus la discussion des opérateurs autour du comportement de redémarrage/mise à jour.
- Bonnes qualités :
  - Les responsabilités du cycle de vie sont centralisées dans des modules CLI et daemon dédiés.
  - La documentation est explicite sur le comportement de redémarrage sécurisé par rapport au redémarrage forcé.
  - Il existe une couverture d'intégration launchd réelle au lieu de simulations uniquement.
- Mauvaises qualités :
  - Les problèmes ouverts montrent que la sémantique du cycle de vie systemd et du redémarrage régressent toujours.
  - Les interactions de redémarrage/mise à jour restent particulièrement fragiles sous les services gérés.
  - Le comportement multiplateforme est difficile à rendre uniforme.
- Exclu de la qualité :
  - `src/daemon/launchd.integration.e2e.test.ts` et les suites unitaires ci-dessous comptent vers la couverture, pas la qualité.

## Lacunes connues

- La preuve du cycle de vie systemd et Windows en direct traîne launchd macOS.
- La remise de redémarrage et la récupération d'unité obsolète sont toujours des zones de risque actives pour les opérateurs.

## Preuves

### Documentation

- `docs/cli/gateway.md`
- `docs/gateway/troubleshooting.md`
- `docs/install/updating.md`

### Source

- `src/cli/gateway-cli/run.ts`
- `src/cli/gateway-cli/run-loop.ts`
- `src/cli/daemon-cli/shared.ts`
- `src/daemon/launchd.ts`
- `src/daemon/systemd.ts`
- `src/daemon/schtasks.ts`

### Tests d'intégration

- `src/daemon/launchd.integration.e2e.test.ts`

### Tests unitaires

- `src/cli/daemon-cli/status.gather.test.ts`
- `src/cli/daemon-cli/status.print.test.ts`
- `src/daemon/service-audit.test.ts`
- `src/daemon/schtasks.install.test.ts`
- `src/daemon/schtasks.stop.test.ts`

### Commandes de validation de surface

- `none declared in taxonomy`: `pass` - La surface CLI ne déclare pas de commandes de validation supplémentaires pour la notation.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "gateway install restart status start stop" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`

Résultats :

- `[{"number":81410,"state":"open","title":"Gateway lifecycle commands target stale SUDO_USER scope from root shell instead of root systemd user service","url":"https://github.com/openclaw/openclaw/issues/81410"},{"number":83360,"state":"open","title":"[Bug]: auto-update can never succeed under systemd — updater is spawned as a child of the gateway it needs to restart","url":"https://github.com/openclaw/openclaw/issues/83360"},{"number":83354,"state":"open","title":"Helper commands can silently resurrect stopped user-level openclaw-gateway units","url":"https://github.com/openclaw/openclaw/issues/83354"},{"number":79375,"state":"open","title":"Upgrade leaves stale user-level systemd unit, dueling services kill each other on Linux","url":"https://github.com/openclaw/openclaw/issues/79375"},{"number":79534,"state":"open","title":"Gateway wrapper's spawned child process can survive parent SIGTERM, blocking systemd restarts on EADDRINUSE","url":"https://github.com/openclaw/openclaw/issues/79534"}]`

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "gateway install restart status stop"`

Résultats :

- Les conseils de test de version appellent explicitement le redémarrage géré, `openclaw update status`, la réouverture du tableau de bord et les avertissements de wrapper obsolète comme zones à vérifier, ce qui correspond à la pression de problème ouvert sur cette surface.
