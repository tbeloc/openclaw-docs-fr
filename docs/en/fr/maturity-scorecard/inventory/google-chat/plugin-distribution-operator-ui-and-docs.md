---
title: "Google Chat - Plugin Distribution Operator UI and Docs Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Google Chat - Plugin Distribution Operator UI and Docs Maturity Note

## Summary

Google Chat est bien représenté dans les métadonnées des plugins, la navigation des docs, les catalogues d'installation, les étiquettes Android, les cartes d'état de l'interface de contrôle et les pages d'aperçu des canaux. La couverture de distribution est plus forte que la surface d'exécution, mais la qualité reste Alpha car les docs/status/operator UI n'absorbent pas encore la complexité complète de Workspace/admin, la limitation user-OAuth, la nuance appPrincipal et les modes de défaillance space/thread exposés dans les preuves d'archive.

## Category Scope

Cette note couvre les métadonnées des plugins npm/ClawHub, la navigation des docs, les références de plugins, le catalogue officiel de plugins externes, les étiquettes de canal Android/interface de contrôle, le rendu des cartes d'état, les métadonnées d'installation/mise à jour, les alias de canaux et la documentation destinée aux opérateurs. Elle exclut le comportement d'exécution principal déjà noté dans les notes de configuration, webhook, routage, livraison, actions, média et compte/statut.

## Features

- Installation NPM et ClawHub : Couvre l'installation NPM et ClawHub sur les métadonnées des plugins npm/ClawHub, la navigation des docs, les références de plugins, le catalogue officiel de plugins externes et le comportement associé de l'interface utilisateur et des docs de l'opérateur de distribution de plugins.
- Routage des docs et du catalogue des plugins : Couvre le routage des docs et du catalogue des plugins sur les métadonnées des plugins npm/ClawHub, la navigation des docs, les références de plugins, le catalogue officiel de plugins externes et le comportement associé de l'interface utilisateur et des docs de l'opérateur de distribution de plugins.
- Alias et étiquettes de canaux : Couvre les alias et étiquettes de canaux sur les métadonnées des plugins npm/ClawHub, la navigation des docs, les références de plugins, le catalogue officiel de plugins externes et le comportement associé de l'interface utilisateur et des docs de l'opérateur de distribution de plugins.
- Interface utilisateur d'état de l'opérateur : Couvre l'interface utilisateur d'état de l'opérateur sur les métadonnées des plugins npm/ClawHub, la navigation des docs, les références de plugins, le catalogue officiel de plugins externes et le comportement associé de l'interface utilisateur et des docs de l'opérateur de distribution de plugins.
- Métadonnées d'installation/mise à jour : Couvre les métadonnées d'installation/mise à jour sur les métadonnées des plugins npm/ClawHub, la navigation des docs, les références de plugins, le catalogue officiel de plugins externes et le comportement associé de l'interface utilisateur et des docs de l'opérateur de distribution de plugins.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Coverage Score

- Score: `Beta (70%)`
- Signaux positifs : Les métadonnées des plugins déclarent les routes d'installation npm/ClawHub, le chemin des docs, les alias, les variables d'environnement de canal, les options CLI add, les métadonnées de publication et la compatibilité. Les tests couvrent la résolution du catalogue officiel de plugins externes, les entrées de build groupées, les assistants d'installation, les ID/alias de canaux, le rendu des cartes de l'interface de contrôle et les garde-fous d'importation de plugins.
- Signaux négatifs : La couverture de distribution/statut ne prouve pas l'installation de bout en bout réelle à partir de npm/ClawHub via la configuration de Google Cloud et le premier message. La couverture de l'interface utilisateur/statut est également principalement un rendu statique et une preuve d'état de configuration, pas un flux de travail de réparation d'opérateur.
- Lacunes d'intégration : Ajouter un smoke d'installation qui installe `@openclaw/googlechat`, vérifie les liens des docs et les champs de la carte d'état, exécute l'assistant d'installation ou `channels add`, démarre la passerelle et confirme que l'opérateur peut diagnostiquer un webhook Google-side défaillant.

## Quality Score

- Score: `Alpha (66%)`
- Rapports Gitcrawl : #9764, #58514, #65007, #80995, #82014, #42510 et #69422 montrent que les surfaces docs/opérateur n'ont pas encore éliminé la confusion autour de user OAuth, des espaces, des charges utiles, du routage des threads et du cycle de vie de la saisie. #71078/#57542/#53888 montrent que les diagnostics d'authentification ont dû être améliorés après les défaillances opaque appPrincipal.
- Rapports Discrawl : `discrawl search "Google Chat setup service account audience" --limit 10` a retourné des conseils d'opérateur et une confusion appPrincipal ; `discrawl search "Google Chat appPrincipal" --limit 10` a retourné une discussion issue/PR montrant que les avertissements et les journaux se sont améliorés mais le contrat de configuration reste nuancé. Les discussions de version pour 2026.5.27-beta.1 ont explicitement appelé le comportement des threads Google Chat DM comme valant la peine d'être testé, pas réglé.
- Bonnes qualités : Les docs sont découvrables, le plugin est externalisé avec des métadonnées de production, la carte de canal expose l'état des identifiants/audience/sonde et les pages de référence acheminent les utilisateurs de l'inventaire des plugins vers les docs de canal. Le canal est également visible dans les docs CLI, les références de l'assistant, les étiquettes Android et la navigation des docs.
- Mauvaises qualités : Les surfaces d'opérateur surestiment la disponibilité si elles sont lues uniquement comme installées/configurées/en cours d'exécution. Les docs publiques ne portent pas encore tous les points douloureux en direct : valeurs numériques appPrincipal, variantes de charge utile add-on, lacunes de portée OAuth service-account versus user, pas de réception de tous les messages d'espace et comportements de saisie/thread obsolètes.
- Exclu de la qualité : La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Completeness Score

- Score: `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-chat.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent l'étendue de la taxonomie pour l'installation NPM et ClawHub, le routage des docs et du catalogue des plugins, les alias et étiquettes de canaux, l'interface utilisateur d'état de l'opérateur, les métadonnées d'installation/mise à jour.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Ajouter une section « Ce que le statut prouve et ce qu'il ne prouve pas » pour Google Chat.
- Mettre à jour les docs pour séparer les capacités supportées par service-account des capacités requises par user-OAuth.
- Ajouter un tableau de réparation d'opérateur pour appPrincipal, les charges utiles add-on, les listes blanches d'espaces, les fuites de threads et les espaces réservés de saisie obsolètes.
- Ajouter un vrai smoke d'installation/configuration/statut pour le package de plugin externalisé.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md`: docs de canal principal avec installation, configuration, URL publique, config, cibles, dépannage et liens connexes.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/googlechat.md`: référence de plugin pour `@openclaw/googlechat`.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md` et `/Users/kevinlin/code/openclaw/docs/plugins/reference.md`: listent Google Chat avec distribution npm/ClawHub et surface de canal.
- `/Users/kevinlin/code/openclaw/docs/channels/index.md`: liste Google Chat comme canal de plugin téléchargeable.
- `/Users/kevinlin/code/openclaw/docs/docs.json`: contient la route des docs Google Chat et la redirection depuis `/providers/googlechat`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/googlechat/package.json`: contient les métadonnées du plugin OpenClaw, la spécification npm, le chemin des docs, les alias, les métadonnées d'installation, les métadonnées de compatibilité et les drapeaux de version.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/index.ts`: exporte l'ID du plugin, le nom, la description, la configuration et les points d'entrée d'exécution.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/channels.googlechat.ts`: rend les champs de la carte d'état Google Chat incluant les identifiants, l'audience, les horodatages de dernier démarrage/sonde, le résultat de la sonde et la section de configuration.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/channels.ts`: inclut Google Chat dans la vue des canaux.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/NodeRuntime.kt`: mappe `googlechat` à `Google Chat` pour les étiquettes de canal Android.
- `/Users/kevinlin/code/openclaw/src/plugins/official-external-plugin-catalog.test.ts`: vérifie que le catalogue officiel de plugins externes résout Google Chat en `@openclaw/googlechat`.

### Integration tests

- Aucun smoke d'installation/configuration/statut en direct dédié pour le package Google Chat externe n'a été trouvé.
- `/Users/kevinlin/code/openclaw/test/scripts/bundled-plugin-build-entries.test.ts`: couvre les entrées de build de plugin groupées Google Chat.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/contracts/channel-import-guardrails.test.ts`: inclut Google Chat dans les garde-fous d'importation de canal.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/channels.test.ts`: couvre les chemins de rendu de vue de canal qui incluent Google Chat.

### Unit tests

- `/Users/kevinlin/code/openclaw/src/channels/ids.test.ts`: vérifie que les alias `gchat` et `google-chat` se normalisent en `googlechat`.
- `/Users/kevinlin/code/openclaw/src/plugins/official-external-plugin-catalog.test.ts`: vérifie les métadonnées d'installation officielles pour `googlechat`.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/bundled.shape-guard.test.ts`: couvre la forme du point d'entrée d'exécution/API Google Chat.
- `/Users/kevinlin/code/openclaw/extensions/googlechat/src/channel.test.ts`: couvre le comportement des métadonnées/capacités de l'adaptateur de canal Google Chat.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/setup-wizard-helpers.test.ts`: inclut les chemins d'assistance d'installation Google Chat.

### Gitcrawl queries

Query:

`gitcrawl search issues "Google Chat plugin install npm ClawHub disabled" --repo openclaw/openclaw --limit 15 --json number,title,state,updatedAt,url`

Results:

- N'a retourné aucun hit direct de problème d'installation Google Chat. C'est neutre après les vérifications de fraîcheur réussies ; les préoccupations de qualité provenaient de rapports d'opérateur/exécution plus larges.

Query:

`gitcrawl search issues "Google Chat" --repo openclaw/openclaw --limit 20 --json number,title,state,updatedAt,url`

Results:

- A retourné les problèmes d'exécution/opérateur ouverts #65007, #80995, #82014, #44347, #49350, #77307, #58514, #42510, #9764, #69422 et #39843, qui affectent tous les attentes des surfaces docs/statut d'opérateur.

Query:

`gitcrawl gh issue view 71078 --repo openclaw/openclaw --json number,title,state,updatedAt,url,body`

Results:

- A retourné le #71078 fermé, qui documente la lacune d'observabilité antérieure autour des raisons de rejet d'authentification Google Chat avalées.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search "Google Chat setup service account audience" --limit 10`

Results:

- A retourné des conseils de configuration d'opérateur et un contexte de débogage appPrincipal/audience, montrant que la surface docs/statut doit couvrir plus que l'installation de package.

Query:

`/Users/kevinlin/.local/bin/discrawl search "Google Chat appPrincipal" --limit 10`

Results:

- A retourné des commentaires de problèmes et des discussions de PR sur les avertissements appPrincipal, les valeurs JWT numériques `sub` et les améliorations de journalisation de rejet d'authentification.
