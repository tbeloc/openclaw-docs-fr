---
title: "iMessage / BlueBubbles - Note de maturité de la configuration et des opérations du canal"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Note de maturité de la configuration et des opérations du canal

## Résumé

La configuration de la configuration, du statut, du docteur et du compte est en version bêta. La fonctionnalité dispose d'un modèle source clair pour la configuration au niveau supérieur et au niveau du compte, de la détection des sources locales en double, des sondes de statut et des modifications de politique de configuration. Elle reste en dessous de Stable car le chemin de configuration doit finalement valider l'état réel de macOS et `imsg`, et il n'y a pas de voie de configuration en direct couvrant les flux d'opérateur pris en charge.

## Normalisation

Catégorie active après la normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Configuration et opérations du canal`
- Fusionnée à partir de : `Configuration et exécution de l'hôte`
- Report du score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Traduire la configuration héritée : Couvre la traduction de la configuration héritée dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur.
- Basculer en toute sécurité : Couvre le basculement en toute sécurité dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur.
- Gérer les avertissements de migration : Couvre la gestion des avertissements de migration dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur.
- Exécuter imsg local : Couvre l'exécution d'imsg local dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Exécuter via le wrapper SSH : Couvre l'exécution via le wrapper SSH dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Accorder les permissions macOS : Couvre l'octroi des permissions macOS dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Sonder la santé de l'exécution : Couvre le sondage de la santé de l'exécution dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Invites de configuration du compte : Couvre les invites de configuration, les écritures de politique, la fusion de comptes, la sélection du compte par défaut et le comportement de configuration du compte pour iMessage/BlueBubbles.
- Vérifications du statut du compte : Couvre la sortie du statut du compte, l'état de configuration, la fusion de comptes et la sélection du compte par défaut pour iMessage/BlueBubbles.
- Vérifications de réparation du docteur : Couvre les vérifications du docteur, les invites de réparation de configuration et la vérification de la politique pour la configuration du compte iMessage/BlueBubbles.
- Configuration du compte : Couvre la configuration du compte dans les invites de configuration, les écritures de politique, la fusion de comptes, la sélection du compte par défaut et le comportement de configuration, de statut, de docteur et de compte associé.
- Traduire la configuration héritée : Couvre la traduction de la configuration héritée dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur
- Basculer en toute sécurité : Couvre le basculement en toute sécurité dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur
- Gérer les avertissements de migration : Couvre la gestion des avertissements de migration dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur
- Exécuter imsg local : Couvre l'exécution d'imsg local dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions
- Exécuter via le wrapper SSH : Couvre l'exécution via le wrapper SSH dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions
- Accorder les permissions macOS : Couvre l'octroi des permissions macOS dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions
- Sonder la santé de l'exécution : Couvre le sondage de la santé de l'exécution dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions

## Fonctionnalités

- Traduire la configuration héritée : Couvre la traduction de la configuration héritée dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur.
- Basculer en toute sécurité : Couvre le basculement en toute sécurité dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur.
- Gérer les avertissements de migration : Couvre la gestion des avertissements de migration dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de transition de l'opérateur.
- Exécuter imsg local : Couvre l'exécution d'imsg local dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Exécuter via le wrapper SSH : Couvre l'exécution via le wrapper SSH dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Accorder les permissions macOS : Couvre l'octroi des permissions macOS dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Sonder la santé de l'exécution : Couvre le sondage de la santé de l'exécution dans `imsg rpc` local et distant, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Invites de configuration du compte : Couvre les invites de configuration, les écritures de politique, la fusion de comptes, la sélection du compte par défaut et le comportement de configuration du compte pour iMessage/BlueBubbles.
- Vérifications du statut du compte : Couvre la sortie du statut du compte, l'état de configuration, la fusion de comptes et la sélection du compte par défaut pour iMessage/BlueBubbles.
- Vérifications de réparation du docteur : Couvre les vérifications du docteur, les invites de réparation de configuration et la vérification de la politique pour la configuration du compte iMessage/BlueBubbles.
- Configuration du compte : Couvre la configuration du compte dans les invites de configuration, les écritures de politique, la fusion de comptes, la sélection du compte par défaut et le comportement de configuration, de statut, de docteur et de compte associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (74%)`
- Signaux positifs :
  - La documentation inclut la configuration rapide, la sonde de statut, la configuration à distance, la configuration multi-compte, le dépannage et les entrées de référence de configuration.
  - La source dispose d'un adaptateur de configuration, d'un résolveur de compte, d'un docteur de source en double, d'un démarrage d'exécution de canal et d'un adaptateur de statut/sonde par compte.
  - Les tests couvrent l'héritage de compte, la sélection du compte par défaut, le stationnement du moniteur en double, les avertissements du docteur, le schéma de configuration, les lignes de statut et le comportement de la sonde.
  - Les tests de passerelle `channels.status` exercent l'intégration de sonde iMessage fournie par le plugin.
- Signaux négatifs :
  - Le succès de la configuration dépend de `imsg` externe, des permissions macOS et de l'état de la session utilisateur connecté.
  - Il n'y a pas de fumée de configuration unique qui commence à partir d'une configuration vide et atteint un vrai moniteur iMessage fonctionnant sur un Mac.
  - La gestion des sources en double est robuste dans la source, mais les opérateurs doivent toujours comprendre la propriété du compte et la reliaison.
- Lacunes d'intégration :
  - Ajouter une fumée d'installation/configuration/statut contre un binaire `imsg` en direct ou hermétique qui valide les invites de configuration de bout en bout et `channels status`.
  - Ajouter un scénario de wrapper distant multi-compte prouvant les avertissements de source en double et la sélection du propriétaire dans une exécution opérationnelle.

## Score de qualité

- Score : `Bêta (73%)`
- Rapports Gitcrawl :
  - `channels.imessage allowFrom` a retourné #73822 pour la configuration SecretRef du numéro de téléphone et #62387 pour la gestion de la clé de promotion du compte nommé.
  - `iMessage channels status probe imsg private API` n'a retourné aucun résultat direct dans la dernière passe gitcrawl.
- Rapports Discrawl :
  - `iMessage Full Disk Access Automation cliPath dbPath` a retourné un fil de support où la réparation de la configuration a nécessité de définir en dur `cliPath` et `dbPath`.
  - La requête étroite `iMessage channels status probe imsg private API` n'a retourné aucun extrait.
- Bonnes qualités :
  - La fusion de comptes est explicite et prend en charge les remplacements au niveau du compte sans hériter silencieusement de l'état des frères et sœurs.
  - Les sources Messages locales en double sont détectées et converties en un seul propriétaire de moniteur au lieu de créer des réponses entrantes en double.
  - La sortie de statut/sonde est au niveau du compte et sépare l'état configuré de la disponibilité réelle de RPC/API privée.
  - La configuration rejette les entrées `allowFrom` DM qui sont en réalité des cibles de groupe/chat.
- Mauvaises qualités :
  - La surface de configuration est suffisamment large pour que la configuration correcte puisse toujours échouer en raison de l'état de l'hôte externe.
  - Les avertissements de propriété du compte exigent que les opérateurs réorientent les liaisons ou désactivent les doublons inutilisés.
  - Certains durcissements de configuration apparaissent toujours dans les problèmes d'archive adjacents.
- Exclus de la qualité :
  - Les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves de documentation archivée, de source, de test, de Gitcrawl et de Discrawl couvrent la portée de la taxonomie pour Traduire la configuration héritée, Basculer en toute sécurité, Gérer les avertissements de migration, Exécuter imsg local, Exécuter via le wrapper SSH, Accorder les permissions macOS, Sonder la santé de l'exécution, Invites de configuration du compte, Vérifications du statut du compte, Vérifications de réparation du docteur, Configuration du compte.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve de configuration de bout en bout sur un Mac en direct est manquante.
- La propriété du compte est cohérente en interne mais toujours visible par l'opérateur et subtile.
- Le statut peut être sain pour le canal tandis que la capacité d'API privée spécifique à l'action est obsolète jusqu'à ce qu'elle soit à nouveau sondée.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:41`: la configuration rapide vérifie `imsg`, démarre `imsg launch`, et exécute `openclaw channels status --probe`.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:76`: l'approbation d'appairage du premier DM fait partie du flux de configuration par défaut.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:399`: chaque compte peut pointer `cliPath` et `dbPath` vers un profil utilisateur spécifique.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:442`: les remplacements de compte incluent `cliPath`, `dbPath`, les listes blanches, la politique de groupe, les limites de médias, les paramètres d'historique et les racines de pièces jointes.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:777`: le dépannage renvoie les opérateurs à `openclaw channels status --probe --channel imessage`.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:605`: la référence de configuration expose `cliPath`.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:606`: la référence de configuration expose `dbPath`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/setup-core.ts:62`: la configuration rejette les entrées de style chat-target dans `allowFrom` DM.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/setup-core.ts:122`: la configuration écrit `channels.imessage.dmPolicy`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/setup-core.ts:123`: la configuration écrit `channels.imessage.allowFrom`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/accounts.ts:52`: la configuration du compte détecte les clés de comportement spécifiques au compte.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/accounts.ts:82`: la gestion des sources locales en double est liée à openclaw/openclaw#65141.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/accounts.ts:178`: l'avertissement d'aperçu de source en double explique le compte propriétaire et la réparation de liaison.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/channel.runtime.ts:82`: les emplacements de surveillance en double non-propriétaire sont garés au lieu d'être démarrés.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:92`: la limite de rechargement du plugin est `channels.imessage`.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/channels.status.test.ts:213`: le gestionnaire de statut enregistre une sonde de plugin iMessage.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/channels.status.test.ts:225`: la charge utile de statut inclut l'ordre du canal iMessage après sondage.
- Aucun test de configuration en direct vers Messages n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/accounts.test.ts:12`: préserve le compte par défaut de niveau supérieur lorsque des comptes nommés sont configurés.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/accounts.test.ts:29`: utilise le `defaultAccount` configuré lorsque l'ID de compte est omis.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/accounts.test.ts:56`: marque le défaut comme non-propriétaire lorsqu'un compte nommé partage sa source.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/doctor.test.ts:5`: le docteur marque les comptes partageant la source Messages locale.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/channel.runtime.test.ts:42`: le non-propriétaire de source en double ne génère pas le moniteur.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/status.test.ts:138`: les lignes de statut de configuration utilisent le `cliPath` du compte sélectionné.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/config-schema.test.ts:119`: accepte `remoteHost` sûr.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/config-schema.test.ts:127`: rejette `remoteHost` non sûr.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "channels.imessage allowFrom" --json --limit 6`

Résultats :

- Problème ouvert #73822 : support SecretRef pour les numéros de téléphone dans les configurations de canal.
- Problème ouvert #62387 : les clés de promotion de compte nommé suppriment les défauts partagés.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage channels status probe imsg private API" --json --limit 6`

Résultats :

- Aucun résultat direct dans le dernier passage.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage Full Disk Access Automation cliPath dbPath" --limit 6`

Résultats :

- Un fil de support a conseillé d'ajouter l'accès disque complet/Automation pour le processus exact exécutant Gateway/`imsg`, puis de définir en dur `cliPath` et `dbPath`.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage channels status probe imsg private API" --limit 6`

Résultats :

- Aucun extrait retourné.
