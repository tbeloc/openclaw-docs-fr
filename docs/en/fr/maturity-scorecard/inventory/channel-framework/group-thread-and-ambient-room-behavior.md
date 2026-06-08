---
title: "Cadre de canal - Note de maturité du comportement des threads de groupe et des salons ambiants"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Cadre de canal - Note de maturité du comportement des threads de groupe et des salons ambiants

## Résumé

Le comportement des groupes, threads et salons ambiants est bien documenté et dispose d'un vrai modèle multi-canal : les sessions de groupe sont isolées des DM, les portes de mention et de liste blanche contrôlent l'activation, l'historique du groupe peut être conservé pour le contexte, les événements de salon ambiant peuvent écouter silencieusement, et les politiques de thread/session acheminent les threads natifs et les sujets.

La limite de maturité est le support inégal des fournisseurs et la complexité opérationnelle. Le modèle fonctionne sur les principaux canaux, mais les preuves d'archive montrent que la liaison des threads et la sémantique ambiante/groupe continuent de changer, et les docs contiennent toujours des exceptions spécifiques aux fournisseurs que les opérateurs doivent réconcilier.

## Portée de la catégorie

Inclus dans cette catégorie :

- Isolation de session groupe/canal : Isolation de session groupe/canal et contexte d'historique de groupe
- Mention requise : Modes mention requise, toujours actif et événement de salon ambiant
- Threads natifs : Threads natifs, sujets, liaisons parent-enfant et comportement de génération de thread
- Groupes de diffusion : Groupes de diffusion et routage de groupe multi-agent
- Protection contre les boucles de bot : Protection contre les boucles de bot pour le comportement de salon

## Fonctionnalités

- Isolation de session groupe/canal : Isolation de session groupe/canal et contexte d'historique de groupe
- Mention requise : Modes mention requise, toujours actif et événement de salon ambiant
- Threads natifs : Threads natifs, sujets, liaisons parent-enfant et comportement de génération de thread
- Groupes de diffusion : Groupes de diffusion et routage de groupe multi-agent
- Protection contre les boucles de bot : Protection contre les boucles de bot pour le comportement de salon

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs :
  - Les docs couvrent les réponses visibles du groupe, l'accès au groupe, l'autorisation de déclenchement, la visibilité du contexte, les clés de session, le comportement de mention, l'historique du groupe, les événements de salon ambiant et les groupes de diffusion (`docs/channels/groups.md:21`, `docs/channels/groups.md:112`, `docs/channels/groups.md:149`, `docs/channels/groups.md:321`, `docs/channels/groups.md:373`, `docs/channels/ambient-room-events.md:11`, `docs/channels/broadcast-groups.md:21`).
  - La source couvre la politique de liaison des threads, la projection d'itinéraire, la résolution de conversation, le nettoyage de l'historique du groupe du noyau de tour, la protection contre les boucles de bot dans la distribution et les métadonnées de session.
  - Les tests unitaires exercent directement la politique de liaison des threads, la projection d'itinéraire, la résolution de conversation et le comportement du noyau de tour pour l'historique du groupe et les abandons de paires de bot.
  - Les docs des fournisseurs pour Discord et Matrix ont un comportement détaillé des threads natifs.
- Signaux négatifs :
  - Le support des événements de salon ambiant est explicitement limité à certains canaux.
  - Le comportement du groupe varie selon le canal et les docs des opérateurs s'appuient sur plusieurs pages plus des sections spécifiques aux fournisseurs.
  - Les preuves d'archive montrent que la liaison des threads/sessions reste un travail actif, en particulier pour Discord.
- Lacunes d'intégration :
  - Aucune matrice large groupe/ambiant/thread en direct n'a été trouvée sur Slack, Discord, Telegram, Matrix, WhatsApp et Signal.
  - Les groupes de diffusion ont des docs étendues, mais une preuve en direct plus forte n'a pas été trouvée dans ce passage d'audit.

## Score de qualité

- Score : `Alpha (68%)`
- Justification de la qualité :
  - La conception est cohérente mais difficile : les groupes peuvent être mention-gated, toujours actifs, ambiant uniquement, message-tool uniquement, diffusion, thread-bound ou fournisseur-topic scoped.
  - Les docs sont détaillées et honnêtes sur les différences de fournisseur, mais la surface reste facile à mal configurer.
  - Les preuves d'archive récentes autour de la liaison des threads Discord et des sessions parentes indiquent que ce domaine se stabilise toujours.
- Principaux risques de qualité :
  - Les opérateurs peuvent confondre l'appairage DM avec l'autorisation de groupe, ou les réponses visibles automatiques avec la livraison visible message-tool uniquement.
  - Les grammaires de threads spécifiques aux fournisseurs et les fallbacks parents rendent les modèles mentaux multi-canal fragiles.
  - Le support du salon ambiant n'est pas universel, ce qui réduit la prévisibilité pour les cas d'utilisation « écouter silencieusement ».
- Le score de qualité exclut la quantité de tests ; les tests sont enregistrés uniquement comme preuve de couverture.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/channel-framework.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'isolation de session groupe/canal, mention requise, threads natifs, groupes de diffusion, protection contre les boucles de bot.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une matrice de mode de salon multi-canal pour le groupe, le canal, MPIM, le thread, le sujet et le support ambiant.
- Ajouter une trace de route/activation pour les abandons de groupe, l'observation ambiante et la suppression de réponse visible.
- Ajouter la conformité en direct pour les groupes de diffusion et les événements de salon ambiant sur tous les canaux qui revendiquent le support.

## Preuve

### Docs

- `docs/channels/groups.md:21` à `docs/channels/groups.md:29` décrivent les réponses visibles et les contrôles d'accès au groupe.
- `docs/channels/groups.md:46` à `docs/channels/groups.md:54` décrivent les réponses visibles automatiques par rapport à message-tool.
- `docs/channels/groups.md:112` à `docs/channels/groups.md:126` distinguent l'autorisation de déclenchement de la visibilité du contexte.
- `docs/channels/groups.md:149` à `docs/channels/groups.md:152` définissent le comportement de session groupe/canal/sujet/chat direct et les battements de cœur de groupe ignorés.
- `docs/channels/groups.md:321` à `docs/channels/groups.md:323` documentent les groupes mention requise et les mentions implicites.
- `docs/channels/groups.md:371` à `docs/channels/groups.md:373` documentent le stockage des événements de salon et le contexte d'historique de groupe uniforme.
- `docs/channels/group-messages.md:11` à `docs/channels/group-messages.md:27` documente l'activation spécifique à WhatsApp, les sessions par groupe, le contexte en attente et le comportement d'invite de groupe.
- `docs/channels/ambient-room-events.md:11` à `docs/channels/ambient-room-events.md:15` définissent les événements de salon ambiant et les canaux pris en charge.
- `docs/channels/ambient-room-events.md:177` à `docs/channels/ambient-room-events.md:191` décrivent les modes de réponse visible, les limites d'historique et la rétention d'historique des événements de salon Discord.
- `docs/channels/broadcast-groups.md:21` et `docs/channels/broadcast-groups.md:179` définissent l'évaluation de diffusion après les listes blanches/activation et la sémantique sans contournement.
- `docs/channels/discord.md:736` à `docs/channels/discord.md:868` et `docs/channels/matrix.md:504` à `docs/channels/matrix.md:532` documentent le comportement des threads natifs.

### Source

- `src/channels/thread-bindings-policy.ts:50` à `src/channels/thread-bindings-policy.ts:257` implémente le placement des threads, l'état inactif, la politique de génération et les erreurs.
- `src/channels/conversation-resolution.ts:265` à `src/channels/conversation-resolution.ts:294` gère le contexte de threading et le placement de liaison par défaut.
- `src/channels/route-projection.ts:84` à `src/channels/route-projection.ts:153` projette les itinéraires à partir des conversations et compare les cibles de livraison.
- `src/channels/turn/kernel.ts:188` à `src/channels/turn/kernel.ts:225` gère l'historique supprimé avec les médias ; `src/channels/turn/kernel.ts:768` efface l'historique du groupe en attente après les tours préparés réussis.
- `src/channels/turn/kernel.ts:669` et `src/channels/turn/kernel.ts:964` abandonnent les tours préparés/directs protégés contre les boucles de bot avant l'enregistrement et la distribution.
- `src/channels/session.ts:32` à `src/channels/session.ts:80` enregistre les métadonnées de session entrante utilisées par la persistance de l'itinéraire groupe/thread.

### Tests d'intégration

- `src/gateway/gateway-acp-bind.live.test.ts:565` couvre un chemin de liaison et de reroutage de conversation en direct de forme Slack, adjacent au routage thread/session.
- `scripts/e2e/mcp-channels-docker-client.ts:254` et `scripts/e2e/mcp-channels-docker-client.ts:311` exercent les chemins de conversation et de pièce jointe du canal via le harnais de canal MCP.
- Aucune matrice ambiante/groupe/thread en direct multi-canal n'a été trouvée.

### Tests unitaires

- `src/channels/thread-bindings-policy.test.ts:11` à `src/channels/thread-bindings-policy.test.ts:110` couvre le placement des enfants, thread-here, les générations thread-bound par défaut, `spawnSessions` et les remplacements de compte.
- `src/channels/conversation-resolution.test.ts:140` à `src/channels/conversation-resolution.test.ts:437` couvre le fallback parent/thread, la normalisation des sujets, les ID de thread entrants, la casse de la salle Matrix, le rejet et les métadonnées de placement.
- `src/channels/route-projection.test.ts:80` à `src/channels/route-projection.test.ts:164` couvre les projections parent-enfant, les enregistrements de liaison de session, la priorité du dernier itinéraire et la comparaison des cibles de livraison.
- `src/channels/turn/kernel.test.ts:669` à `src/channels/turn/kernel.test.ts:1023` couvre les abandons de boucle de bot, l'admission observe uniquement, le nettoyage de l'historique du groupe, les abandons de vol, les abandons répétés de paires de bot et le flux de style événement de salon observe uniquement.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "channel groups threads ambient room events mention gating" --json --limit 8`

Résultats :

- N'a retourné aucun résultat, ce qui est neutre après les vérifications de fraîcheur pour cette requête exacte multi-canal.

Requête : `gitcrawl search openclaw/openclaw --query "Discord thread binding channel parent session" --json --limit 8`

Résultats :

- A retourné le problème #64199, PR #64322, problème #53548, PR #81341, problème #87599, PR #82023, PR #81402 et PR #74163, montrant un cluster d'archive substantiel autour de la liaison des threads Discord et du comportement de session parente.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channel groups threads ambient room events mention gating" --limit 8`

Résultats :

- A retourné null, ce qui est neutre après les vérifications de fraîcheur.

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "Discord thread binding channel parent session" --limit 8`

Résultats :

- A trouvé une discussion d'implémentation pour l'héritage de liaison parente et la génération de sous-agent thread-bound.
- A trouvé une erreur utilisateur en direct autour de l'échec de l'adaptateur de liaison de session et une discussion d'examen autour du comportement de liaison des threads Discord.
