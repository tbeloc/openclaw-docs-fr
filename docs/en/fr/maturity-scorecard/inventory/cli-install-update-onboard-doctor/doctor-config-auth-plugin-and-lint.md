---
title: CLI - Doctor Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# CLI - Doctor Maturity Note

## Résumé

`openclaw doctor` couvre la logique de réparation de la configuration, de l'authentification, des plugins, du lint et de la plateforme/service avec une large couverture de tests. La couverture est globalement solide. La qualité reste en dessous de stable car la validation des plugins/schémas et les flux de réparation de services multi-plateformes produisent toujours des lacunes et des bugs visibles par les opérateurs.

## Portée de la catégorie

Cette catégorie couvre le comportement du doctor pour la migration de configuration, les vérifications d'authentification, la gestion des SecretRef, la validation et la réparation des plugins, la sortie de lint lisible par machine, la découverte de services supplémentaires, la réparation de la dérive du superviseur, les vérifications des chemins d'exécution et les conseils de redémarrage.

## Fonctionnalités

- Réparation interactive : openclaw doctor supporte les postures d'inspection, de réparation, non-interactive et de réparation forcée.
- Migration de configuration : Doctor réécrit la configuration héritée ou endommagée et l'état dans les formats actuels supportés.
- Vérifications d'authentification et de SecretRef : Doctor audite la forme de l'authentification, la génération de tokens et les chemins de configuration supportés par SecretRef.
- Validation et réparation des plugins : Doctor met en évidence les problèmes de configuration des plugins et la dérive de schéma d'extension qui bloquent le fonctionnement normal du runtime.
- Lint et résultats JSON : openclaw doctor --lint --json fournit des résultats stables lisibles par machine pour l'automatisation.
- Découverte de passerelle supplémentaire : Doctor peut scanner les services de passerelle inattendus et les installations conflictuelles.
- Réparation de la dérive du superviseur : Doctor vérifie les définitions de service gérées et peut réparer la dérive de launchd, systemd ou Scheduled Task.
- Diagnostic de port et de démarrage : Doctor pointe les opérateurs vers les conflits de port, les échecs de redémarrage et les erreurs récentes de passerelle.
- Vérifications des chemins d'exécution : Doctor vérifie les bonnes pratiques des chemins d'exécution et les erreurs de configuration de chemin courantes.
- Conseils de redémarrage : Doctor explique quand un problème de santé nécessite un redémarrage ou un chemin de réparation de service plus profond.

## Fraîcheur de l'archive

- gitcrawl : `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`, `api_supported=false`, `github_token_present=false`.
- discrawl : `generated_at=2026-05-30T01:10:41Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs :
  - `docs/cli/doctor.md`, `docs/gateway/doctor.md`, `docs/gateway/secrets.md` et `docs/gateway/troubleshooting.md` documentent le modèle de réparation, le mode lint, les attentes de SecretRef et les chemins de dépannage de la dérive de service.
  - L'implémentation du doctor est décomposée entre les modules de configuration, authentification, état, plugin, lint, gateway-service et platform-note sous `src/commands/doctor*.ts`.
  - La logique de réparation de configuration et d'authentification a une couverture de test large, incluant les migrations héritées et le comportement non-interactif.
  - Doctor a également une couverture de réparation de service sur la dérive de port, la dérive de token, les avertissements de source-checkout et les chemins de politique externe.
  - Des tests de style E2E du doctor existent pour les répertoires d'état manquants, les migrations d'état héritées et les scénarios d'avertissement de sandbox.
- Signaux négatifs :
  - La commande a un mandat très large, ce qui augmente la chance de cas limites non gérés.
  - Certaines ruptures de runtime liées aux plugins nécessitent toujours une inspection manuelle des logs.
  - La réparation de service multi-utilisateur et multi-plateforme dépend toujours fortement de la couverture de test plutôt que de preuves en direct largement diffusées.
- Lacunes d'intégration :
  - Aucune preuve de bout en bout n'a été trouvée validant chaque schéma de plugin/outil actif par rapport au chemin de projection de runtime exact avant les tours d'utilisateur.
  - Aucune suite d'intégration de réparation systemd ou Windows en direct correspondant à la profondeur macOS/launchd n'a été trouvée.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports de Gitcrawl :
  - La requête `gitcrawl search issues "doctor config plugin SecretRef lint" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné `[]`.
  - La requête `gitcrawl search issues "doctor gateway service repair port" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné des problèmes ouverts incluant `#76707 doctor --fix can repair the wrong Unix home when live gateway runs under another user`, `#87156 Windows doctor update leaves Startup-folder gateway fallback stale and does not install Scheduled Task` et `#85027 2026.5.6 → 2026.5.19 upgrade left macOS LaunchAgent Gateway unrecoverable`.
- Rapports de Discrawl :
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw doctor config plugin"` a mis en évidence un rapport d'utilisateur où un schéma d'outil dynamique non supporté a empoisonné le démarrage de l'assistant tandis que `openclaw doctor` n'a pas signalé le problème racine.
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "doctor gateway service repair"` a retourné des conseils de test bêta mettant l'accent sur la robustesse de la mise à jour/doctor et la validation du statut de redémarrage, ce qui indique que cela reste une surface de risque opérationnel actif.
- Bonnes qualités :
  - Doctor a des modes explicites de lecture seule, réparation et lint lisible par machine.
  - Les migrations de configuration et d'authentification héritées sont couvertes directement dans les tests.
  - L'authentification gérée par SecretRef et la gestion des tokens sont traitées comme de première classe.
  - La logique de dérive de service a des tests dédiés pour plusieurs classes d'échec réelles.
  - Les docs pointent les opérateurs vers des commandes concrètes de redémarrage et réinstallation.
- Mauvaises qualités :
  - Les ruptures de runtime/schéma des plugins peuvent toujours échapper au passage initial du doctor.
  - Certains échecs de validation de plugin produisent toujours des conseils aux opérateurs qui sont moins directs qu'ils ne devraient l'être.
  - Les bugs actifs couvrent les chemins exacts multi-utilisateur et de secours Windows que la réparation de service du doctor possède.
  - La réparation de mise à niveau peut toujours laisser les passerelles irrécupérables sur certaines plateformes.
- Exclus de la qualité :
  - La couverture de test du doctor ci-dessous est comptée uniquement vers la couverture.

## Lacunes connues

- La validation du schéma d'outil de runtime n'est pas aussi complète que le chemin de l'assistant en direct le nécessite.
- La validation du manifeste et du schéma des plugins manque toujours certaines ruptures de runtime avant la première utilisation.
- Le comportement de réparation multi-utilisateur sur Unix est toujours sujet aux bugs.
- La réparation de secours Windows Scheduled Task reste un territoire de bug actif.
- La preuve de réparation de plateforme en direct est mince en dehors des harnais de test existants.

## Preuves

### Docs

- `docs/cli/doctor.md`
- `docs/gateway/doctor.md`
- `docs/gateway/secrets.md`
- `docs/gateway/troubleshooting.md`

### Source

- `src/commands/doctor.ts`
- `src/commands/doctor-config-flow.ts`
- `src/commands/doctor-auth.ts`
- `src/commands/doctor-lint.ts`
- `src/commands/doctor-gateway-services.ts`
- `src/commands/doctor-service-repair-policy.ts`
- `src/commands/doctor-platform-notes.ts`
- `src/daemon/service-audit.ts`
- `src/config/validation.ts`

### Tests d'intégration

- `src/commands/doctor.warns-state-directory-is-missing.e2e.test.ts`
- `src/commands/doctor.runs-legacy-state-migrations-yes-mode-without.e2e.test.ts`
- `src/commands/doctor.warns-per-agent-sandbox-docker-browser-prune.e2e.test.ts`

### Tests unitaires

- `src/commands/doctor-config-flow.test.ts`
- `src/commands/doctor-auth.deprecated-cli-profiles.test.ts`
- `src/commands/doctor-auth-flat-profiles.test.ts`
- `src/commands/doctor-lint.test.ts`
- `src/commands/doctor-plugin-manifests.test.ts`
- `src/commands/doctor-gateway-services.test.ts`
- `src/commands/doctor-platform-notes.launchctl-env-overrides.test.ts`
- `src/commands/doctor-platform-notes.startup-optimization.test.ts`
- `src/daemon/service-audit.test.ts`

### Commandes de validation de surface

- `none declared in taxonomy` : `pass` - La surface CLI ne déclare pas de commandes de validation supplémentaires pour la notation.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "doctor config plugin SecretRef lint" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`
- `gitcrawl search issues "doctor gateway service repair port" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`

Résultats :

- `[]`
- `[{"number":76707,"state":"open","title":"[UX]: doctor --fix can repair the wrong Unix home when live gateway runs under another user","url":"https://github.com/openclaw/openclaw/issues/76707"},{"number":87156,"state":"open","title":"[Bug]: Windows doctor update leaves Startup-folder gateway fallback stale and does not install Scheduled Task","url":"https://github.com/openclaw/openclaw/issues/87156"},{"number":75502,"state":"open","title":"Downgrading from 2026.4.29 to 2026.4.27 fails due to stale file-transfer entry in ~/.openclaw/plugins/installs.json","url":"https://github.com/openclaw/openclaw/issues/75502"},{"number":85027,"state":"open","title":"[Bug] 2026.5.6 → 2026.5.19 upgrade left macOS LaunchAgent Gateway unrecoverable; Time Machine restore required","url":"https://github.com/openclaw/openclaw/issues/85027"},{"number":52184,"state":"open","title":"[Feature]: Prefer Volta shim path over version-pinned Volta node path for macOS gateway LaunchAgent","url":"https://github.com/openclaw/openclaw/issues/52184"}]`

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw doctor config plugin"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "doctor gateway service repair"`

Résultats :

- La discussion d'archive incluait un rapport réel où un schéma d'extension cassé a causé un échec de démarrage de l'assistant sans que le doctor ne détecte le problème en premier.
- Les conseils de test de version de l'archive traitent toujours la validation doctor-plus-redémarrage comme une vérification bêta critique, ce qui correspond à la pression des problèmes ouverts sur cette catégorie.
