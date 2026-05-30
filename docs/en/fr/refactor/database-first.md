---
summary: "Plan de migration pour faire de SQLite la couche d'état durable et de cache principale tout en conservant la configuration basée sur des fichiers"
title: "Refactorisation d'état orientée base de données"
read_when:
  - Déplacement des données d'exécution OpenClaw, du cache, des transcriptions, de l'état des tâches ou des fichiers de travail dans SQLite
  - Conception des migrations du docteur à partir de fichiers JSON ou JSONL hérités
  - Modification du comportement de sauvegarde, restauration, VFS ou stockage des workers
  - Suppression des verrous de session, élagage, troncature ou chemins de compatibilité JSON
---

# Refactorisation d'état orientée base de données

## Décision

Utiliser une disposition SQLite à deux niveaux :

- Base de données globale : `~/.openclaw/state/openclaw.sqlite`
- Base de données d'agent : une base de données SQLite par agent pour l'espace de travail détenu par l'agent,
  la transcription, le VFS, l'artefact et l'état d'exécution volumineux par agent
- La configuration reste basée sur des fichiers : `openclaw.json` reste en dehors de la
  base de données. Les profils d'authentification d'exécution se déplacent vers SQLite ; les fichiers d'identifiants de fournisseur externe ou CLI
  restent gérés par le propriétaire en dehors de la base de données d'OpenClaw.

La base de données globale est la base de données du plan de contrôle. Elle possède la découverte d'agents,
l'état de passerelle partagée, l'appairage, l'état du périphérique/nœud, les registres de tâches et de flux, l'état du plugin, l'état d'exécution du planificateur, les métadonnées de sauvegarde et l'état de migration.

La base de données d'agent est la base de données du plan de données. Elle possède les métadonnées de session de l'agent, le flux d'événements de transcription, l'espace de travail VFS ou l'espace de noms de travail, les artefacts d'outils, les artefacts d'exécution et les données de cache locales à l'agent recherchables/indexables.

Cela donne une vue durable globale sans forcer les grands espaces de travail d'agent,
les transcriptions et les données de travail binaires dans la voie d'écriture partagée de la passerelle.

## Contrat strict

Cette migration a une seule forme d'exécution canonique :

- Les lignes de session persistent uniquement les métadonnées de session. Elles ne doivent pas persister
  `transcriptLocator`, les chemins de fichiers de transcription, les chemins JSONL frères, les chemins de verrous,
  les métadonnées d'élagage ou les pointeurs de compatibilité d'ère de fichier.
- L'identité de transcription est toujours l'identité SQLite : `{agentId, sessionId}` plus
  les métadonnées de sujet optionnelles où le protocole en a besoin.
- `sqlite-transcript://...` n'est pas une identité d'exécution ou de protocole. Le nouveau code ne doit
  pas dériver, persister, passer, analyser ou migrer les localisateurs de transcription. L'exécution et
  les tests ne doivent pas contenir du tout de pseudo-localisateurs ; la documentation peut mentionner la chaîne
  uniquement pour l'interdire.
- Les `sessions.json` hérités, la transcription JSONL, `.jsonl.lock`, l'élagage, la troncature,
  et l'ancienne logique de chemin de session appartiennent uniquement au chemin de migration/importation du docteur.
- Les alias de configuration de session hérités appartiennent uniquement à la migration du docteur. L'exécution
  n'interprète pas `session.idleMinutes`, `session.resetByType.dm` ou
  les alias de session principale entre agents `agent:main:*` pour un autre agent configuré.
- L'identité de routage de session est un état relationnel typé. Les chemins d'exécution chauds et d'interface utilisateur
  doivent lire `sessions.session_scope`, `sessions.account_id`,
  `sessions.primary_conversation_id`, `conversations` et
  `session_conversations` ; ils ne doivent pas analyser `session_key` ou extraire
  `session_entries.entry_json` pour l'identité du fournisseur sauf comme ombre de compatibilité pendant que les anciens sites d'appel sont supprimés.
- Les marqueurs de message direct au niveau du canal tels que `dm` par rapport à `direct` sont du vocabulaire de routage,
  pas des localisateurs de transcription ou des poignées de compatibilité de magasin de fichiers.
- La configuration du gestionnaire de hook hérité appartient uniquement aux surfaces d'avertissement/migration du docteur.
  L'exécution ne doit pas charger `hooks.internal.handlers` ; les hooks s'exécutent via les répertoires de hook découverts et les métadonnées `HOOK.md` uniquement.
- Le démarrage d'exécution, les chemins de réponse chauds, la compaction, la réinitialisation, la récupération, les diagnostics,
  TTS, les hooks de mémoire, les sous-agents, le routage des commandes de plugin, les limites de protocole et
  les hooks doivent passer `{agentId, sessionId}` via l'exécution.
- Les tests doivent ensemencer et affirmer les lignes de transcription SQLite via
  `{agentId, sessionId}`. Les tests qui ne prouvent que le transfert de chemin JSONL,
  la préservation du localisateur fourni par l'appelant ou la compatibilité du fichier de transcription doivent
  être supprimés sauf s'ils couvrent l'importation du docteur, la matérialisation de support/débogage sans session ou la forme de protocole.
- `runEmbeddedPiAgent(...)`, les exécutions de worker préparées et la tentative interne
  ne doivent pas accepter les localisateurs de transcription. Ils ouvrent le gestionnaire de transcription SQLite par `{agentId, sessionId}` et passent ce gestionnaire à la session d'agent compatible PI internalisée, donc les anciens appelants ne peuvent pas faire écrire au runner des transcriptions JSON/JSONL.
- Les diagnostics du runner doivent stocker les enregistrements de trace d'exécution/cache/charge utile dans SQLite.
  Les diagnostics d'exécution ne doivent pas exposer les boutons de remplacement de fichier JSONL ou les assistants d'exportation de transcription JSONL génériques ; les exportations orientées utilisateur peuvent matérialiser des artefacts explicites à partir de lignes de base de données sans réinjecter les noms de fichiers dans l'exécution.
- La journalisation de flux brut utilise `OPENCLAW_RAW_STREAM=1` plus les lignes de diagnostics SQLite.
  Le contrat du logger de fichier `PI_RAW_STREAM`, `PI_RAW_STREAM_PATH` et
  `raw-openai-completions.jsonl` hérité de pi-mono ne fait pas partie de l'exécution ou des tests d'OpenClaw.
- L'indexation de mémoire QMD ne doit pas exporter les transcriptions SQLite vers des fichiers markdown.
  Les index QMD indexent uniquement les fichiers de mémoire configurés ; la recherche de transcription de session reste
  basée sur SQLite.
- Le sous-chemin du SDK QMD est QMD uniquement pour le nouveau code. Les assistants d'indexation de transcription de session SQLite vivent sur `memory-core-host-engine-session-transcripts` ; toute réexportation QMD est uniquement pour la compatibilité et ne doit pas être utilisée par le code d'exécution.
- Les index de mémoire intégrés vivent dans la base de données d'agent propriétaire. La configuration d'exécution et
  les contrats d'exécution résolus ne doivent pas exposer `memorySearch.store.path` ; le docteur
  supprime cette clé de configuration hérité et le code actuel passe le `databasePath` d'agent en interne.

Le travail d'implémentation doit continuer à supprimer le code jusqu'à ce que ces déclarations soient vraies
sans exceptions en dehors des limites du docteur/importation/exportation/débogage.

## État objectif et progression

### Objectif strict

- Une base de données SQLite globale possède l'état du plan de contrôle :
  `state/openclaw.sqlite`.
- Une base de données SQLite par agent possède l'état du plan de données :
  `agents/<agentId>/agent/openclaw-agent.sqlite`.
- La configuration reste basée sur des fichiers. `openclaw.json` ne fait pas partie de cette refactorisation de base de données.
- Les fichiers hérités sont uniquement des entrées de migration du docteur.
- L'exécution n'écrit jamais ou ne lit jamais la session ou la transcription JSONL comme état actif.

### États objectifs

- `not-started` : le code d'exécution d'ère de fichier écrit toujours l'état actif.
- `migrating` : le code du docteur/importation peut déplacer les données de fichier dans SQLite.
- `dual-read` : un pont temporaire lit à la fois SQLite et les fichiers hérités. Cet état
  est interdit pour cette refactorisation sauf s'il est explicitement documenté comme
  docteur uniquement.
- `sqlite-runtime` : l'exécution lit et écrit uniquement SQLite.
- `clean` : les API d'exécution hérités et les tests sont supprimés, et la garde empêche
  les régressions.
- `done` : la documentation, les tests, la sauvegarde, la migration du docteur et les vérifications modifiées prouvent l'état
  clean.

### État actuel

- Sessions : `clean` pour l'exécution. Les lignes de session vivent dans la base de données par agent,
  les API d'exécution utilisent `{agentId, sessionId}` ou `{agentId, sessionKey}` et
  `sessions.json` est une entrée hérité du docteur uniquement.
- Transcriptions : `clean` pour l'exécution. Les événements de transcription, les identités, les instantanés
  et les événements de trajectoire d'exécution vivent dans la base de données par agent. L'exécution n'accepte plus
  les localisateurs de transcription ou les chemins de transcription JSONL.
- Runner PI intégré : `clean`. Les exécutions PI intégrées, les workers préparés, la compaction
  et les boucles de nouvelle tentative utilisent la portée de session SQLite et rejettent les poignées de transcription obsolètes.
- Cron : `clean` pour l'exécution. L'exécution utilise `cron_jobs` et `cron_run_logs` ;
  les tests d'exécution utilisent la dénomination SQLite `storeKey` et les chemins cron d'ère de fichier restent dans
  les tests de migration hérité du docteur uniquement.
- Registre de tâches : `clean`. Les lignes d'exécution Task et Task Flow vivent dans
  `state/openclaw.sqlite` ; les importateurs SQLite sidecar non expédiés sont supprimés.
- État du plugin : `clean`. Les lignes d'état/blob du plugin vivent dans la base de données globale partagée ;
  les anciens assistants SQLite sidecar d'état du plugin sont protégés contre.
- Mémoire : `sqlite-runtime` pour la mémoire intégrée et l'indexation de transcription de session.
  Les tables d'index de mémoire vivent dans la base de données par agent, l'état de mémoire du plugin utilise
  les lignes d'état du plugin partagé et les fichiers de mémoire hérités sont des entrées de migration du docteur
  ou du contenu de l'espace de travail utilisateur.
- Sauvegarde : `sqlite-runtime`. Les étapes de sauvegarde compactent les instantanés SQLite, omettent les sidecars WAL/SHM en direct,
  vérifient l'intégrité SQLite et enregistrent les exécutions de sauvegarde dans la base de données globale.
- Migration du docteur : `migrating`, intentionnellement. Le docteur importe les JSON, JSONL hérités et
  les magasins sidecar retirés dans SQLite, enregistre les exécutions/sources de migration
  et supprime les sources réussies.
- Scripts E2E : `clean` pour la couverture d'exécution. L'ensemencement Docker MCP écrit les lignes SQLite.
  Le script Docker de contexte d'exécution crée JSONL hérité uniquement à l'intérieur de la
  graine de migration du docteur et nomme explicitement le chemin d'index de session hérité.

### Travail restant

- [x] Renommer les variables de magasin de test d'exécution cron loin de `storePath` sauf si
      elles sont des entrées hérité du docteur.
      Fichiers : `src/cron/service.test-harness.ts`,
      `src/cron/service.runs-one-shot-main-job-disables-it.test.ts`,
      `src/cron/service/timer.regression.test.ts`,
      `src/cron/service/ops.test.ts`, `src/cron/service/store.test.ts`,
      `src/cron/service.heartbeat-ok-summary-suppressed.test.ts`,
      `src/cron/service.main-job-passes-heartbeat-target-last.test.ts`,
      `src/cron/store.test.ts`.
      Preuve : `pnpm check:database-first-legacy-stores` ; `rg -n 'storePath' src/cron --glob '!**/commands/doctor/**'`.
- [x] Supprimer ou renommer les mocks de test d'exportation d'ère de fichier obsolètes.
      Fichier : `src/auto-reply/reply/commands-export-test-mocks.ts`.
      Preuve : `rg -n 'resolveSessionFilePath|sessionFile|storePath|transcriptLocator' src/auto-reply/reply`.
- [x] Rendre la graine JSONL hérité du contexte d'exécution Docker évidemment docteur uniquement.
      Fichier : `scripts/e2e/session-runtime-context-docker-client.ts`.
      Preuve : `rg -n 'sessions\\.json|sessionFile|\\.jsonl' scripts/e2e/session-runtime-context-docker-client.ts` affiche uniquement
      `seedBrokenLegacySessionForDoctorMigration`.
- [x] Garder les types générés Kysely alignés après tout changement de schéma.
      Fichiers : `src/state/openclaw-state-schema.sql`,
      `src/state/openclaw-agent-schema.sql`,
      `src/state/*generated*`.
      Preuve : aucun changement de schéma dans cette passe ; `pnpm db:kysely:check` ;
      `pnpm lint:kysely`.
- [x] Réexécuter les tests ciblés pour les magasins, commandes et scripts touchés.
      Preuve : `pnpm test src/cron/service/store.test.ts src/cron/store.test.ts src/cron/service.heartbeat-ok-summary-suppressed.test.ts src/cron/service.main-job-passes-heartbeat-target-last.test.ts src/cron/service.every-jobs-fire.test.ts src/cron/service.persists-delivered-status.test.ts src/cron/service.runs-one-shot-main-job-disables-it.test.ts src/cron/service/ops.test.ts src/cron/service/timer.regression.test.ts src/auto-reply/reply/commands-export-trajectory.test.ts extensions/telegram/src/thread-bindings.test.ts extensions/slack/src/monitor/message-handler/prepare.test.ts src/acp/translator.session-lineage-meta.test.ts` ; `git diff --check`.
- [x] Avant de déclarer `done`, exécutez la porte modifiée ou la preuve large à distance.
      Preuve : `pnpm check:changed --timed -- <changed extension paths>` réussi sur
      l'exécution Hetzner Crabbox `run_3f1cabf6b25c` après la configuration temporaire de Node 24/pnpm et
      le routage de chemin explicite pour l'espace de travail synchronisé sans `.git`.

### Ne pas régresser

- Aucun localisateur de transcription.
- Aucun fichier de session actif.
- Aucun fixture JSONL de test faux sauf les tests de migration hérité du docteur.
- Aucun accès SQLite brut où Kysely est attendu.
- Aucune nouvelle migration de base de données hérité. Cette disposition n'a pas été expédiée ; gardez la version de schéma
  à `1` sauf s'il y a une bonne raison.

## Hypothèses de lecture du code

Aucune décision produit ultérieure ne bloque ce plan. L'implémentation doit
procéder avec ces hypothèses :

- Utiliser `node:sqlite` directement et exiger le runtime Node 22+ pour ce chemin
  de stockage.
- Conserver exactement un fichier de configuration normal. Ne pas déplacer la
  configuration, les manifestes de plugins ou les espaces de travail Git dans
  SQLite dans cette refonte.
- Les fichiers de compatibilité runtime ne sont pas requis. Les fichiers JSON et
  JSONL hérités sont des entrées de migration uniquement. Les barres latérales
  SQLite locales aux branches n'ont jamais été livrées et sont supprimées au lieu
  d'être importées.
- `openclaw doctor --fix` possède l'étape de migration de fichier vers base de
  données hérité. Le démarrage runtime et `openclaw migrate` ne doivent pas
  porter les chemins de mise à niveau de base de données OpenClaw hérités.
- La compatibilité des identifiants suit la même règle : les identifiants runtime
  vivent dans SQLite. Les anciens fichiers `auth-profiles.json`, `auth.json` par
  agent et `credentials/oauth.json` partagés sont des entrées de migration doctor,
  puis supprimés après importation.
- L'état du catalogue de modèles généré est soutenu par la base de données. Le
  code runtime ne doit pas écrire `agents/<agentId>/agent/models.json` ; les
  fichiers `models.json` existants sont des entrées doctor hérités et sont
  supprimés après importation dans `agent_model_catalogs`.
- Le runtime ne doit pas migrer, normaliser ou créer de pont pour les localisateurs
  de transcription. L'identité de transcription active est `{agentId, sessionId}`
  dans SQLite. Les chemins de fichiers sont des entrées doctor hérités uniquement,
  et `sqlite-transcript://...` doit disparaître des surfaces runtime, protocole,
  hook et plugin au lieu d'être traité comme un handle de limite.
- Les lectures de transcription SQLite runtime n'exécutent pas les anciennes
  migrations de forme d'entrée JSONL ou ne réécrivent pas les transcriptions
  entières pour la compatibilité. La normalisation d'entrée hérité reste dans les
  utilitaires doctor/import explicites. Doctor normalise les fichiers de
  transcription JSONL hérités avant d'insérer les lignes SQLite ; les lignes
  runtime actuelles sont déjà écrites dans le schéma de transcription actuel.
  L'export de trajectoire/session lit ces lignes telles quelles et ne doit pas
  effectuer les migrations hérités au moment de l'export.
- Les assistants d'analyse/migration de transcription JSONL hérité sont doctor
  uniquement. Le code de format de transcription runtime construit uniquement le
  contexte de transcription SQLite actuel ; doctor possède les mises à niveau
  d'entrée JSONL anciennes avant d'insérer les lignes.
- L'ancien assistant de streaming de transcription JSONL détenu par le runtime a
  été supprimé. Le code d'importation doctor possède les lectures de fichiers
  hérités explicites ; la lecture d'historique de session runtime lit les lignes
  SQLite.
- Les liaisons du serveur d'application Codex utilisent le `sessionId` OpenClaw
  comme clé canonique dans l'espace de noms d'état du plugin Codex. `sessionKey`
  est des métadonnées pour le routage/affichage et ne doit pas remplacer l'id de
  session durable ou ressusciter l'identité du fichier de transcription.
- Les moteurs de contexte reçoivent le contrat runtime actuel directement. Le
  registre ne doit pas envelopper les moteurs avec des shims de nouvelle tentative
  qui suppriment `sessionKey`, `transcriptScope` ou `prompt` ; les moteurs qui ne
  peuvent pas accepter les paramètres actuels orientés base de données doivent
  échouer bruyamment au lieu d'être pontés.
- La sortie de sauvegarde doit rester un fichier d'archive. Le contenu de la base
  de données doit entrer dans cette archive sous forme d'instantanés SQLite
  compacts, pas de barres latérales WAL en direct brutes.
- La recherche de transcription est utile mais non requise pour la première coupe
  orientée base de données. Concevez le schéma pour que FTS puisse être ajouté
  ultérieurement.
- L'exécution des workers doit rester expérimentale derrière les paramètres
  pendant que la limite de la base de données se stabilise.

## Résultats de la lecture du code

La branche actuelle a déjà dépassé le stade de la preuve de concept. La base de
données partagée existe, Node `node:sqlite` est câblé via un petit assistant
runtime, et les anciens magasins écrivent maintenant dans `state/openclaw.sqlite`
ou la base de données `openclaw-agent.sqlite` propriétaire.

Le travail restant ne consiste pas à choisir SQLite ; il s'agit de maintenir la
nouvelle limite propre et de supprimer toutes les interfaces en forme de
compatibilité qui ressemblent encore à l'ancien monde des fichiers :

- Le `storePath` de session n'est plus une identité runtime, une forme de fixture
  de test ou un champ de charge utile d'état. Le code runtime et les tests de
  pont ne contiennent plus le nom de contrat `storePath` ; le code doctor/migration
  possède ce vocabulaire hérité.
- Les écritures de session ne passent plus par l'ancienne file d'attente
  `store-writer.ts` en processus. Les écritures de patch SQLite utilisent la
  détection de conflit et la nouvelle tentative bornée à la place.
- La découverte de chemin hérité a toujours des utilisations de migration valides,
  mais le code runtime doit arrêter de traiter `sessions.json` et les fichiers
  JSONL de transcription comme des cibles d'écriture possibles.
- Les tables détenues par l'agent vivent dans les bases de données SQLite par
  agent. La base de données globale conserve les lignes du plan de contrôle/registre ;
  l'identité de transcription est `{agentId, sessionId}` dans les lignes de
  transcription par agent. Le code runtime ne doit pas persister les chemins de
  fichiers de transcription ou migrer les localisateurs de transcription.
- Doctor importe déjà plusieurs fichiers hérités. Le nettoyage consiste à en faire
  une implémentation de migration explicite unique que doctor appelle, avec un
  rapport de migration durable.

Aucune question produit supplémentaire ne bloque l'implémentation.

## Forme actuelle du code

La branche a déjà une vraie base SQLite partagée :

- Le plancher d'exécution est maintenant Node 22+ : `package.json`, la garde d'exécution CLI,
  les valeurs par défaut du programme d'installation, le localisateur d'exécution macOS, CI et la documentation d'installation publique
  s'accordent tous. L'ancienne voie de compatibilité Node 22 est supprimée.
- `src/state/openclaw-state-db.ts` ouvre `openclaw.sqlite`, définit WAL,
  `synchronous=NORMAL`, `busy_timeout=30000`, `foreign_keys=ON`, et applique
  le module de schéma généré dérivé de
  `src/state/openclaw-state-schema.sql`.
- Les types de table Kysely et les modules de schéma d'exécution sont générés à partir de bases de données
  SQLite jetables créées à partir des fichiers `.sql` validés ; le code d'exécution
  ne conserve plus les chaînes de schéma copiées-collées pour les bases de données
  globales, par agent ou de capture proxy.
- Les magasins d'exécution dérivaient les types de lignes sélectionnées et insérées de ces
  interfaces `DB` Kysely générées au lieu de reproduire les formes de lignes SQLite à la main. Le SQL brut
  reste limité à l'application de schéma, aux pragmas et au DDL de migration uniquement.
- Les schémas SQLite sont réduits à `user_version = 1` car cette disposition de base de données
  n'a pas encore été expédiée. Les ouvreurs d'exécution créent uniquement le schéma actuel ;
  l'importation fichier-vers-base de données reste dans le code du docteur, et les assistants
  de mise à niveau de base de données locaux à la branche ont été supprimés.
- La propriété relationnelle est appliquée là où la limite de propriété est canonique :
  les lignes de migration source en cascade de `migration_runs`, l'état de livraison des tâches
  en cascade de `task_runs`, et les lignes d'identité de transcription en cascade des
  événements de transcription.
- Les tables partagées actuelles incluent `agent_databases`,
  `auth_profile_stores`, `auth_profile_state`,
  `plugin_state_entries`, `plugin_blob_entries`, `media_blobs`,
  `skill_uploads`, `capture_sessions`, `capture_events`, `capture_blobs`,
  `sandbox_registry_entries`, `cron_run_logs`, `cron_jobs`, `commitments`,
  `delivery_queue_entries`, `model_capability_cache`,
  `workspace_setup_state`, `native_hook_relay_bridges`,
  `current_conversation_bindings`, `plugin_binding_approvals`,
  `tui_last_sessions`, `task_runs`, `task_delivery_state`, `flow_runs`,
  `subagent_runs`, `migration_runs`, et `backup_runs`.
- L'état arbitraire détenu par les plugins n'obtient pas de tables typées détenues par l'hôte. Les plugins installés utilisent `plugin_state_entries` pour les charges utiles JSON versionnées et
  `plugin_blob_entries` pour les octets, avec propriété d'espace de noms/clé, nettoyage TTL,
  sauvegarde et enregistrements de migration de plugins. L'état d'orchestration de plugins détenu par l'hôte peut
  toujours avoir des tables typées lorsque l'hôte possède le contrat de requête, comme
  `plugin_binding_approvals`.
- Les migrations de plugins sont des migrations de données sur les espaces de noms détenus par les plugins, pas des
  migrations de schéma d'hôte. Un plugin peut migrer son propre état versé/entrées blob
  via un fournisseur de migration, et l'hôte enregistre l'état source/exécution dans
  le registre de migration normal. Les nouvelles installations de plugins ne nécessitent pas de modifier
  `openclaw-state-schema.sql` sauf si l'hôte lui-même prend possession d'un
  nouveau contrat inter-plugins.
- `src/state/openclaw-agent-db.ts` ouvre
  `agents/<agentId>/agent/openclaw-agent.sqlite`, enregistre la base de données dans la
  base de données globale, et possède les tables de session, transcription, VFS, artefact, cache,
  et index mémoire locales à l'agent. La découverte d'exécution partagée lit maintenant le `agent_databases`
  typé généré au lieu de réimplémenter cette requête à chaque site d'appel.
- Les bases de données globales et par agent enregistrent une ligne `schema_meta` avec le rôle de base de données,
  la version de schéma, les horodatages et l'id d'agent pour les bases de données d'agent. La disposition reste
  à `user_version = 1` car ce schéma SQLite n'a pas encore été expédié.
- L'identité de session par agent a maintenant une table racine `sessions` canonique indexée par
  `session_id`, avec `session_key`, `session_scope`, `account_id`,
  `primary_conversation_id`, horodatages, champs d'affichage, métadonnées de modèle,
  id de harnais et liaison parent/spawn comme colonnes interrogeables. `session_routes`
  est l'index de route active unique de `session_key` vers le
  `session_id` actuel, donc une clé de route peut se déplacer vers une session durable fraîche sans
  faire en sorte que les lectures à chaud choisissent entre les lignes `sessions.session_key` en double. L'ancienne
  charge utile compatible `session_entries.entry_json` pend de la
  racine durable `session_id` par clé étrangère ; ce n'est plus la seule
  représentation au niveau du schéma d'une session.
- L'identité de conversation externe par agent est également relationnelle :
  `conversations` stocke l'identité normalisée du fournisseur/compte/conversation, et
  `session_conversations` lie une session OpenClaw à une ou plusieurs conversations externes. Cela couvre
  les sessions DM partagées-principales où plusieurs pairs peuvent intentionnellement mapper à une session
  sans mentir dans `session_key`. SQLite applique également l'unicité pour l'identité
  du fournisseur naturel afin que le même tuple canal/compte/type/pair/thread ne puisse pas se diviser
  entre les ids de conversation. Les pairs directs partagés-principaux sont liés avec un rôle `participant`, donc une
  session OpenClaw peut représenter plusieurs pairs DM externes sans rétrograder
  les pairs plus anciens en lignes vagues. `sessions.primary_conversation_id` pointe toujours
  vers la cible de livraison typée actuelle. Les colonnes de routage/statut fermées
  sont appliquées avec les contraintes SQLite `CHECK` au lieu de s'appuyer uniquement sur
  les unions TypeScript.
  La projection de session d'exécution efface les ombres de routage de compatibilité de
  `session_entries.entry_json` avant d'appliquer les colonnes de session/conversation typées, donc les charges utiles JSON obsolètes
  ne peuvent pas ressusciter les cibles de livraison.
  L'annonce de sous-agent de routage nécessite également le contexte de livraison SQLite typé ;
  elle ne revient plus aux champs de route de compatibilité `SessionEntry`.
  L'héritage de livraison explicite de la passerelle `chat.send` lit le contexte
  de livraison SQLite typé au lieu des champs de compatibilité `origin`/`last*`.
  `tools.effective` dérive également le contexte du fournisseur/compte/thread des
  lignes de livraison/routage SQLite typées, pas les ombres de session-entry `last*` obsolètes.
  La reconstruction du contexte d'invite d'événement système recréé les champs canal/à/compte/thread à partir
  des champs de livraison typés au lieu des ombres `origin`.
  L'assistant partagé `deliveryContextFromSession` et le mappeur session-vers-conversation
  ignorent maintenant entièrement `SessionEntry.origin` ; seuls les champs de livraison typés
  et les lignes de conversation relationnelles peuvent créer l'identité de route à chaud.
  La normalisation de l'entrée de session d'exécution supprime `origin` avant de persister ou
  de projeter `entry_json`, et les écritures de métadonnées entrantes tapent les champs canal/chat
  plus les lignes de conversation relationnelles au lieu de créer de nouvelles ombres d'origine.
- Les événements de transcription, les instantanés de transcription et les événements d'exécution de trajectoire
  référencent maintenant la racine `sessions` canonique par agent et en cascade à la suppression de session. Les lignes
  d'identité/idempotence de transcription continuent à en cascade de la ligne d'événement de transcription exacte.
- Les index de mémoire-core utilisent maintenant les tables de base de données d'agent explicites
  `memory_index_meta`, `memory_index_sources`, `memory_index_chunks`, et
  `memory_embedding_cache` ; les index FTS/vecteur optionnels côté utilisent le même
  préfixe `memory_index_*` au lieu des tables génériques `meta`, `files`, `chunks`, ou
  `chunks_vec`. `memory_index_sources` est indexée par
  `(source_kind, source_key)` et porte la propriété `session_id` optionnelle, donc
  les sources et chunks dérivés de session en cascade à la suppression de session. Les embeddings de chunk mis en cache
  sont stockés sous forme de BLOBs SQLite Float32, pas de tableaux de texte JSON.
  Ces tables sont dérivées/cache de recherche, pas de stockage de transcription canonique ; elles
  peuvent être supprimées et reconstruites à partir de `sessions`, `transcript_events` et des fichiers
  d'espace de travail mémoire.
- L'état de récupération d'exécution de sous-agent vit maintenant dans les lignes `subagent_runs` partagées typées
  avec les clés de session enfant, demandeur et contrôleur indexées. L'ancien
  fichier `subagents/runs.json` est une entrée de migration docteur uniquement.
- Les liaisons de conversation actuelles vivent maintenant dans les lignes `current_conversation_bindings` partagées typées
  indexées par id de conversation normalisé, avec les colonnes d'agent/session cible, le type de conversation, le statut,
  l'expiration et les métadonnées stockées comme colonnes relationnelles au lieu d'un enregistrement de liaison opaque dupliqué.
  La clé de liaison durable inclut le type de conversation normalisé afin que les références directs/groupe/canal ne puissent pas
  entrer en collision, et SQLite rejette les valeurs de type/statut de liaison invalides. L'ancien
  fichier `bindings/current-conversations.json` est une entrée de migration docteur uniquement.
- La récupération de la file d'attente de livraison superpose maintenant les colonnes de file d'attente typées pour le canal, la cible,
  le compte, la session, la tentative, l'erreur, l'envoi de plateforme et l'état de récupération sur le JSON de relecture. `entry_json` conserve les charges utiles de relecture, les crochets et la charge utile de formatage,
  mais les colonnes typées sont autoritaires pour le routage/état de la file d'attente à chaud.
- Les pointeurs de restauration de dernière session TUI vivent maintenant dans les lignes `tui_last_sessions` partagées typées
  indexées par la portée de connexion/session TUI hachée.
  L'ancien fichier JSON TUI est une entrée de migration docteur uniquement.
- Les préférences TTS par défaut vivent maintenant dans les lignes d'état de plugin SQLite partagées indexées sous
  le plugin `speech-core`. L'ancien fichier `settings/tts.json` est une entrée de migration docteur uniquement ; l'exécution
  ne lit ni n'écrit plus les fichiers JSON de préférences TTS, et le résolveur de chemin hérité vit dans le module de migration docteur.
- Les métadonnées de cible secrète parlent maintenant de magasins au lieu de prétendre que chaque
  cible de credential est un fichier de configuration. `openclaw.json` reste le magasin de configuration ;
  les cibles de profil d'authentification utilisent les lignes SQLite typées `auth_profile_stores` avec
  les credentials en forme de fournisseur conservées comme charges utiles JSON.
- L'audit secret ne scanne plus les fichiers `auth.json` par agent retraités. Le docteur possède
  l'avertissement sur, l'importation et la suppression de ce fichier hérité.
- Les assistants de chemin de profil d'authentification hérités vivent maintenant dans le code hérité du docteur. Les assistants de chemin de profil d'authentification principal exposent
  l'identité du magasin SQLite d'authentification et les emplacements d'affichage,
  pas les chemins d'exécution `auth-profiles.json` ou `auth-state.json`.
- Les modules d'exécution de récupération d'exécution de sous-agent et de cache de capacité de modèle OpenRouter
  gardent maintenant les lecteurs/écrivains d'instantané SQLite séparés des assistants d'importation JSON hérités du docteur uniquement. Les capacités OpenRouter utilisent les lignes `model_capability_cache`
  génériques typées sous `provider_id = "openrouter"` au lieu d'un blob de cache opaque ou d'une table d'hôte spécifique au fournisseur. Le sous-agent `taskName` est stocké dans la colonne typée `subagent_runs.task_name` ; la
  copie `payload_json` est une donnée de relecture/débogage, pas la source pour les champs d'affichage ou de recherche à chaud.
- `src/agents/filesystem/virtual-agent-fs.sqlite.ts` implémente un VFS SQLite
  sur la table `vfs_entries` de la base de données d'agent. Les lectures de répertoire, les exportations récursives,
  les suppressions et les renommages utilisent les plages de préfixe indexées `(namespace, path)`
  au lieu de scanner un espace de noms entier ou de s'appuyer sur la correspondance de chemin `LIKE`.
- `src/agents/runtime-worker.entry.ts` crée des magasins VFS SQLite, d'artefact d'outil,
  d'artefact d'exécution et de cache délimité par exécution pour les workers.
- Les marqueurs d'achèvement d'amorçage d'espace de travail vivent maintenant dans les lignes `workspace_setup_state` partagées typées
  indexées par chemin d'espace de travail résolu au lieu de `.openclaw/workspace-state.json` ; l'exécution
  ne lit ni ne réécrit plus le marqueur d'espace de travail hérité, et les API d'assistance
  ne passent plus un chemin `.openclaw/setup-state` factice juste pour dériver l'identité de stockage.
- Les approbations d'exécution vivent maintenant dans la ligne singleton SQLite partagée typée `exec_approvals_config`. Le docteur importe le `~/.openclaw/exec-approvals.json` hérité ;
  les écritures d'exécution ne créent, ne réécrivent plus ou ne signalent plus ce fichier comme son emplacement de magasin actif. Le compagnon macOS lit et écrit la même
  ligne de table `state/openclaw.sqlite` ; il garde uniquement le socket d'invite Unix sur disque
  car c'est de l'IPC, pas de l'état d'exécution durable.
- L'identité de l'appareil, l'authentification de l'appareil et les modules d'exécution d'amorçage gardent maintenant leurs
  lecteurs/écrivains d'instantané SQLite séparés des assistants d'importation JSON hérités du docteur uniquement. L'identité de l'appareil utilise les lignes typées `device_identities` et les jetons d'authentification de l'appareil utilisent les lignes typées `device_auth_tokens`. Les écritures d'authentification de l'appareil réconcilient les lignes
  par appareil/rôle au lieu de tronquer la table de jetons, et l'exécution ne route plus les mises à jour de jeton unique via l'ancien adaptateur de magasin entier. Les charges utiles JSON version-1 héritées existent uniquement comme formes d'importation/exportation du docteur.
- Le cache d'échange de jetons GitHub Copilot utilise la table d'état de plugin SQLite partagée
  sous `github-copilot/token-cache/default`. C'est un état de cache détenu par le fournisseur,
  donc il n'ajoute intentionnellement pas une table de schéma d'hôte.
- L'exécution Swift partagée (`OpenClawKit`) utilise les mêmes
  lignes `state/openclaw.sqlite` pour l'identité de l'appareil et l'authentification de l'appareil. Les assistants d'application macOS importent les assistants SQLite partagés au lieu de posséder un deuxième chemin JSON ou SQLite.
  Un fichier hérité `identity/device.json` bloque la création d'identité
  jusqu'à ce que le docteur l'importe dans SQLite, correspondant à la porte de démarrage TypeScript et Android.
- L'identité de l'appareil Android utilise le même matériel clé compatible TypeScript
  stocké dans les lignes typées `state/openclaw.sqlite#table/device_identities`. Il ne lit ni n'écrit jamais `openclaw/identity/device.json` ;
  un fichier hérité restant bloque le démarrage jusqu'à ce que le docteur l'importe dans SQLite.
- Les jetons d'authentification de l'appareil mis en cache Android utilisent également les lignes typées
  `state/openclaw.sqlite#table/device_auth_tokens` et partagent la même sémantique de jeton version-1 que TypeScript et Swift. L'exécution ne lit plus les clés de compatibilité `SecurePrefs`
  `gateway.deviceToken*` ; celles-ci appartiennent à la logique de migration/docteur uniquement.
- L'historique des packages récents de notification Android utilise les lignes typées
  `android_notification_recent_packages`. L'exécution ne migre plus ou ne lit les anciennes clés CSV `SharedPreferences`.
- La création d'identité de l'appareil échoue fermée lorsque le `identity/device.json` hérité
  existe, lorsque la ligne d'identité SQLite est invalide, ou lorsque le
  magasin d'identité SQLite ne peut pas être ouvert. Le docteur importe et supprime ce fichier en premier, donc le démarrage d'exécution
  ne peut pas faire silencieusement tourner l'identité d'appairage avant la migration.
- La sélection d'identité de l'appareil est une clé de ligne SQLite, pas un localisateur de fichier JSON. Les tests
  et les assistants de passerelle passent des clés d'identité explicites ; seule la migration du docteur et la
  porte de démarrage fermée connaissent le nom de fichier `identity/device.json` retraité.
- La compatibilité de réinitialisation de session vit maintenant dans la migration de configuration du docteur :
  `session.idleMinutes` est déplacé dans `session.reset.idleMinutes`,
  `session.resetByType.dm` est déplacé dans `session.resetByType.direct`, et
  la politique de réinitialisation d'exécution ne lit que les clés de réinitialisation canoniques.
- La compatibilité de configuration héritée vit maintenant sous `src/commands/doctor/`. La validation normale
  `readConfigFileSnapshot()` n'importe pas les détecteurs hérités du docteur
  ou n'annote les problèmes hérités ; `runDoctorConfigPreflight()` ajoute ces problèmes pour
  la réparation/signalement du docteur. Le flux de configuration du docteur importe
  `src/commands/doctor/legacy-config.ts`, et la réparation d'id de profil OAuth hérité vit sous
  `src/commands/doctor/legacy/oauth-profile-ids.ts`.
- Les commandes non-docteur ne réparent pas automatiquement la configuration héritée. Par exemple,
  `openclaw update --channel` échoue maintenant sur une configuration héritée invalide et demande à
  l'utilisateur d'exécuter le docteur, plutôt que d'importer silencieusement le code de migration du docteur.
- Web push, APNs, Voice Wake, vérifications de mise à jour et santé de configuration utilisent maintenant des tables SQLite partagées typées
  pour les abonnements, les clés VAPID, les enregistrements de nœud, les lignes de déclenchement,
  les lignes de routage, l'état de notification de mise à jour et les entrées de santé de configuration au lieu de
  blobs JSON opaques entiers. Les écritures d'instantané Web push et APNs réconcilient maintenant
  les abonnements/enregistrements par clé primaire au lieu de vider leurs tables ; la santé de configuration fait de même par chemin de configuration.
  Leurs modules d'exécution gardent les lecteurs/écrivains d'instantané SQLite séparés des assistants d'importation JSON hérités du docteur uniquement.
- La configuration d'hôte de nœud utilise maintenant une ligne singleton typée dans la base de données SQLite partagée ;
  le docteur importe l'ancien fichier `node.json` avant l'utilisation d'exécution normale.
- L'appairage appareil/nœud, l'appairage de canal, les listes blanches de canal et l'état d'amorçage
  utilisent maintenant les lignes SQLite typées au lieu de blobs JSON opaques entiers. Les approbations de liaison de plugin et l'état de travail cron suivent la même division : les modules d'exécution exposent les opérations soutenues par SQLite et les assistants d'instantané neutres, et l'appairage/amorçage
  plus les écritures d'instantané d'approbation de liaison de plugin réconcilient les lignes par clé primaire
  au lieu de tronquer les tables, tandis que le docteur importe/supprime les anciens fichiers JSON via
  les modules `src/commands/doctor/legacy/*`.
- Les enregistrements de plugin installés vivent maintenant dans l'index de plugin installé SQLite.
  La lecture/écriture de configuration d'exécution ne migre plus ou ne préserve les données de configuration créées `plugins.installs` ;
  le docteur importe cette forme de configuration héritée dans SQLite avant l'utilisation d'exécution normale.
- Les instantanés de récupération de credential QQBot vivent maintenant dans l'état de plugin SQLite sous
  `qqbot/credential-backups`. L'exécution n'écrit plus
  `qqbot/data/credential-backup*.json` ; le docteur importe et supprime ces fichiers de sauvegarde hérités avec les autres entrées d'état QQBot.
- La planification du rechargement de la passerelle compare les instantanés d'index de plugin installé SQLite sous
  un espace de noms de diff interne `installedPluginIndex.installRecords.*`. Les décisions de rechargement d'exécution
  n'enveloppent plus ces lignes dans des objets de configuration `plugins.installs` factices.
- La mise à niveau de credential de compte nommé Matrix ne se produit plus pendant les lectures d'exécution.
  Le docteur possède l'ancien renommage `credentials/matrix/credentials.json` de niveau supérieur
  lorsqu'un compte Matrix unique/par défaut peut être résolu.
- Les modules d'exécution d'appairage principal et cron n'exportent plus les constructeurs de chemin JSON hérités.
  Les modules hérités du docteur construisent les chemins source `pending.json`, `paired.json`,
  `bootstrap.json` et `cron/jobs.json` pour les tests d'importation et la migration uniquement. La normalisation de forme de travail cron hérité et l'importation de journal d'exécution cron
  vivent sous `src/commands/doctor/legacy/cron*.ts`.
- `src/commands/doctor/legacy/runtime-state.ts` importe les fichiers d'état JSON hérités,
  y compris la configuration d'hôte de nœud, dans SQLite à partir du docteur. Les nouveaux importateurs de fichiers hérités restent sous `src/commands/doctor/legacy/`.
- `src/commands/doctor/state-migrations.ts` importe les transcriptions `sessions.json` et
  `*.jsonl` héritées directement dans SQLite et supprime les sources réussies. Il
  n'étape plus les transcriptions racine héritées via
  `agents/<agentId>/sessions/*.jsonl` ou ne crée une cible JSONL canonique avant
  l'importation.
- Les vérifications d'intégrité d'état du docteur ne scannent plus les répertoires de session hérités ou
  n'offrent la suppression JSONL orpheline. Les fichiers de transcription hérités sont des entrées de migration
  uniquement, et l'étape de migration possède l'importation plus la suppression de source.
- L'importation du registre sandbox hérité vit sous
  `src/commands/doctor/legacy/sandbox-registry.ts` ; les lectures et écritures du registre sandbox actif
  restent SQLite uniquement.
- La réparation de santé/importation de transcription de session héritée vit sous `src/commands/doctor/legacy/session-transcript-health.ts` ;
  les modules de commande d'exécution ne portent plus le code de parsing de transcription JSONL ou de réparation de branche active.

Points forts de consolidation/suppression complétés :

- L'état de plugin utilise maintenant la base de données `state/openclaw.sqlite` partagée. L'ancien
  importateur de sidecar `plugin-state/state.sqlite` local à la branche est supprimé car
  cette disposition SQLite n'a jamais été expédiée. Les assistants de sonde/test signalent le `databasePath` partagé
  au lieu d'exposer un chemin SQLite spécifique à l'état du plugin.
- Les tables d'exécution Task et Task Flow vivent maintenant dans la base de données
  `state/openclaw.sqlite` partagée au lieu de `tasks/runs.sqlite` et
  `tasks/flows/registry.sqlite` ; les anciens importateurs de sidecar sont supprimés pour
  la même raison de disposition non expédiée.
- `src/config/sessions/store.ts` n'a plus besoin de `storePath` pour les métadonnées entrantes,
  les mises à jour de route ou les lectures mises à jour. La persistance de commande, le nettoyage de session CLI, la profondeur de sous-agent, les remplacements d'authentification et l'identité de session de transcription utilisent les API de ligne d'agent/session. Les écritures sont appliquées comme des correctifs de ligne SQLite
  avec tentative de conflit optimiste.
- La résolution de cible de session expose maintenant les cibles de base de données par agent, pas les chemins `sessions.json` hérités. La passerelle partagée, les métadonnées ACP, la réparation de route du docteur et
  `openclaw sessions` énumèrent `agent_databases` plus les agents configurés.
- Le routage de session de la passerelle utilise maintenant `resolveGatewaySessionDatabaseTarget` ;
  la cible retournée porte `databasePath` et les clés de ligne SQLite candidates au lieu
  d'un chemin de fichier de magasin de session hérité.
- Les types d'exécution de session de canal exposent maintenant `{agentId, sessionKey}` pour
  les lectures mises à jour, les métadonnées entrantes et les mises à jour de dernière route. L'ancien
  type de compatibilité `saveSessionStore(storePath, store)` est parti.
- L'exécution de plugin, l'API d'extension et les surfaces de baril `config/sessions` orientent maintenant
  le code de plugin vers les assistants de ligne de session soutenues par SQLite. Les exportations de compatibilité de la bibliothèque racine
  (`loadSessionStore`, `saveSessionStore`, `resolveStorePath`) restent comme des shims dépréciés pour les consommateurs existants. L'ancien
  assistant `resolveLegacySessionStorePath` est parti ; la construction de chemin `sessions.json` hérité est maintenant locale à la migration et aux fixtures de test.
- `src/config/sessions/session-entries.sqlite.ts` stocke maintenant les entrées de session canoniques
  dans la base de données par agent et a le support de correctif de lecture/upsert/suppression au niveau des lignes. L'upsert/correctif/suppression d'exécution
  ne scanne plus les variantes de casse ou n'élagage les clés d'alias héritées ; le docteur possède la canonicalisation. L'assistant d'importation JSON autonome est parti, et la migration fusionne les lignes upsert plus récentes
  au lieu de remplacer la table de session entière. Les assistants publics de lecture/liste/chargement
  projettent les métadonnées de session à chaud à partir des lignes typées `sessions` et `conversations` ;
  `entry_json` est une ombre de compatibilité/débogage et peut être obsolète ou invalide
  sans perdre l'identité de session typée ou le contexte de livraison.
- `src/config/sessions/delivery-info.ts` résout maintenant le contexte de livraison à partir des
  lignes typées par agent `sessions` + `conversations` + `session_conversations`.
  Il ne reconstruit plus l'identité de livraison d'exécution à partir de
  `session_entries.entry_json` ; une ligne de conversation typée manquante est un problème de migration/réparation du docteur, pas un repli d'exécution.
- Les décisions de réinitialisation de session stockée préfèrent maintenant les métadonnées typées `sessions.session_scope`,
  `sessions.chat_type` et `sessions.channel`. L'analyse de `sessionKey` reste uniquement pour les suffixes de thread/sujet explicites sur les cibles de commande ; la classification de réinitialisation groupe vs direct ne provient plus de la forme de clé.
- La classification d'affichage de liste/statut de session utilise maintenant les métadonnées de chat typées et le type de session de la passerelle. Elle ne traite plus les substrings `:group:` ou `:channel:` à l'intérieur de `session_key` comme vérité durable groupe/direct.
- La sélection de politique de réponse silencieuse utilise maintenant uniquement le type de conversation explicite ou les métadonnées de surface. Elle ne devine plus la politique direct/groupe à partir
  des substrings `session_key`.
- La résolution du modèle d'affichage de session reçoit maintenant l'id d'agent à partir de la cible de base de données de session SQLite
  au lieu de le diviser de `session_key`.
- L'hydratation de cible d'annonce d'agent à agent utilise maintenant uniquement le `deliveryContext` typé `sessions.list`. Elle ne récupère plus le routage canal/compte/thread
  à partir de l'`origin` hérité, des champs `last*` en miroir ou de la forme `session_key`.
- Le rejet de cible de thread `sessions_send` lit maintenant les métadonnées de routage SQLite typées. Il ne rejette plus ou n'accepte les cibles en analysant les suffixes de thread
  de la clé cible.
- La validation de politique d'outil délimitée par groupe lit maintenant le routage de conversation SQLite typé
  pour la session actuelle ou générée. Elle ne fait plus confiance à l'identité groupe/canal en décodant `sessionKey` ;
  les ids de groupe fournis par l'appelant sont supprimés lorsqu'aucune ligne de session typée ne les garantit.
- La correspondance de remplacement de modèle de canal utilise maintenant les métadonnées de groupe et de conversation parent explicites. Elle ne décode plus les ids de conversation parent à partir de
  `parentSessionKey`.
- L'héritage de remplacement de modèle stocké nécessite maintenant une clé de session parent explicite
  à partir du contexte de session typé. Elle ne dérive plus les remplacements parent à partir
  des suffixes `:thread:` ou `:topic:` dans `sessionKey`.
- L'ancien wrapper d'info de thread de session et le parseur de thread de plugin chargé sont partis ;
  aucun code d'exécution n'importe `config/sessions/thread-info`.
- L'assistant de conversation de canal n'expose plus les ponts d'analyse de clé de session complète. Le cœur normalise toujours
  les ids de conversation bruts détenus par le fournisseur via
  `resolveSessionConversation(...)`, mais il ne reconstruit pas les faits de route
  à partir de `sessionKey`.
- La livraison d'achèvement, la politique d'envoi et la maintenance des tâches ne dérivaient plus le type de chat
  à partir de la forme `session_key`. L'ancien parseur de type de chat clé a été supprimé ;
  ces chemins nécessitent des métadonnées de session typées, un contexte de livraison typé ou
  un vocabulaire de cible de livraison explicite.
- La liste/statut de session, les diagnostics, la liaison de compte de demande d'approbation, le filtrage de battement cardiaque TUI et les résumés d'utilisation
  ne minent plus `SessionEntry.origin` pour le routage du fournisseur/compte/thread/affichage. Les seules lectures `origin` d'exécution restantes
  sont des concepts non-session ou des objets de livraison de tour actuel.
- La recherche de conversation native de demande d'approbation lit maintenant les lignes de routage de session par agent typées. Elle ne parse plus
  l'identité de conversation canal/groupe/thread à partir de `sessionKey` ;
  les métadonnées typées manquantes sont un problème de migration/réparation.
- Les charges utiles d'événement de session modifiée/chat/session de la passerelle n'échos plus
  `SessionEntry.origin` ou les ombres de route `last*` ; les clients reçoivent le `channel`, `chatType` et `deliveryContext` typés.
- La résolution de livraison de battement cardiaque peut maintenant recevoir directement le `deliveryContext` SQLite
  typé, et l'exécution de battement cardiaque passe la ligne de livraison de session par agent au lieu de s'appuyer sur les ombres de compatibilité `session_entries`
  pour le routage actuel.
- La résolution de cible de livraison d'agent isolé cron hydrate également sa route actuelle
  à partir de la ligne de livraison de session par agent typée avant de revenir à la charge utile d'entrée de compatibilité.
- La résolution d'origine d'annonce de sous-agent enfile maintenant le contexte de livraison de session de demandeur typé via `loadRequesterSessionEntry` et préfère cette ligne
  aux ombres de compatibilité `last*`/`deliveryContext`.
- Les mises à jour de métadonnées de session entrante fusionnent maintenant contre la ligne de livraison par agent typée en premier ;
  les anciens champs de livraison `SessionEntry` ne sont que le repli
  lorsqu'aucune ligne de conversation typée n'existe.
- L'extraction de livraison de redémarrage/mise à jour laisse maintenant le `threadId` de livraison SQLite typé gagner sur les fragments de sujet/thread analysés à partir de `sessionKey` ;
  l'analyse n'est qu'un repli pour les clés de thread en forme héritée.
- Les ids de canal du contexte d'agent de crochet préfèrent maintenant l'identité de conversation SQLite typée,
  puis les métadonnées de message explicites. Ils ne parsent plus les fragments de fournisseur/groupe/canal
  à partir de `sessionKey`.
- L'héritage de route externe de la passerelle `chat.send` lit maintenant les métadonnées de routage de session SQLite typées
  au lieu de déduire la portée canal/direct/groupe à partir des pièces `sessionKey`. Les sessions délimitées par canal héritent uniquement lorsque le canal de session typé et le type de chat correspondent au contexte de livraison stocké ;
  les sessions partagées-principales gardent leur règle CLI/pas-de-métadonnées-client plus stricte.
- Le réveil de sentinelle de redémarrage et le routage de continuation lisent maintenant les lignes de livraison/routage SQLite typées
  avant de mettre en file d'attente les réveils de battement cardiaque ou les continuations de tour d'agent routées. Elle ne reconstruit plus le contexte de livraison à partir de
  l'ombre JSON de session-entry.
- La résolution de contexte de la passerelle `tools.effective` lit maintenant les lignes de livraison/routage SQLite typées
  pour les entrées de fournisseur, compte, cible, thread et mode de réponse. Elle ne récupère plus ces champs de routage à chaud
  à partir des ombres `session_entries.entry_json` origin obsolètes.
- Le routage de consultation vocale en temps réel résout maintenant la livraison parent/appel à partir des lignes de session SQLite par agent typées. Elle ne revient plus aux ombres de compatibilité
  `SessionEntry.deliveryContext` lors du choix de la route de message d'agent intégré.
- Le relais de battement cardiaque de spawn ACP et le routage de flux parent lisent maintenant la livraison parent
  à partir des lignes de session SQLite typées. Ils ne reconstruisent plus le contexte de livraison parent
  à partir des ombres de session-entry de compatibilité.
- La préservation de route de livraison de session suit maintenant les métadonnées de chat typées et les colonnes de livraison persistées. Elle ne tire plus les indices de canal, les marqueurs direct/principal ou la forme de thread
  à partir de `sessionKey` ; les routes webchat internes héritent uniquement d'une cible externe lorsque SQLite a déjà
  l'identité de livraison typée/persistée pour la session.
- L'extraction de livraison de session générique lit maintenant uniquement la ligne de livraison de session SQLite typée exacte. Elle ne parse plus les suffixes de thread/sujet ou ne revient
  d'une clé en forme de thread à une clé de session de base.
- La dispatch de réponse, la récupération de sentinelle de redémarrage et le routage de consultation vocale en temps réel
  utilisent maintenant les lignes de session/conversation SQLite typées exactes pour le routage de thread. Elles ne récupèrent plus les ids de thread ou le contexte de livraison de session de base
  en analysant les clés de session en forme de thread.
- La limitation d'historique PI intégré utilise maintenant la projection de routage de session SQLite typée
  (`sessions` + `conversations` primaire) pour le fournisseur, le type de chat et l'identité de pair. Elle ne parse plus le fournisseur, DM, groupe ou forme de thread
  à partir de `sessionKey`.
- L'inférence de livraison d'outil cron utilise maintenant la livraison explicite ou le contexte de livraison typé actuel uniquement. Elle ne décode plus le canal, le pair, le compte ou les cibles de thread
  à partir de `agentSessionKey`.
- Les lignes de session d'exécution ne portent plus l'ancien alias de route `lastProvider`.
  Les assistants et les tests utilisent les champs typés `lastChannel` et `deliveryContext` ;
  la migration du docteur est le seul endroit qui devrait traduire les anciens alias de route
  ou les ombres `origin` persistées.
- Les événements de transcription, les lignes VFS et les lignes d'artefact d'outil écrivent maintenant dans la base de données par agent. La table de mappage de fichier de transcription globale non expédiée est partie ;
  le docteur enregistre les chemins source hérités dans les lignes de migration durables à la place.
- La recherche de transcription d'exécution ne scanne plus les décalages d'octet JSONL ou ne sonde les fichiers de transcription hérités. Les chemins de chat/média/historique de la passerelle lisent les lignes de transcription à partir de SQLite ;
  la JSONL de session est maintenant uniquement une entrée du docteur hérité, pas un état d'exécution ou un format d'exportation.
- Les relations parent et branche de transcription utilisent les métadonnées structurées
  `parentTranscriptScope: {agentId, sessionId}` dans les en-têtes de transcription SQLite, pas les chaînes de localisateur `agent-db:...transcript_events...`.
- Le contrat du gestionnaire de transcription n'expose plus les constructeurs implicites persistés
  `create(cwd)` ou `continueRecent(cwd)`. Les gestionnaires de transcription persistés sont ouverts avec une portée explicite `{agentId, sessionId}` ;
  seuls les gestionnaires en mémoire restent sans portée pour les tests et les transformations de transcription pures.
- Les API de magasin de transcription d'exécution résolvent la portée SQLite, pas les chemins du système de fichiers. L'ancien
  assistant `resolve...ForPath` et les options d'écriture `transcriptPath` inutilisées
  sont partis des appelants d'exécution.
- La résolution de session d'exécution utilise maintenant `{agentId, sessionId}` et ne doit pas dériver
  les chaînes `sqlite-transcript://<agent>/<session>` pour les limites externes.
  Les chemins JSONL absolus hérités sont des entrées de migration docteur uniquement.
- Les enregistrements de pont direct de relais de crochet natif vivent maintenant dans les lignes `native_hook_relay_bridges` partagées typées
  indexées par id de relais. L'exécution n'écrit plus un registre JSON `/tmp` ou des enregistrements génériques opaques pour ces enregistrements de pont de courte durée.
- `runEmbeddedPiAgent(...)` n'a plus de paramètre de localisateur de transcription.
  Les descripteurs de worker préparés omettent également les localisateurs de transcription. L'état de session d'exécution et les exécutions de suivi en file d'attente portent `{agentId, sessionId}`
  au lieu des poignées de transcription dérivées.
- La compaction intégrée prend maintenant la portée SQLite à partir de `agentId` et `sessionId`.
  Les crochets de compaction, les appels du moteur de contexte, la délégation CLI et les réponses de protocole
  ne doivent pas recevoir les poignées `sqlite-transcript://...` dérivées. Le code d'exportation/débogage
  peut matérialiser les artefacts utilisateur explicites à partir des lignes, mais il ne fournit pas
  un chemin d'exportation JSONL de session générique ou ne réalimente les noms de fichier dans l'identité d'exécution.
- `/export-session` lit les lignes de transcription à partir de SQLite et écrit uniquement la vue HTML autonome demandée. Le visualiseur intégré ne reconstruit plus ou ne télécharge la JSONL de session à partir de ces lignes.
- La délégation du moteur de contexte ne parse plus un localisateur de transcription pour récupérer l'identité de l'agent. Le contexte d'exécution préparé porte le `agentId` résolu
  dans l'adaptateur de compaction intégré.
- La réécriture de transcription et la troncature de résultat d'outil en direct lisent et persistent maintenant
  l'état de transcription par `{agentId, sessionId}` et ne dérivaient pas les localisateurs temporaires
  pour les charges utiles d'événement de mise à jour de transcription.
- La surface d'assistant d'état de transcription n'a plus les variantes basées sur le localisateur
  `readTranscriptState`, `replaceTranscriptStateEvents` ou
  `persistTranscriptStateMutation`. Les appelants d'exécution doivent utiliser les API `{agentId, sessionId}`. L'importation du docteur lit les fichiers hérités par chemin de fichier explicite et écrit les lignes SQLite ;
  elle ne migre pas les chaînes de localisateur.
- Le contrat du gestionnaire de session d'exécution n'expose plus `open(locator)`,
  `forkFrom(locator)` ou `setTranscriptLocator(...)`. Les gestionnaires de session persistés ouvrent par `{agentId, sessionId}` uniquement ;
  les assistants de liste/fork vivent sur les API de session et de point de contrôle orientées lignes au lieu de la façade du gestionnaire de transcription.
- Les API de lecteur de transcription de la passerelle sont d'abord délimitées. Elles prennent
  `{agentId, sessionId}` et n'acceptent pas un localisateur de transcription positionnel qui
  pourrait accidentellement devenir l'identité d'exécution. L'analyse active du localisateur de transcription est partie ;
  les chemins source hérités sont lus uniquement par le code d'importation du docteur.
- Les événements de mise à jour de transcription sont également d'abord délimités. `emitSessionTranscriptUpdate`
  n'accepte plus une chaîne de localisateur nue, et les écouteurs routent par
  `{agentId, sessionId}` sans analyser une poignée.
- La diffusion de message de session de la passerelle résout les clés de session à partir de la portée d'agent/session,
  pas à partir d'un localisateur de transcription. L'ancien résolveur/cache de localisateur de transcription vers clé de session est parti.
- Les filtres SSE d'historique de session de la passerelle mettent à jour les mises à jour en direct par portée d'agent/session. Elle ne canonicalise plus les candidats de localisateur de transcription, les chemins réels ou les identités de transcription en forme de fichier
  pour décider si un flux doit recevoir une mise à jour.
- Les crochets de cycle de vie de session ne dérivaient plus ou n'exposaient les localisateurs de transcription sur
  `session_end`. Les consommateurs de crochet obtiennent `sessionId`, `sessionKey`, les ids de session suivante et le contexte d'agent ;
  les fichiers de transcription ne font pas partie du contrat de cycle de vie.
- Les crochets de réinitialisation ne dérivaient plus ou n'exposaient les localisateurs de transcription non plus. La charge utile `before_reset`
  porte les messages SQLite récupérés plus la raison de la réinitialisation, tandis que l'identité de session reste dans le contexte du crochet.
- La réinitialisation du harnais d'agent n'accepte plus un localisateur de transcription. La dispatch de réinitialisation
  est délimitée par `sessionId`/`sessionKey` plus la raison.
- Les types de session d'extension d'agent n'exposent plus `transcriptLocator` ;
  les extensions doivent utiliser le contexte de session et les API d'exécution plutôt que de chercher une identité de transcription en forme de fichier.
- Les crochets de compaction de plugin n'exposent plus les localisateurs de transcription. Le contexte du crochet
  porte déjà l'identité de session, et les lectures de transcription doivent passer par les API conscientes de la portée SQLite
  au lieu des poignées en forme de fichier.
- Les crochets `before_agent_finalize` n'exposent plus `transcriptPath`, y compris
  les charges utiles de relais de crochet natif. Les crochets de finalisation utilisent uniquement le contexte de session.
- Les réponses de réinitialisation de la passerelle ne synthétisent plus un localisateur de transcription sur
  l'entrée retournée. La réinitialisation crée les lignes de transcription SQLite, retourne l'entrée de session propre et laisse l'accès à la transcription
  aux lecteurs conscients de la portée.
- Les résultats d'exécution intégrés et de compaction ne surfacent plus les localisateurs de transcription pour la comptabilité de session. La compaction automatique met à jour uniquement le `sessionId` actif,
  les compteurs de compaction et les métadonnées de jeton.
- Les résultats de tentative intégrés ne retournent plus `transcriptLocatorUsed`, et
  les résultats du moteur de contexte `compact()` ne retournent plus les localisateurs de transcription.
  Les boucles de tentative d'exécution acceptent uniquement un `sessionId` successeur.
- Les résultats d'ajout de transcription de miroir de livraison ne retournent plus les localisateurs de transcription. Les appelants obtiennent le `messageId` ajouté ;
  les signaux de mise à jour de transcription utilisent la portée SQLite.
- Les assistants de fork de session parent retournent uniquement le `sessionId` forké. La préparation de sous-agent
  passe la portée d'agent/session enfant aux moteurs.
- Les paramètres du runner CLI et la réensemencement d'historique n'acceptent plus les localisateurs de transcription.
  La lecture d'historique CLI résout la portée de transcription SQLite à partir de `{agentId,
sessionId}` et du contexte de clé de session.
- Les fixtures de test du runner CLI et intégré ensemencent et lisent maintenant les lignes de transcription SQLite
  par id de session au lieu de prétendre que les sessions actives sont des fichiers `*.jsonl` ou
  de passer une chaîne `sqlite-transcript://...` via les paramètres d'exécution.
- Les événements de garde de résultat d'outil de session émettent à partir de la portée de session connue même lorsqu'un
  gestionnaire en mémoire n'a pas de localisateur dérivé. Ses tests ne simulent plus les fichiers de transcription `/tmp/*.jsonl` actifs.
- Les assistants BTW et de point de contrôle de compaction lisent et forquent maintenant les lignes de transcription par
  portée SQLite. Les métadonnées de point de contrôle stockent maintenant uniquement les ids de session et les ids de feuille/entrée ;
  les localisateurs dérivés ne sont plus écrits dans les charges utiles de point de contrôle.
- La recherche de clé de transcription de la passerelle utilise la portée de transcription SQLite aux limites de protocole
  et ne réalise plus ou ne stats les noms de fichier de transcription.
- La rotation de transcription de compaction automatique écrit les lignes de transcription successeur directement via le magasin de transcription SQLite. Les lignes de session gardent uniquement l'identité de session successeur, pas un chemin JSONL durable ou un localisateur persisté.
- La compaction du moteur de contexte intégré utilise les assistants de rotation de transcription nommés SQLite. Les tests de rotation ne construisent plus les chemins successeur JSONL ou
  ne modélisent les sessions actives comme des fichiers.
- La rétention d'image sortante gérée indexe son cache de message de transcription à partir des statistiques de transcription SQLite
  au lieu des appels stat du système de fichiers.
- Les verrous de session d'exécution et la voie du docteur `.jsonl.lock` autonome hérité ont été supprimés.
- Le baril d'exécution Microsoft Teams et la surface SDK de plugin public ne réexportent plus
  l'ancien assistant de verrou de fichier ; les chemins d'état de plugin durable sont soutenues par SQLite.
- L'élagage de l'âge/du nombre de session et le nettoyage de session explicite ont été supprimés.
  Le docteur possède l'importation héritée ; les sessions obsolètes sont réinitialisées ou supprimées explicitement.
- Les vérifications d'intégrité du docteur ne comptent plus un fichier JSONL hérité comme une transcription active valide pour une ligne de session SQLite. La santé de transcription active est SQLite uniquement ;
  les fichiers JSONL hérités sont signalés comme entrées de migration/nettoyage orphelin.
- Le docteur ne traite plus `agents/<agent>/sessions/` comme un état d'exécution requis. Il scanne uniquement ce répertoire lorsqu'il existe déjà, comme entrée de migration héritée
  ou de nettoyage orphelin.
- La passerelle `sessions.resolve`, les chemins de correctif/réinitialisation/compaction de session, la génération de sous-agent, l'avortement rapide, les métadonnées ACP et le correctif TUI
  ne migrent plus ou n'élaguent les clés de session héritées comme effet secondaire du travail d'exécution normal.
- La résolution de session de commande CLI retourne maintenant le `agentId` propriétaire au lieu d'un
  `storePath`, et elle ne copie plus les lignes de session principale héritées pendant la résolution normale
  `--to` ou `--session-id`. La canonicalisation de ligne principale héritée appartient au docteur uniquement.
- La résolution de profondeur de sous-agent d'exécution ne lit plus `sessions.json` ou les magasins de session JSON5. Elle lit `session_entries` SQLite par id d'agent, et les métadonnées de profondeur/session héritées
  ne peuvent entrer que via le chemin d'importation du docteur.
- Les remplacements de session de profil d'authentification persistent via les upserts de ligne `{agentId, sessionKey}` directs
  au lieu du chargement paresseux d'un magasin de session en forme de fichier d'exécution.
- La porte de réponse automatique verbale et les assistants de mise à jour de session lisent/upsert maintenant les lignes de session SQLite par identité de session
  et ne nécessitent plus un chemin de magasin hérité avant de toucher l'état de ligne persisté.
- Les assistants de métadonnées de session d'exécution de commande utilisent maintenant les noms orientés entrée et les chemins de module ;
  la surface d'assistant de commande `session-store` hérité a été supprimée.
- L'ensemencement d'en-tête d'amorçage et le durcissement de limite de compaction manuel mutent maintenant les lignes de transcription SQLite directement. Les appelants d'exécution passent l'identité de session, pas les chemins `.jsonl` inscriptibles.
- La relecture de rotation de session silencieuse copie les tours utilisateur/assistant récents par
  `{agentId, sessionId}` à partir des lignes de transcription SQLite. Elle n'accepte plus
  les localisateurs de transcription source ou cible.
- Les nouvelles lignes de session d'exécution persistées ne stockent plus les localisateurs de transcription. Les appelants utilisent
  `{agentId, sessionId}` directement ; les commandes d'exportation/débogage peuvent choisir les noms de fichier de sortie lorsqu'elles matérialisent les lignes.
- Le démarrage d'une nouvelle session de transcription persistée ouvre maintenant toujours les lignes SQLite par
  portée. Le gestionnaire de session ne réutilise plus un chemin de transcription d'ère de fichier précédent ou un localisateur comme l'identité
  de la nouvelle session.
- Les sessions de transcription persistées utilisent l'API explicite
  `openTranscriptSessionManagerForSession({agentId, sessionId})`. Les anciennes façades statiques `SessionManager.create/openForSession/list/forkFromSession` sont
  parties afin que les tests et le code d'exécution ne puissent pas accidentellement recréer la découverte de session d'ère de fichier.
- L'exécution de plugin n'expose plus `api.runtime.agent.session.resolveTranscriptLocatorPath` ;
  le code de plugin utilise les assistants de ligne SQLite et les valeurs de portée.
- La surface SDK publique `session-store-runtime` exporte maintenant uniquement les assistants de ligne de session
  et de ligne de transcription. Les assistants d'ouverture/fermeture/réinitialisation de base de données SQLite brute et de chemin vivent dans la surface SDK `sqlite-runtime` ciblée,
  afin que les tests de plugin ne tirent plus le baril de test large dépréciée pour le nettoyage de base de données.
- Les classificateurs de nom de fichier de trajectoire `.jsonl` et de point de contrôle hérités vivent maintenant dans le module de fichier de session hérité du docteur. La validation de session principale n'importe plus
  les assistants d'artefact de fichier pour décider les ids de session SQLite normaux.
- Les exécutions de sous-agent de blocage de mémoire active utilisent maintenant les lignes de transcription SQLite au lieu de créer
  des fichiers `session.jsonl` temporaires ou persistés sous l'état du plugin. L'ancienne option `transcriptDir` est supprimée.
- La génération de slug unique et les exécutions du planificateur Crestodian utilisent les lignes de transcription SQLite
  au lieu de créer des fichiers `session.jsonl` temporaires.
- Les exécutions d'assistant `llm-task` et l'extraction d'engagement cachée utilisent également les lignes de transcription SQLite,
  afin que ces sessions d'assistant de modèle uniquement ne créent plus les fichiers de transcription JSON/JSONL temporaires.
- `TranscriptSessionManager` est maintenant uniquement une portée de transcription SQLite ouverte.
  Le code d'exécution l'ouvre avec `openTranscriptSessionManagerForSession({agentId,
sessionId})` ; les flux de création, branche, continuation, liste et fork vivent dans leurs
  assistants de ligne SQLite propriétaires plutôt que les façades du gestionnaire statique.
  Le code du docteur/importation/débogage gère les fichiers source hérités explicites en dehors du
  gestionnaire de session d'exécution.
- Les méthodes de façade `SessionManager.newSession()` et
  `SessionManager.createBranchedSession()` obsolètes ont été supprimées. Les nouvelles sessions et les descendants de transcription
  sont créés par leur flux de travail SQLite propriétaire au lieu de muter un gestionnaire déjà ouvert
  dans une session persistée différente.
- Les assistants de décision de fork de transcription parent et de création de fork n'acceptent plus
  `storePath` ou `sessionsDir` ; ils utilisent la portée de transcription SQLite `{agentId, sessionId}` au lieu
  des métadonnées de chemin du système de fichiers retenues.
- L'hôte mémoire n'exporte plus les assistants de classification de répertoire de transcription sans opération ;
  le filtrage de transcription dérive maintenant des métadonnées de ligne SQLite lors de la construction d'entrée.
- L'hôte mémoire et les tests d'exportation de session QMD utilisent les portées de transcription SQLite. Les anciens chemins `agents/<agentId>/sessions/*.jsonl`
  restent couverts uniquement lorsqu'un test prouve intentionnellement la compatibilité du docteur/importation/exportation.
- L'inspection de session brute QA-lab utilise maintenant `sessions.list` via la passerelle
  au lieu de lire `agents/qa/sessions/sessions.json` ; les commentaires MSteams s'ajoutent directement aux transcriptions SQLite
  sans fabriquer un chemin JSONL.
- Les tours de canal entrant partagé portent maintenant `{agentId, sessionKey}` plutôt qu'un
  `storePath` hérité. Les chemins d'enregistrement LINE, WhatsApp, Slack, Discord, Telegram, Matrix, Signal,
  iMessage, BlueBubbles, Feishu, Google Chat, IRC, Nextcloud Talk, Zalo,
  Zalo Personal, QA Channel, Microsoft Teams, Mattermost, Synology Chat, Tlon,
  Twitch et QQBot lisent maintenant les métadonnées mises à jour et enregistrent les lignes de session entrante via

## Forme du schéma cible

Gardez les schémas explicites. L'état d'exécution détenu par l'hôte utilise des tables typées. L'état opaque détenu par le plugin utilise `plugin_state_entries` / `plugin_blob_entries` ; il n'y a pas de table générique `kv` pour l'hôte.

Base de données globale :

```text
state_leases(scope, lease_key, owner, expires_at, heartbeat_at, payload_json, created_at, updated_at)
exec_approvals_config(config_key, raw_json, socket_path, has_socket_token, default_security, default_ask, default_ask_fallback, auto_allow_skills, agent_count, allowlist_count, updated_at_ms)
schema_meta(meta_key, role, schema_version, agent_id, app_version, created_at, updated_at)
agent_databases(agent_id, path, schema_version, last_seen_at, size_bytes)
task_runs(...)
task_delivery_state(...)
flow_runs(...)
subagent_runs(run_id, child_session_key, requester_session_key, controller_session_key, created_at, ended_at, cleanup_handled, payload_json)
current_conversation_bindings(binding_key, binding_id, target_agent_id, target_session_id, target_session_key, channel, account_id, conversation_kind, parent_conversation_id, conversation_id, target_kind, status, bound_at, expires_at, metadata_json, updated_at)
plugin_binding_approvals(plugin_root, channel, account_id, plugin_id, plugin_name, approved_at)
tui_last_sessions(scope_key, session_key, updated_at)
plugin_state_entries(plugin_id, namespace, entry_key, value_json, created_at, expires_at)
plugin_blob_entries(plugin_id, namespace, entry_key, metadata_json, blob, created_at, expires_at)
media_blobs(subdir, id, content_type, size_bytes, blob, created_at, updated_at)
skill_uploads(upload_id, kind, slug, force, size_bytes, sha256, actual_sha256, received_bytes, archive_blob, created_at, expires_at, committed, committed_at, idempotency_key_hash)
web_push_subscriptions(endpoint_hash, subscription_id, endpoint, p256dh, auth, created_at_ms, updated_at_ms)
web_push_vapid_keys(key_id, public_key, private_key, subject, updated_at_ms)
apns_registrations(node_id, transport, token, relay_handle, send_grant, installation_id, topic, environment, distribution, token_debug_suffix, updated_at_ms)
node_host_config(config_key, version, node_id, token, display_name, gateway_host, gateway_port, gateway_tls, gateway_tls_fingerprint, updated_at_ms)
device_identities(identity_key, device_id, public_key_pem, private_key_pem, created_at_ms, updated_at_ms)
device_auth_tokens(device_id, role, token, scopes_json, updated_at_ms)
macos_port_guardian_records(pid, port, command, mode, timestamp)
workspace_setup_state(workspace_key, workspace_path, version, bootstrap_seeded_at, setup_completed_at, updated_at)
native_hook_relay_bridges(relay_id, pid, hostname, port, token, expires_at_ms, updated_at_ms)
model_capability_cache(provider_id, model_id, name, input_text, input_image, reasoning, supports_tools, context_window, max_tokens, cost_input, cost_output, cost_cache_read, cost_cache_write, updated_at_ms)
agent_model_catalogs(catalog_key, agent_dir, raw_json, updated_at)
managed_outgoing_image_records(attachment_id, session_key, message_id, created_at, updated_at, retention_class, alt, original_media_id, original_media_subdir, original_content_type, original_width, original_height, original_size_bytes, original_filename, record_json)
gateway_restart_sentinel(sentinel_key, version, kind, status, ts, session_key, thread_id, delivery_channel, delivery_to, delivery_account_id, message, continuation_json, doctor_hint, stats_json, payload_json, updated_at_ms)
channel_pairing_requests(channel_key, account_id, request_id, code, created_at, last_seen_at, meta_json)
channel_pairing_allow_entries(channel_key, account_id, entry, sort_order, updated_at)
voicewake_triggers(config_key, position, trigger, updated_at_ms)
voicewake_routing_config(config_key, version, default_target_mode, default_target_agent_id, default_target_session_key, updated_at_ms)
voicewake_routing_routes(config_key, position, trigger, target_mode, target_agent_id, target_session_key, updated_at_ms)
update_check_state(state_key, last_checked_at, last_notified_version, last_notified_tag, last_available_version, last_available_tag, auto_install_id, auto_first_seen_version, auto_first_seen_tag, auto_first_seen_at, auto_last_attempt_version, auto_last_attempt_at, auto_last_success_version, auto_last_success_at, updated_at_ms)
config_health_entries(config_path, last_known_good_json, last_promoted_good_json, last_observed_suspicious_signature, updated_at_ms)
sandbox_registry_entries(registry_kind, container_name, session_key, backend_id, runtime_label, image, created_at_ms, last_used_at_ms, config_label_kind, config_hash, cdp_port, no_vnc_port, entry_json, updated_at)
cron_run_logs(store_key, job_id, seq, ts, status, error, summary, diagnostics_summary, delivery_status, delivery_error, delivered, session_id, session_key, run_id, run_at_ms, duration_ms, next_run_at_ms, model, provider, total_tokens, entry_json, created_at)
cron_jobs(store_key, job_id, name, description, enabled, delete_after_run, created_at_ms, agent_id, session_key, schedule_kind, schedule_expr, schedule_tz, every_ms, anchor_ms, at, stagger_ms, session_target, wake_mode, payload_kind, payload_message, payload_model, payload_fallbacks_json, payload_thinking, payload_timeout_seconds, payload_allow_unsafe_external_content, payload_external_content_source_json, payload_light_context, payload_tools_allow_json, delivery_mode, delivery_channel, delivery_to, delivery_thread_id, delivery_account_id, delivery_best_effort, failure_delivery_mode, failure_delivery_channel, failure_delivery_to, failure_delivery_account_id, failure_alert_disabled, failure_alert_after, failure_alert_channel, failure_alert_to, failure_alert_cooldown_ms, failure_alert_include_skipped, failure_alert_mode, failure_alert_account_id, next_run_at_ms, running_at_ms, last_run_at_ms, last_run_status, last_error, last_duration_ms, consecutive_errors, consecutive_skipped, schedule_error_count, last_delivery_status, last_delivery_error, last_delivered, last_failure_alert_at_ms, job_json, state_json, runtime_updated_at_ms, schedule_identity, sort_order, updated_at)
delivery_queue_entries(queue_name, id, status, entry_kind, session_key, channel, target, account_id, retry_count, last_attempt_at, last_error, recovery_state, platform_send_started_at, entry_json, enqueued_at, updated_at, failed_at)
commitments(id, agent_id, session_key, channel, account_id, recipient_id, thread_id, sender_id, kind, sensitivity, source, status, reason, suggested_text, dedupe_key, confidence, due_earliest_ms, due_latest_ms, due_timezone, source_message_id, source_run_id, created_at_ms, updated_at_ms, attempts, last_attempt_at_ms, sent_at_ms, dismissed_at_ms, snoozed_until_ms, expired_at_ms, record_json)
migration_runs(id, started_at, finished_at, status, report_json)
migration_sources(source_key, migration_kind, source_path, target_table, source_sha256, source_size_bytes, source_record_count, last_run_id, status, imported_at, removed_source, report_json)
backup_runs(id, created_at, archive_path, status, manifest_json)
```

Base de données d'agent :

```text
schema_meta(meta_key, role, schema_version, agent_id, app_version, created_at, updated_at)
sessions(session_id, session_key, session_scope, created_at, updated_at, started_at, ended_at, status, chat_type, channel, account_id, primary_conversation_id, model_provider, model, agent_harness_id, parent_session_key, spawned_by, display_name)
conversations(conversation_id, channel, account_id, kind, peer_id, parent_conversation_id, thread_id, native_channel_id, native_direct_user_id, label, metadata_json, created_at, updated_at)
session_conversations(session_id, conversation_id, role, first_seen_at, last_seen_at)
session_routes(session_key, session_id, updated_at)
session_entries(session_id, session_key, entry_json, updated_at)
transcript_events(session_id, seq, event_json, created_at)
transcript_event_identities(session_id, event_id, seq, event_type, has_parent, parent_id, message_idempotency_key, created_at)
transcript_snapshots(session_id, snapshot_id, reason, event_count, created_at, metadata_json)
vfs_entries(namespace, path, kind, content_blob, metadata_json, updated_at)
tool_artifacts(run_id, artifact_id, kind, metadata_json, blob, created_at)
run_artifacts(run_id, path, kind, metadata_json, blob, created_at)
trajectory_runtime_events(session_id, run_id, seq, event_json, created_at)
memory_index_meta(meta_key, schema_version, provider, model, provider_key, sources_json, scope_hash, chunk_tokens, chunk_overlap, vector_dims, fts_tokenizer, config_hash, updated_at)
memory_index_sources(source_kind, source_key, path, session_id, hash, mtime, size)
memory_index_chunks(id, source_kind, source_key, path, session_id, start_line, end_line, hash, model, text, embedding, embedding_dims, updated_at)
memory_embedding_cache(provider, model, provider_key, hash, embedding, dims, updated_at)
cache_entries(scope, key, value_json, blob, expires_at, updated_at)
```

La recherche future peut ajouter des tables FTS sans modifier les tables d'événements canoniques :

```text
transcript_events_fts(session_id, seq, text)
vfs_entries_fts(namespace, path, text)
```

Les grandes valeurs doivent utiliser des colonnes `blob`, pas l'encodage de chaîne JSON. Conservez `value_json` pour les petites données structurées qui doivent rester inspectables avec les outils SQLite ordinaires.

`agent_databases` est le registre canonique pour cette branche. N'ajoutez pas de table `agents` jusqu'à ce qu'un véritable propriétaire d'enregistrement d'agent existe ; la configuration d'agent reste dans `openclaw.json`.

## Forme de migration Doctor

Doctor doit appeler une étape de migration explicite qui est signalable et sûre à réexécuter :

```bash
openclaw doctor --fix
```

`openclaw doctor --fix` invoque l'implémentation de migration d'état après le contrôle de préflight de configuration ordinaire et crée une sauvegarde vérifiée avant l'importation. Le démarrage du runtime et `openclaw migrate` ne doivent pas importer les fichiers d'état OpenClaw hérités.

Propriétés de migration :

- Une passe de migration découvre tous les sources de fichiers hérités et produit un plan avant de modifier quoi que ce soit.
- Doctor crée une archive de sauvegarde pré-migration vérifiée avant d'importer les fichiers hérités.
- Les importations sont idempotentes et clés par chemin source, mtime, taille, hash et table cible.
- Les fichiers sources réussis sont supprimés ou archivés après que la base de données cible ait validé.
- Les importations échouées laissent la source intacte et enregistrent un avertissement dans `migration_runs`.
- Le code runtime lit SQLite uniquement après l'existence de la migration.
- Aucun chemin de rétrogradation/export-vers-fichiers-runtime n'est requis.

## Inventaire de Migration

Déplacez ces éléments dans la base de données globale :

- Les écritures runtime du registre de tâches utilisent désormais la base de données partagée ; l'importateur de fichier sidecar non expédié `tasks/runs.sqlite` est supprimé. Les sauvegardes d'instantané effectuent un upsert par ID de tâche et suppriment uniquement les lignes de tâche/livraison manquantes.
- Les écritures runtime du flux de tâches utilisent désormais la base de données partagée ; l'importateur de fichier sidecar non expédié `tasks/flows/registry.sqlite` est supprimé. Les sauvegardes d'instantané effectuent un upsert par ID de flux et suppriment uniquement les lignes de flux manquantes.
- Les écritures runtime de l'état du plugin utilisent désormais la base de données partagée ; l'importateur de fichier sidecar non expédié `plugin-state/state.sqlite` est supprimé.
- La recherche en mémoire intégrée ne prend plus par défaut `memory/<agentId>.sqlite` ; ses tables d'index se trouvent dans la base de données de l'agent propriétaire, et l'opt-in sidecar explicite `memorySearch.store.path` a été retiré vers la migration de configuration du docteur.
- La réindexation de la mémoire intégrée réinitialise uniquement les tables appartenant à la mémoire dans la base de données de l'agent. Elle ne doit pas remplacer l'intégralité du fichier SQLite, car la même base de données possède les sessions, les transcriptions, les lignes VFS, les artefacts et les caches runtime.
- Les registres de conteneur/navigateur sandbox à partir de JSON monolithique et fragmenté. Les écritures runtime utilisent désormais la base de données partagée ; l'importation JSON héritée reste.
- Les définitions de travaux cron, l'état de la planification et l'historique des exécutions utilisent désormais SQLite partagé ; le docteur importe/supprime les fichiers hérités `jobs.json`, `jobs-state.json` et `cron/runs/*.jsonl`
- Identité/authentification de l'appareil, push, vérification des mises à jour, engagements, cache du modèle OpenRouter, index des plugins installés et liaisons serveur d'application
- L'appairage appareil/nœud et les enregistrements d'amorçage utilisent désormais des tables SQLite typées
- Les abonnés aux notifications d'appairage d'appareil et les marqueurs de demande livrée utilisent désormais la table plugin-state SQLite partagée au lieu de `device-pair-notify.json`.
- Les enregistrements d'appels vocaux utilisent désormais la table plugin-state SQLite partagée sous l'espace de noms `voice-call` / `calls` au lieu de `calls.jsonl` ; la CLI du plugin suit et résume l'historique des appels sauvegardé par SQLite.
- Les sessions de passerelle QQBot, les enregistrements d'utilisateurs connus et le cache d'index de citation utilisent désormais l'état du plugin SQLite sous les espaces de noms `qqbot` (`sessions`, `known-users`, `ref-index`) au lieu de `session-*.json`, `known-users.json` et `ref-index.jsonl` ; la migration du docteur/setup QQBot importe et supprime les fichiers hérités.
- Les préférences du sélecteur de modèle Discord, les hachages de déploiement de commande et les liaisons de thread utilisent désormais l'état du plugin SQLite sous les espaces de noms `discord` (`model-picker-preferences`, `command-deploy-hashes`, `thread-bindings`) au lieu de `model-picker-preferences.json`, `command-deploy-cache.json` et `thread-bindings.json` ; la migration du docteur/setup Discord importe et supprime les fichiers hérités.
- Les curseurs de rattrapage BlueBubbles et les marqueurs de déduplications entrantes utilisent désormais l'état du plugin SQLite sous les espaces de noms `bluebubbles` (`catchup-cursors`, `inbound-dedupe`) au lieu de `bluebubbles/catchup/*.json` et `bluebubbles/inbound-dedupe/*.json` ; la migration du docteur/setup BlueBubbles importe et supprime les fichiers hérités.
- Les décalages de mise à jour Telegram, les entrées du cache des autocollants, les entrées du cache des messages de chaîne de réponse, les entrées du cache des messages envoyés, les entrées du cache des noms de sujets et les liaisons de thread utilisent désormais l'état du plugin SQLite sous les espaces de noms `telegram` (`update-offsets`, `sticker-cache`, `message-cache`, `sent-messages`, `topic-names`, `thread-bindings`) au lieu de `update-offset-*.json`, `sticker-cache.json`, `*.telegram-messages.json`, `*.telegram-sent-messages.json`, `*.telegram-topic-names.json` et `thread-bindings-*.json` ; la migration du docteur/setup Telegram importe et supprime les fichiers hérités.
- Les curseurs de rattrapage iMessage, les mappages d'ID court de réponse et les lignes de déduplications d'écho envoyé utilisent désormais l'état du plugin SQLite sous les espaces de noms `imessage` (`catchup-cursors`, `reply-cache`, `sent-echoes`) au lieu de `imessage/catchup/*.json`, `imessage/reply-cache.jsonl` et `imessage/sent-echoes.jsonl` ; la migration du docteur/setup iMessage importe et supprime les fichiers hérités.
- Les conversations Microsoft Teams, les sondages, les jetons délégués, les téléchargements en attente et les apprentissages de rétroaction utilisent désormais les espaces de noms plugin-state/blob SQLite (`conversations`, `polls`, `delegated-tokens`, `pending-uploads`, `feedback-learnings`) au lieu de `msteams-conversations.json`, `msteams-polls.json`, `msteams-delegated.json`, `msteams-pending-uploads.json` et `*.learnings.json` ; la migration du docteur/setup Microsoft Teams importe et supprime les fichiers hérités.
- Le cache de synchronisation Matrix, les métadonnées de stockage, les liaisons de thread, les marqueurs de déduplications entrantes, l'état du délai de vérification au démarrage, les identifiants, les clés de récupération et les instantanés crypto IndexedDB du SDK utilisent désormais les espaces de noms plugin-state/blob SQLite sous `matrix` (`sync-store`, `storage-meta`, `thread-bindings`, `inbound-dedupe`, `startup-verification`, `credentials`, `recovery-key`, `idb-snapshots`) au lieu de `bot-storage.json`, `storage-meta.json`, `thread-bindings.json`, `inbound-dedupe.json`, `startup-verification.json`, `credentials.json`, `recovery-key.json` et `crypto-idb-snapshot.json` ; la migration du docteur/setup Matrix importe et supprime ces fichiers hérités à partir des racines de stockage Matrix délimitées par compte.
- Les curseurs de bus Nostr et l'état de publication de profil utilisent désormais l'état du plugin SQLite sous les espaces de noms `nostr` (`bus-state`, `profile-state`) au lieu de `bus-state-*.json` et `profile-state-*.json` ; la migration du docteur/setup Nostr importe et supprime les fichiers hérités.
- Les bascules de session Active Memory utilisent désormais l'état du plugin SQLite sous `active-memory/session-toggles` au lieu de `session-toggles.json`.
- Les files d'attente de propositions Skill Workshop et les compteurs d'examen utilisent désormais l'état du plugin SQLite sous `skill-workshop/proposals` et `skill-workshop/reviews` au lieu des fichiers `skill-workshop/<workspace>.json` par espace de travail.
- Les files d'attente de livraison sortante et de livraison de session partagent désormais la table SQLite globale `delivery_queue_entries` sous des noms de file d'attente séparés (`outbound-delivery`, `session-delivery`) au lieu des fichiers durables `delivery-queue/*.json`, `delivery-queue/failed/*.json` et `session-delivery-queue/*.json`. L'étape legacy-state du docteur importe les lignes en attente et échouées, supprime les marqueurs livrés obsolètes et supprime les anciens fichiers JSON après l'importation. Les champs de routage à chaud et de nouvelle tentative sont des colonnes typées ; la charge utile JSON est conservée uniquement pour la relecture/débogage.
- Les baux de processus ACPX utilisent désormais l'état du plugin SQLite sous `acpx/process-leases` au lieu de `process-leases.json`.
- Métadonnées d'exécution de sauvegarde et de migration

Déplacez ces éléments dans les bases de données d'agent :

- Racines de session d'agent et charges utiles d'entrée de session de forme compatible. Effectué pour les écritures runtime : les métadonnées de session à chaud sont interrogeables dans `sessions`, tandis que la charge utile `SessionEntry` de forme héritée complète reste dans `session_entries`.
- Événements de transcription d'agent. Effectué pour les écritures runtime.
- Points de contrôle de compaction et instantanés de transcription. Effectué pour les écritures runtime : les copies de transcription de point de contrôle sont des lignes de transcription SQLite et les métadonnées de point de contrôle sont enregistrées dans `transcript_snapshots`. Les assistants de point de contrôle de passerelle nomment désormais ces valeurs comme des instantanés de transcription plutôt que des fichiers source.
- Espaces de noms VFS scratch/workspace d'agent. Effectué pour les écritures VFS runtime.
- Charges utiles de pièces jointes de sous-agent. Effectué pour les écritures runtime : ce sont des entrées de graine VFS SQLite et jamais des fichiers d'espace de travail durable.
- Artefacts d'outil. Effectué pour les écritures runtime.
- Artefacts d'exécution. Effectué pour les écritures runtime de worker via la table `run_artifacts` par agent.
- Caches runtime locaux à l'agent. Effectué pour les écritures de cache délimitées par worker via la table `cache_entries` par agent. Les caches de modèle à l'échelle de la passerelle restent dans la base de données globale sauf s'ils deviennent spécifiques à l'agent.
- Journaux de flux parent ACP. Effectué pour les écritures runtime.
- Sessions du registre de relecture ACP. Effectué pour les écritures runtime via `acp_replay_sessions` et `acp_replay_events` ; le fichier hérité `acp/event-ledger.json` reste uniquement comme entrée du docteur.
- Sidecars de trajectoire lorsqu'ils ne sont pas des fichiers d'exportation explicites. Effectué pour les écritures runtime : la capture de trajectoire écrit les lignes `trajectory_runtime_events` de la base de données d'agent et reflète les artefacts délimités par exécution dans SQLite. Les sidecars hérités sont uniquement des entrées d'importation du docteur ; l'exportation peut matérialiser des sorties de bundle de support JSONL fraîches mais ne lit ni ne migre pas les anciens sidecars de trajectoire/transcription au runtime. La capture de trajectoire runtime expose la portée SQLite ; les assistants de chemin JSONL sont isolés à l'exportation/débogage et ne sont pas réexportés à partir du module runtime. Les métadonnées de trajectoire du runner intégré enregistrent l'identité `{agentId, sessionId, sessionKey}` au lieu de persister un localisateur de transcription.

Conservez ces fichiers pour l'instant :

- `openclaw.json`
- Fichiers d'identifiants de fournisseur ou CLI
- Manifestes de plugin/package
- Espaces de travail utilisateur et référentiels Git lorsque le mode disque est sélectionné
- Journaux destinés à la surveillance par l'opérateur, sauf si une surface de journal spécifique est déplacée

## Plan de Migration

### Phase 0 : Geler la Limite

Rendre la limite de l'état durable explicite avant de déplacer plus de lignes :

- Ajouter une table `migration_runs` à la base de données globale.
  Fait pour les rapports d'exécution de migration d'état hérité.
- Ajouter un service de migration d'état unique appartenant au docteur pour l'importation fichier-vers-base de données.
  Fait : `openclaw doctor --fix` utilise l'implémentation de migration d'état hérité.
- Rendre `plan` en lecture seule et faire en sorte que `apply` crée une sauvegarde, importe, vérifie, puis supprime ou met en quarantaine les anciens fichiers.
  Fait : doctor crée une sauvegarde pré-migration vérifiée, transmet le chemin de sauvegarde dans `migration_runs`, et réutilise les chemins d'importation/suppression.
- Ajouter des interdictions statiques pour que le nouveau code runtime ne puisse pas écrire les fichiers d'état hérité tandis que le code de migration et les tests peuvent toujours les ensemencer/lire.
  Fait pour les magasins hérités actuellement migrés ; la garde analyse également les tests imbriqués pour les contrats de localisateur de transcription runtime interdits.

### Phase 1 : Terminer le Plan de Contrôle Global

Conserver l'état de coordination partagé dans `state/openclaw.sqlite` :

- Registre des agents et de la base de données des agents
- Registres des tâches et des flux de tâches
- État du plugin
- Registre des conteneurs/navigateurs sandbox
- Historique des exécutions Cron/planificateur
- Appairage, appareil, push, vérification de mise à jour, TUI, caches OpenRouter/modèle et autre état runtime limité à la passerelle
- Métadonnées de sauvegarde et de migration
- Octets de pièces jointes multimédias de la passerelle. Fait pour les écritures runtime ; les chemins de fichiers directs sont des matérialisations temporaires pour la compatibilité avec les expéditeurs de canaux et la mise en scène sandbox. Les listes blanches runtime acceptent les chemins de matérialisation SQLite, pas les racines multimédias d'état/config hérité. Doctor importe les fichiers multimédias hérités dans `media_blobs` et supprime les fichiers source après les écritures de lignes réussies.
- Sessions de capture de proxy de débogage, événements et blobs de charge utile. Fait : les captures vivent dans la base de données d'état partagée et s'ouvrent via les paramètres de bootstrap, schéma, WAL et busy-timeout de la base de données d'état partagée. Il n'y a pas de remplacement de base de données sidecar runtime de proxy de débogage, de répertoire de blobs ou de cible de schéma/codegen générée uniquement pour la capture de proxy.

Cette phase supprime également les ouvreurs sidecar en double, les aides aux permissions, la configuration WAL, l'élagage du système de fichiers et les rédacteurs de compatibilité de ces sous-systèmes.

### Phase 2 : Introduire des Bases de Données par Agent

Créer une base de données par agent et l'enregistrer à partir de la base de données globale :

```text
~/.openclaw/state/openclaw.sqlite
~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite
```

La ligne `agent_databases` globale stocke le chemin, la version du schéma, l'horodatage de la dernière visualisation et les métadonnées de base de taille/intégrité. Le code runtime demande le registre pour la base de données de l'agent au lieu de dériver directement les chemins de fichiers.

La base de données de l'agent possède :

- `sessions` comme racine de session canonique, avec `session_entries` comme table de charge utile en forme de compatibilité attachée à cette racine, et `session_routes` comme recherche unique de `session_key` active
- `conversations` et `session_conversations` comme identité de routage du fournisseur normalisée attachée aux sessions
- `transcript_events`
- instantanés de transcription et points de contrôle de compaction. Fait pour les écritures runtime.
- `vfs_entries`
- `tool_artifacts` et artefacts d'exécution
- lignes runtime/cache locales à l'agent. Fait pour les caches limités aux workers.
- Événements de flux parent ACP
- événements runtime de trajectoire lorsqu'ils ne sont pas des artefacts d'export explicites

### Phase 3 : Remplacer les API du Magasin de Sessions

Fait pour le runtime. La surface du magasin de sessions en forme de fichier n'est pas un contrat runtime actif :

- Le runtime n'appelle plus `loadSessionStore(storePath)` et ne traite pas `storePath` comme identité de session.
- Les opérations de lignes runtime sont `getSessionEntry`, `upsertSessionEntry`, `patchSessionEntry`, `deleteSessionEntry` et `listSessionEntries`.
- Les aides de réécriture de magasin entier, les rédacteurs de fichiers, les tests de file d'attente, l'élagage d'alias et les paramètres de suppression de clé hérité sont supprimés du runtime.
- Les exports de compatibilité du package racine dépréciés adaptent toujours les chemins canoniques `sessions.json` sur les API de lignes SQLite.
- L'analyse `sessions.json` reste uniquement dans le code de migration/importation du docteur et les tests du docteur.
- Le fallback du cycle de vie runtime lit les en-têtes de transcription SQLite, pas les premières lignes JSONL.

Continuez à supprimer tout ce qui réintroduit les paramètres de verrouillage de fichiers, le vocabulaire d'élagage/troncature-comme-maintenance-de-fichiers, l'identité du chemin du magasin ou les tests dont la seule assertion est la persistance JSON.

### Phase 4 : Déplacer les Transcriptions, les Flux ACP, les Trajectoires et le VFS

Rendre chaque flux de données d'agent natif à la base de données :

- Les écritures d'ajout de transcription passent par une transaction SQLite qui garantit l'en-tête de session, vérifie l'idempotence des messages, sélectionne la queue parent, insère dans `transcript_events` et enregistre les métadonnées d'identité interrogeables dans `transcript_event_identities`. Fait pour les ajouts de messages de transcription directs et les ajouts `TranscriptSessionManager` persistants normaux ; les opérations de branche explicites conservent leur choix de parent explicite et écrivent toujours les lignes SQLite sans dériver aucun localisateur de fichier.
- Les journaux de flux parent ACP deviennent des lignes, pas des fichiers `.acp-stream.jsonl`. Fait.
- La configuration de spawn ACP ne persiste plus les chemins JSONL de transcription. Fait.
- Les écritures de capture de trajectoire runtime écrivent directement les lignes d'événements/artefacts. La commande de support/export explicite peut toujours produire des artefacts JSONL de bundle de support comme format d'export, mais l'export de session ne recrée pas la session JSONL. Fait.
- Les espaces de travail disque restent sur disque lorsqu'ils sont configurés en mode disque.
- Le mode VFS scratch et le mode espace de travail VFS uniquement expérimental utilisent la base de données de l'agent.

La migration importe les anciens fichiers JSONL une fois, enregistre les comptes/hashes dans `migration_runs` et supprime les fichiers importés après les vérifications d'intégrité.

### Phase 5 : Sauvegarde, Restauration, Aspiration et Vérification

Les sauvegardes restent un fichier d'archive :

- Créer un point de contrôle pour chaque base de données globale et agent.
- Créer un instantané de chaque base de données avec la sémantique de sauvegarde SQLite ou `VACUUM INTO`.
- Archiver les instantanés de base de données compacts, la configuration, les identifiants externes et les exports d'espace de travail demandés.
- Omettre les fichiers `*.sqlite-wal` et `*.sqlite-shm` en direct.
- Vérifier en ouvrant chaque instantané de base de données et en exécutant `PRAGMA integrity_check`.
  `openclaw backup create` fait cette vérification d'archive par défaut ; `--no-verify` ignore uniquement la passe d'archive post-écriture, pas la vérification d'intégrité de création d'instantané.
- Restaurer copie les instantanés vers leurs chemins cibles. Cette branche réinitialise la disposition SQLite non expédiée à `user_version = 1` ; les futures modifications de schéma expédiées peuvent ajouter des migrations explicites lorsqu'elles sont nécessaires.

### Phase 6 : Runtime Worker

Garder le mode worker expérimental pendant que la division de base de données se déploie :

- Les workers reçoivent l'id d'agent, l'id d'exécution, le mode système de fichiers et l'identité du registre de base de données.
- Chaque worker ouvre sa propre connexion SQLite.
- Le parent conserve la livraison de canal, les approbations, la configuration et l'autorité d'annulation.
- Commencer avec un worker par exécution active ; ajouter le pooling uniquement après que le cycle de vie et la propriété de la connexion de base de données soient stables.

### Phase 7 : Supprimer l'Ancien Monde

Fait pour la gestion des sessions runtime. L'ancien monde n'est autorisé que comme entrée explicite du docteur ou sortie de support/export :

- Aucune écriture runtime `sessions.json`, transcription JSONL, JSON du registre sandbox, SQLite sidecar de tâche ou SQLite sidecar d'état du plugin.
- Aucun élagage de fichier JSON/session, troncature de transcription de fichier, verrous de fichier de session ou tests en forme de verrou de session.
- Aucun export de compatibilité runtime dont le but est de maintenir les anciens fichiers de session à jour.
- Les exports de support explicites restent des formats d'archive/matérialisation demandés par l'utilisateur et ne doivent pas réintroduire les noms de fichiers dans l'identité runtime.

## Sauvegarde et Restauration

Les sauvegardes doivent être un fichier d'archive, mais la capture de base de données doit être native à SQLite :

1. Arrêter l'activité d'écriture longue durée ou entrer dans une courte barrière de sauvegarde.
2. Pour chaque base de données globale et agent, exécuter un point de contrôle.
3. Créer un instantané de chaque base de données en utilisant la sémantique de sauvegarde SQLite ou `VACUUM INTO` dans un répertoire de sauvegarde temporaire.
4. Archiver les instantanés de base de données compacts, le fichier de configuration, le répertoire des identifiants, les espaces de travail sélectionnés et un manifeste.
5. Vérifier l'archive en ouvrant chaque instantané SQLite inclus et en exécutant `PRAGMA integrity_check`.
   `openclaw backup create` le fait par défaut ; `--no-verify` est uniquement pour ignorer intentionnellement la passe d'archive post-écriture.

Ne pas compter sur les copies brutes en direct `*.sqlite`, `*.sqlite-wal` et `*.sqlite-shm` comme format de sauvegarde principal. Le manifeste d'archive doit enregistrer le rôle de base de données, l'id d'agent, la version du schéma, le chemin source, le chemin d'instantané, la taille en octets et l'état d'intégrité.

La restauration doit reconstruire les fichiers de base de données globale et de base de données agent à partir des instantanés d'archive. Parce que la disposition SQLite n'a pas encore été expédiée, ce refactoring conserve uniquement le schéma version-1 plus l'importation fichier-vers-base de données du docteur. La commande de restauration valide d'abord l'archive, puis remplace chaque actif du manifeste à partir de la charge utile extraite vérifiée.

## Plan de refonte du runtime

1. Ajouter des APIs de registre de base de données.
   - Résoudre les chemins de base de données globale et par agent.
   - Conserver les schémas non expédiés à `user_version = 1` ; ne pas ajouter de code de migration de schéma jusqu'à ce qu'un schéma expédié en ait besoin.
   - Ajouter des assistants de fermeture/point de contrôle/intégrité utilisés par les tests, la sauvegarde et le docteur.

2. Réduire les magasins SQLite sidecar.
   - Déplacer les tables d'état du plugin dans la base de données globale. Fait pour les écritures runtime ; l'importateur sidecar hérité non expédié est supprimé.
   - Déplacer les tables de registre des tâches dans la base de données globale. Fait pour les écritures runtime ; l'importateur sidecar hérité non expédié est supprimé.
   - Déplacer les tables Task Flow dans la base de données globale. Fait pour les écritures runtime ; l'importateur sidecar hérité non expédié est supprimé.
   - Déplacer les tables de recherche mémoire intégrées dans chaque base de données d'agent. Fait ; le `memorySearch.store.path` personnalisé explicite est maintenant supprimé par la migration de configuration du docteur. La réindexation complète s'exécute sur place par rapport aux tables mémoire uniquement ; l'ancien chemin d'échange de fichier entier et l'assistant d'échange d'index sidecar sont supprimés.
   - Supprimer les ouvreurs de base de données en double, la configuration WAL, les assistants de permissions et les chemins de fermeture de ces sous-systèmes.

3. Déplacer les tables appartenant à l'agent dans les bases de données par agent.
   - Créer la base de données d'agent à la demande via le registre de base de données globale. Fait.
   - Déplacer les entrées de session runtime, les événements de transcription, les lignes VFS et les artefacts d'outils vers les bases de données d'agent. Fait.
   - Ne pas migrer les entrées de session de base de données partagée locale de branche, les événements de transcription, les lignes VFS ou les artefacts d'outils ; cette disposition n'a jamais été expédiée. Conserver uniquement l'importation hérité fichier-vers-base de données dans le docteur.

4. Remplacer les APIs de magasin de session.
   - Supprimer `storePath` comme identité runtime. Fait pour le runtime et gardé par `check:database-first-legacy-stores` : les métadonnées de session, les mises à jour d'itinéraire, la persistance des commandes, le nettoyage de session CLI, les aperçus de raisonnement Feishu, la persistance de l'état de transcription, la profondeur du sous-agent, les remplacements de session du profil d'authentification, la logique parent-fork et l'inspection du laboratoire QA résolvent maintenant la base de données à partir des clés agent/session canoniques.
     Les réponses de liste de session Gateway/TUI/UI/macOS exposent maintenant `databasePath` au lieu du `path` hérité ; les surfaces de débogage macOS affichent la base de données par agent en tant qu'état en lecture seule au lieu d'écrire la configuration `session.store`.
     `/status`, l'export de trajectoire piloté par chat et les proxies de dépendance CLI ne propagent plus les chemins de magasin hérités ; la lecture de secours d'utilisation de transcription lit SQLite par identité agent/session. Le runtime et les tests de pont n'exposent plus `storePath` ; les entrées doctor/migration possèdent ce nom de champ hérité.
     Le chargement de session combinée Gateway n'a plus de branche runtime spéciale pour les valeurs `session.store` non modélisées ; il agrège les lignes SQLite par agent.
     La voie doctor de verrouillage de session hérité et son assistant de nettoyage `.jsonl.lock` ont été supprimés ; SQLite est maintenant la limite de concurrence de session.
     Les sites d'appel runtime chauds utilisent des noms d'assistants orientés lignes tels que `resolveSessionRowEntry` ; l'alias de compatibilité ancien `resolveSessionStoreEntry` a été supprimé des exports runtime et plugin SDK.

- Utiliser les opérations de lignes `{ agentId, sessionKey }`.
  Fait : `getSessionEntry`, `upsertSessionEntry`, `deleteSessionEntry`, `patchSessionEntry` et `listSessionEntries` sont des APIs SQLite-first qui ne nécessitent pas de chemin de magasin de session. Le résumé de statut, le statut de l'agent local, la santé et la commande de liste `openclaw sessions` lisent maintenant les lignes par agent directement et affichent les chemins de base de données SQLite par agent au lieu des chemins `sessions.json`.
- Remplacer la suppression/insertion de magasin entier par `upsertSessionEntry`, `deleteSessionEntry`, `listSessionEntries` et les requêtes de nettoyage SQL.
  Fait pour le runtime : les chemins chauds utilisent maintenant les APIs de lignes et les patches de lignes avec nouvelle tentative de conflit ; les assistants d'importation/remplacement de magasin entier restants sont limités au code d'importation de migration et aux tests de backend SQLite.
  - Supprimer `store-writer.ts` et les tests de file d'attente d'écrivain. Fait.
  - Supprimer l'élagage de clé hérité runtime et les paramètres de suppression d'alias des upserts/patches de lignes de session. Fait.

5. Supprimer le comportement du registre JSON runtime.
   - Rendre les lectures et écritures du registre sandbox SQLite uniquement. Fait.
   - Importer JSON monolithique et fragmenté uniquement à partir de l'étape de migration. Fait.
   - Supprimer les verrous de registre fragmentés et les écritures JSON. Fait.

- Conserver une table de registre typée au lieu de stocker les lignes de registre en tant que JSON opaque générique si la forme reste un état opérationnel de chemin chaud. Fait.

6. Supprimer la mutation de session en forme de verrou de fichier.
   - Fait pour la création de verrou runtime et les APIs de verrou runtime.
   - La voie doctor autonome de nettoyage `.jsonl.lock` hérité est supprimée.
   - `session.writeLock` est une configuration hérité migrée par doctor, pas un paramètre runtime typé.
   - L'intégrité de l'état n'a plus de chemin d'élagage de fichier de transcription orphelin séparé ; la migration doctor importe/supprime les sources JSONL hérités en un seul endroit.
   - La coordination singleton Gateway utilise les lignes SQLite typées `state_leases` sous `gateway_locks` et n'expose plus une couture de répertoire de verrou de fichier.
   - La persistance de dédupliquage du plugin SDK générique n'utilise plus les verrous de fichier ou les fichiers JSON ; elle écrit les lignes de plugin-state SQLite partagées. Fait.
   - La coordination d'intégration QMD utilise un bail d'état SQLite au lieu de `qmd/embed.lock`. Fait.

7. Rendre les workers conscients de la base de données.
   - Les workers ouvrent leurs propres connexions SQLite.
   - Le parent possède la livraison, les rappels de canal et la configuration.
   - Le worker reçoit l'ID d'agent, l'ID d'exécution, le mode du système de fichiers et l'identité du registre DB, pas les handles en direct.
   - `vfs-only` reste expérimental et utilise la base de données d'agent comme racine de stockage.
   - Conserver un worker par exécution active en premier. Le pooling peut attendre que la durée de vie de la connexion à la base de données et le comportement d'annulation soient ennuyeux.

8. Intégration de sauvegarde.
   - Enseigner à la sauvegarde de faire un snapshot des bases de données globale et d'agent via la sauvegarde SQLite ou `VACUUM INTO`. Fait pour les fichiers `*.sqlite` découverts sous l'actif d'état.
   - Ajouter la vérification de sauvegarde pour l'intégrité SQLite et la version du schéma. Fait pour la création de sauvegarde et les vérifications d'intégrité de vérification d'archive par défaut.
   - Enregistrer les métadonnées d'exécution de sauvegarde dans SQLite. Fait via la table `backup_runs` partagée avec le chemin d'archive, le statut et le JSON du manifeste.
   - Ajouter la restauration à partir des snapshots d'archive vérifiés. Fait : `openclaw backup restore` valide avant l'extraction, utilise le manifeste normalisé du vérificateur, supporte `--dry-run` et nécessite `--yes` avant de remplacer les chemins source enregistrés.
   - Inclure l'export VFS/workspace uniquement si demandé ; ne pas exporter les internes de session en tant que JSON ou JSONL.

9. Supprimer les tests et le code obsolètes. Fait pour les surfaces de session runtime connues.

- Supprimer les tests qui affirment la création runtime de fichiers `sessions.json` ou JSONL de transcription. Fait pour le magasin de session principal, le chat, les événements de transcription gateway, l'aperçu, le cycle de vie, les mises à jour d'entrée de session de commande, la réinitialisation/trace de réponse automatique et les fixtures de rêve de mémoire-core, le routage de cible d'approbation, la réparation de transcription de session et l'export de session.
  Les tests de transcription de mémoire active affirment maintenant les portées SQLite et aucune création de fichier JSONL temporaire ou persisté.
  La régression de pruning de transcription du battement de cœur ancien a été supprimée car le runtime ne tronque plus les transcriptions JSONL.
  Les tests d'outil de liste de session d'agent ne modélisent plus les chemins `sessions.json` hérités comme la forme de réponse gateway ; les tests app/UI/macOS utilisent `databasePath`.
  Les tests d'utilisation de transcription `/status` ensemencent maintenant les lignes de transcription SQLite directement au lieu d'écrire des fichiers JSONL.
  Les tests de cycle de vie de session Gateway utilisent maintenant directement les assistants d'ensemencement de transcription SQLite ; la vieille forme de fixture de fichier de session sur une seule ligne est partie de la couverture de réinitialisation et de suppression.
  `sessions.delete` ne retourne plus un champ `archived: []` de l'ère des fichiers ; la suppression rapporte uniquement le résultat de mutation de ligne. L'ancienne option `deleteTranscript` est également partie : supprimer une session supprime la racine `sessions` canonique et laisse SQLite mettre en cascade les lignes de transcription, snapshot et trajectoire appartenant à la session, donc aucun appelant ne peut laisser les orphelins de transcription derrière ou oublier une branche de nettoyage.
  Les tests de capture de trajectoire du moteur de contexte lisent maintenant les lignes `trajectory_runtime_events` à partir d'une base de données d'agent isolée au lieu de lire `session.trajectory.jsonl`.
  Les scripts de seed du canal Docker MCP ensemencent maintenant les lignes SQLite directement. Les écritures directes `sessions.json` sont limitées aux fixtures doctor.
  Tool Search Gateway E2E lit les preuves d'appel d'outil à partir des lignes de transcription SQLite au lieu de scanner les fichiers `agents/<agentId>/sessions/*.jsonl`.
  Les événements d'hôte de mémoire-core et les lignes de scratch de corpus de session vivent maintenant dans le plugin-state SQLite partagé ; `events.jsonl` et `session-corpus/*.txt` sont des entrées de migration doctor hérités uniquement. Les lignes actives utilisent les chemins virtuels `memory/session-ingestion/`, pas `.dreams/session-corpus`. L'ancien module de réparation de rêve de mémoire-core et ses tests CLI/Gateway ont été supprimés car le runtime ne possède plus la réparation d'archive de fichier pour ce corpus. Les tests de pont/artefact public de mémoire-core ne font plus surface `.dreams/events.jsonl` ; ils utilisent le nom d'artefact JSON virtuel soutenu par SQLite.
  Les docs de test SDK/Codex public disent maintenant l'état de session SQLite au lieu des fichiers de session, et l'exemple de tour de canal n'expose plus un argument `storePath`.
  L'état de synchronisation Matrix utilise maintenant directement le magasin de plugin-state SQLite. Les contrats client/runtime actifs passent une racine de stockage de compte, pas un chemin `bot-storage.json`, et doctor importe le `bot-storage.json` hérité dans SQLite avant de supprimer la source. Les scénarios de redémarrage/destructif QA Matrix mutent maintenant la ligne de synchronisation SQLite directement au lieu de créer ou supprimer des fichiers `bot-storage.json` faux, et le substrat E2EE passe une racine de magasin de synchronisation au lieu d'un chemin `sync-store.json` faux.
  La sélection de racine de stockage Matrix ne note plus les racines par les fichiers JSON de synchronisation/thread hérités ; elle utilise les métadonnées de racine durables plus l'état crypto réel.
  La suite de tests du backend de session SQLite runtime ne fabrique plus un `sessions.json` ; les fixtures de source hérités vivent maintenant dans les tests doctor qui les importent.
  Les tests de session Gateway n'exposent plus un assistant `createSessionStoreDir` ou une configuration de chemin de magasin de session temporaire inutilisée ; les répertoires de fixture sont explicites et la configuration de ligne directe utilise la dénomination de ligne de session SQLite.
  La couverture du parseur de session-store JSON5 doctor-only a été déplacée hors des tests infra et dans les tests de migration doctor, donc les suites de tests runtime ne possèdent plus l'analyse de fichier de session hérité.
  Les tests SSO/téléchargement en attente du runtime Microsoft Teams ne portent plus les fixtures ou les parseurs sidecar JSON ; l'analyse de jeton SSO hérité vit uniquement dans le module de migration du plugin. Les tests Telegram ne font plus de seed des chemins de magasin `/tmp/*.json` faux ; ils réinitialisent directement le cache de messages soutenu par SQLite. L'assistant de test-state OpenClaw générique n'expose plus un écrivain `auth-profiles.json` hérité ; les tests de migration auth doctor possèdent cette fixture localement.
  Les tests runtime pour les pointeurs de dernière session TUI, les approbations exec, les bascules de mémoire active, la vérification de démarrage/dédupliquage Matrix, la synchronisation de source Memory Wiki, les liaisons de conversation actuelle, l'authentification d'intégration et les importations de secret Hermes ne fabriquent plus les anciens fichiers sidecar ou n'affirment plus que les anciens noms de fichiers sont absents. Ils prouvent le comportement par les lignes SQLite et les APIs de magasin public ; les tests doctor/migration sont le seul endroit où les noms de fichier source hérités appartiennent.
  Les tests runtime pour l'appairage de périphérique/nœud, allowFrom de canal, les intentions de redémarrage, la remise de redémarrage, les entrées de file d'attente de livraison de session, la santé de la configuration, les caches iMessage, les travaux cron, les en-têtes de transcription PI, les registres de sous-agent et les pièces jointes d'image gérées ne créent également plus les fichiers JSON/JSONL retraités juste pour prouver qu'ils sont ignorés ou absents.
  La récupération de débordement PI n'a plus de secours de réécriture/troncature SessionManager : la troncature de résultat d'outil et les réécritures de transcription du moteur de contexte mutent les lignes de transcription SQLite, puis actualisent l'état d'invite actif à partir de la base de données.
  Les ajouts de message SessionManager persistés délèguent à l'assistant d'ajout de transcription SQLite atomique pour la sélection de parent et l'idempotence. Les ajouts d'entrée de métadonnées/personnalisés normaux sélectionnent également le parent actuel dans SQLite, donc les instances de gestionnaire obsolètes ne ressuscitent pas les courses de chaîne parent pré-SQLite.
  Le nettoyage de queue PI synthétique pour les préchecks mid-turn et `sessions_yield` tronque maintenant directement l'état de transcription SQLite ; le pont de suppression de queue SessionManager ancien et ses tests sont supprimés.
  La capture de point de contrôle de compaction fait également un snapshot à partir de SQLite uniquement ; les appelants ne passent plus un SessionManager en direct comme source de transcription alternative.
- Conserver les tests qui ensemencent les fichiers hérités uniquement pour la migration.
- La preuve de fichier JSON a été remplacée par la preuve de ligne SQL pour les surfaces runtime actives.

- Ajouter des interdictions statiques pour les écritures runtime vers les chemins JSON de session/cache hérités.
  Fait pour la garde du repo.

10. Rendre le rapport de migration auditable.
    - Enregistrer les exécutions de migration dans SQLite avec les horodatages de début/fin, les chemins source, les hashes source, les comptages, les avertissements et le chemin de sauvegarde.
      Fait : les exécutions de migration d'état hérité persistent maintenant un rapport `migration_runs` avec l'inventaire de chemin/table source, le SHA-256 du fichier source, les tailles, les comptages d'enregistrements, les avertissements et le chemin de sauvegarde.
      Fait : les exécutions de migration d'état hérité persistent également les lignes `migration_sources` pour l'audit au niveau de la source et les décisions futures de saut/remplissage.
    - Rendre l'application idempotente. La réexécution après une importation partielle doit soit ignorer une source déjà importée, soit fusionner par clé stable.
      Fait : les index de session, les transcriptions, les files d'attente de livraison, l'état du plugin, les registres de tâches et les lignes SQLite globales appartenant à l'agent importent via des clés stables ou la sémantique upsert/replace, donc les réexécutions fusionnent sans dupliquer les lignes durables.
    - Les importations échouées doivent conserver le fichier source d'origine en place.
      Fait : les importations de transcription échouées laissent maintenant la source JSONL d'origine à son chemin détecté, et `migration_sources` enregistre la source en tant que `warning` avec `removed_source=0` pour la prochaine exécution doctor.

## Règles de Performance

- Une connexion par thread/processus est acceptable ; ne pas partager les handles entre les workers.
- Utiliser WAL, `foreign_keys=ON`, un timeout d'occupation de 30s, et des transactions d'écriture `BEGIN IMMEDIATE` courtes.
- Garder les helpers de transaction d'écriture synchrones sauf/jusqu'à ce qu'une API de transaction asynchrone ajoute une sémantique explicite de mutex/backpressure.
- Garder les écritures de livraison parent petites et transactionnelles.
- Éviter les réécriture de tout le magasin ; utiliser l'upsert/suppression au niveau des lignes.
- Ajouter des index pour list-by-agent, list-by-session, updated-at, run id, et les chemins d'expiration avant de déplacer le code critique.
- Stocker les artefacts volumineux, les médias et les vecteurs en tant que BLOBs ou lignes BLOB fragmentées, pas en base64 ou JSON de tableau numérique.
- Garder les entrées d'état de plugin opaque petites et délimitées.
- Ajouter un nettoyage SQL pour TTL/expiration au lieu du nettoyage du système de fichiers.
  Fait pour les magasins d'exécution appartenant à la base de données : les médias, l'état du plugin, les blobs du plugin, la déduplication persistante et le cache d'agent expirent tous via les lignes SQLite. Le nettoyage du système de fichiers restant est limité aux matérialisations temporaires ou aux commandes de suppression explicites.

## Interdictions Statiques

Ajouter une vérification de repo qui échoue les nouvelles écritures d'exécution vers les chemins d'état hérités :

- `sessions.json`
- `*.trajectory.jsonl` sauf les sorties de support-bundle matérialisées
- `.acp-stream.jsonl`
- `acp/event-ledger.json`
- `cache/*.json` fichiers de cache d'exécution
- `agents/<agentId>/agent/auth.json`
- `agents/<agentId>/agent/models.json`
- `credentials/oauth.json`
- `github-copilot.token.json`
- `openrouter-models.json`
- `auth-profiles.json`
- `auth-state.json`
- `exec-approvals.json`
- `workspace-state.json`
- Matrix `credentials*.json` et `recovery-key.json`
- `cron/runs/*.jsonl`
- `cron/jobs.json`
- `jobs-state.json`
- `device-pair-notify.json`
- `devices/pending.json`
- `devices/paired.json`
- `devices/bootstrap.json`
- `nodes/pending.json`
- `nodes/paired.json`
- `identity/device.json`
- `identity/device-auth.json`
- `push/web-push-subscriptions.json`
- `push/vapid-keys.json`
- `push/apns-registrations.json`
- `process-leases.json`
- `gateway-instance-id`
- `session-toggles.json`
- Memory-core `.dreams/events.jsonl`
- Memory-core `.dreams/session-corpus/`
- Memory-core `.dreams/daily-ingestion.json`
- Memory-core `.dreams/session-ingestion.json`
- Memory-core `.dreams/short-term-recall.json`
- Memory-core `.dreams/phase-signals.json`
- Memory-core `.dreams/short-term-promotion.lock`
- Skill Workshop `skill-workshop/<workspace>.json`
- Skill Workshop `skill-workshop/skill-workshop-review-*.json`
- Nostr `bus-state-*.json`
- Nostr `profile-state-*.json`
- `calls.jsonl`
- `known-users.json`
- `ref-index.jsonl`
- QQBot `session-*.json`
- BlueBubbles `bluebubbles/catchup/*.json`
- BlueBubbles `bluebubbles/inbound-dedupe/*.json`
- Telegram `update-offset-*.json`
- Telegram `sticker-cache.json`
- Telegram `*.telegram-messages.json`
- Telegram `*.telegram-sent-messages.json`
- Telegram `*.telegram-topic-names.json`
- Telegram `thread-bindings-*.json`
- iMessage `catchup/*.json`
- iMessage `reply-cache.jsonl`
- iMessage `sent-echoes.jsonl`
- Microsoft Teams `msteams-conversations.json`
- Microsoft Teams `msteams-polls.json`
- Microsoft Teams `msteams-sso-tokens.json`
- Microsoft Teams `msteams-delegated.json`
- Microsoft Teams `msteams-pending-uploads.json`
- Microsoft Teams `*.learnings.json`
- Matrix `bot-storage.json`
- Matrix `sync-store.json`
- Matrix `thread-bindings.json`
- Matrix `inbound-dedupe.json`
- Matrix `startup-verification.json`
- Matrix `storage-meta.json`
- Matrix `crypto-idb-snapshot.json`
- Discord `model-picker-preferences.json`
- Discord `command-deploy-cache.json`
- fichiers JSON de partage de registre sandbox
- fichiers JSON de relais de hook natif `/tmp`
- `plugin-state/state.sqlite`
- sidecars d'exécution `openclaw-state.sqlite` ad-hoc
- `tasks/runs.sqlite`
- `tasks/flows/registry.sqlite`
- `bindings/current-conversations.json`
- `restart-sentinel.json`
- `gateway-restart-intent.json`
- `gateway-supervisor-restart-handoff.json`
- `gateway.<hash>.lock`
- `qmd/embed.lock`
- `commands.log`
- `config-health.json`
- `port-guard.json`
- `settings/voicewake.json`
- `settings/voicewake-routing.json`
- `plugin-binding-approvals.json`
- `plugins/installs.json`
- `audit/file-transfer.jsonl`
- `audit/crestodian.jsonl`
- `crestodian/rescue-pending/*.json`
- `plugins/phone-control/armed.json`
- Memory Wiki `.openclaw-wiki/log.jsonl`
- Memory Wiki `.openclaw-wiki/state.json`
- Memory Wiki `.openclaw-wiki/locks/`
- Memory Wiki `.openclaw-wiki/source-sync.json`
- Memory Wiki `.openclaw-wiki/import-runs/*.json`
- Memory Wiki `.openclaw-wiki/cache/agent-digest.json`
- Memory Wiki `.openclaw-wiki/cache/claims.jsonl`
- ClawHub `.clawhub/lock.json`
- ClawHub `.clawhub/origin.json`
- Décoration de profil navigateur `.openclaw-profile-decorated`
- `SessionManager.open(...)` ouvreurs de session sauvegardés sur fichier
- `SessionManager.listAll(...)` et `TranscriptSessionManager.listAll(...)`
  façades de listage de transcription
- `SessionManager.forkFromSession(...)` et
  `TranscriptSessionManager.forkFromSession(...)` façades de fork de transcription
- `SessionManager.newSession(...)` et `TranscriptSessionManager.newSession(...)`
  façades de remplacement de session mutable
- `SessionManager.createBranchedSession(...)` et
  `TranscriptSessionManager.createBranchedSession(...)` façades de session de branche

L'interdiction doit permettre aux tests de créer des fixtures héritées et permettre au code de migration de lire/importer/supprimer les sources de fichiers hérités. Les sidecars SQLite non expédiés restent interdits et ne reçoivent pas d'autorisations d'importation du docteur.

## Critères d'Achèvement

- Les écritures de données d'exécution et de cache vont à la base de données SQLite globale ou d'agent.
- L'exécution n'écrit plus les index de session, la transcription JSONL, le registre sandbox JSON, le SQLite sidecar de tâche, ou le SQLite sidecar d'état de plugin. Les importateurs de sidecar SQLite de tâche et d'état de plugin non expédiés sont supprimés.
- L'importation de fichiers hérités est réservée au docteur.
- La sauvegarde produit une archive avec des snapshots SQLite compacts et une preuve d'intégrité.
- Les workers d'agent peuvent s'exécuter avec un stockage sur disque, scratch VFS, ou expérimental VFS uniquement.
- Les fichiers de configuration et d'identifiants explicites restent les seuls fichiers de contrôle non-base de données persistants attendus.
- Les vérifications de repo empêchent de réintroduire les magasins de fichiers d'exécution hérités.
