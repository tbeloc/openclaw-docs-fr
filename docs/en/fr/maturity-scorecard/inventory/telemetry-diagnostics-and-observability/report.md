---
title: "Rapport de Maturité de l'Observabilité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité de l'Observabilité

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Stable (80%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (80%)`
- Fonctionnalités LTS : `3/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `telemetry-diagnostics-and-observability` de `/Users/kevinlin/tmp/maturity/telemetry-diagnostics-and-observability` dans le contrat d'inventaire process-version-3 actuel.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                        | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Santé et Réparation](health-status-probes.md)                   | ✅  | `Stable (80%)` | `Beta (76%)`   | `Stable (80%)` | Boucle de surveillance de santé en arrière-plan, Paramètres d'activation/désactivation par compte, Délai de démarrage, Journalisation des redémarrages, openclaw doctor, Vérifications de santé structurées, Vérifications doctor principales, Contrats doctor/health du SDK Plugin, openclaw status, openclaw health, Santé RPC Gateway, Snapshots de santé en cache                                                   |
| [Journalisation](logging-log-tail-and-redaction.md)              | ✅  | `Stable (82%)` | `Stable (84%)` | `Stable (82%)` | Journaux de fichiers JSONL Gateway roulants, openclaw logs, Journaux RPC Gateway.tail, Modèles de rédaction et récepteurs, Champs de corrélation de trace                                                                                                                                                                                                                                                       |
| [Collecte Diagnostique](diagnostics-export-support-bundles.md)   | ❌  | `Beta (76%)`   | `Beta (74%)`   | `Beta (76%)`   | Exportation de diagnostiques openclaw gateway, openclaw gateway stability --bundle, Chat /diagnostics, Composition du zip de support, Enregistreur de stabilité en processus limité, openclaw gateway stability, Événements de pression mémoire, Option de snapshot de pression mémoire critique                                                                                                                   |
| [Exportation de Télémétrie](diagnostic-events-hooks-and-trace-context.md) | ❌  | `Beta (78%)`   | `Beta (78%)`   | `Beta (78%)`   | Types d'événements diagnostiques, Dispatch asynchrone, Création de contexte de trace W3C, Exportations de runtime diagnostiques du SDK Plugin, Événements diagnostiques d'appel de modèle, Installation du plugin diagnostics-otel, Traces OTLP/HTTP, Contexte de trace approuvé, Télémétrie de modèle et runtime, Installation du plugin diagnostics-prometheus, GET /api/diagnostics/prometheus authentifié par Gateway, Exposition de texte Prometheus, Abonnement à événement diagnostique approuvé |
| [Diagnostiques de Session](session-run-and-usage-diagnostics.md) | ✅  | `Stable (82%)` | `Beta (78%)`   | `Stable (82%)` | session.state, Snapshots d'activité de session diagnostique, Utilisation du modèle, Exportation des signaux de session vers la stabilité                                                                                                                                                                                                                                                                        |

## Rubrique de notation

- Couverture :
  évaluation maturity-label pour l'intégration, e2e, live, ou les preuves de flux
  serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation maturity-label pour la robustesse de l'implémentation et opérationnelle. La couverture des tests
  unitaires, d'intégration, e2e, live et de flux runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  évaluation maturity-label pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Santé et Réparation

Ancres de recherche : moniteur de santé des canaux, délais de redémarrage, activité de transport obsolète, openclaw doctor --fix, vérifications de santé structurées, résultats de réparation, openclaw health --json, santé RPC de la passerelle, snapshots de santé en cache.

Note de catégorie : [Santé et Réparation](health-status-probes.md)

Décisions de score :

- Couverture : `Stable (80%)`
- Qualité : `Beta (76%)`
- Complétude : `Stable (80%)`
- LTS : ✅

Fonctionnalités :

- Boucle de moniteur de santé en arrière-plan : Boucle de moniteur de santé en arrière-plan pour les comptes de canaux configurés
- Paramètres d'activation/désactivation par compte : Comportement des paramètres d'activation/désactivation par compte, statut et vérification visible par l'opérateur.
- Délai de démarrage : Délai de démarrage, délai de connexion, détection d'activité de transport obsolète, gestion des états occupé/bloqué, délais de redémarrage et redémarrages maximum par heure
- Journalisation des redémarrages : Journalisation des redémarrages et évaluation des snapshots d'exécution
- openclaw doctor : openclaw doctor, openclaw doctor --fix, --repair, --yes, --non-interactive, --deep et --lint
- Vérifications de santé structurées : Vérifications de santé structurées, résultats, résultats de réparation, sélection de vérifications, sortie JSON lint, filtrage de sévérité et comportement de sortie
- Vérifications doctor principales : Vérifications doctor principales pour la configuration de la passerelle, les services, l'authentification, l'intégrité de l'état, les compétences, les plugins, le sandbox, les migrations et la santé de la route du fournisseur
- Contrats doctor/health du SDK Plugin : Comportement des contrats doctor/health du SDK Plugin, statut et vérification visible par l'opérateur.
- openclaw status : openclaw status, openclaw status --all et openclaw status --deep
- openclaw health : openclaw health, openclaw health --verbose et openclaw health --json
- Santé RPC de la passerelle : Santé RPC de la passerelle et statut
- Snapshots de santé en cache : Snapshots de santé en cache, actualisation de sonde en direct, champs sensibles contrôlés par la portée d'administrateur opérateur et attachement de santé de la boucle d'événements

Docs principales :

- `docs/gateway/health.md`
- `docs/channels/telegram.md`
- `docs/cli/doctor.md`
- `docs/gateway/doctor.md`
- `docs/plugins/sdk-subpaths.md`
- `docs/cli/health.md`
- `docs/gateway/protocol.md`

### 2. Journalisation

Ancres de recherche : openclaw logs --follow, logs.tail, motifs de rédaction.

Note de catégorie : [Journalisation](logging-log-tail-and-redaction.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Stable (84%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Journaux de fichiers JSONL de la passerelle roulants : Journaux de fichiers JSONL de la passerelle roulants et sortie console
- openclaw logs : openclaw logs, openclaw logs --follow, modes JSON/plain/color/timezone et comportement de secours local
- Comportement RPC logs.tail de la passerelle : Comportement RPC logs.tail de la passerelle, statut et vérification visible par l'opérateur.
- Motifs et récepteurs de rédaction : console, journaux de fichiers, enregistrements de journaux OTLP, texte de transcription, événements d'appel d'outil de l'interface utilisateur de contrôle, exports de support et journaux de protocole WS
- Champs de corrélation de trace : Champs de corrélation de trace sur les enregistrements de journaux et événements de diagnostic liés.

Docs principales :

- `docs/logging.md`
- `docs/gateway/logging.md`
- `docs/cli/logs.md`

### 3. Collecte de Diagnostics

Ancres de recherche : export de diagnostics de passerelle, bundle de support, manifeste de confidentialité, stabilité de la passerelle, événements de pression mémoire, snapshot de pression mémoire critique.

Note de catégorie : [Collecte de Diagnostics](diagnostics-export-support-bundles.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- openclaw gateway diagnostics export : openclaw gateway diagnostics export et options --json / --output / log-size
- openclaw gateway stability --bundle : openclaw gateway stability --bundle latest --export
- Chat /diagnostics : Chat /diagnostics et flux d'approbation /codex diagnostics
- Composition du zip de support : Composition du zip de support, chemins relatifs sûrs, fichiers de config/statut/santé/journal/stabilité assainis et manifeste de confidentialité
- Enregistreur de stabilité borné en processus : Enregistreur de stabilité borné en processus et RPC diagnostics.stability
- openclaw gateway stability : openclaw gateway stability, filtrage de stabilité, bundles de stabilité persistés et export-from-bundle
- Événements de pression mémoire : Événements de pression mémoire, avertissements de vivacité de la boucle d'événements, événements de charge utile surdimensionnée, résumés de file d'attente/session et snapshots fatals/arrêt/redémarrage
- Option de snapshot de pression mémoire critique : Option de snapshot de pression mémoire critique avec preuves V8/cgroup/session-file

Docs principales :

- `docs/gateway/diagnostics.md`
- `docs/gateway/health.md`
- `docs/plugins/codex-harness.md`
- `docs/gateway/protocol.md`

### 4. Export de Télémétrie

Ancres de recherche : événements de diagnostic, contexte de trace W3C, champs de trace de contexte de hook, diagnostics-otel, traces OTLP/HTTP, traceparent, diagnostics-prometheus, /api/diagnostics/prometheus, exposition de texte Prometheus.

Note de catégorie : [Export de Télémétrie](diagnostic-events-hooks-and-trace-context.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (78%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Types d'événements de diagnostic : Types d'événements de diagnostic et limites d'abonnement de confiance/interne/public
- Dispatch asynchrone : Dispatch asynchrone, résumés de saturation de file d'attente, copies d'événements immuables, gestion des données privées et activation des diagnostics
- Création de contexte de trace W3C : Création de contexte de trace W3C, portées de requête actives, spans enfants et formatage de traceparent de confiance
- Exports de diagnostic du SDK Plugin : Exports de diagnostic du SDK Plugin et champs de trace de contexte de hook
- Événements de diagnostic d'appel de modèle : Événements de diagnostic d'appel de modèle, outil, exec, webhook, message, Talk, session, harness et exporter.
- Installation du plugin diagnostics-otel : Installation du plugin diagnostics-otel, activation, config, remplacements env, échantillonnage, intervalle de flush et mode SDK préchargé
- Traces OTLP/HTTP : Traces, métriques et journaux OTLP/HTTP
- Contexte de trace de confiance : Contexte de trace de confiance, propagation de traceparent W3C aux appels de modèle, corrélation de journal de fichier, contrôles de capture de contenu et attributs réduits/bornés
- Télémétrie de modèle et d'exécution : Signaux de modèle, outil, message, session, file d'attente, Talk, exec, webhook, assemblage de contexte, harness et santé d'exporter
- Installation du plugin diagnostics-prometheus : Installation du plugin diagnostics-prometheus et activation
- Comportement GET /api/diagnostics/prometheus authentifié par passerelle : Comportement GET /api/diagnostics/prometheus authentifié par passerelle, statut et vérification visible par l'opérateur.
- Exposition de texte Prometheus : Exposition de texte Prometheus, compteurs, jauges, histogrammes, politique d'étiquette, limite de série et métrique de débordement
- Abonnement à événement de diagnostic de confiance : Abonnement à événement de diagnostic de confiance et rendu des métriques d'exécution, modèle, outil, message, Talk, file d'attente, session, vivacité, charge utile, mémoire et exporter

Docs principales :

- `docs/plugins/hooks.md`
- `docs/gateway/opentelemetry.md`
- `docs/logging.md`
- `docs/plugins/sdk-subpaths.md`
- `docs/plugins/reference/diagnostics-otel.md`
- `docs/gateway/prometheus.md`
- `docs/plugins/reference/diagnostics-prometheus.md`

### 5. Diagnostics de Session

Ancres de recherche : session.state, diagnostics d'utilisation, export de stabilité.

Note de catégorie : [Diagnostics de Session](session-run-and-usage-diagnostics.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- session.state : session.state, session.stuck, session.long_running, session.stalled, session.recovery.\* et événements de diagnostic session.turn.created
- Snapshots d'activité de session de diagnostic : Snapshots d'activité de session de diagnostic pour les exécutions intégrées, appels de modèle et appels d'outil
- Utilisation du modèle : Utilisation du modèle, token/coût, byte/timing d'appel de modèle, tentatives d'exécution et journaux d'utilisation
- Export des signaux de session vers la stabilité : Export des signaux de session vers la stabilité, OpenTelemetry et Prometheus

Docs principales :

- `docs/gateway/opentelemetry.md`
- `docs/gateway/prometheus.md`
- `docs/gateway/diagnostics.md`
- `docs/gateway/protocol.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, les docs et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/telemetry-diagnostics-and-observability/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/telemetry-diagnostics-and-observability`.
