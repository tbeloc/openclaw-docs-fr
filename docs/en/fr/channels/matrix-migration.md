---
summary: "Comment OpenClaw met à niveau le plugin Matrix précédent sur place, y compris les limites de récupération d'état chiffré et les étapes de récupération manuelle."
read_when:
  - Mise à niveau d'une installation Matrix existante
  - Migration de l'historique Matrix chiffré et de l'état de l'appareil
title: "Migration Matrix"
---

Mise à niveau du plugin public `matrix` précédent vers l'implémentation actuelle.

Pour la plupart des utilisateurs, la mise à niveau se fait sur place :

- le plugin reste `@openclaw/matrix`
- le canal reste `matrix`
- votre config reste sous `channels.matrix`
- les identifiants en cache restent sous `~/.openclaw/credentials/matrix/`
- l'état d'exécution reste sous `~/.openclaw/matrix/`

Vous n'avez pas besoin de renommer les clés de config ou de réinstaller le plugin sous un nouveau nom.

## Ce que la migration fait automatiquement

Lorsque la passerelle démarre et lorsque vous exécutez [`openclaw doctor --fix`](/fr/gateway/doctor), OpenClaw tente de réparer l'ancien état Matrix automatiquement.
Avant que toute étape de migration Matrix exploitable ne mute l'état sur disque, OpenClaw crée ou réutilise un snapshot de récupération ciblé.

Lorsque vous utilisez `openclaw update`, le déclencheur exact dépend de la façon dont OpenClaw est installé :

- les installations à partir de la source exécutent `openclaw doctor --fix` pendant le flux de mise à jour, puis redémarrent la passerelle par défaut
- les installations du gestionnaire de paquets mettent à jour le paquet, exécutent une passe doctor non-interactive, puis s'appuient sur le redémarrage de passerelle par défaut pour que le démarrage puisse terminer la migration Matrix
- si vous utilisez `openclaw update --no-restart`, la migration Matrix basée sur le démarrage est reportée jusqu'à ce que vous exécutiez ultérieurement `openclaw doctor --fix` et redémarriez la passerelle

La migration automatique couvre :

- la création ou la réutilisation d'un snapshot pré-migration sous `~/Backups/openclaw-migrations/`
- la réutilisation de vos identifiants Matrix en cache
- le maintien de la même sélection de compte et de la config `channels.matrix`
- le déplacement du plus ancien magasin de synchronisation Matrix plat vers l'emplacement actuel limité au compte
- le déplacement du plus ancien magasin de crypto Matrix plat vers l'emplacement actuel limité au compte lorsque le compte cible peut être résolu en toute sécurité
- l'extraction d'une clé de déchiffrement de sauvegarde de clé de salle Matrix précédemment enregistrée à partir de l'ancien magasin de crypto rust, lorsque cette clé existe localement
- la réutilisation de la racine de stockage de hash de jeton la plus complète existante pour le même compte Matrix, serveur d'accueil et utilisateur lorsque le jeton d'accès change ultérieurement
- l'analyse des racines de stockage de hash de jeton frères pour les métadonnées de restauration d'état chiffré en attente lorsque le jeton d'accès Matrix a changé mais l'identité du compte/appareil est restée la même
- la restauration des clés de salle sauvegardées dans le nouveau magasin de crypto au prochain démarrage Matrix

Détails du snapshot :

- OpenClaw écrit un fichier marqueur à `~/.openclaw/matrix/migration-snapshot.json` après un snapshot réussi afin que les passes de démarrage et de réparation ultérieures puissent réutiliser la même archive.
- Ces snapshots de migration Matrix automatiques sauvegardent uniquement la config + l'état (`includeWorkspace: false`).
- Si Matrix n'a que l'état de migration d'avertissement uniquement, par exemple parce que `userId` ou `accessToken` est toujours manquant, OpenClaw ne crée pas encore le snapshot car aucune mutation Matrix n'est exploitable.
- Si l'étape de snapshot échoue, OpenClaw ignore la migration Matrix pour cette exécution au lieu de muter l'état sans point de récupération.

À propos des mises à niveau multi-comptes :

- le plus ancien magasin Matrix plat (`~/.openclaw/matrix/bot-storage.json` et `~/.openclaw/matrix/crypto/`) provenait d'une disposition à magasin unique, donc OpenClaw ne peut le migrer que vers une cible de compte Matrix résolue
- les magasins Matrix hérités déjà limités au compte sont détectés et préparés par compte Matrix configuré

## Ce que la migration ne peut pas faire automatiquement

Le plugin Matrix public précédent n'a **pas** créé automatiquement de sauvegardes de clé de salle Matrix. Il a persisté l'état de crypto local et a demandé la vérification de l'appareil, mais il n'a pas garanti que vos clés de salle ont été sauvegardées sur le serveur d'accueil.

Cela signifie que certaines installations chiffrées ne peuvent être migrées que partiellement.

OpenClaw ne peut pas récupérer automatiquement :

- les clés de salle locales uniquement qui n'ont jamais été sauvegardées
- l'état chiffré lorsque le compte Matrix cible ne peut pas encore être résolu car `homeserver`, `userId` ou `accessToken` ne sont toujours pas disponibles
- la migration automatique d'un magasin Matrix plat partagé lorsque plusieurs comptes Matrix sont configurés mais `channels.matrix.defaultAccount` n'est pas défini
- les installations de chemin de plugin personnalisé qui sont épinglées à un chemin de repo au lieu du paquet Matrix standard
- une clé de récupération manquante lorsque l'ancien magasin avait des clés sauvegardées mais n'a pas conservé la clé de déchiffrement localement

Portée d'avertissement actuelle :

- les installations de chemin de plugin Matrix personnalisé sont surfacées à la fois par le démarrage de la passerelle et par `openclaw doctor`

Si votre ancienne installation avait un historique chiffré local uniquement qui n'a jamais été sauvegardé, certains anciens messages chiffrés peuvent rester illisibles après la mise à niveau.

## Flux de mise à niveau recommandé

1. Mettez à jour OpenClaw et le plugin Matrix normalement.
   Préférez le simple `openclaw update` sans `--no-restart` afin que le démarrage puisse terminer la migration Matrix immédiatement.
2. Exécutez :

   ```bash
   openclaw doctor --fix
   ```

   Si Matrix a un travail de migration exploitable, doctor créera ou réutilisera d'abord le snapshot pré-migration et imprimera le chemin de l'archive.

3. Démarrez ou redémarrez la passerelle.
4. Vérifiez l'état actuel de la vérification et de la sauvegarde :

   ```bash
   openclaw matrix verify status
   openclaw matrix verify backup status
   ```

5. Mettez la clé de récupération du compte Matrix que vous réparez dans une variable d'environnement spécifique au compte. Pour un seul compte par défaut, `MATRIX_RECOVERY_KEY` convient. Pour plusieurs comptes, utilisez une variable par compte, par exemple `MATRIX_RECOVERY_KEY_ASSISTANT`, et ajoutez `--account assistant` à la commande.

6. Si OpenClaw vous dit qu'une clé de récupération est nécessaire, exécutez la commande pour le compte correspondant :

   ```bash
   printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin
   printf '%s\n' "$MATRIX_RECOVERY_KEY_ASSISTANT" | openclaw matrix verify backup restore --recovery-key-stdin --account assistant
   ```

7. Si cet appareil n'est toujours pas vérifié, exécutez la commande pour le compte correspondant :

   ```bash
   printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin
   printf '%s\n' "$MATRIX_RECOVERY_KEY_ASSISTANT" | openclaw matrix verify device --recovery-key-stdin --account assistant
   ```

   Si la clé de récupération est acceptée et la sauvegarde est utilisable, mais `Cross-signing verified`
   est toujours `no`, complétez l'auto-vérification à partir d'un autre client Matrix :

   ```bash
   openclaw matrix verify self
   ```

   Acceptez la demande dans un autre client Matrix, comparez les emoji ou les décimales,
   et tapez `yes` uniquement lorsqu'ils correspondent. La commande se termine avec succès uniquement
   après que `Cross-signing verified` devienne `yes`.

8. Si vous abandonnez intentionnellement l'ancien historique irrécupérable et souhaitez une nouvelle ligne de base de sauvegarde pour les messages futurs, exécutez :

   ```bash
   openclaw matrix verify backup reset --yes
   ```

9. Si aucune sauvegarde de clé côté serveur n'existe encore, créez-en une pour les récupérations futures :

   ```bash
   openclaw matrix verify bootstrap
   ```

## Comment fonctionne la migration chiffrée

La migration chiffrée est un processus en deux étapes :

1. Le démarrage ou `openclaw doctor --fix` crée ou réutilise le snapshot pré-migration si la migration chiffrée est exploitable.
2. Le démarrage ou `openclaw doctor --fix` inspecte l'ancien magasin de crypto Matrix via l'installation active du plugin Matrix.
3. Si une clé de déchiffrement de sauvegarde est trouvée, OpenClaw l'écrit dans le nouveau flux de clé de récupération et marque la restauration de clé de salle comme en attente.
4. Au prochain démarrage Matrix, OpenClaw restaure automatiquement les clés de salle sauvegardées dans le nouveau magasin de crypto.

Si l'ancien magasin signale des clés de salle qui n'ont jamais été sauvegardées, OpenClaw avertit au lieu de prétendre que la récupération a réussi.

## Messages courants et leur signification

### Messages de mise à niveau et de détection

`Matrix plugin upgraded in place.`

- Signification : l'ancien état Matrix sur disque a été détecté et migré dans la disposition actuelle.
- À faire : rien sauf si la même sortie inclut également des avertissements.

`Matrix migration snapshot created before applying Matrix upgrades.`

- Signification : OpenClaw a créé une archive de récupération avant de modifier l'état Matrix.
- À faire : conservez le chemin d'archive imprimé jusqu'à ce que vous confirmiez que la migration a réussi.

`Matrix migration snapshot reused before applying Matrix upgrades.`

- Signification : OpenClaw a trouvé un marqueur de snapshot de migration Matrix existant et a réutilisé cette archive au lieu de créer une sauvegarde en double.
- À faire : conservez le chemin d'archive imprimé jusqu'à ce que vous confirmiez que la migration a réussi.

`Legacy Matrix state detected at ... but channels.matrix is not configured yet.`

- Signification : l'ancien état Matrix existe, mais OpenClaw ne peut pas le mapper à un compte Matrix actuel car Matrix n'est pas configuré.
- À faire : configurez `channels.matrix`, puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`Legacy Matrix state detected at ... but the new account-scoped target could not be resolved yet (need homeserver, userId, and access token for channels.matrix...).`

- Signification : OpenClaw a trouvé l'ancien état, mais il ne peut toujours pas déterminer la racine exacte du compte/appareil actuel.
- À faire : démarrez la passerelle une fois avec une connexion Matrix fonctionnelle, ou réexécutez `openclaw doctor --fix` après que les identifiants en cache existent.

`Legacy Matrix state detected at ... but multiple Matrix accounts are configured and channels.matrix.defaultAccount is not set.`

- Signification : OpenClaw a trouvé un magasin Matrix plat partagé, mais il refuse de deviner quel compte Matrix nommé devrait le recevoir.
- À faire : définissez `channels.matrix.defaultAccount` sur le compte prévu, puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`Matrix legacy sync store not migrated because the target already exists (...)`

- Signification : le nouvel emplacement limité au compte a déjà un magasin de synchronisation ou de chiffrement, donc OpenClaw ne l'a pas écrasé automatiquement.
- À faire : vérifiez que le compte actuel est le bon avant de supprimer ou de déplacer manuellement la cible en conflit.

`Failed migrating Matrix legacy sync store (...)` ou `Failed migrating Matrix legacy crypto store (...)`

- Signification : OpenClaw a tenté de déplacer l'ancien état Matrix mais l'opération du système de fichiers a échoué.
- À faire : inspectez les permissions du système de fichiers et l'état du disque, puis réexécutez `openclaw doctor --fix`.

`Legacy Matrix encrypted state detected at ... but channels.matrix is not configured yet.`

- Signification : OpenClaw a trouvé un ancien magasin Matrix chiffré, mais il n'y a pas de configuration Matrix actuelle à laquelle l'attacher.
- À faire : configurez `channels.matrix`, puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`Legacy Matrix encrypted state detected at ... but the account-scoped target could not be resolved yet (need homeserver, userId, and access token for channels.matrix...).`

- Signification : le magasin chiffré existe, mais OpenClaw ne peut pas décider en toute sécurité quel compte/appareil actuel il appartient.
- À faire : démarrez la passerelle une fois avec une connexion Matrix fonctionnelle, ou réexécutez `openclaw doctor --fix` après que les identifiants en cache sont disponibles.

`Legacy Matrix encrypted state detected at ... but multiple Matrix accounts are configured and channels.matrix.defaultAccount is not set.`

- Signification : OpenClaw a trouvé un magasin de chiffrement hérité plat partagé, mais il refuse de deviner quel compte Matrix nommé devrait le recevoir.
- À faire : définissez `channels.matrix.defaultAccount` sur le compte prévu, puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`Matrix migration warnings are present, but no on-disk Matrix mutation is actionable yet. No pre-migration snapshot was needed.`

- Signification : OpenClaw a détecté l'ancien état Matrix, mais la migration est toujours bloquée sur des données d'identité ou d'identifiants manquantes.
- À faire : terminez la configuration de connexion ou de configuration Matrix, puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`Legacy Matrix encrypted state was detected, but the Matrix plugin helper is unavailable. Install or repair @openclaw/matrix so OpenClaw can inspect the old rust crypto store before upgrading.`

- Signification : OpenClaw a trouvé l'ancien état Matrix chiffré, mais il n'a pas pu charger le point d'entrée d'aide du plugin Matrix qui inspecte normalement ce magasin.
- À faire : réinstallez ou réparez le plugin Matrix (`openclaw plugins install @openclaw/matrix`, ou `openclaw plugins install ./path/to/local/matrix-plugin` pour un checkout de repo), puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`Matrix plugin helper path is unsafe: ... Reinstall @openclaw/matrix and try again.`

- Signification : OpenClaw a trouvé un chemin de fichier d'aide qui s'échappe de la racine du plugin ou échoue les vérifications de limite du plugin, donc il a refusé de l'importer.
- À faire : réinstallez le plugin Matrix à partir d'un chemin de confiance, puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`- Failed creating a Matrix migration snapshot before repair: ...`

`- Skipping Matrix migration changes for now. Resolve the snapshot failure, then rerun "openclaw doctor --fix".`

- Signification : OpenClaw a refusé de modifier l'état Matrix car il n'a pas pu créer le snapshot de récupération en premier.
- À faire : résolvez l'erreur de sauvegarde, puis réexécutez `openclaw doctor --fix` ou redémarrez la passerelle.

`Failed migrating legacy Matrix client storage: ...`

- Signification : le secours côté client Matrix a trouvé l'ancien magasin plat, mais le déplacement a échoué. OpenClaw abandonne maintenant ce secours au lieu de démarrer silencieusement avec un magasin frais.
- À faire : inspectez les permissions du système de fichiers ou les conflits, conservez l'ancien état intact et réessayez après avoir résolu l'erreur.

`Matrix is installed from a custom path: ...`

- Signification : Matrix est épinglé à une installation de chemin, donc les mises à jour de la ligne principale ne le remplacent pas automatiquement par le package Matrix standard du repo.
- À faire : réinstallez avec `openclaw plugins install @openclaw/matrix` quand vous voulez revenir au plugin Matrix par défaut.

### Messages de récupération d'état chiffré

`matrix: restored X/Y room key(s) from legacy encrypted-state backup`

- Signification : les clés de salle sauvegardées ont été restaurées avec succès dans le nouveau magasin de chiffrement.
- À faire : généralement rien.

`matrix: N legacy local-only room key(s) were never backed up and could not be restored automatically`

- Signification : certaines anciennes clés de salle existaient uniquement dans l'ancien magasin local et n'avaient jamais été téléchargées vers la sauvegarde Matrix.
- À faire : attendez-vous à ce que certains anciens historiques chiffrés restent indisponibles sauf si vous pouvez récupérer ces clés manuellement à partir d'un autre client vérifié.

`Legacy Matrix encrypted state for account "..." has backed-up room keys, but no local backup decryption key was found. Ask the operator to run "openclaw matrix verify backup restore --recovery-key-stdin" after upgrade if they have the recovery key.`

- Signification : la sauvegarde existe, mais OpenClaw n'a pas pu récupérer la clé de récupération automatiquement.
- À faire : exécutez `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin`.

`Failed inspecting legacy Matrix encrypted state for account "..." (...): ...`

- Signification : OpenClaw a trouvé l'ancien magasin chiffré, mais il n'a pas pu l'inspecter suffisamment en toute sécurité pour préparer la récupération.
- À faire : réexécutez `openclaw doctor --fix`. Si cela se répète, conservez le répertoire d'état ancien intact et récupérez en utilisant un autre client Matrix vérifié plus `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin`.

`Legacy Matrix backup key was found for account "...", but .../recovery-key.json already contains a different recovery key. Leaving the existing file unchanged.`

- Signification : OpenClaw a détecté un conflit de clé de sauvegarde et a refusé d'écraser le fichier de clé de récupération actuel automatiquement.
- À faire : vérifiez quelle clé de récupération est correcte avant de réessayer une commande de restauration.

`Legacy Matrix encrypted state for account "..." cannot be fully converted automatically because the old rust crypto store does not expose all local room keys for export.`

- Signification : c'est la limite difficile du format de stockage ancien.
- À faire : les clés sauvegardées peuvent toujours être restaurées, mais l'historique chiffré local uniquement peut rester indisponible.

`matrix: failed restoring room keys from legacy encrypted-state backup: ...`

- Signification : le nouveau plugin a tenté la restauration mais Matrix a renvoyé une erreur.
- À faire : exécutez `openclaw matrix verify backup status`, puis réessayez avec `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin` si nécessaire.

### Messages de récupération manuelle

`Backup key is not loaded on this device. Run 'openclaw matrix verify backup restore' to load it and restore old room keys.`

- Signification : OpenClaw sait que vous devriez avoir une clé de sauvegarde, mais elle n'est pas active sur cet appareil.
- À faire : exécutez `openclaw matrix verify backup restore`, ou définissez `MATRIX_RECOVERY_KEY` et exécutez `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin` si nécessaire.

`Store a recovery key with 'openclaw matrix verify device --recovery-key-stdin', then run 'openclaw matrix verify backup restore'.`

- Signification : cet appareil n'a pas actuellement la clé de récupération stockée.
- À faire : définissez `MATRIX_RECOVERY_KEY`, exécutez `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`, puis restaurez la sauvegarde.

`Backup key mismatch on this device. Re-run 'openclaw matrix verify device --recovery-key-stdin' with the matching recovery key.`

- Signification : la clé stockée ne correspond pas à la sauvegarde Matrix active.
- À faire : définissez `MATRIX_RECOVERY_KEY` sur la clé correcte et exécutez `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`.

Si vous acceptez de perdre l'ancien historique chiffré irrécupérable, vous pouvez à la place réinitialiser la ligne de base de sauvegarde actuelle avec `openclaw matrix verify backup reset --yes`. Quand le secret de sauvegarde stocké est cassé, cette réinitialisation peut également recréer le stockage secret afin que la nouvelle clé de sauvegarde puisse se charger correctement après le redémarrage.

`Backup trust chain is not verified on this device. Re-run 'openclaw matrix verify device --recovery-key-stdin'.`

- Signification : la sauvegarde existe, mais cet appareil ne fait pas suffisamment confiance à la chaîne de signature croisée.
- À faire : définissez `MATRIX_RECOVERY_KEY` et exécutez `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`.

`Matrix recovery key is required`

- Signification : vous avez tenté une étape de récupération sans fournir une clé de récupération quand une était requise.
- À faire : réexécutez la commande avec `--recovery-key-stdin`, par exemple `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`.

`Invalid Matrix recovery key: ...`

- Signification : la clé fournie n'a pas pu être analysée ou ne correspondait pas au format attendu.
- À faire : réessayez avec la clé de récupération exacte de votre client Matrix ou fichier de clé de récupération.

`Matrix recovery key was applied, but this device still lacks full Matrix identity trust.`

- Signification : OpenClaw a pu appliquer la clé de récupération, mais Matrix n'a toujours pas établi la confiance d'identité de signature croisée complète pour cet appareil. Vérifiez la sortie de la commande pour `Recovery key accepted`, `Backup usable`, `Cross-signing verified`, et `Device verified by owner`.
- À faire : exécutez `openclaw matrix verify self`, acceptez la demande dans un autre client Matrix, comparez le SAS et tapez `yes` uniquement quand il correspond. La commande attend la confiance d'identité Matrix complète avant de signaler le succès. Utilisez `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify bootstrap --recovery-key-stdin --force-reset-cross-signing` uniquement quand vous voulez intentionnellement remplacer l'identité de signature croisée actuelle.

`Matrix key backup is not active on this device after loading from secret storage.`

- Signification : le stockage secret n'a pas produit une session de sauvegarde active sur cet appareil.
- À faire : vérifiez d'abord l'appareil, puis revérifiez avec `openclaw matrix verify backup status`.

`Matrix crypto backend cannot load backup keys from secret storage. Verify this device with 'openclaw matrix verify device --recovery-key-stdin' first.`

- Signification : cet appareil ne peut pas restaurer à partir du stockage secret jusqu'à ce que la vérification de l'appareil soit complète.
- À faire : exécutez d'abord `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`.

### Messages d'installation de plugin personnalisé

`Matrix is installed from a custom path that no longer exists: ...`

- Signification : votre enregistrement d'installation de plugin pointe vers un chemin local qui a disparu.
- À faire : réinstallez avec `openclaw plugins install @openclaw/matrix`, ou si vous exécutez à partir d'un checkout de repo, `openclaw plugins install ./path/to/local/matrix-plugin`.

## Si l'historique chiffré ne revient toujours pas

Exécutez ces vérifications dans l'ordre :

```bash
openclaw matrix verify status --verbose
openclaw matrix verify backup status --verbose
printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin --verbose
```

Si la sauvegarde se restaure avec succès mais que certains anciens salons n'ont toujours pas d'historique, ces clés manquantes n'ont probablement jamais été sauvegardées par le plugin précédent.

## Si vous voulez recommencer à zéro pour les futurs messages

Si vous acceptez de perdre l'ancien historique chiffré irrécupérable et que vous ne voulez qu'une ligne de base de sauvegarde propre à l'avenir, exécutez ces commandes dans l'ordre :

```bash
openclaw matrix verify backup reset --yes
openclaw matrix verify backup status --verbose
openclaw matrix verify status
```

Si l'appareil n'est toujours pas vérifié après cela, terminez la vérification depuis votre client Matrix en comparant les emoji SAS ou les codes décimaux et en confirmant qu'ils correspondent.

## Connexes

- [Matrix](/fr/channels/matrix) : configuration et paramétrage du canal.
- [Règles de notification Matrix](/fr/channels/matrix-push-rules) : routage des notifications.
- [Doctor](/fr/gateway/doctor) : vérification de santé et déclenchement automatique de migration.
- [Guide de migration](/fr/install/migrating) : tous les chemins de migration (déplacements de machines, importations inter-systèmes).
- [Plugins](/fr/tools/plugin) : installation et enregistrement des plugins.
