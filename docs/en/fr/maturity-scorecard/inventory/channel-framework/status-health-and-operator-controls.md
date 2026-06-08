---
title: "Cadre de canal - Note de maturité des contrôles de santé d'état et d'opérateur"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Cadre de canal - Note de maturité des contrôles de santé d'état et d'opérateur

## Résumé

L'état, la santé et les contrôles d'opérateur sont solides. La passerelle expose les instantanés d'état, les sondes, les lignes de compte, les avertissements, les redémarrages du moniteur de santé, la détection de socket obsolète, les limites de redémarrage, les RPC de démarrage/arrêt/déconnexion et la documentation CLI/opérateur. L'implémentation inclut les budgets de temps, les instantanés partiels, la santé de la boucle d'événements et les remplacements du moniteur de santé par canal.

La limite de maturité est l'explicabilité plutôt que la capacité de base. Les preuves d'archive montrent que les opérateurs peuvent toujours être confus par un état de canal d'apparence saine lorsque la politique de groupe, le comportement d'auto-groupe, les écouteurs obsolètes ou les restrictions d'intention de contenu bloquent les réponses.

## Portée de la catégorie

Inclus dans cette catégorie :

- channels.status : channels.status, sondes, instantanés de compte et avertissements
- Politique de santé des canaux : Politique de santé des canaux, redémarrages du moniteur de santé, détection de socket obsolète, refroidissements et limites de redémarrage
- Contrôles CLI d'opérateur : Contrôles CLI d'opérateur pour démarrage, arrêt, déconnexion, état, redémarrage et dépannage
- Modèle de lecture d'état : Modèle de lecture d'état et instantanés d'état du plugin

## Fonctionnalités

- channels.status : channels.status, sondes, instantanés de compte et avertissements
- Politique de santé des canaux : Politique de santé des canaux, redémarrages du moniteur de santé, détection de socket obsolète, refroidissements et limites de redémarrage
- Contrôles CLI d'opérateur : Contrôles CLI d'opérateur pour démarrage, arrêt, déconnexion, état, redémarrage et dépannage
- Modèle de lecture d'état : Modèle de lecture d'état et instantanés d'état du plugin

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - La documentation documente l'état local/passerelle, les sondes de santé profonde, le dépannage des sondes d'état par canal, la configuration du moniteur de santé, les seuils d'événements obsolètes, les limites de redémarrage et les exclusions par canal (`docs/gateway/health.md:13`, `docs/gateway/health.md:38`, `docs/gateway/configuration-reference.md:556`, `docs/channels/troubleshooting.md:16`, `docs/channels/troubleshooting.md:58`).
  - La source a une politique de santé dédiée, un moniteur de santé, un gestionnaire channels.status, un modèle de lecture d'état et des aides d'instantané d'état du plugin.
  - La couverture unitaire est large pour la politique de santé, les cas limites du moniteur de santé, la détection de socket obsolète, les délais d'expiration des sondes d'état, les instantanés partiels, les annotations malsaines, les contrôles de démarrage/arrêt/déconnexion et le comportement de redémarrage du gestionnaire de canaux.
  - La documentation d'opérateur inclut les signatures de dépannage par canal.
- Signaux négatifs :
  - L'état peut signaler la santé du transport/configuration tandis que la politique au niveau du message bloque toujours les réponses, ce que les utilisateurs perçoivent comme une inadéquation d'état.
  - Les champs d'état sont répartis entre CLI, RPC Gateway, docs, instantanés de plugin et tableaux de dépannage.
  - Certaines preuves d'archive pointent vers des instantanés d'état sains qui nécessitaient toujours une explication de politique/routage.
- Lacunes d'intégration :
  - Aucune matrice de sonde de santé en direct pour tous les canaux n'a été trouvée.
  - Aucun E2E n'a été trouvé qui crée intentionnellement chaque état malsain/obsolète/occupé/arrêt manuel/reconnexion et valide la sortie côté opérateur.

## Score de qualité

- Score : `Beta (78%)`
- Justification de la qualité :
  - Le moniteur de santé est soigneusement délimité : grâce au démarrage, comportement occupé/obsolète, refroidissement, limites horaires, arrêts manuels ignorés, sauts désactivés/non configurés et vérifications de vol unique sont modélisés.
  - Les gestionnaires d'état se dégradent gracieusement avec des instantanés partiels et des avertissements lorsque les sondes lèvent ou dépassent les budgets.
  - La documentation expose des commandes d'opérateur utiles et des boutons de configuration.
- Principaux risques de qualité :
  - L'état ne fait pas toujours le lien entre la santé du transport et « pourquoi mon message n'a-t-il pas reçu de réponse ».
  - Plusieurs surfaces d'état utilisent des termes chevauchants, de sorte que les opérateurs peuvent mal lire configuré/en cours d'exécution/connecté/fonctionne/audit ok.
  - Les sondes et permissions spécifiques au fournisseur rendent la sémantique de santé uniforme difficile.
- La notation de qualité exclut la quantité de tests ; les tests sont enregistrés uniquement comme preuve de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/channel-framework.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour channels.status, Politique de santé des canaux, Contrôles CLI d'opérateur, Modèle de lecture d'état.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une couche d'explication d'état qui distingue la santé du transport, la santé de l'authentification, l'admission de politique, le routage et la livraison.
- Ajouter une matrice d'état E2E pour les raisons de redémarrage du moniteur de santé et la sortie channels.status.
- Consolider les termes d'état d'opérateur dans un tableau de docs lié aux champs JSON RPC Gateway.

## Preuves

### Docs

- `docs/gateway/health.md:13` à `docs/gateway/health.md:19` listent `openclaw status`, `openclaw status --all`, `openclaw status --deep`, `openclaw health` et le canal `/status`.
- `docs/gateway/health.md:38` à `docs/gateway/health.md:42` documentent l'intervalle du moniteur de santé des canaux, le seuil d'événement obsolète, les limites de redémarrage et les exclusions par canal/compte.
- `docs/gateway/health.md:47` et `docs/gateway/health.md:67` documentent les conseils de reliaison et le contenu des instantanés de santé.
- `docs/gateway/configuration-reference.md:556` à `docs/gateway/configuration-reference.md:560` documentent les clés de configuration du moniteur de santé.
- `docs/channels/troubleshooting.md:16` à `docs/channels/troubleshooting.md:28` documentent les vérifications de base saines.
- `docs/channels/troubleshooting.md:58` à `docs/channels/troubleshooting.md:60` documentent les boucles de reconnexion, les boucles de délai d'expiration, les réponses tardives et les actions de docteur/redémarrage.
- `docs/channels/discord.md:1535` à `docs/channels/discord.md:1546` utilisent `channels status --probe` pour déboguer la politique de groupe, les listes blanches et la mention de portage.

### Source

- `src/gateway/channel-health-policy.ts:48` à `src/gateway/channel-health-policy.ts:143` modélise les seuils de santé, l'évaluation et les raisons de redémarrage.
- `src/gateway/channel-health-monitor.ts:76` à `src/gateway/channel-health-monitor.ts:184` implémente la grâce de démarrage, les états ignorés, l'évaluation de la santé, les refroidissements, les limites de redémarrage et le travail de redémarrage arrêt/démarrage.
- `src/gateway/server-methods/channels.ts:57` à `src/gateway/server-methods/channels.ts:127` définissent le délai d'expiration et la concurrence d'état et accrochent la gestion des délais d'expiration/erreurs.
- `src/gateway/server-methods/channels.ts:285` à `src/gateway/server-methods/channels.ts:541` implémentent channels.status, la construction de sonde/audit/instantané, les avertissements, la santé de la boucle d'événements et les résultats partiels.
- `src/channels/status/read-model.ts:26` à `src/channels/status/read-model.ts:135` construit les comptes d'exécution, les instantanés normalisés, la recherche de compte, la disponibilité des identifiants et les lignes de compte.
- `src/channels/plugins/status.ts:8` à `src/channels/plugins/status.ts:92` construit les instantanés d'état du compte de canal à partir de la configuration/inspection.
- `src/gateway/protocol/schema/channels.ts:633` à `src/gateway/protocol/schema/channels.ts:753` définit les paramètres/résultats channels.status et les schémas de démarrage/arrêt.

### Tests d'intégration

- `scripts/e2e/npm-onboard-channel-agent-docker.sh:164` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:171` vérifient les surfaces `channels status` et `status` après l'ajout de canal.
- `scripts/e2e/lib/release-user-journey/assertions.mjs` est utilisé par le parcours utilisateur de version pour affirmer l'état du canal après redémarrage.
- Aucune matrice d'état du moniteur de santé/sonde en direct pour tous les canaux n'a été trouvée.

### Tests unitaires

- `src/gateway/channel-health-policy.test.ts:17` à `src/gateway/channel-health-policy.test.ts:311` couvre les comptes désactivés, la grâce de connexion, le comportement occupé/obsolète, la détection de socket obsolète, les horodatages de transport, les cas webhook/sondage, les horodatages hérités et le mappage des raisons de redémarrage.
- `src/gateway/channel-health-monitor.test.ts:152` à `src/gateway/channel-health-monitor.test.ts:616` couvre la grâce de démarrage, les défaillances d'instantané, les sauts sains/désactivés/non configurés/arrêt manuel, les redémarrages bloqués/déconnectés/reconnexion, le comportement occupé/obsolète, les refroidissements, les limites horaires, les vérifications de vol unique, l'abandon/arrêt et la détection de socket obsolète.
- `src/gateway/server-methods/channels.status.test.ts:97` à `src/gateway/server-methods/channels.status.test.ts:369` couvre les instantanés de configuration, les limites de délai d'expiration de sonde, le filtrage, les sondes lèvent, les délais d'expiration du budget d'état, les résumés de secours, les annotations malsaines et la santé de la boucle d'événements.
- `src/gateway/server-methods/channels.start.test.ts:67` à `src/gateway/server-methods/channels.start.test.ts:253` couvre les gestionnaires de démarrage, arrêt et déconnexion d'opérateur.
- `src/gateway/server-channels.test.ts:935` à `src/gateway/server-channels.test.ts:1050` couvre la résolution du remplacement du moniteur de santé et le comportement de fermeture défaillante lors de la résolution du compte.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "channel status health readiness disconnected stale socket" --json --limit 8`

Résultats :

- N'a retourné aucun résultat, ce qui est neutre après les vérifications de fraîcheur pour cette phrase exacte.

Requête : `gitcrawl search openclaw/openclaw --query "channels status configured connected running channelAccounts" --json --limit 8`

Résultats :

- N'a retourné aucun résultat, ce qui est neutre après les vérifications de fraîcheur.

Requête : `gitcrawl search openclaw/openclaw --query "channel readiness stale socket disconnected gateway" --json --limit 8`

Résultats :

- N'a retourné aucun résultat, ce qui est neutre après les vérifications de fraîcheur.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channels status configured connected running channelAccounts" --limit 8`

Résultats :

- Ont trouvé des discussions de support WhatsApp et Discord où l'état semblait sain ou partiellement sain mais les réponses étaient bloquées par le comportement de groupe/auto, l'état d'écouteur actif manquant, les limitations d'intention de contenu, les ID de canal non résolus ou les erreurs du pipeline de statut/sonde.
- Cela soutient l'évaluation selon laquelle la capacité d'état est forte mais l'explicabilité entre le transport, la politique et la livraison nécessite plus de travail.

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channel status health readiness disconnected stale socket" --limit 8`

Résultats :

- A retourné null, ce qui est neutre après les vérifications de fraîcheur.

Requête : `/Users/kevinlin/.local/bin/discrawl --json search "channel readiness stale socket disconnected gateway" --limit 8`

Résultats :

- A retourné null, ce qui est neutre après les vérifications de fraîcheur.
