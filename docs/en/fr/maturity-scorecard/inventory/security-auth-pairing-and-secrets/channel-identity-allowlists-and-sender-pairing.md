---
title: "Sécurité, authentification, appairage et secrets - Note de Maturité du Contrôle d'Accès aux Canaux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de Maturité du Contrôle d'Accès aux Canaux

## Résumé

OpenClaw dispose d'un large modèle de politique partagée pour la confiance des canaux entrants : appairage DM, listes blanches DM, listes blanches de groupe, groupes d'accès, mention gating, bootstrap du propriétaire et normalisation des expéditeurs spécifique au canal. La couverture est Beta car de nombreux canaux fournis ont des tests de politique ciblés, mais la parité est inégale et tous les canaux ne partagent pas encore un contrat d'entrée unifié. La qualité est Alpha car les preuves Discord montrent une confusion fréquente des opérateurs entre l'appairage DM et l'autorisation de groupe, les remplacements au niveau du compte, les listes blanches Slack/WhatsApp/Telegram et les avertissements d'exposition de commandes de groupe non sécurisées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Identité du Canal : Couvre l'Identité du Canal pour qui peut communiquer avec OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et l'identité du canal associée, les listes blanches et le comportement d'appairage des expéditeurs.
- Listes Blanches : Couvre les Listes Blanches pour qui peut communiquer avec OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et l'identité du canal associée, les listes blanches et le comportement d'appairage des expéditeurs.
- Appairage des Expéditeurs : Couvre l'Appairage des Expéditeurs pour qui peut communiquer avec OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et l'identité du canal associée, les listes blanches et le comportement d'appairage des expéditeurs.

## Fonctionnalités

- Identité du Canal : Couvre l'Identité du Canal pour qui peut communiquer avec OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et l'identité du canal associée, les listes blanches et le comportement d'appairage des expéditeurs.
- Listes Blanches : Couvre les Listes Blanches pour qui peut communiquer avec OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et l'identité du canal associée, les listes blanches et le comportement d'appairage des expéditeurs.
- Appairage des Expéditeurs : Couvre l'Appairage des Expéditeurs pour qui peut communiquer avec OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et l'identité du canal associée, les listes blanches et le comportement d'appairage des expéditeurs.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation des canaux publics documente systématiquement les contrôles d'appairage DM et de liste blanche, et de nombreux plugins de canal ont des tests de politique pour la correspondance des expéditeurs, la politique de groupe, le mention gating, l'authentification par approbation et l'autorisation de commande native.
- Signaux négatifs : Les preuves sont distribuées dans les suites de tests par canal. Une algèbre d'autorisation d'entrée partagée unique est toujours décrite comme un plan de refactorisation, ce qui rend la parité plus difficile à prouver sur les canaux de longue traîne.
- Lacunes d'intégration : Ajouter une suite de conformité inter-canaux pour l'appairage DM, le bootstrap du premier propriétaire, les listes blanches au niveau du compte, l'authentification des expéditeurs de groupe, le mention gating, les commandes natives et les effets secondaires de l'authentification par approbation.

## Score de Qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : La requête de problème exacte a retourné le problème ouvert #81876 concernant le basculement automatique des paramètres DM du canal vers les listes blanches du propriétaire après le bootstrap du premier propriétaire. La requête PR a retourné la PR ouverte #84461 pour la limitation de débit entrant par expéditeur Telegram.
- Rapports Discrawl : L'historique du support Discord montre une confusion et une mauvaise configuration récurrentes : commandes de groupe sans listes blanches d'expéditeurs, politique de groupe Slack bloquant les mentions, remplacements `dmPolicy` au niveau du compte WhatsApp, confusion de liaison groupe/DM BlueBubbles et utilisateurs collant des configurations avec des jetons de canal en texte brut lors du débogage d'accès.
- Bonnes qualités : La documentation distingue explicitement l'appairage DM de l'autorisation de groupe ; les groupes d'accès sont réutilisables ; de nombreux canaux définissent par défaut les groupes sur liste blanche ; et l'audit de sécurité détecte l'exposition de commandes de groupe à fort impact.
- Mauvaises qualités : La variance des canaux reste élevée, les diagnostics orientés utilisateur nécessitent souvent une interprétation approfondie de la configuration, et l'approbation d'appairage peut être confondue avec une autorisation de groupe ou de commande plus large.
- Exclu de la qualité : La largeur de couverture, la largeur des tests unitaires et la profondeur des tests d'intégration ne sont notées que sous Couverture.

## Score de Complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'Identité du Canal, les Listes Blanches, l'Appairage des Expéditeurs.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- La politique d'entrée partagée est toujours en cours de refactorisation des arbres de décision par plugin vers un graphe d'accès central unique.
- L'approbation d'appairage DM ne résout pas automatiquement l'accès au groupe, mais cette distinction reste un problème de support fréquent.
- Certaines documentations de canal et avertissements d'exécution utilisent une terminologie spécifique au canal, donc les opérateurs ont toujours besoin de connaissances par canal pour réparer l'accès.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/pairing.md` documente l'appairage DM, l'expiration du code d'appairage, les capacités en attente, le bootstrap du premier propriétaire, les canaux pris en charge, les groupes d'accès, les chemins du magasin d'appairage et la limite DM-versus-groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md`, `/Users/kevinlin/code/openclaw/docs/channels/discord.md`, `/Users/kevinlin/code/openclaw/docs/channels/slack.md` et `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md` documentent le comportement représentatif spécifique au canal DM, groupe, liste blanche et approbation.
- `/Users/kevinlin/code/openclaw/docs/channels/access-groups.md` documente les groupes d'expéditeurs réutilisables.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/audit-checks.md` documente `security.exposure.open_channels_with_exec`, les vérifications de groupe ouvert et de liste blanche d'expéditeurs.

### Source

- `/Users/kevinlin/code/openclaw/src/channels/direct-dm-access.ts` résout les décisions d'accès et d'appairage DM entrants.
- `/Users/kevinlin/code/openclaw/src/channels/allow-from.ts`, `/Users/kevinlin/code/openclaw/src/channels/allowlist-match.ts` et `/Users/kevinlin/code/openclaw/src/channels/mention-gating.ts` implémentent la correspondance des expéditeurs partagée et les mention gates.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/group-access.ts` et `/Users/kevinlin/code/openclaw/src/plugin-sdk/access-groups.ts` fournissent des aides d'accès réutilisables orientées plugin.
- Les implémentations de canaux fournis représentatifs se trouvent sous `/Users/kevinlin/code/openclaw/extensions/telegram`, `/Users/kevinlin/code/openclaw/extensions/discord`, `/Users/kevinlin/code/openclaw/extensions/slack`, `/Users/kevinlin/code/openclaw/extensions/whatsapp` et `/Users/kevinlin/code/openclaw/extensions/matrix`.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/group-access.base-access.test.ts` et `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.group-auth.test.ts` couvrent l'autorisation de groupe et de commande native Telegram.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/channel-access.test.ts` couvre le comportement d'accès au canal Discord.
- `/Users/kevinlin/code/openclaw/extensions/slack/src/group-policy.test.ts` et `/Users/kevinlin/code/openclaw/extensions/slack/src/monitor/provider.allowlist.test.ts` couvrent la politique de groupe Slack et les listes blanches du fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/access-control.test.ts` et `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/group-policy.test.ts` couvrent le contrôle d'accès entrant WhatsApp et la politique de groupe.
- `/Users/kevinlin/code/openclaw/extensions/zalo/src/monitor.pairing.lifecycle.test.ts` couvre le cycle de vie d'appairage du canal pour Zalo.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/channels/allowlist-match.test.ts`, `/Users/kevinlin/code/openclaw/src/channels/allow-from.test.ts` et `/Users/kevinlin/code/openclaw/src/channels/mention-gating.test.ts` couvrent les aides de politique partagée.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/pairing-adapters.test.ts` couvre le comportement de l'adaptateur d'appairage du plugin.
- Les fichiers `/Users/kevinlin/code/openclaw/extensions/*/src/approval-auth.test.ts` couvrent l'autorisation par approbation par canal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/resolve-allowlist-common.test.ts` et `/Users/kevinlin/code/openclaw/extensions/slack/src/resolve-allowlist-common.test.ts` couvrent la normalisation de la liste blanche.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "channel pairing dmPolicy allowlist groupPolicy ownerAllowFrom"`

Résultats :

- A retourné le problème ouvert #81876, `Auto-flip channel DM defaults to allowlist:[owner] after first-owner bootstrap`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "channel pairing dmPolicy ownerAllowFrom allowlist"`

Résultats :

- A retourné la PR ouverte #84461, `feat(channels/telegram): per-sender inbound rate limit`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "channel pairing dmPolicy allowlist groupPolicy ownerAllowFrom"`

Résultats :

- A retourné une configuration de support où Telegram avait `dmPolicy="pairing"`, des listes blanches du propriétaire, des cibles d'approbation exec et une configuration de jeton de passerelle ; utile comme preuve d'opérateur mais pas un défaut direct.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "dmPolicy pairing allowlist groupPolicy"`

Résultats :

- A trouvé des notes de conception du responsable pour une refactorisation d'entrée de canal.
- A trouvé des cas de support expliquant les listes blanches de politique de groupe Slack, les remplacements de politique au niveau du compte WhatsApp, le routage groupe/DM BlueBubbles, le bootstrap du propriétaire Telegram et les résultats d'audit de sécurité pour les commandes de groupe Telegram sans liste blanche d'expéditeurs.
