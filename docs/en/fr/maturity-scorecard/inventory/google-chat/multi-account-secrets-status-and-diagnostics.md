---
title: "Google Chat - Multi Account Secrets Status and Diagnostics Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Multi Account Secrets Status and Diagnostics Maturity Note

## Summary

Le compte Google Chat, SecretRef et le plumbing de statut sont larges mais toujours en Alpha. La source supporte les comptes de service au niveau supérieur et au niveau du compte, les identifiants env/fichier/inline, les valeurs par défaut partagées, l'assignation SecretRef à l'exécution, les sondes de statut, les problèmes de configuration pour les champs audience manquants, et les avertissements de liste d'autorisation mutable. Le frein à la maturité est que les véritables défaillances de configuration Google Chat émergent toujours comme des problèmes d'authentification/exécution nuancés, et aucune suite de sonde en direct ne prouve le comportement multi-compte SecretRef par rapport aux API Google.

## Category Scope

Cette note couvre `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs de compte de service, les assignations de configuration à l'exécution, le fallback env, les snapshots de statut, `channels status --probe`, la sonde API Google Chat, les problèmes d'audience/audienceType manquants, les avertissements de liste d'autorisation mutable, l'énumération des pairs/groupes du répertoire, et les diagnostics de l'opérateur. Elle exclut les détails de l'assistant de configuration, les internals d'authentification webhook, et le comportement de livraison de messages en aval après qu'un compte soit en cours d'exécution.

## Features

- Account resolution: Couvre la résolution des comptes dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs de compte de service, et le comportement de statut et diagnostics multi-compte secrets associé.
- Service account SecretRefs: Couvre les SecretRefs de compte de service dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs de compte de service, et le comportement de statut et diagnostics multi-compte secrets associé.
- Env file and inline credentials: Couvre les identifiants env fichier et inline dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs de compte de service, et le comportement de statut et diagnostics multi-compte secrets associé.
- Channel status and probes: Couvre le statut et les sondes de canal dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs de compte de service, et le comportement de statut et diagnostics multi-compte secrets associé.
- Directory and mutable-id diagnostics: Couvre les diagnostics de répertoire et mutable-id dans `accounts`, `defaultAccount`, l'héritage des identifiants au niveau supérieur et au niveau du compte, les SecretRefs de compte de service, et le comportement de statut et diagnostics multi-compte secrets associé.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Coverage Score

- Score: `Alpha (66%)`
- Positive signals: Les tests unitaires couvrent la résolution du compte par défaut, le fallback des identifiants env, les valeurs par défaut partagées spécifiques au compte, l'héritage des identifiants au niveau supérieur, le comportement des comptes désactivés, les entrées du registre SecretRef, les avertissements de secret inactif, la configuration du statut, l'énumération du répertoire, et les champs de statut/sonde.
- Negative signals: Je n'ai trouvé aucune preuve Google Chat multi-compte en direct couvrant deux comptes sur des chemins webhook partagés/différents, la résolution serviceAccountRef spécifique au compte, et le comportement réel de `channels status --probe` par rapport à l'API Google Chat.
- Integration gaps: Ajouter une sonde multi-compte en direct avec un compte par défaut/env et un compte SecretRef/fichier nommé, incluant les secrets de compte désactivé, les valeurs par défaut d'audience partagées, le remplacement du chemin webhook spécifique au compte, et les assertions de problème de statut.

## Quality Score

- Score: `Alpha (64%)`
- Gitcrawl reports: `gitcrawl search issues "Google Chat serviceAccount SecretRef setup"` n'a retourné aucun résultat direct, mais #77307 montre que les régressions d'identifiants/authentification peuvent casser l'ensemble du canal, et les problèmes d'appPrincipal/audience ont une piste de support récente. #58514 et #65007 montrent que le statut peut dire HTTP accepté tandis que les messages d'espace ne produisent toujours pas de comportement d'exécution utile.
- Discrawl reports: `discrawl search "Google Chat DMs work spaces" --limit 10` a retourné une configuration et une sortie de statut montrant Google Chat `enabled, configured, running, dm:pairing, works` tandis que l'utilisateur a toujours signalé que les messages ne déclenchaient pas de journalisation utile. `discrawl search "Google Chat setup service account audience" --limit 10` a retourné une discussion de support de configuration/authentification autour du JSON de compte de service, de l'audience et d'appPrincipal, démontrant que le statut et les docs doivent rendre l'état principal/audience plus actionnable.
- Good qualities: La fusion de comptes est explicite, les entrées d'assignation SecretRef sont enregistrées pour les chemins au niveau supérieur et au niveau du compte, les comptes désactivés produisent des avertissements de secret inactif, les résumés de statut incluent la source d'identifiants et les champs d'audience, et la sonde appelle `spaces` avec un jeton de compte de service via le même chemin API gardé.
- Bad qualities: Le statut peut prouver les identifiants et un appel API superficiel sans prouver la livraison webhook, l'admission d'espace, le comportement des threads, ou les portées d'action/média. Les configurations multi-compte héritent les valeurs par défaut de manière subtile, et les SecretRefs non résolus échouent intentionnellement en dehors des snapshots d'exécution actifs, ce qui peut surprendre les utilisateurs CLI/action.
- Excluded from quality: La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Completeness Score

- Score: `Alpha (66%)`
- Surface instructions: évaluées par rapport à `references/completeness/google-chat.md`.
- Positive signals: les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la résolution des comptes, les SecretRefs de compte de service, les identifiants env fichier et inline, le statut et les sondes de canal, les diagnostics de répertoire et mutable-id.
- Negative signals: la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Missing capability branches: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Ajouter des sondes de statut qui distinguent la santé des identifiants, la santé de l'authentification webhook, le dernier webhook entrant, le dernier espace/DM accepté, et la dernière raison de politique d'accès abandonnée.
- Ajouter une preuve SecretRef multi-compte en direct pour les comptes de service au niveau du compte et les valeurs par défaut webhook/audience partagées.
- Inclure la capacité OAuth d'action/média dans le statut afin que les limitations de compte de service uniquement soient visibles avant l'utilisation d'outils.
- Améliorer la copie CLI pour les SecretRefs non résolus en dehors d'un snapshot d'exécution de passerelle actif.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md`: documente `serviceAccount`, `serviceAccountFile`, `serviceAccountRef`, les refs par compte, `audienceType`, `audience`, `webhookPath`, le dépannage de statut/sonde, et `plugins.entries.googlechat.enabled`.
- `/Users/kevinlin/code/openclaw/docs/gateway/secrets.md`: documente le comportement SecretRef et le comportement de compatibilité Google Chat.
- `/Users/kevinlin/code/openclaw/docs/reference/secretref-credential-surface.md`: liste `channels.googlechat.serviceAccount` et `channels.googlechat.accounts.*.serviceAccount`.
- `/Users/kevinlin/code/openclaw/docs/gateway/health.md`: liste Google Chat parmi les canaux avec des remplacements de moniteur de santé.

### Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/accounts.ts`: résout les IDs de compte, les valeurs par défaut partagées, le fallback env pour le compte par défaut, les sources d'identifiants par compte, et les erreurs SecretRef en dehors des snapshots d'exécution.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/secret-contract.ts`: enregistre les cibles SecretRef de compte de service Google Chat et collecte les assignations de configuration d'exécution avec les avertissements de compte inactif.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.ts`: construit le statut de compte calculé, les problèmes de statut pour l'audience/audienceType manquants, le comportement de sonde, les adaptateurs de configuration, l'adaptateur de répertoire, et le câblage du registre de secrets.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/api.ts`: implémente `probeGoogleChat` via le point de terminaison API Chat `spaces`.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/doctor.ts`: collecte les avertissements de liste d'autorisation mutable pour les champs DM et groupe.

### Integration tests

- Aucun scénario multi-compte/SecretRef/statut Google Chat en direct dédié n'a été trouvé sous `/Users/kevinlin/code/openclaw/extensions/qa-lab` ou `qa/scenarios`.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-external-channel-audit.test.ts`: inclut les surfaces de compte de service Google Chat dans l'audit de secret de canal externe.
- `/Users/kevinlin/code/openclaw/src/secrets/target-registry.fast-path.test.ts`: couvre le chemin rapide du registre de cible de compte de service Google Chat.

### Unit tests

- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/setup.test.ts`: couvre la résolution des comptes, le fallback env, l'héritage du compte par défaut et du compte nommé, les valeurs par défaut partagées, les comptes désactivés, et le câblage du statut.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/secret-contract.test.ts`: couvre les entrées de cible SecretRef et le comportement d'assignation d'exécution.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/doctor-contract.test.ts`: couvre les règles de compatibilité de configuration/doctor héritées.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.test.ts`: couvre l'énumération du répertoire, les adaptateurs adjacents au statut, la résolution de cible, et le threading de compte via les envois.

### Gitcrawl queries

Query:

`gitcrawl search issues "Google Chat serviceAccount SecretRef setup" --repo openclaw/openclaw --limit 15 --json number,title,state,updatedAt,url`

Results:

- N'a retourné aucun résultat de problème direct. C'est neutre après les vérifications de fraîcheur d'archive réussies; le risque de statut/configuration provenait de problèmes d'authentification et de livraison Google Chat plus larges.

Query:

`gitcrawl gh issue view 77307 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Results:

- A retourné le #77307 ouvert, un rapport de régression où les envois Google Chat ont échoué avec `unsupported_grant_type`, montrant la fragilité du chemin d'authentification/identifiants.

Query:

`gitcrawl gh issue view 58514 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Results:

- A retourné le #58514 ouvert, où les requêtes HTTP ont été reçues et les DMs ont fonctionné, mais les sessions de groupe n'ont pas été créées, montrant que le statut configuré/en cours d'exécution superficiel n'est pas suffisant.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search "Google Chat DMs work spaces" --limit 10`

Results:

- A retourné une configuration réelle et une sortie de statut montrant Google Chat `enabled, configured, running, dm:pairing, works` tandis que l'utilisateur a toujours signalé que les messages ne déclenchaient pas de journalisation utile.

Query:

`/Users/kevinlin/.local/bin/discrawl search "Google Chat setup service account audience" --limit 10`

Results:

- A retourné une discussion de support de configuration/authentification autour du JSON de compte de service, de l'audience et d'appPrincipal, démontrant que le statut et les docs doivent rendre l'état principal/audience plus actionnable.
