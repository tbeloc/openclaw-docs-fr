---
summary: "Design for live Gateway proof of the Path 3 SQLite session/transcript flip"
read_when:
  - You are proving the Path 3 SQLite storage flip against a live Gateway
  - You need to distinguish expected legacy JSONL drift from runtime failures
  - You are building or reviewing the agent-driven live SQLite E2E harness
title: "Path 3 live SQLite E2E harness"
---

Le harnais E2E SQLite live Path 3 prouve que la Gateway utilise SQLite comme magasin canonique de session et de transcription, tandis que les fichiers JSONL hérités restent du matériel d'entrée de migration ou d'archivage. C'est un harnais de preuve pour les mainteneurs, pas un diagnostic utilisateur normal.

Après qu'une Gateway a traité le trafic post-migration, la parité JSONL hérité n'est plus un signal de santé d'exécution valide. Une Gateway migrée saine peut avoir des lignes de transcription SQLite qui diffèrent des comptages JSONL hérités, car les nouveaux tours doivent faire avancer SQLite uniquement. Le harnais live doit donc mesurer le comportement de la Gateway, le mouvement des lignes SQLite, la quiescence des fichiers hérités et la santé des journaux à chaque étape.

## Forme de la commande

La commande live prévue est :

```bash
node scripts/path3-live-sqlite-e2e.mjs \
  --url http://127.0.0.1:18789 \
  --agent main \
  --session-key agent:main:path3-live-e2e:<timestamp> \
  --json
```

La commande se connecte à une Gateway déjà en cours d'exécution. Elle ne démarre pas, n'arrête pas, n'importe pas et ne réexécute pas la migration sauf si un mode de migration explicite est ajouté ultérieurement. Une variante CI ou locale isolée peut utiliser `test/helpers/openclaw-test-instance.ts`, mais le chemin de preuve live doit inspecter la Gateway de l'opérateur réel et sa base de données SQLite réelle par agent.

## Preuve CLI construite isolée

Le runner de preuve CLI construit amorce un magasin de session hérité isolé, démarre la Gateway reconstruite et prouve que l'importation au démarrage charge les sessions hérités chauds dans SQLite avant que les lectures d'exécution ne commencent. Il ne doit pas exécuter `openclaw doctor --fix` avant le premier démarrage de la Gateway, car cela prouverait le chemin de migration manuel au lieu du chemin de mise à niveau que les utilisateurs reçoivent au premier démarrage après le basculement.

Après l'importation au démarrage, la preuve isolée peut exécuter `openclaw doctor --session-sqlite inspect` et `openclaw doctor --session-sqlite validate` comme preuve diagnostique. Ces commandes doctor ne sont pas le pilote de migration pour la preuve de mise à niveau au démarrage. Les scénarios doctor-import séparés doivent amorcer les fichiers de transcription hérités plus les sidecars de trajectoire et vérifier que doctor archive ces artefacts tandis que SQLite reste canonique.

## Préflight

Le préflight collecte une ligne de base et échoue avant d'envoyer un tour de preuve si la Gateway n'est pas utilisable :

- `GET /health` et l'état profond de la Gateway doivent signaler une Gateway en cours d'exécution et accessible.
- Les versions CLI et Gateway doivent correspondre à la branche testée.
- Le harnais enregistre un curseur de journal pour le fichier journal actif de la Gateway.
- Le harnais enregistre les comptages de table SQLite par agent pour `sessions`, `session_entries`, `transcript_events`, `transcript_event_identities` et `session_routes`.
- Le harnais enregistre `mtime`, `size` et l'existence pour `sessions.json` hérité, les fichiers JSONL référencés et les chemins JSONL de session de preuve candidats.
- `lsof -p <gateway-pid>` doit afficher les handles SQLite DB/WAL/SHM et aucun handle `.jsonl` ou `sessions.json` chaud.

`openclaw doctor --session-sqlite validate` est informatif uniquement en mode live. Après le trafic post-basculement, il peut signaler une dérive attendue par rapport aux fichiers hérités. Le harnais doit utiliser la sortie doctor pour la classification et l'inventaire de migration, pas comme l'oracle pass/fail d'exécution.

## Scénario piloté par agent

Le scénario live utilise une clé de session de preuve dédiée et pilote la Gateway à travers les chemins RPC publics autant que possible. Un tour d'agent devrait suffire pour exercer la persistance ordinaire, mais la preuve complète doit couvrir les coutures 3.1b qui nécessitaient auparavant des vérifications live individuelles :

- Tour de chat ordinaire : créer ou réutiliser la session de preuve, envoyer une véritable invite d'agent, attendre le résultat final de l'assistant et vérifier `chat.history` ou la projection Gateway équivalente.
- Identité de transcription : vérifier que le même marqueur apparaît dans l'historique de la Gateway et dans les lignes de transcription SQLite, y compris les lignes d'identité d'événement stable le cas échéant.
- Accesseurs de métadonnées de session : lire la session de preuve et les sessions live existantes sélectionnées via les accesseurs Gateway/session et les comparer aux lignes SQLite.
- Projection de patch de session : appliquer un changement de métadonnées de modèle/session réversible sur la session de preuve, puis vérifier que la ligne projetée et la réponse Gateway s'accordent.
- Cycle de vie du point de contrôle de compaction : lister, brancher et restaurer un point de contrôle uniquement sur la session de preuve ou une session de fixture synthétique créée par le harnais.
- Récupération au redémarrage : exécuter le chemin du marqueur de récupération sûr contre une session de preuve contrôlée ou une instance de test isolée ; le mode live ne peut exécuter cette étape que lorsque l'ensemble de sessions cible est explicite et réversible.
- Cycle de vie du nettoyage : supprimer ou réinitialiser la session de preuve, puis vérifier les lignes de cycle de vie SQLite et l'état de transcription archivé.

Les coutures spécifiques au transport qui ne peuvent pas être exercées en toute sécurité sur la Gateway de l'opérateur live, comme l'entrée WhatsApp ou d'appel vocal, doivent utiliser des sondes d'exécution au niveau du propriétaire contre le même contrat SQLite plutôt que de faux transports externes.

## Assertions par étape

Chaque étape capture l'état avant et après et écrit un enregistrement d'assertion structuré :

- Les comptages de lignes SQLite avancent uniquement où attendu.
- Les lignes d'exécution de trajectoire avancent pour les sessions de preuve soutenues par des marqueurs qui enregistrent les événements d'exécution.
- La ligne de session de preuve a le `session_id`, le statut, les horodatages, les métadonnées et les lignes de route attendus.
- La projection d'historique/session de la Gateway correspond à la queue de transcription SQLite.
- Aucun fichier JSONL de session de preuve n'est créé ou modifié.
- Aucun sidecar `.trajectory.jsonl`, `.trajectory-path.json` ou `trajectory/<session>.jsonl` dérivé de marqueur de session de preuve n'est créé.
- Les fichiers JSONL hérités existants et `sessions.json` restent inchangés sauf si l'étape est explicitement une opération de migration ou d'archivage hors ligne.
- Le processus Gateway n'ouvre pas les handles `.jsonl` ou `sessions.json`.
- Les journaux depuis le curseur précédent ne contiennent pas `ERROR`, `FATAL`, `SQLITE_`, `no such column`, session-store indisponible, échec de restart-recovery ou avertissement de transcript-reconcile sauf si le scénario l'autorise explicitement.

L'analyse des journaux fait partie du contrat pass/fail. Une Gateway qui répond aux vérifications de santé mais émet des erreurs de schéma SQLite ou des échecs de réconciliation de transcription répétés n'est pas verte pour Path 3.

## Artefact de preuve

Le harnais doit écrire la preuve sous `.artifacts/path3-live-e2e/<timestamp>/` et la garder hors de git :

- `summary.json` : arguments de commande, version de la Gateway, résultat, assertion échouée et chemins d'artefacts.
- `sqlite-before.json` et `sqlite-after.json` : comptages de lignes et lignes de preuve sélectionnées.
- `legacy-files.json` : existence de fichier hérité, `mtime`, taille et si chaque fichier a changé.
- `gateway-log-scan.json` : plage de curseur, lignes de journal correspondantes et décisions de liste d'autorisation.
- `events.jsonl` : observations ordonnées par étape adaptées aux commentaires de preuve PR.

La preuve PR doit résumer ces artefacts au lieu de coller des transcriptions complètes ou du contenu de messages privés.

## Règles de sécurité

- Le mode live ne doit jamais réimporter JSONL hérité pendant que la Gateway est en cours d'exécution.
- Le mode live ne doit pas muter les sessions non-preuve sauf pour les sondes de réparation explicitement sélectionnées et réversibles.
- Toute étape de migration destructrice ou large nécessite une sauvegarde fraîche de la base de données SQLite affectée et du répertoire de session hérité.
- Les sauvegardes doivent être limitées au répertoire DB/session d'agent touché et réutilisées pendant une exécution de preuve pour éviter une croissance de disque illimitée.
- L'étape de nettoyage ne doit laisser aucune session de preuve, JSONL de preuve ou fichier hérité modifié sauf si l'appelant passe `--keep-artifacts`.

## Résultat de passage

Une exécution live réussie signifie que la Gateway a accepté un flux de session piloté par agent réel, tout l'état canonique observé était dans SQLite, les fichiers d'exécution hérités sont restés quiescents et la santé des journaux est restée propre pour la fenêtre mesurée. Cela ne signifie pas que la parité JSONL hérité reste propre après le trafic live ; la dérive live est attendue une fois que SQLite est le magasin canonique.
