---
title: "Application compagne Windows native - Permissions, Secrets, et Note de Maturité de la Posture de Sécurité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Windows native - Permissions, Secrets, et Note de Maturité de la Posture de Sécurité

## Résumé

OpenClaw dispose d'un code de sécurité Windows natif pour les ACL du système de fichiers, la gestion des chemins,
l'authentification Gateway, et les portes de commandes de nœud dangereuses. L'application compagne Windows native
n'existe pas dans la source supportée, donc les permissions spécifiques à l'application, le stockage des secrets,
l'identité de signature, la confiance IPC locale, et les flux de consentement Windows sont indéfinis.

## Portée de la Catégorie

- Secrets d'application, persistance des jetons, IPC local sécurisé, identité de signature d'application, posture de permission AppContainer ou bureau.
- Hygiène ACL Windows et système de fichiers pour l'état détenu par l'application.
- Approbation de commande et gating de capacité dangereuse tel que présenté aux utilisateurs.

## Fonctionnalités

- Secrets d'application : Secrets d'application, persistance des jetons, IPC local sécurisé, identité de signature d'application, posture de permission AppContainer ou bureau
- ACL Windows : ACL Windows et hygiène du système de fichiers pour l'état détenu par l'application
- Approbation de commande : Approbation de commande et gating de capacité dangereuse tel que présenté aux utilisateurs

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Experimental (5%)`
- Signaux positifs : le code Windows ACL, chemin, authentification Gateway, et gating de commande existe en dehors de la surface de l'application.
- Signaux négatifs : aucun magasin de secrets d'application Windows, identité de signature, invite de permission, IPC d'application sécurisé, ou interface utilisateur d'approbation d'application n'existe dans le main actuel.
- Lacunes d'intégration : aucune configuration de sécurité d'application, invite de permission, migration de jeton, authentification IPC d'application, ou scénario d'approbation de commande dangereuse ne peut être exécuté.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct, ou la preuve du flux d'exécution réel sur
le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par
eux-mêmes.

## Score de Qualité

- Score : `Experimental (28%)`
- Rapports Gitcrawl : la requête spécifique à la fonctionnalité `Windows ACL secret path companion app` n'a retourné aucun résultat ; les requêtes d'application native Windows plus larges montrent des propositions plutôt que du support.
- Rapports Discrawl : la requête spécifique à la fonctionnalité `Windows ACL secret path companion app` n'a retourné aucun message.
- Bonnes qualités : le code principal existant échoue de manière fermée pour les commandes de nœud à haut risque et inclut des tests ACL/sécurité Windows.
- Mauvaises qualités : l'architecture de sécurité spécifique à l'application est absente, y compris l'identité de l'application, le stockage des secrets, la confiance IPC locale, et la réparation de permission visible par l'utilisateur.
- Exclu de la qualité : les preuves unitaires, d'intégration, e2e, en direct, et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer la Qualité.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture de test unitaire, d'intégration, e2e, en direct, ou d'exécution réelle
comme entrée de notation.

## Score de Complétude

- Score : `Experimental (5%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour Secrets d'application, ACL Windows, Approbation de commande.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucune conception de signature d'application, confiance, stockage de secrets, ou sécurité IPC locale n'existe dans les docs/source supportées.
- Aucune UX de permission d'application n'existe pour l'écran, la caméra, la localisation, les notifications, ou l'exécution de shell.
- Aucune politique documentée ne dit aux opérateurs comment auditer une compilation d'application compagne Windows externe.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md` mentionne les réinitialisations ACL Windows pour la sécurité du système de fichiers.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md` documente les concepts d'approbation exec partagés, pas une surface d'approbation d'application Windows.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md` ne définit pas les permissions d'application, la signature, ou les secrets.

### Source

- `/Users/kevinlin/code/openclaw/src/security/windows-acl.ts` implémente le support ACL Windows.
- `/Users/kevinlin/code/openclaw/src/security/audit-filesystem-windows.test.ts` couvre les cas de sécurité du système de fichiers Windows.
- `/Users/kevinlin/code/openclaw/src/gateway/node-command-policy.ts:64-73` définit les commandes de nœud dangereuses qui nécessitent une autorisation explicite.
- Aucune source de sécurité ou permission d'application Windows n'a été trouvée.

### Tests d'intégration

- Aucun test d'intégration de sécurité d'application compagne Windows n'a été trouvé.
- Une fumée CLI/Gateway Windows adjacente existe en dehors de ce composant.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/security/windows-acl.test.ts`
- `/Users/kevinlin/code/openclaw/src/security/audit-filesystem-windows.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-misc.test.ts`
- Aucun test de permission ou secret Windows spécifique à l'application n'a été trouvé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows ACL secret path companion app" --json`
- `gitcrawl search openclaw/openclaw --query "native Windows app" --json`

Résultats :

- La requête ACL/secret spécifique à la fonctionnalité n'a retourné aucun résultat.
- La requête plus large a surfacé `#12505`, une demande de fonctionnalité sandbox mentionnant un futur travail sandbox/AppContainer Windows natif de plateforme, plus des mentions Windows non liées.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows ACL secret path companion app"`

Résultats :

- Aucun message.
