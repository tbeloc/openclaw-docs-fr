---
title: "Chemin d'installation Nix - Mise à jour de la configuration Doctor et note de maturité des gardes de mutation du service Daemon"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Mise à jour de la configuration Doctor et note de maturité des gardes de mutation du service Daemon

## Résumé

OpenClaw dispose de garde-fous explicites pour plusieurs commandes à haut risque d'auto-mutation en mode Nix : la documentation de configuration avertit les utilisateurs, la génération de jetons de réparation du doctor est bloquée, l'installation/désinstallation du service daemon est désactivée, et les vérifications de mise à jour de la passerelle sont ignorées. L'écart de maturité principal est que les preuves sont dispersées dans les tests de commandes et les branches source plutôt que d'être exercées comme un seul flux d'installation Nix réel.

## Portée de la catégorie

Cette catégorie couvre `openclaw setup`, les modes réparation/jeton de `openclaw doctor`, le comportement `openclaw update`/mise à jour automatique au démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.

## Fonctionnalités

- Refus d'écriture de configuration : Couvre le refus d'écriture de configuration dans `openclaw setup`, les modes réparation/jeton de `openclaw doctor`, le comportement `openclaw update`/mise à jour automatique au démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Refus de réparation du doctor : Couvre le refus de réparation du doctor dans `openclaw setup`, les modes réparation/jeton de `openclaw doctor`, le comportement `openclaw update`/mise à jour automatique au démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Transfert de mise à jour : Couvre le transfert de mise à jour dans `openclaw setup`, les modes réparation/jeton de `openclaw doctor`, le comportement `openclaw update`/mise à jour automatique au démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Transfert du cycle de vie du service : Couvre le transfert du cycle de vie du service dans `openclaw setup`, les modes réparation/jeton de `openclaw doctor`, le comportement `openclaw update`/mise à jour automatique au démarrage, et le comportement d'installation/désinstallation du service daemon en mode Nix.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (40%)`
- Signaux positifs : La génération de jetons/réparation du doctor dispose d'une couverture de régression ciblée, l'installation du service daemon a un comportement d'abandon en mode Nix, et les vérifications de mise à jour au démarrage reviennent tôt en mode Nix.
- Signaux négatifs : La couverture des gardes est distribuée par commande et ne prouve pas un flux de travail d'opérateur complet en mode Nix.
- Lacunes d'intégration : Aucun e2e de service launchd/systemd local n'a prouvé que le cycle de vie du service géré par Nix est délégué à Nix plutôt qu'aux mutateurs OpenClaw.

## Score de qualité

- Score : `Expérimental (49%)`
- Rapports Gitcrawl : `doctor Nix mode` a retourné la PR ouverte `#79734` sur le dry-run du doctor en mode Nix et la PR `#82032` sur les internals de configuration, montrant que le domaine est toujours actif.
- Rapports Discrawl : Un message du responsable de mai 2026 a explicitement déclaré que le bug du doctor semblait plus étroit que le correctif de limite de politique générale et devrait être suivi séparément.
- Bonnes qualités : Les messages de commande sont directs, et les chemins d'installation/désinstallation de service à haut risque échouent fermés en mode Nix.
- Mauvaises qualités : Doctor reste large, et le contexte d'archive montre que les responsables s'inquiètent toujours des chemins de réparation qui pourraient muter alors qu'ils ne devraient que rapporter.
- Exclus de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Expérimental (40%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le refus d'écriture de configuration, le refus de réparation du doctor, le transfert de mise à jour, le transfert du cycle de vie du service.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun scénario unique ne démarre une passerelle Nix et ne valide la configuration, le doctor, la mise à jour et la sémantique du cycle de vie du service ensemble.
- Le comportement du dry-run du doctor est toujours discuté dans le contexte GitHub ouvert.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/cli/setup.md:15` documente que la configuration refuse les écritures en mode Nix.
- `/Users/kevinlin/code/openclaw/docs/cli/doctor.md:190` dit que les vérifications du doctor en lecture seule fonctionnent mais `doctor --fix`, `--repair`, `--yes`, et `--generate-gateway-token` sont désactivés en mode Nix.
- `/Users/kevinlin/code/openclaw/docs/install/nix.md:70` énumère la mise à jour mutante, la génération de jetons/réparation du doctor, et les rédacteurs de configuration/onboarding/setup comme désactivés contre la configuration immuable.

### Source

- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/shared.ts:37` échoue l'installation du service avec `Nix mode detected; service install is disabled.`
- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/lifecycle-core.ts:194` échoue la désinstallation du service avec `Nix mode detected; service uninstall is disabled.`
- `/Users/kevinlin/code/openclaw/src/commands/uninstall.ts:57` à `:59` désactive la désinstallation du service et dit aux utilisateurs de gérer le service via leur profil Nix.
- `/Users/kevinlin/code/openclaw/src/infra/update-startup.ts:305` à `:318` revient tôt des vérifications de mise à jour de la passerelle quand `isNixMode` est vrai.
- `/Users/kevinlin/code/openclaw/src/flows/doctor-health.ts:13` appelle `assertConfigWriteAllowedInCurrentMode`.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/doctor.runs-legacy-state-migrations-yes-mode-without.e2e.test.ts:67` à `:79` vérifie que le mode réparation du doctor refuse en mode Nix avant les effets secondaires de réparation.
- `/Users/kevinlin/code/openclaw/src/commands/doctor.runs-legacy-state-migrations-yes-mode-without.e2e.test.ts:86` à `:98` vérifie que la génération de jeton de passerelle refuse en mode Nix.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/install.test.ts:154` à `:158` vérifie la messagerie d'échec du mode Nix de l'installation daemon.
- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/lifecycle-core.config-guard.test.ts:19` couvre le contexte de garde du cycle de vie daemon.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "doctor Nix mode" --json`

Résultats :

- A retourné la PR `#79734` sur le `--dry-run` du doctor et la compatibilité du mode Nix.
- A retourné la PR `#82032` sur les internals de configuration et les diagnostics de validation.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "doctor Nix mode"`

Résultats :

- `maintainers` le 2026-05-06 a dit que la PR `#78047` a corrigé la politique d'écriture de configuration automatique/d'exécution, mais un problème de doctor devrait toujours être suivi séparément.
- Un rapport d'utilisateur de janvier a mentionné `moltbot doctor --non-interactive` sur une installation Nix, montrant que le doctor fait partie du dépannage réel de l'opérateur Nix.
