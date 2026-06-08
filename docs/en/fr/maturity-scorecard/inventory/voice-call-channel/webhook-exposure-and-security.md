---
title: "Canal Voice Call - Note de Maturité Accès et Identité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Canal Voice Call - Note de Maturité Accès et Identité

## Résumé

Cette note migre les preuves de maturité archivées pour `canal Voice Call` / `Exposition et Sécurité Webhook` dans l'inventaire actuel du scorecard process-version-3.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Accès et Identité`
- Fusionnée depuis : `Sécurité Webhook`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Canal Voice Call : Exposition et Sécurité Webhook

## Fonctionnalités

- Canal Voice Call : Exposition et Sécurité Webhook

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (60%)`

L'exposition et la sécurité des webhooks disposent de preuves d'implémentation larges : validation d'URL publique, service par tunnel/Tailscale, gestion des proxies de confiance, vérification de signature, protection contre la relecture, limites de corps, délais de requête, limites en vol, chemins stricts et portes de mise à niveau WebSocket. La couverture est Alpha plutôt que Beta car les preuves sont encore principalement au niveau local/intégration et l'état de l'archive montre des corrections actives des bords proxy/chemin.

## Score de Qualité

- Score : `Alpha (62%)`

La qualité est basée sur la posture de sécurité fail-closed, les contraintes proxy/en-tête, la conception de relecture et l'état de défaut actif. L'existence de tests et l'étendue des tests n'ont pas été comptabilisées dans ce score de Qualité.

C'est l'un des composants les plus solides car il rejette le trafic non authentifié avant l'analyse coûteuse du corps, contraint les hôtes/proxies transférés et nécessite des URL publiques pour les fournisseurs externes. Il reste Alpha car l'exposition publique est opérationnellement fragile et il y a des problèmes actifs de bord webhook/proxy.

## Score de Complétude

- Score : `Alpha (60%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-call-channel.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le Canal Voice Call.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude process-version-3, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Les corrections de proxy et de chemin de flux sont assez actives pour maintenir ceci en dessous de Beta.
- L'exposition publique dépend de l'infrastructure de l'opérateur et ne peut pas être déduite des vérifications unitaires/locales.
- Aucune matrice de scénario relecture/signature/URL publique en direct n'a été trouvée pour les trois fournisseurs externes.

## Preuves

### Docs

- `docs/plugins/voice-call.md:83-88` nécessite une URL de webhook publique pour Twilio, Telnyx et Plivo et indique que les hôtes loopback/privés sont rejetés pour les fournisseurs externes.
- `docs/plugins/voice-call.md:170-204` documente les notes d'exposition/sécurité du fournisseur, les limites de connexion de flux et le comportement de migration du docteur.
- `docs/plugins/voice-call.md:683-704` documente la sécurité des webhooks, les hôtes autorisés, les IP de proxy de confiance, les en-têtes de transfert, la protection contre la relecture pour Twilio/Plivo, les jetons par tour, le rejet non authentifié avant l'analyse du corps, les limites de requête 64 KB/5 secondes et les limites en vol par IP.
- `docs/cli/voicecall.md:178-199` documente les commandes d'exposition Tailscale serve/funnel.

### Source

- `extensions/voice-call/src/runtime.ts:263-528` résout la sélection d'URL publique/tunnel/Tailscale et échoue les fournisseurs externes si seule l'exposition de webhook local/privé est disponible.
- `extensions/voice-call/src/webhook-security.ts:240-345` reconstruit les URL publiques à partir des en-têtes de proxy de confiance, des hôtes autorisés et des IP de proxy de confiance.
- `extensions/voice-call/src/webhook-security.ts:482-547` implémente la vérification de signature Telnyx avec gestion de l'horodatage/relecture.
- `extensions/voice-call/src/webhook-security.ts:552-683` implémente la vérification de signature Twilio, les variantes d'URL publique/transférée, la gestion de la relecture et le comportement de saut de développement.
- `extensions/voice-call/src/webhook-security.ts:854-980` implémente la vérification Plivo V3/V2 et la gestion de la relecture.
- `extensions/voice-call/src/webhook.ts:657-810` applique les portes de chemin/méthode, les en-têtes de pré-authentification, les limites de corps/en vol, la vérification du fournisseur, les vérifications de relecture, les listes blanches en temps réel et le comportement d'analyse/traitement/cache.

### Tests d'intégration

- `extensions/voice-call/src/webhook.test.ts:348-460` couvre le comportement de confiance IP du client de flux média.
- `extensions/voice-call/src/webhook.test.ts:620-650` rejette les chemins de webhook ressemblant à des préfixes.
- `extensions/voice-call/src/webhook.test.ts:703-800` couvre le comportement de relecture et les effets secondaires de relecture Plivo.
- `extensions/voice-call/src/webhook.test.ts:972-1031` empêche les webhooks Twilio en temps réel relus de frapper l'état du flux.
- `extensions/voice-call/src/webhook.test.ts:1098-1200` couvre le rejet de liste blanche en temps réel et les chemins de flux acceptés.
- `extensions/voice-call/src/webhook.test.ts:1276-1394` couvre le rejet de signature manquante, les limites de taille de corps et les limites en vol avant authentification.

### Tests unitaires

- `extensions/voice-call/src/webhook-security.test.ts:286-500` couvre la détection de relecture et le comportement de vérification Plivo V2/V3.
- `extensions/voice-call/src/webhook-security.test.ts:502-628` couvre la relecture Telnyx, la gestion des requêtes Twilio, l'idempotence, le rejet d'hôte transféré invalide et la compatibilité ngrok.
- `extensions/voice-call/src/config.test.ts:32-279` couvre la validation des identifiants/env du fournisseur qui contrôle le démarrage du runtime webhook.

### Requêtes Gitcrawl

- `gitcrawl search issues "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #79918 pour les mises à niveau WebSocket en temps réel acceptant les chemins de flux frères et #86525 pour les proxies de confiance signalés comme des adresses mappées IPv4.
- `gitcrawl search prs "voice-call" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : a retourné #79919 pour le resserrement des chemins de mise à niveau de flux en temps réel et #86527 pour la correspondance de proxy de confiance mappée IPv4.
- `gitcrawl search issues "voicecall setup smoke webhook" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20` : n'a retourné aucun résultat pour les termes exacts de configuration/smoke webhook.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call webhook guard public url"` : a retourné des preuves que la garde webhook a atterri sur main donc Twilio/Telnyx/Plivo échouent rapidement si la résolution d'URL publique/tunnel/Tailscale reviendrait à des URL loopback/privées.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call twilio telnyx plivo"` : a retourné des conseils répétés visibles par l'utilisateur selon lesquels les vrais fournisseurs de transporteurs ont besoin d'une Gateway webhook accessible publiquement.
- `/Users/kevinlin/.local/bin/discrawl --json search --limit 10 "voice-call realtime twilio"` : a retourné une discussion d'examen et de PR autour de l'interception TwiML en temps réel sortante, les appels de notification et le comportement d'attachement de flux.

### Snapshot de source archivée

- `gitcrawl doctor --json` : `version=0.2.1`, `api_supported=false`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `github_token_present=false`, `openai_key_present=true`.
- `/Users/kevinlin/.local/bin/discrawl status --json` : `state=current`, `generated_at=2026-05-29T16:49:09Z`, `last_sync_at=2026-05-29T15:59:50Z`, `messages=1487061`, `channels=25819`, `threads=25591`, `embedding_backlog=0`, `share.needs_update=true`.
