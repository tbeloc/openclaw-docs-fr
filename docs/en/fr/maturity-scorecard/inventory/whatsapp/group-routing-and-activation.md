---
title: "WhatsApp - Note de Maturité du Routage et de la Livraison des Conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Note de Maturité du Routage et de la Livraison des Conversations

## Résumé

Le routage et l'activation des groupes WhatsApp sont en Beta. La documentation et le code source couvrent les listes blanches de groupes, le contrôle d'accès par mention, l'activation du propriétaire, les clés de session de groupe déterministes, la diffusion en éventail, le contexte des participants et le comportement des invites de groupe. Le statut reste en Beta car la configuration des groupes est fragile en pratique et les archives montrent toujours une confusion des opérateurs autour des JID de groupe exacts, des ID de compte et des exigences de mention.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Conversation Routing and Delivery`
- Fusionnée à partir de : `Message Routing and Delivery`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Listes blanches de groupes : Listes blanches de groupes, groupPolicy, JID de groupe exacts, requireMention, propriétaire
- Clés de session de groupe : Clés de session de groupe, diffusion en éventail, mentions sortantes et invite de groupe
- Envois de texte sortants : Envois de texte sortants, livraison par outil de message, DM/groupe/infolettre explicites
- Reçus acceptés par le fournisseur : Reçus acceptés par le fournisseur et identifiants de livraison durables
- Envois de texte sortants : Couvre les envois de texte sortants, la livraison par outil de message, le comportement explicite DM/groupe/infolettre.
- Reçus acceptés par le fournisseur et identifiants de livraison durables : Portée des preuves pour les reçus acceptés par le fournisseur et les identifiants de livraison durables.

## Fonctionnalités

- Listes blanches de groupes : Listes blanches de groupes, groupPolicy, JID de groupe exacts, requireMention, propriétaire
- Clés de session de groupe : Clés de session de groupe, diffusion en éventail, mentions sortantes et invite de groupe
- Envois de texte sortants : Envois de texte sortants, livraison par outil de message, DM/groupe/infolettre explicites
- Reçus acceptés par le fournisseur : Reçus acceptés par le fournisseur et identifiants de livraison durables

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (76%)`
- Signaux positifs : la documentation couvre le routage des groupes, les messages de groupe, l'activation, les clés de session de groupe, les mentions et le dépannage ; le code source couvre le contrôle d'accès à la réception de message, l'activation de groupe, la diffusion, les clés de session, la politique entrante et les mentions sortantes.
- Signaux négatifs : une preuve en direct existe pour le contrôle d'accès par mention, mais pas la matrice complète des groupes de configuration JID exacte, activation, invites génériques, diffusion et contexte des participants.
- Lacunes d'intégration : aucun scénario en direct localisé ne prouve le routage JID de groupe multi-compte, l'activation du propriétaire, l'admission contrôlée par mention et la diffusion en éventail des réponses ensemble.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : `whatsapp group mention gating groupPolicy` a surfacé #63589 pour l'identité des participants/contexte de réponse citée dans les journaux d'entrée de passerelle et #76135 pour les sessions de groupe de messagerie privée afin de surfacer la progression détaillée/outil.
- Rapports Discrawl : les recherches de groupe ont retourné des conseils selon lesquels le JID de groupe exact et l'ID de compte doivent correspondre et que la plupart des rapports « messages de groupe non reçus » sont des problèmes de contrôle d'accès par mention ou de contrôle d'accès.
- Bonnes qualités : l'admission au groupe est explicite, les clés de session de groupe sont déterministes, les invites de groupe distinguent l'admission générique et le code source centralise le contrôle d'accès avant la distribution.
- Mauvaises qualités : la configuration de l'opérateur a plusieurs champs de correspondance exacte, la découverte du JID de groupe n'est pas toujours évidente et la progression des groupes/sessions privés a toujours des demandes UX ouvertes.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas augmenté ni diminué ce score de Qualité.

## Score de Complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : les archives de documentation, code source, tests, Gitcrawl et preuves Discrawl couvrent la portée de la taxonomie pour les listes blanches de groupes, les clés de session de groupe, les envois de texte sortants, les reçus acceptés par le fournisseur.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un scénario de routage de groupe en direct qui prouve le JID de groupe exact, l'ID de compte, le contrôle d'accès par mention, l'activation du propriétaire et la livraison des réponses de groupe.
- Améliorer les diagnostics pour les messages de groupe supprimés afin que les défaillances de politique de mention, de politique de liste blanche et de politique de mauvais compte soient distinctes.
- Décider si les sessions de groupe privé doivent surfacer la progression détaillée/outil.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:165` documente les envois de groupe, les métadonnées de mention, le comportement d'ignorance de statut/diffusion, les clés de session de groupe et le comportement du JID de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:279` documente la politique de groupe, les mentions et l'activation.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:685` documente le dépannage pour les messages de groupe ignorés par le bot.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:703` documente la hiérarchie des invites système et les avertissements d'admission d'invite de groupe générique.
- `/Users/kevinlin/code/openclaw/docs/channels/group-messages.md:11` documente le comportement et le contexte spécifiques à WhatsApp pour les groupes.
- `/Users/kevinlin/code/openclaw/docs/channels/group-messages.md:61` documente l'activation réservée au propriétaire, l'utilisation, les vérifications de fumée et les considérations connues.

### Code Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/on-message.ts:97` achemine les messages et résout les sessions avant le traitement.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/on-message.ts:214` applique le contrôle d'accès de groupe, la gestion de la diffusion et la distribution des processus.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/group-gating.ts:131` applique les listes blanches de groupes, les mentions, l'activation et l'historique en attente.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/group-activation.ts:1` implémente l'état d'activation du groupe.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/broadcast.ts:1` gère la diffusion en éventail.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/group-session-key.ts:1` implémente le comportement de la clé de session de groupe.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/outbound-mentions.ts:1` mappe le comportement des mentions sortantes pour le contexte de groupe entrant.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:235` définit le scénario en direct `whatsapp-mention-gating`.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.test.ts:235` vérifie la configuration du scénario de groupe de mention.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.broadcast-groups.combined.test.ts:1` couvre le comportement combiné de diffusion de groupe de réponse automatique.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.web-auto-reply.connection-and-logging.e2e.test.ts:939` couvre le traitement du moniteur des messages entrants dans la résolution des réponses.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/web-auto-reply-monitor.test.ts:170` couvre le comportement du contrôle d'accès de groupe.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/group-gating.allowlist-warn.test.ts:1` couvre les avertissements de liste blanche de groupe.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/group-activation.test.ts:1` couvre l'activation du groupe.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/group-gating.audio-preflight.test.ts:1` couvre le contrôle d'accès de groupe lors du précontrôle audio.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/group-policy.test.ts:1` et `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/group-session-key.test.ts:1` couvrent le comportement de la politique et de la clé de session.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp group mention gating groupPolicy" --json`

Résultats :

- A surfacé #63589 pour l'identité des participants/contexte de réponse citée dans les journaux d'entrée de passerelle.
- A surfacé #76135 pour les sessions de groupe de messagerie privée afin de surfacer la progression détaillée/outil.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp group mention gating groupPolicy" --limit 5`

Résultats :

- A retourné des conseils selon lesquels le JID de groupe exact et l'ID de compte doivent correspondre pour plusieurs comptes, que le routage de groupe ne contourne pas les contrôles d'accès, une note d'examen sur les valeurs par défaut de compte héritées dans le contrôle d'accès de groupe et un fil de support où « les messages de groupe non reçus » était probablement un contrôle d'accès par mention.
