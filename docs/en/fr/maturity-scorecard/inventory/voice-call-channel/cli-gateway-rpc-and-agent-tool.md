---
title: "Voice Call channel - CLI, Gateway RPC, and Agent Tool Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice Call channel - CLI, Gateway RPC, and Agent Tool Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Voice Call channel` / `CLI, Gateway RPC, and Agent Tool` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Voice Call channel représentée par ces fonctionnalités de taxonomie :

- Voice Call Channel: Cli, Gateway Rpc, and Agent Tool

## Fonctionnalités

- Voice Call Channel: Cli, Gateway Rpc, and Agent Tool

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (45%)`

La surface de commande/RPC/outil existe et est documentée : sous-commandes CLI `voicecall`, délégation d'exécution Gateway, actions d'outil `voice_call`, méthodes RPC Gateway, journaux, latence et assistants d'exposition. Elle reste Experimental car les preuves n'incluent pas une matrice d'opérateur stable de bout en bout et les preuves d'archive Discord montrent que le comportement singleton/RPC d'exécution peut échouer dans les configurations Gateway déployées.

## Score de qualité

- Score : `Alpha (56%)`

La qualité est basée sur la forme de l'API, la conception de délégation Gateway, la sémantique de secours, les crochets d'observabilité et l'état d'archive d'opérateur actif. L'existence de tests et l'étendue des tests n'ont pas été comptabilisées dans ce score de qualité.

La conception CLI est pratique : la délégation Gateway-first évite la duplication d'exécution locale en cas de bon fonctionnement, les valeurs par défaut de smoke sont prudentes, et les commandes status/tail/latency exposent l'état opérationnel. La qualité est limitée par l'exigence documentée que la commande n'existe que lorsqu'elle est installée/activée et par un rapport d'opérateur où l'invocation de `voice_call` pourrait initialiser un deuxième runtime webhook et rencontrer `EADDRINUSE`.

## Score de complétude

- Score : `Experimental (45%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour Voice Call Channel.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le comportement singleton d'exécution pour l'invocation d'outil agent a besoin d'une preuve plus forte.
- Le comportement de redémarrage Gateway/enregistrement RPC a une incertitude d'opérateur dans les preuves d'archive Discord.
- Aucune matrice de scénario CLI/Gateway/outil de bout en bout n'a été trouvée pour les commandes install, setup, call, speak, DTMF, end, status, logs, latency et expose.

## Preuves

### Docs

- `docs/cli/voicecall.md:9-14` documente la disponibilité de la commande plugin, la délégation Gateway et le secours autonome.
- `docs/cli/voicecall.md:17-45` documente les sous-commandes voicecall.
- `docs/cli/voicecall.md:47-155` documente les drapeaux de configuration, smoke et cycle de vie d'appel.
- `docs/cli/voicecall.md:157-177` documente les métriques de journaux et de latence.
- `docs/cli/voicecall.md:178-199` documente les assistants expose/Tailscale serve/funnel.
- `docs/plugins/voice-call.md:725-748` documente les commandes CLI, la délégation Gateway lors de l'exécution et la latence de `calls.jsonl`.
- `docs/plugins/voice-call.md:750-763` documente les actions d'outil agent `voice_call`.
- `docs/plugins/voice-call.md:765-778` documente les méthodes RPC Gateway.
- `skills/voice-call/SKILL.md:15-44` documente le flux de compétence voice-call, l'exigence d'activation du plugin, CLI, les actions d'outil et les notes de configuration.

### Source

- `extensions/voice-call/openclaw.plugin.json:1-12` déclare l'id du plugin, l'alias de commande et le contrat d'outil `voice_call`.
- `extensions/voice-call/src/cli.ts:406-515` enregistre le comportement de la commande setup/smoke.
- `extensions/voice-call/src/cli.ts:520-867` enregistre les commandes call, start, continue, speak, DTMF, end, status, tail, latency, expose et le comportement de secours Gateway.
- `extensions/voice-call/src/runtime.ts:263-528` crée l'exécution utilisée par les chemins CLI/Gateway/outil.
- `docs/gateway/protocol.md:390` inclut la couverture `talk.event` pour l'observabilité de la téléphonie.

### Tests d'intégration

- `extensions/voice-call/src/runtime.test.ts:208-260` couvre le nettoyage d'exécution en cas d'échec d'initialisation, pertinent pour les risques de duplication/exécution locale.
- `extensions/voice-call/src/runtime.test.ts:284-303` vérifie le transfert de configuration d'exécution à la configuration du serveur webhook.
- `extensions/voice-call/src/runtime.test.ts:380-465` couvre les métadonnées d'outil de consultation en temps réel et le comportement spawned-by.

### Tests unitaires

- `extensions/voice-call/src/config.test.ts:32-545` couvre la validation de configuration utilisée par les chemins de démarrage CLI/Gateway.
- `extensions/voice-call/src/manager.notify.test.ts:137-370` couvre le comportement de notification d'appel initial utilisé par les appels initiés par outil/CLI.
- `extensions/voice-call/src/manager.closed-loop.test.ts:35-245` couvre le comportement continue/turn utilisé par les chemins de cycle de vie CLI/outil.

### Requêtes Gitcrawl

- `gitcrawl search issues "voice_call agent tool voicecall status" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : n'a retourné aucun résultat pour ces termes exacts.
- `gitcrawl search issues "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #80840 pour les entrées realtime.tools annoncées au modèle sans chemin de liaison de gestionnaire, plus #77753 pour le routage d'appel multi-agent et #83967 pour le suivi de clé de session canonique.
- `gitcrawl search prs "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #80845 pour la livraison de résultat de consultation asynchrone, #77763 pour le routage des appels vers l'agent appelant et #83942 pour les objectifs sortants privés.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice_call agent tool voicecall status"` : a retourné un rapport d'opérateur où l'invocation de l'outil `voice_call` a produit `EADDRINUSE` sur le port webhook, suggérant qu'un deuxième runtime a été initialisé au lieu de partager le singleton Gateway ; le même fil a demandé si les méthodes RPC enregistrées par plugin devraient survivre au redémarrage Gateway.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call twilio telnyx plivo"` : a retourné des conseils orientés utilisateur selon lesquels la commande `openclaw voicecall call ...` n'est réelle que lorsque le plugin est installé et activé.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "google meet twilio voice-call"` : a retourné des notes d'utilisation en direct selon lesquelles `voice_call.initiate_call` a été utilisé pour un test Twilio audible frais tandis que l'état de transport Google Meet a été débogué séparément.

### Snapshot de source archivée

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
