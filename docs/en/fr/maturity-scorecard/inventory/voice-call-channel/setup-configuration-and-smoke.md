---
title: "Canal Voice Call - Note de Maturité de Configuration et d'Exploitation du Canal"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Canal Voice Call - Note de Maturité de Configuration et d'Exploitation du Canal

## Résumé

Cette note migre les preuves de maturité archivées pour le `canal Voice Call` / `Configuration, Setup et Smoke` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Configuration et Exploitation du Canal`
- Fusionnée à partir de : `Configuration et Exploitation`, `Sécurité des Webhooks`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Canal Voice Call : Cli, Gateway Rpc et Agent Tool
- Canal Voice Call : Configuration, Setup et Smoke
- Canal Voice Call : Exposition et Sécurité des Webhooks

## Fonctionnalités

- Canal Voice Call : Cli, Gateway Rpc et Agent Tool
- Canal Voice Call : Configuration, Setup et Smoke

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Expérimental (42%)`

La configuration dispose d'un vrai chemin de documentation, de métadonnées de manifeste, de validation du runtime Gateway, de vérifications d'état de configuration et de commandes smoke en mode dry-run/live. Elle reste Expérimentale car les preuves ne montrent pas une suite de configuration live reproductible sur les opérateurs supportés, et les preuves archivées montrent que la configuration reste sensible à la configuration du processus Gateway, à l'exposition publique des webhooks et à l'alignement des schémas/SecretRef.

## Score de Qualité

- Score : `Alpha (56%)`

La qualité est basée sur la documentation, les contrats de runtime, le comportement fail-closed et l'état des problèmes ouverts/archives. L'existence et l'étendue des tests n'ont pas été comptabilisées dans ce score de Qualité.

L'implémentation dispose d'un modèle de configuration cohérent centré sur Gateway, d'une validation explicite des identifiants du fournisseur, de valeurs par défaut smoke en mode dry-run et d'un comportement fail-closed pour les URL publiques. Elle n'est pas plus élevée car la configuration s'étend sur l'env du service local, l'état d'installation du plugin, l'état de redémarrage du Gateway, les webhooks publics, les SecretRefs et les tunnels optionnels, qui apparaissent tous comme des frictions d'opérateur dans les archives.

## Score de Complétude

- Score : `Expérimental (42%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Voice Call Channel, Voice Call Channel.
- Signaux négatifs : la note archivée a précédé la notation de Complétude process-version-3, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucune matrice de configuration live n'a été trouvée pour Twilio, Telnyx et Plivo.
- La configuration dépend de l'env du processus Gateway et de l'état de redémarrage, que les preuves Discord montrent peuvent différer de l'état CLI interactif.
- Les chemins Manifest/schéma, SecretRef et identifiants du fournisseur ont suffisamment de friction historique pour que le chemin de configuration reste Expérimental.

## Preuves

### Documentation

- `docs/plugins/voice-call.md:19-23` indique que le plugin s'exécute à l'intérieur du processus Gateway et doit être installé/configuré sur la machine Gateway.
- `docs/plugins/voice-call.md:25-80` documente les commandes d'installation, configuration, setup et smoke ; la configuration vérifie l'activation du plugin, les identifiants du fournisseur, l'exposition des webhooks et le mode audio ; smoke utilise par défaut le mode dry-run et nécessite `--yes` pour les appels live.
- `docs/plugins/voice-call.md:83-99` nécessite une URL de webhook publique pour Twilio/Telnyx/Plivo et indique que les identifiants de fournisseur manquants ignorent l'initialisation du runtime.
- `docs/cli/voicecall.md:9-14` indique que la commande `voicecall` apparaît lorsque le plugin est installé/activé et que les commandes Gateway acheminent vers le runtime Gateway avec secours autonome.
- `docs/cli/voicecall.md:47-78` documente le comportement de setup et smoke, y compris l'exigence de webhook public.

### Source

- `extensions/voice-call/openclaw.plugin.json:1-26` définit l'id du plugin `voice-call`, l'alias de commande `voicecall`, le contrat d'outil `voice_call` et les variables d'env du fournisseur/tunnel.
- `extensions/voice-call/src/config.ts:740-883` résout les paramètres du fournisseur/tunnel/webhook basés sur l'env et valide les identifiants du fournisseur plus les contraintes de streaming/realtime.
- `extensions/voice-call/src/runtime.ts:263-528` crée le runtime, valide le comportement du fournisseur/URL publique, démarre le serveur webhook et nettoie les défaillances d'initialisation.
- `extensions/voice-call/src/cli.ts:285-332` construit l'état de configuration pour l'activation du plugin, la configuration du fournisseur, l'exposition des webhooks et le mode audio.
- `extensions/voice-call/src/cli.ts:406-515` enregistre les commandes setup et smoke, y compris les chemins dry-run et appels live.

### Tests d'intégration

- `extensions/voice-call/src/runtime.test.ts:208-260` couvre le nettoyage lorsque l'initialisation du runtime échoue.
- `extensions/voice-call/src/runtime.test.ts:284-303` vérifie que la configuration complète est transmise à la configuration du serveur webhook.
- `extensions/voice-call/src/runtime.test.ts:305-351` vérifie que les fournisseurs externes échouent fermés sur les webhooks locaux uniquement et acceptent les URL publiques.

### Tests unitaires

- `extensions/voice-call/src/config.test.ts:32-279` couvre la validation des identifiants/env du fournisseur et la gestion des SecretRef.
- `extensions/voice-call/src/config.test.ts:399-545` couvre les valeurs par défaut, le chemin de flux realtime personnalisé, les remplacements TTS et les paramètres realtime.
- `extensions/voice-call/src/config-compat.test.ts:11-162` couvre la migration de la forme de configuration héritée et la sortie d'avertissement/changement du doctor.

### Requêtes Gitcrawl

- `gitcrawl search issues "voicecall setup smoke webhook" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : n'a retourné aucun résultat, donc aucune preuve d'archive de problèmes n'a été trouvée pour ces termes exacts de setup/smoke.
- `gitcrawl search prs "voicecall setup smoke webhook" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : n'a retourné aucun résultat, donc aucune preuve d'archive de PR n'a été trouvée pour ces termes exacts de setup/smoke.
- `gitcrawl search issues "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné des problèmes voice-call ouverts larges incluant la latence (#79521), le reaper Twilio obsolète (#79121), la musique d'attente échouée/sans flux (#81122), double salutation (#85846), mises à niveau du chemin de flux frère (#79918) et liaison d'outil (#80840), qui maintiennent la certitude de configuration en dessous de Beta car le chemin change encore activement.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voicecall setup smoke webhook"` : a retourné `null`, donc aucun hit d'archive Discord n'a été trouvé pour ces termes exacts.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call twilio telnyx plivo"` : a retourné des conseils de configuration visibles par l'utilisateur pour installer `@openclaw/voice-call`, configurer `plugins.entries["voice-call"].config`, choisir Twilio/Telnyx/Plivo, exposer un webhook public et noter que le plugin s'exécute à l'intérieur du Gateway.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call webhook guard public url"` : a retourné des preuves que la garde webhook a atterri pour que les fournisseurs externes échouent rapidement lorsqu'ils reviendraient à des URL loopback/privées.

### Snapshot source archivé

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
