---
title: "Windows via WSL2 - Diagnostics and Repair Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - Diagnostics and Repair Maturity Note

## Résumé

Les diagnostics et réparations sont largement implémentés via la pile Linux/systemd Gateway : l'état de surface des services et l'état d'exécution de la passerelle, les journaux peuvent revenir aux journaux systemd actifs, et le docteur possède la réparation des services, les diagnostics SecretRef et les vérifications de systemd linger. La qualité spécifique à WSL2 reste Beta car les preuves d'archive actuelles montrent des faux négatifs de sonde de service, une confusion utilisateur-bus et une PR de diagnostics d'environnement WSL ouverte.

## Portée de la catégorie

Inclus dans cette catégorie :

- openclaw doctor : openclaw doctor et réparation/migration pour WSL2 Gateway
- openclaw status : openclaw status, status --all, et résumé du service/runtime Gateway
- openclaw logs : openclaw logs et secours du journal systemd Linux
- SecretRef : SecretRef et diagnostics d'authentification visibles depuis status/doctor
- Indices WSL/systemd indisponibles : indices WSL/systemd indisponibles et vérifications de linger
- Guidance de réparation opérateur après WSL2 service : Guidance de réparation opérateur après WSL2 service, config, ou défaillances Gateway

## Fonctionnalités

- openclaw doctor : openclaw doctor et réparation/migration pour WSL2 Gateway
- openclaw status : openclaw status, status --all, et résumé du service/runtime Gateway
- openclaw logs : openclaw logs et secours du journal systemd Linux
- SecretRef : SecretRef et diagnostics d'authentification visibles depuis status/doctor
- Indices WSL/systemd indisponibles : indices WSL/systemd indisponibles et vérifications de linger
- Guidance de réparation opérateur après WSL2 service : Guidance de réparation opérateur après WSL2 service, config, ou défaillances Gateway

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : les docs pointent la réparation WSL2 vers `openclaw doctor` ; les docs de status incluent le runtime du service Gateway et du nœud hôte ; les docs de logs incluent le secours du journal systemd ; la source/les tests couvrent les indices systemd indisponibles, status, logs fallback, et le comportement de réparation de service.
- Signaux négatifs : les diagnostics spécifiques à WSL2 sont encore en émergence et s'appuient actuellement sur des vérifications Linux/service générales plus l'interprétation de l'opérateur.
- Lacunes d'intégration : aucun e2e de diagnostics spécifique à WSL2 n'a été trouvé pour la défaillance du user-bus systemd, le portproxy obsolète, la réachabilité de l'interface utilisateur de contrôle Windows-host, et la réparation du service Gateway dans un scénario.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : `Windows WSL2 gateway systemd` a retourné la PR #58853 pour les diagnostics WSL, la PR #68400 pour la détection du socket D-Bus utilisateur WSL, le problème #55563 pour le cyclage de passerelle induit par le docteur, et le problème #84610 pour les lacunes de boucle/diagnostic WSL2. `WSL2 doctor logs update Gateway` a retourné 0 résultats.
- Rapports Discrawl : la recherche WSL2 systemd/diagnostics a retourné le rapport de sonde de service `No medium found`, les sorties de status où le service systemd est en cours d'exécution mais la passerelle est inaccessible, et les conseils de support pour exécuter `openclaw status --deep`, inspecter les processus, et séparer les installations Windows natives des installations WSL2.
- Bonnes qualités : la surface de diagnostics est large et soutenue par la source ; les logs rédactent les secrets lors de la lecture du journal systemd ; status rapporte les diagnostics de mise à jour, service, passerelle, sécurité et secret.
- Mauvaises qualités : les causes racines spécifiques à WSL2 peuvent toujours être présentées comme des défaillances systemd, port ou passerelle génériques, donc les utilisateurs ont besoin d'aide au support pour choisir la vérification suivante.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, live et runtime-flow sont exclues de ce score de qualité.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/windows-via-wsl2.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour openclaw doctor, openclaw status, openclaw logs, SecretRef, indices WSL/systemd indisponibles, Guidance de réparation opérateur après WSL2 service.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin que les diagnostics d'environnement WSL arrivent et soient reflétés dans les docs/status.
- Besoin de vérifications de portproxy obsolète, démarrage WSL, pare-feu Windows et localhost Windows-host dans un chemin de réparation axé sur WSL2.
- Besoin d'exemples spécifiques à WSL2 pour interpréter `status --all` quand le service est en cours d'exécution mais la passerelle WebSocket Gateway est inaccessible.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:88` : la réparation/migration WSL2 pointe vers `openclaw doctor`.
- `/Users/kevinlin/code/openclaw/docs/cli/status.md:32` : l'aperçu du status inclut l'installation et le runtime du service Gateway et du nœud hôte quand disponibles.
- `/Users/kevinlin/code/openclaw/docs/cli/status.md:37` : status résout les SecretRefs supportés et rapporte une sortie dégradée pour les indisponibles.
- `/Users/kevinlin/code/openclaw/docs/cli/logs.md:61` : les logs reviennent au journal de fichier Gateway configuré quand le RPC Gateway local est indisponible.
- `/Users/kevinlin/code/openclaw/docs/cli/logs.md:62` : sur Linux, `logs --follow` peut utiliser le journal Gateway systemd utilisateur actif par PID.
- `/Users/kevinlin/code/openclaw/docs/cli/doctor.md:196` : le docteur non-interactif rapporte les définitions de service manquantes/obsolètes mais ne les installe pas en dehors du mode de réparation de mise à jour.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:464` : le docteur vérifie le systemd linger sur Linux.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:529` : le docteur audite et répare la dérive de configuration du superviseur.

### Source

- `/Users/kevinlin/code/openclaw/src/daemon/systemd-hints.ts:24` : les indices systemd indisponibles spécifiques à WSL sont rendus quand WSL est détecté.
- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/lifecycle-core.ts:68` : les actions de cycle de vie augmentent les indices de service avec les conseils systemd conscients de WSL.
- `/Users/kevinlin/code/openclaw/src/flows/doctor-health-contributions.ts:623` : la santé systemd-linger du docteur s'intègre avec l'état du service Linux.
- `/Users/kevinlin/code/openclaw/src/commands/status.format.ts` : le formatage du status inclut le runtime du service et les résumés d'hygiène cgroup systemd.
- `/Users/kevinlin/code/openclaw/src/cli/logs-cli.ts` : la CLI des logs lit le runtime du service systemd actif et le secours du journal.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:122` : l'e2e vérifie que le docteur peut basculer les points d'entrée de service entre les variantes d'installation.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:174` : l'e2e vérifie le nettoyage de l'environnement de service.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/logs-cli.test.ts:415` : les tests de logs utilisent le journal systemd actif pour les défaillances de suivi local implicites.
- `/Users/kevinlin/code/openclaw/src/commands/status.daemon.test.ts:46` : les tests de status incluent l'hygiène cgroup systemd suspecte dans le résumé du runtime de service.
- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/response.test.ts:34` : les tests de réponse classifient les indices systemd WSL.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd.test.ts:165` : les tests systemd réparent l'environnement du user-bus manquant.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "WSL2 doctor logs update Gateway" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "Windows WSL2 gateway systemd" --mode keyword --limit 10 --json`

Résultats :

- La requête WSL2 doctor/logs/update a retourné 0 résultats.
- Windows WSL2 gateway systemd a retourné 10 résultats, incluant la PR de diagnostics WSL #58853, le problème de cyclage docteur/passerelle #55563, la PR user-bus WSL #68400, le problème de gel de boucle d'événement WSL2 #56733, le problème RestartSec/lock #80696, et le problème de boucle SIGTERM WSL2 Gateway #84610.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 doctor logs update Gateway"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "Windows WSL2 gateway systemd"`

Résultats :

- WSL2 doctor/logs/update a retourné 8 résultats, incluant les défaillances Telegram/canal WSL2, les erreurs d'analyse de plugin personnalisé, les tentatives de récupération `doctor --fix`, et les logs Gateway montrant la sortie de politique réseau spécifique à WSL2.
- Windows WSL2 gateway systemd a retourné 8 résultats, incluant les rapports de sonde de service `No medium found`, les extraits de status où le service systemd est en cours d'exécution mais la passerelle est inaccessible, et les conseils de support pour distinguer l'état du service de la réachabilité de la passerelle.
