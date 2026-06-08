---
title: "Native Windows - Native Onboarding, Config, and Credential Setup Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Native Windows - Native Onboarding, Config, and Credential Setup Maturity Note

## Résumé

L'intégration native de Windows est implémentée via le flux de configuration CLI partagé, avec
des budgets de santé spécifiques à Windows et une messagerie de secours explicite pour les tâches planifiées.
La fonctionnalité est utilisable, mais elle est toujours assortie de mises en garde dans la documentation et
les preuves d'archive montrent que l'intégration Windows peut être lente ou confuse lorsque la santé de la passerelle,
le chargement du catalogue des fournisseurs ou le démarrage géré sont impliqués.

## Portée de la catégorie

- `openclaw onboard` et `openclaw onboard --non-interactive` sur Windows natif.
- Configuration locale de la passerelle, choix d'authentification, gestion des SecretRef de jeton/mot de passe de passerelle,
  écritures d'espace de travail/bootstrap et vérifications de santé.
- `--install-daemon`, `--skip-health` et conseils d'échec spécifiques à Windows.
- Séparation entre les conseils d'intégration Windows natif et WSL2.

## Fonctionnalités

- openclaw onboard: openclaw onboard et openclaw onboard --non-interactive sur Windows natif
- Configuration locale de la passerelle: Configuration locale de la passerelle, choix d'authentification, gestion des SecretRef de jeton/mot de passe de passerelle et valeurs par défaut des points de terminaison locaux.
- Indicateurs d'installation du démon: Indicateurs d'installation du démon pour l'intégration native de Windows.
- Limite de configuration native-vs-WSL: Limite de configuration entre la passerelle Windows native et le chemin WSL2 recommandé.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score: `Beta (72%)`
- Signaux positifs: la documentation et le code source d'intégration couvrent la configuration interactive et
  non-interactive; les constantes de synchronisation spécifiques à Windows et les indices de démarrage géré existent; les tests couvrent
  la santé de la passerelle non-interactive et le comportement d'installation du démon.
- Signaux négatifs: l'intégration native de Windows est toujours documentée avec des mises en garde,
  et la piste de preuve en environnement réel n'est pas aussi large que pour macOS/Linux.
- Lacunes d'intégration: aucun scénario Windows natif en direct n'a été trouvé pour
  script d'installation -> intégration -> installation du démon -> santé de la passerelle -> authentification du fournisseur -> premier tour d'agent.

## Score de qualité

- Score: `Alpha (66%)`
- Rapports Gitcrawl: `Windows onboarding` a retourné le problème #82594 pour un chargement de modèle extrêmement
  lent sur Windows lors de l'intégration et d'autres rapports de configuration Windows.
- Rapports Discrawl: les résumés Windows natifs mentionnent la stabilisation de l'intégration,
  des budgets de santé de passerelle Windows plus longs et une confusion de support entre les commandes PowerShell natives et WSL2.
- Bonnes qualités: la configuration non-interactive échoue fermée pour les références d'authentification de passerelle non résolues,
  a des budgets de santé spécifiques à Windows et dit explicitement aux utilisateurs Windows quand le démarrage géré
  utilise les tâches planifiées ou le secours du dossier de démarrage.
- Mauvaises qualités: le chemin de configuration est toujours facile à exécuter dans le mauvais environnement,
  et la latence de découverte du fournisseur/modèle peut faire que l'intégration Windows semble cassée.
- Exclu de la qualité: les preuves de test unitaire, intégration, e2e, en direct et flux d'exécution
  sont enregistrées uniquement sous Couverture et Preuves.

## Score de complétude

- Score: `Beta (72%)`
- Instructions de surface: évaluées par rapport à `references/completeness/native-windows-cli-and-gateway.md`.
- Signaux positifs: les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour openclaw onboard,
  configuration locale de la passerelle, indicateurs d'installation du démon, limite de configuration native-vs-WSL.
- Signaux négatifs: la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score
  est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes: voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées
  et les mises en garde visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve de scénario d'intégration Windows natif pour les chemins `--install-daemon` et
  CLI uniquement `--skip-health`.
- Ajouter une documentation plus nette pour choisir PowerShell natif par rapport à WSL2 avant que l'utilisateur
  n'exécute les commandes d'installation/intégration.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/cli/onboard.md:81` documente
  la configuration du fournisseur personnalisé non-interactive.
- `/Users/kevinlin/code/openclaw/docs/cli/onboard.md:138` documente les options de jeton de passerelle
  et le comportement de SecretRef en mode non-interactive.
- `/Users/kevinlin/code/openclaw/docs/cli/onboard.md:164` indique que
  la configuration locale non-interactive attend une passerelle locale accessible sauf si
  `--skip-health` est passé.
- `/Users/kevinlin/code/openclaw/docs/cli/onboard.md:170` documente le secours
  de démarrage géré Windows natif.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:37` énumère les mises en garde
  d'intégration native.

### Source

- `/Users/kevinlin/code/openclaw/src/cli/program/register.onboard.ts:91`
  enregistre la commande `openclaw onboard` et les indicateurs.
- `/Users/kevinlin/code/openclaw/src/cli/program/register.onboard.ts:148`
  enregistre les indicateurs de port/liaison/authentification de la passerelle.
- `/Users/kevinlin/code/openclaw/src/commands/onboard-non-interactive/local.ts:33`
  définit des budgets de santé du démon Windows plus longs.
- `/Users/kevinlin/code/openclaw/src/commands/onboard-non-interactive/local.ts:262`
  invoque l'installation du démon non-interactive.
- `/Users/kevinlin/code/openclaw/src/commands/onboard-non-interactive/local.ts:355`
  émet des conseils de démarrage géré spécifiques à Windows lorsque la santé échoue.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/onboard-docker.sh` exerce le
  chemin d'intégration partagé dans Docker.
- `/Users/kevinlin/code/openclaw/scripts/e2e/release-typed-onboarding-docker.sh`
  couvre les scénarios d'intégration de version.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-windows-smoke.sh:1`
  distribue la voie de fumée Windows native.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/onboard-non-interactive.gateway.test.ts`
  couvre la configuration de passerelle non-interactive, la santé et les simulations d'installation du démon.
- `/Users/kevinlin/code/openclaw/src/commands/onboard-auth.config-shared.test.ts`
  couvre le comportement de configuration d'authentification d'intégration.
- `/Users/kevinlin/code/openclaw/src/commands/onboard-non-interactive.gateway-health-auth.test.ts`
  couvre la gestion de l'authentification de santé de la passerelle.
- `/Users/kevinlin/code/openclaw/src/cli/program/register.onboard.test.ts`
  couvre l'enregistrement des indicateurs CLI y compris les indicateurs d'installation du démon.

### Requêtes Gitcrawl

Requête:

- `gitcrawl search openclaw/openclaw --query "native Windows onboarding install-daemon skip-health gateway health" --mode keyword --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "Windows onboarding" --mode keyword --limit 5 --json`

Résultats:

- La requête d'intégration native étroite a retourné 0 résultats.
- `Windows onboarding` a retourné le problème #82594 pour un chargement de modèle Windows lent
  lors de l'intégration, plus le signal de problème et PR lié à la configuration.

### Requêtes Discrawl

Requête:

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "native Windows onboarding install-daemon skip-health gateway health"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "install.ps1 Windows PowerShell installer"`

Résultats:

- La requête d'intégration native étroite n'a retourné aucun résultat direct.
- La requête d'installation a retourné des résumés de mainteneur selon lesquels l'intégration Windows native
  avait un travail de stabilisation, des indicateurs de progression de démarrage et des budgets de santé de passerelle plus longs
  car le démarrage Windows est plus lent/bruyant que Linux.
