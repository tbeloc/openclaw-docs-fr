---
title: "Automation: cron, hooks, tasks, polling Rapport de maturité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling Rapport de maturité

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (76%)`
- Qualité : `Alpha (69%)`
- Complétude : `Beta (76%)`
- Fonctionnalités LTS : `0/6`

## Résumé

Ce rapport promeut les preuves de maturité archivées `automation-cron-hooks-tasks-polling` de `/Users/kevinlin/tmp/maturity/automation-cron-hooks-tasks-polling` dans le contrat d'inventaire actuel process-version-3.

Les scores de Couverture et Qualité proviennent des lignes de score soutenues par les preuves archivées. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Cron Jobs](cron-job-lifecycle.md)                      | ❌  | `Stable (82%)` | `Beta (73%)`  | `Stable (82%)` | Create/edit/remove jobs, Schedule types, Timezone and stagger, Cron RPCs, Agent cron tool, Manual cron runs, Isolated cron execution, Model/provider preflight, Run history, Timeout and denial diagnostics, Chat announce delivery, Webhook delivery, Failure destinations, Skipped-run alerts, Delivery previews              |
| [Event Ingress](channel-polling-webhooks.md)            | ❌  | `Alpha (65%)`  | `Alpha (58%)` | `Alpha (65%)`  | Telegram long polling, Telegram webhook mode, Zalo polling/webhook mode, Polling stall diagnostics, iMessage watch fallback, Gmail setup wizard, Watcher start/serve, Tailscale/public routing, Push token validation, Gmail event routing, POST /hooks/wake, POST /hooks/agent, Mapped hooks, Hook auth policy, Async dispatch |
| [Automation Hooks](internal-hooks.md)                   | ❌  | `Beta (78%)`   | `Beta (72%)`  | `Beta (78%)`   | HOOK.md authoring, Hook discovery, Hook CLI management, Hook packs, Lifecycle event dispatch, api.on registration, Tool-call policy hooks, Message hooks, Session/lifecycle hooks, Plugin approval requests, cron_changed                                                                                                       |
| [Background Tasks and Flows](background-task-ledger.md) | ❌  | `Beta (73%)`   | `Alpha (68%)` | `Beta (73%)`   | Task list/show/cancel, Task notifications, Task audit and maintenance, Chat task board, Task pressure status, Managed flows, Mirrored flows, openclaw tasks flow, Flow audit and maintenance, Plugin managedFlows                                                                                                               |
| [Heartbeat](heartbeat-commitments.md)                   | ❌  | `Stable (82%)` | `Beta (72%)`  | `Stable (82%)` | Heartbeat scheduling, Active hours, Wake and cooldown handling, Due-only heartbeat tasks, Commitment check-ins                                                                                                                                                                                                                  |
| [Polling Controls](message-polls-process-polling.md)    | ❌  | `Beta (74%)`   | `Beta (70%)`  | `Beta (74%)`   | openclaw message poll, Telegram polls, Teams polls, Poll flags, Channel capability gates, process poll, process log, Background process status, No-progress loop detection, Process input controls                                                                                                                              |

## Rubrique de notation

- Couverture :
  évaluation maturity-label pour l'intégration, e2e, live, ou les preuves de
  flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation maturity-label pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et de flux runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  évaluation maturity-label pour la mesure dans laquelle la catégorie fournit l'ensemble de
  capacités spécifiques à la surface prévues. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  libellé de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Tâches planifiées (Cron Jobs)

Ancres de recherche : Créer/modifier/supprimer des tâches, Types de planification, Fuseau horaire et décalage, RPC Cron, Outil cron Agent, openclaw cron, Exécutions cron manuelles, Exécution cron isolée, Précontrôle modèle/fournisseur, Historique des exécutions, Diagnostics de délai d'attente et de refus, Livraison d'annonce de chat, Livraison webhook, Destinations d'échec, Alertes d'exécution ignorée, Aperçus de livraison, destination d'échec, annonce.

Note de catégorie : [Tâches planifiées](cron-job-lifecycle.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (73%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Créer/modifier/supprimer des tâches : Couvre Créer/modifier/supprimer des tâches dans la création de tâches planifiées, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches planifiées associé.
- Types de planification : Couvre Types de planification dans la création de tâches planifiées, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches planifiées associé.
- Fuseau horaire et décalage : Couvre Fuseau horaire et décalage dans la création de tâches planifiées, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches planifiées associé.
- RPC Cron : Couvre RPC Cron dans la création de tâches planifiées, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches planifiées associé.
- Outil cron Agent : Couvre Outil cron Agent dans la création de tâches planifiées, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches planifiées associé.
- Exécutions cron manuelles : Couvre Exécutions cron manuelles dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Exécution cron isolée : Couvre Exécution cron isolée dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Précontrôle modèle/fournisseur : Couvre Précontrôle modèle/fournisseur dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Historique des exécutions : Couvre Historique des exécutions dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Diagnostics de délai d'attente et de refus : Couvre Diagnostics de délai d'attente et de refus dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Livraison d'annonce de chat : Couvre Livraison d'annonce de chat dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et alertes d'échec associé.
- Livraison webhook : Couvre Livraison webhook dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et alertes d'échec associé.
- Destinations d'échec : Couvre Destinations d'échec dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et alertes d'échec associé.
- Alertes d'exécution ignorée : Couvre Alertes d'exécution ignorée dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et alertes d'échec associé.
- Aperçus de livraison : Couvre Aperçus de livraison dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et alertes d'échec associé.

Documentation principale :

- `docs/automation/cron-jobs.md`
- `docs/cli/cron.md`
- `docs/gateway/protocol.md`
- `docs/automation/tasks.md`
- `docs/channels/discord.md`

### 2. Ingestion d'événements

Ancres de recherche : Interrogation longue Telegram, Mode webhook Telegram, Mode interrogation/webhook Zalo, Diagnostics de blocage d'interrogation, Secours de surveillance iMessage, Assistant de configuration Gmail, Démarrage/service du moniteur, Routage Tailscale/public, Validation du jeton de notification, Routage d'événement Gmail, POST /hooks/wake, POST /hooks/agent, Hooks mappés, Politique d'authentification des hooks, Distribution asynchrone.

Note de catégorie : [Ingestion d'événements](channel-polling-webhooks.md)

Décisions de score :

- Couverture : `Alpha (65%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (65%)`
- LTS : ❌

Fonctionnalités :

- Interrogation longue Telegram : Couvre Interrogation longue Telegram dans les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de surveillance et comportement d'interrogation de canal et webhooks associé.
- Mode webhook Telegram : Couvre Mode webhook Telegram dans les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de surveillance et comportement d'interrogation de canal et webhooks associé.
- Mode interrogation/webhook Zalo : Couvre Mode interrogation/webhook Zalo dans les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de surveillance et comportement d'interrogation de canal et webhooks associé.
- Diagnostics de blocage d'interrogation : Couvre Diagnostics de blocage d'interrogation dans les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de surveillance et comportement d'interrogation de canal et webhooks associé.
- Secours de surveillance iMessage : Couvre Secours de surveillance iMessage dans les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de surveillance et comportement d'interrogation de canal et webhooks associé.
- Assistant de configuration Gmail : Couvre Assistant de configuration Gmail dans `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur et comportement des moniteurs pub/sub Gmail associé.
- Démarrage/service du moniteur : Couvre Démarrage/service du moniteur dans `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur et comportement des moniteurs pub/sub Gmail associé.
- Routage Tailscale/public : Couvre Routage Tailscale/public dans `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur et comportement des moniteurs pub/sub Gmail associé.
- Validation du jeton de notification : Couvre Validation du jeton de notification dans `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur et comportement des moniteurs pub/sub Gmail associé.
- Routage d'événement Gmail : Couvre Routage d'événement Gmail dans `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur et comportement des moniteurs pub/sub Gmail associé.
- POST /hooks/wake : Couvre POST /hooks/wake dans `/hooks/wake`, `/hooks/agent`, hooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- POST /hooks/agent : Couvre POST /hooks/agent dans `/hooks/wake`, `/hooks/agent`, hooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Hooks mappés : Couvre Hooks mappés dans `/hooks/wake`, `/hooks/agent`, hooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Politique d'authentification des hooks : Couvre Politique d'authentification des hooks dans `/hooks/wake`, `/hooks/agent`, hooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Distribution asynchrone : Couvre Distribution asynchrone dans `/hooks/wake`, `/hooks/agent`, hooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.

Documentation principale :

- `docs/channels/telegram.md`
- `docs/channels/zalo.md`
- `docs/channels/troubleshooting.md`
- `docs/channels/imessage-from-bluebubbles.md`
- `docs/automation/cron-jobs.md#gmail-pubsub-integration`
- `docs/automation/gmail-pubsub.md`
- `docs/cli/webhooks.md`
- `docs/automation/cron-jobs.md#webhooks`
- `docs/automation/webhook.md`

### 3. Hooks d'automatisation

Ancres de recherche : Création HOOK.md, Découverte de hooks, Gestion CLI des hooks, Packs de hooks, Distribution d'événements de cycle de vie, Enregistrement api.on, Hooks de politique d'appel d'outil, Hooks de message, Hooks de session/cycle de vie, Demandes d'approbation de plugin, cron_changed.

Note de catégorie : [Hooks d'automatisation](internal-hooks.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Création HOOK.md : Couvre Création HOOK.md dans les métadonnées `HOOK.md`, chargement du gestionnaire, découverte de hooks groupés/gérés/espace de travail/plugin, politique d'éligibilité et comportement des hooks internes associé.
- Découverte de hooks : Couvre Découverte de hooks dans les métadonnées `HOOK.md`, chargement du gestionnaire, découverte de hooks groupés/gérés/espace de travail/plugin, politique d'éligibilité et comportement des hooks internes associé.
- Gestion CLI des hooks : Couvre Gestion CLI des hooks dans les métadonnées `HOOK.md`, chargement du gestionnaire, découverte de hooks groupés/gérés/espace de travail/plugin, politique d'éligibilité et comportement des hooks internes associé.
- Packs de hooks : Couvre Packs de hooks dans les métadonnées `HOOK.md`, chargement du gestionnaire, découverte de hooks groupés/gérés/espace de travail/plugin, politique d'éligibilité et comportement des hooks internes associé.
- Distribution d'événements de cycle de vie : Couvre Distribution d'événements de cycle de vie dans les métadonnées `HOOK.md`, chargement du gestionnaire, découverte de hooks groupés/gérés/espace de travail/plugin, politique d'éligibilité et comportement des hooks internes associé.
- Enregistrement api.on : Couvre Enregistrement api.on dans les hooks typés `api.on(...)`, comportement de priorité/délai d'attente, hooks de décision tels que `before_tool_call`, hooks de message et distribution et comportement des hooks de plugin associé.
- Hooks de politique d'appel d'outil : Couvre Hooks de politique d'appel d'outil dans les hooks typés `api.on(...)`, comportement de priorité/délai d'attente, hooks de décision tels que `before_tool_call`, hooks de message et distribution et comportement des hooks de plugin associé.
- Hooks de message : Couvre Hooks de message dans les hooks typés `api.on(...)`, comportement de priorité/délai d'attente, hooks de décision tels que `before_tool_call`, hooks de message et distribution et comportement des hooks de plugin associé.
- Hooks de session/cycle de vie : Couvre Hooks de session/cycle de vie dans les hooks typés `api.on(...)`, comportement de priorité/délai d'attente, hooks de décision tels que `before_tool_call`, hooks de message et distribution et comportement des hooks de plugin associé.
- Demandes d'approbation de plugin : Couvre Demandes d'approbation de plugin dans les hooks typés `api.on(...)`, comportement de priorité/délai d'attente, hooks de décision tels que `before_tool_call`, hooks de message et distribution et comportement des hooks de plugin associé.
- cron_changed : Couvre cron_changed dans les hooks typés `api.on(...)`, comportement de priorité/délai d'attente, hooks de décision tels que `before_tool_call`, hooks de message et distribution et comportement des hooks de plugin associé.

Documentation principale :

- `docs/automation/hooks.md`
- `docs/cli/hooks.md`
- `docs/plugins/hooks.md`
- `docs/plugins/plugin-permission-requests.md`
- `docs/plugins/sdk-subpaths.md`

### 4. Tâches de fond et flux

Ancres de recherche : Liste/affichage/annulation de tâches, Notifications de tâches, Audit et maintenance des tâches, Tableau de tâches de chat, État de pression des tâches, Flux gérés, Flux en miroir, openclaw tasks flow, Audit et maintenance des flux, Plugin managedFlows.

Note de catégorie : [Tâches de fond et flux](background-task-ledger.md)

Décisions de score :

- Couverture : `Beta (73%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (73%)`
- LTS : ❌

Fonctionnalités :

- Liste/affichage/annulation de tâches : Couvre Liste/affichage/annulation de tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre de tâches de fond associé.
- Notifications de tâches : Couvre Notifications de tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre de tâches de fond associé.
- Audit et maintenance des tâches : Couvre Audit et maintenance des tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre de tâches de fond associé.
- Tableau de tâches de chat : Couvre Tableau de tâches de chat dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre de tâches de fond associé.
- État de pression des tâches : Couvre État de pression des tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre de tâches de fond associé.
- Flux gérés : Couvre Flux gérés dans les modes de flux gérés et en miroir, persistance du registre de flux, suivi des révisions, accès limité au propriétaire et comportement du flux de tâches associé.
- Flux en miroir : Couvre Flux en miroir dans les modes de flux gérés et en miroir, persistance du registre de flux, suivi des révisions, accès limité au propriétaire et comportement du flux de tâches associé.
- openclaw tasks flow : Couvre openclaw tasks flow dans les modes de flux gérés et en miroir, persistance du registre de flux, suivi des révisions, accès limité au propriétaire et comportement du flux de tâches associé.
- Audit et maintenance des flux : Couvre Audit et maintenance des flux dans les modes de flux gérés et en miroir, persistance du registre de flux, suivi des révisions, accès limité au propriétaire et comportement du flux de tâches associé.
- Plugin managedFlows : Couvre Plugin managedFlows dans les modes de flux gérés et en miroir, persistance du registre de flux, suivi des révisions, accès limité au propriétaire et comportement du flux de tâches associé.

Documentation principale :

- `docs/automation/tasks.md`
- `docs/automation/index.md`
- `docs/cli/tasks.md`
- `docs/automation/taskflow.md`
- `docs/plugins/sdk-runtime.md`

### 5. Battement de cœur

Ancres de recherche : Planification du battement de cœur, Heures actives, Gestion du réveil et refroidissement, Tâches de battement de cœur dues uniquement, Enregistrements d'engagement, openclaw cron.

Note de catégorie : [Battement de cœur](heartbeat-commitments.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Planification du battement de cœur : Couvre Planification du battement de cœur dans les exécutions périodiques du battement de cœur, comportement de planification variable et heures actives, gestion du réveil/refroidissement, invites de battement de cœur et mode de tâche dues uniquement et comportement du battement de cœur et engagements associé.
- Heures actives : Couvre Heures actives dans les exécutions périodiques du battement de cœur, comportement de planification variable et heures actives, gestion du réveil/refroidissement, invites de battement de cœur et mode de tâche dues uniquement et comportement du battement de cœur et engagements associé.
- Gestion du réveil et refroidissement : Couvre Gestion du réveil et refroidissement dans les exécutions périodiques du battement de cœur, comportement de planification variable et heures actives, gestion du réveil/refroidissement, invites de battement de cœur et mode de tâche dues uniquement et comportement du battement de cœur et engagements associé.
- Tâches de battement de cœur dues uniquement : Couvre Tâches de battement de cœur dues uniquement dans les exécutions périodiques du battement de cœur, comportement de planification variable et heures actives, gestion du réveil/refroidissement, invites de battement de cœur et mode de tâche dues uniquement et comportement du battement de cœur et engagements associé.
- Enregistrements d'engagement : Couvre Enregistrements d'engagement dans les exécutions périodiques du battement de cœur, comportement de planification variable et heures actives, gestion du réveil/refroidissement, invites de battement de cœur et mode de tâche dues uniquement et comportement du battement de cœur et engagements associé.

Documentation principale :

- `docs/automation/index.md`
- `docs/gateway/heartbeat.md`
- `docs/concepts/commitments.md`

### 6. Contrôles d'interrogation

Ancres de recherche : openclaw message poll, Sondages Telegram, Sondages Teams, Drapeaux de sondage, Portes de capacité de canal, process poll, process log, État du processus de fond.

Note de catégorie : [Contrôles d'interrogation](message-polls-process-polling.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- openclaw message poll : Couvre openclaw message poll dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- Sondages Telegram : Couvre Sondages Telegram dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- Sondages Teams : Couvre Sondages Teams dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- Drapeaux de sondage : Couvre Drapeaux de sondage dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- Portes de capacité de canal : Couvre Portes de capacité de canal dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- process poll : Couvre process poll dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- process log : Couvre process log dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- État du processus de fond : Couvre État du processus de fond dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- Détection de boucle sans progrès : Couvre Détection de boucle sans progrès dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.
- Contrôles d'entrée de processus : Couvre Contrôles d'entrée de processus dans `openclaw message poll`, adaptateurs d'interrogation de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram et comportement des sondages de message et interrogation de processus associé.

Documentation principale :

- `docs/automation/poll.md`
- `docs/cli/message.md`
- `docs/channels/telegram.md`
- `docs/channels/msteams.md`
- `docs/gateway/background-process.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/automation-cron-hooks-tasks-polling/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/automation-cron-hooks-tasks-polling`.
