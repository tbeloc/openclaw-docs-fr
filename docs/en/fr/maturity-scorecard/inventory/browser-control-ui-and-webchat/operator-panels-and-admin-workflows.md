---
title: "Gateway Web App - Operator Panels and Admin Workflows Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - Operator Panels and Admin Workflows Maturity Note

## Résumé

L'interface utilisateur de contrôle est bien plus qu'un chat : elle expose les canaux, instances, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et workflows de configuration/connexion via les RPC Gateway. La couverture est Stable car les RPC sous-jacents et de nombreux contrôleurs/vues UI ont des tests, mais la matrice de workflow d'opérateur de bout en bout est large. La qualité est Beta car les panneaux sont utiles et délimités en portée, tandis que les preuves d'archive montrent que les utilisateurs ont toujours du mal avec l'exécution élevée, le statut des canaux/configuration, l'interface utilisateur des compétences et la portée multi-agent/session.

## Portée de la catégorie

Cette catégorie couvre les panneaux d'opérateur non-config dans l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les expose.

## Fonctionnalités

- Canaux/connexion : Couvre les canaux/connexion dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les expose.
- Gestionnaire de session et historique : Couvre le gestionnaire de session de l'interface utilisateur de contrôle du navigateur, l'historique des sessions, la présence des instances, les approbations, les diagnostics et les onglets de journal.
- Cron : Couvre Cron dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les expose.
- Compétences/nœuds : Couvre les compétences/nœuds dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les expose.
- Approbations d'exécution/agents : Couvre les approbations d'exécution/agents dans les panneaux d'opérateur non-config de l'interface utilisateur de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves et la navigation du tableau de bord qui les expose.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : Les descripteurs de méthode Gateway délimitent les RPC pertinents ; les contrôleurs UI et les tests de vue couvrent les canaux, sessions, cron, compétences, nœuds, approbations d'exécution, agents, utilisation et panneaux adjacents aux activités.
- Signaux négatifs : Les workflows complets s'étendent sur les API de canal en amont, les hôtes de nœuds, les registres de compétences/plugins, l'exécution cron, la politique d'exécution et l'état de session multi-agent. De nombreux panneaux sont couverts indépendamment plutôt que par le biais de parcours d'opérateur complets du navigateur.
- Lacunes d'intégration : Ajouter des scénarios de version pour la connexion/statut QR du canal, la correction de session, la création/exécution/édition cron, la mise à jour de l'installation de compétence/clé API, l'édition d'approbation d'exécution de nœud, la portée d'utilisation multi-agent et la création d'agent.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : La requête de panneau d'opérateur spécifique a retourné `[]`, mais les larges PR de l'interface utilisateur de contrôle ont retourné #80388 pour les points d'entrée de l'interface utilisateur de contrôle des plugins, #80192 pour l'activité Codex dans l'interface utilisateur de contrôle, #87147 pour la portée de l'agent de la page d'utilisation, #81954 pour le flux New Agent de l'onglet Agents et #74715 pour la visibilité de l'onglet Notifications.
- Rapports Discrawl : La recherche du panneau d'opérateur a trouvé une transcription complète de l'interface utilisateur de contrôle où un utilisateur a activé l'exécution élevée pour WebChat, a frappé une mauvaise forme de config, a redémarré et n'a toujours pas pu exécuter la commande demandée en session. D'autres exemples de support montrent des utilisateurs s'appuyant sur l'interface utilisateur de contrôle pour le statut, les journaux, les canaux et le triage de configuration.
- Bonnes qualités : Les RPC d'administration sont délimités en portée, les panneaux utilisent généralement l'état dérivé de Gateway, les sondes de canal lentes préservent les snapshots et l'édition d'approbation d'exécution utilise des gardes de hash de base.
- Mauvaises qualités : La surface opérationnelle est suffisamment large pour que les utilisateurs puissent mal interpréter la politique, la portée, l'exécution ou l'état de rechargement de config, en particulier autour de l'exécution élevée et des workflows de canal/nœud.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel affectent uniquement la couverture.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Canaux/connexion, Gestionnaire de session et historique, Cron, Compétences/nœuds, Approbations d'exécution/agents.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'état au niveau du panneau est large mais manque toujours d'un petit ensemble de scorecards de scénario d'opérateur stables et publics.
- La politique d'exécution élevée et les permissions d'origine WebChat ont besoin d'une transmission UX plus claire après les changements de config.
- Les surfaces d'extension de l'interface utilisateur de contrôle des plugins/compétences évoluent toujours.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente les panneaux Canaux, Instances, Sessions, Rêves, Cron, Compétences, Nœuds, Approbations d'exécution, Débogage, Journaux et Mise à jour.
- `/Users/kevinlin/code/openclaw/docs/gateway/protocol.md` énumère les portées et RPC pour les canaux, nœuds, cron, sessions, compétences, modèles, approbations d'exécution et appareils.
- `/Users/kevinlin/code/openclaw/docs/web/dashboard.md` documente l'interface utilisateur de contrôle comme une surface d'administration.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/methods/core-descriptors.ts` délimite les méthodes Gateway principales utilisées par les panneaux de l'interface utilisateur de contrôle.
- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/channels.ts` charge le statut du canal et démarre/attend la connexion web.
- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/sessions.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/cron.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/skills.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/nodes.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/agents.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/exec-approvals.ts` implémentent les contrôleurs de panneau.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/channels.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/sessions.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/cron.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/skills.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/nodes.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/agents.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/views/exec-approval.ts` rendent les panneaux.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-channels.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-cron.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-methods/sessions.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/skills-upload.test.ts` couvrent les capacités du panneau côté Gateway.
- `/Users/kevinlin/code/openclaw/src/gateway/operator-approvals-client.e2e.test.ts` couvre le comportement du client d'approbation d'opérateur.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/channels.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/cron.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/sessions.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/exec-approval.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/channels.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/cron.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/skills.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/nodes.devices.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/views/agents.test.ts` couvrent la logique et le rendu des panneaux.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Control UI channels sessions cron skills nodes exec approvals"`

Résultats :

- A retourné `[]`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "Control UI"`

Résultats :

- A retourné les PR adjacentes au panneau d'opérateur #80388, #80192, #87147, #81954, #74715 et #79747.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI channels sessions cron skills nodes exec approvals"`

Résultats :

- A trouvé une transcription de l'interface utilisateur de contrôle où un utilisateur a essayé d'activer l'exécution élevée depuis WebChat, a corrigé la config, a redémarré et n'a toujours pas pu exécuter la commande dans la session actuelle.
- A trouvé des exemples de support utilisant les panneaux de statut/journaux/canaux de l'interface utilisateur de contrôle pour le triage de configuration.
